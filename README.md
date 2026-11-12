# Buch-Setup für Codex

Ein Setup, mit dem Codex (ChatGPT-Desktop-App) bei einem Roman mitarbeitet: Welt und Figuren aufbauen, Kapitel schreiben, prüfen, den Überblick über viele Sitzungen halten.

## Herunterladen

Auf der Seite **Releases** (rechts auf dieser Seite) die neueste Version öffnen und die Datei `buchsetup-codex-<Version>.zip` herunterladen. Du brauchst dafür kein GitHub-Konto. Im ZIP liegt der Ordner `Buch-Setup`; entpacken, an einen festen Platz legen, in Codex öffnen und die `LIES_MICH_ZUERST.md` lesen.

## Versionen

Die Nummer steht in `VERSION`; was sich je Version ändert und was du tun musst, in `AENDERUNGEN.md`.

- **Erste Zahl** (1.0 → 2.0): größerer Umbau, ein Blick in `AENDERUNGEN.md` lohnt.
- **Zweite Zahl** (1.0 → 1.1): Verbesserungen und neue Werkzeuge, du änderst nichts.

Neue Version einspielen: ZIP neben dein Buch entpacken und Codex sagen: „Arbeite die neue Vorlage aus <Ordner> ein.“ Dein Buch bleibt unberührt.

## Inhalt dieses Repos

- `buchsetup/` – das Setup selbst (so, wie es im ZIP liegt).
- `VERSION`, `AENDERUNGEN.md` – Stand und Änderungen.
- `README.md` – diese Seite.

Gebaut wird alles aus dem Arbeitsordner des Autors mit `python _werkzeuge/system.py codex`; Änderungen bitte dort, nicht hier.
