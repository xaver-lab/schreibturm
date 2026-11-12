"""Prüfskript für das Buchprojekt. Zählt und findet, urteilt nicht.

Aufruf:
    python _werkzeuge/pruefen.py text <datei> [--ziel 4000-6000]   # Länge, Satzbau, überladene Sätze, Echos, Floskeln
    python _werkzeuge/pruefen.py namen                             # Schreibvarianten, neue Namen, Verworfenes
    python _werkzeuge/pruefen.py wissen                            # Marker, leere Abschnitte, tote Verweise, Kleinstdateien
    python _werkzeuge/pruefen.py werkstatt                         # Alter und Größe der Entwürfe, Länge von STAND.md
    python _werkzeuge/pruefen.py gezeigt [bis-kapitel | wort,wort]  # was über die Welt schon gezeigt wurde (Feld erzaehlt:); mit Wörtern: nur dazu, und wo der Text es nennt
    python _werkzeuge/pruefen.py akte <name[,name]> [--bis N]       # alles zu einem Namen: Glossar, In Kürze, gezeigt, Szenen, Textstellen, Wissen
    python _werkzeuge/pruefen.py paket <kNN>                         # Pflichtlektüre zu einem Kapitel in eine Datei (_werkzeuge/ausgabe/paket_kNN.md)
    python _werkzeuge/pruefen.py woerter [kNN]                      # Wörter zählen: häufig, doppelt vergeben, je Sicht, Stimmung je Kapitel, ähnliche Namen
    python _werkzeuge/pruefen.py erzaehlt [--schreiben]            # Übersicht je Kapitel (Wegmarke, Fixpunkt, Sicht, Tag, Geld, Kurzfassung); --schreiben baut sie in 30_struktur/erzaehlt.md
    python _werkzeuge/pruefen.py index                             # baut 30_struktur/index.md aus den Feldern szenen:
    python _werkzeuge/pruefen.py ueberarbeiten                     # je Kapitel offene {{ }}, Kommentare, Korrekturen; bald / später
    python _werkzeuge/pruefen.py weiss <figur> [--bis N]           # was die Figur erfahren hat (szenen: „X erfährt …“)
    python _werkzeuge/pruefen.py wiederholung <kNN>                # Sätze um Glossarorte hier und in früheren Kapiteln, für einen Prüfer
    python _werkzeuge/pruefen.py szene <kNN> <sN> [--um 1]         # eine Szene ausgeben, mit Nachbarszenen
    python _werkzeuge/pruefen.py treffen <figur[,figur]>           # Szenen, in denen Figuren zusammen vorkommen; eine Figur: mit jeder anderen Sicht
    python _werkzeuge/pruefen.py zeitleiste                        # alle Szenen aller Sichten nach Tag; Tage mit mehreren Sichten markiert
    python _werkzeuge/pruefen.py vorsprung [figur]                 # was der Leser weiß und die Figur (noch) nicht
    python _werkzeuge/pruefen.py faeden                            # Fäden je Strang: lange still und ohne Auflösung
    python _werkzeuge/pruefen.py paket <kNN> --szene sN            # Paket für eine Szene (mit Nachbarn und Anmerkungen)
    python _werkzeuge/pruefen.py alles                             # namen, wissen, werkstatt
"""

import argparse
import json
import re
import statistics
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
PROJEKT = json.loads((Path(__file__).resolve().parent / "projekt.json").read_text(encoding="utf-8"))
WISSEN = ["10_welt", "20_figuren", "30_struktur"]
TEXTE = ["40_manuskript", "50_stil/proben"]
ZIEL_KAPITEL = (4000, None)   # nach oben offen; kürzer nur bei parallelen Kapiteln
ZIEL_PROBE = (300, 1000)
SCHWELLE_WOERTER = 80          # darunter: Kandidat für eine Sammeldatei
WERKSTATT_MAX = 8
WERKSTATT_TAGE = 7
STAND_MAX = 5
GROSS_DATEI = 1500             # Wissensdatei: darüber teilen oder verdichten
GROSS_KURZ = 200               # „In Kürze“
GROSS_STECKBRIEF = 900         # Kopfdaten eines fertigen Kapitels
OFFEN_FELDER = {"notizen", "korrekturen", "bericht", "dringlich", "kritik"}   # zählen nicht zum Steckbrief
# geprüfte Wörter, die nur zufällig einem Namen ähneln
KAPITEL_UEBERSCHRIFT = "## Kapitel"
KEINE_VARIANTEN = set(PROJEKT["pruefen"]["keine_varianten"])

WORT = re.compile(r"[A-Za-zÄÖÜäöüß]+")
BUCHSTABE = "A-Za-zÄÖÜäöüß"
ENDUNGEN = "(?:s|es|n|en|e|ns)?"   # Beugung: Kessel, Kessels; Turm, Turmes

STOPP = set("""
aber alle allem allen aller alles als also am an ander andere anderen anders auch auf aus bei beim bin bis bist
da dabei dafür dagegen daher damit dann daran darauf darin darum das dass dein deine dem den denn der des dessen
dich die dies diese diesem diesen dieser dieses dir doch dort du durch ein eine einem einen einer eines einmal er
es etwas euch euer für gegen gewesen hab habe haben hat hatte hatten hier hin hinter ich ihm ihn ihnen ihr ihre
ihrem ihren ihrer im in indem ins ist ja jede jedem jeden jeder jedes jetzt kann kein keine keinem keinen keiner
können konnte konnten man manche mehr mein meine mich mir mit muss musste nach nicht nichts noch nun nur ob oder
ohne schon sehr sein seine seinem seinen seiner seit selbst sich sie sind so solche soll sollte sondern um und uns
unter viel vom von vor war waren warst was weil weiter welche wenn wer werde werden wie wieder will wir wird wo
wollte würde würden zu zum zur zwar zwischen über sagte fragte dann noch einen einer immer wieder hatte stand
ging kam sah lag saß wusste
""".split())

FUELLWOERTER = ["eigentlich", "irgendwie", "plötzlich", "wirklich", "ganz", "sehr", "einfach", "gerade",
                "etwas", "schon", "beinahe", "fast", "ziemlich", "irgendwo", "irgendwann", "genau"]

GEFUEHLE = (r"Angst|Furcht|Wut|Zorn|Trauer|Freude|Erleichterung|Scham|Schuld|Panik|Hoffnung|Sehnsucht|"
            r"Unbehagen|Nervosität|Stolz|Einsamkeit|Verzweiflung|Zärtlichkeit|Ekel|Neid|Eifersucht|Mitleid")

MUSTER = {
    "nicht X, sondern Y": r"\bnicht\b[^.!?;:]{1,50},\s*sondern\b",
    "als ob / als wäre": r"\bals (?:ob|wäre|hätte|würde)\b|\bwie wenn\b",
    "benanntes Gefühl": rf"\b(?:spürte|fühlte|empfand|verspürte)\b(?:\s+\w+){{0,4}}\s+(?:{GEFUEHLE})\b"
                        rf"|\b(?:{GEFUEHLE})\b\s+(?:stieg|kroch|breitete|durchflutete|überkam|erfasste)",
    "Floskel": r"\b(?:ein Hauch von|in diesem Moment|etwas in ihr|etwas in ihm|ohne zu wissen, warum|"
               r"die Stille war|es war, als|zum ersten Mal seit|einen Herzschlag lang|für einen Moment)\b",
    "Füllgeste": r"\bzuckte\b[^.]{0,25}\bSchultern\b|\bohne hinzusehen\b"
                 r"|\batmete\b(?:\s+\w+){0,2}\s+(?:ein|aus)\b",
    "Dreierreihung": r"\b\w+, \w+ und \w+\b",
}

# Ein Satz am Absatzende sagt, was das Gezeigte bedeutet („Sie verstand, dass …“).
NACHDEUTEN = re.compile(
    r"(?<!bevor er )(?<!bevor sie )(?<!der )(?<!die )(?<!dem )\b(?:verstand|begriff|erkannte|ahnte)\b"
    r"(?:\s+(?!nicht\b|nie\b|kaum\b|noch\b)\w+){0,3},\s*(?:dass|was|warum|wie)\b"
    r"|\bwurde (?:ihr|ihm|ihnen) (?:klar|bewusst)\b|\bdas (?:hieß|bedeutete)\b|\bvielleicht war es das\b",
    re.IGNORECASE)


# ---------------------------------------------------------------- Hilfen

def lesen(pfad):
    return Path(pfad).read_text(encoding="utf-8")


def kopf_trennen(text):
    """Gibt (Kopf als Text, Rumpf, Zeilenversatz des Rumpfs) zurück."""
    if text.startswith("---"):
        ende = text.find("\n---", 3)
        if ende != -1:
            kopf = text[3:ende]
            rumpf = text[ende + 4:]
            return kopf, rumpf, text[:ende + 4].count("\n")
    return "", text, 0


def kopf_felder(kopf):
    """Einfache YAML-Lesung: Skalar oder Liste von '- '-Zeilen."""
    felder, aktuell = {}, None
    for zeile in kopf.splitlines():
        ohne = zeile.split(" #", 1)[0].rstrip()
        if not ohne.strip():
            continue
        if not zeile.startswith(" ") and ":" in ohne:
            schluessel, wert = ohne.split(":", 1)
            aktuell = schluessel.strip()
            felder[aktuell] = wert.strip() if wert.strip() else []
        elif aktuell and felder[aktuell] in (">", "|") or (aktuell and isinstance(felder[aktuell], str) and felder[aktuell].startswith(">>")):
            # Textblock (">"): Folgezeilen anhängen
            felder[aktuell] = ">>" + (felder[aktuell][2:] + " " + zeile.strip()).strip() if felder[aktuell].startswith(">>") else ">>" + zeile.strip()
        elif aktuell and ohne.strip().startswith("- "):
            if isinstance(felder[aktuell], list):
                eintrag = ohne.strip()[2:].strip()
                if eintrag:
                    felder[aktuell].append(eintrag)
    return {k: (v[2:] if isinstance(v, str) and v.startswith(">>") else v) for k, v in felder.items()}


def alle_md():
    for pfad in sorted(WURZEL.rglob("*.md")):
        if not {".git", "_obsidian", "_system", ".agents", "_agenten", "ausgabe"} & set(pfad.parts):
            yield pfad


