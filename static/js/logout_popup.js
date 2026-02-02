document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logoutBtn");
    const modal = document.getElementById("logoutModal");
    const confirmLogout = document.getElementById("confirmLogout");
    const cancelLogout = document.getElementById("cancelLogout");
  
    // Show modal
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      modal.classList.remove("fade-out");
      modal.classList.add("show");
    });
  
    // Fade out animation before hiding
    function closeModal() {
      modal.classList.add("fade-out");
      modal.classList.remove("show");
  
      // remove fade-out class after animation completes for reset
      setTimeout(() => {
        modal.classList.remove("fade-out");
      }, 300);
    }
  
    cancelLogout.addEventListener("click", closeModal);
  
    confirmLogout.addEventListener("click", () => {
      window.location.href = "{% url 'admin_logout' %}";
    });
  
    // Close if clicked outside modal content
    window.addEventListener("click", (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });
  });
  