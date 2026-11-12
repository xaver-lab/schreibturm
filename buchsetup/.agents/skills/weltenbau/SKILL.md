---
name: weltenbau
description: Arbeitet am Buchprojekt, wenn gerade kein Text geschrieben wird – Welt, Figuren, Handlung, Struktur, Stil-Doku, Eingaben des Autors einarbeiten, Ernte nach einem Takt, Werkstatt-Entwürfe, Entscheidungen, Aufräumen der Wissensdateien. Zu Beginn jeder Sitzung ohne Schreibauftrag laden. Für Leseproben und Kapitel gilt stattdessen der Skill `schreiben`.
---

# Weltenbau

Für alle Sitzungen, in denen kein Kapitel und keine Leseprobe entsteht: Welt, Figuren, Handlung, Anweisungen und Doku. Die geltenden Entscheidungen stehen in `entscheidungen.md`.

**Schlanker Start:** Zu Beginn nur `STAND.md` und den Stand in `30_struktur/erzaehlt.md` lesen. Alles andere holt man, wenn der Autor es braucht: für eine neue Wendung etwa die Wegmarken des Strangs, die Fixpunkte und die Dateien der beteiligten Figuren, für eine Frage zum Text die Szene über `30_struktur/index.md`. Der Job ist, auf den Autor einzugehen und mit ihm Welt und Buch voranzubringen, nicht, alles im Kopf zu haben.

Drei Schichten, getrennt gehalten: **Welt** (`10_welt/`, `20_figuren/`: was immer gilt), **Plan** (`30_struktur/`: was geschehen soll, grob), **Erzählt** (`30_struktur/erzaehlt.md` und Index: was der Leser erlebt hat).
- Skripte bei Bedarf (`_werkzeuge/LIESMICH.md`): `pruefen.py alles` nach merklichen Änderungen; `obsidian_bauen.py` und `epub_bauen.py` nur auf Wunsch.

## 1. Eingaben des Autors einarbeiten
- In einzelne Aussagen zerlegen, auf den Kern kürzen, in die passende Datei: Festgelegtes als `[A]`, Vages („vielleicht“, „optional“, „maybe“) als `[A?]`; was Claude dazu ausarbeitet, als `[C✓]`. Dem Autor kurz zeigen, wie verdichtet und was gesetzt wurde.
- Notizen in `00_eingang/` danach löschen.
- **Kommentare zu Kapiteln**, je nach Reichweite:
  - zu einer Stelle: als unsichtbarer Kommentar auf eigener Zeile direkt hinter dem Absatz, `<!-- [A] „Anfang des Satzes …“: … -->`. Der Autor nennt Kapitel und ein paar Worte; die Stelle über die Worte finden, nie über Zeilennummern.
  - Hat der Autor selbst im Kapitel `{{ … }}` gesetzt (Schreibweise: `_vorlagen/textregeln.md`), gilt es wie ein Kommentar zu einer Stelle: noch nicht eingearbeitet, bis er „Kapitel X überarbeiten“ sagt. Mit `grep -n "{{"` zu finden; nie still entfernen.
  - zum ganzen Kapitel: unter `korrekturen:` als Ziel, gern mit Beispiel; was gefällt, unter `notizen:`.
  - für mehrere Kapitel (Stil, Figur, Welt): einmal in die Regel-Datei (Stilprofil, Stimme, Figur, Welt). In betroffene ältere Kapitel kommt höchstens ein kurzer Merker unter `korrekturen:`, beginnend mit „prüfen: …“. Er sperrt nichts: Die Sitzung, die das Kapitel überarbeitet, liest die Regel selbst. Neue Kapitel lesen sie beim Schreiben.
  - Wer die Anmerkungen eines Kapitels gelesen hat, setzt im Kopf `dringlich: bald` (Handlung, Aufbau, Übergänge, Kanon; bevor das nächste Kapitel darauf baut) oder `dringlich: später` (Wortwahl und Kleines, gesammelt), gern mit ein paar Worten Grund; `pruefen.py ueberarbeiten` sortiert danach. Kommt Neues dazu, neu bewerten.
  - Was noch unter `korrekturen:` oder als Kommentar im Text steht, ist noch nicht eingearbeitet. Umgesetzt wird erst, wenn der Autor „Kapitel X überarbeiten“ sagt.
