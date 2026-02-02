document.addEventListener("DOMContentLoaded", () => {
    const resendBtn = document.querySelector(".btn-resend");
    let cooldown = 30;
    resendBtn.disabled = true;

    const timer = setInterval(() => {
        resendBtn.textContent = `Resend OTP in ${cooldown}s`;
        cooldown--;

        if (cooldown < 0) {
            clearInterval(timer);
            resendBtn.textContent = "Resend OTP";
            resendBtn.disabled = false;
        }
    }, 1000);
});
