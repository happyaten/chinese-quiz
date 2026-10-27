def sec(a,b): return lambda n:0 if n<=a else 1
T={'zh':('國文','國文'),'ma':('數學','數學'),'en':('英文','英語閱讀'),'el':('英文','英語聽力（附聽力稿）'),'sci':('理化','自然'),'soc':('社會','社會')}
CUT={}
exec(open('cuts.py').read())
subj,nm=T[k]; secs,f=CUT[k]
build(k,subj,N+nm,secs,f,f'../m9{k}.json')
