import re as _re
def _t(n): return ''.join(E[str(n)]['t'])
for n in E:
    t=_t(n)
    t=_re.sub(r'^答\s*\([A-D]\)','',t)
    for cut in ['教育會考模擬測驗詳解','答 4','答 5','112 學年國中教']:
        if cut in t: t=t[:t.index(cut)]
    fix[int(n)]=t
for k in fix: fix[k]=fix[k].replace('\uf0e8','與' if k==34 else '→')
fix[24]=fix[24][:fix[24].index('島外。')+3]
fix[40]=fix[40][:fix[40].index('提出申請許可。')+7] if '提出申請許可。' in fix[40] else fix[40][:fix[40].index('不須向我國政府申請許可。')+12]
fix[54]=fix[54][:fix[54].index('應屬於變動性。')+7]
