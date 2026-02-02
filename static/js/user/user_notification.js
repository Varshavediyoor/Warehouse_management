// Select all delete buttons
const deleteButtons = document.querySelectorAll(".delete-btn");
const popup = document.getElementById("deletePopup");
const confirmBtn = document.getElementById("confirmDelete");
const cancelBtn = document.getElementById("cancelDelete");

let targetNotification = null;

// Show popup when trash clicked
deleteButtons.forEach(btn => {
  btn.addEventListener("click", (e) => {
    targetNotification = e.currentTarget.closest(".notification-card");
    popup.style.display = "flex";
  });
});

// Confirm deletion
confirmBtn.addEventListener("click", () => {
  if(targetNotification) {
    targetNotification.remove();
  }
  popup.style.display = "none";
  targetNotification = null;
});

// Cancel deletion
cancelBtn.addEventListener("click", () => {
  popup.style.display = "none";
  targetNotification = null;
});

// Close popup on clicking outside
popup.addEventListener("click", (e) => {
  if(e.target === popup) {
    popup.style.display = "none";
    targetNotification = null;
  }
});
