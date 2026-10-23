// 把測驗卷文字整理成 {sections, passages, questions}
function parseQuiz(src){
  const NONASCII='[^\\x00-\\x7f]';
  const TR={'﹝':'(','﹞':')','〔':'(','〕':')','［':'(','］':')','【':'(','】':')'};
  const norm=l=>{
    l=l.normalize('NFKC').replace(/　/g,' ').replace(/[﹝﹞〔〕［］【】]/g,c=>TR[c]).replace(/\s+$/,'');
    const s=l.trim();
    if(s){const r=(s.match(/ /g)||[]).length/s.length;
      if(r>0.25) l=l.replace(/(?<=[^\x00-\x7f]) +(?=[^\x00-\x7f])/g,'');
      if(r>0.35) l=l.replace(/(?<=[^\x00-\x7f]) +(?=[\x00-\x7f])|(?<=[\x00-\x7f]) +(?=[^\x00-\x7f])/g,'');}
    return l.replace(/(?<=[^\x00-\x7f]) (?=[^\x00-\x7f])/g,'');
  };
  const lines=src.replace(/\r/g,'').split('\n').map(norm);
  const QA=/^\s*\(\s*([A-Da-d1-4#](?:[.,、 ]*[A-Da-d])*)\s*\)\s*\.?\s*(\d[\d ]{0,4}?)\s*[.、]\s*/;
  const QA2=/^\s*\(\s*([A-Da-d1-4#](?:[.,、 ]*[A-Da-d])*)\s*\)\s*\.?\s*(\d{1,3})\s*(?=[^\x00-\x7f(])/;
  const QN=/^\s*(\d{1,3})\s*[.、]\s*(?!\d)/;
  const SEC=/^\s*(第\s*[一二三四五六七八九十百\d]+\s*[回卷單元部分課章節]+|[一二三四五六七八九十]+、\s*(?:單選題|選擇題|多選題|題組)[^\n]{0,20})\s*$/;
  const KEYHEAD=/^\s*[\(]?(?:參考)?(?:答案|解答)[\)]?\s*[:：]?\s*(.*)$/;
  const items=[]; let cur=null, inKey=false, anyQ=false;
  const keyLines=[];
  for(const ln of lines){
    let m;
    if((m=ln.match(SEC))){items.push({t:'sec',name:m[1].replace(/\s/g,'')});cur=null;inKey=false;continue}
    if(anyQ&&(m=ln.match(KEYHEAD))&&ln.trim().length<60&&!QA.test(ln)){inKey=true;cur=null;keyLines.push({sec:items.filter(i=>i.t==='sec').length,text:m[1]});continue}
    if(inKey){
      if(/^[\s\dA-Da-d.、:：,，()\-~～ ]+$/.test(ln)){keyLines[keyLines.length-1].text+=' '+ln;continue}
      inKey=false;
    }
    if((m=ln.match(QA))){cur={t:'q',ans:m[1],n:parseInt(m[2].replace(/ /g,'')),body:[ln.slice(m[0].length)]};items.push(cur);anyQ=true;continue}
    if((m=ln.match(QA2))&&cur&&cur.t==='q'){const n=+m[2];if(n-cur.n>0&&n-cur.n<=2){cur={t:'q',ans:m[1],n,body:[ln.slice(m[0].length)]};items.push(cur);continue}}
    if((m=ln.match(QN))){cur={t:'q',ans:null,n:+m[1],body:[ln.slice(m[0].length)]};items.push(cur);anyQ=true;continue}
    if(cur) cur.body.push(ln); else items.push({t:'text',line:ln});
  }
  const marker=i=>{const L='ABCD'[i],l=L.toLowerCase(),d=String(i+1);
    return new RegExp(`\\(\\s*[${L}${l}${d}]\\s*\\)\\s*\\.?\\s*|(?<![A-Za-z(])${L}\\s*[.)]\\s*|(?<![\\d(])${d}\\)\\s*|(?<![A-Za-z(])${L}(?=[ \\n]|[^\\x00-\\x7f])\\s*`,'g')};
  const noWS=s=>s.replace(/\s/g,'');
  function splitOpts(body){
    let text='';const offs=[];
    for(const b of body){offs.push(text.length);text+=b.trim()+'\n'}
    const pos=[];let p=0;
    for(let i=0;i<4;i++){
      let mk=marker(i);mk.lastIndex=p;let m=mk.exec(text);
      if(!m&&i===3){mk=marker(2);mk.lastIndex=p;m=mk.exec(text)}
      if(!m) return null;
      pos.push([m.index,m.index+m[0].length]);p=m.index+m[0].length;
    }
    const opts=[0,1,2].map(i=>text.slice(pos[i][1],pos[i+1][0]));
    const ds=pos[3][1];
    let k=0;offs.forEach((o,i)=>{if(o<=ds)k=i});
    let end=text.indexOf('\n',ds);
    const dmax=Math.max(...opts.map(o=>noWS(o).length))*1.6+8;
    while(k+1<body.length&&noWS(text.slice(ds,end)).length<dmax&&body[k].trim().length>=32&&!/[。？]$/.test(body[k].trim())
      &&!/^\s*(※|▲|依上文|閱讀|\(?[甲乙丙丁]\)?[、.])/.test(body[k+1])&&body[k+1].trim()
      &&(body[k+1].trim().length<20||noWS(text.slice(ds,end)).length+body[k+1].trim().length<=dmax)){
      k++;end=text.indexOf('\n',offs[k]);
    }
    opts.push(text.slice(ds,end));
    const clean=s=>s.replace(/\s*\n\s*/g,'').trim().replace(/[。.;；]+$/,'').trim();
    return {stem:text.slice(0,pos[0][0]).replace(/\s*\n\s*/g,'').trim(),opts:opts.map(clean),rest:text.slice(end).split('\n')};
  }
  const REF=/文中|上文|此詩|本詩|詩中|本文|作者|上引|上列|上述|依據|此文|這首|文章|該文|此段|這段|此詞|引文|根據上|上段|本段|文意|全文|主旨|此篇|本篇|篇中|這篇|短文|此則|詞中|曲中|本詞|此曲|句中/;
  const sections=[],passages=[],questions=[],fails=[];
  let pending=[],curP=null,sec=-1,seenQ=false;
  const flush=()=>{
    let t=pending.map(x=>x.trim()).filter(Boolean);pending=[];
    t=t.filter(x=>!/^(依上文回答.*|閱讀下文.*|▲.*回答.*題)$/.test(x));
    if(t.join('').length>=40){passages.push(t.join('\n'));curP=passages.length-1;return true}
    return false;
  };
  for(const it of items){
    if(it.t==='sec'){flush();sections.push(it.name);sec=sections.length-1;curP=null;continue}
    if(it.t==='text'){pending.push(it.line);continue}
    if(sec<0){sections.push('全部題目');sec=0}
    if(!seenQ){seenQ=true;if(pending.join('').match(/姓名|班級|座號|得分|考試時間/))pending=[]}
    const r=splitOpts(it.body);
    if(!r){fails.push({sec:sections[sec],n:it.n,text:it.body.join(' ').slice(0,120)});continue}
    let first=false;
    if(pending.length) first=flush();
    let p=null;
    if(curP!=null&&(REF.test(r.stem)||(first&&!r.stem.startsWith('下列')))) p=curP; else curP=null;
    let a=[];
    if(it.ans&&it.ans!=='#') a=[...new Set([...it.ans].filter(c=>/[A-Da-d1-4]/.test(c)).map(c=>/\d/.test(c)?+c-1:'ABCD'.indexOf(c.toUpperCase())))].sort();
    const q={s:sec,n:it.n,q:r.stem,o:r.opts,a};
    if(p!=null) q.p=p;
    questions.push(q);
    pending.push(...r.rest);
  }
  // 卷末答案表：如「1.B 2.C」或「1-5 BCADA」
  keyLines.forEach(k=>{
    const map={};
    const t=k.text.normalize('NFKC');
    let m;const re1=/(\d{1,3})\s*[.、:：]?\s*\(?([A-Da-d])\)?/g;
    while((m=re1.exec(t))) map[+m[1]]='ABCD'.indexOf(m[2].toUpperCase());
    const re2=/(\d{1,3})\s*[-~～]\s*(\d{1,3})\s*[:：]?\s*([A-Da-d]{2,})/g;
    while((m=re2.exec(t))){const s=+m[1];[...m[3]].forEach((c,i)=>map[s+i]='ABCD'.indexOf(c.toUpperCase()))}
    const sIdx=Math.max(0,k.sec-1);
    questions.forEach(q=>{if(!q.a.length&&(q.s===sIdx||sections.length<=1)&&map[q.n]!=null)q.a=[map[q.n]]});
  });
  const FW={',':'，',':':'：',';':'；','?':'？','!':'！','(':'（',')':'）'};
  const fw=t=>t.replace(/(?<=[^\x00-\x7f])[,:;?!()]|[,:;?!()](?=[^\x00-\x7f])/g,c=>FW[c]);
  questions.forEach(q=>{q.q=fw(q.q);q.o=q.o.map(fw)});
  return {sections,passages:passages.map(fw),questions,fails};
}
if(typeof module!=='undefined') module.exports=parseQuiz;
