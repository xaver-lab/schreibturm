"""Prüft das KI-Setup des Buchprojekts und gibt es als Vorlage nach _system/kern/ aus. Zählt und findet, urteilt nicht.

Aufruf:
    python _werkzeuge/system.py pruefen     # Skripte, Ordner, Hooks, Verweise, Längen, harte Wörter, Buchnamen im Kern
    python _werkzeuge/system.py ausgeben    # Kern ohne Buchdaten nach _system/kern/ spiegeln, danach pruefen auf der Kopie
    python _werkzeuge/system.py version     # lokale Version mit dem neuesten Release vergleichen; --holen lädt und entpackt es
    python _werkzeuge/system.py codex       # ausgeben, dann Codex-Fassung nach _system/release/ und als ZIP (Version: _system/VERSION)

Kern = alles, was bei jedem Buch gleich ist (Skills, Agenten, Vorlagen, Skripte, AGENTS.md ohne Abschnitt 0).
Buchdaten = AGENTS.md Abschnitt 0, _werkzeuge/projekt.json und alle Inhaltsordner.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "_system" / "kern"

KERN = ["AGENTS.md", ".claude/settings.json", ".agents/skills/*/*", "_agenten/*.md", "_vorlagen/*.md",
        "_werkzeuge/*.py", "_werkzeuge/LIESMICH.md", "_werkzeuge/daten/*", ".gitignore", ".gitattributes"]
ORDNER = ["00_eingang", "01_werkstatt", "10_welt", "10_welt/orte", "20_figuren", "30_struktur", "40_manuskript",
          "50_stil", "50_stil/stimmen", "_vorlagen", "_werkzeuge"]
# weiche Schwellen in Wörtern: darüber lohnt ein Blick (kürzen, teilen, hinter einen Verweis legen)
LAENGE = {"AGENTS.md": 1200, "SKILL.md": 2000, "agents": 1200, "_vorlagen": 800, "sonst": 1000,
          "schreibablauf.md": 1500}   # Ablauf des Schreibens: ausgelagerter Teil des Skills
HART = re.compile(r"\b(immer|nie|niemals|muss|müssen|Pflicht|zwingend|ausnahmslos|verboten|darf nicht|auf keinen Fall)\b")
HART_GRENZE = 6               # je 1.000 Wörter; darüber: Kandidat für den Blick „zu starr“
ENTSCHEIDUNG = re.compile(r"\bE-\d{3}\b")
ABSCHNITT_0 = re.compile(r"(## 0\. Das Buch\n)(.*?)(?=\n## )", re.S)
PLATZHALTER_0 = """
Alles, was nur zu diesem Buch gehört und jede Arbeitsweise braucht. Skills, Agenten und Vorlagen bleiben allgemein und verweisen hierher; die Skripte lesen Titel, Namen und Wortlisten aus `_werkzeuge/projekt.json`. Füllt der Skill `system` (Art „einrichten“) mit dem Autor.
- Reihe und Titel (Arbeitstitel) · Gattung und Zielgruppe · Sprache · gestartet am
- **Perspektivfiguren:** Name (`20_figuren/datei.md`), …
- **Schauplatz:** `10_welt/…` (im Ganzen); Bereiche …; Technik oder Magie …
- **Stil:** Grundton nach Vorbild …; Vorbilder je Szenenart (`50_stil/stilprofile.md`)
- **Zeit:** Wann ist Tag 1, woran erkennt man die Tageszeit?
"""
PROJEKT_LEER = {"titel": "Titel des Buchs", "autor": "Name", "epub": {"datei": "Titel - Band 01", "calibre":
                r"C:\Program Files\Calibre2\ebook-convert.exe"}, "obsidian": {"aliase": {}, "nur_genitiv": [],
                "story_extra": {}, "kurznamen": {}}, "pruefen": {"keine_varianten": []},
                "system": {"im_kern_erlaubt": [], "quelle": ""},
                "nutzer": {"erfahrung": "", "bekannt": []},
                "paket": {"immer": []}}


def offene_punkte(pfad):
    """Zahl der Punkte („- “ am Zeilenanfang); in der Werkbank nur unter „## Offen“."""
    if not pfad.exists():
        return 0
    text = pfad.read_text(encoding="utf-8")
    if "## Offen" in text:
        text = text.split("## Offen", 1)[1].split("\n## ", 1)[0]
    return sum(1 for z in text.splitlines() if z.startswith("- "))


