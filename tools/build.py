import pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent
EMAIL = 'ashwilens@gmail.com'

import hashlib as _h, os as _o
def _v(path):
    try: return _h.md5(open(_o.path.join(_o.path.dirname(__file__),'..',path),'rb').read()).hexdigest()[:8]
    except Exception: return '1'
ASSET_V=True

def page(fname, title, desc, body, current=''):
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
<meta property="og:image" content="images/thumb-synth-city.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Hanken+Grotesk:wght@400;500;600&display=swap">
<link rel="stylesheet" href="css/style.css?v={_v('css/style.css')}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="wrap">
<a class="wordmark" href="index.html">A. WILENS</a>
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
<script src="js/livephone.js?v={_v('js/livephone.js')}" defer></script>
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
            '<p class="live-phone-note">Live, not a recording. Tap Accept, sound on. <button class="live-phone-reload" type="button">Restart ↻</button></p></div>')

def case(fname, name, tags, lede, intro, hero, hero_alt, sections, nxt, nxt_name, desc):
    split = ''
    phone_open = ''
    if hero.startswith('phone:'):
        src, himg, hcap = hero[6:].split('|')
        hero_html = (f'<div class="wrap cs-hero"><figure><img src="images/{himg}.jpg" alt="{hero_alt}"><figcaption>{hcap}</figcaption></figure></div>'
                     f'<div class="wrap cs-open"><p class="body-copy">{intro}</p>'
                     '<p class="answer-prompt">How do we know? <span>Answer the call below to find out</span></p>'
                     f'{live_phone(src)}</div>')
        phone_open = 'yes'
    elif hero.startswith('video:'):
        src, poster = hero[6:].split('|')
        hero_html = f'<div class="wrap cs-hero"><div class="video-embed"><video controls playsinline preload="metadata" poster="images/{poster}.jpg" aria-label="{hero_alt}"><source src="{src}" type="video/mp4">Your browser does not support video.</video></div></div>'
    else:
        hero_html = f'<div class="wrap cs-hero"><img src="images/{hero}.jpg" alt="{hero_alt}"></div>'
    tag_html = ''.join(f'<span class="tag{" solid" if i==0 else ""}">{t}</span>' for i, t in enumerate(tags))
    head_text = f'''<a class="text-link back" href="index.html#work">← All work</a>
<div class="cs-meta">{tag_html}</div>
<h1 class="display">{name.upper()}</h1>
<p class="lede">{lede}</p>''' + ('' if phone_open else f'<p class="body-copy">{intro}</p>')
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
    ('brown-co.html','thumb-brown-co','Brown &amp; Co','Pitch','Every light of the season, ending with her name in lights.'),
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
films = [('Episode 1','The Coat Pocket'),('Episode 2','The Keepsake'),('Episode 3','[Title]'),('Episode 4','The Friendly Visit'),('Episode 5','The Signal'),('Episode 6','[Title]')]
film_html = '<div class="callout"><p>Watch all six episodes of Synth City.</p><a class="btn" href="https://youtube.com/playlist?list=PLzGEOC0lqaKMDMQ1OlSfnQW9dEJkE7zTB" target="_blank" rel="noopener">Watch the series on YouTube</a></div>'
def beat(title, line, text, content):
    return (f'<div class="beat"><div class="beat-head"><h3>{title}</h3><p class="beat-line">{line}</p></div>'
            f'<p class="body-copy">{text}</p>{content}</div>')

insight_card = insight_box('Lab-grown made diamonds abundant. Rarity only matters when you imagine losing it.', 'Natural diamonds. Beyond fiction.')

final_card = ('<div class="endcard"><p class="endcard-small">Synthetic diamonds. Synthetic love. Synthetic everything.</p>'
              '<p class="endcard-mid">Hold something the future can&#39;t make.</p>'
              '<p class="endcard-big">Natural diamonds. Beyond fiction.</p>'
              '<p class="endcard-small brand">Premier Gem</p></div>')

