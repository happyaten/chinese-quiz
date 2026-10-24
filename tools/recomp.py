import json,re,io,base64,sys
from PIL import Image
def enc(src):
    mt,b=src.split(',',1)
    im=Image.open(io.BytesIO(base64.b64decode(b)))
    if im.mode in('RGBA','LA','P'): 
        bg=Image.new('RGB',im.size,'white'); im=im.convert('RGBA'); bg.paste(im,mask=im.split()[-1]); im=bg
    if im.mode!='L':
        rgb=im.convert('RGB'); 
        from PIL import ImageChops
        r,g,bb=rgb.split()
        if max(ImageChops.difference(r,g).getextrema()[1],ImageChops.difference(g,bb).getextrema()[1])<24: im=rgb.convert('L')
        else: im=rgb
    if im.size[0]>900: im=im.resize((900,int(im.size[1]*900/im.size[0])),Image.LANCZOS)
    outs=[]
    p=io.BytesIO(); im.save(p,'PNG',optimize=True); outs.append(('png',p.getvalue()))
    if im.mode=='L':
        q=im.quantize(16) if False else im.point(lambda v:min(255,(v//16)*17))
        p=io.BytesIO(); q.save(p,'PNG',optimize=True); outs.append(('png',p.getvalue()))
    j=io.BytesIO(); im.save(j,'JPEG',quality=70,optimize=True); outs.append(('jpeg',j.getvalue()))
    m,d=min(outs,key=lambda x:len(x[1]))
    new='data:image/%s;base64,'%m+base64.b64encode(d).decode()
    return new if len(new)<len(src) else src
def walk(o):
    if isinstance(o,dict): return {k:walk(v) for k,v in o.items()}
    if isinstance(o,list): return [walk(v) for v in o]
    if isinstance(o,str) and o.startswith('data:image/'): return enc(o)
    if isinstance(o,str) and 'data:image/' in o:
        return re.sub(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+',lambda m:enc(m.group(0)),o)
    return o
for f in sys.argv[1:]:
    a=len(open(f).read()); d=walk(json.load(open(f))); json.dump(d,open(f,'w'),ensure_ascii=False)
    print(f,a,len(open(f).read()))
