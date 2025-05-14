document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("darkModeToggle");
    if (!toggle) return;

    // Applica classe dark-theme in tempo reale
    toggle.addEventListener("change", function () {
        document.body.classList.toggle("dark-theme", toggle.checked);
    });
});
