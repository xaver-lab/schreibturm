---
name: sitzung-abschliessen
description: Schließt eine Arbeitssitzung am Buchprojekt sauber ab – aufräumen, auf falschen Kontext prüfen, Übergabe in STAND.md schreiben, sichern. Verwenden, wenn der Autor die Sitzung beenden will oder „Übergabe“, „Sitzungsende“ oder „aufräumen“ sagt.
---

# Sitzung abschließen

Je nach Größe der Sitzung: Nach einer kleinen Sitzung (eine Frage, eine Änderung) genügen Übergabe (Abschnitt 3) und Commit; Aufräumen und Prüfen nur, wenn sich merklich etwas geändert hat. Nach einer großen Sitzung der ganze Ablauf.

## 1. Aufräumen
- `00_eingang/`: eingearbeitete Notizen löschen.
- `01_werkstatt/`: Was entschieden ist, in die Wissensdateien übernehmen und aus dem Entwurf streichen. Vollständig entschiedene Entwürfe löschen.
- Abgelehnte `[C?]` löschen. Nach „Bewusst verworfen“ in `entscheidungen.md` nur kleine Entscheidungen, die sonst leicht wiederkehren, als Einzeiler; sparsam.
- Beantwortete offene Fragen löschen; Erzähltes aus `30_struktur/vorrat.md` löschen.
- `50_stil/proben/` und Proben in `01_werkstatt/`: bei ausgewerteten Leseproben die Essenz herausziehen, dann die Probe löschen.

## 2. Auf falschen Kontext prüfen
- Wurden Wissensdateien oder Texte merklich geändert, zuerst `python _werkzeuge/pruefen.py alles` laufen lassen und jeden Befund beheben oder bewusst stehen lassen (Schreibvarianten sind oft gewöhnliche Wörter). Hat sich ein Kapitel geändert, danach `pruefen.py erzaehlt --schreiben` und `pruefen.py index --schreiben`, damit Übersicht und Szenenindex stimmen.
- Die neuen Einträge der Sitzung einmal nachsehen: am richtigen Ort (Skill `weltenbau`, Abschnitt 2, „Wohin damit?“) und so kurz wie möglich?
- Steht ein `[A?]` oder `[C?]` irgendwo als Tatsache formuliert, etwa in `STAND.md` oder in einer anderen Wissensdatei?
- Hat Claude etwas hinzugedichtet (Geschlecht, Alter, Herkunft, Namen), ohne es nach `AGENTS.md`, Abschnitt 2 einzutragen und zu melden?
- Stehen Dinge doppelt oder widersprechen sich Dateien?
- Hat sich der Kanon geändert? Dann betroffene Kapitel unter `korrekturen:` vermerken, wenn man die Stellen kennt, sonst als Merker „prüfen: …“.
- Neue Deutungen von Diktatfehlern in der Übergabe erwähnen. Hat der Autor eine zwei Sitzungen lang nicht korrigiert, gilt sie als bestätigt und fällt dort weg.

## 3. Übergabe in `STAND.md`
- **Wo wir stehen:** fünf Zeilen höchstens; wo die Hauptfiguren im Buch stehen, sagt `30_struktur/erzaehlt.md`.
- **Wartet auf den Autor:** worauf er noch nicht geantwortet hat (gilt als ungelesen). Höchstens fünf Punkte, je ein Thema in einer Zeile mit Dateipfad, das Wichtigste zuerst; ein unbeantworteter Nachbericht des Schreibers ist ein Punkt. Alles Weitere steht nur im Entwurf, darunter eine Zeile „Außerdem offen in: …“ mit den Dateien.
- Fragen zum System selbst (Abläufe, Regeln, was in die Wissensdateien gehört) entscheidet Claude nach den geltenden Regeln und nennt das Ergebnis in einer Zeile; zum Autor kommt nur, was den Kanon oder die Geschichte ändert.
- Hakte in der Sitzung ein Skript oder Ablauf, eine Zeile in `_system/hinweise.md` (Form steht dort). Aufträge am Setup selbst kommen nach `_system/werkbank.md`, nicht in diese Übergabe.
- **Nächster Arbeitsschritt.**
- **Vielversprechende Ideen** und **Achtung, Kontext.**
- Datum aktualisieren.

## 4. Sichern
- `git add -A`, Commit mit kurzer Nachricht (nur was sich inhaltlich geändert hat), `git push`, ohne Rückfrage. Bei kleinen Sitzungen genügt der Commit.
- **Auf `main` bringen:** Cloud- und Tochtersitzungen in einem eigenen Zweig arbeiten erst `main` ein (`git fetch origin`, `git merge origin/main`), mergen dann nach `main` und pushen, damit keine Branches liegen bleiben. Danach `git fetch --prune origin` und prüfen, dass `git branch -r --no-merged origin/main` keinen eigenen Branch mehr zeigt; den eigenen Arbeitsbranch nach dem Merge löschen (remote und lokal). Konflikte im Kanon nicht still auflösen, sondern dem Autor vorlegen.
- Auf Wunsch aufs Kindle: `python _werkzeuge/epub_bauen.py --kindle` und `--proben --kindle`.

## 5. Antwort
Drei Sätze: was aufgeräumt wurde, was beim Prüfen auffiel, was als Nächstes ansteht.
