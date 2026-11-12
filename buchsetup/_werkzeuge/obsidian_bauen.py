"""Baut aus den Wissensdateien eine Obsidian-Ablage zum Ansehen (_obsidian/).

Aufruf:
    python _werkzeuge/obsidian_bauen.py
    python _werkzeuge/obsidian_bauen.py --grafik-neu    # eigene Graph-Einstellungen verwerfen
    python _werkzeuge/obsidian_bauen.py --ohne-animation  # Erstelldaten nicht in Erzählreihenfolge setzen
    python _werkzeuge/obsidian_bauen.py --statisch        # ohne Wachstum: alle Orte von Anfang an verlinkt

Standard: Es liegen die Orte von Beginn an als lose Punkte im Graph (ohne Verknüpfung, zu Beginn der Animation). Die
Links von Orten und Hauptpersonen zu anderen Orten werden dafür in der Ablage zu schlichtem Text; verbunden wird erst,
wenn ein Kapitel Person und Ort zusammenbringt. Fäden entstehen mit dem Kapitel, in dem sie zuerst vorkommen.

Obsidians "Animieren" im Graph spielt die Notizen nach Erstelldatum ab. Darum bekommen die Dateien Erstelldaten in
Erzählreihenfolge: erst die Hauptpersonen, dann Kapitel für Kapitel das Kapitel selbst, was darin zum ersten Mal
auftaucht (Figuren, Orte) und die Fäden, die dort angelegt werden. Erstelldaten setzen geht unter Windows und macOS.

Der Ordner _obsidian/ wird bei jedem Lauf gelöscht und neu gebaut. Die Quelldateien bleiben unverändert.
"""

import json
import re
import shutil
import sys
import time
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "_obsidian"

QUELLEN = ["10_welt", "20_figuren", "30_struktur"]
EINZELDATEIEN = ["glossar.md", "entscheidungen.md"]
KAPITEL_ORDNER = "40_manuskript"
FADEN_DATEI = "30_struktur/faeden.md"

PROJEKT = json.loads((Path(__file__).resolve().parent / "projekt.json").read_text(encoding="utf-8"))["obsidian"]
PLATZHALTER = PROJEKT["aliase"]
NUR_GENITIV = set(PROJEKT["nur_genitiv"])
SUFFIXE = {"", "s", "es", "n", "en", "e", "in", "innen"}

ARTEN_GRUPPE = {"Institution", "Familie", "Volk"}
UNGUELTIG = re.compile(r'[<>:"/\\|?*\[\]#^]')
MARKER = re.compile(r"^\[(A\?|C\?)\]\s*(.*)$")
CALLOUT_TITEL = {"A?": "Idee des Autors (A?)", "C?": "Vorschlag von Claude (C?)"}
CALLOUT_TYP = {"A?": "idee", "C?": "vorschlag"}
AUSSCHLUSS_DAVOR = {"zweite", "zweiter", "zweiten", "erste", "ersten", "erster", "dritte", "weitere", "weiteren",
                    "eine", "einer", "keine", "jede", "jeder", "andere", "anderen", "drei"}
PERSOENLICH = ["nodeSizeMultiplier",
               "lineSizeMultiplier", "textFadeMultiplier", "showArrow", "search", "scale"]
GRAPH_FILTER = "-file:Glossar -file:Entscheidungen -file:Nebenfiguren -tag:#uebersicht -tag:#welt -tag:#struktur -tag:#begriff"
ALTE_FILTER = [
    "-file:Glossar -file:Übersicht -file:Entscheidungen -file:Nebenfiguren",
    "-file:Glossar -file:Übersicht -file:Entscheidungen -file:Nebenfiguren -file:Kapitelfolge "
    "-tag:#welt -tag:#struktur -tag:#begriff",
]
STORY_EXTRA = PROJEKT["story_extra"]
ARBEITSFLAECHE = {
    "main": {"id": "a1", "type": "split", "direction": "vertical", "children": [
        {"id": "a2", "type": "tabs", "children": [
            {"id": "a3", "type": "leaf", "state": {"type": "markdown", "state": {"file": "Übersicht.md", "mode": "preview"}}}]}]},
    "left": {"id": "b1", "type": "split", "direction": "horizontal", "width": 260, "children": [
        {"id": "b2", "type": "tabs", "children": [{"id": "b3", "type": "leaf", "state": {"type": "file-explorer", "state": {}}}]}]},
    "right": {"id": "c1", "type": "split", "direction": "horizontal", "width": 340, "children": [
        {"id": "c2", "type": "tabs", "children": [
            {"id": "c3", "type": "leaf", "state": {"type": "localgraph", "state": {}}},
            {"id": "c4", "type": "leaf", "state": {"type": "backlink", "state": {}}}]}]},
    "active": "a3",
}
KURZNAMEN = PROJEKT["kurznamen"]
FUELLWOERTER = {"am", "an", "im", "in", "mit", "der", "die", "das", "und", "zum", "zur", "von", "auf", "bei", "den", "dem", "des"}
VORIGE_GRAFIK = {}
VORIGE_ARBEIT = {}
LISTE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")

