#!/usr/bin/env python3
"""Generate Elementor (v3 container) data for the RCR Rive-Sud Home page,
UAE header and footer templates, from the Home v5 design.

Outputs JSON element trees into build/elementor/out/.
Every visible element is a native Elementor container or widget so it can be
edited in the Elementor editor. Decorative-only artwork (hex patterns, dashed
line, crosses, rotating ring ticks) lives in the child theme's style.css.
"""
import hashlib
import json
import os

OUT = os.path.join(os.path.dirname(__file__), "out")
SITE = "https://rcr-rive-sud.wsdfy.com"
UP = SITE + "/wp-content/uploads/2026/11/"
BOOK = "https://clients3.clicsante.ca/65675/take-appt"
PLACEHOLDER = SITE + "/wp-content/plugins/elementor/assets/images/placeholder.png"

# Media library attachments
IMG = {
    "mannequin": (7, UP + "epipen-training-mannequin.webp"),
    "heimlich": (8, UP + "heimlich-choking-rescue.webp"),
    "group": (9, UP + "epipen-group-training.webp"),
    "cpr": (10, UP + "rcr-rive-sud-cpr-instructor.webp"),
    "naloxone": (11, UP + "naloxone-overdose-response.webp"),
    "hexband": (12, UP + "hex-band.png"),
    "logo": (32, UP + "rcr-rive-sud-logo.png"),
}

# Design tokens
RED, RED_D = "#D7191F", "#A9121A"
NAVY, INK, BODY = "#0B3470", "#0E1B33", "#1C2230"
MUTED, TEXT2 = "#5B6780", "#3F4B63"
SKY, PALE, PINK, LINE = "#EAF1FA", "#F5F7FB", "#FDECEC", "#EEF1F6"
DEEP = "#072553"
MONT, SANS = "Montserrat", "Source Sans 3"

_counter = [0]


def uid(seed):
    _counter[0] += 1
    return hashlib.md5(f"{seed}-{_counter[0]}".encode()).hexdigest()[:7]


def px(v, unit="px"):
    return {"unit": unit, "size": v, "sizes": []}


