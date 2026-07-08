# Post Apocalyptic Radio — Site Roadmap

## North star

**Purpose:** Capture emails (segmented by artist vs fan) and drive people to social channels.

**Not in scope:** Streaming, wallets, product UI, or full email automation (yet).

---

## Locked decisions

| # | Topic | Decision |
|---|--------|----------|
| 1 | Blog | **Markdown** via Jekyll (`_posts/`) |
| 2 | SEO page CTA | **Hybrid** — email + Artist/Fan selector on page; links to deep pages |
| 3 | Homepage bottom | **Two paths** — “I am an artist” / “I am a music fan” (no form on home) |
| 4 | Hosting | **GitHub Pages** on `postapocalypticradio.com` |
| 5 | Stack | **Static HTML + Jekyll** — **no React** |
| 6 | Email tool | **Placeholder** until vendor is chosen (ConvertKit, Mailchimp, Resend, etc.) |
| 7 | Emergent cleanup | **Delete all references** — Phase 5 only, not before static site is live |
| 8 | API | **Separate backend** (e.g. `api.postapocalypticradio.com`), not on GitHub Pages |

React exists in this repo only because Emergent builds with it by default. This marketing site does not require React.

---

## Site map

```
/                           Home — hero, features, social; CTA = Artist / Fan buttons
/for-artists                What artists get + onboarding + email form (role: artist)
/for-fans                   What fans get + onboarding + email form (role: fan)

/vs/spotify                 SEO — hybrid email form + role selector
/vs/soundcloud              SEO — same form pattern
/alternatives/bandcamp      SEO — same form pattern

/blog                       Article index (Jekyll)
/blog/[slug]                Markdown posts

Footer (every page)         Social links — X, TikTok, Discord, Instagram, Ko-fi, etc.
```

---

## Form spec (shared)

**Fields:** `email` (required) + `role` (`artist` | `fan`, required)

| Page | Form behavior |
|------|----------------|
| Home | No form — only Artist / Fan buttons |
| `/for-artists` | Email form; hidden/fixed `role=artist` |
| `/for-fans` | Email form; hidden/fixed `role=fan` |
| SEO pages | Email + role pills/dropdown + “For artists · For fans” links |
| Blog posts | Same as SEO (inline CTA block) |

**Now:** Placeholder handler (stub API or sheet) + success/error UI.

**Later:** Wire to chosen email automation with segments/tags.

---

## Tech stack

| Layer | Choice |
|-------|--------|
| Pages | Static HTML + Jekyll layouts/includes |
| Blog | Markdown `_posts/` |
| Styles | Shared CSS (`static/css/…`; migrate off React hash names in Phase 5) |
| Deploy | GitHub Pages (`_config.yml`, custom domain) |
| Backend | FastAPI (or form-only service) on separate host/subdomain |
| Retired | `frontend/`, React bundle, CRA, Emergent tooling |

---

## Phases

### Phase 1 — Static core

- [ ] Rebuild **home** as static HTML (no React)
- [ ] Bottom CTA: **I am an artist** / **I am a music fan** → respective pages
- [ ] Build **`/for-artists`** and **`/for-fans`** (copy, onboarding steps, email form)
- [ ] Shared **`_includes`**: nav, footer, social links, form snippet
- [ ] Placeholder form submit (email + role stored/logged; user sees thank-you)

### Phase 2 — SEO + go live

- [ ] Update SEO pages with **hybrid CTA** (email + role selector)
- [ ] Replace live old static site with this repo on GitHub Pages
- [ ] Canonical domain (`www` vs apex) + redirects aligned
- [ ] Cross-links: home ↔ SEO ↔ persona pages
- [ ] Point forms at placeholder backend (or `api.` subdomain when ready)

### Phase 3 — Blog

- [ ] Jekyll `_layouts` for blog index + post
- [ ] `/blog` index + first 3–5 Markdown posts (SEO-aligned topics)
- [ ] CTA block on every post (hybrid form or artist/fan links)
- [ ] RSS/sitemap for SEO (optional but recommended)

### Phase 4 — Email automation

- [ ] Choose email tool
- [ ] Connect form → tool with **artist** / **fan** segments
- [ ] Welcome flows per segment
- [ ] Optional: notify `hello@postapocalypticradio.com` on signup

### Phase 5 — Cleanup & polish

- [ ] **Remove all Emergent references** (badge, PostHog, titles, preview URLs, asset hosts)
- [ ] Delete **`frontend/`**, `static/js/main.*.js`, CRA/craco, `asset-manifest.json`
- [ ] Stable CSS path (e.g. `par.css`) — no React build hashes
- [ ] Fix meta/title/OG for all pages (P.A.R. branding)
- [ ] Copyright year, accessibility pass, analytics (non-Emergent) if desired

---

## Success metrics

| Metric | Role |
|--------|------|
| Email signups | Primary KPI |
| Artist vs fan split | Segmentation quality |
| Blog → signup | Content funnel |
| Social link clicks | Community growth |
| Organic traffic (SEO + blog) | Top of funnel |

---

## Still open (minor)

- **Canonical host:** `www` vs apex (pick one and redirect)
- **Email vendor:** decide in Phase 4
- **First blog topics:** draft when Phase 3 starts

---

## Explicitly deferred

- Emergent removal → **Phase 5 only**
- React maintenance → **none** (retire after Phase 1 static home is done)
- Product/streaming features → **out of scope**

---

## Known issues (pre-migration baseline)

From code review before this roadmap:

- SEO pages use placeholder `YOUR_BACKEND_URL` — forms non-functional until backend URL is set
- Production React bundle pointed at expired Emergent preview backend (404)
- Live site at `postapocalypticradio.com` is an older static page, not this repo
- Backend `server.py` has `logger` used before definition; root `Dockerfile` path/requirements need fixes before deploy

These are addressed during Phases 1–2 and backend deployment, not in this document alone.
