/* ═══════════════════════════════════════════════════════════
   GIGI'S CORNER — JAVASCRIPT
   Odoo 17 Frontend JS
   ═══════════════════════════════════════════════════════════ */

/** @odoo-module **/
import { Component, onMounted } from "@odoo/owl";
import publicWidget from "@web/legacy/js/public/public_widget";

// ── SCROLL REVEAL ──────────────────────────────────────────
publicWidget.registry.GigisScrollReveal = publicWidget.Widget.extend({
    selector: '.gc-fade-up',
    start() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('gc-visible');
                }
            });
        }, { threshold: 0.12 });

        document.querySelectorAll('.gc-fade-up').forEach(el => observer.observe(el));
        return this._super(...arguments);
    },
});

// ── COUNTER ANIMATION ─────────────────────────────────────
publicWidget.registry.GigisCounter = publicWidget.Widget.extend({
    selector: '.gc-count-up',
    start() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.counted) {
                    entry.target.dataset.counted = true;
                    const target = parseInt(entry.target.dataset.target || entry.target.innerText);
                    const suffix = entry.target.dataset.suffix || '';
                    let start = 0;
                    const duration = 1800;
                    const step = Math.ceil(target / (duration / 16));
                    const timer = setInterval(() => {
                        start = Math.min(start + step, target);
                        entry.target.innerText = start + suffix;
                        if (start >= target) clearInterval(timer);
                    }, 16);
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('.gc-count-up').forEach(el => observer.observe(el));
        return this._super(...arguments);
    },
});

// ── FORM VALIDATION ───────────────────────────────────────
publicWidget.registry.GigisForm = publicWidget.Widget.extend({
    selector: '#gc-personalizacion-form',
    events: {
        'submit': '_onSubmit',
    },

    _onSubmit(ev) {
        ev.preventDefault();
        const form = ev.target;
        let valid = true;

        form.querySelectorAll('[required]').forEach(field => {
            if (!field.value.trim()) {
                field.style.borderColor = 'var(--gc-coral)';
                field.style.boxShadow = '0 0 0 3px rgba(255,92,100,0.2)';
                valid = false;
            } else {
                field.style.borderColor = '';
                field.style.boxShadow = '';
            }
        });

        if (!valid) {
            const firstError = form.querySelector('[required][value=""]') ||
                               Array.from(form.querySelectorAll('[required]'))
                               .find(f => !f.value.trim());
            if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return;
        }

        // Mostrar loading
        const btn = form.querySelector('.gc-form-submit-btn');
        const originalText = btn.innerHTML;
        btn.innerHTML = '⏳ Enviando...';
        btn.disabled = true;

        // Submit nativo Odoo
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
        }).then(res => res.json())
          .then(data => {
            form.innerHTML = `
                <div class="text-center py-5">
                    <div style="font-size:4rem">🎉</div>
                    <h3 style="font-family:var(--font-title);color:var(--gc-navy);margin-top:1rem">
                        ¡Recibimos tu historia!
                    </h3>
                    <p style="color:var(--gc-gray);max-width:400px;margin:0 auto 1.5rem">
                        Ana y su equipo te contactarán pronto para comenzar a iluminar la historia de tu pequeño. 💛
                    </p>
                    <a href="https://wa.me/525529451680" target="_blank" class="gc-btn-whatsapp">
                        💬 También puedes escribirnos por WhatsApp
                    </a>
                </div>`;
          })
          .catch(() => {
            btn.innerHTML = originalText;
            btn.disabled = false;
            alert('Hubo un error. Por favor intenta de nuevo o escríbenos por WhatsApp.');
          });
    },
});

// ── VIDEO MODAL ───────────────────────────────────────────
publicWidget.registry.GigisVideoModal = publicWidget.Widget.extend({
    selector: '.gc-play-btn',
    events: {
        'click': '_openVideo',
    },

    _openVideo(ev) {
        const btn = ev.currentTarget;
        const videoUrl = btn.dataset.video;
        if (!videoUrl) return;

        const modal = document.createElement('div');
        modal.style.cssText = `
            position:fixed;top:0;left:0;width:100%;height:100%;
            background:rgba(0,0,0,0.88);z-index:99999;
            display:flex;align-items:center;justify-content:center;
        `;
        modal.innerHTML = `
            <div style="position:relative;max-width:800px;width:90%;border-radius:18px;overflow:hidden;">
                <button onclick="this.closest('div').parentElement.remove()"
                    style="position:absolute;top:12px;right:12px;background:rgba(255,255,255,0.2);
                           border:none;color:white;font-size:1.4rem;width:38px;height:38px;
                           border-radius:50%;cursor:pointer;z-index:2">✕</button>
                <video src="${videoUrl}" controls autoplay style="width:100%;display:block;"></video>
            </div>`;
        document.body.appendChild(modal);
        modal.addEventListener('click', e => { if (e.target === modal) modal.remove(); });
    },
});