case('synth-city.html', 'Synth City', ['Premier Gem','In development · Soft launch 2026','Creative Direction · Concept · Art Direction'],
     'The future made everything available. Except one thing: rarity.',
     'Synth City is a dystopian brand world for Premier Gem, told across six films, a live broadcast network and working AI tools. Each touchpoint goes a layer deeper, built to feel like something you discover rather than an ad you&#39;re served. Soft-launched in 2026 to test the world and its tools; the full rollout is in development.',
     'phone:https://synthcity.tv/|synth-hero|The last natural diamond on display. The real thing draws a crowd.', 'A crowd presses around a single rough natural diamond in a vitrine while workers sweep piles of synthetic diamonds off the floor',
     [section('01','The insight','', insight_card),

      section('02','The journey','Every piece hands off to the next. A viewer can enter anywhere, but the path always ends with something real.',
              '<ol class="journey"><li><span class="j-n">01</span><strong>The film</strong><span>Each episode plants a QR code inside the world.</span></li><li><span class="j-n">02</span><strong>synthcity.tv</strong><span>A call from 2187 patches you into the Bureau&#39;s broadcast, live.</span></li><li><span class="j-n">03</span><strong>Rarity Detector</strong><span>Scan any stone. The Bureau decides what&#39;s real.</span></li><li><span class="j-n">04</span><strong>Synth-Mate Lab</strong><span>Order a partner. Meet the system&#39;s endgame.</span></li><li><span class="j-n">05</span><strong>The transmission</strong><span>The last geologist breaks through.</span></li><li><span class="j-n">06</span><strong>Premier Gem</strong><span>Hold something the future can&#39;t make.</span></li></ol>'),

      section('03','The world','In 2187, synthetic won. Diamonds are infinite, identical and Bureau approved. Even a proposal is something you grab on the way to your gate.',
              '<div class="stack">' + img('synth-aerial','Aerial view of Synth City at night: flying cars, neon towers and a Welcome to Synth City sign','Welcome to Synth City, Cycle 2187.') + img('synth-world','Bureau Approved billboards selling lab-grown happiness over a crowded plaza at night')
              + img('synth-factory','A vast night factory complex of glowing carbon pressure chambers growing diamonds','Carbon Pressure Chamber 07. Diamonds, grown by the ton.')
              + img('synth-vending','A proposal kit vending machine in a 2187 airport terminal','In 2187, a proposal ring comes out of a vending machine.')
              + '<div class="narrow">' + img('synth-protocol','Bureau poster of a smiling couple in gloves showing matching rings: Love is a protocol. Bureau approved compatibility.','Even marriage comes pre-approved.') + '</div></div>'),

      section('04','The system','A world this perfect needs enforcing. The Synthetic Bureau controls what people see, what counts as real and, finally, who they love. Each of its tools is a live piece of the campaign.',
              img('synth-hq','The Synthetic Bureau headquarters, a brutalist monolith with a wireframe-head seal, citizens queuing beneath drones')
              + beat('The Broadcasts','It controls the story.',
                     'A Bureau news network and public announcements, one message repeated until it sticks: synthetic is better.',
                     '<div class="stack">' + img('synth-broadcast','The SCB7 news network site: Bureau classifies global synthetic diamond oversupply as economic success') + img('scfn-newsroom','A financial news anchor in front of a market wall: natural diamond values surpass Manhattan real estate per gram','SCFN: natural diamonds overtake Manhattan real estate, per gram.') + img('scfn-street','The same market update on a giant screen over a rainy Fifth Avenue in 2187','The story everyone stops for.') + '<div class="pair">' + img('synth-relay','The broadcast received on a relay station screen beside a battered deep-space probe','How it reaches us: a deep-space relay picks up the feed from 2187.') + img('synth-relay-live','The live synthcity.tv broadcast inside the relay station frame','The live site.') + '</div>' + '<div class="pair">' + img('sbcn-cubes','A reporter holds out a palm of raw cube-shaped diamonds','Tonight on SBCN: cubic diamonds, the Bureau&#39;s newest luxury standard.') + img('sbcn-rings','Cube-diamond rings held up to the camera','Unpolished. Unfiltered. The future is cubic.') + '</div>' + '<div class="pair">' + img('sbcn-socialite','A socialite in sunglasses shows off cube-diamond jewelry on camera','The red carpet goes cubic.') + img('scb-internal','Bureau internal surveillance still of cube-diamond rings on display','Bureau internal feed: the Cubic Diamond Index.') + '</div></div>' + '<div class="outlinks"><a class="text-link" href="https://synthcity.tv">Watch the broadcasts: synthcity.tv →</a></div>')
              + beat('The Rarity Detector','It erases the real.',
                     'A working AI tool. Upload any diamond and the Bureau classifies it. Natural stones are flagged as origin anomalies: non-compliant, removed from the record.',
                     img('synth-detector','Four screens of the Rarity Detector: load a specimen, analyzing material, scan complete, signal detected') + '<p class="body-copy" style="margin:28px 0 20px">And people really use it. Real scans from real visitors: in 2187, almost everything is obsolete.</p>' + '<div class="trio">' + img('det-dollar','Detector result: a dollar bill classified as obsolete physical tender','A dollar bill: obsolete physical tender.') + img('det-mouse','Detector result: a wireless mouse classified as an obsolete peripheral','A mouse: obsolete peripheral.') + img('det-earbuds','Detector result: wireless earbuds classified as a pre-2100 artifact','Earbuds: pre-2100 artifact.') + '</div>' + '<div class="outlinks"><a class="text-link" href="https://raritydetector.com">Try it: raritydetector.com →</a></div>')
              + beat('The Synth-Mate Lab','It replaces love.',
                     'The system&#39;s final step. Visitors ride up to the Synthesis Division, upload a face scan and watch the lab grow a partner engineered for perfect compatibility: flawless, loyal and programmed never to leave. If love can be manufactured, what is it worth?',
                     '<div class="stack">' + img('sm-lobby','The Bureau lobby, a marble hall with the wireframe-head seal and a terminal reading Accessing Synthesis Division')
                     + '<div class="pair">' + img('sm-forming','Two growth chambers filled with vapor, figures taking shape inside','Production: a subject takes shape.')
                     + img('sm-assembly','Two half-assembled porcelain androids in the chambers, the terminal reading Assembly 87%, calibrating devotion','Assembly: calibrating devotion.') + '</div>'
                     + img('sm-beach','An android couple at a candlelit beach table at sunset, staring at each other with mechanical hands','Every sunset. Never missed. The perfect relationship, minus anything real.')
                     + '</div><div class="outlinks"><a class="text-link" href="https://syntheticbureau.com" target="_blank" rel="noopener">Enter the lab: syntheticbureau.com →</a></div>')
              + beat('Meet the Clonesworths','The Synth-Mates commercial.',
                     'Inside the world, the Bureau sells it like a 1950s dream. Real love is messy. Synth-Mates come home perfect: always smiling, always on time, always in the right light.',
                     img('sm2-clonesworths','A porcelain-skinned 1950s couple wave in front of a pastel house under a sign: Meet the Clonesworths.')
                     + img('sm2-reality','A tired real couple on a cluttered couch, one on a phone and one on a laptop','Before: real love, real mess.')
                     + img('sm2-sallybob','Two retro synthetic people in glass chambers holding name cards: Sally and Bob','Order your match: Sally and Bob, ready for pickup.')
                     + img('sm2-dinner','The synthetic couple at a candlelit dinner in a 1950s kitchen','Dinner, every night at six.')
                     + img('sm2-shopping','The synthetic couple strolling with shopping bags and an ice cream cone','Never a bad day.')
                     + img('sm2-amalfi','The synthetic couple walking arm in arm by the sea at sunset','Never a missed sunset.')
                     + img('sm2-toast','The synthetic couple toasting with red wine on a rooftop at dusk','Never anything real.'))
              + '<div class="callout"><p>The Detector and the Lab started as &quot;what ifs.&quot;</p><a class="btn" href="lab.html">See what else I&#39;ve built</a></div>'),

      section('05','The signal','Then the broadcast breaks. Across the city&#39;s screens, a recovered transmission cuts through: the last geologist, deep beneath what was once the Diamond District, still searching for something real.',
              '<div class="stack">' + img('synth-signal','The Bureau billboards glitching as a transmission from an underground tunnel breaks through, a crowd stopping to look up','The first crack in the system.')
              + img('synth-transmission','The last transmission: a geologist with a headlamp beneath the buried 47th Street and 5th Avenue street sign','Last transmission, beneath 47th Street.') + img('synth-transmission-live','The live Last Known Transmission page with the geologist&#39;s headlamp video','The live transmission page.') + img('synth-warning','Report card: Geologists warn humanity may be losing the ability to recognize rare things. Report classified. Researcher reassigned.','The report the Bureau buried.') + '</div>'
              + '<div class="outlinks"><a class="text-link" href="https://synthcity.tv/kalahari">Follow the transmission: synthcity.tv/kalahari →</a></div>'),

      section('06','The films','The heart of the campaign. Six short films, one dystopian future and one question running through all of it: what happens to love when nothing is rare anymore? Each episode was produced like a release, with an original score, cinematic visuals and QR-connected environments that pull viewers deeper into the world.',
              film_html),

      section('07','The proof','Everything leads here. One rough stone, the only warm light in a cold world, and the reason it still matters today.',
              '<div class="stack">' + img('synth-proof','A dirt-covered hand opens in a dark tunnel to reveal a glowing rough natural diamond','Proof that something real remains.')
              + img('synth-now','Present day: a woman&#39;s hand with a natural diamond engagement ring resting on a sunlit kitchen table beside a coffee cup','Back to now.')
              + final_card
              + '</div>'),

      section('08','What&#39;s next','The soft launch tested the world and its tools. The full rollout is in development.',
              '<ol class="journey roadmap"><li><span class="j-n">01</span><strong>Full release</strong><span>All six films released on a schedule, each one unlocking the next layer of the world.</span></li><li><span class="j-n">02</span><strong>The QR journey at scale</strong><span>Every episode, broadcast and poster becomes a door into the tools.</span></li><li><span class="j-n">03</span><strong>Trade partnership</strong><span>A trade-network partnership to bring the Rarity Detector to dealers worldwide.</span></li><li><span class="j-n">04</span><strong>Retail moments</strong><span>The Detector and the transmission brought into stores, where the real stone is waiting.</span></li></ol>')],
     'desert-diamonds.html', 'Desert Diamonds', 'Synth City, a dystopian brand world for Premier Gem: six films, a live broadcast network and working AI tools.')