- Stil-Eingaben gehen nach `50_stil/stilprofile.md` oder in die Stimme einer Figur (`50_stil/stimmen/`), als Richtung formuliert.

## 2. Das Wissen kompakt halten
- **Verdichten ist Daueraufgabe.** Wer eine Datei anfasst, schaut, ob sie dabei kürzer werden kann: Doppeltes zusammenlegen, Überholtes streichen, Einzelheiten auf den Kern bringen. Neues ersetzt lieber, als dass es anhängt. Das Wissen soll so knapp bleiben, dass ein Schreiber eine Datei ganz lesen kann.
- Jede Aussage steht an einer Stelle; andere Dateien verweisen darauf.
- **Offen lassen ist erlaubt.** Nicht jede Lücke füllen: Was die Schreiber selbst finden können, bleibt offen. Wo das besonders willkommen ist, markiert ein kurzer Abschnitt „Spielraum für Schreiber“ oben in der Datei.
- **Wohin damit?** Vor jedem neuen Eintrag kurz sortieren:
  - **Welt** (`10_welt/`, `20_figuren/`): was ein Schreiber braucht, dessen Kapitel nicht dort spielt, weil es wiederkehrt oder andere Kapitel bindet.
  - **Plan** (`30_struktur/`): was geschehen soll.
  - **Vorrat** (`30_struktur/vorrat.md`): Ausgearbeitetes, das gilt, aber noch in kein Kapitel gehört; ist es erzählt, wird es dort gelöscht.
  - **Brief**: was nur ein kommendes Kapitel trägt.
  - **nirgends**: was nichts trägt. Einzelheiten aus einer Szene bleiben im Kapitel und im Index; sie gelten, weil sie erzählt sind. Wer eine Datei anfasst, darf solche Zeilen dorthin zurückgeben.

  Kanon so kurz wie möglich, so lang wie nötig.
- **Aus Kapiteln kommt nur Welt herein:** Namen, Orte, Gegenstände, Vorgeschichte, Aussehen, Regeln, ohne Kapitelvermerk (woher etwas stammt, weiß Git). Gesten, Stimmungen und Verhalten einer Szene bleiben im Kapitel; der Schreiber läse sie sonst als Eigenschaft und wiederholte sie.
- **Gewicht mitschreiben:** Was in der Welt Alltag und kein Thema ist (kleine Diebe, Armut, Dunkelheit), steht auch so da („Alltag, am Rand“), am besten als konkretes Ding statt als Stimmungswort; ein bloßes Stimmungswort liest der Schreiber als Auftrag.
- Perspektivfiguren und große Ortsdateien haben oben „In Kürze“ (etwa fünf Zeilen), das der Schreiber liest. Bei Änderungen im Kanon nachführen.
- **Schwelle:** eigene Datei für eine Figur oder einen Ort ab etwa zehn Zeilen Inhalt, bei Perspektivfiguren oder auf Wunsch des Autors; davor `20_figuren/nebenfiguren.md` bzw. die Datei des Bereichs (`AGENTS.md`, Abschnitt 0).
- **Deckel:** höchstens acht Entwürfe (inklusive Leseproben) in `01_werkstatt/`, höchstens fünf Punkte unter „Wartet auf den Autor“ in `STAND.md` (Skill `sitzung-abschliessen`, Abschnitt 3). Wird es mehr, ältere Entwürfe zu offenen Fragen in den Wissensdateien verdichten und den Entwurfstext löschen.
- Leere Abschnitte und Platzhalter entfallen; beantwortete Fragen werden gelöscht, ihre Antwort steht im Kanon.
- Was ein Schreiber braucht, steht dort, wo der Skill `schreiben` liest (Stilprofil, Stimmen, Figuren, Orte, Struktur). `entscheidungen.md` ist für den Weltenbau.

