import importlib.util, math, subprocess, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('design',ROOT.parent/'singular-values-ch0'/'render.py'); b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
W,H,FPS=b.W,b.H,b.FPS
text,arrow,plane,ease=b.text,b.arrow,b.plane,b.ease
def text(d,xy,s,*args,**kwargs):
 return b.text(d,xy,s.replace('‖','||'),*args,**kwargs)
BLUE,ORANGE,PURPLE,GREEN,WHITE,MUTED=b.BLUE,b.ORANGE,b.PURPLE,b.GREEN,b.WHITE,b.MUTED
ENDS=[4,10,16,20,24,30,36,42,49,54,59,65,70,77,82,87,95,100]
LINES=['행렬을 이용해 벡터를 변환하면, 일반적으로 벡터의 크기와 방향이 함께 변화합니다.','고윳값은 이 중에서 벡터가 원래 놓여 있던 직선을 유지하는 특별한 경우를 다룹니다.','하지만 이번에는 방향이 어떻게 변하는지에 관계없이, 오직 벡터의 길이가 얼마나 변화하는지만 살펴보겠습니다.','먼저 이차원 평면 위에 하나의 벡터를 그려보겠습니다.','이 벡터에 행렬 에이를 곱하면 새로운 벡터가 만들어집니다.','변환된 벡터의 길이를 원래 벡터의 길이로 나누면, 행렬에 의해 길이가 얼마나 변화했는지 알 수 있습니다.','이 값이 1보다 크다면 벡터의 길이가 늘어난 것이고, 1보다 작다면 길이가 줄어든 것입니다.','그런데 선형변환에서는 원래 벡터의 길이를 두 배로 늘리면, 변환된 벡터의 길이도 두 배로 늘어납니다.','따라서 같은 방향에 놓인 벡터라면, 처음 길이가 얼마인지와 관계없이 길이의 변화 배율은 동일합니다.','결국 우리가 관찰해야 하는 것은 벡터의 크기가 아니라, 처음 벡터가 놓여 있던 방향입니다.','이를 좀 더 간단하게 살펴보기 위해, 길이가 1인 단위벡터를 사용해 보겠습니다.','입력 벡터의 길이가 항상 1이라면, 변환된 벡터의 길이 자체가 곧 길이의 변화 배율이 됩니다.','이제 단위벡터의 방향을 조금씩 회전시키면서, 동일한 행렬을 계속해서 적용해 보겠습니다.','입력 벡터의 길이는 항상 일정하지만, 변환된 벡터의 길이는 처음 벡터의 방향에 따라 연속적으로 변화합니다.','어떤 방향에서는 길이가 크게 늘어나고, 또 다른 방향에서는 길이가 크게 줄어듭니다.','이처럼 하나의 행렬이라도 공간의 모든 방향에 동일한 배율로 작용하는 것은 아닙니다.','그렇다면 무수히 많은 방향 중에서 길이가 가장 크게 늘어나는 방향과, 길이가 가장 작아지는 방향을 찾아낼 수 있을까요?','이 질문에 답하기 위해, 이번에는 모든 방향의 단위벡터를 하나의 도형으로 표현해 보겠습니다.']
TITLES=['크기와 방향이 함께 바뀌는 변환','고윳값이 관찰하는 특별한 경우','방향에서 길이로','하나의 벡터','행렬을 적용하면','길이의 변화 배율','1을 기준으로 비교하기','입력 길이가 두 배가 된다면?','처음 길이는 달라도, 배율은 같다','관찰해야 하는 것은 입력 방향','길이를 1로 고정하기','출력 길이 = 길이 변화 배율','단위벡터의 방향을 바꾸면?','방향에 따라 달라지는 출력 길이','늘어나는 방향, 줄어드는 방향','하나의 행렬, 방향마다 다른 배율','최대와 최소는 어디에 있을까?','모든 방향의 단위벡터를 하나의 도형으로']
A=np.array([[1.,2.],[0.,1.]])
def unit(a):return np.array([math.cos(a),math.sin(a)])
def circle(d,c,s):
 for a in np.arange(0,2*math.pi,.13):
  d.line([b.point(c,unit(a),s),b.point(c,unit(a+.065),s)],fill='#35557c',width=2)
def pair(d,p,c1=(490,520),c2=(1370,520),s=110,output=True):
 for c in [c1,c2]:plane(d,c,s)
 arrow(d,c1,p,BLUE,s)
 if output:arrow(d,c2,A@p,ORANGE,s)
 text(d,(960,c1[1]),'A →',42,MUTED)
def bars(d,x,y,length,col,label):
 text(d,(x,y-35),label,28,col,'lm');d.rounded_rectangle((x,y,x+max(2,length),y+20),8,fill=col)
