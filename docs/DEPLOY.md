# GitHub Pages deployment — Post Apocalyptic Radio

## Quick setup

1. **Merge to `main`** — the [GitHub Actions workflow](.github/workflows/pages.yml) builds Jekyll and deploys to Pages.
2. **Repo Settings → Pages**
   - Source: **GitHub Actions**
   - Custom domain: `postapocalypticradio.com` (matches `CNAME`)
   - Enforce HTTPS: **on**
3. **DNS** (at your registrar)

   | Type | Host | Value |
   |------|------|-------|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | CNAME | `www` | `postapocalypticradio.com` (with redirect to apex at registrar) |

## Canonical host

**Apex (`postapocalypticradio.com`)** is canonical — all `<link rel="canonical">` tags and `_config.yml` `url` use the apex domain.

Redirect `www.postapocalypticradio.com` → `postapocalypticradio.com` at your DNS provider (most registrars offer “redirect” or “forwarding” for the `www` CNAME). GitHub Pages serves one custom domain per site; www→apex redirect is a DNS/registrar setting, not something Jekyll can enforce.

## Signup API

Forms POST to `https://api.postapocalypticradio.com/api/signup` (configured in `_config.yml` as `signup_api_url`).

Deploy the FastAPI backend separately (see `backend/`) and point `api.postapocalypticradio.com` at that host. Mailjet integration is Phase 4; until then Google Sheets logging works as the placeholder.

## What gets deployed

- Static Jekyll site: home, `/for-artists`, `/for-fans`, SEO comparison pages
- Compiled CSS in `/static/css/` (Phase 5 will rename to stable path)
- `backend/`, `frontend/`, and dev artifacts are excluded via `_config.yml`
