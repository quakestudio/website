# QUAKE Gym & Pilates website

Website for QUAKE Gym & Pilates, a private personal training and Pilates
studio in Cihangir, Beyoğlu, Istanbul. Live at https://quake-studio.com.

- Plain static HTML and CSS in `site/`. No build step.
- Turkish at `/`, English at `/en/`.
- Cloudflare Pages deploys `main`; every pull request gets a preview link.
- `scripts/check_site.py` runs before every deploy and blocks broken changes.

| Doc | For |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Rules for Codex / AI agents editing the site |
| [SETUP.md](SETUP.md) | Hosting, domain, accounts, launch checklist |
| [docs/BERKER-CHATGPT-GUIDE.md](docs/BERKER-CHATGPT-GUIDE.md) | Berker uploads this to ChatGPT; it walks him through making changes |

## Local preview

```bash
python3 -m http.server 8787 --directory site
```

```bash
python3 scripts/check_site.py
```
