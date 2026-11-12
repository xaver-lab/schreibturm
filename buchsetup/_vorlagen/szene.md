---
kapitel: 1
band: 1
titel:
perspektive:          # welche Figur
wegmarke:             # Kennung der Wegmarke (E3, T2 …) in 30_struktur/buchstruktur.md; leer, wenn der Strang frei läuft
fixpunkt:             # nur, wenn ein Fixpunkt im Kapitel liegt (F1 …)
status: plan          # plan | entwurf | autor-bearbeitet | fest
verfasser: Claude     # Claude | Autor | gemischt
stil: S-02
ziel:                 # das grobe Ziel des Kapitels, ein Satz: was ändert sich für die Figur, welcher Schritt in ihrem Bogen
figuren: []           # wer vorkommt; bestimmt, welche Dateien in 20_figuren/ geladen werden
orte: []              # wo es spielt; bestimmt, welche Dateien in 10_welt/orte/ geladen werden
zeit:                 # Tag und Tageszeit am Anfang und Ende, nach der Zeitrechnung in AGENTS.md, Abschnitt 0
geld:                 # was die Perspektivfigur am Ende hat und schuldet, kurz; ändert sich nichts: „wie zuvor“
zusammenfassung: >    # 5–8 Sätze; die ersten ein, zwei Sätze stehen in der Übersicht (30_struktur/erzaehlt.md)
  …
schlussbild:          # das letzte Bild des Kapitels in einem Satz; der nächste Plan wählt gern ein anderes
erzaehlt:             # was das Kapitel neu über die Welt zeigt, ein paar Stichworte; die Art (gezeigt, Gerede, erklärt) nur, wo sie zählt; pruefen.py gezeigt
  -
szenen:               # je Szene eine Zeile, Ort zuerst mit Doppelpunkt: was geschieht, Figuren, Faden, Wissen („X erfährt: …“); pruefen.py index
  -
notizen:              # Rückmeldungen des Autors, verdichtet; solange etwas offen ist
  -
korrekturen:          # offene Änderungen und Verweise „prüfen: …“; was hier steht, ist noch nicht drin; nach dem Einarbeiten löschen
  -
dringlich:            # bald oder später, nach dem Lesen der Anmerkungen (Skill weltenbau, Abschnitt 1); nach dem Überarbeiten löschen
kritik:               # Datum des letzten kritiker-Laufs über dieses Kapitel
bericht:              # Bericht des Schreibers (Unsicherheiten, Erfundenes, gemeldete Fälle); bleibt, bis der Autor geantwortet hat
  -
brief:                # Brief, Welt, Spuren, Plan, neue_elemente gelten nur, solange das Kapitel entsteht, und werden danach gelöscht. Brief: vom Weltenbau angelegt: das Wenige, das die Szene aus dem Wissen braucht
  leser_weiss: >      # was der Leser vorher schon weiß (zwei, drei Sätze)
    …
  figuren:            # je Figur ein Satz: wer sie gerade ist, was sie will, wie sie zur Perspektivfigur steht
    -
  welt:               # zwei, drei Angebote, je mit Quelle; eins oder zwei davon tragen die Szene
    -
  moeglichkeiten:     # aus der Wegmarke oder der Richtung; eine oder zwei wählen
    -
spuren: []            # leise Hinweise auf später; nach dem Schreiben gehören sie nach 30_struktur/faeden.md
plan:                 # nur bei Bedarf, wenige Zeilen: je Szene Art und Wollen → Widerstand → Wendung, Schlussbild
  -
neue_elemente:        # nur neue Welt, die ein späteres Kapitel an anderem Ort wissen muss (wiederkehrende Namen, Orte, Regeln, Vorgeschichte), nach `AGENTS.md`, Abschnitt 2 in die Wissensdateien eingetragen ([C✓] oder [C?]); Einzelheiten nur dieser Szene bleiben im Kapitel
  -
---

# Kapitel 1: Titel

<!-- s1 -->
Text …

<!-- s2 -->
Text …

<!-- Kommentar des Autors zu einer Stelle, auf eigener Zeile hinter dem Absatz:
[A] „Anfang des Satzes …“: was sich ändern soll -->

<!--
Vorschläge von Claude bei Status "autor-bearbeitet":
> [C?] Vorschlag: …
-->