FARBEN = {"hauptperson": 0xE5484D, "figur": 0xE0894B, "ort": 0x4BA3C7, "kapitel": 0x7BC27B, "faden": 0xC76BC0, "gruppe": 0xD9C24A}
CSS_IDEE = """.callout[data-callout="idee"] {
  --callout-color: 217, 160, 40;
  --callout-icon: lucide-lightbulb;
}
.callout[data-callout="vorschlag"] {
  --callout-color: 90, 150, 220;
  --callout-icon: lucide-sparkles;
}
"""


def sicher(name):
    name = UNGUELTIG.sub("", name.replace(":", " –"))
    return re.sub(r"\s+", " ", name).strip(" .")


def kurz(text, grenze=28):
    if text in KURZNAMEN:
        return KURZNAMEN[text]
    kopf = re.split(r"[;:,(]| – ", text)[0].strip()
    if len(kopf) <= grenze:
        return kopf
    woerter = []
    for w in kopf.split():
        if len(" ".join(woerter + [w])) > grenze:
            break
        woerter.append(w)
    while len(woerter) > 1 and woerter[-1] in FUELLWOERTER:
        woerter.pop()
    return " ".join(woerter)


def kurz_titel(titel):
    kopf = titel.split(" – ")[0].strip()
    if len(kopf) > 25 and " und " in kopf:
        kopf = kopf.split(" und ")[0]
    return kopf


def beschreibung(ab, notiz):
    if "uebersicht" in notiz.tags:
        return ""
    roh = notiz.kurz
    if not roh:
        g = next((e for e in ab.glossar if sicher(ohne_klammer(e["begriff"])) == notiz.name), None)
        if g:
            roh = f"{g['herkunft']} {g['kurz']}"
    if not roh:
        for zeile in notiz.text.split("\n")[1:]:
            z = zeile.strip().lstrip("-*+ ").strip()
            if z and not z.startswith(("#", "|", "---")):
                roh = z
                break
    roh = roh.replace("`", "").replace("**", "").strip()
    if roh.startswith("[A?]"):
        roh = "Idee: " + roh[4:].strip()
    elif roh.startswith("[C?]"):
        roh = "Vorschlag: " + roh[4:].strip()
    elif roh.startswith(("[A]", "[C✓]")):
        roh = roh.split("]", 1)[1].strip()
    if len(roh) > 200:
        roh = roh[:200].rsplit(" ", 1)[0] + " …"
    return roh


def lesen(pfad):
    return pfad.read_text(encoding="utf-8").replace("\r\n", "\n")


def ohne_klammer(text):
    return re.sub(r"\s*\([^)]*\)", "", text).strip()


def ohne_artikel(text):
    return re.sub(r"^(Der|Die|Das|Zum|Zur)\s+", "", text)


def tabellenzellen(zeile):
    return [z.strip() for z in zeile.strip().strip("|").split("|")]


class Notiz:
    def __init__(self, name, ordner, tags, text="", aliase=None, quelle=None, titel=None):
        self.name = name
        self.ordner = ordner
        self.tags = tags
        self.text = text
        self.aliase = aliase or []
        self.quelle = quelle
        self.titel = titel
        self.kurz = ""
        self.stories = set()
        self.extra = {}


class Ablage:
    def __init__(self):
        self.notizen = {}
        self.pfad_zu_name = {}
        self.glossar = []
        self.kapitel = []
        self.faeden = []

    def neu(self, notiz):
        if notiz.name in self.notizen:
            notiz.name = f"{notiz.name} ({notiz.ordner})"
        self.notizen[notiz.name] = notiz
        return notiz

    def name_zu_notiz(self, text):
        schluessel = text.casefold()
        for n in self.notizen.values():
            if n.name.casefold() == schluessel or any(a.casefold() == schluessel for a in n.aliase):
                return n
        return None


def glossar_lesen(text):
    zeilen = [z for z in text.split("\n") if z.startswith("|")]
    eintraege = []
    for z in zeilen[2:]:
        zellen = tabellenzellen(z)
        if len(zellen) >= 5:
            eintraege.append(dict(zip(["begriff", "art", "kurz", "herkunft", "datei"], zellen)))
    return eintraege


def frontmatter_lesen(text):
    if not text.startswith("---\n"):
        return {}, text
    ende = text.index("\n---", 3)
    kopf, rest = text[4:ende], text[ende + 4:].lstrip("\n")
    daten, schluessel = {}, None
    for zeile in kopf.split("\n"):
        if not zeile.strip() or zeile.lstrip().startswith("#"):
            continue
        m = re.match(r"^([\wäöüÄÖÜ]+):\s*(.*)$", zeile)
        if m and not zeile.startswith(" "):
            schluessel, wert = m.group(1), re.sub(r"\s+#.*$", "", m.group(2)).strip()
            if wert in (">", "|", ""):
                daten[schluessel] = [] if wert == "" else ""
            elif wert.startswith("["):
                daten[schluessel] = [w.strip() for w in wert.strip("[]").split(",") if w.strip()]
            else:
                daten[schluessel] = wert.strip("\"'")
        elif schluessel is not None:
            inhalt = zeile.strip()
            if inhalt.startswith("-"):
                if not isinstance(daten[schluessel], list):
                    daten[schluessel] = []
                if inhalt[1:].strip():
                    daten[schluessel].append(inhalt[1:].strip())
            elif isinstance(daten[schluessel], list):
                if daten[schluessel]:
                    daten[schluessel][-1] += " " + inhalt
            else:
                daten[schluessel] = (daten[schluessel] + " " + inhalt).strip()
    return daten, rest


