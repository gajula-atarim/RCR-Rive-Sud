import json, re, sys, html
src_dir, out_dir = sys.argv[1], sys.argv[2]
DROP_LINES = {"Pour vous aider à mieux comprendre nos services", "Prendre rendez-vous"}
def clean_md(md, title):
    lines = md.split('\n')
    # join headings split across lines (e.g. "### Symptômes\nphysiques")
    out = []
    for i, l in enumerate(lines):
        if out and re.match(r'^#{1,6} \S', out[-1]) and l.strip() and not l.startswith(('#', '-')) and (len(l.split()) <= 3 or out[-1].rstrip().endswith(':')) and (i + 1 < len(lines) and not lines[i + 1].strip()):
            out[-1] = out[-1].rstrip() + ' ' + l.strip(); continue
        out.append(l)
    lines = out
    # drop empty headings, duplicate title, stray taglines
    lines = [l for l in lines if not re.match(r'^#{1,6}\s*$', l)]
    lines = [l for l in lines if l.strip() not in DROP_LINES]
    lines = [l for l in lines if l.strip('# ').strip() != title]
    text = '\n'.join(lines)
    # drop the clinic CTA banner at the end
    text = re.split(r'\n#{1,6} Accédez à des soins spécialisés', text)[0]
    return text.strip()
def inline(t):
    t = html.escape(t.strip(), quote=False)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
def to_blocks(text):
    blocks, para, items = [], [], []
    def flush_para():
        if para:
            blocks.append(f'<!-- wp:paragraph -->\n<p>{inline(" ".join(para))}</p>\n<!-- /wp:paragraph -->'); para.clear()
    def flush_list():
        if items:
            lis = '\n'.join(f'<!-- wp:list-item -->\n<li>{inline(i)}</li>\n<!-- /wp:list-item -->' for i in items)
            blocks.append(f'<!-- wp:list -->\n<ul class="wp-block-list">{lis}</ul>\n<!-- /wp:list -->'); items.clear()
    for l in text.split('\n'):
        s = l.strip()
        m = re.match(r'^(#{1,6}) (.+)$', s)
        if m:
            flush_para(); flush_list()
            lvl = min(max(len(m.group(1)), 2), 4)   # article title is the post title (h1); body headings h2-h4
            blocks.append(f'<!-- wp:heading {{"level":{lvl}}} -->\n<h{lvl} class="wp-block-heading">{inline(m.group(2))}</h{lvl}>\n<!-- /wp:heading -->')
        elif s.startswith('- '):
            flush_para(); items.append(s[2:])
        elif not s:
            flush_para(); flush_list()
        else:
            flush_list(); para.append(s)
    flush_para(); flush_list()
    return '\n\n'.join(blocks)
for slug in ['tdah-adulte', 'anxiete', 'burn-out', 'depression']:
    r = json.load(open(f'{src_dir}/fr-{slug}.json'))
    text = clean_md(r['markdown'], r['title'])
    body = to_blocks(text)
    open(f'{out_dir}/fr-{slug}.html', 'w').write(body + '\n')
    first = re.search(r'<p>(.+?)</p>', body).group(1)
    first = re.sub('<[^>]+>', '', html.unescape(first))
    print(slug, len(body), 'blocks:', body.count('<!-- wp:'), '| excerpt:', first[:110])
