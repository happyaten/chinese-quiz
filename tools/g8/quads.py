# usage: python3 quads.py <pdf> <outdir> [first last]
# renders p-NN.png at 200dpi (for crops) and q/NN-{1..4}.png quadrants at 150dpi for reading (1=左上 2=左下 3=右上 4=右下)
import sys,os,subprocess,glob
from PIL import Image
pdf,out=sys.argv[1],sys.argv[2]; os.makedirs(out+'/q',exist_ok=True)
rng=['-f',sys.argv[3],'-l',sys.argv[4]] if len(sys.argv)>4 else []
subprocess.run(['pdftoppm','-r','200','-gray','-png',*rng,pdf,out+'/p'],check=True)
for f in sorted(glob.glob(out+'/p-*.png')):
    n=int(f.rsplit('-',1)[1][:-4]); im=Image.open(f); w,h=im.size
    im=im.resize((w*3//4,h*3//4)); w,h=im.size; ox,oy=int(w*.02),int(h*.03)
    for i,(x0,y0,x1,y1) in enumerate([(0,0,w//2+ox,h//2+oy),(0,h//2-oy,w//2+ox,h),(w//2-ox,0,w,h//2+oy),(w//2-ox,h//2-oy,w,h)],1):
        im.crop((x0,y0,x1,y1)).save(f'{out}/q/{n:02d}-{i}.png')
    os.rename(f,f'{out}/p-{n:02d}.png') if f!=f'{out}/p-{n:02d}.png' else None
print(len(glob.glob(out+'/q/*.png')),'quads')
