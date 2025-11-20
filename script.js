document.addEventListener("DOMContentLoaded", function() {
    // Muat Header
    fetch('header.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header-placeholder').innerHTML = data;
            highlightActiveMenu();
        });

    // Muat Footer
    fetch('footer.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('footer-placeholder').innerHTML = data;
        });
});

// Fungsi untuk menandai menu yang sedang aktif
function highlightActiveMenu() {
    const currentPath = window.location.pathname.split("/").pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = '#007E33';
            link.style.fontWeight = 'bold';
        }
    });
}