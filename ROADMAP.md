# Post Apocalyptic Radio — Site Roadmap

## North star

**Purpose:** Capture emails (segmented by artist vs fan) and drive people to social channels.

**Not in scope:** Streaming, wallets, product UI, or the streaming product itself.

---

## Locked decisions

| # | Topic | Decision |
|---|--------|----------|
| 1 | Blog | **Markdown** via Jekyll (`_posts/`) |
| 2 | SEO page CTA | **Hybrid** — email + Artist/Fan selector on page; links to deep pages |
| 3 | Homepage bottom | **Two paths** — “I am an artist” / “I am a music fan” (no form on home) |
| 4 | Hosting | **GitHub Pages** on `postapocalypticradio.com` |
| 5 | Stack | **Static HTML + Jekyll** — **no React** |
| 6 | Email tool | **Mailjet Starter ($9/mo)** — see [Email (Mailjet)](#email-mailjet) |
| 7 | Emergent cleanup | **Delete all references** — Phase 5 only, not before static site is live |
| 8 | API | **Separate backend** (e.g. `api.postapocalypticradio.com`), not on GitHub Pages |

React exists in this repo only because Emergent builds with it by default. This marketing site does not require React.

**Resend is out of scope:** the free tier is already used on another project; Pro ($20/mo) is transactional-only and poor value for list-building. Email reroute through the other project is not viable. Existing Resend code in `backend/server.py` will be replaced in Phase 4.

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

**Phases 1–3:** Placeholder handler (stub API or Google Sheet) + success/error UI.

**Phase 4:** Wire to Mailjet via backend API (see below).

---

## Email (Mailjet)

### Why Mailjet

| Option | Verdict |
|--------|---------|
| **Resend Free** | Unavailable — already used on another project |
| **Resend Pro ($20/mo)** | Transactional volume only; marketing/list is a separate product ($40+/mo) |
| **Mailjet Starter ($9/mo)** | **Chosen** — 2,000 contacts, 15,000 emails/mo, API, fits list + welcome + broadcasts |

Welcome emails on signup do **not** require Mailjet Premium automations — they are sent via the **Send API** from the backend when the form is submitted. Dashboard automations (drip sequences) are optional later if needed (Premium ~$27/mo).

### Signup flow (Phase 4)

```
Form (any page)
  → POST api.postapocalypticradio.com/api/signup  { email, role }
  → FastAPI
      1. Mailjet Contacts API — create/update contact with custom property `role`
      2. Mailjet Send API — welcome email (artist template vs fan template)
      3. Mailjet Send API — optional notify hello@postapocalypticradio.com
  → 200 + success message to user
```

### Mailjet setup checklist (Phase 4)

- [ ] Create Mailjet account (test on free tier first; upgrade to **Starter $9** at go-live)
- [ ] Verify sending domain `postapocalypticradio.com`
- [ ] Create contact list + custom property `role` (`artist` | `fan`)
- [ ] Create two welcome templates (artist / fan)
- [ ] Add `MAILJET_API_KEY` + `MAILJET_API_SECRET` to backend env
- [ ] Replace Resend code in `backend/server.py`
- [ ] Remove `resend` from backend dependencies

### Optional

- Keep Google Sheets as a backup log (or drop once Mailjet is trusted)
- Upgrade to Mailjet Essential ($17) later if dashboard segmentation for campaigns is needed

---

## Tech stack

| Layer | Choice |
|-------|--------|
| Pages | Static HTML + Jekyll layouts/includes |
| Blog | Markdown `_posts/` |
| Styles | Shared CSS (`static/css/…`; migrate off React hash names in Phase 5) |
| Deploy | GitHub Pages (`_config.yml`, custom domain) |
| Backend | FastAPI on separate host/subdomain (`api.postapocalypticradio.com`) |
| Email | **Mailjet** (Contacts + Send API) |
| Retired | `frontend/`, React bundle, CRA, Emergent tooling, **Resend** |

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
- [ ] Point forms at placeholder backend on `api.` subdomain (Mailjet wired in Phase 4)

### Phase 3 — Blog

- [ ] Jekyll `_layouts` for blog index + post
- [ ] `/blog` index + first 3–5 Markdown posts (SEO-aligned topics)
- [ ] CTA block on every post (hybrid form or artist/fan links)
- [ ] RSS/sitemap for SEO (optional but recommended)

### Phase 4 — Mailjet integration

- [ ] Complete [Mailjet setup checklist](#mailjet-setup-checklist-phase-4)
- [ ] Upgrade to **Mailjet Starter ($9/mo)** at go-live
- [ ] Implement `POST /api/signup` → Mailjet contacts + welcome send (artist / fan)
- [ ] Notify `hello@postapocalypticradio.com` on new signup
- [ ] Remove all **Resend** code and dependencies from backend
- [ ] Fix backend deploy (`logger` order, Dockerfile, `backend/requirements.txt`)
- [ ] Point all site forms at production API URL

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
| Artist vs fan split | Segmentation quality (Mailjet contact property) |
| Blog → signup | Content funnel |
| Social link clicks | Community growth |
| Organic traffic (SEO + blog) | Top of funnel |

---

## Still open (minor)

- **Canonical host:** `www` vs apex (pick one and redirect)
- **First blog topics:** draft when Phase 3 starts
- **Google Sheets backup:** keep or drop after Mailjet is live

---

## Explicitly deferred

- Emergent removal → **Phase 5 only**
- React maintenance → **none** (retire after Phase 1 static home is done)
- Product/streaming features → **out of scope**
- Mailjet Premium automations (drip flows) → only if needed after launch
- Resend → **not used for this project**

---

## Known issues (pre-migration baseline)

From code review before this roadmap:

- SEO pages use placeholder `YOUR_BACKEND_URL` — forms non-functional until backend URL is set
- Production React bundle pointed at expired Emergent preview backend (404)
- Live site at `postapocalypticradio.com` is an older static page, not this repo
- Backend `server.py` has `logger` used before definition; root `Dockerfile` path/requirements need fixes before deploy
- Backend currently references **Resend** — to be replaced with Mailjet in Phase 4

These are addressed during Phases 1–4 and backend deployment.
