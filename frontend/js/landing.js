document.addEventListener('DOMContentLoaded', () => {

  // ——— Navbar scroll effect ———
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
  });

  // ——— Parallax Hero Background ———
  const heroBg = document.getElementById('heroBg');
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (heroBg && y < window.innerHeight * 1.5) {
      heroBg.style.transform = `translateY(${y * 0.35}px)`;
    }
  }, { passive: true });

  // ——— Image Reveal (mouse cursor mask) ———
  const reveal = document.getElementById('image-reveal');
  const revealImg = reveal ? reveal.querySelector('.img-reveal') : null;
  const revealCursor = document.getElementById('reveal-cursor');
  let mouseX = 50, mouseY = 50, curX = 50, curY = 50;

  if (reveal && revealImg) {
    // Initialize centered
    revealImg.style.webkitMaskImage = `radial-gradient(circle at 50% 50%, black 240px, transparent 270px)`;
    revealImg.style.maskImage = `radial-gradient(circle at 50% 50%, black 240px, transparent 270px)`;

    reveal.addEventListener('mousemove', e => {
      const rect = reveal.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
      if (revealCursor) {
        revealCursor.style.left = mouseX + 'px';
        revealCursor.style.top = mouseY + 'px';
      }
    });
    reveal.addEventListener('touchmove', e => {
      const rect = reveal.getBoundingClientRect();
      const touch = e.touches[0];
      mouseX = touch.clientX - rect.left;
      mouseY = touch.clientY - rect.top;
      e.preventDefault();
    }, { passive: false });

    function animateReveal() {
      curX += (mouseX - curX) * 0.12;
      curY += (mouseY - curY) * 0.12;
      // Radius increased by 20px: was 200/220, now 220/240
      const mask = `radial-gradient(circle at ${curX}px ${curY}px, black 220px, transparent 260px)`;
      revealImg.style.webkitMaskImage = mask;
      revealImg.style.maskImage = mask;
      requestAnimationFrame(animateReveal);
    }
    animateReveal();
  }

  // ——— Image Slider (fixed images, only clip changes) ———
  const slider = document.getElementById('image-slider');
  const wrapper = document.getElementById('slider-wrapper');
  const handle = document.getElementById('slider-handle');
  let isDragging = false;

  // Ensure img-top width matches slider exactly
  function fixSliderImages() {
    if (!slider) return;
    const w = slider.getBoundingClientRect().width;
    const imgTop = slider.querySelector('.img-top');
    if (imgTop) imgTop.style.width = w + 'px';
  }
  fixSliderImages();
  window.addEventListener('resize', fixSliderImages);

  const updateSlider = (x) => {
    if (!slider) return;
    const rect = slider.getBoundingClientRect();
    let offset = x - rect.left;
    offset = Math.max(0, Math.min(offset, rect.width));
    const percent = (offset / rect.width) * 100;
    wrapper.style.width = percent + '%';
    handle.style.left = percent + '%';
  };

  if (handle) {
    handle.addEventListener('mousedown', e => { isDragging = true; e.preventDefault(); });
    window.addEventListener('mouseup', () => isDragging = false);
    window.addEventListener('mousemove', e => { if (isDragging) updateSlider(e.clientX); });
    handle.addEventListener('touchstart', e => { isDragging = true; }, { passive: true });
    window.addEventListener('touchend', () => isDragging = false);
    window.addEventListener('touchmove', e => { if (isDragging) updateSlider(e.touches[0].clientX); }, { passive: true });
    slider && slider.addEventListener('click', e => updateSlider(e.clientX));
  }

  // ——— Bubble Canvas ———
  const canvas = document.getElementById('bubbleCanvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    const bubbles = [];
    function resizeCanvas() {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    for (let i = 0; i < 18; i++) {
      bubbles.push({
        x: Math.random() * 1200,
        y: Math.random() * 220 + 20,
        r: Math.random() * 18 + 6,
        vy: -(Math.random() * 0.4 + 0.15),
        vx: (Math.random() - 0.5) * 0.3,
        opacity: Math.random() * 0.5 + 0.15,
      });
    }

    function drawBubbles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      bubbles.forEach(b => {
        ctx.beginPath();
        ctx.arc(b.x * (canvas.width / 1200), b.y, b.r, 0, Math.PI * 2);
        // Neon white glow
        ctx.shadowBlur = 18;
        ctx.shadowColor = 'rgb(0, 119, 255)';
        ctx.strokeStyle = `rgba(255,255,255,${b.opacity})`;
        ctx.lineWidth = 1.5;
        ctx.stroke();
        ctx.shadowBlur = 0;
        b.y += b.vy;
        b.x += b.vx;
        if (b.y < -b.r * 2) {
          b.y = canvas.height + b.r;
          b.x = Math.random() * 1200;
        }
      });
      requestAnimationFrame(drawBubbles);
    }
    drawBubbles();
  }

  // ——— Horizontal Scroll Features ———
