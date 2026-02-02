document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll(".form-error-message");

    messages.forEach((message) => {
        setTimeout(() => {
            message.classList.add("fade-out");
        }, 3000); // Fade out after 3 seconds

        message.addEventListener("animationend", (e) => {
            if (e.animationName === "fadeOut") {
                message.remove(); // Remove element after fade-out
            }
        });
    });
});
