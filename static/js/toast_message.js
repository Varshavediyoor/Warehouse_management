document.addEventListener("DOMContentLoaded", function () {
    const overlay = document.getElementById("toast-overlay");
    const toasts = document.querySelectorAll(".toast-message");

    if (!overlay) return;

    // Show overlay instantly
    overlay.classList.add("show");

    // Show toasts instantly
    toasts.forEach((toast) => {
        toast.style.opacity = "1";
    });

    const fadeOutDuration = 2000; // 1 second

    // Fade out everything after 1 second
    setTimeout(() => {
        // Fade out all toasts immediately
        toasts.forEach((toast) => {
            toast.classList.add("fade-out");
            setTimeout(() => {
                toast.remove();
            }, fadeOutDuration);
        });

        // Fade out overlay
        overlay.classList.add("fade-out");
        setTimeout(() => {
            overlay.remove();
        }, fadeOutDuration);

    }, fadeOutDuration); // start disappearing after 1s
});
