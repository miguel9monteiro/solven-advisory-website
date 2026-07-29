#!/usr/bin/env python3
"""Regenerate ai-flix.html from the VIDEOS list below.

To add a video: append an entry to VIDEOS (url + len are required; title,
src, and note override or extend what YouTube reports), then run from the
repo root:  python3 tools/build_ai_flix.py
The tool fetches each video's title, channel, and thumbnail from YouTube's
oEmbed endpoint, prefers the full-resolution thumbnail when it exists, and
rebuilds the page with matching JSON-LD. Needs network access.
"""
import json
import re
import urllib.request

VIDEOS = [
    {
        "shelf": "Now screening",
        "url": "https://www.youtube.com/watch?v=YFjfBk8HI5o",
        "len": "3 h 16 min",
        "title": "OpenClaw: The Viral AI Agent that Broke the Internet",
        "src": "Peter Steinberger · Lex Fridman Podcast",
        "note": "",
    },
    {
        "shelf": "Now screening",
        "url": "https://www.youtube.com/watch?v=96jN2OCOfLs",
        "len": "30 min",
        "title": "From Vibe Coding to Agentic Engineering",
        "src": "Andrej Karpathy · Sequoia Capital",
        "note": "",
    },
    {
        "shelf": "Now screening",
        "url": "https://www.youtube.com/watch?v=EWvNQjAaOHw",
        "len": "2 h 11 min",
        "title": "How I use LLMs",
        "src": "Andrej Karpathy",
        "note": "",
    },
    {
        "shelf": "Now screening",
        "url": "https://www.youtube.com/watch?v=Bs_VjCqyDfU",
        "len": "18 min",
        "title": "What Happens When All Training Data is AI Generated?",
        "src": "Mutual Information",
        "note": "",
    },
    {
        "shelf": "Now screening",
        "url": "https://www.youtube.com/watch?v=wjZofJX0v4M",
        "len": "27 min",
        "title": "Transformers, the tech behind LLMs",
        "src": "3Blue1Brown",
        "note": "",
    },
    {
        "shelf": "Now screening",
        "url": "https://www.youtube.com/watch?v=v7cTQfeUICY",
        "len": "21 min",
        "title": "How AI is Replacing the Private Equity Analyst",
        "src": "Francis Huang · Apers @ Harvard",
        "note": "",
    },
    {
        "shelf": "Now screening",
        "url": "https://www.youtube.com/watch?v=2UigwwWcl6g",
        "len": "30 min",
        "title": "The New AI Playbook for Private Equity",
        "src": "Amrit Saxena · Proof of Work",
        "note": "",
    },
    {
        "shelf": "Now screening",
        "url": "https://www.youtube.com/watch?v=9vM4p9NN0Ts",
        "len": "1 h 45 min",
        "title": "Building Large Language Models",
        "src": "Stanford CS229 · Stanford Online",
        "note": "",
    },
    {
        "shelf": "Now screening",
        "url": "https://www.youtube.com/watch?v=d95J8yzvjbQ",
        "len": "1 h 24 min",
        "title": "The Thinking Game",
        "src": "Google DeepMind · Documentary",
        "note": "",
    },
    {
        "shelf": "Now screening",
        "url": "https://www.youtube.com/watch?v=n1E9IZfvGMA",
        "len": "2 h 22 min",
        "title": "«We are near the end of the exponential»",
        "src": "Dario Amodei · Dwarkesh Podcast",
        "note": "",
    },
]

SHELF_ORDER = ["Now screening"]

