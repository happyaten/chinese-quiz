import json,base64,sys,re
sys.path.insert(0,'.')
from root import R
from pyth import P
from fact import F
def img(k):
    return 'data:image/png;base64,'+base64.b64encode(open(f'fig{k}.png','rb').read()).decode()
Q=[]
for s,rows in enumerate([R,P,F]):
    for i,row in enumerate(rows):
        q,o,a,e=row[:4]; fig=row[4] if len(row)>4 else None
        assert len(o)==4
        nl=lambda t: re.sub(r'\\n(?![a-z])','\n',t)
        d={'s':s,'n':i+1,'q':nl(q),'o':o,'a':['ABCD'.index(a)],'e':nl(e)}
        if fig is not None: d['img']=img(fig)
        Q.append(d)
bank={'id':'math8-a','name':'八上數學 練習卷','source':'高雄楷模書院練習卷','math':True,'sections':['根式的運算','畢氏定理','因式分解'],'passages':[],'questions':Q}
json.dump(bank,open('../math.json','w'),ensure_ascii=False)
print(len(Q),[len(x) for x in (R,P,F)])
