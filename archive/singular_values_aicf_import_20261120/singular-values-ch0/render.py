import math, subprocess, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
W,H,FPS=1920,1080,30
BG='#0c111c'; GRID='#253144'; BLUE='#62a8ff'; ORANGE='#ff9c45'; GREEN='#4de09b'; PURPLE='#bc88ff'; WHITE='#edf3fc'; MUTED='#99abc2'
FONT='C:/Windows/Fonts/malgun.ttf'
def font(s): return ImageFont.truetype(FONT,s)
ENDS=[6,11,12,17,21,28,33,41,49,53,63]
LINES=[
'선형대수학에서 고윳값과 고유벡터는 행렬이 수행하는 공간의 변환을 이해하기 위한 중요한 도구입니다.',
'그렇다면 고윳값이 같은 두 행렬은 공간을 비슷한 방식으로 변화시킬까요?',
'여기 두 개의 행렬이 있습니다.',
'첫 번째 행렬은 공간에 아무런 변화도 일으키지 않는 항등행렬입니다.',
'반면 두 번째 행렬은 공간을 한쪽으로 기울이는 전단변환을 수행합니다.',
'정사각형은 평행사변형으로 변하고, 일부 벡터는 길이가 늘어나며, 다른 벡터는 오히려 길이가 줄어듭니다.',
'그런데 흥미롭게도 두 행렬의 고윳값은 모두 1과 1로 동일합니다.',
'고윳값은 고유벡터라는 특별한 방향에서 일어나는 변환을 설명하지만, 공간의 모든 방향에서 일어나는 길이 변화까지 알려주지는 않기 때문입니다.',
'그렇다면 벡터가 원래 놓여 있던 직선을 유지해야 한다는 조건에서 벗어나, 공간이 실제로 얼마나 늘어나고 줄어드는지를 측정할 수는 없을까요?',
'이러한 관점에서 등장하는 개념이 바로 특잇값입니다.',
'이번 영상에서는 특잇값이 어떻게 정의되는지, 그리고 이 숫자들이 행렬의 기하학적 구조부터 정보의 손실과 계산의 안정성까지 어떻게 설명할 수 있는지 살펴보겠습니다.']
def ease(x):
 x=max(0,min(1,x)); return x*x*(3-2*x)
def text(d,xy,s,size=40,color=WHITE,anchor='mm'):
 d.text(xy,s,font=font(size),fill=color,anchor=anchor)
def point(c,p,scale=90):return (c[0]+p[0]*scale,c[1]-p[1]*scale)
def arrow(d,c,p,col,scale=90,width=5):
 a=np.array(c,float); b=np.array(point(c,p,scale)); v=b-a; n=np.linalg.norm(v)
 if n<2:return
 u=v/n; q=np.array([-u[1],u[0]])
 d.line([tuple(a),tuple(b)],fill=col,width=width)
 d.polygon([tuple(b),tuple(b-u*17+q*7),tuple(b-u*17-q*7)],fill=col)
def plane(d,c,scale=90,shear=0,extent=3):
 def pt(x,y):return point(c,(x+shear*y,y),scale)
 # Clipped per-panel layer keeps shear lines inside their coordinate panel.
 layer=Image.new('RGBA',(W,H)); ld=ImageDraw.Draw(layer)
 for k in range(-extent*2,extent*2+1):
  z=k/2; ld.line([pt(z,-extent),pt(z,extent)],fill=GRID,width=1);ld.line([pt(-extent,z),pt(extent,z)],fill=GRID,width=1)
 ld.line([pt(-extent,0),pt(extent,0)],fill='#4b5d74',width=2);ld.line([pt(0,-extent),pt(0,extent)],fill='#4b5d74',width=2)
 box=(int(c[0]-extent*scale),int(c[1]-extent*scale),int(c[0]+extent*scale),int(c[1]+extent*scale))
 d._image.paste(layer.crop(box),box[:2],layer.crop(box))
def square(d,c,k=0,col=BLUE,scale=90):
 pts=[point(c,p,scale) for p in [(0,0),(1,0),(1+k,1),(k,1)]]
 d.polygon(pts,fill='#192b42');d.line(pts+[pts[0]],fill=col,width=4)
 arrow(d,c,(1,0),col,scale);arrow(d,c,(k,1),col,scale)
