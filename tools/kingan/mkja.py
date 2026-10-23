import sys,json,base64,io,importlib.util
from PIL import Image
H='/tmp/claude-0/-home-claude/507b3014-0a99-59e4-82b8-b7bcfbf8a10b/scratchpad/quiz/his/'
TOP={1:640,2:130,3:640,4:130,5:640,6:130}; BOT={1:3300,2:2930,3:3300,4:2930,5:3300,6:3020}
OFF={1:(20,-4),2:(16,4),3:(8,-4),4:(12,4),5:(8,-12),6:(4,12)}
def load(f):
    s=importlib.util.spec_from_file_location(f,f); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def page_box(b):
    k=b[0]
    if k.startswith('P'): p=int(k[1:]); return p,b[1:]
    p=int(k[0]); x0=60 if k[1]=='L' else 1060; h=(BOT[p]-TOP[p])//2+(BOT[p]-TOP[p])%2+ (30 if p in(1,3,5) else 25 if p in(2,) else 30 if p==4 else 30)
    y0=TOP[p] if k[2]=='1' else None
    return p,(b[1]+x0,b[2]+(TOP[p] if k[2]=='1' else BOT[p]-HQ[p]),b[3]+x0,b[4]+(TOP[p] if k[2]=='1' else BOT[p]-HQ[p]))
HQ={1:1360,2:1425,3:1360,4:1430,5:1360,6:1475}
def crop(b):
    p,(x0,y0,x1,y1)=page_box(b); dx,dy=OFF[p]
    im=Image.open(f'{H}S-{p}.png').convert('L')
    m=8; return im.crop((x0-dx-m,y0-dy-m,x1-dx+m,y1-dy+m))
def enc(g):
    if g.size[0]>1100: g=g.resize((1100,int(g.size[1]*1100/g.size[0])),Image.LANCZOS)
    b=io.BytesIO(); g.save(b,'PNG',optimize=True); b2=io.BytesIO(); g.save(b2,'JPEG',quality=78,optimize=True)
    mt,bb=('png',b) if len(b.getvalue())<=len(b2.getvalue()) else ('jpeg',b2)
    return f'data:image/{mt};base64,'+base64.b64encode(bb.getvalue()).decode()
Q=[];PS=[];secs=['第 4 次練習：中國的人口','第 5 次練習：中國的經濟發展和全球關連','第 6 次練習：綜合練習']
for s,f in enumerate(['j1.py','j2.py','j3.py']):
    m=load(f); base=len(PS); PS+=m.PS
    assert [d[0] for d in m.D]==list(range(1,31)),f
    for d in m.D:
        n,q,o,a,e,bx=d[:6]
        assert len(o)==4 and a in 'ABCD'
        r={'s':s,'n':n,'q':q,'o':o,'a':['ABCD'.index(a)] ,'e':e}
        if len(d)>6: r['p']=base+d[6]
        if bx:
            ims=[crop(b) for b in bx]
            if len(ims)==1: g=ims[0]
            else:
                W=max(i.size[0] for i in ims); g=Image.new('L',(W,sum(i.size[1] for i in ims)),255); y=0
                for i in ims: g.paste(i,(0,y)); y+=i.size[1]
            g.save(f'fig_{s}_{n}.png'); r['img']=enc(g)
        Q.append(r)
bank={'id':'geo8-kingan-a','subj':'地理','name':'金安 地理(三) A 卷 第 4～6 次練習','source':'金安文教 K-HA 地理 3《4-1～6-2》練習卷（教用版答案與解析）','sections':secs,'passages':PS,'questions':Q}
json.dump(bank,open('../ja.json','w'),ensure_ascii=False)
print(len(Q),sum('img' in q for q in Q))
