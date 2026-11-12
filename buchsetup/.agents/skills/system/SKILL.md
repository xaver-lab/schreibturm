---
name: system
description: Kümmert sich um das KI-Setup des Buchprojekts, auch um sich selbst – Störungen beheben (Skill oder Skript fehlt oder streikt, Python fehlt), nach einer neuen Version suchen, laden und einarbeiten, ein neues Buch einrichten, den Nutzer nach seiner KI-Erfahrung fragen und Erklärungen danach anpassen, prüfen, ausmisten, Blick von außen, als Vorlage ausgeben. Verwenden bei Fragen zu Setup, System, Skills, Skripten, Version, „gibt es etwas Neues?“, „es geht nicht“, beim ersten Start eines unfertigen Buchs und beim Weitergeben an andere; nicht für Welt, Figuren oder Kapitel.
---

# System

**Auftrag:** Das ganze Setup laufend besser machen: `AGENTS.md`, alle Skills, Agenten, Vorlagen und Skripte, auch diesen Skill selbst. Besser heißt meist kleiner, klarer und passender zum Buch, wie es gerade ist; neu denken und streichen ist erwünscht, auch bei Abläufen, die einmal gut waren. Das Setup ist Werkzeug, nicht Werk: Es soll klein bleiben und sich mit dem Buch ändern. Lockern und streichen geht vor neuen Regeln (`AGENTS.md`, Abschnitt 6). Die Arten unten sind Richtschnur; nimm, was zur Frage passt, oft mehrere nacheinander.

**Kern und Buch.** Kern ist, was bei jedem Buch gleich ist: Skills, Agenten, Vorlagen, Skripte, `AGENTS.md` ohne Abschnitt 0. Buch ist Abschnitt 0, `_werkzeuge/projekt.json` und alle Inhaltsordner. Namen aus dem Buch gehören nicht in den Kern; braucht ein Skill ihn, verweist er auf Abschnitt 0.

Wissensdateien (Welt, Figuren, Struktur) pflegt `weltenbau`, ihren Bestand prüft der `pruefer` (Art `bestand`). Hier geht es um die Steuertexte.

**Ablage.** Der Skill hat einen eigenen Ort, getrennt von der Buch-Werkstatt: `_system/werkbank.md` (offene Vorhaben am Setup, Ideen, Messungen; nur dieser Skill schreibt hier) und `_system/hinweise.md` (Eingang: was Sitzungen an Werkzeugen gemeldet haben). Setup-Aufträge aus anderen Sitzungen gehören dorthin, nicht nach `STAND.md` oder `01_werkstatt/`. Nur dieser Skill liest beide; andere Sitzungen, vor allem Schreiber, bekommen davon nichts zu sehen (es wäre falscher Kontext).

**Zu Beginn** beide lesen: erst die Hinweise, dann „Offen“ in der Werkbank; mit dem Autor wählen, was heute dran ist.

## Den Nutzer kennenlernen (Erklärtiefe)
Wer das Setup benutzt, ist verschieden erfahren. Beim Einrichten und immer, wenn `nutzer.erfahrung` in `_werkzeuge/projekt.json` leer ist, eine Frage: „Wie vertraut bist du mit KI-Assistenten, die Dateien bearbeiten?“ (neu dabei / etwas / viel) und dann `erfahrung` auf `einsteiger`, `geuebt` oder `profi` setzen.
- **einsteiger:** Vor einem Schritt ein Satz, was passiert und warum; Fachwörter (Git, Skript, Skill, Branch) vermeiden oder einmal erklären; nach getaner Arbeit ein Satz in Alltagssprache.
- **geuebt:** Knapp; erklären nur, was neu oder riskant ist.
- **profi:** Keine Erklärungen, Fachsprache, nur Befunde und Entscheidungen.
- **Bekanntes fällt weg:** Was einmal erklärt wurde oder was die Person kennt („kenne ich“), kommt in `nutzer.bekannt` und wird nicht wieder erklärt. Sagt die Person, es sei zu viel oder zu wenig, `erfahrung` sofort ändern.
Das Niveau gilt für alle Skills (`AGENTS.md`, Abschnitt 4); der Kern bleibt auf Profi-Niveau sauber, nur die Antworten passen sich an.

## Störungen
Meldet jemand „es geht nicht“ (Skill nicht gefunden, Skript bricht ab, Python fehlt): erst `python _werkzeuge/system.py pruefen`, dann die Ursache an ihrer Stelle beheben und der Person in ihrer Erklärtiefe sagen, was war. Skills fehlen? Prüfen, ob der Skill-Ordner da ist (`.agents/skills/` bei Codex, `.agents/skills/` bei Claude Code); sonst direkt die `SKILL.md` lesen und danach arbeiten. Was am Kern liegt, eine Zeile in `_system/hinweise.md` für den Betreuer der Vorlage.

