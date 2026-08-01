# Next Millionaire Co-operative

**Live site:** https://mizaaaan.github.io/nextmillionaireqr2/

A multilingual static website for **Next Millionaire Co-operative** (Registration No. CO-4471/2010) — a member-owned co-operative that builds community wealth through shared ownership, a commercial car-fleet driver program, and collective enterprise.

## Features

- **Trilingual interface (EN / বাংলা / عربي)** — per-page translation dictionaries applied by `js/i18n.js`. Arabic renders right-to-left automatically.
- **Dark / light theme toggle** — applied instantly in `<head>` to avoid flash-of-wrong-theme, synced across tabs via `localStorage` (`js/theme-toggle.js`).
- **Live fleet grid** — car availability ("Available" / "Booked") is driven by a single JSON file and rendered on both the homepage and the Fleet page.
- **Driver program** — visitors can apply to rent a fleet car for monthly-lease income via an external Google Form.
- **Member portal** — dashboard with member cards and downloadable documents (financial report, meeting minutes, announcements, member guide, events calendar, t-shirt size form, share balance statement).
- **Scroll-reveal animations, animated hero heading, back-to-top button, responsive layout** for mobile.

## Pages

| Page          | Description                                            |
| ------------- | ------------------------------------------------------ |
| `index.html`  | Home — hero, about, gallery, management team, fleet preview, contact |
| `about.html`  | Co-operative story, values, and principles             |
| `team.html`   | Full management team                                   |
| `fleet.html`  | Full car fleet with availability status                |
| `contact.html`| Contact details & join form                            |
| `portal.html` | Member portal with cards and downloadable PDFs         |

## Project structure

```
├── index.html / about.html / team.html / fleet.html / contact.html / portal.html
├── css/styles.css            # Global styles
├── js/
│   ├── i18n.js               # Language switcher engine (shared)
│   └── theme-toggle.js       # Dark/light mode (shared)
├── data/fleet-status.json    # Car statuses (single source of truth for the fleet grid)
├── docs/                     # Generated member-portal PDFs
├── scripts/generate-pdfs.py  # Python generator for the docs/ PDFs
├── images/                   # Photos, gallery, favicons, fleet car images
├── sitemap.xml / robots.txt  # SEO
└── README.md
```

## How to update the fleet status

Edit `data/fleet-status.json` — flip a car's `"status"` between `"booked"` and `"available"`. The homepage and the Fleet page both read from this single file; no HTML or JS changes are needed.

## How to add a new translatable string

1. Add `data-i18n="some.key"` to the HTML element.
2. Add `"some.key": "..."` under `en`, `bn`, and `ar` in that page's inline `translations` object.

The shared engine in `js/i18n.js` applies the text and falls back to English if a key is missing.

## Generating the portal PDFs

The PDFs in `docs/` are generated with Python + [ReportLab](https://www.reportlab.com/):

```bash
pip install reportlab
python3 scripts/generate-pdfs.py
```

This regenerates all 7 documents: financial report, meeting minutes, announcements, member guide, events calendar, t-shirt sizes, and share balance statement. (Bangla text requires the Noto Sans Bengali TTF font at `~/.fonts/NotoSansBengali.ttf`.)

> Note: `share-statement.pdf` is currently not committed in `docs/`, but running the script will recreate it.

## Deployment

Static site — host it anywhere static files are served. Currently deployed on GitHub Pages at `mizaaaan/nextmillionaireqr2` (branch: `main`).