BASE = "https://solvenadvisory.ai"
TITLE = "AI Flix · The Solven screening room | Solven Advisory"
DESC = "AI Flix is Solven Advisory's screening room: a hand-curated shelf of the AI videos actually worth your hours, each watched end to end before it earns a place."


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def head_ok(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status == 200
    except Exception:
        return False


def enrich(v):
    vid = re.search(r"[?&]v=([\w-]{6,})", v["url"]).group(1)
    v = dict(v)
    v["id"] = vid
    maxres = f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
    v["thumb"] = maxres if head_ok(maxres) else f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    try:
        # Videos with embedding disabled return 401 here; those cards fall
        # back to opening on YouTube instead of the on-site player.
        oe = fetch_json(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json")
    except Exception:
        oe = None
    v["embeddable"] = oe is not None
    if oe:
        v.setdefault("title", "") or v.update(title=oe["title"])
        v.setdefault("src", "") or v.update(src=oe["author_name"])
    assert v.get("title") and v.get("src"), (
        f"{vid}: oEmbed unavailable (embedding disabled?); set title and src manually")
    return v


def main():
    videos = [enrich(v) for v in VIDEOS]
    total = len(videos)
    plural = "videos" if total != 1 else "video"

    shelves_html = []
    for shelf in SHELF_ORDER:
        items = [v for v in videos if v["shelf"] == shelf]
        if not items:
            continue
        cards = "\n".join(f"""        <li>
          <a class="vid" href="{esc(v['url'])}"{f' data-embed="{v["id"]}"' if v['embeddable'] else ''} target="_blank" rel="noopener">
            <span class="vid__thumb">
              <img src="{esc(v['thumb'])}" alt="" loading="lazy" width="1280" height="720" />
              <span class="vid__play" aria-hidden="true"><svg viewBox="0 0 40 36"><path d="M 0 0 L 20 36 L 40 0 L 34 0 L 20 25 L 6 0 Z"/></svg></span>
              <span class="vid__len">{esc(v['len'])}</span>
            </span>
            <span class="vid__body">
              <h3>{esc(v['title'])}</h3>
              <p class="vid__src">{esc(v['src'])}</p>{(chr(10) + '              <p class="vid__note">' + esc(v['note']) + '</p>') if v.get('note') else ''}
            </span>
          </a>
        </li>""" for v in items)
        key = re.sub(r"[^a-z0-9]+", "-", shelf.lower()).strip("-")
        shelves_html.append(f"""    <section class="shelf reveal" aria-labelledby="shelf-{key}">
      <div class="shelf__head">
        <h2 id="shelf-{key}">{esc(shelf)}</h2>
        <span class="shelf__count">{len(items):02d} {'entries' if len(items) != 1 else 'entry'}</span>
      </div>
      <ul class="rail" data-stagger>
{cards}
      </ul>
    </section>""")

    ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "AI Flix · The Solven screening room",
        "url": f"{BASE}/ai-flix",
        "description": DESC,
        "publisher": {"@id": f"{BASE}/#organization"},
        "inLanguage": "en-GB",
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": total,
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": v["title"],
                 "url": v["url"], "image": v["thumb"]}
                for i, v in enumerate(videos)
            ],
        },
    }, ensure_ascii=False, indent=2)

    about = open("about.html", encoding="utf-8").read()
    header = about[about.index('<header class="site-header">'):about.index('</header>') + len('</header>')]
    footer = about[about.index('<footer class="site-footer">'):about.index('</footer>') + len('</footer>')]
    header = header.replace('<a href="/about" class="is-current">About</a>', '<a href="/about">About</a>')
    header = header.replace('<a href="/ai-flix">AI Flix</a>', '<a href="/ai-flix" class="is-current">AI Flix</a>')
    header = header.replace('<a href="/pt/sobre" class="nav-lang"', '<a href="/pt" class="nav-lang"')
    assert 'is-current">AI Flix' in header

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{TITLE}</title>
<meta name="description" content="{DESC}" />
<link rel="canonical" href="{BASE}/ai-flix" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Solven Advisory" />
<meta property="og:title" content="{TITLE}" />
<meta property="og:description" content="{DESC}" />
<meta property="og:url" content="{BASE}/ai-flix" />
<meta property="og:image" content="{BASE}/assets/og.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:locale" content="en_GB" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{TITLE}" />
<meta name="twitter:description" content="{DESC}" />
<meta name="twitter:image" content="{BASE}/assets/og.png" />
<link rel="icon" type="image/svg+xml" href="/assets/logos/05_solven_favicon.svg" />
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
<link rel="manifest" href="/site.webmanifest" />
<script type="application/ld+json">
{ld}
</script>
<link rel="stylesheet" href="/solven.css" />
<style>
  /* ===== MARQUEE ===== */
  .fxhero {{ position: relative; overflow: hidden; padding-block: clamp(3.5rem, 7vw, 7rem) clamp(2rem, 4vw, 3.5rem); }}
  .fxhero__chev {{ position: absolute; right: -8%; top: -22%; width: clamp(360px, 44vw, 680px); opacity: 0.07; }}
  .fxhero__inner {{ position: relative; z-index: 1; }}
  .fxhero .eyebrow {{ margin-bottom: clamp(1.25rem, 3vw, 2rem); }}
  .fxhero h1 {{ font-size: var(--t-2xl); line-height: 1.04; max-width: 14ch; color: var(--bone); }}
  .fxhero .lead {{ margin-top: clamp(1.5rem, 3vw, 2.25rem); max-width: 52ch; }}
  .fxhero__meta {{ margin-top: clamp(1.5rem, 3vw, 2rem); font-family: var(--sans); font-size: var(--t-meta); font-weight: 600; letter-spacing: var(--track-label); text-transform: uppercase; color: var(--grey-light); }}

  /* ===== SHELVES (dark) ===== */
  .fxshelves {{ padding-block: 0 clamp(3rem, 6vw, 5rem); }}
  .shelf {{ padding-top: clamp(2rem, 4vw, 3rem); }}
  .shelf__head {{ display: flex; align-items: baseline; justify-content: space-between; gap: var(--s-5); border-top: 0.5px solid rgba(244,242,235,0.18); padding-top: var(--s-5); margin-bottom: var(--s-5); }}
  .shelf__head h2 {{ font-size: var(--t-lg); }}
  .shelf__count {{ flex: 0 0 auto; font-family: var(--sans); font-size: var(--t-meta); font-weight: 600; letter-spacing: var(--track-label); text-transform: uppercase; color: var(--grey-light); }}

  .rail {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--s-6) var(--s-4); list-style: none; margin: 0; padding: 2px 0 var(--s-5); }}
  .rail li {{ display: flex; }}
  @media (max-width: 980px) {{ .rail {{ grid-template-columns: repeat(2, 1fr); }} }}
  @media (max-width: 620px) {{ .rail {{ grid-template-columns: 1fr; }} }}

  .vid {{ display: block; width: 100%; text-decoration: none; color: inherit; }}
  .vid__thumb {{ position: relative; display: block; overflow: hidden; background: #000; aspect-ratio: 16 / 9; }}
  .vid__thumb img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .vid__play {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; opacity: 0; background: rgba(31,36,32,0.35); transition: opacity 0.3s ease; }}
  .vid__play svg {{ width: 54px; height: 49px; transform: rotate(-90deg); fill: var(--sage); }}
  .vid:hover .vid__play, .vid:focus-visible .vid__play {{ opacity: 1; }}
  .vid__len {{ position: absolute; right: 8px; bottom: 8px; font-family: var(--sans); font-size: var(--t-meta); font-weight: 600; letter-spacing: 0.04em; color: var(--bone); background: rgba(31,36,32,0.85); padding: 0.25em 0.6em; }}
  .vid__body {{ display: block; padding: var(--s-4) 2px 0; }}
  .vid h3 {{ font-size: var(--t-md); line-height: 1.25; color: var(--bone); transition: color var(--fast); }}
  .vid:hover h3 {{ color: var(--sage); }}
  .vid__src {{ margin: 0.35em 0 0; font-family: var(--sans); font-size: var(--t-sm); color: var(--sage-pale); }}
  .vid__note {{ margin: 0.5em 0 0; font-size: var(--t-sm); line-height: 1.5; color: var(--sage-pale); }}
  @media (prefers-reduced-motion: no-preference) {{
    .vid__thumb img {{ transition: transform 0.45s cubic-bezier(0.22, 0.61, 0.36, 1), opacity 0.3s ease; }}
    .vid:hover .vid__thumb img {{ transform: scale(1.05); opacity: 0.85; }}
  }}

  /* ===== THE SOLVEN PLAYER ===== */
  .player {{ position: fixed; inset: 0; z-index: 200; display: flex; align-items: center; justify-content: center; padding: clamp(0.75rem, 3vw, 3rem); opacity: 0; }}
  .player[hidden] {{ display: none; }}
  .player.open {{ opacity: 1; }}
  .player__scrim {{ position: absolute; inset: 0; background: rgba(31, 36, 32, 0.94); cursor: pointer; }}
  .player__stage {{ position: relative; z-index: 1; width: min(1080px, 100%); }}
  .player__bar {{ display: flex; justify-content: space-between; align-items: flex-start; gap: var(--s-5); margin-bottom: var(--s-4); }}
  .player__title {{ margin: 0; font-family: var(--serif); font-size: var(--t-lg); line-height: 1.15; color: var(--bone); }}
  .player__src {{ margin: 0.3em 0 0; font-family: var(--sans); font-size: var(--t-sm); color: var(--sage-pale); }}
  .player__close {{ flex: 0 0 auto; background: none; border: 1px solid rgba(244, 242, 235, 0.4); color: var(--bone); font-family: var(--sans); font-size: 1rem; line-height: 1; padding: 0.55em 0.7em; cursor: pointer; transition: border-color var(--fast), color var(--fast); }}
  .player__close:hover {{ border-color: var(--sage); color: var(--sage); }}
  .player__frame {{ aspect-ratio: 16 / 9; background: #000; border-top: 2px solid var(--sage-deep); }}
  .player__frame iframe {{ width: 100%; height: 100%; display: block; border: 0; }}
  .player__note {{ margin: var(--s-3) 0 0; font-family: var(--sans); font-size: var(--t-meta); color: var(--grey-light); }}
  @media (prefers-reduced-motion: no-preference) {{
    .player {{ transition: opacity 0.25s ease; }}
    .player__stage {{ transform: translateY(14px) scale(0.985); transition: transform 0.3s cubic-bezier(0.22, 0.61, 0.36, 1); }}
    .player.open .player__stage {{ transform: none; }}
  }}

  /* ===== CLOSER ===== */
  .fxcta {{ position: relative; overflow: hidden; border-top: 0.5px solid rgba(244,242,235,0.18); }}
  .fxcta__chev {{ position: absolute; right: 5%; top: 50%; transform: translateY(-50%); width: clamp(160px, 20vw, 320px); opacity: 0.1; }}
  .fxcta__inner {{ position: relative; z-index: 1; max-width: 46ch; }}
  .fxcta h2 {{ font-size: var(--t-2xl); line-height: 1.05; }}
  .fxcta p {{ color: var(--sage-pale); margin: var(--s-5) 0 var(--s-7); max-width: 44ch; }}
</style>
</head>
<body data-intro>
<a href="#main" class="skip-link">Skip to content</a>

{header}

<main id="main">

  <!-- MARQUEE -->
  <section class="band-dark fxhero">
    <svg class="fxhero__chev intro-chev" style="--chev-rest:.07" viewBox="0 0 40 36" aria-hidden="true"><path d="M 0 0 L 20 36 L 40 0 L 34 0 L 20 25 L 6 0 Z" fill="#8FA68A"/></svg>
    <div class="shell fxhero__inner">
      <div class="eyebrow intro-rise" style="--intro-delay:.15s">
        <p class="label">AI Flix · The screening room</p>
      </div>
      <h1 class="line-mask" style="--intro-delay:.28s">The extra mile, curated.</h1>
      <p class="lead intro-rise" style="--intro-delay:.45s">Video only, and only what we would put in front of a client: watched end to end before it earns a place on the shelf. The library grows as the frontier does.</p>
      <p class="fxhero__meta intro-rise" style="--intro-delay:.6s">{total} {plural} · chosen by hand · updated July 2026</p>
    </div>
  </section>

  <!-- SHELVES -->
  <section class="band-dark fxshelves" aria-label="The shelves">
    <div class="shell">
{chr(10).join(shelves_html)}
    </div>
  </section>

  <!-- CLOSER -->
  <section class="band-dark section fxcta">
    <svg class="fxcta__chev" viewBox="0 0 40 36" aria-hidden="true"><path d="M 0 0 L 20 36 L 40 0 L 34 0 L 20 25 L 6 0 Z" fill="#8FA68A"/></svg>
    <div class="shell">
      <div class="fxcta__inner reveal">
        <p class="label">The honest caveat</p>
        <h2 style="margin-top:1.25rem">The library is the extra mile. The programmes are the road.</h2>
        <p>Everything on these shelves is free and excellent, and none of it runs on your firm's own deals, models, and memos. That part is our job.</p>
        <div class="cta-row">
          <a href="/contact#book" class="btn btn--dark">Book a call <span class="arw">→</span></a>
          <a href="/programmes" class="tlink tlink--dark">Explore the programmes <span class="arw">→</span></a>
        </div>
      </div>
    </div>
  </section>

</main>

<!-- THE SOLVEN PLAYER -->
<div class="player" id="player" role="dialog" aria-modal="true" aria-labelledby="player-title" hidden>
  <div class="player__scrim" data-player-close></div>
  <div class="player__stage">
    <div class="player__bar">
      <div>
        <p class="player__title" id="player-title"></p>
        <p class="player__src" id="player-src"></p>
      </div>
      <button class="player__close" data-player-close aria-label="Close the player">✕</button>
    </div>
    <div class="player__frame" id="player-frame"></div>
    <p class="player__note">The Solven player streams through YouTube's privacy-enhanced service; nothing is stored until you press play.</p>
  </div>
</div>

{footer}

<script>
  /* The Solven player: cards open in an on-site dialog rather than leaving
     for YouTube. Progressive enhancement: without JS every card is a plain
     link, and cards whose videos disallow embedding keep the plain link. */
  (function () {{
    var player = document.getElementById("player");
    var frame = document.getElementById("player-frame");
    var titleEl = document.getElementById("player-title");
    var srcEl = document.getElementById("player-src");
    var lastFocus = null;

    function openPlayer(card) {{
      var id = card.getAttribute("data-embed");
      if (!id) return false;
      lastFocus = document.activeElement;
      titleEl.textContent = card.querySelector("h3").textContent;
      var src = card.querySelector(".vid__src");
      srcEl.textContent = src ? src.textContent : "";
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
      f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      f.allowFullscreen = true;
      f.title = titleEl.textContent;
      frame.replaceChildren(f);
      player.hidden = false;
      window.requestAnimationFrame(function () {{ player.classList.add("open"); }});
      document.body.style.overflow = "hidden";
      player.querySelector(".player__close").focus();
      return true;
    }}

    function closePlayer() {{
      player.classList.remove("open");
      document.body.style.overflow = "";
      window.setTimeout(function () {{ player.hidden = true; frame.replaceChildren(); }}, 220);
      if (lastFocus) lastFocus.focus();
    }}

    Array.prototype.forEach.call(document.querySelectorAll(".vid[data-embed]"), function (card) {{
      card.addEventListener("click", function (e) {{ if (openPlayer(card)) e.preventDefault(); }});
    }});
    player.addEventListener("click", function (e) {{
      if (e.target.hasAttribute("data-player-close")) closePlayer();
    }});
    document.addEventListener("keydown", function (e) {{
      if (e.key === "Escape" && !player.hidden) closePlayer();
    }});
  }})();
</script>
<script src="/solven.js"></script>
<script src="/consent.js"></script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""
    assert "—" not in page, "em dash found"
    with open("ai-flix.html", "w", encoding="utf-8") as f:
        f.write(page)
    print(f"ai-flix.html: {total} {plural} on {len(shelves_html)} shelf/shelves")
    for v in videos:
        print(f"  · {v['title']} ({v['len']}) thumb={'maxres' if 'maxres' in v['thumb'] else 'hq'}")


if __name__ == "__main__":
    main()
