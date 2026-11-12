# Änderungen

Neueste oben. Je Version: was sich ändert, was der Empfänger tun muss. Nummern: erste Zahl = größerer Umbau, zweite = Verbesserungen ohne Aufwand.

## 1.0 (2026-11-12)

Erste Ausgabe, für Codex (ChatGPT-Desktop-App) übersetzt aus dem Claude-Code-Setup.
- Vier Skills (`weltenbau`, `schreiben`, `sitzung-abschliessen`, `system`) unter `.agents/skills/`, Regeln in `AGENTS.md`, Prüf- und Kritikrolle in `_agenten/`.
- Skripte in `_werkzeuge/` (Python 3), Vorlagen in `_vorlagen/`.
- Läuft ohne GitHub: lokales Git, Sicherung durch Kopieren des Ordners.
- Der Skill `system` kümmert sich um Störungen, sucht auf Wunsch neue Versionen (`system.py version`), lädt und arbeitet sie ein und fragt beim Einrichten nach deiner KI-Erfahrung, um die Erklärungen anzupassen (`projekt.json`, `nutzer`).
- Du musst nichts tun. Anfangen mit `LIES_MICH_ZUERST.md`.