def rel(pfad):
    return pfad.relative_to(WURZEL).as_posix()


def git(*argumente):
    try:
        return subprocess.run(["git", *argumente], cwd=WURZEL, capture_output=True, text=True,
                              encoding="utf-8").stdout
    except FileNotFoundError:
        return ""


def stamm(wort):
    w = wort.lower()
    for endung in ("ungen", "ung", "en", "er", "es", "em", "e", "n", "s"):
        if len(w) > 5 and w.endswith(endung):
            return w[: -len(endung)]
    return w


def ausgabe(titel, zeilen, leer="nichts gefunden"):
    print(f"\n## {titel}")
    if zeilen:
        for z in zeilen:
            print(f"- {z}")
    else:
        print(f"- {leer}")


# ---------------------------------------------------------------- text

def befehl_text(pfad, ziel_text=None):
    pfad = Path(pfad)
    if not pfad.is_absolute():
        pfad = WURZEL / pfad
    kopf, rumpf, versatz = kopf_trennen(lesen(pfad))
    felder = kopf_felder(kopf)
    zeilen = rumpf.splitlines()
    # Überschriften und Kommentare nicht mitzählen
    textzeilen = [(i + versatz + 1, z) for i, z in enumerate(zeilen)
                  if z.strip() and not z.lstrip().startswith(("#", "<!--", ">"))]

    woerter = [(nr, w) for nr, z in textzeilen for w in WORT.findall(z)]
    anzahl = len(woerter)
    if ziel_text:
        a, b = (int(x) for x in ziel_text.split("-"))
        hinweis = "zu kurz"
    elif "proben" in pfad.parts or pfad.name.startswith("probe-"):
        a, b = ZIEL_PROBE
        hinweis = "zu kurz"
    else:
        a, b = ZIEL_KAPITEL
        hinweis = "kurz, nur bei parallelen Kapiteln gewollt"
    print(f"# Textprüfung: {rel(pfad)}")
    print(f"Status: {felder.get('status', '?')} · Wörter: {anzahl} · Ziel: {a}–{b or ''}"
          + (f"  ← {hinweis}" if anzahl < a else "  ← zu lang" if b and anzahl > b else ""))

    # Sätze
    saetze = []
    for nr, z in textzeilen:
        for s in re.split(r"(?<=[.!?…])[\"“”»«']?\s+", z):
            n = len(WORT.findall(s))
            if n:
                saetze.append((nr, s.strip(), n))
    laengen = [n for _, _, n in saetze]
    if laengen:
        mittel = statistics.mean(laengen)
        streu = statistics.pstdev(laengen)
        kurz = sum(1 for n in laengen if n <= 4) / len(laengen)
        lang = sum(1 for n in laengen if n >= 30) / len(laengen)
        print(f"Sätze: {len(laengen)} · mittlere Länge {mittel:.1f} Wörter · Streuung {streu:.1f}"
              f" · sehr kurz (≤4) {kurz:.0%} · sehr lang (≥30) {lang:.0%}")
        if streu < 5:
            print("  ← Satzlängen sehr gleichförmig")

    # Überladene Sätze: lang oder mit vielen Einschüben (ein Satz, eine Sache)
    ueberladen = [f"Z. {nr}: {n} Wörter, {s.count(',')} Kommas: „{s[:70]}…“"
                  for nr, s, n in saetze if n >= 30 or s.count(",") >= 4]
    ausgabe(f"Überladene Sätze (≥30 Wörter oder ≥4 Kommas): {len(ueberladen)}×", ueberladen[:12])

    # Echos: Inhaltswort mindestens 3x in 40 Wörtern
    echos, gemeldet = [], set()
    inhalt = [(nr, w, stamm(w)) for nr, w in woerter if len(w) >= 4 and w.lower() not in STOPP]
    positionen = defaultdict(list)
    index = {id(t): i for i, t in enumerate(woerter)}
    pos_liste = []
    zaehler = 0
    for nr, w in woerter:
        if len(w) >= 4 and w.lower() not in STOPP:
            pos_liste.append((zaehler, nr, w, stamm(w)))
        zaehler += 1
    for pos, nr, w, st in pos_liste:
        positionen[st].append((pos, nr, w))
    for st, vorkommen in positionen.items():
        for i in range(len(vorkommen) - 2):
            if vorkommen[i + 2][0] - vorkommen[i][0] <= 40:
                schluessel = (st, vorkommen[i][1])
                if not any((st, z) in gemeldet for z in range(vorkommen[i][1] - 3, vorkommen[i][1] + 1)):
                    gemeldet.add(schluessel)
                    formen = sorted({v[2] for v in vorkommen[i:i + 3]})
                    echos.append((vorkommen[i][1], f"Z. {vorkommen[i][1]}: „{'/'.join(formen)}“ 3× in 40 Wörtern"))
    ausgabe("Echos", [t for _, t in sorted(echos)])

    # Gleiche Satzanfänge
    anfaenge = []
    for i in range(len(saetze) - 2):
        w = [WORT.findall(saetze[i + k][1])[:1] for k in range(3)]
        if all(w) and w[0][0] == w[1][0] == w[2][0] and w[0][0].lower() not in ("der", "die", "das", "ein", "eine"):
            anfaenge.append(f"Z. {saetze[i][0]}: drei Sätze nacheinander mit „{w[0][0]}“")
    ausgabe("Gleiche Satzanfänge", list(dict.fromkeys(anfaenge)))

    # Füllwörter
    zaehl = Counter(w.lower() for _, w in woerter if w.lower() in FUELLWOERTER)
    pro_tausend = {w: n * 1000 / max(anzahl, 1) for w, n in zaehl.items()}
    ausgabe("Füllwörter (pro 1.000 Wörter)",
            [f"{w}: {n}× ({pro_tausend[w]:.1f})" for w, n in zaehl.most_common() if n >= 3])

    # Muster
    for name, muster in MUSTER.items():
        treffer = []
        for nr, z in textzeilen:
            for m in re.finditer(muster, z, flags=re.IGNORECASE if name != "Dreierreihung" else 0):
                treffer.append(f"Z. {nr}: …{m.group(0)[:70]}…")
        if name == "Dreierreihung":
            dichte = len(treffer) * 1000 / max(anzahl, 1)
            kopfzeile = f"{name}: {len(treffer)}× ({dichte:.1f} pro 1.000 Wörter)"
            ausgabe(kopfzeile, treffer[:8] if dichte > 3 else [], "unauffällig")
        else:
            ausgabe(f"{name}: {len(treffer)}×", treffer)

    # Nachdeuten: der letzte Satz eines Erzählabsatzes erklärt, was gezeigt wurde
    nachdeuten = []
    for nr, z in textzeilen:
        if z.startswith(("„", "\"", "»")):
            continue
        letzter = re.split(r"(?<=[.!?…])\s+", z.strip())[-1]
        m = NACHDEUTEN.search(letzter)
        if m:
            nachdeuten.append(f"Z. {nr}: …{letzter[:80]}")
    ausgabe(f"Nachdeuten am Absatzende: {len(nachdeuten)}×", nachdeuten)

    # Wiederkehrende Wendungen (4 Wörter, mind. 3x)
    folge = [w.lower() for _, w in woerter]
    vierer = Counter(tuple(folge[i:i + 4]) for i in range(len(folge) - 3))
    wendungen = [f"„{' '.join(k)}“ {n}×" for k, n in vierer.most_common(20)
                 if n >= 3 and not all(x in STOPP for x in k)]
    ausgabe("Wiederkehrende Wendungen", wendungen)

    # Absatzschlüsse
    absaetze = [z for _, z in textzeilen if not z.startswith(("„", "\"", "»"))]
    kurz_ende = [z for z in absaetze if len(WORT.findall(re.split(r"(?<=[.!?…])\s+", z.strip())[-1])) <= 4]
    if absaetze:
        anteil = len(kurz_ende) / len(absaetze)
        print(f"\n## Absatzschlüsse\n- {anteil:.0%} der Erzählabsätze enden mit einem Kurzsatz (≤4 Wörter)"
              + ("  ← gleichförmig" if anteil > 0.35 else ""))

    offene = felder.get("korrekturen", [])
    if isinstance(offene, list) and offene:
        print(f"\n## Offene Korrekturen in den Kopfdaten: {len(offene)}")


# ---------------------------------------------------------------- namen

def glossar_namen():
    namen = []
    for zeile in lesen(WURZEL / "glossar.md").splitlines():
        if zeile.startswith("|") and not zeile.startswith(("| Begriff", "|---")):
            begriff = zeile.split("|")[1].strip()
            namen += WORT.findall(begriff)
    return {n for n in namen if n[0].isupper()}


def distanz1(a, b):
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    kurz, lang = sorted((a, b), key=len)
    return any(lang[:i] + lang[i + 1:] == kurz for i in range(len(lang)))


def befehl_namen():
    namen = glossar_namen()
    texte = [p for t in TEXTE for p in sorted((WURZEL / t).glob("*.md")) if p.name != "LIESMICH.md"]
    texte += sorted((WURZEL / "01_werkstatt").glob("probe-*.md"))
    pruef = texte + [p for w in WISSEN for p in sorted((WURZEL / w).rglob("*.md"))]

    # Schreibvarianten bekannter Namen (Beugungen und gewöhnliche Wörter ausgenommen)
    klein = set()
    for p in pruef:
        klein |= {w for w in WORT.findall(lesen(p)) if w[0].islower()}
    varianten = defaultdict(set)
    for p in pruef:
        for w in set(WORT.findall(lesen(p))):
            if not w[0].isupper() or len(w) < 3 or w in namen or w in KEINE_VARIANTEN or w.lower() in klein:
                continue
            for n in namen:
                if len(n) >= 4 and distanz1(w, n) and not (w.startswith(n) or n.startswith(w)):
                    varianten[(w, n)].add(rel(p))
    ausgabe("Mögliche Schreibvarianten", [f"„{w}“ statt „{n}“? ({', '.join(sorted(d))})"
                                          for (w, n), d in sorted(varianten.items())])

    # Namenskandidaten in Texten, die nicht im Glossar stehen
    hinweis = re.compile(r"(?:hieß|heißt|namens|genannt|Herr|Frau|Meister|Meisterin|Familie|Mutter|Vater|"
                         r"Schwester|Bruder|Turm der|Haus der)\s+([A-ZÄÖÜ][a-zäöüß]+)")
    kandidaten = defaultdict(set)
    for p in texte:
        for m in hinweis.finditer(lesen(p)):
            n = m.group(1)
            if n not in namen and n.lower() not in STOPP:
                kandidaten[n].add(rel(p))
    ausgabe("Namen in Texten, die nicht im Glossar stehen",
            [f"{n} ({', '.join(sorted(d))})" for n, d in sorted(kandidaten.items())])

    # Bewusst verworfene Begriffe
    entsch = lesen(WURZEL / "entscheidungen.md")
    teil = entsch.split("## Bewusst verworfen", 1)[-1]
    begriffe = set(re.findall(r"„([^“]+)“", teil))
    funde = []
    for p in alle_md():
        if p.name in ("entscheidungen.md",):
            continue
        inhalt = lesen(p)
        for b in begriffe:
            if b in inhalt:
                funde.append(f"„{b}“ in {rel(p)}")
    ausgabe("Verworfene Begriffe, die noch auftauchen", funde)


