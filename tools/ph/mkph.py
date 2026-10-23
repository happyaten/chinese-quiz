import sys,re,json,base64
sys.path.insert(0,'.')
from zhparse import parse_paper, parse_ans
SEC=['3-1、3-2 波的傳播・聲波','3-3、3-4 聲波的反射・多變的聲音','第四章 光']
FIG={1:[5,7,12,13,17,18,21,23],2:[1,5,9,13,22],3:[1,7,9,10,13,14,16,18,20,21,22,25]}
PICOPT={(2,9),(3,10),(3,13)}
SUP=str.maketrans('0123456789','⁰¹²³⁴⁵⁶⁷⁸⁹')
def sup(t): return re.sub(r'×10(\d)\b',lambda m:'×10'+m.group(1).translate(SUP),t)
E_OV={
(1,21):'由圖知半個波長 50 cm，λ＝100 cm；週期 T＝20÷50＝0.4 秒；v＝λ/T＝100÷0.4＝250（cm/s）。',
(1,23):'2 秒內有 6 個波，(A)週期＝2/6＝1/3 秒；(B)波長＝48÷6＝8 公分；(C)頻率＝6÷2＝3 赫；(D)波速＝48 公分÷2 秒＝24 公分/秒，所以(D)錯。',
(2,16):'(A)1500×0.04÷2＝30（m）；(B)是反射原理；(C)各種頻率的聲波都能在海水中傳播；(D)傳入空氣後速率變慢。',
(2,19):'聲音走的路程＝船出發時到山壁距離的 2 倍再加上船走的距離：(340×6－15×6)÷2＝975（公尺）。',
(2,25):'喬瑜距甲峭壁 340×2÷2＝340 公尺，距乙峭壁 340×(2＋1)÷2＝510 公尺，兩峭壁相距 340＋510＝850 公尺。',
(3,6):'光 1 秒走 3×10⁸ 公尺＝繞地球 8 圈，8×2πR＝3×10⁸，R＝3×10⁸÷(2×3.14×8)≒5.97×10⁶ 公尺。',
(3,8):'時間＝4×10⁸÷(3×10⁸)≒1.33 秒。',
(3,10):'(B)光線射到兩面互相垂直的平面鏡，第二次反射後應沿與入射光平行的反方向射回，圖中路徑不符合反射定律。',
(3,18):'影子面積與到光源距離的平方成正比：(10＋5)²：(10＋5＋5)²＝18：A，9：16＝18：A，A＝32 cm²。',
}
Q=[];seen=set()
for i in (1,2,3):
    qs,ps,f=parse_paper(f'q{i}.txt');an=parse_ans(f'a{i}.txt')
    assert len(qs)==len(an)==25
    for q,(k,e) in zip(qs,an):
        n=q['n']; key=re.sub(r'\W','',q['q'])
        if key in seen: continue
        seen.add(key)
        e=re.sub(r'\s*\d+\.\s*$','',e).strip()
        e=E_OV.get((i,n),e)
        d={'s':i-1,'n':n,'q':sup(q['q']).replace('cm 2','cm²'),'o':[sup(o) for o in q['o']],'a':[k]}
        if (i,n)==(1,23):
            d['q']='振動一輕繩產生連續週期波，若振動 2 秒產生如圖的波形，則下列關於此繩波的敘述何者錯誤？'
            d['o']=['週期為 1/3 秒','波長為 8 公分','頻率為 3 赫','波速為 16 公分／秒']
        if (i,n)==(2,13):
            d['q']='四個振動源分別在同一個環境中產生聲音，它們所產生聲音的特性如表所示（請看下圖）。下列有關它們產生的聲音在空氣中傳播的敘述，何者正確？［95.基測Ⅱ］'
        if (i,n) in PICOPT: d['o']=[f'圖中選項 {c}' for c in 'ABCD']
        if e: d['e']=e
        if n in FIG[i]:
            d['img']='data:image/png;base64,'+base64.b64encode(open(f'f{i}_{n}.png','rb').read()).decode()
        Q.append(d)
bank={'id':'phys8-mid2','subj':'理化','name':'國二・二段 理化練習卷','source':'高雄楷模書院練習卷・八上理化全版本 3-1～3-4、第四章','sections':SEC,'passages':[],'questions':Q}
json.dump(bank,open('../ph2.json','w'),ensure_ascii=False)
print(len(Q),sum('img' in q for q in Q),sum('e' in q for q in Q))
for q in Q:
    if re.search(r'\s{3,}|[0-9]\s*$',q['q']+''.join(q['o'])): print('CHK',q['s'],q['n'],q['q'][-40:],q['o'])
