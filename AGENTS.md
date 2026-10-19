# AGENTS.md: rules for AI coding agents (Codex, Claude Code)

This repository is the website for **QUAKE Gym & Pilates**, a private,
appointment-based personal training and Pilates studio in Cihangir, Beyoğlu,
Istanbul. The owner, Berker, requests changes in plain language (often Turkish)
through ChatGPT Codex. He is not technical. Your job is to make the change he
asked for, keep the site correct in both languages, and open a small pull
request he can preview and merge.

## How the site works

- Plain static HTML and one CSS file. **No build step, no framework, no npm, no
  bundler.** Do not add any of these.
- Cloudflare Pages deploys the `site/` folder. Every pull request gets a
  preview URL; merging to `main` publishes to https://quakegym.com.
- The Cloudflare build runs `python3 scripts/check_site.py`. If it fails, the
  deploy fails and the live site stays as it was.

```
site/
  index.html                       Turkish homepage            /
  personal-training/index.html     Turkish Personal Training   /personal-training/
  pilates/index.html               Turkish Pilates             /pilates/
  en/index.html                    English homepage            /en/
  en/personal-training/index.html  English Personal Training   /en/personal-training/
  en/pilates/index.html            English Pilates             /en/pilates/
  404.html                         Not-found page (both languages)
  assets/css/site.css              All styles. Colours and fonts are in :root.
  assets/js/site.js                Mobile menu and click tracking. Keep it small.
  assets/img/                      Images. Real photos go in assets/img/photos/.
  sitemap.xml, robots.txt, _headers
scripts/check_site.py              Pre-deploy check. Run it before every PR.
```

## Every change

1. **Both languages.** Turkish lives at the root, English under `/en/`. Any
   content change goes into both versions unless Berker says it is for one
   language only. Write natural Turkish (formal "siz") and natural British
   English; do not translate word for word.
2. **Shared parts are copied into every page.** The header, footer, mobile
   contact bar and `<head>` tags are repeated in all seven HTML files. If you
   change the menu, footer, phone number, address or hours, change every file.
3. **Run the check:** `python3 scripts/check_site.py`. It must report
   `0 error(s)`. Fix anything it reports before opening the PR.
4. **Keep the PR small.** One request, one pull request. Describe what changed
   in plain words, in the language Berker used, and list the pages affected so
   he knows where to look in the preview.

## Business facts (single source of truth)

If any of these change, update every place they appear: visible text, the
contact section, footer, FAQ answers, and the JSON-LD `<script>` blocks.

| Fact | Value |
| --- | --- |
| Name | QUAKE Gym & Pilates |
| Address | Kuloğlu Mah., Sıraselviler Cd. No: 2, 34134 Beyoğlu / İstanbul |
| Phone and WhatsApp | 0506 519 25 05 (links use `+905065192505` / `wa.me/905065192505`) |
| Hours | Mon–Fri 08:00–22:00, Sat 08:00–18:00, Sun closed |
| Google Maps | https://maps.google.com/?cid=8926959691805171702 |
| Instagram | https://www.instagram.com/quake.gym/ |
| Google rating | 5.0 from 27 reviews (update the number in both languages when it changes) |
| Domain | https://quakegym.com (do not change canonical URLs unless told to) |

WhatsApp links carry a pre-filled message, URL-encoded. Personal Training pages
and the homepage use the Personal Training message; Pilates pages use the
Pilates message. Copy an existing link rather than writing a new one.

## Brand and copy rules

- Personal Training is the main service. Pilates is secondary. Do not shift the
  emphasis toward Pilates.
- Tone: calm, direct, specific. Short sentences. Coaching-first.
- Never use fitness clichés: "become the best version of yourself", "transform
  your life", "no pain no gain", "unleash", "journey", "elevate", "kendinin en
  iyi versiyonu", "hayatını değiştir".
- Say "Cihangir, Beyoğlu" (not just "Cihangir"; there is another Cihangir in
  Avcılar). Mention Sıraselviler where natural. No keyword stuffing.
- Only describe services and equipment that exist: 1-on-1 personal training,
  1-on-1 Pilates on the Reformer and Cadillac. Do not mention physiotherapy,
  group classes, nutrition plans, pricing or anything else unless Berker
  confirms it.
- **Reviews:** only genuine Google reviews that Berker supplies. Never write,
  edit, shorten or "improve" review text. Use the reviewer's first name and
  surname initial as shown on Google.
- **Photos:** only real photos of QUAKE, its coaches and its clients. Never add
  stock photos or AI-generated images of the studio or people.
- No pricing page, blog, booking system or new SEO landing pages in this
  version.

## Design rules

- Use the existing classes in `site/assets/css/site.css`. No inline `style=""`
  attributes, no new fonts, no new colours.
- The lime accent (`--accent`) is for buttons and highlights on dark
  backgrounds only.
- Mobile comes first. After a layout change, make sure nothing scrolls
  sideways at 375 px wide.

## Draft markers

Unfinished content is marked so it is easy to find:

- `<mark class="todo" data-todo>[...]</mark>` for missing text (yellow on the page).
- `<figure class="photo photo--placeholder" data-todo="photo">` for missing photos.

When Berker provides the real content, replace the marker completely (remove
the `<mark>` or the placeholder `<figure>`). `python3 scripts/check_site.py
--strict` fails while any markers remain; use it before launch.

## Replacing a placeholder photo

1. Put the photo in `site/assets/img/photos/` with a short lowercase name,
   for example `coaching-squat.jpg`. Keep it under 400 KB and about 1600 px on
   the long side. JPG or WebP.
2. Replace the whole placeholder `<figure>` with the same classes minus
   `photo--placeholder` and `data-todo`, and an `<img>` inside:

```html
<figure class="photo photo--wide">
  <img src="/assets/img/photos/coaching-squat.jpg"
       alt="Berker bir danışanın squat tekniğini düzeltiyor"
       width="1600" height="1000" loading="lazy">
</figure>
```

- `alt` describes the photo in the page's language (Turkish on Turkish pages).
- `width` and `height` are the file's real pixel size.
- Use `loading="lazy"` everywhere except the first photo on the page (the hero).
- Keep the aspect class that was there (`photo--portrait`, `photo--wide`,
  `photo--square`, or none for 4:3).

## Adding a Google review

Copy the existing `<figure class="review-card">` in the reviews section of both
homepages. On the Turkish page, show the review in its original language and
add "· İngilizceden çevrildi" only if Berker supplies a translation.

## Analytics hooks

Contact links carry `data-track="click_whatsapp|click_phone|click_maps|click_instagram"`
and `data-track-location="..."`. Keep these on any new contact link.
`site.js` pushes them to `dataLayer` / `gtag` when Google Tag Manager or GA4 is
installed. The tag snippet goes where each page has the comment
`<!-- ANALYTICS: ... -->`, in all seven HTML files.

## Do not change without Kev's approval

`scripts/`, `wrangler.toml`, `site/_headers`, `.github/`, this file, canonical
URLs and the domain. If a request needs one of these, say so in the PR
description and ask Berker to forward it to Kev.

Never commit passwords, API keys or personal data other than the business
contact details above.
