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
