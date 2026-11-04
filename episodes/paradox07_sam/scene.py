"""SAM: a temporary ascent probe and an update that starts at original theta."""
import json
import sys
from pathlib import Path
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True
ROOT=Path(__file__).resolve().parent
ORANGE='#FFAA66'
H=np.array([[1.5,.25],[.25,.6]])
THETA=np.array([.25,.35]);RHO=.65;ETA=.38;VALLEY_RHO=.35

def loss(v):return float(.12+.5*np.asarray(v)@H@np.asarray(v))
def grad(v):return H@np.asarray(v)
EPS=RHO*grad(THETA)/np.linalg.norm(grad(THETA))
ADV=THETA+EPS
NEW=THETA-ETA*grad(ADV)
SGD_NEW=THETA-.8*grad(THETA)

def exact_probe():
    angles=np.linspace(0,2*np.pi,4097)
    candidates=THETA+RHO*np.column_stack([np.cos(angles),np.sin(angles)])
    return max(candidates,key=loss)

def sharp(u):return .08+3.8*u*u
def wide(u):return .26+.45*u*u

def t(s,y=0,x=0,size=28,color=INK,width=7.7):
    obj=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.2)
    if obj.width>width:obj.scale_to_fit_width(width)
    return obj.move_to([x,y,0])

def box(s,x=0,y=0,w=7.2,h=1,color=WEIGHT):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,color=color,stroke_width=1.5,fill_color=BG,fill_opacity=1).move_to([x,y,0]),t(s,y,x,size=27,color=color,width=w-.3))

def valleys(neighbors=True):
    g=VGroup()
    for x,fn,color in [(-1.95,sharp,PRUNE),(1.95,wide,GOOD)]:
        title='좁고 깊은 골짜기' if x<0 else '넓고 완만한 골짜기'
        ax=Axes(x_range=[-.7,.7,.35],y_range=[0,1.1,.25],x_length=3.2,y_length=3.4,tips=False,axis_config={'color':MUTED,'stroke_width':1.3}).move_to([x,1.25,0])
        plot=ax.plot(fn,x_range=[-.5,.5,.005] if x<0 else [-.7,.7,.005],color=color,stroke_width=3)
        g.add(ax,plot,t(title,3.75,x,size=23,color=color,width=3.65),Dot(ax.c2p(0,fn(0)),color=WEIGHT,radius=.09),t(f'현재 L = {fn(0):.2f}',-2.1,x,size=26,color=WEIGHT,width=3.65))
        if neighbors:
            for u in [-VALLEY_RHO,VALLEY_RHO]:
                g.add(DashedLine(ax.c2p(u,0),ax.c2p(u,fn(u)),color=ORANGE,stroke_width=1.4),Dot(ax.c2p(u,fn(u)),color=ORANGE,radius=.065))
            g.add(Line(ax.c2p(-VALLEY_RHO,-.07),ax.c2p(VALLEY_RHO,-.07),color=ACCENT,stroke_width=3),t('동일 반경 ρ',-1.25,x,size=23,color=ACCENT,width=3.6),t(f'주변 최대 {fn(VALLEY_RHO):.3f}',-3.15,x,size=25,color=ORANGE if x<0 else GOOD,width=3.65))
    g.add(t('양쪽의 좌표 눈금·반경 동일 · 설명용 손실 모형',-4.45,size=20,color=MUTED))
    return g

def plane():
    ax=Axes(x_range=[-1.8,1.8,.6],y_range=[-1.8,1.8,.6],x_length=5.6,y_length=5.6,tips=False,axis_config={'color':MUTED,'stroke_width':1.2,'stroke_opacity':.5}).move_to([0,.65,0])
    contours=VGroup()
    vals,vecs=np.linalg.eigh(H)
    for level in [.2,.38,.65,1.0]:
        transform=vecs@np.diag(np.sqrt(2*(level-.12)/vals))
        contour=ParametricFunction(lambda a:ax.c2p(*(transform@np.array([np.cos(a),np.sin(a)]))),t_range=[0,2*np.pi],color=WEIGHT,stroke_width=1,stroke_opacity=.32,fill_opacity=0)
        contours.add(contour)
    return ax,contours

