"""The same white point connects rotation, coordinates and complex exponentials."""
import json,os,sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT,INK,MUTED,pill,configure_vertical
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import motion
configure_vertical(frame_rate=60)
config.background_color='#0B1020'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
GREEN='#34D399';BLUE='#60A5FA';PURPLE='#C084FC';YELLOW='#FBBF24'

def text(s,y=0,x=0,size=28,color=INK,width=7.6):
    obj=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.15)
    if obj.width>width:obj.scale_to_fit_width(width)
    return obj.move_to([x,y,0])
def block(s,x=0,y=0,w=2,color=BLUE):return pill(s,color,w).move_to([x,y,0])
def wrap(s,limit=27):
    lines=[];line=''
    for word in s.split():
        if line and len(line)+len(word)+1>limit:lines.append(line);line=word
        else:line=(line+' '+word).strip()
    if line:lines.append(line)
    return '\n'.join(lines)
def exponential(exponent='iθ',size=40,color=YELLOW):
    e=text('e',size=size,color=color)
    sup=text(exponent,size=size*.55,color=PURPLE if exponent=='iθ' else color).next_to(e,UR,buff=.025).shift(LEFT*.06+DOWN*.05)
    return VGroup(e,sup)
def trig(size=34):
    return VGroup(text('cos θ',size=size,color=BLUE),text('+',size=size),text('i',size=size,color=PURPLE),text('sin θ',size=size,color=GREEN)).arrange(RIGHT,buff=.14)
def formula(y=-3.4,size=34):
    return VGroup(exponential(size=size+7),text('=',size=size),trig(size)).arrange(RIGHT,buff=.22).move_to([0,y,0])

class RotatingPoint(VGroup):
    def __init__(self,clock,small=False,projections=True):
        super().__init__();self.clock=clock
        self.r=1.15 if small else 1.85
        self.center=np.array([-2.25,1.65,0]) if small else np.array([0,1,0])
        c=self.center;r=self.r
        self.circle=Circle(radius=r,color=MUTED,stroke_width=2).move_to(c)
        self.axes=VGroup(Line(c+LEFT*(r+.3),c+RIGHT*(r+.3),color=MUTED,stroke_width=1),Line(c+DOWN*(r+.3),c+UP*(r+.3),color=MUTED,stroke_width=1))
        self.radius=Line(c,c+RIGHT*r,color=WHITE,stroke_width=2.3)
        self.vline=Line(c,c+UP*.01,color=GREEN,stroke_width=1.8,stroke_opacity=.6)
        self.hline=Line(c,c+RIGHT*.01,color=BLUE,stroke_width=1.8,stroke_opacity=.6)
        self.yp=Dot(c,radius=.065,color=GREEN);self.xp=Dot(c,radius=.065,color=BLUE)
        self.point=Dot(c+RIGHT*r,radius=.085,color=WHITE).set_z_index(5)
        self.add(self.axes,self.circle,self.radius,self.vline,self.hline,self.yp,self.xp,self.point)
        if not projections:VGroup(self.vline,self.hline,self.yp,self.xp).set_opacity(0)
        self.sync();self.add_updater(lambda obj,dt:obj.sync())
    def sync(self):
        x,y=motion.coordinates(self.clock());c=self.center;r=self.r
        p=c+np.array([r*x,r*y,0]);self.point.move_to(p)
        self.radius.put_start_and_end_on(c,p)
        self.xp.move_to(c+np.array([r*x,0,0]));self.yp.move_to(c+np.array([0,r*y,0]))
        self.vline.put_start_and_end_on(p,self.yp.get_center()+RIGHT*1e-7)
        self.hline.put_start_and_end_on(p,self.xp.get_center()+UP*1e-7)
        return self

