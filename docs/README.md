# GovStart Bridge — SIH26136

Multi-page prototype. **Open `index.html`** in a browser; it runs entirely offline
from `file://` with no server and no network.

## Pages

| Page | What it is |
|---|---|
| `index.html` | Landing — the claim, and why innovation procurement is hard |
| `run-a-challenge.html` | Overview of the six steps |
| `step-1..6-*.html` | The mechanism, one step per page. Your choices carry forward. |
| `where-it-runs.html` | Maharashtra's six revenue divisions + photographs |
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
  of Maharashtra;
- **the photographs** — real places, in their own colours.

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

    extract → guard → nav → flatten → pages → mono → search

Edit the build scripts, not these pages: re-running the build overwrites `docs/`.

Checks in `../build/`: `check_links.py`, `pagetest.js`, `flowtest.js`, `regress.js`.
The three `.js` suites need `jsdom`.
