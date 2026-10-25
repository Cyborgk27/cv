# -*- coding: utf-8 -*-
"""Regenera las imagenes de marca (OG image y favicons PNG).

Requiere Playwright. No corre en CI: los PNG se versionan en el repo.

    pip install playwright && playwright install chromium
    python scripts/gen_assets.py

Si no hay Playwright, imprime los pasos manuales.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(ROOT, "assets")
OG_SOURCE = os.path.join(ASSETS, "og", "og-source.html")
ICON_SVG = os.path.join(ASSETS, "icons", "favicon.svg")

SIZES = [
    (180, "apple-touch-icon.png"),
    (32, "favicon-32.png"),
    (16, "favicon-16.png"),
]


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Playwright no esta instalado.\n"
            "  pip install playwright && playwright install chromium\n"
            "O genera las imagenes manualmente:\n"
            f"  - {OG_SOURCE} a 1200x630 -> assets/og/og-image.png\n"
            f"  - {ICON_SVG} a 180/32/16 -> assets/icons/*.png"
        )
        return 1

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        page.set_viewport_size({"width": 1200, "height": 630})
        page.goto("file:///" + OG_SOURCE.replace(os.sep, "/"))
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(ASSETS, "og", "og-image.png"))
        print("assets/og/og-image.png")

        for size, name in SIZES:
            page.set_viewport_size({"width": size, "height": size})
            page.goto("file:///" + ICON_SVG.replace(os.sep, "/"))
            page.wait_for_timeout(300)
            page.screenshot(path=os.path.join(ASSETS, "icons", name))
            print(f"assets/icons/{name}")

        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
