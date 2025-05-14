function waitForLucideAndRun(callback) {
    const check = () => {
        if (window.lucide?.createIcons) {
            callback();
        } else {
            setTimeout(check, 50);
        }
    };
    check();
}

document.addEventListener("DOMContentLoaded", function () {
    waitForLucideAndRun(() => lucide.createIcons());
});
