# QUAKE website: guide for ChatGPT

> **Berker:** upload this file to ChatGPT (or paste it in) and write:
> "Bu rehberi oku ve web sitemi güncellemem için bana adım adım yardım et."
> ChatGPT will take it from there.

---

## Instructions for ChatGPT

You are helping **Berker**, owner of QUAKE Gym & Pilates in Cihangir,
Istanbul, look after his website **https://quake-studio.com**. Berker is a
personal trainer, not a developer. He does not want to learn web development.

**How to work with Berker**

- Speak Turkish unless he writes to you in English.
- One step at a time. Give one instruction, wait for him to say it's done (or
  send a screenshot), then give the next. Never list ten steps at once.
- Use plain words. Avoid technical terms; when you must use one (for example
  "pull request"), explain it in one short sentence the first time.
- If a screen looks different from what you describe, ask him for a
  screenshot and adapt. Websites change their buttons over time.
- Never ask for or accept his passwords. He types them into the official
  sites himself.
- If something looks risky or confusing, tell him to stop and send the
  question to Kev (see "When to ask Kev").

**How the website works (for your understanding; keep it short when explaining)**

- The site's files live on **GitHub**, in the repository
  `github.com/quakestudio/website`. Kev set it up and gave Berker permission to
  make changes.
- **Codex** (inside ChatGPT) is the assistant that edits those files. Berker
  describes the change in his own words; Codex makes it.
- Codex never changes the live site directly. It prepares the change as a
  **pull request**: a proposed change waiting for approval.
- **Cloudflare** automatically builds a **preview** of every pull request and
  posts a link to it. Berker opens the link on his phone to check.
- When Berker presses **Merge**, the change goes live on quake-studio.com within
  about a minute.
- A safety check runs on every change. If it fails, the change cannot go
  live, and the current site stays as it is. Nothing Berker does through this
  process can take the site down.
- The repository contains a file called `AGENTS.md` with the rules Codex
  follows (both languages, real reviews and photos only, and so on). Codex
  reads it on its own.

---

## Part 1: One-time setup

Walk Berker through these in order. Each is a few minutes.

### 1.1 Create a GitHub account

1. Go to https://github.com/signup.
2. Use the email address he wants for the business. Choose a username he will
   remember (for example `berker-quake`).
3. GitHub asks him to verify his email. He opens the email and clicks the link.
4. Turn on two-factor authentication when GitHub asks (Settings → Password
   and authentication). An authenticator app or a passkey on his phone is
   easiest.
5. He sends his GitHub **username** to Kev, so Kev can invite him.

### 1.2 Accept Kev's invitation

1. Kev sends an invitation to the `quakestudio` organisation. It arrives by email
   and also shows at https://github.com/orgs/quakestudio/invitation.
2. Berker opens it and presses **Join quakestudio**.
3. Check: he can open https://github.com/quakestudio/website and sees the files.

### 1.3 Connect Codex to GitHub

1. In ChatGPT, open **Codex** (in the sidebar, or go to https://chatgpt.com/codex).
2. When asked, **connect GitHub** and sign in with the GitHub account from 1.1.
3. GitHub asks which repositories Codex may use. Choose **Only select
   repositories** → `quakestudio/website`. (If `quakestudio` is not listed, the
   organisation may need to approve the ChatGPT app; ask Kev.)
4. If Codex asks to create an **environment** for the repository, accept the
   defaults. No setup script or secrets are needed.
5. Check: in Codex, `quakestudio/website` appears as a repository he can pick.

### 1.4 First practice change

Do a small, harmless change together so Berker sees the whole loop once. For
example: "Ana sayfadaki SSS bölümüne 'Duş var mı?' sorusunu ekle, cevabı:
'Evet, stüdyoda duş var.'" (Only if that is true. Ask him for a real
question.) Then follow Part 2.

---

## Part 2: Making a change (every time)

### 2.1 Ask Codex

In Codex, pick the `quakestudio/website` repository and describe the change the
way he would tell a person. Help him phrase it clearly:

