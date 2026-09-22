# -*- coding: utf-8 -*-
"""Stage 9: the landing page's main screen.

Built to a reference the author supplied: the photograph runs full strength
behind the government chrome, the claim sits left rather than centred, and
the navigation floats under it as a rounded bar rather than sitting in a
full-width strip above it.

Nothing goes white.  The reference put the floating bar and the cards on
light surfaces; here they stay dark glass, because the rest of the site is
dark and a white bar on this page alone would read as a different site.

Only index.html is touched.  Every other page keeps the standard chrome.
"""
import re, os

DOCS = "/home/lenin/Apps Developed/SIH 26136/docs"
CSS  = os.path.join(DOCS, "assets", "style.css")
HOME = os.path.join(DOCS, "index.html")


def block(html, start_tag, open_re):
    """Nesting-aware slice of one element, by its opening tag."""
    i = html.find(start_tag)
    if i < 0: return None
    depth, j = 0, i
    for m in re.finditer(open_re, html[i:]):
        depth += 1 if not m.group(0).startswith("</") else -1
        if depth == 0:
            j = i + m.end()
            break
    return i, j


def run():
    h = open(HOME, encoding="utf-8").read()
    if "landing-done" in h:
        return

    # ---- the navigation moves below the claim -------------------------
    hdr = block(h, '<header class="site">', r"</?header\b[^>]*>")
    assert hdr, "no site header"
    header_html = h[hdr[0]:hdr[1]]
    h = h[:hdr[0]] + h[hdr[1]:]

    hero = block(h, '<div class="hero">', r"</?div\b[^>]*>")
    assert hero, "no hero"
    h = h[:hero[1]] + "\n" + header_html + "\n" + h[hero[1]:]

    h = h.replace("<body ", '<body data-landing-done="1" ', 1)
    h = h.replace('class="ph-kokan">', 'class="ph-kokan home">', 1)

    # The landing page holds one bright photograph rather than moving
    # through five: the complaint about this page was that it was dark and
    # busy, and a picture that changes under the claim is both.
    h = re.sub(r'<div class="bgshow".*?</div>',
               '<div class="bgshow" aria-hidden="true">'
               '<i class="ph-pratapgad" data-src="assets/img/bg-pratapgad.webp" data-on="1"'
               ' style="background-image:url(assets/img/bg-pratapgad.webp)"></i>'
               '<b></b></div>', h, count=1, flags=re.S)

    # the caption names the photograph, and the photograph has changed
    h = h.replace("<p class=\"hnote\">Sahyadri range, Raigad district</p>",
                  "<p class=\"hnote\">Pratapgad fort, Satara district</p>", 1)

    # CC BY-SA, so it is credited where the others are
    old_cr = "Cropped and compressed; otherwise unaltered.</p>"
    if h.count(old_cr) == 1:
        h = h.replace(old_cr, "Cropped and compressed; otherwise unaltered."
                      " Pratapgad fort, Satara \u2014 \u0938\u0941\u092c\u094b\u0927 "
                      "\u0915\u0941\u0932\u0915\u0930\u094d\u0923\u0940 (CC BY-SA 4.0).</p>")
    open(HOME, "w", encoding="utf-8").write(h)

    css = open(CSS, encoding="utf-8").read()
    if "THE LANDING PAGE" not in css:
        open(CSS, "w", encoding="utf-8").write(css + ADD)
    print("landing page: chrome over the photograph, claim left, nav floated")


ADD = """
/* ===================================================================
   THE LANDING PAGE
   The photograph runs behind the chrome, the claim sits left, and the
   navigation floats under it. Dark throughout - a white bar on this one
   page would read as a different site.
   =================================================================== */
body.home .bgshow i{background-position:center 68%}
body.home .bgshow b{background:rgba(0,0,0,.34)}      /* the picture, brighter */
/* the chrome keeps a thin ground: over a bright sky, 11px type on bare
   photograph comes in at 2.2:1, and the picture still reads through .42 */
body.home .utility,body.home .masthead{background:rgba(0,0,0,.44);border-bottom:0}
body.home .crumbs{display:none}                      /* a breadcrumb to itself */
body.home .masthead{padding-bottom:4px}

/* the claim sits left, and the scrim is heaviest where the words are so the
   right-hand side of the photograph stays a photograph */
body.home .hero{background-color:transparent;padding:54px 0 128px;text-align:left}
body.home .hero:before{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(97deg,rgba(0,0,0,.86) 0%,rgba(0,0,0,.78) 30%,
    rgba(0,0,0,.34) 62%,rgba(0,0,0,.10) 84%,rgba(0,0,0,.04) 100%)}
body.home .hero>.wrap{position:relative;z-index:1;text-align:left}
body.home .hero h1{text-align:left;max-width:760px;font-size:52px;line-height:1.12;
  margin:0 0 18px;font-weight:600}
body.home .hero h1 em{font-style:normal;font-weight:800;color:#fff}
body.home .hero p{text-align:left;margin-left:0;max-width:46ch;font-size:17px;
  color:#ededed}
body.home .hero .hero-cta,body.home .hero .btnrow{justify-content:flex-start}
body.home .hero .cap,body.home .hero .photo-cap{text-align:left}

/* the navigation, floated under the claim */
body.home header.site{background:transparent;margin-top:-74px;position:relative;z-index:6}
body.home header.site>.wrap.nav{max-width:1240px;margin:0 auto;
  background:rgba(0,0,0,.72);border:1px solid rgba(255,255,255,.20);
  border-radius:16px;padding:7px 12px;
  box-shadow:0 18px 40px rgba(0,0,0,.45)}
body.home header.site .navlinks{gap:2px}
body.home .navlinks>a,body.home .mmbtn{border-radius:10px}

/* a mark beside each nav item, in the same geometric family as the rest */
body.home [data-i18n="nav_mech"]:before  {content:"\\25F4\\00a0\\00a0"}
body.home [data-i18n="nav_market"]:before{content:"\\25C8\\00a0\\00a0"}
body.home [data-i18n="nav_ev"]:before    {content:"\\00a7\\00a0\\00a0"}
body.home [data-i18n="nav_dept"]:before  {content:"\\25A6\\00a0\\00a0"}
body.home [data-i18n="nav_about"]:before {content:"\\25CE\\00a0\\00a0"}
body.home .navlinks .cv:before{content:none}

/* the bands below sit on a ground of their own, because the page scrim is
   lighter here than anywhere else on the site */
body.home main>section>.wrap{background:rgba(0,0,0,.46);border-radius:20px;
  padding:40px 34px;margin-top:26px;margin-bottom:26px}
body.home main>section{background:transparent}

@media(max-width:900px){
  body.home .hero h1{font-size:34px;max-width:none}
  body.home .hero{padding:36px 0 96px}
  body.home header.site{margin-top:-58px}
  body.home header.site>.wrap.nav{margin:0 14px;border-radius:14px}
  body.home main>section>.wrap{padding:26px 18px;border-radius:16px}
}
body.hc.home .hero:before{background:#000!important}
body.hc.home .utility,body.hc.home .masthead{background:#000!important}
body.hc.home main>section>.wrap{background:#000!important;border:1px solid #ff0!important}
body.hc.home header.site>.wrap.nav{background:#000!important;border-color:#ff0!important}
"""

run()
