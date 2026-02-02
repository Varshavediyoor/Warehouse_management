document.addEventListener('DOMContentLoaded', () => {
    const fields = ['category', 'supplier', 'size', 'color', 'batch_number'];
    const skuInput = document.getElementById('id_sku');
    const warning = document.getElementById('sku-warning');

    if (!skuInput) return;

    async function checkSKU() {
        const params = fields.map(f => {
            const el = document.getElementById('id_' + f);
            return el ? `${f}=${encodeURIComponent(el.value.trim())}` : `${f}=`;
        }).join('&');

        try {
            // Generate SKU
            const response = await fetch(`/generate-sku/?${params}`);
            const data = await response.json();
            skuInput.value = data.sku || '';

            // Check if SKU exists
            const checkResponse = await fetch(`/check-sku-exists/?sku=${data.sku}`);
            const checkData = await checkResponse.json();
            warning.style.display = checkData.exists ? 'block' : 'none';

        } catch (err) {
            console.error('Error generating/checking SKU:', err);
            warning.style.display = 'none';
        }
    }

    fields.forEach(f => {
        const el = document.getElementById('id_' + f);
        if (el) el.addEventListener('input', checkSKU);
    });

    checkSKU(); // Run on page load
});