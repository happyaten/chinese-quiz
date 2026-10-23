import re,subprocess,unicodedata,os,html,sys
from PIL import Image
import numpy as np
def N(s): return re.sub(r'\s','',unicodedata.normalize('NFKC',s))
def lines(pdf):
    x=subprocess.run(['pdftotext','-bbox-layout',pdf,'-'],capture_output=True,text=True).stdout
    out=[]
    for pi,pg in enumerate(x.split('<page ')[1:]):
        H=float(re.search(r'height="([\d.]+)"',pg).group(1));W=float(re.search(r'width="([\d.]+)"',pg).group(1))
        for ln in re.findall(r'<line xMin="[\d.]+" yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">(.*?)</line>',pg,re.S):
            t=''.join(html.unescape(w) for w in re.findall(r'>([^<]*)</word>',ln[2]))
            out.append((pi+1,float(ln[0]),float(ln[1]),N(t),W,H))
    out.sort(key=lambda l:(l[0],l[1]))
    return out
def render(pdf,page):
    out=f'pg_{os.path.basename(pdf)[:2]}_{page}'
    if not os.path.exists(out+'.png'): subprocess.run(['pdftoppm','-r','200','-png','-singlefile','-f',str(page),'-l',str(page),pdf,out])
    return Image.open(out+'.png')
def squeeze(out):
    a=np.array(out); blank=(a>245).all(axis=1); keep=[]; run=0
    for i,b in enumerate(blank):
        run=run+1 if b else 0
        if run<=12: keep.append(i)
    a=a[keep]; cols=np.where((a<=245).any(axis=0))[0]
    if len(cols): a=a[:,max(cols[0]-10,0):cols[-1]+10]
    return Image.fromarray(a)
def block(L,n):
    i=next(i for i,l in enumerate(L) if re.match(r'^%d\.\('%n,l[3]))
    j=next((k for k in range(i+1,len(L)) if re.match(r'^%d\.\('%(n+1),L[k][3])),len(L))
    global NX
    nx=L[j] if j<len(L) else None
    NX=nx
    return [l for l in L[i:j] if '本試卷' not in l[3] and not (nx and l[0]==nx[0] and l[1]>=nx[1]-4)]
def cut(pdf,p,y0,y1,W):
    im=render(pdf,p); sc=im.size[0]/W
    return im.crop((int(25*sc),int(y0*sc),int((W-20)*sc),int(y1*sc))).convert('L')
def crop(pdf,n,name,whole=False):
    L=lines(pdf); B=block(L,n); W=B[0][4]
    if whole:
        parts=[]
        p0=B[0][0]; p1=NX[0] if NX else B[-1][0]
        for pg in range(p0,p1+1):
            H=next(l[5] for l in L if l[0]==pg)
            foot=min([l[1] for l in L if l[0]==pg and '本試卷' in l[3]]+[H-20])
            y0=B[0][1]-2 if pg==p0 else 25
            y1=(NX[1]-3) if (NX and pg==NX[0]) else foot-2
            if y1-y0>8: parts.append(cut(pdf,pg,y0,y1,W))
    else:
        cands=[]
        def foot(pg):
            H=next(l[5] for l in L if l[0]==pg)
            return min([l[1] for l in L if l[0]==pg and '本試卷' in l[3]]+[H-20])
        seq=B+([NX] if NX else [])
        for a,b in zip(seq,seq[1:]):
            if a[0]==b[0]: cands.append((b[1]-a[2],a[0],a[2]+1,b[1]-1))
            else:
                cands.append((foot(a[0])-a[2],a[0],a[2]+1,foot(a[0])-2))
                cands.append((b[1]-25,b[0],25,b[1]-1))
        g,pg,y0,y1=max(cands)
        parts=[cut(pdf,pg,y0,y1,W)]
    w=max(x.size[0] for x in parts); h=sum(x.size[1] for x in parts)
    out=Image.new('L',(w,h),255); y=0
    for x in parts: out.paste(x,(0,y)); y+=x.size[1]
    out=squeeze(out); out.save(name,optimize=True); return out.size
