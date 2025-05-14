function toggleDropdownMenu() {
    const menu = document.querySelector(".dropdown-menu");
    if (menu) {
        menu.classList.toggle("open");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.querySelector(".dropdown-toggle");
    const menu = document.querySelector(".dropdown-menu");

    // Nascondi all'avvio
    menu?.classList.remove("open");

    // Attiva/disattiva al click sull'avatar
    toggle?.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleDropdownMenu();
    });

    // Chiudi cliccando fuori
    document.addEventListener("click", function (e) {
        if (!menu?.contains(e.target) && !toggle?.contains(e.target)) {
            menu?.classList.remove("open");
        }
    });

    // Sezione attività completate
    const toggleButton = document.querySelector(".collapsible-toggle");
    const content = document.getElementById("completed-content");
    const icon = toggleButton?.querySelector(".toggle-icon");

    if (toggleButton && content) {
        toggleButton.addEventListener("click", function () {
            content.classList.toggle("open");
            toggleButton.classList.toggle("rotated");

            if (icon) {
                const isOpen = content.classList.contains("open");
                icon.setAttribute("data-lucide", isOpen ? "chevron-up" : "chevron-down");
                lucide.createIcons(); // Rende effettiva l'icona aggiornata
            }
        });
    }
});
