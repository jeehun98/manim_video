"""Directional Jacobian action: geometric illustrations, not a PDE simulation."""
from pathlib import Path
import json
from manim import *

ROOT=Path(__file__).resolve().parent
config.background_color='#081622'
config.frame_width=14.222222222
config.frame_height=8
INK,MUTED,CYAN,GREEN,GOLD,PINK='#EAF5FB','#8FAABD','#51D8EE','#8BE0B1','#F4C978','#F28A9F'
FONT='Malgun Gothic'

def txt(s,size=27,color=INK,width=12):
    t=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.15)
    if t.width>width:t.scale_to_fit_width(width)
    return t

def label(s,x,y,color=INK,size=27):return txt(s,size,color).move_to([x,y,0])

def project(p):
    x,y,z=p
    return np.array([x+.38*y,.25*y+.9*z,0.])

def cube(edge=2,center=(-2,0,0),color=CYAN):
    c=np.array(center);v=[c+project(np.array([x,y,z])*edge/2) for x in [-1,1] for y in [-1,1] for z in [-1,1]]
    g=VGroup()
    for i in range(8):
        for bit in [1,2,4]:
            j=i^bit
            if i<j:g.add(Line(v[i],v[j],color=color,stroke_width=2))
    return g

def core(r=1,h=2.7,phase=0,center=(-2,0,0)):
    c=np.array(center);g=VGroup()
    for z in np.linspace(-h/2,h/2,7):
        ring=VMobject(stroke_color=CYAN,stroke_width=1.7,fill_opacity=0)
        ring.set_points_as_corners([c+project([r*np.cos(t),r*np.sin(t),z]) for t in np.linspace(0,TAU,40)])
        g.add(ring)
    for t in np.arange(6)*TAU/6:
        g.add(Line(c+project([r*np.cos(t),r*np.sin(t),-h/2]),c+project([r*np.cos(t),r*np.sin(t),h/2]),color=CYAN,stroke_opacity=.4))
    for sign in [-1,1]:
        g.add(Arrow(c+project([0,0,sign*h/2]),c+project([0,0,sign*(h/2+.55)]),buff=0,color=PINK,stroke_width=3))
    for t in np.arange(5)*TAU/5+phase:
        p=c+project([1.5*r*np.cos(t),1.5*r*np.sin(t),0])
        q=c+project([r*np.cos(t+.4),r*np.sin(t+.4),0])
        g.add(Arrow(p,q,buff=0,color=GOLD,stroke_width=2,max_tip_length_to_length_ratio=.25))
    return g

def field(center=(-2,0,0),peak=False):
    c=np.array(center);g=VGroup()
    for x in np.linspace(-2,2,11):
        for y in np.linspace(-1.5,1.5,9):
            a=np.array([-.13*y,.13*x,0]);a+=np.array([.11,0,0])
            if peak:a*=1+2*np.exp(-4*(x*x+y*y))
            g.add(Arrow(c+[x,y,0],c+[x,y,0]+a,buff=0,color=GOLD if peak and x*x+y*y<.5 else CYAN,stroke_width=2,max_tip_length_to_length_ratio=.3))
    return g

