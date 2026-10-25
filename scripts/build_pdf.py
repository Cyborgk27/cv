# -*- coding: utf-8 -*-
"""Genera el CV imprimible (ODT + PDF) desde data/cv.<lang>.json.

Uso:
    python scripts/build_pdf.py [--lang es] [--no-pdf]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE = os.path.join(ROOT, "templates", "cv-harvard.odt")
DIST = os.path.join(ROOT, "dist")

MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt_month(value: str | None) -> str:
    if not value:
        return ""
    year, month = value.split("-")
    return f"{MESES[int(month)]} {year}"


def fmt_range(start: str | None, end: str | None, current: bool) -> str:
    if current:
        return f"{fmt_month(start)} \u2013 Presente"
    return f"{fmt_month(start)} \u2013 {fmt_month(end)}"


def replace_region(xml: str, key: str, payload: str) -> str:
    begin = f"<!--CV:{key}-->"
    end = f"<!--/CV:{key}-->"
    i = xml.find(begin)
    j = xml.find(end)
    if i == -1 or j == -1:
        raise SystemExit(f"Marcador {key} no encontrado en la plantilla")
    return xml[: i + len(begin)] + payload + xml[j:]


def group_by_company(entries: list[dict]) -> list[dict]:
    groups: list[dict] = []
    for entry in entries:
        if groups and groups[-1]["company"] == entry["company"]:
            groups[-1]["entries"].append(entry)
        else:
            groups.append({"company": entry["company"], "entries": [entry]})
    return groups


def render_bullets(bullets: list[dict]) -> str:
    out = ['<text:list text:style-name="L1">']
    last = len(bullets) - 1
    for idx, bullet in enumerate(bullets):
        style = "P9K" if idx < last else "P9"
        out.append(
            f'<text:list-item><text:p text:style-name="{style}">'
            f'<text:span text:style-name="T5">{esc(bullet["lead"])}</text:span> '
            f'<text:span text:style-name="T2">{esc(bullet["text"])}</text:span>'
            "</text:p></text:list-item>"
        )
    out.append("</text:list>")
    return "".join(out)


def render_client(entry: dict, employer_dates: str = "") -> str:
    note = entry.get("client_note") or ""
    label = esc(entry["client"]) + (f" \u00b7 {esc(note)}" if note else "")
    html = [f'<text:p text:style-name="PCliente"><text:span text:style-name="T5">{label}</text:span>']
    dates = fmt_range(entry["start"], entry["end"], entry["current"])
    if dates != employer_dates:
        html.append(f"<text:tab/>{esc(dates)}")
    html.append("</text:p>")
    html.append(render_bullets(entry["bullets"]))
    return "".join(html)


def render_experience(entries: list[dict]) -> str:
    blocks = []
    for group in group_by_company(entries):
        items = group["entries"]
        role = items[0].get("company_role") or items[0]["role"]
        start = min(i["start"] for i in items)
        ends = [i["end"] for i in items if i["end"]]
        current = any(i["current"] for i in items)
        end = max(ends) if ends else None
        dates = fmt_range(start, end, current)
        block = (
            '<text:p text:style-name="P7">'
            f'<text:span text:style-name="T5">{esc(group["company"])}</text:span>'
            f'<text:span text:style-name="TNorm"> \u2013 {esc(role)}</text:span>'
            f'<text:tab/><text:span text:style-name="TNorm">{esc(dates)}</text:span>'
            "</text:p>"
        )
        for entry in items:
            block += render_client(entry, dates)
        blocks.append(block)
    return '<text:p text:style-name="P10"/>'.join(blocks)


def render_education(education: list[dict], location: str) -> str:
    parts = [p.strip() for p in location.split(",")]
    short_location = f"{parts[0]}, {parts[-1]}" if len(parts) > 1 else parts[0]
    out = []
    for item in education:
        dates = fmt_range(item["start"], item["end"], False)
        out.append(
            '<text:p text:style-name="P25">'
            f'<text:span text:style-name="T5">{esc(item["institution"])} | {esc(short_location)} '
            f"<text:tab/></text:span>"
            f'<text:span text:style-name="T17">{esc(dates)}</text:span>'
            f'<text:line-break/><text:span text:style-name="T10">{esc(item["degree"])}</text:span>'
        )
        if item.get("note"):
            out.append(
                f'<text:line-break/><text:span text:style-name="T10">{esc(item["note"])}</text:span>'
            )
        out.append("</text:p>")
    return "".join(out)


def render_skills(skills: dict, languages: list[dict]) -> str:
    rows = [(g["label"], g["items"]) for g in skills["groups"]]
    if languages:
        rows.append(
            (
                "Idiomas",
                " \u00b7 ".join(l.get("display") or f'{l["name"]} ({l["level"]})' for l in languages),
            )
        )
    out = ['<text:list text:style-name="L6">']
    for label, items in rows:
        out.append(
            '<text:list-item><text:p text:style-name="P29">'
            f'<text:span text:style-name="T5">{esc(label)}</text:span>: {esc(items)}'
            "</text:p></text:list-item>"
        )
    out.append("</text:list>")
    return "".join(out)


def render_certifications(items: list[dict]) -> str:
    parts = []
    for idx, cert in enumerate(items):
        if idx:
            parts.append("<text:line-break/>")
        parts.append(
            f'<text:span text:style-name="T5">{esc(cert["name"])}</text:span> \u2014 '
            f'{esc(cert["issuer"])} \u00b7 {esc(cert["year"])}'
        )
    return '<text:p text:style-name="P25">' + "".join(parts) + "</text:p>"


def write_odt(xml: str, destination: str) -> None:
    tmp = destination + ".tmp"
    with zipfile.ZipFile(TEMPLATE) as zin, zipfile.ZipFile(tmp, "w") as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "content.xml":
                data = xml.encode("utf-8")
            if item.filename == "mimetype":
                zi = zipfile.ZipInfo("mimetype", date_time=item.date_time)
                zi.compress_type = zipfile.ZIP_STORED
            else:
                zi = zipfile.ZipInfo(item.filename, date_time=item.date_time)
                zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = item.external_attr
            zout.writestr(zi, data)
    shutil.move(tmp, destination)


def find_soffice() -> str | None:
    candidates = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        "/usr/bin/soffice",
        "/usr/bin/libreoffice",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return shutil.which("soffice") or shutil.which("libreoffice")


def to_pdf(odt_path: str) -> str:
    soffice = find_soffice()
    if not soffice:
        raise SystemExit("LibreOffice no encontrado: no se puede generar el PDF")
    profile = os.path.join(ROOT, ".lo_profile")
    subprocess.run(
        [
            soffice,
            "--headless",
            "--norestore",
            f"-env:UserInstallation=file:///{profile.replace(os.sep, '/').lstrip('/')}",
            "--convert-to",
            "pdf",
            "--outdir",
            DIST,
            odt_path,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return os.path.splitext(odt_path)[0] + ".pdf"


def build(lang: str = "es", make_pdf: bool = True) -> dict[str, str]:
    with open(os.path.join(ROOT, "data", f"cv.{lang}.json"), encoding="utf-8") as fh:
        cv = json.load(fh)

    with zipfile.ZipFile(TEMPLATE) as zin:
        xml = zin.read("content.xml").decode("utf-8")

    xml = replace_region(xml, "PROFILE", f'<text:p text:style-name="P2">{esc(cv["profile"])}</text:p>')
    xml = replace_region(xml, "EXPERIENCE", render_experience(cv["experience"]))
    xml = replace_region(
        xml, "EDUCATION", render_education(cv["education"], cv["person"]["location"])
    )
    xml = replace_region(xml, "SKILLS", render_skills(cv["skills"], cv.get("languages", [])))
    xml = replace_region(xml, "CERTIFICATIONS", render_certifications(cv.get("certifications", [])))

    ET.fromstring(xml.encode("utf-8"))

    os.makedirs(DIST, exist_ok=True)
    base = cv["meta"]["file_name"]
    odt_path = os.path.join(DIST, base + ".odt")
    write_odt(xml, odt_path)
    result = {"odt": odt_path}

    if make_pdf:
        result["pdf"] = to_pdf(odt_path)

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera el CV imprimible desde el JSON")
    parser.add_argument("--lang", default="es")
    parser.add_argument("--no-pdf", action="store_true")
    args = parser.parse_args()

    result = build(args.lang, not args.no_pdf)
    for key, value in result.items():
        print(f"{key.upper()}: {os.path.relpath(value, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
