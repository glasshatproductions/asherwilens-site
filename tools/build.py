import pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent
EMAIL = 'ashwilens@gmail.com'

import hashlib as _h, os as _o
def _v(path):
    try: return _h.md5(open(_o.path.join(_o.path.dirname(__file__),'..',path),'rb').read()).hexdigest()[:8]
    except Exception: return '1'
ASSET_V=True

# PROPOSALMATIC launch switch. False = the page is live at /proposalmatic.html but
# unlisted: no card on Synth City and search engines are asked not to index it.
# Set to True and rebuild to launch it publicly.
PM_LISTED = False

LASTCALL_TAG = ''
MOMENTS_TAG = ''
DETECTOR_TAG = ''
BUZZ_TAG = ''
# Small rotating lines under the wordmark. Edit, add or remove freely.
TAGLINES = [
    'Ideas, made.',
]
TAGLINES_HTML = ('<p class="taglines" aria-label="' + ' / '.join(TAGLINES) + '">'
                 + ''.join(f'<span class="tl{" on" if i == 0 else ""}" aria-hidden="true">{t}</span>' for i, t in enumerate(TAGLINES)) + '</p>')

# Absolute base for social previews (crawlers ignore relative image paths).
# Change this one line if the site moves to its own domain.
SITE_URL = 'https://asherwilens.com/'

def page(fname, title, desc, body, current='', og='thumb-synth-city', head_extra='', scripts_extra=''):
    def nav(href, label, key):
        cur = ' aria-current="page"' if key == current else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE_URL}{'' if fname == 'index.html' else fname}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Asher Wilens">
<meta property="og:url" content="{SITE_URL}{'' if fname == 'index.html' else fname}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE_URL}images/{og}.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE_URL}images/{og}.jpg">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="author" content="Asher Wilens">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Hanken+Grotesk:wght@400;500;600&display=swap">
<link rel="stylesheet" href="css/style.css?v={_v('css/style.css')}">{head_extra}
</head>
<body class="pg-{fname[:-5]}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="wrap">
<div class="brandline"><a class="wordmark" href="index.html">A. WILENS</a>{TAGLINES_HTML}</div>
<nav class="site-nav" aria-label="Main">
{nav("index.html#work","Work","work")}
{nav("lab.html","Inventions","lab")}
{nav("index.html#about","About","about")}
<a href="resume.pdf" target="_blank" rel="noopener">Résumé</a>
<a href="mailto:{EMAIL}">Contact</a>
</nav>
</div>
</header>
<main id="main">
{body}
</main>
<section class="contact-band" aria-label="Contact">
<div class="wrap">
<div><h2>Some ideas need a headline. Others need a patent.</h2></div>
<a class="btn" href="mailto:{EMAIL}">Get in touch</a>
</div>
</section>
<footer class="site-footer">
<div class="wrap">
<span>© 2026 Asher Wilens. <em class="mom">My mom says I&#39;m creative.</em></span>
<span><a href="index.html#work">Work</a> · <a href="lab.html">Inventions</a> · <a href="index.html#about">About</a> · <a href="resume.pdf" target="_blank" rel="noopener">Résumé</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div>
</footer>
<script src="js/gallery.js?v={_v('js/gallery.js')}"></script>
<script src="js/livephone.js?v={_v('js/livephone.js')}" defer></script>
<script src="js/nav.js?v={_v('js/nav.js')}" defer></script>{LASTCALL_TAG if fname == 'uber.html' else ''}{MOMENTS_TAG if fname == 'brown-co.html' else ''}{DETECTOR_TAG if fname == 'synth-city.html' else ''}{BUZZ_TAG if fname == 'fage.html' else ''}{scripts_extra}
</body>
</html>
'''
    (OUT / fname).write_text(html)

TALL = {'det-dollar','det-mouse','det-earbuds','synth-transmission-live'}
def img(src, alt, cap=''):
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    FIT = {'synth-warning','synth-site'}
    k = ' class="tall"' if src in TALL else (' class="fit"' if src in FIT else '')
    return f'<figure{k}><img src="images/{src}.jpg" alt="{alt}" loading="lazy">{c}</figure>'

def section(num, label, intro, content):
    n = f'<span class="num">{num}</span>' if num else ''
    i = f'<p class="body-copy">{intro}</p>' if intro else ''
    return f'''<section class="cs-section"><div class="wrap">
