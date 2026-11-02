/* Scroll the real featured list without inventing cart or stock states. */
(() => {
  const track = document.querySelector('[data-landing-track]');
  if (!track) return;
  const previous = document.querySelector('[data-landing-prev]');
  const next = document.querySelector('[data-landing-next]');
  if (!previous || !next) return;
  const update = () => {
    previous.disabled = track.scrollLeft <= 2;
    next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
  };
  const scroll = direction => {
    const card = track.firstElementChild;
    const distance = card ? card.getBoundingClientRect().width + parseFloat(getComputedStyle(track).gap || 0) : track.clientWidth;
    track.scrollBy({left: direction * distance, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  };
  previous.addEventListener('click', () => scroll(-1));
  next.addEventListener('click', () => scroll(1));
  track.addEventListener('scroll', update, {passive: true});
  window.addEventListener('resize', update, {passive: true});
  update();
})();
