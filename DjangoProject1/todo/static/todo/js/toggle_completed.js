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
});
