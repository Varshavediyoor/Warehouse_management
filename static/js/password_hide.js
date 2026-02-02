document.addEventListener("DOMContentLoaded", function () {
    const toggleIcons = document.querySelectorAll(".toggle-password");

    toggleIcons.forEach(icon => {
        icon.addEventListener("click", function () {
            const input = this.closest(".password-wrapper").querySelector("input");

            if (input.type === "password") {
                input.type = "text";
                this.classList.remove("bi-eye-slash-fill");
                this.classList.add("bi-eye-fill");
            } else {
                input.type = "password";
                this.classList.remove("bi-eye-fill");
                this.classList.add("bi-eye-slash-fill");
            }
        });
    });
});
