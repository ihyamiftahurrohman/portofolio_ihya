// Animasi Reveal saat scroll
function initReveal() {
    const reveals = document.querySelectorAll(".reveal");
    
    // Tampilkan elemen yang sudah ada di layar (viewport) saat pertama kali dimuat
    setTimeout(() => {
        reveals.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
                el.classList.add("active");
            }
        });
    }, 50);

    // Gunakan Intersection Observer untuk elemen yang muncul saat di-scroll
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("active");
                    // Hapus observer setelah animasi berjalan sekali
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: "0px 0px -50px 0px"
        });

        reveals.forEach(el => observer.observe(el));
    } else {
        // Fallback untuk browser lama
        reveals.forEach(el => el.classList.add("active"));
    }
}

// Eksekusi fungsi
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initReveal);
} else {
    initReveal();
}
