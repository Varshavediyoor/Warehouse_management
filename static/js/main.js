function toggleLanguage() {
  const langBtn = document.getElementById("lang-btn");
  const currentLang = document.documentElement.lang; // "en" or "ar"
  const form = document.getElementById("language-form");
  const langInput = document.getElementById("language-input");

  // Determine new language
  const newLang = currentLang === "ar" ? "en" : "ar";

  // Set form value and submit
  langInput.value = newLang;
  form.submit();
}


  
  // Scroll animation
  const sections = document.querySelectorAll("section");
  window.addEventListener("scroll", () => {
    sections.forEach(sec => {
      const top = sec.getBoundingClientRect().top;
      if (top < window.innerHeight - 100) {
        sec.style.opacity = "1";
        sec.style.transform = "translateY(0)";
        sec.style.transition = "0.8s";
      }
    });
  });


  //---------------------- message pop ---------------------------
  

  document.addEventListener("DOMContentLoaded", function() {
    const popup = document.getElementById("messagePopup");
    if (popup) {
      popup.style.display = "flex"; // show popup
      setTimeout(() => { popup.style.display = "none"; }, 2000); // auto-hide after 4s
    }
  });

  function closePopup() {
    document.getElementById("messagePopup").style.display = "none";
  }


  //------------------------- admin popup -------------------------


  function openPopup() {
  document.getElementById("admin-popup").style.display = "flex";
}

function closePopup() {
  document.getElementById("admin-popup").style.display = "none";
}
document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("menu-toggle");
  const sidebar = document.getElementById("mobile-sidebar");
  const closeBtn = document.getElementById("close-sidebar");

  // Open sidebar
  menuToggle.addEventListener("click", () => {
    sidebar.classList.add("active");
  });

  // Close sidebar
  closeBtn.addEventListener("click", () => {
    sidebar.classList.remove("active");
  });

  // Close sidebar when a link is clicked
  sidebar.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      sidebar.classList.remove("active");
    });
  });
});