# ---------------------------------------------------------------- wissen

MARKER = re.compile(r"\[(A|A\?|C✓|C\?)\]")
VERMERK = re.compile(r"\((?:Kapitel|K) ?\d+[^)]*\)")


def befehl_wissen():
    falsch, leer, klein = [], [], []
    for w in WISSEN:
        for p in sorted((WURZEL / w).rglob("*.md")):
            abschnitt = None
            zeilen = lesen(p).splitlines()
            for i, z in enumerate(zeilen, 1):
                if z.startswith("## "):
                    abschnitt = z[3:].strip().lower()
                    # leerer Abschnitt: nächste nichtleere Zeile ist wieder eine ## Überschrift oder Dateiende
                    rest = [x for x in zeilen[i:] if x.strip()]
                    if not rest or rest[0].startswith("## "):
                        leer.append(f"{rel(p)} Z. {i}: „{z[3:].strip()}“ ist leer")
                    continue
                for m in MARKER.finditer(z):
                    mk = m.group(1)
                    if abschnitt and abschnitt.startswith("kanon") and mk in ("A?", "C?"):
                        falsch.append(f"{rel(p)} Z. {i}: [{mk}] steht unter Kanon")
                    if abschnitt and abschnitt.startswith("ideen") and mk in ("A", "C✓"):
                        falsch.append(f"{rel(p)} Z. {i}: [{mk}] steht unter Ideen")
            woerter = len(WORT.findall(lesen(p)))
            if p.parent.name in ("20_figuren", "orte") and woerter < SCHWELLE_WOERTER:
                klein.append(f"{rel(p)}: {woerter} Wörter, Kandidat für Sammeldatei")
    ausgabe("Marker im falschen Abschnitt", falsch)
    ausgabe("Leere Abschnitte", leer)
    vermerke = []
    for w in WISSEN + ["50_stil"]:
        for p in sorted((WURZEL / w).rglob("*.md")):
            for i, z in enumerate(lesen(p).splitlines(), 1):
                if VERMERK.search(z):
                    vermerke.append(f"{rel(p)} Z. {i}: Vermerk „(Kapitel N)“ (woher etwas stammt, weiß Git)")
    ausgabe("Kapitelvermerke in Wissensdateien", vermerke)

    # tote Verweise
    alle = {rel(p) for p in alle_md()} | {rel(p) for p in WURZEL.rglob("*") if p.is_file() and ".git" not in p.parts}
    namen_index = defaultdict(list)
    for a in alle:
        namen_index[a.rsplit("/", 1)[-1]].append(a)
    tot = []
    for p in alle_md():
        for m in re.finditer(r"`([^`\s]+\.(?:md|py))`", lesen(p)):
            ziel = m.group(1)
            if any(x in ziel for x in ("NN", "kurztitel", "variante", "<")):
                continue
            kandidat = (p.parent / ziel).resolve()
            if ziel in alle or (kandidat.exists() and WURZEL in kandidat.parents):
                continue
            if "/" not in ziel and namen_index.get(ziel):
                continue
            tot.append(f"{rel(p)}: `{ziel}`")
    ausgabe("Verweise auf Dateien, die es nicht gibt", sorted(set(tot)))
    ausgabe(f"Kleinstdateien (unter {SCHWELLE_WOERTER} Wörtern)", klein)

    gross = []
    for w in WISSEN:
        for p in sorted((WURZEL / w).rglob("*.md")):
            text = lesen(p)
            n = len(WORT.findall(text))
            if n > GROSS_DATEI and p.name not in ("index.md", "erzaehlt.md"):
                gross.append(f"{rel(p)}: {n} Wörter (über {GROSS_DATEI}): teilen oder verdichten")
            if "## In Kürze" in text:
                kurz = text.split("## In Kürze", 1)[1].split("\n## ", 1)[0]
                k = len(WORT.findall(kurz))
                if k > GROSS_KURZ:
                    gross.append(f"{rel(p)}: „In Kürze“ {k} Wörter (über {GROSS_KURZ})")
    for p, nr, felder, text in kapitel_koepfe():
        kopf = kopf_trennen(text)[0]
        k = len(WORT.findall(kopf_ohne(kopf, OFFEN_FELDER)))   # was offen ist, fällt später ohnehin weg
        if k > GROSS_STECKBRIEF:
            gross.append(f"{rel(p)}: Steckbrief {k} Wörter ohne offene Felder (über {GROSS_STECKBRIEF}); "
                         "`zusammenfassung:`, `erzaehlt:`, `szenen:` verdichten")
    ausgabe("Große Dateien (Kontext)", gross)


# ---------------------------------------------------------------- werkstatt

def befehl_werkstatt():
    jetzt = time.time()
    zeilen = []
    entwuerfe = [p for p in sorted((WURZEL / "01_werkstatt").glob("*.md")) if p.name != "LIESMICH.md"]
    for p in entwuerfe:
        stempel = git("log", "-1", "--format=%ct", "--", rel(p)).strip()
        tage = int((jetzt - int(stempel)) / 86400) if stempel else 0
        woerter = len(WORT.findall(lesen(p)))
        zeilen.append((tage, f"{p.name}: {woerter} Wörter, {tage} Tage unverändert"
                       + ("  ← alt" if tage > WERKSTATT_TAGE else "")))
    print(f"# Werkstatt: {len(entwuerfe)} Entwürfe (Deckel {WERKSTATT_MAX})"
          + ("  ← zu viele" if len(entwuerfe) > WERKSTATT_MAX else ""))
    for _, z in sorted(zeilen, reverse=True):
        print(f"- {z}")
    stand = lesen(WURZEL / "STAND.md")
    teil = stand.split("**Wartet auf den Autor**", 1)[-1].split("\n**", 1)[0]
    punkte = sum(1 for z in teil.splitlines() if z.startswith("- "))
    print(f"\nSTAND.md, „Wartet auf den Autor“: {punkte} Punkte (Deckel {STAND_MAX})"
          + ("  ← zu viele" if punkte > STAND_MAX else ""))


def kapitel_koepfe():
    """Kopfdaten aller Kapitel ohne Status plan, in der Reihenfolge der Dateien."""
    for p in sorted((WURZEL / "40_manuskript").glob("k*.md")):
        text = lesen(p)
        felder = kopf_felder(kopf_trennen(text)[0])
        if felder.get("status") == "plan":
            continue
        try:
            nr = int(str(felder.get("kapitel", "0")))
        except ValueError:
            nr = 0
        yield p, nr, felder, text


def such_muster(begriffe):
    """Ganze Wörter mit Beugungsendung: „Kessel“ trifft Kessel und Kessels, nicht Eisenkessel oder Kesselherr."""
    teile = sorted({b.strip() for b in begriffe if b.strip()}, key=len, reverse=True)
    if not teile:
        return None
    kern = "|".join(re.escape(b) for b in teile)
    return re.compile(rf"(?<![{BUCHSTABE}])(?:{kern}){ENDUNGEN}(?![{BUCHSTABE}])", re.I)


def glossar_zeilen():
    """Glossar als Liste von dict(begriff, grund, klammer, art, kurz, datei)."""
    zeilen = []
    for zeile in lesen(WURZEL / "glossar.md").splitlines():
        if not zeile.startswith("|") or zeile.startswith(("| Begriff", "|---")):
            continue
        z = [x.strip() for x in zeile.strip().strip("|").split("|")]
        if len(z) < 5:
            continue
        m = re.match(r"^(.*?)\s*\((.*)\)\s*$", z[0])
        zeilen.append({"begriff": z[0], "grund": m.group(1) if m else z[0], "klammer": m.group(2) if m else "",
                       "art": z[1], "kurz": z[2], "datei": z[-1]})
    return zeilen


def begriffe_zu(namen):
    """Ein Name und alles, was dasselbe meint: Aliase aus projekt.json, Klammer im Glossar."""
    begriffe = set(namen)
    for haupt, neben in PROJEKT.get("obsidian", {}).get("aliase", {}).items():
        gruppe = {haupt, *neben}
        if gruppe & begriffe:
            begriffe |= gruppe
    for g in glossar_zeilen():
        if g["grund"] in begriffe or g["begriff"] in begriffe:
            begriffe.add(g["grund"])
            if g["klammer"]:
                begriffe.add(g["klammer"])
    return begriffe


def treffer_zeilen(text, muster, versatz=0, hoechstens=6):
    zeilen = [i + versatz for i, z in enumerate(text.splitlines(), 1) if muster.search(z)]
    if not zeilen:
        return None
    rest = " …" if len(zeilen) > hoechstens else ""
    wort = "Zeile" if len(zeilen) == 1 else "Zeilen"
    return f"{len(zeilen)} {wort}, Z. " + ", ".join(map(str, zeilen[:hoechstens])) + rest


