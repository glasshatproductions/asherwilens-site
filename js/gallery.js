/* Case-study galleries: one lead image per section, the rest as thumbnails, all open in a viewer. */
(function () {
  var main = document.querySelector('main');
  if (!main || !document.querySelector('.cs-section')) return;

  function figuresIn(container, excludeBeats) {
    return Array.prototype.filter.call(container.querySelectorAll('figure'), function (f) {
      if (!f.querySelector('img') || f.classList.contains('film')) return false;
      if (excludeBeats && f.closest('.beat')) return false;
      return true;
    });
  }

  var groups = [];
  document.querySelectorAll('.beat').forEach(function (b) { groups.push(figuresIn(b, false)); });
  document.querySelectorAll('.cs-section').forEach(function (s) { groups.push(figuresIn(s, true)); });

  // Viewer
  var lb = document.createElement('div');
  lb.className = 'lb'; lb.hidden = true;
  lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Image viewer');
  lb.innerHTML = '<button class="lb-close" aria-label="Close">&times;</button>' +
    '<button class="lb-prev" aria-label="Previous image">&#8249;</button>' +
    '<figure class="lb-fig"><img alt=""><figcaption></figcaption><p class="lb-count"></p></figure>' +
    '<button class="lb-next" aria-label="Next image">&#8250;</button>';
  document.body.appendChild(lb);
  var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('figcaption'), lbCount = lb.querySelector('.lb-count');
  var cur = null, idx = 0, opener = null;

  function show() {
    var f = cur[idx], im = f.querySelector('img'), cap = f.querySelector('figcaption');
    lbImg.src = im.currentSrc || im.src; lbImg.alt = im.alt;
    lbCap.textContent = cap ? cap.textContent : '';
    lbCount.textContent = cur.length > 1 ? (idx + 1) + ' / ' + cur.length : '';
    lb.querySelector('.lb-prev').hidden = lb.querySelector('.lb-next').hidden = cur.length < 2;
  }
  function open(group, i, from) {
    cur = group; idx = i; opener = from; show();
    lb.hidden = false; document.body.style.overflow = 'hidden';
    lb.querySelector('.lb-close').focus();
  }
  function close() {
    lb.hidden = true; document.body.style.overflow = '';
    if (opener) opener.focus();
  }
  function step(d) { idx = (idx + d + cur.length) % cur.length; show(); }
  lb.querySelector('.lb-close').onclick = close;
  lb.querySelector('.lb-prev').onclick = function () { step(-1); };
  lb.querySelector('.lb-next').onclick = function () { step(1); };
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowRight') step(1);
    else if (e.key === 'ArrowLeft') step(-1);
  });

  function makeOpenable(fig, group, i) {
    var im = fig.querySelector('img');
    var btn = document.createElement('button');
    btn.className = 'zoom';
    btn.setAttribute('aria-label', 'View larger: ' + (im.alt || 'image'));
    im.parentNode.insertBefore(btn, im); btn.appendChild(im);
    btn.addEventListener('click', function () { open(group, i, btn); });
  }

  groups.forEach(function (figs) {
    if (!figs.length) return;
    if (figs.length === 2 && !figs[0].parentNode.classList.contains('pair')) {
      var pair = document.createElement('div'); pair.className = 'pair';
      figs[0].parentNode.insertBefore(pair, figs[0]);
      pair.appendChild(figs[0]); pair.appendChild(figs[1]);
    }
    if (figs.length >= 3) {
      var lead = figs[0];
      lead.classList.add('lead');
      // a lead sitting in a two/three-up row moves out so it can stand alone
      var lp = lead.parentNode;
      if (lp.classList.contains('pair') || lp.classList.contains('trio')) lp.parentNode.insertBefore(lead, lp);
      var anchor = figs[1];
      // insert the strip where the first supporting image sat (at its top-level block)
      var block = anchor;
      function isTop(n) { return n.classList.contains('wrap') || n.classList.contains('beat') || n.classList.contains('stack'); }
      while (block.parentNode && !isTop(block.parentNode)) block = block.parentNode;
      var strip = document.createElement('div'); strip.className = 'thumbs';
      block.parentNode.insertBefore(strip, block);
      figs.slice(1).forEach(function (f) { f.classList.add('thumb'); strip.appendChild(f); });
      if (figs.slice(1).every(function (f) { return f.classList.contains('tall'); })) strip.classList.add('tall');
      var n = figs.length - 1, cols = n <= 5 ? n : (n % 3 === 0 ? 3 : 4);
      strip.style.setProperty('--cols', cols);
      // tidy now-empty wrappers
      main.querySelectorAll('.pair, .trio, .narrow, .stack').forEach(function (w) {
        if (!w.children.length) w.remove();
      });
    }
    figs.forEach(function (f, i) { makeOpenable(f, figs, i); });
  });

  // social reels: autoplay muted; click opens the clip full screen with sound
  document.querySelectorAll('.reel-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var v = btn.querySelector('video');
      if (v.requestFullscreen) { v.muted = false; v.controls = true; v.currentTime = 0; v.play(); v.requestFullscreen(); }
    });
    document.addEventListener('fullscreenchange', function () {
      var v = btn.querySelector('video');
      if (!document.fullscreenElement) { v.muted = true; v.controls = false; v.play(); }
    });
  });
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('.reel-btn video').forEach(function (v) { v.removeAttribute('autoplay'); v.pause(); });
  }

  // case-study hero opens too
  var hero = document.querySelector('.cs-hero img');
  if (hero) {
    var hf = document.createElement('figure'); hero.parentNode.insertBefore(hf, hero); hf.appendChild(hero);
    makeOpenable(hf, [hf], 0);
  }
})();
