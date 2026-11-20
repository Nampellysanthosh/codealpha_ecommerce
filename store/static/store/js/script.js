/**
 * BAZAAR E-COMMERCE - VANILLA JAVASCRIPT INTERACTION ENGINE
 */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Navbar Toggle
  const mobileToggle = document.getElementById('mobileNavToggle');
  const navMenu = document.getElementById('navMenu');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
    });
  }

  // Auto-dismiss Alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s ease';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // Quantity Control Buttons (+ / -) in Product Details & Cart
  const qtyWrappers = document.querySelectorAll('.qty-control-group');
  qtyWrappers.forEach(group => {
    const decBtn = group.querySelector('.btn-dec');
    const incBtn = group.querySelector('.btn-inc');
    const input = group.querySelector('.qty-input');

    if (input) {
      const maxStock = parseInt(input.getAttribute('max') || '9999', 10);
      const minQty = parseInt(input.getAttribute('min') || '1', 10);

      if (decBtn) {
        decBtn.addEventListener('click', (e) => {
          e.preventDefault();
          let val = parseInt(input.value || '1', 10);
          if (val > minQty) {
            input.value = val - 1;
            input.dispatchEvent(new Event('change'));
          }
        });
      }

      if (incBtn) {
        incBtn.addEventListener('click', (e) => {
          e.preventDefault();
          let val = parseInt(input.value || '1', 10);
          if (val < maxStock) {
            input.value = val + 1;
            input.dispatchEvent(new Event('change'));
          } else {
            alert(`Maximum available stock reached (${maxStock} items).`);
          }
        });
      }

      input.addEventListener('change', () => {
        let val = parseInt(input.value, 10);
        if (isNaN(val) || val < minQty) {
          input.value = minQty;
        } else if (val > maxStock) {
          input.value = maxStock;
          alert(`Quantity adjusted to maximum available stock (${maxStock}).`);
        }
      });
    }
  });

  // Confirm Item Removal in Cart
  const removeForms = document.querySelectorAll('.remove-item-form');
  removeForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      const confirmRemove = confirm("Are you sure you want to remove this item from your cart?");
      if (!confirmRemove) {
        e.preventDefault();
      }
    });
  });
});
