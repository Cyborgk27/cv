/* ==========================================================================
   CV INTERACTIVO — SCRIPT PRINCIPAL
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initScrollReveal();
    initJobFilter();
});

/* ==========================================================================
   1. TEMA (dark-first, respeta preferencia del sistema)
   ========================================================================== */
function initTheme() {
    const root = document.documentElement;
    const button = document.getElementById('theme-toggle');

    const saved = localStorage.getItem('theme');
    const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
    const initial = saved || (prefersLight ? 'light' : 'dark');
    root.dataset.theme = initial;

    if (!button) return;

    const syncLabel = () => {
        button.setAttribute(
            'aria-label',
            root.dataset.theme === 'dark' ? 'Activar tema claro' : 'Activar tema oscuro'
        );
    };
    syncLabel();

    button.addEventListener('click', () => {
        const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
        root.dataset.theme = next;
        localStorage.setItem('theme', next);
        syncLabel();
    });
}

/* ==========================================================================
   2. APARICIÓN AL HACER SCROLL
   ========================================================================== */
function initScrollReveal() {
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) return;

    const targets = document.querySelectorAll('.company-block, .project-card, .skill-group');
    if (!targets.length) return;

    const observer = new IntersectionObserver(
        entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('reveal-active');
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );

    targets.forEach(target => {
        target.classList.add('reveal-hidden');
        observer.observe(target);
    });
}

/* ==========================================================================
   3. FILTRO DE EXPERIENCIA
   El filtro opera por cargo: oculta los que no coinciden y esconde el
   empleador cuando no queda ninguno visible.
   ========================================================================== */
function initJobFilter() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const blocks = document.querySelectorAll('.company-block');

    if (filterButtons.length === 0 || blocks.length === 0) return;

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const selectedFilter = button.getAttribute('data-filter');

            blocks.forEach(block => {
                const positions = block.querySelectorAll('.position');
                let visible = 0;

                positions.forEach(position => {
                    const positionTech = (position.getAttribute('data-tech') || '').toLowerCase();
                    const matchesFilter =
                        selectedFilter === 'all' || positionTech.includes(selectedFilter);

                    position.classList.toggle('is-hidden', !matchesFilter);
                    if (matchesFilter) visible++;
                });

                block.classList.toggle('is-hidden', visible === 0);
            });
        });
    });
}
