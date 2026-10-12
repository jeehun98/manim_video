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
        record=records[self.index-1];self.chapter=3 if len(records)==5 else 4
        self.timing=json.loads((ROOT/record['directory']/'timing.json').read_text(encoding='utf-8'))
        spec=(ROOT/record['directory']/'spec.md').read_text(encoding='utf-8').splitlines()[0]
        title=spec.split(' — ',1)[1]
        self.add(label('NAVIER–STOKES × NEURAL NETWORKS',-3.7,3.65,MUTED,15),label(f'{self.chapter:02}막  /  {self.index:02} — '+title,0,3.15,INK,29))
        self.add(Line([-6.2,-2.85,0],[6.2,-2.85,0],color='#294958'))
        self.caption=VGroup();self.progress=Line([-6.2,-3.8,0],[-6.19,-3.8,0],color=CYAN,stroke_width=3);self.add(self.progress)
        getattr(self,f'chapter{self.chapter}_{self.index}')()
        frames=round(self.timing['duration']*config.frame_rate)-round(self.time*config.frame_rate)
        if frames<0:raise ValueError('Scene overrun')
        if frames:self.wait(frames/config.frame_rate)

    def cue(self,n,*animations,seconds=3):
        self.remove(self.caption);s=self.timing['lines'][n-1]
        for a,b in [('이천이십육 년 구월 팔일','2026년 9월 8일'),('오픈에이아이','OpenAI'),('구월 십일','9월 11일'),('나비에 스토크스','Navier–Stokes'),('엘투 노름','L₂ 노름')]:s=s.replace(a,b)
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

    def note(self,s):return label(s,0,-2.45,MUTED,20)

    def gauge(self,x=3,y=.2):
        outline=RoundedRectangle(width=3.4,height=.45,corner_radius=.08,stroke_color=GREEN)
        fill=Rectangle(width=2.2,height=.33,stroke_width=0,fill_color=GREEN,fill_opacity=.65).align_to(outline,LEFT).shift(RIGHT*.08)
        return VGroup(outline,fill).move_to([x,y,0])

    def chapter3_1(self):
        f=field();self.add(label('전체 에너지는 유한',3,1.3,GREEN,29),label('가장 빠른 곳도 제한될까?',3,.35,GOLD,25))
        self.cue(1)
        self.cue(2,FadeIn(f))
        gauge=self.gauge(y=-.3);dots=VGroup(*[Dot([-2+x*.6,y*.5,0],radius=.05,color=CYAN) for x in range(-2,3) for y in range(-2,3)])
        self.add(dots)
        self.cue(3,*[d.animate.move_to([3,-.3,0]).set_opacity(0) for d in dots],FadeIn(gauge),seconds=4)
        self.cue(4,Transform(f,field(peak=True)),FadeIn(label('합친 값과, 가장 긴 화살표',3,-1.25,INK,24)))

    def setup_volume(self,u,v,coupled):
        volume=lambda:1/u.get_value()**2 if coupled[0] else v.get_value()
        box=always_redraw(lambda:cube(2.1*volume()**(1/3),center=(-2.8,0,0)))
        arrow=always_redraw(lambda:Arrow([-2.8,0,0],[-2.8+u.get_value()*.22,0,0],buff=0,color=GOLD,stroke_width=5,max_tip_length_to_length_ratio=.3))
        nums=VGroup()
        for y,title,color,fn,places in [(1.25,'속도',GOLD,u.get_value,1),(.4,'영역 부피',CYAN,volume,4),(-.45,'에너지 기여',GREEN,lambda:u.get_value()**2*volume(),2)]:
            number=DecimalNumber(fn(),num_decimal_places=places,mob_class=Text,font_size=32,color=color).move_to([4.5,y,0])
            number.add_updater(lambda m,fn=fn:m.set_value(fn()))
            nums.add(label(title,2.45,y,color,27),number)
        self.add(box,arrow,nums,label('단순 모형 · 상대값',0,2.25,MUTED,22))
        return box,arrow,nums

    def chapter3_2(self):
        u=ValueTracker(1);v=ValueTracker(1);coupled=[False]
        items=self.setup_volume(u,v,coupled)
        self.cue(1)
        self.cue(2,u.animate.set_value(2),seconds=4)
        self.cue(3,v.animate.set_value(.25),seconds=4)
        self.cue(4,FadeIn(label('속도 2배 · 부피 ¼ → 같은 기여',0,-1.75,GREEN,28)))
        for item in items:item.clear_updaters(recursive=True)

    def chapter3_3(self):
        u=ValueTracker(2);v=ValueTracker(.25);coupled=[True]
        items=self.setup_volume(u,v,coupled)
        self.cue(1,u.animate.set_value(8),seconds=5)
        self.cue(2,u.animate.set_value(16),seconds=5)
        self.cue(3,FadeIn(label('물 덩어리의 압축이 아닌, 빠른 영역의 축소',0,-1.7,INK,25)))
        self.cue(4,FadeIn(self.note('실제 유체의 해가 아닌, 에너지 집중을 설명하는 모형')))
        for item in items:item.clear_updaters(recursive=True)

    def chapter3_4(self):
        left=field().scale(.65).move_to([-3,0,0]);right=left.copy().move_to([3,0,0])
        self.add(left,right,label('모두 합하기',-3,1.9,GREEN,30),label('가장 큰 것 찾기',3,1.9,GOLD,30))
        self.cue(1)
        g=self.gauge(-3,-1.6);peak=Arrow([2.2,-1.6,0],[4.1,-1.6,0],buff=0,color=GOLD,stroke_width=6)
        self.cue(2,FadeIn(g),FadeIn(peak))
        self.cue(3,FadeIn(label('전체에 걸친 크기',-3,-2.2,GREEN,23)),FadeIn(label('국소적인 극단',3,-2.2,GOLD,23)))
        line=Line([-4.8,2.35,0],[4.8,2.35,0],color=MUTED);dot=Dot([-4.8,2.35,0],color=PINK)
        self.add(line,dot,label('T',5.2,2.35,PINK,23))
        self.cue(4,dot.animate.move_to([4.65,2.35,0]),peak.animate.put_start_and_end_on([1.4,-1.6,0],[5.4,-1.6,0]),seconds=5)

    def rules(self):
        return VGroup(*[label(s,3.2,y,c,27) for s,y,c in [('이동',1.4,CYAN),('압력',.5,PINK),('점성에 의한 퍼짐',-.4,GREEN),('외부의 힘',-1.3,GOLD)]])

    def chapter3_5(self):
        picture=VGroup(cube(.65,(-2.5,0,0)),Arrow([-2.5,0,0],[-.4,0,0],buff=0,color=GOLD,stroke_width=5))
        self.add(picture);self.cue(1)
        self.cue(2,FadeIn(label('그릴 수 있는 모양',-2.5,1.6,CYAN,27)))
        rules=self.rules();self.cue(3,FadeIn(rules))
        self.cue(4,FadeIn(label('다음 막：운동 법칙을 따르는 흐름을 만들 수 있을까?',0,-2.25,INK,26)))

    def chapter4_1(self):
        c=cube(.7,(-3,0,0));arrow=Arrow([-3,0,0],[-.8,0,0],buff=0,color=GOLD,stroke_width=5)
        self.add(c,arrow,label('설계한 모양',-3,1.7,CYAN,29));self.cue(1)
        gate=RoundedRectangle(width=4,height=3.7,corner_radius=.15,stroke_color=MUTED).move_to([3,0,0])
        self.cue(2,FadeIn(gate),FadeIn(label('실제 움직임의 조건',3,2.2,INK,25)))
        self.cue(3,FadeIn(self.rules()))
        self.cue(4,FadeIn(self.note('모양의 가능성 → 운동 법칙을 만족하는 흐름')))

    def chapter4_2(self):
        force=label('가하는 힘',-3,1.3,GREEN,32);flow=label('생기는 흐름',3,1.3,CYAN,32)
        arrow=Arrow([-1.4,.2,0],[1.4,.2,0],buff=0,color=INK,stroke_width=4)
        self.add(force,flow,arrow);self.cue(1)
        self.cue(2,Transform(arrow,Arrow([1.4,.2,0],[-1.4,.2,0],buff=0,color=GOLD,stroke_width=4)),FadeTransform(flow,label('원하는 흐름',3,1.3,GOLD,32)))
        self.cue(3,FadeTransform(force,label('필요한 힘',-3,1.3,GREEN,32)),FadeIn(label('흐름에서 힘으로, 거꾸로 따져보기',0,-1.2,INK,28)))
        self.cue(4,FadeIn(self.note('역으로 계산하는 관점 · 정밀한 구성 전체를 대신하지는 않는다')))

    def chapter4_3(self):
        bad=VGroup(label('속도 ↑',-3,1.5,GOLD,29),label('외력도 특이해짐',-3,.65,PINK,27))
        good=VGroup(label('속도 ↑',3,1.5,GOLD,29),label('외력은 매끄러움',3,.65,GREEN,27))
        self.add(bad);self.cue(1)
        self.cue(2,FadeIn(label('찾는 조건을 만족하지 못함',-3,-1.5,PINK,22)))
        smooth=ParametricFunction(lambda t:np.array([t,.15*np.sin(2*t)-.35,0]),t_range=[1.3,4.7,.03],color=GREEN,fill_opacity=0)
        jagged=VMobject(stroke_color=PINK,fill_opacity=0).set_points_as_corners([[-4.7+i*.34,-.35+(.45 if i%2 else -.45),0] for i in range(11)])
        self.cue(3,Create(jagged),FadeIn(good),Create(smooth),FadeIn(label('연구가 목표로 한 조건',3,-1.5,GREEN,22)))
        self.cue(4,FadeIn(self.note('크기가 작은 것과 매끄러운 것은 다른 조건 · 비교 개념도')))

    def chapter4_4(self):
        grid=VGroup(*[Dot([-2.5+x*.4,y*.35,0],radius=.025,color=CYAN) for x in range(-4,5) for y in range(-4,5)])
        self.add(label('OpenAI 공개 논문 · 2026.09.08',0,2.3,MUTED,23))
        self.cue(1)
        self.cue(2,FadeIn(grid),FadeIn(label('정지한 초기 상태',3,1.4,CYAN,28)),FadeIn(label('매끄러운 외력',3,.65,GREEN,28)))
        r=ValueTracker(1);h=ValueTracker(2.7);phase=ValueTracker(0)
        shape=always_redraw(lambda:core(r.get_value(),h.get_value(),phase.get_value(),(-2.5,0,0)))
        self.cue(3,FadeOut(grid),FadeIn(shape),phase.animate.set_value(PI),seconds=5)
        self.cue(4,r.animate.set_value(.25),h.animate.set_value(1.35),FadeIn(label('반지름 ↓   높이 ↓',3,-.2,CYAN,25)),seconds=5)
        self.cue(5,FadeIn(label('최대 속도 ↑',3,-1,GOLD,29)),FadeIn(label('전체 에너지：유계',3,-1.75,GREEN,27)),FadeIn(self.note('원문 §2의 기하학 개념도 · 실제 해를 계산한 영상 아님')))
        shape.clear_updaters()

    def chapter4_5(self):
        positive=Arrow([-4.6,.8,0],[-.7,.8,0],buff=0,color=CYAN,stroke_width=8)
        negative=Arrow([-.7,-.3,0],[-4.1,-.3,0],buff=0,color=PINK,stroke_width=8)
        self.add(label('운동 법칙 안의 여러 효과',0,2.2,MUTED,24));self.cue(1,FadeIn(positive))
        self.cue(2,FadeIn(negative),FadeIn(label('반대 방향으로 작용',-2.7,-1.5,INK,25)))
        resultant=Arrow([2.6,.2,0],[3.1,.2,0],buff=0,color=GREEN,stroke_width=6,max_tip_length_to_length_ratio=.3)
        self.cue(3,FadeIn(resultant),FadeIn(label('합쳐진 결과',3,1.25,GREEN,27)),positive.animate.shift(DOWN*.55),negative.animate.shift(UP*.55),seconds=4)
        self.cue(4,FadeIn(label('정밀한 상쇄 → 매끄러운 외력',0,-1.95,GREEN,27)),FadeIn(self.note('상쇄 원리의 비유 · 실제 항의 수치나 증명을 재현한 것은 아님')))

    def chapter4_6(self):
        tiles=VGroup(*[Square(side_length=.44,stroke_color='#294958',stroke_width=1,fill_color=CYAN,fill_opacity=.12).move_to([-3.8+j*.5,1.1-i*.5,0]) for i in range(5) for j in range(7)])
        self.add(tiles,label('시간 →',-2.3,1.9,MUTED,23),label('공간의 여러 위치',-2.3,-1.65,MUTED,22))
        errors=[tiles[i] for i in [2,13,19,30]]
        self.cue(1,errors[0].animate.set_fill(PINK,.9))
        self.cue(2,*[t.animate.set_fill(PINK,.9) for t in errors[1:]],FadeIn(label('모든 위치 · 전체 시간',3,1.2,INK,26)))
        self.cue(3,errors[0].animate.set_fill(GREEN,.5),errors[1].animate.set_fill(GREEN,.5),tiles[10].animate.set_fill(PINK,.9),FadeIn(label('수정하면 다른 오차도 변한다',3,.25,PINK,24)))
        conditions=VGroup(label('원하는 흐름',3,-.65,GOLD,25),label('매끄러운 외력',3,-1.25,GREEN,25),label('운동 법칙의 성립',3,-1.85,CYAN,25))
        self.cue(4,*[t.animate.set_fill(GREEN,.2) for t in tiles],FadeIn(conditions),FadeIn(self.note('조건을 동시에 맞추는 어려움의 개념도 · 실제 보정 알고리즘 아님')))

    def chapter4_7(self):
        cards=VGroup(*[label(s,x,y,c,26) for s,x,y,c in [('정지한 초기 상태',-3,1.5,CYAN),('특별히 구성한 매끄러운 외력',3,1.5,GREEN),('유계인 전체 에너지',-3,.55,GREEN),('유한시간에 발산하는 속도',3,.55,GOLD)]])
        self.add(cards,label('논문이 제시한 결과',0,2.3,MUTED,23));self.cue(1)
        self.cue(2,FadeIn(label('무외력 유체 전체에 대한 주장이 아님',0,-.45,PINK,25)))
        self.cue(3,FadeIn(label('Clay · 2026.09.11 평가 절차 안내',0,-1.2,MUTED,23)))
        self.cue(4,FadeOut(cards),FadeIn(label('전체의 크기  /  가장 극단적인 부분',0,1.4,GREEN,30)),FadeIn(label('가능한 모양  /  운동 법칙을 따르는 움직임',0,.5,CYAN,28)))
        self.cue(5,FadeIn(label('다음 막：신경망의 표현과 증폭',0,-2.1,INK,28)))

