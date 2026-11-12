# Hinweise für Codex (gilt vor allem anderen in dieser Datei)

Dieses Setup wurde für Claude Code gebaut und für Codex übersetzt. Lies den Rest der Datei so:

- **„Claude“ bist du.** Wo „Claude“ steht, ist die Arbeit gemeint, die du tust. Der **Autor** ist hier eine **Autorin**; sprich sie so an.
- **Skills** liegen in `.agents/skills/<name>/SKILL.md` (`schreiben`, `weltenbau`, `system`, `sitzung-abschliessen`). Werden sie nicht von selbst angeboten, lies die Datei direkt, sobald die Arbeitsweise passt.
- **Start-Check:** Es gibt keinen Hook. Führe zu Beginn jeder Sitzung `python _werkzeuge/sitzung_start.py` aus (meist ohne Ausgabe), lies dann `STAND.md` und den Stand in `30_struktur/erzaehlt.md`.
- **Modelle und Agenten:** Modellnamen (Opus, Sonnet, Haiku) und „Tochtersitzung“ gelten für dich nicht; arbeite mit dem Modell, das läuft. Die Rollen `kritiker` und `pruefer` liegen als Textdateien in `_agenten/`. Auf Wunsch der Autorin (und beim `kritiker` nur mit ihrem Ja) lies die Datei und führe die Prüfung nach ihrem Auftrag aus, am besten in einem frischen Thread oder Unteragenten, wenn die App das kann. Sonst entfällt sie.
- **Git ohne Server:** Es gibt kein GitHub und keinen `origin`. Commit lokal, aber **kein `git push`, kein `fetch`, keine Branch-Aufräumschritte**; Zweige und Tochtersitzungen entfallen. Arbeite auf `main`.
- **Sicherung:** Die Autorin kopiert den ganzen Ordner regelmäßig in einen Cloud-Ordner oder auf einen Stick. Erinnere sie beim Sitzungsabschluss in einem Satz daran.
- **Python 3** wird für die Skripte gebraucht. Fehlt es (`python --version` schlägt fehl), sag es der Autorin und führe die Schritte aus der Anleitung `LIES_MICH_ZUERST.md` mit ihr durch.
- **Schreib- und Antwortregeln** unten (Abschnitt 4) gelten besonders: kurz antworten, eine Frage pro Antwort.

---

# Buchprojekt – Arbeitsregeln

Unser eigenes Projekt, kein Programm im Umlauf: Umbauen, Streichen und Neudenken ist erwünscht, auch am Setup selbst. Rücksicht auf Bestehendes nur, wo es trägt.

Dieser Workspace dient dem Aufbau einer Welt, ihrer Figuren und dem Manuskript. Die Datei gilt für jede Sitzung und hält nur, was alle Arbeitsweisen brauchen.

## 0. Das Buch

Alles, was nur zu diesem Buch gehört und jede Arbeitsweise braucht. Skills, Agenten und Vorlagen bleiben allgemein und verweisen hierher; die Skripte lesen Titel, Namen und Wortlisten aus `_werkzeuge/projekt.json`. Füllt der Skill `system` (Art „einrichten“) mit dem Autor.
- Reihe und Titel (Arbeitstitel) · Gattung und Zielgruppe · Sprache · gestartet am
- **Perspektivfiguren:** Name (`20_figuren/datei.md`), …
- **Schauplatz:** `10_welt/…` (im Ganzen); Bereiche …; Technik oder Magie …
- **Stil:** Grundton nach Vorbild …; Vorbilder je Szenenart (`50_stil/stilprofile.md`)
- **Zeit:** Wann ist Tag 1, woran erkennt man die Tageszeit?

## 1. Zwei Arbeitsweisen

