# -*- coding: utf-8 -*-
"""Inserta marcadores logicos en la plantilla ODT para que build_pdf.py
pueda reemplazar contenido sin depender del texto actual.

Se ejecuta UNA sola vez (idempotente: si ya hay marcadores, no hace nada).
"""
import io, os, re, shutil, sys, zipfile
import xml.etree.ElementTree as ET

TPL = os.path.join(os.path.dirname(__file__), "..", "templates", "cv-harvard.odt")
TPL = os.path.abspath(TPL)

zin = zipfile.ZipFile(TPL)
xml = zin.read("content.xml").decode("utf-8")
if "<!--CV:PROFILE-->" in xml:
    print("Marcadores ya presentes, nada que hacer.")
    sys.exit(0)


def wrap(xml, start_marker, end_marker, begin_idx, end_idx):
    """Envuelve xml[begin_idx:end_idx] con comentarios."""
    return (xml[:begin_idx] + start_marker + xml[begin_idx:end_idx] + end_marker + xml[end_idx:])


# --- PROFILE: parrafo P2 que sigue al titulo PERFIL PROFESIONAL ---
i = xml.find("PERFIL PROFESIONAL</text:p>") + len("PERFIL PROFESIONAL</text:p>")
if not xml.startswith('<text:p text:style-name="P2">', i):
    raise SystemExit("estructura inesperada en PERFIL")
j = xml.find("</text:p>", i) + len("</text:p>")
xml = wrap(xml, "<!--CV:PROFILE-->", "<!--/CV:PROFILE-->", i, j)

# --- EXPERIENCE: desde el primer P7 hasta el espaciador previo a EDUCACION ---
i = xml.find("EXPERIENCIA LABORAL</text:p>") + len("EXPERIENCIA LABORAL</text:p>")
edu = xml.find("EDUCACI\u00d3N")
j = xml.rfind('<text:p text:style-name="P25"/>', 0, edu)
if i < 0 or j < i:
    raise SystemExit("estructura inesperada en EXPERIENCIA")
xml = wrap(xml, "<!--CV:EXPERIENCE-->", "<!--/CV:EXPERIENCE-->", i, j)

# --- EDUCATION: parrafo que contiene la universidad ---
k = xml.find("Universidad de Guayaquil")
i = xml.rfind("<text:p ", 0, k)
j = xml.find("</text:p>", k) + len("</text:p>")
xml = wrap(xml, "<!--CV:EDUCATION-->", "<!--/CV:EDUCATION-->", i, j)

# --- SKILLS: lista L6 ---
i = xml.find('<text:list text:style-name="L6">')
j = xml.find("</text:list>", i) + len("</text:list>")
xml = wrap(xml, "<!--CV:SKILLS-->", "<!--/CV:SKILLS-->", i, j)

# --- CERTIFICATIONS: contenido tras el titulo CERTIFICACIONES ---
i = xml.find("CERTIFICACIONES</text:p>") + len("CERTIFICACIONES</text:p>")
j = xml.find("</office:text>")
xml = wrap(xml, "<!--CV:CERTIFICATIONS-->", "<!--/CV:CERTIFICATIONS-->", i, j)

ET.fromstring(xml.encode("utf-8"))

tmp = TPL + ".tmp"
with zipfile.ZipFile(tmp, "w") as zout:
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
zin.close()
shutil.move(tmp, TPL)
print("Marcadores insertados en", TPL)
