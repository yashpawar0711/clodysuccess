/**
 * CLOUDY SUCCESS — MASTER APPLICATION LOGIC
 * Founder: Yash Pawar | pawaryash0711@gmail.com | +91 93560 47461
 * Tagline: Your Vision. Our Digital Solutions.
 */

const confetti = window.confetti;

document.addEventListener('DOMContentLoaded', () => {

  /* =========================================================================
     1. PRELOADER ORCHESTRATION
     ========================================================================= */
  const preloader = document.getElementById('preloader');
  const preloaderBar = document.getElementById('preloader-bar');
  const preloaderStatus = document.getElementById('preloader-status');

  const statusMessages = [
    'Initializing digital studio...',
    'Loading custom design tokens...',
    'Preparing responsive layouts...',
    'Optimizing high-performance assets...',
    'Your Vision. Our Digital Solutions.'
  ];

  let progress = 0;
  let statusIndex = 0;

  const progressInterval = setInterval(() => {
    progress += Math.floor(Math.random() * 14) + 8;
    if (progress > 100) progress = 100;

    if (preloaderBar) {
      preloaderBar.style.width = `${progress}%`;
    }

    const nextStatusIndex = Math.min(
      Math.floor((progress / 100) * statusMessages.length),
      statusMessages.length - 1
    );

    if (nextStatusIndex !== statusIndex && preloaderStatus) {
      statusIndex = nextStatusIndex;
      preloaderStatus.textContent = statusMessages[statusIndex];
    }

    if (progress >= 100) {
      clearInterval(progressInterval);
      setTimeout(() => {
        if (preloader) {
          preloader.classList.add('fade-out');
          setTimeout(() => {
            preloader.remove();
            triggerInitialEntrance();
          }, 600);
        }
      }, 300);
    }
  }, 45);

  /* =========================================================================
     2. AMBIENT CONSTELLATION CANVAS
     ========================================================================= */
  const canvas = document.getElementById('ambient-canvas');
  if (canvas && window.innerWidth > 768) {
    const ctx = canvas.getContext('2d');
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener('resize', () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const particleCount = Math.min(Math.floor((width * height) / 32000), 45);

    class Particle {
      constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.4;
        this.vy = (Math.random() - 0.5) * 0.4;
        this.radius = Math.random() * 1.5 + 0.8;
      }
      update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;
      }
      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(56, 189, 248, 0.4)';
        ctx.fill();
      }
    }

    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }

    function animateParticles() {
      ctx.clearRect(0, 0, width, height);

      for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();

        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 130) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(56, 189, 248, ${0.15 * (1 - dist / 130)})`;
            ctx.lineWidth = 0.7;
            ctx.stroke();
          }
        }
      }
      requestAnimationFrame(animateParticles);
    }
    animateParticles();
  }

  /* =========================================================================
     3. DESKTOP CUSTOM CURSOR
     ========================================================================= */
  const cursor = document.getElementById('custom-cursor');
  const follower = document.getElementById('custom-cursor-follower');

  if (cursor && follower && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    let mouseX = -100;
    let mouseY = -100;
    let followerX = -100;
    let followerY = -100;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursor.style.left = `${mouseX}px`;
      cursor.style.top = `${mouseY}px`;
    });

    const renderFollower = () => {
      followerX += (mouseX - followerX) * 0.16;
      followerY += (mouseY - followerY) * 0.16;
      follower.style.left = `${followerX}px`;
      follower.style.top = `${followerY}px`;
      requestAnimationFrame(renderFollower);
    };
    renderFollower();

    // Hover effect over interactive elements
    const interactiveSelectors = 'a, button, input, select, textarea, .service-card, .portfolio-card, .faq-question';
    document.querySelectorAll(interactiveSelectors).forEach((el) => {
      el.addEventListener('mouseenter', () => follower.classList.add('cursor-hover'));
      el.addEventListener('mouseleave', () => follower.classList.remove('cursor-hover'));
    });
  }

  /* =========================================================================
     4. HEADER SCROLL EFFECT & SCROLL PROGRESS
     ========================================================================= */
  const header = document.getElementById('site-header');
  const scrollProgressBar = document.getElementById('scroll-progress-bar');
  const backToTopBtn = document.getElementById('back-to-top-btn');
  const progressCircle = document.getElementById('progress-circle');

  const circumference = 2 * Math.PI * 20; // r=20 -> 125.66

  const handleScroll = () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;

    // Header styling
    if (header) {
      if (scrollTop > 40) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }

    // Scroll progress bar at top
    if (scrollProgressBar) {
      scrollProgressBar.style.width = `${scrollPercent}%`;
    }

    // Back to top button & circular progress
    if (backToTopBtn && progressCircle) {
      if (scrollTop > 350) {
        backToTopBtn.classList.add('is-visible');
        const offset = circumference - (scrollPercent / 100) * circumference;
        progressCircle.style.strokeDashoffset = offset;
      } else {
        backToTopBtn.classList.remove('is-visible');
      }
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* =========================================================================
     5. NAVIGATION ACTIVE SECTION SPY
     ========================================================================= */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.desktop-nav .nav-link');
  const mobileLinks = document.querySelectorAll('.mobile-nav-links .mobile-link');

  const updateActiveNav = () => {
    const scrollPos = window.scrollY + 140;

    sections.forEach((section) => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach((link) => {
          if (link.getAttribute('data-nav') === id) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
        mobileLinks.forEach((link) => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
      }
    });
  };

  window.addEventListener('scroll', updateActiveNav, { passive: true });

  /* =========================================================================
     6. MOBILE DRAWER NAVIGATION
     ========================================================================= */
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileDrawer = document.getElementById('mobile-drawer');
  const drawerCloseBtn = document.getElementById('drawer-close-btn');
  const drawerBackdrop = document.getElementById('mobile-drawer-backdrop');

  const openDrawer = () => {
    if (!mobileDrawer) return;
    mobileDrawer.classList.add('is-open');
    mobileDrawer.setAttribute('aria-hidden', 'false');
    if (mobileMenuBtn) {
      mobileMenuBtn.classList.add('is-active');
      mobileMenuBtn.setAttribute('aria-expanded', 'true');
    }
    document.body.style.overflow = 'hidden';
  };

  const closeDrawer = () => {
    if (!mobileDrawer) return;
    mobileDrawer.classList.remove('is-open');
    mobileDrawer.setAttribute('aria-hidden', 'true');
    if (mobileMenuBtn) {
      mobileMenuBtn.classList.remove('is-active');
      mobileMenuBtn.setAttribute('aria-expanded', 'false');
    }
    document.body.style.overflow = '';
  };

  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
      if (mobileDrawer.classList.contains('is-open')) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });
  }

  if (drawerCloseBtn) drawerCloseBtn.addEventListener('click', closeDrawer);
  if (drawerBackdrop) drawerBackdrop.addEventListener('click', closeDrawer);

  document.querySelectorAll('.mobile-link, #mobile-drawer-cta').forEach((link) => {
    link.addEventListener('click', closeDrawer);
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileDrawer && mobileDrawer.classList.contains('is-open')) {
      closeDrawer();
    }
  });

  /* =========================================================================
     7. HERO 3D CARD PERSPECTIVE TILT
     ========================================================================= */
  const heroVisual = document.querySelector('.hero-visual-wrapper');
  const heroCard = document.getElementById('hero-3d-card');

  if (heroVisual && heroCard && window.innerWidth > 960) {
    heroVisual.addEventListener('mousemove', (e) => {
      const rect = heroVisual.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = ((y - centerY) / centerY) * -9;
      const rotateY = ((x - centerX) / centerX) * 9;

      heroCard.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
    });

    heroVisual.addEventListener('mouseleave', () => {
      heroCard.style.transform = 'rotateX(0deg) rotateY(0deg) scale(1)';
    });
  }

  /* =========================================================================
     8. VERIFIED ANIMATED NUMBER COUNTERS
     ========================================================================= */
  const statNumbers = document.querySelectorAll('.stat-number');
  let statsTriggered = false;

  const countUpStats = () => {
    if (statsTriggered) return;
    statsTriggered = true;

    statNumbers.forEach((counter) => {
      const target = parseFloat(counter.getAttribute('data-target'));
      const isDecimal = counter.getAttribute('data-decimal') === '1';
      const duration = 1800;
      const steps = 60;
      const stepDuration = duration / steps;
      let current = 0;
      const increment = target / steps;

      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          current = target;
          clearInterval(timer);
        }
        counter.textContent = isDecimal ? current.toFixed(1) : Math.floor(current);
      }, stepDuration);
    });
  };

  /* =========================================================================
     9. SCROLL REVEAL OBSERVER
     ========================================================================= */
  const revealElements = document.querySelectorAll('.reveal-fade-up');

  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const delay = entry.target.getAttribute('data-delay') || 0;
          setTimeout(() => {
            entry.target.classList.add('is-revealed');
          }, delay);

          // If hero stats strip was revealed, trigger numbers
          if (entry.target.querySelector('.stat-number') || entry.target.classList.contains('hero-content')) {
            countUpStats();
          }

          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  revealElements.forEach((el) => revealObserver.observe(el));

  function triggerInitialEntrance() {
    document.querySelectorAll('#hero .reveal-fade-up').forEach((el) => {
      const delay = el.getAttribute('data-delay') || 0;
      setTimeout(() => el.classList.add('is-revealed'), delay);
    });
    countUpStats();
  }

  /* =========================================================================
     10. PORTFOLIO DATA & CASE STUDY MODAL
     ========================================================================= */
  const projectDatabase = {
    corporate: {
      title: 'Apex Horizon Capital',
      category: 'Corporate Business Website',
      year: '2026 Production Standard',
      image: '/assets/portfolio-corporate.jpg',
      desc: 'An institutional web presence designed for a boutique private equity and financial consulting firm. The project emphasizes executive credibility, clear client service pathways, and real-time interactive financial performance telemetry.',
      highlights: [
        'Dark mode aesthetic with electric cyan data visualizations and custom growth metrics',
        'Intuitive investor portal UX with secure document request workflows',
        'Sub-1.2s average load performance across all global test locations',
        'Full lead-capture integration with automated email alerts and WhatsApp routing'
      ],
      tech: ['Vanilla HTML5', 'Chart.js', 'Responsive Grid', 'SEO Schema', 'High-Performance CSS']
    },
    restaurant: {
      title: 'The Obsidian Room',
      category: 'Hospitality & Fine Dining',
      year: '2026 Production Standard',
      image: '/assets/portfolio-restaurant.jpg',
      desc: 'A luxury fine-dining gastronomic showcase engineered with dark slate textures, ambient gold lighting, dynamic seasonal menu categorizations, and an integrated frictionless table reservation flow.',
      highlights: [
        'Interactive culinary dish explorer with dietary filters (Vegan, Gluten-Free, Chef Special)',
        'Table reservation booking bar with instant guest count and date selection',
        'Mobile-first digital menu with touch-friendly navigation and wine pairings',
        'Zero layout shifts (CLS < 0.01) for seamless mobile dining reservations'
      ],
      tech: ['Touch Gestures', 'Mobile Menu', 'WebP Artistry', 'Custom CSS Tokens', 'Booking Engine UX']
    },
    portfolio: {
      title: 'Aeterna Architecture',
      category: 'Personal & Studio Portfolio',
      year: '2026 Production Standard',
      image: '/assets/portfolio-architect.jpg',
      desc: 'A Swiss-inspired minimalist editorial portfolio designed for an award-winning architectural firm. The site allows spatial photography and floorplan blueprints to take center stage with refined typography and smooth transitions.',
      highlights: [
        'Interactive architectural blueprint viewer and split-screen comparison mode',
        'Smooth gallery transitions and full-screen image lightboxes',
        'Editorial serif and mono typography pairing with high legibility',
        'Direct inquiry button with pre-selected project type'
      ],
      tech: ['CSS Grid', 'Minimalist UI', 'Blueprint Lightbox', 'Parallax Scrolling', 'Editorial Typography']
    },
    ecommerce: {
      title: 'Velo Audio Elite',
      category: 'E-Commerce Storefront',
      year: '2026 Production Standard',
      image: '/assets/portfolio-ecommerce.jpg',
      desc: 'A modern direct-to-consumer online storefront for high-end audiophile hardware. Engineered for high conversion with instant cart drawer previews, product color selectors, customer review carousels, and rapid checkout pathways.',
      highlights: [
        'Instant sliding cart drawer with live subtotal and free shipping progress meter',
        'Interactive color variant toggles with smooth product asset swapping',
        'Secure multi-gateway payment architecture (Stripe, Razorpay, Apple Pay)',
        'Speed-tuned product grid with lazy loading and instant search'
      ],
      tech: ['Cart Drawer UX', 'E-Commerce Core', 'Payment Gateways', 'Inventory Filter', 'Conversion Funnel']
    },
    saas: {
      title: 'Aurora Cloud Analytics',
      category: 'SaaS Dashboard Web Application',
      year: '2026 Production Standard',
      image: '/assets/portfolio-saas.jpg',
      desc: 'A futuristic telemetry and subscription analytics web app interface designed for SaaS startups. Features glowing neon charts, live MRR tracking, user cohort trends, churn probability monitoring, and role-based access management.',
      highlights: [
        'Real-time data visualization with neon area charts and custom SVG tooltips',
        'Modular widget dashboard with customizable metric card arrangements',
        'High contrast dark UI complying with WCAG 2.1 accessibility standards',
        'Scalable component architecture ready for backend API hydration'
      ],
      tech: ['API Ready', 'Dark Mode UI', 'Single Page App', 'Custom SVG Charts', 'Data Visualizations']
    },
    agency: {
      title: 'Nebula Digital Studio',
      category: 'Creative Agency Website',
      year: '2026 Production Standard',
      image: '/assets/portfolio-agency.jpg',
      desc: 'A boundary-pushing motion-heavy digital studio website designed to captivate prospective clients. Incorporates electric laser glows, 3D floating visual layers, magnetic button interactions, and award-winning micro-animations.',
      highlights: [
        'Advanced CSS keyframe motion choreography and subtle layered depth',
        'Magnetic cursor hover physics on all primary call-to-actions',
        'Interactive project carousel with smooth keyboard and drag navigation',
        'Strictly optimized for 60fps rendering without memory leaks'
      ],
      tech: ['CSS Keyframes', 'Custom Motion', 'WebGL Ambience', 'Fluid Typography', 'Magnetic Physics']
    }
  };

  // Portfolio Filtering
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioCards = document.querySelectorAll('.portfolio-card');

  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      filterBtns.forEach((b) => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const filterValue = btn.getAttribute('data-filter');

      portfolioCards.forEach((card) => {
        const category = card.getAttribute('data-category');
        if (filterValue === 'all' || category === filterValue) {
          card.style.display = 'flex';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, 40);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'translateY(20px)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 250);
        }
      });
    });
  });

  // Modal logic
  const modal = document.getElementById('project-modal');
  const modalBackdrop = document.getElementById('modal-backdrop');
  const modalCloseBtn = document.getElementById('modal-close-btn');
  const modalDismissBtn = document.getElementById('modal-dismiss-btn');
  const modalImg = document.getElementById('modal-project-image');
  const modalCategory = document.getElementById('modal-project-category');
  const modalTitle = document.getElementById('modal-project-title');
  const modalDesc = document.getElementById('modal-project-desc');
  const modalHighlights = document.getElementById('modal-project-highlights');
  const modalTech = document.getElementById('modal-project-tech');
  const modalDiscussBtn = document.getElementById('modal-discuss-btn');

  const openModal = (projectId) => {
    const data = projectDatabase[projectId];
    if (!data || !modal) return;

    modalImg.src = data.image;
    modalImg.alt = `${data.title} - ${data.category}`;
    modalCategory.textContent = data.category;
    modalTitle.textContent = data.title;
    modalDesc.textContent = data.desc;

    // Highlights
    modalHighlights.innerHTML = '';
    data.highlights.forEach((item) => {
      const li = document.createElement('li');
      li.textContent = item;
      modalHighlights.appendChild(li);
    });

    // Tech
    modalTech.innerHTML = '';
    data.tech.forEach((t) => {
      const tag = document.createElement('span');
      tag.className = 'tech-tag';
      tag.textContent = t;
      modalTech.appendChild(tag);
    });

    modal.hidden = false;
    modal.removeAttribute('hidden');
    modal.classList.add('is-active');
    document.body.style.overflow = 'hidden';
  };

  const closeModal = () => {
    if (!modal) return;
    modal.classList.remove('is-active');
    modal.hidden = true;
    modal.setAttribute('hidden', '');
    document.body.style.overflow = '';
  };

  document.querySelectorAll('.view-case-btn, .portfolio-card').forEach((el) => {
    el.addEventListener('click', (e) => {
      const btn = el.classList.contains('view-case-btn') ? el : el.querySelector('.view-case-btn');
      if (btn) {
        e.preventDefault();
        const projectId = btn.getAttribute('data-project-id');
        if (projectId) openModal(projectId);
      }
    });
  });

  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
  if (modalDismissBtn) modalDismissBtn.addEventListener('click', closeModal);
  if (modalBackdrop) modalBackdrop.addEventListener('click', closeModal);
  
  if (modalDiscussBtn) {
    modalDiscussBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const currentCategory = modalCategory ? modalCategory.textContent : '';
      const currentTitle = modalTitle ? modalTitle.textContent : '';
      closeModal();

      const serviceSelect = document.getElementById('select-service');
      const messageText = document.getElementById('textarea-message');

      if (serviceSelect) {
        if (currentCategory.includes('E-Commerce')) {
          serviceSelect.value = 'E-commerce Website Development';
        } else if (currentCategory.includes('Portfolio')) {
          serviceSelect.value = 'Portfolio Websites';
        } else if (currentCategory.includes('SaaS') || currentCategory.includes('Web App')) {
          serviceSelect.value = 'Web Applications';
        } else {
          serviceSelect.value = 'Business Website Development';
        }
      }

      if (messageText && currentTitle) {
        messageText.value = `Hello Yash! I am interested in building a project similar to "${currentTitle}". Let's discuss scope, quotation, and timeline!`;
      }

      const contactSec = document.getElementById('contact');
      if (contactSec) {
        contactSec.scrollIntoView({ behavior: 'smooth' });
        setTimeout(() => {
          const nameInput = document.getElementById('input-name');
          if (nameInput) nameInput.focus();
        }, 500);
      }
    });
  }

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && !modal.hidden) {
      closeModal();
    }
  });

  /* =========================================================================
     12. QUICK ACTIONS FROM SERVICES & PRICING
     ========================================================================= */
  // Service enquiry buttons
  document.querySelectorAll('.service-enquire-btn, .footer-service-link').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const serviceName = btn.getAttribute('data-service');
      const serviceSelect = document.getElementById('select-service');
      if (serviceSelect && serviceName) {
        serviceSelect.value = serviceName;
        // Scroll to contact form smoothly
        const contactSec = document.getElementById('contact');
        if (contactSec) {
          contactSec.scrollIntoView({ behavior: 'smooth' });
          const nameInput = document.getElementById('input-name');
          if (nameInput) setTimeout(() => nameInput.focus(), 600);
        }
      }
    });
  });

  // Pricing plan buttons
  document.querySelectorAll('.select-tier-btn').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const plan = btn.getAttribute('data-plan');
      const serviceSelect = document.getElementById('select-service');
      const messageText = document.getElementById('textarea-message');

      if (serviceSelect) {
        if (plan === 'Starter Website') serviceSelect.value = 'Business Website Development';
        else if (plan === 'Business Website') serviceSelect.value = 'Business Website Development';
        else serviceSelect.value = 'Web Applications';
      }

      if (messageText) {
        messageText.value = `I am interested in the ${plan} package. Let's discuss details and next steps!`;
      }
    });
  });

  /* =========================================================================
     13. FAQ ACCORDION WITH ACCESSIBILITY
     ========================================================================= */
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach((item) => {
    const questionBtn = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');

    if (questionBtn && answer) {
      questionBtn.addEventListener('click', () => {
        const isOpen = item.classList.contains('is-open');

        // Close all other items
        faqItems.forEach((other) => {
          if (other !== item) {
            other.classList.remove('is-open');
            const otherBtn = other.querySelector('.faq-question');
            const otherAns = other.querySelector('.faq-answer');
            if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
            if (otherAns) {
              otherAns.style.maxHeight = null;
              otherAns.hidden = true;
            }
          }
        });

        // Toggle current item
        if (isOpen) {
          item.classList.remove('is-open');
          questionBtn.setAttribute('aria-expanded', 'false');
          answer.style.maxHeight = null;
          answer.hidden = true;
        } else {
          item.classList.add('is-open');
          questionBtn.setAttribute('aria-expanded', 'true');
          answer.hidden = false;
          answer.style.maxHeight = `${answer.scrollHeight + 20}px`;
        }
      });
    }
  });

  /* =========================================================================
     14. CONTACT FORM VALIDATION & DISPATCH
     ========================================================================= */
  const form = document.getElementById('project-enquiry-form');
  const successCard = document.getElementById('form-success-card');
  const successMessageText = document.getElementById('success-message-text');
  const successWhatsAppLink = document.getElementById('success-whatsapp-link');
  const resetFormBtn = document.getElementById('reset-form-btn');

  const inputName = document.getElementById('input-name');
  const inputEmail = document.getElementById('input-email');
  const inputPhone = document.getElementById('input-phone');
  const selectService = document.getElementById('select-service');
  const selectBudget = document.getElementById('select-budget');
  const textareaMessage = document.getElementById('textarea-message');

  const submitFormBtn = document.getElementById('submit-form-btn');
  const sendWhatsAppDirectBtn = document.getElementById('send-whatsapp-direct-btn');
  const sendEmailDirectBtn = document.getElementById('send-email-direct-btn');

  // Real-time validation helper
  const validateField = (input, errorId, validatorFn, errorMsg) => {
    const errorEl = document.getElementById(errorId);
    const parentField = input.closest('.form-field');
    const isValid = validatorFn(input.value.trim());

    if (!isValid) {
      if (parentField) parentField.classList.add('has-error');
      if (errorEl) errorEl.textContent = errorMsg;
      return false;
    } else {
      if (parentField) parentField.classList.remove('has-error');
      if (errorEl) errorEl.textContent = '';
      return true;
    }
  };

  const isNotEmpty = (val) => val.length >= 2;
  const isValidEmail = (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
  const isValidPhone = (val) => val.replace(/[\s\-\(\)\+]/g, '').length >= 8;
  const isSelected = (val) => val !== '';
  const isMessageValid = (val) => val.length >= 8;

  // Real-time input listeners
  if (inputName) {
    inputName.addEventListener('blur', () =>
      validateField(inputName, 'error-name', isNotEmpty, 'Please enter your full name (at least 2 characters).')
    );
    inputName.addEventListener('input', () => {
      if (inputName.closest('.form-field').classList.contains('has-error')) {
        validateField(inputName, 'error-name', isNotEmpty, 'Please enter your full name.');
      }
    });
  }

  if (inputEmail) {
    inputEmail.addEventListener('blur', () =>
      validateField(inputEmail, 'error-email', isValidEmail, 'Please enter a valid email address.')
    );
    inputEmail.addEventListener('input', () => {
      if (inputEmail.closest('.form-field').classList.contains('has-error')) {
        validateField(inputEmail, 'error-email', isValidEmail, 'Please enter a valid email address.');
      }
    });
  }

  if (inputPhone) {
    inputPhone.addEventListener('blur', () =>
      validateField(inputPhone, 'error-phone', isValidPhone, 'Please enter a valid contact / WhatsApp number.')
    );
    inputPhone.addEventListener('input', () => {
      if (inputPhone.closest('.form-field').classList.contains('has-error')) {
        validateField(inputPhone, 'error-phone', isValidPhone, 'Please enter a valid contact number.');
      }
    });
  }

  if (selectService) {
    selectService.addEventListener('change', () =>
      validateField(selectService, 'error-service', isSelected, 'Please select the service you require.')
    );
  }

  if (textareaMessage) {
    textareaMessage.addEventListener('blur', () =>
      validateField(textareaMessage, 'error-message', isMessageValid, 'Please describe your project vision (at least 8 characters).')
    );
  }

  // Validate entire form
  const validateForm = () => {
    const v1 = validateField(inputName, 'error-name', isNotEmpty, 'Please enter your full name.');
    const v2 = validateField(inputEmail, 'error-email', isValidEmail, 'Please enter a valid email address.');
    const v3 = validateField(inputPhone, 'error-phone', isValidPhone, 'Please enter a valid contact number.');
    const v4 = validateField(selectService, 'error-service', isSelected, 'Please select a service.');
    const v5 = validateField(textareaMessage, 'error-message', isMessageValid, 'Please provide a brief project description.');
    return v1 && v2 && v3 && v4 && v5;
  };

  // Build WhatsApp pre-filled text
  const generateEnquiryText = () => {
    return `*New Project Enquiry — Cloudy Success*
👤 *Client Name:* ${inputName.value.trim()}
📧 *Email:* ${inputEmail.value.trim()}
📱 *Phone:* ${inputPhone.value.trim()}
🛠️ *Required Service:* ${selectService.value}
💰 *Estimated Budget:* ${selectBudget.value}

📝 *Project Details:*
"${textareaMessage.value.trim()}"

Sent via cloudy-success.com`;
  };

  // Form Submit Handler
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      if (!validateForm()) {
        const firstError = form.querySelector('.has-error input, .has-error select, .has-error textarea');
        if (firstError) firstError.focus();
        return;
      }

      // Simulate sending state
      submitFormBtn.classList.add('is-submitting');
      submitFormBtn.disabled = true;

      const enquiryText = generateEnquiryText();
      const waUrl = `https://api.whatsapp.com/send?phone=919356047461&text=${encodeURIComponent(enquiryText)}`;

      // Save to localStorage as a safety copy
      try {
        localStorage.setItem(
          'cloudy_last_enquiry',
          JSON.stringify({
            name: inputName.value.trim(),
            email: inputEmail.value.trim(),
            phone: inputPhone.value.trim(),
            service: selectService.value,
            budget: selectBudget.value,
            message: textareaMessage.value.trim(),
            submittedAt: new Date().toISOString()
          })
        );
      } catch (err) {
        console.warn('LocalStorage save skipped');
      }

      setTimeout(() => {
        submitFormBtn.classList.remove('is-submitting');
        submitFormBtn.disabled = false;

        // Trigger celebratory confetti
        try {
          confetti({
            particleCount: 80,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#38bdf8', '#2563eb', '#10b981', '#ffffff']
          });
        } catch (err) {
          // fallback if confetti fails
        }

        // Hide form, show success card
        form.hidden = true;
        if (successCard) {
          successCard.hidden = false;
          if (successWhatsAppLink) {
            successWhatsAppLink.href = waUrl;
          }
          if (successMessageText) {
            successMessageText.textContent = `Thank you, ${inputName.value.trim()}! Your project enquiry has been generated. Click the button below to send it directly to Yash Pawar on WhatsApp (+91 93560 47461).`;
          }
        }
      }, 700);
    });
  }

  // Direct WhatsApp Send Button (Always opens prefilled WhatsApp chat!)
  if (sendWhatsAppDirectBtn) {
    sendWhatsAppDirectBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const name = inputName && inputName.value.trim() ? inputName.value.trim() : 'Prospective Client';
      const service = selectService && selectService.value ? selectService.value : 'Website Development / Redesign';
      const budget = selectBudget && selectBudget.value ? selectBudget.value : 'To Be Discussed';
      const userMsg = inputMessage && inputMessage.value.trim() ? inputMessage.value.trim() : 'I would like to discuss a website project with Cloudy Success.';

      const message = `Hello Yash! I am reaching out regarding a website project on Cloudy Success:
• Name: ${name}
• Required Service: ${service}
• Estimated Budget: ${budget}
• Details: ${userMsg}

Please let me know when we can discuss!`;

      const waUrl = `https://api.whatsapp.com/send?phone=919356047461&text=${encodeURIComponent(message)}`;
      window.location.href = waUrl;
    });
  }

  // Direct Email Send Button (Always opens prefilled email draft!)
  if (sendEmailDirectBtn) {
    sendEmailDirectBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const name = inputName && inputName.value.trim() ? inputName.value.trim() : 'Prospective Client';
      const service = selectService && selectService.value ? selectService.value : 'Website Development / Consultation';
      const budget = selectBudget && selectBudget.value ? selectBudget.value : 'To Be Discussed';
      const phone = inputPhone && inputPhone.value.trim() ? inputPhone.value.trim() : 'Not provided';
      const userMsg = inputMessage && inputMessage.value.trim() ? inputMessage.value.trim() : 'I would like to discuss a website project with Cloudy Success.';

      const subject = `Website Project Enquiry: ${name} - ${service}`;
      const body = `Hello Yash Pawar,

I would like to discuss a website project with Cloudy Success:

• Client / Brand: ${name}
• Required Service: ${service}
• Estimated Budget: ${budget}
• Contact Phone: ${phone}

Project Details & Requirements:
${userMsg}

Looking forward to your reply!`;

      openUniversalEmail(subject, body);
    });
  }

  // Reset form handler
  if (resetFormBtn) {
    resetFormBtn.addEventListener('click', () => {
      form.reset();
      form.hidden = false;
      if (successCard) successCard.hidden = true;
    });
  }

  // Year Auto-Update
  const yearEl = document.getElementById('current-year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  /* =========================================================================
     25. THEME SWITCHER (DARK & WHITE / LIGHT MODE)
     ========================================================================= */
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const drawerThemeToggleBtn = document.getElementById('drawer-theme-toggle-btn');
  const htmlRoot = document.documentElement;

  function updateThemeUI(theme) {
    const isLight = theme === 'light';
    const accessibleLabel = isLight ? 'Switch to Dark Mode' : 'Switch to White (Light) Mode';

    if (themeToggleBtn) {
      themeToggleBtn.setAttribute('aria-label', accessibleLabel);
      themeToggleBtn.setAttribute('title', accessibleLabel);
    }
    if (drawerThemeToggleBtn) {
      drawerThemeToggleBtn.setAttribute('aria-label', accessibleLabel);
      const textElem = drawerThemeToggleBtn.querySelector('.theme-mode-text');
      if (textElem) {
        textElem.textContent = isLight ? 'Dark Mode' : 'White Mode';
      }
    }
  }

  function applyTheme(theme) {
    if (theme === 'light') {
      htmlRoot.setAttribute('data-theme', 'light');
      document.body.setAttribute('data-theme', 'light');
    } else {
      htmlRoot.setAttribute('data-theme', 'dark');
      document.body.setAttribute('data-theme', 'dark');
    }
    localStorage.setItem('cloudy_theme', theme);
    updateThemeUI(theme);
  }

  function toggleTheme() {
    const currentTheme = htmlRoot.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
    const nextTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(nextTheme);
  }

  // Initialize theme on load from storage (Default to CloudRegex Light & Contrast theme)
  let savedTheme = localStorage.getItem('cloudy_theme');
  if (savedTheme !== 'dark') {
    savedTheme = 'light';
    localStorage.setItem('cloudy_theme', 'light');
  }
  applyTheme(savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', toggleTheme);
  }
  if (drawerThemeToggleBtn) {
    drawerThemeToggleBtn.addEventListener('click', toggleTheme);
  }

  /* =========================================================================
     26. DYNAMIC PRICING HYDRATOR (SYNC WITH DJANGO ADMIN PORTAL)
     ========================================================================= */
  async function hydrateDynamicPricing() {
    try {
      const response = await fetch('/api/pricing/');
      if (!response.ok) return;
      const data = await response.json();
      if (data && data.success && Array.isArray(data.tiers) && data.tiers.length > 0) {
        const pricingGrid = document.querySelector('.pricing-grid');
        if (pricingGrid) {
          data.tiers.forEach((tier) => {
            const cards = pricingGrid.querySelectorAll('.pricing-card');
            cards.forEach((card) => {
              const nameEl = card.querySelector('.package-name');
              if (nameEl && nameEl.textContent.trim().toLowerCase() === tier.name.trim().toLowerCase()) {
                const amountEl = card.querySelector('.amount');
                if (amountEl && tier.price) amountEl.textContent = tier.price;
                const currEl = card.querySelector('.currency');
                if (currEl && tier.currency_symbol) currEl.textContent = tier.currency_symbol;
                const periodEl = card.querySelector('.period');
                if (periodEl && tier.period) periodEl.textContent = tier.period;
                const usdEl = card.querySelector('.usd-equivalent');
                if (usdEl && tier.usd_equivalent) usdEl.textContent = tier.usd_equivalent;
              }
            });
          });
        }
      }
    } catch (e) {
      // Graceful fallback to static pre-rendered cards
    }
  }
  hydrateDynamicPricing();

  /* =========================================================================
     27. UNIVERSAL EMAIL HANDLER & SMART FALLBACK (GMAIL + MAILTO)
     ========================================================================= */
  function showToast(message, duration = 3200) {
    let toast = document.getElementById('cloudy-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'cloudy-toast';
      toast.className = 'cloudy-floating-toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('is-visible');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
      toast.classList.remove('is-visible');
    }, duration);
  }

  function openUniversalEmail(customSubject, customBody) {
    const email = 'pawaryash0711@gmail.com';
    const subject = customSubject || 'Website Project Enquiry - Cloudy Success';
    const body = customBody || 'Hello Yash Pawar,\n\nI would like to discuss a website project with Cloudy Success.';
    
    const mailtoUrl = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    const gmailUrl = `https://mail.google.com/mail/?view=cm&fs=1&to=${email}&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    
    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    
    if (isMobile) {
      window.location.href = mailtoUrl;
      showToast(`✉️ Opening Mail app for ${email}...`);
    } else {
      // Desktop: Open Gmail compose in new tab directly (guaranteed to work even if Windows Mail is unconfigured)
      const newWin = window.open(gmailUrl, '_blank');
      if (!newWin || newWin.closed || typeof newWin.closed === 'undefined') {
        window.location.href = mailtoUrl;
      }
      showToast(`✉️ Opening Gmail Compose for ${email}`);
    }
  }

  function initUniversalEmailHandler() {
    document.addEventListener('click', (e) => {
      const emailLink = e.target.closest('a[href^="mailto:"], .dock-email');
      if (emailLink && emailLink.id !== 'send-email-direct-btn') {
        e.preventDefault();
        const href = emailLink.getAttribute('href') || '';
        let subject = 'Website Project Enquiry - Cloudy Success';
        let body = 'Hello Yash, I would like to discuss a website project with Cloudy Success.';
        if (href.includes('subject=')) {
          try {
            const urlParams = new URLSearchParams(href.replace(/^mailto:[^?]*\?/, ''));
            if (urlParams.get('subject')) subject = urlParams.get('subject');
            if (urlParams.get('body')) body = urlParams.get('body');
          } catch(err) {}
        }
        openUniversalEmail(subject, body);
      }
    });
  }
  initUniversalEmailHandler();

  /* =========================================================================
     28. INTERACTIVE CLICK ANIMATIONS FOR ALL BOXES
     ========================================================================= */
  function initBoxClickAnimation() {
    const boxSelectors = [
      '.service-card',
      '.portfolio-card',
      '.process-step',
      '.pricing-card',
      '.guarantee-card',
      '.about-card',
      '.founder-card',
      '.contact-info-card',
      '.contact-form-card',
      '.faq-item',
      '.portfolio-cta-banner',
      '.testimonial-invitation',
      '.hero-stat-item',
      '.info-item',
      '.glass-panel'
    ].join(', ');

    document.querySelectorAll(boxSelectors).forEach(box => {
      box.addEventListener('click', function(e) {
        if (e.target.closest('a, button, input, select, textarea')) return;

        const rect = box.getBoundingClientRect();
        const ripple = document.createElement('span');
        ripple.className = 'box-click-ripple';
        
        const size = Math.max(rect.width, rect.height) * 1.5;
        const x = (e.clientX ? (e.clientX - rect.left) : (rect.width / 2)) - size / 2;
        const y = (e.clientY ? (e.clientY - rect.top) : (rect.height / 2)) - size / 2;
        
        ripple.style.width = `${size}px`;
        ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;

        box.appendChild(ripple);
        box.classList.add('box-clicked-active');

        setTimeout(() => {
          ripple.remove();
          box.classList.remove('box-clicked-active');
        }, 550);
      });
    });
  }
  initBoxClickAnimation();

});
