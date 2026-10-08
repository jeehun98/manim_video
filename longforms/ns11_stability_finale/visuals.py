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
        record=records[self.index-1];self.chapter=11
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
        if self.index==9 and n==11 and frames>round(1.5*config.frame_rate):
            fade_frames=round(1.5*config.frame_rate)
            self.wait((frames-fade_frames)/config.frame_rate)
            self.play(FadeOut(self.caption),FadeOut(self.progress),run_time=fade_frames/config.frame_rate)
        elif frames:self.wait(frames/config.frame_rate)
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

    def heatmap(self,center=(3,0,0)):
        c=np.array(center);g=VGroup()
        for i in range(8):
            for j in range(8):
                col=GOLD if j==5 and i==3 else '#265D70'
                g.add(Square(side_length=.28,color=col,fill_color=col,fill_opacity=.8,stroke_width=.5).move_to(c+[(j-3.5)*.32,(3.5-i)*.32,0]))
        return g

    def scene1(self):
        f=field(center=(0,0,0));self.cue(1,FadeIn(f));self.cue(2,Rotate(f,angle=.25))
        smooth=field(center=(0,0,0));self.cue(3,Transform(f,smooth),FadeIn(label('운반 · 변형    /    확산 · 완화',0,2,CYAN,29)))
        tube=self.vortex(center=(0,0,0));self.cue(4,FadeOut(f),FadeIn(tube));self.cue(5,Transform(tube,self.vortex(stretch=2,center=(0,0,0))))
        self.cue(6,FadeOut(tube),FadeIn(field(center=(0,0,0))),FadeIn(self.note('다시 처음의 질문: 매끄러움은 언제까지 유지되는가?')))

    def scene2(self):
        fluid=field(center=(-3.3,0,0),peak=True);matrix=self.heatmap();headers=VGroup(label('유체의 속도장',-3.3,1.95,CYAN,27),label('신경망의 활성값',3,1.95,GOLD,27))
        self.cue(1,FadeIn(headers));self.cue(2,FadeIn(fluid),FadeIn(label('전체 운동에너지',-3.3,-1.9,MUTED,23)))
        self.cue(3,FadeIn(label('전체의 합  ≠  가장 빠른 곳',-3.3,1.5,CYAN,22)))
        self.cue(4,Indicate(fluid));self.cue(5,FadeIn(matrix));self.cue(6,FadeIn(label('평균 |a| ≈ 0.62   /   max |a| = 8',3,-1.9,GOLD,21)))
        self.cue(7,Indicate(matrix));self.cue(8,FadeIn(self.note('전체 요약 ≠ 국소 극단값 · 유한 행렬의 이상치와 유체 특이점은 다르다')))

    def scene3(self):
        theta=ValueTracker(0);c1=np.array([-3.5,0,0]);c2=np.array([3.5,0,0]);v=lambda:np.array([np.cos(theta.get_value()),np.sin(theta.get_value())])
        def fluid_vectors():
            w=v();S=np.diag([.7,-.7]);return VGroup(self.state(c1,w,.9,CYAN),Arrow(c1+np.r_[w*.9,0],c1+np.r_[w*.9+S@w*.65,0],buff=0,color=GOLD,stroke_width=4))
        def nn_vectors():return VGroup(self.state(c2,v(),.7,GREEN),self.state(c2,np.diag([1.8,.5])@v(),.7,GOLD))
        self.add(label('보티시티 + 변형률',-3.5,1.9,CYAN,26),label('입력 변화 + Jacobian',3.5,1.9,GREEN,26))
        self.cue(1);self.cue(2,FadeIn(always_redraw(fluid_vectors)));self.cue(3,FadeIn(label('Sω: 강도의 증감에 관여',-3.5,-1.65,CYAN,24)))
        self.cue(4,FadeIn(Circle(radius=.7,color=GREEN).move_to(c2)),FadeIn(Ellipse(width=2.52,height=.7,color=GOLD).move_to(c2)),FadeIn(always_redraw(nn_vectors)))
        self.cue(5,theta.animate.set_value(PI/2),seconds=4);self.cue(6,theta.animate.set_value(PI),seconds=3)
        self.cue(7,FadeIn(label('같은 크기라도, 방향에 따라 다르게 작용',0,2.45,INK,24)))
        self.cue(8,FadeIn(self.note('유체의 시간 변화 항과 신경망의 국소 입력 반응은 서로 다른 양')))

    def scene4(self):
        grid=self.mesh(spacing=.7,center=(-3,0,0),width=4.2,height=2.8);small=self.mesh(spacing=.175,center=(-3,0,0),width=1.4,height=1.4,color=GOLD)
        contours=self.contours(center=(3,0,0),ratio=3.4)
        self.cue(1,FadeIn(label('전체 업데이트를 제한하는 조건',0,2.3,INK,29)));self.cue(2,FadeIn(grid),FadeIn(small),FadeIn(label('명시적 확산',-3,1.9,CYAN,25)))
        self.cue(3,FadeIn(contours),FadeIn(label('경사하강법 · 이차 손실',3,2,GREEN,25)));self.cue(4,FadeIn(label('작은 Δx → 작은 Δt',-3,-1.9,GOLD,26)),FadeIn(label('큰 곡률 → 작은 학습률',3,-1.9,GOLD,26)))
        self.cue(5,Indicate(small),Indicate(contours));self.cue(6,FadeIn(self.note('계산 방법의 안정성 조건 · 유체의 물리적 특이점과 구별')))

    def scene5(self):
        f=field(center=(-3.5,0,0));self.cue(1,FadeIn(label('가능한 상태  ≠  실제로 실현된 상태',0,2.4,GOLD,28)))
        self.cue(2,FadeIn(f));self.cue(3,FadeIn(label('운동 법칙 · 초기 조건 · 외력',-3.5,-1.9,CYAN,22)))
        plane=self.mesh(spacing=.6,center=(3,0,0),width=4.2,height=2.8,color=GREEN);self.cue(4,FadeIn(plane))
        # Two gradient descent trajectories in a double-well potential.
        def path(x0):
            p=np.array(x0,dtype=float);points=[]
            for _ in range(160):
                points.append(np.array([3+p[0],p[1],0]));p-=.04*np.array([4*p[0]*(p[0]**2-1),2*p[1]])
            g=VMobject(stroke_color=GOLD if x0[0]>0 else PINK,fill_opacity=0);g.set_points_as_corners(points);return g
        a=path([.3,1.2]);b=path([-.3,1.2]);self.cue(5,Create(a));self.cue(6,Create(b),FadeIn(Dot([4,0,0],color=GOLD)),FadeIn(Dot([2,0,0],color=PINK)))
        self.cue(7,FadeIn(self.note('유体 후보의 조건 검증 / 학습 동역학의 해 선택'.replace('유体','유체'))))

    def scene6(self):
        t=ValueTracker(0);c=np.array([-4.6,-.7,0]);p=lambda z:c+np.r_[self.propagator(z)@[0,1],0]
        state=always_redraw(lambda:self.state(c,self.propagator(t.get_value())@[0,1]));self.add(self.axes2(c),state)
        o=np.array([1,-1.5,0]);graph=self.curve(lambda z:o+np.array([.75*z,.72*np.linalg.norm(self.propagator(z)@[0,1]),0]),end=6)
        axes=VGroup(Arrow(o,o+[4.8,0,0],color=MUTED,buff=0),Arrow(o,o+[0,3,0],color=MUTED,buff=0),label('時間'.replace('時間','시간'),5.7,-1.9,MUTED,18))
        self.cue(1);self.cue(2,t.animate.set_value(1),Create(self.curve(p,end=1)),seconds=4)
        self.cue(3,FadeIn(label('A = [−1, 10; 0, −1]',-3,2,CYAN,27)))
        self.cue(4,FadeIn(axes),Create(graph));self.cue(5,t.animate.set_value(6),Create(self.curve(p,start=1,end=6)),seconds=4)
        self.cue(6,FadeIn(label('고유값: 장기 감쇠   /   특잇값: 시간별 최대 증폭',0,2.45,GOLD,24)),FadeIn(self.note('결국 감소해도, 그 사이에는 커질 수 있다')))

    def question_cards(self):
        g=VGroup()
        for x,y,title,q,col in [(-4,1,'Global','전체가 유계인가?',CYAN),(0,1,'Local','극단값도 제한되는가?',GOLD),(4,1,'Directional','어떤 방향이 증폭되는가?',PINK),(-2,-1,'Temporal','어느 시간 동안인가?',GREEN),(2,-1,'Dynamical','어떤 법칙과 경로인가?',CYAN)]:
            g.add(VGroup(RoundedRectangle(width=3.65,height=1.5,corner_radius=.12,color=col).move_to([x,y,0]),label(title,x,y+.35,col,25),label(q,x,y-.35,INK,20)))
        return g

    def scene7(self):
        word=label('STABILITY?',0,0,INK,55);cards=self.question_cards();self.cue(1,FadeIn(word));self.cue(2)
        self.cue(3,FadeOut(word),FadeIn(cards[0]));self.cue(4,FadeIn(cards[1]));self.cue(5,FadeIn(cards[2]));self.cue(6,FadeIn(cards[3]));self.cue(7,FadeIn(cards[4]))
        self.cue(8,FadeIn(self.note('서로 다른 수학적 질문 · 하나의 조건이 나머지 전부를 보장하지 않는다')));self.cue(9)

    def scene8(self):
        self.add(label('NAVIER–STOKES',-4.4,2.2,CYAN,28),label('NEURAL NETWORK',4.4,2.2,GOLD,28))
        left=['전체 에너지','소용돌이의 변형','명시적 시간 간격','유효한 PDE 해','전단의 과도 증폭'];right=['활성값 요약','Jacobian의 작용','학습률 제한','학습이 선택한 해','RNN의 과도 증폭'];mid=['전체와 국소','크기와 방향','제한적인 모드','법칙과 경로','장기와 중간']
        rows=VGroup()
        for i in range(5):
            y=1.25-i*.7;rows.add(VGroup(label(left[i],-4.4,y,CYAN,23),Line([-2.7,y,0],[-1.1,y,0],color=MUTED),label(mid[i],0,y,INK,21),Line([1.1,y,0],[2.7,y,0],color=MUTED),label(right[i],4.4,y,GOLD,23)))
        self.cue(1);self.cue(2);self.cue(3);self.cue(4,FadeIn(rows[0]));self.cue(5,Indicate(rows[0]))
        self.cue(6,FadeIn(rows[1]));self.cue(7,FadeIn(rows[2]));self.cue(8,FadeIn(rows[3]),FadeIn(rows[4]));self.cue(9,FadeIn(self.note('같은 질문과 도구를 공유해도, 서로 같은 현상은 아니다')))

    def scene9(self):
        f=field(center=(0,0,0));self.cue(1,FadeIn(f));matrix=self.heatmap(center=(0,0,0));self.cue(2,FadeOut(f),FadeIn(matrix))
        self.cue(3,FadeIn(label('공통 구조  ≠  동일한 시스템',0,2.1,INK,31)));self.cue(4)
        self.cue(5,FadeIn(label('전체와 국소',0,-1.9,CYAN,29)))
        geometry=VGroup(Circle(radius=1,color=GREEN).move_to([-2,0,0]),Arrow([-.7,0,0],[.7,0,0],color=MUTED),Ellipse(width=3.6,height=1,color=GOLD).move_to([2.8,0,0]))
        self.cue(6,FadeOut(matrix),FadeIn(geometry));terrain=self.contours(center=(0,0,0),ratio=3.4)
        self.cue(7,FadeOut(geometry),FadeIn(terrain));self.cue(8)
        question=label('무엇이, 어디서, 어떤 방향으로, 언제까지 안정적인가?',0,0,INK,33)
        body=Group(*[m for m in self.mobjects if m is not self.caption and m is not self.progress])
        self.cue(9,FadeOut(body));self.cue(10,FadeIn(question),seconds=3);self.cue(11,FadeOut(question),seconds=3)
