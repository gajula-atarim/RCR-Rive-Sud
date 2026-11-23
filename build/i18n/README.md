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

## Inner pages (11 Nov 2026)
Built from the English designs (About, Services, Team, FAQ, Contact) by `build/elementor/pages_fr.py`, all native
Elementor blocks: À propos (506, /a-propos/), Services (507, /services/), Équipe (508, /equipe/), FAQ (509, /faq/),
Contact (510, /contact/). The Blog page was skipped on request.
- Text: client's own French where it exists (Cardio-secours/SIR pages, trainer paragraphs, the docx Q&A for the FAQ),
  home-page French strings, otherwise a translation of the design copy.
- Contact form: CF7 505 "Contact (FR)" (copy of 202; fields name, phone, email, training type, participants, message;
  mail to the site admin address with Reply-To the visitor).
- Services shows one service at a time (pills, sidebar, previous/next) through a small script in functions.php;
  each service is a container with its own anchor (#cardio-secours, #sir, #anaphylaxie, #sur-place, #tarifs).
- Menu 3, footer navigation and the header quote buttons now point to these pages.
- `functions.php` now marks every front-end page as French (lang fr-CA + rcr-lang-fr), not only the home page.
- Photos photo-rcr-nourrisson (533) and photo-rcr-mannequin (534) added on 11 Nov 2026 (no placeholders left).
- Scroll fade-ins (fadeInUp, Elementor Motion Effects) were added live on 11 Nov 2026 to Services (main column, sidebar),
  Équipe (three text blocks, three sidebar cards), FAQ (hero text, accordion) and Contact (info cards, map, form,
  hours, pricing), matching Home and À propos. `pages_fr.py` does not set these; re-add them if a page is regenerated.
- Banners were reworked live too (photo panel on the right half, 300/260/200 px tall); `pages_fr.py` matches.
- FAQ page rebuilt as option B (11 Nov 2026): sticky "Sujets" menu (renamed from "Thèmes" on 12 Nov 2026) (8 themes, client's question order) with a
  "Vous ne trouvez pas votre réponse ?" card, questions in Elementor Toggle widgets per theme; no question counts in the menu since 12 Nov 2026; compact 2-column menu on phones ≤420 px (all closed on load).
  functions.php highlights the theme being read and prints one FAQPage JSON-LD built from the toggles
  (class rcr-faqtg), so the toggles' own faq_schema is off to avoid duplicates. Old layout kept in option rcr_backup_509_faq.
- Équipe: Lucie Bourassa added (11 Nov 2026) below Fethi's profile, laid out as option B (text left, pink profile card right). Bio copied word for word from the client's other site
  (cliniquesantementaleenligne.ca/equipe-sante-mentale/), title "Infirmière" (old site: "L'infirmière de notre clinique"),
  photo cropped from a screenshot of that page (347 x 372 px, the domain is blocked in this build environment).
  No booking links, per the client's 7 Nov request. Fethi's bio kept as the client's CPR-trainer text.
- Inner-page banners, option B (12 Nov 2026): style.css v1.12.x draws the diagonal photo (existing .rcr-banner-photo /
  .rcr-faq-photo layer, clip-path) and the red band touching it (::after on the banner). Phones/tablets: photo on top,
  red band along its slanted bottom edge, text below. Breadcrumb moved above the title; subtitle lines added live
  (À propos, Services, Équipe, Contact, Politique). pages_fr.py still generates the previous order.
- Home "Savez-vous que…" (12 Nov 2026): "Lire la suite" opens the article in a pop-up (functions.php, front page only;
  styles in style.css v1.13.0). The article text still lives in each card's Elementor Toggle (edit it there); the
  pop-up copies the card's image, label, title, intro and toggle text. Closes with ×, a click outside or Esc;
  keyboard accessible. Layout option B (12 Nov 2026, style.css v1.14.0): navy left column with image, label and title,
  text on the right; on phones it stacks (image, red line, text) and rises from the bottom.

## Contact map (12 Nov 2026)
- The map address was "Rive-Sud, Montréal, QC". That is not a place, so Google ran a search and pinned random businesses with "Rive Sud" in their names. It now reads "Longueuil, QC" at zoom 11, chosen by the client team. Google outlines Longueuil and shows its own card with "Open in Maps".
- Removed our white "RCR Rive-Sud" label (062c1b4). It covered Google's card and button.

## English version with Polylang (18 Nov 2026)
French stays the main language at `/`; English lives under `/en/`. Polylang 3.9.2 (free).

| French | English |
|---|---|
| Accueil 203 `/` | Home 647 `/en/home/` |
| À propos 506 | About us 648 `/en/about/` |
| Services 507 | Services 649 `/en/our-services/` |
| Équipe 508 | Team 650 `/en/team/` |
| FAQ 509 | FAQ 651 `/en/faqs/` |
| Contact 510 | Contact 652 `/en/contact-us/` |
| Politique de confidentialité 382 | Privacy Policy 653 `/en/privacy/` |
| Cardio-secours 380 | Cardiac First Aid 654 `/en/cardiac-first-aid/` |
| Soins immédiats en réanimation 381 | Immediate Resuscitation Care 655 `/en/immediate-resuscitation-care/` |
| En-tête (FR) 297 | Header (EN) 656 |
| Pied de page (FR) 298 | Footer (EN) 657 |
| Menu principal (FR) 3 | Main menu (EN) 10 |
| CF7 202 (quote, home) | CF7 14 "Request a quote" (the site's original English form) |
| CF7 505 Contact (FR) | CF7 640 Contact (EN) |

- The English pages are copies of the live French Elementor pages with every text replaced (same containers,
  classes, responsive settings and animations). Texts: `en_strings.py` (client's own English from the English docx
  files wherever it exists); `make_en.py` builds `out/en_map.json`; `fr_export.json` is the French export they map from.
- Slugs differ from French ones (Polylang free cannot share slugs): services → our-services, faq → faqs, contact → contact-us.
- Section anchors are English too (#cardiac-first-aid, #anaphylaxis, #on-site, #pricing, #faq-cpr, …).
- UAE: header/footer templates are translatable in Polylang (French 297/298 = fr, English 656/657 = en); UAE shows the
  template whose language matches the page, so both target the entire site.
- `functions.php`: `rcr_lang()`, lang attribute and `rcr-lang-fr` / `rcr-lang-en` body class, English tagline,
  English image alt texts (option `rcr_en_alts`, media ID ⇒ text), FR/EN header buttons pointing to the same page in
  the other language (from Polylang's hreflang links), scripts for Services/FAQ on both languages (`rcr_is_page_tr()`),
  English aria labels. `style.css` 1.15.0: "Showing" label on English Services, typography rules for both languages.
- English home address: `/en/home/` (client's choice, 18 Nov 2026). Polylang option "front page URL contains the language code
  instead of the page name" is off; the old English draft Home (15) slug was renamed `home-old` to free `home`.
- `wp-content/mu-plugins/rcr-pll-front.php` (source `build/mu-plugins/`): keeps the English home as the English front page in
  Polylang's languages cache (requests such as REST calls could otherwise rebuild the cache without it).
- Footer/hours in English use the short format "9 am – 7 pm" so they stay on one line.
- "Did you know…" images on the English home: English versions supplied by the client (18 Nov 2026), media 666 EpiPen,
  667 Naloxone, 668 Choking, 669 CPR/AED (`assets/media/article-*-en.webp`). The two tall ones (667, 668) are cropped from
  the top in the cards (object-position top center) so their titles show; the pop-up shows the whole image.
- Editing later: change French text in the French page and English text in the English page (Elementor, as usual);
  they are separate pages linked by Polylang (Pages list shows the FR/EN columns).

## Home links (18 Nov 2026)
- "Nos formations" / "Our training courses" Read more buttons now open the Services panels: FR `/services/#cardio-secours`,
  `/services/#sir`; EN `/en/our-services/#cardiac-first-aid`, `/en/our-services/#sir` (buttons 7977d41, 897455b on 203/647).
- "Voir l'équipe" / "Meet the team" (6a2dcf8) now goes to `/equipe/` and `/en/team/` (was `#team` on the home page).
- The older course pages (380, 381, 654, 655) stay published but are no longer linked from the site.

## Client update of 22 Nov 2026 (docs/WebSiteUpdateRcr22Nov.docx), applied page by page
### Équipe / Team (508 / 650), 23 Nov 2026
- Removed: banner subtitle (03f716d), "Domaines d'expertise" (d45a51f), "Expérience et titres" (87a3b73),
  Fethi's clinic photo in the pink card (4bf29e6, choice confirmed with the team), Lucie Bourassa section (4cfc7cf).
- Red line under Fethi's name (7a044b8): "Instructeur agréé par la Fondation des maladies du cœur et de l'AVC du Canada" /
  "Instructor certified by the Heart and Stroke Foundation of Canada".
### Accueil / Home (203 / 647), 23 Nov 2026
- Certification titles: "Cardio-secours" / "Cardiac First Aid" (3bdfd69), "Soins immédiats en réanimation (SIR)" /
  "Immediate Resuscitation Care (SIR)" (5b23c77); 2nd card line (a2874e1) now "Carte d'attestation Cœur + AVC" /
  "Heart & Stroke course completion card".
- "RCR Rive-Sud" eyebrow above À propos no longer uppercase (c4e5c4a). Avatar label (4a4265f): "Notre formateur et
  fondateur" / "Our Instructor and Founder".
- Savez-vous que…: "L'anaphylaxie" label removed (a2e3098); EpiPen card shows one panel only (media 694 FR / 695 EN,
  cropped from the green "Administration d'EpiPen" half); Naloxone card image aligned to the top (89f67c5).
- New choking photo (media 696, desobstruction-adulte.webp) in the À propos section (59a8608) and the
  "Ce que vous apprendrez" choking circle (dbb8121). English alt texts for 694/696 added to option rcr_en_alts.

### FAQ (509 / 651), 23 Nov 2026
- Naloxone, "Une seule dose suffit-elle toujours ?" / "Is one dose always enough?" (toggle ae6f0b4, tab 63a7b47):
  repeat dose now "après 4 à 5 minutes" / "after 4 to 5 minutes" (was 2 à 3 / 2 to 3).
- Screenshots: docs/screenshots/nov22/faq/.

### EpiPen and choking technique photos, 23 Nov 2026
- Media: 718 epipen-cuisse-adulte, 719 epipen-enfant, 720 desobstruction-tapes-dorsales,
  721 desobstruction-adulte-enfant, 722 desobstruction-nourrisson (source: images 2-6 of the docx, in assets/media/).
  English alts for 718-722 added to option rcr_en_alts. Same images on FR and EN (French text inside the images).
- Home (203/647), Savez-vous que… / Did you know…: EpiPen card ebc6d4e -> 718; choking card d90b39b -> 721
  (object-position top center). The pop-ups reuse the card image.
- Services (507/649): Module anaphylaxie image ddd3649 -> 719 (rcr-169 class removed so the whole image shows);
  photo row 322a9e5 -> 720; new image widget in the Niveau C card (899b85c): 17010a1 (FR) / 99cca50 (EN) -> 722.
- Screenshots: docs/screenshots/nov22/photos/.
- English image versions: 735 epipen-cuisse-adulte-en (made by build/images/translate_epipen_adult.py: French text
  inpainted, English redrawn in Nunito Sans; logo kept). EN home ebc6d4e -> 735.
- 738 epipen-enfant-en (build/images/translate_epipen_child.py) on EN Services ddd3649;
  737 desobstruction-adulte-enfant-en (build/images/translate_choking_adult_child.py) on EN home d90b39b.
- "Ce que vous apprendrez" choking circle (dbb8121, FR + EN) now uses 743 desobstruction-adulte-carre (square crop of
  696) so it renders as a circle; 696 itself was portrait and showed as an oval. EN alt for 743 added to rcr_en_alts.
