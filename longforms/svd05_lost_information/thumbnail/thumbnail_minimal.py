"""Editable SVG + matching antialiased PNG. No generated image assets.

All positions use a 1920x1080 canvas. Unit bases are calculated, not hand drawn.
Run from any directory: python path/to/thumbnail_minimal.py
"""
from pathlib import Path
from html import escape
import json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'exports';OUT.mkdir(exist_ok=True)
HERE=Path(__file__).resolve().parent
W,H,S=1920,1080,3
BG='#0A1725';GRID='#142B3B';WHITE='#E8EDF0';MUTED='#91A3AE'
CYAN='#80BEC5';GOLD='#D0BD85';AXIS='#5C7281'
FONTS={'sans':'C:/Windows/Fonts/malgun.ttf','math':'C:/Windows/Fonts/georgiai.ttf','roman':'C:/Windows/Fonts/georgia.ttf'}
FAMILIES={'sans':'Malgun Gothic','math':'Georgia','roman':'Georgia'}
im=Image.new('RGB',(W*S,H*S),BG);draw=ImageDraw.Draw(im)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
 '<title>신경망의 표현과 정보 복원 — SVD, 선형변환의 기하학</title>',
 '<desc>행렬 A의 구성요소 U, Sigma, V transpose를 수식 순서로 배치한 기하학적 분해. U와 V의 두 벡터는 각각 길이 1이며 서로 직교한다. 화살표 연결은 연산 순서를 나타내지 않는다.</desc>',
 f'<rect width="{W}" height="{H}" fill="{BG}"/>']
bounds=[]
def font(size,kind='sans',scale=1):return ImageFont.truetype(FONTS[kind],round(size*scale))
def width(s,size,kind='sans'):return font(size,kind).getlength(s)
def line(points,color=AXIS,stroke=1.6,dash=None):
 p=[tuple(map(float,q)) for q in points]
 if dash:
  a,b=np.array(p[0]),np.array(p[1]);length=np.linalg.norm(b-a);d=(b-a)/length
  for x in np.arange(0,length,dash[0]+dash[1]):
   q=a+d*x;r=a+d*min(x+dash[0],length);draw.line([tuple(q*S),tuple(r*S)],fill=color,width=max(1,round(stroke*S)))
 else:draw.line([(x*S,y*S) for x,y in p],fill=color,width=max(1,round(stroke*S)),joint='curve')
 pts=' '.join(f'{x:.3f},{y:.3f}' for x,y in p)
 attr=f' stroke-dasharray="{dash[0]} {dash[1]}"' if dash else ''
 svg.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round"{attr}/>')