def in_kuerze(pfad, grenze=250):
    """Abschnitt „In Kürze“ einer Wissensdatei; fehlt er, die Datei selbst, wenn sie kurz ist."""
    text = lesen(pfad)
    m = re.search(r"^## In Kürze\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if m:
        return m.group(1).strip()
    rumpf = re.sub(r"^#.*\n", "", text, count=1).strip()
    if len(rumpf.split()) <= grenze:
        return rumpf
    anfang, zahl = [], 0
    for zeile in rumpf.splitlines():
        if zahl > 120:
            break
        anfang.append(zeile)
        zahl += len(zeile.split())
    return "\n".join(anfang) + "\n(Datei länger, hier nur der Anfang; Rest gezielt nachlesen)"


def akte_daten(namen, bis=None):
    """Sammelt zu Namen: Glossar, Dateien, schon gezeigt, Szenen, Textstellen, Erwähnungen im Wissen."""
    begriffe = begriffe_zu(namen)
    muster = such_muster(begriffe)
    d = {"begriffe": begriffe, "glossar": [], "verwandt": [], "dateien": [], "gezeigt": [], "szenen": [],
         "text": [], "wissen": []}
    if not muster:
        return d
    glossar = glossar_zeilen()
    d["glossar"] = [g for g in glossar if g["grund"] in begriffe or g["begriff"] in begriffe]
    d["verwandt"] = [g["begriff"] for g in glossar if g not in d["glossar"] and muster.search(g["kurz"])]
    for g in d["glossar"]:
        if g["datei"] not in d["dateien"] and (WURZEL / g["datei"]).exists():
            d["dateien"].append(g["datei"])

    for p, nr, felder, voll in kapitel_koepfe():
        if bis is not None and nr > bis:
            continue
        for e in felder.get("erzaehlt", []) or []:
            if muster.search(str(e)):
                d["gezeigt"].append(f"Kap. {nr}: {str(e).strip(chr(34))}")
        _, rumpf, versatz = kopf_trennen(voll)
        tz = treffer_zeilen(rumpf, muster, versatz)
        if tz:
            d["text"].append(f"Kap. {nr} ({p.name}): {tz}")

    index = WURZEL / "30_struktur" / "index.md"
    if index.exists():
        for zeile in lesen(index).splitlines():
            m = re.match(r"^\| (\d+)\.(\d+)\.(\d+) \| (?:s\d+ )?(.*) \|$", zeile)
            if not m or not muster.search(m.group(4)) or (bis is not None and int(m.group(2)) > bis):
                continue
            ort = m.group(4).split(":", 1)[0]
            dort = " [spielt dort]" if len(ort) < 40 and muster.search(ort) else ""
            d["szenen"].append((f"{m.group(1)}.{m.group(2)}.{m.group(3)}", dort, m.group(4)))

    for w in WISSEN:
        for p in sorted((WURZEL / w).rglob("*.md")):
            rel = p.relative_to(WURZEL).as_posix()
            if rel in d["dateien"] or rel.endswith(("index.md", "erzaehlt.md")):
                continue
            tz = treffer_zeilen(lesen(p), muster, hoechstens=4)
            if tz:
                d["wissen"].append(f"{rel}: {tz}")
    return d


def befehl_akte(suche, bis=None):
    """Alles zu einem Namen in einem Aufruf: Glossar, Datei, schon gezeigt, Szenen, Textstellen, Erwähnungen im Wissen."""
    namen = [w.strip() for w in suche.split(",") if w.strip()]
    d = akte_daten(namen, bis)
    print(f"# Akte: {', '.join(namen)}  (gesucht: {', '.join(sorted(d['begriffe']))})")
    ausgabe("Glossar", [f"{g['begriff']} · {g['art']} · {g['kurz']} · {g['datei']}" for g in d["glossar"]])
    if d["verwandt"]:
        print("- verwandt: " + ", ".join(d["verwandt"]))
    for datei in d["dateien"]:
        print(f"\n## In Kürze: {datei}\n{in_kuerze(WURZEL / datei)}")
    ausgabe("Schon gezeigt (erzaehlt:)", d["gezeigt"], leer="noch nichts")
    ausgabe("Szenen (Index)", [f"{k}{dort}: {z}" for k, dort, z in d["szenen"]], leer="keine")
    ausgabe("Im Kapiteltext", d["text"], leer="nirgends")
    ausgabe("Erwähnt im Wissen", d["wissen"], leer="sonst nirgends")


# ---------------------------------------------------------------- Paket für den Schreiber

PAKET_WEG = {"korrekturen", "bericht"}     # vom vorigen Kapitel nicht mitlesen


def liste_aus(wert):
    """Kopffeld als Liste: [a, b] in einer Zeile oder '- '-Zeilen."""
    if isinstance(wert, list):
        return [str(x).strip() for x in wert if str(x).strip()]
    if isinstance(wert, str) and wert.strip().startswith("["):
        return [x.strip() for x in wert.strip()[1:-1].split(",") if x.strip()]
    return [wert.strip()] if isinstance(wert, str) and wert.strip() else []


def kopf_ohne(kopf, weg):
    """Kopftext ohne die Felder in weg (ein Feld reicht bis zum nächsten Feld oben links)."""
    aus, ueberspringen = [], False
    for zeile in kopf.splitlines():
        m = re.match(r"^([a-z_]+):", zeile)
        if m:
            ueberspringen = m.group(1) in weg
        if not ueberspringen:
            aus.append(zeile)
    return "\n".join(aus).strip()


def letzte_szene(rumpf, ersatz_woerter=900):
    """Ab der letzten Marke <!-- sN --> bis zum Ende; ohne Marken die letzten Wörter."""
    marken = list(re.finditer(r"<!-- s\d+ -->", rumpf))
    if marken:
        return rumpf[marken[-1].start():].strip()
    woerter = rumpf.split(" ")
    return "(ohne Szenenmarken, nur das Ende)\n… " + " ".join(woerter[-ersatz_woerter:]).strip()


def kapitel_dateien():
    """Alle Kapitel mit Nummer, Kopf (Text), Feldern und Rumpf, auch mit Status plan."""
    for p in sorted((WURZEL / "40_manuskript").glob("k*.md")):
        kopf, rumpf, _ = kopf_trennen(lesen(p))
        felder = kopf_felder(kopf)
        try:
            nr = int(str(felder.get("kapitel", "0")))
        except ValueError:
            nr = 0
        yield p, nr, kopf, felder, rumpf


def befehl_paket(ziel, szene=None):
    """Stellt die Pflichtlektüre zu einem Kapitel in eine Datei: _werkzeuge/ausgabe/paket_kNN.md.
    Mit szene (sN): dazu die Szene mit Nachbarn und ihren Anmerkungen, für gezieltes Überarbeiten."""
    alle = list(kapitel_dateien())
    zahl = re.fullmatch(r"k?0*(\d+)", ziel.strip())
    treffer = [k for k in alle if (zahl and k[1] == int(zahl.group(1))) or k[0].name in (ziel, Path(ziel).name)]
    if not treffer:
        sys.exit(f"Kein Kapitel zu „{ziel}“ in 40_manuskript/")
    p, nr, kopf, felder, _ = treffer[0]
    sicht = str(felder.get("perspektive") or "").strip()
    teile = []

    def teil(titel, text, quelle=""):
        if text and text.strip():
            teile.append((titel, quelle, text.strip()))

    teil(f"Das Kapitel: {p.name}", kopf.strip(), p.relative_to(WURZEL).as_posix())
    if szene:
        sn = int(re.sub(r"\D", "", str(szene)) or 0)
        alle_szenen = szenen_text(treffer[0][4])
        if sn not in alle_szenen:
            sys.exit(f"{p.name}: keine Szene s{sn} (Marken <!-- sN -->)")
        stuecke = [f"### s{i}" + (" (zu überarbeiten)" if i == sn else " (Nachbarszene, nur zum Anschluss)") + "\n\n" + alle_szenen[i]
                   for i in (sn - 1, sn, sn + 1) if i in alle_szenen]
        teil(f"Szene s{sn} mit Nachbarn", "\n\n".join(stuecke), p.relative_to(WURZEL).as_posix())
        anm = re.findall(r"<!--\s*\[(?:A|C\?)\].*?-->|\{\{.*?\}\}", alle_szenen[sn], flags=re.S)
        teil(f"Anmerkungen in s{sn}", "\n".join(f"- {a.strip()}" for a in anm) or "- keine im Text; siehe `korrekturen:` im Kopf")
    erzaehlt = WURZEL / "30_struktur" / "erzaehlt.md"
    if erzaehlt.exists():
        teil("Stand und Übersicht", lesen(erzaehlt), "30_struktur/erzaehlt.md")

    frueher = [k for k in alle if k[1] < nr and k[3].get("status") != "plan"]
    vorig = frueher[-1] if frueher else None
    if vorig:
        teil(f"Voriges Kapitel {vorig[1]}: Steckbrief", kopf_ohne(vorig[2], PAKET_WEG), vorig[0].name)
        teil(f"Voriges Kapitel {vorig[1]}: letzte Szene", letzte_szene(vorig[4]), vorig[0].name)
    gleich = [k for k in frueher if str(k[3].get("perspektive") or "").strip() == sicht]
    if gleich and (not vorig or gleich[-1][0] != vorig[0]):
        k = gleich[-1]
        teil(f"Letztes Kapitel aus Sicht {sicht} ({k[1]}): eine Szene", letzte_szene(k[4]), k[0].name)

    teil("Stilprofil", lesen(WURZEL / "50_stil" / "stilprofile.md"), "50_stil/stilprofile.md")
    stimme = WURZEL / "50_stil" / "stimmen" / f"{sicht.casefold()}.md"
    if stimme.exists():
        teil(f"Stimme: {sicht}", lesen(stimme), stimme.relative_to(WURZEL).as_posix())
    proben = sorted((WURZEL / "50_stil" / "proben").glob("*.md")) if (WURZEL / "50_stil" / "proben").exists() else []
    if proben:
        teil("Freigegebene Leseproben", "\n".join(f"- {q.relative_to(WURZEL).as_posix()}" for q in proben))

    figuren = [sicht] + [x for x in liste_aus(felder.get("figuren")) if x != sicht]
    orte = liste_aus(felder.get("orte"))
    dateien = []
    for name in figuren + orte:
        for g in akte_daten([name])["glossar"]:
            if g["datei"] not in dateien and (WURZEL / g["datei"]).exists() and not g["datei"].endswith("nebenfiguren.md"):
                dateien.append(g["datei"])
    for d in PROJEKT.get("paket", {}).get("immer", []):
        if d not in dateien and (WURZEL / d).exists():
            dateien.append(d)
    for d in dateien:
        teil(f"In Kürze: {d}", in_kuerze(WURZEL / d), d)

    zeilen = []
    for name in figuren + orte:
        if name[:1].islower():   # Rolle statt Name („der Vater“): träfe jeden Vater im Buch
            zeilen.append(f"### {name}\n- Rolle ohne Namen, nicht abgeglichen; Brief und Figurendatei sagen, wer gemeint ist")
            continue
        a = akte_daten([name], bis=nr - 1)
        if not a["gezeigt"] and not a["szenen"]:
            wo = "im Glossar" if a["glossar"] else "nicht im Glossar"
            zeilen.append(f"### {name}\n- {wo}, dem Leser noch nicht erzählt")
            continue
        block = [f"### {name}"]
        block += [f"- gezeigt {z}" for z in a["gezeigt"]]
        if a["szenen"]:
            block.append("- Szenen: " + ", ".join(k + dort for k, dort, _ in a["szenen"]))
        zeilen.append("\n".join(block))
    teil("Was der Leser schon kennt (je Figur und Ort, bis zum Kapitel davor)", "\n\n".join(zeilen))

    kopfzeile = (f"# Paket für {p.name}\n\nGebaut von `pruefen.py paket`; nicht von Hand ändern. "
                 "Das ist die Lektüre vorher (Skill `schreiben`, Abschnitt 1). Alles Weitere gezielt: `pruefen.py akte <name>`.\n")
    inhalt = [kopfzeile, "## Inhalt"]
    inhalt += [f"- {titel} ({len(text.split())} Wörter)" for titel, _, text in teile]
    for titel, quelle, text in teile:
        inhalt.append(f"\n---\n\n## {titel}" + (f"  (`{quelle}`)" if quelle else "") + "\n\n" + text)
    ausgabe_ordner = WURZEL / "_werkzeuge" / "ausgabe"
    ausgabe_ordner.mkdir(exist_ok=True)
    ziel_datei = ausgabe_ordner / (f"paket_{p.stem}_s{int(re.sub(r'\D', '', str(szene)))}.md" if szene else f"paket_{p.stem}.md")
    ziel_datei.write_text("\n".join(inhalt) + "\n", encoding="utf-8")
    summe = sum(len(text.split()) for _, _, text in teile)
    print(f"Paket: {ziel_datei.relative_to(WURZEL).as_posix()} ({summe} Wörter, {len(teile)} Teile)")
    for titel, _, text in teile:
        print(f"- {titel}: {len(text.split())}")


def befehl_gezeigt(bis=None, suche=None):
    """Sammelt das Kopffeld erzaehlt: aller Kapitel (ohne Status plan), damit nichts doppelt oder widersprüchlich gezeigt wird.
    Mit Suchwörtern (durch Komma getrennt) nur die passenden Einträge, dazu die Kapitel, deren Text das Wort nennt."""
    woerter = [w.strip() for w in suche.split(",") if w.strip()] if suche else []
    muster = such_muster(begriffe_zu(woerter)) if woerter else None
    zeilen, nennungen = [], []
    for p, nr, felder, rumpf in kapitel_koepfe():
        if bis is not None and nr > bis:
            continue
        for e in felder.get("erzaehlt", []) or []:
            e = str(e).strip(chr(34))
            if not muster or muster.search(e):
                zeilen.append(f"Kap. {nr}: {e}")
        if muster:
            _, text, versatz = kopf_trennen(rumpf)   # nur der erzählte Text, ohne Steckbrief und Brief
            t = treffer_zeilen(text, muster, versatz)
            if t:
                nennungen.append(f"Kap. {nr} ({p.name}): {t}")
    ausgabe("Schon gezeigt (Kopffeld erzaehlt:)", zeilen, leer="noch nichts eingetragen")
    if woerter:
        ausgabe("Im Text genannt (dort nachlesen, wie es schon beschrieben ist)", nennungen, leer="nirgends")


def erste_saetze(text, n=2, woerter=40):
    """Ein, zwei Sätze vom Anfang: höchstens n Sätze, nach dem ersten nur, solange es unter woerter Wörtern bleibt."""
    text = " ".join(str(text).split())
    saetze = re.split(r"(?<=[.!?])\s+", text)
    aus = []
    for s in saetze[:n]:
        if aus and len(WORT.findall(" ".join(aus + [s]))) > woerter:
            break
        aus.append(s)
    return " ".join(aus).replace("|", "/")


def kurz_zelle(text, n=100):
    """Erste Klausel (bis zum Semikolon außerhalb von Klammern), auf höchstens n Zeichen gekürzt."""
    text = " ".join(str(text).split())
    tiefe, ende = 0, len(text)
    for i, z in enumerate(text):
        tiefe += (z == "(") - (z == ")")
        if z == ";" and tiefe <= 0:
            ende = i
            break
    text = text[:ende].strip()
    if len(text) > n:
        text = text[:n].rsplit(" ", 1)[0] + " …"
    return text.replace("|", "/")


def befehl_erzaehlt(schreiben=False):
    """Übersicht je Kapitel aus den Kopfdaten (Wegmarke, Fixpunkt, Sicht, Tag, Geld, Kurzfassung; Zeit und Geld gekürzt, ganz stehen sie im Steckbrief) und Hinweise zur Zeit.
    Zwischen den Figuren darf ein Kapitel früher spielen als das vorige (buchstruktur.md, Reihenfolge der Zeit)."""
    reihen, hinweise, letzter, letzter_alle = [], [], {}, None
    for p, nr, felder, _ in kapitel_koepfe():
        zeit, geld = felder.get("zeit") or "", felder.get("geld") or ""
        zeit = zeit if isinstance(zeit, str) else ""
        geld = geld if isinstance(geld, str) else ""
        kurz = felder.get("zusammenfassung") or ""
        kurz = erste_saetze(kurz) if isinstance(kurz, str) else ""
        wegmarke = felder.get("wegmarke") or ""
        wegmarke = wegmarke if isinstance(wegmarke, str) else ""
        fixpunkt = felder.get("fixpunkt") or ""
        fixpunkt = fixpunkt if isinstance(fixpunkt, str) else ""
        if not zeit:
            hinweise.append(f"Kap. {nr}: Feld zeit: fehlt")
        if not geld:
            hinweise.append(f"Kap. {nr}: Feld geld: fehlt")
        perspektive = felder.get("perspektive", "")
        sicht = perspektive if isinstance(perspektive, str) else ""
        tage = [int(t) for t in re.findall(r"Tag (\d+)", zeit)]
        if tage:
            if sicht in letzter and min(tage) < letzter[sicht]:
                hinweise.append(f"Kap. {nr} ({sicht}): Tag {min(tage)} liegt vor Tag {letzter[sicht]} im letzten Kapitel derselben Figur")
            elif letzter_alle is not None and min(tage) < letzter_alle:
                hinweise.append(f"Kap. {nr} ({sicht}): Rücksprung auf Tag {min(tage)} (erlaubt zwischen Figuren; Anker für den Leser?)")
            letzter[sicht] = max(tage)
            letzter_alle = max(tage) if letzter_alle is None else max(letzter_alle, max(tage))
        reihen.append(f"| {nr} | {wegmarke} | {fixpunkt} | {sicht} | {kurz_zelle(zeit, 90)} | {kurz_zelle(geld)} | {kurz} |")
    kopf = ["| Kap. | Wegmarke | Fixpunkt | Sicht | Zeit | Geld | Kurz |", "|---|---|---|---|---|---|---|"]
    ausgabe("Erzählt (aus den Kopfdaten)", kopf + reihen if reihen else [], leer="noch nichts eingetragen")
    ausgabe("Hinweise zur Zeit", hinweise)
    if schreiben:
        ziel = WURZEL / "30_struktur" / "erzaehlt.md"
        alt = lesen(ziel) if ziel.exists() else "# Erzählt\n\n## Stand\n\n"
        oben = alt.split(KAPITEL_UEBERSCHRIFT, 1)[0].rstrip("\n")
        ziel.write_text(oben + "\n\n" + KAPITEL_UEBERSCHRIFT + "\n\n" + "\n".join(kopf + reihen) + "\n", encoding="utf-8")
        print(f"\n(geschrieben: {rel(ziel)})")


def befehl_index():
    """Baut 30_struktur/index.md aus den Feldern szenen: (je Szene eine Zeile); Kennung Band.Kapitel.Szene."""
    zeilen, hinweise = [], []
    for p, nr, felder, text in kapitel_koepfe():
        band = str(felder.get("band", "1"))
        szenen = felder.get("szenen", []) or []
        if not szenen:
            hinweise.append(f"Kap. {nr}: Feld szenen: leer, noch nicht im Index")
            continue
        marken = len(re.findall(r"<!--\s*s\d+\s*-->", text))
        if marken != len(szenen):
            hinweise.append(f"Kap. {nr}: {len(szenen)} Zeilen in szenen:, aber {marken} Marken <!-- sN -->")
        for i, s in enumerate(szenen, 1):
            zeilen.append(f"| {band}.{nr:02d}.{i} | {str(s).strip(chr(34)).replace('|', '/')} |")
    ausgabe("Hinweise zum Index", hinweise)
    ziel = WURZEL / "30_struktur" / "index.md"
    ziel.write_text("# Szenenindex\n\nWird von `python _werkzeuge/pruefen.py index` aus den Feldern `szenen:` der Kapitel gebaut; nicht von Hand ändern. Kennung: Band.Kapitel.Szene; die Marke `<!-- sN -->` steht im Text am Anfang der Szene.\n\n"
                    + "\n".join(["| Szene | Was geschieht, Figuren, Ort, Faden, Wissen |", "|---|---|"] + zeilen) + "\n", encoding="utf-8")
    print(f"\n(geschrieben: {rel(ziel)}, {len(zeilen)} Szenen)")


# ---------------------------------------------------------------- main

# ---------------------------------------------------------------- Wörter zählen

# Stimmungswörter: kleine, allgemeine Liste als Muster auf das ganze Wort (Groß- und Kleinschreibung zählt:
# „arm“ ist das Adjektiv, „Arm“ der Körperteil)
STIMMUNG = {
    "Gefahr": r"Gefahr(en)?|gefährlich\w*|bedroh\w*|[Dd]roh\w*",
    "Angst": r"Angst|Ängste\w*|ängstlich\w*|Furcht|fürcht\w*|Panik|zitter\w*",
    "Dunkel": r"[Dd]unkel\w*|dunkl\w*|[Ff]inster\w*|Schatten\w*|schwarz\w*",
    "Gewalt": r"Blut\w*|blutig\w*|Messer\w*|Gewalt\w*|Knüppel\w*|schlug|geschlagen|töte\w*|getötet",
    "Verbrechen": r"Dieb\w*|gestohlen|stiehlt|Raub\w*|raubt\w*|betr[üo]g\w*|Verbrech\w*",
    "Armut": r"arm(e[nmrs]?)?|Armut|Hunger\w*|hungrig\w*|Elend|elend\w*|Schmutz\w*|schmutzig\w*|Dreck\w*|dreckig\w*|Lumpen",
    "Kälte": r"kalt\w*|Kälte|fr[io]er\w*|fror\w*|Eis|eisig\w*|Frost\w*",
    "Wärme": r"warm\w*|Wärme|Glut|glüh\w*|Feuer\w*",
}
STIMMUNG_RE = {feld: re.compile(rf"(?:{muster})") for feld, muster in STIMMUNG.items()}
# zu gewöhnlich für die Liste „häufig“
GEWOEHNLICH = set("""zwei drei vier fünf sechs sieben acht zehn nahm legte gesagt hätte wurde wurden blieb hielt stehen
zurück jemand sagen sagte sagt musste konnte wollte ließ machte macht kein einen einem eines etwas dass immer schon
noch selbst wieder dann wenn ihre seine ihren seinen ihrem seinem waren weiß wissen wusste gab gibt geht ging kommt
kamen sahen sehen sieht stand lagen darauf davon dabei hinter neben unter über nichts alles beide beiden einmal""".split())

HAEUFIGKEIT = Path(__file__).resolve().parent / "daten" / "de_50k.txt"


def alltagsdeutsch():
    """Häufigkeit im gewöhnlichen Deutsch (daten/de_50k.txt: Wort und Anzahl je Zeile); leer, wenn die Datei fehlt."""
    if not HAEUFIGKEIT.exists():
        return Counter()
    ref = Counter()
    for zeile in HAEUFIGKEIT.read_text(encoding="utf-8").splitlines():
        teile = zeile.split()
        if len(teile) == 2 and teile[1].isdigit():
            ref[teile[0]] = int(teile[1])
    return ref


def lieblingswoerter(zaehlung, ref, ausschluss, mindest=8, hoechstens=20):
    """Wörter, die hier viel häufiger sind als im gewöhnlichen Deutsch. Wörter, die dort fehlen (Welt, Namen), zählen nicht."""
    n, n_ref = sum(zaehlung.values()) or 1, sum(ref.values()) or 1
    werte = []
    for w, k in zaehlung.items():
        if k < mindest or w in ausschluss or w not in ref:
            continue
        verh = (k / n) / (ref[w] / n_ref)
        if verh >= 5:
            werte.append((verh, w, k))
    return [f"{w} {k}× (×{verh:.0f})" for verh, w, k in sorted(werte, reverse=True)[:hoechstens]]


def manuskript_texte(bis=None):
    """(Nummer, Datei, Sicht, Wörter in Kleinschrift) je Kapitel ohne Status plan; ohne Kopf, Marken, Kommentare."""
    for p, nr, felder, voll in kapitel_koepfe():
        if bis is not None and nr > bis:
            continue
        _, rumpf, _ = kopf_trennen(voll)
        rumpf = re.sub(r"<!--.*?-->|\{\{.*?\}\}", " ", rumpf, flags=re.S)
        yield nr, p, str(felder.get("perspektive") or "").strip(), WORT.findall(rumpf)



def auffaellig(teil, rest, mindest=5, hoechstens=12):
    """Wörter, die im Teil viel häufiger sind als im Rest (Verhältnis der Anteile)."""
    n_teil, n_rest = sum(teil.values()) or 1, sum(rest.values()) or 1
    werte = []
    for w, k in teil.items():
        if k < mindest:
            continue
        verh = (k / n_teil) / ((rest.get(w, 0) + 1) / n_rest)
        if verh >= 2.5:
            werte.append((verh, w, k))
    return [f"{w} {k}× (×{verh:.0f})" for verh, w, k in sorted(werte, reverse=True)[:hoechstens]]


def befehl_woerter(ziel=None):
    """Zählt Wörter im Manuskript: häufig, doppelt vergeben, je Sicht, Stimmung je Kapitel, ähnliche Namen. Urteilt nicht."""
    kapitel = list(manuskript_texte())
    if not kapitel:
        sys.exit("Noch keine Kapitel mit Text.")
    glossar = glossar_zeilen()
    namen_klein = {w.casefold() for g in glossar for w in WORT.findall(g["begriff"])}
    namen_klein |= {n + "s" for n in namen_klein}   # Ennas, Tesks
    zahl = re.fullmatch(r"k?0*(\d+)", ziel.strip()) if ziel else None
    nur = int(zahl.group(1)) if zahl else None
    if ziel and nur is None:
        sys.exit("woerter nimmt ein Kapitel, etwa: woerter k06")

    def inhalt(woerter):
        return Counter(w.lower() for w in woerter if len(w) > 3 and w.lower() not in STOPP)

    alle = Counter()
    je_kapitel, roh = {}, {}
    for nr, p, sicht, woerter in kapitel:
        c = inhalt(woerter)
        je_kapitel[nr] = (p, sicht, c, len(woerter))
        roh[nr] = Counter(woerter)
        alle += c
    gesamt = sum(n for *_, n in je_kapitel.values())
    print(f"# Wörter: {len(kapitel)} Kapitel, {gesamt} Wörter" + (f", Schwerpunkt Kapitel {nur}" if nur else ""))

    # 1. häufig
    if nur:
        p, sicht, c, n = je_kapitel.get(nur, (None, "", Counter(), 0))
        if not p:
            sys.exit(f"Kapitel {nur} hat noch keinen Text (oder Status plan).")
        rest = alle - c
        ausgabe(f"Auffällig in Kapitel {nur} gegenüber dem übrigen Buch (Lieblingswörter des Kapitels?)",
                auffaellig({w: k for w, k in c.items() if w not in namen_klein and w not in GEWOEHNLICH}, rest))
        basis = c
    else:
        haeufig = [(k, w) for w, k in alle.items() if w not in namen_klein and w not in GEWOEHNLICH]
        ausgabe("Häufigste Inhaltswörter (ohne Namen)", [f"{w} {k}×" for k, w in sorted(haeufig, reverse=True)[:25]])
        basis = alle
    ref = alltagsdeutsch()
    if ref:
        wissen = Counter()   # was auch im Wissen steht, ist Welt; der Rest ist Erzählweise
        for w in WISSEN:
            for p in (WURZEL / w).rglob("*.md"):
                wissen.update(x.lower() for x in WORT.findall(lesen(p)))
        liste = lieblingswoerter(basis, ref, namen_klein, mindest=4 if nur else 8, hoechstens=60)
        welt = [z for z in liste if wissen[z.split()[0]] >= 2]
        art = [z for z in liste if wissen[z.split()[0]] < 2]
        ausgabe("Lieblingswörter der Erzählweise gegenüber gewöhnlichem Deutsch (Gesten, Verben, Füllbilder?)", art[:20])
        ausgabe("Lieblingswörter der Welt (stehen auch im Wissen; meist gewollt)", welt[:12])
    else:
        print("\n(Ohne _werkzeuge/daten/de_50k.txt kein Vergleich mit gewöhnlichem Deutsch.)")

    # 2. doppelt vergeben: ein Glossarname, der auch als Teil anderer Wörter oder in anderen Glossar-Einträgen steht
    text_woerter = Counter()
    for nr, p, sicht, woerter in kapitel:
        if not nur or nr == nur:
            text_woerter.update(woerter)
    funde = []
    for g in glossar:
        for name in {g["grund"], *WORT.findall(g["grund"])}:
            if len(name) < 4 or not name[0].isupper() or name.casefold() in STOPP:
                continue
            form = re.compile(rf"{re.escape(name)}{ENDUNGEN}")
            allein = sum(k for w, k in text_woerter.items() if form.fullmatch(w))
            klein = sum(k for w, k in text_woerter.items() if form.fullmatch(w[:1].upper() + w[1:]) and w[:1].islower())
            # Zusammensetzungen: großgeschrieben, beginnt oder endet mit dem Namen (Kalkgasse, Varreturm)
            teile = Counter({w: k for w, k in text_woerter.items() if w[:1].isupper() and not form.fullmatch(w)
                             and (w.startswith(name) or re.search(rf"{re.escape(name.casefold())}{ENDUNGEN}$", w.casefold()))
                             and len(w) > len(name) + 2})
            andere = [] if g["art"] == "Figur" else \
                [h["begriff"] for h in glossar if h is not g and re.search(rf"(?<![{BUCHSTABE}]){re.escape(name)}", h["kurz"])]
            gewicht = 2 * klein + (len(andere) if len(andere) >= 2 else 0) + sum(teile.values()) / 5
            if allein and gewicht >= 3:
                zeile = f"{name} ({g['begriff']}): {allein}× allein"
                if klein:
                    zeile += f"; {klein}× klein, als gewöhnliches Wort"
                if teile:
                    zeile += "; in Zusammensetzungen: " + ", ".join(f"{w} {k}" for w, k in teile.most_common(5))
                if len(andere) >= 2:
                    zeile += f"; im Glossar auch bei: {', '.join(andere[:5])}"
                funde.append((gewicht, zeile))
    gesehen, zeilen = set(), []
    for _, z in sorted(funde, reverse=True):
        if z.split(" (")[0] not in gesehen:
            gesehen.add(z.split(" (")[0])
            zeilen.append(z)
    ausgabe("Vielleicht doppelt vergeben (ein Wort, mehrere Dinge?)", zeilen[:12], leer="nichts Auffälliges")

    # 3. je Sicht
    if not nur:
        sichten = defaultdict(Counter)
        for p, sicht, c, n in je_kapitel.values():
            sichten[sicht or "ohne Sicht"] += c
        if len(sichten) > 1:
            for sicht, c in sichten.items():
                rest = alle - c
                ausgabe(f"Wörter der Sicht {sicht} (gegenüber den anderen Sichten)",
                        auffaellig({w: k for w, k in c.items() if w not in namen_klein}, rest, hoechstens=10))

    # 4. Stimmung je Kapitel (je 1.000 Wörter), Ausreißer markiert
    werte = {}
    for nr, (p, sicht, c, n) in je_kapitel.items():
        werte[nr] = {feld: 1000 * sum(k for w, k in roh[nr].items() if muster.fullmatch(w)) / max(n, 1)
                     for feld, muster in STIMMUNG_RE.items()}
    zeilen = []
    for feld in STIMMUNG:
        reihe = sorted(werte[nr][feld] for nr in werte)
        mitte = statistics.median(reihe) if reihe else 0
        teile = []
        for nr in sorted(werte):
            v = werte[nr][feld]
            marke = " ↑" if mitte and v > 1.8 * mitte and v >= 1 else ""
            if not nur or nr == nur:
                teile.append(f"{nr}: {v:.1f}{marke}")
        zeilen.append(f"{feld}: " + " · ".join(teile) + f"  (Mitte {mitte:.1f})")
    ausgabe("Stimmungswörter je 1.000 Wörter (↑ = deutlich über der Mitte des Buchs)", zeilen)

    # 5. Namen: neu je Kapitel und ähnliche Figurennamen
    if not nur:
        erste = {}
        for nr, p, sicht, woerter in kapitel:
            vorhanden = set(woerter)
            for g in glossar:
                if g["grund"] not in erste and g["grund"] in vorhanden:
                    erste[g["grund"]] = nr
        neu = Counter(erste.values())
        ausgabe("Neue Glossarnamen je Kapitel", [f"Kap. {nr}: {neu[nr]}" for nr in sorted(je_kapitel)])
        figuren = sorted({g["grund"] for g in glossar if g["art"] == "Figur" and " " not in g["grund"]})
        aehnlich = []
        for i, a in enumerate(figuren):
            for b in figuren[i + 1:]:
                if a[:3] == b[:3] or (len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1):
                    aehnlich.append(f"{a} – {b}")
        ausgabe("Ähnliche Figurennamen (gleicher Anfang oder ein Buchstabe Unterschied)", aehnlich, leer="keine")


# ---------------------------------------------------------------- Überarbeiten, Wissen, Wiederholung

def befehl_ueberarbeiten():
    """Je Kapitel, was zur Überarbeitung offen ist; „bald“, wenn der Autor etwas angemerkt hat."""
    zeilen = []
    for p, nr, felder, text in kapitel_koepfe():
        rumpf = kopf_trennen(text)[1]
        klammern = len(re.findall(r"\{\{", rumpf))
        autor = len(re.findall(r"<!-- \[A\]", rumpf))
        claude = len(re.findall(r"<!-- \[C\?\]", rumpf))
        grob = len(re.findall(r"<!-- \[C\?\] grob", rumpf))
        claude -= grob
        korr = liste_aus(felder.get("korrekturen"))
        merker = sum(1 for k in korr if k.strip('"').startswith("prüfen"))
        ziele = len(korr) - merker
        bewertet = str(felder.get("dringlich", "")).strip().strip('"').split(" ", 1)[0].rstrip(":·,")
        if bewertet in ("bald", "später"):
            stufe, art = bewertet, "bewertet"
        elif klammern or autor or ziele or grob:
            stufe, art = "bald", "geschätzt"
        elif claude or merker:
            stufe, art = "später", "geschätzt"
        else:
            stufe, art = "–", ""
        teile = [f"{n} {w}" for n, w in ((klammern, "{{ }}"), (autor, "Kommentar [A]"), (ziele, "Korrektur"),
                                          (grob, "grob [C?]"), (claude, "klein [C?]"), (merker, "Merker prüfen")) if n]
        zeilen.append((stufe, nr, f"{p.stem} ({felder.get('status', '?')}): {stufe}" + (f" ({art})" if art else "") + " · "
                       + (", ".join(teile) if teile else "nichts offen")
                       + f" · Kritik: {str(felder.get('kritik') or '–').strip(chr(34))}"))
    reihenfolge = {"bald": 0, "später": 1, "–": 2}
    ausgabe("Überarbeitung je Kapitel (bewertet: Feld dringlich:; sonst geschätzt: Anmerkungen des Autors bald, nur Merker später)",
            [z for _, _, z in sorted(zeilen, key=lambda x: (reihenfolge[x[0]], x[1]))])


def befehl_weiss(name, bis=None):
    """Was eine Figur bis Kapitel N erfahren hat, aus den Zeilen „X erfährt …“ in szenen:."""
    muster = such_muster(begriffe_zu([name]))
    treffer = []
    for p, nr, felder, _ in kapitel_koepfe():
        if bis is not None and nr > bis:
            continue
        for eintrag in liste_aus(felder.get("szenen")):
            for satz in re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ])", eintrag.strip('"')):
                m = re.search(r"(\w+(?: und \w+)?) erfährt\b", satz)
                if m and muster.search(m.group(1)):
                    treffer.append(f"Kap. {nr}: {satz[m.start():][:220]}")
    ausgabe(f"{name} erfährt" + (f" (bis Kapitel {bis})" if bis else ""), treffer, leer="nichts in szenen:")


