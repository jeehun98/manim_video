import importlib.util, math, subprocess, json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('design',R.parent/'singular-values-ch0/render.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
W,H,FPS=b.W,b.H,b.FPS
BLUE,ORANGE,PURPLE,GREEN,WHITE,MUTED=b.BLUE,b.ORANGE,b.PURPLE,b.GREEN,b.WHITE,b.MUTED
arrow,plane,ease=b.arrow,b.plane,b.ease
def text(d,xy,s,*args,**kw):
 for old,new in [('‖','||'),('≈','~'),('−','-'),('ᵀ','^T'),('≥','>=')]:s=s.replace(old,new)
 return b.text(d,xy,s,*args,**kw)
ENDS=[6,8,12,18,23,27,35,44,48,51,54,60,65,71,78,82,87,93,97,106,110,116,121]
LINES=['이차원 평면에서 길이가 1인 모든 벡터를 그려보면, 벡터의 끝점들은 반지름이 1인 하나의 원을 이루게 됩니다.','이것이 바로 단위 원입니다.','이제 이 모든 벡터에 동일한 행렬을 적용해 보겠습니다.','입력 벡터의 길이는 모두 같지만, 변환된 벡터의 길이는 처음 벡터가 놓여 있던 방향에 따라 달라집니다.','그리고 이 벡터들의 끝점을 연결해 보면, 원이 아닌 하나의 타원이 만들어집니다.','이 타원에는 서로 수직인 두 개의 특별한 축이 존재합니다.','하나는 타원의 중심에서 가장 멀리 떨어진 점들을 연결하는 장축이고, 다른 하나는 가장 가까운 점들을 연결하는 단축입니다.','처음 원의 반지름은 모든 방향에서 1이었으므로, 변환된 타원의 가장 긴 반지름은 행렬이 만들어낼 수 있는 최대 길이 변화 배율을 나타냅니다.','반대로 가장 짧은 반지름은 최소 길이 변화 배율을 나타냅니다.','이 두 숫자가 바로 이 행렬의 특잇값입니다.','여기서 고윳값과 특잇값의 중요한 차이를 발견할 수 있습니다.','고윳값을 구할 때는 변환 이전과 이후의 벡터가 같은 직선 위에 놓여 있어야 했습니다.','하지만 특잇값에서는 변환된 벡터가 원래 어떤 방향을 향하고 있었는지는 중요하지 않습니다.','두 벡터의 방향이 서로 다르더라도, 길이가 얼마나 변화했는지를 측정할 수 있기 때문입니다.','따라서 고윳값은 음수나 복소수가 될 수도 있지만, 길이의 변화 배율을 나타내는 특잇값은 항상 0 이상의 실수입니다.','이러한 기하학적 관계는 더 높은 차원에서도 동일하게 나타납니다.','삼차원 공간에서 모든 방향의 단위벡터를 모으면 하나의 구가 만들어집니다.','그리고 이 구에 행렬을 적용하면, 일반적으로 서로 다른 길이의 세 반축을 가진 타원체가 만들어집니다.','이때 각 반축의 길이가 행렬의 특잇값이 됩니다.','즉, 특잇값은 단순히 최대값과 최소값을 나타내는 것이 아니라, 서로 직교하는 특별한 방향들에서 일어나는 길이의 변화 배율을 나타내는 숫자들입니다.','그렇다면 이러한 숫자들을 구하기 위해 모든 방향의 벡터를 직접 관찰해야 할까요?','흥미롭게도 벡터의 길이를 수식으로 표현하는 과정에서 하나의 새로운 행렬이 등장합니다.','그리고 그 행렬의 고윳값을 이용하면, 우리가 찾고 있던 특잇값을 계산할 수 있습니다.']
TITLES=['모든 방향의 단위벡터','단위 원','모든 방향에 같은 행렬을 적용하면','같은 입력 길이, 서로 다른 출력 길이','끝점들을 연결하면, 타원','서로 수직인 두 개의 축','장축과 단축','가장 긴 반지름 = 최대 길이 변화 배율','가장 짧은 반지름 = 최소 길이 변화 배율','이 두 숫자가 특잇값','같은 행렬에서 얻는 서로 다른 정보','고윳값 · 같은 직선 위의 변환','입력 방향과 출력 방향은 달라도 된다','방향이 달라도 길이는 비교할 수 있다','특잇값은 항상 0 이상의 실수','이차원에서 삼차원으로','모든 방향의 단위벡터가 만드는 구면','단위구에서 타원체로','세 반축, 세 특잇값','최대와 최소를 넘어, 여러 주축의 배율로','모든 방향을 직접 탐색해야 할까?','벡터의 길이를 수식으로 표현하면','다시 등장하는 고윳값']
A=np.array([[1.,2.],[0.,1.]])
def unit(a):return np.array([math.cos(a),math.sin(a)])
V=[unit(math.radians(a)) for a in [67.5,157.5]];OUT=[A@p for p in V]
def curve(d,c,s=110,m=A,col=ORANGE,progress=1):
 pts=[b.point(c,m@unit(a),s) for a in np.linspace(0,2*math.pi*max(.001,progress),200)];d.line(pts,fill=col,width=4)
def axes(d,c,s=110):plane(d,c,s,extent=2)
def duo(d,rad=None,s=110):
 for c in [(500,530),(1400,530)]:axes(d,c,s)
 curve(d,(500,530),s,np.eye(2),BLUE);curve(d,(1400,530),s)
 text(d,(500,275),'입력 공간',32,BLUE);text(d,(1400,275),'출력 공간',32,ORANGE);text(d,(960,530),'A →',42,MUTED)
 if rad is not None:
  p=unit(rad);arrow(d,(500,530),p,PURPLE,s);arrow(d,(1400,530),A@p,PURPLE,s)
def principal(d,c,s=180,full=False):
 for p in OUT:
  if full:d.line([b.point(c,-p,s),b.point(c,p,s)],fill=PURPLE,width=4)
  else:arrow(d,c,p,PURPLE,s)
def project(p,c,s,angle):
 # Orthographic camera projection of actual three-dimensional coordinates.
 x,y,z=p;u=math.cos(angle)*x-math.sin(angle)*y;v=.42*(math.sin(angle)*x+math.cos(angle)*y)-.9*z
 return (c[0]+s*u,c[1]+s*v)
def wire(d,c,scales=(1,1,1),s=180,angle=.55,col=ORANGE,ax=False):
 scales=np.array(scales)
 for phi in np.linspace(.15,math.pi-.15,9):
  pts=[project(scales*np.array([math.sin(phi)*math.cos(a),math.sin(phi)*math.sin(a),math.cos(phi)]),c,s,angle) for a in np.linspace(0,2*math.pi,90)];d.line(pts,fill=col,width=1)
 for a in np.linspace(0,2*math.pi,14):
  pts=[project(scales*np.array([math.sin(phi)*math.cos(a),math.sin(phi)*math.sin(a),math.cos(phi)]),c,s,angle) for phi in np.linspace(0,math.pi,60)];d.line(pts,fill=col,width=1)
 if ax:
  for k in range(3):
   p=np.zeros(3);p[k]=scales[k];end=project(p,c,s,angle);d.line([c,end],fill=PURPLE,width=5);d.ellipse((end[0]-6,end[1]-6,end[0]+6,end[1]+6),fill=PURPLE)
def frame(t):
 im=Image.new('RGB',(W,H),b.BG);d=ImageDraw.Draw(im)
 i=next((i for i,e in enumerate(ENDS) if t<e),22);q=t-(ENDS[i-1] if i else 0)
 text(d,(90,58),'LINEAR ALGEBRA  /  02',24,MUTED,'lm');text(d,(1830,58),'단위 원에서 발견하는 특잇값',24,MUTED,'rm');d.line([(90,100),(1830,100)],fill=b.GRID,width=2)
 text(d,(960,166),TITLES[i],44)
 if i==0:
  c=(960,545);axes(d,c,230);curve(d,c,230,np.eye(2),BLUE)
  if q>1:
   for a in np.linspace(0,2*math.pi,8 if q<2 else 24 if q<4 else 64,endpoint=False):
    p=unit(a)
    if q<5:arrow(d,c,p,'#365478',230,2)
    x,y=b.point(c,p,230);d.ellipse((x-4,y-4,x+4,y+4),fill=BLUE)
  text(d,(960,850),'‖v‖ = 1',40,BLUE)
 elif i==1:
  c=(650,545);axes(d,c,210);curve(d,c,210,np.eye(2),BLUE);arrow(d,c,(1,0),BLUE,210);text(d,(760,500),'1',36,BLUE)
  text(d,(1330,475),'단위 원 · Unit Circle',44);text(d,(1330,620),'x² + y² = 1',44,BLUE)
 elif i in [2,3,4]:
  for c in [(500,530),(1400,530)]:axes(d,c,110)
  text(d,(960,300),'A(x, y) = (x + 2y, y)',34,MUTED);text(d,(960,530),'A →',42,MUTED)
  k=ease(q/2) if i==2 else 1;m=np.array([[1.,2*k],[0.,1.]])
  for a in np.linspace(0,2*math.pi,32,endpoint=False):
   p=unit(a)
   if i!=4 or q<2:
    arrow(d,(500,530),p,BLUE if i==2 else '#365478',110,2);arrow(d,(1400,530),m@p,ORANGE if i==2 else '#644a34',110,2)
   for c,v,col in [((500,530),p,BLUE),((1400,530),m@p,ORANGE)]:
    x,y=b.point(c,v,110);d.ellipse((x-3,y-3,x+3,y+3),fill=col)
  if i==3:
   a=q*math.pi/3;p=unit(a);arrow(d,(500,530),p,BLUE,110);arrow(d,(1400,530),A@p,ORANGE,110);text(d,(500,820),'입력 길이 1.000',36,BLUE);text(d,(1400,820),f'출력 길이 {np.linalg.norm(A@p):.3f}',36,ORANGE)
  if i==4:
   for c,m,col in [((500,530),np.eye(2),BLUE),((1400,530),A,ORANGE)]:curve(d,c,110,m,col,ease((q-1)/2))
 elif i in [5,6,9]:
  c=(960,530);axes(d,c,165);curve(d,c,165);principal(d,c,165,full=i!=9)
  if i==5:
   e=OUT[0]/np.linalg.norm(OUT[0]);f=OUT[1]/np.linalg.norm(OUT[1]);p=[np.zeros(2),e*.18,(e+f)*.18,f*.18];d.line([b.point(c,v,165) for v in p],fill=WHITE,width=3);text(d,(1030,470),'90°',28)
  if i==6:
   p=A@unit(q*math.pi/3);arrow(d,c,p,'#718198',165,2);text(d,(600,820),'장축 · 중심에서 가장 먼 점',32,PURPLE);text(d,(1330,880),'단축 · 중심에서 가장 가까운 점',32,PURPLE)
  if i==9:
   text(d,(520,800),'σ₁ = 1 + √2 ≈ 2.414',42,PURPLE);text(d,(1400,800),'σ₂ = √2 − 1 ≈ 0.414',42,PURPLE)
 elif i in [7,8,12]:
  a=math.radians(67.5 if i!=8 else 67.5+90*ease(q/2));duo(d,a)
  val=np.linalg.norm(A@unit(a));text(d,(500,800),f'입력 방향 {math.degrees(a):.1f}° · 길이 1',34,BLUE)
  angle=math.degrees(math.atan2(*(A@unit(a))[::-1]));text(d,(1400,800),f'출력 방향 {angle:.1f}° · 길이 {val:.3f}',34,PURPLE)
  text(d,(960,880),'입력 방향과 출력 방향이 같을 필요는 없다' if i==12 else ('최대 길이 변화 배율 ≈ 2.414' if i==7 else '최소 길이 변화 배율 ≈ 0.414'),34,PURPLE)
 elif i==10:
  for cx,col,label,value in [(500,GREEN,'고윳값 · Eigenvalues','λ₁ = λ₂ = 1'),(1400,PURPLE,'특잇값 · Singular Values','σ₁ ≈ 2.414   σ₂ ≈ 0.414')]:
   b.card(d,(cx-365,360,cx+365,740));text(d,(cx,440),label,34,col);text(d,(cx,580),value,40,col)
  text(d,(960,280),'A = [ 1  2 ; 0  1 ]',34,MUTED)
 elif i==11:
  for cx in [500,1400]:
   axes(d,(cx,530),110);d.line([(cx-300,530),(cx+300,530)],fill=GREEN,width=2);arrow(d,(cx,530),(1,0),GREEN,160)
  text(d,(960,530),'A →',42,MUTED);text(d,(960,825),'Av = λv   ·   λ = 1',48,GREEN)
 elif i==13:
  c=(540,570);axes(d,c,120);arrow(d,c,V[0],BLUE,140);arrow(d,c,OUT[0],ORANGE,140)
  for y,l,col,label in [(430,140,BLUE,'입력 길이 1'),(620,140*np.linalg.norm(OUT[0]),ORANGE,'출력 길이 2.414…')]:
   text(d,(1150,y-45),label,32,col,'lm');d.rounded_rectangle((1150,y,1150+l*ease((q-1)/2),y+22),8,fill=col)
  text(d,(960,850),'‖Av₁‖ = σ₁ ‖v₁‖',44,PURPLE)
 elif i==14:
  text(d,(500,300),'고윳값 · 다른 행렬의 예시',34,GREEN);text(d,(1400,300),'특잇값 · 길이의 배율',34,PURPLE)
  d.line([(270,560),(770,560)],fill=MUTED,width=2);d.line([(520,340),(520,760)],fill=MUTED,width=2)
  for x,y,label in [(350,560,'−2'),(610,440,'a + bi'),(520,380,'i')]:d.ellipse((x-7,y-7,x+7,y+7),fill=GREEN);text(d,(x+40,y-35),label,30,GREEN)
  d.line([(1120,560),(1700,560)],fill=PURPLE,width=4);text(d,(1100,610),'0',28);text(d,(1400,760),'σ ≥ 0',68,PURPLE);text(d,(500,820),'실수 또는 복소수',36,GREEN)
 elif i in [15,16,17,18,19]:
  ang=.55+.1*(t-78)
  if i==15:
   curve(d,(470,540),185,np.eye(2),BLUE);wire(d,(1400,540),s=185,angle=ang,col=BLUE);text(d,(960,540),'2D → 3D',36,MUTED)
  elif i==16:
   wire(d,(730,550),s=250,angle=ang,col=BLUE);text(d,(1430,470),'단위구 · Unit Sphere',40);text(d,(1430,610),'x² + y² + z² = 1',38,BLUE)
  elif i in [17,18]:
   z=ease((q-1)/3) if i==17 else 1;sc=(1+z,1,1-.5*z);c=(780,550)
   wire(d,c,s=200,angle=ang,col='#2d4564');wire(d,c,sc,s=200,angle=ang,col=ORANGE,ax=True)
   text(d,(1420,300),'B = diag(2, 1, 0.5)',36,MUTED)
   for j,v in enumerate(sc):text(d,(1470,450+j*135),f'σ{["₁","₂","₃"][j]} = {v:g}' if i==18 else f'반축 {j+1} · {v:.2f}',46,PURPLE)
  else:
   wire(d,(500,480),s=150,angle=ang,col=BLUE,ax=True);wire(d,(1400,480),(2,1,.5),s=150,angle=ang,col=ORANGE,ax=True);text(d,(960,480),'B →',40,MUTED)
   for j,v in enumerate([2,1,.5]):
    cx=360+j*600;text(d,(cx,760),['최대 배율','중간 배율','최소 배율'][j],30,MUTED);d.rounded_rectangle((cx-200,810,cx-200+v*180,830),8,fill=PURPLE);text(d,(cx,885),f'σ{["₁","₂","₃"][j]} = {v:g}',36,PURPLE)
 elif i==20:
  c=(600,530);curve(d,c,210,np.eye(2),BLUE)
  for a in np.linspace(0,2*math.pi,64,endpoint=False):arrow(d,c,unit(a),'#2d4564',210,2)
  arrow(d,c,unit(q*2),WHITE,210)
  for j in range(4):text(d,(1320,350+j*120),f's(θ{j+1}) = …',36,MUTED)
  text(d,(1630,550),'?',100,PURPLE)
 elif i==21:
  text(d,(960,360),'‖v‖² = x² + y²',54,BLUE)
  if q>1.5:text(d,(960,530),'‖v‖² = vᵀv',54)
  if q>3.5:text(d,(960,740),'‖Av‖² = (Av)ᵀ(Av)',58,PURPLE)
 elif i==22:
  if q<4:
   for cx,col,label in [(380,BLUE,'A'),(960,GREEN,'?'),(1540,PURPLE,'σ₁, σ₂, …')]:b.card(d,(cx-200,330,cx+200,600));text(d,(cx,460),label,64,col)
   text(d,(670,450),'→',54,MUTED);text(d,(1250,450),'→',54,MUTED);text(d,(960,660),'길이 측정    →    새로운 행렬의 고윳값    →    특잇값',30,MUTED)
  text(d,(960,800 if q<4 else 540),'‖Av‖² = (Av)ᵀ(Av)',58,PURPLE)
 lines=b.wrap(LINES[i],55)
 for j,line in enumerate(lines):text(d,(960,982+(j-(len(lines)-1)/2)*42),line,30)
 d.rectangle((90,1055,90+1740*t/121,1058),fill=PURPLE)
 return im
if __name__=='__main__':
 (R/'timing.json').write_text(json.dumps(dict(ends=ENDS,narration=LINES),ensure_ascii=False,indent=2),encoding='utf-8')
 for t in [3,10,20,25,31,40,46,50,63,69,76,85,91,95,102,114,120.9]:frame(t).resize((960,540)).save(R/f'preview-{t:g}.png')
 with (R/'render.log').open('w') as log:
  p=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',str(R/'visual.mp4')],stdin=subprocess.PIPE,stderr=log)
  for n in range(121*FPS):
   p.stdin.write(frame(n/FPS).tobytes())
   if n%600==0:print(f'{n/FPS:.0f}/121 sec',flush=True)
  p.stdin.close()
  if p.wait():raise RuntimeError('ffmpeg failed')
