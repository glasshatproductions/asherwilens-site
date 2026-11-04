/* Scroll story: one pinned image that evolves as the visitor scrolls.
   Markup: [data-sq] > .sq-track > .sq-sticky > (.sq-media > .sq-frame > .sq-f*) + .lab-text
   Scroll position sets each frame's opacity; nothing moves, scales or plays on
   its own. Frames hold, then dissolve, and scrolling back reverses it.
   Reduced motion, no JS or a very short window leave the static sequence. */
(function () {
  var mq = window.matchMedia ? matchMedia('(prefers-reduced-motion: reduce)') : null;
  if (mq && mq.matches) return;

  var header = document.querySelector('.site-header');

  function ease(t) { return t * t * (3 - 2 * t); }

  // Phones: while any story is pinned, the site header slides away so the
  // image owns the whole screen; it returns as soon as the story releases.
  var pinned = [];
  function setPinned(root, on) {
    var i = pinned.indexOf(root);
    if (on && i < 0) pinned.push(root); else if (!on && i >= 0) pinned.splice(i, 1);
    document.documentElement.classList.toggle('sq-full', pinned.length > 0);
  }

  document.querySelectorAll('[data-sq]').forEach(function (root) {
    var track = root.querySelector('.sq-track');
    var sticky = root.querySelector('.sq-sticky');
    var media = root.querySelector('.sq-media');
    var text = root.querySelector('.lab-text');
    var frames = Array.prototype.slice.call(root.querySelectorAll('.sq-f'));
    var readout = root.querySelector('.sq-readout');
    var step = readout && readout.querySelector('.sq-step');
    var cap = readout && readout.querySelector('.sq-cap');
    var mobileOut = root.querySelector('.sq-mobile-readout');
    var caps = readout ? readout.getAttribute('data-caps').split('|') : [];
    var cards = readout && readout.getAttribute('data-cards') ? readout.getAttribute('data-cards').split(',') : [];
    var n = frames.length;
    if (n < 2 || !track) return;

    // each dissolve's share of the scroll; longer stories get shorter dissolves, holds stay
    var FADE = Math.min(0.16, 0.66 / (n - 1));
    var hold = (1 - (n - 1) * FADE) / n;
    var active = false, ticking = false, shown = -1;
    var mobile = false, stickTop = 0, natural = 0;

    function measure() {
      mobile = window.matchMedia('(max-width: 820px)').matches;
      if (window.innerHeight < 520) { root.classList.remove('sq-on'); return false; }
      root.classList.add('sq-on');
      stickTop = mobile ? 0 : 24;   // the header steps aside while a story is pinned
      root.style.setProperty('--sq-top', stickTop + 'px');
      natural = mobile && text ? text.getBoundingClientRect().height + parseFloat(getComputedStyle(track).rowGap || 0) : 0;
      return true;
    }

    var swapT = null;
    function label(k, instant) {
      var s = (k + 1 < 10 ? '0' : '') + (k + 1) + ' / ' + (n < 10 ? '0' : '') + n;
      var put = function () { if (step) step.textContent = s; if (cap) cap.textContent = caps[k] || ''; if (readout) { readout.classList.toggle('is-card', cards[k] === '1'); readout.style.color = cards[k] === '1' ? frames[k].style.getPropertyValue('--card-fg') : ''; readout.classList.remove('is-out'); } };
      clearTimeout(swapT);
      if (instant || !readout) { put(); return; }
      readout.classList.add('is-out');          // fade the line out, swap, fade back in
      swapT = setTimeout(put, 280);
    }

    function render() {
      ticking = false;
      if (!root.classList.contains('sq-on')) return;
      var el = mobile ? media : sticky;
      var r = track.getBoundingClientRect();
      var range = track.offsetHeight - natural - el.offsetHeight;
      var p = range > 0 ? (stickTop - (r.top + natural)) / range : 0;
      setPinned(root, p > -0.02 && p < 1);
      p = Math.max(0, Math.min(1, p));
      var current = 0;
      for (var k = 1; k < n; k++) {
        var start = k * hold + (k - 1) * FADE;
        var o = ease(Math.max(0, Math.min(1, (p - start) / FADE)));
        frames[k].style.opacity = o.toFixed(3);
        if (o >= 0.5) current = k;
      }
      if (current !== shown) { shown = current; label(current); }
    }

    function onScroll() { if (active && !ticking) { ticking = true; requestAnimationFrame(render); } }

    if (!measure()) return;
    label(0, true); shown = 0;

    // Run only while the story is near the viewport; warm the later frames first.
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        active = e.isIntersecting;
        if (!active) setPinned(root, false);
        if (active) {
          frames.forEach(function (f) {
            var img = f.querySelector('img');
            if (img && img.loading === 'lazy') { img.loading = 'eager'; if (img.decode) img.decode().catch(function () {}); }
          });
          onScroll();
        }
      });
    }, { rootMargin: '100% 0px' });
    io.observe(root);

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { measure(); onScroll(); }, { passive: true });
    if (mq && mq.addEventListener) mq.addEventListener('change', function () { location.reload(); });
    render();
  });
})();
