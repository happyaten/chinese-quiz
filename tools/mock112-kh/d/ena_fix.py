for n in E:
    t=''.join(E[n]['t'])
    if '（第' in t: t=t[:t.index('（第')]
    t=t.replace('不會小其對開樹再；上不而樹在，綠入','')
    for g in ['a故，拒的','能。0早不，']: t=t.replace(g,'')
    fix[int(n)]=t
fix[16]=fix[16][:fix[16].index('教育會考')]
