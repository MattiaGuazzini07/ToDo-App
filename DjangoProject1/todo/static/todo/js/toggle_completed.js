function toggleCompleted() {
    const content = document.getElementById("completed-content");
    if (content) {
        content.classList.toggle("open");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("completed-content")?.classList.remove("open");
});
