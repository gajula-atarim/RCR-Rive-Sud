#!/usr/bin/env python3
"""French inner pages built from the English designs (About, Services, Team, FAQ, Contact).

Text sources, in order of preference:
  1. the client's own French text already on the site or in the client documents
     (Cardio-secours / SIR pages, trainer paragraphs, Q&A of WebSiteUpdateCpr7Nov.docx),
  2. French strings already used on the home page (build/i18n/fr_home_strings.py),
  3. a French translation of the design copy.

Photos missing from the media library (photo-rcr-nourrisson.png, photo-rcr-mannequin.png) are left as
Elementor placeholders (image widgets) or as a plain colour (banners) until the client team sends them.

Output: build/elementor/out/page_<slug>.json, one Elementor tree per page.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from generate import (  # noqa: E402
    RED, RED_D, NAVY, INK, MUTED, TEXT2, SKY, PALE, PINK, LINE, DEEP, MONT, SANS, PLACEHOLDER,
    uid, px, dims, gap, gaps, shadow, typo, anim, con, section, grid, w, heading, eyebrow, text,
    button, more, image, icon, bg_image, overlay_gradient, photo_layer, strip_none,
)
import generate as _g  # noqa: E402

_g._counter[0] = 900000  # new ids stay clear of the ids on the live pages
_g.SVG.update({"anaphylaxis": 511, "pin": 512, "heart": 513, "pulse": 514, "cap": 515, "people": 516})

OUT = os.path.join(os.path.dirname(__file__), "out")
N = " "
TEL, MAIL = "tel:4503747995", "mailto:rcrrivesud@outlook.com"
U = {"about": "/a-propos/", "services": "/services/", "team": "/equipe/", "faq": "/faq/", "contact": "/contact/"}
CF7 = '[contact-form-7 id="505" title="Contact (FR)" html_class="rcr-cform"]'
BORDER = "#D9E0EC"
BODY_TXT = "#C9D3E5"


def fr(s):
    """No-break space before ? ! : ; and around » « (French typography). Text itself is unchanged."""
    s = re.sub(r" ([?!:;»])", N + r"\1", s)
    return s.replace("« ", "«" + N)


def nw(s):
    return f'<span style="white-space:nowrap">{s}</span>'


# --------------------------------------------------------------------------- small builders
def h(txt, tag="h3", size=17, color=INK, weight="700", **kw):
    return heading(fr(txt), tag, size, color, weight, MONT, **kw)


def p(html, size=16, color=MUTED, lh=1.75, **kw):
    if not html.startswith("<"):
        html = f"<p>{html}</p>"
    return text(fr(html), size, color, lh, **kw)


def checks(items, size=15, color=TEXT2, cols=1, divider=False, gap_px=10, **extra):
    s = {"icon_list": [{"_id": uid("li"), "text": fr(t),
                        "selected_icon": {"value": "fas fa-check", "library": "fa-solid"}} for t in items],
         "view": "traditional", "space_between": px(gap_px), "icon_color": RED, "icon_size": px(13),
         "text_color": color, "text_indent": px(10), "icon_self_vertical_align": "flex-start",
         "icon_vertical_offset": px(5), **typo("icon_typography", SANS, "400", size, 1.5)}
    if divider:
        s.update({"divider": "yes", "divider_style": "solid", "divider_weight": px(1), "divider_color": LINE,
                  "space_between": px(28)})
    cls = ["rcr-checks"] + (["rcr-check2"] if cols == 2 else [])
    s["_css_classes"] = " ".join(cls)
    s.update(extra)
    return w("icon-list", s)


def crumbs(*items):
    parts = []
    for label, url in items[:-1]:
        parts.append(f'<a href="{url}">{label}</a>' if url else label)
    parts.append(f'<span class="rcr-cur">{items[-1][0]}</span>')
    return text("<p>" + " / ".join(parts) + "</p>", 14, TEXT2, 1.5, _css_classes="rcr-crumbs")


def banner(title, crumb_items, img_key=None, xpos=70, ypos=45, height=240, h1_extra=None):
    bg = {"background_background": "classic", "background_color": "#BFD9F2"}
    if img_key:
        iid, url = _g.IMG[img_key]
        bg.update({"background_image": {"url": url, "id": iid, "size": "", "alt": "", "source": "library"},
                   "background_position": "initial", "background_xpos": px(xpos, "%"),
                   "background_ypos": px(ypos, "%"), "background_repeat": "no-repeat",
                   "background_size": "cover"})
        bg.update(overlay_gradient("rgba(191,217,242,0.96)", 40, "rgba(191,217,242,0.2)", 75, 90))
    return section([
        heading(title, "h1", 46, INK, "800", MONT, lh=1.1, size_t=40, size_m=32, **(h1_extra or {})),
        crumbs(*crumb_items),
    ], min_height=px(height), min_height_mobile=px(180), flex_justify_content="center", flex_gap=gap(10),
        padding=dims(0, 32, 0, 32), padding_mobile=dims(0, 20, 0, 20), css_classes="rcr-banner",
        html_tag="section", **bg)


def icon_circle(name, size=28, pad=18, **extra):
    return icon("svg:" + name, RED, size, stacked=True, bg=PINK, pad=pad, **extra)


def hover_lift(y=-6, sh=None):
    d = {"_transform_translateY_effect_hover": px(y), "_transform_transition_hover": px(350, "ms")}
    if sh:
        d.update({"box_shadow_hover_box_shadow_type": "yes", "box_shadow_hover_box_shadow": sh,
                  "border_hover_transition": px(0.35, "s")})
    return d


def link_con(children, url, **s):
    return con(children, html_tag="a", link={"url": url, "is_external": "", "nofollow": ""}, **s)


def hours_rows(label_color, value_color, line, size=15, pad=11):
    rows = [("Lundi au jeudi", f"9{N}h à 19{N}h"), ("Vendredi", f"9{N}h à 12{N}h"),
            ("Samedi et dimanche", f"9{N}h à 15{N}h")]
    return [con([
        heading(a, "div", size, label_color, "400", SANS, lh=1.4),
        heading(b, "div", size, value_color, "400", SANS, lh=1.4, _flex_size="none"),
    ], flex_direction="row", flex_justify_content="space-between", flex_gap=gap(16), padding=dims(pad, 0, pad, 0),
        border_border="solid", border_width=dims(0, 0, 1, 0), border_color=line) for a, b in rows]


def question_card(with_button=False):
    kids = [
        h("Une question ?", "div", 24, "#FFFFFF", "800"),
        p("Communiquez avec nous par téléphone ou par courriel pour discuter de vos besoins.", 15, "#D5DEEE", 1.55),
        heading("(450) 374-7995", "div", 20, "#FFFFFF", "800", MONT, lh=1.3, link=TEL, _margin=dims(6, 0, 0, 0),
                _css_classes="rcr-light-link"),
        heading("rcrrivesud@outlook.com", "div", 15, "#FFFFFF", "400", SANS, lh=1.4, link=MAIL,
                _css_classes="rcr-light-link"),
    ]
    if with_button:
        kids.append(button("Demander une soumission", U["contact"], size=13, pad=(12, 18), shadow_on=False,
                           _margin=dims(8, 0, 0, 0)))
    bg = bg_image("cpr", "center center")
    bg.update(background_background="classic", background_color=DEEP, background_position="initial",
              background_xpos=px(60, "%"), background_ypos=px(50, "%"))
    bg.update(overlay_gradient("rgba(7,37,83,0.92)", 0, "rgba(7,37,83,0.6)", 100, 180))
    return con(kids, min_height=px(300), padding=dims(30, 26, 30, 26), flex_gap=gap(12), **bg)


def two_col(main, aside):
    """Main column + 330px sidebar (stacks below 1025px)."""
    return grid([main, aside], "minmax(0,1fr) 330px", cols_t="1fr", cols_m=1, g=48,
                grid_align_items="start", width=px(100, "%"))


def page_section(children, **s):
    st = dict(padding=dims(80, 32, 100, 32), padding_mobile=dims(60, 20, 80, 20), html_tag="section")
    st.update(s)
    return section(children, **st)


def ph_image(alt, cls, **extra):
    """Placeholder for a photo the client team still has to send (see README)."""
    return image(None, url_override=PLACEHOLDER, alt=alt, cls=cls + " rcr-ph", **extra)


# --------------------------------------------------------------------------- À propos
def page_about():
    intro = section([
        grid([
            con([
                image("cpr", alt="Formateur démontrant les compressions thoraciques", cls="rcr-sq rcr-zoom1"),
                ph_image("Pratique de la RCR chez le nourrisson", "rcr-sq rcr-inset",
                         _position="absolute", _offset_orientation_h="end", _offset_x_end=px(0),
                         _offset_orientation_v="end", _offset_y_end=px(0), _element_width="initial",
                         _element_custom_width=px(56, "%")),
            ], padding=dims(0, 18, 22, 0, "%"), css_classes="rcr-adots", **anim("fadeInLeft", 0, True)),
            con([
                eyebrow("RCR Rive-Sud"),
                heading(f"Apprenez les bons gestes.<br>Soyez prêt à sauver une vie.", "h2", 44, INK, "800", MONT,
                        lh=1.15, size_t=38, size_m=30),
                p("RCR Rive-Sud est une entreprise privée spécialisée en formation en RCR. Notre mission est de "
                  "transmettre des connaissances pratiques et de développer les habiletés nécessaires pour intervenir "
                  "lors d’un arrêt cardiorespiratoire et contribuer à sauver des vies.", 17, INK, 1.7,
                  weight="600"),
                checks(["Grand public", "Pratique concrète", "Travailleurs", "Mises en situation réalistes",
                        "Professionnels de la santé", "Gestes d’urgence essentiels", "Étudiants en santé",
                        "En personne, sur la Rive-Sud"], cols=2),
                con([
                    image("fethi", 60, alt="Fethi Boudebza", width_pct=100, radius=50, cls="rcr-avatar",
                          _element_width="initial", _element_custom_width=px(60), _flex_size="none",
                          css_filters_css_filter="custom", css_filters_brightness=px(85),
                          css_filters_contrast=px(105)),
                    con([
                        heading("Fethi Boudebza", "div", 16, INK, "700", MONT, lh=1.3),
                        heading("Instructeur · Fondation des maladies du cœur et de l’AVC du Canada", "div", 14,
                                RED, "400", SANS, lh=1.4),
                    ], flex_gap=gap(3), _flex_size="grow", width={"unit": "custom", "size": "auto", "sizes": []}),
                    more("Voir l’équipe", U["team"], _flex_size="none"),
                ], flex_direction="row", flex_align_items="center", flex_gap=gap(16), flex_wrap_mobile="wrap",
                    padding=dims(24, 0, 0, 0), margin=dims(10, 0, 0, 0), border_border="solid",
                    border_width=dims(1, 0, 0, 0), border_color=LINE),
            ], flex_gap=gap(22), **anim("fadeInUp", 100, True)),
        ], 2, cols_t=1, cols_m=1, g=72, grid_gaps_tablet=gaps(56, 56), grid_gaps_mobile=gaps(48, 48),
            grid_align_items="center", width=px(100, "%")),
    ], padding=dims(110, 32, 120, 32), padding_tablet=dims(90, 32, 100, 32), padding_mobile=dims(70, 20, 80, 20),
        html_tag="section")

    def info(num, title, body, line, delay):
        return con([
            heading(num, "div", 30, RED, "800", MONT, lh=1),
            h(title, "h3", 21),
            p(body, 16, MUTED, 1.7),
        ], background_background="classic", background_color="#FFFFFF", padding=dims(40, 36, 40, 36),
            padding_tablet=dims(32, 24, 32, 24), flex_gap=gap(14), border_border="solid",
            border_width=dims(4, 0, 0, 0), border_color=line,
            **hover_lift(-6, shadow(0, 22, 44, 0, "rgba(11,52,112,0.12)")), **anim("fadeInUp", delay, True))

    who = section([
        grid([
            info("01", "Ce que nous offrons",
                 "RCR Rive-Sud offre des formations pratiques en réanimation cardiorespiratoire (RCR) destinées au "
                 "grand public, aux entreprises et aux professionnels de la santé. Nos formations vous permettent "
                 "d’acquérir les connaissances et les habiletés essentielles pour reconnaître une urgence vitale et "
                 "intervenir efficacement.", NAVY, 0),
            info("02", "À qui s’adressent nos formations",
                 "Nos formations s’adressent au grand public, aux travailleurs, aux professionnels de la santé et aux "
                 "personnes qui étudient dans le domaine de la santé.", RED, 100),
            info("03", "Où",
                 "Nous offrons des formations en personne, principalement sur la Rive-Sud de Montréal, avec "
                 "possibilité de déplacement dans d’autres régions sur demande.", NAVY, 200),
        ], 3, cols_t=3, cols_m=1, g=28, grid_gaps_tablet=gaps(18, 18), width=px(100, "%")),
    ], padding=dims(90, 32, 90, 32), padding_mobile=dims(70, 20, 70, 20), background_background="classic",
        background_color=PALE, html_tag="section")

    def tcard(ic, title, body, url, delay, corner=False):
        return link_con([
            icon_circle(ic, 28, 18, align="center"),
            h(title, "h3", 17, align="center", lh=1.3, _margin=dims(6, 0, 0, 0)),
            p(body, 14, MUTED, 1.6, align="center"),
            heading("Lire la suite →", "div", 12, NAVY, "700", MONT, lh=1, ls=0.7, tt="uppercase",
                    _css_classes="rcr-pill"),
        ], url, background_background="classic", background_color="#FFFFFF", padding=dims(36, 26, 30, 26),
            flex_align_items="center", flex_gap=gap(12), overflow="hidden",
            css_classes="rcr-tcard" + (" rcr-corner" if corner else ""),
            **hover_lift(-8, shadow(0, 24, 44, 0, "rgba(0,0,0,0.3)")), **anim("fadeInUp", delay, True))

    s = U["services"]
    training = section([
        con([
            heading("Nos formations", "h2", 42, "#FFFFFF", "800", MONT, lh=1.15, size_t=38, size_m=30),
            p("Notre approche mise sur la pratique, des mises en situation réalistes et l’apprentissage des gestes "
              "essentiels qui peuvent faire toute la différence en situation d’urgence.", 16, BODY_TXT, 1.65),
        ], flex_gap=gap(14), width=px(620), width_mobile=px(100, "%"), **anim("fadeInUp", 0, True)),
        grid([
            tcard("course-heartsaver-a", "Cardio-secours · Niveau A",
                  f"RCR et interventions chez l’adulte. Environ 2{N}h.", s + "#cardio-secours", 0),
            tcard("people", "Cardio-secours · Niveau C",
                  f"Adultes, enfants et nourrissons. Environ 3{N}h{N}30.", s + "#cardio-secours", 100),
            tcard("course-bls", "Soins immédiats en réanimation (SIR)",
                  f"Pour les professionnels de la santé. Environ 4{N}à{N}5{N}h.", s + "#sir", 200, corner=True),
            tcard("anaphylaxis", "Module complémentaire : anaphylaxie",
                  f"Sur demande. Format court (1{N}h{N}30) ou détaillé (4{N}h).", s + "#anaphylaxie", 0),
            tcard("feature-on-site", "Formation sur place",
                  "Vous choisissez le lieu ; nous nous occupons de la formation.", s + "#sur-place", 100),
            tcard("feature-groups", f"Groupes de 3{N}à{N}12",
                  "Participation active et encadrement adapté à votre groupe.", s + "#sur-place", 200),
        ], 3, cols_t=2, cols_m=1, g=24, width=px(100, "%")),
    ], flex_gap=gap(48), padding=dims(100, 32, 110, 32), padding_mobile=dims(70, 20, 80, 20),
        background_background="classic", background_color=DEEP,
        **bg_image("hexband", "center center", "initial", "fixed"), background_bg_width=px(1900),
        css_classes="rcr-courses", html_tag="section")

    return [banner("À propos", [("Accueil", "/"), ("À propos", None)], "mannequin", 70, 45, 240),
            intro, who, training]


# --------------------------------------------------------------------------- Services
SERVICES = [  # anchor, label (pills, sidebar, previous/next)
    ("cardio-secours", "Cardio-secours"),
    ("sir", "Soins immédiats en réanimation (SIR)"),
    ("anaphylaxie", "Module anaphylaxie"),
    ("sur-place", "Formation sur place"),
    ("tarifs", "Tarifs et soumissions"),
]


def acc(title, items):
    return con([
        h(title, "h3", 24, weight="800"),
        w("accordion", {
            "tabs": [{"_id": uid("a"), "tab_title": fr(f"{i + 1:02d}. {t}"), "tab_content": fr(f"<p>{d}</p>")}
                     for i, (t, d) in enumerate(items)],
            "selected_icon": {"value": "fas fa-plus", "library": "fa-solid"},
            "selected_active_icon": {"value": "fas fa-minus", "library": "fa-solid"},
            "title_html_tag": "div", "icon_align": "right", "border_width": px(0),
            "title_background": "rgba(0,0,0,0)", "title_color": INK, "tab_active_color": RED,
            "icon_color": RED, "icon_active_color": RED, "icon_space": px(16),
            "title_padding": dims(16, 20, 16, 20), "content_padding": dims(0, 20, 18, 20),
            "content_background_color": "rgba(0,0,0,0)", "content_color": TEXT2,
            "_css_classes": "rcr-acc",
            **typo("title_typography", MONT, "700", 15, 1.4),
            **typo("content_typography", SANS, "400", 15, 1.65),
        }),
    ], flex_gap=gap(12), margin=dims(8, 0, 0, 0))


def level_card(title, duration, items, line):
    return con([
        h(title, "h3", 16),
        heading(fr(duration), "div", 13, RED, "700", SANS, lh=1.4, ls=0.8, tt="uppercase"),
        checks(items, 15),
    ], background_background="classic", background_color=PALE, padding=dims(24, 24, 24, 24), flex_gap=gap(10),
        border_border="solid", border_width=dims(3, 0, 0, 0), border_color=line,
        **hover_lift(-4, shadow(0, 16, 32, 0, "rgba(11,52,112,0.1)")))


def panel(anchor, children):
    return con(children, _element_id=anchor, flex_gap=gap(28), css_classes="rcr-svc-panel")


def page_services():
    cardio = panel("cardio-secours", [
        heading("Cardio-secours", "h2", 38, INK, "800", MONT, lh=1.2, size_m=28),
        p("<p><strong>RCR, défibrillateur externe automatisé (DEA) et désobstruction des voies respiratoires.</strong> "
          "La formation Cardio-secours de Cœur + AVC vous apprend à reconnaître un arrêt cardiaque et à intervenir "
          "rapidement grâce aux techniques de réanimation cardiorespiratoire (RCR), à l’utilisation d’un "
          "défibrillateur externe automatisé (DEA) et aux manœuvres de désobstruction des voies respiratoires.</p>"),
        ph_image("Compressions thoraciques sur un mannequin de RCR", "rcr-169"),
        h("Aperçu", "h3", 24, weight="800"),
        p("<p><strong>Devenez un maillon fort de la chaîne de survie.</strong> Accessible sans prérequis médical, "
          "cette formation s’adresse aux personnes qui souhaitent acquérir les compétences essentielles pour "
          "intervenir en situation d’urgence, tant au travail que dans la vie quotidienne.</p>",
          _margin=dims(-12, 0, 0, 0)),
        h("Choisissez le niveau adapté à vos besoins", "h3", 19),
        grid([
            level_card("Niveau A — Adulte", "Durée indicative : 2 heures en classe",
                       ["RCR et interventions auprès des adultes",
                        "Milieux de travail où les interventions concernent principalement des adultes",
                        "Bureaux, commerces et certains environnements industriels"], NAVY),
            level_card("Niveau C — Adulte, enfant et nourrisson", f"Durée indicative : 3{N}h{N}30 en classe",
                       ["Interventions auprès des personnes de tous âges",
                        "Parents, personnel des garderies et des écoles, entraîneurs sportifs",
                        "Professionnels de la santé souhaitant acquérir des compétences en RCR pédiatrique"], RED),
        ], 2, cols_t=2, cols_m=1, g=24, width=px(100, "%"), _margin=dims(-12, 0, 0, 0)),
        grid([
            con([
                h("Certification", "h3", 20, "#FFFFFF"),
                p("Les participants qui satisfont aux exigences du programme reçoivent une carte d’attestation de "
                  "Cœur + AVC. La durée de validité indiquée est de deux ans, sous réserve des conditions "
                  "applicables à la certification concernée.", 15, BODY_TXT, 1.65),
            ], flex_gap=gap(10)),
            image("cpr", alt="", cls="rcr-43"),
        ], 2, cols_t=2, cols_m=1, g=24, grid_align_items="center", background_background="classic",
            background_color=DEEP, padding=dims(28, 28, 28, 28)),
        acc("Ce que vous apprendrez", [
            ("Reconnaître les urgences", "Repérer les signes d’un arrêt cardiaque et reconnaître certaines "
             "situations critiques, selon le programme suivi."),
            ("Effectuer une RCR de qualité", "Pratiquer les compressions thoraciques et les ventilations "
             "appropriées."),
            ("Utiliser un DEA", "Apprendre à utiliser un défibrillateur externe automatisé de manière sécuritaire."),
            ("Intervenir en cas d’étouffement", "Appliquer les techniques appropriées de désobstruction des voies "
             "respiratoires."),
            ("Développer vos réflexes", "Pratiquer les gestes essentiels sur des mannequins et participer à des "
             "mises en situation."),
        ]),
    ])

    def chip(big, small, bg, color):
        return con([heading(big, "div", 22, color, "800", MONT, lh=1.2),
                    heading(fr(small), "div", 13, TEXT2, "400", SANS, lh=1.4)],
                   background_background="classic", background_color=bg, padding=dims(14, 20, 14, 20),
                   flex_gap=gap(2), width={"unit": "custom", "size": "auto", "sizes": []})

    sir = panel("sir", [
        heading("Soins immédiats en réanimation (SIR)", "h2", 38, INK, "800", MONT, lh=1.2, size_m=28),
        p("<p><strong>Une formation destinée aux professionnels de la santé.</strong> La formation en soins immédiats "
          "en réanimation (SIR) de Cœur + AVC s’adresse aux professionnels de la santé qui doivent reconnaître "
          "rapidement un arrêt cardiorespiratoire et intervenir efficacement, seuls ou au sein d’une équipe de "
          "réanimation.</p>"),
        image("ballon", alt="RCR avec ballon-masque", cls="rcr-169"),
        h("Aperçu", "h3", 24, weight="800"),
        p("Entièrement dispensée en personne par un instructeur qualifié, cette formation combine des apprentissages "
          "théoriques, des exercices pratiques et des simulations afin de développer les compétences nécessaires à "
          "la prise en charge des urgences cardiorespiratoires.", _margin=dims(-12, 0, 0, 0)),
        con([chip(f"4{N}à{N}5{N}h", "durée indicative", PINK, RED),
             chip(f"1{N}an", "validité de la certification, selon le programme SIR applicable", SKY, NAVY)],
            flex_direction="row", flex_wrap="wrap", flex_gap=gap(16)),
        grid([
            con([h("Compétences acquises", "div", 16),
                 checks(["Reconnaître un arrêt cardiorespiratoire et activer le système d’intervention d’urgence.",
                         "Pratiquer une RCR de haute qualité chez l’adulte, l’enfant et le nourrisson, selon le "
                         "programme applicable.",
                         "Effectuer des ventilations efficaces à l’aide des dispositifs de protection appropriés et "
                         "d’un ballon-masque.",
                         "Utiliser un défibrillateur externe automatisé (DEA).",
                         "Appliquer les manœuvres de désobstruction des voies respiratoires en cas d’étouffement.",
                         "Coordonner les interventions et collaborer efficacement au sein d’une équipe de "
                         "réanimation.",
                         "Utilisation de Naloxone lors de dépression respiratoire secondaires aux opiodes"])],
                flex_gap=gap(10)),
            con([h("Contenu de la formation", "div", 16),
                 checks(["Les chaînes de survie.", "La RCR chez l’adulte, l’enfant et le nourrisson.",
                         "La RCR pratiquée par un ou deux secouristes.",
                         "Les ventilations efficaces et l’utilisation du ballon-masque.", "L’utilisation du DEA.",
                         "Les manœuvres de désobstruction des voies respiratoires.",
                         "La reconnaissance et la prise en charge initiale de certaines urgences vitales, notamment "
                         "les surdoses d’opioïdes, l’anaphylaxie, la noyade et l’arrêt cardiaque pendant la "
                         "grossesse.",
                         "La reconnaissance des signes d’une crise cardiaque et d’un accident vasculaire cérébral "
                         "(AVC)."])],
                flex_gap=gap(10)),
        ], 2, cols_t=2, cols_m=1, g=28, width=px(100, "%")),
        acc("Une formation axée sur la pratique", [
            ("Encadrement par un instructeur", "Les exercices en personne permettent aux participants de pratiquer "
             "les gestes essentiels et de recevoir des conseils personnalisés pour améliorer leur technique."),
            ("Rétroaction sur les compressions thoraciques", "Selon le matériel disponible, des mannequins dotés de "
             "dispositifs de rétroaction peuvent être utilisés afin d’aider les participants à améliorer la qualité "
             "de leurs compressions thoraciques."),
            ("Simulations cliniques", "Des mises en situation permettent de s’exercer à reconnaître une urgence et à "
             "intervenir dans un contexte proche de la réalité clinique."),
            ("Travail d’équipe", "Une attention particulière est accordée à la communication, à la coordination et "
             "à la répartition des rôles pendant une réanimation."),
        ]),
    ])

    def fmt(big, small, color, line):
        return con([heading(big, "div", 28, color, "800", MONT, lh=1.2),
                    heading(small, "div", 15, TEXT2, "400", SANS, lh=1.4)],
                   background_background="classic", background_color=PALE, padding=dims(26, 26, 26, 26),
                   flex_gap=gap(6), border_border="solid", border_width=dims(3, 0, 0, 0), border_color=line)

    ana = panel("anaphylaxie", [
        heading(fr("Module complémentaire : anaphylaxie"), "h2", 38, INK, "800", MONT, lh=1.2, size_m=28),
        p("Un module complémentaire portant sur la reconnaissance de l’anaphylaxie, une réaction allergique grave, et "
          "sur l’intervention appropriée est offert sur demande."),
        image("group", alt="Pratique avec un auto-injecteur d’épinéphrine", cls="rcr-169"),
        h("Deux formats", "h3", 24, weight="800"),
        grid([fmt(f"1{N}h{N}30", "Format court", NAVY, NAVY), fmt(f"4{N}h", "Format détaillé", RED, RED)],
             2, cols_t=2, cols_m=1, g=24, width=px(100, "%"), _margin=dims(-12, 0, 0, 0)),
        p("Ce module est particulièrement pertinent pour les garderies, les écoles et les entreprises qui souhaitent "
          "mieux préparer leur personnel à reconnaître une réaction allergique grave et à intervenir rapidement."),
    ])

    onsite = panel("sur-place", [
        heading("Formation sur place", "h2", 38, INK, "800", MONT, lh=1.2, size_m=28),
        p("<p><strong>Nous nous déplaçons.</strong> Vous souhaitez former votre équipe sans vous déplacer ? "
          "RCR Rive-Sud offre des formations privées directement sur place, principalement sur la Rive-Sud de "
          "Montréal. Des déplacements dans d’autres régions peuvent également être organisés sur demande.</p>"),
        ph_image("Pratique de la RCR chez le nourrisson", "rcr-169"),
        h("Où pouvons-nous nous déplacer ?", "h3", 24, weight="800"),
        p("Selon le type de formation et les modalités convenues, nous pouvons nous déplacer :",
          _margin=dims(-12, 0, 0, 0)),
        checks(["Dans vos bureaux et milieux de travail", "Dans les établissements de santé",
                "Dans les garderies et les écoles", "Dans les organismes communautaires", "À votre domicile"],
               cols=2),
        heading(fr("Vous choisissez le lieu ; nous nous occupons de la formation."), "div", 17, NAVY, "700", MONT,
                lh=1.4),
        grid([
            heading(f"3–12", "div", 40, "#FF8A8D", "800", MONT, lh=1),
            con([h("Nombre de participants", "div", 18, "#FFFFFF"),
                 p(f"Nos formations privées sont conçues pour des groupes de 3{N}à{N}12 participants. Ce format "
                   "favorise la participation active, la pratique des gestes essentiels et un encadrement adapté aux "
                   "besoins du groupe. Pour toute demande particulière, communiquez avec nous afin d’évaluer les "
                   "possibilités.", 15, BODY_TXT, 1.6)], flex_gap=gap(6)),
        ], "auto minmax(0,1fr)", cols_t="auto minmax(0,1fr)", cols_m=1, g=24, grid_align_items="center",
            background_background="classic", background_color=DEEP, padding=dims(28, 28, 28, 28)),
    ])

    pricing = panel("tarifs", [
        heading("Tarifs et soumissions", "h2", 38, INK, "800", MONT, lh=1.2, size_m=28),
        p("<p><strong>Une offre adaptée à vos besoins.</strong> Chaque demande étant différente, nos tarifs sont "
          "établis en fonction de plusieurs facteurs :</p>"),
        checks(["Le type de formation choisi", "Le nombre de participants",
                "Le lieu de la formation et les frais de déplacement, s’il y a lieu",
                "Le format du module complémentaire, le cas échéant"], 16, INK, divider=True),
        p("Communiquez avec nous par téléphone ou par courriel pour discuter de vos besoins et obtenir une soumission "
          "personnalisée."),
        button(fr("Demandez votre soumission dès aujourd’hui !"), U["contact"], pad=(16, 28)),
    ])

    def pill(anchor, label):
        return button(label, "#" + anchor, size=13, pad=(10, 16), radius=999, tt="none", shadow_on=False,
                      background_color="#FFFFFF", button_text_color=NAVY, button_background_hover_color="#FFFFFF",
                      hover_color=NAVY, hover_animation="", _css_classes="rcr-svc-pill")

    def navbox(cls, small, label, align, color):
        return link_con([
            heading(small, "div", 12, color, "700", SANS, lh=1.3, ls=1, tt="uppercase", align=align),
            heading(label, "div", 15, INK, "700", MONT, lh=1.35, align=align, _css_classes="rcr-svc-label"),
        ], "#", padding=dims(18, 20, 18, 20), flex_gap=gap(4), css_classes=cls)

    def zoom(key):
        return image(key, alt="", cls="rcr-43 rcr-zoom")

    main = con([
        con([
            heading('Parcourir nos services · <span class="rcr-svc-pos">1</span> sur 5', "div", 12, MUTED, "700",
                    MONT, lh=1.4, ls=1.7, tt="uppercase"),
            con([pill(a, l) for a, l in SERVICES], flex_direction="row", flex_wrap="wrap", flex_gap=gap(8)),
        ], flex_gap=gap(12), padding=dims(0, 0, 24, 0), border_border="solid", border_width=dims(0, 0, 1, 0),
            border_color=LINE),
        con([cardio, sir, ana, onsite, pricing], flex_gap=gap(56), css_classes="rcr-svc-panels"),
        grid([navbox("rcr-svc-prev", "← Service précédent", "", "start", MUTED),
              navbox("rcr-svc-next", "Service suivant →", SERVICES[1][1], "end", RED)],
             2, cols_t=2, cols_m=1, g=14, padding=dims(24, 0, 0, 0), border_border="solid",
             border_width=dims(1, 0, 0, 0), border_color=LINE, css_classes="rcr-svc-nav"),
        grid([zoom("heimlich"), zoom("naloxone"), zoom("mannequin")], 3, cols_t=3, cols_m=3, g=14,
             grid_gaps_mobile=gaps(8, 8), _margin=dims(8, 0, 0, 0)),
    ], flex_gap=gap(32), css_classes="rcr-svc-main")

    def tab(i, anchor, label):
        return link_con([
            heading(f"{i + 1:02d}", "div", 12, "#FFFFFF", "700", MONT, lh=1, _css_classes="rcr-svc-num",
                    _flex_size="none"),
            heading(label, "div", 14, INK, "700", MONT, lh=1.35, _css_classes="rcr-svc-tab-label",
                    _flex_size="grow"),
            heading("›", "div", 20, "#B8C6DE", "400", SANS, lh=1, _css_classes="rcr-svc-arrow", _flex_size="none"),
        ], "#" + anchor, flex_direction="row", flex_align_items="center", flex_gap=gap(14),
            padding=dims(18, 20, 18, 20), border_border="solid", border_width=dims(0, 0, 1, 0), border_color=LINE,
            css_classes="rcr-svc-tab")

    aside = con([
        con([
            con([h("Nos services", "div", 17, "#FFFFFF", "800"),
                 p("Sélectionnez un service pour en voir les détails", 13, BODY_TXT, 1.45)],
                background_background="classic", background_color=DEEP, padding=dims(18, 20, 18, 20),
                flex_gap=gap(4)),
            *[tab(i, a, l) for i, (a, l) in enumerate(SERVICES)],
        ], background_background="classic", background_color="#FFFFFF",
            box_shadow_box_shadow_type="yes", box_shadow_box_shadow=shadow(0, 14, 36, 0, "rgba(11,52,112,0.1)"),
            css_classes="rcr-svc-tabs"),
        question_card(),
        con([
            h("Demander une soumission", "div", 20, weight="800"),
            p("Pour votre entreprise, votre établissement ou un groupe privé : vérifiez nos disponibilités et "
              "obtenez une soumission adaptée à vos besoins.", 15, MUTED, 1.55),
            button("Demandez votre soumission", U["contact"], size=13, pad=(14, 20), shadow_on=False,
                   align="justify"),
        ], background_background="classic", background_color="#FFFFFF", padding=dims(28, 24, 28, 24),
            flex_gap=gap(14), box_shadow_box_shadow_type="yes",
            box_shadow_box_shadow=shadow(0, 14, 36, 0, "rgba(11,52,112,0.1)")),
    ], flex_gap=gap(28), css_classes="rcr-sticky")

    return [banner("Nos formations", [("Accueil", "/"), ("Services", None), ("Cardio-secours", None)], None,
                   height=220),
            page_section([two_col(main, aside)], css_classes="rcr-svc")]


# --------------------------------------------------------------------------- Équipe
def page_team():
    def xcard(ic, title, sub, span=False):
        return con([
            icon_circle(ic, 20, 12, _flex_size="none"),
            con([h(title, "div", 15), p(sub, 14, MUTED, 1.45)], flex_gap=gap(4)),
        ], flex_direction="row", flex_align_items="flex-start", flex_gap=gap(16), padding=dims(22, 22, 22, 22),
            border_border="solid", border_width=dims(1, 1, 1, 1), border_color=BORDER,
            css_classes="rcr-xcard" + (" rcr-span2" if span else ""))

    main = con([
        con([
            h("Présentation", "h2", 26, weight="800"),
            text(fr("<p>« Son expérience clinique et pédagogique lui permet d’offrir un encadrement rigoureux, axé sur "
                    "la pratique et adapté aux besoins des participants. »</p>"), 19, INK, 1.5, "700", family=MONT,
                 typography_font_style="italic", _padding=dims(4, 0, 4, 22), _border_border="solid",
                 _border_width=dims(0, 0, 0, 4), _border_color=RED),
            p("Fethi Boudebza est un formateur agréé par la Fondation des maladies du cœur et de l’AVC du Canada. "
              "Certifié depuis 2017, il possède plusieurs années d’expérience en réanimation cardiorespiratoire et en "
              "formation clinique."),
            p("Il a notamment exercé les fonctions de chef d’équipe du code bleu à l’Hôpital Douglas. Il a également "
              "formé du personnel en RCR, en premiers soins et en intervention lors d’urgences vitales. De plus, il a "
              "assuré la formation en réanimation cardiorespiratoire du personnel infirmier de l’Institut "
              f"{nw('Philippe-Pinel')} de Montréal."),
            p("Infirmier praticien spécialisé (IPS), il possède également une expérience clinique en soins aigus à "
              "l’Hôpital général juif. Il a par ailleurs enseigné les soins infirmiers au Cégep "
              f"{nw('André-Laurendeau')}."),
        ], flex_gap=gap(18)),
        con([
            h("Domaines d’expertise", "h2", 26, weight="800"),
            p("Plusieurs années d’expérience en réanimation cardiorespiratoire, en formation clinique et en "
              "enseignement."),
            checks(["Réanimation cardiorespiratoire (RCR)", "Chef d’équipe du code bleu",
                    "Formation en premiers soins", "Intervention lors d’urgences vitales", "Formation clinique",
                    "Soins aigus", "Enseignement des soins infirmiers", "Infirmier praticien spécialisé (IPS)"],
                   cols=2),
        ], flex_gap=gap(18)),
        con([
            h("Expérience et titres", "h2", 26, weight="800"),
            p("Formateur agréé par la Fondation des maladies du cœur et de l’AVC du Canada, avec une expérience "
              "clinique et en enseignement dans des établissements de Montréal."),
            grid([
                xcard("heart", "Fondation des maladies du cœur et de l’AVC du Canada",
                      "Formateur agréé, certifié depuis 2017"),
                xcard("course-bls", "Hôpital Douglas", "Chef d’équipe du code bleu"),
                xcard("people", f"Institut {nw('Philippe-Pinel')} de Montréal",
                      "Formation en RCR du personnel infirmier"),
                xcard("pulse", "Hôpital général juif", "Expérience clinique en soins aigus"),
                xcard("cap", f"Cégep {nw('André-Laurendeau')}", "Enseignement des soins infirmiers", span=True),
            ], 2, cols_t=2, cols_m=1, g=18, width=px(100, "%")),
        ], flex_gap=gap(18)),
    ], flex_gap=gap(56))

    aside = con([
        con([
            image("fethi", alt="Fethi Boudebza", cls="rcr-43", css_filters_css_filter="custom",
                  css_filters_brightness=px(85), css_filters_contrast=px(105)),
            con([
                h("Fethi Boudebza", "div", 20, weight="800"),
                p("Instructeur · Infirmier praticien spécialisé (IPS)", 14, RED, 1.45),
                p("Instructeur de la Fondation des maladies du cœur et de l’AVC du Canada depuis 2017", 14, TEXT2,
                  1.5, _margin=dims(6, 0, 0, 0)),
            ], padding=dims(22, 22, 24, 22), flex_gap=gap(6)),
        ], background_background="classic", background_color=PINK),
        con([
            h("Horaire", "div", 19, weight="800"),
            con([], width=px(44), min_height=px(3), background_background="classic", background_color=RED,
                margin=dims(0, 0, 6, 0)),
            *hours_rows(MUTED, INK, "#E3E8F1", 14, 9),
            p("Horaire flexible selon vos besoins", 14, MUTED, 1.5, _padding=dims(4, 0, 0, 0)),
        ], background_background="classic", background_color=PALE, padding=dims(26, 24, 26, 24), flex_gap=gap(10)),
        question_card(with_button=True),
    ], flex_gap=gap(28), css_classes="rcr-sticky")

    return [banner("Notre formateur", [("Accueil", "/"), ("Équipe", None), ("Fethi Boudebza", None)],
                   "ballon", 70, 40, 220),
            page_section([two_col(main, aside)])]


# --------------------------------------------------------------------------- FAQ (client's Q&A, verbatim)
FAQ = [
    ("Qu’est-ce que la RCR ?", "La réanimation cardiorespiratoire (RCR) est une technique de premiers secours qui permet de maintenir une circulation sanguine et un apport d’oxygène aux organes lorsqu’une personne est en arrêt cardiaque."),
    ("Quand faut-il commencer la RCR ?", "Lorsqu’une personne est inconsciente et ne respire pas normalement. Appelez le 911 et commencez immédiatement la RCR selon votre formation et les consignes du répartiteur."),
    ("Pourquoi chaque seconde compte-t-elle ?", "Parce que le cerveau et les autres organes sont rapidement privés d’oxygène lors d’un arrêt cardiaque. Une intervention rapide augmente les chances de survie."),
    ("Peut-on pratiquer la RCR sans formation ?", "Oui. Le répartiteur du 911 peut vous guider par téléphone. Il est toutefois recommandé de suivre une formation pratique pour acquérir les bons réflexes."),
    ("Qu’est-ce qu’un DEA ?", "Un défibrillateur externe automatisé est un appareil qui analyse le rythme cardiaque et détermine si un choc électrique est nécessaire."),
    ("Qui peut utiliser un DEA ?", "Les DEA sont conçus pour être utilisés par le grand public. L’appareil donne des instructions vocales simples pour guider l’intervention."),
    ("Le DEA peut-il être dangereux ?", "Lorsqu’il est utilisé conformément à ses instructions, le DEA est sécuritaire. Il faut simplement s’assurer que personne ne touche la victime pendant l’analyse et l’administration éventuelle du choc."),
    ("Faut-il continuer la RCR après l’utilisation du DEA ?", "Oui. Reprenez immédiatement la RCR lorsque l’appareil vous le demande et poursuivez jusqu’à l’arrivée des secours ou jusqu’à ce que la personne montre des signes de vie."),
    ("Comment reconnaître un étouffement ?", "Une personne qui s’étouffe peut avoir de la difficulté à respirer, ne plus être capable de parler ou de tousser efficacement, et parfois porter les mains à son cou."),
    ("Que faire si la personne tousse encore efficacement ?", "Encouragez-la à continuer de tousser et surveillez son état. Une toux efficace peut permettre d’expulser l’objet."),
    ("Que faire en cas d’obstruction grave ?", "Intervenez rapidement en appliquant les manœuvres de désobstruction adaptées à l’âge et à la condition de la personne, selon votre formation et les recommandations en vigueur."),
    ("Que faire si la personne perd connaissance ?", "Appelez le 911, commencez la RCR selon votre formation et suivez les instructions du répartiteur."),
    ("Qu’est-ce que l’anaphylaxie ?", "L’anaphylaxie est une réaction allergique grave et potentiellement mortelle qui nécessite une intervention immédiate."),
    ("Quels sont les signes à reconnaître ?", "Les symptômes peuvent comprendre une difficulté respiratoire, un gonflement de la langue ou de la gorge, de l’urticaire, des étourdissements ou une chute de pression artérielle."),
    ("Quel est le traitement de première intention ?", "L’épinéphrine (adrénaline) est le traitement de première intention. Elle doit être administrée rapidement à l’aide d’un auto-injecteur lorsqu’une anaphylaxie est suspectée."),
    ("Faut-il appeler le 911 après l’administration d’épinéphrine ?", "Oui. Même si la personne semble aller mieux, une évaluation médicale urgente est nécessaire."),
    ("À quoi sert un EpiPen ?", "L’EpiPen est un auto-injecteur qui permet d’administrer rapidement une dose d’épinéphrine lors d’une réaction allergique grave."),
    ("Où faut-il administrer l’injection ?", "Dans la face extérieure de la cuisse, conformément aux instructions du dispositif."),
    ("Peut-on administrer l’EpiPen à travers les vêtements ?", "Certains modèles permettent l’administration à travers les vêtements. Il faut toujours suivre les instructions du fabricant."),
    ("Que faire après l’injection ?", "Appelez le 911, surveillez la personne et suivez les recommandations des secours. Une deuxième dose peut être nécessaire selon l’évolution de la situation et les instructions médicales ou du dispositif."),
    ("Qu’est-ce que la naloxone ?", "La naloxone est un médicament qui peut renverser temporairement les effets d’une surdose d’opioïdes, notamment en aidant à rétablir la respiration."),
    ("Comment reconnaître une possible surdose d’opioïdes ?", "La personne peut être inconsciente ou difficile à réveiller, respirer très lentement ou ne plus respirer, et présenter des pupilles très petites."),
    ("Que faire si vous soupçonnez une surdose ?", "Appelez immédiatement le 911, administrez la naloxone selon les instructions du dispositif et donnez les soins respiratoires ou la RCR selon votre formation."),
    ("Une seule dose suffit-elle toujours ?", "Non. Une dose supplémentaire peut être nécessaire après 2 à 3 minutes si la personne ne répond pas ou si les symptômes persistent, conformément aux instructions du produit et au protocole applicable."),
    ("La naloxone remplace-t-elle les soins médicaux ?", "Non. Son effet peut être temporaire et elle agit uniquement contre les opioïdes. La personne doit recevoir une assistance médicale urgente et être surveillée."),
    ("Qu’est-ce que le SIR ?", "Les soins immédiats en réanimation regroupent les interventions essentielles à effectuer lorsqu’une personne présente une urgence vitale, notamment un arrêt cardiaque."),
    ("Quels sont les premiers gestes à poser ?", "Vérifiez la sécurité des lieux, évaluez l’état de conscience et la respiration, demandez de l’aide et appelez le 911. Commencez les interventions appropriées selon votre formation."),
    ("Pourquoi suivre une formation en SIR ?", "Parce qu’elle permet de reconnaître rapidement une urgence, d’intervenir avec confiance et de contribuer à sauver des vies."),
    ("La RCR est-elle différente chez l’enfant et le nourrisson ?", "Oui. Les techniques, la profondeur des compressions et certaines étapes diffèrent selon l’âge et la taille de la victime."),
    ("Pourquoi est-il important de connaître la RCR pédiatrique ?", "Parce que les urgences cardiorespiratoires chez les enfants et les nourrissons peuvent nécessiter des interventions adaptées à leur développement."),
    ("Que faire si un enfant ou un nourrisson ne respire pas normalement ?", "Appelez le 911, demandez un DEA et commencez les manœuvres de réanimation adaptées à son âge, selon votre formation et les consignes du répartiteur."),
    ("Pourquoi suivre une formation?", "Une urgence peut survenir à la maison, au travail, à l’école ou dans un lieu public. Savoir reconnaître les signes d’une situation critique et connaître les bons gestes peut faire toute la différence.</p><p>Se former, c’est être mieux préparé, agir avec confiance et contribuer à sauver des vies.</p><p>Nos formations vous permettent de développer les connaissances et les habiletés nécessaires pour intervenir efficacement lors d’une situation d’urgence."),
]


def page_faq():
    hero = section([
        photo_layer("heimlich", "right", 55, 50, 50,
                    overlay_gradient("#EAF1FA", 0, "rgba(234,241,250,0)", 55, 90), "rcr-faq-photo",
                    width_mobile=px(100, "%")),
        con([
            crumbs(("Accueil", "/"), ("FAQ", None)),
            heading("Foire aux questions", "h1", 56, INK, "800", MONT, lh=1.1, size_t=46, size_m=36),
            p("Pour vous aider à mieux comprendre nos formations", 18, TEXT2, 1.6, _css_classes="rcr-maxw480"),
        ], flex_gap=gap(16), z_index=1, padding=dims(100, 0, 100, 0), padding_mobile=dims(70, 0, 70, 0)),
    ], padding=dims(0, 32, 0, 32), padding_mobile=dims(0, 20, 0, 20), background_background="classic",
        background_color=SKY, overflow="hidden", css_classes="rcr-faq-hero", html_tag="section")

    acc_w = w("accordion", {
        "tabs": [{"_id": uid("q"), "tab_title": fr(q), "tab_content": fr(f"<p>{a}</p>")} for q, a in FAQ],
        "selected_icon": {"value": "fas fa-plus", "library": "fa-solid"},
        "selected_active_icon": {"value": "fas fa-minus", "library": "fa-solid"},
        "title_html_tag": "h2", "faq_schema": "yes", "icon_align": "right", "border_width": px(0),
        "title_background": "rgba(0,0,0,0)", "title_color": INK, "tab_active_color": INK,
        "icon_color": "#FFFFFF", "icon_active_color": "#FFFFFF", "icon_space": px(20),
        "title_padding": dims(22, 26, 22, 26), "title_padding_mobile": dims(18, 18, 18, 18),
        "content_padding": dims(0, 26, 24, 26), "content_padding_mobile": dims(0, 18, 20, 18),
        "content_background_color": "rgba(0,0,0,0)", "content_color": TEXT2, "_css_classes": "rcr-faqacc",
        **typo("title_typography", MONT, "700", 17, 1.4, size_m=16),
        **typo("content_typography", SANS, "400", 16, 1.7),
    })
    body = section([acc_w], boxed_width=px(880), padding=dims(100, 32, 100, 32),
                   padding_mobile=dims(70, 20, 70, 20), html_tag="section")
    return [hero, body]


# --------------------------------------------------------------------------- Contact
def page_contact():
    def infocard(ic, title, value, url=None):
        kids = [icon_circle(ic, 24, 18, align="center"), h(title, "h3", 18, align="center", _margin=dims(6, 0, 0, 0)),
                p(value, 15, MUTED, 1.55, align="center")]
        st = dict(background_background="classic", background_color="#FFFFFF", padding=dims(40, 24, 40, 24),
                  flex_align_items="center", flex_gap=gap(12), box_shadow_box_shadow_type="yes",
                  box_shadow_box_shadow=shadow(0, 14, 36, 0, "rgba(11,52,112,0.08)"),
                  **hover_lift(-6, shadow(0, 24, 48, 0, "rgba(11,52,112,0.14)")))
        return link_con(kids, url, **st) if url else con(kids, **st)

    cards = section([
        grid([
            infocard("pin", "Zone desservie", "Principalement sur la Rive-Sud de Montréal. Autres régions sur demande."),
            infocard("header-email", "Adresse courriel", "rcrrivesud@outlook.com", MAIL),
            infocard("header-phone", "Téléphone", f"(450) 374-7995 · Télécopieur (450) 693-0702", TEL),
        ], 3, cols_t=3, cols_m=1, g=24, grid_gaps_tablet=gaps(16, 16), width=px(100, "%")),
    ], padding=dims(80, 32, 40, 32), padding_mobile=dims(60, 20, 30, 20), html_tag="section")

    mapbox = con([
        w("google_maps", {"address": "Rive-Sud, Montréal, QC", "zoom": px(10), "height": px(480),
                          "height_mobile": px(360), "_css_classes": "rcr-map"}),
        con([
            heading("RCR Rive-Sud", "div", 14, INK, "700", MONT, lh=1.3),
            heading("Rive-Sud de Montréal, QC", "div", 13, MUTED, "400", SANS, lh=1.4),
        ], position="absolute", _offset_orientation_h="start", _offset_x=px(16), _offset_orientation_v="start",
            _offset_y=px(16), z_index=2, background_background="classic", background_color="#FFFFFF",
            padding=dims(14, 16, 14, 16), flex_gap=gap(2), width={"unit": "custom", "size": "auto", "sizes": []},
            box_shadow_box_shadow_type="yes", box_shadow_box_shadow=shadow(0, 8, 20, 0, "rgba(0,0,0,0.12)"),
            css_classes="rcr-maplabel"),
    ], background_background="classic", background_color="#E6EAF0", overflow="hidden", min_height=px(480),
        min_height_mobile=px(360))

    form = con([
        heading("Communiquez avec nous", "h2", 38, INK, "800", MONT, lh=1.2, size_t=34, size_m=28),
        p("Pour votre entreprise, votre établissement ou un groupe privé, communiquez avec nous pour vérifier nos "
          "disponibilités et obtenir une soumission adaptée à vos besoins.", 15, MUTED, 1.6,
          _margin=dims(-6, 0, 4, 0)),
        w("shortcode", {"shortcode": CF7}),
    ], _element_id="formulaire", flex_gap=gap(18))

    mapform = section([
        grid([mapbox, form], "minmax(0,1.1fr) minmax(0,1fr)", cols_t="1fr", cols_m=1, g=48,
             grid_align_items="stretch", width=px(100, "%")),
    ], padding=dims(40, 32, 100, 32), padding_mobile=dims(30, 20, 80, 20), html_tag="section")

    hours = con([
        h("Horaire", "h3", 22, "#FFFFFF", _margin=dims(0, 0, 6, 0)),
        *hours_rows(BODY_TXT, "#FFFFFF", "rgba(255,255,255,0.14)", 16, 11),
        p("Horaire flexible selon vos besoins", 16, BODY_TXT, 1.5),
        p("Pour toute demande particulière, communiquez avec nous afin d’évaluer les possibilités.", 15, BODY_TXT,
          1.6, _margin=dims(8, 0, 0, 0)),
    ], background_background="classic", background_color=DEEP, padding=dims(36, 32, 36, 32),
        padding_mobile=dims(30, 24, 30, 24), flex_gap=gap(12))

    pricing = con([
        eyebrow("Tarifs et soumissions"),
        h("Une offre adaptée à vos besoins", "h3", 24, weight="800"),
        p("Chaque demande est différente. Nos tarifs dépendent :", 15, MUTED, 1.65),
        checks(["Du type de formation choisi", "Du nombre de participants",
                "Du lieu de la formation et des frais de déplacement, s’il y a lieu",
                "Du format du module complémentaire, le cas échéant"], 15, INK, divider=True,
               _margin=dims(0, 0, 18, 0)),
        button(fr("Demandez votre soumission dès aujourd’hui !"), "#formulaire", size=13, pad=(14, 22),
               shadow_on=False, background_color=NAVY, button_background_hover_color=RED,
               _margin=dims(0, 0, 0, 0)),
    ], background_background="classic", background_color="#FFFFFF", padding=dims(36, 32, 36, 32),
        padding_mobile=dims(30, 24, 30, 24), flex_gap=gap(12), box_shadow_box_shadow_type="yes",
        box_shadow_box_shadow=shadow(0, 18, 40, 0, "rgba(11,52,112,0.08)"), css_classes="rcr-pricebox")

    hp = section([grid([hours, pricing], 2, cols_t=2, cols_m=1, g=32, grid_align_items="stretch",
                       width=px(100, "%"))],
                 padding=dims(90, 32, 90, 32), padding_mobile=dims(70, 20, 70, 20), background_background="classic",
                 background_color=PALE, html_tag="section")

    return [banner("Contactez-nous", [("Accueil", "/"), ("Contact", None)], None, height=220),
            cards, mapform, hp]


PAGES = {"a_propos": page_about, "services": page_services, "equipe": page_team, "faq": page_faq,
         "contact": page_contact}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in PAGES.items():
        tree = strip_none(fn())
        path = os.path.join(OUT, f"page_{name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(tree, f, ensure_ascii=False, separators=(",", ":"))
        print(name, os.path.getsize(path), "bytes")