def quellen_sammeln(ab):
    dateien = []
    for ordner in QUELLEN:
        dateien += sorted((WURZEL / ordner).rglob("*.md"))
    dateien += [WURZEL / d for d in EINZELDATEIEN]
    glossar_text = lesen(WURZEL / "glossar.md")
    ab.glossar = glossar_lesen(glossar_text)
    nach_datei = {}
    for e in ab.glossar:
        nach_datei.setdefault(e["datei"], []).append(e)

    for datei in dateien:
        rel = datei.relative_to(WURZEL).as_posix()
        text = lesen(datei)
        h1 = re.match(r"# (.+)", text)
        titel = h1.group(1) if h1 else datei.stem
        art = {"20_figuren": "Figur", "10_welt/orte": "Ort"}
        gesuchte_art = next((a for p, a in art.items() if rel.startswith(p + "/")), None)

        if "Sammeldatei" in titel:
            index = ab.neu(Notiz(sicher(ohne_klammer(titel)), "Figuren", ["figur"], quelle=rel, titel=titel))
            ab.pfad_zu_name[rel] = index.name
            teile = re.split(r"^## (.+)$", text, flags=re.M)
            vorspann = teile[0].split("\n", 1)[1].strip()
            links = []
            for ueberschrift, inhalt in zip(teile[1::2], teile[2::2]):
                name = sicher(ohne_klammer(ueberschrift))
                alias = [ohne_artikel(name)] if ohne_artikel(name) != name else []
                n = ab.neu(Notiz(name, "Figuren", ["figur"], f"# {name}\n\n{inhalt.strip()}\n",
                                 alias, rel, ueberschrift))
                links.append(f"- [[{n.name}]]")
            index.text = f"# {ohne_klammer(titel)}\n\n{vorspann}\n\n" + "\n".join(links) + "\n"
            continue

        kandidaten = [e for e in nach_datei.get(rel, []) if e["art"] == gesuchte_art]
        if gesuchte_art and len(kandidaten) == 1:
            name = sicher(ohne_klammer(kandidaten[0]["begriff"]))
            tags = ["figur"] if gesuchte_art == "Figur" else ["ort"]
            ordner = "Figuren" if gesuchte_art == "Figur" else "Orte"
        else:
            name = sicher(kurz_titel(ohne_klammer(titel).replace("„", "").replace("“", "")))
            tags, ordner = [], "Welt"
            if rel.startswith("30_struktur"):
                tags, ordner = ["struktur"], "Struktur"
            elif rel.startswith("10_welt"):
                tags = ["welt"]
            elif rel.startswith("20_figuren"):
                tags, ordner = ["figur"], "Figuren"
            elif rel.startswith("10_welt/orte"):
                tags, ordner = ["ort"], "Orte"
            else:
                tags, ordner = [rel.split(".")[0]], ""
        if rel in EINZELDATEIEN:
            name, ordner = datei.stem.capitalize(), ""
        aliase = list(PLATZHALTER.get(name, []))
        rolle = re.search(r"^Rolle:.*$", text, re.M)
        if rolle and "Hauptperson" in rolle.group(0):
            tags = tags + ["hauptperson"]
        n = ab.neu(Notiz(name, ordner, tags, text, aliase, rel, titel))
        ab.pfad_zu_name[rel] = n.name

    for e in ab.glossar:
        if ab.name_zu_notiz(sicher(ohne_klammer(e["begriff"]))):
            continue
        name = sicher(ohne_klammer(e["begriff"]))
        art = e["art"]
        if art == "Figur":
            tags, ordner = ["figur"], "Figuren"
        elif art == "Ort":
            tags, ordner = ["ort"], "Orte"
        elif art in ARTEN_GRUPPE:
            tags, ordner = ["gruppe"], "Gruppen"
        else:
            tags, ordner = ["begriff"], "Begriffe"
        m = re.search(r"\(([^)]+)\)", e["begriff"])
        aliase = ([m.group(1)] if m else []) + PLATZHALTER.get(name, [])
        ziel = ab.pfad_zu_name.get(e["datei"])
        text = f"# {name}\n\n- {e['herkunft']} {e['kurz']}\n"
        if ziel:
            text += f"\nSiehe [[{ziel}]].\n"
        ab.neu(Notiz(name, ordner, tags, text, aliase, "glossar.md"))


