"""Representability, training trajectories, and implicit selection."""
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
        record=records[self.index-1];self.chapter=9
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
        s=s.replace('암묵적 편향, 임플리시트 바이어스','암묵적 편향, Implicit Bias')
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

    def mesh(self,spacing=.7,center=(0,0,0),width=7,height=3,color=CYAN):
        c=np.array(center);g=VGroup()
        for x in np.arange(-width/2,width/2+.001,spacing):g.add(Line(c+[x,-height/2,0],c+[x,height/2,0],color=color,stroke_width=1,stroke_opacity=.55))
        for y in np.arange(-height/2,height/2+.001,spacing):g.add(Line(c+[-width/2,y,0],c+[width/2,y,0],color=color,stroke_width=1,stroke_opacity=.55))
        return g

    def ticks(self,n,center=(0,-1.8,0),width=7,color=GOLD):
        c=np.array(center);g=VGroup(Line(c+[-width/2,0,0],c+[width/2,0,0],color=MUTED))
        for x in np.linspace(-width/2,width/2,n+1):g.add(Line(c+[x,-.12,0],c+[x,.12,0],color=color))
        return g

    def contours(self,center=(0,0,0),ratio=3.464):
        return VGroup(*[Ellipse(width=4*k/ratio,height=4*k,color=GREEN,fill_opacity=0,stroke_opacity=.6).move_to(center) for k in [.25,.45,.65,.85]])

    def gaussian(self,sigma,center=(3,-.7,0),conserve=True):
        c=np.array(center);height=(.55/sigma)**2 if conserve else 1
        pts=[c+[x,1.7*height*np.exp(-x*x/(2*sigma*sigma)),0] for x in np.linspace(-2,2,90)]
        return VMobject(stroke_color=GREEN,stroke_width=3,fill_opacity=0).set_points_as_corners(pts)

    def stage_arrows(self,values,y=0,color=GOLD,scale=.18):
        xs=np.linspace(-5,5,len(values));arrows=VGroup();numbers=VGroup()
        for x,n in zip(xs,values):
            arrows.add(Arrow([x,y,0],[x+scale*n,y,0],buff=0,color=color,stroke_width=4,max_tip_length_to_length_ratio=.25))
            numbers.add(label(f'{n:g}',x,y-.65,color,26))
        return arrows,numbers

    def scene1(self):
        stretch=ValueTracker(1);sigma=ValueTracker(.55)
        tube=always_redraw(lambda:self.vortex(stretch.get_value(),center=(-3,0,0),scale=.8))
        profile=always_redraw(lambda:self.gaussian(sigma.get_value()))
        self.add(tube,profile,label('Vortex Stretching',-3,1.8,CYAN,26),label('Viscous Diffusion',3,1.8,GREEN,26))
        self.cue(1)
        self.cue(2,stretch.animate.set_value(1.8),seconds=4)
        self.cue(3,sigma.animate.set_value(.95),seconds=4)
        self.cue(4,stretch.animate.set_value(2),sigma.animate.set_value(1.1),seconds=3)
        self.cue(5,FadeIn(label('점성의 존재만으로 충분할까?',0,2.35,GOLD,28)),FadeIn(self.note('늘어남과 Gaussian 확산을 분리한 개념도 · 실제 흐름에서는 함께 작용')))
        tube.clear_updaters();profile.clear_updaters()

    def scene2(self):
        angle=ValueTracker(0);width=ValueTracker(1.1);c=np.array([-3,0,0])
        omega=always_redraw(lambda:Arrow(c,c+np.array([np.cos(angle.get_value()),np.sin(angle.get_value()),0]),buff=0,color=GOLD,stroke_width=5))
        bell=always_redraw(lambda:self.gaussian(width.get_value(),conserve=False))
        self.add(Circle(radius=1,color=MUTED).move_to(c),omega,bell)
        self.cue(1,FadeIn(label('Dω/Dt = Jᵤω + νΔω',0,2.35,INK,28)))
        self.cue(2,FadeIn(label('변형과 정렬',-3,1.8,CYAN,25)),FadeIn(label('공간 분포와 확산',3,1.8,GREEN,25)))
        self.cue(3,FadeIn(label('두 항의 비율은 고정되어 있지 않다',0,-1.65,INK,25)))
        self.cue(4,angle.animate.set_value(PI/2),seconds=4)
        self.cue(5,width.animate.set_value(.5),FadeIn(label('같은 ν · 다른 공간적 차이',3,-1.2,GREEN,22)),seconds=4)
        self.cue(6,FadeIn(self.note('고정 S의 정렬 비교 · Laplacian의 값은 공간 분포에 의존 · 실제 NS 해 아님')))
        self.cue(7)
        omega.clear_updaters();bell.clear_updaters()

    def scene3(self):
        xs=[-5,-5/3,5/3,5]
        labels=VGroup(*[label(t,x,1.65,INK,26) for t,x in zip(['입력','층 1','층 2','출력'],xs)])
        arrows,nums=self.stage_arrows([1,2,4,8]);self.add(labels,arrows[0],nums[0])
        self.cue(1)
        forward_label=label('작은 입력 변화：순전파',0,2.35,CYAN,27)
        self.cue(2,FadeIn(forward_label))
        self.cue(3,FadeIn(arrows[1:]),FadeIn(nums[1:]),seconds=4)
        self.cue(4,FadeIn(label('정렬된 방향의 예시 · J=diag(2,0.5)',0,-1.65,MUTED,23)))
        reverse,reverse_nums=self.stage_arrows([8,4,2,1],color=PINK)
        self.cue(5,FadeOut(forward_label),FadeOut(arrows),FadeOut(nums),FadeIn(reverse),FadeIn(reverse_nums),FadeIn(Arrow([4,.75,0],[-4,.75,0],buff=0,color=PINK)),seconds=3)
        self.cue(6,FadeIn(label('역전파：g_l = J_lᵀ g_(l+1)',0,-2.05,PINK,26)))
        self.cue(7,FadeIn(self.note('Exploding Gradient · 순전파 변화와 역전파 gradient는 구별')))

    def scene4(self):
        c=np.array([-3,-.6,0]);circle=Circle(radius=.75,color=GREEN).move_to(c)
        vector=Arrow(c,c+[1.5,2,0],buff=0,color=GOLD,stroke_width=5)
        self.add(vector,label('전체 gradient 노름',3,1.3,INK,27))
        self.cue(1)
        self.cue(2,Create(circle),FadeIn(label('임계값 c=3',-3,1.9,GREEN,26)))
        self.cue(3,Transform(vector,Arrow(c,c+[.45,.6,0],buff=0,color=GOLD,stroke_width=5)),FadeIn(label('길이 10 → 3 · 방향 유지',3,.5,GOLD,27)),seconds=4)
        self.cue(4,FadeIn(label('Global Norm Clipping',0,2.35,INK,29)),FadeIn(label('g̃ = g · min(1, 3 / ‖g‖)',3,-1.2,MUTED,24)))
        self.cue(5,FadeIn(label('SGD · η=0.1 → 보폭 ≤ 0.3',3,-.4,GREEN,25)))
        self.cue(6,FadeIn(self.note('모은 파라미터 gradient의 L₂ 노름 · optimizer 후처리와 내부 신호는 별도')))
        self.cue(7,FadeIn(label('큰 결과를 제한한다',0,-1.95,GOLD,27)))

    def scene5(self):
        a,an=self.stage_arrows([1,2,4,8,3],y=.7,color=PINK,scale=.13)
        b,bn=self.stage_arrows([1,1.2,1.1,1.3,1.2],y=-.8,color=GREEN,scale=.4)
        self.add(label('A：내부 증폭 후 결과 제한',0,2.1,PINK,26))
        self.cue(1)
        self.cue(2,FadeIn(a[:4]),FadeIn(an[:4]))
        self.cue(3,FadeIn(a[4]),FadeIn(an[4]),FadeIn(label('Clipping',5,1.4,GOLD,22)))
        self.cue(4,FadeIn(b),FadeIn(bn),FadeIn(label('B：전달 구조의 증폭 제어',0,-1.95,GREEN,25)))
        self.cue(5)
        self.cue(6,FadeIn(self.note('두 경로는 이상적인 선형 비교 · 작은 개별 증폭도 누적될 수 있음')))
        self.cue(7,FadeIn(label('어디에 개입하는가?',0,2.65,INK,26)))

    def scene6(self):
        self.add(label('Normalization',-3,1.85,CYAN,28),label('Residual Connection',3,1.85,GREEN,26))
        before=label('[10, 12, 14]',-3,.6,CYAN,27);after=label('[−1.22, 0, 1.22]',-3,-.2,CYAN,26)
        self.cue(1)
        self.cue(2,FadeIn(before),FadeIn(after),FadeIn(label('평균과 스케일 조절',-3,-1,MUTED,23)))
        split=VGroup(Arrow([1.2,.55,0],[4.8,.55,0],buff=0,color=GREEN),Arrow([1.2,.55,0],[2.2,-.45,0],buff=0,color=MUTED),Arrow([3.8,-.45,0],[4.8,.55,0],buff=0,color=MUTED),label('F',3,-.45,GOLD,25),label('x + F(x)',3,1.15,GREEN,27))
        self.cue(3,FadeIn(split))
        self.cue(4,FadeIn(self.note('표현의 크기 조절과 잔차 경로는 모든 방향의 축소를 보장하지 않는다')))
        self.cue(5,FadeOut(split),FadeIn(label('J_y = I + J_F',3,1.05,GREEN,28)))
        origin=np.array([2.3,-.6,0]);identity=Arrow(origin,origin+[1,0,0],buff=0,color=CYAN,stroke_width=4);residual=Arrow(origin+[1,0,0],origin+[1.8,0,0],buff=0,color=GOLD,stroke_width=4)
        gain=label('같은 방향：1+0.8=1.8',3,.3,GOLD,24)
        opposite=label('반대 방향：1−0.8=0.2',3,.3,GOLD,24)
        self.cue(6,Succession(AnimationGroup(FadeIn(identity),FadeIn(residual),FadeIn(gain)),AnimationGroup(Transform(residual,Arrow(origin+[1,0,0],origin+[.2,0,0],buff=0,color=GOLD,stroke_width=4)),FadeOut(gain)),FadeIn(opposite)),seconds=5)

    def scene7(self):
        columns=[-4.4,0,4.2]
        headings=VGroup(*[label(t,x,2.1,INK,24) for t,x in zip(['시스템','증폭 가능성','제어의 대상'],columns)])
        rows=VGroup(*[VGroup(*[label(t,x,y,c,22) for t,x in zip(texts,columns)]) for y,texts,c in [(1,['유체','소용돌이 늘어남','공간 차이의 확산'],CYAN),(0,['신경망 역전파','gradient 증폭','큰 gradient 결과'],PINK),(-1,['신경망 순전파','방향별 증폭','표현과 전달 구조'],GREEN)]])
        self.add(headings)
        self.cue(1)
        self.cue(2,FadeIn(rows[0]))
        self.cue(3,FadeIn(rows[1]))
        self.cue(4,FadeIn(rows[2]))
        self.cue(5,FadeIn(label('서로 같은 연산이 아니다',0,-1.9,GOLD,26)))
        self.cue(6)
        self.cue(7,FadeIn(self.note('무엇을 제한하며, 그 제한은 무엇을 보장하는가?')))
        self.cue(8,FadeOut(headings),FadeOut(rows),FadeIn(label('제어 장치의 존재 ≠ 전체 안정성의 증명',0,.55,INK,30)))

    def scene8(self):
        def p(t,norm):return np.array([-5+10*t/6,-1.35+.75*norm,0])
        ts=np.linspace(0,6,180)
        monotone=VMobject(stroke_color=GREEN,stroke_width=3,fill_opacity=0).set_points_as_corners([p(t,np.exp(-t)) for t in ts])
        transient=VMobject(stroke_color=PINK,stroke_width=3,fill_opacity=0).set_points_as_corners([p(t,np.hypot(12*(np.exp(-t)-np.exp(-2*t)),np.exp(-2*t))) for t in ts])
        axes=VGroup(Line(p(0,0),p(6,0),color=MUTED),Line(p(0,0),p(0,3.5),color=MUTED),label('시간',5,-1.8,MUTED,22),label('변화의 크기',-4.3,1.75,MUTED,23))
        self.cue(1,FadeIn(axes))
        self.cue(2,Create(monotone),FadeIn(label('계속 감소',-2,1.85,GREEN,25)))
        self.cue(3,Create(transient),FadeIn(label('일시적 증가 후 감소',2.6,1.85,PINK,25)),seconds=4)
        self.cue(4,FadeIn(label('장기 감소 ≠ 매 순간 감소',0,2.35,INK,28)))
        self.cue(5,Indicate(transient,color=GOLD))
        self.cue(6,FadeIn(self.note('두 곡선 모두 장기적으로 0 · 실제 점근안정 선형 모형의 노름')))
        self.cue(7,Indicate(Dot(p(6,0),color=GOLD),color=GOLD))
        values=np.hypot(12*(np.exp(-ts)-np.exp(-2*ts)),np.exp(-2*ts));i=int(np.argmax(values))
        self.cue(8,Indicate(Circle(radius=.16,color=GOLD).move_to(p(ts[i],values[i])),color=GOLD),FadeIn(label('다음 막：Non-normal Dynamics',0,-2.05,GOLD,26)))

