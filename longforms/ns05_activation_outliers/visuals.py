"""Energy concentration: illustrative models, not a numerical PDE solution."""
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
        record=records[self.index-1];self.chapter=5
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

    def heat(self,values=None,center=(-2.7,.1,0)):
        values=np.full((8,8),.5) if values is None else np.array(values)
        g=VGroup()
        for i in range(8):
            for j in range(8):
                val=abs(values[i,j]);color=GOLD if val>2 else CYAN
                g.add(Square(side_length=.34,stroke_color='#294958',stroke_width=1,fill_color=color,fill_opacity=min(.12+.1*val,1)).move_to(np.array(center)+[(j-3.5)*.39,(3.5-i)*.39,0]))
        return g

    def gauge(self,x=3,y=.1):
        outline=RoundedRectangle(width=3.2,height=.4,corner_radius=.08,stroke_color=GREEN)
        fill=Rectangle(width=2.05,height=.28,stroke_width=0,fill_color=GREEN,fill_opacity=.65).align_to(outline,LEFT).shift(RIGHT*.08)
        return VGroup(outline,fill).move_to([x,y,0])

    def scene1(self):
        f=field();self.add(f,label('흐름의 변형',3,1.35,CYAN,29),label('점성에 의한 퍼짐',3,.5,GREEN,29))
        self.cue(1)
        self.cue(2,Transform(f,field(peak=True)),seconds=4)
        gauge=self.gauge(y=-.4)
        self.cue(3,FadeIn(gauge),FadeIn(label('전체 에너지',3,-1.05,GREEN,27)))
        maximum=Arrow([1.9,-1.7,0],[4.1,-1.7,0],buff=0,color=GOLD,stroke_width=5)
        self.cue(4,FadeIn(maximum))
        self.cue(5,FadeIn(self.note('합친 값과 가장 빠른 곳의 속도는 다른 정보')))

    def scene2(self):
        u=ValueTracker(1)
        box=always_redraw(lambda:cube(2.2*u.get_value()**(-2/3),center=(-2.7,.1,0)))
        arrow=always_redraw(lambda:Arrow([-2.7,.1,0],[-2.7+.25*u.get_value(),.1,0],buff=0,color=GOLD,stroke_width=4))
        gauge=self.gauge(y=.2)
        region=label('작아지는 빠른 영역',-2.7,1.9,CYAN,25);energy=label('에너지 기여는 일정',3,1.1,GREEN,27)
        self.add(box,arrow,gauge,region,energy)
        self.cue(1,u.animate.set_value(8),seconds=5)
        region_note=self.note('같은 물 조각의 압축이 아닌, 강한 흐름의 영역 축소')
        self.cue(2,FadeIn(region_note))
        rules=label('실제 흐름에는 운동 법칙도 필요',3,-.9,INK,24)
        self.cue(3,FadeIn(rules))
        matrix=self.heat(center=(-2.7,.1,0));vals=label('신경망：유한한 개수의 활성값',3,1.1,CYAN,25)
        self.cue(4,FadeOut(box),FadeOut(arrow),FadeOut(gauge),FadeOut(rules),FadeOut(region),FadeOut(energy),FadeOut(region_note),FadeIn(matrix),FadeIn(vals))
        box.clear_updaters();arrow.clear_updaters()
        self.cue(5,FadeIn(label('활성값 이상치 ≠ 유체의 특이점',3,-.4,PINK,26)))
        self.cue(6,FadeIn(label('공통 관점：전체 요약 + 국소적인 극단',0,-1.9,INK,27)))

    def scene3(self):
        f=field(center=(-2.7,.1,0));cells=self.heat()
        self.add(f);self.cue(1)
        self.cue(2,ReplacementTransform(f,cells),seconds=4)
        axes=VGroup(label('특징 차원 →',-2.7,2.05,CYAN,24),label('토큰',-4.8,.1,CYAN,24),label('행 = 토큰',3,1.4,INK,29),label('열 = 특징 차원',3,.55,INK,29))
        self.cue(3,FadeIn(axes))
        enlarged=Square(side_length=1,stroke_color=GOLD,fill_color=CYAN,fill_opacity=.2).move_to([3,-.65,0])
        self.cue(4,Indicate(cells[21],color=GOLD),FadeIn(enlarged),FadeIn(label('0.5',3,-.65,GOLD,36)))
        self.cue(5,FadeIn(self.note('한 칸 = 특정 토큰·차원의 활성값 · 설명용 행렬')))

    def scene4(self):
        cells=self.heat();self.add(cells,label('대부분：작은 값',3,1.2,CYAN,29));self.cue(1)
        self.cue(2,cells[29].animate.set_fill(GOLD,.95),FadeIn(label('일부：훨씬 큰 값',3,.2,GOLD,29)))
        column=[cells[i*8+5] for i in [0,1,2,4,6,7]]
        self.cue(3,*[cell.animate.set_fill(GOLD,.75) for cell in column],FadeIn(label('같은 특징 차원에 집중',3,-.9,INK,25)))
        self.cue(4,FadeIn(self.note('LLM.int8() · NeurIPS 2022 · 일부 모델의 관찰을 참고한 개념도')))
        self.cue(5,FadeIn(label('이상치의 존재만으로 계산 오류가 되는 것은 아님',0,2.35,MUTED,22)))

    def scene5(self):
        values=np.full((8,8),.5);values[3,5]=8
        cells=self.heat(values);self.add(cells)
        self.cue(1)
        self.cue(2,FadeIn(label('63개：0.5    1개：8',3,1.45,INK,28)))
        self.cue(3,FadeIn(label('평균 절댓값 ≈ 0.617',3,.45,GREEN,29)),FadeIn(label('최대 절댓값 = 8',3,-.4,GOLD,29)))
        self.cue(4,Indicate(cells[29],color=GOLD),FadeIn(label('그 값은 어디에 있고, 어떻게 쓰일까?',0,2.35,MUTED,23)))
        self.cue(5,FadeIn(label('최대값 8 ≤ L₂ 노름 ≈ 8.93',3,-1.5,INK,23)),FadeIn(self.note('유한 행렬의 이상치 · 연속 유체의 무한대 폭주와 구별')))

    def ruler(self,maximum=1):
        g=VGroup(Line([-5,0,0],[5,0,0],color=MUTED))
        step=maximum/127
        for k in range(-int(1/step),int(1/step)+1):
            x=k*step
            g.add(Line([5*x,-.11,0],[5*x,.11,0],color=CYAN,stroke_width=1))
        g.add(label('−1',-5,-.45,MUTED,22),label('0',0,-.45,MUTED,22),label('1',5,-.45,MUTED,22))
        return g

    def scene6(self):
        self.add(label('실수 → 가까운 정수 눈금',0,2.25,INK,28));self.cue(1)
        baseline=Line([-5,0,0],[5,0,0],color=MUTED)
        points=VGroup(*[Dot([5*x,.28,0],color=GOLD,radius=.055) for x in [.1,.2,.4,.8]])
        self.cue(2,Create(baseline),FadeIn(points))
        ruler=self.ruler()
        self.cue(3,FadeIn(ruler),*[dot.animate.move_to([5*round(x*127)/127,0,0]) for dot,x in zip(points,[.1,.2,.4,.8])])
        self.cue(4,FadeIn(label('같은 묶음은 같은 눈금 간격을 공유',0,-1.35,GREEN,27)))
        overview=VGroup(Line([-4.8,1.35,0],[4.8,1.35,0],color=MUTED),Dot([-4.7,1.35,0],color=CYAN),Dot([4.8,1.35,0],color=PINK),label('작은 값들',-4,1.85,CYAN,22),label('큰 값 100',4.3,1.85,PINK,24))
        self.cue(5,FadeIn(overview),FadeIn(self.note('대칭 INT8 −127…127 · 같은 양자화 그룹의 예시')))

    def scene7(self):
        ruler=self.ruler(1);self.add(ruler,label('작은 값 근처만 확대：−1…1',0,2.35,MUTED,22))
        step=label('최대값 1  /  눈금 간격 ≈ 0.0079',0,1.65,CYAN,27)
        self.add(step);self.cue(1)
        new=label('최대값 100  /  눈금 간격 ≈ 0.7874',0,1.65,GOLD,27)
        self.cue(2,Transform(ruler,self.ruler(100)),FadeTransform(step,new),seconds=4)
        dots=VGroup(*[Dot([5*x,.3,0],color=GOLD,radius=.06) for x in [.1,.2,.4,.8]])
        self.add(dots)
        moves=[dot.animate.move_to([5*round(x*127/100)*100/127,.12*(i%2),0]) for i,(dot,x) in enumerate(zip(dots,[.1,.2,.4,.8]))]
        collapse=label('0.1, 0.2 → 0    /    0.4, 0.8 → 0.7874',0,-1.35,GOLD,25)
        self.cue(3,*moves,FadeIn(collapse),seconds=4)
        # A compact, exact reconstruction table is introduced after the collapse.
        table=VGroup(label('원래 값',-3,.75,INK,23),label('최대 1：복원값',0,.75,CYAN,23),label('최대 100：복원값',3,.75,GOLD,23))
        for i,x in enumerate([.1,.2,.4,.8]):
            y=.1-i*.55
            table.add(label(f'{x:.1f}',-3,y,INK,25),label(f'{round(x*127)/127:.3f}',0,y,CYAN,25),label(f'{round(x*127/100)*100/127:.3f}',3,y,GOLD,25))
        self.cue(4,FadeOut(ruler),FadeOut(dots),FadeOut(collapse),FadeIn(table),seconds=4)
        self.cue(5,FadeIn(self.note('같은 그룹의 absmax 스케일 · 묶음과 방식에 따라 영향은 달라짐')))

    def scene8(self):
        cells=self.heat();col=[cells[i*8+5] for i in range(8)]
        for cell in col:cell.set_fill(GOLD,.9)
        self.add(cells,label('이상치 차원',3,1.45,GOLD,29));self.cue(1)
        self.cue(2,Indicate(VGroup(*col),color=PINK),FadeIn(label('제거하면 중요한 기여도 사라질 수 있음',3,.55,PINK,23)))
        self.cue(3,FadeIn(label('LLM.int8() · NeurIPS 2022',0,2.35,MUTED,23)))
        normal=label('일반 차원 → INT8',2.3,-.25,CYAN,28);outlier=label('이상치 차원 → FP16',2.3,-1.05,GOLD,28)
        self.cue(4,FadeIn(normal),FadeIn(outlier))
        self.cue(5,FadeIn(label('두 계산의 기여를 합친다',2.3,-1.95,INK,25)))

    def scene9(self):
        self.add(label('SmoothQuant · ICML 2023',0,2.35,MUTED,23),label('활성값',-3,1.75,CYAN,28),label('가중치',3,1.75,GOLD,28))
        xbar=Rectangle(width=.8,height=1.7,stroke_width=0,fill_color=CYAN,fill_opacity=.65).move_to([-3,.2,0])
        wbar=Rectangle(width=.8,height=.2,stroke_width=0,fill_color=GOLD,fill_opacity=.75).move_to([3,-.55,0])
        self.add(xbar,wbar);self.cue(1)
        before=label('8 × 0.25 = 2',0,-1.2,INK,36)
        self.cue(2,FadeIn(before))
        after=label('1 × 2 = 2',0,-1.2,INK,36)
        self.cue(3,Transform(xbar,Rectangle(width=.8,height=.22,stroke_width=0,fill_color=CYAN,fill_opacity=.65).move_to([-3,-.55,0])),Transform(wbar,Rectangle(width=.8,height=1.6,stroke_width=0,fill_color=GOLD,fill_opacity=.75).move_to([3,.15,0])),FadeTransform(before,after),FadeIn(label('÷8',-1.65,.4,CYAN,29)),FadeIn(label('×8',1.65,.4,GOLD,29)),seconds=5)
        self.cue(4,FadeIn(label('활성값의 부담을 가중치 쪽으로 옮긴다',0,-2.0,GREEN,26)))
        self.cue(5,FadeIn(self.note('한 차원의 보상 예시 · 정확한 산술의 곱은 동일 · 양자화 오차는 달라질 수 있음')))

    def scene10(self):
        cells=self.heat();col=[cells[i*8+5] for i in range(8)]
        for cell in col:cell.set_fill(GOLD,.8)
        summary=label('크기와 표현 정밀도',3,1.2,INK,28);connection=label('연결：전체 요약 + 국소 극단',3,.35,GREEN,26)
        question=label('다음 계산을 통과하면?',0,2.35,INK,28)
        self.add(cells,summary);self.cue(1)
        self.cue(2,FadeIn(connection))
        self.cue(3,FadeOut(cells),FadeOut(summary),FadeOut(connection),FadeIn(question))
        origins=[[-3,-.2,0],[3,-.2,0]]
        a=Arrow(origins[0],[-2,-.2,0],buff=0,color=CYAN,stroke_width=5)
        b=Arrow(origins[1],[3,.8,0],buff=0,color=GOLD,stroke_width=5)
        self.add(a,b,label('입력 길이 1',-3,-1.2,CYAN,25),label('입력 길이 1',3,-1.2,GOLD,25))
        self.cue(4,a.animate.put_start_and_end_on(origins[0],[-1,-.2,0]),b.animate.put_start_and_end_on(origins[1],[3,.3,0]),FadeIn(label('출력 길이 2',-3,-1.9,CYAN,25)),FadeIn(label('출력 길이 0.5',3,-1.9,GOLD,25)),seconds=4)
        self.cue(5,FadeOut(question),FadeIn(label('다음 막：방향에 따른 증폭',0,1.9,INK,30)),FadeIn(self.note('같은 입력 길이 · 다른 방향 · W = diag(2, 0.5) 설명용 변환')))

