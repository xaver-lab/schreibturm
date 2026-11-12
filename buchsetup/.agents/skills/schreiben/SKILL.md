---
name: schreiben
description: Schreibt für das Buchprojekt eine Leseprobe oder ein Kapitel – lesen (Paket), schreiben, selbst prüfen; Auftrag, Takt, Steckbrief, Bericht und Prüfer nach `_vorlagen/schreibablauf.md`. Gilt im Chat ebenso wie in einer Tochtersitzung, die ein Kapitel schreibt. Verwenden, wenn der Autor eine Leseprobe, ein neues Kapitel, einen Ausbau oder eine Neufassung möchte.
---

# Schreiben

Dieser Skill ist das Handwerk: lesen, schreiben, selbst prüfen. Was davor und danach geschieht (Auftrag, Takt, Tochtersitzung, Überarbeitung, Sitzungen schneiden, Steckbrief, Bericht, Prüfer, Abschluss), steht in `_vorlagen/schreibablauf.md`: einmal vor dem Start lesen und wieder vor dem Abschluss. Dateien und Status: `_vorlagen/textregeln.md`. Welt, Pläne und Doku pflegt der Skill `weltenbau`. Wenig, passender Kontext trägt am weitesten.

## 0. Wer hier schreibt
Du erzählst im Grundton des Buchs (`AGENTS.md`, Abschnitt 0; Einzelheiten `50_stil/stilprofile.md`): klar, nah an einer Figur, mit Lust an Spannung und Bewegung. Die Sprache ist eine Fensterscheibe, durch die der Leser die Figur sieht. Vorbilder je Szenenart färben einzelne Szenen; alles andere läuft im Grundton. Die Wahrnehmung gehört immer der Perspektivfigur (`50_stil/stimmen/`).
- **Du stehst im Kopf der Perspektivfigur.** Du weißt, was sie weiß, und siehst, was sie bemerkt: das, was für sie gerade zählt, Gefahr, Ziel, ein Mensch.
- **Jede Szene beginnt mit einem Wollen.** Erst die Figur und was sie will, dann der Ort, durch ihren Blick.
- **Wenige Dinge, jedes mit Grund.** Wer im Bild sitzt, hat einen Grund, dort zu sitzen, und die Figur ahnt ihn oder fragt sich danach.
- **Ein Satz, ein Gedanke.** Ein Satz bringt eine neue Sache; die nächste bekommt ihren eigenen Satz.
- **Die Welt erscheint, wo sie zählt:** wenn sie der Figur im Weg steht oder hilft, in ein, zwei Einzelheiten.

Danach liest du Welt und Regeln. Sie sagen dir, *was* geschieht; dieser Abschnitt sagt, *wie* du es erzählst.

## 1. Lesen: vorher, während, nachher
Alles, was du liest, wirkt wie ein Auftrag. Darum gilt: **Was die Handlung trägt, vorher; was nur die Oberfläche färbt, erfinden und nachher prüfen lassen.**

**Vorher: das Paket.** `python _werkzeuge/pruefen.py paket kNN`, dann `_werkzeuge/ausgabe/paket_kNN.md` ganz lesen. Es enthält die Kapiteldatei mit Brief, den Stand und die Übersicht aus `erzaehlt.md`, Steckbrief und letzte Szene des vorigen Kapitels, eine Szene aus dem letzten Kapitel derselben Sicht, Stilprofil und Stimme, die „In Kürze“ der Figuren, Orte und Bereiche aus dem Kopf und je Figur und Ort, was der Leser schon kennt. Das genügt für den Anfang.
- Mehrere kurze Kapitel eines Ereignisses mit wechselnder Sicht: je Sicht das Paket ihres Kapitels.
- Leseprobe ohne Kapiteldatei: Stilprofil, Stimme und die „In Kürze“ der Figuren von Hand.
- Fehlt im Kopf eine Figur oder ein Ort, der auftritt, erst `figuren:` und `orte:` ergänzen, dann das Paket neu bauen.