bc_insight = insight_box('Jewelry is chosen under showroom lights. It&#39;s worn under every other kind.', 'Every light of the season.')

bc_steps = '''<ol class="steps">
<li><strong>Choose the ring.</strong> Engagement rings purchased December 1&ndash;24 qualify.</li>
<li><strong>Choose the night.</strong> The customer books a time slot and a first name, approved by Brown &amp; Co.</li>
<li><strong>Light it up.</strong> The question runs on a digital board over Buckhead, and Brown &amp; Co. captures the moment for the couple to share.</li>
</ol>'''

bc_end = ('<div class="endcard"><p class="endcard-small">Every light of the season.</p>'
          '<p class="endcard-big">The brightest one has her name on it.</p>'
          '<p class="endcard-small brand">Brown &amp; Co. Jewelers &middot; Buckhead | Roswell</p></div>')

case('brown-co.html', 'Brown &amp; Co', ['Pitch','Integrated campaign','Concept · Creative Direction · Art Direction'],
     'Every light of the season.',
     'A holiday campaign pitched to Brown &amp; Co. Jewelers in Buckhead and Roswell. Every piece is built on light: billboards that outshine the season, a print promise, an in-store proof, and a finale that puts the customer&#39;s own proposal in lights.',
     'bc-plugin', 'Billboard at dusk: The only light on this tree we didn&#39;t have to plug in.',
     [section('01','The insight','', bc_insight),

      section('02','Out-of-home: it outshines the season','Every holiday light needs a plug, a battery or a box in the attic. The diamond doesn&#39;t.',
              '<div class="stack">' + img('bc-strings','Billboard: String lights come down in January. This doesn&#39;t.')
              + img('bc-forever','Billboard at night over the Atlanta skyline: This ornament stays lit forever.') + '</div>'),

      section('03','Print: it makes the promise','The spread turns the idea into a claim: Brown &amp; Co. tests every stone in the light it will actually live in, not just the light of the showroom.',
              img('bc-magazine','Magazine spread at night: One ring. Every light of the season. Six ring photos, each passing a lighting test, ending with the skyline test') ),

      section('04','In-store: it proves it','The Lighting Bar brings the claim to the counter: five lighting booths, from string lights to the phone flash, so customers see a stone in every light before they buy. The sixth booth and a card on the counter sell the finale: Your Name in Lights.',
              img('bc-lightingbar','The Lighting Bar: six booths testing a ring under string lights, candlelight, morning sun, party lights, a phone flash and a miniature skyline billboard, with a Your Name in Lights card on the counter') ),

      section('05','The final light: your name in lights','First, the space goes dark. One board across Buckhead runs almost empty, holding a place for a name. Then customers fill it: buy an engagement ring in December, and Brown &amp; Co. lights that board with one question. The campaign starts on billboards and ends on one, only now the billboard belongs to the customer, and every proposal becomes a story the couple shares for us.',
              '<div class="stack">' + img('bc-reserved','Night billboard, almost entirely empty black, reading This space reserved for her name, with a gold line where a name would go and a small ring by the logo','The teaser.')
              + img('bc-proposal-night','On a Buckhead rooftop at dusk, a man kneels with a ring as a Brown &amp; Co. billboard over the highway reads Sarah, will you marry me?','The payoff: the same space, filled.')
              + bc_steps + bc_end + '</div>')],
     'fage.html', 'Fage', 'Brown & Co: Every light of the season. A holiday campaign pitch that ends with her name in lights.')


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
              img('fage-corpcam','The Corp-Cam site: nine live feeds from milk reception to the loading dock. Watch us make it.')
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
     [section('01','The campaign','Print and social executions that cast natural diamonds as a rare species and the people hunting them as obsessive field photographers.',
              '<div class="stack">' + img('dd-1','A photographer hides in a hedge while a woman with a diamond bracelet sits on a desert terrace') + '<div class="pair">' + img('dd-3-photo','A photographer hides inside a saguaro cactus as a woman adjusts her sunglasses, showing a yellow diamond ring','The cactus.') + img('dd-4-photo','A photographer floats in a flamingo pool float, lens aimed at a yellow diamond ring','The pool float.') + '</div>' + '<div class="pair">' + img('dd-5-photo','A man at breakfast watches through binoculars beside a woman wearing a diamond pendant','The binoculars.') + img('dd-2-photo','Grainy night-vision shot of a woman in a gown, her diamond flaring in a hotel corridor','Night vision.') + '</div></div>'),
      section('02','Social: built for the feed','The same series recut for Instagram and mobile: 4:5 frames, the line set large enough to read in a scroll, and the photographer right in the middle of the shot.',
              '<div class="feed">' + img('dd-social-lizard','4:5 social ad: A natural diamond is a rare sighting, the lizard','The lizard.') + img('dd-social-hedge','4:5 social ad: A natural diamond is a rare sighting, the hedge','The hedge.') + img('dd-social-cactus','4:5 social ad: A natural diamond is a rare sighting, the cactus','The cactus.') + img('dd-social-pool','4:5 social ad: A natural diamond is a rare sighting, the pool float','The pool float.') + img('dd-social-binoculars','4:5 social ad: A natural diamond is a rare sighting, the binoculars','The binoculars.') + img('dd-social-nightvision','4:5 social ad: A natural diamond is a rare sighting, night vision','Night vision.') + '</div>'),
      section('03','The films','Short films that play the stakeout for laughs: the long lens, the binoculars, the paparazzo who will go anywhere, even underwater, for one glimpse of the real thing.',
              '<div class="films">' + film('TheBinoculars.mp4','The Binoculars','dd-film-binoculars') + film('ThePool_DesertRing.mp4','The Pool','dd-film-pool') + film('TheSubmarine_DesertPendant.mp4','The Submarine','') + '</div>'),
      section('04','The microsite: Rare Sightings','The campaign lands on a field expedition. The researcher has left; the notes, maps and binoculars are waiting for you.',
              img('dd-site-hero','Rare Sightings homepage: a field desk with binoculars and a note reading Departed on a field expedition to document rare sightings')),
      section('05','The archive','Every ring becomes a numbered field entry, logged by location and date and classified by species: the round, the pear, the oval, the halo. Each one confirmed.',
              img('dd-site-sightings','Recent Sightings archive cards')),
      section('06','The field reporter program','Owners upload a photo or video of their own ring, name it and say where it was spotted. They get an official field report back, and the best sightings are featured in the archive and on Instagram. The audience becomes the content engine.',
              img('dd-site-reporter','Become a Field Reporter upload section')),
      section('07','The full experience','From expedition to field guide to available stones: one page that moves from story to shopping without breaking character.',
              '<div style="max-width:620px;margin:0 auto">' + img('dd-site-full','Full Rare Sightings microsite design') + '</div>' + '<div class="outlinks"><a class="text-link" href="https://premiergem.com/rare-sightings" target="_blank" rel="noopener">Visit Rare Sightings: premiergem.com/rare-sightings →</a></div>')],
     'brown-co.html', 'Brown &amp; Co', 'Desert Diamonds: A natural diamond is a rare sighting. Campaign, films and UGC microsite.')

