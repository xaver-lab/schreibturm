<div align="center">

# 🗼 Schreibturm

**Dein Roman bekommt einen Turm voller Helfer.**
Ein Setup für Codex (ChatGPT-Desktop-App), das mit dir Welten baut, Figuren pflegt und Kapitel schreibt, und beim nächsten Mal noch weiß, wo ihr stehen geblieben seid.

[![Neueste Version](https://img.shields.io/github/v/release/xaver-lab/schreibturm?label=Version&color=8a5a2b)](https://github.com/xaver-lab/schreibturm/releases/latest)
&nbsp;
**[📥 Herunterladen](https://github.com/xaver-lab/schreibturm/releases/latest)**

*Kein GitHub-Konto nötig. Ein ZIP, ein Ordner, los.*

</div>

---

## 🕯️ In drei Schritten

1. **Python 3 installieren** (Microsoft Store, „Python 3“). Das ist alles, was du vorab brauchst.
2. **Einen neuen Ordner für dein Buch anlegen** und ihn in der Codex-App als Projekt öffnen.
3. **Den Startprompt schicken** (unten). Codex lädt den Schreibturm selbst herunter und richtet alles mit dir ein.

<details>
<summary><b>📜 Der Startprompt zum Kopieren</b></summary>

```text
Ziel: Ich will mit dir ein Buch schreiben.

Aufgabe: Lade von https://github.com/xaver-lab/schreibturm/releases/latest
das ZIP herunter und entpacke es so, dass der Inhalt des Ordners
„Buch-Setup“ direkt in diesem Ordner liegt. Lies danach AGENTS.md und
LIES_MICH_ZUERST.md und prüfe mit „python --version“, ob Python läuft.
Richte dann mein Buch ein.

So sollst du mit mir reden: Ich bin neu mit KI. Erklär kurz, was du tust,
und stell mir immer nur eine Frage auf einmal.
```

Das ist übrigens ein guter Aufbau für jeden Prompt: erst das **Ziel**, dann die **Aufgabe**, dann **wie die KI mit dir reden soll**.

</details>

## 🏛️ Die Räume im Turm

| | Raum | Wofür |
|---|---|---|
| 🗺️ | **Kartenzimmer** (`weltenbau`) | Du erzählst Ideen, Codex ordnet sie: Welt, Figuren, Handlung, Stil. |
| ✒️ | **Schreibstube** (`schreiben`) | Kapitel und Leseproben entstehen, prüfen sich selbst und liegen dir zur Durchsicht vor. |
| 🌙 | **Feierabend** (`sitzung-abschliessen`) | Aufräumen und eine Übergabe, damit die nächste Sitzung da weitermacht, wo ihr aufgehört habt. |
| 🔧 | **Werkstatt im Keller** (`system`) | Einrichten, Störungen beheben, nach neuen Versionen suchen, Erklärungen an deine Erfahrung anpassen. |

Du musst dazu keine Befehle lernen. Du erzählst, Codex wählt den passenden Raum.

## 📚 Gut zu wissen

- **Alles liegt als Dateien in deinem Ordner**, nichts im Netz. Sichern heißt: den Ordner kopieren (Cloud, Stick).
- **Du hast das letzte Wort.** Was Codex vorschlägt, ist markiert (`[C?]`), und was du setzt, ist Kanon (`[A]`).
- **Neue Version?** Frag Codex: „Gibt es eine neue Version?“ Es sucht, lädt und arbeitet sie ein. Dein Buch bleibt dabei unberührt.

## 🔖 Versionen

Die Nummer steht in `VERSION`, die Änderungen in [`AENDERUNGEN.md`](AENDERUNGEN.md).
Erste Zahl (1.0 → 2.0) ist ein größerer Umbau, zweite Zahl (1.0 → 1.1) eine Verbesserung, bei der du nichts tun musst.

## 🗂️ Inhalt dieses Repos

`buchsetup/` das Setup selbst, so wie es im ZIP liegt · `VERSION` · `AENDERUNGEN.md` · diese Seite.

<div align="center">
<sub>Gebaut für Schreibende, die lieber erzählen als konfigurieren. ✒️</sub>
</div>
