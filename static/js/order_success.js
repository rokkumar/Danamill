// ========================================
// ORDER SUCCESS PAGE - CONFETTI ANIMATION
// ========================================
// Khushi Pal

(function() {
    const canvas = document.getElementById('confetti-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    let width = window.innerWidth;
    let height = window.innerHeight;
    let particles = [];
    const colors = ['#22c55e', '#2563eb', '#facc15', '#ef4444', '#a855f7'];

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    }
    
    window.addEventListener('resize', resize);
    resize();

    function randomRange(min, max) {
        return Math.random() * (max - min) + min;
    }

    function createParticle(x, y) {
        return {
            x: x,
            y: y,
            size: randomRange(5, 12),
            speedX: randomRange(-3, 3),
            speedY: randomRange(-8, -2),
            color: colors[Math.floor(Math.random() * colors.length)],
            rotation: randomRange(0, 360),
            rotSpeed: randomRange(-5, 5),
            gravity: 0.2,
            life: 1,
            fade: 0.02
        };
    }

    function updateParticles() {
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            p.x += p.speedX;
            p.y += p.speedY;
            p.speedY += p.gravity;
            p.rotation += p.rotSpeed;
            p.life -= p.fade;
            if (p.y > height || p.life <= 0) {
                particles.splice(i, 1);
                i--;
            }
        }
    }

    function drawParticles() {
        ctx.clearRect(0, 0, width, height);
        for (const p of particles) {
            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rotation * Math.PI / 180);
            ctx.globalAlpha = p.life;
            ctx.fillStyle = p.color;
            ctx.fillRect(-p.size/2, -p.size/2, p.size, p.size);
            ctx.restore();
        }
        requestAnimationFrame(drawParticles);
        updateParticles();
    }

    function burstConfetti() {
        const centerX = width / 2;
        const centerY = height * 0.3;
        for (let i = 0; i < 120; i++) {
            particles.push(createParticle(centerX + randomRange(-80, 80), centerY + randomRange(-20, 20)));
        }
    }

    drawParticles();
    burstConfetti();
    setTimeout(() => burstConfetti(), 500);
})();