#!/usr/bin/env python3
"""Builds build/i18n/out/en_map.json for the English importer (functions.php ?rcr_i18n_build).

Input: fr_export.json (live French texts, exported 18 Nov 2026) and en_strings.py (translations).
"""
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import en_strings as S  # noqa: E402

e = json.load(open(os.path.join(D, 'fr_export.json')))
seen, order = set(), []
for pid, p in e['posts'].items():
    for s in p['strings']:
        if s not in seen:
            seen.add(s)
            order.append(s)
assert len(order) == len(S.EN) == max(S.EN), (len(order), len(S.EN))
strings = {}
for i, fr in enumerate(order, 1):
    en = S.EN[i]
    if en is not None and en != fr:
        strings[fr] = en
json.dump({'n': i}, open(os.devnull, 'w'))
out = {
    'strings': strings,
    'alts': {str(k): v for k, v in S.ALTS.items()},
    'pages': {str(k): {'title': t, 'slug': s} for k, (t, s) in S.PAGES.items()},
    'templates': {str(k): v for k, v in S.TEMPLATES.items()},
    'paths': S.PATHS,
    'anchors': S.ANCHORS,
    'menu': S.MENU,
    'cf7_contact': S.CF7_CONTACT,
    'cf7_quote': S.CF7_QUOTE_ID,
}
os.makedirs(os.path.join(D, 'out'), exist_ok=True)
with open(os.path.join(D, 'out', 'en_map.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('strings', len(strings), 'of', len(order))
