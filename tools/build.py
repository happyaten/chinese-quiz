import json,re,sys
sys.path.insert(0,'.')
FW={',':'，',':':'：',';':'；','?':'？','!':'！','(':'（',')':'）'}
def fw(t): return re.sub(r'(?<=[^\x00-\x7f])[,:;?!()]|[,:;?!()](?=[^\x00-\x7f])', lambda m: FW[m.group()], t)
d=json.load(open('data.json'))
qs=[]
for q in d['questions']:
    o={'s':q['r']-1,'n':q['n'],'q':fw(q['q']),'o':[fw(x) for x in q['o']],'a':q['a'] or []}
    if 'p' in q: o['p']=q['p']
    qs.append(o)
data={'sections':['第'+c+'回' for c in '一二三四五六七八九十'],'passages':[fw(p) for p in d['passages']],'questions':qs}
s=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
phys=json.dumps(json.load(open('phys.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
page=open('template.html').read().replace('__DATA__',s).replace('__PHYS__',phys).replace('__ZH2__',json.dumps(json.load(open('zh2.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__MATH__',json.dumps(json.load(open('math.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__PH2__',json.dumps(json.load(open('ph2.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__GT__',json.dumps(json.load(open('gt.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__GEO__',json.dumps(json.load(open('geo2.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__HIS__',json.dumps(json.load(open('his2.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__CIV__',json.dumps(json.load(open('civ2.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__JA__',json.dumps(json.load(open('ja.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__EN__',json.dumps(json.load(open('en2.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__ENC__',json.dumps(json.load(open('en2c.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__M2ZH__',json.dumps(json.load(open('m2zh.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__M2MA__',json.dumps(json.load(open('m2ma.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__M2ER__',json.dumps(json.load(open('m2er.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__M2EL__',json.dumps(json.load(open('m2el.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__M2SCI__',json.dumps(json.load(open('m2sci.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__M2SOC__',json.dumps(json.load(open('m2soc.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__PARSER__',open('parser.js').read().replace("if(typeof module!=='undefined') module.exports=parseQuiz;",''))
open('index-artifact.html','w').write(page)