def graph(d,box,theta=None,upto=2*math.pi,extrema=False):
 x,y,w,h=box
 for k in range(4):
  yy=y+h-k*h/3;d.line([(x,yy),(x+w,yy)],fill=b.GRID,width=1);text(d,(x-25,yy),str(k),22,MUTED)
 for k in range(5):
  xx=x+w*k/4;d.line([(xx,y),(xx,y+h)],fill=b.GRID,width=1);text(d,(xx,y+h+32),f'{90*k}°',22,MUTED)
 d.line([(x,y+h-h/3),(x+w,y+h-h/3)],fill=BLUE,width=2)
 def gp(a):return (x+w*a/(2*math.pi),y+h-np.linalg.norm(A@unit(a))*h/3)
 pts=[gp(a) for a in np.linspace(0,max(.001,upto),400)];d.line(pts,fill=ORANGE,width=4)
 if theta is not None:
  p=gp(theta);d.line([(p[0],y),(p[0],y+h)],fill=PURPLE,width=2);d.ellipse((p[0]-7,p[1]-7,p[0]+7,p[1]+7),fill=PURPLE)
 if extrema:
  for a,label,col in [(3*math.pi/8,'최대?',GREEN),(11*math.pi/8,'최대?',GREEN),(7*math.pi/8,'최소?',PURPLE),(15*math.pi/8,'최소?',PURPLE)]:
   xx,yy=gp(a);d.ellipse((xx-10,yy-10,xx+10,yy+10),fill=col);text(d,(xx,yy-32),label,28,col)