def dims(t, r, b, l, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": False}


def gap(v):
    return {"column": str(v), "row": str(v), "isLinked": True, "unit": "px", "size": v}


def gaps(c, r):
    return {"column": str(c), "row": str(r), "isLinked": False, "unit": "px"}


def shadow(x, y, blur, spread, color):
    return {"horizontal": x, "vertical": y, "blur": blur, "spread": spread, "color": color}


def typo(prefix="typography", family=MONT, weight="700", size=None, lh=None, ls=None, tt=None,
         size_t=None, size_m=None, lh_unit="em"):
    d = {f"{prefix}_typography": "custom", f"{prefix}_font_family": family, f"{prefix}_font_weight": str(weight)}
    if size is not None:
        d[f"{prefix}_font_size"] = px(size)
    if size_t is not None:
        d[f"{prefix}_font_size_tablet"] = px(size_t)
    if size_m is not None:
        d[f"{prefix}_font_size_mobile"] = px(size_m)
    if lh is not None:
        d[f"{prefix}_line_height"] = px(lh, lh_unit)
    if ls is not None:
        d[f"{prefix}_letter_spacing"] = px(ls)
    if tt:
        d[f"{prefix}_text_transform"] = tt
    return d


def anim(kind="fadeInUp", delay=0, container=False):
    k = "" if container else "_"
    d = {f"{k}animation": kind}
    if delay:
        d[f"{k}animation_delay"] = delay
    return d


# ---------- elements ----------

def con(children, inner=True, **s):
    """Flexbox container. Inner containers get zero padding / explicit gap so kit defaults never leak in."""
    base = {"flex_direction": "column", "flex_gap": gap(0), "padding": dims(0, 0, 0, 0)}
    if inner:
        base["content_width"] = "full"
    base.update(s)
    return {"id": uid("c"), "elType": "container", "isInner": inner, "settings": base, "elements": children}


def section(children, **s):
    """Top-level boxed section, 1200px content width."""
    base = {"content_width": "boxed", "boxed_width": px(1200), "flex_direction": "column", "flex_gap": gap(0)}
    base.update(s)
    return con(children, inner=False, **base)


def grid(children, cols, cols_t=None, cols_m=1, g=28, row_g=None, **s):
    st = {
        "container_type": "grid",
        "grid_columns_grid": {"unit": "fr", "size": cols, "sizes": []} if isinstance(cols, int)
        else {"unit": "custom", "size": cols, "sizes": []},
        "grid_rows_grid": {"unit": "fr", "size": 1, "sizes": []},
        "grid_auto_flow": "row",
        "grid_gaps": gaps(g, row_g if row_g is not None else g),
        "grid_columns_grid_mobile": {"unit": "fr", "size": cols_m, "sizes": []},
    }
    if cols_t is not None:
        st["grid_columns_grid_tablet"] = {"unit": "fr", "size": cols_t, "sizes": []} if isinstance(cols_t, int) \
            else {"unit": "custom", "size": cols_t, "sizes": []}
    st.update(s)
    return con(children, **st)


def w(kind, settings):
    return {"id": uid("w"), "elType": "widget", "widgetType": kind, "settings": settings, "elements": []}


def heading(text, tag="h2", size=44, color=INK, weight="800", family=MONT, align=None, lh=None, ls=None,
            tt=None, size_t=None, size_m=None, link=None, **extra):
    s = {"title": text, "header_size": tag, "title_color": color}
    s.update(typo("typography", family, weight, size, lh, ls, tt, size_t, size_m))
    if align:
        s["align"] = align
    if link:
        s["link"] = {"url": link, "is_external": "", "nofollow": ""}
    s.update(extra)
    return w("heading", s)


def h2(text, color=INK, align=None, **extra):
    return heading(text, "h2", 44, color, "800", MONT, align, 1.15, -0.44, None, 38, 30, **extra)


def eyebrow(text, color=RED, align=None, **extra):
    return heading(text, "div", 13, color, "700", MONT, align, 1.4, 2.08, "uppercase", **extra)


def text(html, size=16, color=MUTED, lh=1.7, weight="400", align=None, family=SANS, size_m=None, **extra):
    s = {"editor": html if html.startswith("<") else f"<p>{html}</p>", "text_color": color}
    s.update(typo("typography", family, weight, size, lh, None, None, None, size_m))
    if align:
        s["align"] = align
    s.update(extra)
    return w("text-editor", s)


def button(label, url, primary=True, external=False, size=14, pad=(17, 30), radius=3, tt="uppercase",
           align=None, shadow_on=True, **extra):
    s = {
        "text": label,
        "link": {"url": url, "is_external": "on" if external else "", "nofollow": ""},
        "background_color": RED,
        "button_text_color": "#FFFFFF",
        "button_background_hover_color": RED_D,
        "hover_color": "#FFFFFF",
        "border_radius": dims(radius, radius, radius, radius),
        "text_padding": dims(pad[0], pad[1], pad[0], pad[1]),
        "hover_animation": "float",
    }
    s.update(typo("typography", MONT, "700", size, 1, 0.2, tt))
    if shadow_on:
        s["button_box_shadow_box_shadow_type"] = "yes"
        s["button_box_shadow_box_shadow"] = shadow(0, 10, 24, 0, "rgba(215,25,31,0.28)")
    if align:
        s["align"] = align
    s.update(extra)
    return w("button", s)


def more(label="Read more", url="#", light=False, external=False, **extra):
    """Text link with arrow — Elementor Button widget styled as a link."""
    s = {
        "text": label,
        "link": {"url": url, "is_external": "on" if external else "", "nofollow": ""},
        "selected_icon": svg_icon("arrow-pink" if light else "arrow-red"),
        "icon_align": "row-reverse",
        "icon_indent": px(8),
        "background_color": "rgba(0,0,0,0)",
        "button_background_hover_color": "rgba(0,0,0,0)",
        "button_text_color": "#FFFFFF" if light else INK,
        "hover_color": "#FF8A8D" if light else RED,
        "text_padding": dims(0, 0, 0, 0),
        "border_radius": dims(0, 0, 0, 0),
        "_css_classes": "rcr-more rcr-more-light" if light else "rcr-more",
    }
    s.update(typo("typography", MONT, "700", 13, 1.2, 0.4, "uppercase"))
    s.update(extra)
    return w("button", s)


def image(key, height=None, width_pct=100, radius=None, cls="", height_m=None, link=None, url_override=None,
          alt=None, **extra):
    if url_override:
        img = {"url": url_override, "id": "", "alt": alt or "", "source": "library"}
    else:
        iid, url = IMG[key]
        img = {"url": url, "id": iid, "alt": alt or "", "source": "library"}
    s = {"image": img, "image_size": "full", "width": px(width_pct, "%"), "align": "start"}
    if height:
        s["height"] = px(height)
        s["object-fit"] = "cover"
    if height_m:
        s["height_mobile"] = px(height_m)
    if radius is not None:
        s["image_border_radius"] = dims(radius, radius, radius, radius, "%" if radius == 50 else "px")
    if cls:
        s["_css_classes"] = cls
    if link:
        s["link_to"] = "custom"
        s["link"] = {"url": link, "is_external": "", "nofollow": ""}
    s.update(extra)
    return w("image", s)


SVG = {  # custom icons from the design, uploaded via Safe SVG (attachment id, file)
    "feature-on-site": 46, "feature-groups": 47, "feature-quote": 48, "course-heartsaver-a": 49,
    "course-heartsaver-c": 50, "course-bls": 51, "cert-heartsaver": 52, "cert-bls": 53,
    "header-phone": 44, "header-email": 45, "footer-phone": 54, "footer-fax": 55, "footer-email": 56,
    "arrow-red": 68, "arrow-pink": 69,
}


def svg_icon(name):
    return {"value": {"url": UP + f"rcr-icon-{name}.svg", "id": SVG[name]}, "library": "svg"}


def icon(value, color=NAVY, size=34, library="fa-solid", stacked=False, bg=None, pad=None, **extra):
    sel = svg_icon(value[4:]) if value.startswith("svg:") else {"value": value, "library": library}
    s = {"selected_icon": sel, "primary_color": color, "size": px(size),
         "align": "left"}
    if stacked:
        s.update({"view": "stacked", "shape": "circle", "primary_color": bg, "secondary_color": color,
                  "icon_padding": px(pad or 14)})
    s.update(extra)
    return w("icon", s)


def absolute(x, y, unit_x="px", unit_y="px", width=None):
    d = {"_position": "absolute", "_offset_orientation_h": "start", "_offset_x": px(x, unit_x),
         "_offset_orientation_v": "start", "_offset_y": px(y, unit_y)}
    if width:
        d["_element_width"] = "initial"
        d["_element_custom_width"] = px(width)
    return d


CARD_SHADOW = {"box_shadow_box_shadow_type": "yes", "box_shadow_box_shadow": shadow(0, 18, 40, 0, "rgba(11,52,112,0.10)")}
CARD_HOVER = {
    "box_shadow_hover_box_shadow_type": "yes",
    "box_shadow_hover_box_shadow": shadow(0, 28, 54, 0, "rgba(11,52,112,0.16)"),
    "_transform_translateY_effect_hover": px(-6),
    "_transform_transition_hover": px(350, "ms"),
    "border_hover_transition": px(0.35, "s"),
}


def card(children, **s):
    st = {"background_background": "classic", "background_color": "#FFFFFF", "overflow": "hidden"}
    st.update(CARD_SHADOW)
    st.update(CARD_HOVER)
    st.update(s)
    return con(children, **st)


def bg_image(key, position="center center", size="cover", attachment=None):
    iid, url = IMG[key]
    d = {"background_image": {"url": url, "id": iid, "size": "", "alt": "", "source": "library"},
         "background_position": position, "background_repeat": "no-repeat", "background_size": size}
    if attachment:
        d["background_attachment"] = attachment
    return d


def overlay_gradient(c1, s1, c2, s2, angle=90):
    return {"background_overlay_background": "gradient", "background_overlay_color": c1,
            "background_overlay_color_stop": px(s1, "%"), "background_overlay_color_b": c2,
            "background_overlay_color_b_stop": px(s2, "%"), "background_overlay_gradient_type": "linear",
            "background_overlay_gradient_angle": px(angle, "deg"), "background_overlay_opacity": px(1)}



def photo_layer(key, side, width, xpos, ypos, ov, cls, **extra):
    """Absolutely positioned photo container (reference: <img> covering part of the section)."""
    iid, url = IMG[key]
    pos = {"_offset_orientation_h": "end", "_offset_x_end": px(0)} if side == "right" else \
        {"_offset_orientation_h": "start", "_offset_x": px(0)}
    return con([], position="absolute", _offset_orientation_v="start", _offset_y=px(0), width=px(width, "%"),
               min_height={"unit": "custom", "size": "100%", "sizes": []}, z_index=0,
               background_background="classic",
               background_image={"url": url, "id": iid, "size": "", "alt": "", "source": "library"},
               background_position="initial", background_xpos=px(xpos, "%"), background_ypos=px(ypos, "%"),
               background_repeat="no-repeat", background_size="cover", css_classes=cls, **pos, **ov, **extra)

SECTION_PAD = {"padding": dims(110, 32, 110, 32), "padding_tablet": dims(90, 32, 90, 32),
               "padding_mobile": dims(70, 20, 70, 20)}

# ======================= HOME PAGE =======================


def hero():
    return section([
        photo_layer("cpr", "right", 68, 70, 30, overlay_gradient(SKY, 3, "rgba(234,241,250,0)", 56), "rcr-hero-photo"),
        eyebrow("Cardiopulmonary resuscitation (CPR) training", **anim("fadeInUp", 0)),
        heading("Learn the right moves. Be ready to save a life.", "h1", 58, INK, "800", MONT, None, 1.1, -1.16,
                size_t=46, size_m=36, _element_width="initial", _element_custom_width=px(560),
                _element_width_mobile="inherit", **anim("fadeInUp", 150)),
        text("Hands-on CPR training for the general public, businesses and healthcare professionals. Learn to "
             "recognize a life-threatening emergency and respond effectively.", 17, TEXT2, 1.7,
             _element_width="initial", _element_custom_width=px(480), _element_width_mobile="inherit",
             **anim("fadeInUp", 300)),
        button("Request a quote", BOOK, external=True, _margin=dims(14, 0, 0, 0), **anim("fadeInUp", 450)),
    ],
        min_height=px(720), min_height_mobile=px(0),
        flex_justify_content="center", flex_align_items="flex-start", flex_gap=gap(24),
        padding=dims(150, 32, 240, 32), padding_tablet=dims(390, 32, 200, 32), padding_mobile=dims(300, 20, 170, 20),
        background_background="classic", background_color=SKY, overflow="hidden",
        css_classes="rcr-hero", html_tag="section",
    )


def feature_cards():
    def fcard(ic, title, body, url, ext, delay, corner=False):
        return card([
            con([icon(ic, NAVY, 40), heading(title, "h3", 19, INK, "700", MONT, lh=1.3)],
                flex_direction="row", flex_align_items="center", flex_gap=gap(16)),
            text(body, 15, MUTED, 1.65, _flex_size="grow"),
            more("Read more", url, external=ext),
        ], padding=dims(36, 28, 32, 28), padding_tablet=dims(30, 22, 28, 22), flex_gap=gap(16),
            css_classes="rcr-fcard" + (" rcr-corner" if corner else ""), **anim("fadeInUp", delay, True))

    return section([
        grid([
            fcard("svg:feature-on-site", "We come to you", "Private training at your location: offices, healthcare "
                  "facilities, daycares, schools, community organizations or your home.", "#quote", False, 0, True),
            fcard("svg:feature-groups", "Groups of 3 to 12", "Small groups encourage active participation, hands-on "
                  "practice and coaching adapted to your group's needs.", "#quote", False, 150),
            fcard("svg:feature-quote", "Personalized quote", "Pricing depends on the type of training, the number of "
                  "participants, the location and any travel costs.", BOOK, True, 300),
        ], 3, cols_t=1, g=28, grid_gaps_tablet=gaps(18, 18)),
    ], padding=dims(0, 32, 0, 32), padding_mobile=dims(0, 20, 0, 20),
        margin=dims(-110, 0, 0, 0), margin_mobile=dims(-110, 0, 0, 0), z_index=5, css_classes="rcr-features")


def about():
    left = grid([
        image("heimlich", 400, height_m=300, alt="Responding to choking", _margin=dims(80, 0, 0, 0),
              _margin_mobile=dims(30, 0, 0, 0)),
        image("cpr", 400, height_m=300, alt="Chest compressions on a CPR manikin"),
    ], 2, cols_t=2, cols_m=2, g=22, row_g=22, grid_align_items="start", css_classes="rcr-dots",
        grid_gaps_mobile={"column": "14", "row": "14", "isLinked": True, "unit": "px"},
        width=px(50, "%"), width_tablet=px(100, "%"), **anim("fadeInLeft", 0, True))
    right = con([
        eyebrow("RCR Rive-Sud"),
        h2("About us"),
        text("RCR Rive-Sud is a private company specializing in CPR training. Our mission is to share practical "
             "knowledge and build the hands-on skills needed to respond to cardiopulmonary arrest and help save "
             "lives.", 17, INK, 1.65, "600"),
        text("Our training is for the general public, workers, healthcare professionals and healthcare students."),
        text("Our approach focuses on practice, realistic scenarios and learning the essential skills that can make "
             "all the difference in an emergency."),
        con([
            image(None, 64, url_override=PLACEHOLDER, alt="Fethi Boudebza", radius=50,
                  width_pct=100, _element_width="initial", _element_custom_width=px(64)),
            con([
                heading("Fethi Boudebza", "div", 16, INK, "700", MONT, lh=1.3),
                heading("Instructor · Nurse Practitioner (NP)", "div", 14, RED, "400", SANS, lh=1.4),
            ], flex_gap=gap(3), width=px(75, "%")),
        ], flex_direction="row", flex_align_items="center", flex_gap=gap(16),
            border_border="solid", border_width=dims(1, 0, 0, 0), border_color=LINE,
            padding=dims(24, 0, 0, 0), margin=dims(14, 0, 0, 0)),
    ], flex_gap=gap(20), width=px(50, "%"), width_tablet=px(100, "%"), **anim("fadeInRight", 150, True))
    return section([left, right], flex_direction="row", flex_direction_tablet="column", flex_gap=gap(64),
                   flex_gap_tablet=gap(48), flex_align_items="center", flex_wrap="nowrap",
                   **SECTION_PAD, _element_id="about", html_tag="section")


def courses():
    def ccard(key, ic, title, body, delay):
        return card([
            image(key, 240, height_m=220, alt=""),
            con([
                icon(ic, RED, 24, stacked=True, bg="#FFFFFF", pad=14, _css_classes="rcr-iconbadge",
                     **absolute(24, -26, width=52)),
                heading(title, "h3", 19, INK, "700", MONT, lh=1.3),
                text(body, 15, MUTED, 1.6, _flex_size="grow"),
                more(),
            ], padding=dims(44, 26, 30, 26), flex_gap=gap(12), _flex_size="grow"),
        ], **anim("fadeInUp", delay, True))

    return section([
        con([
            h2("Our training", "#FFFFFF", "center"),
            text("We offer in-person training, mainly on Montreal's South Shore, with the option to travel to other "
                 "areas on request.", 18, "#FFFFFF", 1.65, align="center",
                 text_shadow_text_shadow_type="yes",
                 text_shadow_text_shadow={"horizontal": 0, "vertical": 2, "blur": 12, "color": "rgba(7,37,83,0.9)"}),
        ], flex_gap=gap(16), flex_align_items="center", width=px(720), width_mobile=px(100, "%"),
            **anim("fadeInUp", 0, True)),
        grid([
            ccard("cpr", "svg:course-heartsaver-a", "Heartsaver · Level A", "CPR and interventions for adults. Suited to "
                  "offices, retail and some industrial settings. Approx. 2 h, 2-year certification.", 0),
            ccard("mannequin", "svg:course-heartsaver-c", "Heartsaver · Level C", "Adults, children and infants. Suited to "
                  "parents, daycare and school staff, coaches and healthcare professionals. Approx. 3.5 h.", 150),
            ccard("group", "svg:course-bls", "Basic Life Support (BLS)", "For healthcare professionals, "
                  "alone or within a resuscitation team. Theory, practice and simulations. Approx. 4–5 h, "
                  "1-year certification.", 300),
        ], 3, cols_t=3, g=28, width=px(100, "%"), grid_gaps_tablet=gaps(18, 18)),
        text("<p>Add-on module on request: <strong>Anaphylaxis</strong>, short format (1.5 h) or detailed format "
             "(4 h).</p>", 16, "#C9D3E5", 1.6, align="center", _css_classes="rcr-on-dark"),
    ], _element_id="courses", flex_gap=gap(56), flex_align_items="center",
        padding=dims(110, 32, 120, 32), padding_tablet=dims(90, 32, 100, 32), padding_mobile=dims(70, 20, 80, 20),
        background_background="classic", background_color=DEEP,
        **bg_image("hexband", "center center", "initial", "fixed"),
        background_bg_width=px(1900), css_classes="rcr-courses", html_tag="section")


def learn():
    def step(key, num, title, body, offset, delay, pos="center center"):
        return con([
            con([
                image(key, 230, height_m=210, radius=50, cls="rcr-step-img", alt="", **{"object-position": pos}),
                heading(num, "div", 14, "#FFFFFF", "700", MONT, "center", 1.43,
                        _background_background="classic", _background_color=RED,
                        _border_radius=dims(50, 50, 50, 50, "%"), _padding=dims(12, 0, 12, 0),
                        _box_shadow_box_shadow_type="yes", _box_shadow_box_shadow=shadow(0, 0, 0, 6, PINK),
                        **absolute(6, 6, "%", "%", 44)),
            ], width=px(230), width_mobile=px(210), flex_align_items="center"),
            heading(title, "h3", 18, INK, "700", MONT, "center", 1.3, _margin=dims(12, 0, 0, 0)),
            text(body, 15, MUTED, 1.6, align="center"),
        ], flex_align_items="center", flex_gap=gap(14),
            padding=dims(offset, 0, 0, 0), padding_mobile=dims(0, 0, 0, 0), **anim("zoomIn", delay, True))

    return section([
        con([
            h2("What you'll learn", align="center"),
            text("Practise the essential skills on manikins and take part in realistic scenarios.", 16, MUTED,
                 1.65, align="center"),
        ], flex_gap=gap(16), flex_align_items="center", width=px(720), width_mobile=px(100, "%"),
            **anim("fadeInUp", 0, True)),
        grid([
            step("naloxone", "01", "Recognize emergencies", "Spot the signs of cardiac arrest and certain critical "
                 "situations.", 40, 0),
            step("cpr", "02", "Perform high-quality CPR", "Practise chest compressions and proper ventilations.",
                 0, 150),
            step("mannequin", "03", "Use an AED", "Use an automated external defibrillator safely.", 40, 300,
                 "center right"),
            step("heimlich", "04", "Respond to choking", "Apply the right airway obstruction techniques.", 0, 450),
        ], 4, cols_t=2, g=28, row_g=48, width=px(100, "%"), css_classes="rcr-steps"),
    ], flex_gap=gap(64), flex_align_items="center", **SECTION_PAD, css_classes="rcr-learn", html_tag="section")


def quote():
    iid, url = IMG["group"]
    # Photo layer: right 58% of the section, full height, cropped 40%/50% with a fade into the sky colour,
    # matching the reference (<img> absolutely positioned, width 58%, object-position 40% 50%).
    photo = con([], position="absolute", _offset_orientation_h="end", _offset_x_end=px(0),
                _offset_orientation_v="start", _offset_y=px(0), width=px(58, "%"), width_tablet=px(45, "%"),
                min_height={"unit": "custom", "size": "100%", "sizes": []}, z_index=0,
                background_background="classic",
                background_image={"url": url, "id": iid, "size": "", "alt": "", "source": "library"},
                background_position="initial", background_xpos=px(40, "%"), background_ypos=px(50, "%"),
                background_repeat="no-repeat", background_size="cover",
                **overlay_gradient(SKY, 3, "rgba(234,241,250,0)", 62),
                css_classes="rcr-quote-photo")
    return section([photo, 
        con([
            h2("Request your quote"),
            text("For your business, your facility or a private group, contact us to check availability and get a "
                 "quote tailored to your needs. You choose the place; we handle the training.", 16, TEXT2, 1.65),
            # Free Elementor has no form widget: Contact Form 7 provides the working form.
            w("shortcode", {"shortcode": '[contact-form-7 id="14" title="Request a quote" html_class="rcr-form"]',
                            "_margin": dims(14, 0, 0, 0)}),
        ], flex_gap=gap(20), width=px(520), width_tablet=px(100, "%"), width_mobile=px(100, "%"), z_index=1,
            **anim("fadeInUp", 0, True)),
    ], _element_id="quote", padding=dims(100, 32, 110, 32), padding_tablet=dims(330, 32, 100, 32),
        padding_mobile=dims(250, 20, 80, 20),
        background_background="classic", background_color=SKY, overflow="hidden",
        css_classes="rcr-quote", html_tag="section")


def trainer():
    exp = [("Douglas Hospital", "Code blue team leader"),
           ("Institut Philippe-Pinel de Montréal", "CPR training for nursing staff"),
           ("Jewish General Hospital", "Nurse Practitioner (NP), acute care"),
           ("Cégep André-Laurendeau", "Nursing instructor")]
    items = [con([
        heading(t, "div", 16, BODY, "700", MONT, lh=1.35),
        heading(s, "div", 14, MUTED, "400", SANS, lh=1.4),
    ], flex_gap=gap(4), padding=dims(14, 0, 14, 0), border_border="solid", border_width=dims(1, 0, 0, 0),
        border_color="#E3E8F1") for t, s in exp]
    return section([
        grid([
            con([
                eyebrow("Our trainer"),
                h2("Meet your instructor"),
                text("His clinical and teaching experience allows him to offer rigorous coaching, focused on practice "
                     "and adapted to participants' needs."),
                more("Meet the team", "#team", _margin=dims(4, 0, 0, 0)),
            ], flex_gap=gap(20), **anim("fadeInUp", 0, True)),
            grid([
                con([
                    image(None, 440, height_m=380, url_override=PLACEHOLDER, alt="Fethi Boudebza"),
                    con([
                        heading("Fethi Boudebza", "div", 20, INK, "700", MONT, lh=1.3),
                        heading("Heart and Stroke Foundation of Canada instructor since 2017", "div", 14, RED, "400",
                                SANS, lh=1.4),
                    ], flex_gap=gap(4)),
                ], flex_gap=gap(16), **anim("fadeInUp", 150, True)),
                con([heading("Experience", "div", 15, NAVY, "700", MONT, lh=1.4, ls=0.9, tt="uppercase",
                             _padding=dims(0, 0, 10, 0))] + items,
                    flex_gap=gap(0), padding=dims(32, 28, 32, 28), background_background="classic",
                    background_color=PALE, **anim("fadeInUp", 300, True)),
            ], 2, cols_t=2, g=24),
        ], "minmax(280px,1fr) 2fr", cols_t="1fr", g=48, grid_align_items="start", width=px(100, "%")),
    ], _element_id="team", **SECTION_PAD, css_classes="rcr-trainer rcr-deco", html_tag="section")


def certification():
    def ccard(accent, grad_b, ic_bg, num, unit, title, body, validity, note, delay):
        ring = con([
            con([
                heading(num, "div", 34, accent, "900", MONT, "center", 0.9),
                heading(unit, "div", 10, INK, "800", MONT, "center", 1.2, 1.2, "uppercase"),
            ], width=px(68), width_mobile=px(68), min_height=px(68), flex_justify_content="center", flex_align_items="center",
                flex_gap=gap(2), background_background="classic", background_color="#FFFFFF",
                border_radius=dims(50, 50, 50, 50, "%"), box_shadow_box_shadow_type="yes",
                box_shadow_box_shadow=shadow(0, 8, 20, 0, "rgba(0,0,0,0.25)"), css_classes="rcr-ring-core"),
        ], width=px(96), width_mobile=px(96), min_height=px(96), flex_justify_content="center",
            flex_align_items="center", css_classes="rcr-ring", _flex_size="none")
        band = con([
            ring,
            con([
                heading("Certification validity", "div", 12, "rgba(255,255,255,0.85)", "700", MONT, lh=1.4,
                        ls=1.92, tt="uppercase"),
                heading(validity, "div", 22, "#FFFFFF", "800", MONT, lh=1.15),
                heading(note, "div", 14, "rgba(255,255,255,0.88)", "400", SANS, lh=1.4),
            ], flex_gap=gap(4), width=px(55, "%"), width_mobile=px(100, "%"), _flex_size="grow"),
        ], flex_direction="row", flex_wrap="wrap", flex_align_items="center", flex_gap=gap(18),
            padding=dims(24, 24, 24, 24), min_height=px(150), background_background="gradient",
            background_color=accent, background_color_b=grad_b, background_gradient_angle=px(120, "deg"),
            background_color_stop=px(0, "%"), background_color_b_stop=px(100, "%"), overflow="hidden",
            css_classes="rcr-band")
        return card([
            con([
                icon("svg:cert-heartsaver" if accent == RED else "svg:cert-bls", accent, 22, stacked=True, bg=ic_bg, pad=13),
                heading(title, "h3", 20, INK, "700", MONT, lh=1.3),
                text(body, 15, MUTED, 1.65),
            ], padding=dims(30, 28, 24, 28), flex_gap=gap(12), _flex_size="grow"),
            band,
        ], border_border="solid", border_width=dims(4, 0, 0, 0), border_color=accent,
            css_classes="rcr-cert-card", box_shadow_box_shadow=shadow(0, 18, 40, 0, "rgba(11,52,112,0.08)"),
            **anim("fadeInUp", delay, True))

    return section([
        photo_layer("group", "left", 52, 40, 50, overlay_gradient("rgba(245,247,251,0)", 58, PALE, 100),
                    "rcr-cert-photo"),
        con([
            h2("Certification", **anim("fadeInUp", 0)),
            grid([
                ccard(RED, "#8E0E14", PINK, "2", "Years", "Heartsaver", "Participants who meet the program "
                      "requirements receive a Heart &amp; Stroke course completion card.", "2 years",
                      "Heart & Stroke course completion card", 0),
                ccard(NAVY, "#04193A", SKY, "1", "Year", "Basic Life Support", "Certification according to the "
                      "requirements of the applicable BLS program.", "1 year", "Per the applicable BLS program", 150),
            ], 2, cols_t=2, g=24, grid_align_items="stretch"),
        ], flex_gap=gap(28), width=px(65, "%"), width_tablet=px(100, "%")),
    ], flex_direction="row", flex_justify_content="flex-end", padding=dims(100, 32, 100, 32),
        padding_tablet=dims(350, 32, 90, 32),
        padding_mobile=dims(70, 20, 70, 20), background_background="classic", background_color=PALE,
        overflow="hidden", css_classes="rcr-cert", html_tag="section")


def blog():
    def light_card(key, delay):
        return card([
            image(key, 255, height_m=230, alt=""),
            con([
                heading("Date", "div", 13, MUTED, "400", SANS, lh=1.4),
                heading("Article title (migrated)", "h3", 20, INK, "700", MONT, lh=1.3, link="#"),
                more(_margin=dims(6, 0, 0, 0)),
            ], padding=dims(28, 26, 30, 26), flex_gap=gap(12)),
        ], box_shadow_box_shadow=shadow(0, 18, 40, 0, "rgba(11,52,112,0.08)"), **anim("fadeInUp", delay, True))

    dark = card([
        heading("Date", "div", 13, "#D5DEEE", "400", SANS, lh=1.4),
        heading("Article title (migrated)", "h3", 20, "#FFFFFF", "700", MONT, lh=1.3, link="#"),
        more(light=True, _margin=dims(6, 0, 0, 0)),
    ], min_height=px(420), flex_justify_content="flex-end", flex_gap=gap(12), padding=dims(28, 26, 30, 26),
        background_color="#072553", **bg_image("group", "center center"),
        **overlay_gradient("rgba(7,37,83,0)", 30, "rgba(7,37,83,0.92)", 100, 180),
        box_shadow_box_shadow=shadow(0, 18, 40, 0, "rgba(11,52,112,0.08)"), **anim("fadeInUp", 150, True))

    return section([
        con([
            h2("Latest articles", align="center"),
            text("Articles migrated from rcrrivesud.ca", 16, MUTED, 1.65, align="center"),
        ], flex_gap=gap(16), flex_align_items="center", **anim("fadeInUp", 0, True)),
        grid([light_card("naloxone", 0), dark, light_card("mannequin", 300)], 3, cols_t=3, g=28,
             width=px(100, "%"), grid_gaps_tablet=gaps(18, 18)),
    ], _element_id="blog", flex_gap=gap(56), flex_align_items="center",
        padding=dims(110, 32, 150, 32), padding_mobile=dims(70, 20, 90, 20),
        background_background="gradient", background_color="#FFFFFF", background_color_stop=px(60, "%"),
        background_color_b="#F3F7FC", background_color_b_stop=px(100, "%"),
        background_gradient_angle=px(180, "deg"), css_classes="rcr-blog", html_tag="section")


def home():
    return [hero(), feature_cards(), about(), courses(), learn(), quote(), trainer(), certification(), blog()]

# ======================= HEADER =======================


def contact_box(ic, label, value, url, hide_m=False):
    s = {
        "selected_icon": svg_icon(ic),
        "view": "stacked", "shape": "circle", "primary_color": PINK, "secondary_color": RED,
        "icon_size": px(18), "icon_padding": px(14), "position": "inline-start", "position_mobile": "inline-start",
        "content_vertical_alignment": "middle", "icon_space": px(14), "text_align": "start",
        "title_text": label, "description_text": value, "title_size": "div",
        "link": {"url": url, "is_external": "", "nofollow": ""},
        "title_color": MUTED, "description_color": BODY,
        "title_bottom_space": px(2),
    }
    s.update(typo("title_typography", SANS, "400", 13, 1.3))
    s.update(typo("description_typography", MONT, "600", 15, 1.3))
    if hide_m:
        s["hide_mobile"] = "hidden-mobile"
    return w("icon-box", s)


def header():
    top = section([
        con([
            image("logo", width_pct=100, link="/", alt="RCR Rive-Sud", _element_width="initial",
                  _element_custom_width=px(76), _element_custom_width_mobile=px(54)),
            heading("RCR Rive-Sud", "div", 24, NAVY, "800", MONT, lh=1, size_t=20, size_m=20, link="/",
                    _flex_size="none"),
        ], flex_direction="row", flex_align_items="center", flex_gap=gap(12), width=px(320),
            width_tablet=px(260), width_mobile=px(100, "%")),
        con([
            contact_box("header-phone", "Call us", "(450) 374-7995", "tel:4503747995", hide_m=True),
            contact_box("header-email", "Email us", "rcrrivesud@outlook.com", "mailto:rcrrivesud@outlook.com",
                        hide_m=True),
        ], flex_direction="row", flex_wrap="wrap", flex_gap=gap(24), flex_align_items="center",
            width=px(560), width_tablet=px(470), flex_justify_content="flex-end",
            flex_justify_content_tablet="flex-end",
            flex_gap_tablet={"column": "16", "row": "10", "isLinked": False, "unit": "px", "size": 16},
            hide_mobile="hidden-mobile"),
    ], flex_direction="row", flex_justify_content="space-between", flex_align_items="center",
        flex_wrap="wrap", flex_wrap_tablet="nowrap", flex_gap=gap(28), flex_gap_tablet=gap(16),
        padding=dims(22, 32, 22, 32), padding_mobile=dims(16, 20, 16, 20),
        background_background="classic", background_color="#FFFFFF", css_classes="rcr-header-top")

    nav = w("navigation-menu", {
        "menu": "primary-menu", "layout": "horizontal", "navmenu_align": "left",
        "pointer": "underline", "animation_line": "fade",
        "dropdown": "tablet", "resp_align": "left", "full_width_dropdown": "yes",
        "padding_horizontal_menu_item": px(0), "padding_vertical_menu_item": px(18),
        "menu_space_between": px(22),
        **typo("menu_typography", MONT, "600", 13, 1.2, 0.4, "uppercase"),
        "color_menu_item": BODY, "color_menu_item_hover": RED, "pointer_color_menu_item_hover": RED,
        "color_menu_item_active": RED, "pointer_color_menu_item_active": RED,
        "color_dropdown_item": BODY, "background_color_dropdown_item": "#FFFFFF",
        "color_dropdown_item_hover": RED, "background_color_dropdown_item_hover": PALE,
        "color_dropdown_item_active": RED,
        **typo("dropdown_typography", MONT, "600", 13, 1.2, 0.4, "uppercase"),
        "padding_horizontal_dropdown_item": px(20), "padding_vertical_dropdown_item": px(14),
        "toggle_color": NAVY, "toggle_size": px(22),
        "_css_classes": "rcr-nav",
    })

    def lang(label, active):
        return w("button", {
            "text": label, "link": {"url": "#", "is_external": "", "nofollow": ""},
            "background_color": NAVY if active else "rgba(0,0,0,0)",
            "button_text_color": "#FFFFFF" if active else MUTED,
            "button_background_hover_color": NAVY, "hover_color": "#FFFFFF",
            "text_padding": dims(5, 9, 5, 9), "border_radius": dims(3, 3, 3, 3),
            **typo("typography", MONT, "700", 12, 1.2),
        })

    bar = section([
        con([nav], width=px(60, "%"), width_tablet=px(20, "%"), width_mobile=px(15, "%")),
        con([
            con([lang("FR", False), lang("EN", True)], flex_direction="row", flex_gap=gap(2),
                flex_align_items="center", width=px(80), width_mobile=px(72), flex_wrap="nowrap"),
            button("Request a quote", BOOK, external=True, size=13, pad=(12, 20), shadow_on=False,
                   typography_font_size_mobile=px(12), text_padding_mobile=dims(11, 14, 11, 14)),
        ], flex_direction="row", flex_wrap="nowrap", flex_align_items="center", flex_justify_content="flex-end",
            flex_gap=gap(16),
            flex_gap_mobile=gap(10), width=px(40, "%"), width_tablet=px(80, "%"), width_mobile=px(85, "%")),
    ], flex_direction="row", flex_justify_content="space-between", flex_align_items="center",
        flex_wrap="nowrap", flex_gap=gap(20), padding=dims(0, 32, 0, 32), padding_tablet=dims(12, 32, 12, 32),
        padding_mobile=dims(10, 20, 10, 20), border_border="solid", border_width=dims(1, 0, 1, 0),
        border_color=LINE, background_background="classic", background_color="#FFFFFF",
        css_classes="rcr-header-bar")
    return [top, bar]

# ======================= FOOTER =======================


def footer():
    fh = dict(size=21, color="#FFFFFF", weight="700", lh=1.3)

    def col_head(t):
        return heading(t, "div", fh["size"], fh["color"], fh["weight"], MONT, lh=fh["lh"],
                       _margin=dims(0, 0, 8, 0))

    def hours(day, time):
        return con([
            heading(day, "div", 15, "#C9D3E5", "400", SANS, lh=1.4),
            heading(time, "div", 15, "#FFFFFF", "400", SANS, lh=1.4),
        ], flex_direction="row", flex_justify_content="space-between", flex_gap=gap(14))

    def links(items, icons=False):
        lst = []
        for i, (label, url, ic) in enumerate(items):
            lst.append({"_id": uid("li"), "text": label,
                        "selected_icon": svg_icon(ic) if ic else {"value": "", "library": ""},
                        "link": {"url": url, "is_external": "", "nofollow": ""} if url else {"url": ""}})
        s = {"icon_list": lst, "view": "traditional", "space_between": px(14),
             "text_color": "#FFFFFF" if icons else "#C9D3E5", "text_color_hover": "#FFFFFF",
             "icon_color": "#FFFFFF", "icon_size": px(18), "text_indent": px(12 if icons else 0),
             **typo("icon_typography", SANS, "400", 16, 1.4)}
        return w("icon-list", s)

    main = section([
        grid([
            con([
                con([
                    image("logo", width_pct=100, link="/", alt="RCR Rive-Sud", radius=50, _element_width="initial",
                          _element_custom_width=px(60), _background_background="classic",
                          _background_color="#FFFFFF", _border_radius=dims(50, 50, 50, 50, "%"),
                          _padding=dims(6, 6, 6, 6)),
                    heading("RCR Rive-Sud", "div", 26, "#FFFFFF", "800", MONT, lh=1.1, link="/"),
                ], flex_direction="row", flex_align_items="center", flex_gap=gap(12)),
                text("Cardiopulmonary resuscitation (CPR) training. Essential skills to act when every second "
                     "counts.", 16, "#C9D3E5", 1.6, _element_width="initial", _element_custom_width=px(360),
                     _element_width_mobile="inherit"),
                button("Request a quote", BOOK, external=True, size=14, pad=(14, 22), radius=6, tt="none",
                       shadow_on=False, _margin=dims(10, 0, 0, 0)),
            ], flex_gap=gap(20), grid_column_tablet="custom", grid_column_custom_tablet="1 / -1"),
            con([col_head("Navigation"), links([
                ("About us", "/#about", ""), ("Services", "/#courses", ""), ("Team", "/#team", ""),
                ("Blog", "/#blog", ""), ("FAQ", "#", ""), ("Contact", "/#quote", "")])], flex_gap=gap(14)),
            con([col_head("Hours"), hours("Monday to Thursday", "9h to 19h"), hours("Friday", "9h to 12h"),
                 hours("Saturday & Sunday", "9h to 15h"),
                 heading("Flexible schedule as needed", "div", 15, "#C9D3E5", "400", SANS, lh=1.4)],
                flex_gap=gap(14)),
            con([col_head("Contact"), links([
                ("(450) 374-7995", "tel:4503747995", "footer-phone"),
                ("(450) 693-0702", "", "footer-fax"),
                ("rcrrivesud@outlook.com", "mailto:rcrrivesud@outlook.com", "footer-email")], icons=True)],
                flex_gap=gap(14)),
        ], "minmax(200px,1.4fr) minmax(110px,.7fr) minmax(170px,1fr) minmax(200px,1fr)",
            cols_t="minmax(0,.8fr) minmax(0,1.2fr) minmax(0,1.1fr)", g=28, row_g=40, width=px(100, "%"),
            grid_gaps_tablet=gaps(24, 40)),
    ], padding=dims(80, 32, 48, 32), padding_mobile=dims(60, 20, 36, 20),
        background_background="classic", background_color=DEEP, css_classes="rcr-footer")

    bottom = section([
        con([
            text('<p>2026 © RCR Rive-Sud | All Rights Reserved | <a href="/privacy-policy/">Privacy Policy</a> | '
                 '<a href="#">Web Design by Delisoft</a></p>', 15, "#C9D3E5", 1.6, _css_classes="rcr-on-dark",
                 width=None),
            w("social-icons", {
                "social_icon_list": [{"_id": uid("s"), "social_icon": {"value": "fab fa-facebook-f",
                                                                       "library": "fa-brands"},
                                      "link": {"url": "#", "is_external": "on", "nofollow": ""}}],
                "shape": "circle", "icon_color": "custom", "icon_primary_color": RED,
                "icon_secondary_color": "#FFFFFF", "icon_size": px(18), "icon_padding": px(14),
                "hover_primary_color": RED_D, "hover_secondary_color": "#FFFFFF", "hover_animation": "grow",
                "_css_classes": "rcr-social",
            }),
        ], flex_direction="row", flex_direction_mobile="column", flex_justify_content="space-between",
            flex_align_items="center", flex_align_items_mobile="flex-start", flex_gap=gap(16), flex_wrap="wrap",
            padding=dims(22, 0, 30, 0), border_border="solid", border_width=dims(1, 0, 0, 0),
            border_color="rgba(255,255,255,0.1)"),
    ], padding=dims(0, 32, 0, 32), padding_mobile=dims(0, 20, 0, 20), background_background="classic",
        background_color=DEEP, css_classes="rcr-footer-bottom")
    return [main, bottom]


def strip_none(o):
    if isinstance(o, dict):
        return {k: strip_none(v) for k, v in o.items() if v is not None}
    if isinstance(o, list):
        return [strip_none(v) for v in o]
    return o


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, tree in (("home", home()), ("header", header()), ("footer", footer())):
        tree = strip_none(tree)
        with open(os.path.join(OUT, f"{name}.json"), "w") as f:
            json.dump(tree, f, ensure_ascii=False, separators=(",", ":"))
        print(name, os.path.getsize(os.path.join(OUT, f"{name}.json")), "bytes")
