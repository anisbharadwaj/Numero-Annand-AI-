// Numero Annand AI - Interactive Script

document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Navbar background on scroll
    window.addEventListener('scroll', () => {
        const header = document.querySelector('header');
        if (window.scrollY > 100) {
            header.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.2)';
        } else {
            header.style.boxShadow = 'var(--shadow-sm)';
        }
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            let isValid = true;
            form.querySelectorAll('[required]').forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.parentElement.classList.add('error');
                } else {
                    field.parentElement.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });

        // Remove error class on input
        form.querySelectorAll('input, select, textarea').forEach(field => {
            field.addEventListener('input', () => {
                if (field.value.trim()) {
                    field.parentElement.classList.remove('error');
                }
            });
        });
    });

    // Number cards animation
    const numberCards = document.querySelectorAll('.number-card');
    numberCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.animation = 'float 2s ease-in-out infinite';
        });
    });

    // Stats counter animation
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .number-card').forEach(el => {
        observer.observe(el);
    });

    // Download report functionality
    const downloadBtn = document.getElementById('downloadReportBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            const name = document.getElementById('name')?.value || 'Report';
            const birthNumber = document.getElementById('birthNumberDisplay')?.textContent || '';
            
            if (!birthNumber) {
                alert('Please generate analysis first');
                return;
            }

            // Create simple text report
            const reportContent = `
NUMERO ANNAND AI - NUMEROLOGY REPORT
=====================================

Name: ${name}
Generated: ${new Date().toLocaleDateString()}

BIRTH NUMBER: ${document.getElementById('birthNumberDisplay')?.textContent}
${document.getElementById('birthNumberName')?.textContent}

DESTINY NUMBER: ${document.getElementById('destinyNumberDisplay')?.textContent}
${document.getElementById('destinyNumberName')?.textContent}

NAME NUMBER: ${document.getElementById('nameNumberDisplay')?.textContent}
${document.getElementById('nameNumberName')?.textContent}

Thank you for using Numero Annand AI!
            `;

            const element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(reportContent));
            element.setAttribute('download', `numerology_report_${Date.now()}.txt`);
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        });
    }

    // Share functionality
    const shareBtn = document.getElementById('shareBtn');
    if (shareBtn) {
        shareBtn.addEventListener('click', () => {
            const text = `Check out my Vedic numerology analysis from Numero Annand AI! My birth number is ${document.getElementById('birthNumberDisplay')?.textContent}. Get your free analysis now!`;
            
            if (navigator.share) {
                navigator.share({
                    title: 'My Vedic Numerology Analysis',
                    text: text,
                    url: window.location.href
                }).catch(err => console.log('Share cancelled'));
            } else {
                // Fallback: Copy to clipboard
                navigator.clipboard.writeText(text).then(() => {
                    alert('Results copied to clipboard!');
                });
            }
        });
    }

    // Language switching
    const languageSelect = document.getElementById('language');
    if (languageSelect) {
        languageSelect.addEventListener('change', (e) => {
            console.log('[v0] Language changed to:', e.target.value);
            // Language change logic here
        });
    }
});

// Utility functions
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Analytics tracking
function trackEvent(eventName, eventData = {}) {
    console.log('[v0] Event:', eventName, eventData);
    // Add your analytics code here
}

// Accessibility improvements
document.addEventListener('keydown', (e) => {
    // Close alerts on Escape
    if (e.key === 'Escape') {
        document.querySelectorAll('.alert').forEach(alert => {
            alert.classList.remove('show');
        });
    }
});

// Dark mode support
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.body.setAttribute('data-theme', 'dark');
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    document.body.setAttribute('data-theme', e.matches ? 'dark' : 'light');
});