def neighborhood(mode='probe'):
    ax,contours=plane();center=ax.c2p(*THETA)
    estimated=mode!='exact'
    adv=ADV if estimated else exact_probe()
    ap=ax.c2p(*adv)
    radius=np.linalg.norm(ax.c2p(RHO,0)-ax.c2p(0,0))
    circle=Circle(radius=radius,color=ORANGE,stroke_width=2,fill_color=ORANGE,fill_opacity=.025).move_to(center)
    ghost=Dot(center,color=WEIGHT,radius=.085)
    temp=Dot(center if mode=='probe' else ap,color=ORANGE,radius=.09)
    arrow=Arrow(center,ap,buff=.03,color=ORANGE,stroke_width=3)
    g=VGroup(ax,contours,circle,ghost,temp,t('θ',.8,-.15,size=28,color=WEIGHT),t('θ₂',3.7,-2.95,size=23,color=MUTED),t('θ₁',-2.55,2.95,size=23,color=MUTED),
             t('ρ',2.15,-.65,size=27,color=ORANGE),t('같은 학습 데이터 · 파라미터만 교란',4.15,size=23,color=MUTED))
    if mode=='exact':
        g.add(arrow,t('개념적 최대점',2.7,2.1,size=24,color=ORANGE,width=3),t('정의: ‖ε‖₂ ≤ ρ 안에서 가장 큰 손실',-3.5,size=29,color=ACCENT),t('목표의 개념도 · 실제 SAM은 전방향을 탐색하지 않음',-4.5,size=20,color=MUTED))
    elif mode=='update':
        g.add(arrow,t('임시 θ + ε̂',2.65,2.1,size=23,color=ORANGE,width=3))
        step=Arrow(center,ax.c2p(*NEW),buff=.02,color=GOOD,stroke_width=4)
        g2=grad(ADV)/np.linalg.norm(grad(ADV))*.45
        g.add(Arrow(ap,ax.c2p(*(ADV+g2)),buff=.02,color=PRUNE,stroke_width=3),t('두 번째 기울기',3.4,1.8,size=22,color=PRUNE,width=3.2),
              t('θnew = θ − η ∇L(θ + ε̂)',-3.45,size=33,color=GOOD),t('기울기 평가: 임시 점 / 갱신 출발: 원래 θ',-4.5,size=21,color=MUTED))
        g.update_arrow=step
        g.current_dot=Dot(center,color=WEIGHT,radius=.09);g.add(g.current_dot)
        g.updated_location=ax.c2p(*NEW)
    else:
        g.add(t('ε̂ = ρ ∇L(θ) / ‖∇L(θ)‖₂',-3.45,size=31,color=ORANGE),t('정확한 최악점이 아닌 1차 근사 · ∇L(θ) ≠ 0',-4.5,size=21,color=MUTED))
    g.probe_dot=temp;g.probe_arrow=arrow;g.probe_location=ap
    return g

def intro(sgd=False):
    ax,contours=plane();c=ax.c2p(*THETA)
    down=ax.c2p(*SGD_NEW);up=ax.c2p(*ADV)
    current=Dot(c,color=WEIGHT,radius=.1)
    p=VGroup(ax,contours,current,Arrow(c,down,buff=.02,color=WEIGHT,stroke_width=4),t('Minimize Loss',-.55,-1.4,size=25,color=WEIGHT,width=3.8),
             t('θ',.9,.75,size=26,color=WEIGHT),t('입력은 고정 · 움직이는 것은 파라미터',-4.45,size=22,color=MUTED))
    if not sgd:p.add(Arrow(c,up,buff=.02,color=ORANGE,stroke_width=4),t('Find Higher Loss',2.8,1.4,size=25,color=ORANGE,width=4.4),t('임시 탐색',3.6,size=26,color=ORANGE))
    else:p.add(t('현재 기울기의 반대 방향으로',3.8,size=27,color=WEIGHT),t('θnew = θ − η ∇L(θ)',-3.3,size=34,color=WEIGHT))
    p.current_dot=current;p.down_location=down
    return p

