# 拆檔版：題庫各自存成 banks/*.json，頁面只內嵌目錄，切換題庫時才讀取。
# 單檔版仍由 build.py 產生（repo 的 index.html 用）；這裡借用它組好的頁面再拆開。
import json,re,os,sys
OUT=sys.argv[1] if len(sys.argv)>1 else 'split'
src=open('build.py').read().replace("open('index-artifact.html','w').write(page)",'')
g={};exec(src,g);page=g['page']
os.makedirs(OUT+'/banks',exist_ok=True)
man=[]
def cut(m):
    sid,body=m.group(1),m.group(2)
    if sid=='data':
        e={'id':'builtin','subj':'國文','name':'國文選擇題 3000 題','source':'朱源葆博士彙編'}
    else:
        d=json.loads(body); e={k:d[k] for k in ('id','subj','stage','name','source') if k in d}
    f='banks/%s.json'%sid
    open(OUT+'/'+f,'w').write(body)
    e['file']=f; man.append(e)
    return ''
page=re.sub(r'<script id="(data[^"]*)" type="application/json">(.*?)</script>\n?',cut,page,flags=re.S)
assert man[0]['id']=='builtin'
mj=json.dumps(man,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
a=page.index('const BUILTIN=('); b=page.index('\n',page.index('const BUILTINS=['))
page=page[:a]+'''const MANIFEST=%s;
const BUILTINS=MANIFEST.map(m=>Object.assign({},m));
const BUILTIN=BUILTINS[0];
function loadBank(b){
  if(b.questions) return Promise.resolve(b);
  if(!b._p) b._p=fetch(b.file).then(r=>{if(!r.ok) throw new Error(r.status);return r.json()})
    .then(d=>{['id','subj','stage','name','source'].forEach(k=>delete d[k]);Object.assign(b,d);return b})
    .catch(e=>{b._p=null;throw e});
  return b._p;
}'''%mj+page[b:]
old='''function useBank(id){
  B=allBanks().find(b=>b.id===id)||BUILTIN; store.cur=B.id;'''
assert old in page
page=page.replace(old,'''function useBank(id){
  const nb=allBanks().find(b=>b.id===id)||BUILTIN;
  if(!nb.questions){S=null;clearFoot();app.innerHTML='<p class="sub" style="padding:40px 0;text-align:center">題庫載入中…</p>'}
  return loadBank(nb).then(()=>pickBank(nb)).catch(()=>{
    app.innerHTML='<p class="sub" style="padding:40px 0;text-align:center">題庫載入失敗，請確認網路連線。<br><br><button class="chip" id="retry">重新載入</button></p>';
    document.getElementById('retry').onclick=()=>useBank(nb.id).then(home);
    return Promise.reject();
  });
}
function pickBank(nb){
  B=nb; store.cur=B.id;''')
# app 要先存在，才能顯示載入中
page=page.replace("applyFs(); useBank(store.cur);\nconst app=document.getElementById('app');","applyFs();\nconst app=document.getElementById('app');")
assert "const app=document.getElementById('app');" in page and 'useBank(store.cur)' not in page
page=re.sub(r'useBank\((.*?)\);\s*home\(\)',r'useBank(\1).then(home)',page)
i=page.rindex('\nhome();\n</script>')
page=page[:i]+'\nuseBank(store.cur).then(home,()=>{});\n</script>'+page[i+len('\nhome();\n</script>'):]
open(OUT+'/index.html','w').write(page)
print(len(page),len(man),sum(os.path.getsize(OUT+'/'+e['file']) for e in man))
