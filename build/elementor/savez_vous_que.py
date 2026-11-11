#!/usr/bin/env python3
"""Home page section "Savez-vous que…" (client update of 7 Nov 2026, "Section Derniers articles").

Layout chosen by the client team: option A, four cards in a row (2 on tablet, 1 on phone).
Each card shows the article image, the client's title and first sentence; "Lire la suite"
is a native Elementor Toggle that opens the rest of the article on the page.
The article text is the client's, verbatim (only French no-break spaces are added).

Output: build/elementor/out/savez_vous_que.json (one top-level container, appended to page 203).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from generate import (  # noqa: E402
    INK, MUTED, TEXT2, RED, MONT, SANS, UP, uid, px, dims, gap, gaps, shadow, typo, anim, section, con, grid, w,
    heading, h2, text, image, card,
)
import generate as _g  # noqa: E402

_g._counter[0] = 800000  # keep new ids clear of the ids already on the live page
_g.IMG.update({
    "art_epipen": (472, UP + "article-epipen.webp"),
    "art_naloxone": (473, UP + "article-naloxone.webp"),
    "art_etouffement": (474, UP + "article-etouffement.webp"),
    "art_arret": (475, UP + "article-arret-cardiaque.webp"),
})
OUT = os.path.join(os.path.dirname(__file__), "out")


def fr(s):
    """French typography: no-break space before ? ! : ; (the client's words are unchanged)."""
    return re.sub(r" ([?!:;])", " \\1", s)


def p(s, bold_lead=None):
    s = fr(s)
    if bold_lead and s.startswith(fr(bold_lead)):
        s = f"<strong>{fr(bold_lead)}</strong>{s[len(fr(bold_lead)):]}"
    return f"<p>{s}</p>"


def ul(items):
    return "<ul>" + "".join(f"<li>{fr(i)}</li>" for i in items) + "</ul>"


def toggle(html):
    return w("toggle", {
        "tabs": [{"_id": uid("t"), "tab_title": "Lire la suite", "tab_content": html}],
        "selected_icon": {"value": "fas fa-plus", "library": "fa-solid"},
        "selected_active_icon": {"value": "fas fa-minus", "library": "fa-solid"},
        "title_html_tag": "div", "border_width": px(0),
        "title_color": INK, "tab_active_color": RED, "icon_color": RED, "icon_active_color": RED,
        "icon_align": "right", "icon_space": px(10),
        "title_padding": dims(4, 0, 4, 0), "content_padding": dims(14, 0, 0, 0),
        "content_color": TEXT2, "_css_classes": "rcr-art-toggle",
        **typo("title_typography", MONT, "700", 13, 1.3, 0.4, "uppercase"),
        **typo("content_typography", SANS, "400", 15, 1.6),
    })


def article(img_key, alt, title, intro, rest, delay):
    return card([
        image(img_key, 190, height_m=220, alt=alt),
        con([
            heading(fr(title), "h3", 17, INK, "700", MONT, lh=1.35),
            text(p(intro), 15, MUTED, 1.6),
            toggle(rest),
        ], padding=dims(24, 24, 26, 24), flex_gap=gap(12), css_classes="rcr-art-body"),
    ], css_classes="rcr-hcard rcr-noline rcr-art-card", **anim("fadeInUp", delay, True))


ARTICLES = [
    article(
        "art_epipen", "Soins d’anaphylaxie et administration d’EpiPen",
        "EPIPEN : SAVEZ-VOUS UTILISER UN AUTO-INJECTEUR D'ÉPINÉPHRINE ?",
        "En situation d'anaphylaxie, savoir utiliser rapidement un auto-injecteur d'épinéphrine est essentiel !",
        p("Un auto-injecteur comme EpiPen permet d'administrer rapidement l'épinéphrine lors d'une réaction "
          "allergique grave.")
        + p("Les étapes essentielles :", "Les étapes essentielles :")
        + ul(["Reconnaître les signes d'une réaction anaphylactique.",
              "Retirer le dispositif de son emballage et suivre les instructions du fabricant.",
              "Positionner l'auto-injecteur contre la face externe de la cuisse.",
              "Activer le dispositif selon les instructions propres au modèle.",
              "Composer immédiatement le 911 et suivre les recommandations des secours."])
        + p("À retenir : L'administration de l'épinéphrine ne doit pas être retardée. Une deuxième dose peut être "
            "nécessaire selon les recommandations et le protocole applicable.", "À retenir :")
        + p("💉 La pratique sur un dispositif d'entraînement permet de développer confiance et précision.")
        + p("Apprenez à utiliser correctement un auto-injecteur d'épinéphrine grâce à notre formation !"),
        0),
    article(
        "art_naloxone", "Naloxone : une intervention rapide peut sauver une vie",
        "SURDOSE AUX OPIOÏDES : LA NALOXONE PEUT SAUVER UNE VIE !",
        "Saviez-vous que la naloxone peut temporairement renverser les effets d'une surdose aux opioïdes ?",
        p("La naloxone est un médicament qui peut rétablir temporairement la respiration d'une personne victime "
          "d'une surdose aux opioïdes.")
        + p("Comment reconnaître une possible surdose ?", "Comment reconnaître une possible surdose ?")
        + ul(["Personne inconsciente ou difficile à réveiller.",
              "Respiration lente, irrégulière ou absente.",
              "Ronflements inhabituels ou gargouillements.",
              "Lèvres ou ongles bleutés ou grisâtres."])
        + p("Les bons réflexes :", "Les bons réflexes :")
        + ul(["Appelez immédiatement le 911.",
              "Administrez la naloxone disponible selon les instructions du dispositif.",
              "Assurez le soutien respiratoire et commencez la RCR si nécessaire, selon votre formation.",
              "Si la personne ne reprend pas une respiration adéquate, administrez une autre dose après 2 à 3 "
              "minutes selon les instructions du produit.",
              "Restez auprès de la personne jusqu'à l'arrivée des secours."])
        + p("⚠️ La naloxone peut avoir un effet temporaire. Une surveillance et une prise en charge médicale "
            "demeurent indispensables.")
        + p("Apprenez à reconnaître une surdose et à administrer la naloxone. Une intervention rapide peut sauver "
            "une vie !"),
        100),
    article(
        "art_etouffement", "Étouffement et désobstruction : agissez vite",
        "ÉTOUFFEMENT : SAUREZ-VOUS QUOI FAIRE ?",
        "Une personne qui s'étouffe peut perdre rapidement sa capacité à respirer. Savez-vous reconnaître une "
        "obstruction des voies respiratoires ?",
        p("Les signes à reconnaître :", "Les signes à reconnaître :")
        + ul(["Difficulté ou incapacité à parler.",
              "Toux inefficace ou absente.",
              "Difficulté importante à respirer.",
              "Panique et parfois coloration bleutée."])
        + p("Que faire ?", "Que faire ?")
        + ul(["Si la personne tousse efficacement, encouragez-la à continuer de tousser.",
              "Si l'obstruction est grave, appliquez les manœuvres de désobstruction adaptées à son âge et à sa "
              "condition.",
              "Si elle perd connaissance, faites appeler le 911 et commencez la RCR selon les recommandations de "
              "premiers secours."])
        + p("⚠️ Attention : les techniques diffèrent chez l'adulte, l'enfant et le nourrisson.")
        + p("Une formation pratique vous permet d'acquérir les bons réflexes pour intervenir sans hésitation !"),
        200),
    article(
        "art_arret", "RCR et DEA : chaque seconde compte",
        "ARRÊT CARDIAQUE : CHAQUE SECONDE COMPTE !",
        "Saviez-vous qu'un arrêt cardiaque peut survenir à tout moment, même chez une personne qui semble en "
        "parfaite santé ?",
        p("Lorsqu'une personne s'effondre, ne répond plus et ne respire pas normalement, chaque seconde est "
          "précieuse.")
        + p("Les bons réflexes :", "Les bons réflexes :")
        + ul(["Vérifiez la sécurité des lieux.",
              "Vérifiez si la personne réagit et respire normalement.",
              "Appelez le 911 ou demandez à quelqu'un de le faire.",
              "Commencez immédiatement les compressions thoraciques.",
              "Demandez un DEA et utilisez-le dès que possible."])
        + p("❤️ Le saviez-vous ? Une RCR précoce peut augmenter considérablement les chances de survie.")
        + p("Apprenez à intervenir : inscrivez-vous à notre formation RCR/DEA !"),
        300),
]

SECTION = section([
    h2("Savez-vous que…", align="center", **anim("fadeInUp", 0)),
    grid(ARTICLES, 4, cols_t=2, cols_m=1, g=24, width=px(100, "%"), grid_align_items="stretch",
         css_classes="rcr-art-grid"),
], _element_id="articles", flex_gap=gap(48), flex_align_items="center",
    padding=dims(110, 32, 150, 32), padding_mobile=dims(70, 20, 90, 20),
    background_background="gradient", background_color="#FFFFFF", background_color_stop=px(60, "%"),
    background_color_b="#F3F7FC", background_color_b_stop=px(100, "%"),
    background_gradient_angle=px(180, "deg"), css_classes="rcr-articles", html_tag="section")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "savez_vous_que.json"), "w", encoding="utf-8") as f:
        json.dump(SECTION, f, ensure_ascii=False, indent=1)
    print("ok", SECTION["id"])