def kapitel_bauen(ab):
    for datei in sorted((WURZEL / KAPITEL_ORDNER).glob("*.md")):
        daten, _ = frontmatter_lesen(lesen(datei))
        for feld in ("titel", "ziel", "perspektive", "zeit", "status", "kapitel"):
            if feld in daten and not isinstance(daten[feld], str):
                daten[feld] = " ".join(daten[feld])  # leeres Feld (z. B. ziel: ohne Wert) wird zu ""
        nummer = daten.get("kapitel", "offen")
        titel = daten.get("titel")
        if not titel or not isinstance(titel, str):
            titel = "ohne Titel"
        name = f"Kapitel {nummer} – {titel}" if nummer.isdigit() else f"Probekapitel – {titel}"
        n = ab.neu(Notiz(sicher(name), "Kapitel", ["kapitel"], aliase=[titel], quelle=f"{KAPITEL_ORDNER}/{datei.name}"))
        n.daten, n.datei = daten, datei.stem
        n.kurz = daten.get("ziel", "")
        n.extra = {"kapitel": nummer, "status": daten.get("status", "")}
        ab.kapitel.append(n)

    for n in ab.kapitel:
        d = n.daten
        zeilen = [f"# {n.name}", "", f"**Ziel:** {d.get('ziel', '–')}", "", f"**Status:** {d.get('status', '–')}", ""]
        if d.get("perspektive"):
            zeilen += [f"**Perspektive:** {d['perspektive']}", ""]
        if d.get("zusammenfassung"):
            zeilen += ["## Zusammenfassung", "", d["zusammenfassung"], ""]
        for kopf, schluessel, ordner, tag in [("Figuren", "figuren", "Figuren", "figur"), ("Orte", "orte", "Orte", "ort")]:
            eintraege = d.get(schluessel, [])
            if not eintraege:
                continue
            zeilen += [f"## {kopf}", ""]
            for eintrag in eintraege:
                ziel = ab.name_zu_notiz(eintrag) or ab.name_zu_notiz(ohne_artikel(eintrag))
                if ziel is None:
                    ziel = ab.neu(Notiz(sicher(eintrag), ordner, [tag],
                                        f"# {eintrag}\n\nNur in Kapiteln erwähnt, noch ohne eigene Wissensdatei.\n"))
                zeilen.append(f"- [[{ziel.name}]]" if ziel.name.casefold() == eintrag.casefold() else f"- [[{ziel.name}|{eintrag}]]")
            zeilen.append("")
        korrekturen = d.get("korrekturen", [])
        if korrekturen:
            zeilen += [f"> [!note]- Offene Korrekturen ({len(korrekturen)})"] + [f"> - {k}" for k in korrekturen] + [""]
        n.text = "\n".join(zeilen)


def kapitel_zu_zahlen(ab, text):
    gefunden = []
    for m in re.finditer(r"Kap\.\s*(\d+(?:\s*(?:und|,)\s*\d+)*)", text):
        for zahl in re.findall(r"\d+", m.group(1)):
            for k in ab.kapitel:
                if k.daten.get("kapitel") == zahl and k.name not in gefunden:
                    gefunden.append(k.name)
    for m in re.finditer(r"Probekapitel\s+(\w+)", text):
        wort = m.group(1).casefold()
        for k in ab.kapitel:
            if k.daten.get("kapitel") == "offen" and wort in k.datei.casefold() and k.name not in gefunden:
                gefunden.append(k.name)
    return gefunden


def faeden_bauen(ab):
    zeilen = [z for z in lesen(WURZEL / FADEN_DATEI).split("\n") if z.startswith("|")]
    figuren = [n for n in ab.notizen.values() if "figur" in n.tags and n.quelle != FADEN_DATEI]
    muster = []
    for f in figuren:
        for s in [f.name] + f.aliase:
            muster.append((s, f.name))
    muster.sort(key=lambda p: -len(p[0]))
    for z in zeilen[2:]:
        zellen = tabellenzellen(z)
        if len(zellen) < 3 or set(zellen[0]) <= set("-: "):
            continue
        faden, angelegt, stand = zellen[:3]
        name = sicher(kurz(faden))
        gesamt = f"{faden} {angelegt} {stand}"
        betrifft = []
        for s, ziel in muster:
            if re.search(rf"(?<!\w){re.escape(s)}(?:s|n|es)?(?!\w)", gesamt) and ziel not in betrifft:
                betrifft.append(ziel)
        kapitel = kapitel_zu_zahlen(ab, gesamt)
        text = [f"# {faden}", "", "## Angelegt", "", angelegt, "", "## Stand", "", stand, ""]
        if betrifft or kapitel:
            text += ["## Verknüpft", ""]
            if betrifft:
                text += ["Figuren: " + ", ".join(f"[[{b}]]" for b in betrifft), ""]
            if kapitel:
                text += ["Kapitel: " + ", ".join(f"[[{k}]]" for k in kapitel), ""]
        n = ab.neu(Notiz(name, "Fäden", ["faden"], "\n".join(text), [faden] if sicher(faden) != name else [], FADEN_DATEI))
        n.kurz = f"{faden}: " + " ".join(stand.replace("[A]", "").replace("[C✓]", "").split())
        n.betrifft, n.kapitel_namen, n.stand = betrifft, kapitel, stand
        ab.faeden.append(n)


