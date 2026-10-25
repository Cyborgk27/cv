<!doctype html>
<html lang="{{LANG}}" data-theme="dark">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>{{PAGE_TITLE}}</title>
    <meta name="description" content="{{META_DESCRIPTION}}" />
    <meta name="keywords" content="{{META_KEYWORDS}}" />
    <meta name="author" content="{{NAME}}" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="{{SITE_URL}}" />

    <meta property="og:type" content="profile" />
    <meta property="og:title" content="{{NAME}} | {{SUBTITLE}}" />
    <meta property="og:description" content="{{META_DESCRIPTION}}" />
    <meta property="og:url" content="{{SITE_URL}}" />
    <meta property="og:site_name" content="CV {{NAME}}" />
    <meta property="og:image" content="{{SITE_URL}}assets/og/og-image.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="{{NAME}} — {{SUBTITLE}}" />
    <meta property="og:locale" content="es_EC" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{{NAME}} | {{SUBTITLE}}" />
    <meta name="twitter:description" content="{{META_DESCRIPTION}}" />
    <meta name="twitter:image" content="{{SITE_URL}}assets/og/og-image.png" />

    <meta name="theme-color" content="#0b0f14" media="(prefers-color-scheme: dark)" />
    <meta name="theme-color" content="#f6f7f9" media="(prefers-color-scheme: light)" />

    <script>
        (function () {
            var saved = localStorage.getItem("theme");
            if (!saved) {
                saved = window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
            }
            document.documentElement.dataset.theme = saved;
        })();
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&family=JetBrains+Mono:wght@400;600&display=swap" />
    <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0,0&icon_names=api,arrow_outward,check_circle,cloud_sync,code,dark_mode,dashboard,data_object,database,deployed_code,dns,download,folder_special,gpp_maybe,hub,layers,light_mode,mail,memory,merge,monitoring,open_in_new,palette,query_stats,school,security,shield,storage,sync,terminal,timeline,translate,web,widgets,work,workspace_premium&display=block" />

    <link rel="stylesheet" href="css/styles.css" />

    <link rel="icon" type="image/svg+xml" href="assets/icons/favicon.svg" />
    <link rel="icon" type="image/png" sizes="32x32" href="assets/icons/favicon-32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="assets/icons/favicon-16.png" />
    <link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png" />
    <link rel="manifest" href="site.webmanifest" />

    <script type="application/ld+json">{{JSONLD}}</script>
</head>

<body>
    <a class="skip-link" href="#main">Saltar al contenido</a>

    <div class="page">
        <header class="hero">
            <div class="terminal">
                <div class="terminal-bar">
                    <span class="dot dot-r"></span>
                    <span class="dot dot-y"></span>
                    <span class="dot dot-g"></span>
                    <p class="terminal-path">kevin@guayaquil:~$ <span class="cmd">whoami</span></p>
                </div>

                <div class="terminal-body">
                    <div class="avatar" aria-hidden="true">
                        <span>KC</span>
                    </div>

                    <div class="hero-text">
                        <h1>{{NAME}}</h1>
                        <p class="role"><span class="chev">&gt;</span> {{SUBTITLE}}</p>
                        <p class="status">
                            <span class="pulse" aria-hidden="true"></span>
                            Disponible para oportunidades · {{LOCATION}}
                        </p>

                        <nav class="actions" aria-label="Enlaces de contacto y descarga">
                            {{ACTIONS}}
                        </nav>
                    </div>
                </div>
            </div>

            <ul class="stats">
                {{STATS}}
            </ul>
        </header>

        <main id="main" class="layout">
            <div class="col-main">
                <section id="profile">
                    <h2><span class="marker">//</span> perfil</h2>
                    {{PROFILE}}
                </section>

                <section id="experience">
                    <h2><span class="marker">//</span> experiencia</h2>

                    <div class="filter-container" aria-label="Filtrar experiencia por tecnología">
                        {{FILTERS}}
                    </div>

                    {{EXPERIENCE}}
                </section>

                <section id="projects">
                    <h2><span class="marker">//</span> proyectos</h2>
                    <div class="projects-grid">
                        {{PROJECTS}}
                    </div>
                </section>
            </div>

            <aside class="col-side">
                <section id="skills">
                    <h2><span class="marker">//</span> skills</h2>
                    {{SKILLS}}
                </section>

                <section id="certifications">
                    <h2><span class="marker">//</span> certificaciones</h2>
                    <ul class="cert-list">
                        {{CERTIFICATIONS}}
                    </ul>
                </section>

                <section id="education">
                    <h2><span class="marker">//</span> educación</h2>
                    {{EDUCATION}}
                </section>

                <section id="languages">
                    <h2><span class="marker">//</span> idiomas</h2>
                    <ul class="lang-list">
                        {{LANGUAGES}}
                    </ul>
                </section>
            </aside>
        </main>

        <footer class="site-footer">
            <p class="footer-mono">built with <span class="hl">python</span> + <span class="hl">libreoffice</span>
                · <span class="hl">vanilla js</span></p>
            <p class="footer-meta">actualizado {{UPDATED}} · <a href="{{PDF_HREF}}">descargar pdf</a></p>
        </footer>
    </div>

    <button id="theme-toggle" class="theme-toggle" aria-label="Cambiar tema visual" title="Cambiar tema">
        <span class="material-symbols-rounded icon-sun" aria-hidden="true">light_mode</span>
        <span class="material-symbols-rounded icon-moon" aria-hidden="true">dark_mode</span>
    </button>

    <script src="js/script.js"></script>
</body>

</html>