def matrix(d,c,name,rows,col):
 text(d,(c[0],c[1]-105),name,42,col)
 x,y=c
 d.line([(x-125,y-65),(x-140,y-65),(x-140,y+65),(x-125,y+65)],fill=col,width=3)
 d.line([(x+125,y-65),(x+140,y-65),(x+140,y+65),(x+125,y+65)],fill=col,width=3)
 for i in range(2):
  for j in range(2):text(d,(x-55+j*110,y-35+i*70),str(rows[i][j]),46,ORANGE if name=='B' and (i,j)==(0,1) else WHITE)
def card(d,box):d.rounded_rectangle(box,22,fill='#121c2b',outline='#2a3a51',width=2)
def wrap(s,n=48):
 words=s.split(); out=[]; line=''
 for w in words:
  if len(line+' '+w)>n:out.append(line);line=w
  else:line=(line+' '+w).strip()
 if line:out.append(line)
 return out
def frame(t):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 i=next((i for i,e in enumerate(ENDS) if t<e),10); start=0 if i==0 else ENDS[i-1]; q=t-start
 text(d,(90,58),'LINEAR ALGEBRA  /  00',24,MUTED,'lm');text(d,(1830,58),'특잇값 · 새로운 측정 기준',24,MUTED,'rm')
 d.line([(90,100),(1830,100)],fill=GRID,width=2)
 titles=['행렬 속의 특별한 방향','고윳값이 같다면, 변환도 비슷할까?','두 행렬을 비교해 봅시다','A · 항등변환','B · 전단변환','같은 변환, 서로 다른 길이 변화','변환은 다르지만, 고윳값은 같다','고윳값이 설명하는 특별한 방향','방향의 조건을 내려놓고, 길이를 비교하면?','특잇값','특잇값이 알려주는 것']
 if i!=9:text(d,(960,166),titles[i],48)
 if i==0:
  c=(960,540); k=ease((q-1)/2)*1.2;plane(d,c,105,k)
  for a in np.arange(0,2*math.pi,math.pi/4):
   p=(1.6*math.cos(a),1.6*math.sin(a));arrow(d,c,(p[0]+k*p[1],p[1]),GREEN if abs(p[1])<.01 else BLUE,105)
  text(d,(960,875),'Av = λv',48,GREEN)
 elif i in [1,2]:
  for cx,name in [(520,'A'),(1400,'B')]:
   card(d,(cx-300,300,cx+300,740))
   if i==1:
    text(d,(cx,405),'Matrix '+name,44);text(d,(cx,560),'λ₁ = 1,  λ₂ = 1',48,GREEN)
   else:matrix(d,(cx,530),name,[[1,0 if name=='A' else 2],[0,1]],BLUE if name=='A' else ORANGE)
  text(d,(960,520),'?' if i==1 else '≠',78,PURPLE)
 elif i in [3,4,6]:
  k=0 if i==3 else 2*ease((q-.5)/2) if i==4 else 2
  for cx in [510,1410]:plane(d,(cx,540),100,k if cx==1410 else 0)
  square(d,(510,540),0,BLUE,100);square(d,(1410,540),k,BLUE if i==3 else ORANGE,100)
  text(d,(960,530),'→',76,MUTED)
  for cx,label in [(510,'변환 이전' if i!=6 else '항등변환 A'),(1410,'변환 이후' if i!=6 else '전단변환 B')]:text(d,(cx,850),label,32,MUTED)
  if i==6:
   for cx in [510,1410]:text(d,(cx,770),'λ₁ = λ₂ = 1',42,GREEN)
  else: text(d,(960,800),'Av = v' if i==3 else 'B(x, y) = (x + 2y, y)',36,GREEN if i==3 else ORANGE)
 elif i==5:
  k=2*ease((q-2)/2);u=np.array([1,2])/math.sqrt(5);v=np.array([-2,1])/math.sqrt(5)
  for cx in [510,1410]:
   c=(cx,540);plane(d,c,100)
   for p,col in [(u,BLUE),(v,PURPLE)]:arrow(d,c,(p[0]+(k*p[1] if cx==1410 else 0),p[1]),col,100)
   text(d,(cx,840),'입력 길이: 모두 1' if cx==510 else '팽창 2.41배    ·    수축 0.45배',32,MUTED if cx==510 else PURPLE)
  text(d,(960,530),'B →',50,MUTED);text(d,(960,895),'선택한 두 단위벡터의 길이 변화 배율',26,MUTED)
 elif i==7:
  c=(960,550);plane(d,c,105)
  for a in np.arange(0,2*math.pi,math.pi/6):
   p=(2*math.cos(a),2*math.sin(a));arrow(d,c,p,GREEN if abs(p[1])<.01 else (BLUE if q>5 else '#435167'),105)
  d.line([(580,550),(1340,550)],fill=GREEN,width=2)
  text(d,(1300,500),'λ = 1',34,GREEN);text(d,(960,840),'Bv = v  ·  가로 방향의 고유벡터',36,GREEN)
 elif i==8:
  c=(630,590);plane(d,c,90);p=np.array([1,2])/math.sqrt(5);b=np.array([p[0]+2*p[1],p[1]])
  arrow(d,c,p,BLUE,130);arrow(d,c,b*ease((q-1)/2),ORANGE,130)
  if q>4:
   text(d,(1430,370),'길이만 비교',36)
   d.rounded_rectangle((1210,470,1330,494),10,fill=BLUE);d.rounded_rectangle((1210,600,1500,624),10,fill=ORANGE)
   text(d,(1210,440),'변환 이전',26,BLUE,'lm');text(d,(1210,570),'변환 이후',26,ORANGE,'lm')
  text(d,(960,850),'길이의 변화만 측정할 수 있을까?',40,PURPLE)
 elif i==9:
  d.ellipse((570,355,1350,725),outline='#403258',width=2)
  text(d,(960,430),'σ',135,PURPLE);text(d,(960,600),'특잇값',80);text(d,(960,700),'Singular Value',34,MUTED)
 elif i==10:
  for j,(label,eng) in enumerate([('기하학적 구조','Geometry'),('정보의 손실','Information Loss'),('계산의 안정성','Numerical Stability')]):
   if q<j*3:continue
   cx=370+j*590;card(d,(cx-265,285,cx+265,845));cy=530
   z=ease((q-j*3)/2)
   if j==0:d.ellipse((cx-180,cy-140+80*z,cx+180,cy+140-80*z),outline=PURPLE,width=4);d.line([(cx-180,cy),(cx+180,cy)],fill=GRID,width=2)
   if j==1:
    h=max(2,int(125*(1-z)));d.ellipse((cx-180,cy-h,cx+180,cy+h),outline=BLUE,width=4)
    for a in range(-3,4):d.ellipse((cx+a*50-5,cy-5,cx+a*50+5,cy+5),fill=BLUE)
   if j==2:
    d.ellipse((cx-185,cy-22,cx+185,cy+22),outline=PURPLE,width=3);arrow(d,(cx,cy),(0,.2+1.4*z),'#ff6388',100);text(d,(cx+70,cy-160),'오차',26,'#ff6388')
   text(d,(cx,735),label,36);text(d,(cx,792),eng,24,MUTED)
  if q>9:im=Image.blend(im,Image.new('RGB',(W,H),BG),ease(q-9));d=ImageDraw.Draw(im)
 # Narration captions are separate from diagram labels.
 lines=wrap(LINES[i],55)
 for j,line in enumerate(lines):text(d,(960,982+(j-(len(lines)-1)/2)*42),line,30)
 d.rectangle((90,1055,90+1740*t/63,1058),fill=PURPLE)
 return im

if __name__=='__main__':
 for t in [3,11.5,19,26,30,37,47,51,61]:frame(t).resize((960,540)).save(ROOT/f'preview-{t:g}.png')
 cmd=['ffmpeg','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',str(ROOT/'visual.mp4')]
 with (ROOT/'render.log').open('w') as log:
  p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
  for n in range(63*FPS):
   p.stdin.write(frame(n/FPS).tobytes())
   if n%300==0:print(f'{n/FPS:.0f}/63 sec',flush=True)
  p.stdin.close()
  if p.wait():raise RuntimeError('ffmpeg failed')
 (ROOT/'timing.json').write_text(json.dumps(dict(ends=ENDS,narration=LINES),ensure_ascii=False,indent=2),encoding='utf-8')
