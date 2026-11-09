# python3 shrink.py bank.json [maxw] : re-encode images smaller (descreen + jpeg/png)
import sys,json,io,base64
from PIL import Image,ImageFilter
f=sys.argv[1]; MW=int(sys.argv[2]) if len(sys.argv)>2 else 520
d=json.load(open(f)); out=[]
for u in d['imgs']:
    im=Image.open(io.BytesIO(base64.b64decode(u.split(',',1)[1]))).convert('L')
    if im.size[0]>MW: im=im.filter(ImageFilter.GaussianBlur(1.3)).resize((MW,int(im.size[1]*MW/im.size[0])),Image.LANCZOS)
    b=io.BytesIO(); im.save(b,'JPEG',quality=60,optimize=True)
    q=im.quantize(16); b2=io.BytesIO(); q.save(b2,'PNG',optimize=True)
    mt,bb=('jpeg',b) if len(b.getvalue())<=len(b2.getvalue()) else ('png',b2)
    out.append(f'data:image/{mt};base64,'+base64.b64encode(bb.getvalue()).decode())
d['imgs']=out; json.dump(d,open(f,'w'),ensure_ascii=False); print(f,len(json.dumps(d))//1024,'KB')
