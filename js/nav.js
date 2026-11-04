/* Header: scrolls away as you read down, slides back in when you scroll up.
   Always shown near the top of the page and when the menu has focus. */
(function () {
  var header = document.querySelector('.site-header');
  if (!header) return;
  var root = document.documentElement, lastY = window.scrollY, ticking = false;
  var DELTA = 6;                         // ignore tiny jitters
  function update() {
    ticking = false;
    var y = window.scrollY, h = header.offsetHeight;
    if (y <= h) root.classList.remove('nav-hidden');
    else if (y > lastY + DELTA) root.classList.add('nav-hidden');
    else if (y < lastY - DELTA) root.classList.remove('nav-hidden');
    else return;
    lastY = y;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  header.addEventListener('focusin', function () { root.classList.remove('nav-hidden'); });
})();
