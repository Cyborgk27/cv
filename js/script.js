/* ==========================================================================
   CV INTERACTIVO - SCRIPT PRINCIPAL
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initScrollReveal();
    initJobFilter();
});

/* ==========================================================================
   1. MODO OSCURO (THEME TOGGLE)
   ========================================================================== */
function initThemeToggle() {
    const themeToggleBtn = document.getElementById('theme-toggle');
    if (!themeToggleBtn) return;

    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Sincronizar el estado inicial lógico
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.classList.add('dark-mode');
    }

    // El evento muta el estado del body; el CSS controla qué icono renderizar
    themeToggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
}

/* ==========================================================================
   2. ANIMACIÓN AL HACER SCROLL (SCROLL REVEAL)
   ========================================================================== */
function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
                observer.unobserve(entry.target); 
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    const cards = document.querySelectorAll('.job-card, .education-card, #profile');
    cards.forEach(card => {
        card.classList.add('reveal-hidden');
        observer.observe(card);
    });
}

/* ==========================================================================
   3. FILTRADO DINÁMICO DE EXPERIENCIA
   ========================================================================== */
function initJobFilter() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const blocks = document.querySelectorAll('.company-block');

    if (filterButtons.length === 0 || blocks.length === 0) return;

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Alternar estado activo del botón presionado
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const selectedFilter = button.getAttribute('data-filter');

            // Se filtra a nivel de cargo y se oculta el empleador si no queda ninguno visible
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