/* A real, interactive page inside a phone frame. The site renders at true
   phone size (390x844) and is scaled to fit, so it behaves exactly like on
   a phone. It loads when scrolled near (or on tap), never on page load. */
(function () {
  var W = 390, H = 844;
  document.querySelectorAll('.live-phone').forEach(function (ph) {
    var screen = ph.querySelector('.live-phone-screen');
    var frame = ph.querySelector('iframe');
    var start = ph.querySelector('.live-phone-start');
    var reload = ph.parentNode.querySelector('.live-phone-reload');
    var src = ph.getAttribute('data-src');
    function fit() {
      var s = screen.clientWidth / W;
      frame.style.transform = 'scale(' + s + ')';
      screen.style.height = Math.round(H * s) + 'px';
    }
    function load() {
      if (frame.getAttribute('src')) return;
      frame.setAttribute('src', src);
      ph.classList.add('loaded');
    }
    fit(); window.addEventListener('resize', fit);
    start.addEventListener('click', load);
    if (reload) reload.addEventListener('click', function () { frame.setAttribute('src', src + (src.indexOf('?') < 0 ? '?' : '&') + 'r=' + Date.now()); ph.classList.add('loaded'); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es, io) {
        es.forEach(function (e) { if (e.isIntersecting) { load(); io.disconnect(); } });
      }, { rootMargin: '200px' }).observe(ph);
    }
  });
})();

/* Keep the category line on one line: shrink a touch if it would wrap. */
(function () {
  function fit() {
    document.querySelectorAll('.cs-meta.byline').forEach(function (e) {
      e.style.fontSize = '';
      var f = parseFloat(getComputedStyle(e).fontSize);
      while (e.scrollWidth > e.clientWidth + 1 && f > 8.5) { f -= 0.25; e.style.fontSize = f + 'px'; }
    });
  }
  fit(); window.addEventListener('resize', fit);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
})();

/* Rotate the lines under the wordmark (pauses when the tab is hidden). */
(function () {
  document.querySelectorAll('.taglines').forEach(function (box) {
    var lines = Array.prototype.slice.call(box.querySelectorAll('.tl'));
    if (lines.length < 2) return;
    var i = 0;
    function fit() {
      box.style.fontSize = ''; box.style.width = '';
      var wrap = box.closest('.wrap'), cs = getComputedStyle(wrap);
      var avail = wrap.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      var f = parseFloat(getComputedStyle(box).fontSize), w;
      do { box.style.fontSize = f + 'px'; w = 0; lines.forEach(function (l) { w = Math.max(w, l.scrollWidth); }); f -= 0.25; } while (w > avail && f > 7.5);
      box.style.width = Math.min(w, avail) + 'px';
    }
    fit(); window.addEventListener('resize', fit);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
    setInterval(function () {
      if (document.hidden) return;
      var cur = lines[i]; i = (i + 1) % lines.length; var nxt = lines[i];
      cur.classList.remove('on'); cur.classList.add('out');
      nxt.classList.remove('out'); nxt.classList.add('on');
      setTimeout(function () { cur.classList.remove('out'); }, 650);
    }, 3800);
  });
})();

/* Trailer hero: one large play control. Plays with sound on press, then hands
   over to the native controls (progress, volume, fullscreen). */
(function () {
  document.querySelectorAll('.trailer-frame').forEach(function (fr) {
    var v = fr.querySelector('video'), b = fr.querySelector('.trailer-play');
    function fail() { fr.classList.add('failed'); fr.style.backgroundImage = 'url(' + v.getAttribute('poster') + ')'; }
    function start() {
      v.controls = true; v.muted = false; fr.classList.add('started');
      var p = v.play(); if (p && p.catch) p.catch(function () { fr.classList.remove('started'); });
    }
    b.addEventListener('click', start);
    v.addEventListener('play', function () { fr.classList.add('started'); v.controls = true; });
    v.addEventListener('error', fail, true);
    var src = v.querySelector('source'); if (src) src.addEventListener('error', fail);
    if (v.error) fail();
    v.addEventListener('loadedmetadata', function () { fr.classList.remove('failed'); fr.style.backgroundImage = ''; });
  });
})();
