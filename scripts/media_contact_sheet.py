"""Create a labelled QA contact sheet from original rendered images."""
from pathlib import Path
from PIL import Image,ImageDraw
import argparse
p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('output',type=Path);p.add_argument('--start',type=int,default=0);p.add_argument('--end',type=int,default=60);p.add_argument('--step',type=int,default=1);args=p.parse_args()
files=[f for f in sorted(args.folder.glob('*.png')) if f.stem.isdigit() and args.start<=int(f.stem)<args.end][::args.step];assert files
out=Image.new('RGB',(1500,((len(files)+4)//5)*208),'#17262c');d=ImageDraw.Draw(out)
for n,f in enumerate(files):
 with Image.open(f) as im:
  im.thumbnail((296,180));x=(n%5)*300;y=(n//5)*208;out.paste(im,(x,y));d.text((x+8,y+183),f.stem,fill='white')
out.save(args.output)