def frame(t):
 im=Image.new('RGB',(W,H),b.BG);d=ImageDraw.Draw(im)
 i=next((i for i,e in enumerate(ENDS) if t<e),17);q=t-(ENDS[i-1] if i else 0)
 text(d,(90,58),'LINEAR ALGEBRA  /  01',24,MUTED,'lm');text(d,(1830,58),'방향이 아닌 길이의 변화',24,MUTED,'rm');d.line([(90,100),(1830,100)],fill=b.GRID,width=2)
 text(d,(960,166),TITLES[i],46)
 if i==0:
  pair(d,np.array([1.,1.]));arrow(d,(1370,520),np.array([1.,1.])+ease((q-.7)/2)*np.array([2.,0.]),ORANGE,110)
  text(d,(960,820),'A = [ 1  2 ; 0  1 ]   ·   A(x, y) = (x + 2y, y)',34,MUTED)
 elif i==1:
  c=(960,540);plane(d,c,100);z=ease(q/2)
  for a in np.arange(0,2*math.pi,math.pi/6):
   p=unit(a)*2;p[0]+=2*z*p[1];arrow(d,c,p,GREEN if abs(p[1])<.01 else '#3d4c61',100)
  d.line([(580,540),(1340,540)],fill=GREEN,width=2);text(d,(960,850),'Av = λv     ·     λ = 1',44,GREEN)
 elif i==2:
  c=(560,580);plane(d,c,100);arrow(d,c,(1,1),BLUE,110);arrow(d,c,(3,1),ORANGE,110)
  if q>1:
   z=ease((q-1)/2);bars(d,1210,440,155*z,BLUE,'입력 길이');bars(d,1210,600,347*z,ORANGE,'출력 길이')
  text(d,(960,850),'방향이 아닌 길이의 변화',40,PURPLE)
 elif i in [3,4]:
  c=(760,650);plane(d,c,120,extent=4);arrow(d,c,(1,1),BLUE,120);text(d,(880,485),'v = (1, 1)',34,BLUE)
  if i==4:arrow(d,c,np.array([3.,1.])*ease(q/1.7),ORANGE,120);text(d,(1180,485),'Av = (3, 1)',34,ORANGE)
  text(d,(960,280),'A(x, y) = (x + 2y, y)',36,MUTED)
 elif i==5:
  bars(d,430,350,220,BLUE,'입력 길이  ‖v‖ = √2');bars(d,430,490,492,ORANGE,'출력 길이  ‖Av‖ = √10')
  text(d,(960,650),'√10 / √2 = √5 ≈ 2.236',52,PURPLE)
  if q>2.5:text(d,(960,800),'s(v) = ‖Av‖ / ‖v‖    (v ≠ 0)',44)
 elif i==6:
  for j,(label,r) in enumerate([('팽창 · s > 1',math.sqrt(5)),('유지 · s = 1',1),('수축 · s < 1',1/math.sqrt(5))]):
   y=320+j*200;text(d,(340,y+20),label,36);bars(d,650,y,190,BLUE,'');bars(d,650,y+40,190*r,ORANGE,'');text(d,(1510,y+20),f'{r:.3f}배',38,PURPLE)
 elif i==7:
  c=1+ease((q-1)/3);pair(d,np.array([1.,1.])*c,c1=(400,600),c2=(1250,600),s=75)
  text(d,(960,280),'A(cv) = c(Av)',44)
  text(d,(500,835),f'입력 길이  {math.sqrt(2)*c:.3f}',34,BLUE);text(d,(1350,835),f'출력 길이  {math.sqrt(10)*c:.3f}',34,ORANGE);text(d,(960,900),'변화 배율은 언제나  √5 ≈ 2.236',32,PURPLE)
 elif i==8:
  for j,c in enumerate([.5,1,2]):
   y=320+j*160;text(d,(290,y+20),f'{c:g}v',34,MUTED);bars(d,450,y,100*c,BLUE,'');bars(d,850,y,100*c*math.sqrt(5),ORANGE,'');text(d,(1570,y+10),'√5',40,PURPLE)
  text(d,(960,850),'s(cv) = |c| ‖Av‖ / (|c| ‖v‖) = s(v)    (c ≠ 0)',36)
 elif i in [9,10]:
  c=(680,610);plane(d,c,150)
  for r in [.5,1,1.7]:
   r=r+(1-r)*ease(q/3) if i==10 else r;arrow(d,c,unit(math.pi/4)*r,BLUE,150)
  if i==10:circle(d,c,150);text(d,(1370,470),'v̂ = v / ‖v‖',48);text(d,(1370,640),'‖v̂‖ = 1',50,PURPLE)
  else:text(d,(1390,470),'크기 r → 고정',38,MUTED);text(d,(1390,620),'입력 방향 θ',52,PURPLE)
 elif i==11:
  text(d,(960,345),'s(v) = ‖Av‖ / ‖v‖',54);text(d,(960,490),'↓    ‖v‖ = 1',40,BLUE)
  text(d,(960,650),'s(v) = ‖Av‖',64,PURPLE);text(d,(960,820),'입력 길이 1     →     출력 길이 √5 ≈ 2.236',34,MUTED)
 elif i in [12,13]:
  theta=(t-65)*math.pi/10 if t<70 else math.pi/2+(t-70)*3*math.pi/14
  # One angle drives input, output, readouts and graph cursor.
  p=unit(theta);out=A@p;z=ease((t-70)/2);cy=510-100*z;s=105-15*z
  pair(d,p,c1=(500,cy),c2=(1400,cy),s=s)
  for cx in [500,1400]:circle(d,(cx,cy),s)
  text(d,(500,265),f'입력 v · {math.degrees(theta):.1f}°',32,BLUE);text(d,(1400,265),'출력 Av · 같은 행렬을 한 번 적용',30,ORANGE)
  if i==12:
   text(d,(500,810),'‖v‖ = 1.000',38,BLUE);text(d,(1400,810),f'‖Av‖ = {np.linalg.norm(out):.3f}',38,ORANGE)
  else:graph(d,(290,720,1340,155),theta=theta,upto=theta)
 elif i==14:
  for cx,deg,label in [(520,60,'길이가 늘어나는 방향'),(1400,150,'길이가 줄어드는 방향')]:
   c=(cx,540);p=unit(math.radians(deg));plane(d,c,110);circle(d,c,110);arrow(d,c,p,BLUE,110);arrow(d,c,A@p,ORANGE,110)
   text(d,(cx,270),label,34);text(d,(cx,830),f'θ = {deg}°    ·    {np.linalg.norm(A@p):.3f}배',38,PURPLE)
 elif i==15:
  for cx in [500,1400]:plane(d,(cx,540),100)
  for a in np.arange(0,2*math.pi,math.pi/8):
   p=unit(a);arrow(d,(500,540),p,BLUE,100,3);arrow(d,(1400,540),A@p,ORANGE,100,3)
  text(d,(960,850),'동일한 입력 길이   →   방향에 따라 달라지는 출력 길이',36,PURPLE)
 elif i==16:
  graph(d,(260,350,1400,400),theta=min(2*math.pi,q*math.pi/2) if q<3 else None,extrema=q>=3)
  text(d,(960,860),'단위벡터 중에서 출력 길이의 최대와 최소를 찾는다면?',34,PURPLE)
 elif i==17:
  c=(960,545);s=230;plane(d,c,s,extent=1)
  count=8 if q<1 else 16 if q<2 else 32 if q<2.5 else 64
  for a in np.arange(0,2*math.pi,2*math.pi/count):
   p=unit(a)
   if q<3:arrow(d,c,p,BLUE,s,2)
   x,y=b.point(c,p,s);d.ellipse((x-4,y-4,x+4,y+4),fill=BLUE)
  if q>=3:d.ellipse((730,315,1190,775),outline=BLUE,width=4)
  text(d,(960,850),'x² + y² = 1',44,BLUE)
 lines=b.wrap(LINES[i],55)
 for j,line in enumerate(lines):text(d,(960,982+(j-(len(lines)-1)/2)*42),line,30)
 d.rectangle((90,1055,90+1740*t/100,1058),fill=PURPLE)
 return im
if __name__=='__main__':
 (ROOT/'timing.json').write_text(json.dumps(dict(ends=ENDS,narration=LINES),ensure_ascii=False,indent=2),encoding='utf-8')
 for t in [2,22,28,40,46,62,69,74,80,90,99.9]:frame(t).resize((960,540)).save(ROOT/f'preview-{t:g}.png')
 with (ROOT/'render.log').open('w') as log:
  p=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',str(ROOT/'visual.mp4')],stdin=subprocess.PIPE,stderr=log)
  for n in range(100*FPS):
   p.stdin.write(frame(n/FPS).tobytes())
   if n%450==0:print(f'{n/FPS:.0f}/100 sec',flush=True)
  p.stdin.close()
  if p.wait():raise RuntimeError('ffmpeg failed')
