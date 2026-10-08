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
        record=records[self.index-1];self.chapter=8
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

    @staticmethod
    def grad(p):
        x,y=p;return np.array([x**3-x+.12,y])

    def lossmap(self):
        g=VGroup()
        for level in [-.09,.03,.15,.3,.5,.8]:
            roots=np.roots([.25,0,-.5,.12,.25-level])
            roots=sorted(float(z.real) for z in roots if abs(z.imag)<1e-8)
            bounds=[-1.95]+[x for x in roots if -1.95<x<1.95]+[1.95]
            for lo,hi in zip(bounds,bounds[1:]):
                mid=(lo+hi)/2
                if .25*(mid*mid-1)**2+.12*mid>level:continue
                x=np.linspace(lo,hi,100)
                y=np.sqrt(np.maximum(0,2*(level-.25*(x*x-1)**2-.12*x)))
                for sign in [-1,1]:
                    pts=[[1.9*a,1.25*sign*b,0] for a,b in zip(x,y)]
                    g.add(VMobject(stroke_color=CYAN,stroke_width=1,stroke_opacity=.45,fill_opacity=0).set_points_as_corners(pts))
        return g

    def lossfield(self):
        g=VGroup()
        for x in np.linspace(-1.6,1.6,9):
            for y in np.linspace(-1.05,1.05,7):
                v=-self.grad([x,y]);q=np.array([1.9*v[0],1.25*v[1],0]);q=q*.27/max(np.linalg.norm(q),.4)
                p=np.array([1.9*x,1.25*y,0]);g.add(Arrow(p,p+q,buff=0,color=MUTED,stroke_width=1.5,max_tip_length_to_length_ratio=.25))
        return g

    def gd_path(self,start,n=50):
        p=np.array(start,dtype=float);points=[p.copy()]
        for _ in range(n):p=p-.12*self.grad(p);points.append(p.copy())
        return [np.array([1.9*p[0],1.25*p[1],0]) for p in points]

    def curve(self,points,color):return VMobject(stroke_color=color,stroke_width=3,fill_opacity=0).set_points_as_corners(points)

    def animate_path(self,points,color):
        dot=Dot(points[0],radius=.07,color=color)
        path=self.curve(points,color);return dot,path

    def solution_plane(self,center=(0,0,0),scale=1):
        c=np.array(center)
        def p(a,b):return c+scale*np.array([a,b,0])
        axes=VGroup(Line(p(-1.3,0),p(1.5,0),color=MUTED),Line(p(0,-.2),p(0,2.2),color=MUTED))
        line=Line(p(-1.1,2.1),p(1.1,-.1),color=GREEN,stroke_width=3)
        return VGroup(axes,line)

    def scene1(self):
        flow=field(center=(-3,0,0),peak=True);self.add(flow)
        self.cue(1)
        concentration_label=label('빠른 영역 ↓ / 속도 ↑',-3,2.05,GOLD,24)
        self.cue(2,FadeIn(concentration_label))
        card=RoundedRectangle(width=4.4,height=2.6,corner_radius=.15,stroke_color=MUTED).move_to([3,.2,0])
        self.cue(3,FadeIn(card),FadeIn(label('이 모양이 해인가?',3,.85,INK,28)))
        self.cue(4,FadeIn(label('PDE · 초기 조건 · 외력',3,.05,CYAN,25)),FadeIn(label('비압축성 · 공간 조건',3,-.6,MUTED,23)))
        self.cue(5,FadeOut(concentration_label),FadeIn(label('모양의 구성 → 조건의 검증',0,2.35,INK,26)),FadeIn(self.note('설명용 집중 모형 · 실제 Navier–Stokes 해를 새로 검증하는 장면 아님')))
        self.cue(6,FadeIn(label('존재와 도달은 같은가?',0,-1.95,GOLD,29)))

    def scene2(self):
        dots=VGroup(*[Dot([x,y,0],radius=.035,color=MUTED) for x in np.linspace(-5,5,15) for y in np.linspace(-1.6,1.7,7)])
        self.add(dots)
        self.cue(1)
        self.cue(2,FadeIn(label('파라미터마다 다른 함수',0,2.35,INK,26)))
        target=Circle(radius=.19,color=GREEN).move_to([2.7,.7,0]);self.cue(3,Create(target))
        self.cue(4,FadeIn(label('θ*',3.2,1.15,GREEN,29)))
        self.cue(5,FadeIn(label('L(θ*) ≈ 0',3,-.1,GREEN,28)))
        self.cue(6,Indicate(target,color=GOLD))
        start=Dot([-3.6,-.9,0],color=GOLD,radius=.1)
        self.cue(7,FadeIn(start),FadeIn(label('θ₀',-4,-1.4,GOLD,28)),FadeIn(self.note('좋은 답의 존재만으로 이동 경로가 정해지지는 않는다')))

    def scene3(self):
        bg=self.lossmap();self.add(bg)
        self.cue(1)
        arrows=self.lossfield();self.cue(2,FadeIn(arrows))
        points=self.gd_path([-.25,1.]);dot,path=self.animate_path(points,GOLD);self.cue(3,FadeIn(dot))
        self.cue(4,Create(path),MoveAlongPath(dot,path,rate_func=linear),seconds=5)
        self.cue(5,FadeIn(label('현재 위치의 정보로 다음 위치를 결정',0,2.35,INK,25)))
        self.cue(6,FadeIn(label('θ_next = θ − η∇L(θ)',0,-1.95,GOLD,28)),FadeIn(self.note('같은 toy loss · 실제 이산 GD 경로 · 미리 목표점을 지정한 이동 아님')))

    def scene4(self):
        self.add(self.lossmap())
        points=[self.gd_path(p) for p in [[-1.7,.9],[1.7,.9]]]
        items=[self.animate_path(p,c) for p,c in zip(points,[GREEN,PINK])]
        self.add(*[d for d,p in items]);self.cue(1)
        self.cue(2,FadeIn(label('같은 손실 · 같은 학습률 η=0.12',0,2.35,INK,25)))
        self.cue(3,FadeIn(self.lossfield()))
        self.cue(4,*[a for d,p in items for a in [Create(p),MoveAlongPath(d,p,rate_func=linear)]],seconds=5)
        self.cue(5,FadeIn(label('더 낮은 손실',-3,-1.95,GREEN,25)),FadeIn(label('더 높은 국소 최소',3,-1.95,PINK,25)))
        self.cue(6,FadeIn(self.note('설명용 비볼록 모형 · 실제 신경망의 모든 학습 실패를 국소 최소로 설명하지 않는다')))

    def scene5(self):
        centers=[-3,3]
        self.add(*[self.solution_plane((c,-1.05,0),.85) for c in centers])
        self.cue(1)
        self.cue(2,FadeIn(label('f(x)=ax+b · 훈련점 (1,1)',0,2.35,INK,27)))
        ends=[np.array([.5,.5]),np.array([-.5,1.5])];starts=[np.array([0,0]),np.array([0,2])]
        for c,st,en,color in zip(centers,starts,ends,[CYAN,PINK]):
            a=np.array([c,-1.05,0])+.85*np.r_[st,0];b=np.array([c,-1.05,0])+.85*np.r_[en,0]
            self.add(Dot(a,color=color,radius=.055),Arrow(a,b,buff=.05,color=color,stroke_width=3),Dot(b,color=color,radius=.08))
        self.cue(3,FadeIn(label('A：(a,b)=(0.5,0.5)',-3,1.8,CYAN,24)),FadeIn(label('B：(a,b)=(−0.5,1.5)',3,1.8,PINK,24)))
        self.cue(4,FadeIn(label('새 입력 x=−1 → 0',-3,-1.8,CYAN,27)),FadeIn(label('새 입력 x=−1 → 2',3,-1.8,PINK,27)))
        self.cue(5,FadeIn(label('훈련 예측은 둘 다 1 · 손실은 0',0,1.3,GREEN,24)))
        self.cue(6,FadeIn(self.note('단일 훈련점 선형 모델의 수렴 극한 해 · 새 입력 참값 미지정, 성능 우열 아님')))
        self.cue(7,*[Indicate(Circle(radius=.15,color=GOLD).move_to(np.array([c,-1.05,0])+.85*np.r_[en,0]),color=GOLD) for c,en in zip(centers,ends)])

    def scene6(self):
        center=np.array([-.6,-1.1,0]);scale=1.25
        def pos(v):return center+scale*np.r_[v,0]
        plane=self.solution_plane(center,scale);self.add(plane)
        self.cue(1)
        self.cue(2,FadeIn(label('좋은 해들의 집합：a+b=1',0,2.35,GREEN,28)))
        a=Arrow(pos([0,0]),pos([.5,.5]),buff=.03,color=CYAN);b=Arrow(pos([0,2]),pos([-.5,1.5]),buff=.03,color=PINK)
        self.cue(3,Create(a),Create(b),FadeIn(label('출발점이 달라지면 선택도 달라진다',3.4,.9,INK,22)))
        extra=Arrow(pos([0,0]),pos([.8,.2]),buff=.03,color=GOLD)
        self.cue(4,Create(extra),FadeIn(label('Implicit Bias',3.4,.05,GOLD,29)),FadeIn(label('같은 출발 · 방향별 보정 → 다른 해',3.4,-.65,GOLD,21)))
        self.cue(5,FadeIn(self.note('초기값 (0,0)：GD→(0.5,0.5) / 고정 보정 diag(4,1)→(0.8,0.2) · 정규화 추가 없음')))

    def scene7(self):
        left=self.vortex(center=(-3,0,0),scale=.8);right=self.solution_plane((3,-.8,0),1)
        self.add(left,right,label('유체',-3,1.8,CYAN,29),label('신경망',3,1.8,GREEN,29))
        self.cue(1)
        self.cue(2,FadeIn(label('후보 속도장의 구성',-3,-1.7,CYAN,24)))
        self.cue(3,FadeIn(label('PDE · 초기 조건 · 외력 검증',-3,-2.1,MUTED,21)))
        self.cue(4,FadeIn(label('표현 가능한 여러 해',3,-1.7,GREEN,24)))
        arrow=Arrow([2,-.8,0],[3.5,-.3,0],buff=.05,color=GOLD)
        self.cue(5,Create(arrow),FadeIn(label('초기값 · 학습 규칙에 따른 선택',3,-2.1,MUTED,21)))
        self.cue(6,FadeIn(label('검증과 선택은 서로 다른 문제',0,2.35,INK,28)))
        self.cue(7,Indicate(left,color=CYAN),Indicate(right,color=GREEN))
        self.cue(8)
        self.cue(9,FadeIn(self.note('가능한 상태의 집합만으로 실제 실현되는 상태를 설명할 수 없다')))

    def scene8(self):
        names=['전체와 국소','방향별 증폭','가장 제한적인 모드','학습 경로와 해 선택'];xs=[-4.8,-1.6,1.6,4.8]
        cards=VGroup(*[VGroup(RoundedRectangle(width=2.9,height=1.3,corner_radius=.12,stroke_color=c),txt(n,22,c,width=2.6)).move_to([x,.5,0]) for x,n,c in zip(xs,names,[CYAN,GREEN,GOLD,PINK])])
        self.cue(1,FadeIn(cards))
        self.cue(2,Indicate(cards[3],color=PINK))
        self.cue(3,FadeIn(label('최종 상태만으로는 부족하다',0,2.35,INK,28)))
        self.cue(4,FadeIn(label('비슷한 손실 · 서로 다른 경로와 선택',0,-1.2,GREEN,27)))
        self.cue(5,Indicate(cards[3],color=GOLD))
        self.cue(6)
        self.cue(7,*[Indicate(card,color=GOLD) for card in cards])
        self.cue(8,FadeOut(cards))
        self.cue(9,FadeIn(label('증폭과 안정화는 어떻게 함께 작용할까?',0,.45,GOLD,31)),FadeIn(self.note('다음 막：지금까지 발견한 패턴을 다시 모은다')))

    def profile(self,u,center,color):
        c=np.array(center);pts=[c+[x,1.4*y,0] for x,y in zip(np.linspace(-2.2,2.2,len(u)),u)]
        curve=VMobject(stroke_color=color,stroke_width=3,fill_opacity=0).set_points_as_corners(pts)
        return VGroup(curve,*[Dot(p,radius=.035,color=color) for p in pts])

