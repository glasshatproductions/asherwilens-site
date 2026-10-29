/* PROPOSALMATIC™: a working engagement-ring vending machine from Synth City, 2187.
   A small state machine drives the touchscreen, the dispensing mechanism and the
   receipt printer:
     WELCOME → PACKAGE → CONFIGURATION → PROCESSING → DISPENSING → RECEIPT → REVEAL
   No network calls, no storage, no personal data. Sound is synthesized locally
   with Web Audio and stays off until the visitor turns it on. */
(function () {
  'use strict';
  var root = document.getElementById('pm');
  if (!root) return;

  function $(sel, el) { return (el || root).querySelector(sel); }
  function $$(sel, el) { return Array.prototype.slice.call((el || root).querySelectorAll(sel)); }
  var motionQuery = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  function still() { return motionQuery.matches; }

  var machine = $('#pmMachine');
  var bay = $('.pm-bay');
  var sep = $('.pm-sep');
  var sepT = $('.pm-sep-t');
  var box = $('.pm-box');
  var tray = $('.pm-tray');
  var paper = $('#pmPaper');
  var receipt = $('#pmReceipt');
  var actions = $('.pm-actions');
  var statusEl = $('.pm-status');
  var live = $('#pmLive');
  var reveal = $('#pmReveal');
  var log = $('.pm-log');
  var soundBtn = $('.pm-sound');

  // ---------- Data ----------
  var PACKAGE_ROW = { 'FOREVER+': 0, 'PREMIUM': 1, 'STANDARD': 2 };  // top shelf for the top package
  var MESSAGES = ['Compatibility optimized', 'Emotional uncertainty removed', 'Originality deemed unnecessary'];
  var IDENTICAL = '8,492,611';  // a deliberately fictional Bureau claim

  var picks = { pkg: null, time: null, resp: null };
  var order = null;  // frozen at confirmation, so the receipt can never disagree with it

  // ---------- State machine ----------
  var STATES = ['WELCOME', 'PACKAGE', 'CONFIGURATION', 'PROCESSING', 'DISPENSING', 'RECEIPT', 'REVEAL'];
  var ALLOWED = {
    WELCOME: ['PACKAGE'],
    PACKAGE: ['CONFIGURATION', 'WELCOME'],
    CONFIGURATION: ['PROCESSING', 'PACKAGE'],
    PROCESSING: ['DISPENSING'],
    DISPENSING: ['RECEIPT'],
    RECEIPT: ['REVEAL', 'WELCOME'],
    REVEAL: ['WELCOME']
  };
  var state = 'WELCOME';
  var runId = 0;
  var timers = [];
  function later(fn, ms, id) {
    var t = setTimeout(function () { if (id === runId) fn(); }, ms);
    timers.push(t);
  }
  function clearTimers() { timers.forEach(clearTimeout); timers = []; }

  function go(next) {
    if ((ALLOWED[state] || []).indexOf(next) < 0) return false;
    state = next;
    root.setAttribute('data-state', next);
    showView(next);
    return true;
  }

  function showView(name) {
    $$('.pm-view').forEach(function (v) {
      var on = v.getAttribute('data-view') === name;
      v.hidden = !on;
      v.classList.remove('is-enter');
      if (on) { void v.offsetWidth; v.classList.add('is-enter'); }
    });
    var pips = $$('.pm-pips i');
    var lit = { WELCOME: 0, PACKAGE: 1, CONFIGURATION: 2, PROCESSING: 3, DISPENSING: 3, RECEIPT: 4, REVEAL: 4 }[name];
    pips.forEach(function (p, i) { p.classList.toggle('on', i < lit); });
    var view = $('.pm-view[data-view="' + name + '"]');
    var h = view && view.querySelector('h2');
    // Move focus with the screen, but only once the visitor has started (no focus grab on load).
    if (h && started) { try { h.focus({ preventScroll: true }); } catch (e) { h.focus(); } }
  }
  var started = false;

  function say(text) { live.textContent = ''; setTimeout(function () { live.textContent = text; }, 40); }

  // ---------- Sound (synthesized, cheerful, off by default) ----------
  var Sound = (function () {
    var ctx = null, out = null, on = false;
    function ensure() {
      if (!ctx) {
        var AC = window.AudioContext || window.webkitAudioContext;
        if (!AC) return null;
        ctx = new AC();
        out = ctx.createGain(); out.gain.value = 0.55;
        var comp = ctx.createDynamicsCompressor();
        out.connect(comp); comp.connect(ctx.destination);
      }
      if (ctx.state === 'suspended') ctx.resume();
      return ctx;
    }
    function tone(t, f, dur, type, vol, f2, attack) {
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.type = type || 'sine';
      o.frequency.setValueAtTime(f, t);
      if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + dur);
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(vol, t + (attack || 0.008));
      g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(g); g.connect(out); o.start(t); o.stop(t + dur + 0.05);
    }
    var noiseBuf = null;
    function noise(t, dur, vol, freq, q, kind) {
      if (!noiseBuf) {
        noiseBuf = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
        var d = noiseBuf.getChannelData(0);
        for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
      }
      var s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
      s.buffer = noiseBuf; s.loop = true;
      f.type = kind || 'bandpass'; f.frequency.value = freq; f.Q.value = q || 1;
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(vol, t + 0.005);
      g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      s.connect(f); f.connect(g); g.connect(out); s.start(t); s.stop(t + dur + 0.05);
      return g;
    }
    var fx = {
      boot: function (t) { tone(t, 330, 0.5, 'sine', 0.07, 660, 0.12); tone(t + 0.22, 880, 0.55, 'triangle', 0.05); tone(t + 0.4, 1318.5, 0.7, 'sine', 0.04); },
      select: function (t) { tone(t, 1046.5, 0.09, 'triangle', 0.07); tone(t + 0.06, 1568, 0.14, 'sine', 0.05); },
      toggle: function (t) { noise(t, 0.025, 0.12, 2600, 2); tone(t, 220, 0.05, 'square', 0.025); tone(t + 0.03, 1318.5, 0.08, 'sine', 0.035); },
      back: function (t) { tone(t, 784, 0.08, 'triangle', 0.05); tone(t + 0.05, 587, 0.1, 'sine', 0.04); },
      tick: function (t) { tone(t, 2093, 0.05, 'sine', 0.035); },
      scan: function (t) { tone(t, 1760, 0.035, 'sine', 0.02); },
      approved: function (t) { tone(t, 1318.5, 0.25, 'triangle', 0.06); tone(t + 0.12, 1975.5, 0.4, 'sine', 0.05); },
      shutter: function (t) { noise(t, 0.22, 0.08, 900, 0.7, 'lowpass'); tone(t + 0.2, 140, 0.08, 'sine', 0.06); },
      motor: function (t, dur) {
        var o = ctx.createOscillator(), f = ctx.createBiquadFilter(), g = ctx.createGain();
        o.type = 'sawtooth'; o.frequency.setValueAtTime(70, t); o.frequency.linearRampToValueAtTime(115, t + dur * 0.5); o.frequency.linearRampToValueAtTime(80, t + dur);
        f.type = 'lowpass'; f.frequency.value = 520;
        g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.05, t + 0.08); g.gain.setValueAtTime(0.05, t + dur - 0.1); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
        o.connect(f); f.connect(g); g.connect(out); o.start(t); o.stop(t + dur + 0.05);
      },
      clunk: function (t) { tone(t, 150, 0.2, 'sine', 0.18, 55); noise(t, 0.06, 0.1, 700, 0.8, 'lowpass'); },
      conveyor: function (t, dur) { noise(t, dur, 0.035, 400, 0.6, 'lowpass'); },
      print: function (t, dur) {
        // thermal printer: a fast buzzing chatter
        var g = noise(t, dur, 0.06, 3400, 1.4);
        var lfo = ctx.createOscillator(), depth = ctx.createGain();
        lfo.type = 'square'; lfo.frequency.value = 26; depth.gain.value = 0.03;
        lfo.connect(depth); depth.connect(g.gain); lfo.start(t); lfo.stop(t + dur);
      },
      chime: function (t) {
        [1046.5, 1318.5, 1568, 2093].forEach(function (f, i) { tone(t + i * 0.09, f, 0.9, 'triangle', 0.06); tone(t + i * 0.09, f / 2, 0.7, 'sine', 0.025); });
      }
    };
    return {
      get on() { return on; },
      set: function (v) { on = v; if (v) ensure(); },
      play: function (name, arg) {
        if (!on) return;
        var c = ensure(); if (!c) return;
        try { fx[name](c.currentTime + 0.01, arg); } catch (e) { /* audio is decoration */ }
      }
    };
  })();

  soundBtn.addEventListener('click', function () {
    var v = soundBtn.getAttribute('aria-pressed') !== 'true';
    soundBtn.setAttribute('aria-pressed', String(v));
    $('.pm-sound-t', soundBtn).textContent = v ? 'Sound on' : 'Sound off';
    Sound.set(v);
    if (v) Sound.play('select');
  });

  // ---------- Power on ----------
  function powerOn() {
    if (still()) { machine.setAttribute('data-power', 'on'); return; }
    machine.setAttribute('data-power', 'boot');
    setTimeout(function () { if (machine.getAttribute('data-power') === 'boot') machine.setAttribute('data-power', 'on'); }, 950);
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      if (es.some(function (e) { return e.isIntersecting; })) { io.disconnect(); setTimeout(powerOn, 350); }
    }, { threshold: 0.25 });
    io.observe(machine);
  } else { setTimeout(powerOn, 350); }

  // ---------- Selections ----------
  function syncSelections() {
    $$('.pm-pkg, .pm-seg').forEach(function (l) { l.classList.toggle('is-on', l.querySelector('input').checked); });
    $('[data-act="toConfig"]').disabled = !picks.pkg;
    var ready = !!(picks.time && picks.resp);
    $('[data-act="confirm"]').disabled = !ready;
    root.classList.toggle('cfg-ready', ready);
  }
  root.addEventListener('change', function (e) {
    var t = e.target;
    if (!t.matches('input[type="radio"]')) return;
    if (state === 'PACKAGE' && t.name === 'pmPkg') { picks.pkg = t.value; Sound.play('select'); }
    else if (state === 'CONFIGURATION' && t.name === 'pmTime') { picks.time = t.value; Sound.play('toggle'); }
    else if (state === 'CONFIGURATION' && t.name === 'pmResp') { picks.resp = t.value; Sound.play('toggle'); }
    syncSelections();
  });
  // keyboard focus ring for browsers without :has()
  root.addEventListener('focusin', function (e) {
    if (e.target.matches('.pm-pkg input, .pm-seg input')) {
      var kb = true; try { kb = e.target.matches(':focus-visible'); } catch (x) {}
      if (kb) e.target.parentNode.classList.add('is-focus');
    }
  });
  root.addEventListener('focusout', function (e) {
    if (e.target.matches('.pm-pkg input, .pm-seg input')) e.target.parentNode.classList.remove('is-focus');
  });

  // ---------- Actions ----------
  root.addEventListener('click', function (e) {
    var b = e.target.closest('[data-act]');
    if (!b || b.disabled) return;
    var act = b.getAttribute('data-act');
    if (act === 'start' && state === 'WELCOME') { started = true; Sound.play('boot'); go('PACKAGE'); }
    else if (act === 'cancel' && state === 'PACKAGE') { Sound.play('back'); go('WELCOME'); }
    else if (act === 'toConfig' && state === 'PACKAGE' && picks.pkg) { Sound.play('select'); go('CONFIGURATION'); }
    else if (act === 'back' && state === 'CONFIGURATION') { Sound.play('back'); go('PACKAGE'); }
    else if (act === 'confirm' && state === 'CONFIGURATION') confirmOrder();
    else if (act === 'viewReceipt') showReceipt();
    else if (act === 'restart') restart();
    else if (act === 'save') saveImage();
    else if (act === 'copy') copyReceipt();
    else if (act === 'share') shareReceipt();
  });

  function confirmOrder() {
    if (!(picks.pkg && picks.time && picks.resp)) return;
    var row = PACKAGE_ROW[picks.pkg];
    var col = Math.floor(Math.random() * 4);
    var now = new Date();
    var no = 'PM-2187-' + String(Math.floor(10000 + Math.random() * 90000)) + '-' + 'ABCDEFGHJKLMNPRSTUVWXYZ'.charAt(Math.floor(Math.random() * 23));
    order = Object.freeze({
      pkg: picks.pkg, time: picks.time, resp: picks.resp,
      row: row, col: col, cell: String((row + 1) * 100 + col + 1),
      no: no,
      issued: ('0' + now.getHours()).slice(-2) + ':' + ('0' + now.getMinutes()).slice(-2) + ' · Cycle 2187',
      bars: barsFor(no)
    });
    $$('fieldset', $('.pm-views')).forEach(function (f) { f.disabled = true; });
    fillReceipt();
    Sound.play('select');
    if (go('PROCESSING')) runProcessing(runId);
  }

  // ---------- Processing ----------
  function cells() { return $$('.pm-cell'); }
  function cellAt(r, c) { return $('.pm-cell[data-row="' + r + '"][data-col="' + c + '"]'); }

  function runProcessing(id) {
    log.innerHTML = '';
    root.classList.remove('is-analyzing'); void root.offsetWidth; root.classList.add('is-analyzing');
    say('Analyzing commitment.');
    var quick = still();
    if (!quick) root.classList.add('is-scanning');
    // the machine scans its shelves, then settles on "your" ring
    var hops = quick ? 0 : 9, all = cells(), prev = null;
    for (var i = 0; i < hops; i++) {
      (function (i) {
        later(function () {
          if (prev) prev.classList.remove('is-scan');
          prev = all[Math.floor(Math.random() * all.length)];
          prev.classList.add('is-scan');
          Sound.play('scan');
        }, 200 + i * 230, id);
      })(i);
    }
    var step = quick ? 450 : 620, t0 = quick ? 300 : 900;
    MESSAGES.forEach(function (m, i) {
      later(function () { addLog(m); Sound.play('tick'); }, t0 + i * step, id);
    });
    later(function () {
      if (prev) prev.classList.remove('is-scan');
      root.classList.remove('is-scanning');
      var pick = cellAt(order.row, order.col);
      pick.classList.add('is-pick');
      addLog('Proposal approved', true);
      Sound.play('approved');
    }, t0 + MESSAGES.length * step, id);
    later(function () {
      if (go('DISPENSING')) runDispense(id);
    }, t0 + MESSAGES.length * step + (quick ? 600 : 900), id);
  }
  function addLog(text, final) {
    var li = document.createElement('li');
    li.textContent = text;
    if (final) li.className = 'is-final';
    log.appendChild(li);
    say(text + '.');
  }

  // ---------- Dispensing: retrieval behind the shutter, drop into the bay ----------
  // Three beats the visitor can read on the screen and see in the machine:
  // SELECTED (the compartment goes dark and shutters while the ring is retrieved
  // internally), DISPENSED (the presentation box drops into the collection bay),
  // REPLACED (the shutter lifts on an identical ring).
  function seq(key, mode) {
    var li = $('.pm-seq li[data-k="' + key + '"]');
    if (!li) return;
    li.classList.remove('is-active', 'is-done');
    if (mode) li.classList.add(mode);
  }
  // the strip under the glass reads out what the machine is doing while the UI is away
  function sepText(t) {
    if (t) { sepT.textContent = t; sep.classList.add('is-live'); }
    else { sepT.textContent = sepT.getAttribute('data-default'); sep.classList.remove('is-live'); }
  }
  function shutterText(cell, t) { var n = cell.querySelector('.pm-sh-t'); if (n) n.textContent = t; }
  function work(cell, ms) {
    cell.style.setProperty('--pm-work', ms + 'ms');
    cell.classList.remove('is-working'); void cell.offsetWidth; cell.classList.add('is-working');
  }

  function runDispense(id) {
    var pick = cellAt(order.row, order.col);
    var quick = still();
    say('Selected: compartment ' + order.cell + '. Retrieving.');
    // keep the collection bay in view (short screens, phones)
    var tb = tray.getBoundingClientRect();
    if (tb.bottom > window.innerHeight - 8) window.scrollBy({ top: tb.bottom - window.innerHeight + 28, behavior: quick ? 'auto' : 'smooth' });
    seq('sel', 'is-done'); seq('disp', 'is-active');
    shutterText(pick, 'Retrieving');
    sepText('Retrieving \u00b7 Compartment ' + order.cell);

    var bw = box.offsetWidth, bh = box.offsetHeight, tw = tray.clientWidth, th = tray.clientHeight;
    var xRest = (tw - bw) / 2, yFloor = th - bh - (th > 90 ? 12 : 9), yTop = -bh - 6;
    function T(x, y) { return 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)'; }

    if (quick || !box.animate) {
      pick.classList.remove('is-pick');
      pick.classList.add('is-dark', 'is-shut');
      box.style.transform = T(xRest, yFloor);
      box.classList.add('is-in');
      landed(id, pick);
      return;
    }
    var RETRIEVE = 1100;
    // 1. the compartment light goes out, then the shutter closes over it
    later(function () { pick.classList.remove('is-pick'); pick.classList.add('is-dark'); }, 120, id);
    later(function () {
      pick.classList.add('is-shut');
      Sound.play('shutter');
      work(pick, RETRIEVE - 150);
      root.classList.add('is-moving');
      Sound.play('motor', (RETRIEVE - 200) / 1000);
    }, 380, id);
    // 2. the box drops from inside the machine into the collection bay
    later(function () {
      box.classList.add('is-in');
      var dur = 900;
      var anim = box.animate([
        { transform: T(xRest, yTop), offset: 0, easing: 'cubic-bezier(.55,0,1,.45)' },   // falls
        { transform: T(xRest, yFloor), offset: 0.48, easing: 'cubic-bezier(.2,.6,.4,1)' },  // lands
        { transform: T(xRest, yFloor - 5), offset: 0.62, easing: 'cubic-bezier(.5,0,.75,0)' }, // small bounce
        { transform: T(xRest, yFloor), offset: 0.76, easing: 'ease-out' },
        { transform: T(xRest, yFloor - 1), offset: 0.86, easing: 'ease-in' },
        { transform: T(xRest, yFloor), offset: 1 }
      ], { duration: dur, fill: 'forwards' });
      later(function () { Sound.play('clunk'); }, dur * 0.48, id);
      later(function () { root.classList.add('is-tray-open'); }, dur * 0.7, id);
      anim.onfinish = function () {
        if (id !== runId) return;
        root.classList.remove('is-moving');
        box.style.transform = T(xRest, yFloor);
        try { anim.cancel(); } catch (e) {}
        landed(id, pick);
      };
    }, 380 + RETRIEVE, id);
  }
  function landed(id, pick) {
    var quick = still();
    root.classList.add('is-tray-lit', 'is-tray-open');
    Sound.play('chime');
    seq('disp', 'is-done'); seq('rep', 'is-active');
    say('Dispensed. Your ring is in the collection bay.');
    sepText('Dispensed \u00b7 Please collect your ring');
    // 3. the compartment is restocked with an identical ring, in plain view
    later(function () {
      shutterText(pick, 'Restocking');
      sepText('Restocking \u00b7 Compartment ' + order.cell);
      work(pick, 800);
      Sound.play('tick');
    }, quick ? 100 : 450, id);
    later(function () {
      pick.classList.remove('is-shut', 'is-working', 'is-dark');
      pick.classList.add('is-restocked', 'is-flash');
      Sound.play('shutter');
      seq('rep', 'is-done');
      say('Replaced. Compartment ' + order.cell + ' holds an identical ring.');
      sepText('Compartment ' + order.cell + ' \u00b7 Identical replacement loaded');
    }, quick ? 300 : 1350, id);
    later(function () { pick.classList.remove('is-flash'); }, quick ? 400 : 2550, id);
    later(function () { sepText(''); if (go('RECEIPT')) runReceipt(id); }, quick ? 700 : 2450, id);
  }

  // ---------- Receipt ----------
  function fillReceipt() {
    $$('[data-f="cell"]').forEach(function (n) { n.textContent = order.cell; });
    $$('[data-f="no"]').forEach(function (n) { n.textContent = order.no; });
    $$('[data-f="issued"]').forEach(function (n) { n.textContent = order.issued; });
    $$('[data-f="pkg"]').forEach(function (n) { n.textContent = order.pkg; });
    $$('[data-f="resp"]').forEach(function (n) { n.textContent = order.resp; });
    $$('[data-f="time"]').forEach(function (n) { n.textContent = order.time; });
    var svg = $('[data-f="bars"]'), x = 0, html = '';
    order.bars.forEach(function (w, i) { if (i % 2 === 0) html += '<rect x="' + x + '" y="0" width="' + w + '" height="34"/>'; x += w; });
    svg.setAttribute('viewBox', '0 0 ' + x + ' 34');
    svg.innerHTML = html;
  }
  function barsFor(seed) {
    var h = 2166136261;
    for (var i = 0; i < seed.length; i++) { h ^= seed.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
    var bars = [];
    for (var j = 0; j < 58; j++) { h ^= h << 13; h >>>= 0; h ^= h >>> 17; h ^= h << 5; h >>>= 0; bars.push(1 + (h % 3)); }
    return bars;
  }

  function runReceipt(id) {
    var full = receipt.offsetHeight;
    if (still()) {
      paper.style.height = full + 'px';
      printed(id);
      return;
    }
    root.classList.add('is-printing');
    Sound.play('print', 2.3);
    void paper.offsetHeight;
    paper.style.height = full + 'px';
    later(function () {
      var r = paper.getBoundingClientRect();
      if (r.top + Math.min(full, 420) > window.innerHeight) {
        window.scrollBy({ top: Math.min(r.top + full + 120 - window.innerHeight, r.top - 90), behavior: 'smooth' });
      }
    }, 250, id);
    later(function () { printed(id); }, 2350, id);
  }
  function printed(id) {
    root.classList.remove('is-printing');
    root.classList.add('has-receipt', 'has-actions');
    actions.hidden = false;
    prepareImage();
    say('Proposal complete. Your receipt has printed below the machine.');
    later(function () { if (go('REVEAL')) runReveal(); }, still() ? 1800 : 3200, id);
  }
  function showReceipt() {
    if (!order) return;
    paper.scrollIntoView({ behavior: still() ? 'auto' : 'smooth', block: 'center' });
    try { receipt.focus({ preventScroll: true }); } catch (e) { receipt.focus(); }
  }

  // ---------- Campaign reveal ----------
  function runReveal() {
    machine.setAttribute('data-power', 'standby');
    root.classList.remove('is-tray-lit');
    reveal.hidden = false;
    root.classList.add('is-revealed');
    say('Everything can be manufactured. Except rarity. Premier Gem.');
    if (window.matchMedia && window.matchMedia('(max-width: 980px)').matches) {
      setTimeout(function () {
        var r = reveal.getBoundingClientRect();
        if (r.top > window.innerHeight - 140) window.scrollBy({ top: r.top - window.innerHeight * 0.35, behavior: still() ? 'auto' : 'smooth' });
      }, 900);
    }
  }

  // ---------- Restart ----------
  function restart() {
    runId++;
    clearTimers();
    if (box.getAnimations) box.getAnimations().forEach(function (a) { a.cancel(); });
    if (box.classList.contains('is-in')) {
      box.classList.add('is-collected');
      setTimeout(function () { box.classList.remove('is-in', 'is-collected'); box.style.transform = ''; }, 420);
    }
    root.classList.remove('is-moving', 'is-tray-lit', 'is-tray-open', 'is-printing', 'has-receipt', 'has-actions', 'is-revealed', 'is-analyzing', 'is-scanning', 'cfg-ready');
    cells().forEach(function (c) { c.classList.remove('is-scan', 'is-pick', 'is-shut', 'is-dark', 'is-working', 'is-restocked', 'is-flash'); shutterText(c, 'Retrieving'); });
    $$('.pm-seq li').forEach(function (li) { li.classList.remove('is-active', 'is-done'); });
    sepText('');
    paper.style.height = '0px';
    actions.hidden = true;
    reveal.hidden = true;
    statusEl.textContent = '';
    log.innerHTML = '';
    $$('input[type="radio"]').forEach(function (i) { i.checked = false; });
    $$('fieldset', $('.pm-views')).forEach(function (f) { f.disabled = false; });
    picks = { pkg: null, time: null, resp: null };
    order = null; imageBlob = null; imagePromise = null;
    syncSelections();
    machine.setAttribute('data-power', 'on');
    state = 'WELCOME';
    root.setAttribute('data-state', 'WELCOME');
    showView('WELCOME');
    Sound.play('boot');
    var r = machine.getBoundingClientRect();
    if (r.top < 0 || r.top > window.innerHeight * 0.5) machine.scrollIntoView({ behavior: still() ? 'auto' : 'smooth', block: 'start' });
  }

  // ---------- Share: text, image, native share ----------
  function receiptText() {
    return [
      'SYNTHETIC BUREAU',
      'PROPOSALMATIC™ · CYCLE 2187',
      'ORDER ' + order.no,
      '',
      'PROPOSAL COMPLETE',
      'PACKAGE: ' + order.pkg,
      'EMOTIONAL RESPONSE: ' + order.resp,
      'DEPLOYMENT: ' + order.time,
      'LOVE: APPROVED',
      'COMPATIBILITY: OPTIMIZED',
      'ORIGINALITY: 0%',
      '',
      'CONGRATULATIONS.',
      'YOUR RING IS IDENTICAL TO ' + IDENTICAL + ' OTHERS.',
      'THE RING OF YOUR DREAMS. AND EVERYONE ELSE’S.',
      '',
      'Thank you for choosing efficiency.',
      '',
      '(A fictional receipt from Synth City, 2187. A campaign for Premier Gem.)'
    ].join('\n');
  }
  function pageUrl() { return /^https?:/.test(location.protocol) ? location.href.split('#')[0] : ''; }
  function fileName() { return 'proposalmatic-receipt-' + order.no.toLowerCase() + '.png'; }
  function setStatus(t) { statusEl.textContent = ''; setTimeout(function () { statusEl.textContent = t; }, 30); }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return legacyCopy(text); });
    }
    return Promise.resolve(legacyCopy(text));
  }
  function legacyCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.top = '-1000px'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    var ok = false; try { ok = document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    return ok;
  }
  function copyReceipt() {
    if (!order) return;
    var url = pageUrl();
    copyText(receiptText() + (url ? '\n' + url : '')).then(function (ok) {
      setStatus(ok ? 'Receipt text copied.' : 'Copy isn’t available here. Select the receipt text to copy it.');
      if (ok) Sound.play('tick');
    });
  }

  var imageBlob = null, imagePromise = null;
  function prepareImage() {
    if (imagePromise) return imagePromise;
    var forOrder = order;
    imagePromise = renderImage().then(function (canvas) {
      return new Promise(function (resolve) {
        if (canvas.toBlob) canvas.toBlob(function (b) { resolve(b); }, 'image/png');
        else resolve(dataUrlToBlob(canvas.toDataURL('image/png')));
      });
    }).then(function (b) { if (order === forOrder) imageBlob = b; return b; });
    return imagePromise;
  }
  function dataUrlToBlob(u) {
    var parts = u.split(','), bin = atob(parts[1]), arr = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
    return new Blob([arr], { type: 'image/png' });
  }
  function saveImage() {
    if (!order) return;
    prepareImage().then(function (blob) {
      if (!blob) throw new Error('no image');
      var url = URL.createObjectURL(blob), a = document.createElement('a');
      a.href = url; a.download = fileName(); a.rel = 'noopener';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
      setStatus('Receipt saved as a PNG.');
      Sound.play('tick');
    }).catch(function () { setStatus('The image couldn’t be made in this browser. Copy the text instead.'); });
  }
  function shareReceipt() {
    if (!order) return;
    var text = receiptText(), url = pageUrl();
    var data = { title: 'PROPOSALMATIC™ receipt', text: text };
    if (imageBlob && window.File && navigator.canShare) {
      try {
        var file = new File([imageBlob], fileName(), { type: 'image/png' });
        if (navigator.canShare({ files: [file] })) { data.files = [file]; }
      } catch (e) {}
    }
    if (!data.files && url) data.url = url;
    if (navigator.share) {
      navigator.share(data).then(function () { setStatus('Shared.'); }, function (err) {
        if (err && err.name === 'AbortError') return;
        fallbackShare(text, url);
      });
      return;
    }
    fallbackShare(text, url);
  }
  function fallbackShare(text, url) {
    copyText(text + (url ? '\n' + url : '')).then(function (ok) {
      setStatus(ok ? 'Sharing isn’t available in this browser, so the receipt text was copied. Save the PNG to post the image.'
                   : 'Sharing isn’t available in this browser. Save the PNG to post it.');
    });
  }

  // Draw the receipt into a canvas from the same frozen order data (no screenshots, no libraries).
  function renderImage() {
    var fontsReady = (document.fonts && document.fonts.load) ? Promise.all([
      document.fonts.load('40px "Bebas Neue"'), document.fonts.load('16px "Marcellus"'), document.fonts.load('600 12px "Hanken Grotesk"')
    ]).catch(function () {}) : Promise.resolve();
    return fontsReady.then(function () { return drawReceipt(order); });
  }
  function drawReceipt(o) {
    var S = 2, W = 600, PW = 380, PX = (W - PW) / 2, IN = 28, CW = PW - IN * 2;
    var MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace';
    var BEBAS = '"Bebas Neue", "Marcellus", Georgia, serif';
    var c = document.createElement('canvas'), x = c.getContext('2d');
    var ops = [];
    function center(text, font, lh, color, track) { ops.push({ k: 'c', t: text, f: font, lh: lh, col: color, tr: track || 0 }); }
    function kv(a, b) { ops.push({ k: 'kv', a: a, b: b }); }
    function rule() { ops.push({ k: 'rule' }); }
    function gap(h) { ops.push({ k: 'gap', h: h }); }
    var F = '500 13px ' + MONO, FB = '700 13px ' + MONO;
    center('SYNTHETIC BUREAU', FB, 20, '#1c1c1c', 2);
    center('PROPOSALMATIC™', '34px ' + BEBAS, 36, '#1c1c1c', 2);
    center('CYCLE 2187', F, 20);
    rule();
    kv('ORDER', o.no); kv('ISSUED', o.issued.toUpperCase()); kv('UNIT / COMPARTMENT', 'PM-07 / ' + o.cell);
    rule();
    center('PROPOSAL COMPLETE', FB, 26, '#1c1c1c', 2);
    kv('PACKAGE:', o.pkg); kv('EMOTIONAL RESPONSE:', o.resp); kv('DEPLOYMENT:', o.time);
    kv('LOVE:', 'APPROVED'); kv('COMPATIBILITY:', 'OPTIMIZED'); kv('ORIGINALITY:', '0%');
    rule();
    // punchline hierarchy: the identical count leads, the tagline supports
    center('CONGRATULATIONS.', '26px ' + BEBAS, 32, '#111', 3);
    gap(4);
    center('YOUR RING IS IDENTICAL TO', '34px ' + BEBAS, 34, '#111', 1);
    center(IDENTICAL, '92px ' + BEBAS, 88, '#111', 1);
    center('OTHERS.', '34px ' + BEBAS, 36, '#111', 1);
    gap(10);
    center('THE RING OF YOUR DREAMS. AND EVERYONE ELSE\u2019S.', '21px ' + BEBAS, 24, '#4a4842', 1.5);
    rule();
    center('THANK YOU FOR CHOOSING EFFICIENCY.', F, 20);
    ops.push({ k: 'bars' });
    center('FICTIONAL RECEIPT · NO PURCHASE MADE', '500 9.5px ' + MONO, 16, '#6a675f');

    // measure: wrap centered lines, decide kv layout
    function wrap(text, font, max, track) {
      x.font = font;
      if ('letterSpacing' in x) x.letterSpacing = (track || 0) + 'px';
      var words = text.split(' '), lines = [], line = '';
      words.forEach(function (w) {
        var test = line ? line + ' ' + w : w;
        if (x.measureText(test).width > max && line) { lines.push(line); line = w; } else line = test;
      });
      if (line) lines.push(line);
      return lines;
    }
    var H = 34;
    ops.forEach(function (op) {
      if (op.k === 'c') { op.lines = wrap(op.t, op.f, CW, op.tr); H += op.lines.length * op.lh; }
      else if (op.k === 'kv') {
        x.font = F; if ('letterSpacing' in x) x.letterSpacing = '0px';
        var wa = x.measureText(op.a).width; x.font = FB; var wb = x.measureText(op.b).width;
        op.split = wa + wb + 14 > CW; H += op.split ? 40 : 21;
      }
      else if (op.k === 'rule') H += 22;
      else if (op.k === 'gap') H += op.h;
      else if (op.k === 'bars') H += 64;
    });
    H += 34;
    var TOP = 64, CAP = 88, CH = TOP + H + CAP;
    c.width = W * S; c.height = CH * S;
    x.scale(S, S);
    // backdrop: the Synth City night
    var bg = x.createLinearGradient(0, 0, 0, CH);
    bg.addColorStop(0, '#15120e'); bg.addColorStop(1, '#060505');
    x.fillStyle = bg; x.fillRect(0, 0, W, CH);
    var glow = x.createRadialGradient(W / 2, TOP, 10, W / 2, TOP, W * 0.8);
    glow.addColorStop(0, 'rgba(255,214,160,.16)'); glow.addColorStop(1, 'rgba(255,214,160,0)');
    x.fillStyle = glow; x.fillRect(0, 0, W, CH);
    // printer slot
    x.fillStyle = '#000'; x.fillRect(PX - 24, TOP - 8, PW + 48, 8);
    x.fillStyle = 'rgba(255,255,255,.12)'; x.fillRect(PX - 24, TOP, PW + 48, 1);
    // paper with torn bottom
    x.save();
    x.shadowColor = 'rgba(0,0,0,.55)'; x.shadowBlur = 24; x.shadowOffsetY = 10;
    x.beginPath(); x.moveTo(PX, TOP); x.lineTo(PX + PW, TOP); x.lineTo(PX + PW, TOP + H - 8);
    for (var zx = PX + PW, up = true; zx > PX; zx -= 6, up = !up) x.lineTo(Math.max(PX, zx - 6), TOP + H - (up ? 0 : 8));
    x.closePath(); x.fillStyle = '#f3f1ea'; x.fill();
    x.restore();
    // content
    var y = TOP + 34;
    x.textBaseline = 'alphabetic';
    ops.forEach(function (op) {
      if (op.k === 'c') {
        x.font = op.f; x.fillStyle = op.col || '#1c1c1c'; x.textAlign = 'center';
        if ('letterSpacing' in x) x.letterSpacing = op.tr + 'px';
        op.lines.forEach(function (l) { x.fillText(l, W / 2 + op.tr / 2, y + op.lh * 0.72); y += op.lh; });
        if ('letterSpacing' in x) x.letterSpacing = '0px';
      } else if (op.k === 'kv') {
        x.fillStyle = '#1c1c1c';
        x.font = F; x.textAlign = 'left'; x.fillText(op.a, PX + IN, y + 15);
        x.font = FB; x.textAlign = 'right';
        if (op.split) { x.fillText(op.b, PX + PW - IN, y + 34); y += 40; } else { x.fillText(op.b, PX + PW - IN, y + 15); y += 21; }
      } else if (op.k === 'rule') {
        x.strokeStyle = '#8f8c84'; x.setLineDash([4, 3]); x.lineWidth = 1;
        x.beginPath(); x.moveTo(PX + IN, y + 11.5); x.lineTo(PX + PW - IN, y + 11.5); x.stroke(); x.setLineDash([]);
        y += 22;
      } else if (op.k === 'gap') y += op.h;
      else if (op.k === 'bars') {
        var total = o.bars.reduce(function (s, v) { return s + v; }, 0), unit = CW / total, bx = PX + IN;
        x.fillStyle = '#1c1c1c';
        o.bars.forEach(function (w, i) { if (i % 2 === 0) x.fillRect(bx, y + 12, w * unit, 40); bx += w * unit; });
        y += 64;
      }
    });
    // caption
    x.textAlign = 'center'; x.fillStyle = '#d8cfbf';
    x.font = '15px "Marcellus", Georgia, serif';
    if ('letterSpacing' in x) x.letterSpacing = '5px';
    x.fillText('SYNTH CITY · 2187', W / 2 + 2.5, TOP + H + 46);
    x.fillStyle = '#7d8590'; x.font = '600 10px "Hanken Grotesk", Helvetica, Arial, sans-serif';
    if ('letterSpacing' in x) x.letterSpacing = '2.5px';
    x.fillText('A FICTIONAL CAMPAIGN EXPERIENCE FOR PREMIER GEM', W / 2 + 1.25, TOP + H + 66);
    return c;
  }

  // start clean (e.g. after a back/forward cache restore)
  syncSelections();
  window.addEventListener('pageshow', function (e) { if (e.persisted && state !== 'WELCOME') restart(); });

  // test hook for automated checks (read-only)
  root.pmState = function () { return { state: state, order: order, states: STATES }; };
})();
