/* Case-study galleries: one lead image per section, the rest as thumbnails, all open in a viewer. */
(function () {
  var main = document.querySelector('main');
  if (!main || !document.querySelector('.cs-section')) return;

  function figuresIn(container, excludeBeats) {
    return Array.prototype.filter.call(container.querySelectorAll('figure'), function (f) {
      if (!f.querySelector('img') || f.classList.contains('film') || f.closest('.feed')) return false;
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
    // hand-arranged layouts keep their order; images still open in the viewer
    if (figs[0].closest('.k9, .sequence, .now, .g')) { figs.forEach(function (f, i) { makeOpenable(f, figs, i); }); return; }
    if (figs.length === 2 && !figs[0].parentNode.classList.contains('pair') && !figs[0].closest('.sequence')) {
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
      // items per row; the last row stretches to fill the width
      var n = figs.length - 1;
      var cols = n <= 4 ? n : (n % 4 === 0 ? 4 : 3);
      var colsM = n <= 3 ? n : (n === 4 ? 2 : 3);
      strip.style.setProperty('--cols', cols);
      strip.style.setProperty('--cols-m', colsM);
      // tidy now-empty wrappers
      main.querySelectorAll('.pair, .trio, .narrow, .stack').forEach(function (w) {
        if (!w.children.length) w.remove();
      });
    }
    figs.forEach(function (f, i) { makeOpenable(f, figs, i); });
  });

  // social reels: autoplay muted in the grid; tap opens a player with sound
  // (works on iPhone too, unlike element fullscreen). Esc / arrows / close.
  var reels = Array.prototype.slice.call(document.querySelectorAll('.reel-btn'));
  if (reels.length) {
    var rv = document.createElement('div');
    rv.className = 'rv'; rv.hidden = true;
    rv.setAttribute('role', 'dialog'); rv.setAttribute('aria-modal', 'true'); rv.setAttribute('aria-label', 'Video player');
    rv.innerHTML = '<button class="lb-close" aria-label="Close">&times;</button>' +
      '<button class="lb-prev" aria-label="Previous video">&#8249;</button>' +
      '<figure class="rv-fig"><video controls playsinline preload="auto"></video><figcaption></figcaption></figure>' +
      '<button class="lb-next" aria-label="Next video">&#8250;</button>';
    document.body.appendChild(rv);
    var rvVid = rv.querySelector('video'), rvCap = rv.querySelector('figcaption'), rvIdx = 0, rvFrom = null;
    reels.forEach(function (btn) { btn.insertAdjacentHTML('beforeend', '<span class="reel-play" aria-hidden="true">&#9654; Sound on</span>'); });
    function rvLoad(i, play) {
      rvIdx = (i + reels.length) % reels.length;
      var src = reels[rvIdx].querySelector('source').getAttribute('src');
      var cap = reels[rvIdx].parentNode.querySelector('figcaption');
      rvVid.src = src; rvVid.poster = reels[rvIdx].querySelector('video').getAttribute('poster') || '';
      rvCap.textContent = cap ? cap.textContent : '';
      rvVid.muted = false;
      if (play) rvVid.play().catch(function () { /* controls are there to start it */ });
    }
    function rvOpen(i, from) {
      rvFrom = from; reels.forEach(function (b) { b.querySelector('video').pause(); });
      rv.hidden = false; document.body.style.overflow = 'hidden';
      rvLoad(i, true); rv.querySelector('.lb-close').focus();
    }
    function rvClose() {
      rvVid.pause(); rvVid.removeAttribute('src'); rvVid.load();
      rv.hidden = true; document.body.style.overflow = '';
      reels.forEach(function (b) { var v = b.querySelector('video'); if (v.hasAttribute('autoplay')) v.play().catch(function () {}); });
      if (rvFrom) rvFrom.focus();
    }
    reels.forEach(function (btn, i) { btn.addEventListener('click', function () { rvOpen(i, btn); }); });
    rv.querySelector('.lb-close').onclick = rvClose;
    rv.querySelector('.lb-prev').onclick = function () { rvLoad(rvIdx - 1, true); };
    rv.querySelector('.lb-next').onclick = function () { rvLoad(rvIdx + 1, true); };
    rv.querySelector('.lb-prev').hidden = rv.querySelector('.lb-next').hidden = reels.length < 2;
    rv.addEventListener('click', function (e) { if (e.target === rv) rvClose(); });
    document.addEventListener('keydown', function (e) {
      if (rv.hidden) return;
      if (e.key === 'Escape') rvClose();
      else if (e.key === 'ArrowRight') rvLoad(rvIdx + 1, true);
      else if (e.key === 'ArrowLeft') rvLoad(rvIdx - 1, true);
    });
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('.reel-btn video').forEach(function (v) { v.removeAttribute('autoplay'); v.pause(); });
  }

  document.querySelectorAll('.feed').forEach(function (fd) {
    var fs = Array.prototype.slice.call(fd.querySelectorAll('figure'));
    fs.forEach(function (f, i) { makeOpenable(f, fs, i); });
  });

  // case-study hero opens too
  var hero = document.querySelector('.cs-hero img');
  if (hero) {
    var hf = document.createElement('figure'); hero.parentNode.insertBefore(hf, hero); hf.appendChild(hero);
    makeOpenable(hf, [hf], 0);
  }
})();