def polygon(points,color):
 draw.polygon([(x*S,y*S) for x,y in points],fill=color)
 svg.append('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in points)+f'" fill="{color}"/>')
def arrow(a,b,color,stroke=3,head=12):
 a,b=np.array(a,dtype=float),np.array(b,dtype=float);d=(b-a)/np.linalg.norm(b-a);n=np.array([-d[1],d[0]])
 line([a,b-d*head*.7],color,stroke);polygon([b,b-d*head+n*head*.36,b-d*head-n*head*.36],color)
def text(s,x,y,size=32,color=WHITE,kind='sans',align='left'):
 length=width(s,size,kind);xx=x-length/2 if align=='center' else x-length if align=='right' else x
 draw.text((round(xx*S),round(y*S)),s,font=font(size,kind,S),fill=color,anchor='ls',stroke_width=0)
 style='italic' if kind=='math' else 'normal'
 svg.append(f'<text x="{xx:.3f}" y="{y:.3f}" fill="{color}" font-family="{FAMILIES[kind]}" font-size="{size}" font-weight="400" font-style="{style}">{escape(s)}</text>')
 box=font(size,kind).getbbox(s,anchor='ls');bounds.append([s,xx+box[0],y+box[1],xx+box[2],y+box[3]])
 return length
def variable(letter,index,x,y,size=34,color=WHITE,align='left'):
 w=width(letter,size,'math')+width(str(index),size*.58,'roman')
 xx=x-w/2 if align=='center' else x-w if align=='right' else x
 text(letter,xx,y,size,color,'math');text(str(index),xx+width(letter,size,'math'),y+size*.2,size*.58,color,'roman')
 return w
def symbol(letter,x,y,size=67):
 if letter=='Vᵀ':
  vw=width('V',size,'math');tw=width('T',size*.5,'roman');xx=x-(vw+tw)/2
  text('V',xx,y,size,WHITE,'math');text('T',xx+vw,y-size*.49,size*.5,WHITE,'roman')
 else:text(letter,x,y,size,WHITE,'roman' if letter=='Σ' else 'math','center')

# Grid remains well below the contrast of coordinate axes and main text.
for x in range(0,W+1,80):line([(x,0),(x,H)],GRID,.7)
for y in range(0,H+1,80):line([(0,y),(W,y)],GRID,.7)

svg.append('<g id="title">')
text('SVD',88,252,34,CYAN)
text('신경망의 표현과',86,451,66,WHITE)
text('정보 복원',86,565,82,CYAN)
text('선형변환의 기하학',90,660,31,MUTED)
svg.append('</g>')

# Formula is centered over three structures. Superscript T is real positioned text.
svg.append('<g id="decomposition-formula">')
parts=[('A','math'),(' = ','roman'),('U','math'),('Σ','roman'),('V','math')]
fs=90;tw=width('T',44,'roman');fw=sum(width(s,fs,k) for s,k in parts)+tw
xx=1280-fw/2
for s,k in parts:xx+=text(s,xx,262,fs,WHITE,k)
text('T',xx,218,44,WHITE,'roman')
svg.append('</g>')

U_CENTER=np.array([895.,592.]);V_CENTER=np.array([1665.,592.]);LENGTH=127
def basis(deg):
 a=math.radians(deg);return np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
U=basis(30);V=basis(-20)
sigma=np.array([1.6,.8]);BAR_SCALE=90
def screen_vector(v):return np.array([v[0],-v[1]])
def basis_panel(name,o,Q):
 svg.append(f'<g id="{name}-orthonormal-basis">')
 axis=151
 arrow(o+[-axis,0],o+[axis,0],AXIS,1.5,8)
 arrow(o+[0,axis],o+[0,-axis],AXIS,1.5,8)
 for j,col in [(0,CYAN),(1,GOLD)]:
  v=screen_vector(Q[:,j]);tip=o+v*LENGTH
  arrow(o,tip,col,3,13)
  # Label outside each arrowhead, separated from the fixed coordinate axes.
  p=tip+v*22
  variable(name,j+1,p[0],p[1]+9,33,col,'center')
 # Right angle marker spans a precisely orthogonal 18px corner.
 e1,e2=screen_vector(Q[:,0]),screen_vector(Q[:,1]);a=18
 line([o+a*e1,o+a*(e1+e2),o+a*e2],MUTED,1.25)
 svg.append('</g>')

symbol('U',895,411,65);symbol('Σ',1280,411,65);symbol('Vᵀ',1665,411,65)
basis_panel('u',U_CENTER,U);basis_panel('v',V_CENTER,V)

# Diagonal matrix is primary; compact comparison bars are secondary.
svg.append('<g id="singular-values">')
for x,inside in [(1162,1180),(1398,1380)]:line([(inside,486),(x,486),(x,645),(inside,645)],WHITE,2)
variable('σ',1,1220,548,48,WHITE,'center');text('0',1340,548,45,MUTED,'roman','center')
text('0',1220,619,45,MUTED,'roman','center');variable('σ',2,1340,619,48,WHITE,'center')
variable('σ',1,1190,700,24,MUTED,'right');line([(1215,693),(1215+sigma[0]*BAR_SCALE,693)],CYAN,5)
variable('σ',2,1190,733,24,MUTED,'right');line([(1215,726),(1215+sigma[1]*BAR_SCALE,726)],GOLD,5)
svg.append('</g>')

svg.append('<g id="structure-captions">')
for x,s in [(895,'출력 방향'),(1280,'방향별 배율'),(1665,'입력 방향')]:text(s,x,823,31,WHITE,'sans','center')
svg.append('</g></svg>')

# Validate actual Euclidean bases, not merely labels in the illustration.
assert np.allclose(U.T@U,np.eye(2)) and np.allclose(V.T@V,np.eye(2))
assert sigma[0]>=sigma[1]>=0
assert all(0<=a and 0<=b and c<=W and d<=H for _,a,b,c,d in bounds),bounds
assert width('신경망의 표현과',66)<570
svgpath=OUT/'svd_thumbnail_minimal.svg';pngpath=OUT/'svd_thumbnail_minimal.png'
svgpath.write_text('\n'.join(svg),encoding='utf-8')
final=im.resize((W,H),Image.Resampling.LANCZOS);final.save(pngpath,optimize=True)
final.resize((480,270),Image.Resampling.LANCZOS).save(HERE/'preview_480.png')
report={'canvas':[W,H],'source':str(svgpath),'png':str(pngpath),'rendering':'native vector geometry and installed Malgun Gothic/Georgia fonts; 3x supersampling for PNG','U':U.tolist(),'V':V.tolist(),'U_transpose_U':(U.T@U).tolist(),'V_transpose_V':(V.T@V).tolist(),'vector_pixel_lengths':[LENGTH,LENGTH],'singular_values':sigma.tolist(),'ordering':['U: 출력 방향','Σ: 방향별 배율','Vᵀ: 입력 방향'],'no_pipeline_arrows':True,'title_font':'Malgun Gothic Regular','title_font_sizes':[66,82],'formula_font_size':90,'text_bounds':bounds}
(HERE/'geometry_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(pngpath,final.size,pngpath.stat().st_size);print(svgpath)
