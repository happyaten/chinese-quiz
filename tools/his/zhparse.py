import re, json, sys, unicodedata
def N(s): return unicodedata.normalize('NFKC', s).replace('　',' ')
JUNK = re.compile(r'本試卷由.*提供|練習卷[-－]|^\s*第.課\s*(題目卷|解析卷)|^\s*\[滿分|^\s*一、\s*單一?選擇?題|^\s*二、\s*題組|^\s*\f')
def lines_of(path):
    out=[]
    for l in open(path, encoding='utf-8').read().split('\n'):
        l=N(l).replace('\f','').rstrip()
        if JUNK.search(l): 
            if re.match(r'^\s*二、\s*題組', l): out.append('##GROUPS##')
            continue
        out.append(l)
    return out
def join(ls, para=True):
    ls=[l for l in ls if l.strip()]
    if not ls: return ''
    ind=lambda l: len(l)-len(l.lstrip())
    base=min(ind(l) for l in ls); mx=max(len(l.strip()) for l in ls)
    out=ls[0].strip(); prev=ls[0]
    for l in ls[1:]:
        newp = para and (ind(l)>=base+3 or len(prev.strip())<mx*0.7 or re.match(r'\s*(【|註|\d+\.|○)', l))
        out += ('\n' if newp else '') + l.strip(); prev=l
    return out
OPT=[re.compile(r'\(\s*%s\s*\)' % c) for c in 'ABCD']
def split_opts(text):
    pos=[];p=0
    for m in OPT:
        r=m.search(text,p)
        if not r: return None
        pos.append((r.start(),r.end())); p=r.end()
    stem=text[:pos[0][0]]
    opts=[text[pos[i][1]:(pos[i+1][0] if i<3 else len(text))] for i in range(4)]
    clean=lambda s: re.sub(r'\s*\n\s*','',s).strip().rstrip('。').strip()
    return stem, [clean(o) for o in opts]
def parse_paper(path):
    L=lines_of(path); blocks=[]; cur=None; groups=False
    for l in L:
        if l=='##GROUPS##': groups=True; cur=None; continue
        m=re.match(r'^\s*(\d{1,2})\.\s*(\(\s*\))?\s*(.*)$', l)
        sub=re.match(r'^\s*\(\s*\)\s*\((\d)\)\s*(.*)$', l)
        if sub:
            cur={'k':'sub','n':int(sub.group(1)),'lines':[sub.group(2)]}; blocks.append(cur); continue
        if m and (not groups or m.group(3).startswith('請') or m.group(2)) and (cur is None or cur['k']!='group' or m.group(3).startswith('請')) and not (cur and cur['k']=='group' and not m.group(3).startswith('請')):
            if groups and not m.group(2):
                cur={'k':'group','n':int(m.group(1)),'lines':[]}; blocks.append(cur); continue
            if not groups:
                cur={'k':'q','n':int(m.group(1)),'lines':[m.group(3)]}; blocks.append(cur); continue
        if cur is not None: cur['lines'].append(l)
    qs=[];passages=[];fails=[]
    gp=None
    for b in blocks:
        if b['k']=='group':
            passages.append(join(b['lines'])); gp=len(passages)-1; continue
        raw='\n'.join(b['lines'])
        r=split_opts(raw)
        if not r: fails.append((b['k'],b['n'],raw[:80])); continue
        stem_raw, opts = r
        sl=[x for x in stem_raw.split('\n')]
        q={'n':b['n'],'o':opts,'raw':raw}
        stemtxt=re.sub(r'\s*\n\s*','',stem_raw).strip()
        if b['k']=='sub':
            q['p']=gp; q['sub']=True; q['q']=stemtxt
        else:
            q['q']=stemtxt
            if len(stemtxt)>160:
                nz=[i for i,x in enumerate(sl) if x.strip()]
                cut=[i for i in nz[:-1] if re.search(r'[)\]］）]\s*$', sl[i].strip())]
                if cut:
                    i=cut[-1]; ps=join(sl[:i+1]); st=re.sub(r'\s*\n\s*','',('\n'.join(sl[i+1:]))).strip()
                    if st:
                        passages.append(ps); q['p']=len(passages)-1; q['q']=st
        qs.append(q)
    return qs, passages, fails
def parse_ans(path):
    L=lines_of(path); items=[]; cur=None
    for l in L:
        if l=='##GROUPS##': continue
        m=re.match(r'^\s*(?:\d{1,2}\s*\.)?\s*答案[:：]\s*(.*)$', l)
        if m:
            cur={'a':m.group(1),'e':[]}; items.append(cur); continue
        e=re.match(r'^\s*(解析|語譯|翻譯)[:：]\s*(.*)$', l)
        if e and cur is not None:
            cur['e'].append(('' if e.group(1)=='解析' else e.group(1)+'：')+e.group(2)); cur['in']=True; continue
        if cur is not None and cur.get('in'):
            if re.match(r'^\s*\d{1,2}\.\s', l) or re.match(r'^\s*\(\s*\)', l) : cur['in']=False; continue
            if l.strip(): cur['e'].append(l)
    out=[]
    for it in items:
        letters=re.findall(r'\(([A-D])\)', it['a'])
        exp='\n'.join(x.strip() for x in it['e'])
        exp=re.sub(r'\n(?!語譯|翻譯|\(\d\))','',exp)
        if len(letters)>1 and re.search(r'\(1\)', it['a']):
            parts=re.split(r'(?=\(\d\)\s*)', exp)
            subs={}
            for pt in parts:
                mm=re.match(r'\((\d)\)\s*(.*)', pt, re.S)
                if mm: subs[int(mm.group(1))]=mm.group(2).strip()
            for i,c in enumerate(letters): out.append(('ABCD'.index(c), subs.get(i+1, exp if i==0 else '')))
        elif letters:
            out.append(('ABCD'.index(letters[0]), exp))
    return out
if __name__=='__main__':
    qs,ps,fails=parse_paper(sys.argv[1]); ans=parse_ans(sys.argv[2])
    print(len(qs),'q',len(ans),'ans',len(ps),'passages',len(fails),'fails',fails)