<div class="cs-section-head">{n}<h2>{label}</h2>{i}</div>
{content}
</div></section>'''


VIDEO_BASE = 'https://superborn-dev.s3.us-east-1.amazonaws.com/Rare-Sightings/'
def film(file, title, poster):
    p = f' poster="images/{poster}.jpg"' if poster else ''
    src = VIDEO_BASE + file + ('' if poster else '#t=0.1')
    return f'<figure class="film"><video controls playsinline preload="metadata"{p}><source src="{src}" type="video/mp4">Your browser does not support video.</video><figcaption>{title}</figcaption></figure>'


def insight_box(line, tagline):
    return (f'<div class="insight"><p class="ins-line">{line}</p>'
            f'<p class="eyebrow">The idea</p><p class="ins-tag">{tagline}</p></div>')

def live_phone(src):
    return ('<div class="live-phone-wrap"><div class="live-phone" data-src="' + src + '">'
            '<div class="live-phone-screen"><iframe title="synthcity.tv, live" allow="autoplay; fullscreen" loading="lazy"></iframe>'
            '<button class="live-phone-start" type="button">Load the live call</button></div></div>'
            '<p class="live-phone-note">Tap Accept, sound on. <button class="live-phone-reload" type="button">Restart ↻</button></p></div>')

# Phone-width versions of the category line, short enough to stay on one line.
SHORT_TAGS = {
    'synth-city.html': ['Premier Gem', 'Soft launch 2026', 'Concept, CD, AD'],
    'desert-diamonds.html': ['Premier Gem', 'Films + microsite', 'Concept, AD, Design'],
    'brown-co.html': ['Pitch', 'Integrated', 'Concept, CD, AD'],
    'fage.html': ['Spec', 'Integrated', 'Concept, CD, AD'],
    'uber.html': ['Spec', 'Integrated', 'Concept, CD, AD'],
    'turbochef.html': ['Spec', 'Integrated', 'Concept, CD, AD'],
}

# ---------- Uber helpers ----------
LASTCALL_TAG = f'\n<script src="js/lastcall.js?v={_v("js/lastcall.js")}" defer></script>'
# Each optional asset switches its piece on as soon as the file is added;
# until then nothing empty or non-working is shown on the live page.
_ROOT = _o.path.join(_o.path.dirname(__file__), '..')
def has_file(rel): return _o.path.exists(_o.path.join(_ROOT, rel))
def has_img(name): return has_file(f'images/{name}.jpg')

UB_COASTERS = [
    ('ub-coaster-ex', 'Coaster: Should I text my ex? Just to say hi. Time to go. Uber.', 'The ex.'),
    ('ub-coaster-boat', 'Coaster: Let&#39;s all quit our jobs and buy a boat. Time to go. Uber.', 'The boat.'),
    ('ub-coaster-dj', 'Coaster: I could definitely be a DJ. Time to go. Uber.', 'The DJ.') if has_img('ub-coaster-dj') else ('ub-coaster-tattoos', 'Coaster: We should all get matching tattoos. Time to go. Uber.', 'The tattoos.'),
    ('ub-coaster-sommelier', 'Coaster: I&#39;m basically a sommelier. Time to go. Uber.', 'The sommelier.') if has_img('ub-coaster-sommelier') else ('ub-coaster-food', 'Coaster: Let&#39;s order bar to the food. Time to go. Uber.', 'The order.'),
]

# Digital billboard with time-based headlines (a proposed schedule, shown as examples).
# Turns on when images/ub-billboard-clean.jpg exists. The headline layer is a
# 1000x380 design surface warped onto the board's blank face with a perspective
# matrix measured from that photo (corners 412,330 / 1450,58 / 1468,535 / 395,672
# in its 1672x941 pixels). Re-measure if the image is ever replaced.
UB_BB_HEADLINES = [
    ('10:00 PM', 'Just one more.'),
    ('12:30 AM', 'We should<br>start a band.'),
    ('1:45 AM', 'You&#39;re giving the bartender<br>career advice.'),
    ('2:00 AM', 'Close your tab.<br>Open your app.'),
]
UB_BB_MATRIX = 'matrix3d(0.616071194,-0.288877152,0,-0.000290985384,-0.0735691713,0.850948544,0,-7.29932386e-05,0,0,1,0,412,330,0,1)'

def billboard_html():
    if not has_img('ub-billboard-clean'):
        return img('ub-billboard', 'Digital billboard over a nightlife street: Close your tab. Open your app.', 'Digital billboard.')
    tabs = ''.join(f'<button type="button" class="bb-time" role="tab" aria-selected="false" data-i="{i}">{tm}</button>' for i, (tm, _) in enumerate(UB_BB_HEADLINES))
    heads = ''.join(f'<p class="bb-head" data-i="{i}" aria-hidden="true">{hl}</p>' for i, (_, hl) in enumerate(UB_BB_HEADLINES))
    alts = ' / '.join(f'{tm}: ' + hl.replace('<br>', ' ') for tm, hl in UB_BB_HEADLINES)
    return ('<div class="billboard"><div class="bb-art" role="img" aria-label="A rooftop billboard over a Manhattan street at night, with headlines that change through the night: ' + alts + '. When it&#39;s time to go. Uber.">'
            '<img src="images/ub-billboard-clean.jpg" alt="" loading="lazy">'
            '<div class="bb-stage"><div class="bb-face" style="transform:' + UB_BB_MATRIX + '">'
            f'<div class="bb-heads">{heads}</div>'
            '<div class="bb-foot"><span class="bb-tag">When it&#39;s time to go.</span><img class="bb-logo" src="images/uber-logo-white.png" alt=""></div>'
            '</div></div></div>'
            f'<div class="bb-times" role="tablist" aria-label="Headline by time of night">{tabs}</div>'
            '<p class="bb-note">A proposed schedule: one digital board, four headlines through the night. Example times. Pick one.</p></div>')

UB_SAMPLES = [
    ('audio/ub-lastcall-business-partners.mp3', 'The Business Partners'),
    ('audio/ub-lastcall-text-message.mp3', 'The Text Message'),
    ('audio/ub-lastcall-great-idea.mp3', 'The Great Idea'),
]
# Future real-time AI operator: set to your server's session endpoint, which
# issues short-lived tokens. Empty = no live control is shown. Never put API keys here.
UB_LIVE_ENDPOINT = ''

UB_LASTCALL = has_img('ub-payphone') or has_img('ub-payphone-closeup')

def lastcall_panel():
    """The approved close-up is the payphone itself. A transparent button sits
    exactly over the photographed PICK UP THE PHONE key (percent-positioned, so
    it stays aligned at every size). The button only exists once something can
    actually happen: sample recordings, or later a live operator endpoint."""
    if not has_img('ub-payphone-closeup'):
        return ''
    samples = [(src, label) for src, label in UB_SAMPLES if has_file(src)]
    interactive = bool(samples) or bool(UB_LIVE_ENDPOINT)
    art = ('<img src="images/ub-payphone-closeup-v2.jpg" width="805" height="1581" alt="The Last Call Department payphone: worn chrome keypad, an empty receiver cradle and a plate reading For great ideas after midnight. '
           'Pick up. Share your brilliant idea. We&#39;ll decide if it&#39;s time to go. Pick up the phone. Uber." loading="lazy">')
    if not interactive:
        return f'<div class="lastcall-art">{art}</div>'
    btns = ''.join(f'<button type="button" class="lc-sample" data-src="{src}" aria-pressed="false"><span class="lc-ic" aria-hidden="true"></span>{label}</button>' for src, label in samples)
    return (f'<div class="lastcall-art is-interactive" data-live-endpoint="{UB_LIVE_ENDPOINT}">{art}'
            '<button type="button" class="lc-hot" aria-label="Pick up the phone" aria-expanded="false" aria-controls="lcOverlay"></button>'
            '<div class="lc-overlay" id="lcOverlay" hidden>'
            '<p class="lc-label">Concept demo · AI voice · sample recordings</p>'
            '<p class="lc-prompt">Choose a case to hear the operator.</p>'
            f'<div class="lc-samples" role="group" aria-label="Sample calls">{btns}</div>'
            '<div class="lc-live" hidden></div>'
            '<p class="lc-status" aria-live="polite"></p>'
            '<button type="button" class="lc-hangup">Hang up</button>'
            '</div></div>')

def sample_audio(src, label):
    return f'<div class="sample-audio"><p class="lc-label">{label}</p><audio controls preload="none" src="{src}"></audio></div>'

# ---------- Layout system (left-aligned rows, nothing cropped) ----------
# rows(...) takes explicit rows of images; images in a row share one height,
# widths follow each image's own shape, captions sit under their own image.
from PIL import Image as _PILImage
def _ratio(src):
    try:
        w, h = _PILImage.open(_o.path.join(_ROOT, 'images', src + '.jpg')).size
        return w / h
    except Exception:
        return 1.5

# A Mac browser window around a screen grab (shared component).
def browser_fig(src, alt, cap='', url='synthcity.tv'):
    r = _ratio(src)
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    lock = '<svg viewBox="0 0 12 14" aria-hidden="true" focusable="false"><rect x="1.5" y="6" width="9" height="7" rx="1.5"/><path d="M3.5 6V4.2a2.5 2.5 0 0 1 5 0V6" fill="none"/></svg>'
    return (f'<div class="g-row bw-row"><figure class="gf bwf" style="--r:{r:.4f}"><div class="bw">'
            f'<div class="bw-bar" aria-hidden="true"><span class="bw-lights"><i></i><i></i><i></i></span>'
            f'<span class="bw-url">{lock}{url}</span><span class="bw-end"></span></div>'
            f'<img src="images/{src}.jpg" alt="{alt}" loading="lazy" decoding="async"></div>{c}</figure></div>')

# FAGE "Buzz for the truth": tap a name on the photographed intercom to hear
# that neighbor's confession. Hotspots are % boxes over each name plate.
BUZZ = [   # (name, audio, left, top, width, height)
    ('6F · Matt',  'audio/fage-buzz-matt.mp3',  48.3, 42.6, 22.8, 3.9),
    ('3C · Helen', 'audio/fage-buzz-helen.mp3', 48.3, 52.6, 22.8, 3.9),
    ('2A · Lisa',  'audio/fage-buzz-lisa.mp3',  48.3, 57.6, 22.8, 4.0),
]
BUZZ_TAG = f'\n<script src="js/buzz.js?v={_v("js/buzz.js")}" defer></script>'

def buzz_panel():
    hots = ''.join(f'<button type="button" class="bz-hot" data-src="{src}" data-name="{n}" aria-pressed="false" '
                   f'style="left:{l}%;top:{t}%;width:{w}%;height:{h}%"><span class="sr">Buzz {n}</span></button>'
                   for n, src, l, t, w, h in BUZZ)
    return (f'<figure class="gf bz" style="--r:{_ratio("fage-buzz"):.4f}"><div class="bz-art">'
            '<img src="images/fage-buzz.jpg" alt="A woman presses a buzzer on a brass intercom under a sign reading Buzz for the truth. Everyone here has a yogurt secret. Go on. Buzz someone." loading="lazy">'
            f'{hots}</div><figcaption>Buzz for the truth. <span class="bz-note">Tap a name to hear their confession. Concept demo, sample recordings.</span>'
            '<span class="bz-status" aria-live="polite"></span></figcaption></figure>')

def gfig(src, alt, cap=''):
    r = _ratio(src)
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    return f'<figure class="gf" style="--r:{r:.4f}"><img src="images/{src}.jpg" alt="{alt}" loading="lazy">{c}</figure>'

def rows(*rs):
    """Each row is a list of (src, alt, cap). A row may instead be ('cls', [items])
    to add a class (e.g. 'narrow' caps the row width for very tall pairs).
    A raw HTML string is inserted as its own row (for interactive pieces)."""
    out = []
    for r in rs:
        if isinstance(r, str):
            out.append(r); continue
        cls = ''
        if isinstance(r, tuple) and len(r) == 2 and isinstance(r[0], str) and isinstance(r[1], list):
            cls, r = ' ' + r[0], r[1]
        figs = ''.join(gfig(*it) for it in r)
        solo = ' solo' if len(r) == 1 and _ratio(r[0][0]) < 1.2 else ''
        out.append(f'<div class="g-row{solo}{cls}">{figs}</div>')
    return '<div class="g">' + ''.join(out) + '</div>'

# A second image shown directly under a case-study hero (a reveal).
HERO_ROWS = {
    'fage-blank': [('fage-blank', 'A huge, almost entirely blank billboard over a New York street, with only a small ingredients label: milk, live active cultures', 'The billboard.'),
                   ('fage-closeup', 'Close-up of the billboard&#39;s small label: Ingredients: milk, live active cultures. Honestly crafted. Nothing to hide. FAGE.', 'Read the fine print.')],
    'dd-hero': [('dd-hero', 'A photographer disguised as a lizard watches a woman wearing a diamond ring', '')],
    'ub-receipt': [('ub-receipt', 'An itemized bar receipt from the Tipsy Oak: two Old Fashioneds, fries, four OK one more, I&#39;m not even tired, we should start a business, I love you guys. Total: time to go. Close your tab. Open your app. Signed off with the Uber logo.', '')],
}
HERO_FOLLOW = {
    'fage-blank': ('fage-closeup', 'Close-up of the billboard&#39;s small label: Ingredients: milk, live active cultures. Honestly crafted. Nothing to hide. FAGE.', 'Read the fine print.'),
}

# Credits, classification and sharing details for each case study.
# Classification is stated plainly; nothing here claims results or launches
# that aren't documented.
CREDITS = {
    'synth-city.html': ('Commissioned', 'Premier Gem, where I&#39;m Creative Director. Soft-launched in 2026; the full rollout is in development.',
                        'Concept, creative direction, art direction'),
    'desert-diamonds.html': ('Commissioned', 'Premier Gem. The Rare Sightings microsite is live at premiergem.com; the field reporter program is rolling out.',
                             'Concept, art direction, design'),
    'brown-co.html': ('Pitch', 'Proposed to Brown &amp; Co. Jewelers. The Moments Lamp and the billboard program are proposals. Visuals AI-assisted.',
                      'Concept, creative direction, art direction'),
    'fage.html': ('Spec', 'Self-initiated. Not commissioned by FAGE. Visuals AI-assisted.', 'Concept, creative direction, art direction'),
    'uber.html': ('Spec', 'Self-initiated. Not commissioned by Uber. Visuals AI-assisted; the payphone samples are AI voice.', 'Concept, creative direction, art direction'),
    'turbochef.html': ('Spec', 'Self-initiated. Not commissioned by TurboChef. Visuals AI-assisted.', 'Concept, creative direction, art direction'),
}
CASE_META = {   # page title, social preview image
    'synth-city.html': ('Synth City: The Future Ran Out of Rarity | Asher Wilens', 'thumb-synth-city'),
    'desert-diamonds.html': ('Desert Diamonds: A Natural Diamond Is a Rare Sighting | Asher Wilens', 'thumb-desert-diamonds-v2'),
    'brown-co.html': ('Brown &amp; Co.: Love Looks Different in Every Light | Asher Wilens', 'thumb-brown-co-v2'),
    'fage.html': ('FAGE: Nothing to Hide | Asher Wilens', 'thumb-fage'),
    'uber.html': ('Uber: When It&#39;s Time to Go | Asher Wilens', 'thumb-uber-v2'),
    'turbochef.html': ('TurboChef: Compliments to the Chef | Asher Wilens', 'thumb-turbochef'),
}
NEXT = {
    'synth-city.html': ('fage.html', 'Fage'), 'fage.html': ('uber.html', 'Uber'), 'uber.html': ('desert-diamonds.html', 'Desert Diamonds'),
    'desert-diamonds.html': ('brown-co.html', 'Brown &amp; Co.'), 'brown-co.html': ('turbochef.html', 'TurboChef'), 'turbochef.html': ('synth-city.html', 'Synth City'),
}

def credits_html(fname):
    c = CREDITS.get(fname)
    if not c:
        return ''
    kind, note, role = c
    return (f'<section class="credits wrap" aria-label="Credits"><dl>'
            f'<div><dt>Work</dt><dd><b>{kind}.</b> {note}</dd></div>'
            f'<div><dt>Role</dt><dd>{role}</dd></div></dl>'
            f'<p class="credits-links"><a class="text-link" href="index.html#work">All work</a><a class="text-link" href="resume.pdf" target="_blank" rel="noopener">Résumé</a><a class="text-link" href="mailto:{EMAIL}">{EMAIL}</a></p></section>')

def case(fname, name, tags, lede, intro, hero, hero_alt, sections, nxt, nxt_name, desc):
    nxt, nxt_name = NEXT.get(fname, (nxt, nxt_name))
    split = ''
    phone_open = ''
    if hero == 'moments:':
        hero_html = moments_hero()
    elif hero.startswith('trailer:'):
        src, poster = hero[8:].split('|')
        hero_html = ('<div class="wrap trailer"><p class="trailer-label">Watch the campaign trailer</p>'
                     '<div class="trailer-frame">'
                     f'<video class="trailer-video" playsinline preload="metadata" poster="images/{poster}.jpg" aria-label="{hero_alt}">'
                     f'<source src="{src}" type="video/mp4">'
                     f'<a href="{src}">Watch the Synth City trailer (MP4)</a></video>'
                     '<button type="button" class="trailer-play" aria-label="Play the Synth City trailer with sound"><span aria-hidden="true"></span></button>'
                     '<p class="trailer-soon" role="status">The trailer didn&#39;t load here. Use the link below.</p></div>'
                     f'<p class="trailer-fallback">Trouble playing it? <a class="text-link" href="{src}" target="_blank" rel="noopener">Open the trailer video →</a></p></div>')
    elif hero.startswith('phone:'):
        src, himg, hcap = hero[6:].split('|')
        hero_html = (f'<div class="wrap cs-hero"><figure><img src="images/{himg}.jpg" alt="{hero_alt}"><figcaption>{hcap}</figcaption></figure></div>'
                     '<div class="wrap cs-open">'
                     '<p class="answer-prompt">How do we know? <span>Answer the call below to find out</span></p>'
                     f'{live_phone(src)}</div>')
        phone_open = 'yes'
    elif hero.startswith('video:'):
        src, poster = hero[6:].split('|')
        hero_html = f'<div class="wrap cs-hero"><div class="video-embed"><video controls playsinline preload="metadata" poster="images/{poster}.jpg" aria-label="{hero_alt}"><source src="{src}" type="video/mp4">Your browser does not support video.</video></div></div>'
    elif hero in HERO_ROWS:
        hero_html = '<div class="wrap cs-hero">' + rows(HERO_ROWS[hero]).replace(' loading="lazy"', ' fetchpriority="high"', 1) + '</div>'
    else:
        hero_html = f'<div class="wrap cs-hero"><img src="images/{hero}.jpg" alt="{hero_alt}"></div>'
        if hero in HERO_FOLLOW:
            f_img, f_alt, f_cap = HERO_FOLLOW[hero]
            hero_html += f'<div class="wrap cs-hero cs-hero-follow"><figure><img src="images/{f_img}.jpg" alt="{f_alt}" loading="lazy"><figcaption>{f_cap}</figcaption></figure></div>'
    sep = '<span class="dot">•</span>'
    full = sep.join((f'<b>{t}</b>' if i == 0 else t) for i, t in enumerate(tags))
    short_tags = SHORT_TAGS.get(fname, tags)
    short = sep.join((f'<b>{t}</b>' if i == 0 else t) for i, t in enumerate(short_tags))
    tag_html = f'<span class="full">{full}</span><span class="short">{short}</span>'
    head_text = f'''<a class="text-link back" href="index.html#work">← All work</a>
