#!/usr/bin/env python3
"""Client update of 7 Nov 2026 (WebSiteUpdateCpr7Nov.docx) for the French site.

Input : the live Elementor tree of "Accueil" (page 203), exported to JSON (argv[1]).
Output (build/elementor/out/):
  home_fr.json              updated home tree (existing element ids kept)
  page_cardio_secours.json  new course page "Cardio-secours"
  page_sir.json             new course page "Soins immédiats en réanimation (SIR)"
  page_confidentialite.json new "Politique de confidentialité" page

Everything stays native Elementor (containers, headings, text editors, buttons, images,
icon lists, toggle and accordion widgets) so the client can edit it.
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from generate import (  # noqa: E402
    RED, NAVY, INK, BODY, MUTED, TEXT2, SKY, PALE, PINK, DEEP, MONT, SANS, SECTION_PAD,
    uid, px, dims, gap, gaps, shadow, typo, anim, con, section, grid, w, heading, h2, eyebrow, text,
    button, more, image, icon, card, svg_icon, bg_image,
)

import generate as _g  # noqa: E402
_g._counter[0] = 700000  # new element ids must not collide with ids already on the live page

N = " "  # no-break space (French punctuation, number + unit)
OUT = os.path.join(os.path.dirname(__file__), "out")
CARDIO_URL = "/cardio-secours/"
SIR_URL = "/soins-immediats-en-reanimation/"
PRIVACY_URL = "/politique-de-confidentialite/"
QUOTE = "/#quote"
DISCLAIMER = ("<p class=\"rcr-note\"><em>Information générale. En situation d’urgence, appelez le 911 et suivez "
              "les consignes des secours.</em></p>")


# --------------------------------------------------------------------------- helpers
def index(tree):
    idx, parent = {}, {}

    def walk(e, p):
        idx[e["id"]] = e
        parent[e["id"]] = p
        for c in e.get("elements", []):
            walk(c, e)
    for e in tree:
        walk(e, None)
    return idx, parent


def check_list(items, size=16, color=TEXT2, **extra):
    s = {"icon_list": [{"_id": uid("li"), "text": t, "selected_icon": {"value": "fas fa-check-circle",
                                                                        "library": "fa-solid"}}
                       for t in items],
         "view": "traditional", "space_between": px(12), "icon_color": RED, "icon_size": px(18),
         "text_color": color, "text_indent": px(12), "icon_self_vertical_align": "flex-start",
         "icon_vertical_offset": px(4), **typo("icon_typography", SANS, "400", size, 1.55)}
    s.update(extra)
    return w("icon-list", s)


def toggle(title, html, **extra):
    s = {"tabs": [{"_id": uid("t"), "tab_title": title, "tab_content": html}],
         "selected_icon": {"value": "fas fa-plus", "library": "fa-solid"},
         "selected_active_icon": {"value": "fas fa-minus", "library": "fa-solid"},
         "title_html_tag": "div", "border_width": px(0), "title_color": RED, "tab_active_color": RED_D_,
         "icon_color": RED, "icon_active_color": RED_D_, "icon_align": "right", "icon_space": px(8),
         "title_padding": dims(6, 0, 6, 0), "content_padding": dims(10, 4, 4, 4),
         "content_color": TEXT2, "_css_classes": "rcr-learn-toggle",
         **typo("title_typography", MONT, "700", 13, 1.3, 0.6, "uppercase"),
         **typo("content_typography", SANS, "400", 15, 1.6)}
    s.update(extra)
    return w("toggle", s)


RED_D_ = "#A9121A"


def accordion(items, **extra):
    s = {"tabs": [{"_id": uid("a"), "tab_title": q, "tab_content": f"<p>{a}</p>"} for q, a in items],
         "selected_icon": {"value": "fas fa-plus", "library": "fa-solid"},
         "selected_active_icon": {"value": "fas fa-minus", "library": "fa-solid"},
         "title_html_tag": "h4", "faq_schema": "yes",
         "space_between": px(10),
         "title_background": "#FFFFFF", "title_color": INK, "tab_active_color": RED,
         "icon_color": RED, "icon_active_color": RED, "icon_align": "right", "icon_space": px(12),
         "title_padding": dims(16, 20, 16, 20), "content_padding": dims(4, 20, 18, 20),
         "content_background_color": "#FFFFFF", "content_color": TEXT2,
         "_css_classes": "rcr-faq",
         **typo("title_typography", MONT, "600", 15, 1.4),
         **typo("content_typography", SANS, "400", 15, 1.65)}
    s.update(extra)
    return w("toggle", s)  # Toggle (not Accordion): every question starts closed


def page_hero(eyebrow_txt, title, subtitle, tagline, img_key, img_pos="center center"):
    return section([
        grid([
            con([
                eyebrow(eyebrow_txt),
                heading(title, "h1", 48, INK, "800", MONT, lh=1.1, ls=-0.5, size_t=40, size_m=32),
                text(f"<p>{subtitle}</p>", 19, INK, 1.55, "600", size_m=17),
                text(f"<p>{tagline}</p>", 17, RED, 1.5, "600", size_m=16) if tagline else None,
                con([
                    button("Demander une soumission", QUOTE),
                    more("Toutes nos formations", "/#courses"),
                ], flex_direction="row", flex_wrap="wrap", flex_align_items="center", flex_gap=gap(28),
                    _margin=dims(8, 0, 0, 0)),
            ], flex_gap=gap(18), **anim("fadeInUp", 0, True)),
            image(img_key, 420, height_m=260, radius=None, alt="",
                  image_border_radius=dims(6, 6, 6, 6), **{"object-position": img_pos},
                  _css_classes="rcr-page-hero-img", **anim("fadeInUp", 150)),
        ], "minmax(0,1.1fr) minmax(0,1fr)", cols_t="1fr", g=56, grid_align_items="center",
            width=px(100, "%")),
    ], padding=dims(90, 32, 90, 32), padding_tablet=dims(70, 32, 70, 32), padding_mobile=dims(50, 20, 60, 20),
        background_background="classic", background_color=SKY, css_classes="rcr-page-hero", html_tag="section")


def narrow(children, width=820, **s):
    return con(children, width=px(width), width_mobile=px(100, "%"), width_tablet=px(100, "%"), **s)


def cta_band():
    return section([
        con([
            h2("Prêt à organiser une formation ?", "#FFFFFF", "center"),
            text("<p>Que vous soyez une entreprise, un organisme ou un groupe privé, communiquez avec nous pour "
                 "vérifier nos disponibilités et obtenir une soumission adaptée à vos besoins.</p>",
                 17, "#C9D3E5", 1.65, align="center", _css_classes="rcr-on-dark"),
            con([
                button("Demander une soumission", QUOTE),
                button("(450) 374-7995", "tel:4503747995", shadow_on=False, background_color="rgba(0,0,0,0)",
                       button_background_hover_color="#FFFFFF", hover_color=NAVY, border_border="solid",
                       border_width=dims(2, 2, 2, 2), border_color="#FFFFFF"),
            ], flex_direction="row", flex_wrap="wrap", flex_justify_content="center", flex_gap=gap(16),
                _margin=dims(8, 0, 0, 0)),
        ], flex_gap=gap(18), flex_align_items="center", width=px(760), width_mobile=px(100, "%"),
            **anim("fadeInUp", 0, True)),
    ], padding=dims(90, 32, 90, 32), padding_mobile=dims(64, 20, 64, 20), flex_align_items="center",
        background_background="classic", background_color=DEEP, css_classes="rcr-cta", html_tag="section")


def strip_none(o):
    if isinstance(o, dict):
        return {k: strip_none(v) for k, v in o.items() if v is not None}
    if isinstance(o, list):
        return [strip_none(v) for v in o if v is not None]
    return o


# --------------------------------------------------------------------------- home page
def update_home(tree):
    tree = copy.deepcopy(tree)
    idx, parent = index(tree)

    def S(eid):
        return idx[eid]["settings"]

    def remove(eid):
        p = parent[eid]
        siblings = p["elements"] if p else tree
        siblings[:] = [e for e in siblings if e["id"] != eid]

    # 0. anchors used by the menu
    S("65fb1d6")["_element_id"] = "about"

    # 1. no more links to the other site's booking platform
    for eid in ("0b400f1", "6c6341a"):
        S(eid)["link"] = {"url": "#quote", "is_external": "", "nofollow": ""}

    # 2. Services: one Cardio-secours card (levels A + C) and the SIR card
    remove("cb2c8bf")                                   # Heartsaver · Niveau A
    S("2d8bbf8")["image"] = {"url": image("cpr")["settings"]["image"]["url"], "id": 10, "alt": "",
                             "source": "library"}
    S("8e40441")["title"] = "Cardio-secours"
    S("73a5a88")["editor"] = (
        "<p><strong>RCR, DEA et désobstruction des voies respiratoires.</strong> Devenez un maillon fort de "
        "la chaîne de survie. Accessible sans prérequis médical, au travail comme dans la vie quotidienne. "
        f"Niveau{N}A (adulte, 2{N}h) ou niveau{N}C (adulte, enfant et nourrisson, 3{N}h{N}30).</p>")
    S("7977d41")["link"] = {"url": CARDIO_URL, "is_external": "", "nofollow": ""}
    S("dc66bea")["title"] = f"Soins immédiats en réanimation{N}(SIR)"
    S("8482a9b")["editor"] = (
        "<p><strong>Une formation destinée aux professionnels de la santé.</strong> Reconnaître rapidement un "
        "arrêt cardiorespiratoire et intervenir efficacement, seul ou au sein d’une équipe de réanimation. "
        f"Théorie, pratique et simulations. Durée indicative{N}: 4{N}à{N}5{N}h.</p>")
    S("897455b")["link"] = {"url": SIR_URL, "is_external": "", "nofollow": ""}
    grid_s = S("1bb3574")
    grid_s["grid_columns_grid"] = {"unit": "fr", "size": 2, "sizes": []}
    grid_s["grid_columns_grid_tablet"] = {"unit": "fr", "size": 2, "sizes": []}
    grid_s["width"] = px(940)
    grid_s["width_tablet"] = px(100, "%")
    grid_s["width_mobile"] = px(100, "%")

    # 3. "Ce que vous apprendrez": 4 round images, no numbers, click reveals the basics
    steps = [
        ("9bdce9e", "549668f", "a3942d1", "158340c", "aaf8f4b", "f8fdcb2", 7, "center right", "Anaphylaxie",
         "Une réaction allergique grave peut survenir en quelques minutes.",
         "<p>Reconnaissez les signes : difficulté à respirer, gonflement de la gorge, malaise ou urticaire "
         "généralisée. Administrez rapidement l’épinéphrine avec un auto-injecteur et appelez le 911.</p>"),
        ("2dec292", "53dc714", "f4e53a2", "b69494f", "bd5bfbb", "6a99e31", 10, "center center", "RCR",
         "Chaque seconde compte lors d’un arrêt cardiaque.",
         "<p>Si une personne est inconsciente et ne respire pas normalement, appelez le 911, commencez la RCR "
         "et demandez un DEA. Agir rapidement peut sauver une vie.</p>"),
        ("d2da309", "c7f3a36", "3172cdd", "c847254", "cb13603", "d6b200a", 11, "center center", "Naloxone",
         "Un médicament qui peut renverser temporairement une surdose d’opioïdes.",
         "<p>En cas de suspicion de surdose, appelez le 911, administrez la naloxone selon les instructions et "
         "surveillez la respiration. Une autre dose peut être nécessaire.</p>"),
        ("831cf49", "6578ca3", "dbb8121", "c4a0a41", "baead61", "1971198", 8, "center center", "Étouffement",
         "Une obstruction des voies respiratoires peut devenir rapidement grave.",
         "<p>Si la personne ne peut plus parler, respirer ou tousser efficacement, intervenez avec les manœuvres "
         "adaptées à son âge et appelez le 911.</p>"),
    ]
    files = {7: "epipen-training-mannequin.webp", 10: "rcr-rive-sud-cpr-instructor.webp",
             11: "naloxone-overdose-response.webp", 8: "heimlich-choking-rescue.webp"}
    for col, wrap, img, num, ttl, body, iid, pos, title, lead, more_html in steps:
        remove(num)
        si = S(img)
        si["image"] = {"url": f"https://rcr-rive-sud.wsdfy.com/wp-content/uploads/2026/11/{files[iid]}",
                       "id": iid, "alt": "", "source": "library"}
        si["object-position"] = pos
        si["_css_classes"] = "rcr-step-img rcr-step-trigger"
        S(ttl)["title"] = title
        S(body)["editor"] = f"<p>{lead}</p>"
        idx[col]["elements"].append(toggle("En savoir plus", more_html + DISCLAIMER))
        S(col)["css_classes"] = "rcr-step"
    S("f264fff")["editor"] = ("<p>Cliquez sur une image pour découvrir les gestes de base. Nos formations vous "
                              "permettent de les pratiquer sur mannequin, en mises en situation réalistes.</p>")

    # 4. Trainer: experience as paragraphs, not separate titles
    box = idx["33bd2d6"]
    box["elements"] = [idx["51b4617"], text(
        "<p>Fethi Boudebza est un formateur agréé par la Fondation des maladies du cœur et de l’AVC du Canada. "
        "Certifié depuis 2017, il possède plusieurs années d’expérience en réanimation cardiorespiratoire et en "
        "formation clinique.</p>"
        "<p>Il a notamment exercé les fonctions de chef d’équipe du code bleu à l’Hôpital Douglas. Il a également "
        "formé du personnel en RCR, en premiers soins et en intervention lors d’urgences vitales. De plus, il a "
        "assuré la formation en réanimation cardiorespiratoire du personnel infirmier de l’Institut "
        "<span style=\"white-space:nowrap\">Philippe-Pinel</span> de Montréal.</p>"
        "<p>Infirmier praticien spécialisé (IPS), il possède également une expérience clinique en soins aigus à "
        "l’Hôpital général juif. Il a par ailleurs enseigné les soins infirmiers au Cégep "
        "<span style=\"white-space:nowrap\">André-Laurendeau</span>.</p>",
        15, TEXT2, 1.7, _css_classes="rcr-exp-text")]
    S("a1796a6")["editor"] = ("<p>Son expérience clinique et pédagogique lui permet d’offrir un encadrement "
                              "rigoureux, axé sur la pratique et adapté aux besoins des participants.</p>")

    # 5. Fethi's photo less bright (both photos)
    for eid in ("4ef95f5", "6cd122e"):
        S(eid).update({"css_filters_css_filter": "custom", "css_filters_brightness": px(88),
                       "css_filters_contrast": px(104), "css_filters_saturate": px(96)})

    # 6. Certification: Cardio-secours / Soins immédiats en réanimation
    S("3bdfd69")["title"] = "Cardio-secours"
    S("5b23c77")["title"] = "Soins immédiats en réanimation"
    card_txt = ("<p>Les participants qui satisfont aux exigences du programme reçoivent une carte d’attestation de "
                "la Fondation des maladies du cœur et de l’AVC du Canada.</p>")
    S("70153d5")["editor"] = card_txt
    S("03b39f4")["editor"] = card_txt
    S("a2874e1")["title"] = f"Selon le programme SIR{N}applicable"

    # 7. Blog section removed (client request); FAQ section takes its place
    remove("e5952c3")
    tree.append(faq_section())
    return tree


FAQ = [
    ("RCR", [
        ("Qu’est-ce que la RCR ?", "La réanimation cardiorespiratoire (RCR) est une technique de premiers secours qui "
         "permet de maintenir une circulation sanguine et un apport d’oxygène aux organes lorsqu’une personne est en "
         "arrêt cardiaque."),
        ("Quand faut-il commencer la RCR ?", "Lorsqu’une personne est inconsciente et ne respire pas normalement. "
         "Appelez le 911 et commencez immédiatement la RCR selon votre formation et les consignes du répartiteur."),
        ("Pourquoi chaque seconde compte-t-elle ?", "Parce que le cerveau et les autres organes sont rapidement privés "
         "d’oxygène lors d’un arrêt cardiaque. Une intervention rapide augmente les chances de survie."),
        ("Peut-on pratiquer la RCR sans formation ?", "Oui. Le répartiteur du 911 peut vous guider par téléphone. Il "
         "est toutefois recommandé de suivre une formation pratique pour acquérir les bons réflexes."),
    ]),
    ("DEA", [
        ("Qu’est-ce qu’un DEA ?", "Un défibrillateur externe automatisé est un appareil qui analyse le rythme cardiaque "
         "et détermine si un choc électrique est nécessaire."),
        ("Qui peut utiliser un DEA ?", "Les DEA sont conçus pour être utilisés par le grand public. L’appareil donne "
         "des instructions vocales simples pour guider l’intervention."),
        ("Le DEA peut-il être dangereux ?", "Lorsqu’il est utilisé conformément à ses instructions, le DEA est "
         "sécuritaire. Il faut simplement s’assurer que personne ne touche la victime pendant l’analyse et "
         "l’administration éventuelle du choc."),
        ("Faut-il continuer la RCR après l’utilisation du DEA ?", "Oui. Reprenez immédiatement la RCR lorsque "
         "l’appareil vous le demande et poursuivez jusqu’à l’arrivée des secours ou jusqu’à ce que la personne montre "
         "des signes de vie."),
    ]),
    ("Étouffement", [
        ("Comment reconnaître un étouffement ?", "Une personne qui s’étouffe peut avoir de la difficulté à respirer, ne "
         "plus être capable de parler ou de tousser efficacement, et parfois porter les mains à son cou."),
        ("Que faire si la personne tousse encore efficacement ?", "Encouragez-la à continuer de tousser et surveillez "
         "son état. Une toux efficace peut permettre d’expulser l’objet."),
        ("Que faire en cas d’obstruction grave ?", "Intervenez rapidement en appliquant les manœuvres de désobstruction "
         "adaptées à l’âge et à la condition de la personne, selon votre formation et les recommandations en vigueur."),
        ("Que faire si la personne perd connaissance ?", "Appelez le 911, commencez la RCR selon votre formation et "
         "suivez les instructions du répartiteur."),
    ]),
    ("Anaphylaxie", [
        ("Qu’est-ce que l’anaphylaxie ?", "L’anaphylaxie est une réaction allergique grave et potentiellement mortelle "
         "qui nécessite une intervention immédiate."),
        ("Quels sont les signes à reconnaître ?", "Les symptômes peuvent comprendre une difficulté respiratoire, un "
         "gonflement de la langue ou de la gorge, de l’urticaire, des étourdissements ou une chute de pression "
         "artérielle."),
        ("Quel est le traitement de première intention ?", "L’épinéphrine (adrénaline) est le traitement de première "
         "intention. Elle doit être administrée rapidement à l’aide d’un auto-injecteur lorsqu’une anaphylaxie est "
         "suspectée."),
        ("Faut-il appeler le 911 après l’administration d’épinéphrine ?", "Oui. Même si la personne semble aller "
         "mieux, une évaluation médicale urgente est nécessaire."),
    ]),
    ("EpiPen", [
        ("À quoi sert un EpiPen ?", "L’EpiPen est un auto-injecteur qui permet d’administrer rapidement une dose "
         "d’épinéphrine lors d’une réaction allergique grave."),
        ("Où faut-il administrer l’injection ?", "Dans la face extérieure de la cuisse, conformément aux instructions "
         "du dispositif."),
        ("Peut-on administrer l’EpiPen à travers les vêtements ?", "Certains modèles permettent l’administration à "
         "travers les vêtements. Il faut toujours suivre les instructions du fabricant."),
        ("Que faire après l’injection ?", "Appelez le 911, surveillez la personne et suivez les recommandations des "
         "secours. Une deuxième dose peut être nécessaire selon l’évolution de la situation et les instructions "
         "médicales ou du dispositif."),
    ]),
    ("Naloxone", [
        ("Qu’est-ce que la naloxone ?", "La naloxone est un médicament qui peut renverser temporairement les effets "
         "d’une surdose d’opioïdes, notamment en aidant à rétablir la respiration."),
        ("Comment reconnaître une possible surdose d’opioïdes ?", "La personne peut être inconsciente ou difficile à "
         "réveiller, respirer très lentement ou ne plus respirer, et présenter des pupilles très petites."),
        ("Que faire si vous soupçonnez une surdose ?", "Appelez immédiatement le 911, administrez la naloxone selon les "
         "instructions du dispositif et donnez les soins respiratoires ou la RCR selon votre formation."),
        ("Une seule dose suffit-elle toujours ?", "Non. Une dose supplémentaire peut être nécessaire après 2 à "
         "3 minutes si la personne ne répond pas ou si les symptômes persistent, conformément aux instructions du "
         "produit et au protocole applicable."),
        ("La naloxone remplace-t-elle les soins médicaux ?", "Non. Son effet peut être temporaire et elle agit "
         "uniquement contre les opioïdes. La personne doit recevoir une assistance médicale urgente et être "
         "surveillée."),
    ]),
    ("Soins immédiats en réanimation (SIR)", [
        ("Qu’est-ce que le SIR ?", "Les soins immédiats en réanimation regroupent les interventions essentielles à "
         "effectuer lorsqu’une personne présente une urgence vitale, notamment un arrêt cardiaque."),
        ("Quels sont les premiers gestes à poser ?", "Vérifiez la sécurité des lieux, évaluez l’état de conscience et "
         "la respiration, demandez de l’aide et appelez le 911. Commencez les interventions appropriées selon votre "
         "formation."),
        ("Pourquoi suivre une formation en SIR ?", "Parce qu’elle permet de reconnaître rapidement une urgence, "
         "d’intervenir avec confiance et de contribuer à sauver des vies."),
    ]),
    ("RCR pédiatrique", [
        ("La RCR est-elle différente chez l’enfant et le nourrisson ?", "Oui. Les techniques, la profondeur des "
         "compressions et certaines étapes diffèrent selon l’âge et la taille de la victime."),
        ("Pourquoi est-il important de connaître la RCR pédiatrique ?", "Parce que les urgences cardiorespiratoires "
         "chez les enfants et les nourrissons peuvent nécessiter des interventions adaptées à leur développement."),
        ("Que faire si un enfant ou un nourrisson ne respire pas normalement ?", "Appelez le 911, demandez un DEA et "
         "commencez les manœuvres de réanimation adaptées à son âge, selon votre formation et les consignes du "
         "répartiteur."),
    ]),
]


def fr_punct(s):
    return s.replace(" ?", N + "?").replace(" :", N + ":").replace(" ;", N + ";").replace("2 à 3 minutes",
                                                                                         f"2{N}à{N}3{N}minutes")


def faq_section():
    blocks = []
    for i, (topic, qa) in enumerate(FAQ):
        blocks.append(con([
            heading(topic, "h3", 20, NAVY, "700", MONT, lh=1.3, _padding=dims(0, 0, 4, 0)),
            accordion([(fr_punct(q), fr_punct(a)) for q, a in qa]),
        ], flex_gap=gap(14), **anim("fadeInUp", (i % 2) * 120, True)))
    why = con([
        heading("Pourquoi suivre une formation" + N + "?", "h3", 26, "#FFFFFF", "800", MONT, lh=1.25, size_m=22),
        text("<p>Une urgence peut survenir à la maison, au travail, à l’école ou dans un lieu public. Savoir "
             "reconnaître les signes d’une situation critique et connaître les bons gestes peut faire toute la "
             "différence.</p><p>Se former, c’est être mieux préparé, agir avec confiance et contribuer à sauver des "
             "vies. Nos formations vous permettent de développer les connaissances et les habiletés nécessaires pour "
             "intervenir efficacement lors d’une situation d’urgence.</p>", 16, "#C9D3E5", 1.7,
             _css_classes="rcr-on-dark"),
        button("Demander une soumission", "#quote", _margin=dims(6, 0, 0, 0)),
    ], flex_gap=gap(16), padding=dims(40, 40, 40, 40), padding_mobile=dims(30, 22, 30, 22),
        background_background="classic", background_color=NAVY, grid_column="custom", grid_column_custom="1 / -1",
        css_classes="rcr-why", **anim("fadeInUp", 0, True))
    return section([
        con([
            eyebrow("FAQ", align="center"),
            h2("Questions fréquentes", align="center"),
            text("<p>Les réponses aux questions les plus courantes sur la RCR, le DEA, l’étouffement, l’anaphylaxie "
                 "et la naloxone. Information générale : en situation d’urgence, appelez le 911.</p>", 16, MUTED,
                 1.65, align="center"),
        ], flex_gap=gap(14), flex_align_items="center", width=px(760), width_mobile=px(100, "%"),
            **anim("fadeInUp", 0, True)),
        grid(blocks + [why], 2, cols_t=1, g=32, row_g=40, width=px(100, "%"), grid_align_items="start"),
    ], _element_id="faq", flex_gap=gap(56), flex_align_items="center", **SECTION_PAD,
        background_background="classic", background_color="#FFFFFF", css_classes="rcr-faq-section",
        html_tag="section")


# --------------------------------------------------------------------------- course pages
def info_card(title, body, delay=0):
    return card([
        heading(title, "h3", 18, INK, "700", MONT, lh=1.3),
        text(f"<p>{body}</p>", 15, MUTED, 1.65),
    ], padding=dims(30, 28, 30, 28), flex_gap=gap(10), css_classes="rcr-fcard", **anim("fadeInUp", delay, True))


def page_cardio():
    level = lambda lvl, dur, p1, p2, ic, delay: card([  # noqa: E731
        con([icon(ic, RED, 24, stacked=True, bg=PINK, pad=13),
             heading(lvl, "h3", 21, INK, "700", MONT, lh=1.3)],
            flex_direction="row", flex_align_items="center", flex_gap=gap(14),
            flex_wrap_mobile="nowrap", flex_wrap_tablet="nowrap"),
        heading(dur, "div", 13, RED, "700", MONT, lh=1.4, ls=0.6, tt="uppercase"),
        text(f"<p>{p1}</p><p>{p2}</p>", 15.5, MUTED, 1.7),
    ], padding=dims(34, 30, 34, 30), flex_gap=gap(14), border_border="solid", border_width=dims(4, 0, 0, 0),
        border_color=RED, css_classes="rcr-fcard", **anim("fadeInUp", delay, True))
    learn = [
        ("Reconnaître les urgences", "Repérer les signes d’un arrêt cardiaque et reconnaître certaines situations "
         "critiques, selon le programme suivi."),
        ("Effectuer une RCR de qualité", "Pratiquer les compressions thoraciques et les ventilations appropriées."),
        ("Utiliser un DEA", "Apprendre à utiliser un défibrillateur externe automatisé de manière sécuritaire."),
        ("Intervenir en cas d’étouffement", "Appliquer les techniques appropriées de désobstruction des voies "
         "respiratoires."),
        ("Développer vos réflexes", "Pratiquer les gestes essentiels sur des mannequins et participer à des mises en "
         "situation."),
    ]
    return [
        page_hero("Formation Cœur + AVC", "Cardio-secours",
                  "RCR, défibrillateur externe automatisé (DEA) et désobstruction des voies respiratoires",
                  "Devenez un maillon fort de la chaîne de survie.", "cpr"),
        section([
            narrow([
                text("<p>La formation Cardio-secours de Cœur + AVC vous apprend à reconnaître un arrêt cardiaque et à "
                     "intervenir rapidement grâce aux techniques de réanimation cardiorespiratoire (RCR), à "
                     "l’utilisation d’un défibrillateur externe automatisé (DEA) et aux manœuvres de désobstruction "
                     "des voies respiratoires.</p><p>Accessible sans prérequis médical, cette formation s’adresse aux "
                     "personnes qui souhaitent acquérir les compétences essentielles pour intervenir en situation "
                     "d’urgence, tant au travail que dans la vie quotidienne.</p>", 18, TEXT2, 1.75, size_m=16.5),
            ], **anim("fadeInUp", 0, True)),
            con([
                h2("Choisissez le niveau adapté à vos besoins", align="center"),
            ], flex_align_items="center", width=px(760), width_mobile=px(100, "%"), _margin=dims(30, 0, 0, 0),
                **anim("fadeInUp", 0, True)),
            grid([
                level(f"Niveau{N}A — Adulte", f"Durée indicative{N}: 2{N}heures en classe",
                      "Cette formation porte sur la RCR et les interventions auprès des adultes.",
                      "Elle convient particulièrement aux milieux de travail où les interventions concernent "
                      "principalement des adultes, notamment les bureaux, les commerces et certains environnements "
                      "industriels.", "svg:course-heartsaver-a", 0),
                level(f"Niveau{N}C — Adulte, enfant et nourrisson", f"Durée indicative{N}: 3{N}h{N}30 en classe",
                      "Cette formation couvre les interventions auprès des personnes de tous âges : adultes, enfants "
                      "et nourrissons.",
                      "Elle convient particulièrement aux parents, au personnel des garderies et des écoles, aux "
                      "entraîneurs sportifs ainsi qu’aux professionnels de la santé qui souhaitent acquérir des "
                      "compétences en RCR pédiatrique.", "svg:course-heartsaver-c", 150),
            ], 2, cols_t=1, g=28, width=px(100, "%")),
        ], flex_gap=gap(40), flex_align_items="center", **SECTION_PAD, html_tag="section"),
        section([
            con([h2("Ce que vous apprendrez", align="center")], flex_align_items="center",
                **anim("fadeInUp", 0, True)),
            grid([info_card(t, b, (i % 3) * 120) for i, (t, b) in enumerate(learn)], 3, cols_t=2, g=24,
                 width=px(100, "%")),
        ], flex_gap=gap(40), flex_align_items="center", **SECTION_PAD, background_background="classic",
            background_color=PALE, html_tag="section"),
        cta_band(),
    ]


def page_sir():
    skills = [
        "Reconnaître un arrêt cardiorespiratoire et activer le système d’intervention d’urgence.",
        "Pratiquer une RCR de haute qualité chez l’adulte, l’enfant et le nourrisson, selon le programme applicable.",
        "Effectuer des ventilations efficaces à l’aide des dispositifs de protection appropriés et d’un ballon-masque.",
        "Utiliser un défibrillateur externe automatisé (DEA).",
        "Appliquer les manœuvres de désobstruction des voies respiratoires en cas d’étouffement.",
        "Coordonner les interventions et collaborer efficacement au sein d’une équipe de réanimation.",
        "Utiliser la naloxone lors de dépressions respiratoires secondaires aux opioïdes.",
    ]
    practice = [
        ("Encadrement par un instructeur", "Les exercices en personne permettent aux participants de pratiquer les "
         "gestes essentiels et de recevoir des conseils personnalisés pour améliorer leur technique."),
        ("Rétroaction sur les compressions thoraciques", "Selon le matériel disponible, des mannequins dotés de "
         "dispositifs de rétroaction peuvent être utilisés afin d’aider les participants à améliorer la qualité de "
         "leurs compressions thoraciques."),
        ("Simulations cliniques", "Des mises en situation permettent de s’exercer à reconnaître une urgence et à "
         "intervenir dans un contexte proche de la réalité clinique."),
        ("Travail d’équipe", "Une attention particulière est accordée à la communication, à la coordination et à la "
         "répartition des rôles pendant une réanimation."),
    ]
    content = [
        "Les chaînes de survie.",
        "La RCR chez l’adulte, l’enfant et le nourrisson.",
        "La RCR pratiquée par un ou deux secouristes.",
        "Les ventilations efficaces et l’utilisation du ballon-masque.",
        "L’utilisation du DEA.",
        "Les manœuvres de désobstruction des voies respiratoires.",
        "La reconnaissance et la prise en charge initiale de certaines urgences vitales, notamment les surdoses "
        "d’opioïdes, l’anaphylaxie, la noyade et l’arrêt cardiaque pendant la grossesse.",
        "La reconnaissance des signes d’une crise cardiaque et d’un accident vasculaire cérébral (AVC).",
    ]
    return [
        page_hero("Formation Cœur + AVC", f"Soins immédiats en réanimation{N}(SIR)",
                  "Une formation destinée aux professionnels de la santé", None, "group"),
        section([
            narrow([
                text("<p>La formation en soins immédiats en réanimation (SIR) de Cœur + AVC s’adresse aux "
                     "professionnels de la santé qui doivent reconnaître rapidement un arrêt cardiorespiratoire et "
                     "intervenir efficacement, seuls ou au sein d’une équipe de réanimation.</p><p>Entièrement "
                     "dispensée en personne par un instructeur qualifié, cette formation combine des apprentissages "
                     "théoriques, des exercices pratiques et des simulations afin de développer les compétences "
                     "nécessaires à la prise en charge des urgences cardiorespiratoires.</p>", 18, TEXT2, 1.75,
                     size_m=16.5),
            ], **anim("fadeInUp", 0, True)),
            narrow([
                h2("Compétences acquises"),
                text(f"<p>Au cours de cette formation, les participants apprennent notamment à{N}:</p>", 17, MUTED,
                     1.6),
                check_list(skills),
            ], flex_gap=gap(18), padding=dims(36, 36, 36, 36), padding_mobile=dims(26, 20, 26, 20),
                background_background="classic", background_color=PALE, **anim("fadeInUp", 0, True)),
        ], flex_gap=gap(48), flex_align_items="center", **SECTION_PAD, html_tag="section"),
        section([
            con([h2("Une formation axée sur la pratique", align="center")], flex_align_items="center",
                width=px(760), width_mobile=px(100, "%"), **anim("fadeInUp", 0, True)),
            grid([info_card(t, b, (i % 2) * 120) for i, (t, b) in enumerate(practice)], 2, cols_t=2, g=24,
                 width=px(100, "%")),
        ], flex_gap=gap(40), flex_align_items="center", **SECTION_PAD, background_background="classic",
            background_color=PALE, html_tag="section"),
        section([
            narrow([
                h2("Contenu de la formation"),
                text(f"<p>Selon le programme applicable, les thèmes abordés comprennent{N}:</p>", 17, MUTED, 1.6),
                check_list(content),
                heading(f"Durée indicative{N}: de 4{N}à{N}5{N}heures", "div", 18, RED, "700", MONT, lh=1.4,
                        _margin=dims(8, 0, 0, 0)),
            ], flex_gap=gap(18), **anim("fadeInUp", 0, True)),
        ], flex_align_items="center", **SECTION_PAD, html_tag="section"),
        cta_band(),
    ]


def page_privacy():
    def sec(title, html):
        return con([heading(title, "h2", 22, INK, "700", MONT, lh=1.3), text(html, 16, TEXT2, 1.75)],
                   flex_gap=gap(10))
    ul = lambda items: "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"  # noqa: E731
    body = [
        text("<p>La protection de votre vie privée est importante pour nous. Cette politique explique comment notre "
             "site Web recueille, utilise, conserve et protège vos renseignements personnels lorsque vous le consultez "
             "ou communiquez avec nous.</p>", 17, TEXT2, 1.75),
        sec("1. Renseignements recueillis",
            f"<p>Selon les services utilisés, nous pouvons recueillir certains renseignements, notamment{N}:</p>"
            + ul([f"Votre nom et prénom{N};", f"Votre adresse courriel{N};", f"Votre numéro de téléphone{N};",
                  f"Les renseignements nécessaires à une inscription ou à une demande d’information{N};",
                  "Certaines données relatives à votre navigation sur notre site Web."])
            + "<p>Nous recueillons uniquement les renseignements nécessaires au fonctionnement de nos services et à "
              "nos communications avec vous.</p>"),
        sec("2. Utilisation des renseignements",
            f"<p>Vos renseignements personnels peuvent être utilisés pour{N}:</p>"
            + ul([f"Répondre à vos questions et demandes{N};", f"Gérer les inscriptions aux formations{N};",
                  f"Communiquer avec vous concernant nos activités{N};",
                  f"Améliorer le contenu et le fonctionnement de notre site Web{N};",
                  "Respecter nos obligations légales."])
            + "<p>Nous ne vendons ni ne louons vos renseignements personnels à des tiers.</p>"),
        sec("3. Protection et conservation des renseignements",
            "<p>Nous prenons des mesures raisonnables pour protéger vos renseignements personnels contre l’accès non "
            "autorisé, la perte, la divulgation ou l’utilisation inappropriée.</p><p>Vos renseignements sont conservés "
            "uniquement pendant la période nécessaire aux fins pour lesquelles ils ont été recueillis, sous réserve "
            "des obligations légales applicables.</p>"),
        sec("4. Témoins de connexion (cookies)",
            "<p>Notre site Web peut utiliser des témoins de connexion afin d’améliorer votre expérience de navigation, "
            "de faciliter certaines fonctionnalités et, le cas échéant, de mesurer l’achalandage du site.</p><p>Vous "
            "pouvez modifier les paramètres de votre navigateur pour limiter ou désactiver les témoins de "
            "connexion.</p>"),
        sec("5. Partage des renseignements",
            "<p>Vos renseignements personnels ne sont communiqués à des tiers que lorsque cela est nécessaire à la "
            "prestation de nos services, avec votre consentement ou lorsque la loi l’autorise.</p><p>Certains "
            "fournisseurs technologiques peuvent également traiter des renseignements pour notre compte, notamment "
            "pour l’hébergement du site Web ou la gestion des inscriptions.</p>"),
        sec("6. Vos droits",
            f"<p>Conformément aux lois applicables, vous pouvez notamment demander{N}:</p>"
            + ul([f"L’accès aux renseignements personnels que nous détenons à votre sujet{N};",
                  f"La rectification de renseignements inexacts ou incomplets{N};",
                  "Le retrait de votre consentement lorsque celui-ci constitue le fondement de leur utilisation."])
            + "<p>Pour exercer vos droits ou poser une question concernant cette politique, vous pouvez communiquer "
              "avec nous.</p>"),
        sec("7. Responsable de la protection des renseignements personnels",
            "<p>Pour toute question, demande ou préoccupation concernant la confidentialité de vos renseignements "
            f"personnels, veuillez communiquer avec notre responsable{N}:</p>"
            f"<p><strong>Nom{N}:</strong> Fethi Boudebza<br><strong>Courriel{N}:</strong> "
            "<a href=\"mailto:rcrrivesud@outlook.com\">rcrrivesud@outlook.com</a><br>"
            f"<strong>Organisation{N}:</strong> RCR Rive-Sud</p>"),
        sec("8. Modifications de la politique",
            "<p>Nous nous réservons le droit de modifier cette politique afin de tenir compte de l’évolution de nos "
            "pratiques ou des exigences légales.</p><p>Toute modification sera publiée sur cette page avec sa date de "
            "mise à jour.</p>"),
        text("<p><strong>Votre confiance est importante pour nous.</strong> Merci de visiter notre site et de "
             "contribuer à une communauté mieux informée et mieux préparée à intervenir en situation "
             "d’urgence.</p>", 16, TEXT2, 1.75),
    ]
    return [
        section([
            con([
                eyebrow("RCR Rive-Sud"),
                heading("Politique de confidentialité", "h1", 44, INK, "800", MONT, lh=1.15, size_t=38, size_m=30),
                text(f"<p>Dernière mise à jour{N}: 7{N}novembre 2026</p>", 16, MUTED, 1.6),
            ], flex_gap=gap(14), width=px(820), width_tablet=px(100, "%"), width_mobile=px(100, "%")),
        ], padding=dims(80, 32, 60, 32), padding_mobile=dims(50, 20, 40, 20), flex_align_items="center",
            background_background="classic", background_color=SKY, html_tag="section"),
        section([narrow(body, flex_gap=gap(32), css_classes="rcr-legal")],
                padding=dims(60, 32, 100, 32), padding_mobile=dims(40, 20, 70, 20), flex_align_items="center",
                html_tag="section"),
    ]


if __name__ == "__main__":
    src = json.load(open(sys.argv[1]))
    tree = src["tree"] if isinstance(src, dict) else src
    os.makedirs(OUT, exist_ok=True)
    outputs = {"home_fr": update_home(tree), "page_cardio_secours": page_cardio(), "page_sir": page_sir(),
               "page_confidentialite": page_privacy()}
    for name, data in outputs.items():
        data = strip_none(data)
        path = os.path.join(OUT, f"{name}.json")
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        print(name, os.path.getsize(path), "bytes")
