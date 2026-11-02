/* Enhance native quantity fields without replacing Shopify validation or stock rules. */
(() => {
  const groups = document.querySelectorAll('[data-bento-quantity]');
  const limits = input => {
    const min = Number(input.min) || 1;
    const step = Number(input.step) || 1;
    const rawMax = Number(input.max);
    const max = input.hasAttribute('max') && Number.isFinite(rawMax) ? rawMax : Infinity;
    return {min, step, max};
  };
  groups.forEach(group => {
    const input = group.querySelector('input[name="quantity"]');
    const minus = group.querySelector('[data-quantity-minus]');
    const plus = group.querySelector('[data-quantity-plus]');
    if (!input || !minus || !plus) return;
    const refresh = () => {
      const {min, step, max} = limits(input);
      const value = Number(input.value);
      minus.disabled = !Number.isFinite(value) || value <= min;
      plus.disabled = !Number.isFinite(value) || value + step > max;
    };
    const adjust = direction => {
      const {min, step, max} = limits(input);
      let value = Number(input.value);
      if (!Number.isFinite(value) || value < min) value = min;
      value = min + Math.round((value - min) / step) * step;
      value = Math.max(min, value + direction * step);
      if (Number.isFinite(max)) value = Math.min(value, min + Math.floor((max - min) / step) * step);
      input.value = String(Math.max(min, value));
      input.dispatchEvent(new Event('input', {bubbles: true}));
      input.dispatchEvent(new Event('change', {bubbles: true}));
      refresh();
    };
    minus.addEventListener('click', () => adjust(-1));
    plus.addEventListener('click', () => adjust(1));
    input.addEventListener('input', refresh);
    input.addEventListener('change', refresh);
    group.closest('[data-product]')?.querySelector('[data-variants]')?.addEventListener('change', () => queueMicrotask(refresh));
    refresh();
  });
})();
