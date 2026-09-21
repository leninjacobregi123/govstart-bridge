"""Stage 7: the page sits on the photograph.

There is no white page.  Each page carries one Maharashtra photograph,
fixed behind the whole document under a black scrim, and every surface
that used to be white becomes dark glass the photograph shows through.

The palette does not change - it is the same monochrome, read the other
way round: light type on dark ground.  Colour still survives only in the
insignia and in the photographs themselves.

The scrim is 0.62 and that number is not a taste.  White text needs a
background of relative luminance <= 0.1833 to clear 4.5:1.  Compositing
a pixel over black at alpha a scales each channel by (1-a), and the
brightest possible pixel (255) lands at 0.1833 when (1-a) = 0.466, so
any alpha at or above 0.534 holds for every photograph regardless of
what is in it.  0.62 is the floor once 15px prose has to sit straight on the
photograph rather than on a card; the bands that carry 11px type take a
further ground of their own.
"""
import re, os, glob

DOCS = "/home/lenin/Apps Developed/SIH 26136/docs"
CSS  = os.path.join(DOCS, "assets", "style.css")
css  = open(CSS, encoding="utf-8").read()

# ---- 1. which photograph stands behind which page ---------------------
# Grouped so a family of pages shares one image and the site does not
# flicker between photographs as you move around inside a section.
KOKAN   = ["index.html", "grievance.html", "contact.html", "help.html", "about.html"]
ELLORA  = ["why-its-hard.html", "rule-book.html", "government-laws.html", "templates.html",
           "working-reports.html", "judges-questions.html", "resources.html"]
KAAS    = ["run-a-challenge.html", "where-it-runs.html"] + \
          [f for f in os.listdir(DOCS) if f.startswith("step-")]
SULA    = ["marketplace.html", "categories.html", "products.html", "services.html",
           "skill-purchase.html", "sellers.html", "become-a-seller.html", "licence.html",
           "buyer-login.html", "buyer-registration.html", "buyer-background.html"]
DEEKSHA = ["skills.html", "skill.html", "employment.html", "entrepreneurship.html",
           "schemes.html", "skill-gap.html", "training.html", "training-videos.html",
           "apps.html", "department-services.html"]
PHOTO = {}
for names, cls in ((KOKAN,"ph-kokan"), (ELLORA,"ph-ellora"), (KAAS,"ph-kaas"),
                   (SULA,"ph-sula"), (DEEKSHA,"ph-deeksha")):
    for n in names:
        PHOTO[n] = cls

# ---- 2. tokens used for type and for rules flip; tokens used for a
#         surface do not, because a surface still has to be dark -------
TEXT = {"--navy":"#ffffff", "--ink":"#ffffff", "--blue":"#ffffff", "--green":"#e4e4e4",
        "--red":"#ffffff", "--amber":"#dadada", "--saffron":"#ffffff", "--violet":"#ffffff"}
RULE = {"--navy":"rgba(255,255,255,.34)", "--ink":"rgba(255,255,255,.34)",
        "--blue":"rgba(255,255,255,.40)", "--green":"rgba(255,255,255,.40)",
        "--red":"rgba(255,255,255,.60)",  "--amber":"rgba(255,255,255,.36)",
        "--saffron":"rgba(255,255,255,.60)"}

def retype(m):
    sel, body = m.group(1), m.group(2)
    if "body.hc" in sel or ".tricolour" in sel:      # both keep their own palette
        return m.group(0)
    out = []
    for decl in body.split(";"):
        if ":" in decl:
            prop, val = decl.split(":", 1)
            p = prop.strip()
            table = TEXT if p == "color" else (RULE if p.startswith(("border","outline")) else None)
            if table:
                for tok, lit in table.items():
                    val = val.replace("var(%s)" % tok, lit)
            decl = prop + ":" + val
        out.append(decl)
    return "%s{%s}" % (sel, ";".join(out))

css = re.sub(r"([^{}]*)\{([^{}]*)\}", retype, css)