def kern_dateien(wurzel):
    gesehen = []
    for muster in KERN:
        for p in sorted(wurzel.glob(muster)):
            if p.is_file() and "worktrees" not in p.parts and p not in gesehen:
                gesehen.append(p)
    return gesehen


def woerter(text):
    return len(re.findall(r"\w+", text))


def buchnamen(wurzel):
    """Namen aus Glossar und projekt.json: dürfen im Kern (außer Abschnitt 0 und projekt.json) nicht stehen."""
    namen = set()
    g = wurzel / "glossar.md"
    if g.exists():
        for zeile in g.read_text(encoding="utf-8").splitlines():
            zellen = [z.strip() for z in zeile.split("|")]
            if len(zellen) > 2 and zellen[1] and zellen[1] not in ("Begriff",) and not zellen[1].startswith("-"):
                namen.add(re.sub(r"\s*\(.*?\)", "", zellen[1]).strip())
    pj = wurzel / "_werkzeuge" / "projekt.json"
    if pj.exists():
        p = json.loads(pj.read_text(encoding="utf-8"))
        o = p.get("obsidian", {})
        namen |= set(o.get("aliase", {})) | set(o.get("story_extra", {}))
        if p.get("titel") and p["titel"] != PROJEKT_LEER["titel"]:
            namen.add(p["titel"])
        namen -= set(p.get("system", {}).get("im_kern_erlaubt", []))
    return {n for n in namen if len(n) > 2}


def pruefen(wurzel, ist_kopie=False):
    befunde = []
    def melde(art, text):
        befunde.append((art, text))

    for o in ORDNER:
        if not (wurzel / o).is_dir():
            melde("Ordner", f"fehlt: {o}/")

    for p in sorted((wurzel / "_werkzeuge").glob("*.py")):
        try:
            compile(p.read_text(encoding="utf-8"), str(p), "exec")
        except SyntaxError as e:
            melde("Skript", f"{p.name}, Z. {e.lineno}: {e.msg}")
            continue
        # Rauchtest: startet das Skript überhaupt? Nur mit argparse, damit --help nichts ausführt.
        if "argparse" in p.read_text(encoding="utf-8"):
            lauf = subprocess.run([sys.executable, str(p), "--help"], cwd=wurzel, capture_output=True,
                                  text=True, encoding="utf-8", errors="replace", timeout=60)
            if lauf.returncode != 0:
                letzte = (lauf.stderr.strip().splitlines() or ["?"])[-1]
                melde("Skript", f"{p.name} startet nicht: {letzte[:120]}")

    s = wurzel / ".claude" / "settings.json"
    if s.exists():
        for befehl in re.findall(r'"command":\s*"([^"]+)"', s.read_text(encoding="utf-8")):
            for teil in befehl.split():
                if teil.endswith((".py", ".sh", ".ps1")) and not (wurzel / teil).exists():
                    melde("Hook", f"Skript fehlt: {teil}")

    dateien = kern_dateien(wurzel)
    alle_namen = {p.name for p in wurzel.rglob("*") if "worktrees" not in p.parts and ".git" not in p.parts}
    namen = buchnamen(wurzel) if not ist_kopie else buchnamen(WURZEL)
    for p in dateien:
        if p.suffix != ".md":
            continue
        rel = p.relative_to(wurzel).as_posix()
        text = p.read_text(encoding="utf-8")
        rumpf = ABSCHNITT_0.sub(r"\1", text) if p.name == "AGENTS.md" else text

        # Verweise auf Dateien in `…`
        for ref in sorted(set(re.findall(r"`([\w./\-äöüß]+\.(?:md|py|json))`", rumpf))):
            if "<" in ref or "NN" in ref or ref.startswith(("kNN", "probe-")):
                continue
            ziel = wurzel / ref
            if not ziel.exists() and Path(ref).name not in alle_namen and not ist_kopie:
                melde("Verweis", f"{rel}: `{ref}` gibt es nicht")

        # Länge
        art = "AGENTS.md" if p.name == "AGENTS.md" else "SKILL.md" if p.name == "SKILL.md" else \
            "agents" if "_agenten" in p.parts else "_vorlagen" if "_vorlagen" in p.parts else "sonst"
        w = woerter(text)
        grenze = LAENGE.get(p.name, LAENGE[art])
        if w > grenze:
            melde("Länge", f"{rel}: {w} Wörter (Richtwert {grenze})")

        # harte Wörter
        ohne_zitat = re.sub(r"„[^“]*“|`[^`]*`", "", rumpf)   # zitierte Suchwörter zählen nicht
        harte = HART.findall(ohne_zitat)
        if w > 300 and len(harte) * 1000 / w > HART_GRENZE:
            zeilen = [str(i) for i, z in enumerate(ohne_zitat.splitlines(), 1) if HART.search(z)][:8]
            melde("Hart", f"{rel}: {len(harte)} harte Wörter auf {w} (Z. {', '.join(zeilen)} …)")

        # Buchnamen im Kern
        treffer = sorted({n for n in namen if re.search(rf"(?<![\w-]){re.escape(n)}(?![\w-])", rumpf)})
        if treffer:
            melde("Buchname", f"{rel}: {', '.join(treffer)}")

        if ist_kopie and ENTSCHEIDUNG.search(rumpf):
            melde("Entscheidung", f"{rel}: noch {len(ENTSCHEIDUNG.findall(rumpf))} Verweise auf E-Nummern")

    for datei, wort in (("hinweise.md", "Hinweise"), ("werkbank.md", "Vorhaben")):
        n = offene_punkte(wurzel / "_system" / datei)
        if n:
            melde("Offen", f"{n} {wort} in _system/{datei}")

    if not befunde:
        print("System gesund.")
    for art in dict.fromkeys(a for a, _ in befunde):
        print(f"\n{art}:")
        for a, t in befunde:
            if a == art:
                print(f"- {t}")
    return befunde


