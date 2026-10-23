import re,json,io,base64,sys
sys.path.insert(0,'.')
import pfigs
from PIL import Image
P=[('k1','康 L3 上'),('h1','翰 L3 上'),('n1','南 L3 上'),('k2','康 L3 下'),('h2','翰 L3 下'),('n2','南 L3 下'),('k3','康 L4 上'),('h3','翰 L4 上'),('n3','南 L4 上')]
KIND={'二':'依提示作答','三':'翻譯','四':'填充'}
def secs(f):
    out={};cur=None
    for l in open(f).read().split('\n'):
        m=re.match(r'\s*([一二三四])、',l)
        if m: cur=m.group(1); out[cur]=[]; continue
        if cur and cur!='一' and '本試卷由' not in l and l.strip(): out[cur].append(l.rstrip())
    return out
def items(L):
    it=[]
    for l in L:
        m=re.match(r'\s*(\d+)\.\s*(.*)',l)
        if m and (not it or int(m.group(1))==it[-1][0]+1): it.append([int(m.group(1)),[m.group(2)]])
        elif it: it[-1][1].append(l.strip())
    return it
def bl(s): return re.sub(r'(?<!＿)＿(?!＿) ?','',re.sub(r'＿{2,}','＿＿＿',s))
def enc(g):
    if g.size[0]>1100: g=g.resize((1100,int(g.size[1]*1100/g.size[0])),Image.LANCZOS)
    b=io.BytesIO(); g.save(b,'PNG',optimize=True); return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
def lineimg(pdf,sec,n):
    L=pfigs.lines(pdf)
    h=next(i for i,l in enumerate(L) if l[3].startswith(sec+'、'))
    i=next(k for k in range(h,len(L)) if l_start(L[k][3],n))
    j=next(k for k in range(i+1,len(L)) if re.match(r'^(\d+\.|[二三四]、|本試卷)',L[k][3]) or set(L[k][3])<={'＿','_'})
    l0,l1=L[i],L[j-1]
    return pfigs.squeeze(pfigs.cut(pdf,l0[0],l0[1]-3,l1[2]+4,l0[4]))
def l_start(t,n): return t.startswith(f'{n}.')
Q=[];log=[];sid=0
for si,(k,name) in enumerate(P):
    qs=secs(k+'q.txt'); an=secs(k+'a.txt'); cnt=0
    for sec in '二三四':
        if sec not in qs: continue
        qi=items(qs[sec]); ai=items(an[sec])
        assert [x[0] for x in qi]==[x[0] for x in ai],(k,sec,[x[0] for x in qi],[x[0] for x in ai])
        for (n,ql),(_,al) in zip(qi,ai):
            ql=[x for x in ql if not set(x)<={'＿',' '}]
            q=''
            for x in ql:
                x=bl(re.sub(r'\s+',' ',x))
                if not q: q=x
                elif re.match(r'([A-Z][a-z]*|[甲乙丙丁])\s*[：:]|\d+\.|（',x) or re.search(r'[。？！：]$',q): q+='\n'+x
                else: q+=(' ' if re.search(r'[\x21-\x7e＿]$',q) and re.match(r'[\x21-\x7e＿]',x) else '')+x
            q=re.sub(r'\n(（[^）]*）)$',r' \1',q)
            ans=[];ex=[]
            for x in al:
                if x.startswith('解析') or ex: ex.append(re.sub(r'^解析：?','',x))
                else: ans.append(x)
            d={'s':si,'n':n,'card':1,'kind':KIND[sec],'q':q,'o':[],'a':[],'ans':' '.join(ans).strip()}
            e='\n'.join(x for x in ex if x).strip()
            # join wrapped explanation lines
            e=re.sub(r'(?<=[A-Za-z.,])\n(?=[A-Za-z])',' ',e)
            e=re.sub(r'(?<=[^\n。？！])\n(?!\d+\.)','',e)
            if e: d['e']=e
            if '畫線' in q:
                g=lineimg(k+'q.pdf',sec,n); g.save(f'u_{k}_{sec}_{n}.png'); d['img']=enc(g); d['q']='（畫線部分請看下圖）\n'+d['q']
            Q.append(d); cnt+=1
    log.append((k,cnt))
bank={'id':'en8-mid2-cards','subj':'英文','name':'國二・二段 英文寫作題練習卡','source':'高雄楷模書院練習卷・八上英文 康／翰／南 B3 L3～L4 的改寫、重組、翻譯、填充題；看題目後按「看答案」自我檢查','sections':[n for _,n in P],'passages':[],'questions':Q}
json.dump(bank,open('../en2c.json','w'),ensure_ascii=False)
print(len(Q),log,sum('img' in q for q in Q))
