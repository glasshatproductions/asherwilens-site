/* FAGE "Buzz for the truth": the name plates on the photographed intercom are
   buttons. Tap one to hear that neighbor; tap again to stop. One at a time.
   The plates pulse softly until the first buzz. */
(function () {
  document.querySelectorAll('.bz').forEach(function (fig) {
    var art = fig.querySelector('.bz-art');
    var hots = Array.prototype.slice.call(fig.querySelectorAll('.bz-hot'));
    var status = fig.querySelector('.bz-status');
    var audio = new Audio(), current = null;
    audio.preload = 'none';

    function reset() {
      hots.forEach(function (h) { h.classList.remove('playing'); h.setAttribute('aria-pressed', 'false'); });
      current = null;
      if (status) status.textContent = '';
    }
    audio.addEventListener('ended', reset);
    audio.addEventListener('error', function () { reset(); if (status) status.textContent = 'Couldn’t play that one.'; });

    hots.forEach(function (h) {
      h.addEventListener('click', function (e) {
        e.stopPropagation();
        art.classList.add('used');
        if (current === h) { audio.pause(); reset(); return; }
        reset();
        current = h;
        h.classList.add('playing'); h.setAttribute('aria-pressed', 'true');
        if (status) status.textContent = 'Buzzing ' + h.getAttribute('data-name') + '…';
        audio.src = h.getAttribute('data-src');
        var p = audio.play();
        if (p && p.catch) p.catch(function () { reset(); });
      });
    });
  });
})();