## 3. Ideen entwerfen (Werkstatt)
1. Neue Konzepte und Varianten, zwischen denen der Autor wählen soll, entstehen in `01_werkstatt/`, nicht direkt in den Wissensdateien; Ausgearbeitetes ohne echte Wahl geht gleich ins Wissen. Der Autor entscheidet Teil für Teil; Übernommenes geht ins Wissen, der Entwurf wird gelöscht. Ersetzt eine Idee eine alte, wird die alte entfernt.
2. **Langsam entwickeln.** Keine vorschnellen Verbindungen, Geheimnisse oder Lore; höchstens eine neue Verknüpfung pro Vorschlag, nur wo sie sich ergibt. Offene Fäden: `30_struktur/faeden.md`.
3. **Jede Figur entwickelt sich.** Wer eine Figur vorschlägt oder ausbaut, nennt ihren Bogen: wo sie beginnt, was sie verändert, wo sie endet.
4. Ältere unentschiedene Vorschläge: Einzeiler unter „Ältere Ideen“ im passenden Werkstatt-Entwurf; Claude baut nicht darauf auf, bis der Autor einen aufgreift.
5. Ein Entwurf beginnt mit „Kurz: die drei wichtigsten Vorschläge“, damit der Autor Teil für Teil nehmen kann.

## 3a. Ernte nach einem Takt
Nach einem Takt (zwei, drei Kapitel) liest der Weltenbau Steckbriefe und Index und die Szenen nur bei Bedarf und fragt:
- **Was hat der Text Neues und Gutes gezeigt, das in die Welt gehört?** Nur, was wiederkehrt oder andere Kapitel bindet (Abschnitt 2, „Wer muss es wissen?“). Was klein und stimmig als `[C✓]` hereinkam, nennt die Ernte in ein, zwei Zeilen. Die neuen `[C?]` kommen gesammelt zum Autor, nach Gewicht sortiert: nehmen, ändern, weg. Abgelehntes wird sofort gelöscht, Übernommenes wird `[C✓]`.
- **Was im Plan hat sich durch den Text überholt?** Neue Wendungen aus dem Schreiben legt die Ernte dem Autor vor; was er nimmt, kommt nach `30_struktur/handlung.md` oder `buchstruktur.md`. Hat ein Schreiber einen Fixpunkt geändert, zieht die Ernte die anderen Stränge nach.
- **Was liegt still?** `pruefen.py faeden` nennt Fäden, die lange nicht berührt wurden, `vorsprung` was der Leser einer Figur voraus hat; beides sind Kandidaten für den Ausblick, kein Auftrag.
- **Welche Geheimnisse und Verbindungen sind entstanden?** Sie kommen zum Autor; was er nimmt, kommt nach `30_struktur/faeden.md`.
- **War es zu viel auf einmal?** Bringen die Kapitel mehr Neues, als der Leser tragen kann, schlägt die Ernte vor, was zurückgeschnitten oder auf später verschoben wird.
- **Ausblick als Wahl:** Was Schreiber (Bericht) und `kritiker` (Ausblick, Begegnungen) für die Zukunft vorschlagen, legt die Ernte gebündelt vor: je Perspektivfigur zwei, drei Wege und mögliche Begegnungen, je mit Empfehlung, so knapp, dass der Autor einen wählt, umformt oder „Empfehlung“ sagt. Gewähltes geht in `30_struktur/handlung.md` oder `buchstruktur.md` und in die Briefe (`moeglichkeiten`); Ausgearbeitetes ohne Kapitel in den Vorrat; der Rest entfällt. Liest der Autor nicht gleich, steht der Ausblick in `01_werkstatt/ausblick.md` (eine Datei, bei jeder Ernte ersetzt).
- Danach ein kurzes Richtungsgespräch: Was bleibt, was formt der Autor um, wohin geht der nächste Takt? Wichtig ist die Welt, die das nächste Kapitel braucht; weiter voraus nur grobe Wege.

## 4. Entscheidungen
- Eine neue Entscheidung des Autors, die das Projekt prägt, bekommt einen Eintrag in `entscheidungen.md`: ein kurzer Satz, Verweis auf die Datei mit den Einzelheiten, in die passende Gruppe.
- „Bewusst verworfen“ nur für kleine Dinge, die sonst leicht wiederkehren, als Einzeiler.