Wenig, passender Kontext trägt weiter als viel. Darum gibt es zwei getrennte Skills:
- **`schreiben`**, sobald eine Leseprobe oder ein Kapitel entsteht (Richtung für einen Takt von zwei, drei Kapiteln statt eines Plans vor jedem). Er lädt nur, was die Szene braucht.
- **`weltenbau`** in jeder anderen Sitzung: Welt, Figuren, Handlung, Stil-Doku, Werkstatt, Entscheidungen, Briefe für den Schreiber. Zu Beginn laden, wenn kein Schreibauftrag ansteht.
- **`system`**, wenn es um das Setup selbst geht statt ums Buch: Störungen, neue Version, Einrichten (auch wenn Abschnitt 0 noch leer ist), Erklärtiefe, Skills, Skripte, Vorlage für andere (`_system/`).

Drei Schichten bleiben getrennt: **Welt** (was immer gilt: `10_welt/`, `20_figuren/`), **Plan** (was geschehen soll: `30_struktur/`) und **Erzählt** (was der Leser erlebt hat: `30_struktur/erzaehlt.md`, Index). Aus Kapiteln kommt nur Welt in die Wissensdateien, keine Gesten oder Stimmungen einer Szene.

Zu Beginn jeder Sitzung läuft automatisch der Start-Check (Hook, `_werkzeuge/sitzung_start.py`): er holt `main`, prüft alle Branches auf `origin` auf Commits, die nicht in `main` stehen, und bringt die sauber mergebaren lokal nach `main` ein. Meldet er einen Konflikt, legt die Sitzung ihn dem Autor vor, bevor sie Kanon ändert. Erst danach `STAND.md` und den Stand in `30_struktur/erzaehlt.md` lesen. Am Ende Skill `sitzung-abschliessen` (Übergabe, Commit; bei großen Sitzungen aufräumen, prüfen, Push, auf `main` bringen; danach keine offenen Branches mit eigenen Commits).

## 2. Herkunft: Wer hat was erdacht?

| Marker | Bedeutung | Kanon? |
|---|---|---|
| `[A]` | vom Autor gesetzt | ja |
| `[A?]` | Idee des Autors, noch nicht festgelegt („maybe“) | nein |
| `[C✓]` | Zusatz von Claude: bestätigt, klein und stimmig oder ausgearbeitet | ja |
| `[C?]` | Vorschlag von Claude, den der Autor entscheiden soll | nein |

- `[A]` sind die Eingaben des Autors, **verdichtet** auf den Kern, in seinem Sinn. Claude darf kürzen und gliedern, aber nichts hinzudichten; was Claude ergänzt, folgt der nächsten Regel.
- **Was passt, gilt.** Kleine, stimmige Zusätze von Claude oder einem Schreiber (Einzelheiten, kleine Orte, Gegenstände, Bräuche, Preise, Aussehen, Nebenfiguren ohne Rolle in der Handlung) gelten gleich und werden dem Autor in einer Zeile genannt; er kann sie jederzeit streichen. **Wohin:** Was ein Kapitel erfindet, gilt, weil es erzählt ist, und bleibt im Kapitel (`erzaehlt:`, `szenen:`, Index). In eine Wissensdatei kommt es als `[C✓]` nur, wenn ein Schreiber es wissen muss, dessen Kapitel nicht dort spielt: Es kehrt wieder, bindet andere Kapitel (wiederkehrende Figur, Ort, Regel, Vorgeschichte) oder der Autor will es dort.
- **Ausarbeiten heißt Kanon.** Was Claude mit dem Autor oder in seinem Sinn ausarbeitet, steht gleich als `[C✓]` und wird in einer Zeile genannt, nicht einzeln erfragt. `[C?]` bleibt für grobe Ideen und für das, was der Autor entscheiden soll: eine Kanonänderung (siehe unten, mit Empfehlung), neue Verbindungen oder Geheimnisse und echte Wahlmöglichkeiten. Wohin ein Eintrag gehört (Welt, Plan, Vorrat, Brief oder nirgends): Skill `weltenbau`, Abschnitt 2.
- `[C?]` wird mit Zustimmung `[C✓]`. Ändert der Autor einen Vorschlag ab, wird er `[A]`. Abgelehnte `[C?]` werden sofort gelöscht.
- Aufbau jeder Wissensdatei (nur Abschnitte mit Inhalt): `## Kanon` (nur [A] und [C✓]), `## Ideen & Vorschläge` ([A?] und [C?]), `## Offene Fragen`.
- **Widersprüche zum Kanon melden, nie still auflösen.** Kanonänderung ist alles, was ändert, wer was weiß, warum etwas geschieht, wann und in welcher Reihenfolge, wo etwas liegt, wie es aussieht und wer wie heißt.
- Neue Namen und Begriffe sofort in `glossar.md`.
- **Wissen verdichtet halten:** ersetzen statt anhängen, Doppeltes zusammenlegen (Skill `weltenbau`, Abschnitt 2).

