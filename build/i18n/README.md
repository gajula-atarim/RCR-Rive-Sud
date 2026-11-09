# French version (/fr/)

The French home page is a separate WordPress page built from a copy of the English one.

| What | English | French |
|---|---|---|
| Page | Home (ID 15) `/` | Accueil (ID 203) `/fr/` |
| UAE header | Site Header (16) — all pages except /fr/ | En-tête (FR) (297) — /fr/ only |
| UAE footer | Site Footer (17) — all pages except /fr/ | Pied de page (FR) (298) — /fr/ only |
| Menu | Primary Menu (2) | Menu principal (FR) (3) |
| Quote form (CF7) | 14 | 202 (French labels, messages and email) |

- `fr_home_strings.py` maps every English string on the home page to its French translation
  (no-break spaces ` ` are deliberate: French punctuation and number+unit pairs, and to avoid
  one-word last lines).
- Header FR/EN buttons: FR → `/fr/`, EN → `#` (placeholder, as requested). The active language is shown in navy.
- Phone header on /fr/ uses a shorter "Soumission" button (phone-only widget) because
  "Demander une soumission" does not fit beside FR/EN at 360px.
- `functions.php` sets `lang="fr-CA"` and a `rcr-lang-fr` body class on /fr/; `style.css` uses that
  class for `text-wrap: balance` on headings and `text-wrap: pretty` on paragraphs.
- Course names: Heartsaver kept; BLS shown as "Soins immédiats (BLS)" (full name "Soins immédiats en
  réanimation" in the card text) to keep the client's Heartsaver/BLS naming.

## Current state: French only (since 2026-11-03)

- Home page (Settings → Reading) = **Accueil (203)**, served at `/`. `/fr/` 301-redirects to `/`.
- English **Home (15)**, **Site Header (16)** and **Site Footer (17)** are drafts (kept, not deleted).
- **En-tête (FR) (297)** and **Pied de page (FR) (298)** display site-wide (UAE rule: entire site).
- French menu, footer links, logos and the FR button point to `/` and `/#about`, `/#courses`, … ; EN button = `#`.

To bring English back: publish 15/16/17, give English its own address (e.g. keep 15 at `/en/` or
make it the front page again), set 297/298 back to "specific page: 203" and 16/17 to exclude 203,
then point the EN button to the English page.

## 7 Nov 2026 client update (applied 9 Nov)
`build/elementor/fr_update_nov7.py` generated the first version of this update. On request, every element that
was not explicitly asked for by the client was then removed directly on the live site (FAQ section, extra text,
course-page hero photos/buttons/CTA bands, label/icon additions, footer phone sizes, extra anchors). The live
site is the source of truth; the script output in `out/` reflects the first version, not the final one.
