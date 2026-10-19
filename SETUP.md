# Setup and handover plan

Goal: Kev sets up hosting once. After that Berker makes his own changes
through ChatGPT Codex, and the site updates itself when he merges a pull
request. Kev only gets involved for infrastructure.

## Who owns what

| Piece | Lives in | Notes |
| --- | --- | --- |
| Domain `quake-studio.com` | Kev's Cloudflare account (Cloudflare Registrar) | Register it with **Berker as the registrant contact** so the domain is legally his. Turn on auto-renew. About $10–11 a year, at cost. |
| Hosting | Kev's Cloudflare account, Pages project `quake-website` | Free tier. Deploys `site/` from `main`. |
| Code | GitHub org `quakestudio` (free), repo `website` | Kev is owner. Berker gets **Write** access. An org (not Kev's personal account) makes a later handover a single click. |
| Edits | Berker's ChatGPT Plus, Codex connected to his GitHub account | Codex opens pull requests; Berker previews and merges. |
| Google Business Profile, Search Console, Analytics | Berker's Google account | Add Kev as a manager/admin where needed. |

Domain status: `quake-studio.com` is the working choice, pending Berker's
sign-off. Berker prefers "studio" in the name. `quakestudio.com` (no hyphen)
belongs to another business, so anyone who leaves out the hyphen lands on
their site; say "quake dash studio" when giving out the address, and print it
with the hyphen. Checked 2026-10-19: `quake-studio.com`, `quakegym.com`,
`quake.studio` and `quakestudyo.com` were unregistered. If the choice changes,
replace the domain everywhere (site, `scripts/check_site.py`, these docs) in one
commit.

Public or private repo: either works with Codex and Cloudflare. Public is the
better fit here because GitHub's free plan only enforces branch rules on public
repos (see step 5), and nothing in the repo is secret. The handover
`.docx` is excluded by `.gitignore`.

If Kev ever steps away: make Berker an owner of the GitHub org and a Super
Administrator on the Cloudflare account, or transfer the domain out to a
registrar of Berker's choice (allowed 60 days after registration).

## One-time setup (Kev, about an hour)

1. **Domain.** Cloudflare dashboard → Domain Registration → Register Domains →
   `quake-studio.com`. Registrant contact: Berker / QUAKE Gym & Pilates, his email
   and phone. Auto-renew on.
2. **Repository.** Signed in to GitHub as **kevb** (not the work account),
   create the org `quakestudio`, then a repo `website`. This folder is already a
   git repo with a local identity for kevb
   (`11970+kevb@users.noreply.github.com`) and `core.sshCommand` pinned to
   `~/.ssh/id_ed25519_personal`, so commits and pushes don't use the global
   work identity. Check `gh` is on kevb, then push through the `github-kevb`
   SSH alias:

   ```bash
   gh auth switch --user kevb
   ```

   ```bash
   git add -A && git commit -m "QUAKE website V1"
   ```

   ```bash
   git remote add origin git@github-kevb:quakestudio/website.git && git push -u origin main
   ```

3. **Cloudflare Pages.** Workers & Pages → Create → Pages → Connect to Git →
   `quakestudio/website`.
   - Production branch: `main`
   - Framework preset: None
   - Build command: `python3 scripts/check_site.py`
   - Build output directory: `site`

   The first deploy gives a `*.pages.dev` address. Send that to Berker for
   review before buying anything else.
4. **Custom domain.** Pages project → Custom domains → add `quake-studio.com` and
   `www.quake-studio.com`. Then Rules → Redirect Rules: redirect
   `www.quake-studio.com/*` to `https://quake-studio.com/${1}` (301, keep query
   string).
5. **Branch rule.** GitHub repo → Settings → Rules → New branch ruleset for
   `main`: require a pull request before merging (0 approvals), require the
   Cloudflare Pages status check to pass, block force pushes. This stops a
   broken edit from going live and stops anyone pushing straight to `main`.
   `.github/CODEOWNERS` asks for Kev's review automatically when a PR touches
   infrastructure files.
6. **Berker's access.** Once Berker has a GitHub account (his guide walks him
   through it), invite him: org → People → Invite → role Member, then repo →
   Settings → Collaborators and teams → give him **Write**.
7. **Analytics.** For launch, turn on Cloudflare Web Analytics (Pages project →
   Metrics). It is free and sets no cookies, so no consent banner is needed.
   Add Google Tag Manager / GA4 when Google Ads starts; that needs a cookie
   consent banner under KVKK. The click events (`click_whatsapp`,
   `click_phone`, `click_maps`, `click_instagram`) are already wired up.
8. **Search Console.** Add `quake-studio.com` as a Domain property (verify with a
   DNS TXT record in Cloudflare), submit `https://quake-studio.com/sitemap.xml`,
   then add Berker as an owner.
9. **Google Business Profile.** Berker sets the website field to
   `https://quake-studio.com/?utm_source=google&utm_medium=organic&utm_campaign=gbp`.

## Berker's side

Give Berker [docs/BERKER-CHATGPT-GUIDE.md](docs/BERKER-CHATGPT-GUIDE.md). He
uploads it to ChatGPT, and ChatGPT walks him through creating a GitHub
account, accepting the invite, connecting Codex, and making his first change.

The everyday loop:

1. Berker asks Codex for a change in plain language.
2. Codex edits the repo, runs the check, and opens a pull request.
3. Cloudflare comments on the PR with a preview link.
4. Berker checks the preview on his phone and presses **Merge**.
5. The live site updates in about a minute.

Codex follows [AGENTS.md](AGENTS.md) for the rules: both languages, real
reviews and photos only, no new services, run the check.

## What is still needed from Berker before launch

The site works now, but it has yellow draft markers and grey photo
placeholders. `python3 scripts/check_site.py --strict` lists them and must pass
before launch.

1. **Photos (12–18).** 2 entrance/exterior, 3 wide studio, 4–5 coaching in
   action, 3 Pilates, 2 coach portraits, 2–3 equipment details. Real QUAKE
   photos only. Each placeholder on the site is labelled with the shot it needs.
2. **Logo as SVG.** The mountain mark on the site is a redraw of the Instagram
   logo, so swap in the original file.
3. **Berker's details.** Surname, qualifications/certifications, specialties.
4. **Second coach.** Name, role, short bio, qualifications, languages,
   portrait. Who teaches the Pilates sessions, and with what certification?
5. **2–4 more Google reviews** he wants featured. Paste them exactly as written.
6. **Confirm these claims** used in the copy:
   - 0506 519 25 05 is on WhatsApp.
   - Only one session runs in the studio at a time (from a client review).
   - No group classes; all Pilates is 1-on-1.
   - Reformer and Cadillac are the only Pilates apparatus.
   - "2–3 sessions a week is a good start" is advice he's happy to give.
   - Weights and reps are tracked between sessions.
   - Physiotherapy: Instagram lists it, but the website doesn't mention it.
     Should it?
7. **A native read of the Turkish copy.** It was written for him but should
   sound like him.

The featured review on the homepage is Kev's own Google review. Swap it out if
you'd rather not feature it.

## Running it locally

```bash
python3 -m http.server 8787 --directory site
```

Then open http://localhost:8787. Run the check before pushing:

```bash
python3 scripts/check_site.py
```
