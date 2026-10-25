# -*- coding: utf-8 -*-
"""Orquesta la generacion del sitio y del CV imprimible.

Uso:
    python scripts/build.py                 # regenera index.html + dist/*.pdf
    python scripts/build.py --check         # valida que el sitio este sincronizado
    python scripts/build.py --site-only
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(ROOT, "scripts")


def run(script: str, *args: str) -> int:
    cmd = [sys.executable, os.path.join(SCRIPTS, script), *args]
    return subprocess.run(cmd, cwd=ROOT).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Build del CV")
    parser.add_argument("--lang", default="es")
    parser.add_argument("--check", action="store_true", help="No escribe: valida sincronizacion")
    parser.add_argument("--site-only", action="store_true", help="No regenera el PDF")
    args = parser.parse_args()

    if args.check:
        code = run("build_site.py", "--lang", args.lang, "--check")
        if code:
            return code
        pdf = os.path.join(ROOT, "dist", "Kevin_Cepeda_CV.pdf")
        if not os.path.exists(pdf):
            print("Falta dist/Kevin_Cepeda_CV.pdf: ejecuta scripts/build.py")
            return 1
        print("PDF OK")
        return 0

    code = run("build_site.py", "--lang", args.lang)
    if code:
        return code

    if not args.site_only:
        code = run("build_pdf.py", "--lang", args.lang)
        if code:
            return code

    print("\nListo. Recuerda: nunca edites index.html ni dist/* a mano.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