## 5. Briefe für den Schreiber
Der Weltenbau kennt das ganze Wissen, der Schreiber bekommt das Wenige, das er braucht. Bevor ein Kapitel geschrieben wird, legt Claude die Kapiteldatei (`40_manuskript/kNN_kurztitel.md`, Status `plan`, Vorlage `_vorlagen/szene.md`) mit dem Feld `brief:` an:
- `leser_weiss`: was der Leser vorher schon weiß, zwei, drei Sätze (aus dem Stand in `erzaehlt.md`).
- `figuren`: je Figur der Szene ein Satz (wer sie gerade ist, was sie will, wie sie zur Perspektivfigur steht); Nebenfiguren nur, wenn sie reden oder handeln.
- `welt`: zwei, drei Angebote, die dieses Kapitel trägt, je mit Quelle, gern aus `30_struktur/vorrat.md`. Dinge, die der Figur begegnen; Hintergrund bleibt im Regal.
- `sicht`: nur bei einer Szene mit zwei Hauptfiguren ein Satz, warum diese Figur sie erzählt (`30_struktur/buchstruktur.md`, „Gemeinsame Szenen“).
- `moeglichkeiten`: die Möglichkeiten der Wegmarke oder der Richtung, aus denen der Schreiber eine oder zwei wählt; er darf auch einen eigenen Weg gehen. Wo die Szene sich anbietet, gern ein Hinweis auf Spielraum (etwa „hier darf ein neuer Ort entstehen“).
Den Abstand zum Vorgängerkapitel nimmt der Brief aus dessen fertigem Text (`zeit:`, Schluss); ist es noch nicht geschrieben, bleibt er offen („nach Kapitel N“). Der Brief bleibt kurz (etwa 150 bis 250 Wörter) und enthält nur Kanon oder deutlich als Angebot Gekennzeichnetes. Nach dem Schreiben wird er gelöscht.

## 6. Steuerung der Schreibsitzung
Die Hauptsitzung ist die Mitte: Agenten reden nicht untereinander, sie lesen und schreiben Dateien und berichten dem, der sie gestartet hat. Wer eine Schreibsitzung startet, steuert sie. Freigaben holt die Hauptsitzung beim Autor, möglichst als ein Klick: die Richtung vor einem Takt (oder „lauf einfach“), Opus für die Schreibsitzung einmal pro Takt, den Kritiker auf Vorschlag, den Kanon (gesammelt, Ernte), Befunde (die wichtigsten drei, Kleines setzt die Schreibsitzung um) und große Fragen mitten im Takt.

| Wer | Modell | Liest | Schreibt | Startet |
|---|---|---|---|---|
| **Autor** | – | Kapitel, Werkstatt, was die Hauptsitzung zeigt | `{{ … }}` in Kapiteln | spricht nur mit der Hauptsitzung |
| **Hauptsitzung** (`weltenbau`) | Opus | immer `STAND.md` und den Stand; sonst nur auf Bedarf Index, Welt, Plan, einzelne Szenen | Welt, Plan, Briefe, Werkstatt, `STAND.md`, `entscheidungen.md`, Korrekturen | Schreibsitzung, Sitzungen für Umbau und Sichtung, `pruefer` (Bestand, Rückbezug), `kritiker`, `Explore` |
| **Schreibsitzung** (`schreiben`) | Opus | das Paket (`pruefen.py paket kNN`), dann gezielt `akte` | Kapiteltext, Steckbrief mit `szenen:`, neue Welt nach, Bericht | `pruefer` (Sprache, Kanon, Stand), `Explore` |
| **`pruefer`** | Haiku oder Sonnet | nur, was seine Art braucht | nichts; meldet dem Starter (Art `stand`: gibt den Stand als Text zurück) | niemanden |
| **`kritiker`** | Sonnet | Kapitel, Steckbriefe der Nachbarn | nichts; meldet der Hauptsitzung | niemanden |
| **Skripte** (`pruefen.py`) | – | Kopfdaten aller Kapitel | Übersicht in `30_struktur/erzaehlt.md`, `30_struktur/index.md` | – |

## 7. Abschluss
Skill `sitzung-abschliessen`.
