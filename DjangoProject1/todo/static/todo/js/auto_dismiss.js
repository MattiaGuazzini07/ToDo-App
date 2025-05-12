document.addEventListener("DOMContentLoaded", function () {
    const alertBox = document.getElementById("alert-box");
    if (alertBox) {
        setTimeout(() => {
            alertBox.style.transition = "opacity 0.5s ease-out";
            alertBox.style.opacity = 0;
            setTimeout(() => alertBox.remove(), 500);
        }, 2000);
    }
});
