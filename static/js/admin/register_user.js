document.addEventListener('DOMContentLoaded', () => {
    const userTypeSelect = document.getElementById('id_role');
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    const step1 = document.getElementById('step-1');
    const step2 = document.getElementById('step-2');
    const supplierFields = document.getElementById('supplier-fields');
    const deliveryBoyFields = document.getElementById('deliveryboy-fields');
    const registerBtn = document.getElementById('register-btn');
    const formSteps = document.querySelector('.form-steps');

    // Initialize: ensure step2 hidden via class
    step1.classList.add('active');
    step1.setAttribute('aria-hidden', 'false');
    step2.classList.remove('active');
    step2.setAttribute('aria-hidden', 'true');

    // Small helper to add animation classes (doesn't change your animations)
    const addAnimation = (el, name) => {
      if (!el) return;
      el.classList.add(name);
      // remove after animation period (400ms)
      setTimeout(() => el.classList.remove(name), 420);
    };

    userTypeSelect.addEventListener('change', () => {
      const selectedType = (userTypeSelect.value || '').toLowerCase().trim();
      if (selectedType.includes('supplier') || selectedType.includes('delivery')) {
        nextBtn.style.display = 'inline-block';
        registerBtn.style.display = 'none';
      } else {
        nextBtn.style.display = 'none';
        registerBtn.style.display = 'inline-block';
      }
    });

    nextBtn.addEventListener('click', () => {
      const selectedType = (userTypeSelect.value || '').toLowerCase().trim();
      if (!selectedType) {
        alert('Please select a user type');
        return;
      }

      // animate step1 out
      addAnimation(step1, 'slide-out-left');

      // after animation swap active class — using classes prevents layout jumps
      setTimeout(() => {
        step1.classList.remove('active');
        step1.setAttribute('aria-hidden', 'true');

        step2.classList.add('active');
        step2.setAttribute('aria-hidden', 'false');

        addAnimation(step2, 'slide-in-right');

        if (selectedType.includes('supplier')) {
          supplierFields.setAttribute('aria-hidden', 'false');
          supplierFields.style.display = '';
          deliveryBoyFields.setAttribute('aria-hidden', 'true');
          deliveryBoyFields.style.display = 'none';
        } else if (selectedType.includes('delivery')) {
          deliveryBoyFields.setAttribute('aria-hidden', 'false');
          deliveryBoyFields.style.display = '';
          supplierFields.setAttribute('aria-hidden', 'true');
          supplierFields.style.display = 'none';
        }

        nextBtn.style.display = 'none';
        registerBtn.style.display = 'inline-block';
        prevBtn.style.display = 'inline-block';
      }, 320); // slightly longer than animation
    });

    prevBtn.addEventListener('click', () => {
      // animate step2 out
      addAnimation(step2, 'slide-out-right');

      setTimeout(() => {
        step2.classList.remove('active');
        step2.setAttribute('aria-hidden', 'true');

        step1.classList.add('active');
        step1.setAttribute('aria-hidden', 'false');

        addAnimation(step1, 'slide-in-left');

        // hide extra sections
        supplierFields.setAttribute('aria-hidden', 'true');
        supplierFields.style.display = 'none';
        deliveryBoyFields.setAttribute('aria-hidden', 'true');
        deliveryBoyFields.style.display = 'none';

        // button visibility
        nextBtn.style.display = 'inline-block';
        registerBtn.style.display = 'none';
        prevBtn.style.display = 'none';
      }, 420); // match CSS animation timing
    });

    // ensure initial state matches if page pre-populates value
    // (trigger change once)
    if (userTypeSelect) {
      const ev = new Event('change');
      userTypeSelect.dispatchEvent(ev);
    }
  });