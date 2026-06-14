/* ═══════════════════════════════════════════════════════════
   GIGI'S CORNER — JAVASCRIPT
   Compatible Odoo 17 Community (sin @odoo/owl ni publicWidget)
   ═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

    // ── 1. SCROLL REVEAL ──────────────────────────────────
    // Solo activamos la animación si el navegador soporta IntersectionObserver.
    // Marcamos <html> con .gc-animate para que el CSS oculte y luego revele.
    // Si algo falla, el contenido queda visible (failsafe en CSS).
    try {
        if ('IntersectionObserver' in window) {
            var fadeEls = document.querySelectorAll('.gc-fade-up');
            if (fadeEls.length) {
                document.documentElement.classList.add('gc-animate');

                var observer = new IntersectionObserver(function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('gc-visible');
                            observer.unobserve(entry.target);
                        }
                    });
                }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

                fadeEls.forEach(function (el) { observer.observe(el); });

                // Failsafe: a los 2.5s revela cualquier bloque que siga oculto
                setTimeout(function () {
                    document.querySelectorAll('.gc-fade-up:not(.gc-visible)').forEach(function (el) {
                        el.classList.add('gc-visible');
                    });
                }, 2500);
            }
        }
    } catch (e) {
        document.documentElement.classList.remove('gc-animate');
    }


    // ── 2. CONTADOR ANIMADO (stats) ───────────────────────
    const counterObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting && !entry.target.dataset.counted) {
                entry.target.dataset.counted = 'true';
                var target = parseInt(entry.target.dataset.target || entry.target.innerText);
                var suffix = entry.target.dataset.suffix || '';
                var start = 0;
                var step = Math.ceil(target / 80);
                var timer = setInterval(function () {
                    start = Math.min(start + step, target);
                    entry.target.innerText = start + suffix;
                    if (start >= target) clearInterval(timer);
                }, 20);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.gc-count-up').forEach(function (el) {
        counterObserver.observe(el);
    });


    // ── 3. VALIDACIÓN DEL FORMULARIO ──────────────────────
    var form = document.getElementById('gc-personalizacion-form');
    if (form) {
        form.addEventListener('submit', function (ev) {
            var valid = true;
            var firstError = null;

            form.querySelectorAll('[required]').forEach(function (field) {
                if (!field.value.trim()) {
                    field.style.borderColor = 'var(--gc-coral)';
                    field.style.boxShadow = '0 0 0 3px rgba(255,92,100,0.2)';
                    valid = false;
                    if (!firstError) firstError = field;
                } else {
                    field.style.borderColor = '';
                    field.style.boxShadow = '';
                }
            });

            if (!valid) {
                ev.preventDefault();
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
                return;
            }

            // Loading state
            var btn = form.querySelector('.gc-form-submit-btn');
            if (btn) {
                btn.innerHTML = '⏳ Enviando...';
                btn.disabled = true;
            }
        });

        // Limpiar error al escribir
        form.querySelectorAll('[required]').forEach(function (field) {
            field.addEventListener('input', function () {
                if (field.value.trim()) {
                    field.style.borderColor = '';
                    field.style.boxShadow = '';
                }
            });
        });
    }


    // ── 4. VIDEO MODAL ────────────────────────────────────
    document.querySelectorAll('.gc-play-btn[data-video]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var videoUrl = btn.getAttribute('data-video');
            if (!videoUrl) return;

            var overlay = document.createElement('div');
            overlay.style.cssText = [
                'position:fixed', 'top:0', 'left:0', 'width:100%', 'height:100%',
                'background:rgba(0,0,0,0.88)', 'z-index:99999',
                'display:flex', 'align-items:center', 'justify-content:center',
                'cursor:pointer'
            ].join(';');

            var box = document.createElement('div');
            box.style.cssText = 'position:relative;max-width:820px;width:92%;border-radius:18px;overflow:hidden;';
            box.innerHTML =
                '<button style="position:absolute;top:12px;right:12px;background:rgba(255,255,255,0.18);' +
                'border:none;color:white;font-size:1.4rem;width:40px;height:40px;border-radius:50%;' +
                'cursor:pointer;z-index:2;line-height:1;">✕</button>' +
                '<video src="' + videoUrl + '" controls autoplay playsinline ' +
                'style="width:100%;display:block;max-height:80vh;"></video>';

            overlay.appendChild(box);
            document.body.appendChild(overlay);

            // Cerrar al clickear fuera o en el botón X
            overlay.addEventListener('click', function (e) {
                if (e.target === overlay) overlay.remove();
            });
            box.querySelector('button').addEventListener('click', function () {
                overlay.remove();
            });
        });
    });


    // ── 5. NAVBAR ACTIVE LINK ─────────────────────────────
    var currentPath = window.location.pathname;
    document.querySelectorAll('.gc-navbar .nav-link').forEach(function (link) {
        var href = link.getAttribute('href') || '';
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });


    // ── 6. SMOOTH SCROLL para anclas ─────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

});