const featuresWrapper = document.querySelector('.features-wrapper');
const featuresScroll = document.getElementById('features-scroll');

if (featuresWrapper && featuresScroll) {
  window.addEventListener('scroll', () => {
    const rect = featuresWrapper.getBoundingClientRect();
    const start = window.scrollY + rect.top;
    const end = start + featuresWrapper.offsetHeight - window.innerHeight;
    const scrollY = window.scrollY;
    if (scrollY >= start && scrollY <= end) {
      const progress = (scrollY - start) / (end - start);
      // largura REAL visível
      const visibleWidth = featuresWrapper.clientWidth;
      // scroll horizontal real
      const maxScroll = featuresScroll.scrollWidth - visibleWidth;
      featuresScroll.style.transform =
        `translateX(-${progress * maxScroll}px)`;
    }
  }, { passive: true });

}
  // ——— Workflow IntersectionObserver ———
  const wfDiagram = document.getElementById('workflowDiagram');
  if (wfDiagram) {
    const wfBlocks = wfDiagram.querySelectorAll('.wf-block');
    const flowPaths = wfDiagram.querySelectorAll('.flow-path');
    const flowParticles = wfDiagram.querySelectorAll('.flow-particle');

    const wfObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          wfBlocks.forEach((block, i) => {
            setTimeout(() => {
              block.classList.add('visible');
            }, i * 200);
          });
          flowPaths.forEach((path, i) => {
            setTimeout(() => {
              path.classList.add('active');
            }, 600 + i * 150);
          });
          flowParticles.forEach(p => {
            setTimeout(() => p.classList.add('active'), 900);
          });
          wfObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    wfObserver.observe(wfDiagram);
  }

  // ——— Stats counter ———
  const statValues = document.querySelectorAll('.stat-value[data-target]');
  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseFloat(el.dataset.target);
      const duration = 2000;
      const start = performance.now();
      const isLarge = target > 10000;

      function tick(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        let val = target * ease;
        if (isLarge) {
          val = Math.round(val);
          el.textContent = val >= 1000000
            ? (val / 1000000).toFixed(1) + 'M'
            : val >= 1000
              ? (val / 1000).toFixed(0) + 'k'
              : val;
        } else {
          el.textContent = Math.round(val * 10) / 10;
        }
        if (progress < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
      statsObserver.unobserve(el);
    });
  }, { threshold: 0.5 });
  statValues.forEach(el => statsObserver.observe(el));

  // ——— Generic fade-in for testimonials ———
  const fadeEls = document.querySelectorAll('.testimonial-card, .stat-item');
  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        fadeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  fadeEls.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(28px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    fadeObserver.observe(el);
  });

  // Chip cell cycling animation
  const chipCells = document.querySelectorAll('.chip-cell');
  if (chipCells.length) {
    setInterval(() => {
      chipCells.forEach(cell => {
        cell.classList.toggle('active', Math.random() > 0.5);
      });
    }, 800);
  }

  // ms counter animation
  const msCounter = document.querySelector('.wf-ms-counter');
  if (msCounter) {
    setInterval(() => {
      const val = Math.floor(Math.random() * 80 + 90);
      msCounter.textContent = `~${val}ms`;
    }, 1200);
  }
});
