import sys,re,glob,json,base64
sys.path.insert(0,'.')
from zhparse import parse_paper, parse_ans
P={("deeab7f9","1d9afdd6"):("南一","第四課"),("4998d149","66e36993"):("康軒","第四課"),("3326603c","925beeea"):("翰林","第四課"),
("d3650c96","76f58ff5"):("南一","第五課"),("7077fb98","d238434d"):("康軒","第五課"),("775f98f9","d7a6c909"):("翰林","第五課"),
("82d479d1","7ac150a1"):("翰林","第六課"),("1105-八上國文-適南版-第六課-題目卷","1105-八上國文-適南版-第六課-解析卷簡"):("南一","第六課"),("1105-八上國文-適康版-第六課-題目卷","1105-八上國文-適康版-第六課-解析卷簡"):("康軒","第六課")}
FIGS={("南一","第四課",8):'fig_n4_8',("南一","第四課",9):'fig_n4_9',("南一","第四課",10):'fig_n4_10',("康軒","第四課",14):'fig_k4_14',
("翰林","第六課",'g1'):'fig_h6_g2',("南一","第六課",7):'fig_n6_7',("南一","第六課",9):'fig_n6_9',("康軒","第六課",1):'fig_k6_1',("康軒","第六課",8):'fig_k6_8',("康軒","第六課",11):'fig_k6_11'}
order=sorted(P.items(),key=lambda kv:(['第四課','第五課','第六課'].index(kv[1][1]),['翰林','南一','康軒'].index(kv[1][0])))
sections=[];passages=[];Q=[]
for (a,b),(pub,les) in order:
    qs,ps,f=parse_paper(glob.glob(a+'*.txt')[0]); an=parse_ans(glob.glob(b+'*.txt')[0])
    assert len(qs)==len(an), (pub,les)
    s=len(sections); sections.append(f'{les}・{pub}版')
    off=len(passages); passages+=ps
    main=0; gi=0
    for q,(k,e) in zip(qs,an):
        d={'s':s,'q':q['q'],'o':q['o'],'a':[k]}
        if q.get('sub'):
            d['n']=f"題組{q['p']+1-0}" ; key=None
        if 'p' in q and q['p'] is not None: d['p']=q['p']+off
        if q.get('sub'):
            # 題組編號：第幾組第幾小題
            grp=sorted({x['p'] for x in qs if x.get('sub')}).index(q['p'])+1
            d['n']=f'題組{grp}-{q["n"]}'; key=(pub,les,f'g{grp}') if q['n']==2 else None
        else:
            main+=1; d['n']=q['n']; key=(pub,les,q['n'])
        if e: d['e']=e
        if key in FIGS:
            d['img']='data:image/png;base64,'+base64.b64encode(open(FIGS[key]+'.png','rb').read()).decode()
            last=re.split(r'(?<=[。」）)])',d['q'])
            d['q']='（題目與圖表請看下圖）'
            d['o']=[o if o else f'圖中選項 {"ABCD"[i]}' for i,o in enumerate(d['o'])]
        Q.append(d)
bank={'id':'zh8-mid2','subj':'國文','name':'國二・二段 國文練習卷','source':'高雄楷模書院練習卷・翰林／南一／康軒 第四～六課','sections':sections,'passages':passages,'questions':Q}
json.dump(bank,open('../zh2.json','w'),ensure_ascii=False)
print(len(Q),sections,sum('img' in q for q in Q),sum('e' in q for q in Q))
for q in Q:
    if 'img' in q: print(q['s'],q['n'],q['q'][:60],q['o'][:1])
