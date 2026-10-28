import sys,json,io,base64
from PIL import Image
# usage: python3 mke5.py <dir> <out.json>   (dir has d.py and p-NN.png at 200dpi; crop boxes in 1090-wide coords)
def enc(g):
    if g.size[0]>760: g=g.resize((760,int(g.size[1]*760/g.size[0])),Image.LANCZOS)
    b=io.BytesIO(); g.save(b,'PNG',optimize=True); b2=io.BytesIO(); g.save(b2,'JPEG',quality=80,optimize=True)
    mt,bb=('png',b) if len(b.getvalue())<=len(b2.getvalue()) else ('jpeg',b2)
    return f'data:image/{mt};base64,'+base64.b64encode(bb.getvalue()).decode()
def crop(D,b):
    im=Image.open(f'{D}/p-{b[0]:02d}.png').convert('RGB'); sc=im.size[0]/1090
    g=im.crop((int(b[1]*sc),int(b[2]*sc),int(b[3]*sc),int(b[4]*sc)))
    if len(b)>5 and not b[5]: return g.convert('L')
    px=g.load(); W,H=g.size
    for y in range(H):          # erase red/pink answer ink
        for x in range(W):
            r,gg,bl=px[x,y]
            if r-gg>12 and r>=bl-5: px[x,y]=(255,255,255)
    return g.convert("L").point(lambda v:255 if v>242 else v)
D=sys.argv[1]; out=sys.argv[2]
SECS=[];Q=[];META={};PS=[];CURP=None;IMGS=[]
def sec(name): SECS.append(name); globals()['_n']=0; globals()['CURP']=None
def psg(text): PS.append(text); globals()['CURP']=len(PS)-1
def endp(): globals()['CURP']=None
def _add(r,img,e):
    global _n; _n+=1; r={'s':len(SECS)-1,'n':_n,**r}
    if e: r['e']=e
    if CURP is not None: r['p']=CURP
    if img:
        bx=img if isinstance(img,list) else [img]
        ims=[crop(D,b) for b in bx]
        W=max(i.size[0] for i in ims); im=Image.new('L',(W,sum(i.size[1] for i in ims)),255); y=0
        for i in ims: im.paste(i,(0,y)); y+=i.size[1]
        im.save(f'{D}/fig_{len(SECS)}_{_n}.png'); u=enc(im)
        if u not in IMGS: IMGS.append(u)
        r['img']='#%d'%IMGS.index(u)
    Q.append(r)
def ch(q,o,a,e=None,img=None):
    assert 2<=len(o)<=8 and 1<=a<=len(o),q; _add({'q':q,'o':o,'a':[a-1]},img,e)
def tf(q,a,e=None,img=None): ch(q,['○ 正確','✕ 錯誤'],1 if a else 2,e,img)
def cd(q,ans,e=None,img=None,kind='填充'): _add({'q':q,'o':[],'a':[],'card':True,'kind':kind,'ans':ans},img,e)
exec(open(f'{D}/d.py').read())
bank={**META,'sections':SECS,'passages':PS,'questions':Q,'imgs':IMGS}
json.dump(bank,open(out,'w'),ensure_ascii=False)
print(out,len(Q),'choice',sum(not q.get('card') for q in Q),'img',sum('img' in q for q in Q),len(json.dumps(bank))//1024,'KB')