class WaveTrace(VGroup):
    def __init__(self,rig,kind='sin'):
        super().__init__();self.rig=rig;self.kind=kind
        self.cy=rig.center[1] if kind=='sin' else -1.55
        self.left=-.2;self.right=3.6;self.color_wave=GREEN if kind=='sin' else BLUE
        self.axis=Line([self.left,self.cy,0],[self.right,self.cy,0],color=MUTED,stroke_width=1)
        self.trace=VMobject(color=self.color_wave,stroke_width=2.6)
        self.dot=Dot(radius=.065,color=self.color_wave)
        self.link=Line(ORIGIN,RIGHT,color=self.color_wave,stroke_width=1.2,stroke_opacity=.35)
        self.label=text('sin θ · 세로 위치' if kind=='sin' else 'cos θ · 가로 위치',self.cy+1.45,1.6,22,self.color_wave,4)
        self.add(self.axis,self.trace,self.dot,self.link,self.label)
        self.sync();self.add_updater(lambda obj,dt:obj.sync())
    def sync(self):
        t=max(10.,self.rig.clock());ts=np.linspace(max(10.,t-10),t+1e-7,101)
        x,y=motion.coordinates(ts);vals=y if self.kind=='sin' else x
        xx=self.right-(t-ts)/10*(self.right-self.left)
        points=np.array([xx,self.cy+self.rig.r*vals,np.zeros_like(xx)]).T
        self.trace.set_points_as_corners(points);self.dot.move_to(points[-1])
        source=self.rig.point.get_center() if self.kind=='sin' else self.rig.xp.get_center()
        self.link.put_start_and_end_on(source,points[-1]);return self


