# -*- coding: utf-8 -*-
"""Genera index.html + archivos SEO desde data/cv.<lang>.json.

Salidas:
    index.html, robots.txt, sitemap.xml, site.webmanifest

Uso:
    python scripts/build_site.py [--lang es] [--check]
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE = os.path.join(ROOT, "templates", "index.html.tpl")
OUTPUT = os.path.join(ROOT, "index.html")

MESES_CORTO = {
    1: "ene", 2: "feb", 3: "mar", 4: "abr", 5: "may", 6: "jun",
    7: "jul", 8: "ago", 9: "sep", 10: "oct", 11: "nov", 12: "dic",
}

MESES = {
    1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic",
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


def fmt_updated(value: str) -> str:
    year, month, day = value.split("-")
    return f"{int(day)} {MESES_CORTO[int(month)]} {year}"


def group_by_company(experience: list[dict]) -> list[dict]:
    groups: list[dict] = []
    for job in experience:
        if groups and groups[-1]["company"] == job["company"]:
            groups[-1]["jobs"].append(job)
        else:
            groups.append({"company": job["company"], "jobs": [job]})
    return groups


def months_between(start: str, end: str | None) -> int:
    y1, m1 = int(start[:4]), int(start[5:7])
    if end:
        y2, m2 = int(end[:4]), int(end[5:7])
    else:
        today = date.today()
        y2, m2 = today.year, today.month
    return max(1, (y2 - y1) * 12 + (m2 - m1) + 1)


def fmt_duration(months: int) -> str:
    years, rest = divmod(months, 12)
    parts = []
    if years:
        parts.append(f"{years} año" + ("s" if years > 1 else ""))
    if rest:
        parts.append(f"{rest} mes" + ("es" if rest > 1 else ""))
    return " y ".join(parts) if parts else "1 mes"


def icon(name: str, extra_class: str = "") -> str:
    cls = f"material-symbols-rounded {extra_class}".strip()
    return f'<span class="{cls}" aria-hidden="true">{esc(name)}</span>'


# --------------------------------------------------------------------------
# Renderizadores
# --------------------------------------------------------------------------
def render_profile(cv: dict) -> str:
    return f'<p class="profile-text">{esc(cv["profile"])}</p>'


def render_actions(cv: dict, pdf_href: str) -> str:
    person = cv["person"]
    items = [
        (icon("code"), "GitHub", person["links"]["github"], True),
        (icon("work"), "LinkedIn", person["links"]["linkedin"], True),
        (icon("mail"), "Email", f'mailto:{person["email"]}', False),
        (icon("download"), "PDF", pdf_href, False),
    ]
    out = []
    for ico, label, href, blank in items:
        extra = ' target="_blank" rel="noopener noreferrer"' if blank else ' download' if label == "PDF" else ""
        out.append(
            f'<a class="action" href="{esc(href)}"{extra} title="{esc(label)}">{ico}<span>{esc(label)}</span></a>'
        )
    return "\n                            ".join(out)


def render_stats(cv: dict) -> str:
    return "\n                ".join(
        f'<li class="stat"><span class="stat-value">{esc(s["value"])}</span>'
        f'<span class="stat-label">{esc(s["label"])}</span></li>'
        for s in cv.get("stats", [])
    )


def render_filters(cv: dict) -> str:
    parts = []
    for idx, item in enumerate(cv["filters"]):
        active = " active" if idx == 0 else ""
        parts.append(
            f'<button class="filter-btn{active}" data-filter="{esc(item["id"])}">{esc(item["label"])}</button>'
        )
    return "\n                        ".join(parts)


def render_experience(cv: dict) -> str:
    blocks = []
    for group in group_by_company(cv["experience"]):
        jobs = group["jobs"]
        start = min(j["start"] for j in jobs)
        ends = [j["end"] for j in jobs if j["end"]]
        current = any(j["current"] for j in jobs)
        end = max(ends) if ends else None
        months = months_between(start, end)
        meta = f"{fmt_range(start, end, current)} · {fmt_duration(months)}"

        positions = []
        for job in jobs:
            client = ""
            if job.get("client"):
                note = (
                    f' <span class="position-note">· {esc(job["client_note"])}</span>'
                    if job.get("client_note")
                    else ""
                )
                client = f'\n                        <p class="position-client">{esc(job["client"])}{note}</p>'
            bullets = "\n".join(
                f'                                <li><strong>{esc(b["lead"])}</strong> {esc(b["text"])}</li>'
                for b in job["bullets"]
            )
            positions.append(
                f"""                    <li class="position" data-tech="{esc(' '.join(job['tech']))}">
                        <div class="position-header">
                            <h4 class="position-role">{esc(job['role'])}</h4>
                            <time class="position-date" datetime="{esc(job['start'])}">{esc(fmt_range(job['start'], job['end'], job['current']))}</time>
                        </div>{client}
                        <ul class="position-bullets">
{bullets}
                        </ul>
                    </li>"""
            )

        blocks.append(
            f"""                <article class="job-card company-block">
                    <div class="company-header">
                        <h3 class="company-name">{esc(group['company'])}</h3>
                        <p class="company-meta">{esc(meta)}</p>
                    </div>
                    <ol class="positions">
{chr(10).join(positions)}
                    </ol>
                </article>"""
        )
    return "\n\n".join(blocks)


def render_projects(cv: dict) -> str:
    cards = []
    for project in cv.get("projects", []):
        stack = "".join(f"<li>{esc(item)}</li>" for item in project.get("stack", []))
        link = ""
        if project.get("url"):
            link = (
                f'\n                    <a class="project-link" href="{esc(project["url"])}" target="_blank" '
                f'rel="noopener noreferrer">{icon("arrow_outward")} ver proyecto</a>'
            )
        cards.append(
            f"""                <article class="project-card">
                    <div class="project-head">
                        {icon(project.get("icon", "folder_special"), "project-icon")}
                        <h3 class="project-name">{esc(project['name'])}</h3>
                        <span class="badge">{esc(project.get('badge', ''))}</span>
                    </div>
                    <p class="project-desc">{esc(project.get('description', ''))}</p>
                    <ul class="stack">{stack}</ul>{link}
                </article>"""
        )
    return "\n\n".join(cards)


def render_skills(cv: dict) -> str:
    groups = []
    for category in cv["skills"].get("categories", []):
        chips = "".join(
            f'<li class="chip">{icon(tag["icon"])}{esc(tag["name"])}</li>'
            for tag in category["tags"]
        )
        groups.append(
            f"""                <div class="skill-group">
                    <h3 class="skill-group-title">{icon(category['icon'])}{esc(category['label'])}</h3>
                    <ul class="chips">{chips}</ul>
                </div>"""
        )
    return "\n".join(groups)


def render_certifications(cv: dict) -> str:
    return "\n                        ".join(
        f'<li class="cert-item"><strong>{esc(c["name"])}</strong>'
        f'<span class="cert-meta">{esc(c["issuer"])} · {esc(c["year"])}</span></li>'
        for c in cv.get("certifications", [])
    )


def render_languages(cv: dict) -> str:
    return "\n                        ".join(
        f'<li class="lang-item"><strong>{esc(l["name"])}</strong>'
        f'<span class="lang-meta">{esc(l.get("display") or l["level"])}</span></li>'
        for l in cv.get("languages", [])
    )


def render_education(cv: dict) -> str:
    blocks = []
    for item in cv["education"]:
        note = (
            f'\n                    <p class="education-note">{esc(item["note"])}</p>'
            if item.get("note")
            else ""
        )
        blocks.append(
            f"""                <article class="education-card">
                    <h3>{esc(item['institution'])}</h3>
                    <p class="education-degree">{esc(item['degree'])}</p>
                    <time class="sidebar-date" datetime="{esc(item['start'])}/{esc(item['end'])}">{esc(item['start'][:4])} - {esc(item['end'][:4])}</time>{note}
                </article>"""
        )
    return "\n".join(blocks)


def build_jsonld(cv: dict, site_url: str) -> str:
    person = cv["person"]
    knows = [
        tag["name"]
        for category in cv["skills"].get("categories", [])
        for tag in category["tags"]
    ]
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": person["name"],
        "jobTitle": person["subtitle"],
        "description": person["seo"]["description"],
        "url": site_url,
        "image": f"{site_url}assets/og/og-image.png",
        "email": f'mailto:{person["email"]}',
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Guayaquil",
            "addressRegion": "Guayas",
            "addressCountry": "EC",
        },
        "sameAs": [person["links"]["linkedin"], person["links"]["github"]],
        "knowsAbout": knows[:12],
        "knowsLanguage": ["es", "en"],
        "alumniOf": {
            "@type": "CollegeOrUniversity",
            "name": cv["education"][0]["institution"],
        },
    }
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return payload.replace("</", "<\\/")


# --------------------------------------------------------------------------
# Archivos auxiliares
# --------------------------------------------------------------------------
def build_manifest(cv: dict) -> str:
    person = cv["person"]
    manifest = {
        "name": f'{person["name"]} — {person["subtitle"]}',
        "short_name": person["name"],
        "description": person["seo"]["description"],
        "start_url": "./",
        "display": "standalone",
        "background_color": "#0b0f14",
        "theme_color": "#0b0f14",
        "icons": [
            {"src": "assets/icons/favicon-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "assets/icons/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
            {"src": "assets/icons/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
        ],
    }
    return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


def build_robots(site_url: str) -> str:
    return f"User-agent: *\nAllow: /\n\nSitemap: {site_url}sitemap.xml\n"


def build_sitemap(cv: dict, site_url: str) -> str:
    updated = cv["meta"]["updated"]
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url>\n    <loc>{site_url}</loc>\n    <lastmod>{updated}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n    <priority>1.0</priority>\n  </url>\n"
        "</urlset>\n"
    )


# --------------------------------------------------------------------------
# Render principal
# --------------------------------------------------------------------------
def render(lang: str = "es") -> dict[str, str]:
    with open(os.path.join(ROOT, "data", f"cv.{lang}.json"), encoding="utf-8") as fh:
        cv = json.load(fh)
    with open(TEMPLATE, encoding="utf-8") as fh:
        tpl = fh.read()

    person = cv["person"]
    site_url = cv["meta"].get("site_url", "https://cyborgk27.github.io/cv/")
    if not site_url.endswith("/"):
        site_url += "/"
    pdf_href = f"dist/{cv['meta']['file_name']}.pdf"

    replacements = {
        "LANG": cv["meta"]["lang"],
        "PAGE_TITLE": f'{person["name"]} | {person["subtitle"]}',
        "NAME": esc(person["name"]),
        "SUBTITLE": esc(person["subtitle"]),
        "LOCATION": esc(person["location"]),
        "META_DESCRIPTION": esc(person["seo"]["description"]),
        "META_KEYWORDS": esc(person["seo"]["keywords"]),
        "SITE_URL": esc(site_url),
        "PDF_HREF": pdf_href,
        "UPDATED": esc(fmt_updated(cv["meta"]["updated"])),
        "JSONLD": build_jsonld(cv, site_url),
        "ACTIONS": render_actions(cv, pdf_href),
        "STATS": render_stats(cv),
        "PROFILE": render_profile(cv),
        "FILTERS": render_filters(cv),
        "EXPERIENCE": render_experience(cv),
        "PROJECTS": render_projects(cv),
        "SKILLS": render_skills(cv),
        "CERTIFICATIONS": render_certifications(cv),
        "EDUCATION": render_education(cv),
        "LANGUAGES": render_languages(cv),
    }
    for key, value in replacements.items():
        tpl = tpl.replace("{{" + key + "}}", value)

    if "{{" in tpl:
        start = tpl.find("{{")
        raise SystemExit(f"Placeholder sin resolver: {tpl[start:start + 40]}")

    return {
        "index.html": tpl,
        "site.webmanifest": build_manifest(cv),
        "robots.txt": build_robots(site_url),
        "sitemap.xml": build_sitemap(cv, site_url),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera index.html y archivos SEO")
    parser.add_argument("--lang", default="es")
    parser.add_argument("--check", action="store_true", help="Falla si hay archivos desincronizados")
    args = parser.parse_args()

    outputs = render(args.lang)

    if args.check:
        stale = []
        for name, content in outputs.items():
            path = os.path.join(ROOT, name)
            current = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
            if current != content:
                stale.append(name)
        if stale:
            print(f"Desincronizado: {', '.join(stale)} — ejecuta scripts/build.py")
            return 1
        print("index.html y SEO OK")
        return 0

    for name, content in outputs.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
    print("index.html + robots.txt + sitemap.xml + site.webmanifest generados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