def stories_zuordnen(ab):
    haupt = {n.name: "story-" + n.name.casefold() for n in ab.notizen.values() if "hauptperson" in n.tags}
    marken = {**haupt, **{name: tag for name, tag in STORY_EXTRA.items() if name in ab.notizen}}
    for name, tag in marken.items():
        ab.notizen[name].stories.add(tag)
    for k in ab.kapitel:
        sicht = ab.name_zu_notiz(k.daten.get("perspektive", ""))
        tag = marken.get(sicht.name) if sicht else None
        if not tag:
            continue
        k.stories.add(tag)
        for schluessel in ("figuren", "orte"):
            for eintrag in k.daten.get(schluessel, []):
                ziel = ab.name_zu_notiz(eintrag) or ab.name_zu_notiz(ohne_artikel(eintrag))
                if ziel and ziel.name not in marken:
                    ziel.stories.add(tag)
    for f in ab.faeden:
        for b in f.betrifft:
            if b in marken:
                f.stories.add(marken[b])


def kapitelfolge_bauen(ab):
    zeilen = ["# Kapitelfolge", "", "| Kap. | Titel | Status | Ziel |", "|---|---|---|---|"]
    for k in ab.kapitel:
        ziel = k.daten.get("ziel", "–").replace("|", "/")
        zeilen.append(f"| {k.daten.get('kapitel', '–')} | [[{k.name}]] | {k.daten.get('status', '–')} | {ziel} |")
    ab.neu(Notiz("Kapitelfolge", "", ["uebersicht"], "\n".join(zeilen) + "\n"))


def faedentafel_bauen(ab):
    zeilen = ["# Fädentafel", "", "| Faden | Figuren | Kapitel | Stand |", "|---|---|---|---|"]
    for f in ab.faeden:
        figuren = ", ".join(f"[[{b}]]" for b in f.betrifft)
        kapitel = ", ".join(f"[[{k}]]" for k in f.kapitel_namen)
        zeilen.append(f"| [[{f.name}]] | {figuren} | {kapitel} | {f.stand.replace('|', '/')} |")
    ab.neu(Notiz("Fädentafel", "", ["uebersicht"], "\n".join(zeilen) + "\n"))


def offene_fragen_bauen(ab):
    zeilen = ["# Offene Fragen", ""]
    for n in ab.notizen.values():
        if not n.quelle or not n.quelle.endswith(".md") or n.ordner in ("Kapitel", "Fäden", "Begriffe", "Gruppen"):
            continue
        fragen, offen = [], False
        for z in n.text.split("\n"):
            if z.startswith("#"):
                offen = z.strip("# ").strip() == "Offene Fragen"
            elif offen and z.strip():
                fragen.append(z)
        if fragen:
            zeilen += [f"## [[{n.name}]]", ""] + fragen + [""]
    ab.neu(Notiz("Offene Fragen", "", ["uebersicht"], "\n".join(zeilen) + "\n"))


def uebersicht_bauen(ab):
    def liste(tag):
        return [f"- [[{n.name}]]" for n in ab.notizen.values() if tag in n.tags]

    zeilen = ["# Übersicht", "", "## Hauptpersonen", ""] + liste("hauptperson") + ["", "## Orte", ""] + liste("ort")
    zeilen += ["", "## Teil 1: Fixpunkte und Wegmarken", "", "Ganze Struktur: [[Buchstruktur]]", ""]
    struktur = lesen(WURZEL / "30_struktur/buchstruktur.md")
    teil1 = struktur.split("**Teil 1", 1)[-1].split("**Kalender", 1)[0].split("\n## ", 1)[0]
    zeilen += [z.strip() for z in teil1.split("\n") if re.match(r"^(\s+\d+\.\s|- F\d)", z)]
    zeilen += ["", "## Offene Fäden", ""] + [f"- [[{n.name}]]" for n in ab.faeden]
    zeilen += ["", "## Nachschlagen", "", "- [[Kapitelfolge]]", "- [[Fädentafel]]", "- [[Offene Fragen]]", "- [[Glossar]]", "- [[Entscheidungen]]"]
    ab.neu(Notiz("Übersicht", "", ["uebersicht"], "\n".join(zeilen) + "\n", quelle="30_struktur/buchstruktur.md"))