def befehl_wiederholung(ziel, hoechstens=3):
    """Sätze um Orte des Glossars: in diesem Kapitel und in früheren nebeneinander, für einen Prüfer."""
    nr_ziel = int(re.sub(r"\D", "", str(ziel)) or 0)
    saetze = lambda rumpf: [s.strip() for s in re.split(r"(?<=[.!?…])\s+", re.sub(r"<!--.*?-->", "", rumpf, flags=re.S))
                            if s.strip()]
    texte = {nr: saetze(rumpf) for _, nr, _, _, rumpf in kapitel_dateien()}
    if nr_ziel not in texte:
        sys.exit(f"Kapitel {ziel} nicht gefunden")
    eigene = texte[nr_ziel]
    frueher = [(n, s) for n in sorted(texte) if n < nr_ziel for s in texte[n]]
    for g in [g for g in glossar_zeilen() if g["art"] == "Ort"]:
        muster = such_muster(begriffe_zu([g["grund"]]))
        hier = [s for s in eigene if muster.search(s)]
        if not hier:
            continue
        vorher = [f"Kap. {n}: {s[:200]}" for n, s in frueher if muster.search(s)]
        if not vorher:
            continue
        print(f"\n## {g['grund']}")
        for s in hier[:hoechstens]:
            print(f"- hier: {s[:200]}")
        for z in vorher[:hoechstens]:
            print(f"- früher {z}")


