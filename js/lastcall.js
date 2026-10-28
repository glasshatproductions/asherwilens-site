/* The Last Call Department.
   The approved payphone photo is the interface. A transparent button sits over
   the photographed PICK UP THE PHONE key.

   Demo mode (now): picking up opens a small panel of sample calls.
   One sample at a time, play/pause, never autoplays, keyboard accessible,
   HANG UP returns to the photograph.

   Live mode (later): if the page sets data-live-endpoint AND a script defines
   window.LastCallLive = { start(box, ui), stop() }, picking up hands the call to
   it instead. `ui` gives it the panel's status line and the empty .lc-live slot
   for mute / end-call controls, so the visual design doesn't change. The live
   script must request the microphone only after this click, get a short-lived
   session from the endpoint, and never ship an API key to the browser. */
(function () {
  document.querySelectorAll('.lastcall-art.is-interactive').forEach(function (box) {
    var hot = box.querySelector('.lc-hot');
    var overlay = box.querySelector('.lc-overlay');
    var status = box.querySelector('.lc-status');
    var hangup = box.querySelector('.lc-hangup');
    var liveSlot = box.querySelector('.lc-live');
    var buttons = Array.prototype.slice.call(box.querySelectorAll('.lc-sample'));
    var endpoint = box.getAttribute('data-live-endpoint');
    var audio = new Audio(); audio.preload = 'none';
    var current = null, liveOn = false;

    function setState(btn, playing) { btn.setAttribute('aria-pressed', playing ? 'true' : 'false'); btn.classList.toggle('playing', playing); }
    function stopAudio() { audio.pause(); if (current) setState(current, false); current = null; }
    function play(btn) {
      if (current === btn && !audio.paused) { audio.pause(); setState(btn, false); status.textContent = 'Paused.'; return; }
      if (current === btn && audio.paused && audio.currentTime > 0) { audio.play(); setState(btn, true); status.textContent = 'Playing: ' + btn.textContent + '.'; return; }
      stopAudio(); current = btn; audio.src = btn.getAttribute('data-src'); setState(btn, true);
      status.textContent = 'Connecting…';
      audio.play().then(function () { status.textContent = 'Playing: ' + btn.textContent + '.'; })
        .catch(function () { setState(btn, false); status.textContent = 'This sample could not be played.'; });
    }
    audio.addEventListener('ended', function () { if (current) setState(current, false); current = null; status.textContent = 'Call ended. Choose another case, or hang up.'; });
    audio.addEventListener('error', function () { if (!current) return; setState(current, false); current.disabled = true; current = null; status.textContent = 'This sample isn’t available right now.'; });

    function open() {
      overlay.hidden = false; box.classList.add('off-hook'); hot.setAttribute('aria-expanded', 'true');
      if (endpoint && window.LastCallLive && typeof window.LastCallLive.start === 'function') {
        liveOn = true; liveSlot.hidden = false;
        box.querySelector('.lc-samples').hidden = true;
        window.LastCallLive.start(box, { status: status, slot: liveSlot, endpoint: endpoint });
      } else {
        status.textContent = '';
      }
      (buttons[0] || hangup).focus();
    }
    function close() {
      stopAudio();
      if (liveOn && window.LastCallLive && window.LastCallLive.stop) window.LastCallLive.stop();
      liveOn = false; overlay.hidden = true; box.classList.remove('off-hook'); hot.setAttribute('aria-expanded', 'false');
      hot.focus();
    }
    hot.addEventListener('click', open);
    hangup.addEventListener('click', close);
    buttons.forEach(function (b) { b.addEventListener('click', function () { play(b); }); });
    box.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !overlay.hidden) { e.preventDefault(); close(); } });
  });
})();

/* Digital billboard: four headlines on a proposed schedule. The headline layer
   lives in the photo's own pixel space (1672x941) and is scaled to fit, so the
   perspective warp stays locked to the board at any screen size. Each headline
   is sized to fit inside the board's face. Opens on the slot matching the
   visitor's clock (before the first slot: the first). */
(function () {
  document.querySelectorAll('.billboard').forEach(function (bb) {
    var art = bb.querySelector('.bb-art'), stage = bb.querySelector('.bb-stage');
    var tabs = Array.prototype.slice.call(bb.querySelectorAll('.bb-time'));
    var heads = Array.prototype.slice.call(bb.querySelectorAll('.bb-head'));
    var box = bb.querySelector('.bb-heads');
    function scale() { stage.style.transform = 'scale(' + (art.clientWidth / 1672) + ')'; }
    function fit(h) {           // shrink until the headline fits the face (design px, so once is enough)
      var f = 120; h.style.fontSize = f + 'px';
      while ((h.scrollHeight > box.clientHeight || h.scrollWidth > box.clientWidth) && f > 40) { f -= 2; h.style.fontSize = f + 'px'; }
    }
    function show(i) {
      tabs.forEach(function (t, k) { t.setAttribute('aria-selected', k === i ? 'true' : 'false'); t.tabIndex = k === i ? 0 : -1; });
      heads.forEach(function (h, k) { h.classList.toggle('on', k === i); });
    }
    function mins(label) {
      var m = label.match(/(\d+):(\d+)\s*(AM|PM)/i); if (!m) return 0;
      var v = ((+m[1]) % 12 + (/pm/i.test(m[3]) ? 12 : 0)) * 60 + (+m[2]);
      return v < 12 * 60 ? v + 24 * 60 : v;
    }
    var d = new Date(), n = d.getHours() * 60 + d.getMinutes(); if (n < 12 * 60) n += 24 * 60;
    var start = 0; tabs.forEach(function (t, k) { if (mins(t.textContent) <= n) start = k; });
    scale(); window.addEventListener('resize', scale);
    function fitAll() { heads.forEach(fit); }
    fitAll(); if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitAll);
    show(start);
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { show(k); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { var j = (k + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length; show(j); tabs[j].focus(); e.preventDefault(); }
      });
    });
  });
})();
