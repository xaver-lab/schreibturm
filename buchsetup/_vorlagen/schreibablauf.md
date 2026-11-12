# Schreibablauf

Was um das Schreiben herum geschieht: Auftrag, Takt, wo geschrieben wird, Steckbrief, Bericht, Prüfer, Abschluss. Lesen vor dem Start und vor dem Abschluss; beim Schreiben selbst trägt der Skill `schreiben`. Dateien und Status: `_vorlagen/textregeln.md`.

## 1. Auftrag klären
- **Leseprobe** (300–1.000 Wörter, `01_werkstatt/probe-NN_kurztitel.md`, erst mit Freigabe des Autors nach `50_stil/proben/`) oder **Kapitel** (`40_manuskript/kNN_kurztitel.md`)?
- **Neu, Ausbau oder Neufassung?**
- Leseprobe: in einem Satz sagen, wie der Auftrag gedeutet wird, dann schreiben.

## 2. Takt, Richtung, Plan
- **Ein Takt sind zwei, drei Kapitel.** Davor gibt der Autor die Richtung in ein paar Sätzen vor oder sagt „lauf einfach“. Dann braucht es keinen Plan vor jedem Kapitel. Geplant sind höchstens die nächsten zwei, drei Wegmarken des Strangs; läuft ein Strang *frei*, genügen sein Ziel und der Plan in `30_struktur/handlung.md`. Fixpunkte (Reihenfolge, ungefähre Zeit) sind das Gerüst, kein Zwang: Will die Geschichte anders, darf die Sitzung einen verschieben, ändern oder ersetzen und nennt es im Bericht (`30_struktur/buchstruktur.md`).
- Fehlt die Richtung, genügt ein kurzer Plan, den der Autor bestätigt: wenige Zeilen, was die Szenen wollen und wohin sie führen, dazu das Schlussbild. Ein starres Raster gibt es nicht; ein anderes Schlussbild als in den letzten Kapiteln hilft gern.
- Für Überarbeitungen nach Anmerkungen des Autors braucht es keinen Plan: Die Anmerkungen sind der Plan (Abschnitt 3).
- **Grundlage ist der Brief** in der Kapiteldatei (`brief:`), den der Skill `weltenbau` anlegt (dort Abschnitt 5). Fehlt er, legt Claude ihn zuerst an.
- Zum Planen: `STAND.md`, der Stand in `30_struktur/erzaehlt.md`, in `30_struktur/buchstruktur.md` die Wegmarke und der nächste Fixpunkt; bei Ausbau oder Neufassung `notizen:`, `korrekturen:` und die Kommentare des Autors im Text (`<!-- [A] … -->`; vom Autor gesetzte `{{ … }}`, Schreibweise in `_vorlagen/textregeln.md`, per `grep -n "{{"` suchen; erledigte samt Klammern entfernen, Unklares erst nachfragen).
- Kopfdaten nach `_vorlagen/szene.md`, Status `plan`.

## 3. Wo geschrieben wird
- **Im Chat:** Claude schreibt selbst weiter nach dem Skill `schreiben`.
- **In einer Tochtersitzung** (Opus, vom Autor einmal pro Takt freigegeben, frischer Kontext, eigener Zweig): Auftrag, etwa: „Lies `.agents/skills/schreiben/SKILL.md` und `_vorlagen/schreibablauf.md`. Schreib das Kapitel `<Pfad>` nach der Richtung des Autors. Hinweise: … Bring am Ende deinen Stand auf `main` (Skill `sitzung-abschliessen`, Abschnitt 4).“ **Wer eine Tochtersitzung startet, steuert sie:** Die Hauptsitzung gibt Richtung und Freigaben weiter, liest den Bericht und gibt dem Autor das Nötige weiter. Der Autor kann jederzeit selbst übernehmen.
- **Innerhalb eines Takts schreibt die Sitzung selbstständig:** Szenen, Gespräche und kleine Erfindungen entscheidet sie selbst. Auch der Plan darf sich dabei ändern. Nur bei großen Fragen meldet sie sich über die Hauptsitzung: etwas widerspricht dem Kanon. Im Bericht nennt sie, wo sie sich Freiheit genommen hat.

