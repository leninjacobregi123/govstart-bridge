# -*- coding: utf-8 -*-
"""Stage 10: strip the top chrome to the two emblems.

What is left at the top of every page is the State Emblem of India and the
seal of the Government of Maharashtra, top left, and nothing else.

Two things do not simply get deleted, because neither is decoration:

  the disclaimer - this site shows both emblems, and use of the State Emblem
    is governed by the State Emblem of India (Prohibition of Improper Use)
    Act, 2005. Showing them with no correction anywhere above the fold would
    present a student prototype as a government portal. It becomes one small
    line under the emblems instead of a full-width banner, and the full
    notice stays in the footer where it already was.

  the accessibility controls - the site claims GIGW 3.0 in its own footer,
    and these are the only route to high contrast, text size and Marathi.
    They move down to sit beside the statutory policy links, which is where
    most government sites keep them. The skip link stays out of the way
    until it is focused.
"""
import re, os, glob

DOCS = "/home/lenin/Apps Developed/SIH 26136/docs"
CSS  = os.path.join(DOCS, "assets", "style.css")

NOTE = ""   # the disclosure lives in the footer


def block(html, start_tag, open_re):
    i = html.find(start_tag)
    if i < 0:
        return None
    depth = 0
    for m in re.finditer(open_re, html[i:]):
        depth += 1 if not m.group(0).startswith("</") else -1
        if depth == 0:
            return i, i + m.end()
    return None


def strip(path):
    h = open(path, encoding="utf-8").read()
    if 'class="mh-embs"' in h:
        return False

    # 1. the accessibility cluster moves to the footer, beside the policies
    ur = block(h, '<span class="u-r">', r"</?span\b[^>]*>")
    if ur:
        cluster = h[ur[0]:ur[1]]
        h = h[:ur[0]] + h[ur[1]:]
        anchor = '<nav class="policy-links"'
        if anchor in h:
            h = h.replace(anchor, '<div class="gf-a11y">' + cluster + "</div>" + anchor, 1)

    # 2. the prototype banner comes off the top; the footer still carries it
    pb = block(h, '<div class="protobar">', r"</?div\b[^>]*>")
    if pb:
        h = h[:pb[0]] + h[pb[1]:]

    # 3. the masthead keeps the two emblems and the one line under them.
    #    On the landing page they already sit together; everywhere else the
    #    State Emblem is still up in the utility bar, so look across the
    #    whole head rather than inside the masthead alone.
    head = h[:h.find("<main")]
    nat = re.search(r'<span class="emb emb-nat-w"[^>]*></span>', head)
    moh = re.search(r'<span class="emb emb-moh"[^>]*></span>', head)
    assert nat and moh, "expected both emblems in " + os.path.basename(path)
    nat, moh = nat.group(0), moh.group(0)
    mh = block(h, '<div class="masthead">', r"</?div\b[^>]*>")
    assert mh, "no masthead in " + os.path.basename(path)
    h = (h[:mh[0]]
         + '<div class="masthead"><div class="wrap">'
         + '<span class="mh-embs">' + nat + moh + "</span>"
         + "</div></div>"
         + h[mh[1]:])

    # 4. the tricolour rule is decoration, and it is aria-hidden already
    tc = block(h, '<div class="tricolour"', r"</?div\b[^>]*>")
    if tc:
        h = h[:tc[0]] + h[tc[1]:]

    # 5. the utility bar has nothing left in it
    ut = block(h, '<div class="utility">', r"</?div\b[^>]*>")
    if ut:
        h = h[:ut[0]] + h[ut[1]:]

    open(path, "w", encoding="utf-8").write(h)
    return True


ADD = """
/* ===================================================================
   THE TOP OF THE PAGE
   Two emblems, and the one line that keeps showing them honest.
   =================================================================== */
.masthead,body.home .masthead{background:transparent;border-bottom:0;padding:0}
/* nothing behind them now, so the artwork carries its own shadow — a white
   emblem over a bright sky would otherwise disappear */
.masthead .emb{filter:drop-shadow(0 1px 3px rgba(0,0,0,.9))
  drop-shadow(0 0 8px rgba(0,0,0,.55))}
/* flush to the corner rather than inside the centred measure */
.masthead>.wrap{max-width:none;width:100%;display:flex;align-items:center;
  gap:14px;flex-wrap:wrap;padding:9px 22px}
.mh-embs{display:flex;align-items:center;gap:11px;flex:none}
.masthead .emb-nat-w{width:21px;height:30px}
.masthead .emb-moh{width:38px;height:38px}
.mh-note{font-size:10.5px;line-height:1.35;color:#c9c9c9;min-width:0}

/* the accessibility controls, now beside the statutory policy links */
.gf-a11y{display:flex;align-items:center;gap:9px;flex-wrap:wrap;
  padding:0 0 12px;margin:0 0 12px;border-bottom:1px solid rgba(255,255,255,.14);
  font-size:11.5px}
.gf-a11y .u-sep{display:none}
.gf-a11y .u-skip{position:absolute;left:-9999px}
.gf-a11y .u-skip:focus{position:static;left:auto}
.gf-a11y a{color:#e0e0e0}
.gf-a11y .a11y-t{display:none}                 /* nothing left to fold */
.gf-a11y .a11y-g{display:flex!important;align-items:center;gap:9px;flex-wrap:wrap}

@media(max-width:700px){
  .masthead>.wrap{padding:8px 16px;gap:10px}
  .mh-note{font-size:9.5px}
}
body.hc .masthead{background:#000!important}
body.hc .mh-note{color:#ff0!important}
"""


def run():
    n = 0
    for f in sorted(glob.glob(DOCS + "/*.html")):
        if strip(f):
            n += 1
    css = open(CSS, encoding="utf-8").read()
    if "THE TOP OF THE PAGE" not in css:
        open(CSS, "w", encoding="utf-8").write(css + ADD)
    print("top chrome reduced to the emblems on %d pages" % n)


run()