## Neue Version
Bei „gibt es etwas Neues?“, nach einem Hinweis auf eine neue Version oder zu Beginn einer Sitzung, wenn länger nichts geprüft wurde: `python _werkzeuge/system.py version` vergleicht die lokale `VERSION` mit dem neuesten Release (Quelle: `system.quelle` in `projekt.json`, `besitzer/repo`; ist sie leer, die Person nach dem Link fragen). Gibt es eine neuere, die Änderungen aus `AENDERUNGEN.md` in der Erklärtiefe der Person nennen und nach ihrem Ja `python _werkzeuge/system.py version --holen` (lädt und entpackt neben das Buch in `Buch-Setup-neu/`), dann Art „Einarbeiten“ (unten). Das Buch bleibt unberührt. Geht das Laden nicht, die Person bitten, das ZIP selbst zu laden und den Ordner zu nennen.

## Ideen des Autors weiterdenken
Die besten Sitzungen entstehen, wenn der Autor eine rohe Idee bringt und die Sitzung sie ernst nimmt, prüft und zu Ende baut. Was sich bewährt hat:
- **Gegen echte Daten prüfen, bevor es Regel wird.** Ein Muster an allen Kapiteln laufen lassen, einen Namen in einen echten Satz setzen, einen Helfer einmal rechnen lassen. Trägt es nicht, Besseres vorschlagen statt umsetzen; die Vorgabe des Autors ist Richtung, kein Wortlaut.
- **Den Kreislauf zu Ende denken.** Wer erzeugt es, wer liest es, wo liegt es, wann fällt es weg? Eine neue Ausgabe ohne Abnehmer oder ohne Ende wird Sediment; meist gibt es schon einen Ort (Kopffeld, Ernte, Werkbank), an den sie gehört.
- **Vorhandenes nutzen.** Neue Werkzeuge bauen auf Feldern, die es schon gibt (`szenen:`, `zeit:`, `perspektive:`, Szenenmarken), statt neue Pflichtfelder einzuführen.
- **Klein sofort, groß auf die Werkbank.** Was in ein paar Minuten steht, gleich bauen, testen, nennen; was länger dauert oder eine Wahl braucht, als eine Zeile unter „Offen“.
- **Fundlisten sind Hinweise.** Nach dem ersten Lauf messen, wie viel davon echt war, und streichen, was nur Gewolltes findet.
- **Arbeiten andere Sitzungen im selben Ordner, nur die eigenen Dateien committen** (bei einer geteilten Datei nur die eigene Zeile stagen).

## Prüfen
Zuerst `_system/hinweise.md`: Was Sitzungen dort gemeldet haben, an der Ursache beheben (Skript, Skill, Vorlage), erledigte Zeilen löschen; was den Autor braucht, als eine Frage. Dann `python _werkzeuge/system.py pruefen`: Skripte kompilieren, Ordner vorhanden, Hook-Skripte da, Verweise in Steuertexten zeigen auf echte Dateien, Längen über dem Richtwert, viele harte Wörter („immer“, „nie“, „muss“), Buchnamen im Kern. Das Skript findet, du urteilst: Ein Glossarbegriff, der zugleich ein gewöhnliches Wort ist, kommt nach `system.im_kern_erlaubt` in `projekt.json`. Danach bei Bedarf `pruefen.py alles` für das Wissen.

## Ausmisten
Steuertexte sind ein Cache dessen, was Ordner, Skripte und Vorlagen schon zeigen; sie tragen nur Gründe, Abläufe, Stolpersteine. Je Datei suchen:
- **veraltet** – Pfad, Befehl, Feld stimmt nicht mehr.
- **doppelt** – dieselbe Regel in `AGENTS.md` und Skill, oder in zwei Skills; eine Stelle behalten, die andere verweist.
- **Sediment** – Begründungen aus einem einzelnen Vorfall, erledigte Umbauten, Entscheidungsnummern ohne heutige Wirkung.
- **falscher Ladeweg** – in `AGENTS.md` (stets geladen), aber nur für eine Arbeitsweise nötig → in deren Skill; im Skill, aber nur selten nötig → in eine Vorlage hinter einen Verweis.
- **kürzbar** – Sätze ohne Wirkung auf das Verhalten.

Vorlegen: je Fund eine Zeile `Datei:Zeile · Art · Vorschlag`, die wichtigsten zuerst, höchstens zehn, dazu Wörter vorher → nachher. Kleines und Eindeutiges (veraltet, tote Verweise) gleich beheben und nennen.

