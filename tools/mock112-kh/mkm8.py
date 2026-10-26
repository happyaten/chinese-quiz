import sys,json,io,base64
from PIL import Image
SC=1653/1415
def enc(g):
    if g.size[0]>1100: g=g.resize((1100,int(g.size[1]*1100/g.size[0])),Image.LANCZOS)
    b=io.BytesIO(); g.save(b,'PNG',optimize=True); b2=io.BytesIO(); g.save(b2,'JPEG',quality=80,optimize=True)
    mt,bb=('png',b) if len(b.getvalue())<=len(b2.getvalue()) else ('jpeg',b2)
    return f'data:image/{mt};base64,'+base64.b64encode(bb.getvalue()).decode()
def crop(b):
    im=Image.open(f'{b[0]}.png').convert('L'); m=6
    sc=im.size[0]/1415
    return im.crop((int(b[1]*sc)-m,int(b[2]*sc)-m,int(b[3]*sc)+m,int(b[4]*sc)+m))
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
    bank={'id':f'mock112-kh-{key}','subj':subj,'name':name,'source':'康軒 112 學年國中教育會考模擬測驗（九年級，範圍 1～4 冊），答案與解析取自官方詳解','sections':secs,'passages':PS,'questions':Q}
    json.dump(bank,open(out,'w'),ensure_ascii=False)
    print(key,len(Q),sum('img' in q for q in Q))
if __name__=='__main__':
    k=sys.argv[1]; N='112 會考模擬二模（康軒 1～4 冊）'
    S={}
    exec(open('secs.py').read())
