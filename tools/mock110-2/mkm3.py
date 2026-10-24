import sys,json,io,base64
from PIL import Image
SC=1653/1415
def enc(g):
    if g.size[0]>1100: g=g.resize((1100,int(g.size[1]*1100/g.size[0])),Image.LANCZOS)
    b=io.BytesIO(); g.save(b,'PNG',optimize=True); b2=io.BytesIO(); g.save(b2,'JPEG',quality=80,optimize=True)
    mt,bb=('png',b) if len(b.getvalue())<=len(b2.getvalue()) else ('jpeg',b2)
    return f'data:image/{mt};base64,'+base64.b64encode(bb.getvalue()).decode()
def crop(b):
    im=Image.open(f'h_{b[0]}.png').convert('L'); m=6
    return im.crop((int(b[1]*SC)-m,int(b[2]*SC)-m,int(b[3]*SC)+m,int(b[4]*SC)+m))
def build(key,subj,name,secs,secof,out):
    g={};exec(open(f'd/{key}.py').read(),g); a={};exec(open(f'd/{key}a.py').read(),a)
    D,PS,K,E=g['D'],g.get('PS',[]),a['KEY'],a['E']
    Q=[]
    for d in D:
        n,q,o,bx=d[:4]
        assert len(o) in (3,4),n
        r={'s':secof(n),'n':n,'q':q,'o':o,'a':['ABCD'.index(K[n-1])]}
        if E.get(n): r['e']=E[n]
        if len(d)>4: r['p']=d[4]
        if bx:
            ims=[crop(b) for b in bx]
            if len(ims)==1: im=ims[0]
            else:
                W=max(i.size[0] for i in ims); im=Image.new('L',(W,sum(i.size[1] for i in ims)),255); y=0
                for i in ims: im.paste(i,(0,y)); y+=i.size[1]
            im.save(f'fig_{key}_{n}.png'); r['img']=enc(im)
        Q.append(r)
    bank={'id':f'mock110-2-{key}','subj':subj,'name':name,'source':'文揚 110 學年九年級國中學習成就評量（1～3 冊），答案與解析取自官方詳解','sections':secs,'passages':PS,'questions':Q}
    json.dump(bank,open(out,'w'),ensure_ascii=False)
    print(key,len(Q),sum('img' in q for q in Q))
if __name__=='__main__':
    k=sys.argv[1]
    if k=='zh': build('zh','國文','110 會考模擬二模（文揚 1～3 冊）國文',['單題（1～31）','題組（32～46）'],lambda n:0 if n<=31 else 1,'../m3zh.json')
    if k=='en': build('en','英文','110 會考模擬二模（文揚 1～3 冊）英語閱讀',['單題（1～18）','題組（19～41）'],lambda n:0 if n<=18 else 1,'../m3en.json')
    if k=='sci': build('sci','理化','110 會考模擬二模（文揚 1～3 冊）自然',['單題（1～39）','題組（40～52）'],lambda n:0 if n<=39 else 1,'../m3sci.json')
    if k=='soc': build('soc','社會','110 會考模擬二模（文揚 1～3 冊）社會',['單題（1～44）','題組（45～54）'],lambda n:0 if n<=44 else 1,'../m3soc.json')
