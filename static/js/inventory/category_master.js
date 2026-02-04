const api = "/en/dashboard/inventory-manager/api/categories/"

// ---------- CSRF ----------
function getCookie(name){
  let v=null
  document.cookie.split(";").forEach(c=>{
    if(c.trim().startsWith(name+"=")){
      v=decodeURIComponent(c.split("=")[1])
    }
  })
  return v
}
const csrftoken = getCookie("csrftoken")

// ---------- VARIANTS ----------
function addVariant(name=""){
  const div = document.createElement("div")
  div.className="variant-row"
  div.innerHTML=`
  <div class="cm-field">
    <input value="${name}">
  </div>
    <button type="button" class="remove-btn">Remove</button>
  `
  div.querySelector("button").onclick=()=>div.remove()
  document.getElementById("variants").appendChild(div)
}

document.getElementById("has_expiry").addEventListener("change",e=>{
  if(e.target.checked) ensureExpiryVariant()
})

function ensureExpiryVariant(){
  let exists=false
  document.querySelectorAll("#variants input").forEach(i=>{
    if(i.value.toLowerCase()==="expiry") exists=true
  })
  if(!exists) addVariant("Expiry")
}

// ---------- SAVE ----------
function saveCategory(){
  const id = cat_id.value
  const variants=[]

  document.querySelectorAll("#variants input").forEach(i=>{
    if(i.value.trim()) variants.push({name:i.value})
  })

  fetch(id?api+id+"/":api,{
    method:id?"PUT":"POST",
    headers:{
      "Content-Type":"application/json",
      "X-CSRFToken":csrftoken
    },
    body:JSON.stringify({
      name:name.value,
      description:desc.value,
      has_expiry:has_expiry.checked,
      variants
    })
  }).then(r=>r.json())
    .then(()=>{
      clearForm()
      loadCategories()
    })
}

// ---------- LOAD ----------
function loadCategories(){
  fetch(api)
  .then(r=>r.json())
  .then(data=>{
    let rows=""
    data.forEach(c=>{
      rows+=`
        <tr>
          <td>${c.name}</td>
          <td>${c.has_expiry?"Yes":"No"}</td>
          <td>${c.variants.map(v=>v.name).join(", ")}</td>
          <td class="center">
           <div class="action-buttons">
              <button class="action-btn normal" onclick='editCat(${c.id})'>Edit</button>
              <button class="action-btn delete" onclick="openDeleteModal(${c.id})">
              Delete
              </button>
           </div>
          </td>
        </tr>
      `
    })
    cat_table.innerHTML=rows
    noData.style.display=data.length?"none":"block"
  })
}

// ---------- EDIT ----------
function editCat(id){
  fetch(api+id+"/")
  .then(r=>r.json())
  .then(c=>{
    cat_id.value=c.id
    name.value=c.name
    desc.value=c.description
    has_expiry.checked=c.has_expiry
    variants.innerHTML=""
    c.variants.forEach(v=>addVariant(v.name))
    if(c.has_expiry) ensureExpiryVariant()
  })
}

// ---------- DELETE ----------
function deleteCat(id){
  if(!confirm("Delete this category?")) return
  fetch(api+id+"/",{method:"DELETE",headers:{"X-CSRFToken":csrftoken}})
    .then(()=>loadCategories())
}

// ---------- CLEAR ----------
function clearForm(){
  document.getElementById("cat_id").value = ""
  document.getElementById("name").value = ""
  document.getElementById("desc").value = ""
  document.getElementById("has_expiry").checked = false
  document.getElementById("variants").innerHTML = ""
}

loadCategories()



let deleteCategoryId = null

const deleteModal = document.getElementById("deleteModal")
const confirmDelete = document.getElementById("confirmDelete")
const cancelDelete = document.getElementById("cancelDelete")

// 🔥 MUST be global (used in inline onclick)
function openDeleteModal(id){
  deleteCategoryId = id
  deleteModal.classList.remove("fade-out")
  deleteModal.classList.add("show")
}

// Close modal
function closeDeleteModal(){
  deleteModal.classList.add("fade-out")
  deleteModal.classList.remove("show")

  setTimeout(() => {
    deleteModal.classList.remove("fade-out")
  }, 300)
}

cancelDelete.addEventListener("click", closeDeleteModal)

// ✅ DELETE CATEGORY PERMANENTLY
confirmDelete.addEventListener("click", () => {
  if(!deleteCategoryId) return

  fetch(api + deleteCategoryId + "/", {
    method: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken
    }
  })
  .then(() => {
    closeDeleteModal()
    loadCategories()   // ✅ correct reload
    deleteCategoryId = null
  })
})

// Close if clicked outside modal
window.addEventListener("click", (e) => {
  if (e.target === deleteModal) {
    closeDeleteModal()
  }
})


