import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

WURZEL = Path(__file__).resolve().parent.parent


def git(*args):
    return subprocess.run(
        ["git", *args],
        cwd=WURZEL,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def zahl(*args):
    lauf = git(*args)
    return int(lauf.stdout.strip() or 0) if lauf.returncode == 0 else 0


def meldung(text):
    print(f"Start-Check: {text}")


def ist_vorfahre(ref, ziel):
    return git("merge-base", "--is-ancestor", ref, ziel).returncode == 0


def probe(ziel, ref):
    lauf = git("merge-tree", "--write-tree", "--name-only", "--no-messages", ziel, ref)
    return lauf.returncode


def main():
    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        meldung("kein Git-Repository, nichts zu prüfen.")
        return 0

    if "origin" not in git("remote").stdout.split():
        return 0   # lokales Repo ohne Server (etwa bei der Codex-Fassung): nichts zu holen

    holen = git("fetch", "--prune", "origin")
    if holen.returncode != 0:
        meldung(f"fetch fehlgeschlagen ({holen.stderr.strip()}). Stand bitte von Hand prüfen.")
        return 0

    aktuell = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    sauber = git("status", "--porcelain", "--untracked-files=no").stdout.strip() == ""

    if aktuell != "main":
        meldung(f"Sitzung steht auf Branch {aktuell}. main wird hier nicht verändert.")
    elif not sauber:
        meldung("Arbeitsbaum nicht sauber. main wird nicht geholt; bitte Änderungen prüfen.")
    elif zahl("rev-list", "--count", "main..origin/main") > 0:
        ff = git("merge", "--ff-only", "origin/main")
        if ff.returncode == 0:
            meldung("main per Fast-Forward auf origin/main gebracht.")
        else:
            meldung(f"main ließ sich nicht fast-forwarden ({ff.stderr.strip()}). Bitte prüfen.")

    refs = [
        r
        for r in git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").stdout.split()
        if r not in ("origin", "origin/HEAD", "origin/main")
    ]

    offen = [r for r in refs if not ist_vorfahre(r, "HEAD")]

    if not offen:
        meldung("keine Branches mit Commits, die nicht in main sind.")
        return 0

    for ref in offen:
        neu = zahl("rev-list", "--count", f"HEAD..{ref}")
        letzter = git("log", "-1", "--format=%cs %s", ref).stdout.strip()
        meldung(f"{ref}: {neu} Commit(s) nicht in main, zuletzt {letzter}")

        if aktuell != "main" or not sauber:
            continue

        code = probe("HEAD", ref)
        if code == 0:
            merge = git("merge", "--no-edit", "-m", f"Start-Check: {ref} nach main eingearbeitet", ref)
            if merge.returncode == 0:
                meldung(f"{ref} sauber nach main eingearbeitet (lokal, noch nicht gepusht).")
            else:
                git("merge", "--abort")
                meldung(f"{ref} ließ sich nicht einarbeiten; Merge abgebrochen. Dem Autor vorlegen.")
        elif code == 1:
            meldung(f"{ref} hat Konflikte mit main. Nicht eingearbeitet; dem Autor vorlegen.")
        else:
            meldung(f"{ref}: Probemerge nicht möglich (Git zu alt?). Von Hand prüfen.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