def szenen_text(rumpf):
    """Rumpf eines Kapitels nach Marken <!-- sN --> geteilt: {N: Text}."""
    teile = re.split(r"<!-- s(\d+) -->", rumpf)
    return {int(teile[i]): teile[i + 1].strip() for i in range(1, len(teile) - 1, 2)}


def kapitel_nr(ziel):
    return int(re.sub(r"\D", "", str(ziel)) or 0)


def befehl_szene(ziel, nr, um=0):
    """Gibt Szene sN eines Kapitels aus, mit um Szenen davor und danach."""
    k, n = kapitel_nr(ziel), int(re.sub(r"\D", "", str(nr)) or 0)
    for p, knr, _, felder, rumpf in kapitel_dateien():
        if knr != k:
            continue
        szenen = szenen_text(rumpf)
        if not szenen:
            sys.exit(f"{p.name} hat keine Szenenmarken <!-- sN -->")
        zeilen = {str(e).strip('"')[:3].strip(): str(e).strip('"') for e in liste_aus(felder.get("szenen"))}
        for i in range(n - um, n + um + 1):
            if i in szenen:
                print(f"\n## {p.stem} · s{i}" + (" (gesucht)" if i == n else ""))
                if f"s{i}" in zeilen:
                    print(f"> {zeilen[f's{i}']}\n")
                print(szenen[i])
        return
    sys.exit(f"Kapitel {ziel} nicht gefunden")


