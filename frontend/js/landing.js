document.addEventListener('DOMContentLoaded', () => {
    // --- Image Reveal (Background Removal Demo) ---
    const reveal = document.getElementById('image-reveal');
    const revealImg = reveal.querySelector('.img-reveal');

    let mouseX = 0;
    let mouseY = 0;
    let currentX = 0;
    let currentY = 0;

    reveal.addEventListener('mousemove', e => {
        const rect = reveal.getBoundingClientRect();
        mouseX = e.clientX - rect.left;
        mouseY = e.clientY - rect.top;
    });

    // Touch support for reveal
    reveal.addEventListener('touchmove', e => {
        const rect = reveal.getBoundingClientRect();
        const touch = e.touches[0];
        mouseX = touch.clientX - rect.left;
        mouseY = touch.clientY - rect.top;
        e.preventDefault();
    }, { passive: false });

    function animateReveal() {
        // Smooth interpolation (easing)
        currentX += (mouseX - currentX) * 0.15;
        currentY += (mouseY - currentY) * 0.15;

        const maskValue = `radial-gradient(circle at ${currentX}px ${currentY}px, black 40px, transparent 60px)`;
        revealImg.style.webkitMaskImage = maskValue;
        revealImg.style.maskImage = maskValue;

        requestAnimationFrame(animateReveal);
    }
    animateReveal();

    // --- Image Slider (Before/After Demo) ---
    const slider = document.getElementById('image-slider');
    const wrapper = document.getElementById('slider-wrapper');
    const handle = document.getElementById('slider-handle');

    let isDragging = false;

    const updateSlider = (x) => {
        const rect = slider.getBoundingClientRect();
        let offset = x - rect.left;
        offset = Math.max(0, Math.min(offset, rect.width));
        const percent = (offset / rect.width) * 100;

        wrapper.style.width = percent + '%';
        handle.style.left = percent + '%';
    };

    handle.addEventListener('mousedown', () => isDragging = true);
    window.addEventListener('mouseup', () => isDragging = false);

    window.addEventListener('mousemove', e => {
        if (!isDragging) return;
        updateSlider(e.clientX);
    });

    // Touch support for slider
    handle.addEventListener('touchstart', () => isDragging = true);
    window.addEventListener('touchend', () => isDragging = false);
    window.addEventListener('touchmove', e => {
        if (!isDragging) return;
        updateSlider(e.touches[0].clientX);
    });

    slider.addEventListener('click', e => {
        updateSlider(e.clientX);
    });

    // --- Sticky Horizontal Scroll for Features ---
    const featuresWrapper = document.querySelector('.features-wrapper');
    const featuresScroll = document.getElementById('features-scroll');

    window.addEventListener('scroll', () => {
        const offsetTop = featuresWrapper.offsetTop;
        const scrollY = window.scrollY;
        const wrapperHeight = featuresWrapper.offsetHeight;
        const windowHeight = window.innerHeight;

        if (scrollY >= offsetTop && scrollY <= offsetTop + wrapperHeight - windowHeight) {
            const progress = (scrollY - offsetTop) / (wrapperHeight - windowHeight);
            const scrollAmount = progress * (featuresScroll.scrollWidth - window.innerWidth * 0.8);
            featuresScroll.style.transform = `translateX(-${scrollAmount}px)`;
        }
    });

    // --- Intersection Observer for Fade-in Animations ---
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Apply initial styles and observe elements
    const animatedElements = document.querySelectorAll('.step, .testimonial-card, .stat-item');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        observer.observe(el);
    });

    // --- Smooth Navbar Background on Scroll ---
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.padding = '0.5rem 0';
            navbar.style.background = 'rgba(255, 255, 255, 0.8)';
        } else {
            navbar.style.padding = '0';
            navbar.style.background = 'rgba(255, 255, 255, 0.7)';
        }
    });
});