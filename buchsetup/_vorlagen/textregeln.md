# Regeln für Texte (Kapitel und Leseproben)

Wird gelesen, wenn ein Text geschrieben, überarbeitet oder geprüft wird, nicht bei jeder Sitzung. Ablauf des Schreibens: `_vorlagen/schreibablauf.md`, Handwerk: Skill `schreiben`.

## Dateien
- Ein Kapitel pro Datei: `40_manuskript/kNN_kurztitel.md`. Die Dateinamen bestimmen die Reihenfolge im EPUB.
- Kopfdaten nach `_vorlagen/szene.md`. Solange ein Kapitel entsteht, trägt es Brief, Welt, Spuren und Plan; **danach bleibt ein Steckbrief** (etwa 600 bis 900 Wörter, ohne die offenen Felder): Titel, Perspektive, Wegmarke, Fixpunkt, Status, Ziel, Figuren, Orte, Zeit, Geld, Zusammenfassung, Schlussbild, Erzählt, Szenen; dazu Notizen, Korrekturen und Bericht, solange etwas offen ist. Länge und Aufbau: `30_struktur/buchstruktur.md`.
- **Szenenmarken:** Jede Szene beginnt mit einer unsichtbaren Zeile `<!-- s1 -->`, `<!-- s2 -->` …, damit ein Agent direkt zur Szene springt. Im Feld `szenen:` steht je Szene eine Zeile (was geschieht, Figuren, Ort, Faden, vor allem Wissen: wer erfährt was); `pruefen.py index` baut daraus `30_struktur/index.md`.
- Stilprofile stehen in `50_stil/stilprofile.md` mit Kürzel `S-02` usw.

## Drei Arten von Text
1. **Leseprobe:** kurz (300–1.000 Wörter), zum Ausprobieren von Ton, Figur oder Szene. Nie Kanon. Entsteht in `01_werkstatt/` als `probe-NN_kurztitel.md` und zählt dort zum Deckel; erst mit Freigabe des Autors kommt sie nach `50_stil/proben/`. Nach der Auswertung wird die Essenz herausgezogen (Ideen als `[C?]` in Wissensdateien oder einen Werkstatt-Entwurf, gelungene Sätze und Stil ins Stilprofil); dann wird die Probe gelöscht, Git hat sie.
2. **Kapitel im Entwurf:** vollständiges Kapitel in `40_manuskript/`.
3. **Sauberes Kapitel:** Status `fest`.

## Status
- `plan`: nur Kapitelplan, noch kein Text; erscheint nicht im EPUB
- `entwurf`: darf frei überarbeitet werden
- `autor-bearbeitet`: der Autor hat hineingeschrieben. Claude überschreibt nicht mehr, sondern schlägt Änderungen in `> [C?] …`-Blöcken vor
- `fest`: nur noch Korrekturen auf Anfrage

## Überarbeiten
- **Ausbauen oder neu schreiben:** Trägt das Gerüst eines Kapitels, wird es ausgebaut. Trägt es nicht mehr (Logik, Reihenfolge, Ton), wird es neu geschrieben; brauchbare Absätze werden übernommen. Vor einer Neufassung bekommt der Autor einen kurzen Plan.
- **Fassungen:** Eine Überarbeitung ersetzt die Datei; ältere Fassungen liegen in Git. Eine verworfene Szene wird gelöscht.
- **Anmerkungen des Autors im Text:** Wer beim Lesen im Kapitel etwas anmerkt, schreibt es als `{{ Kommentar }}` direkt an die Stelle, im Satz oder auf eigener Zeile, auch über mehrere Zeilen. Ein Zeichen vorn ist möglich, aber nicht nötig: `{{! }}` Fehler oder Widerspruch · `{{? }}` Frage oder unklar · `{{+ }}` mehr davon, ausbauen · `{{- }}` kürzen oder streichen. Vor dem Überarbeiten sucht Claude alle `{{` im Kapitel (`grep -n "{{"`). Bei „Kapitel X überarbeiten“ arbeitet er sie ab und entfernt die Klammern samt Inhalt; Gedanken ohne klare Richtung fragt er vorher nach, Grundsätzliches geht zusätzlich unter `notizen:` oder in die Wissensdateien. Die Marken allein machen den Status nicht zu `autor-bearbeitet`; hat der Autor auch Text geändert, gilt der Status wie oben. Im EPUB erscheinen sie nicht.
- **Anmerkungen von Claude im Text** (`kritiker`, Prüfläufe, Skill `system`): auf eigener Zeile hinter dem Absatz, `<!-- [C?] grob · „Anfang des Satzes …“: Befund · Vorschlag -->` oder `klein`. **grob:** Handlung, Aufbau, Figur, Kanon, Verständnis; wird bald überarbeitet. **klein:** Wort, Satz, Geste, Echo; wird gesammelt, wenn das Kapitel ohnehin ganz gelesen wird. Ohne Angabe gilt klein. Den Text ändert die Anmerkung nicht.
- **Notizen:** Rückmeldungen des Autors landen verdichtet in den Kopfdaten unter `notizen:`. Was daraus zu ändern ist, steht unter `korrekturen:`. Allgemeine Erkenntnisse gehen zusätzlich in die Wissensdateien.
- **Logikänderungen:** Ändert sich der Kanon, trägt Claude betroffene Stellen unter `korrekturen:` ein, wenn er sie kennt, oder einen kurzen Verweis „prüfen: …“ als Merker. Bei Status `entwurf` werden sie bei der nächsten Überarbeitung eingearbeitet und dann gelöscht.
- **Neue Fakten:** Erfindet Claude beim Schreiben etwas Bleibendes (Name, Ort, Gegenstand, Vorgeschichte, Aussehen, Regel), das ein späteres Kapitel an anderem Ort wissen muss, kommt es ohne Kapitelvermerk in die Wissensdatei, klein und stimmig als `[C✓]`, sonst als `[C?]`. Gesten, Stimmungen und Verhalten einer Szene bleiben im Kapitel; sie sind keine Eigenschaft der Figur. Wird etwas abgelehnt, muss es auch aus dem Text raus.

## Kindle
`python _werkzeuge/epub_bauen.py --kindle` (Kapitel) bzw. `--proben --kindle` (Leseproben), nur auf Wunsch.