class Verlinker:
    def __init__(self, ab):
        self.ab = ab
        self.ziele = {}
        for n in ab.notizen.values():
            if n.quelle and set(n.tags) & {"figur", "ort", "gruppe", "begriff"} and n.quelle != FADEN_DATEI:
                for s in [n.name] + n.aliase:
                    self.ziele.setdefault(s, n.name)
        for e in ab.glossar:
            name = sicher(ohne_klammer(e["begriff"]))
            if name in ab.notizen:
                self.ziele.setdefault(name, name)
        for s in [s for s in self.ziele if ohne_artikel(s) != s and len(ohne_artikel(s)) > 3]:
            self.ziele.setdefault(ohne_artikel(s), self.ziele[s])
        schluessel = sorted(self.ziele, key=len, reverse=True)
        self.muster = re.compile(
            r"(?<!\w)(?:" + "|".join(re.escape(s) for s in schluessel) + r")(?:s|es|n|en|e|in|innen)?(?!\w)")
        self.schluessel = schluessel

    def pfad_zu_wikilink(self, pfad, aktuell):
        pfad = pfad.strip()
        kandidaten = [
            (aktuell.parent / pfad).as_posix(),
            pfad,
        ]
        for k in kandidaten:
            parts = []
            for teil in k.split("/"):
                if teil == "..":
                    if parts:
                        parts.pop()
                elif teil != ".":
                    parts.append(teil)
            norm = "/".join(parts)
            if norm in self.ab.pfad_zu_name:
                return self.ab.pfad_zu_name[norm]
        gleich = [n for p, n in self.ab.pfad_zu_name.items() if p.endswith("/" + pfad) or p == pfad]
        return gleich[0] if len(set(gleich)) == 1 else None

    def verlinken(self, text, selbst, aktuell, tabelle, gesehen):
        trenner = "\\|" if tabelle else "|"

        def ersetze(m):
            wort = m.group(0)
            for s in self.schluessel:
                if wort.startswith(s) and wort[len(s):] in SUFFIXE:
                    rest = wort[len(s):]
                    break
            else:
                return wort
            if rest and s in NUR_GENITIV and rest != "s":
                return wort
            if s in NUR_GENITIV:
                davor = m.string[:m.start()].split()
                if davor and davor[-1].casefold() in AUSSCHLUSS_DAVOR:
                    return wort
            ziel = self.ziele[s]
            if ziel in selbst or ziel in gesehen:
                return wort
            gesehen.add(ziel)
            return f"[[{ziel}]]" if wort == ziel else f"[[{ziel}{trenner}{wort}]]"

        teile = re.split(r"(`[^`]*`|\[\[[^\]]*\]\])", text)
        for i, teil in enumerate(teile):
            if i % 2:
                if teil.startswith("`"):
                    m = re.fullmatch(r"`([^`]+\.md)`", teil)
                    ziel = self.pfad_zu_wikilink(m.group(1), aktuell) if m else None
                    if ziel:
                        teile[i] = f"[[{ziel}]]"
                continue
            teil = re.sub(r"(?<![\w/\[])((?:\d\d_\w+/)+\w+\.md)\b",
                          lambda m: f"[[{self.ab.pfad_zu_name[m.group(1)]}]]" if m.group(1) in self.ab.pfad_zu_name else m.group(0),
                          teil)
            geteilt = re.split(r"(\[\[[^\]]*\]\])", teil)
            for j in range(0, len(geteilt), 2):
                geteilt[j] = self.muster.sub(ersetze, geteilt[j])
            teile[i] = "".join(geteilt)
        return "".join(teile)

    def umwandeln(self, notiz):
        selbst = {notiz.name}
        aktuell = Path(notiz.quelle) if notiz.quelle and notiz.quelle.endswith(".md") else Path("x.md")
        aus, gesehen = [], set()
        im_block = False
        callout_einzug = None
        absatz_offen = False

        def schliesse():
            nonlocal callout_einzug
            if callout_einzug is not None:
                callout_einzug = None
                if aus and aus[-1] != "":
                    aus.append("")

        for zeile in notiz.text.rstrip("\n").split("\n"):
            if zeile.strip().startswith("```"):
                im_block = not im_block
                aus.append(zeile)
                continue
            if im_block:
                aus.append(zeile)
                continue
            if not zeile.strip():
                schliesse()
                aus.append("")
                gesehen = set()
                continue
            einzug = len(zeile) - len(zeile.lstrip())
            if callout_einzug is not None and einzug > callout_einzug:
                aus.append("> " + self.verlinken(zeile[callout_einzug:], selbst, aktuell, False, gesehen))
                continue
            if re.match(r"^#{1,6}\s", zeile):
                schliesse()
                aus.append(zeile)
                gesehen = set()
                continue
            if zeile.lstrip().startswith("|"):
                schliesse()
                aus.append(self.verlinken(zeile, selbst, aktuell, True, set()))
                continue
            schliesse()
            b = LISTE.match(zeile)
            inhalt = b.group(3) if b else zeile.strip()
            m = MARKER.match(inhalt)
            if b:
                gesehen = set()
            if m:
                gesehen = set()
                if aus and aus[-1] != "":
                    aus.append("")
                aus.append(f"> [!{CALLOUT_TYP[m.group(1)]}] {CALLOUT_TITEL[m.group(1)]}")
                aus.append("> " + self.verlinken(m.group(2), selbst, aktuell, False, gesehen))
                callout_einzug = einzug
                continue
            aus.append(self.verlinken(zeile, selbst, aktuell, False, gesehen))
        schliesse()
        return "\n".join(aus).rstrip("\n") + "\n"


