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
        record=records[self.index-1];self.chapter=7
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

    def profile(self,u,center,color):
        c=np.array(center);pts=[c+[x,1.4*y,0] for x,y in zip(np.linspace(-2.2,2.2,len(u)),u)]
        curve=VMobject(stroke_color=color,stroke_width=3,fill_opacity=0).set_points_as_corners(pts)
        return VGroup(curve,*[Dot(p,radius=.035,color=color) for p in pts])

    def scene1(self):
        f=field(center=(-2.5,0,0));self.add(f)
        self.cue(1)
        self.cue(2,FadeIn(label('컴퓨터 속 유체',3,1.3,CYAN,28)))
        self.cue(3,FadeIn(label('연속적인 공간 · 시간',3,.5,INK,25)))
        self.cue(4,FadeIn(label('모든 위치를 계산할 수는 없다',3,-.35,MUTED,22)))
        mesh=self.mesh(.5,(-2.5,0,0),4.5,3)
        self.cue(5,Create(mesh),FadeIn(self.ticks(6,(3,-1.35,0),4)),seconds=3)
        self.cue(6,FadeIn(label('두 가지 간격',0,2.35,GOLD,28)))
        self.cue(7,FadeIn(label('Δx：공간',-2.5,-2.1,CYAN,24)),FadeIn(label('Δt：시간',3,-2.1,GOLD,24)))

    def scene2(self):
        mesh=self.mesh(1,(-2.8,.1,0),4,2.5);ticks=self.ticks(4,(3,-.5,0),4)
        self.add(mesh,ticks,label('Δx',-2.8,1.8,CYAN,28),label('Δt',3,1.8,GOLD,28))
        self.cue(1)
        self.cue(2,Transform(mesh,self.mesh(.5,(-2.8,.1,0),4,2.5)),FadeIn(label('간격 1/2',-2.8,-1.8,CYAN,27)))
        self.cue(3,Indicate(mesh,color=GOLD))
        self.cue(4,FadeIn(label('시간은 그대로 두어도 될까?',3,.65,INK,25)))
        self.cue(5,FadeIn(self.note('1차원 확산 · 등간격 중앙차분 · Forward Euler')))
        self.cue(6,Transform(ticks,self.ticks(16,(3,-.5,0),4)),FadeIn(label('허용 Δt → 1/4',3,-1.8,GOLD,28)),seconds=4)
        self.cue(7,FadeIn(label('Δt ≤ Δx² / (2ν)',0,2.35,INK,28)))

    def scene3(self):
        j=np.arange(16);initial=.3*np.cos(TAU*j/16)+.03*(-1.)**j
        def states(r):
            values=[initial.copy()]
            for _ in range(10):
                u=values[-1];values.append(u+r*(np.roll(u,1)-2*u+np.roll(u,-1)))
            return values
        good,bad=states(.2),states(.6);left=self.profile(initial,(-3,0,0),GREEN);right=self.profile(initial,(3,0,0),PINK)
        self.add(left,right,Line([-5.2,0,0],[-.8,0,0],color=MUTED),Line([.8,0,0],[5.2,0,0],color=MUTED),label('작은 Δt · r=0.2',-3,1.8,GREEN,25),label('큰 Δt · r=0.6',3,1.8,PINK,25))
        self.cue(1)
        self.cue(2,FadeIn(label('원래 확산은 차이를 완화한다',0,2.35,INK,25)))
        animations=AnimationGroup(Succession(*[Transform(left,self.profile(u,(-3,0,0),GREEN)) for u in good[1:]]),Succession(*[Transform(right,self.profile(u,(3,0,0),PINK)) for u in bad[1:]]))
        self.cue(3,animations,seconds=5)
        error_label=label('오차 모드가 진동하며 커진다',3,-1.85,PINK,23)
        self.cue(4,FadeIn(error_label))
        self.cue(5,FadeIn(self.note('같은 10스텝 비교 · Δt가 달라 물리 경과 시간도 다름')))
        self.cue(6,Succession(FadeOut(error_label),FadeIn(label('수치 불안정 ≠ 실제 특이점',0,-2.05,INK,28))))
        self.cue(7)

    def scene4(self):
        mesh=self.mesh(1,(0,.2,0),9,3);self.add(mesh)
        self.cue(1)
        region_label=label('대부분은 완만한 영역',-3,2.1,MUTED,24)
        self.cue(2,FadeIn(region_label))
        hotspot=Circle(radius=.6,color=PINK).move_to([1.5,.2,0])
        self.cue(3,Create(hotspot))
        fine=self.mesh(.2,(1.5,.2,0),1.6,1.6,GOLD)
        self.cue(4,Create(fine))
        time=self.ticks(6,(0,-1.75,0),9);self.cue(5,FadeIn(time))
        self.cue(6,Transform(time,self.ticks(24,(0,-1.75,0),9)),FadeOut(region_label),FadeIn(label('작은 격자 → 전역 보폭 제한',0,2.35,GOLD,26)),seconds=4)
        self.cue(7,Indicate(fine,color=PINK))
        self.cue(8,FadeIn(self.note('전역 Δt를 쓰는 명시적 계산 예시 · 암시적/국소 적분은 다른 선택')))

    def scene5(self):
        left=self.contours((-3,0,0)).rotate(PI/2);right=self.contours((3,0,0)).rotate(PI/2);self.add(left,right)
        self.cue(1)
        dots=[Dot([-2.2,.1,0],color=GOLD),Dot([3.8,.1,0],color=GOLD)]
        self.cue(2,*[FadeIn(d) for d in dots])
        gradient=Arrow([-2.2,.1,0],[-2.6,-.5,0],buff=0,color=GOLD)
        self.cue(3,Create(gradient),FadeIn(label('−∇L：내려가는 방향',-3,-2,GOLD,23)))
        self.cue(4,FadeIn(label('η=0.1',-3,1.9,GREEN,26)),FadeIn(label('η=0.2',3,1.9,PINK,26)))
        sequences=[]
        for c,d,eta,color in zip([-3,3],dots,[.1,.2],[GREEN,PINK]):
            point=np.array([.8,.1]);an=[]
            for _ in range(8):
                nxt=(1-eta*np.array([1,12]))*point
                an.append(AnimationGroup(Create(Line([c+point[0],point[1],0],[c+nxt[0],nxt[1],0],color=color)),d.animate.move_to([c+nxt[0],nxt[1],0])))
                point=nxt
            sequences.append(Succession(*an))
        self.cue(5,FadeOut(gradient),AnimationGroup(*sequences),seconds=5)
        self.cue(6,FadeIn(self.note('H=diag(1,12)인 이차 손실 · 같은 시작점 · 실제 모델의 측정 궤적 아님')))

    def scene6(self):
        contours=self.contours(ratio=1);self.add(contours)
        self.cue(1)
        self.cue(2,Transform(contours,self.contours().rotate(PI/2)),FadeIn(label('입력 공간 → 파라미터 공간',0,2.35,MUTED,25)))
        flat=Arrow(ORIGIN,[.5,0,0],buff=0,color=CYAN,stroke_width=5)
        steep=Arrow(ORIGIN,[0,.5,0],buff=0,color=PINK,stroke_width=5)
        self.cue(3,Create(flat),FadeIn(label('같은 거리：완만한 방향',-3.5,.6,CYAN,24)),FadeIn(label('ΔL = 0.125',-3.5,-.25,CYAN,28)))
        self.cue(4,Create(steep),FadeIn(label('같은 거리：가파른 방향',3.6,.6,PINK,24)),FadeIn(label('ΔL = 1.5',3.6,-.25,PINK,28)))
        self.cue(5,FadeIn(label('Hessian  H = ∇²L',0,-1.95,INK,29)))
        self.cue(6,FadeIn(self.note('최솟값 주변 · 고유벡터=곡률 방향 / 고유값=휘어지는 정도')))

    def scene7(self):
        self.add(label('같은 학습률 η=0.2',0,2.35,INK,28),label('완만：λ=1',-3,1.8,CYAN,27),label('가파름：λ=12',3,1.8,PINK,27))
        dots=[Dot([-3+.15,0,0],color=CYAN),Dot([3+.15,0,0],color=PINK)]
        self.add(*dots,*[Line([c-1.6,0,0],[c+1.6,0,0],color=MUTED) for c in [-3,3]])
        self.cue(1)
        self.cue(2,FadeIn(label('1 → 0.8 → 0.64…',-3,-1,CYAN,25)))
        self.cue(3,FadeIn(label('1 → −1.4 → 1.96…',3,-1,PINK,25)))
        self.cue(4,AnimationGroup(*[Succession(*[d.animate.move_to([c+.15*g**n,0,0]) for n in range(1,8)]) for d,c,g in zip(dots,[-3,3],[.8,-1.4])]),seconds=5)
        self.cue(5,Indicate(dots[1],color=PINK))
        self.cue(6,FadeIn(label('0 < η < 2 / λmax',0,-1.95,GOLD,29)))
        self.cue(7,FadeIn(self.note('고정 양의 정부호 이차 손실 · 모든 초기 오차에 대한 수렴 조건')))

    def scene8(self):
        mesh=self.mesh(.45,(-3,.2,0),4,2.7);contours=self.contours((3,.2,0));self.add(mesh,contours)
        self.cue(1)
        self.cue(2,FadeIn(label('명시적 확산',-3,1.95,CYAN,27)),FadeIn(label('Δt ∝ Δx²',-3,-1.65,CYAN,30)))
        self.cue(3,FadeIn(label('경사하강법',3,1.95,GREEN,27)),FadeIn(label('η < 2 / λmax',3,-1.65,GREEN,30)))
        self.cue(4,FadeIn(self.note('1D FTCS 확산 / 고정 양의 정부호 이차 손실 · 서로 다른 계산')))
        self.cue(5)
        self.cue(6,FadeIn(label('가장 까다로운 모드에서도 안정적이어야 한다',0,2.35,GOLD,26)))
        self.cue(7,Indicate(mesh,color=PINK),Indicate(contours,color=PINK))

    def modeplot(self,amplitude,center,color):
        return self.profile(amplitude*(-1.)**np.arange(12),center,color)

    def scene9(self):
        left=self.modeplot(.18,(-3,.25,0),CYAN);right=Arrow([3,0,0],[3,.45,0],buff=0,color=GREEN)
        self.add(left,right,label('격자의 고주파 모드',-3,1.8,CYAN,25),label('손실의 고유방향',3,1.8,GREEN,25))
        self.cue(1)
        self.cue(2,FadeIn(label('다음 값 = 배율 × 현재 값',0,2.35,GOLD,29)))
        self.cue(3,FadeIn(label('a_next = g(k) a',-3,-1.2,CYAN,28)))
        self.cue(4,FadeIn(label('e_next = (1−ηλ) e',3,-1.2,GREEN,27)))
        self.cue(5,FadeIn(label('예시 배율：−1.4',0,-1.95,PINK,27)))
        self.cue(6,AnimationGroup(Succession(*[Transform(left,self.modeplot(.18*(-1.4)**n,(-3,.25,0),CYAN)) for n in range(1,5)]),Succession(*[Transform(right,Arrow([3,0,0],[3,.45*(-1.4)**n,0],buff=0,color=GREEN)) for n in range(1,5)])),seconds=5)
        self.cue(7,FadeIn(self.note('|g|>1：증폭 / |g|≤1：비증폭 / |g|<1：감쇠 · 평균 모드 g=1은 보존')))

    def scene10(self):
        cards=VGroup(*[VGroup(RoundedRectangle(width=3.6,height=1.35,corner_radius=.12,stroke_color=c),label(t,0,0,c,26)).move_to([x,.8,0]) for x,t,c in zip([-4.3,0,4.3],['전체와 극단값','방향별 증폭','업데이트 안정성'],[CYAN,GREEN,GOLD])])
        self.cue(1,FadeIn(cards))
        self.cue(2,Indicate(cards[0],color=CYAN))
        self.cue(3,Indicate(cards[1],color=GREEN))
        self.cue(4,Indicate(cards[2],color=GOLD))
        self.cue(5)
        distinction=label('실제 특이점 ≠ 수치 불안정',0,-1.2,PINK,30)
        self.cue(6,FadeIn(distinction))
        self.cue(7,FadeIn(label('가장 제한적인 모드가 전체 보폭을 제약한다',0,2.35,INK,27)))
        self.cue(8,FadeOut(cards),FadeOut(distinction))
        path=VMobject(stroke_color=CYAN,stroke_width=3,fill_opacity=0).set_points_smoothly([[-4,-.8,0],[-2,.25,0],[0,-.25,0],[2,.6,0]])
        goal=Circle(radius=.22,color=GOLD).move_to([4,.8,0])
        self.cue(9,Create(path),Create(goal),FadeIn(label('Possible ≠ Reachable?',0,-1.65,GOLD,32)),FadeIn(self.note('다음 막：가능한 상태와 실제 과정이 도달하는 상태')),seconds=4)

