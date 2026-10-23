import re,json
P=[('k1','康 L3 上'),('h1','翰 L3 上'),('n1','南 L3 上'),('k2','康 L3 下'),('h2','翰 L3 下'),('n2','南 L3 下'),('k3','康 L4 上'),('h3','翰 L4 上'),('n3','南 L4 上')]
def sec1(f):
    L=open(f).read().split('\n'); out=[];on=False
    for l in L:
        if '一、' in l: on=True; continue
        if re.search(r'[二三四]、',l) and on: break
        if on and '本試卷由' not in l and l.strip(): out.append(l.rstrip())
    return out
def clean(s):
    s=re.sub(r'[ \t]+',' ',s).strip()
    s=s.replace('＿','_'); s=re.sub(r'_{2,}','＿＿＿',s); s=re.sub(r'＿＿＿( ?＿＿＿)+','＿＿＿',s)
    return s
Q=[];log=[]
for si,(k,name) in enumerate(P):
    L=sec1(k+'q.txt'); qs=[]
    for l in L:
        m=re.match(r'\s*(\d+)\.\s*[（(]\s*[）)]\s*(.*)',l)
        if m: qs.append([int(m.group(1)),[re.sub(r'^\s{3,}','＿＿＿ ',m.group(2)) if False else m.group(2)]])
        else: qs[-1][1].append(l.strip())
    A=sec1(k+'a.txt'); an={};cur=None
    for l in A:
        m=re.match(r'\s*(\d+)\.\s*\(?([A-D])\)?\s*$',l)
        if m: cur=int(m.group(1)); an[cur]=[m.group(2),'']; continue
        if cur: an[cur][1]+=l.strip()
    assert [q[0] for q in qs]==list(range(1,len(qs)+1)),(k,[q[0] for q in qs])
    assert sorted(an)==[q[0] for q in qs],(k,sorted(an))
    for n,ls in qs:
        txt='\n'.join(ls)
        i=txt.find('(A)'); stem=txt[:i]; opt=txt[i:]
        parts=re.split(r'\(([A-D])\)',opt.replace('\n',' '))
        o=[clean(parts[j]) for j in (2,4,6,8)]
        assert [parts[j] for j in (1,3,5,7)]==list('ABCD'),(k,n)
        # keep dialogue line breaks
        sl=[x.strip() for x in stem.split('\n') if x.strip()]
        out=''
        for x in sl:
            x=re.sub(r'(?<=\S) {4,}(?=\S)',' ＿＿＿ ',x)
            if re.match(r'[A-Z][a-z]*\s*[：:]',x) and out: out+='\n'+x
            else: out+=(' ' if out and re.search(r'[A-Za-z.,?!’\'"]$',out) and re.match(r'[A-Za-z(]',x) else '')+x
        e=an[n][1]; e=re.sub(r'^解析：','',e).strip()
        d={'s':si,'n':n,'q':clean(out) if '\n' not in out else '\n'.join(clean(y) for y in out.split('\n')),'o':o,'a':['ABCD'.index(an[n][0])]}
        if e: d['e']=e
        Q.append(d)
    log.append((k,len(qs)))
bank={'id':'en8-mid2','subj':'英文','name':'國二・二段 英文練習卷（文法選擇題）','source':'高雄楷模書院練習卷・八上英文 康／翰／南 B3 L3～L4 文法測驗','sections':[f'{n}' for _,n in P],'passages':[],'questions':Q}
json.dump(bank,open('../en2.json','w'),ensure_ascii=False)
print(len(Q),log,sum('e' in q for q in Q))