def schreiben(ab, verlinker):
    ZIEL.mkdir()
    for n in ab.notizen.values():
        kurztext = beschreibung(ab, n)
        if kurztext:
            ueberschrift, _, rest = n.text.partition("\n")
            n.text = f"{ueberschrift}\n\n**Kurz:** {kurztext}\n{rest}"
        kopf = ["---", f"tags: [{', '.join(n.tags + sorted(n.stories))}]"]
        if kurztext:
            kopf.append("beschreibung: " + json.dumps(kurztext, ensure_ascii=False))
        for schluessel, wert in n.extra.items():
            kopf.append(f"{schluessel}: {wert}")
        if n.aliase:
            kopf.append("aliases: [" + ", ".join(json.dumps(a, ensure_ascii=False) for a in n.aliase) + "]")
        if n.quelle:
            kopf.append(f"quelle: {n.quelle}")
        kopf.append("---\n")
        ordner = ZIEL / n.ordner
        ordner.mkdir(exist_ok=True)
        inhalt = verlinker.umwandeln(n)
        if WACHSEN:
            inhalt = ortslinks_loesen(ab, n, inhalt)
        (ordner / f"{n.name}.md").write_text("\n".join(kopf) + inhalt, encoding="utf-8", newline="\n")

    config = ZIEL / ".obsidian"
    config.mkdir()
    gruppen = [{"query": f"tag:#{tag}", "color": {"a": 1, "rgb": rgb}} for tag, rgb in FARBEN.items()]
    graph = {
        "collapse-filter": False, "search": GRAPH_FILTER, "showTags": False, "showAttachments": False,
        "hideUnresolved": False, "showOrphans": True, "collapse-color-groups": False,
        "colorGroups": gruppen, "collapse-display": False, "showArrow": False,
        "textFadeMultiplier": 0, "nodeSizeMultiplier": 1.2, "lineSizeMultiplier": 1,
        "collapse-forces": False, "centerStrength": 0.6, "repelStrength": 14, "linkStrength": 1,
        "linkDistance": 140, "scale": 1, "close": False,
    }
    if "--grafik-neu" not in sys.argv:
        graph.update({k: v for k, v in VORIGE_GRAFIK.items()
                      if k in PERSOENLICH and not (k == "search" and v in ALTE_FILTER)})
    (config / "graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    arbeit = VORIGE_ARBEIT if VORIGE_ARBEIT and "--grafik-neu" not in sys.argv else ARBEITSFLAECHE
    (config / "workspace.json").write_text(json.dumps(arbeit, ensure_ascii=False, indent=2), encoding="utf-8")
    (config / "appearance.json").write_text(json.dumps({"enabledCssSnippets": ["idee"]}), encoding="utf-8")
    (config / "snippets").mkdir()
    (config / "snippets" / "idee.css").write_text(CSS_IDEE, encoding="utf-8", newline="\n")


WACHSEN = "--statisch" not in sys.argv
TEMPO = int(sys.argv[sys.argv.index("--tempo") + 1]) if "--tempo" in sys.argv else 10
WIKILINK = re.compile(r"\[\[([^\]|\\#]+)(?:[|\\]+([^\]]*))?\]\]")


def ortslinks_loesen(ab, notiz, text):
    """Im Wachsen-Modus bleibt ein Gerüst: Kapitel verbinden ihre Figuren, Orte und Fäden, Fäden Kapitel, Hauptpersonen und eine Figur, alle übrigen nur die Hauptpersonen."""
    arten = {"hauptperson", "figur", "ort", "gruppe", "kapitel", "faden"}
    art = {n.name.casefold(): (set(n.tags) & arten) for n in ab.notizen.values()}
    if "kapitel" in notiz.tags:
        eigene = set()
        for schluessel in ("figuren", "orte"):
            for eintrag in notiz.daten.get(schluessel, []):
                z = ab.name_zu_notiz(eintrag) or ab.name_zu_notiz(ohne_artikel(eintrag))
                if z is not None:
                    eigene.add(z.name.casefold())
        erlaubt = {"hauptperson", "faden", "kapitel"}
    elif "faden" in notiz.tags:
        eigene, erlaubt = {b.casefold() for b in getattr(notiz, "betrifft", [])[:1]}, {"kapitel", "hauptperson"}
    elif set(notiz.tags) & {"hauptperson", "figur", "ort", "gruppe"}:
        eigene, erlaubt = set(), {"hauptperson"}
    else:
        return text

    def ersetze(m):
        ziel = m.group(1).strip().casefold()
        arten_ziel = art.get(ziel, set())
        if arten_ziel and not (arten_ziel & erlaubt) and ziel not in eigene:
            return (m.group(2) or m.group(1)).strip()
        return m.group(0)

    return WIKILINK.sub(ersetze, text)


def kapitel_schluessel(k):
    nummer = k.daten.get("kapitel", "offen")
    return (0, int(nummer), k.datei) if nummer.isdigit() else (1, 0, k.datei)


def erzaehlreihenfolge(ab):
    """Notizen in der Reihenfolge, in der der Leser sie kennenlernt."""
    reihe, gesehen = [], set()

    def dazu(n):
        if n is not None and n.name not in gesehen:
            gesehen.add(n.name)
            reihe.append(n)

    for n in ab.notizen.values():
        if "hauptperson" in n.tags:
            dazu(n)
    if WACHSEN:
        for n in ab.notizen.values():
            if "ort" in n.tags:
                dazu(n)
    kapitelreihe = sorted(ab.kapitel, key=kapitel_schluessel)
    erstes = {}
    for f in ab.faeden:
        namen = [k for k in kapitelreihe if k.name in f.kapitel_namen]
        if namen:
            erstes[f.name] = namen[0].name
    for k in kapitelreihe:
        dazu(k)
        for schluessel in ("figuren", "orte"):
            for eintrag in k.daten.get(schluessel, []):
                dazu(ab.name_zu_notiz(eintrag) or ab.name_zu_notiz(ohne_artikel(eintrag)))
        for f in ab.faeden:
            if erstes.get(f.name) == k.name:
                dazu(f)
    for n in ab.notizen.values():
        dazu(n)
    return reihe


def erstelldatum_setzen(pfad, zeit):
    """Setzt Erstell- und Änderungsdatum. Gibt False zurück, wo das System es nicht kann."""
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.windll.kernel32
        k32.CreateFileW.restype = wintypes.HANDLE
        k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
                                    wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        handle = k32.CreateFileW(str(pfad), 0x100, 0, None, 3, 0x80, None)  # FILE_WRITE_ATTRIBUTES
        if handle in (None, wintypes.HANDLE(-1).value):
            return False
        ft = ctypes.c_ulonglong(int((zeit + 11644473600) * 10_000_000))
        ok = k32.SetFileTime(handle, ctypes.byref(ft), None, ctypes.byref(ft))
        k32.CloseHandle(handle)
        return bool(ok)
    if sys.platform == "darwin":
        import subprocess
        text = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(zeit))
        try:
            subprocess.run(["SetFile", "-d", text, "-m", text, str(pfad)], check=True, capture_output=True)
            return True
        except (OSError, subprocess.CalledProcessError):
            return False
    return False


