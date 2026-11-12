"""Baut aus 40_manuskript/*.md ein EPUB und spielt es auf Wunsch auf den Kindle.

Aufruf:
    python _werkzeuge/epub_bauen.py                    # nur EPUB bauen
    python _werkzeuge/epub_bauen.py --kindle           # zusätzlich als AZW3 auf den Kindle kopieren
    python _werkzeuge/epub_bauen.py --proben --kindle  # Leseproben aus 50_stil/proben/ als eigenes Buch
"""

import argparse
import datetime
import html
import json
import os
import re
import shutil
import string
import subprocess
import sys
import uuid
import zipfile
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
AUSGABE = Path(__file__).resolve().parent / "ausgabe"

PROJEKT = json.loads((Path(__file__).resolve().parent / "projekt.json").read_text(encoding="utf-8"))
AUTOR = PROJEKT["autor"]
# Je Buch ein fester Kindle-Dateiname, damit jede neue Fassung die alte ersetzt
BUECHER = {
    "manuskript": {"quelle": WURZEL / "40_manuskript", "muster": "*.md", "titel": PROJEKT["titel"],
                   "kindle": PROJEKT["epub"]["datei"] + ".azw3", "datei": PROJEKT["epub"]["datei"]},
    "proben": {"quelle": [WURZEL / "50_stil" / "proben", WURZEL / "01_werkstatt"], "muster": "probe-*.md", "titel": "Leseproben",
               "kindle": "Buchprojekt_Leseproben.azw3", "datei": "Leseproben"},
}
COVER = WURZEL / "50_stil" / "cover" / "cover.jpg"
EBOOK_CONVERT = Path(PROJEKT["epub"]["calibre"])

CSS = """
body { font-family: serif; line-height: 1.2; margin: 0 1em; }
h1 { font-size: 1.6em; text-align: center; margin: 2em 0 1.5em; page-break-before: always; }
p { margin: 0; text-indent: 1.2em; text-align: justify; }
h1 + p, hr + p, blockquote + p, p.erster { text-indent: 0; }
hr { border: none; text-align: center; margin: 1.2em 0; }
hr:after { content: "* * *"; }
blockquote { margin: 1em 1.5em; font-style: italic; }
.cover { text-align: center; margin: 0; }
.cover img { max-width: 100%; max-height: 100%; }
.titelseite { text-align: center; margin-top: 30%; }
.titelseite h1 { page-break-before: avoid; }
.klein { font-size: 0.85em; color: #555; text-indent: 0; text-align: center; }
"""


def kopf_lesen(text):
    """Trennt YAML-Kopf und Text. Gibt (Felder, Text) zurück."""
    felder = {}
    if text.startswith("---"):
        ende = text.find("\n---", 3)
        if ende != -1:
            for zeile in text[3:ende].splitlines():
                zeile = zeile.split("#", 1)[0]
                if ":" in zeile and not zeile.startswith(" "):
                    schluessel, wert = zeile.split(":", 1)
                    felder[schluessel.strip()] = wert.strip()
            text = text[ende + 4:]
    return felder, text


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def markdown_zu_xhtml(text):
    """Wandelt das kleine Markdown der Manuskripte in XHTML um."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"[ \t]*\{\{.*?\}\}", "", text, flags=re.S)  # Anmerkungen des Autors
    teile = []
    for block in re.split(r"\n\s*\n", text.strip()):
        block = block.strip()
        if not block:
            continue
        if block == "---":
            teile.append("<hr/>")
        elif block.startswith("#"):
            kopfzeile, _, rest = block.partition("\n")
            stufe = min(len(kopfzeile) - len(kopfzeile.lstrip("#")), 3)
            teile.append(f"<h{stufe}>{inline(kopfzeile.lstrip('#').strip())}</h{stufe}>")
            if rest.strip():
                teile.append(f"<p>{inline(' '.join(rest.split()))}</p>")
        elif block.startswith(">"):
            zeilen = [z.lstrip(">").strip() for z in block.splitlines()]
            teile.append(f"<blockquote><p>{inline(' '.join(zeilen))}</p></blockquote>")
        else:
            teile.append(f"<p>{inline(' '.join(block.splitlines()))}</p>")
    return "\n".join(teile)


def xhtml_seite(titel, inhalt):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="de" xml:lang="de">
<head><meta charset="utf-8"/><title>{html.escape(titel)}</title><link rel="stylesheet" href="stil.css"/></head>
<body>
{inhalt}
</body>
</html>
"""


