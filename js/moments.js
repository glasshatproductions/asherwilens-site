/* The Moments Lamp: four matching photographs in one frame, one visible at a
   time. Buttons switch the light with a short crossfade (none with reduced
   motion). Arrow keys move between lights. */
(function () {
  document.querySelectorAll('.moments').forEach(function (box) {
    var imgs = Array.prototype.slice.call(box.querySelectorAll('.ml-img'));
    var btns = Array.prototype.slice.call(box.querySelectorAll('.ml-btn'));
    var copy = box.querySelector('.ml-copy');
    function show(i) {
      var mode = btns[i].getAttribute('data-mode');
      btns.forEach(function (b, k) { b.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
      imgs.forEach(function (im) {
        var on = im.getAttribute('data-mode') === mode;
        im.classList.toggle('on', on);
        if (on) im.removeAttribute('aria-hidden'); else im.setAttribute('aria-hidden', 'true');
      });
      copy.textContent = btns[i].getAttribute('data-copy');
    }
    btns.forEach(function (b, i) {
      b.addEventListener('click', function () { show(i); });
      b.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var j = (i + d + btns.length) % btns.length; show(j); btns[j].focus();
      });
    });
  });
})();