class EnergyScene(Scene):
    index=1
    def construct(self):
        records=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
        record=records[self.index-1];self.chapter=6
        self.timing=json.loads((ROOT/record['directory']/'timing.json').read_text(encoding='utf-8'))
        spec=(ROOT/record['directory']/'spec.md').read_text(encoding='utf-8').splitlines()[0]
        title=spec.split(' — ',1)[1]
        self.add(label('NAVIER–STOKES × NEURAL NETWORKS',-3.7,3.65,MUTED,15),label(f'{self.chapter:02}막  /  {self.index:02} — '+title,0,3.15,INK,29))
        self.add(Line([-6.2,-2.85,0],[6.2,-2.85,0],color='#294958'))
        self.caption=VGroup();self.progress=Line([-6.2,-3.8,0],[-6.19,-3.8,0],color=CYAN,stroke_width=3);self.add(self.progress)
        getattr(self,f'scene{self.index}')()
        frames=round(self.timing['duration']*config.frame_rate)-round(self.time*config.frame_rate)
        if frames<0:raise ValueError('Scene overrun')
        if frames:self.wait(frames/config.frame_rate)

    def cue(self,n,*animations,seconds=3):
        self.remove(self.caption);s=self.timing['lines'][n-1]
        for a,b in [('이천이십육 년 구월 팔일','2026년 9월 8일'),('오픈에이아이','OpenAI'),('구월 십일','9월 11일'),('나비에 스토크스','Navier–Stokes'),('엘투 노름','L₂ 노름'),('엘엘엠 인트 에이트','LLM.int8()'),('스무스 퀀트','SmoothQuant'),('팔 비트','8비트'),('십육 비트','16비트')]:s=s.replace(a,b)
        for a,b in [('엘엘엠 인트 에이트', 'LLM.int8()'), ('스무스 퀀트', 'SmoothQuant'), ('십육 비트', '16비트'), ('팔 비트', '8비트'), ('예순네 개', '64개'), ('예순세 개', '63개'), ('영 점 이오', '0.25'), ('영 점 오', '0.5'), ('영 점 육', '0.6'), ('영 점 이는', '0.2는'), ('영 점 일', '0.1'), ('영 점 사', '0.4'), ('영 점 팔', '0.8'), ('하나만 팔', '하나만 8'), ('최대값은 팔', '최대값은 8'), ('최대 절댓값이 일일 때', '최대 절댓값이 1일 때'), ('백일 때', '100일 때'), ('백까지', '100까지'), ('백 배', '100배'), ('활성값이 팔', '활성값이 8'), ('곱은 이', '곱은 2'), ('활성값을 팔로', '활성값을 8로'), ('가중치를 팔 배', '가중치를 8배'), ('일과 이를', '1과 2를')]:s=s.replace(a,b)
        if len(s)>46:
            spaces=[i for i,c in enumerate(s) if c==' ']
            if spaces:
                k=min(spaces,key=lambda i:abs(i-len(s)/2));s=s[:k]+'\n'+s[k+1:]
        self.caption=txt(s,23,width=12.1).move_to([0,-3.32,0]);self.add(self.caption)
        end=round(self.timing['ends'][n-1]*config.frame_rate)/config.frame_rate
        available=end-self.time
        if available<-.01:raise ValueError(f'Cue overrun {n}')
        if animations:self.play(*animations,run_time=round(min(seconds,available)*config.frame_rate)/config.frame_rate)
        frames=round(end*config.frame_rate)-round(self.time*config.frame_rate)
        if frames:self.wait(frames/config.frame_rate)
        self.progress.put_start_and_end_on([-6.2,-3.8,0],[-6.2+12.4*end/self.timing['duration'],-3.8,0])

    def note(self,s):return label(s,0,-2.45,MUTED,19)

    def vortex(self,stretch=1,shear=0,center=(-2.7,0,0),scale=1):
        c=np.array(center);F=np.diag([1/np.sqrt(stretch),1/np.sqrt(stretch),stretch]);F[0,2]=shear*stretch
        g=VGroup()
        def pos(p):return c+scale*project(F@np.array(p))
        for z in np.linspace(-.85,.85,7):
            ring=VMobject(stroke_color=CYAN,stroke_width=1.6,fill_opacity=0)
            ring.set_points_as_corners([pos([.65*np.cos(t),.65*np.sin(t),z]) for t in np.linspace(0,TAU,40)])
            g.add(ring)
        for t in np.arange(6)*TAU/6:
            g.add(Line(pos([.65*np.cos(t),.65*np.sin(t),-.85]),pos([.65*np.cos(t),.65*np.sin(t),.85]),color=CYAN,stroke_opacity=.35))
        g.add(Arrow(c,pos([0,0,1]),buff=0,color=GOLD,stroke_width=5,max_tip_length_to_length_ratio=.2))
        return g

    def pair(self,angle=0,left=(-3,0,0),right=(3,0,0),radius=1.1):
        v=np.array([np.cos(angle),np.sin(angle),0]);out=np.array([1.8*v[0],.5*v[1],0])
        return VGroup(Arrow(left,np.array(left)+radius*v,buff=0,color=GOLD,stroke_width=4),Arrow(right,np.array(right)+radius*out,buff=0,color=GOLD,stroke_width=4))

    def scene1(self):
        stretch=ValueTracker(1);shear=ValueTracker(0)
        shape=always_redraw(lambda:self.vortex(stretch.get_value(),shear.get_value()))
        self.add(shape,label('회전축을 따라',3,1.3,GOLD,30))
        self.cue(1)
        self.cue(2,FadeIn(label('그 방향의 속도 차이가 중요하다',3,.45,INK,25)))
        self.cue(3,FadeIn(label('방향：회전축   /   길이：회전 강도',0,2.35,GOLD,25)))
        self.cue(4,stretch.animate.set_value(1.8),FadeIn(label('늘어남 → 회전 강화',3,-.5,GREEN,27)),seconds=4)
        comparison=Succession(stretch.animate.set_value(.65),AnimationGroup(stretch.animate.set_value(1),shear.animate.set_value(.6)))
        self.cue(5,comparison,FadeIn(label('압축 · 기울어짐도 가능',3,-1.35,PINK,26)),FadeIn(self.note('부피 보존 변형 예시 · 점성 및 외력에 의한 생성은 제외')),seconds=5)
        shape.clear_updaters()

    def scene2(self):
        c=np.array([-2.8,.1,0]);grid=cube(2.1,center=c);self.add(grid)
        J=np.array([[-.5,-.5,0],[.5,-.5,0],[0,0,1.]])
        self.cue(1)
        probes=VGroup();names=VGroup()
        for j,(axis,color) in enumerate(zip(['x','y','z'],[CYAN,PINK,GOLD])):
            delta=np.eye(3)[j]*.7;p=c+project(delta)
            probes.add(Dot(p,color=color,radius=.045),Arrow(c,p,buff=0,color=color,stroke_width=2),Arrow(p,p+project(J@delta),buff=0,color=GREEN,stroke_width=3))
            names.add(label(axis,p[0]+.16,p[1]+.2,color,22))
        self.cue(2,FadeIn(probes),FadeIn(names),FadeIn(label('세 방향의 작은 이동과 속도 차이',3,1.8,INK,24)))
        card=VGroup(RoundedRectangle(width=2.5,height=1.25,corner_radius=.12,stroke_color=CYAN),txt('Jacobian  Jᵤ',27,CYAN,width=2.3)).move_to([2.1,.2,0])
        self.cue(3,FadeIn(card))
        omega=Arrow(c,c+project([0,0,1.2]),buff=0,color=GOLD,stroke_width=5)
        result=Arrow([5,-.45,0],[5,.65,0],buff=0,color=GREEN,stroke_width=5)
        self.cue(4,FadeIn(omega),FadeIn(result),FadeIn(label('Jᵤω = (ω·∇)u',0,2.35,INK,30)),FadeIn(label('변화율의 한 항',5,-1.2,GREEN,23)))
        self.cue(5,FadeIn(self.note('Jᵤω는 다음 보티시티 자체가 아니다 · 점성 확산 등은 별도')))

    def scene3(self):
        theta=ValueTracker(0);c=np.array([-2.7,0,0])
        circle=Circle(radius=1.2,color=MUTED,stroke_opacity=.4).move_to(c)
        current=always_redraw(lambda:Arrow(c,c+1.2*np.array([np.sin(theta.get_value()),np.cos(theta.get_value()),0]),buff=0,color=GOLD,stroke_width=5))
        future=always_redraw(lambda:Arrow(c,c+1.2*np.array([np.exp(-.15)*np.sin(theta.get_value()),np.exp(.3)*np.cos(theta.get_value()),0]),buff=0,color=GREEN,stroke_width=3))
        rate=DecimalNumber(1,num_decimal_places=2,include_sign=True,mob_class=Text,font_size=35,color=GREEN).move_to([3,.2,0])
        rate.add_updater(lambda m:m.set_value(np.cos(theta.get_value())**2-.5*np.sin(theta.get_value())**2))
        self.add(circle,current,future,rate,label('고정：늘어남과 압축 효과 S',0,2.35,MUTED,24),label('순간 크기 증감의 지표',3,1.1,INK,26),label('현재 ω',-4.6,-1.85,GOLD,22),label('짧은 시간 뒤',-1.1,-1.85,GREEN,22))
        self.cue(1)
        self.cue(2,theta.animate.set_value(PI/2),seconds=4)
        self.cue(3,theta.animate.set_value(0),FadeIn(label('축 정렬 → 강화 / 압축 정렬 → 약화',3,-.8,INK,22)),seconds=4)
        self.cue(4,theta.animate.set_value(PI/4),seconds=4)
        self.cue(5,FadeIn(self.note('비점성 · 외력의 컬=0인 변형 효과 · 크기 증감은 ωᵀSω로 결정')))
        current.clear_updaters();future.clear_updaters();rate.clear_updaters()

    def scene4(self):
        tube=self.vortex(center=(-3,0,0),scale=.8)
        circle=Circle(radius=.6,color=CYAN).move_to([1.6,0,0]);ellipse=Ellipse(width=2.16,height=.6,color=GREEN).move_to([4.6,0,0])
        self.add(tube,circle,label('유체',-3,1.8,CYAN,29),label('신경망',3.1,1.8,CYAN,29))
        self.cue(1)
        vectors=self.pair(PI/4,(1.6,0,0),(4.6,0,0),.6)
        self.cue(2,Create(ellipse),FadeIn(vectors))
        arrow=Arrow([2.35,0,0],[3.3,0,0],buff=0,color=MUTED)
        self.cue(3,FadeIn(arrow),FadeIn(label('J_f',2.8,.65,CYAN,28)))
        self.cue(4,FadeIn(label('δy ≈ J_f(x) δx',3.1,-1.6,GREEN,27)))
        self.cue(5,FadeIn(label('Jᵤω',-3,-1.6,GREEN,30)),FadeIn(label('Jacobian × Vector',0,2.35,INK,30)))
        self.cue(6,FadeIn(self.note('유체：시간 변화율의 한 항   /   신경망：작은 입력 변화의 출력 반응')))

    def scene5(self):
        theta=ValueTracker(PI/6)
        circle=Circle(radius=1.1,color=CYAN).move_to([-3,0,0]);ellipse=Ellipse(width=3.96,height=1.1,color=GREEN).move_to([3,0,0])
        arrows=always_redraw(lambda:self.pair(theta.get_value()))
        self.add(circle,label('같은 입력 변화의 크기',-3,1.85,CYAN,25))
        self.cue(1)
        self.cue(2,Indicate(circle,color=GOLD))
        self.add(arrows)
        self.cue(3,Create(ellipse),FadeIn(label('J = diag(1.8, 0.5)',0,2.35,MUTED,24)))
        ratio=DecimalNumber(1.578765,num_decimal_places=2,mob_class=Text,font_size=32,color=GREEN).move_to([3,-1.6,0])
        ratio.add_updater(lambda m:m.set_value(np.hypot(1.8*np.cos(theta.get_value()),.5*np.sin(theta.get_value()))))
        self.add(ratio,label('출력 확대 비율',3,1.85,GREEN,25))
        self.cue(4,theta.animate.set_value(PI/2),seconds=4)
        self.cue(5,theta.animate.set_value(0),FadeIn(label('가장 큰 특잇값 = 최대 확대 비율 = 1.8',0,-2.2,INK,26)),seconds=5)
        arrows.clear_updaters();ratio.clear_updaters()

    def scene6(self):
        xs=[-5,-1.7,1.7,5]
        self.add(label('층별 국소 선형 모형 · 각 층의 최대 확대 비율은 1.8',0,2.35,MUTED,23))
        stages=VGroup(*[label(name,x,1.55,INK,27) for name,x in zip(['입력','층 1','층 2','층 3'],xs)])
        self.add(stages)
        def vec(x,length):return Arrow([x,-.1,0],[x+.3*length,-.1,0],buff=0,color=GOLD,stroke_width=5,max_tip_length_to_length_ratio=.3)
        arrows=[vec(x,n) for x,n in zip(xs,[1,1.8,3.24,5.832])]
        labels=[label(f'{n:.2f}',x,-1,GREEN,27) for x,n in zip(xs,[1,1.8,3.24,5.832])]
        self.add(arrows[0],labels[0]);self.cue(1)
        self.cue(2,FadeIn(arrows[1]),FadeIn(labels[1]))
        aligned=label('늘어나는 방향이 이어지는 경우',0,.8,GREEN,26)
        self.cue(3,FadeIn(arrows[2]),FadeIn(arrows[3]),FadeIn(labels[2]),FadeIn(labels[3]),FadeIn(aligned))
        changed=[label('0.90',xs[2],-1,PINK,27),label('1.62',xs[3],-1,PINK,27)]
        self.cue(4,Transform(arrows[2],vec(xs[2],.9)),Transform(arrows[3],vec(xs[3],1.62)),FadeTransform(labels[2],changed[0]),FadeTransform(labels[3],changed[1]),FadeOut(aligned),FadeIn(label('층 2가 이 방향을 압축하면',0,-1.75,PINK,27)),seconds=4)
        self.cue(5,FadeIn(self.note('각 층의 최대값 곱은 상한 · 실제 증폭은 방향 연결에 좌우 · 유체 시간 발전과 구별')))

    def scene7(self):
        tube=self.vortex(center=(-3,0,0),scale=.85)
        circle=Circle(radius=.65,color=CYAN).move_to([1.4,0,0]);ellipse=Ellipse(width=2.34,height=.65,color=GREEN).move_to([4.4,0,0])
        pair=self.pair(PI/6,(1.4,0,0),(4.4,0,0),.65)
        self.add(tube,circle,ellipse,pair,label('유체',-3,1.8,CYAN,27),label('신경망',3.1,1.8,CYAN,27))
        self.cue(1)
        fluid=label('보티시티의 시간 변화',-3,-1.4,GREEN,24);network=label('작은 입력 변화 → 출력 반응',3.1,-1.4,GREEN,23)
        self.cue(2,FadeIn(fluid),FadeIn(network))
        metrics=VGroup(label('변형률 S와 정렬',-3,-2.1,MUTED,23),label('J_f의 특잇값',3.1,-2.1,MUTED,23))
        self.cue(3,FadeIn(metrics))
        common=label('Local Derivative × Direction',0,2.35,INK,30)
        self.cue(4,FadeIn(common))
        contours=VGroup(*[Ellipse(width=.4*k,height=1.6*k,color=GREEN,stroke_opacity=.7,fill_opacity=0).move_to([3.1,0,0]) for k in [.6,1,1.4,1.8]])
        self.cue(5,FadeOut(circle),FadeOut(ellipse),FadeOut(pair),FadeOut(network),FadeOut(metrics),FadeIn(contours),FadeIn(label('파라미터 공간의 손실 지형',3.1,-2.1,GREEN,23)))
        self.cue(6,Succession(FadeOut(common),FadeIn(label('다음 막：가파른 방향과 Hessian',0,2.35,INK,28))),FadeIn(self.note('입력의 Jacobian과 파라미터 손실의 Hessian은 다른 미분 대상')))