def minmax():
    return VGroup(t('minθ',3,-2.7,size=39,color=GOOD,width=2),t('maxε',3,-.95,size=39,color=ORANGE,width=2),t('L(θ + ε)',3,1.65,size=39,color=INK,width=4),
                  t('조건: ‖ε‖₂ ≤ ρ',1.85,size=29,color=ORANGE),box('max · 주변에서 가장 큰 손실을 평가',0,.2,7.4,1.1,ORANGE),
                  box('min · 그 최대 손실을 낮추는 θ로 갱신',0,-1.55,7.4,1.1,GOOD),t('고정된 학습 데이터에 대한 파라미터 교란',-3.35,size=24,color=MUTED),t('별도 정규화 항을 생략한 핵심 목적',-4.5,size=20,color=MUTED))

def contrast():
    return VGroup(t('일반적인 경사하강법',3.5,size=29,color=WEIGHT),box('현재 위치의 L(θ)를 낮춘다',0,2.1,7.4,1.15,WEIGHT),
                  t('Sharpness-Aware Minimization',.45,size=28,color=ORANGE),box('주변 최대 손실까지 고려해 낮춘다',0,-1.1,7.4,1.3,GOOD),t('먼저 나쁜 방향을 살펴보고',-2.8,size=28,color=ORANGE),t('원래 파라미터의 업데이트를 계산한다',-4,size=28,color=GOOD))

