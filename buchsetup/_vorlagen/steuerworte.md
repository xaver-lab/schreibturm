# Steuerworte – Hilfe für den Autor

Spickzettel: so lenkst du, Claude schreibt. Keine feste Regel, nur eine Hilfe.

Prinzip: **Der Autor gibt Richtung und Entscheidung, Claude macht die Arbeit.** Ein Steuerwort steht am Anfang der Eingabe, danach frei gesprochen. Die Wörter sind so gewählt, dass die Spracheingabe sie kaum verwechselt. Ohne Steuerwort gilt wie bisher: Claude verdichtet die Eingabe und legt sie ab.

## Richtung geben

| Steuerwort | Was Claude tut | Beispiel |
|---|---|---|
| **Weiterdenken** … | entwickelt ein Thema in der Werkstatt weiter: zwei bis drei Varianten, eine Empfehlung, Folgen für Kanon und Kapitel | „Weiterdenken: die Arbeit der Mitbewohnerin“ |
| **Tiefer** … | baut eine einzelne Figur, einen Ort oder eine Gruppe aus: Ziel, Angst, Geheimnis, Alltag, Verbindung zur Hauptlinie | „Tiefer: die Wirtin“ |
| **Was wäre, wenn** … | spielt eine Änderung durch: was sie im Kanon, in der Storyline und in den Kapiteln verändert. Ändert noch nichts | „Was wäre, wenn die Schwester freiwillig gegangen ist?“ |
| **Mehr** … / **Weniger** … | dreht an einem Regler für Welt oder Ton und schlägt konkrete Änderungen vor | „Mehr Licht am Tag“, „Weniger Technik“ |
| **Freie Hand** … | Claude darf in diesem Bereich selbst erfinden und direkt in die Dateien und Texte schreiben. Kleines und Stimmiges gilt gleich, Größeres bleibt `[C?]`, der Autor prüft später gesammelt | „Freie Hand: die Nebenfiguren im Herrenhaus“ |

## Entscheiden

| Steuerwort | Was Claude tut |
|---|---|
| **Fest:** … | trägt die Aussage direkt als `[A]` in den Kanon ein |
| **Vielleicht:** … | trägt sie als `[A?]` ein |
| **Nehmen** (Punkt) | übernimmt einen Vorschlag als `[C✓]` und räumt die Werkstatt auf, z. B. „Nehmen: Variante A“ |
| **Ändern** (Punkt): … | übernimmt den Vorschlag in der Fassung des Autors als `[A]` |
| **Weg** (Punkt) | verwirft einen Vorschlag; löscht ihn und alles, was daran hängt, auch im Text |

## Schreiben

| Steuerwort | Was Claude tut |
|---|---|
| **Probe** … | schreibt eine Leseprobe (300–1.000 Wörter) zu Szene, Figur oder Ton |
| **Kapitel** … | schreibt oder überarbeitet ein Kapitel nach Kanon und Storyline; arbeitet dabei deine `{{ … }}`-Anmerkungen im Text ab |
| **Kritik** … | startet den Kritiker (Claude schlägt ihn auch selbst vor): Text, Schwerpunkte, Modell |

## Überblick

| Steuerwort | Was Claude tut |
|---|---|
| **Stand** (Thema) | zeigt in wenigen Zeilen, was zu einer Figur, einem Ort oder der Storyline feststeht und was offen ist |
| **Was fehlt?** | nennt die drei größten Lücken in Welt, Figuren oder Handlung |
| **Nächste Frage** | holt die nächste offene Frage aus `STAND.md` |
| **Übergabe** | schließt die Sitzung ab (aufräumen, `STAND.md`, sichern) |
| **Obsidian aktualisieren** | baut die Obsidian-Ablage `_obsidian/` neu (`_werkzeuge/obsidian_bauen.py`) |
| **Aufs Kindle** | baut das Buch und kopiert es auf den Kindle (`_werkzeuge/epub_bauen.py --kindle`) |
