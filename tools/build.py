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
page=open('template.html').read().replace('__DATA__',s).replace('__PHYS__',phys).replace('__MATH__',json.dumps(json.load(open('math.json')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__PARSER__',open('parser.js').read().replace("if(typeof module!=='undefined') module.exports=parseQuiz;",''))
open('index-artifact.html','w').write(page)
