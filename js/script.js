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
    const jobCards = document.querySelectorAll('.job-card');
    
    if (filterButtons.length === 0) return;

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Alternar estado activo del botón presionado
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const selectedFilter = button.getAttribute('data-filter');

            // Control de visibilidad delegando transiciones e interpolación al motor CSS
            jobCards.forEach(card => {
                const cardTechnologies = card.getAttribute('data-tech') || '';
                const matchesFilter = selectedFilter === 'all' || cardTechnologies.toLowerCase().includes(selectedFilter);

                card.classList.toggle('is-hidden', !matchesFilter);
            });
        });
    });
}