def ohne_entscheidungen(text):
    """E-Nummern verweisen beim Empfänger ins Leere: in Klammern streichen, in Aufzählungen kürzen."""
    text = re.sub(r"\s?\(E-\d{3}(?:, E-\d{3})*\)", "", text)
    text = re.sub(r"\(E-\d{3}(?:, E-\d{3})*, ", "(", text)
    text = re.sub(r",? E-\d{3}(?=[),;])", "", text)
    return text


def ausgeben():
    ZIEL.mkdir(parents=True, exist_ok=True)
    for alt in ZIEL.iterdir():   # Inhalt leeren, den Ordner selbst stehen lassen (kann offen sein)
        shutil.rmtree(alt) if alt.is_dir() else alt.unlink()
    for p in kern_dateien(WURZEL):
        rel = p.relative_to(WURZEL)
        ziel = ZIEL / rel
        ziel.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix == ".md":
            text = p.read_text(encoding="utf-8")
            if p.name == "AGENTS.md":
                text = ABSCHNITT_0.sub(lambda m: m.group(1) + PLATZHALTER_0, text)
            ziel.write_text(ohne_entscheidungen(text), encoding="utf-8")
        else:
            shutil.copy2(p, ziel)
    (ZIEL / "_werkzeuge" / "projekt.json").write_text(json.dumps(PROJEKT_LEER, ensure_ascii=False, indent=2) + "\n",
                                                      encoding="utf-8")
    for datei in ("hinweise.md", "werkbank.md"):   # leer mitgeben: nur Kopf und Überschriften, ohne unsere Punkte
        quelle = WURZEL / "_system" / datei
        if quelle.exists():
            kopf = [z for z in quelle.read_text(encoding="utf-8").splitlines() if not z.startswith(("- ", "  "))]
            (ZIEL / "_system").mkdir(parents=True, exist_ok=True)
            (ZIEL / "_system" / datei).write_text("\n".join(kopf).rstrip() + "\n", encoding="utf-8")
    for o in ORDNER:
        (ZIEL / o).mkdir(parents=True, exist_ok=True)
        if not any((ZIEL / o).iterdir()):
            (ZIEL / o / ".gitkeep").touch()
    print(f"Kern ausgegeben: {ZIEL.relative_to(WURZEL).as_posix()}/ ({len(kern_dateien(ZIEL))} Dateien)\n")
    print("Prüfung der Kopie:")
    pruefen(ZIEL, ist_kopie=True)


