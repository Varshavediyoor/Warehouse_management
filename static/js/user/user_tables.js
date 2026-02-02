document.addEventListener("DOMContentLoaded", function () {
    const table = document.getElementById("tableContent");
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const rowsPerPage = 15;
    let currentPage = 1;
  
    function displayRows(page) {
      const start = (page - 1) * rowsPerPage;
      const end = start + rowsPerPage;
  
      rows.forEach((row, index) => {
        row.style.display = index >= start && index < end ? "" : "none";
      });
    }
  
    function createButton(label, page, disabled = false, active = false) {
      const btn = document.createElement("button");
      btn.textContent = label;
      btn.classList.add("page-btn");
  
      if (active) btn.classList.add("active");
      if (disabled) btn.disabled = true;
  
      if (!disabled) {
        btn.addEventListener("click", () => {
          currentPage = page;
          displayRows(currentPage);
          setupPagination();
        });
      }
  
      return btn;
    }
  
    function createEllipsis() {
      const span = document.createElement("span");
      span.textContent = "...";
      span.classList.add("ellipsis");
      return span;
    }
  
    function setupPagination() {
      const paginationContainer = document.getElementById("tablePagination");
      paginationContainer.innerHTML = "";
  
      const totalPages = Math.ceil(rows.length / rowsPerPage);
  
      /* Prev */
      paginationContainer.appendChild(
        createButton("Prev", currentPage - 1, currentPage === 1)
      );
  
      /* First 3 pages */
      for (let i = 1; i <= Math.min(3, totalPages); i++) {
        paginationContainer.appendChild(
          createButton(i, i, false, i === currentPage)
        );
      }
  
      /* Left Ellipsis */
      if (currentPage > 5) {
        paginationContainer.appendChild(createEllipsis());
      }
  
      /* Middle Pages */
      const middleStart = Math.max(4, currentPage - 1);
      const middleEnd = Math.min(totalPages - 3, currentPage + 1);
  
      for (let i = middleStart; i <= middleEnd; i++) {
        if (i > 3 && i <= totalPages - 3) {
          paginationContainer.appendChild(
            createButton(i, i, false, i === currentPage)
          );
        }
      }
  
      /* Right Ellipsis */
      if (currentPage < totalPages - 4) {
        paginationContainer.appendChild(createEllipsis());
      }
  
      /* Last 3 pages */
      for (let i = Math.max(totalPages - 2, 4); i <= totalPages; i++) {
        paginationContainer.appendChild(
          createButton(i, i, false, i === currentPage)
        );
      }
  
      /* Next */
      paginationContainer.appendChild(
        createButton("Next", currentPage + 1, currentPage === totalPages)
      );
    }
  
    displayRows(currentPage);
    setupPagination();
  });
  