**Während: nur, was ändert, was geschieht.** Kann die Figur das wissen? Geht das nach den Regeln der Welt? Reichen Geld und Zeit? Kam der Ort schon vor, und wie?
- **Erster Griff bei einem Namen:** `python _werkzeuge/pruefen.py akte <name>` (Ort, Figur, Ding; mehrere mit Komma, `--bis N` für den Stand des Lesers): Glossar, „In Kürze“, schon gezeigt, Szenen im Index, Textstellen mit Zeilen.
- Andere Fragen (Wie funktioniert ein Gerät? Was gilt im Rat?): `Grep` oder der passende Abschnitt in `20_figuren/`, `10_welt/` (Schauplatz, Bereiche und Technik laut `AGENTS.md`, Abschnitt 0), `30_struktur/handlung.md`, `30_struktur/faeden.md`, `glossar.md`; wo etwas geschah und wer es wusste, `30_struktur/index.md`.
- Reicht das nicht, etwa für eine Einzelheit aus älteren Kapiteln ohne festen Namen: ein Suchagent `Explore` (Haiku) mit konkreter Frage, für den ganzen Takt. Vor dem Aufbauen die Fundstelle selbst ansehen.
- **Aus jedem Fund nimmst du, was die Szene braucht, meist ein, zwei Dinge.** Der Rest bleibt im Regal.

**Nachher: die Oberfläche.** Farbe einer Tür, Zahl der Stufen, wer genau am Tisch saß, eine Schreibweise: erfinden und weiterschreiben. Wo du unsicher bist, ob es früher anders stand, ein Merker im Text: `<!-- ? Tür grün oder blau? -->`. Der `pruefer` (Art `kanon`) löst die Merker am Ende des Takts auf; Abweichungen und Wiederholungen findet er dort (Art `rueckbezug`).

`entscheidungen.md` und die Werkstatt liest man beim Schreiben nicht: Der Text entsteht aus Ideen.

## 2. Schreiben
### Wie man die Dateien liest
- **Kanon** (`[A]`, `[C✓]`): Tatsachen der Welt. Darauf baut man.
- **Ideen & Vorschläge** (`[A?]`, `[C?]`): Angebote. Man nimmt, was der Szene dient, und meldet neue Welt (`schreibablauf.md`, Abschnitt 4).
- Alles andere ist offen: Details, Nebenfiguren, Gerüche, Gesten, kleine Orte darf man erfinden. Auch Grundlegendes, das zu einer Figur fehlt (Alter, Aussehen, Herkunft).
- **Spielraum:** Welt und Geschichte sind bewusst nicht fertig. Bietet die Szene es an, darf man Neues setzen: Szenen, Schauplätze, auch größere, Alltag und Leben des Schauplatzes, Bräuche, Redewendungen, Geräte, Seiten der Technik oder Magie. Auch die Hauptgeschichte darf sich im Schreiben entwickeln: eine Wendung, eine Folge, eine Nebenfigur, die wichtiger wird. Das ist eine Option, kein Auftrag; meist reicht ein Ding pro Kapitel, und es muss zum Bestehenden passen. Abschnitte „Spielraum für Schreiber“ in einer Wissensdatei zeigen, wo es besonders willkommen ist. Auch Wegmarken und Fixpunkte dürfen sich so verschieben oder ändern, und es dürfen Geheimnisse und Verbindungen entstehen, langsam, eher als Spur denn als Enthüllung. Der Bericht nennt neue Wendungen, geänderte Fixpunkte und neue Geheimnisse oder Verbindungen; der Autor entscheidet bei der Ernte.
- **Offene Fragen** darf man in der Szene klein und vorläufig beantworten.
- **Der Kanon beschreibt, was gilt, nicht, was eine Figur in jeder Szene tut.** Steht eine Geste dort, ist sie ein Angebot, kein Zwang; ein Ereignis aus einem früheren Kapitel prägt die Figur, wird aber kein Leitmotiv.
- Große Zusammenhänge (Geheimnisse, Verbindungen, Herkunft der Dinge) entfaltet man langsam: Bestehende zeigt man etwa so weit, wie Brief und Richtung es nahelegen; neue darf man anlegen, meist höchstens eine pro Kapitel.
- **Spuren** (`spuren:`) legt man so leise, wie dort steht: ein Detail, ein halber Satz, ein Blick.
- Stößt der Text auf einen Widerspruch zum Kanon: kleine Fälle nach eigenem Ermessen lösen und melden; große (wer was weiß, warum etwas geschah, wie etwas aussieht oder heißt) erst mit dem Autor klären. Kanon ändert man nie still. Der Plan (Wegmarken, Fixpunkte, Bogen) ist dagegen Richtung: Ihn darf der Text ändern, der Bericht nennt es.