class SharpnessAwareMinimization(Scene):
    def chrome(self,i):
        titles=['먼저 손실이 높아지는 방향으로?','Sharpness-Aware Minimization','현재 위치에서 손실을 낮춘다','서로 다른 두 골짜기','낮고 좁은 바닥 · 높고 넓은 바닥','현재 손실만 보면 좁은 쪽이 유리','같은 크기로 파라미터를 교란한다','주변 최대 손실은 순위가 달라진다','SAM이 보는 것은 주변의 손실',
                '반경 ρ 안에서 가장 불리한 지점','주변 최대 손실을 줄이는 갱신','반대되는 두 최적화','내부 max · 외부 min','Min-Max 최적화','실제 계산 · 기울기로 근사한다','두 번째 기울기로 원래 θ를 갱신','왜 두 번 살펴볼까?','한 점의 낮은 손실을 넘어서','주변까지 낮은 손실을 유지하도록','일반화 개선이 보고된 학습 방식','주변 안정성은 정확도 보장이 아니다','어떤 손실을 낮출 것인가?','현재 손실과 주변 최대 손실','나빠지는 방향을 먼저 살펴본다','최악의 상황을 먼저 학습하는 역설']
        return VGroup(t('신경망의 역설  /  07',7.35,size=20,color=MUTED),t('최악의 상황을 먼저\n학습하는 신경망',6.45,size=33),Line([-3.85,5.65,0],[3.85,5.65,0],color=MUTED,stroke_opacity=.3),t(titles[i],5.05,size=25,color=ACCENT),t('SAM · 파라미터 주변의 Min-Max 최적화',-7.45,size=18,color=MUTED))

    def construct(self):
        data=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
        caps=['더 잘 학습하기 위해 일부러\n손실이 커지는 방향을 먼저 찾습니다.','이것이 Sharpness-Aware Minimization,\nSAM입니다.','일반 경사하강법은 현재 위치에서\n손실이 줄어드는 방향으로 이동합니다.','두 개의 골짜기를\n생각해 보겠습니다.','하나는 낮지만 좁고 가파르고,\n다른 하나는 조금 높지만 넓고 완만합니다.','현재 손실만 비교하면\n첫 번째 골짜기가 더 좋아 보입니다.','파라미터를\n조금만 움직여 보면 어떨까요?','좁은 쪽은 손실이 급격히 증가하고,\n넓은 쪽은 비교적 낮게 유지됩니다.','SAM은 이 차이에 주목합니다.',
              '작은 파라미터 영역 안에서\n손실이 가장 커지는 지점을 찾는 목적입니다.','그 가장 불리한 지점에서도 손실이 작도록\n원래 파라미터를 업데이트합니다.','여기에는 반대되는\n두 가지 최적화가 있습니다.','주변의 손실을 최대화하고,\n그 최대 손실을 다시 최소화합니다.','수학적으로는\nMin-Max 최적화입니다.','실제로는 전방향 탐색 대신 기울기로\n손실이 커지는 방향을 근사합니다.','임시 점에서 다시 기울기를 계산하고\n그 값으로 원래 파라미터를 갱신합니다.','왜 이런 과정을 거칠까요?','현재 위치에서만\n손실이 낮은 해를 찾는 것이 아닙니다.','파라미터가 조금 바뀌어도\n주변 손실이 크게 증가하지 않도록 합니다.','일부 환경에서는 일반화 성능 개선이\n보고되었습니다.','주변 안정성이 새 데이터의 정확도를\n항상 보장하는 것은 아닙니다.','여기에는 중요한\n관점의 변화가 있습니다.','현재 위치의 손실을 넘어\n주변의 가장 불리한 상황까지 고려합니다.','더 좋은 해를 위해\n먼저 나빠지는 방향을 살펴봅니다.','최악의 상황을 먼저 학습하는\n신경망의 역설입니다.']
        for i,s in enumerate(data['segments']):
            self.clear();self.add(self.chrome(i),t(caps[i],-6.15,size=24))
            p=self.panel(i);self.play(FadeIn(p),run_time=.3)
            if i==2:self.play(p.current_dot.animate.move_to(p.down_location),run_time=1)
            if i==9:
                ax=p[0]
                for angle in [0,np.pi/2,np.pi,3*np.pi/2]:
                    v=THETA+RHO*np.array([np.cos(angle),np.sin(angle)])
                    self.play(FadeIn(Dot(ax.c2p(*v),color=MUTED,radius=.055)),run_time=.15)
                self.play(Flash(p.probe_dot,color=ORANGE,flash_radius=.3),run_time=.6)
            if i in [11,12,13]:
                self.play(Circumscribe(p[1],color=ORANGE),run_time=.65)
                if i in [12,13]:self.play(Circumscribe(p[0],color=GOOD),run_time=.65)
            if i in [14,23]:
                self.play(Create(p.probe_arrow),p.probe_dot.animate.move_to(p.probe_location),run_time=1.2)
                self.add(t('임시 θ + ε̂',2.65,2.1,size=23,color=ORANGE,width=3))
            if i==15:
                self.play(Create(p.update_arrow),p.current_dot.animate.move_to(p.updated_location).set_color(GOOD),run_time=1.1)
                self.add(t('θnew',.15,-1.1,size=27,color=GOOD,width=2))
            remaining=s['end']-self.time
            if remaining<-.04:raise RuntimeError(f'Timing overrun {i}: {self.time}')
            if remaining>0:self.wait(remaining)
        assert abs(self.time-108)<1/30+.001

    def panel(self,i):
        if i in [0,1,2]:return intro(i==2)
        if i in [3,4,5,6,7,8,16,17,18]:return valleys(i not in [3,4,5])
        if i==9:return neighborhood('exact')
        if i in [10,11,12,13]:return minmax()
        if i in [14,23]:return neighborhood('probe')
        if i==15:return neighborhood('update')
        if i==19:return VGroup(box('이미지 분류',0,3,7.3,1.1,WEIGHT),box('파인튜닝',0,1.1,7.3,1.1,SPARSE),t('일부 환경에서 일반화 성능 개선 보고',-1,size=30,color=GOOD),t('Foret et al. · SAM · ICLR 2021',-2.6,size=25,color=MUTED),t('이 영상의 지형과 수치는 설명용 · 재현 실험이 아님',-4.2,size=20,color=MUTED))
        if i==20:return VGroup(box('파라미터 주변의 안정성',0,3,7.3,1.1,WEIGHT),t('≠',1.45,size=43,color=ACCENT),box('새 데이터 정확도의 보장',0,0,7.3,1.1,PRUNE),t('좌표계 · 노름 · 반경 · 측정 방식에 의존',-2.1,size=28,color=MUTED),t('넓은 골짜기가 항상 더 좋은 일반화를 뜻하지 않음',-4,size=23,color=MUTED))
        return contrast()
