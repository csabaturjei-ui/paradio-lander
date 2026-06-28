# Implementation Notes — Post Apocalyptic Radio Lander

## 1. SEO Comparison / Alternative Pages

Three standalone HTML pages targeting high-intent search queries, deployed via directory-based routing on GitHub Pages (no `.html` extensions needed).

### Pages created
| URL | File |
|-----|------|
| `/vs/spotify` | `vs/spotify/index.html` |
| `/vs/soundcloud` | `vs/soundcloud/index.html` |
| `/alternatives/bandcamp` | `alternatives/bandcamp/index.html` |

### Design system
Each page links to the existing compiled CSS bundle (`/static/css/main.dd476194.css`) so all design tokens — colors, fonts, component classes — match the main React landing page exactly without duplicating styles.

Key tokens: `#0a0a0a` background, `#39ff14` PAR green, `Orbitron` (headings), `Share Tech Mono` (body). Classes used: `.par-card`, `.par-button`, `.par-button-outline`, `.text-shadow-glow`, `.font-orbitron`, `.font-tech`.

### Page structure (each page)
1. Sticky nav with cross-links to all comparison pages
2. Hero — search-intent H1 + subheadline + two CTAs
3. Stats bar — 4 key numbers (PAR vs competitor)
4. 9-row feature comparison table (PAR column highlighted)
5. 3 callout cards — Decentralized Storage / Zero Middlemen / Community Curation
6. Email signup form CTA (see section 3)
7. Footer with cross-links

### SEO specifics
- `<link rel="canonical">` on each page pointing to the final production URL
- Open Graph + Twitter card meta tags
- Unique `<title>` and `<meta name="description">` per page
- H1 matches the target search intent exactly
- Bandcamp page includes a visual acquisition timeline (Epic → Songtradr) as unique editorial content

### Key angles per page
- **Spotify**: 30%+ platform cut vs PAR's 0%; black-box algorithm vs community curation
- **SoundCloud**: Go+ paywall ($9.99/mo) and minimum play thresholds vs PAR's free access and no minimums; corporate investors vs decentralized protocol
- **Bandcamp**: sold to Epic Games (2022) then Songtradr (2023) with mass layoffs — artists have no guarantee of continuity; PAR is a protocol with no acquirable owner

---

## 2. GitHub Pages Config

### `_config.yml`
Jekyll configuration added at repo root:
- `permalink: pretty` — ensures clean URLs without `.html`
- Excludes backend, tests, Dockerfile, and dev artifacts from Jekyll processing
- `keep_files: [static]` — passes the compiled React JS/CSS through untouched
- No theme (site uses its own compiled CSS)

Directory-based `index.html` files (`vs/spotify/index.html` etc.) are served at clean URLs by GitHub Pages natively without any Jekyll involvement.

---

## 3. Resend Email Integration

### What it does
When someone submits their email on any page, the backend:
1. Saves the signup to Google Sheets (existing behaviour)
2. Sends a confirmation email to the user (HTML, on-brand)
3. Sends a notification to `hello@postapocalypticradio.com`

Email sending is **best-effort** — if Resend fails, the signup still succeeds and returns a 200 to the user. Errors are logged but never surfaced to the frontend.

### Backend changes (`backend/`)
- `requirements.txt` — added `resend>=2.0.0`
- `server.py` — added `send_signup_emails()` function called inside `POST /api/signup` after a successful Google Sheets write
- `.env` — added `RESEND_API_KEY` (excluded from git — see below)

### Frontend (SEO pages)
Each SEO page CTA section replaced with an inline form:
- Email `<input>` styled with `.par-input`
- Submit button styled with `.par-button`
- Loading state on submit
- Success: hides form, shows "📡 Signal received — check your inbox."
- Error: shows error message in red, re-enables button
- No external JS dependencies — pure `fetch()`

### Resend prerequisites before going live
1. Verify `postapocalypticradio.com` as a sending domain in the [Resend dashboard](https://resend.com/domains)
2. The `from` address is `hello@postapocalypticradio.com` — this must match a verified domain
3. Add `RESEND_API_KEY` to the backend's production environment variables

### Backend URL placeholder
The SEO pages contain `https://YOUR_BACKEND_URL/api/signup` as the form action. Replace with the actual deployed backend URL (e.g. `https://par-api.railway.app`) once the backend is deployed. Search for `YOUR_BACKEND_URL` across the three SEO page files.

The main React landing page reads its backend URL from the `REACT_APP_BACKEND_URL` build-time environment variable — no change needed there.

---

## 4. Visual Tweak — Headline Glow

The compiled CSS defines `.text-shadow-glow` as three stacked layers (`3px + 6px + 8px`), which rendered as heavy blur on headlines.

Overridden on all pages (via a `<style>` tag after the CSS bundle link) to a single soft layer:
```css
.text-shadow-glow { text-shadow: 0 0 6px rgba(57,255,20,0.55); }
```

---

## 5. Backend Deployment (TODO)

The backend is a FastAPI + Python app with a `Dockerfile` at `backend/`. It is **not yet deployed** — currently only runs locally.

To make the email forms on the SEO pages functional in production, deploy the backend to any container host (Railway, Render, Fly.io) and set these environment variables in the host's dashboard:

| Variable | Value |
|----------|-------|
| `RESEND_API_KEY` | Your Resend API key |
| `MONGO_URL` | MongoDB connection string |
| `DB_NAME` | Database name |
| `GOOGLE_SHEET_ID` | `1eN0tMEULiGkN-a-wWoWb1ezWKLeS05CvbGnoVKl2hPI` |
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Path to service account JSON inside the container |

Once deployed, replace `YOUR_BACKEND_URL` in:
- `vs/spotify/index.html`
- `vs/soundcloud/index.html`
- `alternatives/bandcamp/index.html`