## 3. Ordner

`00_eingang/` Rohnotizen · `01_werkstatt/` Entwürfe und ungeprüfte Leseproben · `10_welt/` Welt, `orte/` je Ort eine Datei · `20_figuren/` je Figur eine Datei · `30_struktur/` Handlung, Fäden, Buchstruktur, Erzählt und Szenenindex · `40_manuskript/` Kapitel · `50_stil/` Stilprofil, Stimmen, freigegebene Proben · `_vorlagen/` Vorlagen und Textregeln · `_werkzeuge/` Skripte (`LIESMICH.md`) · `_system/` das Setup als Vorlage zum Weitergeben (Skill `system`). Im Hauptordner `STAND.md`, `entscheidungen.md`, `glossar.md`. `_obsidian/` liest Claude nie.

## 4. Mit dem Autor schreiben

Der Autor liest von oben und antwortet oft schon nach der Hälfte. Wie viel du erklärst, steht in `_werkzeuge/projekt.json` unter `nutzer` (Skill `system`, „Den Nutzer kennenlernen“).
- Kurz antworten, das Wichtigste zuerst, höchstens eine Frage pro Antwort. Ausführliches in Werkstatt-Dateien, im Chat ein, zwei Sätze und der Verweis.
- Gelesen ist nur, worauf der Autor geantwortet hat. Alles andere bleibt in `STAND.md` unter „Wartet auf den Autor“ und wird später einzeln wieder aufgegriffen.
- **Der Autor diktiert.** Ist aus dem Zusammenhang klar, was gemeint war, das Gemeinte annehmen und die Deutung kurz erwähnen („‚Scham‘ als ‚Charme‘ gelesen“). Nachfragen nur, wenn mehrere Bedeutungen plausibel sind und die Wahl etwas Wichtiges ändert. In den Dateien steht nur die gedeutete Fassung.
- **Weich fassen.** Die Worte des Autors sind Richtung, nicht Wortlaut. Regeln und Pläne als Spielraum schreiben („wenn es passt“, „etwa“, „zum Beispiel“), als Richtung statt als Verbot; Absolutes nur, wo er es ausdrücklich will. Handlung als grober Rahmen, der dem Schreiber Freiheit lässt.

## 5. Agenten und Modelle

Agenten (`_agenten/`) nur bei Bedarf; Opus nur mit Freigabe des Autors, den `kritiker` nur mit seinem Ja. Wer welches Modell nimmt, wer was liest und startet: Skill `weltenbau`, Abschnitt 6; wann eine frische Sitzung beginnt: `_vorlagen/schreibablauf.md`, „Sitzungen schneiden“.

**Git:** Push gilt hier als Sicherung des Buchs und läuft beim Sitzungsabschluss ohne Rückfrage (Ausnahme zur persönlichen Regel „Push nur auf Anweisung“).

## 6. Das System nachschärfen

Das Setup ist nie fertig. Läuft etwas schief (ein Schreiber zieht eine Geste durch, ein Satz im Wissen ist zugespitzt oder falsch, ein Ablauf ist zu starr), wird die Ursache an ihrer Stelle behoben: falscher Kontext im Wissen gestrichen oder weicher gefasst, eine Regel kurz geschärft, ein starrer Ablauf zu „bei Bedarf“ gelockert. Lieber kleiner als größer: streichen und verdichten vor neuen Regeln.
