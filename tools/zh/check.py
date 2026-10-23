import sys,re,glob
sys.path.insert(0,'.')
from zhparse import parse_paper, parse_ans
pairs=[("82d479d1","7ac150a1","翰林","第六課"),("deeab7f9","1d9afdd6","南一","第四課"),("4998d149","66e36993","康軒","第四課"),("3326603c","925beeea","翰林","第四課"),("d3650c96","76f58ff5","南一","第五課"),("7077fb98","d238434d","康軒","第五課"),("775f98f9","d7a6c909","翰林","第五課"),("1105-八上國文-適南版-第六課-題目卷","1105-八上國文-適南版-第六課-解析卷簡","南一","第六課"),("1105-八上國文-適康版-第六課-題目卷","1105-八上國文-適康版-第六課-解析卷簡","康軒","第六課")]
FIG=re.compile(r'圖表|圖片|附圖|下圖|如圖|附表|下表|圖中|圖一|圖二|示意圖|趨勢圖|這張圖|統計數據|座標上|圖女鞋')
for a,b,pub,les in pairs:
    qs,ps,f=parse_paper(glob.glob(a+'*.txt')[0]); an=parse_ans(glob.glob(b+'*.txt')[0])
    for q,(k,e) in zip(qs,an):
        flag=[]
        if any(len(o)==0 for o in q['o']): flag.append('EMPTYOPT')
        if FIG.search(q['q']) or any(FIG.search(o) for o in q['o']): flag.append('FIG')
        if max(len(o) for o in q['o'])>120: flag.append('LONGOPT')
        if flag: print(pub,les,q['n'],flag,q['q'][:50],'|',[o[:20] for o in q['o']])
