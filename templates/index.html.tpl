<!doctype html>
<html lang="{{LANG}}">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>{{PAGE_TITLE}}</title>
    <meta name="description" content="{{META_DESCRIPTION}}" />
    <meta name="keywords" content="{{META_KEYWORDS}}" />
    <meta name="author" content="{{NAME}}" />
    <meta name="robots" content="index, follow" />

    <meta property="og:type" content="profile" />
    <meta property="og:title" content="{{NAME}} | {{SUBTITLE}}" />
    <meta property="og:description" content="{{META_DESCRIPTION}}" />
    <meta property="og:url" content="https://cyborgk27.github.io/cv/" />
    <meta property="og:site_name" content="CV {{NAME}}" />
    <meta name="google-site-verification" content="hOqyMc6OIu9wLZ1B5i_aWnVQgYrsB0Mj_NVgnsuqwto" />

    <link rel="stylesheet" href="css/styles.css" />
    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css" />
    <link rel="icon" type="image/svg+xml" href="assets/icons/favicon.svg" />
</head>

<body>
    <main class="cv-container">
        <div class="main-column">
            <header class="cv-header">
                <div class="header-title-container">
                    <h1>{{NAME}}</h1>
                    <p class="subtitle">{{SUBTITLE}}</p>
                </div>
                <div class="header-actions">
                    <a class="btn-download" href="{{PDF_HREF}}" download title="Descargar CV en PDF">
                        <i class="ri-download-2-line" aria-hidden="true"></i>
                        <span>PDF</span>
                    </a>
                    <button id="theme-toggle" class="theme-btn" aria-label="Cambiar tema visual">
                        <i class="ri-sun-line icon-sun" aria-hidden="true"></i>
                        <i class="ri-moon-line icon-moon" aria-hidden="true"></i>
                    </button>
                </div>
            </header>

            <section id="profile">
                <h2>Perfil Profesional</h2>
                {{PROFILE}}
            </section>

            <section id="experience">
                <h2>Experiencia Laboral</h2>

                <div class="filter-container" aria-label="Filtrar experiencia por tecnología">
                    {{FILTERS}}
                </div>

                {{EXPERIENCE}}
            </section>
        </div>

        <aside class="sidebar-column">
            <section id="contact">
                <h2>Contacto</h2>
                <nav aria-label="Enlaces de contacto">
                    <ul class="contact-list">
                        {{CONTACT}}
                    </ul>
                </nav>
            </section>

            <section id="education">
                <h2>Educación</h2>
                {{EDUCATION}}
            </section>

            <section id="skills">
                <h2>Habilidades</h2>
                <div class="skills-container">
                    {{SKILL_TAGS}}
                </div>
            </section>

            <section id="certifications">
                <h2>Certificaciones</h2>
                <ul class="cert-list">
                    {{CERTIFICATIONS}}
                </ul>
            </section>

            <section id="languages">
                <h2>Idiomas</h2>
                <ul class="lang-list">
                    {{LANGUAGES}}
                </ul>
            </section>
        </aside>
    </main>

    <script src="js/script.js"></script>
</body>

</html>
