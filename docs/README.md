# GovStart Bridge — SIH26136

Multi-page prototype. **Open `index.html`** in a browser; it runs entirely offline
from `file://` with no server and no network.

## Pages

| Page | What it is |
|---|---|
| `index.html` | Landing — the claim, and why innovation procurement is hard |
| `run-a-challenge.html` | Overview of the six steps |
| `step-1..6-*.html` | The mechanism, one step per page. Your choices carry forward. |
| `where-it-runs.html` | Maharashtra's six revenue divisions, and Mumbai as a playback |
| `marketplace.html` | Products, services and 24×7 skill purchases |
| `skills.html` | Skill · Employment · Entrepreneurship |
| `schemes.html` | Scheme eligibility checker |
| `skill-gap.html` | Demand vs certified supply, by district |
| `training.html` | Officer/seller training and videos |
| `resources.html` | Templates · government laws · working reports · apps |
| `rule-book.html` | The GFR provisions behind each step, quoted |
| `judges-questions.html` | Straight answers to the hard questions |
| `help.html` · `about.html` · `grievance.html` · `contact.html` | Support and programme pages |

`assets/` holds the shared stylesheet, script and images — loaded once, cached
across pages. Do not rename it.

## State

Your walkthrough answers, grievance tickets, language and contrast choice live in
this browser's `localStorage`. Nothing is sent anywhere. "Reset" on any step page
clears the walkthrough.

## Colour

The interface is black, white and grey. Colour appears in exactly two places,
because in both it is evidence rather than decoration:

- **the official insignia** — the tricolour rule, and the seal of the Government
  of Maharashtra. There is no invented mark: a department's site carries the
  insignia it is entitled to carry and nothing a designer drew beside them;
- **the photographs** — real places, in their own colours. They sit in a stack of
  fixed layers behind the whole document, under a black scrim, and cross-fade
  from one to the next every eleven seconds. A page opens on the photograph its
  body class names and then moves through the rest; `prefers-reduced-motion`
  leaves it on the first one. Only the opening layer carries an image to begin
  with — the others are given theirs once the page is quiet — so opening a page
  still costs one photograph rather than five.

The scrim is 0.62, and that is arithmetic rather than taste. White text needs a
background of relative luminance at or below 0.1833 to clear 4.5:1; compositing
a pixel over black at alpha *a* scales each channel by (1 − *a*), so the
brightest pixel a photograph can contain lands there at *a* = 0.534. Above that,
the figure holds for any photograph whatever is in it. Bands that carry 11px
type — the utility bar, masthead, breadcrumb — take a further ground of their
own, because a bright sky is exactly where the small type falls.

Because the background moves, every page has to hold against all five
photographs rather than its own, so contrast is measured with the layer forced
to **pure white**: nothing in a photograph can be brighter than that, and three
of the five do reach it. Under that test, muted type takes its value from what
it sits on — nearly white on the open page, quiet inside anything with a ground
of its own, which is where almost all of it lives.

Nothing is white. Cards and panels are dark glass the photograph shows through.

## The Mumbai playback

`where-it-runs.html` carries six photographs of Mumbai — the heritage precinct
and the commercial district — that cross-fade and scale slowly, which is what
reads as footage. It is a playback rather than a video file on purpose: this site
promises to run from `file://` with no network and no external request, and six
stills at 457 KB keep that promise where a video would not.

Advancing is a timer and the progress bar is a CSS transition, so it does not
depend on `requestAnimationFrame` being driven. `prefers-reduced-motion` turns
the motion off and leaves the controls. Play/pause is a real button with
`aria-pressed`, the six chapter marks are real buttons, and every frame names
its photographer and licence.

Everything a designer would otherwise reach for a hue to do is done with weight,
rule and spacing instead. Where colour used to carry meaning — pass, warning,
failure — the distinction is border weight and style, so it survives for a reader
who cannot see colour at all (WCAG 1.4.1). High-contrast mode keeps its own
yellow-on-black palette.

## Rebuilding

`../build/build.py` generates this folder. The stages run **in order**, and the
order matters: `extract.py` rewrites `assets/app.js` from source, so every later
stage has to follow it, and `mono.py` has to follow `pages.py` because it greys
the inline styles in the stamped-out markup as well as the stylesheet.

    extract → guard → nav → flatten → pages → mono → onphoto → mumbai → search

Edit the build scripts, not these pages: re-running the build overwrites `docs/`.

Checks in `../build/`: `check_links.py`, `pagetest.js`, `flowtest.js`, `regress.js`.
The three `.js` suites need `jsdom`.
