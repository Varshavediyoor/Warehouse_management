document.addEventListener("DOMContentLoaded", function () {

    /* ================= MOBILE SIDEBAR ================= */
    const slideToggle = document.getElementById("slide-toggle");
    const sidebar = document.getElementById("mobileSidebar");
    const overlay = document.getElementById("sidebarOverlay");
    const closeBtn = document.getElementById("closeSidebar");

    if (slideToggle && sidebar && overlay) {
        slideToggle.addEventListener("click", () => {
            const checkbox = slideToggle.querySelector("input");

            if (checkbox.checked) {
                sidebar.classList.add("active");
                overlay.classList.add("active");
            } else {
                sidebar.classList.remove("active");
                overlay.classList.remove("active");
            }
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            sidebar.classList.remove("active");
            overlay.classList.remove("active");
            const checkbox = slideToggle?.querySelector("input");
            if (checkbox) checkbox.checked = false;
        });
    }

    if (overlay) {
        overlay.addEventListener("click", () => {
            sidebar.classList.remove("active");
            overlay.classList.remove("active");
            const checkbox = slideToggle?.querySelector("input");
            if (checkbox) checkbox.checked = false;
        });
    }

    /* ================= LANGUAGE DROPDOWN ================= */
    /* ================= LANGUAGE DROPDOWN (MOBILE ONLY) ================= */
    const mobileSidebar = document.getElementById("mobileSidebar");

    if (mobileSidebar) {
        const langLi = mobileSidebar.querySelector("#languageLi");
        const langToggle = mobileSidebar.querySelector("#languageToggle");

        if (langLi && langToggle) {
            langToggle.addEventListener("click", (e) => {
                e.preventDefault();
                e.stopPropagation(); // prevent sidebar close
                langLi.classList.toggle("active");
            });
        }
    }

});
