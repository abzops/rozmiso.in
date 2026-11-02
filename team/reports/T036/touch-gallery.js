
// Touch gallery: reuse thumbnail selection; preserve page scrolling, pinch and tap-to-zoom.
(() => {
  document.querySelectorAll('[data-product]').forEach(root => {
    const frame = root.querySelector('[data-zoom-image]');
    const slides = [...root.querySelectorAll('button[data-image]')];
    if (!frame || slides.length < 2) return;
    frame.style.touchAction = 'pan-y pinch-zoom';
    let gesture = null;
    let suppressClickUntil = 0;
    const pointers = new Set();
    frame.addEventListener('pointerdown', event => {
      if (!['touch', 'pen'].includes(event.pointerType)) return;
      pointers.add(event.pointerId);
      if (pointers.size !== 1 || event.isPrimary === false) {
        gesture = null;
        suppressClickUntil = Date.now() + 700;
        return;
      }
      suppressClickUntil = 0;
      gesture = {id:event.pointerId, x:event.clientX, y:event.clientY, moved:false};
      if (frame.setPointerCapture) frame.setPointerCapture(event.pointerId);
    });
    frame.addEventListener('pointermove', event => {
      if (!gesture || gesture.id !== event.pointerId) return;
      if (Math.hypot(event.clientX - gesture.x, event.clientY - gesture.y) > 12) gesture.moved = true;
    });
    frame.addEventListener('pointerup', event => {
      pointers.delete(event.pointerId);
      if (!gesture || gesture.id !== event.pointerId) return;
      const {x, y, moved} = gesture;
      gesture = null;
      const dx = event.clientX - x;
      const dy = event.clientY - y;
      if (moved || Math.hypot(dx, dy) > 12) suppressClickUntil = Date.now() + 700;
      const threshold = Math.min(72, Math.max(36, frame.clientWidth * .08));
      if (Math.abs(dx) < threshold || Math.abs(dx) <= Math.abs(dy) * 1.25) return;
      const selected = slides.findIndex(button => button.getAttribute('aria-pressed') === 'true');
      const index = Math.max(0, selected);
      slides[(index + (dx < 0 ? 1 : -1) + slides.length) % slides.length].click();
    });
    const cancel = event => {
      pointers.delete(event.pointerId);
      if (gesture?.id === event.pointerId) {
        gesture = null;
        suppressClickUntil = Date.now() + 700;
      }
    };
    frame.addEventListener('pointercancel', cancel);
    frame.addEventListener('lostpointercapture', cancel);
    frame.addEventListener('click', event => {
      if (Date.now() >= suppressClickUntil || event.detail === 0) return;
      event.preventDefault();
      event.stopPropagation();
    }, true);
  });
})();
