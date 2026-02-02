let idx = 0;

function addItem() {
    idx++;

    const row = `
      <tr id="row_${idx}">
          <td>
              <select name="product_${idx}" class="form-control" required>
                  <option value="">Select product</option>
                  ${productOptions}
              </select>
          </td>

          <td>
              <input name="ordered_qty_${idx}" type="number" step="0.01" class="form-control" required>
          </td>

          <td>
              <input name="batch_${idx}" type="text" class="form-control">
          </td>

          <td>
              <button type="button" class="btn-back remove-btn" onclick="removeRow(${idx})">Remove</button>
          </td>
      </tr>
    `;

    document.getElementById("items-body").insertAdjacentHTML('beforeend', row);
}

function removeRow(i) {
    const r = document.getElementById("row_" + i);
    if (r) r.remove();
}