## Blick von außen
Die typischen Fehler KI-gebauter Systeme:
- Regeln wachsen nur an: Jeder Fehler bringt eine Regel, gestrichen wird keine.
- Flicken statt Ursache, Ausnahme auf Ausnahme.
- Eine einmalige Korrektur des Autors wurde Dauerregel („nie X“, Schrittliste nach einem Vorfall).
- Mechanik statt Urteil: Prüfschritte, die jedes Mal laufen, obwohl sie nur manchmal helfen.
- Falsches Zusammenspiel: Der Autor wird bei Routine gefragt oder bei Wichtigem nicht.
- Scheu vor dem Löschen: Bestehendes wird nur ergänzt, nicht neu gedacht.

Prüffrage für jeden Schritt, der jedes Mal läuft: Was geht schief, wenn er einmal ausfällt? Suchen nach „immer“, „nie“, „muss“, „vor jedem“, „erst wenn“, Pflichtfeldern in Vorlagen. Einordnen als **Leitplanke** (schützt Kanon, Manuskript, Git; behalten), **Ablauf** (→ „bei Bedarf“), **Sperre** (nötig?) oder **Widerspruch** (angleichen).

Ausgabe: drei Sätze Bild (wofür, wie Teile und Autor zusammenspielen, wo es hakt), dann Funde wie beim Ausmisten, dann was als Leitplanke bleibt.

## KI-Buchmuster
Fällt dem Autor im Text ein Muster auf, wird es nicht nur im Kapitel geflickt, sondern dort behoben, wo es entsteht: meist ein Satz im Wissen, im Brief oder in einer Regel. Bekannte Muster:
- **Ein Detail färbt alles.** Ein Dieb in einer Szene, und das ganze Kapitel ist von Angst vor Verbrechen durchzogen; dunkle Gassen, Armut und Gefahr verbinden sich zu einer Grundstimmung, die die Welt gar nicht hat. Ursache: Das Wissen nennt Stimmungswörter ohne Gewicht, oder ein Szenendetail wandert in den Brief, und der Schreiber liest jedes Wort als Auftrag. Gegenmittel: im Wissen das Gewicht dazuschreiben („Alltag, am Rand“), Stimmungswörter durch konkrete Dinge ersetzen; beim Schreiben die Dosis-Prüfung (Skill `schreiben`, Abschnitt 3). Früh sichtbar in `pruefen.py woerter` (Stimmungswörter je Kapitel, ↑ bei Ausreißern).
- **Dieselbe Beschreibung in neuen Worten.** Ein Ort aus dem Wissen wird in jedem Kapitel, in dem er vorkommt, neu vorgestellt, jedes Mal anders formuliert. Die Echo-Prüfung schlägt nicht an, der Leser hört es trotzdem zum dritten Mal. Ursache: Der Schreiber liest die Beschreibung im Wissen und weiß nicht, dass der Leser sie schon kennt. Gegenmittel: „Was der Leser schon kennt“ im Paket und `pruefen.py akte <name>` (Skill `schreiben`, Abschnitte 1 und 2), Bekanntes benutzen statt erklären; das Wissen behält die Beschreibung, sie gilt weiter. Im Zweifel knapper: Eine Abweichung findet später der `pruefer` (Art `rueckbezug`), eine Wiederholung bemerkt der Leser sofort.
- **Nachdeuten.** Eine Szene zeigt etwas, dann sagt ein Satz am Absatzende, was es bedeutet („Sie verstand, dass …“). Der Leser fühlt sich belehrt, die Szene verliert ihr Gewicht. Ursache: Der Schreiber will sicher sein, dass es ankommt. Gegenmittel: Satz im Stilprofil („Gilt für alle Profile“); früh sichtbar in `pruefen.py text` („Nachdeuten am Absatzende“, Fundliste, kein Verbot).
- **Füllgesten.** Figuren zucken mit den Schultern, atmen aus, wischen sich die Hände, tun etwas „ohne hinzusehen“, damit die Szene in Bewegung bleibt; jede für sich harmlos, über das Buch ein hörbarer Tick. Ursache: KI-Gewohnheit, verstärkt durch Wissen, das „Gesten“ als Eigenschaft nennt (eine Figur „beobachtet Gesten“, und der Schreiber liefert welche). Gegenmittel: solche Sätze im Wissen durch das Konkrete ersetzen, was die Figur bemerkt; Satz im Stilprofil; Fundliste „Füllgeste“ in `pruefen.py text`, über das Buch in `woerter`.
- **Ein Wort für zwei Dinge.** Ein Name ist zugleich ein gewöhnliches Wort oder meint an anderer Stelle etwas anderes (die Schenke und die Kessel einer Werkstatt). Der Leser stolpert, die Suche mischt beides. Gegenmittel: `pruefen.py woerter`, Abschnitt „Vielleicht doppelt vergeben“; für eines einen eigenen Namen, im Glossar und in `projekt.json` als Alias.

