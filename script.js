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

    // Verificar preferencia guardada o del sistema operativo
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.classList.add('dark-mode');
        themeToggleBtn.textContent = '☀️';
    } else {
        themeToggleBtn.textContent = '🌙';
    }

    // Evento Click
    themeToggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
            themeToggleBtn.textContent = '☀️';
        } else {
            localStorage.setItem('theme', 'light');
            themeToggleBtn.textContent = '🌙';
        }
    });
}

/* ==========================================================================
   2. ANIMACIÓN AL HACER SCROLL (SCROLL REVEAL)
   ========================================================================== */
function initScrollReveal() {
    // Configuramos el observador nativo de alta eficiencia
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
                // Una vez revelado, dejamos de observarlo para ahorrar rendimiento
                observer.unobserve(entry.target); 
            }
        });
    }, {
        threshold: 0.1, // Se activa cuando el 10% del elemento es visible
        rootMargin: '0px 0px -50px 0px' // Margen inferior para anticipar la carga
    });

    // Seleccionamos las tarjetas de experiencia, educación y perfil
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
            // 1. Cambiar estado visual del botón activo
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // 2. Obtener la tecnología seleccionada
            const selectedFilter = button.getAttribute('data-filter');

            // 3. Filtrar las tarjetas de experiencia laboral
            jobCards.forEach(card => {
                const cardTechnologies = card.getAttribute('data-tech') || '';
                
                // Si el filtro es "all" o la tarjeta contiene el string del filtro
                if (selectedFilter === 'all' || cardTechnologies.toLowerCase().includes(selectedFilter)) {
                    // Animación sutil al reaparecer
                    card.style.display = 'block';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'scale(1)';
                    }, 10);
                } else {
                    // Ocultar de forma limpia
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300); // Espera a que termine la transición CSS si existe
                }
            });
        });
    });
}