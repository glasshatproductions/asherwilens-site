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
