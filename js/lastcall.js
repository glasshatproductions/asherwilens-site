/* The Last Call Department: pick up the payphone, play a sample call.
   One sample at a time, never autoplays, keyboard accessible.
   A live AI operator can be added later through data-live-endpoint (a
   server that issues short-lived session tokens); nothing live is shown
   until that endpoint exists and is wired up. */
(function () {
  document.querySelectorAll('.lastcall').forEach(function (box) {
    var pickup = box.querySelector('.lc-pickup');
    var group = box.querySelector('.lc-samples');
    var status = box.querySelector('.lc-status');
    var buttons = Array.prototype.slice.call(box.querySelectorAll('.lc-sample'));
    var audio = new Audio();
    audio.preload = 'none';
    var current = null;

    function setState(btn, playing) {
      btn.setAttribute('aria-pressed', playing ? 'true' : 'false');
      btn.classList.toggle('playing', playing);
    }
    function stop() {
      audio.pause();
      if (current) setState(current, false);
      current = null;
    }
    function play(btn) {
      if (current === btn && !audio.paused) { audio.pause(); setState(btn, false); status.textContent = 'Paused.'; return; }
      if (current === btn && audio.paused && audio.currentTime > 0) { audio.play(); setState(btn, true); status.textContent = 'Playing: ' + btn.textContent + '.'; return; }
      stop();
      current = btn;
      audio.src = btn.getAttribute('data-src');
      setState(btn, true);
      status.textContent = 'Connecting…';
      audio.play().then(function () { status.textContent = 'Playing: ' + btn.textContent + '.'; })
        .catch(function () { setState(btn, false); status.textContent = 'This sample could not be played.'; });
    }
    audio.addEventListener('ended', function () { if (current) setState(current, false); current = null; status.textContent = 'Call ended. Pick another case.'; });
    audio.addEventListener('error', function () {
      if (!current) return;
      setState(current, false); current.disabled = true; current = null;
      status.textContent = 'This sample isn’t available right now.';
    });

    pickup.addEventListener('click', function () {
      var open = pickup.getAttribute('aria-expanded') === 'true';
      if (open) {
        stop(); group.hidden = true; pickup.setAttribute('aria-expanded', 'false');
        pickup.textContent = 'Pick up the phone'; box.classList.remove('off-hook'); status.textContent = 'Hung up.';
      } else {
        group.hidden = false; pickup.setAttribute('aria-expanded', 'true');
        pickup.textContent = 'Hang up'; box.classList.add('off-hook');
        status.textContent = 'Last Call Department. Choose a case to hear the operator.';
        if (buttons[0]) buttons[0].focus();
      }
    });
    buttons.forEach(function (b) { b.addEventListener('click', function () { play(b); }); });
    box.addEventListener('keydown', function (e) { if (e.key === 'Escape' && current) { stop(); status.textContent = 'Stopped.'; } });
  });
})();
