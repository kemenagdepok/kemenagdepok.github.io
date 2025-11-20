document.addEventListener("DOMContentLoaded", function() {
    // 1. Muat Header
    fetch('header.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header-placeholder').innerHTML = data;
            
            // Setelah header muncul, jalankan fungsi pendukung:
            highlightActiveMenu(); 
            initMobileMenu(); // <--- Fungsi baru untuk burger menu
        });

    // 2. Muat Footer
    fetch('footer.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('footer-placeholder').innerHTML = data;
        });
});

// Fungsi Menandai Menu Aktif
function highlightActiveMenu() {
    const currentPath = window.location.pathname.split("/").pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        // Cek apakah href link sama dengan url saat ini
        if (link.getAttribute('href') === currentPath) {
            link.style.color = '#007E33';
            link.style.fontWeight = 'bold';
        }
    });
}

// Fungsi Logika Burger Menu (Mobile)
function initMobileMenu() {
    const burger = document.querySelector('.hamburger');
    const nav = document.querySelector('.nav-links');

    if (burger && nav) {
        burger.addEventListener('click', () => {
            // Toggle class 'active' pada MENU (untuk geser)
            nav.classList.toggle('active');
            
            // Toggle class 'active' pada TOMBOL (untuk animasi jadi X)
            burger.classList.toggle('active'); 
        });
    }
}