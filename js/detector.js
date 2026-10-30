/* Rarity Detector showcase (Synth City).
   Swaps curated screens inside the phone; tall screens scroll in place.
   Markup comes from detector_demo() in tools/build.py. */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FADE = 180;

  document.querySelectorAll('[data-rd]').forEach(function (demo) {
    var screen = demo.querySelector('.rd-screen');
    var shots = demo.querySelectorAll('.rd-shot');
    var tabs = Array.prototype.slice.call(demo.querySelectorAll('.rd-tab'));
    var caption = demo.querySelector('.rd-caption');
    var current = 0, timer = null;

    function show(i, focus) {
      if (i === current || !shots[i]) return;
      tabs.forEach(function (t, k) {
        var on = k === i;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
      });
      if (focus) tabs[i].focus();
      // keep the chosen pill in view on narrow screens (horizontal tab strip)
      if (tabs[i].scrollIntoView) tabs[i].scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
      caption.textContent = tabs[i].getAttribute('data-caption');
      screen.setAttribute('aria-labelledby', tabs[i].id);

      var swap = function () {
        shots[current].hidden = true;
        shots[i].hidden = false;
        current = i;
        screen.scrollTop = 0;          // each example starts at its top
        screen.classList.remove('is-swapping');
        var hint = demo.querySelector('.rd-hint');
        if (hint) hint.classList.toggle('is-quiet', screen.scrollHeight <= screen.clientHeight + 4);
      };
      clearTimeout(timer);
      if (reduce) { swap(); return; }
      screen.classList.add('is-swapping');
      timer = setTimeout(swap, FADE);
    }

    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { show(k, false); });
      t.addEventListener('keydown', function (e) {
        var n = tabs.length, to = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') to = (k + 1) % n;
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') to = (k - 1 + n) % n;
        else if (e.key === 'Home') to = 0;
        else if (e.key === 'End') to = n - 1;
        if (to !== null) { e.preventDefault(); show(to, true); }
      });
    });

    // warm the other screens once the section is near, so swaps are instant
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        if (es.some(function (e) { return e.isIntersecting; })) {
          shots.forEach(function (s) { s.loading = 'eager'; if (s.decode) s.decode().catch(function () {}); });
          io.disconnect();
        }
      }, { rootMargin: '600px 0px' });
      io.observe(demo);
    }
  });
})();