def version(holen=False):
    """Vergleicht VERSION mit dem neuesten Release auf GitHub (system.quelle = besitzer/repo, öffentlich, ohne Konto)."""
    import urllib.request
    lokal = (WURZEL / "VERSION").read_text(encoding="utf-8").strip() if (WURZEL / "VERSION").exists() else "unbekannt"
    pj = json.loads((WURZEL / "_werkzeuge" / "projekt.json").read_text(encoding="utf-8"))
    quelle = pj.get("system", {}).get("quelle", "")
    print(f"Lokale Version: {lokal}")
    if not quelle:
        print("Keine Quelle eingetragen (projekt.json, system.quelle = besitzer/repo). Bitte den Link zum Repo erfragen.")
        return
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{quelle}/releases/latest",
                                     headers={"User-Agent": "buchsetup", "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            rel = json.load(r)
    except Exception as e:
        print(f"Release nicht erreichbar ({e}). Das ZIP von https://github.com/{quelle}/releases von Hand laden.")
        return
    neu = rel.get("tag_name", "").lstrip("v")
    print(f"Neueste Version: {neu}")
    def zahlen(v):
        return tuple(int(x) for x in re.findall(r"\d+", v))
    if not neu or zahlen(neu) <= zahlen(lokal):
        print("Du bist auf dem neuesten Stand.")
        return
    print("Es gibt eine neuere Version.")
    if not holen:
        return
    asset = next((a for a in rel.get("assets", []) if a["name"].endswith(".zip")), None)
    if not asset:
        print("Das Release hat kein ZIP.")
        return
    ziel = WURZEL.parent / "Buch-Setup-neu"
    ziel.mkdir(exist_ok=True)
    zip_pfad = ziel / asset["name"]
    req = urllib.request.Request(asset["browser_download_url"], headers={"User-Agent": "buchsetup"})
    with urllib.request.urlopen(req, timeout=120) as r, open(zip_pfad, "wb") as f:
        shutil.copyfileobj(r, f)
    with zipfile.ZipFile(zip_pfad) as z:
        z.extractall(ziel)
    print(f"Geladen und entpackt nach: {ziel}")


def codex():
    """Codex-Fassung des Kerns: AGENTS.md mit Kopf, Skills nach .agents/skills, Rollen nach _agenten, kein Hook.
    Ausgabe: _system/release/ (Inhalt eines eigenen Repos: README, VERSION, AENDERUNGEN, buchsetup/) und ein ZIP."""
    ausgeben()
    version = (WURZEL / "_system" / "VERSION").read_text(encoding="utf-8").strip()
    quelle = WURZEL / "_system" / "codex"
    release = WURZEL / "_system" / "release"
    paket = release / "buchsetup"
    release.mkdir(parents=True, exist_ok=True)
    for alt in release.iterdir():   # .git des Release-Repos bleibt
        if alt.name != ".git":
            shutil.rmtree(alt) if alt.is_dir() else alt.unlink()
    ersetzen = [("`_agenten/`", "`_agenten/`"), ("_agenten/", "_agenten/"),
                (".agents/skills/", ".agents/skills/"), ("AGENTS.md` (Codex startet es zu Beginn)", "AGENTS.md` (Codex startet es zu Beginn)"),
                ("AGENTS.md", "AGENTS.md")]
    code_ersetzen = [('KERN = ["AGENTS.md", ".claude/settings.json", ".agents/skills/*/*", "_agenten/*.md",',
                      'KERN = ["AGENTS.md", ".agents/skills/*/*", "_agenten/*.md",'),
                     ('"_agenten" in p.parts', '"_agenten" in p.parts'), ('".agents", "_agenten", "ausgabe"', '".agents", "_agenten", "ausgabe"')]
    for p in kern_dateien(ZIEL):
        rel = p.relative_to(ZIEL)
        if rel.as_posix() == ".claude/settings.json":
            continue
        teile = rel.parts
        if teile[:2] == (".claude", "skills"):
            rel = Path(".agents", "skills", *teile[2:])
        elif teile[:2] == (".claude", "agents"):
            rel = Path("_agenten", *teile[2:])
        elif p.name == "AGENTS.md":
            rel = Path("AGENTS.md")
        ziel = paket / rel
        ziel.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix in (".md", ".py", ".json"):
            text = p.read_text(encoding="utf-8")
            if rel.parts[0] == "_agenten":   # Frontmatter (Modell, Werkzeuge) gilt nur für Claude Code
                kopf = re.match(r"---\n(.*?)\n---\n", text, flags=re.S)
                if kopf:
                    beschr = next((z[13:] for z in kopf.group(1).splitlines() if z.startswith("description: ")), "")
                    text = f"# Rolle: {p.stem}\n\n{beschr}\n" + text[kopf.end():]
            for alt, neu_ in ersetzen:
                text = text.replace(alt, neu_)
            if rel.as_posix() == "_werkzeuge/system.py":
                for alt, neu_ in code_ersetzen:
                    text = text.replace(alt, neu_)
            if rel.as_posix() == "_werkzeuge/pruefen.py":
                text = text.replace('".agents", "_agenten", "ausgabe"', '".agents", "_agenten", "ausgabe"')
            if rel.as_posix() == "AGENTS.md":
                text = (quelle / "AGENTS-kopf.md").read_text(encoding="utf-8") + text
            ziel.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(p, ziel)
    for o in ORDNER:   # leere Inhaltsordner (kommen aus ausgeben(), .gitkeep inklusive)
        (paket / o).mkdir(parents=True, exist_ok=True)
        if not any((paket / o).iterdir()):
            (paket / o / ".gitkeep").touch()
    for extra in ("_werkzeuge/projekt.json", "_system/hinweise.md", "_system/werkbank.md"):   # Buchseite des Kerns
        (paket / extra).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ZIEL / extra, paket / extra)
    qdatei = quelle / "quelle.txt"
    if qdatei.exists():
        pfad = paket / "_werkzeuge" / "projekt.json"
        pdat = json.loads(pfad.read_text(encoding="utf-8"))
        pdat["system"]["quelle"] = qdatei.read_text(encoding="utf-8").strip()
        pfad.write_text(json.dumps(pdat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(quelle / "LIES_MICH_ZUERST.md", paket / "LIES_MICH_ZUERST.md")
    (paket / "VERSION").write_text(version + "\n", encoding="utf-8")
    (release / "VERSION").write_text(version + "\n", encoding="utf-8")
    shutil.copy2(quelle / "README-repo.md", release / "README.md")
    aenderungen = WURZEL / "_system" / "AENDERUNGEN.md"
    if aenderungen.exists():
        shutil.copy2(aenderungen, release / "AENDERUNGEN.md")
    rest = [p.relative_to(paket).as_posix() for p in paket.rglob("*") if p.is_file()
            and p.suffix in (".md", ".py", ".json") and ".claude" in p.read_text(encoding="utf-8")
            and p.name != "system.py"]
    if rest:
        print("Achtung, noch .claude in:", ", ".join(rest))
    zip_pfad = WURZEL / "_system" / f"buchsetup-codex-{version}.zip"
    with zipfile.ZipFile(zip_pfad, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(paket.rglob("*")):
            if p.is_file():
                z.write(p, Path("Buch-Setup") / p.relative_to(paket))
    print(f"\nCodex-Fassung {version}: {release.relative_to(WURZEL).as_posix()}/ und {zip_pfad.relative_to(WURZEL).as_posix()} "
          f"({sum(1 for p in paket.rglob('*') if p.is_file())} Dateien)")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("befehl", choices=["pruefen", "ausgeben", "codex", "version"])
    parser.add_argument("--holen", action="store_true", help="bei version: neues Release laden und entpacken")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    {"pruefen": lambda: pruefen(WURZEL), "ausgeben": ausgeben, "codex": codex,
     "version": lambda: version(args.holen)}[args.befehl]()


if __name__ == "__main__":
    main()