**Kapitel kommentieren, nicht umschreiben.** Den Kapiteltext ändert dieser Skill nicht. Funde in Kapiteln kommen als Kommentar `<!-- [C?] klein · … -->` hinter den Absatz (Form: `_vorlagen/textregeln.md`) und als Merker „prüfen: …“ unter `korrekturen:`; eingearbeitet wird, wenn der Autor „Kapitel X überarbeiten“ sagt.

**Helfer und Sitzungen.** Bei vielen Funden darf ein Sonnet-Helfer sie auswerten und kommentieren (Muster, Befehl und Kommentarform mitgeben, das Urteil bleibt bei ihm, im Zweifel lassen); ein paar Funde sieht die Sitzung schneller selbst durch. Ob man ihn weiterfüttert oder frisch startet, entscheidet die Sitzung. Was für sich steht und länger dauert (ein neues Skript, ein Umbau über viele Dateien), darf als eigene Sitzung laufen, die der Autor öffnen und steuern kann; was die Sitzung zum Weitermachen braucht, bleibt beim Helfer. Soll ein Helfer nach einer Pause wieder Aufträge bekommen, ist eine Sitzung meist günstiger, weil ihr Kontext länger warm bleibt (etwa eine Stunde statt fünf Minuten).

Meldet der Autor ein neues Muster, kommt es hierher (Muster, Ursache, Gegenmittel, Beispiel ohne Buchnamen), und das Gegenmittel an die Stelle im Kern, wo es wirkt; dort ein Satz, hier der Grund.

## Ausgeben
Nach einer Sitzung, die das Setup merklich verändert hat, oder wenn der Autor die Vorlage weitergeben will:
1. Prüfen (oben); Buchnamen im Kern zuerst beheben.
2. `python _werkzeuge/system.py ausgeben`: spiegelt den Kern nach `_system/kern/`, ersetzt Abschnitt 0 durch Platzhalter, leert `projekt.json`, streicht Verweise auf E-Nummern (beim Empfänger gibt es unsere `entscheidungen.md` nicht) und prüft die Kopie.
3. Erst wenn die Vorlage einmal ausgeliefert ist (der Autor sagt Bescheid): in `_system/AENDERUNGEN.md` oben eine Version (Datum) mit dem, was sich für den Empfänger ändert und was er tun muss; Kleinkram zusammenfassen. Davor genügt der Spiegel.
4. Lohnt eine Lehre über den Einzelfall hinaus, in `_system/gut-zu-wissen.md` als Satz mit Grund; noch nicht Gebautes in `_system/werkbank.md`. Beides kurz halten, Überholtes ersetzen, Erledigtes löschen.

## Einarbeiten
Eine Vorlage von außen (eine neue Fassung, ein Freund schickt seine) oder eine Rückmeldung:
1. Neue Fassung neben den eigenen Kern legen (Scratchpad) und je Datei vergleichen. Abschnitt 0, `projekt.json` und alle Inhaltsordner bleiben unberührt.
2. Je Änderung eine Zeile: was sie bewirkt, passt sie zu diesem Buch, Empfehlung (nehmen, anpassen, lassen). Eigene Anpassungen, die die neue Fassung überschreiben würde, eigens nennen.
3. Nach dem Ja übernehmen, `system.py pruefen`, kurz berichten.
4. Was dieses Setup besser macht als die Vorlage, als Zeile in `_system/rueckmeldung.md` für den Absender.

## Einrichten (neues Buch)
In einem Ordner mit der Vorlage, auf „Richte das Buch ein“ oder wenn Abschnitt 0 noch Platzhalter trägt: erst die Erfahrungsfrage (Abschnitt „Den Nutzer kennenlernen“), dann Git: `git --version` prüfen; fehlt es, die Person zum Download führen (https://git-scm.com/download/win, bei der Installation überall „Next“, Standard lassen, danach die App neu starten); ist es da und es gibt kein Repository, `git init -b main`, bei leerem `git config user.name` nach dem Namen fragen und lokal `user.name` und `user.email` (etwa `autor@lokal`) setzen, dann der erste Commit. Ohne Git läuft das Buch trotzdem, nur ohne Verlauf; die Person darf es später nachholen. Dann wenige Fragen, je Antwort eine Frage (Gattung, Reihe, wie viele Perspektivfiguren, wie viel eigene Welt, Stilvorbilder), dann Abschnitt 0 und `projekt.json` füllen und nur die Dateien anlegen, die das Buch schon braucht; der Rest entsteht mit dem Buch. Passende Bausteine aus `_system/buchtypen/`, falls es dort welche gibt. Danach `weltenbau`.

## Abschluss
Je Änderung eine Zeile: Datei, was jetzt gilt. In der Werkbank Erledigtes löschen, Neues unter „Offen“. Commit nach Skill `sitzung-abschliessen`.