### Wie man schreibt
- Schreibart nach Abschnitt 0, `50_stil/stilprofile.md` (S-02, Vorbild je Szenenart) und der Stimme der Perspektivfigur: ernst, atmosphärisch, tiefe dritte Person, eine Sicht pro Kapitel; bei großen Ereignissen wechseln die Sichten über kurze Kapitel (`30_struktur/buchstruktur.md`), und jedes beginnt mit der neuen Figur und ihrem Wollen. Die Leitplanken geben Richtung, kein Korsett; es darf mit Lust geschrieben werden.
- Die Szene vor sich sehen, bevor man schreibt: Wo steht die Figur, was ist kalt, was leuchtet, was will sie gerade?
- Jede Szene verändert etwas für die Perspektivfigur (Bogenschritt). Spürbar machen, ohne ihn auszusprechen.
- Die Stimmung kommt aus der Situation: Gefahr knapp und körperlich, Nähe langsam und warm, Leichtigkeit aus den Figuren.
- **Die Welt erzählen:** Ein Stück Welt erscheint dort, wo es der Figur begegnet, konkret und benutzt. Menschen am Rand haben eine Haltung und einen Grund und reden. `welt:` im Brief ist ein Angebot: Ein oder zwei Punkte tragen die Szene.
- **Bekanntes benutzen, nicht neu vorstellen.** Was der Leser von einem Ort, Ding oder Ablauf schon kennt, steht im Paket („Was der Leser schon kennt“) oder in `akte <name>`. Dann wird es benutzt; neu ist meist nur ein Zug, den der Leser noch nicht kennt, oder was sich verändert hat. Im Zweifel knapper.
- Länge, Fixpunkte, Wegmarken, Sichtwechsel und Zeitsprünge nach `30_struktur/buchstruktur.md`.

### Erzählhandwerk (Hinweise)
- **Szenenwechsel:** Versteht der Leser sonst nicht, wo die Figur jetzt ist oder wie sie dorthin kam, hilft ein Halbsatz oder ein kurzer Absatz. Nach einer Spannungsstelle ist ein sanfter Übergang meist besser als ein harter Schnitt.
- **Zeitsprung:** Wo es passt, spürt man, wie viel Zeit vergangen ist und was sich zwischen den Figuren getan hat.
- **Erklären:** erst in der Szene zeigen. Trägt das nicht, hilft ein kurzer Absatz oder eine Rückblende aus Sicht der Figur, klar vom Jetzt abgesetzt.
- **Kapitelende:** Ein Schlussbild oder eine offene Frage ist schön, wo es sich ergibt.
- **Varianten:** Ist der Schreiber an einer Stelle unsicher, darf er für höchstens eine Stelle eine zweite Fassung schreiben, etwa 200 bis 400 Wörter, in `01_werkstatt/kNN_variante.md` (zählt zum Deckel). Im Kapitel steht die Fassung, die er für stärker hält; der Autor entscheidet.

## 3. Selbstprüfung
- `python _werkzeuge/pruefen.py text <datei>`: Echos, gleiche Satzanfänge, Floskeln, benannte Gefühle und überladene Sätze dort verbessern, wo sie stören. Länge gegen Ziel.
- **Dosis:** Zieht sich ein einzelnes Ereignis, eine Geste, eine Idee oder ein Stück Welt als Stimmung (ein Dieb, und plötzlich ist alles Gefahr und Armut) durch das ganze Kapitel, greifen plötzlich mehrere Figuren es auf, oder kehrt es in Kapiteln wieder, in denen es nichts trägt? Dann auf die Stellen zurückschneiden, die es brauchen (`50_stil/stilprofile.md`, „Ein Ereignis wirkt nach“).
- **Schon erzählt:** Wird etwas vorgestellt, das ein früheres Kapitel schon beschrieben hat, auch mit anderen Worten? Auf die Benutzung oder den neuen Zug kürzen.
- **Dichte:** Bringt das Kapitel zu viel Neues auf einmal (Szenen, Orte, Figuren, Wendungen, Geheimnisse)? Was nur dasteht und die Szene nicht trägt, streichen oder für später aufheben.
- Jeden Absatz fragen: Weiß der Leser, warum jede genannte Person und Sache da ist? Was die Figur nicht braucht, streichen. Sätze mit mehr als einer neuen Sache teilen.
- Einmal ganz lesen: Klingt es nach der Perspektivfigur? Trägt der Schluss? Knüpft der Anfang an das vorige Kapitel an? Versteht man an jedem Wechsel, wo wir sind?
- `ziel:` gegen den fertigen Text prüfen und, wenn nötig, anpassen.

Danach: Steckbrief, Wissensdateien, Bericht, Prüfer und Abschluss nach `_vorlagen/schreibablauf.md`, Abschnitte 4 bis 6.