<p class="cs-meta byline">{tag_html}</p>
<h1 class="display">{name.upper()}</h1>
<p class="lede">{lede}</p>''' + f'<p class="body-copy">{intro}</p>'
    if split:
        head_text += '<p class="answer-prompt">Someone from 2187 is calling. <span>Answer it</span></p>'
        head_inner = f'<div class="cs-split"><div class="cs-split-text">{head_text}</div><div class="cs-split-phone">{split}</div></div>'
    else:
        head_inner = head_text
    body = f'''<header class="cs-head{' has-phone' if split else ''}"><div class="wrap">
{head_inner}
</div></header>
{hero_html}
{''.join(sections)}
{credits_html(fname)}
<nav class="next wrap" aria-label="Next project"><a href="{nxt}"><span class="eyebrow">Next project</span><span class="display">{nxt_name.upper()} →</span></a></nav>'''
    title, og = CASE_META.get(fname, (f'{name} | Asher Wilens', 'thumb-synth-city'))
    page(fname, title, desc, body, 'work', og=og)

# ---------- HOME ----------
# Advertising work, in display order. (page, thumbnail, name, campaign line, classification)
FEATURED = ('synth-city.html', 'synth-hero', 'Synth City', 'The future ran out of rarity.', 'Integrated campaign · Premier Gem · Soft launch 2026',
            'Six films, a state-run news network and a working detector, set in a future where everything can be manufactured. Except rarity.')
work = [
    ('fage.html', 'thumb-fage', 'Fage', 'Nothing to hide.', 'Brand platform · Spec'),
    ('uber.html', 'thumb-uber-v2', 'Uber', 'When it&#39;s time to go.', 'Integrated campaign · Spec'),
    ('desert-diamonds.html', 'thumb-desert-diamonds-v2', 'Desert Diamonds', 'A natural diamond is a rare sighting.', 'Campaign · Films · Microsite · Premier Gem'),
    ('brown-co.html', 'thumb-brown-co-v2', 'Brown &amp; Co.', 'Love looks different in every light.', 'Retail experience · Pitch'),
    ('turbochef.html', 'thumb-turbochef', 'TurboChef', 'Compliments to the chef.', 'Integrated campaign · Spec'),
    ('synth-city.html', 'thumb-synth-city', 'Synth City', 'The future ran out of rarity.', 'Integrated campaign · Premier Gem'),
]
SHOW_FEATURE = False   # True puts Synth City back as the large featured piece above the grid
cards = ''.join(f'''<a class="card" href="{h}"><div class="frame"><img src="images/{im}.jpg" alt="{n}: {line}" loading="lazy"></div>
<div class="card-title"><h3>{n}</h3></div><p class="card-line">{line}</p><p class="card-tag">{tag}</p></a>''' for k, (h, im, n, line, tag) in enumerate(work)
    if not (SHOW_FEATURE and h == FEATURED[0]))

LAB_PREVIEW = [
    ('lab.html#orion', 'orion-m-06', 'Project Orion', 'Patented projection that turns any room into the screen.'),
    ('lab.html#incomparables', 'incomp-03', 'Incomparables', 'Diamond offcuts, set in gold. Launched, and still selling.'),
    ('lab.html#riff', 'riff-03', 'The Riff', 'A gig bag that doubles as a guitar stand. A Quirky winner.'),
]
LAB_PV_POS = {'riff-03': '78% 50%'}   # crop focus per thumbnail
lab_cards = ''.join(f'''<a class="lab-pv" href="{h}"><div class="frame"><img src="images/{im}.jpg" alt="{n}" loading="lazy" style="object-position:{LAB_PV_POS.get(im, '50% 50%')}"></div><h3>{n}</h3><p>{d}</p></a>''' for h, im, n, d in LAB_PREVIEW)

about = f'''<section class="section about-sec" id="about"><div class="wrap about-grid">
<div><p class="eyebrow">About</p><h2 class="display">The idea comes first. The medium follows.</h2></div>
<div class="about-copy">
<p>I&#39;m an art director and creative director who believes the best ideas don&#39;t stay inside the ad. They become experiences, products and, occasionally, things that need patents.</p>
<p>Since 2017 I&#39;ve led creative at Premier Gem, a multi-generation natural-diamond house: campaigns, brand identity, trade and retail presentation, social and the digital tools around them. The work has earned multiple Best Design Awards at the Centurion Jewelry Show. Since 2024 I&#39;ve also been a partner and creative director at Superborn Group, building campaign platforms and products for startups and established brands. Along the way I&#39;ve freelanced as an art director for Brown &amp; Co., Lumije and The Woo Agency.</p>
<p>I find a simple human truth, then figure out the most interesting way to bring it into the world: a headline, a print ad, an integrated campaign or something nobody has built yet. I trained in advertising at SVA, and I invent on the side, including a patented AR projection method.</p>
<p class="about-links"><a class="btn" href="resume.pdf" target="_blank" rel="noopener">Résumé (PDF)</a><a class="text-link" href="mailto:{EMAIL}">{EMAIL}</a></p>
</div></div></section>'''

fh, fim, fn, fline, ftag, fdesc = FEATURED
feature_html = (f'''<div class="wrap">
<a class="feature" href="{fh}">
<div class="frame"><img src="images/{fim}.jpg" alt="Synth City: a crowd presses around a single rough natural diamond in a vitrine while workers sweep piles of synthetic diamonds off the floor"></div>
<div class="feature-meta"><div><p class="eyebrow">{ftag}</p><h2>SYNTH CITY</h2><p class="feature-line">{fline}</p></div>
<p>{fdesc}</p></div>
</a>
</div>''' if SHOW_FEATURE else '')
home = f'''<section class="intro"><div class="wrap">
<p class="eyebrow">Asher Wilens</p>
<h1 class="display intro-title"><span class="nw">Senior Art Director <span class="slash">/</span></span> <span class="nw">Creative Director</span></h1>
<p class="intro-copy">I develop campaigns, experiences and products that bring brands into people&#39;s lives in unexpected ways. Part traditional advertising. Part emerging technology. Always idea-first.</p>
<p class="intro-line">Concepts. Campaigns. Experiences. Inventions.</p>
</div></section>
{feature_html}
<section class="section" id="work"><div class="wrap">
<div class="section-head"><h2 class="display">Work</h2></div>
<div class="g-work">{cards}</div>
</div></section>
<section class="section lab-teaser"><div class="wrap">
<div class="section-head"><div><p class="eyebrow">Inventions</p><h2 class="display">Beyond the brief.</h2><p class="lab-teaser-line">Some ideas become campaigns. Others become platforms, products and patents.</p></div><a class="btn" href="lab.html">See the inventions</a></div>
<div class="lab-pvs">{lab_cards}</div>
</div></section>
{about}'''
page('index.html', 'Asher Wilens | Senior Art Director &amp; Creative Director',
     'Portfolio of Asher Wilens, an advertising creative director and senior art director creating integrated campaigns, brand experiences and inventive creative technology.', home, 'work')

# ---------- LAB ----------
# Each invention is one dict. Media is framed 3:2 everywhere; per image:
#   fit: 'cover' (crop) or 'contain' (whole image on a matching ground, for
#        artwork with type running to the edges), pos: object-position for
#        the crop, bg: the ground colour behind 'contain'.
#   video: optional short muted loop (mp4) that replaces the still later; the
#          still stays as its poster.
#   compare: optional {'before': src, 'after': src, 'before_alt', 'after_alt'}
#          reserved for a future before/after reveal (Draiped). Rendered as a
#          static 'after' image until the interaction is built.
LAB = [
    dict(slug='orion', eyebrow='01 · Experiential technology', name='PROJECT ORION',
         head='The room is the screen.',
         copy='Orion projects digital imagery straight onto the objects and surfaces around you. No headset, no phone, nothing to download. A table, a wall or a shop window becomes part of the story, so retail floors, live events and brand activations become places people step into, not screens they look at.',
         src='https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/po_9.png', w=2826, h=1584,
         alt='The Project Orion projector, a small rounded device with three lenses, on a coffee table in a living room',
         fit='cover', pos='50% 50%',
         status='Patented',
         story=dict(w=1080, h=1440, portrait=True, fit_m='contain',
                    seq=dict(dir='images/orion-seq/', count=171, fps=15, w=630, h=840, beats=[0, 0.5, 0.8, 1.9, 3.0, 4.9, 7.1, 11.33]),
                    frames=[
             ('orion-m-01', 'An ordinary living room at night: two sofas, a floor lamp, a couple looking at their phones and the white Orion projector on a round coffee table.', 'An ordinary room.'),
             ('orion-m-02', 'Orion begins to scan, casting a circle of cyan grid onto the far wall and sofa.', 'Orion starts to scan.'),
             ('orion-m-03', 'The cyan grid now covers the walls, ceiling and sofa cushions, mapping the room.', 'Every surface mapped.'),
             ('orion-m-04', 'A projected menu on the gridded wall reads Select projection mode: Gaming entertainment.', 'Choose a world.'),
             ('orion-m-05', 'A swirling cyan portal opens on the wall, spiders massing inside it.', 'The wall opens.'),
             ('orion-m-06', 'Projected spiders pour out of the portal across the wall and sofa as the couple aim their phones.', 'The horde breaks through.'),
             ('orion-m-07', 'Spiders swarm the sofa beneath the glowing portal while the players fight them off with their phones.', 'The room is the screen.'),
         ]),
         patent=('U.S. Patent No. 11,127,212', 'Method of projecting virtual reality imagery for augmenting real world objects and surfaces', 'https://patents.google.com/patent/US11127212B1/en')),
    dict(slug='incomparables', eyebrow='02 · Fine jewelry', name='INCOMPARABLES',
         head='Nothing was cut out to make these. They were what got cut off.',
         copy='Every diamond cut leaves pieces behind. At Premier Gem those offcuts sat in a box collecting dust, so I proposed setting them, rough and one of a kind, in gold. They became the Incomparables: rings, pendants and earrings, sold wholesale to Premier Gem&#39;s retail partners and direct online, and still selling today.',
         src='images/incomp-03.jpg', w=1100, h=1100,
         alt='An Incomparables pendant: a rough diamond offcut bezel-set in yellow gold',
         fit='cover', pos='50% 50%',
         story=dict(w=1100, h=1100, portrait=True, fit_m='contain', frames=[
             ('incomp-01', 'A single rough diamond offcut alone on black rock.', 'What got left behind.'),
             ('incomp-06', 'A rough diamond offcut bezel-set in a rose gold ring, resting on glittering black sand.', 'Set in gold.'),
             ('incomp-07', 'A yellow gold pendant with an irregular rough diamond slice lying on black sand.', 'Then a pendant.'),
             ('incomp-03', 'An Incomparables pendant, an irregular rough diamond in a yellow gold bezel, in warm light.', 'No two the same shape.'),
             ('incomp-08', 'A white gold pendant with a rough diamond hanging over green stone, a painted Tuscan landscape behind.', 'In every metal.'),
             ('incomp-04', 'The collection on blue: rings and pendants in rose, white and yellow gold, each stone a different shape.', 'A whole collection.'),
             ('incomp-05', 'A model wearing Incomparables drop earrings, two rough diamonds set in gold.', 'Every piece one of a kind.'),
             ('incomp-09', 'A model wearing a three-stone Incomparables pendant in white, rose and yellow gold.', 'Worn, not forgotten.'),
         ]),
         status='Launched · Premier Gem · Sold wholesale and online',
         links=[('https://premiergem.com/diamond-rough', 'premiergem.com'), ('https://incomparables.etsy.com', 'Etsy')]),
    dict(slug='draiped', eyebrow='02 · AI creative studio', name='DRAIPED',
         head='One product shot. A whole launch.',
         copy='An AI studio for jewelers. Upload a single photo and get on-model images, Instagram carousels with copy, web banners and marketplace listings in minutes. Built by someone who spent years art-directing fine jewelry the slow way.',
         src='images/lab-draiped.jpg', w=1672, h=941,
         alt='A plain uploaded ring photo beside the Draiped on-model result of the same ring',
         fit='cover', pos='50% 50%', compare=None,
         story=dict(w=928, h=1152, portrait=True, fit_m='contain', frames=[
             ('draiped-w-01', 'A loose round brilliant diamond on cream paper beside tweezers and a jeweler&#39;s loupe.', 'Upload a loose stone.'),
             ('draiped-w-02', 'A pencil design sheet for a white gold teardrop pendant with the diamond in a bezel setting, shown front, side and bail detail, annotated chain, white gold, bezel.', 'Draiped sketches the design.'),
             ('draiped-w-03', 'The finished white gold teardrop pendant rendered on warm sandstone.', 'Renders the finished piece.'),
             ('draiped-w-04', 'The pendant worn on a model in a cream knit top, soft daylight.', 'Puts it on a model.'),
             ('draiped-w-05', 'Campaign still life: the pendant on black glass beside a champagne coupe with a lipstick mark and a satin cloth.', 'Styles the campaign. Ready to post.'),
         ]),
         status='Live', link=('https://draiped.com', 'draiped.com')),
    dict(slug='pinverse', eyebrow='03 · AI game platform', name='PINVERSE ARCADE',
         head='Type a world. Play it as pinball.',
         copy='Pinverse turns any prompt or photo into a playable pinball table in seconds. Players share, remix and compete on each other&#39;s machines, so everyone gets to be the designer.',
         src='images/lab-pinverse.jpg', w=1672, h=941,
         alt='The prompt haunted diner on Saturn becoming a playable pinball table on a phone',
         fit='cover', pos='58% 50%',
         story=dict(w=768, h=1365, portrait=True, fit_m='contain', nocap=True,
                    seq=dict(dir='images/pinverse-seq/', count=71, fps=12, w=450, h=800, beats=[0, 1.5, 4.5, 5.6, 5.85]),
                    frames=[
             ('pinverse-v-01', 'Pinverse Arcade on a phone: Create your pinball world, with the prompt A volcano island typed in and a Generate World button.', 'Type a world.', 'still'),
             ('pinverse-m-04', 'Then you play it: a steel ball in play on the volcano table, lava ramps glowing.', 'Then you play it.'),
             ('pinverse-m-05', 'The volcano erupts on the table as the ball hits the eruption target.', 'Eruption.'),
             ('pinverse-v-03', 'The volcano table in play, a steel ball blazing off the lava bumper in a burst of fire.', 'Play it.', 'still'),
         ]),
         status='Live', link=('https://pinversearcade.com', 'pinversearcade.com')),
    dict(slug='harmony', eyebrow='04 · Wearable music', name='HARMONY HAT',
         head='A hat you can play.',
         copy='A collectible cap with synth keys built into the brim. Wearable music for artist collaborations, limited drops and fan merch.',
         src='https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/hh_promo2.png', w=1672, h=941,
         alt='A hand pressing the piano keys built into the brim of the Harmony Hat',
         fit='contain', bg='#f1f1f3',
         story=dict(w=768, h=1376, portrait=True, frames=[
             ('harmony-v-01', 'A plain black baseball cap resting on a concrete plinth in a soft, neutral room.', 'Just a hat.'),
             ('harmony-v-02', 'The same black cap, now with a row of glowing synth keys built into the brim.', 'Until the brim lights up.'),
             ('harmony-v-03', 'A musician in a smoky club, headphones around his neck, plays the keys on the brim of his Harmony Hat beside a DJ mixer.', 'Now it&#39;s an instrument.'),
             ('harmony-v-04', 'Close-up of a DJ pressing a glowing blue key on the brim of his Harmony Hat while working the mixer with his other hand.', 'Play it on stage.'),
             ('harmony-v-05', 'A young man on a rainy commuter train, earbuds in, plays the keys on the brim of the Harmony Hat he is wearing.', 'Play it on the ride home.'),
             ('harmony-v-06', 'The same commuter takes the hat off and plays the brim keys with both hands, the cap resting on his knee.', 'Or take it off and really play.'),
         ]),
         status='On Kickstarter', link=('https://www.kickstarter.com/projects/harmonyhat/435543195', 'View the campaign')),
    dict(slug='riff', eyebrow='05 · Musician gear', name='THE RIFF',
         head='The gig bag that stands up for itself.',
         copy='Every gigging guitarist hauls two things to the show: the bag and the stand. The Riff is one. A padded gig bag with a fold-out frame that turns the bag itself into a guitar stand. I invented it after one too many nights carrying both across the city.',
         src='images/riff-03.jpg', w=1100, h=1100,
         alt='A guitar resting on the Riff gig bag, its stand folded out, on a small stage',
         fit='cover', pos='50% 50%',
         story=dict(w=1100, h=1100, portrait=True, fit_m='contain', frames=[
             ('riff-01', 'A musician carries the grey Riff gig bag by its handles across a wooden stage.', 'Carry it to the gig.'),
             ('riff-02', 'Product shot on green: the chrome frame folds out from the back of the bag. Lightweight and protective padded body.', 'Flip out the frame.'),
             ('riff-03', 'An acoustic guitar rests against the Riff, held by its fold-out stand, while the guitarist sets up his mic.', 'The bag becomes the stand.'),
             ('riff-04', 'The guitarist plays on stage with the Riff standing beside him, ready to take the guitar between songs.', 'One less thing to carry.'),
         ]),
         status='Quirky community winner · Prototyped'),
    dict(slug='slickster', eyebrow='06 · Product design', name='SLICKSTER',
         head='Less planning. More living.',
         copy='An automated planning app that turns the chaos of scheduling into a single tap. Product design, UX and brand by A. Wilens.',
         src='https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/slickster_promoneon.png', w=1672, h=941,
         alt='Slickster day-plan screens on a phone and tablet over a city at night',
         fit='contain', bg='#031227',
         story=dict(w=768, h=1376, portrait=True, frames=[
             ('slickster-v-01', 'A phone on a sunlit stone table showing the Slickster logo on its launch screen.', 'Open Slickster.'),
             ('slickster-v-02', 'The Slickster map view of Manhattan, a single cyan pin and a Pick a plan tab at the bottom.', 'Drop a pin.'),
             ('slickster-v-03', 'The slycons screen: mood-based activity icons such as Casual, Romantic, Foodie, Music and Night Out, with Romantic selected and a Generate My Plan button.', 'Pick a mood.'),
             ('slickster-v-04', 'Generating your plan: a timeline with dinner at 7:30 PM, a rooftop bar at 9:00 PM and a third stop still being analyzed.', 'The night plans itself.'),
         ]),
         status='Live', link=('https://slickster.app', 'slickster.app')),
]

def lab_media(p, first=False):
    load = '' if first else ' loading="lazy" decoding="async"'
    style = f'--fit:{p.get("fit","cover")};--pos:{p.get("pos","50% 50%")};--ground:{p.get("bg","var(--soft)")}'
    if p.get('compare'):
        c = p['compare']   # future reveal: both layers present, 'after' shown
        inner = (f'<img class="lab-after" src="{c["after"]}" alt="{c["after_alt"]}" width="{p["w"]}" height="{p["h"]}"{load}>'
                 f'<img class="lab-before" src="{c["before"]}" alt="{c["before_alt"]}" width="{p["w"]}" height="{p["h"]}" loading="lazy" hidden>')
        kind = 'compare'
    elif p.get('video'):
        inner = (f'<video src="{p["video"]}" poster="{p["src"]}" muted loop playsinline autoplay preload="none" aria-label="{p["alt"]}"></video>')
        kind = 'video'
    else:
        inner = f'<img src="{p["src"]}" alt="{p["alt"]}" width="{p["w"]}" height="{p["h"]}"{load}>'
        kind = 'image'
    href = p['link'][0] if p.get('link') else (p['patent'][2] if p.get('patent') else '')
    tag_open = f'<a class="lab-frame" href="{href}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true"' if href and kind != 'video' else '<div class="lab-frame"'
    tag_close = '</a>' if href and kind != 'video' else '</div>'
    return f'{tag_open} data-media="{kind}" data-slug="{p["slug"]}" style="{style}">{inner}{tag_close}'

# ---------- Scroll story: a pinned image that evolves as you scroll ----------
# Reusable: give any Lab entry story=dict(w, h, frames=[(img, alt, caption)])
# with frames as images/<img>.webp (+ .jpg fallback), all the same size and
# aligned. js/scrollstory.js drives opacity from scroll; without JS or with
# reduced motion the frames show as a simple static sequence.
STORY_TAG = f'\n<script src="js/scrollstory.js?v={_v("js/scrollstory.js")}" defer></script>'

# Brand title cards: the first frame of every Lab story. A shared composition,
# each brand's own colour. Swap in a logo later with logo='images/<file>.png'
# (or .svg); until then the brand name is set in type.
TITLE_CARDS = {
    'orion':     dict(bg='#121a21', fg='#7fd0f4', name='PROJECT ORION',   line='Spatial technology'),
    'incomparables': dict(bg='#0d0d0d', fg='#e6dfd2', name='INCOMPARABLES', line='Fine jewelry'),
    'draiped':   dict(bg='#f0ece6', fg='#24211d', name='DRAIPED',         line='Creative intelligence'),
    'pinverse':  dict(bg='#12101c', fg='#b79cf3', name='PINVERSE ARCADE', line='Play and creation'),
    'harmony':   dict(bg='#232323', fg='#f1f1f1', name='HARMONY HAT',     line='Wearable music'),
    'riff':      dict(bg='#1f2a1c', fg='#7fd36b', name='THE RIFF',        line='Musician gear'),
    'slickster': dict(bg='#10172a', fg='#5fe0d2', name='SLICKSTER',       line='Experience planning'),
}

def story_items(st, slug):
    """[(kind, data, caption)] with the brand card first when one exists."""
    items = []
    card = TITLE_CARDS.get(slug)
    if card:
        items.append(('card', card, card['line']))
    items += [('img', (f[0], f[1], len(f) > 3 and f[3] == 'still'), f[2]) for f in st['frames']]
    return items

def story_frames(st, slug, overlay='', first=True):
    items = story_items(st, slug)
    n = len(items)
    out = []
    first_img = next((k for k, it in enumerate(items) if it[0] == 'img'), 0)
    for k, (kind, data, cap) in enumerate(items):
        if kind == 'card':
            mark = (f'<img class="sq-logo" src="{data["logo"]}" alt="{data["name"].title()}">' if data.get('logo')
                    else f'<span class="sq-brand">{data["name"]}</span>')
            out.append(f'<figure class="sq-f sq-card" data-k="{k}" data-card style="--card-bg:{data["bg"]};--card-fg:{data["fg"]}">'
                       f'<div class="sq-card-in">{mark}</div>'
                       f'<figcaption><span class="sq-n">{k + 1:02d} / {n:02d}</span> {cap}</figcaption></figure>')
            continue
        img, alt, still = data
        load = ' fetchpriority="high"' if (k == first_img and first) else ' loading="lazy"'
        mob = st.get('mobile')
        msrc = ''
        if mob:   # portrait art-directed frames for phones (same stages, same order)
            mi = mob['prefix'] + img.split('-')[-1]
            msrc = (f'<source media="(max-width:820px)" srcset="images/{mi}.webp" type="image/webp" width="{mob["w"]}" height="{mob["h"]}">'
                    f'<source media="(max-width:820px)" srcset="images/{mi}.jpg" width="{mob["w"]}" height="{mob["h"]}">')
        out.append(f'<figure class="sq-f{" sq-still" if still else ""}" data-k="{k}"><picture>{msrc}<source srcset="images/{img}.webp" type="image/webp">'
                   f'<img src="images/{img}.jpg" alt="{alt}" width="{st["w"]}" height="{st["h"]}" decoding="async"{load}></picture>'
                   f'<figcaption><span class="sq-n">{k + 1:02d} / {n:02d}</span> {cap}</figcaption></figure>')
    m = st.get('mobile')
    mar = f';--sq-ar-m:{m["w"]}/{m["h"]};--sq-r-m:{m["w"]/m["h"]:.4f}' if m else ''
    cls = ' sq-portrait' if st.get('portrait') else ''
    sq = st.get('seq')
    canvas = (f'<canvas class="sq-canvas" width="{sq["w"]}" height="{sq["h"]}" aria-hidden="true" data-seq="{sq["dir"]}" data-count="{sq["count"]}" '
              f'data-fps="{sq["fps"]}" data-beats="{",".join(str(b) for b in sq["beats"])}"></canvas>') if sq else ''
    overlay = canvas + overlay
    pm = (f';--sq-pos-m:{st["pos_m"]}' if st.get('pos_m') else '') + (f';--sq-fit-m:{st["fit_m"]}' if st.get('fit_m') else '')
    return (f'<div class="sq-frame{cls}" style="--sq-ar:{st["w"]}/{st["h"]};--sq-r:{st["w"]/st["h"]:.4f}{mar}{pm}">' + ''.join(out) + overlay + '</div>')

def story_readout(st, slug=''):
    items = story_items(st, slug)
    n = len(items)
    caps = '|'.join(c for _, _, c in items)
    cards = ','.join('1' if k == 'card' else '0' for k, _, _ in items)
    first = items[0][2]
    cls = ' is-card' if items[0][0] == 'card' else ''
    sty = f' style="color:{items[0][1]["fg"]}"' if items[0][0] == 'card' else ''
    return (f'<p class="sq-readout{cls}"{sty} aria-live="polite" data-caps="{caps}" data-cards="{cards}"><span class="sq-step">01 / {n:02d}</span>'
            f'<span class="sq-cap">{first}</span></p>')

def lab_entry(p, i):
    import re as _re
    p = dict(p, eyebrow=_re.sub(r'^\d+ · ', f'{i + 1:02d} · ', p['eyebrow']))   # numbers follow the list order
    st = f'<span class="lab-state">{p["status"]}</span>'
    for href, label in ([p['link']] if p.get('link') else []) + p.get('links', []):
        st += f'<a class="lab-link" href="{href}" target="_blank" rel="noopener">{label} <span aria-hidden="true">→</span></a>'
    patent = ''
    if p.get('patent'):
        num, title, url = p['patent']
        patent = (f'<a class="lab-patent" href="{url}" target="_blank" rel="noopener">'
                  f'<span class="lab-patent-no">{p["status"]} · {num}</span>'
                  f'<span class="lab-patent-title">{title}</span>'
                  f'<span class="lab-patent-cta">Read the patent <span aria-hidden="true">→</span></span></a>')
    if p.get('story'):
        st_ = p['story']
        n_ = len(story_items(st_, p["slug"]))
        per, per_m = 80, 70   # scroll per stage (vh): roughly most of a screen for each image
        return (f'<article class="lab-item lab-story{" sq-nocap" if st_.get("nocap") else ""}" id="{p["slug"]}" data-sq style="--sq-steps:{n_};--sq-per:{per}vh;--sq-per-m:{per_m}vh">'
                f'<div class="sq-track"><div class="sq-sticky">'
                f'<div class="lab-media sq-media">{story_frames(st_, p["slug"], story_readout(st_, p["slug"]), i == 0)}</div>'
                f'<div class="lab-text"><p class="eyebrow">{p["eyebrow"]}</p><h2 class="display">{p["name"]}</h2>'
                f'<p class="lab-head">{p["head"]}</p><p class="body-copy">{p["copy"]}</p>'
                + (patent if patent else f'<div class="lab-status">{st}</div>')
                + '</div></div></div></article>')
    return (f'<article class="lab-item" id="{p["slug"]}">'
            f'<div class="lab-media">{lab_media(p, i == 0)}</div>'
            f'<div class="lab-text"><p class="eyebrow">{p["eyebrow"]}</p><h2 class="display">{p["name"]}</h2>'
            f'<p class="lab-head">{p["head"]}</p><p class="body-copy">{p["copy"]}</p>'
            + (patent if patent else f'<div class="lab-status">{st}</div>') + '</div></article>')

lab = f'''<div class="wrap">
<section class="lab-hero">
<div><p class="eyebrow">Beyond the brief · Products, platforms &amp; a patent</p><h1 class="display">INVENTIONS</h1><p class="lede">Ideas that didn't fit in a brief.</p></div>
<p>Some ideas become campaigns. Others become products, platforms, and the occasional patent. This is where I follow the idea wherever it goes.</p>
</section>
<div class="lab-list-full">{''.join(lab_entry(p, i) for i, p in enumerate(LAB))}</div>
</div>'''
page('lab.html', 'Inventions: Beyond the Brief | Asher Wilens', 'Inventions, products and platforms by Asher Wilens, including Project Orion, a patented projection method that turns any room into the screen.', lab, 'lab', og='thumb-lab',
     head_extra='\n<link rel="preload" as="image" href="images/orion-m-01.webp" type="image/webp">', scripts_extra=STORY_TAG)

# ---------- ABOUT ----------
about = f'''<div class="wrap about">
<div><div class="ph light">[Portrait photo]</div></div>
<div>
<p class="eyebrow">About</p>
<h1 class="display" style="font-size:clamp(44px,6vw,72px)">ASHER WILENS</h1>
<p class="lede" style="margin-top:24px">Creative Director. I know how brands buy work, because I've spent my career on the brand side making it.</p>
<p class="body-copy" style="margin-top:24px">I came up as an in-house art director and grew into creative director at Premier Gem, where I've led campaigns and brand work alongside partners including De Beers, Forevermark and Sam's Club. Most recently I created Synth City, a transmedia series of six films, a live broadcast site and a working AI tool that make the case for natural diamonds.</p>
<p class="body-copy">Outside the brief, I build things: AI products, wearable music and projected AR. The Lab is where those live. I'm looking to bring that mix of craft, client-side judgment and invention to an agency team.</p>
<h2>Capabilities</h2>
<ul>
<li>Creative direction and campaign platforms</li>
<li>Integrated, experiential and OOH</li>
<li>Luxury and fine jewelry art direction</li>
<li>AI-assisted production and prototyping</li>
<li>Brand worlds, film and digital experiences</li>
</ul>
<h2 id="contact">Contact</h2>
<p class="body-copy"><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="https://www.linkedin.com/">LinkedIn</a> · <a href="resume.pdf">Résumé (PDF)</a></p>
</div>
</div>'''
pass  # About page hidden
if False: page('about.html', 'About | A. Wilens', 'Asher Wilens, Creative Director.', about, 'about')

# ---------- CASE STUDIES ----------
TRAILER_URL = 'https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/synthcity-trailer3.mp4'
PLAYLIST_URL = 'https://youtube.com/playlist?list=PLzGEOC0lqaKMDMQ1OlSfnQW9dEJkE7zTB'

def beat(title, line, text, content):
    return (f'<div class="beat"><div class="beat-head"><h3>{title}</h3><p class="beat-line">{line}</p></div>'
            f'<p class="body-copy">{text}</p>{content}</div>')

sc_insight = insight_box('We can make more diamonds than ever. So what still feels special?', 'Welcome to 2187. Everything is perfect. Nothing is rare.')

sc_path = ('<ol class="path" aria-label="How the campaign connects">'
           '<li>The films</li><li>synthcity.tv</li><li>Rarity Detector</li><li>Synth-Mate Lab</li>' + ('<li>Proposalmatic™</li>' if PM_LISTED else '') + '<li>The transmission</li><li>Premier Gem</li></ol>')

# PROPOSALMATIC: compact card here; the working machine lives on proposalmatic.html.
sc_pm = ('<div class="beat" id="proposalmatic"><div class="beat-head"><h3>PROPOSALMATIC™</h3><p class="beat-line">It automates the proposal.</p></div>'
         '<p class="body-copy">In Synth City, the perfect engagement ring is available in seconds. Choose your commitment, optimize the emotional response and receive a ring identical to millions of others.</p>'
         '<a class="series pm-card" href="proposalmatic.html">'
         '<span class="series-img"><img src="images/pm-card.jpg" alt="The Proposal Kits vending machine in a 2187 airport terminal: lit compartments of engagement rings, numbered 101 to 404, beside a slim touchscreen" loading="lazy"></span>'
         '<span class="series-meta"><span class="eyebrow">Interactive · about 30 seconds</span>'
         '<span class="series-title">True love. Now in seconds.</span>'
         '<span class="series-note">A working engagement-ring vending machine from 2187. Pick a package, set the emotional response and keep the receipt.</span>'
         '<span class="btn">Try Proposalmatic™</span></span></a></div>')

sc_series = ('<a class="series series-poster" href="' + PLAYLIST_URL + '" target="_blank" rel="noopener">'
             '<span class="series-img"><img src="images/synth-series-detective.jpg" alt="Series key art: a detective in a dark suit at his desk turns a diamond ring under a lamp, a rain-streaked window full of flying cars and a neon Synth City sign behind him" width="896" height="1280" loading="lazy">'
             '<span class="series-play" aria-hidden="true"></span></span>'
             '<span class="series-meta"><span class="eyebrow">The series</span>'
             '<span class="series-title">Six episodes. One detective.</span>'
             '<span class="series-body">A diamond detective works the cases the Bureau wants buried: natural stones it has officially erased. Every episode ends the same way. The story was synthetic. So was he.</span>'
             '<span class="series-note">Episodes release on YouTube as the campaign rolls out.</span>'
             '<span class="btn">Watch the series on YouTube</span></span></a>')

sc_end = ('<div class="endcard nowcard">'
          '<p class="endcard-small">Synthetic diamonds. Synthetic love. Synthetic everything.</p>'
          '<p class="endcard-big">The future didn&#39;t run out of diamonds.<br>It ran out of rarity.</p>'
          '<p class="endcard-small brand">Premier Gem</p>'
          '<p class="endcard-mid">Celebrate what can&#39;t be replicated.</p></div>')

# ---------- Rarity Detector: curated screens in a phone (Synth City) ----------
# Each example: (label, image in images/, caption, alt). Add or reorder freely;
# js/detector.js reads whatever is rendered. Tall screens scroll inside the phone.
DETECTOR_TAG = f'\n<script src="js/detector.js?v={_v("js/detector.js")}" defer></script>'
RD_EXAMPLES = [
    ('Detector idle', 'rd-idle', 'The Bureau&#39;s utility for Cycle 2187. Load any object and it rates how rare that object will be.',
     'Rarity Detector idle screen: an icosahedron in a scanning frame, Tap to load a specimen'),
    ('Result: Apple mouse', 'rd-mouse-result', 'Uncommon, 3 of 7. Ordinary objects come back obsolete. This one: an early-era consumer peripheral.',
     'Scan complete: Apple wireless mouse, rarity index Uncommon 3 of 7, Bureau status Obsolete, with a short history and a quote'),
    ('Result: Sharpie', 'rd-sharpie-result', 'Fading, 2 of 7. Every result ends with a line of Bureau philosophy and a hand-off to the Synth-Mate lab.',
     'Scan complete: Sharpie permanent marker, rarity index Fading 2 of 7, Bureau status Obsolete, ending with Meet your Synth-Mate'),
    ('Scan: eternity band', 'rd-ring-analyzing', 'Then a visitor loads a natural diamond eternity band. The registry search begins.',
     'Step 2 of 4, Analyzing material: a scan line passes over a diamond eternity band, origin verifying'),
    ('Result: Erased', 'rd-ring-result', 'Erased, 7 of 7. Status: suppressed. The Bureau has no record of this specimen in our time.',
     'Scan complete in gold: diamond eternity band, rarity index Erased 7 of 7, tier 7 critically rare beyond 2187, Bureau status Suppressed, ending with an Incoming signal button'),
    ('Signal detected', 'rd-signal', 'Only natural stones reach step four: an incoming transmission from someone who does have a record.',
     'Step 4 of 4 in pink: Signal detected, incoming transmission, decrypting stream 92 percent. A natural stone. The Bureau has no record of it. Someone else does.'),
]

def detector_demo(examples=RD_EXAMPLES):
    shots = ''.join(
        f'<img class="rd-shot" src="images/{src}.jpg" alt="{alt}" width="780" data-i="{i}"' + ('' if i == 0 else ' hidden loading="lazy"') + '>'
        for i, (_, src, _, alt) in enumerate(examples))
    tabs = ''.join(
        f'<button type="button" class="rd-tab" role="tab" id="rd-tab-{i}" aria-controls="rdScreen" aria-selected="{"true" if i == 0 else "false"}"'
        f' tabindex="{0 if i == 0 else -1}" data-i="{i}" data-caption="{cap}"><span class="rd-n">{i + 1:02d}</span>{label}</button>'
        for i, (label, _, cap, _) in enumerate(examples))
    return ('<div class="rd-demo" data-rd>'
            '<div class="rd-stage"><div class="rd-phone">'
            f'<div class="rd-screen" id="rdScreen" role="tabpanel" tabindex="0" aria-labelledby="rd-tab-0">{shots}</div>'
            '<span class="rd-island" aria-hidden="true"></span></div></div>'
            '<div class="rd-side"><p class="rd-eyebrow">SCB.DETECTOR // Example scans</p>'
            f'<div class="rd-tabs" role="tablist" aria-label="Rarity Detector examples">{tabs}</div>'
            f'<p class="rd-caption" aria-live="polite">{examples[0][2]}</p>'
            '<p class="rd-hint">Scroll inside the phone to read a full result.</p></div></div>')

sc_k9 = ('<div class="k9">'
         + rows([('k9-screens','Across Synth City the Bureau&#39;s giant screens glitch as the geologist&#39;s face breaks through the broadcast, a crowd in the plaza stopping to look up','The network, interrupted.')],
                [('k9-geologist','Low-light camera feed GEO-09: a geologist in a headlamp holds up a rough natural diamond, signal unstable, status critical','The thing that wasn&#39;t supposed to exist.'),
                 ('k9-scan','Synthetic Compliance Bureau scan: Natural origin detected. File K-9, unauthorized. Registry status: not found. Handling protocol: immediate seizure.','The Bureau&#39;s verdict.')])
         + '<div class="outlinks"><a class="text-link" href="https://synthcity.tv/kalahari">Follow the transmission: synthcity.tv/kalahari →</a></div>'
         + '<div class="intercept"><p class="eyebrow">Optional · intercepted from 2187</p>'
         + '<p class="intercept-title">Answer the transmission</p>'
         + '<p class="intercept-note">A recorded call from 2187. Answer it if you like.</p>'
         + live_phone('https://synthcity.tv/') + '</div></div>')

case('synth-city.html', 'Synth City', ['Premier Gem','Integrated campaign · Soft launch 2026','Creative Direction · Concept · Art Direction'],
     'The future didn&#39;t run out of diamonds. It ran out of rarity.',
     'Six films, a state news network and interactive experiences, set in a world where everything can be manufactured. Except rarity. <span class="fine">Soft-launched in 2026; full rollout in development.</span>',
     'trailer:' + TRAILER_URL + '|synth-poster-v2', 'Synth City campaign trailer',
     [section('01','The insight','', sc_insight),

      section('02','The world','Welcome to the perfect future.',
              rows([('synth-aerial','Aerial view of Synth City at night: flying cars, neon towers and a Welcome to Synth City sign','Cycle 2187.')],
                   [('synth-factory-line','Robotic nozzles drop cut diamonds by the hundreds onto a factory conveyor','Diamonds, by the ton.'),
                    ('synth-vending','A proposal kit vending machine in a 2187 airport terminal','Proposals, to go.')],
                   [('synth-protocol-v2','A giant rain-streaked billboard in Synth City: a smiling couple in gloves raise their ring hands under the line Love is a protocol. Bureau approved compatibility. Synthetic. Flying cars and neon towers fill the night beyond.','Love, pre-approved.')])),

      section('03','The campaign','Enter anywhere. Every path ends with something real.',
              sc_path
              + beat('The Synthetic Bureau','It controls the story.',
                     'One network, one message, repeated until it sticks: synthetic is better.',
                     rows(('small', [('synth-hq','The Synthetic Bureau headquarters, a brutalist monolith with a wireframe-head seal, citizens queuing beneath drones','The Bureau.')]),
                          browser_fig('scfn-oversupply', 'SCB7, Synth City News Network: Breaking. Bureau classifies global synthetic diamond oversupply as economic success. Record output. Stable markets. Humanity optimized. Robotic arms drop diamonds onto a factory conveyor.', 'The network, live at synthcity.tv.'),
                          browser_fig('scfn-per-gram', 'Market update: a news anchor at a glass desk beside a screen reading Natural diamond values surpass Manhattan real estate per gram, for the first time since records began in 2149. Manhattan real estate $15,850 per gram; natural diamonds $17,230 per gram.', 'Natural, now priced per gram.'),
                          browser_fig('scfn-popcorn', 'A giant breaking-news billboard on a rain-soaked, rundown building in Synth City: Synthetic diamond prices drop below movie popcorn combo, beside a diamond and a striped popcorn bucket.', 'The story everyone stops for.'))
                     + '<div class="outlinks"><a class="text-link" href="https://synthcity.tv">Watch the broadcasts: synthcity.tv →</a></div>')
              + beat('The Rarity Detector','It erases the original.',
                     'A working AI tool. Scan anything and the Bureau rates how rare it will be in 2187. Natural stones come back as anomalies.',
                     detector_demo()
                     + '<p class="disclaimer">A fictional classification for the story, not a scientific method of verifying a diamond&#39;s origin.</p>'
                     + '<div class="outlinks"><a class="text-link" href="https://synthcity.tv/rarity" target="_blank" rel="noopener">Try it: synthcity.tv/rarity →</a></div>')
              + beat('Synth-Mates','It replaces love.',
                     'Why stop at diamonds? The Bureau grows the people we fall in love with, then sells them like a 1950s dream.',
                     rows([('sm-chambers-1950s','A 1950s couple in pink and tan, glossy and doll-like, stand in two glass growth chambers in an endless hall of chambers','Grown to order.'),
                           ('sm-showroom','A smiling salesman presents rows of glass chambers holding synthetic bodies','The showroom.')],
                          [('sm2-clonesworths-wide','A glossy 1950s couple wave beside a sign reading Meet the Clonesworths, a pink car and a mint-green house behind them','Meet the Clonesworths.'),
                           ('sm2-dinner','The synthetic couple at a candlelit dinner in a 1950s kitchen','Dinner at six. Every night.')])
                     + '<div class="outlinks"><a class="text-link" href="https://syntheticbureau.com" target="_blank" rel="noopener">Enter the lab: syntheticbureau.com →</a></div>')
              + (sc_pm if PM_LISTED else '')),

      section('04','The films','',
              sc_series),

      section('05','File K-9. The last transmission.','Then a transmission broke through. Beneath the Kalahari, a geologist had found something that wasn&#39;t supposed to exist.',
              sc_k9).replace('<section class="cs-section">','<section class="cs-section cs-dark">',1),

      ('<section class="sc-culmination" aria-label="One diamond worth stopping for">'
       '<div class="wrap"><p class="sc-cul-line">In a world with billions of diamonds, one was worth stopping for.</p></div>'
       '<img src="images/synth-hero.jpg" alt="Synth City: a crowd presses around a single rough natural diamond in a vitrine while workers sweep piles of synthetic diamonds off the floor" loading="lazy" width="1672" height="941">'
       '</section>'),

      section('06','Back to now','',
              '<div class="now">' + rows([('synth-now','Present day: a woman&#39;s hand with a natural diamond engagement ring resting on a sunlit kitchen table beside a coffee cup','')]) + sc_end + '</div>')],
     'desert-diamonds.html', 'Desert Diamonds', 'Synth City: the future didn&#39;t run out of diamonds. It ran out of rarity. An integrated campaign for Premier Gem.')


MOMENTS_TAG = f'\n<script src="js/moments.js?v={_v("js/moments.js")}" defer></script>'

bc_insight = insight_box('Jewelry is chosen under showroom lights. It&#39;s worn under every other kind.', 'Bring the lights of real life into the showroom.')

# The Moments Lamp hero: four matching photographs, one shown at a time.
# The Moments Lamp hero: four matching photographs of the lamp, one per light.
# (key, label, copy, alt, hotspot box over the engraved icon on the base as
#  left/top/width/height in % of the photo, ring centre y within that box %)
BC_MODES = [
    ('candlelight', 'Candlelight', 'The intimacy of two.',
     'The Moments Lamp set to candlelight: warm amber light falls on a solitaire in a velvet box; the candlelight icon on the brass base is lit.',
     (23.1, 75.7, 11.4, 14.1, 34.6)),
    ('sunday', 'Sunday morning', 'The quiet beauty of an ordinary morning.',
     'The Moments Lamp set to Sunday morning: soft dappled daylight behind the same solitaire; the sun icon on the base is lit.',
     (37.2, 76.2, 11.3, 15.4, 34.0)),
    ('city', 'City lights', 'A night out, somewhere unforgettable.',
     'The Moments Lamp set to city lights: a blue night skyline glows behind the solitaire; the city icon on the base is lit blue.',
     (51.4, 76.2, 11.4, 15.4, 36.0)),
    ('celebration', 'Celebration', 'The moments worth raising a glass to.',
     'The Moments Lamp set to celebration: pink and violet sparkle surrounds the solitaire; the champagne icon on the base is lit pink.',
     (65.3, 75.0, 11.5, 14.3, 35.5)),
]
BC_LAMP_IMG = 'bc-pedestal-{}'       # images/bc-pedestal-<key>.jpg, 1448 x 1086
BC_LAMP_W, BC_LAMP_H = 1448, 1086

# Small line icons for the pill row (same motifs as the lamp base).
ML_ICONS = {
    'candlelight': '<rect x="9" y="11" width="6" height="9" rx="1"/><path d="M12 8c-1.2-1.2-1-2.6 0-4 1 1.4 1.2 2.8 0 4z"/>',
    'sunday': '<circle cx="12" cy="12" r="3.6"/><path d="M12 3v2.5M12 18.5V21M3 12h2.5M18.5 12H21M5.6 5.6l1.8 1.8M16.6 16.6l1.8 1.8M5.6 18.4l1.8-1.8M16.6 7.4l1.8-1.8"/>',
    'city': '<path d="M5 20V10h4v10M10 20V5h4v15M15 20v-7h4v7M4 20h16"/>',
    'celebration': '<path d="M7 4h4l-.6 5a1.4 1.4 0 0 1-2.8 0zM13 4h4l-.6 5a1.4 1.4 0 0 1-2.8 0zM9 10.5V19M15 10.5V19M7 19.5h4M13 19.5h4"/>',
}
def ml_icon(k):
    return f'<svg class="ml-ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ML_ICONS[k]}</svg>'

def moments_hero():
    imgs = ''.join(
        f'<img src="images/{BC_LAMP_IMG.format(k)}.jpg" alt="{alt}" width="{BC_LAMP_W}" height="{BC_LAMP_H}" class="ml-img{" on" if i == 0 else ""}" data-mode="{k}"'
        + (' fetchpriority="high"' if i == 0 else ' loading="eager" fetchpriority="low" decoding="async"') + (' aria-hidden="true"' if i else '') + '>'
        for i, (k, _, _, alt, _) in enumerate(BC_MODES))
    # Tap targets over the engraved icons. Pointer-only; the pills below are the
    # keyboard / screen-reader controls, so these stay out of the tab order.
    hots = ''.join(
        f'<button type="button" class="ml-hot" data-mode="{k}" tabindex="-1" aria-hidden="true" title="{label}"'
        f' style="left:{l}%;top:{t}%;width:{w}%;height:{h}%;--ring-y:{ry}%"><span class="ml-ring"></span></button>'
        for k, label, _, _, (l, t, w, h, ry) in BC_MODES)
    btns = ''.join(
        f'<button type="button" class="ml-btn" data-mode="{k}" data-copy="{copy}" aria-pressed="{"true" if i == 0 else "false"}">{ml_icon(k)}<span>{label}</span></button>'
        for i, (k, label, copy, _, _) in enumerate(BC_MODES))
    return ('<div class="wrap moments"><div class="ml-frame ml-hint" style="aspect-ratio:' + f'{BC_LAMP_W}/{BC_LAMP_H}' + '">' + imgs + hots + '</div>'
            f'<div class="ml-controls" role="group" aria-label="Moments Lamp lighting">{btns}</div>'
            f'<p class="ml-copy" aria-live="polite">{BC_MODES[0][2]}</p>'
            '<p class="ml-note">The Moments Lamp: a proposed in-store lighting experience. Tap a light on the lamp.</p></div>')

bc_mechanics = ('<p class="body-copy mech-first">As a proposed holiday promotion, Brown &amp; Co. would invite engagement-ring customers to reserve a personal moment on a digital billboard above Buckhead.</p>'
                '<p class="body-copy">A name. A question. A moment they&#39;ll remember every time they see the city lights.</p>'
                '<p class="steps-label">Proposed mechanics</p><ol class="steps">'
                '<li><strong>Choose the ring.</strong></li>'
                '<li><strong>Reserve the moment.</strong></li>'
                '<li><strong>See your question in lights.</strong></li></ol>')

bc_end = ('<div class="endcard"><p class="endcard-big">It begins under a lamp.<br>It ends under the city lights.</p>'
          '<p class="endcard-small brand">Brown &amp; Co. Jewelers<br>Buckhead | Roswell</p></div>')

case('brown-co.html', 'Brown &amp; Co.', ['Pitch','Integrated campaign','Concept · Creative Direction · Art Direction'],
     'Love looks different in every light.',
     'From candlelight to city lights, discover the moments your diamond will become part of. <span class="fine">Pitch work for Brown &amp; Co. Jewelers, Buckhead | Roswell. Visuals AI-assisted.</span>',
     'moments:', 'The Moments Lamp',
     [section('01','The insight','', bc_insight),

      section('02','The Lighting Bar','A diamond isn&#39;t just chosen for the moment you buy it. It&#39;s chosen for every moment that follows.',
              '<p class="body-copy section-more">The Lighting Bar brings those moments into the store through the Moments Lamp, a proposed lighting experience inspired by candlelit dinners, quiet mornings, nights out, and celebrations.</p>'
              '<p class="body-copy section-more"><em>One diamond. A lifetime of different lights.</em></p>'
              + rows(('small', [('bc-lamp-instore-v2','A woman studies the round solitaire on her hand beside a brass Moments Lamp on a marble counter; its base is labeled Candlelight, Sunday morning, City lights and Celebration.','')]))),

      section('03','Every light of the season','The season is full of lights that come and go. Some things stay with us long after they&#39;ve been taken down.',
              rows(('small', [('bc-strings','Brown &amp; Co. billboard: String lights come down in January. This doesn&#39;t.','')]))),

      section('04','Your name in lights','Some moments deserve more than candlelight. For the biggest question of all, Brown &amp; Co. takes the experience beyond the showroom and into the Atlanta skyline.',
              rows(('small pair-s', [('bc-reserved','Night billboard, almost entirely empty black, reading This space reserved for her name, with a gold line where a name would go','The invitation.'),
                    ('bc-proposal-night','On a Buckhead rooftop at dusk, a man kneels with a ring as a Brown &amp; Co. billboard over the highway reads Sarah, will you marry me?','The moment.')]))
              + bc_mechanics + bc_end)],
     'fage.html', 'Fage', 'Brown & Co.: Love looks different in every light. A pitch built on the Moments Lamp, ending with her name in lights.')


fage_insight = insight_box('FAGE&#39;s ingredient list is two lines long. So we made it the ad.', 'Nothing to hide.')

case('fage.html', 'Fage', ['Spec','Integrated campaign','Concept · Creative Direction · Art Direction'],
     'Honestly crafted. Nothing to hide.',
     'A spec campaign built on one simple truth: FAGE has almost nothing in it. Milk and live active cultures. The platform takes that honesty literally, from a nearly empty billboard to a live camera inside the factory. Visuals AI-assisted.',
     'fage-blank', 'A huge, almost entirely blank billboard over a New York street, with only a small ingredients label: milk, live active cultures',
     [section('01','The insight','', fage_insight),

      section('02','Out-of-home: the label is the ad','Where other brands fill every inch, FAGE leaves the space empty. The fine print is the whole message.',
              rows([('fage-transparency','Bus shelter with clear glass and the line Full transparency, footnoted: that&#39;s the fine print, milk and live active cultures','Full transparency.*'),
                    ('fage-legal','A newspaper legal notice: Notice of full disclosure. FAGE hereby discloses the complete contents of its yogurt.','Print: a legal notice with nothing to declare.')])),

      section('03','The people behind it','If the yogurt has nothing to hide, neither do the people who make it. Real roles, real standards, named on the poster.',
              rows([('fage-helen','Poster: Produced in a facility with Helen. She&#39;s tasted every batch since 2012 and sent back 412.','Helen.'),
                    ('fage-dave-v2','Poster: Strained until Dave says stop. Dave has never said stop early.','Dave.'),
                    ('fage-mike-v2','Poster: Keep refrigerated. Keep Mike happy. He&#39;s rejected 96 batches for being a little thin.','Mike.')])),

      section('04','Corp-Cam','Live cameras inside the factory, the lab and the break room at fagelivecam.com. Nine feeds, around the clock. Subway posters show what the cameras catch.',
              rows([('fage-corpcam','The Corp-Cam page on a desktop monitor: nine live feeds from milk reception to the loading dock, beside the line Watch us make it. Nothing to hide.','The site.'),
                    ('fage-caught','Subway poster: a security-cam still of a worker sneaking yogurt in the cold room. Caught on Corp-Cam.','Caught on Corp-Cam.')])),

      section('05','Experiential: the confession booth','Then the brand turns the honesty back on the public. Step into the booth, confess a yogurt secret, walk out with free FAGE.',
              rows([('fage-booth','A woman laughs as she leaves the Nothing to Hide confession booth on a New York sidewalk, free yogurt in hand','The booth.'),
                    ('fage-card','A confession card: Ingredients: milk, live active cultures, and a blank line for your secret','The confession card.')])),

      section('06','Packaging and social','The confessions keep going at home. Every lid lists one more ingredient, and #NothingToHide collects the rest.',
              rows([('fage-lids','Three FAGE cups with lids reading Contains: eaten in bed, twice. Double-dipping, no regrets. Straight from the tub at 2am.','Lids: one more ingredient.'),
                    ('fage-social','#NothingToHide on Instagram and Reels: eating it on the fire escape at 2am, not a diet, a lifestyle','#NothingToHide.')])),

      section('07','Experiential: buzz for the truth','A FAGE-branded intercom on a New York brownstone invites passersby to buzz a neighbor and hear their yogurt confession, live. Every conversation ends the same way: &quot;I&#39;ll send some down.&quot;',
              '<div class="g"><div class="g-row">' + buzz_panel()
              + gfig('fage-basket','A neighbor smiles from a brownstone window, lowering a basket of FAGE Total yogurt on a rope to the woman below','A little something from upstairs.')
              + '</div></div>')],
     'uber.html', 'Uber', 'Fage: Honestly crafted. Nothing to hide. A spec campaign that makes the ingredient list the ad.')


dd_end = ('<div class="endcard dd-end">'
          + ('<img class="dd-macro" src="images/dd-macro.jpg" alt="A natural diamond in macro, lit like a specimen in the field" loading="lazy">' if has_img('dd-macro') else '')
          + '<p class="endcard-big">Some things are worth looking for.</p>'
          + '<p class="endcard-small brand">Desert Diamonds · Premier Gem</p></div>')

case('desert-diamonds.html', 'Desert Diamonds', ['Premier Gem','Campaign · Films · Microsite','Concept · Art Direction · Design'],
     'A natural diamond is a rare sighting.',
     'An elusive subject. An obsessive photographer. An increasingly questionable hiding place.',
     'dd-hero', 'A photographer disguised as a lizard watches a woman wearing a diamond ring',
     [section('01','The sighting','', insight_box('The rarer the sighting, the greater the obsession.', 'A natural diamond is a rare sighting.')),

      section('02','The obsession','Field photographers will go anywhere for one glimpse of the real thing. Anywhere.',
              rows([('dd-3-photo','A photographer hides inside a saguaro cactus as a woman adjusts her sunglasses, showing a yellow diamond ring','Observer, concealed in saguaro.'),
                    ('dd-4-photo','A photographer floats in a flamingo pool float, lens aimed at a yellow diamond ring','Observer, afloat.')],
                   [('dd-2','Print ad: A natural diamond is a rare sighting. Grainy night-vision shot of a woman in a gown, her diamond flaring in a hotel corridor','Night shift.')])
              + '<p class="also-label">Also spotted</p>'
              + rows(('small keep', [('dd-1-photo','A photographer hides in a hedge while a woman with a diamond bracelet sits on a desert terrace','Observer, shrubbery.'),
                                ('dd-5-photo','A man at breakfast watches through binoculars beside a woman wearing a diamond pendant','Observer, brunch.')]),
                     ('small keep', [('dd-social-lizard','4:5 social ad: A natural diamond is a rare sighting, the lizard',''),
                                ('dd-social-cactus','4:5 social ad: A natural diamond is a rare sighting, the cactus',''),
                                ('dd-social-pool','4:5 social ad: A natural diamond is a rare sighting, the pool float','Recut 4:5 for the feed.')]))),

      section('03','Caught on camera','Field footage. The stakeout, played completely straight.',
              '<div class="film-lead">' + film('ThePool_DesertRing.mp4','The Pool','dd-film-pool') + '</div>'
              + '<div class="films two">' + film('TheBinoculars.mp4','The Binoculars','dd-film-binoculars') + film('TheSubmarine_DesertPendant.mp4','The Submarine','dd-film-submarine' if has_img('dd-film-submarine') else '') + '</div>'),

      section('04','The expedition','<strong>The rarest sightings weren&#39;t ours to capture.</strong> They were yours.',
              '<p class="body-copy section-more">Rare Sightings, the campaign&#39;s microsite, hands the binoculars to everyone else. Natural diamond owners upload a photo of their own ring, name it and log where it was spotted. Each submission earns an official field report, and the best sightings will be featured in the archive and on Instagram.</p>'
              + rows(('browser', [('dd-site-hero','Rare Sightings homepage: a field desk with binoculars and a note reading Departed on a field expedition to document rare sightings','The researcher has left. The binoculars are yours.')]),
                     ('browser', [('dd-site-sightings','The Recent Sightings archive: numbered field entries for the round, the pear, the oval and the halo, each confirmed','The archive.'),
                                  ('dd-site-reporter','Become a Field Reporter: upload your sighting and receive an official field report','Become a field reporter.')]))
              + '<div class="outlinks"><a class="text-link" href="https://premiergem.com/rare-sightings" target="_blank" rel="noopener">Visit Rare Sightings: premiergem.com/rare-sightings →</a></div>'),

      section('05','The rare thing','', dd_end)],
     'brown-co.html', 'Brown &amp; Co', 'Desert Diamonds: A natural diamond is a rare sighting. Campaign, films and UGC microsite.')

case('uber.html', 'Uber', ['Spec','Integrated campaign','Concept · Creative Direction · Art Direction'],
     'When it&#39;s time to go.',
     'A spec campaign built around the things people say when a good night has gone on a little too long. From bar receipts and coasters to an AI-powered last-call hotline, Uber helps turn the moment into a way home. <span class="fine">Spec work. Visuals AI-assisted.</span>',
     'ub-receipt', 'An itemized bar receipt from the Tipsy Oak: two Old Fashioneds, fries, four OK one more, I&#39;m not even tired, we should start a business, I love you guys. Total: time to go. Close your tab. Open your app. Signed off with the Uber logo.',
     [s_ for s_ in [
      section('01','The insight','', insight_box('Everyone knows the night is over before they admit it. You can hear it.', 'Turn the ridiculous things people say at last call into Uber&#39;s invitation to head home.')),

      section('02','On-premise: the coasters','A coaster series built from the lines everyone has heard at last call. Each one ends the same way.',
              rows(UB_COASTERS[:2], UB_COASTERS[2:])),

      (section('03','Experiential: The Last Call Department','An old payphone appears in neighborhood bars, offering a second opinion on those brilliant ideas that only seem brilliant after midnight. Pick up the receiver and a deadpan AI operator answers. Every conversation is different. Every case has one thing in common: knowing when it&#39;s time to go.',
              '<div class="g"><div class="g-row lc-row">'
              + (gfig('ub-payphone-v3','A vintage black payphone with its receiver hanging, mounted on a dark wood bar wall under a lit brass plaque: The Last Call Department. For great ideas after midnight. Pick up. Share your brilliant idea. We&#39;ll decide if it&#39;s time to go. Uber.','The installation.') if has_img('ub-payphone') else '')
              + f'<figure class="gf" style="--r:{_ratio("ub-payphone-closeup-v2"):.4f}">' + lastcall_panel() + '<figcaption>Pick up the phone. Tap the glowing key.</figcaption></figure>'
              + '</div></div>') if UB_LASTCALL else ''),

      section('04' if UB_LASTCALL else '03','Out-of-home: on the way out','The last word, placed between the bar door and the curb.',
              rows([('ub-sign','A lit sidewalk sign on a rainy nightlife street as a couple walks past, one checking her phone: Last call is a suggestion. Closing time isn&#39;t. When it&#39;s time to go. Uber.','Sidewalk sign.'),
                    ('ub-shelter-goodbye','Bus shelter at night on a wet city street. The poster reads: You&#39;ve been saying goodbye for 45 minutes. When it&#39;s time to go. Uber.','Bus shelter.')])
              + billboard_html()),

      (section('05','The morning after','<span class="proposed">Proposed extension</span> Some brilliant ideas sound different in daylight. Callers who opt in could hear their late-night pitch again the next morning. The Last Call Department keeps the receipts.',
              (rows([('ub-morning','Morning light on a nightstand: a glass of water, keys and a phone on the lock screen showing an Uber notification: Your brilliant idea from last night is ready for review.','The next morning.')]) if has_img('ub-morning') else '')
              + (sample_audio('audio/ub-morning-after.mp3','Sample: a morning-after follow-up') if has_file('audio/ub-morning-after.mp3') else '')) if UB_LASTCALL else ''),
      ] if s_],
     'turbochef.html', 'Turbochef', 'Uber: When it&#39;s time to go. A spec campaign built on the things you say before it&#39;s time to go.')

tc_insight = insight_box('TurboChef builds the ovens restaurants run on. Now there&#39;s one for the home.', 'Compliments to the chef.')

case('turbochef.html', 'TurboChef', ['Spec','Integrated campaign','Concept · Creative Direction · Art Direction'],
     'Compliments to the chef.',
     'A spec campaign for TurboChef&#39;s home ovens: restaurant-grade, home-cooked. Restaurant-grade speed and searing turn ordinary houses into the best restaurants on the block, from rooftop neon to a lawn sign that ships in the box. Visuals AI-assisted.',
     'video:https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/turbochef-homecoorked1.mp4|tc-poster', 'The TurboChef :30 spot: Compliments to the chef',
     [section('01','The insight','', tc_insight),

      section('02','Out-of-home: new restaurants in the neighborhood','Billboards that make you look twice: real homes with restaurant neon on the roof. Every family that owns a TurboChef gets a name in lights.',
              rows([('tc-hendersons','A white colonial home at blue hour with a red neon restaurant sign on the roof: The Hendersons, steak, chops, Sunday roast, open','The Hendersons. Steak, chops, Sunday roast.'),
                    ('tc-dave','A brick ranch house with a giant orange neon sign: Dave Kowalski, est. last Tuesday','Dave Kowalski. Est. last Tuesday.')],
                   [('tc-garcia','A Spanish-style home with a red neon sign: Casa Garcia, now seating','Casa Garcia. Now seating.'),
                    ('tc-barry','A farmhouse with a teal neon sign on the porch: Barry&#39;s Kitchen, reservations recommended','Barry&#39;s Kitchen. Reservations recommended.')])),

      section('03','Social: dinner service at home','Six-second loops for Reels and TikTok, built to land with the sound off. Each one ends on the payoff with the TurboChef lockup over the final frame.',
              '<div class="reels">' + '<figure class="film reel"><button class="reel-btn" aria-label="Play Passed inspection with sound"><video muted loop playsinline autoplay preload="metadata" poster="images/tc-grandma.jpg"><source src="https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/inspection.mp4" type="video/mp4"></video></button><figcaption>Passed inspection.</figcaption></figure>' + '<figure class="film reel"><button class="reel-btn" aria-label="Play Order up with sound"><video muted loop playsinline autoplay preload="metadata" poster="images/tc-tickets.jpg"><source src="https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/orderup.mp4" type="video/mp4"></video></button><figcaption>Order up.</figcaption></figure>' + '<figure class="film reel"><button class="reel-btn" aria-label="Play Service charge not included with sound"><video muted loop playsinline autoplay preload="metadata" poster="images/tc-check.jpg"><source src="https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/service.mp4" type="video/mp4"></video></button><figcaption>Service charge not included.</figcaption></figure>' + '</div>'),

      section('04','In the box: the sign comes with the oven','Every oven ships with a welcome card and a &quot;Now Serving&quot; lawn sign. Buyers put it in the yard, neighbors stop and ask, and the campaign spreads street by street.',
              rows([('tc-unbox','A woman unboxes a TurboChef oven and lifts out an orange Now Serving, reservations recommended lawn sign from the lid; a card reads Congratulations on your new restaurant','Congratulations on your new restaurant.'),
                    ('tc-sign','A Now Serving, reservations recommended lawn sign in front of a home at dusk as a woman walking her dog stops to look','In the yard.')]))],
     'synth-city.html', 'Synth City', 'TurboChef: Compliments to the chef. A spec campaign that turns homes into the best restaurants on the block.')

# ---------- PROPOSALMATIC (interactive Synth City activation) ----------
# A working engagement-ring vending machine from 2187. Markup only; the machine's
# behaviour lives in js/proposalmatic.js and its look in css/proposalmatic.css.
# The ring compartments are a crop of images/synth-vending.jpg (images/pm-display.jpg).
PM_RINGS = {
    'STANDARD': '<circle cx="24" cy="31" r="10.5"/><path d="M19 15.5 24 10l5 5.5-5 6.5z"/><path d="M19 15.5h10"/>',
    'PREMIUM': '<circle cx="24" cy="31" r="10.5"/><path d="M20.6 15.6 24 12l3.4 3.6L24 20z"/><path d="M20.6 15.6h6.8"/><circle cx="24" cy="16" r="7.4" stroke-dasharray="1.1 2.1"/>',
    'FOREVER+': '<circle cx="24" cy="31" r="10.5"/><path d="M20.4 15.2 24 11l3.6 4.2L24 20.4z"/><path d="M20.4 15.2h7.2"/><path d="M12.6 18.6 15 16l2.4 2.6L15 21.6z"/><path d="M30.6 18.6 33 16l2.4 2.6L33 21.6z"/>',
}
PM_PACKAGES = [('STANDARD', 'Standard', 'Approved for everyday commitment.'),
               ('PREMIUM', 'Premium', 'Enhanced emotional signaling.'),
               ('FOREVER+', 'Forever+', 'Auto-renewable devotion.')]
PM_TIMES = [('IMMEDIATELY', 'Immediately'), ('WITHIN 24 HOURS', 'Within 24 hours'), ('WHEN CONVENIENT', 'When convenient')]
PM_RESPONSES = [('ROMANTIC', 'Romantic'), ('ENTHUSIASTIC', 'Enthusiastic'), ('GUARANTEED ACCEPTANCE', 'Guaranteed acceptance')]

def pm_pkg(v, name, line):
    return (f'<label class="pm-pkg"><input type="radio" name="pmPkg" value="{v}">'
            f'<span class="pm-pkg-ring" aria-hidden="true"><svg viewBox="8 6 32 38">{PM_RINGS[v]}</svg></span>'
            f'<span class="pm-pkg-t"><b>{name}</b><span>{line}</span></span><span class="pm-led" aria-hidden="true"></span></label>')

def pm_seg(group, v, label):
    return (f'<label class="pm-seg"><input type="radio" name="{group}" value="{v}">'
            f'<span class="pm-led" aria-hidden="true"></span><span class="pm-seg-t">{label}</span></label>')

pm_cells = ''.join(f'<span class="pm-cell" data-row="{r}" data-col="{c}"><span class="pm-shutter"><span class="pm-sh-t">Retrieving</span><i></i></span></span>'
                   for r in range(3) for c in range(4))

pm_body = f'''<div class="pm" id="pm" data-state="WELCOME">
<section class="pm-stage" aria-labelledby="pmTitle">
<div class="pm-bg" aria-hidden="true"></div>
<div class="wrap pm-top">
<a class="text-link pm-back" href="synth-city.html">← Synth City</a>
<p class="pm-fiction">Fictional interactive campaign · Synth City, 2187 · Nothing is sold</p>
</div>
<h1 id="pmTitle" class="pm-sr">PROPOSALMATIC™: an interactive Synth City campaign experience</h1>
<div class="pm-rig">
<div class="pm-machine" id="pmMachine" data-power="off">
<span class="pm-pillar pm-pillar-l" aria-hidden="true"></span><span class="pm-pillar pm-pillar-r" aria-hidden="true"></span>
<div class="pm-marquee" aria-hidden="true">
<div class="pm-mq-main"><p class="pm-mq-name">PROPOSALMATIC<sup>™</sup></p><span class="pm-mq-rule"></span><p class="pm-mq-line">True love. Now in seconds.</p></div>
<div class="pm-mq-plate"><span class="pm-mq-year">2187</span><span class="pm-mq-unit">Unit PM-07</span></div>
</div>
<div class="pm-body">
<div class="pm-bay">
<div class="pm-display">
<div class="pm-window" aria-hidden="true"><img src="images/pm-display.jpg" alt="" width="801" height="952"><div class="pm-cells">{pm_cells}</div><span class="pm-scanline"></span><span class="pm-dim"></span><span class="pm-glass"></span></div>
<div class="pm-screen" role="region" aria-label="PROPOSALMATIC touchscreen"><span class="pm-scrim pm-scrim-c" aria-hidden="true"></span><span class="pm-scrim pm-scrim-f" aria-hidden="true"></span>
<div class="pm-sbar"><span class="pm-sbar-id" aria-hidden="true">SB · CRD · PM-07</span><span class="pm-pips" aria-hidden="true"><i></i><i></i><i></i><i></i></span><button type="button" class="pm-sound" aria-pressed="false"><span class="pm-sound-ic" aria-hidden="true"></span><span class="pm-sound-t">Sound off</span></button></div>
<div class="pm-views">
<section class="pm-view pm-v-welcome" data-view="WELCOME">
<span class="pm-wring" aria-hidden="true"><svg viewBox="0 0 64 64"><circle cx="32" cy="42" r="15"/><circle cx="32" cy="42" r="12.6" opacity=".45"/><path d="M24.5 21.5 32 13l7.5 8.5L32 31z"/><path d="M24.5 21.5h15M28.5 21.5 32 13l3.5 8.5L32 31"/><path d="M47 12v6M44 15h6M15 26v4M13 28h4" opacity=".7"/></svg></span>
<p class="pm-k">Synthetic Bureau</p>
<h2 class="pm-logo pm-sr" tabindex="-1">PROPOSALMATIC™</h2>
<p class="pm-hl">Love is complicated.<br>We&#39;ve fixed that.</p>
<button type="button" class="pm-btn pm-primary pm-go" data-act="start">Initiate proposal</button>
</section>
<section class="pm-view" data-view="PACKAGE" hidden>
<p class="pm-step">Step 1 of 2</p><h2 class="pm-h" tabindex="-1">Select your commitment package</h2>
<fieldset class="pm-pkgs" data-group="pkg"><legend class="pm-sr">Commitment package</legend>{''.join(pm_pkg(*x) for x in PM_PACKAGES)}</fieldset>
<div class="pm-nav"><button type="button" class="pm-btn pm-ghost" data-act="cancel">Cancel</button><button type="button" class="pm-btn pm-primary" data-act="toConfig" disabled>Continue</button></div>
<p class="pm-fine">All packages are equally unique.</p>
</section>
<section class="pm-view" data-view="CONFIGURATION" hidden>
<p class="pm-step">Step 2 of 2</p><h2 class="pm-h" tabindex="-1">Configure your proposal</h2>
<fieldset class="pm-set" data-group="time"><legend>Desired proposal timeframe</legend><div class="pm-segs">{''.join(pm_seg('pmTime', *x) for x in PM_TIMES)}</div></fieldset>
<fieldset class="pm-set" data-group="resp"><legend>Preferred emotional response</legend><div class="pm-segs">{''.join(pm_seg('pmResp', *x) for x in PM_RESPONSES)}</div></fieldset>
<div class="pm-nav"><button type="button" class="pm-btn pm-ghost" data-act="back">Back</button><button type="button" class="pm-btn pm-primary" data-act="confirm" disabled>Confirm proposal</button></div>
<p class="pm-fine pm-hint">Select one setting in each row.</p>
</section>
<section class="pm-view pm-v-proc pm-v-low" data-view="PROCESSING" hidden>
<h2 class="pm-h" tabindex="-1">Analyzing commitment<span class="pm-ell" aria-hidden="true">...</span></h2>
<div class="pm-bar" aria-hidden="true"><i></i></div>
<ul class="pm-log"></ul>
</section>
<section class="pm-view pm-v-proc" data-view="DISPENSING" hidden>
<p class="pm-step">Proposal approved</p><h2 class="pm-h" tabindex="-1">Dispensing your ring</h2>
<ol class="pm-seq"><li data-k="sel"><span class="pm-led" aria-hidden="true"></span><span><b>Selected</b> Compartment <span data-f="cell"></span></span></li><li data-k="disp"><span class="pm-led" aria-hidden="true"></span><span><b>Dispensed</b> To the collection bay</span></li><li data-k="rep"><span class="pm-led" aria-hidden="true"></span><span><b>Replaced</b> With an identical ring</span></li></ol>
<div class="pm-bar is-run" aria-hidden="true"><i></i></div>
</section>
<section class="pm-view pm-v-low" data-view="RECEIPT" hidden>
<p class="pm-step">Proposal complete</p><h2 class="pm-h" tabindex="-1">Please collect your ring and receipt.</h2>
<p class="pm-sub">Compartment <span data-f="cell"></span> already holds an identical replacement.</p>
<button type="button" class="pm-btn pm-ghost" data-act="viewReceipt">View receipt</button>
</section>
<section class="pm-view pm-v-low" data-view="REVEAL" hidden>
<p class="pm-step">Transaction closed</p><h2 class="pm-h" tabindex="-1">Thank you for choosing efficiency.</h2>
<p class="pm-sub">Ready for the next customer.</p>
<button type="button" class="pm-btn pm-primary" data-act="restart">New proposal</button>
</section>
</div>
</div>
</div>
<div class="pm-sep" aria-hidden="true"><span class="pm-sep-t" data-default="Synthetic Bureau · Certified dispenser · SB-2187-0451">Synthetic Bureau · Certified dispenser · SB-2187-0451</span></div>
<div class="pm-tray" aria-hidden="true"><span class="pm-tray-in"></span><span class="pm-tray-light"></span><span class="pm-box"></span><span class="pm-tray-flap"><span class="pm-tray-label">Collect your ring</span></span></div>
</div>
<div class="pm-printer" aria-hidden="true"><span class="pm-seal"><svg viewBox="0 0 40 40"><path d="M20 3 37 20 20 37 3 20z"/><circle cx="20" cy="20" r="8.5"/><path d="M20 9.5v21M9.5 20h21"/></svg></span><span class="pm-printer-label">Your receipt</span><span class="pm-printer-led"></span><span class="pm-slot"></span></div>
</div>
<div class="pm-plinth" aria-hidden="true"></div>
<p class="pm-sr" aria-live="polite" id="pmLive"></p>
</div>
<div class="pm-below">
<div class="pm-out">
<div class="pm-paper" id="pmPaper">
<article class="pm-receipt" id="pmReceipt" tabindex="-1" aria-label="Your PROPOSALMATIC receipt">
<p class="r-c r-b">Synthetic Bureau</p>
<p class="r-c r-big">PROPOSALMATIC™</p>
<p class="r-c">Cycle 2187</p>
<p class="r-rule"></p>
<p class="r-kv"><span>Order</span><span data-f="no"></span></p>
<p class="r-kv"><span>Issued</span><span data-f="issued"></span></p>
<p class="r-kv"><span>Unit / compartment</span><span>PM-07 / <span data-f="cell"></span></span></p>
<p class="r-rule"></p>
<p class="r-c r-b r-gap">Proposal complete</p>
<p class="r-kv"><span>Package:</span><span data-f="pkg"></span></p>
<p class="r-kv"><span>Emotional response:</span><span data-f="resp"></span></p>
<p class="r-kv"><span>Deployment:</span><span data-f="time"></span></p>
<p class="r-kv"><span>Love:</span><span>Approved</span></p>
<p class="r-kv"><span>Compatibility:</span><span>Optimized</span></p>
<p class="r-kv"><span>Originality:</span><span>0%</span></p>
<p class="r-rule"></p>
<p class="r-c r-lead">Congratulations.</p>
<p class="r-c r-hero">Your ring is identical to <span class="r-num">8,492,611</span> others.</p>
<p class="r-c r-support">The ring of your dreams. And everyone else&#39;s.</p>
<p class="r-rule"></p>
<p class="r-c">Thank you for choosing efficiency.</p>
<svg class="r-code" data-f="bars" viewBox="0 0 200 34" preserveAspectRatio="none" aria-hidden="true"></svg>
<p class="r-c r-fine">Fictional receipt · No purchase made</p>
</article>
</div>
<div class="pm-actions" hidden>
<button type="button" class="pm-act" data-act="save">Save PNG</button>
<button type="button" class="pm-act" data-act="copy">Copy text</button>
<button type="button" class="pm-act" data-act="share">Share</button>
<button type="button" class="pm-act pm-act-ghost" data-act="restart">Start over</button>
</div>
<p class="pm-status" aria-live="polite"></p>
</div>
<div class="pm-reveal" id="pmReveal" hidden>
<p class="pm-rv-a">Everything can be manufactured.</p>
<p class="pm-rv-b">Except rarity.</p>
<p class="pm-rv-brand">Premier Gem</p>
<p class="pm-rv-line">The future didn&#39;t run out of diamonds.<br>It ran out of rarity.</p>
<a class="text-link pm-rv-link" href="synth-city.html">Explore the Synth City campaign →</a>
</div>
</div>
</div>
</section>
<noscript><p class="wrap pm-noscript">PROPOSALMATIC™ needs JavaScript to run. <a href="synth-city.html">Back to Synth City</a>.</p></noscript>
</div>'''

page('proposalmatic.html', 'PROPOSALMATIC™ | Synth City | Asher Wilens',
     'True love. Now in seconds. An interactive Synth City activation for Premier Gem: a 2187 engagement-ring vending machine that dispenses a ring identical to millions of others, then prints the receipt.',
     pm_body, 'work', og='pm-card',
     head_extra=('' if PM_LISTED else '\n<meta name="robots" content="noindex">') + f'\n<link rel="stylesheet" href="css/proposalmatic.css?v={_v("css/proposalmatic.css")}">',
     scripts_extra=f'\n<script src="js/proposalmatic.js?v={_v("js/proposalmatic.js")}" defer></script>')

print('built')
