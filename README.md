# 📄 Kevin Cepeda — CV Web + CV Imprimible

[![Live Demo](https://img.shields.io/badge/demo-en%20vivo-brightgreen?style=for-the-badge&logo=githubpages)](https://cyborgk27.github.io/cv/)
[![PDF](https://img.shields.io/badge/CV-PDF-red?style=for-the-badge&logo=adobeacrobatreader)](https://cyborgk27.github.io/cv/dist/Kevin_Cepeda_CV.pdf)
[![LinkedIn](https://img.shields.io/badge/linkedin-conectar-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/kevincepeda27/)

Currículum de **Kevin Cepeda** — Full Stack Developer (.NET / Angular) con foco en banca, seguridad de aplicaciones y observabilidad.

Este repositorio mantiene **dos salidas desde una sola fuente de verdad**:

| Salida | Archivo | Uso |
|---|---|---|
| CV web interactivo | `index.html` | Compartir por LinkedIn / WhatsApp |
| CV imprimible | `dist/Kevin_Cepeda_CV.pdf` | Postulaciones y ATS |

**Demo:** [cyborgk27.github.io/cv](https://cyborgk27.github.io/cv/) · **PDF:** [descargar](https://cyborgk27.github.io/cv/dist/Kevin_Cepeda_CV.pdf)

---

## 🏗️ Arquitectura

```
cv/
├─ data/
│  └─ cv.es.json            ← ÚNICA fuente de verdad (contenido)
├─ templates/
│  ├─ index.html.tpl        ← maqueta del sitio (placeholders {{KEY}})
│  └─ cv-harvard.odt        ← plantilla de impresión con marcadores <!--CV:*-->
├─ scripts/
│  ├─ build.py              ← orquesta todo
│  ├─ build_site.py         ← JSON + tpl → index.html
│  ├─ build_pdf.py          ← JSON + odt → dist/*.odt + *.pdf
│  └─ init_template.py      ← utilidad de un solo uso (inserta marcadores en el ODT)
├─ dist/
│  ├─ Kevin_Cepeda_CV.pdf   ← generado
│  └─ Kevin_Cepeda_CV.odt   ← generado
├─ index.html               ← GENERADO (no editar a mano)
├─ css/ · js/ · assets/
└─ .github/workflows/build.yml
```

> ⚠️ `index.html` y `dist/` son **artefactos generados**. Si los editas a mano, el siguiente build los sobrescribe.

---

## ✍️ Cómo actualizar el CV

1. Edita **solo** `data/cv.es.json`:
   - `person` → nombre, titular, contacto, SEO
   - `profile` → párrafo de perfil
   - `experience[]` → `company`, `client`, `role`, `start`/`end` en formato `YYYY-MM`, `current`, `tech` (ids de `filters`), `bullets[]`
   - `education`, `skills`, `certifications`, `languages`
2. Regenera:

```bash
python scripts/build.py
```

3. Revisa `index.html` y `dist/Kevin_Cepeda_CV.pdf`, y haz commit de **ambos** junto con el JSON.

### Reglas de contenido

- **Fechas reales y verificables.** Deben coincidir con LinkedIn; si no, un background check lo detecta.
- **Un cliente por entrada.** Los proyectos de un mismo empleador van como entradas separadas con la misma `company` y se agrupan automáticamente en el PDF (con `company_role` para la progresión de rol).
- **Nada de tecnología sin respaldo** en algún bullet.

### Agregar un idioma

```bash
cp data/cv.es.json data/cv.en.json   # traduce los valores, ajusta meta.lang
python scripts/build.py --lang en
```

`build_site.py` emitirá `index.html` para ese idioma. Para publicar ambos, sirve `es` en la raíz y `en` en una subcarpeta (pendiente: selector de idioma en el header).

---

## 🧰 Requisitos

- **Python 3.10+** (solo librería estándar)
- **LibreOffice** (para exportar el PDF) — se detecta automáticamente en Windows, macOS y Linux

## ✅ Verificación

```bash
python scripts/build.py --check   # falla si index.html está desincronizado o falta el PDF
```

En CI este comando corre antes del build: si alguien edita `index.html` a mano y olvida el JSON, el pipeline falla.

---

## 🚀 Despliegue

Cada push a `main` dispara `.github/workflows/build.yml`:

1. Instala LibreOffice + fuentes métricamente compatibles con Times New Roman (para que el paginado del PDF no cambie).
2. Corre `--check` y luego `build.py`.
3. Publica `index.html`, `css/`, `js/`, `assets/` y `dist/` en GitHub Pages.

---

## ✉️ Contacto

- **Email:** [cepedayupanqui.kevin@gmail.com](mailto:cepedayupanqui.kevin@gmail.com)
- **LinkedIn:** [linkedin.com/in/kevincepeda27](https://www.linkedin.com/in/kevincepeda27/)
- **GitHub:** [github.com/Cyborgk27](https://github.com/Cyborgk27)
- **WhatsApp:** [+593 991 713 814](https://wa.me/593991713814)
