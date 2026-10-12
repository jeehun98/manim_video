"""Non-normal transient amplification and asymptotic stability."""
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
        record=records[self.index-1];self.chapter=10
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


    def matrix_card(self,center=(0,0,0),coupling=10):
        c=np.array(center);g=VGroup(RoundedRectangle(width=3,height=1.7,corner_radius=.15,color=MUTED).move_to(c))
        for text,x,y,col in [('-1',-.7,.4,CYAN),(str(coupling),.7,.4,GOLD),('0',-.7,-.4,MUTED),('-1',.7,-.4,CYAN)]:g.add(label(text,c[0]+x,c[1]+y,col,36))
        return g

    def axes2(self,c,scale=1):
        c=np.array(c);return VGroup(Arrow(c+[-.3,0,0],c+[4*scale,0,0],buff=0,color=MUTED,stroke_width=2),Arrow(c+[0,-.3,0],c+[0,1.6*scale,0],buff=0,color=MUTED,stroke_width=2),label('0',c[0]-.2,c[1]-.2,MUTED,18))

    def propagator(self,t,k=10):return np.exp(-t)*np.array([[1,k*t],[0,1]])

    def curve(self,fun,start=0,end=6,color=CYAN):
        g=VMobject(stroke_color=color,stroke_width=3,fill_opacity=0);g.set_points_as_corners([fun(t) for t in np.linspace(start,end,180)]);return g

    def state(self,c,v,scale=1,color=GOLD):
        c=np.array(c);p=c+scale*np.array([v[0],v[1],0]);return VGroup(Line(c,p,color=color,stroke_width=5),Dot(p,radius=.06,color=color))

    def scene1(self):
        t=ValueTracker(0);c=np.array([0,-.8,0]);v=always_redraw(lambda:self.state(c,[0,1.8*np.exp(-t.get_value())]))
        self.add(self.axes2(c,.8),label('작은 변화',0,1.7,CYAN),v)
        self.cue(1);self.cue(2);self.cue(3);self.cue(4,t.animate.set_value(4),seconds=4)
        a=label('충분히 오래 지나면 → 0',0,.8,GREEN,32);self.cue(5,FadeIn(a))
        self.cue(6,FadeIn(label('결국 감소  ≠  매 순간 감소',0,-1.8,GOLD,31)))

    def scene2(self):
        card=self.matrix_card((-3,.5,0));self.cue(1,FadeIn(label('상태 변화 = A × 현재 상태',0,2.1,CYAN,28)))
        self.cue(2,FadeIn(card));axis=Arrow([.7,0,0],[5.8,0,0],buff=0,color=MUTED)
        eig=VGroup(axis,Line([4,-.7,0],[4,1.0,0],color=MUTED),Dot([2.5,0,0],color=GREEN),label('−1  (중복 2)',2.5,-.5,GREEN),label('Re λ',5.8,-.4,MUTED,19),label('0',4,-.4,MUTED,19))
        self.cue(3,FadeIn(eig));self.cue(4,FadeIn(self.note('고정된 유한차원 · 연속시간 · 선형 시스템')))
        self.cue(5,FadeIn(label('장기적으로 원점에 수렴',2.7,1.35,GREEN,29)))
        self.cue(6,FadeIn(label('그 사이의 경로는?',-3,-1.5,GOLD,30)))

    def scene3(self):
        t=ValueTracker(0);c=np.array([-4.6,-.7,0]);p=lambda z:c+np.r_[self.propagator(z)@np.array([0,1]),0]
        v=always_redraw(lambda:self.state(c,self.propagator(t.get_value())@np.array([0,1])))
        self.add(self.axes2(c),v,label('x(0) = (0, 1)',-2.5,2,CYAN,28))
        nums=VGroup()
        for i,(name,fn) in enumerate([('t',lambda:t.get_value()),('x₁',lambda:10*t.get_value()*np.exp(-t.get_value())),('x₂',lambda:np.exp(-t.get_value())),('‖x‖',lambda:np.linalg.norm(self.propagator(t.get_value())@[0,1]))]):
            y=1.1-i*.7;num=DecimalNumber(fn(),num_decimal_places=2,mob_class=Text,color=GOLD,font_size=30).move_to([4,y,0]);num.add_updater(lambda m,f=fn:m.set_value(f()));nums.add(label(name,2,y,MUTED,27),num)
        self.add(nums);self.cue(1);self.cue(2,t.animate.set_value(.2));self.cue(3,FadeIn(label('x₂ → x₁',-2.7,-1.7,GOLD,30)))
        self.cue(4,t.animate.set_value(1),Create(self.curve(p,0,1)),seconds=4)
        self.cue(5,t.animate.set_value(7),Create(self.curve(p,1,7)),seconds=5)
        self.cue(6,FadeIn(self.note('일시적 증폭: 선택한 초기 벡터의 크기 변화')))

    def scene4(self):
        t=ValueTracker(0)
        for x,k,title in [(-3.8,0,'전달 없음'),(2,10,'성분 사이 전달')]:
            c=[x,-.6,0];self.add(self.axes2(c,.7),label(title,x+1,1.8,CYAN,28),always_redraw(lambda c=c,k=k:self.state(c,self.propagator(t.get_value(),k)@[0,1],.7)),label('고유값 −1, −1',x+1,-1.6,MUTED,23))
        self.cue(1);self.cue(2);self.cue(3,FadeIn(label('같은 장기 감쇠율',0,2.35,GREEN,24)))
        self.cue(4,FadeIn(label('coupling = 10',3,1,GOLD,28)))
        self.cue(5,t.animate.set_value(1),seconds=4);self.cue(6,t.animate.set_value(6),FadeIn(self.note('중간의 증폭은 고유값만으로 읽을 수 없다')),seconds=4)

    def scene5(self):
        left=VGroup(label('정규',-3.3,1.8,GREEN),self.matrix_card((-3.3,0,0),0),label('AᵀA = AAᵀ',-3.3,-1.4,GREEN,27))
        right=VGroup(label('비정규',3.3,1.8,GOLD),self.matrix_card((3.3,0,0),10),label('AᵀA ≠ AAᵀ',3.3,-1.4,GOLD,27))
        self.cue(1);self.cue(2,FadeIn(left));self.cue(3,FadeIn(right));self.cue(4)
        self.cue(5,Indicate(left));self.cue(6,Indicate(right));self.cue(7,FadeIn(self.note('비정규성만으로 일시적 증폭이 보장되지는 않는다')))

    def scene6(self):
        t=ValueTracker(0);lc=np.array([-3.5,-.1,0]);rc=np.array([3,-.1,0]);scale=.85
        def ellipse():
            P=self.propagator(t.get_value());return self.curve(lambda a:rc+scale*np.r_[P@[np.cos(a),np.sin(a)],0],0,TAU)
        def direction():
            P=self.propagator(t.get_value());_,_,vh=np.linalg.svd(P);v=vh[0];return VGroup(self.state(lc,v,scale),self.state(rc,P@v,scale))
        self.add(Circle(radius=scale,color=GREEN).move_to(lc),always_redraw(ellipse),always_redraw(direction),label('같은 크기의 모든 초기 방향',-3.5,1.8,GREEN,24),label('시간 발전 P(t)',3,1.8,CYAN,28),Arrow([-1.8,0,0],[.2,0,0],color=MUTED))
        gain=DecimalNumber(1,num_decimal_places=2,mob_class=Text,color=GOLD,font_size=34).move_to([1,-1.65,0]);gain.add_updater(lambda m:m.set_value(np.linalg.svd(self.propagator(t.get_value()),compute_uv=False)[0]));self.add(label('최대 확대 비율',-1,-1.65,GOLD,26),gain)
        self.cue(1);self.cue(2);self.cue(3);self.cue(4,t.animate.set_value(.5));self.cue(5)
        self.cue(6,t.animate.set_value(1),FadeIn(self.note('σmax(P): 벡터 크기의 배율 · 에너지 배율은 그 제곱')))
        self.cue(7,t.animate.set_value(4),seconds=4)

    def scene7(self):
        rows=VGroup()
        for y,speed in [(-.9,.45),(-.3,.7),(.3,.95),(.9,1.2)]:
            for x in [-4,-2,0,2,4]:rows.add(Arrow([x,y,0],[x+speed,y,0],buff=0,color=CYAN,stroke_width=3))
        self.cue(1,FadeIn(rows));self.cue(2,FadeIn(label('위쪽: 빠른 기본 흐름',0,1.9,CYAN,26)))
        self.cue(3);rolls=VGroup(Arrow([-2,-.9,0],[-2,.5,0],color=GOLD),Arrow([2,.9,0],[2,-.5,0],color=PINK))
        self.cue(4,FadeIn(label('Lift-up',0,-1.8,GOLD,31)));self.cue(5,FadeIn(rolls))
        streaks=VGroup(Line([-4,.5,0],[0,.5,0],color=GOLD,stroke_width=10),Line([0,-.5,0],[4,-.5,0],color=PINK,stroke_width=10),label('느린 유체 ↑ → 저속 교란',-3,1.25,GOLD,22),label('빠른 유체 ↓ → 고속 교란',3,-1.25,PINK,22))
        self.cue(6,FadeIn(streaks));self.cue(7,FadeIn(self.note('전단의 속도 차이 재배치 개념도 · 실제 NS 시뮬레이션 아님')))

    def scene8(self):
        nodes=VGroup(Circle(radius=.45,color=CYAN).move_to([1,-.1,0]),Circle(radius=.45,color=GOLD).move_to([4,-.1,0]),label('h₂',1,-.1,CYAN),label('h₁',4,-.1,GOLD),Arrow([1.5,-.1,0],[3.5,-.1,0],color=GOLD),label('성분 사이 전달',2.5,.7,GOLD,23))
        fluid=VGroup(self.vortex(center=(-3,-.2,0)),label('유체의 작은 교란',-3,1.8,CYAN,26))
        self.cue(1,FadeIn(label('연속시간 순환 신경망',2.5,1.8,GOLD,26)));self.cue(2,FadeIn(nodes));self.cue(3)
        self.cue(4,FadeIn(label('기준 상태 주변: δh의 변화 = A δh',0,-1.65,INK,28)))
        self.cue(5,FadeIn(fluid));self.cue(6,FadeIn(self.note('고정점 주변 선형화 · 이산 RNN은 M의 반복, 안정조건 ρ(M) < 1')))

    def scene9(self):
        origin=np.array([-5,-1.7,0]);axes=VGroup(Arrow(origin,origin+[10,0,0],buff=0,color=MUTED),Arrow(origin,origin+[0,3.8,0],buff=0,color=MUTED),label('시간',5,-1.95,MUTED,20))
        fun=lambda t,v:origin+np.array([1.5*t,.85*np.linalg.norm(self.propagator(t)@v),0])
        self.cue(1,FadeIn(axes));self.cue(2)
        a=self.curve(lambda t:fun(t,[1,0]),color=GREEN);b=self.curve(lambda t:fun(t,[0,1]),color=GOLD)
        self.cue(3,Create(a));self.cue(4,Create(b),seconds=4)
        self.cue(5,FadeIn(label('같은 크기 · 다른 입력 방향',1,2.25,INK,26)))
        self.cue(6,FadeIn(label('e₁: 감소',2,.8,GREEN,27)),FadeIn(label('e₂: 일시적 반응',2,1.45,GOLD,27)))
        self.cue(7,FadeIn(self.note('입력 흔적의 설명용 모형 · 유용성은 과제와 읽기 방식에 달림')))

    def scene10(self):
        cards=VGroup()
        data=[('장기적으로 사라지는가?','Re λmax = −1','고유값',GREEN),('정해진 시간의 최대 증폭','G(3) = 1.50','σmax(P(3))',CYAN),('전체 시간 중 최대 증폭','Gpeak = 3.72','t ≈ 0.98',GOLD)]
        for x,(title,value,metric,col) in zip([-4.3,0,4.3],data):
            cards.add(VGroup(RoundedRectangle(width=3.8,height=2.6,corner_radius=.15,color=col).move_to([x,0,0]),label(title,x,.85,col,21),label(value,x,0,INK,27),label(metric,x,-.8,MUTED,24)))
        self.cue(1);self.cue(2,FadeIn(cards[0]));self.cue(3);self.cue(4);self.cue(5)
        self.cue(6,Indicate(cards[0]));self.cue(7,FadeIn(cards[1]),FadeIn(cards[2]));self.cue(8,Indicate(cards[1]));self.cue(9)
        self.cue(10,Indicate(cards[2]));self.cue(11,FadeIn(self.note('長期・時点・方向を分ける → 何を測るかを先に選ぶ'.replace('長期・時点・方向','장기 · 시점 · 방향'))))

    def scene11(self):
        cards=VGroup()
        for i,(s,col) in enumerate([('전체와 국소',CYAN),('방향별 증폭',GOLD),('제한적인 모드',PINK),('실제로 택한 경로',GREEN),('일시적 증폭',GOLD)]):
            x=(i-2)*2.6;cards.add(VGroup(RoundedRectangle(width=2.4,height=1.4,color=col,corner_radius=.12).move_to([x,.3,0]),label(s,x,.3,col,23)))
        self.cue(1);self.cue(2,FadeIn(cards[0]));self.cue(3,FadeIn(cards[1]));self.cue(4,FadeIn(cards[2]),FadeIn(cards[3]));self.cue(5,FadeIn(cards[4]));self.cue(6)
        self.cue(7,FadeIn(label('안정성은 정확히 무엇을 측정하는가?',0,-1.35,INK,33)))
        self.cue(8,FadeIn(self.note('11막 — 다시 유체로 돌아가 질문을 정리한다')))
