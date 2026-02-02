function openDeletePopup(id) {
    const popup = document.getElementById("deletePopup");
    const deleteForm = document.getElementById("deleteForm");

    let baseUrl = document.getElementById("deleteBaseUrl").value;
    baseUrl = baseUrl.replace("/0/", `/${id}/`);

    deleteForm.action = baseUrl;

    popup.style.display = "flex";
}

function closeDeletePopup() {
    document.getElementById("deletePopup").style.display = "none";
}
function openDeletePopup(id) {
    const popup = document.getElementById("deletePopup");
    const deleteForm = document.getElementById("deleteForm");

    // 🔗 Update delete form action
    let baseUrl = document.getElementById("deleteBaseUrl").value;
    baseUrl = baseUrl.replace("/0/", `/${id}/`);
    deleteForm.action = baseUrl;

    // 🎬 Show with fade animation
    popup.classList.remove("fade-out");
    popup.classList.add("show");
}

function closeDeletePopup() {
    const popup = document.getElementById("deletePopup");

    // 🎬 Add fade-out animation
    popup.classList.add("fade-out");

    // ⏳ Wait for fade animation to end, then fully hide
    setTimeout(() => {
        popup.classList.remove("show", "fade-out");
    }, 300); // must match fadeOut duration
}