# ---- 3. the tokens that are only ever type, ground or rule ------------
FLIP = {
 "--body:#333":"--body:#ebebeb",      "--muted:#666":"--muted:#c4c4c4",
 "--ink:#111":"--ink:#ffffff",        # type, a meter fill, and the QR stripes
 "--link:#111":"--link:#ffffff",
 "--line:#ddd":"--line:rgba(255,255,255,.26)",
 "--line-2:#eee":"--line-2:rgba(255,255,255,.15)",
 "--page:#fff":"--page:transparent",  "--w:#fff":"--w:rgba(0,0,0,.46)",
 "--gov-bar:#f6f6f6":"--gov-bar:transparent",
 "--blue-s:#f4f4f4":"--blue-s:rgba(255,255,255,.10)",
 "--green-s:#f2f2f2":"--green-s:rgba(255,255,255,.10)",
 "--amber-s:#f7f7f7":"--amber-s:rgba(255,255,255,.10)",
 "--red-s:#ededed":"--red-s:rgba(255,255,255,.12)",
 "--violet-s:#f4f4f4":"--violet-s:rgba(255,255,255,.10)",
 "--blue-l:#cfcfcf":"--blue-l:rgba(255,255,255,.44)",
 "--green-l:#c2c2c2":"--green-l:rgba(255,255,255,.40)",
 "--amber-l:#d6d6d6":"--amber-l:rgba(255,255,255,.36)",
 "--red-l:#b5b5b5":"--red-l:rgba(255,255,255,.44)",
 "--sh:0 1px 2px rgba(52,52,52,.06),0 8px 24px rgba(52,52,52,.08)":
 "--sh:0 1px 2px rgba(0,0,0,.35),0 10px 30px rgba(0,0,0,.45)",
}
for a, b in FLIP.items():
    assert css.count(a) == 1, "token not found: " + a
    css = css.replace(a, b)

# ---- 4. the dividers stop carrying a second photograph ----------------
# One picture per page: a band with a different photograph in the middle
# of it reads as a seam, not as rhythm.  The band keeps its scrim, so it
# still darkens the page behind its heading.
css = re.sub(r"section\.pb-[a-z]+,\.pb-[a-z]+\{background-image:url\(img/bg-[a-z]+\.webp\)\}\n?",
             "", css)
css = css.replace("background-size:cover;background-position:center 52%;"
                  "background-attachment:fixed;overflow:hidden",
                  "overflow:hidden")

# ---- 5. everything the light theme painted white -----------------------
css += """
/* ===================================================================
   THE PAGE SITS ON THE PHOTOGRAPH
   =================================================================== */
html{background:#0c0c0c}
body{background-image:linear-gradient(rgba(0,0,0,.62),rgba(0,0,0,.62)),var(--photo);
  background-size:cover,cover;background-position:center,center 45%;
  background-repeat:no-repeat,no-repeat;background-attachment:fixed,fixed;color:#ebebeb}
body.ph-kokan  {--photo:url(img/bg-kokan.webp)}
body.ph-ellora {--photo:url(img/bg-ellora.webp)}
body.ph-kaas   {--photo:url(img/bg-kaas.webp)}
body.ph-sula   {--photo:url(img/bg-sula.webp)}
body.ph-deeksha{--photo:url(img/bg-deekshabhoomi.webp)}

/* --navy, --blue, --green, --red and --amber still paint dark surfaces, so
   they cannot flip.  Type that used them gets a token of its own. */
:root{--navy-t:#fff;--blue-t:#fff;--green-t:#e4e4e4;--red-t:#fff;--amber-t:#dadada;
  --violet-t:#fff}

/* the chrome bands let the photograph through */
section{background:transparent}
/* a photograph's sky is bright enough that 11px type over it lands under
   4.5:1, so the bands that carry small type keep a ground of their own */
.utility,.masthead,.crumbs,.strip{background:rgba(0,0,0,.50)}
.stage{background:transparent}
body{background-color:transparent}
/* two rules outrank a bare selector and have to be answered in kind:
   one carries !important, the other is a child selector with a class */
section[style*="background:var(--w)"]{background:rgba(0,0,0,.40)!important}
.panelled>.wrap{background:rgba(0,0,0,.40);border-color:rgba(255,255,255,.26)}
.protobar,header.site,footer,.govstrip{background:rgba(0,0,0,.66)}
.govfoot{background:rgba(0,0,0,.74)}
.flow{background:rgba(0,0,0,.44)!important}
.cta{background:rgba(0,0,0,.46)}
.hero{background-image:none;background-color:rgba(0,0,0,.30)}
.hero:before{background:none}
.masthead{border-bottom:3px solid rgba(255,255,255,.55)}
.utility,.crumbs{border-bottom:1px solid rgba(255,255,255,.14)}
.strip{border-bottom:1px solid rgba(255,255,255,.14)}

/* cards and panels become dark glass */
.card,.lcard,.acc,.divcard,.mphoto,.taskchip,.contract,.stepchip,.door,
.cbox,.ticket,.rev,.appcard,.vid,.proofcard,.panelled>*,.sr-box,.stage{
  background:rgba(0,0,0,.46);border-color:rgba(255,255,255,.26)}
.minidemo,.note-a,.note-b,.statute,.quote,.acc .panel-in .quote,.rev .quote,
.gate span,.seal.live,.tier .anc,.tag,.tag.a,.tag.n{
  background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.24)}
.acc>button:hover{background:rgba(255,255,255,.10)}
.utility a:hover,.utility button:hover{background:rgba(255,255,255,.15);color:#fff}
.bar{background:rgba(255,255,255,.16)}
.bar i,.fitbar i,.s-head:after,.always:before{background:#fff}
.tsize,.lang-btn,.crumbs .gf-count{background:rgba(255,255,255,.12);
  border-color:rgba(255,255,255,.34);color:#fff}
.btn-o{background:transparent;border-color:rgba(255,255,255,.62);color:#fff}
.btn-o:hover{background:rgba(255,255,255,.14)}
.btn-p,.btn-d{background:#fff;color:#111}
.btn-p:hover,.btn-d:hover{background:#dcdcdc;color:#111}
.tag.r{background:rgba(0,0,0,.6);color:#fff;border:1px solid rgba(255,255,255,.62)}
.tag.g{background:#fff;color:#111;border:1.5px solid #fff}
.tag.v{background:transparent;border:1px solid rgba(255,255,255,.44);color:#fff}
.hdrsearch input:focus{background:rgba(255,255,255,.18);color:#fff;
  border-color:rgba(255,255,255,.6);outline:2px solid rgba(255,255,255,.35)}
.sr-box{box-shadow:0 10px 30px rgba(0,0,0,.6)}
.modal-in{background:rgba(12,12,12,.96);border:1px solid rgba(255,255,255,.22)}

/* type, read the other way round */
h1,h2,h3,h4,.brand b,.mh-site b{color:#fff}
p,li,td,th,dd,dt,label,figcaption{color:#e7e7e7}
.crumbs .sepc{color:rgba(255,255,255,.45)}
.eyebrow,.s-head .eyebrow{color:#ededed}
/* the two bars overlap, so they cannot both be a fill: demand is the faint
   extent, certified supply the solid part of it, and the gap between them is
   what the page is about */
.btrack{background:rgba(0,0,0,.42)}
.btrack .dem{background:rgba(255,255,255,.24)}
.btrack .sup{background:#fff;opacity:1}
a{color:#fff}
/* a QR code is a picture of data: it reads dark-on-light or not at all */
.qr{background:
  repeating-linear-gradient(90deg,#111 0 3px,transparent 3px 6px),
  repeating-linear-gradient(0deg,#111 0 3px,transparent 3px 6px),#fff}
.tag,.tag.a,.tag.n,.gate span{color:#fff}
.btn-o:hover{color:#fff}
/* the language button carries !important, so the override has to as well */
.lang-btn{background:rgba(255,255,255,.12)!important;
  border-color:rgba(255,255,255,.34)!important;color:#fff!important}
"""

