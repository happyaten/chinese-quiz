import json,io,base64,sys
sys.path.insert(0,'.')
from PIL import Image
from d1 import D1; from d2 import D2; from d3 import D3
D=D1+D2+D3
assert [d[0] for d in D]==list(range(1,167)), [d[0] for d in D]
st=json.load(open('starts.json'))
page={};n=1
for p in range(1,20):
    for y in st[str(p)]:
        if y<=125 or (p==1 and y<=210): continue
        page[n]=p;n+=1
assert n==167
S=1.024
def fig(p,boxes,n):
    im=Image.open(f'p{p:02d}.jpg').convert('L')
    parts=[im.crop(tuple(int(v*S) for v in b)) for b in boxes]
    w=max(x.size[0] for x in parts);h=sum(x.size[1] for x in parts)+12*(len(parts)-1)
    o=Image.new('L',(w,h),255);y=0
    for x in parts: o.paste(x,(0,y));y+=x.size[1]+12
    o.save(f'fig/g{n}.png')
    b=io.BytesIO();o.save(b,'JPEG',quality=80,optimize=True)
    return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
import os;os.makedirs('fig',exist_ok=True)
secs=['第1～40題','第41～80題','第81～120題','第121～166題']
Q=[]
for n,q,o,a,e,boxes in D:
    assert len(o)==4 and a in 'ABCD'
    d={'s':min((n-1)//40,3),'n':n,'q':q,'o':o,'a':['ABCD'.index(a)],'e':e}
    if boxes: d['img']=fig(page[n],boxes,n)
    Q.append(d)
bank={'id':'phys8-gifted-mid2','subj':'理化','name':'資優理化(一) 第二次段考模擬試題','source':'資優理化(一)第二次段考模擬試題（114年）166 題；答案與解析為自行解題，非原卷答案','sections':secs,'passages':[],'questions':Q}
json.dump(bank,open('../gt.json','w'),ensure_ascii=False)
print(len(Q),sum('img' in q for q in Q),os.path.getsize('../gt.json'))
