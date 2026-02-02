document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.querySelector(".sidebar");
  const burgerCheck = document.getElementById("burger-check");
  const header = document.querySelector(".dashboard-header");
  const footer = document.querySelector(".user-dashboard-footer");

  burgerCheck.addEventListener("change", () => {
    const collapsed = burgerCheck.checked;

    // Apply smooth animation
    if (header) header.style.transition = "margin-left 0.4s ease";
    if (footer) footer.style.transition = "margin-left 0.4s ease";

    // Toggle collapse class on elements
    sidebar.classList.toggle("collapsed", collapsed);
    if (footer) footer.classList.toggle("collapsed", collapsed);
    if (header) header.classList.toggle("collapsed", collapsed);
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const langBtns = document.querySelectorAll(".lang-btn");

  langBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      langBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      // Here you can trigger language change logic if needed
    });
  });
});

