# -*- coding: utf-8 -*-
"""Genera index.html desde data/cv.<lang>.json + templates/index.html.tpl.

Uso:
    python scripts/build_site.py [--lang es] [--check]
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE = os.path.join(ROOT, "templates", "index.html.tpl")
OUTPUT = os.path.join(ROOT, "index.html")

MESES = {
    1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic",
}

# Iconos Remix por red social
ICONS = {
    "email": "ri-mail-line",
    "linkedin": "ri-linkedin-box-line",
    "github": "ri-github-line",
    "whatsapp": "ri-whatsapp-line",
}


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def fmt_month(value: str | None) -> str:
    if not value:
        return ""
    year, month = value.split("-")
    return f"{MESES[int(month)]} {year}"


def fmt_range(start: str, end: str | None, current: bool) -> str:
    if current:
        return f"{fmt_month(start)} - Actualidad"
    return f"{fmt_month(start)} - {fmt_month(end)}"


def render_profile(cv: dict) -> str:
    return f'<p class="profile-text">{esc(cv["profile"])}</p>'


def render_filters(cv: dict) -> str:
    parts = []
    for idx, item in enumerate(cv["filters"]):
        active = " active" if idx == 0 else ""
        parts.append(
            f'<button class="filter-btn{active}" data-filter="{esc(item["id"])}">{esc(item["label"])}</button>'
        )
    return "\n                    ".join(parts)


def render_experience(cv: dict) -> str:
    cards = []
    for job in cv["experience"]:
        end_iso = "present" if job["current"] else job["end"]
        bullets = []
        for bullet in job["bullets"]:
            bullets.append(
                f'                        <li>\n'
                f'                            <strong>{esc(bullet["lead"])}</strong> {esc(bullet["text"])}\n'
                f"                        </li>"
            )
        client = f' <span class="project-name">| {esc(job["client"])}</span>' if job.get("client") else ""
        cards.append(
            f"""                <article class="job-card" data-tech="{esc(' '.join(job['tech']))}">
                    <div class="job-header">
                        <h3>{esc(job['company'])}{client}</h3>
                        <time class="job-date" datetime="{esc(job['start'])}">{esc(fmt_range(job['start'], job['end'], job['current']))}</time>
                    </div>
                    <p class="job-role">{esc(job['role'])}</p>
                    <p class="job-location">{esc(job['location'])}</p>
                    <ul>
{chr(10).join(bullets)}
                    </ul>
                </article>"""
        )
    return "\n\n".join(cards)


def render_contact(cv: dict) -> str:
    person = cv["person"]
    items = [
        ("email", f'mailto:{person["email"]}', person["email"], "Enviar correo electrónico"),
        (
            "linkedin",
            person["links"]["linkedin"],
            person["links"]["linkedin"].replace("https://www.", "").rstrip("/"),
            "Visitar perfil de LinkedIn",
        ),
        (
            "github",
            person["links"]["github"],
            person["links"]["github"].replace("https://", ""),
            "Visitar perfil de GitHub",
        ),
        (
            "whatsapp",
            f'https://wa.me/{person["whatsapp"]}?text=Hola,%20vi%20tu%20CV%20y%20me%20gustar%C3%ADa%20contactarte',
            person["phone"],
            "Enviar mensaje por WhatsApp",
        ),
    ]
    out = []
    for key, href, label, title in items:
        out.append(
            f"""                        <li>
                            <i class="{ICONS[key]} icon" aria-hidden="true"></i>
                            <a href="{esc(href)}" target="_blank" rel="noopener noreferrer" title="{esc(title)}">{esc(label)}</a>
                        </li>"""
        )
    return "\n".join(out)


def render_education(cv: dict) -> str:
    blocks = []
    for item in cv["education"]:
        note = f'\n                    <p class="education-note">{esc(item["note"])}</p>' if item.get("note") else ""
        blocks.append(
            f"""                <article class="education-card">
                    <h3>{esc(item['institution'])}</h3>
                    <p class="education-degree">{esc(item['degree'])}</p>
                    <time class="sidebar-date" datetime="{esc(item['start'])}/{esc(item['end'])}">{esc(item['start'][:4])} - {esc(item['end'][:4])}</time>{note}
                </article>"""
        )
    return "\n".join(blocks)


def render_skill_tags(cv: dict) -> str:
    return "\n                    ".join(
        f'<span class="skill-tag">{esc(tag)}</span>' for tag in cv["skills"]["tags"]
    )


def render_certifications(cv: dict) -> str:
    return "\n                    ".join(
        f'<li class="cert-item"><strong>{esc(c["name"])}</strong>'
        f'<span class="cert-meta">{esc(c["issuer"])} · {esc(c["year"])}</span></li>'
        for c in cv.get("certifications", [])
    )


def render_languages(cv: dict) -> str:
    return "\n                    ".join(
        f'<li class="lang-item"><strong>{esc(l["name"])}</strong>'
        f'<span class="lang-meta">{esc(l["level"])}</span></li>'
        for l in cv.get("languages", [])
    )


def render(lang: str = "es") -> str:
    with open(os.path.join(ROOT, "data", f"cv.{lang}.json"), encoding="utf-8") as fh:
        cv = json.load(fh)
    with open(TEMPLATE, encoding="utf-8") as fh:
        tpl = fh.read()

    person = cv["person"]
    pdf_name = cv["meta"]["file_name"] + ".pdf"
    replacements = {
        "LANG": cv["meta"]["lang"],
        "PAGE_TITLE": f'{person["name"]} | {person["subtitle"]}',
        "NAME": esc(person["name"]),
        "SUBTITLE": esc(person["subtitle"]),
        "META_DESCRIPTION": esc(person["seo"]["description"]),
        "META_KEYWORDS": esc(person["seo"]["keywords"]),
        "PDF_HREF": f"dist/{pdf_name}",
        "PROFILE": render_profile(cv),
        "FILTERS": render_filters(cv),
        "EXPERIENCE": render_experience(cv),
        "CONTACT": render_contact(cv),
        "EDUCATION": render_education(cv),
        "SKILL_TAGS": render_skill_tags(cv),
        "CERTIFICATIONS": render_certifications(cv),
        "LANGUAGES": render_languages(cv),
    }
    for key, value in replacements.items():
        tpl = tpl.replace("{{" + key + "}}", value)

    if "{{" in tpl:
        raise SystemExit(f"Placeholders sin resolver: {tpl[tpl.find('{{'):tpl.find('{{') + 40]}")

    return tpl


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera index.html desde el JSON")
    parser.add_argument("--lang", default="es")
    parser.add_argument("--check", action="store_true", help="Falla si index.html no coincide con el JSON")
    args = parser.parse_args()

    content = render(args.lang)

    if args.check:
        current = open(OUTPUT, encoding="utf-8").read() if os.path.exists(OUTPUT) else ""
        if current != content:
            print("index.html está desincronizado con data/: ejecuta scripts/build.py")
            return 1
        print("index.html OK")
        return 0

    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    print("index.html generado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
