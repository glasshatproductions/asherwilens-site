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
# Small rotating lines under the wordmark. Edit, add or remove freely.
TAGLINES = [
    'My Middle Name Is Creative. Legally, It Isn&#39;t.',
    'I Put the Art in Artificial.',
    'Always On. Except Shabbos.',
    'AI Can Do a Lot. I Still Have Opinions.',
    'Creative Director. Allegedly.',
]
TAGLINES_HTML = ('<p class="taglines" aria-label="' + ' / '.join(TAGLINES) + '">'
                 + ''.join(f'<span class="tl{" on" if i == 0 else ""}" aria-hidden="true">{t}</span>' for i, t in enumerate(TAGLINES)) + '</p>')

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
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="images/{og}.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Hanken+Grotesk:wght@400;500;600&display=swap">
<link rel="stylesheet" href="css/style.css?v={_v('css/style.css')}">{head_extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="wrap">
<div class="brandline"><a class="wordmark" href="index.html">A. WILENS</a>{TAGLINES_HTML}</div>
<nav class="site-nav" aria-label="Main">
{nav("index.html#work","Work","work")}
{nav("lab.html","Lab","lab")}
{nav("resume.pdf","Résumé","resume")}
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
<span><a href="index.html#work">Work</a> · <a href="lab.html">Lab</a> · <a href="resume.pdf">Résumé</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div>
</footer>
<script src="js/gallery.js?v={_v('js/gallery.js')}"></script>
<script src="js/livephone.js?v={_v('js/livephone.js')}" defer></script>{LASTCALL_TAG if fname == 'uber.html' else ''}{MOMENTS_TAG if fname == 'brown-co.html' else ''}{scripts_extra}
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
    return (f'<div class="insight"><p class="eyebrow">The insight</p><p class="ins-line">{line}</p>'
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
    art = ('<img src="images/ub-payphone-closeup.jpg" alt="The Last Call Department payphone: chrome keypad, black receiver and a plate reading For great ideas after midnight. '
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

# A second image shown directly under a case-study hero (a reveal).
HERO_FOLLOW = {
    'fage-blank': ('fage-closeup', 'Close-up of the billboard&#39;s small label: Ingredients: milk, live active cultures. Honestly crafted. Nothing to hide. FAGE.', 'Read the fine print.'),
}

def case(fname, name, tags, lede, intro, hero, hero_alt, sections, nxt, nxt_name, desc):
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
                     '<p class="trailer-soon" role="status">Trailer coming soon.</p></div>'
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
<nav class="next wrap" aria-label="Next project"><a href="{nxt}"><span class="eyebrow">Next project</span><span class="display">{nxt_name.upper()} →</span></a></nav>'''
    page(fname, f'{name} | A. Wilens', desc, body, 'work')

# ---------- HOME ----------
work = [
    ('synth-city.html','thumb-synth-city','Synth City','Premier Gem','Transmedia brand series: six films, a live site and a working AI tool.'),
    ('desert-diamonds.html','thumb-desert-diamonds','Desert Diamonds','Premier Gem','A natural diamond is a rare sighting. A campaign that grew into a UGC microsite.'),
    ('brown-co.html','thumb-brown-co','Brown &amp; Co.','Pitch','Love looks different in every light: a lamp that shows a diamond in the moments it will live in.'),
    ('fage.html','thumb-fage','Fage','Spec','Nothing to hide: the ingredient list becomes the ad.'),
    ('uber.html','thumb-uber','Uber','Spec','The things you say before it\'s time to go.'),
    ('turbochef.html','thumb-turbochef','Turbochef','Spec','Compliments to the chef: the house becomes the restaurant.'),
]
cards = ''.join(f'''<a class="card" href="{h}"><div class="frame"><img src="images/{im}.jpg" alt="{n} campaign" loading="lazy"></div>
<div class="card-title"><h3>{n}</h3><span class="tag">{t}</span></div><p>{d}</p></a>''' for h, im, n, t, d in work if h != 'synth-city.html')
home = f'''<section class="intro"><div class="wrap">
<p class="eyebrow">Asher Wilens · Creative Director</p>
<p class="lede">The best ads don&#39;t feel like ads.</p>
</div></section>
<div class="wrap">
<a class="feature" href="synth-city.html">
<div class="frame"><img src="images/synth-hero.jpg" alt="Synth City: a crowd presses around a single rough natural diamond in a vitrine while workers sweep piles of synthetic diamonds off the floor"></div>
<div class="feature-meta"><div><p class="eyebrow">Featured · Premier Gem</p><h2>SYNTH CITY</h2></div>
<p>The future made everything available, except rarity. A six-film dystopian series, a live broadcast site and a working AI detector that make the case for natural diamonds.</p></div>
</a>
</div>
<section class="section" id="work"><div class="wrap">
<div class="section-head"><h2 class="display">Work</h2><p class="eyebrow">Spec = self-initiated concept</p></div>
<div class="grid">{cards}</div>
</div></section>
<section class="section lab-teaser"><div class="wrap">
<div class="section-head"><div><p class="eyebrow">Lab</p><h2 class="display">Ideas that didn't fit in a brief.</h2></div><a class="btn" href="lab.html">Visit the Lab</a></div>
<ul class="lab-list">
<li><h3>Draiped</h3><p>An AI creative studio that turns one jewelry product shot into a full launch.</p></li>
<li><h3>Project Orion</h3><p>Projected AR with no headset and no phone. The room becomes the medium.</p></li>
<li><h3>Pinverse Arcade</h3><p>Type a world, play it as pinball. AI-generated tables in seconds.</p></li>
</ul>
</div></section>'''
page('index.html', 'A. Wilens | Creative Director',
     'Asher Wilens, Creative Director. The best ads don&#39;t feel like ads.', home)

# ---------- LAB ----------
projects = [
    ('images/lab-draiped.jpg','A plain uploaded ring photo beside the Draiped on-model result of the same ring','01 · AI creative studio','DRAIPED',
     'AI creative studio for jewelers. Upload a product photo and get campaign-ready assets in minutes: on-model shots, Instagram carousels with copy, web banners for desktop and mobile, and listing images for 1stdibs and Shopify. One product shot becomes a full launch, built by someone who\'s spent years art-directing fine jewelry.',
     '<span>Live</span><a class="text-link" href="https://draiped.com">draiped.com →</a>'),
    ('https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/po_9.png','The Project Orion projector device in a living room','02 · Experiential technology','PROJECT ORION',
     'Projected AR with no headset and no phone. Digital experiences cast directly into physical space, built for retail floors, live events and brand activations where the room itself becomes the medium.',
     '<span>Patented</span><a class="text-link" href="https://patents.google.com/patent/US11127212B1/en">US 11,127,212 →</a>'),
    ('images/lab-pinverse.jpg','The prompt haunted diner on Saturn becoming a playable pinball table on a phone','03 · AI game platform','PINVERSE ARCADE',
     'Type a world, play it as pinball. Pinverse Arcade uses AI to turn any prompt or photo into a playable pinball table in seconds, then lets players share, remix and compete on each other\'s creations. It\'s a game, but it\'s also a creative engine: everyone gets to design the machine.',
     '<span>Live</span><a class="text-link" href="https://pinversearcade.com">pinversearcade.com →</a>'),
    ('https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/hh_promo2.png','A hand pressing the piano keys built into the brim of the Harmony Hat','04 · Wearable music','HARMONY HAT',
     'A collectible hat that plays real synth sounds. Wearable music meets limited-drop culture, built for artist collabs, merch and fan experiences.',
     '<span>On Kickstarter</span><a class="text-link" href="https://www.kickstarter.com/projects/harmonyhat/435543195">View the campaign →</a>'),
    ('https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/slickster_promoneon.png','Slickster day-plan screens on a phone and tablet over a city at night','05 · Product design','SLICKSTER',
     'An automated planning app that turns the chaos of scheduling into a single tap. Product design, UX and brand by A. Wilens.',
     '<span>Live</span><a class="text-link" href="https://slickster.app">slickster.app →</a>'),
]
proj_html = ''.join(f'''<article class="project">
<div class="media"><img src="{src}" alt="{alt}" loading="lazy"></div>
<div class="text"><p class="eyebrow">{eb}</p><h2 class="display">{name}</h2><p class="body-copy">{d}</p><div class="status">{st}</div></div>
</article>''' for src, alt, eb, name, d, st in projects)
lab = f'''<div class="wrap">
<section class="lab-hero">
<div><p class="eyebrow">Inventions, products &amp; platforms</p><h1 class="display">LAB</h1><p class="lede">Ideas that didn't fit in a brief.</p></div>
<p>Some ideas are too big for a campaign, so I build them. These are inventions, products and platforms I've developed on my own. They come from the same instinct that drives my agency work: find the human truth, then make something people want to touch.</p>
</section>
<div>{proj_html}</div>
<div class="callout"><p>Interested in partnering, licensing or building something together?</p><a class="btn" href="mailto:{EMAIL}">Start a conversation</a></div>
</div>'''
page('lab.html', 'Lab | A. Wilens', 'Inventions, products and platforms by Asher Wilens.', lab, 'lab')

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

sc_insight = ('<div class="editorial">'
              '<div class="ed-col"><p class="eyebrow">The insight</p>'
              '<p class="ed-lead">We can manufacture more diamonds than ever.</p>'
              '<p class="ed-body">But what happens to the meaning of something special when everything can be made again?</p></div>'
              '<div class="ed-col"><p class="eyebrow">The idea</p>'
              '<p class="ed-lead">Welcome to 2187.</p>'
              '<p class="ed-body">Diamonds are produced by the ton. Engagement rings come from vending machines. Even love is available on demand.</p>'
              '<p class="ed-kicker">Everything is perfect.<br>Nothing is rare.</p></div></div>')

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

sc_series = ('<a class="series" href="' + PLAYLIST_URL + '" target="_blank" rel="noopener">'
             '<span class="series-img"><img src="images/synth-world.jpg" alt="Bureau Approved billboards selling lab-grown happiness over a crowded plaza at night" loading="lazy">'
             '<span class="series-play" aria-hidden="true"></span></span>'
             '<span class="series-meta"><span class="eyebrow">The series</span>'
             '<span class="series-title">Six episodes. One world.</span>'
             '<span class="series-note">Episodes are released on YouTube as the campaign rolls out.</span>'
             '<span class="btn">Watch the series on YouTube</span></span></a>')

sc_end = ('<div class="endcard nowcard">'
          '<p class="endcard-small">Synthetic diamonds. Synthetic love. Synthetic everything.</p>'
          '<p class="endcard-big">The future didn&#39;t run out of diamonds.<br>It ran out of rarity.</p>'
          '<p class="endcard-small brand">Premier Gem</p>'
          '<p class="endcard-mid">Celebrate what can&#39;t be replicated.</p></div>')

sc_k9 = ('<div class="k9">'
         + img('k9-screens','Across Synth City the Bureau&#39;s giant screens glitch as the geologist&#39;s face breaks through the broadcast, a crowd in the plaza stopping to look up','The network, interrupted.')
         + img('k9-geologist','Low-light camera feed GEO-09: a geologist in a headlamp holds up a rough natural diamond, signal unstable, status critical','The thing that wasn&#39;t supposed to exist.')
         + img('k9-scan','Synthetic Compliance Bureau scan: Natural origin detected. File K-9, unauthorized. Registry status: not found. Handling protocol: immediate seizure.','The Bureau&#39;s verdict.')
         + '<div class="outlinks"><a class="text-link" href="https://synthcity.tv/kalahari">Follow the transmission: synthcity.tv/kalahari →</a></div>'
         + '<div class="intercept"><p class="eyebrow">Optional · intercepted from 2187</p>'
         + '<p class="intercept-title">Answer the transmission</p>'
         + '<p class="intercept-note">The campaign&#39;s live site opens on an incoming call. A recorded voice, not a live person. Answer it if you like.</p>'
         + live_phone('https://synthcity.tv/') + '</div></div>')

case('synth-city.html', 'Synth City', ['Premier Gem','Integrated campaign · Soft launch 2026','Creative Direction · Concept · Art Direction'],
     'The future didn&#39;t run out of diamonds. It ran out of rarity.',
     'An alternate-future campaign for Premier Gem. Six cinematic films, a government-controlled broadcast network and interactive experiences exploring a world where everything can be manufactured. Except rarity. <span class="fine">Soft-launched in 2026; the full rollout is in development.</span>',
     'trailer:' + TRAILER_URL + '|synth-poster', 'Synth City campaign trailer',
     [section('01','The insight','', sc_insight),

      section('02','The world','<strong>Welcome to the perfect future.</strong> In 2187, diamonds are unlimited, happiness is optimized and authenticity has become an inconvenience.',
              '<div class="stack">' + img('synth-aerial','Aerial view of Synth City at night: flying cars, neon towers and a Welcome to Synth City sign','Cycle 2187.')
              + '<div class="pair">' + img('synth-factory-line','Robotic nozzles drop cut diamonds by the hundreds onto a factory conveyor','Diamonds, by the ton.')
              + img('synth-vending','A proposal kit vending machine in a 2187 airport terminal','Proposals, to go.') + '</div>'
              + '<div class="narrow">' + img('synth-protocol','Bureau poster of a smiling couple in gloves showing matching rings: Love is a protocol. Bureau approved compatibility.','Love, pre-approved.') + '</div></div>'),

      section('03','The campaign','Every piece hands off to the next. A viewer can enter anywhere; the path always ends with something real.',
              sc_path
              + beat('The Synthetic Bureau','It controls the story.',
                     'The machinery of a society devoted to manufactured perfection: a news network, public broadcasts and one message repeated until it sticks. Synthetic is better.',
                     img('synth-hq','The Synthetic Bureau headquarters, a brutalist monolith with a wireframe-head seal, citizens queuing beneath drones','The Bureau.')
                     + img('synth-broadcast','The SCB7 news network site: Bureau classifies global synthetic diamond oversupply as economic success','The network, live at synthcity.tv.')
                     + img('scfn-newsroom','A financial news anchor in front of a market wall: natural diamond values surpass Manhattan real estate per gram','Natural, now priced per gram.')
                     + img('scfn-street','The same market update on a giant screen over a rainy Fifth Avenue in 2187','The story everyone stops for.')
                     + '<div class="outlinks"><a class="text-link" href="https://synthcity.tv">Watch the broadcasts: synthcity.tv →</a></div>')
              + beat('The Rarity Detector','It erases the original.',
                     'A working, AI-powered classification tool inside the campaign universe. Upload anything and the Bureau rates how rare it will be in 2187. Natural stones come back flagged as anomalies.',
                     img('synth-detector','Four screens of the Rarity Detector: load a specimen, analyzing material, scan complete, signal detected')
                     + img('det-dollar','Detector result: a dollar bill classified as obsolete physical tender','A visitor&#39;s dollar bill: obsolete.')
                     + img('det-mouse','Detector result: a wireless mouse classified as an obsolete peripheral','A visitor&#39;s mouse: obsolete.')
                     + '<p class="disclaimer">A fictional classification for the story, not a scientific method of verifying a diamond&#39;s origin.</p>'
                     + '<div class="outlinks"><a class="text-link" href="https://raritydetector.com">Try it: raritydetector.com →</a></div>')
              + beat('Synth-Mates','It replaces love.',
                     'If diamonds can be manufactured, why stop there? The Bureau now manufactures the people we fall in love with, then sells them like a 1950s dream.',
                     img('sm-chambers-1950s','A 1950s couple in pink and tan, glossy and doll-like, stand in two glass growth chambers in an endless hall of chambers','Grown to order.')
                     + img('sm-showroom','A smiling salesman presents rows of glass chambers holding synthetic bodies','The showroom.')
                     + img('sm2-clonesworths-wide','A glossy 1950s couple wave beside a sign reading Meet the Clonesworths, a pink car and a mint-green house behind them','Meet the Clonesworths.')
                     + img('sm2-dinner','The synthetic couple at a candlelit dinner in a 1950s kitchen','Dinner at six. Every night.')
                     + '<div class="outlinks"><a class="text-link" href="https://syntheticbureau.com" target="_blank" rel="noopener">Enter the lab: syntheticbureau.com →</a></div>')
              + (sc_pm if PM_LISTED else '')),

      section('04','The films','<strong>Six stories. One synthetic future.</strong> Six interconnected cinematic stories explore what happens to love, identity and meaning in a world where nothing is rare. The trailer opens the door.',
              sc_series),

      section('05','File K-9. The last transmission.','The Bureau promised a world without rarity. Then an unauthorized transmission interrupted the network. Deep beneath the Kalahari Basin, a lone geologist had discovered something that wasn&#39;t supposed to exist.',
              sc_k9).replace('<section class="cs-section">','<section class="cs-section cs-dark">',1),

      section('06','Back to now','',
              '<div class="now">' + img('synth-now','Present day: a woman&#39;s hand with a natural diamond engagement ring resting on a sunlit kitchen table beside a coffee cup') + sc_end + '</div>')],
     'desert-diamonds.html', 'Desert Diamonds', 'Synth City: the future didn&#39;t run out of diamonds. It ran out of rarity. An integrated campaign for Premier Gem.')


MOMENTS_TAG = f'\n<script src="js/moments.js?v={_v("js/moments.js")}" defer></script>'

bc_insight = insight_box('Jewelry is chosen under showroom lights. It&#39;s worn under every other kind.', 'Bring the lights of real life into the showroom.')

# The Moments Lamp hero: four matching photographs, one shown at a time.
BC_MODES = [
    ('candlelight', 'Candlelight', 'The intimacy of two.', 'Under the Moments Lamp set to candlelight, a round solitaire glows warm gold on a dark velvet stand.'),
    ('sunday', 'Sunday morning', 'The quiet beauty of an ordinary morning.', 'Under the Moments Lamp set to Sunday morning, the same solitaire reads crisp and soft-white in pale daylight.'),
    ('city', 'City lights', 'A night out, somewhere unforgettable.', 'Under the Moments Lamp set to city lights, the solitaire flashes cool blue against a night-blue background.'),
    ('celebration', 'Celebration', 'The moments worth raising a glass to.', 'Under the Moments Lamp set to celebration, the solitaire throws warm sparks against pink and violet party lights.'),
]

def moments_hero():
    imgs = ''.join(
        f'<img src="images/bc-lamp-{k}.jpg" alt="{alt}" width="1532" height="1020" class="ml-img{" on" if i == 0 else ""}" data-mode="{k}"'
        + (' fetchpriority="high"' if i == 0 else ' loading="eager" fetchpriority="low" decoding="async"') + (' aria-hidden="true"' if i else '') + '>'
        for i, (k, _, _, alt) in enumerate(BC_MODES))
    btns = ''.join(
        f'<button type="button" class="ml-btn" data-mode="{k}" data-copy="{copy}" aria-pressed="{"true" if i == 0 else "false"}">{label}</button>'
        for i, (k, label, copy, _) in enumerate(BC_MODES))
    return ('<div class="wrap moments"><div class="ml-frame">' + imgs + '</div>'
            f'<div class="ml-controls" role="group" aria-label="Moments Lamp lighting">{btns}</div>'
            f'<p class="ml-copy" aria-live="polite">{BC_MODES[0][2]}</p>'
            '<p class="ml-note">The Moments Lamp: a proposed in-store lighting experience. Choose a light.</p></div>')

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
              + img('bc-lamp-instore','A woman studies the round solitaire on her hand beside a brass Moments Lamp on a marble counter; its base is labeled Candlelight, Sunday morning, City lights and Celebration.')),

      section('03','Every light of the season','The season is full of lights that come and go. Some things stay with us long after they&#39;ve been taken down.',
              img('bc-strings','Brown &amp; Co. billboard: String lights come down in January. This doesn&#39;t.')),

      section('04','Your name in lights','Some moments deserve more than candlelight. For the biggest question of all, Brown &amp; Co. takes the experience beyond the showroom and into the Atlanta skyline.',
              '<div class="stack sequence">' + img('bc-reserved','Night billboard, almost entirely empty black, reading This space reserved for her name, with a gold line where a name would go','The invitation.')
              + img('bc-proposal-night','On a Buckhead rooftop at dusk, a man kneels with a ring as a Brown &amp; Co. billboard over the highway reads Sarah, will you marry me?','The moment.')
              + '</div>' + bc_mechanics + bc_end)],
     'fage.html', 'Fage', 'Brown & Co.: Love looks different in every light. A pitch built on the Moments Lamp, ending with her name in lights.')


fage_insight = insight_box('FAGE&#39;s ingredient list is two lines long. So we made it the ad.', 'Nothing to hide.')

case('fage.html', 'Fage', ['Spec','Integrated campaign','Concept · Creative Direction · Art Direction'],
     'Honestly crafted. Nothing to hide.',
     'A spec campaign built on one simple truth: FAGE has almost nothing in it. Milk and live active cultures. The platform takes that honesty literally, from a nearly empty billboard to a live camera inside the factory. Visuals AI-assisted.',
     'fage-blank', 'A huge, almost entirely blank billboard over a New York street, with only a small ingredients label: milk, live active cultures',
     [section('01','The insight','', fage_insight),

      section('02','Out-of-home: the label is the ad','Where other brands fill every inch, FAGE leaves the space empty. The fine print is the whole message.',
              img('fage-transparency','Bus shelter with clear glass and the line Full transparency, footnoted: that&#39;s the fine print, milk and live active cultures','Full transparency.*')
              + img('fage-legal','A newspaper legal notice: Notice of full disclosure. FAGE hereby discloses the complete contents of its yogurt.','Print: a legal notice with nothing to declare.')),

      section('03','The people behind it','If the yogurt has nothing to hide, neither do the people who make it. Real roles, real standards, named on the poster.',
              img('fage-helen','Poster: Produced in a facility with Helen. She&#39;s tasted every batch since 2012 and sent back 412.')
              + img('fage-dave','Poster: Strained until Dave says stop. Dave has never said stop early.')
              + img('fage-mike','Poster: Keep refrigerated. Keep Mike happy. He&#39;s rejected 96 batches for being a little thin.')),

      section('04','Corp-Cam','Live cameras inside the factory, the lab and the break room at fagelivecam.com. Nine feeds, around the clock. Subway posters show what the cameras catch.',
              img('fage-corpcam','The Corp-Cam page on a desktop monitor: nine live feeds from milk reception to the loading dock, beside the line Watch us make it. Nothing to hide.')
              + img('fage-caught','Subway poster: a security-cam still of a worker sneaking yogurt in the cold room. Caught on Corp-Cam.','Caught on Corp-Cam.')),

      section('05','Experiential: the confession booth','Then the brand turns the honesty back on the public. Step into the booth, confess a yogurt secret, walk out with free FAGE.',
              img('fage-booth','A woman laughs as she leaves the Nothing to Hide confession booth on a New York sidewalk, free yogurt in hand')
              + img('fage-card','A confession card: Ingredients: milk, live active cultures, and a blank line for your secret','The confession card.')),

      section('06','Packaging and social','The confessions keep going at home. Every lid lists one more ingredient, and #NothingToHide collects the rest.',
              img('fage-lids','Three FAGE cups with lids reading Contains: eaten in bed, twice. Double-dipping, no regrets. Straight from the tub at 2am.','Lids: one more ingredient.')
              + img('fage-social','#NothingToHide on Instagram and Reels: eating it on the fire escape at 2am, not a diet, a lifestyle','#NothingToHide.')),

      section('07','Experiential: buzz for the truth','A FAGE-branded intercom on a New York brownstone invites passersby to buzz a neighbor and hear their yogurt confession, live. Every conversation ends the same way: &quot;I&#39;ll send some down.&quot;',
              img('fage-buzz','A woman presses a buzzer on a brass intercom under a sign reading Buzz for the truth. Everyone here has a yogurt secret. Go on. Buzz someone.','Buzz for the truth.')
              + img('fage-basket','A neighbor smiles from a brownstone window, lowering a basket of FAGE Total yogurt on a rope to the woman below','A little something from upstairs.'))],
     'uber.html', 'Uber', 'Fage: Honestly crafted. Nothing to hide. A spec campaign that makes the ingredient list the ad.')


case('desert-diamonds.html', 'Desert Diamonds', ['Premier Gem','Campaign · Films · Microsite','Concept · Art Direction · Design'],
     'A natural diamond is a rare sighting.',
     'Treat a natural diamond like the rarest creature in the desert. The campaign starts with paparazzi going to absurd lengths, hiding in cacti, shrubs and pool floats, for a single glimpse of the real thing. Then it hands the binoculars to everyone else: a microsite and social program where real people document their own rare sightings.',
     'dd-hero', 'A photographer disguised as a lizard watches a woman wearing a diamond ring',
     [section('01','The insight','', insight_box('People will go to absurd lengths to glimpse something truly rare. A natural diamond deserves that kind of attention.', 'A natural diamond is a rare sighting.')),
      section('02','The campaign','Print and social executions that cast natural diamonds as a rare species and the people hunting them as obsessive field photographers.',
              '<div class="stack">' + img('dd-1','A photographer hides in a hedge while a woman with a diamond bracelet sits on a desert terrace') + '<div class="pair">' + img('dd-3-photo','A photographer hides inside a saguaro cactus as a woman adjusts her sunglasses, showing a yellow diamond ring','The cactus.') + img('dd-4-photo','A photographer floats in a flamingo pool float, lens aimed at a yellow diamond ring','The pool float.') + '</div>' + '<div class="pair">' + img('dd-5-photo','A man at breakfast watches through binoculars beside a woman wearing a diamond pendant','The binoculars.') + img('dd-2-photo','Grainy night-vision shot of a woman in a gown, her diamond flaring in a hotel corridor','Night vision.') + '</div></div>'),
      section('03','Social: built for the feed','The same series recut for Instagram and mobile: 4:5 frames, the line set large enough to read in a scroll, and the photographer right in the middle of the shot.',
              '<div class="feed">' + img('dd-social-lizard','4:5 social ad: A natural diamond is a rare sighting, the lizard','The lizard.') + img('dd-social-hedge','4:5 social ad: A natural diamond is a rare sighting, the hedge','The hedge.') + img('dd-social-cactus','4:5 social ad: A natural diamond is a rare sighting, the cactus','The cactus.') + img('dd-social-pool','4:5 social ad: A natural diamond is a rare sighting, the pool float','The pool float.') + img('dd-social-binoculars','4:5 social ad: A natural diamond is a rare sighting, the binoculars','The binoculars.') + img('dd-social-nightvision','4:5 social ad: A natural diamond is a rare sighting, night vision','Night vision.') + '</div>'),
      section('04','The films','Short films that play the stakeout for laughs: the long lens, the binoculars, the paparazzo who will go anywhere, even underwater, for one glimpse of the real thing.',
              '<div class="films">' + film('TheBinoculars.mp4','The Binoculars','dd-film-binoculars') + film('ThePool_DesertRing.mp4','The Pool','dd-film-pool') + film('TheSubmarine_DesertPendant.mp4','The Submarine','') + '</div>'),
      section('05','The microsite: Rare Sightings','The campaign lands on a field expedition. The researcher has left; the notes, maps and binoculars are waiting for you.',
              img('dd-site-hero','Rare Sightings homepage: a field desk with binoculars and a note reading Departed on a field expedition to document rare sightings')),
      section('06','The archive','Every ring becomes a numbered field entry, logged by location and date and classified by species: the round, the pear, the oval, the halo. Each one confirmed.',
              img('dd-site-sightings','Recent Sightings archive cards')),
      section('07','The field reporter program','Owners upload a photo or video of their own ring, name it and say where it was spotted. They get an official field report back, and the best sightings are featured in the archive and on Instagram. The audience becomes the content engine.',
              img('dd-site-reporter','Become a Field Reporter upload section')),
      section('08','The full experience','From expedition to field guide to available stones: one page that moves from story to shopping without breaking character.',
              '<div style="max-width:620px;margin:0 auto">' + img('dd-site-full','Full Rare Sightings microsite design') + '</div>' + '<div class="outlinks"><a class="text-link" href="https://premiergem.com/rare-sightings" target="_blank" rel="noopener">Visit Rare Sightings: premiergem.com/rare-sightings →</a></div>')],
     'brown-co.html', 'Brown &amp; Co', 'Desert Diamonds: A natural diamond is a rare sighting. Campaign, films and UGC microsite.')

case('uber.html', 'Uber', ['Spec','Integrated campaign','Concept · Creative Direction · Art Direction'],
     'When it&#39;s time to go.',
     'A spec campaign built around the things people say when a good night has gone on a little too long. From bar receipts and coasters to an AI-powered last-call hotline, Uber helps turn the moment into a way home. <span class="fine">Spec work. Visuals AI-assisted.</span>',
     'ub-receipt', 'An itemized bar receipt from the Tipsy Oak: two Old Fashioneds, fries, four OK one more, I&#39;m not even tired, we should start a business, I love you guys. Total: time to go. Close your tab. Open your app. Signed off with the Uber logo.',
     [s_ for s_ in [
      section('01','The insight','', insight_box('Everyone knows the night is over before they admit it. You can hear it.', 'The things you say before it&#39;s time to go.')),

      section('02','On-premise: the coasters','A coaster series built from the lines everyone has heard at last call. Each one ends the same way.',
              ''.join(img(f, alt, cap) for f, alt, cap in UB_COASTERS)),

      (section('03','Experiential: The Last Call Department','An old payphone appears in neighborhood bars, offering a second opinion on those brilliant ideas that only seem brilliant after midnight. Pick up the receiver and a deadpan AI operator answers. Every conversation is different. Every case has one thing in common: knowing when it&#39;s time to go.',
              (img('ub-payphone','A vintage payphone on a dark wood bar wall under a brass plaque: The Last Call Department. For great ideas after midnight. Pick up. Share your brilliant idea. We&#39;ll decide if it&#39;s time to go. Uber.','The installation.') if has_img('ub-payphone') else '')
              + lastcall_panel()) if UB_LASTCALL else ''),

      section('04' if UB_LASTCALL else '03','Out-of-home: on the way out','The last word, placed between the bar door and the curb.',
              ('<div class="feed tall9">' if not has_img('ub-billboard-clean') else '<div class="feed tall9 two">')
              + img('ub-sign','A lit sidewalk sign on a rainy nightlife street as a couple walks past, one checking her phone: Last call is a suggestion. Closing time isn&#39;t. When it&#39;s time to go. Uber.','Sidewalk sign.')
              + (img('ub-shelter-goodbye','Bus shelter at night on a wet city street. The poster reads: You&#39;ve been saying goodbye for 45 minutes. When it&#39;s time to go. Uber.','Bus shelter.') if has_img('ub-shelter-goodbye') else img('ub-shelter','Bus shelter: Your tab closed at 1:52. Your ride&#39;s here at 1:55.','Bus shelter.'))
              + (billboard_html() if not has_img('ub-billboard-clean') else '') + '</div>'
              + (billboard_html() if has_img('ub-billboard-clean') else '')),

      (section('05','The morning after','<span class="proposed">Proposed extension</span> Some brilliant ideas sound different in daylight. Callers who opt in could hear their late-night pitch again the next morning. The Last Call Department keeps the receipts.',
              (img('ub-morning','Morning light on a nightstand: a glass of water, keys and a phone on the lock screen showing an Uber notification: Your brilliant idea from last night is ready for review.','The next morning.') if has_img('ub-morning') else '')
              + (sample_audio('audio/ub-morning-after.mp3','Sample: a morning-after follow-up') if has_file('audio/ub-morning-after.mp3') else '')) if UB_LASTCALL else ''),
      ] if s_],
     'turbochef.html', 'Turbochef', 'Uber: When it&#39;s time to go. A spec campaign built on the things you say before it&#39;s time to go.')

tc_insight = insight_box('TurboChef builds the ovens restaurants run on. Now there&#39;s one for the home.', 'Compliments to the chef.')

case('turbochef.html', 'Turbochef', ['Spec','Integrated campaign','Concept · Creative Direction · Art Direction'],
     'Compliments to the chef.',
     'A spec campaign for TurboChef&#39;s home ovens: restaurant-grade, home-cooked. Restaurant-grade speed and searing turn ordinary houses into the best restaurants on the block, from rooftop neon to a lawn sign that ships in the box. Visuals AI-assisted.',
     'video:https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/turbochef-homecoorked1.mp4|tc-poster', 'The TurboChef :30 spot: Compliments to the chef',
     [section('01','The insight','', tc_insight),

      section('02','Out-of-home: new restaurants in the neighborhood','Billboards that make you look twice: real homes with restaurant neon on the roof. Every family that owns a TurboChef gets a name in lights.',
              img('tc-hendersons','A white colonial home at blue hour with a red neon restaurant sign on the roof: The Hendersons, steak, chops, Sunday roast, open','The Hendersons. Steak, chops, Sunday roast.')
              + img('tc-dave','A brick ranch house with a giant orange neon sign: Dave Kowalski, est. last Tuesday','Dave Kowalski. Est. last Tuesday.')
              + img('tc-garcia','A Spanish-style home with a red neon sign: Casa Garcia, now seating','Casa Garcia. Now seating.')
              + img('tc-barry','A farmhouse with a teal neon sign on the porch: Barry&#39;s Kitchen, reservations recommended','Barry&#39;s Kitchen. Reservations recommended.')),

      section('03','Social: dinner service at home','Six-second loops for Reels and TikTok, built to land with the sound off. Each one ends on the payoff with the TurboChef lockup over the final frame.',
              '<div class="reels">' + '<figure class="film reel"><button class="reel-btn" aria-label="Play Passed inspection with sound"><video muted loop playsinline autoplay preload="metadata" poster="images/tc-grandma.jpg"><source src="https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/inspection.mp4" type="video/mp4"></video></button><figcaption>Passed inspection.</figcaption></figure>' + '<figure class="film reel"><button class="reel-btn" aria-label="Play Order up with sound"><video muted loop playsinline autoplay preload="metadata" poster="images/tc-tickets.jpg"><source src="https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/orderup.mp4" type="video/mp4"></video></button><figcaption>Order up.</figcaption></figure>' + '<figure class="film reel"><button class="reel-btn" aria-label="Play Service charge not included with sound"><video muted loop playsinline autoplay preload="metadata" poster="images/tc-check.jpg"><source src="https://superborn-dev.s3.us-east-1.amazonaws.com/Portfolio/service.mp4" type="video/mp4"></video></button><figcaption>Service charge not included.</figcaption></figure>' + '</div>'),

      section('04','In the box: the sign comes with the oven','Every oven ships with a welcome card and a &quot;Now Serving&quot; lawn sign. Buyers put it in the yard, neighbors stop and ask, and the campaign spreads street by street.',
              img('tc-unbox','A woman unboxes a TurboChef oven and lifts out an orange Now Serving, reservations recommended lawn sign from the lid; a card reads Congratulations on your new restaurant','Congratulations on your new restaurant.')
              + img('tc-sign','A Now Serving, reservations recommended lawn sign in front of a home at dusk as a woman walking her dog stops to look','In the yard.'))],
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

pm_cells = ''.join(f'<span class="pm-cell" data-row="{r}" data-col="{c}"><span class="pm-shutter"><span class="pm-sh-t">Dispensing</span><i></i></span></span>'
                   for r in range(3) for c in range(4))

pm_body = f'''<div class="pm" id="pm" data-state="WELCOME">
<section class="pm-stage" aria-labelledby="pmTitle">
<div class="pm-bg" aria-hidden="true"></div>
<div class="wrap pm-top">
<a class="text-link pm-back" href="synth-city.html#proposalmatic">← Synth City</a>
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
<div class="pm-bay" aria-hidden="true">
<div class="pm-display">
<div class="pm-chute"><span class="pm-chute-leds"></span><span class="pm-port" data-row="0"></span><span class="pm-port" data-row="1"></span><span class="pm-port" data-row="2"></span><span class="pm-lift"></span><span class="pm-chute-glass"></span></div>
<div class="pm-window"><img src="images/pm-display.jpg" alt="" width="452" height="552"><div class="pm-cells">{pm_cells}</div><span class="pm-scanline"></span><span class="pm-dim"></span><span class="pm-glass"></span></div>
</div>
<div class="pm-sep"><span>Synthetic Bureau · Certified dispenser · SB-2187-0451</span></div>
<div class="pm-tray"><span class="pm-tray-in"></span><span class="pm-tray-light"></span><span class="pm-tray-flap"><span class="pm-tray-label">Collect your ring</span></span></div>
<span class="pm-box"><span class="pm-box-lid"></span><span class="pm-box-mark"></span></span>
</div>
<div class="pm-screen" role="region" aria-label="PROPOSALMATIC touchscreen">
<div class="pm-sbar"><span class="pm-sbar-id" aria-hidden="true">SB · CRD · PM-07</span><span class="pm-pips" aria-hidden="true"><i></i><i></i><i></i><i></i></span><button type="button" class="pm-sound" aria-pressed="false"><span class="pm-sound-ic" aria-hidden="true"></span><span class="pm-sound-t">Sound off</span></button></div>
<div class="pm-views">
<section class="pm-view pm-v-welcome" data-view="WELCOME">
<p class="pm-k">Synthetic Bureau</p><p class="pm-k2">Consumer Relationship Division</p>
<span class="pm-wring" aria-hidden="true"><svg viewBox="0 0 64 64"><circle cx="32" cy="42" r="15"/><circle cx="32" cy="42" r="12.6" opacity=".45"/><path d="M24.5 21.5 32 13l7.5 8.5L32 31z"/><path d="M24.5 21.5h15M28.5 21.5 32 13l3.5 8.5L32 31"/><path d="M47 12v6M44 15h6M15 26v4M13 28h4" opacity=".7"/></svg></span>
<h2 class="pm-logo" tabindex="-1">PROPOSALMATIC<sup>™</sup></h2>
<p class="pm-hl">Love is complicated. We&#39;ve fixed that.</p>
<button type="button" class="pm-btn pm-primary" data-act="start">Initiate proposal</button>
<p class="pm-fine">Average completion time: 24 seconds.</p>
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
<section class="pm-view pm-v-proc" data-view="PROCESSING" hidden>
<h2 class="pm-h" tabindex="-1">Analyzing commitment<span class="pm-ell" aria-hidden="true">...</span></h2>
<div class="pm-bar" aria-hidden="true"><i></i></div>
<ul class="pm-log"></ul>
</section>
<section class="pm-view pm-v-proc" data-view="DISPENSING" hidden>
<p class="pm-step">Proposal approved</p><h2 class="pm-h" tabindex="-1">Dispensing your ring</h2>
<ol class="pm-seq"><li data-k="sel"><span class="pm-led" aria-hidden="true"></span><span><b>Selected</b> Compartment <span data-f="cell"></span></span></li><li data-k="disp"><span class="pm-led" aria-hidden="true"></span><span><b>Dispensed</b> To the collection bay</span></li><li data-k="rep"><span class="pm-led" aria-hidden="true"></span><span><b>Replaced</b> With an identical ring</span></li></ol>
<div class="pm-bar is-run" aria-hidden="true"><i></i></div>
</section>
<section class="pm-view" data-view="RECEIPT" hidden>
<p class="pm-step">Proposal complete</p><h2 class="pm-h" tabindex="-1">Please collect your ring and receipt.</h2>
<p class="pm-sub">Compartment <span data-f="cell"></span> already holds an identical replacement.</p>
<button type="button" class="pm-btn pm-ghost" data-act="viewReceipt">View receipt</button>
</section>
<section class="pm-view" data-view="REVEAL" hidden>
<p class="pm-step">Transaction closed</p><h2 class="pm-h" tabindex="-1">Thank you for choosing efficiency.</h2>
<p class="pm-sub">Ready for the next customer.</p>
<button type="button" class="pm-btn pm-primary" data-act="restart">New proposal</button>
</section>
</div>
<p class="pm-sr" aria-live="polite" id="pmLive"></p>
</div>
<div class="pm-ctrl" aria-hidden="true">
<span class="pm-seal"><svg viewBox="0 0 40 40"><path d="M20 3 37 20 20 37 3 20z"/><circle cx="20" cy="20" r="8.5"/><path d="M20 9.5v21M9.5 20h21"/></svg><span>Synthetic Bureau</span></span>
<span class="pm-grille"></span>
<span class="pm-plate">Love is a protocol</span>
<span class="pm-sticker">Inspected<br>Cycle 2187 ✓</span>
<span class="pm-plate pm-plate-sm">Do not rock or tilt</span>
</div>
<div class="pm-printer" aria-hidden="true"><span class="pm-printer-label">Your receipt</span><span class="pm-printer-led"></span><span class="pm-slot"></span></div>
</div>
<div class="pm-plinth" aria-hidden="true"></div>
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

page('proposalmatic.html', 'PROPOSALMATIC™ | Synth City | A. Wilens',
     'True love. Now in seconds. An interactive Synth City activation for Premier Gem: a 2187 engagement-ring vending machine that dispenses a ring identical to millions of others, then prints the receipt.',
     pm_body, 'work', og='pm-card',
     head_extra=('' if PM_LISTED else '\n<meta name="robots" content="noindex">') + f'\n<link rel="stylesheet" href="css/proposalmatic.css?v={_v("css/proposalmatic.css")}">',
     scripts_extra=f'\n<script src="js/proposalmatic.js?v={_v("js/proposalmatic.js")}" defer></script>')

print('built')