def befehl_treffen(namen):
    """Szenen, in denen Figuren zusammen vorkommen; ein Name allein: mit jeder anderen Perspektivfigur."""
    gesucht = [n.strip() for n in namen.split(",") if n.strip()]
    koepfe = list(kapitel_dateien())
    sichten = sorted({str(f.get("perspektive") or "").strip() for _, _, _, f, _ in koepfe} - {""})
    if len(gesucht) == 1:
        paare = [(gesucht[0], s) for s in sichten if s != gesucht[0]]
    else:
        paare = [tuple(gesucht)]
    for paar in paare:
        muster = [such_muster(begriffe_zu([n])) for n in paar]
        treffer = []
        for p, nr, _, felder, rumpf in koepfe:
            szenen = szenen_text(rumpf)
            index = {str(e).strip('"')[:3].strip(): str(e).strip('"') for e in liste_aus(felder.get("szenen"))}
            for sn, text in szenen.items():
                zeile = index.get(f"s{sn}", "")
                im_index = all(m.search(zeile) for m in muster)
                im_text = all(m.search(text) for m in muster)
                if im_index or im_text:
                    sicht = str(felder.get("perspektive") or "?").strip()
                    art = "zusammen (Index)" if im_index else "beide im Text erwähnt"
                    treffer.append(f"k{nr:02d} s{sn} · Sicht {sicht} · {art}: {zeile[3:].strip()[:160]}")
        ausgabe(" und ".join(paar), treffer, leer="keine gemeinsame Szene")


def tag_von(text, tage_je_kapitel):
    """Erster „Tag N“ im Text; „wie Kapitel N“ übernimmt dessen Tag."""
    m = re.search(r"Tag (\d+)", text or "")
    if m:
        return int(m.group(1))
    m = re.search(r"wie (?:in )?Kapitel (\d+)", text or "")
    if m:
        return tage_je_kapitel.get(int(m.group(1)))
    return None