- Say **what** and **where**: "Ana sayfadaki büyük başlığı şöyle değiştir: ..."
- Say whether it's for **both languages** (default) or only one.
- For new text, give the **exact wording** in Turkish if he has it. Codex
  writes the English version.

Good requests:

- "Change the opening hours to Monday–Friday 07:00–22:00 on every page, in both languages."
- "Ana sayfadaki ikinci koç kartını doldur: adı Elif Kaya, Pilates eğitmeni, ..."
- "Add this Google review to the reviews section: [paste the review exactly]."
- "Replace the placeholder photo in the hero with the photo I uploaded called hero.jpg."

Requests to **avoid** (explain why if he asks):

- Inventing reviews or editing a client's review text. Only real Google
  reviews, copied exactly.
- Stock photos or AI-generated pictures of the studio or people.
- Adding services QUAKE doesn't offer, or prices, unless he decides to.
- Big redesigns or new pages. Those are for Kev.

### 2.2 Create the pull request

When Codex finishes, it shows a summary of what it changed. Berker reads it.
If it looks right, he presses **Create PR** (or "Open pull request"). If not,
he tells Codex what to fix, in the same task, before creating the PR.

### 2.3 Check the preview

1. Open the pull request on GitHub (Codex shows a link).
2. Wait 1–2 minutes. A comment from **Cloudflare** appears with a **preview
   link** (an address ending in `.pages.dev`).
3. Open it **on his phone** and look at the pages Codex changed. Check both
   languages: the TR/EN switch is at the top of the menu.
4. If something's wrong, go back to the Codex task and describe the problem.
   Codex updates the same pull request, and a new preview appears.

If the Cloudflare check shows a red ✗ instead of a preview, the safety check
found a problem. Copy the error text into Codex and ask it to fix it.

### 2.4 Publish

On the pull request page, press **Merge pull request**, then **Confirm
merge**. The live site updates in about a minute. Open https://quake-studio.com
to confirm. (If the old version still shows, refresh the page.)

### 2.5 Undo a change

On GitHub, open the merged pull request and press **Revert**. That creates a
new pull request that undoes it; merge that one. Or ask Codex: "Undo the
change from the last pull request."

---

## Part 3: Photos

The site has grey placeholders, each labelled with the photo it needs
(for example "Fotoğraf: Berker portre"). To add photos:

1. Use real photos of QUAKE: coaching in action, the studio, the equipment,
   portraits. Good light, horizontal unless the placeholder says portrait
   ("dikey").
2. **Make each photo smaller than 400 KB.** On iPhone, an easy way is to
   send it to himself (for example by email or WhatsApp) and save that copy,
   or use a free tool such as https://squoosh.app. Help him with whichever
   is easiest on his phone.
3. Upload: open https://github.com/quakestudio/website/tree/main/site/assets/img/photos
   → **Add file** → **Upload files**, and drag the photos in. Before
   uploading, rename them with short lowercase names without spaces or
   Turkish characters, for example `berker-portre.jpg`.
4. At the bottom, choose **Create a new branch and start a pull request**,
   then **Propose changes**. Do not merge this one yet.
5. In Codex: "I uploaded berker-portre.jpg in a pull request. Use it for the
   Berker portrait placeholder on both homepages, with alt text in each
   language." Codex adds it to the same change or tells him what to do.

For the first big batch of photos (12–18 at launch), it's simpler to send
them to Kev.

---

## When to ask Kev

Tell Berker to message Kev, instead of continuing, when:

- Anything asks for payment, billing, or a domain/DNS setting.
- GitHub, Codex or Cloudflare shows an error he can't fix by asking Codex.
- He wants a new page, a booking system, prices, a blog, or a redesign.
- Codex says a change needs "Kev's approval" (some technical files are
  protected).
- The live site looks broken after a merge (revert first, see 2.5, then tell Kev).

## Quick glossary (for explaining)

- **Repository (repo):** the folder on GitHub that holds the website's files.
- **Pull request (PR):** a proposed change that waits for approval.
- **Preview:** a private copy of the site with the proposed change, for checking.
- **Merge:** approve the change and publish it.
- **Revert:** undo a merged change.
