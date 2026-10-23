import sys,re,json,base64,io
sys.path.insert(0,'.')
from zhparse import parse_paper, parse_ans
import pfigs
from PIL import Image
P=[('h1','3-1、3-2・翰林版'),('k1','3-1、3-2・康軒／南一版'),('h2','3-3・翰林版'),('k2','3-3・康軒／南一版'),('h3','第四章・翰林版'),('k3','第四章・康軒／南一版')]
FW={',':'，',':':'：',';':'；','?':'？','!':'！','(':'（',')':'）'}
def fw(t): return re.sub(r'(?<=[^\x00-\x7f])[,:;?!()]|[,:;?!()](?=[^\x00-\x7f])', lambda m: FW[m.group()], t)
Q=[];log=[]
for s,(k,name) in enumerate(P):
    qs,ps,f=parse_paper(k+'q.txt');an=parse_ans(k+'a.txt')
    assert len(qs)==len(an)==25 and not f,(k,len(qs),len(an),f)
    L=pfigs.lines(k+'q.pdf')
    for q,(a,e) in zip(qs,an):
        n=q['n']; stem=q['q']
        d={'s':s,'n':n,'q':fw(stem),'o':[fw(o) for o in q['o']],'a':[a]}
        if e: d['e']=fw(re.sub(r'\s*\d+\.\s*$','',e).strip())
        empty=any(not o for o in q['o'])
        need= bool(re.search(r'[附右如下左上]圖|[附右如下]表|圖中|表中|圖示|圖片|[化計料]表|圖資料|圖判斷|根據.{0,8}[圖表]',stem)) or empty or ('p' in q)
        if need:
            B=pfigs.block(L,n)
            whole= empty or ('p' in q) or ('表' in stem and '圖' not in stem)
            fn=f'fig_{k}_{n}.png'
            pfigs.crop(k+'q.pdf',n,fn,whole)
            im=Image.open(fn)
            import numpy as np
            if im.size[1]<40 or (np.array(im.convert('L'))<200).mean()<0.003: log.append((k,n,'BLANK')); Q.append(d); continue
            g=im.convert('L')
            if g.size[0]>1100: g=g.resize((1100,int(g.size[1]*1100/g.size[0])),Image.LANCZOS)
            b=io.BytesIO(); g.save(b,'PNG',optimize=True); b2=io.BytesIO(); g.save(b2,'JPEG',quality=78,optimize=True)
            mt,bb=('png',b) if len(b.getvalue())<=len(b2.getvalue()) else ('jpeg',b2)
            d['img']=f'data:image/{mt};base64,'+base64.b64encode(bb.getvalue()).decode()
            if whole:
                d['q']='（題目與圖表請看下圖）'
                d['o']=[o if o else f'圖中選項 {"ABCD"[i]}' for i,o in enumerate(d['o'])]
            log.append((k,n,'W' if whole else 'G',im.size))
        Q.append(d)
bank={'id':'geo8-mid2','subj':'地理','name':'國二・二段 地理練習卷','source':'高雄楷模書院練習卷・八上地理 翰林／康軒南一版 3-1～第四章','sections':[n for _,n in P],'passages':[],'questions':Q}
json.dump(bank,open('../geo2.json','w'),ensure_ascii=False)
print(len(Q),sum('img' in q for q in Q),sum('e' in q for q in Q))
for l in log: print(l)