### Überarbeitung eines Kapitels („Kapitel X überarbeiten“)
Welches Kapitel dran ist, zeigt `pruefen.py ueberarbeiten`, nach dem Feld `dringlich:` (Skill `weltenbau`, Abschnitt 1) oder, wo es fehlt, geschätzt: „bald“ gern gleich nach dem Schreiben, bevor das nächste Kapitel darauf baut, „später“ gesammelt, wenn es passt. Nach dem Überarbeiten fällt `dringlich:` weg. Wird ein Kapitel ohnehin überarbeitet, darf die Sitzung Grobes aus früheren Kapiteln derselben Sicht mitnehmen, aber nur, wenn es sich gezielt erledigen lässt (Stelle über Kommentar, `grep` oder Szenenmarke; `pruefen.py paket kNN --szene sN` gibt nur diese Szene mit Nachbarn und Anmerkungen); Kleines wartet, bis das Kapitel sowieso ganz gelesen wird. Etwa so, in einer Tochtersitzung mit Opus, ein Kapitel pro Durchgang:
1. Kapitel, `korrekturen:`, `notizen:` und alle Kommentare im Text lesen (`<!-- [A] … -->`, `{{ … }}`; `<!-- [C?] … -->` sind Vorschläge, umsetzen, wo sie tragen), dazu das Paket (Skill `schreiben`, Abschnitt 1). Ohne eigenen Plan: Die Anmerkungen sind der Auftrag. Was davon unklar ist oder den Kanon ändern würde, über die Hauptsitzung beim Autor nachfragen, den Rest umsetzen. Verweise „prüfen: …“ sind Merker: die genannte Regel selbst lesen und anwenden, wo das Kapitel betroffen ist.
2. Überarbeiten nach dem Skill `schreiben`; die Kapitel dürfen länger werden (Gespräche, Übergänge).
3. Bei Bedarf einen `pruefer` (Abschnitt 5); Kleines setzt die Sitzung selbst um, was den Kanon berührt, kommt in den Bericht.
4. Steckbrief, `szenen:`, Szenenmarken und Bericht nach Abschnitt 4.

### Sitzungen schneiden
- Überarbeitungen dürfen sich in einer Sitzung folgen, am besten je Perspektivfigur. **Ein neues Kapitel beginnt in einer frischen Sitzung**, die nur die fertigen Fassungen liest: Wer gerade überarbeitet hat, trägt die alte Fassung und die erledigten Korrekturen noch im Kontext und schriebe sie sonst ins neue Kapitel zurück. Etwa: eine Sitzung überarbeitet Kapitel 4, eine frische schreibt Kapitel 6.
- Vor jedem weiteren Kapitel schaut die Sitzung auf ihren Kontext (Anzeige oder `get_usage`). Ist er unter etwa 40 % voll, darf sie ein weiteres beginnen. Sonst schließt sie ab, und die Hauptsitzung startet eine frische mit kurzem Auftrag. Ein angefangenes Kapitel wird zu Ende gebracht.
- Ist das Nutzungslimit fast erreicht (etwa über 85 %), beginnt kein neues Kapitel.

## 4. Steckbrief, Wissensdateien, Bericht
- **Steckbrief** nach `_vorlagen/szene.md`: `status: entwurf`; `ziel`, `figuren`, `orte`, `zeit`, `geld` (kurz; ändert sich nichts, „wie zuvor“), `zusammenfassung` (5–8 Sätze, die ersten ein, zwei fassen das Kapitel zusammen), `schlussbild`, `erzaehlt` (nur, was das Kapitel neu über die Welt zeigt, ein paar Stichworte), `szenen:` (je Szene eine Zeile, Ort zuerst und Doppelpunkt, vor allem das Wissen: „X erfährt: …“, „Leser erfährt: …“, wo der Leser mehr weiß als die Figur) und im Text die Marken `<!-- s1 -->`. **Gelöscht werden** `brief`, `welt`, `plan`, `spuren` (die gelegten Spuren gehören nach `30_struktur/faeden.md`) und `neue_elemente` (nach dem Eintragen). `notizen`, `korrekturen` und `bericht` bleiben stehen, solange etwas offen ist; bei Ausbau erledigte `korrekturen` und Kommentare im Text löschen. Leseprobe: `titel`, `art: leseprobe`, `stil`, `verfasser`, `zweck`, `ziel`, `figuren`, `orte`, `notizen`.
- **Neue Welt** (Namen, Orte, Gegenstände, Vorgeschichte, Aussehen, Regeln): Prüffrage: Muss ein Schreiber das wissen, dessen Kapitel nicht hier spielt? Nur dann kommt es ohne Kapitelvermerk in die passende Wissensdatei, klein und stimmig als `[C✓]`, sonst als `[C?]` (`AGENTS.md`). Sonst bleibt es im Kapitel und unter `erzaehlt:`; es gilt trotzdem. Neue Namen kommen immer ins `glossar.md` (eine Zeile); danach `pruefen.py alles`. **Gesten, Stimmungen und Verhalten einer Szene tragen wir nicht ein**, sie stehen im Kapitel. Auch was eine Figur im Gespräch beiläufig von sich erzählt, bleibt im Kapitel, außer es soll später tragen; ein Ereignis wird so nicht zur Eigenschaft einer zweiten Figur (Stilprofil, „Ein Ereignis wirkt nach“). Im Zweifel weniger eintragen.
- Die Übersicht in `erzaehlt.md` und den Index baut das Skript beim Sitzungsabschluss neu (Skill `sitzung-abschliessen`), sobald sich ein Kapitel geändert hat. Den Stand schreibt am Ende eines Takts ein Subagent (Abschnitt 5).
- **Bericht** unter `bericht:` in die Kopfdaten, damit er erhalten bleibt, und an den Autor, kurz: Titel, Wortzahl, ein Satz Inhalt; was erfunden wurde, eigens genannt neue Wendungen der Handlung, geänderte Wegmarken oder Fixpunkte und neue Geheimnisse oder Verbindungen; höchstens drei Stellen, an denen man unsicher war oder vom Plan abwich, mit Grund; wo sich die Sitzung Freiheit genommen hat; was sie gestartet hat; höchstens drei Vorschläge, gern als **Ausblick**: wohin der eigene Strang als Nächstes könnte und was das Kapitel anderen Sichten anbietet (eine Begegnung, eine Spur), je mit Empfehlung.
- **Hakte ein Werkzeug** (im Paket fehlte etwas, `akte` fand Falsches, eine Regel stand im Weg), dazu eine Zeile in `_system/hinweise.md`. Nur, was nicht klappte.