def kapitel_sammeln(quelle, muster):
    kapitel = []
    quellen = quelle if isinstance(quelle, (list, tuple)) else [quelle]
    for datei in sorted((d for q in quellen for d in q.glob(muster)), key=lambda d: d.name):
        felder, text = kopf_lesen(datei.read_text(encoding="utf-8"))
        if felder.get("status") == "plan":
            continue  # nur Kapitelplan, noch kein Text
        titel = (felder.get("titel") or datei.stem).strip('"')
        kapitel.append({"titel": titel, "status": felder.get("status", ""), "xhtml": markdown_zu_xhtml(text)})
    return kapitel


def epub_bauen(kapitel, ziel, titel, cover=None):
    jetzt = datetime.datetime.now()
    buch_id = f"urn:uuid:{uuid.uuid4()}"
    stand = jetzt.strftime("%d.%m.%Y, %H:%M")

    titelseite = xhtml_seite(titel, f"""<div class="titelseite">
<h1>{html.escape(titel)}</h1>
<p class="klein">{html.escape(AUTOR)}</p>
<p class="klein">Stand: {stand}</p>
</div>""")

    eintraege = "\n".join(
        f'<li><a href="kap{i:03}.xhtml">{html.escape(k["titel"])}</a>'
        + (f' <span class="klein">({html.escape(k["status"])})</span>' if k["status"] else "")
        + "</li>"
        for i, k in enumerate(kapitel, 1)
    )
    nav = xhtml_seite("Inhalt", f"""<nav epub:type="toc" id="toc"><h1>Inhalt</h1>
<ol>
{eintraege}
</ol></nav>""")

    ncx_punkte = "\n".join(
        f'<navPoint id="n{i}" playOrder="{i}"><navLabel><text>{html.escape(k["titel"])}</text></navLabel>'
        f'<content src="kap{i:03}.xhtml"/></navPoint>'
        for i, k in enumerate(kapitel, 1)
    )
    ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="{buch_id}"/></head>
<docTitle><text>{html.escape(titel)}</text></docTitle>
<navMap>
{ncx_punkte}
</navMap>
</ncx>
"""

    cover_seite = xhtml_seite(titel, '<div class="cover"><img src="cover.jpg" alt="Umschlag"/></div>') if cover else None
    manifest = [
        '<item id="stil" href="stil.css" media-type="text/css"/>',
        '<item id="titel" href="titel.xhtml" media-type="application/xhtml+xml"/>',
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
    ]
    spine = ['<itemref idref="titel"/>', '<itemref idref="nav"/>']
    if cover:
        manifest.append('<item id="cover-bild" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>')
        manifest.append('<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>')
        spine.insert(0, '<itemref idref="cover" linear="no"/>')
    for i in range(1, len(kapitel) + 1):
        manifest.append(f'<item id="kap{i:03}" href="kap{i:03}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="kap{i:03}"/>')

    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="buchid" xml:lang="de">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="buchid">{buch_id}</dc:identifier>
<dc:title>{html.escape(titel)}</dc:title>
<dc:creator>{html.escape(AUTOR)}</dc:creator>
<dc:language>de</dc:language>
{'<meta name="cover" content="cover-bild"/>' if cover else ''}
<meta property="dcterms:modified">{datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}</meta>
</metadata>
<manifest>
{chr(10).join(manifest)}
</manifest>
<spine toc="ncx">
{chr(10).join(spine)}
</spine>
</package>
"""

    container = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