class TimedShot(Scene):
    NUMBER=1

    def refresh(self,target=None):
        t=self.offset+self.time if target is None else target
        idx=next((i for i,s in enumerate(DATA['segments']) if s['start']<=t+1e-5<s['end']),len(DATA['segments'])-1)
        if idx<=self.caption_index:return
        self.caption_index=idx
        c=text(wrap(DATA['segments'][idx]['text']),-6.2,size=25,width=7.5)
        assert c.height<2.15,('caption height',idx,c.height)
        self.caption.become(c)
        self.caption.set_z_index(20)
        self.audit.append(dict(sentence=idx+1,at=round(self.offset+self.time,5)))

    def play(self,*args,**kwargs):
        self.refresh()
        result=super().play(*args,**kwargs)
        self.refresh()
        self.check_bounds()
        return result

    def check_bounds(self):
        for item in self.mobjects:
            if item is self.caption or item is self.chrome:continue
            if not item.has_points() and not item.submobjects:continue
            assert item.get_left()[0]>=-4.15 and item.get_right()[0]<=4.15,('horizontal',self.NUMBER,self.time,item.get_left(),item.get_right())
            assert item.get_bottom()[1]>=-4.8 and item.get_top()[1]<=5.05,('caption or header overlap',self.NUMBER,self.time,item.get_bottom(),item.get_top())

    def to(self,target):
        local=target-self.offset
        if self.time>local+1/60+1e-6:raise ValueError(f'Shot {self.NUMBER}: {self.time+self.offset} > {target}')
        boundaries=[s['start']-self.offset for s in DATA['segments'] if self.time+1e-5<s['start']-self.offset<local-1e-5]+[local]
        for end in boundaries:
            if end-self.time>1e-5:self.wait(end-self.time,frozen_frame=False)
            self.refresh(self.offset+end)

    def at(self,t,*animations,duration=.7):
        self.to(t)
        self.play(*animations,run_time=duration)

    def note(self,s,y=-4.1,color=MUTED,size=23):
        o=text(s,y,size=size,color=color)
        self.play(FadeIn(o),run_time=.4)
        return o

    def construct(self):
        spec=DATA['scenes'][self.NUMBER-1];self.offset=spec['start']
        self.audit=[];self.caption_index=-1;self.caption=VGroup()
        self.chrome=VGroup(text('수학 한 조각  /  EULER',7.35,size=20,color=MUTED),
                 text('원에서 나타나는 파도',6.55,size=34),text(spec['title'],5.62,size=26,color=YELLOW),
                 Line([-3.8,5.13,0],[3.8,5.13,0],color=MUTED,stroke_opacity=.25),
                 Line([-3.8,-4.9,0],[3.8,-4.9,0],color=MUTED,stroke_opacity=.25))
        self.add(self.chrome,self.caption)
        self.refresh()
        getattr(self,f's{self.NUMBER:02}')()
        self.to(spec['end'])
        assert abs(self.time-(spec['end']-spec['start']))<1/60+1e-6
        audit_dir=Path(os.environ.get('EULER_AUDIT',str(HERE.parents[1]/'media/euler01/audit')))
        audit_dir.mkdir(parents=True,exist_ok=True)
        (audit_dir/f'{self.NUMBER:02}.json').write_text(json.dumps(self.audit),encoding='utf-8')

    def rig(self,small=False,projections=True):
        rig=RotatingPoint(lambda:self.offset+self.time,small,projections)
        self.add(rig);return rig

    def s01(self):
        r=self.rig(projections=False)
        self.add(text('같은 속도로, 반시계 방향으로',4.25,size=25,color=MUTED))
        self.to(5)
        self.play(r.vline.animate.set_opacity(.7),r.yp.animate.set_opacity(1),run_time=.6)
        self.at(7,FadeIn(text('높이만 관찰한다면?',-2.4,size=33,color=GREEN)))

    def s02(self):
        r=self.rig(small=True);r.hline.set_opacity(0);r.xp.set_opacity(0)
        sine=WaveTrace(r);self.add(sine)
        self.add(text('원 위의 높이 = 그래프에 기록한 높이',4.4,size=24,color=GREEN),text('시간 →',-.15,1.8,21,MUTED,3))
        self.at(13,FadeIn(text('현재 높이를 시간 순서로 기록',-2.5,size=27,color=GREEN)))
        self.at(18,FadeIn(text('사인파',-3.8,size=37,color=GREEN)),duration=.5)

    def s03(self):
        r=self.rig(small=True);sine=WaveTrace(r);self.add(sine)
        cos=WaveTrace(r,'cos')
        self.play(FadeIn(cos),run_time=.7)
        self.at(20,FadeIn(text('가로 좌표의 값을 그래프 높이로 기록',4.4,size=23,color=BLUE)))
        self.at(22,FadeIn(text('θ = 0일 때:  sin θ = 0,  cos θ = 1',-3.6,size=25,color=YELLOW)))
        self.at(26,FadeIn(text('코사인파',-4.35,size=30,color=BLUE)))

    def s04(self):
        r=self.rig(small=True);self.add(WaveTrace(r),WaveTrace(r,'cos'))
        self.add(text('같은 점 · 같은 시간 · 두 좌표',4.4,size=26,color=MUTED))
        self.at(31,FadeIn(text('세로 위치 → 사인',-3.3,-1.9,25,GREEN,3.6)),FadeIn(text('가로 위치 → 코사인',-3.3,1.9,25,BLUE,3.7)))
        pair=text('(cos θ, sin θ)',-4.3,size=33,color=WHITE)
        self.at(35,FadeIn(pair))

    def s05(self):
        line=NumberLine(x_range=[-2,2,1],length=6.3,include_numbers=False,color=BLUE).move_to([0,.8,0])
        self.add(line,*[text(str(n),.2,line.n2p(n)[0],23,MUTED,1) for n in [-1,0,1]])
        dot=Dot(line.n2p(.8),color=WHITE,radius=.085)
        dot.add_updater(lambda m: m.move_to(line.n2p(motion.coordinates(self.offset+self.time)[0])))
        self.add(dot)
        self.play(FadeIn(text('실수 · 하나의 수직선',3.6,size=29,color=BLUE)),run_time=.6)
        self.at(42,FadeIn(text('한 개의 좌표',-1.5,size=29,color=BLUE)))
        vertical=Line([0,-1.9,0],[0,3.5,0],color=PURPLE,stroke_width=2)
        self.at(46,Create(vertical),FadeIn(text('두 번째 좌표를 위한 축',-3,size=27,color=PURPLE)))

    def s06(self):
        c=np.array([0,.8,0]);scale=1.6
        axis=VGroup(Line([-3.3,.8,0],[3.3,.8,0],color=BLUE),Line([0,-1.9,0],[0,3.5,0],color=PURPLE))
        self.add(axis,text('실수축',.3,2.65,24,BLUE,2),text('허수축',3.9,0,24,PURPLE,2))
        self.add(text('1',.35,1.6,25,BLUE,1),text('−1',.35,-1.6,25,BLUE,1))
        idef=text('i² = −1',-2.55,size=40,color=PURPLE)
        self.play(FadeIn(text('i',2.4,-.35,31,PURPLE,1)),run_time=.6)
        self.at(52,FadeIn(idef))
        p=Dot(c+np.array([1.2*scale,.7*scale,0]),color=WHITE,radius=.09)
        guides=VGroup(DashedLine(c+np.array([1.2*scale,0,0]),p.get_center(),color=GREEN),DashedLine(c+np.array([0,.7*scale,0]),p.get_center(),color=BLUE))
        self.at(55,FadeIn(p),Create(guides),FadeIn(text('a',-.1,1.2*scale,28,BLUE,1)),FadeIn(text('b',.8+.7*scale,-.4,28,GREEN,1)))
        label=VGroup(text('a',size=36,color=BLUE),text('+',size=36),text('b',size=36,color=GREEN),text('i',size=36,color=PURPLE)).arrange(RIGHT,buff=.16).move_to([0,-3.55,0])
        self.at(58,FadeIn(label))
        self.at(62,FadeIn(text('복소평면 · 점 하나를 복소수 하나로',-4.4,size=24,color=INK)))

    def s07(self):
        r=self.rig()
        self.add(text('실수축',.4,2.7,23,BLUE,2),text('허수축',3.7,0,23,PURPLE,2))
        self.play(FadeIn(text('반지름 1인 원',4.4,size=27,color=WHITE)),run_time=.6)
        self.at(66,FadeIn(text('가로: cos θ',-2.1,-1.9,29,BLUE,3.5)),FadeIn(text('세로: sin θ',-2.1,1.9,29,GREEN,3.5)))
        self.at(69,FadeIn(text('θ는 양의 실수축에서 잰 회전 각도',-3.25,size=25,color=MUTED)))
        arc=Arc(radius=.45,start_angle=0,angle=motion.phase(70)%TAU,color=YELLOW).move_arc_center_to(r.center)
        self.at(70,Create(arc),FadeIn(text('θ',1.3,.65,25,YELLOW,1)))
        arc.add_updater(lambda m:m.become(Arc(radius=.45,start_angle=0,angle=max(.001,motion.phase(self.offset+self.time)%TAU),color=YELLOW).move_arc_center_to(r.center)))

    def s08(self):
        r=self.rig();expression=trig(38).move_to([0,-2.4,0])
        self.add(text('가로 좌표',4.3,-1.8,26,BLUE,3),text('세로 좌표',4.3,1.8,26,GREEN,3))
        self.play(TransformFromCopy(r.xp,expression[0]),run_time=.7)
        self.at(74,TransformFromCopy(r.yp,expression[3]))
        self.at(75,FadeIn(expression[1]),FadeIn(expression[2]))
        self.at(78,FadeIn(text('두 좌표를 묶어 나타낸 복소수 하나',-3.7,size=26,color=INK)))

    def s09(self):
        ax=Axes(x_range=[-1.5,1.5,1],y_range=[0,4.5,1],x_length=3.3,y_length=3.8,tips=False,axis_config=dict(color=MUTED,include_ticks=False,stroke_width=1)).move_to([-2,1.5,0])
        curve=ax.plot(lambda x:np.exp(x),x_range=[-1.5,1.45,.04],color=YELLOW,stroke_width=3)
        exp=exponential('x').move_to([-2,4.3,0])
        r=self.rig(small=True);r.clear_updaters()
        # Separate domains: place the complex-plane diagram on the right, never morph the real graph into a circle.
        r.center=np.array([2,1.65,0]);shift=RIGHT*4.25;r.shift(shift);r.sync();r.add_updater(lambda m,dt:m.sync())
        self.add(ax,exp)
        self.play(Create(curve),run_time=.8)
        self.at(83,FadeIn(text('실수 입력 x',-1.2,-2,24,YELLOW,3)))
        marker=Dot(ax.c2p(-1,np.exp(-1)),color=YELLOW)
        self.at(85,FadeIn(marker))
        self.at(86,MoveAlongPath(marker,ax.plot(lambda x:np.exp(x),x_range=[-1,1.1,.04])),duration=1)
        self.at(88,FadeIn(exponential().move_to([2,4.3,0])),FadeIn(text('순허수 입력 iθ',-1.2,2,24,PURPLE,3)))
        self.at(90,FadeIn(text('입력과 출력의 공간을 따로 비교',-3.4,size=25,color=MUTED)))

    def s10(self):
        r=self.rig(projections=False)
        label=exponential().move_to([0,-2.2,0]);self.add(label)
        self.play(FadeIn(text('크기 = 1',4.3,size=32,color=WHITE)),run_time=.6)
        self.at(95,FadeIn(text('변하는 것은 방향',-3.35,size=31,color=YELLOW)))
        self.at(98,FadeIn(text('각도 θ만큼 회전한 같은 점',-4.35,size=25,color=MUTED)))

    def s11(self):
        r=self.rig()
        left=exponential().move_to([-2.1,4.2,0]);right=trig(29).move_to([1.4,4.2,0])
        self.add(left)
        self.play(FadeIn(right),run_time=.6)
        a=Line(left.get_bottom(),r.point.get_center(),color=YELLOW,stroke_width=1.4,stroke_opacity=.5)
        b=Line(right.get_bottom(),r.point.get_center(),color=GREEN,stroke_width=1.4,stroke_opacity=.5)
        a.add_updater(lambda m:m.put_start_and_end_on(left.get_bottom(),r.point.get_center()))
        b.add_updater(lambda m:m.put_start_and_end_on(right.get_bottom(),r.point.get_center()))
        self.at(105,Create(a),Create(b))
        eq=formula(-2.6,34)
        self.at(108,FadeIn(eq[0]),FadeIn(eq[2]))
        self.at(109,FadeIn(eq[1]),duration=.5)
        self.at(110,FadeIn(text('오일러 공식',-3.8,size=32,color=YELLOW)))
        self.at(112,FadeIn(text('지수 표현 = 삼각함수 표현',-4.5,size=23,color=MUTED)))

    def s12(self):
        r=self.rig(small=True);sine=WaveTrace(r);cos=WaveTrace(r,'cos')
        self.add(sine,cos,formula(-3.6,31),text('같은 점 · 같은 각도 · 같은 시간',4.4,size=24,color=MUTED))
        self.to(126)
        self.play(FadeIn(text('회전의 두 좌표가 만드는 진동',-4.45,size=25,color=WHITE)),run_time=.6)
        self.to(133)
        self.play(sine.animate.fade(.82),cos.animate.fade(.82),run_time=.6)
        self.to(134)
        self.play(FadeIn(text('원을 도는 점 하나,\n서로 다른 표현의 연결',-1.8,-1.9,28,YELLOW,4)),run_time=.6)

class Shot01(TimedShot):NUMBER=1
class Shot02(TimedShot):NUMBER=2
class Shot03(TimedShot):NUMBER=3
class Shot04(TimedShot):NUMBER=4
class Shot05(TimedShot):NUMBER=5
class Shot06(TimedShot):NUMBER=6
class Shot07(TimedShot):NUMBER=7
class Shot08(TimedShot):NUMBER=8
class Shot09(TimedShot):NUMBER=9
class Shot10(TimedShot):NUMBER=10
class Shot11(TimedShot):NUMBER=11
class Shot12(TimedShot):NUMBER=12

