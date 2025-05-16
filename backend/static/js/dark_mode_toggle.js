document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("darkModeToggle");
    if (!toggle) return;

    // Applica classe dark-theme in tempo reale
    toggle.addEventListener("change", function () {
        document.body.classList.toggle("dark-theme", toggle.checked);
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const switchInput = document.getElementById("isCompletedSwitch");
    const hiddenInput = document.getElementById("isCompletedHidden");

    if (switchInput && hiddenInput) {
        switchInput.addEventListener("change", function () {
            if (switchInput.checked) {
                hiddenInput.value = "on";  // Django interpreta "on" come True
            } else {
                hiddenInput.removeAttribute("value"); // equivale a False per Django
            }
        });
    }
});