def kapiteltag(n):
    """Erster Tag aus dem Kapitelfeld zeit: ("Tag 16", "etwa Tag 16", "Tag 2 bis etwa Tag 8"); sonst None."""
    m = re.search(r"Tag\s+(\d+)", str(getattr(n, "daten", {}).get("zeit", "")))
    return int(m.group(1)) if m else None


def animation_vorbereiten(ab):
    """Erstelldaten in Erzählreihenfolge, eine Minute Abstand, damit Obsidians Animation die Geschichte nachzeichnet."""
    start = time.mktime((2020, 1, 1, 8, 0, 0, 0, 0, -1))
    fehler, minute, letzter_tag, im_text = 0, 0, None, False
    for n in erzaehlreihenfolge(ab):
        if "kapitel" in n.tags:
            im_text = True
            minute += 20
            tag = kapiteltag(n)
            if tag is not None:
                if letzter_tag is not None and tag > letzter_tag:
                    minute += 12 * (tag - letzter_tag)
                letzter_tag = tag
        pfad = ZIEL / n.ordner / f"{n.name}.md"
        if pfad.exists() and not erstelldatum_setzen(pfad, start + 60 * TEMPO * minute):
            fehler += 1
        minute += 5 if im_text else 1
    print("Erstelldaten nicht gesetzt (nur Windows und macOS)." if fehler else
          "Erstelldaten in Erzählreihenfolge gesetzt: im Graph „Animieren“ (Strg+R vorher).")


def pruefen(ab):
    namen = {n.name.casefold() for n in ab.notizen.values()}
    kanten, offen = {}, []
    for datei in ZIEL.rglob("*.md"):
        text = datei.read_text(encoding="utf-8")
        von = datei.stem
        for m in re.finditer(r"\[\[([^\]|\\#]+)(?:[|\\][^\]]*)?\]\]", text):
            ziel = m.group(1).strip()
            if ziel.casefold() not in namen:
                offen.append((von, ziel))
            else:
                kanten.setdefault(von, set()).add(ziel)
    tags = {}
    for n in ab.notizen.values():
        for t in n.tags:
            tags.setdefault(t, []).append(n.name)
    print(f"{len(ab.notizen)} Notizen, {sum(len(v) for v in kanten.values())} Verknüpfungen")
    for t, liste in sorted(tags.items()):
        print(f"  #{t}: {len(liste)}")
    if offen:
        print(f"Tote Links: {len(offen)}")
        for von, ziel in offen[:10]:
            print(f"  {von} -> {ziel}")
    ungebunden = [n.name for n in ab.notizen.values() if n.name not in kanten
                  and not any(n.name in z for z in kanten.values())]
    if ungebunden:
        print("Ohne Verknüpfung:", ", ".join(ungebunden))
    return not offen


def loeschen():
    if ZIEL.exists():
        arbeit = ZIEL / ".obsidian" / "workspace.json"
        if arbeit.exists():
            try:
                VORIGE_ARBEIT.update(json.loads(arbeit.read_text(encoding="utf-8")))
            except ValueError:
                pass
        alt = ZIEL / ".obsidian" / "graph.json"
        if alt.exists():
            try:
                VORIGE_GRAFIK.update(json.loads(alt.read_text(encoding="utf-8")))
            except ValueError:
                pass
        for versuch in range(3):
            try:
                shutil.rmtree(ZIEL)
                return
            except OSError:
                time.sleep(1)
        sys.exit("_obsidian/ lässt sich nicht löschen. Obsidian schließen und noch einmal starten.")


def main():
    loeschen()
    ab = Ablage()
    quellen_sammeln(ab)
    kapitel_bauen(ab)
    faeden_bauen(ab)
    stories_zuordnen(ab)
    kapitelfolge_bauen(ab)
    faedentafel_bauen(ab)
    offene_fragen_bauen(ab)
    uebersicht_bauen(ab)
    schreiben(ab, Verlinker(ab))
    if "--ohne-animation" not in sys.argv:
        animation_vorbereiten(ab)
    ok = pruefen(ab)
    print(f"Fertig: {ZIEL}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
