# Dein Buch-Setup für Codex

Ein Ordner, in dem Codex (die KI in der ChatGPT-Desktop-App) mit dir an deinem Roman arbeitet: Welt und Figuren aufbauen, Kapitel schreiben, prüfen, und über viele Sitzungen den Überblick halten. Alles liegt als Dateien in diesem Ordner, nichts im Netz. Du brauchst kein GitHub.

## Was du brauchst

1. **ChatGPT-Desktop-App mit Codex** (Windows). Codex ist ein Tarif-Feature; Plus oder höher, Free reicht nach den letzten Angaben von OpenAI nicht. Wenn du Codex in der App siehst und einen Ordner öffnen kannst, passt es.
2. **Python 3** (kostenlos, Microsoft Store oder python.org). Prüfen: PowerShell öffnen, `python --version` eingeben. Zeigt es eine Versionsnummer, ist alles gut. Die Skripte rechnen und suchen; ohne sie läuft das Setup nur halb.
3. **Git** (empfohlen, kostenlos): Es merkt sich den Verlauf deiner Texte, du kannst jederzeit zu einem früheren Stand zurück. Download: https://git-scm.com/download/win. Bei der Installation einfach immer auf „Next“ klicken und alles so lassen, wie es vorgeschlagen ist. Danach die App einmal neu starten. Beim Einrichten richtet Codex Git in deinem Buch-Ordner ein; ohne Git läuft alles trotzdem, nur ohne Verlauf.

## Einrichten (einmal, etwa 15 Minuten)

1. ZIP entpacken, den Ordner an einen festen Platz legen, etwa `Dokumente\Buch`. Nicht im ZIP weiterarbeiten.
2. In Codex diesen Ordner als Projekt öffnen.
3. Schreibe: **„Richte das Buch ein.“** Codex stellt dir wenige Fragen (Gattung, Figuren, Stil, Vorbilder), eine pro Antwort, und füllt damit die Grunddatei. Dauert, ist aber nur einmal nötig.
4. Danach legst du los: einfach erzählen, was du schon im Kopf hast.

## So arbeitest du

Du erzählst, Codex sortiert. Du musst keine Befehle kennen. Vier Arbeitsweisen (Skills), Codex wählt selbst, nach dem, was du sagst:

| Du sagst etwa … | Skill | Was passiert |
|---|---|---|
| „Ich habe eine Idee zu einer Figur / zum Ort / zur Handlung“ | `weltenbau` | Codex ordnet die Idee in die Wissensdateien ein und sagt dir in einer Zeile, was wohin kam. |
| „Schreib Kapitel 3“ / „Schreib eine Leseprobe“ | `schreiben` | Codex liest nur, was die Szene braucht, schreibt, prüft sich selbst und legt dir das Kapitel vor. |
| „Wir sind fertig für heute“ | `sitzung-abschliessen` | Aufräumen, Übergabe für das nächste Mal (`STAND.md`), Sicherung im Verlauf. |
| „Verbessere das Setup“ | `system` | Nur wenn es um die Werkzeuge selbst geht, nicht ums Buch. |

Hilfreich: `_vorlagen/steuerworte.md` hat Wörter wie „Freie Hand …“ oder „Kritik …“, mit denen du lenkst.

**Herkunftsmarken:** In den Dateien steht, von wem etwas stammt. `[A]` hast du gesetzt, `[C✓]` hat Codex ergänzt und ist gültig, `[C?]` ist ein Vorschlag, der auf dein Ja wartet, `[A?]` ist deine Idee, noch nicht festgelegt. Was nicht passt, streichst du einfach.

## Wer macht was

| Du (Autorin) | Codex | Xaver (Betreuung) |
|---|---|---|
| Die Ideen, die Richtung, das letzte Wort. | Sortiert, verdichtet, schreibt Entwürfe, prüft Regeln und Widersprüche. | Liefert das Paket und spielt neue Versionen nach. |
| Entscheidest bei `[C?]` und bei allem, was den Kanon ändert (wer was weiß, was wann geschieht, wie jemand heißt). | Fragt nur dann, höchstens eine Frage pro Antwort; Kleines, das passt, gilt gleich und wird in einer Zeile genannt. | Hilft, wenn Python, Installation oder die App haken. |
| Liest die Kapitel und merkt Anmerkungen mit `{{ … }}` direkt im Text an. | Arbeitet die Anmerkungen ein, wenn du „Kapitel X überarbeiten“ sagst. | Nimmt deine Rückmeldungen auf, damit das Setup besser wird. |
| Sagt „Sitzung abschließen“ und **sichert den Ordner** (siehe unten). | Schreibt die Übergabe in `STAND.md`; das nächste Mal weiß er, wo ihr wart. | |

Was du **nicht** tun musst: Dateien einsortieren, Formate lernen, Skripte starten. Das macht Codex.

## Sicherung, ohne GitHub

Dein Buch ist nur auf diesem Rechner. Darum regelmäßig (wöchentlich, und nach großen Sitzungen) den **ganzen Ordner kopieren**: in OneDrive/Google Drive oder auf einen Stick. Ein Kopieren des ganzen Ordners genügt; der Verlauf liegt in `.git` mit drin. Codex erinnert dich beim Abschließen.

## Neue Version vom Setup

Frag Codex einfach: **„Gibt es eine neue Version?“** Es schaut im Netz nach, sagt dir, was neu ist, lädt die neue Fassung nach deinem Ja neben dein Buch und arbeitet sie Datei für Datei ein. Dein Buch bleibt unberührt. Klappt das Laden nicht, lade das ZIP selbst von der Release-Seite, entpacke es neben deinen Buch-Ordner und sag: **„Arbeite die neue Vorlage aus <Ordner> ein.“**

## Erklärt dir Codex zu viel oder zu wenig?

Beim Einrichten fragt Codex, wie vertraut du mit KI bist, und erklärt danach passend. Sag einfach „das kenne ich schon“ oder „erklär mir das genauer“, dann stellt es sich um.

## Wenn etwas hakt

- Codex findet einen Skill nicht: sag „Lies `.agents/skills/schreiben/SKILL.md` und arbeite danach.“
- Eine Fehlermeldung zu `python`: Python-Installation prüfen (oben), PowerShell neu öffnen.
- Alles andere: schreib Xaver, am besten mit dem Satz, den Codex ausgegeben hat. Eine Zeile unter `_system/hinweise.md` hilft ebenfalls (sag Codex: „Trag ins Hinweisbuch ein, dass …“).
