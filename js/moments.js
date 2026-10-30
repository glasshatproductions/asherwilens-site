/* The Moments Lamp: four matching photographs of the lamp, one visible at a
   time. The engraved icons on the lamp's base are tap targets (.ml-hot); the
   pill row (.ml-btn) carries the same choices for keyboards, screen readers
   and small screens. Unlit icons pulse until the first choice, then rest. */
(function () {
  document.querySelectorAll('.moments').forEach(function (box) {
    var frame = box.querySelector('.ml-frame');
    var imgs = Array.prototype.slice.call(box.querySelectorAll('.ml-img'));
    var btns = Array.prototype.slice.call(box.querySelectorAll('.ml-btn'));
    var hots = Array.prototype.slice.call(box.querySelectorAll('.ml-hot'));
    var copy = box.querySelector('.ml-copy');
    var modes = btns.map(function (b) { return b.getAttribute('data-mode'); });

    function show(mode) {
      var i = modes.indexOf(mode); if (i < 0) return;
      btns.forEach(function (b, k) { b.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
      hots.forEach(function (h) { h.classList.toggle('on', h.getAttribute('data-mode') === mode); });
      imgs.forEach(function (im) {
        var on = im.getAttribute('data-mode') === mode;
        im.classList.toggle('on', on);
        if (on) im.removeAttribute('aria-hidden'); else im.setAttribute('aria-hidden', 'true');
      });
      copy.textContent = btns[i].getAttribute('data-copy');
      if (frame) frame.classList.remove('ml-hint');   // the hint has done its job
    }

    hots.forEach(function (h) {
      h.addEventListener('click', function () { show(h.getAttribute('data-mode')); });
    });
    btns.forEach(function (b, i) {
      b.addEventListener('click', function () { show(modes[i]); });
      b.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var j = (i + d + btns.length) % btns.length; show(modes[j]); btns[j].focus();
      });
    });
    if (hots[0]) hots[0].classList.add('on');
  });
})();
