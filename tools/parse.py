import re, sys, json, unicodedata
src = open(sys.argv[1], encoding='utf-8').read()
ROUNDS = '一二三四五六七八九十'
TR = str.maketrans('﹝﹞〔〕［］【】', '()()()()')
def norm(l):
    l = unicodedata.normalize('NFKC', l).replace('　', ' ').translate(TR).rstrip()
    s = l.strip()
    if s and s.count(' ') / len(s) > 0.25:
        l = re.sub(r'(?<=[^\x00-\x7f]) +(?=[^\x00-\x7f])', '', l)
        l = re.sub(r'(?<=[^\x00-\x7f]) +(?=[\x00-\x7f])|(?<=[\x00-\x7f]) +(?=[^\x00-\x7f])', '', l) if s.count(' ')/len(s) > 0.35 else l
    l = re.sub(r'(?<=[^\x00-\x7f]) (?=[^\x00-\x7f])', '', l)
    return l
lines = [norm(l) for l in src.split('\n')]

QA = re.compile(r'^\s*\(\s*([A-Da-d1-4#](?:[.,、 ]*[A-Da-d])*)\s*\)\s*\.?\s*(\d[\d ]{0,4}?)\s*[\.、]\s*')
QA2 = re.compile(r'^\s*\(\s*([A-Da-d1-4#](?:[.,、 ]*[A-Da-d])*)\s*\)\s*\.?\s*(\d{1,3})\s*(?=[^\x00-\x7f(])')
QN = re.compile(r'^\s*(\d{1,3})\s*[\.、]\s*(?!\d)')
ROUND = re.compile(r'^\s*第([一二三四五六七八九十])回\s*$')

# items: ('round', k) | ('q', ans, num, [lines]) | ('text', line)
items = []
rnd = 0
cur = None
for ln in lines:
    m = ROUND.match(ln)
    if m:
        rnd = ROUNDS.index(m.group(1)) + 1; cur = None; items.append(('round', rnd)); continue
    if rnd == 0: continue
    m = QA.match(ln)
    if m:
        cur = ['q', m.group(1), int(m.group(2).replace(' ', '')), [ln[m.end():]]]; items.append(cur); continue
    m = QA2.match(ln)
    if m and cur is not None and 0 < int(m.group(2)) - cur[2] <= 2:
        cur = ['q', m.group(1), int(m.group(2)), [ln[m.end():]]]; items.append(cur); continue
    m = QN.match(ln)
    if m and not QA.match(ln):
        n = int(m.group(1))
        cur = ['q', None, n, [ln[m.end():]]]; items.append(cur); continue
    if cur is not None:
        cur[3].append(ln)
    else:
        items.append(('text', ln))

def marker(i):
    L = 'ABCD'[i]; l = L.lower(); d = str(i + 1)
    return re.compile(r'\(\s*[%s%s%s]\s*\)\s*\.?\s*|(?<![A-Za-z(])%s\s*[\.\)]\s*|(?<![\d(])%s\)\s*|(?<![A-Za-z(])%s(?=[ \n]|[^\x00-\x7f])\s*' % (L, l, d, L, d, L))

def split_opts(body_lines):
    """body_lines: list of physical lines. returns stem, opts, leftover_lines"""
    text = ''
    offs = []  # line start offsets
    for b in body_lines:
        offs.append(len(text)); text += b.strip() + '\n'
    pos = []
    p = 0
    for i in range(4):
        mk = marker(i)
        # choose first match after p; for A prefer matches after stem
        m = mk.search(text, p)
        if not m and i == 3: m = marker(2).search(text, p)
        if not m: return None
        pos.append((m.start(), m.end())); p = m.end()
    stem = text[:pos[0][0]]
    opts = [text[pos[i][1]:pos[i+1][0]] for i in range(3)]
    # D: until end of its line, continuing while the line is full width
    dstart = pos[3][1]
    k = max(i for i, o in enumerate(offs) if o <= dstart)
    end = text.index('\n', dstart)
    dmax = max(len(re.sub(r'\s', '', o)) for o in opts) * 1.6 + 8
    while k + 1 < len(body_lines) and len(re.sub(r'\s', '', text[dstart:end])) < dmax and len(body_lines[k].strip()) >= 32 and not body_lines[k].strip().endswith(('。', '？')) \
            and not re.match(r'\s*(※|▲|依上文|閱讀|\(?[甲乙丙丁]\)?[、.])', body_lines[k+1]) and body_lines[k+1].strip() \
            and (len(body_lines[k+1].strip()) < 20 or len(re.sub(r'\s', '', text[dstart:end])) + len(body_lines[k+1].strip()) <= dmax):
        k += 1; end = text.index('\n', offs[k])
    opts.append(text[dstart:end])
    rest = [l for l in text[end:].split('\n')]
    clean = lambda s: re.sub(r'\s*\n\s*', '', s).strip().rstrip('。.;；').strip()
    stem = re.sub(r'\s*\n\s*', '', stem).strip()
    return stem, [clean(o) for o in opts], rest

passages = []
qs = []
fails = []
pending_text = []
cur_round = 0
REF = re.compile(r'文中|上文|此詩|本詩|詩中|本文|作者|上引|上列|上述|依據|此文|這首|文章|該文|此段|這段|此詞|引文|根據上|上段|本段|文意|全文|主旨|此篇|本篇|篇中|這篇|短文|此則|詞中|曲中|本詞|此曲|句中')
cur_p = None
def flush_text():
    global pending_text, cur_p
    t = [x.strip() for x in pending_text if x.strip()]
    pending_text = []
    t = [x for x in t if not re.match(r'^(依上文回答.*|閱讀下文.*|▲.*回答.*題)$', x)]
    if sum(len(x) for x in t) >= 40:
        passages.append('\n'.join(t)); cur_p = len(passages) - 1
for it in items:
    if it[0] == 'round':
        flush_text(); cur_round = it[1]; cur_p = None; continue
    if it[0] == 'text':
        pending_text.append(it[1]); continue
    _, ans, num, body = it
    r = split_opts(body)
    if r is None:
        fails.append((cur_round, num, ' / '.join(body)[:200])); continue
    stem, opts, rest = r
    first = False
    if pending_text:
        before = len(passages); flush_text(); first = len(passages) > before
        if not first: cur_p = cur_p
    p = None
    if cur_p is not None and (REF.search(stem) or (first and not stem.startswith('下列'))):
        p = cur_p
    elif cur_p is not None:
        cur_p = None
    a = None
    if ans and ans != '#':
        a = sorted({('ABCD'.index(c.upper()) if c.isalpha() else int(c) - 1) for c in ans if c.isalnum()})
    q = {'r': cur_round, 'n': num, 'q': stem, 'o': opts, 'a': a}
    if p is not None: q['p'] = p
    qs.append(q)
    pending_text.extend(rest)
flush_text()
json.dump({'passages': passages, 'questions': qs}, open('data.json', 'w'), ensure_ascii=False)
import collections
print('questions', len(qs), 'fails', len(fails), 'passages', len(passages))
print('per round', collections.Counter(q['r'] for q in qs))
print('no answer', sum(not q['a'] for q in qs), collections.Counter(q['r'] for q in qs if not q['a']))
for f in fails[:80]: print('FAIL', f)