## 5. Subagenten, Kritik und Prüfung
Ein Subagent lebt so lange wie die Sitzung, die ihn gestartet hat. Mit einer Folgenachricht (`SendMessage`) bekommt er das nächste Kapitel und liest nur das Neue. Das ist billiger und meist besser als ein neuer Start. Keiner ist Pflicht; die Sitzung nimmt, was der Text braucht, und nennt im Bericht, was sie gestartet hat.
- **`pruefer`, Art `sprache`** (Haiku): je Kapitel ein frischer Lauf (kurzer Haiku-Lauf, kein Weiterfüttern), erst wenn niemand mehr am Kapitel ändert; zum Test darf dasselbe Kapitel ein zweites Mal laufen, um zu sehen, ob er noch etwas findet; das Ergebnis im Bericht nennen.
- **`pruefer`, Arten `kanon` und `rueckbezug`** (Sonnet): einmal am Ende des Takts über die neuen Kapitel, mit dem Index. `kanon` löst dabei die Merker `<!-- ? … -->` auf (Skill `schreiben`, Abschnitt 1, „Nachher“).
- **`pruefer`, Art `stand`** (Sonnet): einmal am Ende des Takts. Gibt den neuen Stand als Text zurück; die Sitzung trägt ihn in `erzaehlt.md` ein.
- **`pruefer`, Art `erstleser`** (Haiku): bei Bedarf, vor allem für die ersten Kapitel und Kapitel mit viel Neuem; liest nur das Kapitel und meldet, wo ein neuer Leser nicht mitkommt und was zu viel auf einmal war.
- **`Explore`** (Haiku): ein Suchagent für den ganzen Takt, wenn `akte` nicht reicht.
- **`kritiker`** (Sonnet): bewertet die Wirkung auf den Leser und gibt einen Ausblick. Selten und nur mit dem Ja des Autors: einmal am Ende eines Takts vor der Ernte (die Kapitel des Takts ganz, alles Frühere über Steckbriefe), selten ein Buchlauf ohne Kapiteltext (etwa am Ende eines Teils); nach einem Begegnungskapitel gern ein Lauf ab Figur und Startkapitel, der von der Gegenseite nur die gemeinsamen Szenen liest; bei einer großen Szene oder wenn der Autor zweifelt auch gezielt. Claude nennt Kapitel, Schwerpunkt und Modell. Danach: „Stellen im Text“ als Kommentare `<!-- [C?] grob|klein · … -->` ins Kapitel (bei vielen ein Sonnet-Helfer), Befunde ohne Stelle unter `korrekturen:`, `dringlich:` setzen, im Kopf `kritik: <Datum>`; Muster, Begegnungen und Ausblick gehen in die Ernte (Skill `weltenbau`, Abschnitt 3a).
- **Begegnungskapitel:** Zeigt ein Kapitel eine Szene, die ein anderes aus anderer Sicht schon erzählt hat, liest der `pruefer` (`rueckbezug`) beide Stellen nebeneinander.
- Kleine Prüferbefunde setzt die Sitzung selbst um; sonst die wichtigsten drei nennen und fragen.

## 6. Abschluss
- Bei Neufassung: alte Datei löschen (Git hat sie).
- `STAND.md` anpassen, Commit mit kurzer Nachricht, `git push`; eine Tochtersitzung bringt ihren Zweig auf `main`.
- Auf Wunsch: `python _werkzeuge/epub_bauen.py --kindle` (Kapitel) oder `--proben --kindle`.
