import importlib.util,math,subprocess,json,re
from pathlib import Path
from functools import lru_cache
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('chapter2',R.parent/'singular-values-ch2/render.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
b=p.b;W,H,FPS=b.W,b.H,b.FPS
BLUE,ORANGE,PURPLE,GREEN,WHITE,MUTED=p.BLUE,p.ORANGE,p.PURPLE,p.GREEN,p.WHITE,p.MUTED
TEAL='#2dd4bf';text,arrow,plane,ease=p.text,p.arrow,p.plane,p.ease
A=p.A;M=A.T@A;V=p.V;L=np.array([3+2*math.sqrt(2),3-2*math.sqrt(2)])
ENDS=[5,8,14,18,24,29,34,38,43,48,57,60,66,71,78,82,88,92,97,102,107,112,118,123,132,136,141,145,153,158,167,175,180]
LINES=['특잇값을 구하기 위해 우리가 알아내고 싶은 것은 행렬을 적용한 벡터의 길이입니다.','먼저 벡터의 길이를 수학적으로 표현해 보겠습니다.','이차원 벡터의 길이는 두 성분을 각각 제곱한 뒤, 더하고 제곱근을 취하여 구할 수 있습니다.','여기서 제곱근을 잠시 제외하고 길이의 제곱만 생각해 보겠습니다.','두 성분의 제곱을 더하는 연산은 벡터를 전치한 뒤 자기 자신과 곱하는 연산으로 표현할 수 있습니다.','이러한 표현은 이차원뿐만 아니라 더 높은 차원에서도 동일하게 사용할 수 있습니다.','그렇다면 행렬을 적용한 벡터의 길이 제곱은 어떻게 표현할 수 있을까요?','기존 벡터 대신 행렬 에이와 벡터 브이의 곱을 넣어보겠습니다.','행렬의 곱을 전치하면 곱셈의 순서가 반대로 바뀌므로, 이 식을 다시 정리할 수 있습니다.','그러면 두 벡터 사이에 에이의 전치행렬과 에이의 곱이라는 새로운 행렬이 등장합니다.','흥미로운 점은 우리가 처음부터 이러한 행렬을 만들려고 했던 것이 아니라, 변환된 벡터의 길이를 측정하는 과정에서 자연스럽게 등장했다는 것입니다.','이 새로운 행렬에는 몇 가지 중요한 성질이 존재합니다.','원래 행렬이 정사각행렬이 아니더라도, 새롭게 만들어진 행렬은 항상 정사각행렬입니다.','또한 행과 열을 서로 바꾸어도 동일한 형태를 유지하는 대칭행렬입니다.','대칭행렬의 중요한 성질 중 하나는 서로 직교하는 고유벡터들로 공간의 기저를 구성할 수 있다는 것입니다.','이 고유벡터들 중 하나를 선택하고, 그 길이를 1로 만들어 보겠습니다.','새로운 행렬을 이 벡터에 곱하면, 고유벡터의 성질에 의해 단순히 고윳값을 곱하는 것과 같아집니다.','이 관계를 변환된 벡터의 길이 제곱을 나타내는 식에 대입해 보겠습니다.','고윳값을 밖으로 꺼내면 벡터와 자기 자신의 내적만 남습니다.','그런데 우리가 선택한 벡터는 길이가 1인 단위벡터이므로, 이 내적의 결과는 1입니다.','결국 변환된 벡터의 길이 제곱은 새로운 행렬의 고윳값과 같아집니다.','따라서 고윳값에 제곱근을 취하면, 실제 벡터의 길이 변화 배율을 구할 수 있습니다.','그렇다면 왜 이러한 방향들이 타원의 가장 긴 반축과 가장 짧은 반축에 대응하는 것일까요?','이번에는 임의의 단위벡터를 서로 직교하는 두 고유벡터의 합으로 표현해 보겠습니다.','이 벡터에 기존 행렬을 적용하고 길이의 제곱을 계산하면, 두 고윳값에 각각의 성분을 제곱하여 곱한 뒤 더한 형태가 나타납니다.','입력 벡터의 길이가 1이므로, 두 성분의 제곱을 더한 값은 항상 1입니다.','즉, 변환된 벡터의 길이 제곱은 두 고윳값의 가중평균으로 표현되는 것입니다.','따라서 이 값은 두 고윳값의 범위를 벗어날 수 없습니다.','가장 큰 고윳값에 해당하는 방향에서 길이는 최대가 되고, 가장 작은 고윳값에 해당하는 방향에서 길이는 최소가 됩니다.','이것이 새로운 행렬의 고유벡터들이 타원의 주축에 대응하는 입력 방향이 되는 이유입니다.','결국 특잇값은 원래 행렬과 그 전치행렬을 이용해 새로운 행렬을 구성하고, 그 행렬의 고윳값에 제곱근을 취하여 정의할 수 있습니다.','고윳값만으로는 충분히 설명할 수 없었던 공간의 길이 변화를, 새로운 행렬을 구성하고 다시 고윳값을 이용함으로써 설명할 수 있게 된 것입니다.','이제 이렇게 얻어낸 특잇값들이 행렬에 관한 어떤 정보들을 담고 있는지 살펴보겠습니다.']
TITLES=['우리가 구하고 싶은 것은 변환된 벡터의 길이','벡터의 길이로 돌아가기','피타고라스 정리','길이 대신 길이의 제곱','제곱의 합을 내적으로 표현하기','차원이 달라도 같은 표현','변환된 벡터의 길이 제곱은?','v 대신 Av를 대입하면','전치하면 곱셈의 순서가 바뀐다','길이를 측정하다 발견한 새로운 행렬','우리는 길이를 구하려고 했을 뿐이다','새로운 행렬을 관찰하기','직사각행렬에서도 정사각행렬이 만들어진다','행과 열을 바꿔도 같은 대칭행렬','서로 직교하는 고유기저','하나의 단위 고유벡터 선택','새로운 행렬 M을 적용하면','고유벡터 관계를 대입하기','스칼라인 고윳값을 밖으로','단위벡터의 자기 내적은 1','길이의 제곱 = M의 고윳값','제곱근을 취하면 실제 길이가 된다','왜 이 방향에서 최대와 최소가 될까?','임의의 단위벡터를 고유기저로 표현','직교성에 의해 교차항이 사라진다','두 성분의 제곱을 더하면 1','길이의 제곱은 고윳값의 가중평균','가중평균은 두 값 사이에 있다','최대와 최소가 발생하는 방향','고유벡터와 타원의 반축을 연결하면','특잇값의 수학적 정의','같은 도구, 새로운 대상','특잇값에는 어떤 정보가 담겨 있을까?']
@lru_cache(None)
def mf(size):return ImageFont.truetype('C:/Windows/Fonts/cambria.ttc',size)
def formula(d,xy,s,size=60,col=WHITE):
 parts=re.split(r'(\^T)',s);runs=[(a.replace('‖','||'),mf(int(size*.65)) if a=='^T' else mf(size),-size*.3 if a=='^T' else 0) for a in parts if a]
 widths=[d.textlength('T' if a=='^T' else a,font=f) for a,f,z in runs];x=xy[0]-sum(widths)/2
 for (a,f,z),w in zip(runs,widths):d.text((x,xy[1]+z),'T' if a=='^T' else a,font=f,fill=col,anchor='lm');x+=w
def panel(d,c,s=140):plane(d,c,s,extent=2)
def basis(d,c,s=180):
 panel(d,c,s);p.curve(d,c,s,np.eye(2),BLUE)
 for v,col in zip(V,[PURPLE,BLUE]):arrow(d,c,v,col,s)
def weights(d,w,y=760):
 x=400;width=1120;k=max(0,min(1,w));d.rectangle((x,y,x+width*k,y+34),fill=PURPLE);d.rectangle((x+width*k,y,x+width,y+34),fill=BLUE)
 formula(d,(660,y+75),f'c₁² = {k:.3f}',34,PURPLE);formula(d,(1260,y+75),f'c₂² = {1-k:.3f}',34,BLUE)
def cellmatrix(d,c,rows,cols,col):
 for i in range(rows):
  for j in range(cols):
   x=c[0]+(j-(cols-1)/2)*90;y=c[1]+(i-(rows-1)/2)*90;d.rounded_rectangle((x-36,y-36,x+36,y+36),5,fill='#182936',outline=col,width=2)
def frame(t):
 im=Image.new('RGB',(W,H),b.BG);d=ImageDraw.Draw(im)
 i=next((i for i,e in enumerate(ENDS) if t<e),32);q=t-(ENDS[i-1] if i else 0)
 text(d,(90,58),'LINEAR ALGEBRA  /  03',24,MUTED,'lm');text(d,(1830,58),'특잇값은 어떻게 계산할까?',24,MUTED,'rm');d.line([(90,100),(1830,100)],fill=b.GRID,width=2);text(d,(960,166),TITLES[i],44)
 if i==0:
  p.duo(d,math.radians(67.5));formula(d,(500,830),'‖v‖ = 1',46,BLUE);formula(d,(1400,830),'‖Av‖ = ?',46,ORANGE)
 elif i in [1,2]:
  c=(520,640);panel(d,c,140);arrow(d,c,(1.4,1),BLUE,140);e=b.point(c,(1.4,1),140);d.line([c,(e[0],c[1]),e],fill=TEAL,width=3)
  text(d,(620,680),'x',32,BLUE);text(d,(760,560),'y',32,TEAL)
  if i==2:
   d.rectangle((520,640,716,836),outline=BLUE,width=2);text(d,(618,740),'x²',36,BLUE)
   formula(d,(1310,500),'‖v‖² = x² + y²',54);formula(d,(1310,670),'‖v‖ = √(x² + y²)',54,BLUE)
  else:formula(d,(1300,530),'v = (x, y)^T',64,BLUE)
 elif i==3:
  formula(d,(960,400),'‖v‖ = √(x² + y²)',66,BLUE);text(d,(960,540),'↓  양변을 제곱',32,MUTED);formula(d,(960,700),'‖v‖² = x² + y²',70)
 elif i==4:
  formula(d,(960,350),'v^T v = [x  y] (x, y)^T',62,BLUE)
  formula(d,(960,540),'= x · x + y · y',62,TEAL)
  if q>2:formula(d,(960,740),'= x² + y² = ‖v‖²',64)
 elif i==5:
  for y,s in [(330,'2D :  x₁² + x₂²'),(480,'3D :  x₁² + x₂² + x₃²'),(640,'nD :  x₁² + … + xₙ²')]:formula(d,(960,y),s,52,MUTED)
  formula(d,(960,830),'‖v‖² = v^T v',70,BLUE)
 elif i==6:
  for cx in [500,1400]:panel(d,(cx,530),110)
  arrow(d,(500,530),(.7,.7),BLUE,160);arrow(d,(1400,530),(2.1,.7),ORANGE,160);text(d,(960,530),'A →',46,MUTED);formula(d,(960,825),'‖Av‖² = ?',70,ORANGE)
 elif i in [7,8,9]:
  formula(d,(960,350),'‖Av‖² = (Av)^T (Av)',66)
  if i>=8:formula(d,(960,540),'(Av)^T = v^T A^T',62,BLUE)
  if i>=9:formula(d,(960,690),'M = A^T A',72,TEAL)
  formula(d,(960,850),'‖Av‖² = v^T A^T A v' if i<9 else '‖Av‖² = v^T M v',66,TEAL)
 elif i==10:
  for cx,label,col in [(380,'‖Av‖',BLUE),(960,'(Av)^T (Av)',ORANGE),(1540,'A^T A',TEAL)]:b.card(d,(cx-230,330,cx+230,630));formula(d,(cx,475),label,60,col)
  for cx in [670,1250]:text(d,(cx,480),'→',50,MUTED)
  formula(d,(960,800),'v^T M v = ‖Av‖²',66,TEAL)
 elif i==11:
  formula(d,(960,340),'M = A^T A',76,TEAL)
  for cx,s in [(420,'정사각행렬'),(960,'대칭행렬'),(1500,'직교 고유기저')]:b.card(d,(cx-220,510,cx+220,760));text(d,(cx,635),s,38,TEAL)
 elif i==12:
  for cx,r,c,label,col in [(420,2,3,'A^T : n × m',MUTED),(960,3,2,'A : m × n',WHITE),(1500,2,2,'M : n × n',TEAL)]:cellmatrix(d,(cx,510),r,c,col);formula(d,(cx,770),label,46,col)
  text(d,(680,510),'×',54);text(d,(1220,510),'=',54);text(d,(960,860),'크기를 설명하기 위한 일반적인 직사각행렬 예시',28,MUTED)
 elif i==13:
  formula(d,(960,310),'A^T A = [1  0 ; 2  1] [1  2 ; 0  1]',52)
  b.matrix(d,(620,560),'M',[[1,2],[2,5]],TEAL);formula(d,(1370,520),'M^T = M',70,TEAL);formula(d,(1370,690),'(A^T A)^T = A^T A',48)
 elif i in [14,15]:
  c=(780,550);basis(d,c,210)
  if i==15:arrow(d,c,V[0]*(1.8-.8*ease(q/2)),PURPLE,210)
  formula(d,(1430,450),'Mvᵢ = λᵢvᵢ',58,TEAL);formula(d,(1430,650),'v₁^T v₂ = 0' if i==14 else '‖vᵢ‖ = 1',52,PURPLE)
 elif i==16:
  for cx in [450,1250]:panel(d,(cx,650),65)
  arrow(d,(450,650),V[0],PURPLE,65);arrow(d,(1250,650),V[0]*(1+(L[0]-1)*ease(q/3)),TEAL,65)
  text(d,(960,520),'M →',50,TEAL);formula(d,(960,300),'Mv₁ = λ₁v₁',70,TEAL);formula(d,(960,850),'λ₁ = 3 + 2√2 ≈ 5.828',56,GREEN)
  text(d,(960,910),'M의 배율은 A의 실제 길이 배율과 다릅니다',26,MUTED)
 elif i in [17,18,19,20,21]:
  steps=['‖Avᵢ‖² = vᵢ^T Mvᵢ','‖Avᵢ‖² = vᵢ^T (λᵢvᵢ)','‖Avᵢ‖² = λᵢ (vᵢ^T vᵢ)','vᵢ^T vᵢ = ‖vᵢ‖² = 1','‖Avᵢ‖² = λᵢ','‖Avᵢ‖ = √λᵢ']
  j=i-17;formula(d,(960,350),steps[max(0,j)],58,MUTED);formula(d,(960,570),steps[min(5,j+1)],76,TEAL if i<20 else PURPLE)
  if i>=20:formula(d,(960,800),'λᵢ = ‖Avᵢ‖² ≥ 0' if i==20 else '√5.828… = 2.414…',54,GREEN)
 elif i==22:
  c=(700,550);p.curve(d,c,160);p.principal(d,c,160,True);text(d,(1460,450),'왜 최대일까?',42,PURPLE);text(d,(1460,650),'왜 최소일까?',42,BLUE);formula(d,(960,850),'‖v‖ = 1',44)
 elif i==23:
  c=(650,570);basis(d,c,210);v=.8*V[0]+.6*V[1];arrow(d,c,v,WHITE,210)
  a=b.point(c,.8*V[0],210);e=b.point(c,v,210);d.line([a,e],fill=BLUE,width=3)
  formula(d,(1390,460),'v = c₁v₁ + c₂v₂',58);formula(d,(1390,650),'c₁ = 0.8,  c₂ = 0.6',44,MUTED)
 elif i==24:
  formula(d,(960,320),'‖Av‖² = v^T Mv',60)
  formula(d,(960,470),'= (c₁v₁ + c₂v₂)^T M(c₁v₁ + c₂v₂)',48,MUTED)
  formula(d,(960,610),'v₁^T v₂ = v₂^T v₁ = 0',56,BLUE)
  text(d,(960,710),'직교하는 성분 사이의 교차항은 0',32,MUTED)
  formula(d,(960,840),'‖Av‖² = λ₁c₁² + λ₂c₂²',68,PURPLE)
 elif i in [25,26,27]:
  w=.64 if i!=27 else .5+.5*math.sin(q*math.pi/2)
  formula(d,(960,330),'c₁² + c₂² = 1' if i==25 else '‖Av‖² = λ₁c₁² + λ₂c₂²',64)
  weights(d,w,480)
  if i==27:
   x=400+1120*w;y=740;d.line([(400,y),(1520,y)],fill=TEAL,width=4);d.ellipse((x-12,y-12,x+12,y+12),fill=ORANGE);formula(d,(400,800),'λ₂',38,BLUE);formula(d,(1520,800),'λ₁',38,PURPLE)
   formula(d,(960,870),'λ₂ ≤ ‖Av‖² ≤ λ₁',54)
  else:formula(d,(960,760),'0.64λ₁ + 0.36λ₂ = 3.792…' if i==26 else '‖v‖² = 1',58,GREEN)
 elif i in [28,29]:
  a=(math.pi/4*(1-ease(q/3)) if q<4 else math.pi/2*ease((q-4)/3)) if i==28 else 0
  v=math.cos(a)*V[0]+math.sin(a)*V[1];w=math.cos(a)**2
  for c in [(500,475),(1400,475)]:panel(d,c,95)
  p.curve(d,(500,475),95,np.eye(2),BLUE);p.curve(d,(1400,475),95)
  for j,col in enumerate([PURPLE,BLUE]):arrow(d,(500,475),V[j],col,95);arrow(d,(1400,475),A@V[j],col,95)
  if i==28:arrow(d,(500,475),v,WHITE,95);arrow(d,(1400,475),A@v,ORANGE,95);weights(d,w,745);formula(d,(960,900),f'‖Av‖² = {np.linalg.norm(A@v)**2:.3f}',42,GREEN)
  else:formula(d,(960,800),'(Av₁)^T (Av₂) = λ₂ v₁^T v₂ = 0',52,TEAL)
  text(d,(960,475),'A →',42,MUTED)
 elif i in [30,31]:
  for cx,title,eq,col in [(380,'원래 행렬 A','λ = 1, 1',BLUE),(960,'새로운 행렬 A^T A','λ ≈ 5.828, 0.172',TEAL),(1540,'특잇값 √λ','σ ≈ 2.414, 0.414',PURPLE)]:
   b.card(d,(cx-255,310,cx+255,690));text(d,(cx,395),title,34,col);formula(d,(cx,555),eq,42,col)
  for cx in [670,1250]:text(d,(cx,500),'→',46,MUTED)
  formula(d,(960,830),'σᵢ(A) = √(λᵢ(A^T A))',76,PURPLE)
 elif i==32:
  for j,label in enumerate(['랭크와 정보 손실','공간의 부피 변화','계산의 안정성']):
   if q>4 and j>0:continue
   cx=380+j*580;b.card(d,(cx-240,320,cx+240,790))
   h=max(2,90*(1-ease(q/4))) if j==0 else 80 if j==1 else 16
   d.ellipse((cx-175,540-h,cx+175,540+h),outline=PURPLE if j!=1 else ORANGE,width=3)
   if j==2:arrow(d,(cx,540),(0,1.3),'#ff6388',100)
   text(d,(cx,720),label,32)
 lines=b.wrap(LINES[i],55)
 for j,line in enumerate(lines):text(d,(960,982+(j-(len(lines)-1)/2)*42),line,30)
 d.rectangle((90,1055,90+1740*t/180,1058),fill=PURPLE)
 return im
if __name__=='__main__':
 (R/'timing.json').write_text(json.dumps(dict(ends=ENDS,narration=LINES),ensure_ascii=False,indent=2),encoding='utf-8')
 for t in [11,22,46,54,64,69,85,105,110,128,139,143,150,162,179.9]:frame(t).resize((960,540)).save(R/f'preview-{t:g}.png')
 with (R/'render.log').open('w') as log:
  proc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',str(R/'visual.mp4')],stdin=subprocess.PIPE,stderr=log)
  for n in range(180*FPS):
   proc.stdin.write(frame(n/FPS).tobytes())
   if n%900==0:print(f'{n/FPS:.0f}/180 sec',flush=True)
  proc.stdin.close()
  if proc.wait():raise RuntimeError('ffmpeg failed')