"""

    ziel.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ziel, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/toc.ncx", ncx, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/stil.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        if cover:
            z.writestr("OEBPS/cover.jpg", Path(cover).read_bytes(), compress_type=zipfile.ZIP_STORED)
            z.writestr("OEBPS/cover.xhtml", cover_seite, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/titel.xhtml", titelseite, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
        for i, k in enumerate(kapitel, 1):
            z.writestr(f"OEBPS/kap{i:03}.xhtml", xhtml_seite(k["titel"], k["xhtml"]), compress_type=zipfile.ZIP_DEFLATED)


def archivieren(ziel):
    """Verschiebt eine bestehende Fassung nach ausgabe/archiv und hängt das Datum ihrer Erstellung an."""
    if not ziel.exists():
        return
    archiv = AUSGABE / "archiv"
    archiv.mkdir(exist_ok=True)
    datum = datetime.datetime.fromtimestamp(ziel.stat().st_mtime)
    name = f"{ziel.stem} - {datum:%Y-%m-%d}"
    neu = archiv / f"{name}.epub"
    zaehler = 2
    while neu.exists():
        neu = archiv / f"{name} ({zaehler}).epub"
        zaehler += 1
    shutil.move(str(ziel), str(neu))


def kindle_finden():
    """Sucht das Laufwerk des per USB verbundenen Kindle."""
    for buchstabe in string.ascii_uppercase:
        wurzel = Path(f"{buchstabe}:/")
        if (wurzel / "documents").is_dir() and ((wurzel / "system").exists() or (wurzel / "audible").is_dir()):
            return wurzel
    return None


def auf_kindle(epub, kindle_dateiname):
    kindle = kindle_finden()
    if kindle is None:
        sys.exit("Kein Kindle gefunden. Ist er per USB verbunden?")
    if not EBOOK_CONVERT.exists():
        sys.exit(f"Calibre-Konverter nicht gefunden: {EBOOK_CONVERT}")
    azw3 = epub.with_suffix(".azw3")
    subprocess.run([str(EBOOK_CONVERT), str(epub), str(azw3)], check=True, capture_output=True)
    ziel = kindle / "documents" / kindle_dateiname
    shutil.copyfile(azw3, ziel)
    print(f"Auf den Kindle kopiert: {ziel}")
    vorschaubild(azw3, kindle)
    auswerfen(kindle)


def auswerfen(kindle):
    """Wirft den Kindle am Ende sicher aus (Windows). Der Laufwerksbuchstabe bleibt für den Rechner der Claude-Sitzung oft noch sichtbar."""
    if os.name != "nt":
        print("Bitte den Kindle selbst auswerfen.")
        return
    laufwerk = kindle.drive
    befehl = (f"Write-VolumeCache -DriveLetter {laufwerk[0]} -ErrorAction SilentlyContinue; "
              f"(New-Object -ComObject Shell.Application).Namespace(17).ParseName('{laufwerk}').InvokeVerb('Eject')")
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", befehl], check=True, capture_output=True, timeout=60)
        print("Kindle ausgeworfen, du kannst ihn abstecken.")
    except (subprocess.SubprocessError, OSError):
        print("Auswerfen hat nicht geklappt, bitte den Kindle selbst auswerfen.")


def vorschaubild(azw3, kindle):
    """Legt das Cover als Vorschaubild auf den Kindle, damit es in der Bibliothek erscheint."""
    meta = EBOOK_CONVERT.with_name("ebook-meta.exe")
    if not meta.exists():
        return
    cover = azw3.with_suffix(".cover.jpg")
    ausgabe = subprocess.run([str(meta), str(azw3), f"--get-cover={cover}"],
                             capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    treffer = re.search(r"mobi-asin:([0-9a-fA-F-]{36})", ausgabe)
    if not treffer or not cover.exists():
        print("Kein Cover im Buch gefunden, Vorschaubild übersprungen.")
        return
    ordner = kindle / "system" / "thumbnails"
    if not ordner.is_dir():
        cover.unlink()
        return
    name = f"thumbnail_{treffer.group(1)}_EBOK_portrait.jpg"
    for rest in ordner.glob(f"{name}.tmp*"):
        rest.unlink()
    shutil.copyfile(cover, ordner / name)
    cover.unlink()
    print(f"Vorschaubild abgelegt: {ordner / name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--kindle", action="store_true", help="zusätzlich als AZW3 auf den Kindle kopieren")
    parser.add_argument("--proben", action="store_true", help="Leseproben statt Manuskript")
    args = parser.parse_args()

    buch = BUECHER["proben" if args.proben else "manuskript"]
    kapitel = kapitel_sammeln(buch["quelle"], buch["muster"])
    if not kapitel:
        sys.exit(f"Keine Texte in {buch['quelle']} gefunden.")
    ziel = AUSGABE / f"{buch['datei']}.epub"
    archivieren(ziel)
    epub_bauen(kapitel, ziel, buch["titel"], COVER if COVER.exists() and not args.proben else None)
    print(f"EPUB gebaut ({len(kapitel)} Texte): {ziel}")

    if args.kindle:
        auf_kindle(ziel, buch["kindle"])


if __name__ == "__main__":
    main()
