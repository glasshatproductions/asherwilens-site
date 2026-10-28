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
