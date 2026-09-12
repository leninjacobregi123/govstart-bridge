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

## Rebuilding

`../build/build.py` regenerated this folder from the original single-page file
(`../.govstart-bridge.singlepage.bak.html`). It is a **one-shot migration**, kept as
a record. These pages are now the source of truth — edit them directly; re-running
the build would overwrite your changes.

Checks in `../build/`: `check_links.py`, `pagetest.js`, `flowtest.js`, `regress.js`.
