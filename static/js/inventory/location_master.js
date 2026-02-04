
// ================= CONFIG =================
const API = "/en/dashboard/inventory-manager/api/locations/";

// ================= CSRF FROM COOKIE =================
function getCSRFToken() {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let c of cookies) {
      c = c.trim();
      if (c.startsWith("csrftoken=")) {
        cookieValue = c.substring("csrftoken=".length);
        break;
      }
    }
  }
  return cookieValue;
}

// ================= DOM HELPER =================
function el(id) {
  return document.getElementById(id);
}

// ================= API POST =================
async function apiPost(data) {
  try {
    const res = await fetch(API, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      },
      body: JSON.stringify(data)
    });

    if (!res.ok) {
      const t = await res.text();
      console.error("POST FAILED:", res.status, t);
      alert("Server error while saving.");
      return;
    }

    await res.json().catch(() => ({}));
    loadData();

  } catch (err) {
    console.error("POST ERROR:", err);
    alert("Network error.");
  }
}

// ================= LOAD DATA =================
async function loadData() {
  try {
    const res = await fetch(API);
    if (!res.ok) {
      console.error("LOAD FAILED:", res.status);
      return;
    }

    const d = await res.json();

    // ---------- SAFE SELECT FILL ----------
    fillSelect("rack_zone", d.zones, "name");
    fillSelect("shelf_rack", d.racks, "number");
    fillSelect("bin_shelf", d.shelves, "level");

    // ---------- TABLE ----------
    const table = el("locationTable");
    table.innerHTML = "";

    if (!d.bins || d.bins.length === 0) {
      table.innerHTML = `
        <tr>
          <td colspan="7" class="center">No locations found</td>
        </tr>`;
      return;
    }

    d.bins.forEach(b => {
      const shelf = d.shelves.find(x => x.id == b.shelf);
      const rack  = d.racks.find(x => x.id == b.rack);
      const zone  = d.zones.find(x => x.id == b.zone);

      table.innerHTML += `
        <tr>
          <td>${zone ? zone.name : ""}</td>
          <td>${rack ? rack.number : ""}</td>
          <td>${shelf ? shelf.level : ""}</td>
          <td>${b.bin_number}</td>
          <td>${b.capacity}</td>
          <td>
            ${b.barcode_image
              ? `<img src="${b.barcode_image}" width="100">`
              : "—"}
          </td>
          <td class="center">
          <div class="action-buttons">
          <button class="action-btn delete" onclick="deleteItem('bin', ${b.id})">
          Delete
        </button>
        
          </div>
          </td>
        </tr>`;
    });

  } catch (err) {
    console.error("LOAD ERROR:", err);
  }
}

// ================= SELECT BUILDER =================
function fillSelect(id, data, labelField) {
  const select = el(id);
  if (!select) return;

  select.innerHTML = "";

  if (!data || data.length === 0) {
    select.innerHTML = `<option value="">No data</option>`;
    return;
  }

  data.forEach(item => {
    select.innerHTML += `
      <option value="${item.id}">
        ${item[labelField]}
      </option>`;
  });
}

// ================= ADD FUNCTIONS =================
function addZone() {
  const name = el("zone_name").value.trim();
  if (!name) return alert("Enter zone name");

  apiPost({ action: "add_zone", name });
  el("zone_name").value = "";
}

function addRack() {
  const zone = el("rack_zone").value;
  const number = el("rack_number").value.trim();

  if (!number) return alert("Enter rack number");

  apiPost({
    action: "add_rack",
    zone,
    number
  });

  el("rack_number").value = "";
}

function addShelf() {
  const rack = el("shelf_rack").value;
  const level = el("shelf_level").value.trim();

  if (!level) return alert("Enter shelf level");

  apiPost({
    action: "add_shelf",
    rack,
    level
  });

  el("shelf_level").value = "";
}

function addBin() {
  const shelf = el("bin_shelf").value;
  const bin_number = el("bin_number").value.trim();
  const capacity = el("bin_capacity").value || 0;

  if (!bin_number) return alert("Enter bin number");

  apiPost({
    action: "add_bin",
    shelf,
    bin_number,
    capacity
  });

  el("bin_number").value = "";
}

// ================= DELETE =================
function deleteItem(type, id) {
  if (!confirm("Delete this item permanently?")) return;

  apiPost({
    action: "delete_" + type,
    id
  });
}

// ================= INIT =================
document.addEventListener("DOMContentLoaded", loadData);


// ================= DELETE MODAL STATE =================
let deleteTarget = {
  type: null,
  id: null
};

const deleteModal = document.getElementById("deleteModal");
const confirmDelete = document.getElementById("confirmDelete");
const cancelDelete = document.getElementById("cancelDelete");
const deleteModalText = document.getElementById("deleteModalText");

// ================= OPEN DELETE MODAL =================
function deleteItem(type, id) {
  deleteTarget.type = type;
  deleteTarget.id = id;

  // Optional dynamic message
  if (deleteModalText) {
    deleteModalText.innerText =
      "Are you sure you want to delete this " + type + "?";
  }

  deleteModal.classList.remove("fade-out");
  deleteModal.classList.add("show");
}

// ================= CLOSE MODAL =================
function closeDeleteModal() {
  deleteModal.classList.add("fade-out");
  deleteModal.classList.remove("show");

  setTimeout(() => {
    deleteModal.classList.remove("fade-out");
  }, 300);
}

cancelDelete.addEventListener("click", closeDeleteModal);

// ================= CONFIRM DELETE =================
confirmDelete.addEventListener("click", () => {

  if (!deleteTarget.id) return;

  apiPost({
    action: "delete_" + deleteTarget.type,
    id: deleteTarget.id
  });

  closeDeleteModal();

  deleteTarget.type = null;
  deleteTarget.id = null;
});

// ================= CLICK OUTSIDE CLOSE =================
window.addEventListener("click", (e) => {
  if (e.target === deleteModal) {
    closeDeleteModal();
  }
});

