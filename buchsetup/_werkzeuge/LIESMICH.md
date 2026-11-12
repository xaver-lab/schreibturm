# Werkzeuge

Was nur zu diesem Buch gehört (Titel, Autor, Dateiname des Buchs, Calibre-Pfad, Aliase und Kurznamen für Obsidian, Wörter, die nur zufällig Namen ähneln), steht in `projekt.json`. Die Skripte selbst bleiben allgemein.

## Buch auf den Kindle

Kindle per USB verbinden, dann:

```
python _werkzeuge/epub_bauen.py --kindle
```

Baut aus allen Kapiteln in `40_manuskript/` ein EPUB (`_werkzeuge/ausgabe/<Buchdatei>.epub`, Name aus `projekt.json`, ohne Datum; die vorige Fassung wandert dabei mit dem Datum ihrer Erstellung nach `ausgabe/archiv/`), wandelt es mit Calibre in AZW3 um und kopiert es als `<Buchdatei>.azw3` auf den Kindle. Die neue Fassung ersetzt die alte, es bleibt immer nur ein Buch dort. Das Cover legt das Skript zusätzlich als Vorschaubild in `system/thumbnails` des Kindle, sonst fehlt es in der Bibliothek. Danach wirft das Skript den Kindle selbst aus (Windows); erst wenn es „ausgeworfen“ meldet, abstecken.

Nur das EPUB bauen, ohne Kindle: `python _werkzeuge/epub_bauen.py`

Leseproben aus `50_stil/proben/` und `01_werkstatt/` als eigenes Buch: `python _werkzeuge/epub_bauen.py --proben --kindle`

Im Chat genügt: „Aufs Kindle“.

## Obsidian-Ablage zum Ansehen

```
python _werkzeuge/obsidian_bauen.py
```

In Obsidian den Ordner `_obsidian` als Ablage öffnen, Startseite „Übersicht“; ist Obsidian offen, mit Strg+R neu laden. Der Ordner wird bei jedem Lauf neu gebaut (nicht in Git), Änderungen darin gehen verloren. Claude liest `_obsidian/` nie.

Im Graph: Figuren orange, Orte blau, Kapitel grün, Fäden violett. Filter im Suchfeld, etwa `tag:#story-<name>` je Hauptperson (Rolle „Hauptperson“ in ihrer Datei) und für die Namen unter `story_extra` in `projekt.json`, `tag:#faden`, `tag:#kapitel`. Eigene Graph-Einstellungen bleiben erhalten; `--grafik-neu` setzt sie zurück.

**Graph abspielen:** Die Dateien bekommen Erstelldaten in Erzählreihenfolge (erst Hauptpersonen, dann je Kapitel: Kapitel, neue Figuren und Orte, dort angelegte Fäden). Im Graph unten auf „Animieren“ drücken, das Netz wächst mit der Geschichte. Geht nur unter Windows und macOS; mit `--ohne-animation` abschalten. Im Graph bleibt ein symmetrisches Gerüst: Kapitel verbinden ihre Figuren, Orte und Fäden, Fäden hängen an Kapiteln und einer Figur, alle anderen Notizen nur an den Hauptpersonen (der volle Text mit allen Links bleibt in den Notizen, nur Links zwischen Figuren, Orten und Gruppen sind dort schlichter Text). Standard: Es starten die Orte unverbunden als lose Punkte und werden erst im Kapitel mit den Figuren verknüpft; Fäden entstehen mit ihrem ersten Kapitel.

Im Chat genügt: „Obsidian aktualisieren“.

## Start-Check (läuft automatisch am Sitzungsbeginn)

`_werkzeuge/sitzung_start.py` wird über `AGENTS.md` (Codex startet es zu Beginn) gestartet. Es holt `origin`, bringt `main` per Fast-Forward auf den Stand von `origin/main` (nur bei sauberem Arbeitsbaum), listet alle Branches auf `origin` mit Commits, die nicht in `main` stehen, und mergt die, die sich ohne Konflikt einarbeiten lassen, lokal nach `main`. Konflikte werden nur gemeldet. Gepusht wird erst beim Sitzungsabschluss.

Von Hand: `python _werkzeuge/sitzung_start.py`

## Prüfskript (benutzt Claude selbst)