def befehl_zeitleiste():
    """Alle Szenen aller Sichten nach Tag; markiert Tage, an denen mehrere Sichten erzählen."""
    tage, reihe = {}, []
    for p, nr, _, felder, _ in kapitel_dateien():
        if felder.get("status") == "plan":
            continue
        zeit = str(felder.get("zeit") or "")
        tag_k = tag_von(zeit, tage)
        tage[nr] = tag_k
        sicht = str(felder.get("perspektive") or "?").strip()
        eintraege = liste_aus(felder.get("szenen"))
        for e in eintraege:
            e = str(e).strip('"')
            kopfteil = e.split(":", 1)[0]
            tag = tag_von(kopfteil, tage) or tag_k
            reihe.append((tag if tag is not None else 10**6, nr, e[:3].strip(), sicht, kopfteil[3:].strip()[:70]))
        if not eintraege:
            reihe.append((tag_k if tag_k is not None else 10**6, nr, "–", sicht, zeit[:70]))
    reihe.sort()
    print("# Zeitleiste (Tag aus Szenenzeile, sonst aus zeit: des Kapitels; „wie Kapitel N“ übernimmt dessen Tag)")
    letzter = None
    for tag, nr, sn, sicht, ort in reihe:
        if tag != letzter:
            sichten = sorted({r[3] for r in reihe if r[0] == tag})
            mehr = "  ← mehrere Sichten: wer ist wo?" if len(sichten) > 1 and tag != 10**6 else ""
            print(f"\n## Tag {tag if tag != 10**6 else '?'}{mehr}")
            letzter = tag
        print(f"- k{nr:02d} {sn} · {sicht} · {ort}")


def befehl_vorsprung(name=None):
    """Was der Leser weiß und eine Perspektivfigur (noch) nicht: „Leser erfährt“ aus Kapiteln, in denen sie fehlt,
    und „Leser erfährt“ in ihren eigenen Kapiteln (dort weiß der Leser mehr als sie). Kandidaten, kein Urteil."""
    koepfe = [k for k in kapitel_dateien() if k[3].get("status") != "plan"]
    sichten = sorted({str(k[3].get("perspektive") or "").strip() for k in koepfe} - {""})
    for figur in ([name] if name else sichten):
        muster = such_muster(begriffe_zu([figur]))
        eigen, fremd = [], []
        for p, nr, _, felder, _ in koepfe:
            sicht = str(felder.get("perspektive") or "").strip()
            dabei = any(muster.search(f) for f in liste_aus(felder.get("figuren")))
            for e in liste_aus(felder.get("szenen")):
                e = str(e).strip('"')
                # „Leser erfährt“ zählt überall; „X erfährt“ nur in Kapiteln, in denen die Figur fehlt
                for m in re.finditer(r"(\w+(?: und \w+)?) erfährt\b:?\s*(.+?)(?=(?:\s[A-ZÄÖÜ]\w+(?: und \w+)? erfährt)|$)", e):
                    wer, was = m.group(1), m.group(2).strip()[:180]
                    z = f"k{nr:02d} {e[:3].strip()} · {wer} erfährt: {was}"
                    if wer == "Leser" and sicht == figur:
                        eigen.append(z)
                    elif not dabei and sicht != figur and not muster.search(wer):
                        fremd.append(z)
        ausgabe(f"{figur}: Leser weiß mehr, in den eigenen Kapiteln", eigen, leer="keine Zeile „Leser erfährt“")
        ausgabe(f"{figur}: Leser erfährt es in Kapiteln ohne die Figur (vermutlich weiß sie es nicht)", fremd, leer="nichts")


def befehl_faeden(schwelle=3):
    """Offene Fäden aus 30_struktur/faeden.md je Strang (Abschnitt ## <Perspektivfigur>, sonst alle Kapitel):
    wann zuletzt in szenen:/erzaehlt: berührt (Wortsuche, grob), gezählt in Kapiteln dieses Strangs; dazu Fäden ohne Auflösung."""
    datei = WURZEL / "30_struktur" / "faeden.md"
    if not datei.exists():
        sys.exit("30_struktur/faeden.md fehlt")
    alle_koepfe = [k for k in kapitel_dateien() if k[3].get("status") != "plan"]
    sichten = {str(k[3].get("perspektive") or "").strip() for k in alle_koepfe} - {""}
    still, ohne = defaultdict(list), defaultdict(list)
    strang, spalten = "?", []
    for zeile in lesen(datei).splitlines():
        if zeile.startswith("## "):
            strang = zeile[3:].strip()
            continue
        if zeile.startswith("| Faden"):
            spalten = [x.strip().lower() for x in zeile.strip().strip("|").split("|")]
            continue
        if not zeile.startswith("|") or zeile.startswith("|---"):
            continue
        teile = [x.strip() for x in zeile.strip().strip("|").split("|")]
        faden = teile[0]
        if "auflösung" in spalten and len(teile) > spalten.index("auflösung") and not teile[spalten.index("auflösung")]:
            ohne[strang].append(faden[:90])
        koepfe = [k for k in alle_koepfe if str(k[3].get("perspektive") or "").strip() == strang] if strang in sichten else alle_koepfe
        reihe = [k[1] for k in koepfe]
        wortliste = [w for w in WORT.findall(faden) if w.lower() not in STOPP and w not in ("Kapitel", "Erster", "Entwurf")]
        fragewort = ("Was", "Wo", "Wer", "Warum", "Ob", "Wie", "Der", "Die", "Das")
        namen = {w for w in wortliste if w[0].isupper() and len(w) >= 3 and w not in fragewort}
        woerter = {w for w in wortliste if len(w) >= 5}
        if not namen and not woerter:
            continue
        zuletzt = None
        for p, nr, _, felder, _ in koepfe:
            text = " ".join(str(e) for e in liste_aus(felder.get("szenen")) + liste_aus(felder.get("erzaehlt")))
            hat = lambda w: re.search(rf"\b{re.escape(w[:max(3, len(w) - 2)])}", text, re.I)
            treffer_namen = sum(1 for w in namen if hat(w))
            if (namen and treffer_namen >= min(2, len(namen))) or (not namen and sum(1 for w in woerter if hat(w)) >= min(2, len(woerter))):
                zuletzt = nr
        if zuletzt is None:
            still[strang].append((10**6, f"{faden[:90]} · nie in szenen:/erzaehlt: gefunden"))
        else:
            seit = len([n for n in reihe if n > zuletzt])
            if seit >= schwelle:
                still[strang].append((seit, f"{faden[:90]} · zuletzt k{zuletzt:02d}, seit {seit} Kapiteln des Strangs still"))
    print(f"# Fäden je Strang (still: seit mindestens {schwelle} Kapiteln des Strangs nicht berührt; Wortsuche, darum Kandidaten)")
    for s in dict.fromkeys(list(still) + list(ohne)):
        ausgabe(f"{s}: still", [z for _, z in sorted(still[s], reverse=True)], leer="nichts")
        ausgabe(f"{s}: ohne Auflösung", ohne[s], leer="alle mit Plan")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Prüfskript für das Buchprojekt")
    parser.add_argument("befehl", choices=["text", "namen", "wissen", "werkstatt", "gezeigt", "akte", "paket", "woerter",
                                           "erzaehlt", "index", "ueberarbeiten", "weiss", "wiederholung", "szene", "treffen",
                                           "zeitleiste", "vorsprung", "faeden", "alles"])
    parser.add_argument("datei", nargs="?")
    parser.add_argument("szene_nr", nargs="?", help="szene: Nummer der Szene, etwa s3")
    parser.add_argument("--szene", help="paket: nur für diese Szene (sN), mit Nachbarn und Anmerkungen")
    parser.add_argument("--um", type=int, default=0, help="szene: so viele Szenen davor und danach mit ausgeben")
    parser.add_argument("--ziel", help="Wortziel, z. B. 4000-6000")
    parser.add_argument("--bis", type=int, help="akte: nur bis zu diesem Kapitel (was der Leser bis dahin kennt)")
    parser.add_argument("--schreiben", action="store_true", help="erzaehlt: Tabelle in 30_struktur/erzaehlt.md neu schreiben")
    a = parser.parse_args()
    if a.befehl == "text":
        if not a.datei:
            parser.error("text braucht eine Datei")
        befehl_text(a.datei, a.ziel)
    elif a.befehl == "gezeigt":
        zahl = a.datei and a.datei.isdigit()
        befehl_gezeigt(int(a.datei) if zahl else None, None if zahl else a.datei)
    elif a.befehl == "akte":
        if not a.datei:
            parser.error('akte braucht einen Namen, etwa: akte Orsola oder akte "Zum Kessel"')
        befehl_akte(a.datei, a.bis)
    elif a.befehl == "paket":
        if not a.datei:
            parser.error("paket braucht ein Kapitel, etwa: paket k09 oder paket 9")
        befehl_paket(a.datei, a.szene)
    elif a.befehl == "woerter":
        befehl_woerter(a.datei)
    elif a.befehl == "erzaehlt":
        befehl_erzaehlt(a.schreiben)
    elif a.befehl == "index":
        befehl_index()
    elif a.befehl == "ueberarbeiten":
        befehl_ueberarbeiten()
    elif a.befehl == "weiss":
        if not a.datei:
            parser.error("weiss braucht eine Figur, etwa: weiss Tesk --bis 8")
        befehl_weiss(a.datei, a.bis)
    elif a.befehl == "szene":
        if not a.datei or not a.szene_nr:
            parser.error("szene braucht Kapitel und Szene, etwa: szene k07 s3 --um 1")
        befehl_szene(a.datei, a.szene_nr, a.um)
    elif a.befehl == "treffen":
        if not a.datei:
            parser.error("treffen braucht Figuren, etwa: treffen Enna,Tesk oder treffen Vico")
        befehl_treffen(a.datei)
    elif a.befehl == "zeitleiste":
        befehl_zeitleiste()
    elif a.befehl == "vorsprung":
        befehl_vorsprung(a.datei)
    elif a.befehl == "faeden":
        befehl_faeden()
    elif a.befehl == "wiederholung":
        if not a.datei:
            parser.error("wiederholung braucht ein Kapitel, etwa: wiederholung k09")
        befehl_wiederholung(a.datei)
    elif a.befehl == "alles":
        befehl_namen(); befehl_wissen(); print(); befehl_werkstatt()
    else:
        {"namen": befehl_namen, "wissen": befehl_wissen,
         "werkstatt": befehl_werkstatt}[a.befehl]()


if __name__ == "__main__":
    main()