open(CSS, "w", encoding="utf-8").write(css)

# ---- 6. the script and the markup build inline styles from those tokens
APP = os.path.join(DOCS, "assets", "app.js")
TOKENS = ("navy", "blue", "green", "red", "amber", "violet")
def totext(text):
    """Markup: only a colour declaration flips, because an inline background
       may legitimately want the dark value."""
    for tok in TOKENS:
        text = text.replace("color:var(--%s)" % tok, "color:var(--%s-t)" % tok)
    return text
js = open(APP, encoding="utf-8").read()
for tok in TOKENS:                      # the script's are all colour or border
    js = js.replace("var(--%s)" % tok, "var(--%s-t)" % tok)
js = js.replace("background:#f2f2f2", "background:rgba(255,255,255,.10)")
open(APP, "w", encoding="utf-8").write(js)

# ---- 7. every page names its photograph -------------------------------
n = 0
for f in sorted(glob.glob(DOCS + "/*.html")):
    name = os.path.basename(f)
    cls = PHOTO.get(name, "ph-kokan")
    s = open(f, encoding="utf-8").read()
    out = s.replace("<body>", '<body class="%s">' % cls, 1)
    # the national emblem is black line art drawn for a light ground; on a
    # photograph it disappears, so the inverted artwork takes over.
    out = out.replace('class="emb emb-nat"', 'class="emb emb-nat-w"')
    out = totext(out)
    out = out.replace('style="background:var(--blue)"',            # demand
                      'style="background:rgba(255,255,255,.24);'
                      'outline:1px solid rgba(255,255,255,.45)"')
    out = out.replace('style="background:var(--green)"',           # supply
                      'style="background:#fff"')
    if out != s:
        open(f, "w", encoding="utf-8").write(out)
        n += 1
print("page on the photograph: %d pages, %d photographs" % (n, len(set(PHOTO.values()))))