```
python _werkzeuge/pruefen.py text 40_manuskript/k01_kurztitel.md
python _werkzeuge/pruefen.py alles
python _werkzeuge/pruefen.py gezeigt [bis-kapitel]    # was über die Welt schon gezeigt wurde, pro Kapitel (Feld erzaehlt:)
python _werkzeuge/pruefen.py gezeigt Turm,Brücke      # nur dazu, und in welchen Kapiteln der Text es nennt
python _werkzeuge/pruefen.py paket k09               # Lektüre vor dem Schreiben in eine Datei: _werkzeuge/ausgabe/paket_k09_….md
python _werkzeuge/pruefen.py woerter [k04]           # Wörter zählen: häufig, Lieblingswörter gegen gewöhnliches Deutsch (daten/de_50k.txt), doppelt vergeben, je Sicht, Stimmung je Kapitel, ähnliche Namen
python _werkzeuge/pruefen.py akte Brücke [--bis 4]    # alles zu einem Namen: Glossar, In Kürze, gezeigt, Szenen, Textstellen, Wissen
python _werkzeuge/pruefen.py ueberarbeiten           # je Kapitel offene {{ }}, Kommentare, Korrekturen, Merker; bald / später
python _werkzeuge/pruefen.py weiss <Figur> [--bis 8]   # was eine Figur erfahren hat (Zeilen „X erfährt …“ in szenen:)
python _werkzeuge/pruefen.py wiederholung k09        # Sätze um Glossarorte hier und in früheren Kapiteln, für einen Haiku-Prüfer
python _werkzeuge/pruefen.py szene k07 s3 --um 1      # eine Szene mit Nachbarszenen ausgeben (Marken <!-- sN -->)
python _werkzeuge/pruefen.py treffen <Figur>         # Szenen, in denen Figuren zusammen vorkommen (Index oder Text); <Figur>,<Figur> für ein Paar
python _werkzeuge/pruefen.py paket k03 --szene s4    # Paket für eine Szene: Szene mit Nachbarn, ihre Anmerkungen, Stil und Stimme
python _werkzeuge/pruefen.py zeitleiste             # alle Szenen aller Sichten nach Tag; markiert Tage mit mehreren Sichten
python _werkzeuge/pruefen.py vorsprung [<Figur>]   # was der Leser weiß und die Figur (noch) nicht
python _werkzeuge/pruefen.py faeden                 # Fäden je Strang: lange still (gezählt in Kapiteln des Strangs) und ohne Auflösung
python _werkzeuge/pruefen.py erzaehlt [--schreiben]   # Übersicht je Kapitel (Wegmarke, Fixpunkt, Sicht, Tag, Geld, Kurzfassung); --schreiben baut sie in 30_struktur/erzaehlt.md und lässt den Stand oben stehen
python _werkzeuge/pruefen.py index                    # baut 30_struktur/index.md aus den Feldern szenen: der Kapitel
```

Gesucht wird an Wortgrenzen mit Beugung (Kessel, Kessels, nicht Eisenkessel); Aliase aus `projekt.json` und Namen in Klammern im Glossar zählen mit.

Weitere Befehle: `namen` (Schreibvarianten, neue Namen, Verworfenes), `wissen` (Marker, leere Abschnitte, Kapitelvermerke, tote Verweise, Kleinstdateien, große Dateien, lange „In Kürze“ und Steckbriefe), `werkstatt` (Alter und Größe der Entwürfe, Deckel); `text` nimmt `--ziel` (Wortzahl, z. B. 4000-6000).

`text`: Länge (Kapitel ab 4.000 Wörtern, nach oben offen), Satzbau, überladene Sätze, Echos, Füllwörter, typische KI-Muster. `alles`: Schreibvarianten von Namen (auch in Werkstatt-Proben), verworfene Begriffe, Marker im falschen Abschnitt, tote Verweise, Kleinstdateien, Werkstatt- und STAND-Deckel. Das Skript zählt und findet, es urteilt nicht; seine Befunde sind Hinweise.

Anregungen für Prüfideen: Quill (Apache 2.0), Novel-OS (MIT), writing-template-for-ai (MIT). Nur Ideen, eigene Umsetzung.

## Setup prüfen und als Vorlage ausgeben

```
python _werkzeuge/system.py pruefen     # Skripte, Ordner, Hooks, Verweise, Längen, harte Wörter, Buchnamen im Kern
python _werkzeuge/system.py ausgeben    # Kern ohne Buchdaten nach _system/kern/, danach Prüfung der Kopie
```

Im Chat genügt: „Setup prüfen“ oder „Vorlage ausgeben“ (Skill `system`).

Was an Werkzeugen hakte, sammelt `_system/hinweise.md`; Vorhaben am Setup stehen in `_system/werkbank.md`. `system.py pruefen` meldet offene Punkte; andere Sitzungen sehen sie nicht.