case('uber.html', 'Uber', ['Spec','Integrated campaign','Concept · Creative Direction · Art Direction'],
     'When it&#39;s time to go.',
     'A spec campaign for Uber that meets people at the exact moment a night turns. It uses the things everyone says at the end of a night, printed right where the decision happens: on the coaster, on the tab, on the way out the door. Visuals AI-assisted.',
     'ub-hero', 'End of the night at a bar: a check presenter and a phone showing a ride on its way, as the bartender wipes down and two friends put on their coats',
     [section('01','The insight','', insight_box('Everyone knows the night is over before they admit it. You can hear it.', 'The things you say before it&#39;s time to go.')),

      section('02','On-premise: the coasters','A coaster series built from the lines everyone has heard at last call. Each one ends the same way.',
              img('ub-coaster-ex','Coaster: Should I text my ex? Just to say hi. Time to go.','&quot;Should I text my ex? Just to say hi.&quot;')
              + img('ub-coaster-boat','Coaster: Let&#39;s all quit our jobs and buy a boat. Time to go.','&quot;Let&#39;s all quit our jobs and buy a boat.&quot;')
              + img('ub-coaster-tattoos','Coaster: We should all get matching tattoos. Time to go.','&quot;We should all get matching tattoos.&quot;')
              + img('ub-coaster-food','Coaster: Let&#39;s order bar to the food. Time to go.','&quot;Let&#39;s order bar to the food.&quot;')),

      section('03','The tab','The bill is the natural cue to leave, so that&#39;s where the idea lands hardest: an itemized receipt of everything you said, and a card in the check presenter.',
              img('ub-receipt','An itemized bar receipt listing OK one more, I&#39;m not even tired, we should start a business, I love you guys, with Total: time to go','Itemized.')
              + img('ub-presenter','A check presenter with a card reading Tip your bartender. Then tap your app.','Tip your bartender. Then tap your app.')),

      section('04','Out-of-home: on the way out','The last word, placed between the bar door and the curb.',
              '<div class="feed tall9">' + img('ub-sign','Sidewalk sign: Last call is a suggestion. Closing time isn&#39;t.','Sidewalk sign.')
              + img('ub-shelter','Bus shelter: Your tab closed at 1:52. Your ride&#39;s here at 1:55.','Bus shelter.')
              + img('ub-billboard','Digital billboard over a nightlife street: Close your tab. Open your app.','Digital billboard.') + '</div>')],
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

print('built')
