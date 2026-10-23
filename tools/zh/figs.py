import re,subprocess,glob,unicodedata,os,html
from PIL import Image
PDF={'deeab7f9':glob.glob('/root/.claude/uploads/507b3014-0a99-59e4-82b8-b7bcfbf8a10b/deeab7f9*.pdf')[0],
     '4998d149':glob.glob('/root/.claude/uploads/507b3014-0a99-59e4-82b8-b7bcfbf8a10b/4998d149*.pdf')[0],
     '82d479d1':glob.glob('/root/.claude/uploads/507b3014-0a99-59e4-82b8-b7bcfbf8a10b/82d479d1*.pdf')[0],
     'nan6':'/mnt/project-files/1105-八上國文-適南版-第六課-題目卷.pdf','kang6':'/mnt/project-files/1105-八上國文-適康版-第六課-題目卷.pdf'}
def N(s): return re.sub(r'\s','',unicodedata.normalize('NFKC',s))
def lines(key):
    x=subprocess.run(['pdftotext','-bbox-layout',PDF[key],'-'],capture_output=True,text=True).stdout
    out=[];page=0
    for blk in re.split(r'(<page |<line)',x):
        pass
    pages=x.split('<page ')[1:]
    for pi,pg in enumerate(pages):
        H=float(re.search(r'height="([\d.]+)"',pg).group(1));W=float(re.search(r'width="([\d.]+)"',pg).group(1))
        for ln in re.findall(r'<line xMin="[\d.]+" yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">(.*?)</line>',pg,re.S):
            t=''.join(html.unescape(w) for w in re.findall(r'>([^<]*)</word>',ln[2]))
            out.append((pi+1,float(ln[0]),float(ln[1]),N(t),W,H))
    return out
def render(key,page):
    out=f'/tmp/claude-0/-home-claude/507b3014-0a99-59e4-82b8-b7bcfbf8a10b/scratchpad/quiz/zh/pg_{key}_{page}'
    if not os.path.exists(out+'.png'): subprocess.run(['pdftoppm','-r','170','-png','-singlefile','-f',str(page),'-l',str(page),PDF[key],out])
    return Image.open(out+'.png')
def crop(key,start,end,name):
    L=lines(key)
    s=next(l for l in L if l[3].startswith(N(start)))
    e=next((l for l in L if end and l[3].startswith(N(end)) and (l[0]>s[0] or (l[0]==s[0] and l[1]>s[1]))),None)
    def foot(p,H): return min([l[1] for l in L if l[0]==p and '本試卷' in l[3]]+[H-30])
    def top(p): return min(l[1] for l in L if l[0]==p)
    W,H=s[4],s[5]; parts=[]
    p=s[0]; y0=s[1]
    endp=e[0] if e else s[0]
    while True:
        im=render(key,p); sc=im.size[0]/W
        y1=e[1] if (e and p==e[0]) else foot(p,H)
        parts.append(im.crop((int(20*sc),int((y0-3)*sc),int((W-20)*sc),int((y1-2)*sc))).convert('L'))
        if p>=endp: break
        p+=1; y0=25
    w=max(x.size[0] for x in parts); h=sum(x.size[1] for x in parts)
    out=Image.new('L',(w,h),255); y=0
    for x in parts: out.paste(x,(0,y)); y+=x.size[1]
    # 壓掉大片空白
    import numpy as np
    a=np.array(out); blank=(a>245).all(axis=1); keep=[]; run=0
    for i,b in enumerate(blank):
        run=run+1 if b else 0
        if run<=30: keep.append(i)
    out=Image.fromarray(a[keep])
    out.save(name,optimize=True)
    return s[0], endp, out.size
