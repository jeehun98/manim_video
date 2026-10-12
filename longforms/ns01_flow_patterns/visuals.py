from pathlib import Path
import json
from manim import *

config.background_color='#081622'
config.frame_width=14.222222222
config.frame_height=8
ROOT=Path(__file__).resolve().parent
INK,MUTED,CYAN,GREEN,GOLD='#EAF5FB','#8FAABD','#51D8EE','#8BE0B1','#F4C978'
FONT='Malgun Gothic'

def txt(s,size=28,color=INK,width=12):
    t=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.15)
    if t.width>width: t.scale_to_fit_width(width)
    return t

def panel(x=0,w=11.5,h=4.2):
    return RoundedRectangle(width=w,height=h,corner_radius=.2,stroke_color='#294958',stroke_width=1,fill_color='#102735',fill_opacity=.65).move_to([x,.25,0])

def field(mode='vortex',phase=0,x=0,w=10,h=3,scale=1):
    arrows=VGroup()
    for yy in np.linspace(-h/2,h/2,7):
        for xx in np.linspace(-w/2,w/2,15):
            if mode=='uniform': v=np.array([.7,0,0])
            elif mode=='shear': v=np.array([.55+.27*yy,0,0])
            elif mode=='diffusion':
                sigma=.2+phase*.65
                v=np.array([.15+.85*.2/sigma*np.exp(-yy*yy/(2*sigma*sigma)),0,0])
            elif mode=='force': v=np.array([.3+.45*phase,.12*phase,0])
            elif mode=='pressure': v=np.array([.22+.12*xx*phase,.04*yy*phase,0])
            else:
                v=np.array([-.28*yy+.15*np.cos(xx+phase),.18*xx+.12*np.sin(yy+phase),0])
            v*=scale
            start=np.array([xx+x,yy+.25,0])
            arrows.add(Arrow(start,start+v,buff=0,stroke_width=2,max_tip_length_to_length_ratio=.2,color=CYAN if mode!='diffusion' else GREEN))
    return arrows

def ribbons(phase=0):
    paths=VGroup()
    for j in range(28):
        offset=(j-13.5)*.1
        curve=ParametricFunction(lambda t,o=offset: np.array([4.8*np.cos(t)*(.45+.055*t),1.85*np.sin(t+phase*.25)*(.45+.055*t)+o,.0]),t_range=[0,2*PI,.06],color=CYAN if j%3 else GREEN,stroke_width=1.5+(j%4),stroke_opacity=.18+(j%5)*.12)
        paths.add(curve)
    return paths.move_to([0,.3,0])

def patch(x=0,shear=0,color=GOLD,width=1.2,height=1.8):
    pts=[]
    for t in np.linspace(0,TAU,90):
        y=height/2*np.sin(t); xx=width/2*np.cos(t)+shear*y
        pts.append([xx+x,y+.25,0])
    return Polygon(*pts,stroke_color=color,stroke_width=2,fill_color=color,fill_opacity=.24)

def profile(phase=0,x=0,width=9):
    sigma=.22+.65*phase
    curve=ParametricFunction(lambda y: np.array([x+y*width/3, -.9+1.6*.22/sigma*np.exp(-y*y/(2*sigma*sigma)),0]),t_range=[-1.5,1.5,.025],color=GREEN,stroke_width=4)
    return curve

class FlowScene(Scene):
    index=1
    def construct(self):
        manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
        record=manifest[self.index-1]
        self.timing=json.loads((ROOT/record['directory']/'timing.json').read_text(encoding='utf-8'))
        titles=['물을 멈춰서 바라본다면?','공간을 채우는 속도 화살표','속도장을 바꾸는 네 가지 역할','흐름은 자신의 구조를 운반한다','점성은 속도 차이를 퍼뜨린다','같은 구조, 서로 다른 두 경향','그렇다면 어느 쪽이 이기는가?']
        self.add(txt('NAVIER–STOKES × NEURAL NETWORKS',15,MUTED).move_to([-3.7,3.65,0]))
        self.add(txt(f'01막   /   {self.index:02} — {titles[self.index-1]}',29).move_to([0,3.1,0]))
        self.caption=VGroup()
        self.add(Line([-6.2,-2.85,0],[6.2,-2.85,0],color='#294958',stroke_width=1))
        self.progress=Line([-6.2,-3.8,0],[-6.19,-3.8,0],color=CYAN,stroke_width=3)
        self.add(self.progress)
        getattr(self,f'scene{self.index}')()
        duration=self.timing['duration']
        if self.time>duration+.01: raise ValueError(f'Scene overrun {self.time}/{duration}')
        frames=round(duration*config.frame_rate)-round(self.time*config.frame_rate)
        if frames>0:self.wait(frames/config.frame_rate)

    def cue(self,n,*animations,seconds=3):
        self.remove(self.caption)
        line=self.timing['lines'][n-1]
        # Break long Korean narration into two centered lines inside safe area.
        if len(line)>48:
            spaces=[i for i,c in enumerate(line) if c==' ']
            if spaces:
                at=min(spaces,key=lambda i:abs(i-len(line)/2)); line=line[:at]+'\n'+line[at+1:]
        self.caption=txt(line,23,width=12.1).move_to([0,-3.32,0]); self.add(self.caption)
        end=round(self.timing['ends'][n-1]*config.frame_rate)/config.frame_rate
        available=end-self.time
        if available<0: raise ValueError(f'Cue {n} overrun')
        if animations: self.play(*animations,run_time=round(min(seconds,available)*config.frame_rate)/config.frame_rate,rate_func=smooth)
        remaining_frames=round(end*config.frame_rate)-round(self.time*config.frame_rate)
        if remaining_frames>0: self.wait(remaining_frames/config.frame_rate)
        self.progress.put_start_and_end_on([-6.2,-3.8,0],[-6.2+12.4*end/self.timing['duration'],-3.8,0])

    def scene1(self):
        photo=ImageMobject(str(ROOT/'assets'/'water.png')).set_width(8.8).move_to([0,.25,0])
        water=ribbons(); self.add(photo)
        self.cue(1,photo.animate.scale(1.025),seconds=4)
        self.cue(2,photo.animate.shift(LEFT*.15),FadeIn(water),seconds=6)
        frozen=txt('한순간을 멈추면',24,GOLD).move_to([0,2.25,0])
        arrows=field()
        self.cue(3,FadeIn(frozen),FadeIn(arrows),water.animate.set_stroke(opacity=.25).set_fill(opacity=0),photo.animate.set_opacity(.2),seconds=4)
        label=txt('각 위치의 속도와 방향',27,CYAN).move_to([0,-2.15,0])
        self.cue(4,FadeOut(photo),FadeOut(water),FadeIn(label),seconds=3)

    def scene2(self):
        self.add(panel()); a=field('uniform'); self.add(a)
        self.cue(1,Transform(a,field('shear')),seconds=4)
        dot=Dot([1,.7,0],color=GOLD); ring=Circle(radius=.35,color=GOLD).move_to(dot)
        label=txt('위치 x  →  속도 벡터 u',25,GOLD).move_to([0,2.65,0])
        self.cue(2,FadeIn(dot),FadeIn(ring),FadeIn(label),seconds=3)
        self.cue(3,Transform(label,txt('속도장  /  Velocity Field',28,CYAN).move_to([0,2.65,0])),seconds=2)
        self.cue(4,FadeOut(dot),FadeOut(ring),Transform(a,field('vortex',2)),seconds=4)
        self.cue(5,Transform(label,txt('u(x,t)   —   위치 x, 시간 t에서의 속도',28).move_to([0,2.65,0])),Transform(a,field('vortex',4)),seconds=4)

    def scene3(self):
        terms=VGroup(*[txt(s,31) for s in ['∂u/∂t','+ (u·∇)u','=','−∇p','+ ν∇²u','+ f']]).arrange(RIGHT,buff=.22).move_to([0,2.1,0])
        self.add(terms,txt('∇·u = 0    |    p：밀도로 나눈 압력',18,MUTED).move_to([0,1.5,0]))
        a=field('uniform',w=9,h=2.2).shift(DOWN*.4); self.add(a)
        l=txt('다음 순간의 속도장을 결정하는 역할',24).move_to([0,-1.9,0]); self.add(l)
        self.cue(1,FadeIn(terms),seconds=2)
        self.cue(2,terms[1].animate.set_color(GOLD),Transform(a,field('shear',w=9,h=2.2).shift(DOWN*.4)),Transform(l,txt('이류  /  운반과 변형',26,GOLD).move_to([0,-1.9,0])),seconds=4)
        self.cue(3,terms[1].animate.set_color(INK),terms[3].animate.set_color(CYAN),Transform(a,field('pressure',1,w=9,h=2.2).shift(DOWN*.4)),Transform(l,txt('압력  /  압력 차이에 따른 가속',26,CYAN).move_to([0,-1.9,0])),seconds=4)
        self.cue(4,terms[3].animate.set_color(INK),terms[4].animate.set_color(GREEN),Transform(a,field('diffusion',1,w=9,h=2.2).shift(DOWN*.4)),Transform(l,txt('점성  /  운동량의 확산',26,GREEN).move_to([0,-1.9,0])),seconds=4)
        self.cue(5,terms[4].animate.set_color(INK),terms[5].animate.set_color(GOLD),Transform(a,field('force',1,w=9,h=2.2).shift(DOWN*.4)),Transform(l,txt('외력  /  중력과 외부의 힘',26,GOLD).move_to([0,-1.9,0])),seconds=3)
        self.cue(6,terms.animate.set_color(INK),Transform(a,field('vortex',w=9,h=2.2).shift(DOWN*.4)),Transform(l,txt('이 역할들이 함께 작용합니다',26).move_to([0,-1.9,0])),seconds=3)

    def scene4(self):
        self.add(panel(-3,w=5.5),panel(3,w=5.5))
        a=field('uniform',x=-3,w=4,h=2.7); b=field('shear',x=3,w=4,h=2.7)
        left=patch(-3.7,width=.9); right=patch(2.3,width=.9)
        self.add(a,b,left,right,txt('균일한 흐름',24,CYAN).move_to([-3,2.1,0]),txt('불균일한 흐름',24,GOLD).move_to([3,2.1,0]))
        self.cue(1)
        self.cue(2,left.animate.shift(RIGHT*.5),right.animate.shift(RIGHT*.5),seconds=4)
        self.cue(3,Transform(right,patch(2.8,shear=.5,width=.9)),seconds=4)
        self.cue(4,Transform(right,patch(3.1,shear=1,width=.9)),left.animate.shift(RIGHT*.3),seconds=4)
        note=txt('표지 영역의 면적은 유지됩니다',21,MUTED).move_to([0,-2.1,0])
        self.cue(5,Transform(right,patch(3.2,shear=1.35,width=.9)),FadeIn(note),seconds=4)
        self.cue(6,Transform(note,txt('u가 구조를 운반하고, 바뀐 u가 다음 움직임을 결정',24,GOLD).move_to([0,-2.1,0])),seconds=3)

    def scene5(self):
        a=field('diffusion',w=9,h=2.5).shift(UP*.6); self.add(a)
        graph=profile().shift(DOWN*.6); baseline=Line([-4.5,-1.5,0],[4.5,-1.5,0],color=MUTED,stroke_width=1)
        self.add(graph,baseline,txt('u = (v(y,t), 0)    |    ∂v/∂t = ν ∂²v/∂y²',23,GREEN).move_to([0,2.25,0]),txt('位置 y →'.replace('位置','위치'),18,MUTED).move_to([4.5,-1.8,0]),txt('속도 v(y,t)',18,GREEN).move_to([-4.5,-.3,0]))
        self.cue(1)
        self.cue(2,Indicate(graph,color=GOLD),seconds=2)
        self.cue(3,Transform(a,field('diffusion',.3,w=9,h=2.5).shift(UP*.6)),Transform(graph,profile(.3).shift(DOWN*.6)),seconds=4)
        self.cue(4,Transform(a,field('diffusion',.65,w=9,h=2.5).shift(UP*.6)),Transform(graph,profile(.65).shift(DOWN*.6)),seconds=5)
        self.cue(5,Transform(a,field('diffusion',1,w=9,h=2.5).shift(UP*.6)),Transform(graph,profile(1).shift(DOWN*.6)),seconds=4)
        self.cue(6,FadeIn(txt('最高값 ↓    주변으로 전달    속도 차이 완화'.replace('最高','최고'),24,GREEN).move_to([0,-2.2,0])),seconds=3)

    def scene6(self):
        pa,pb=panel(-3,w=5.5),panel(3,w=5.5); self.add(pa,pb)
        a=field('diffusion',x=-3,w=4,h=2.5); b=field('diffusion',x=3,w=4,h=2.5)
        p=patch(-3,width=.5,height=2.1); q=patch(3,width=.5,height=2.1,color=GREEN)
        labels=VGroup(txt('이류에 의한 변형',24,GOLD).move_to([-3,2.35,0]),txt('점성에 의한 확산',24,GREEN).move_to([3,2.35,0]))
        self.add(a,b,p,q,labels)
        self.cue(1)
        self.cue(2,Transform(a,field('shear',x=-3,w=4,h=2.5)),Transform(p,patch(-3,shear=.7,width=.5,height=2.1)),seconds=5)
        self.cue(3,Transform(b,field('diffusion',1,x=3,w=4,h=2.5)),q.animate.stretch(2.8,0).set_opacity(.35),seconds=5)
        self.cue(4,FadeOut(pa),FadeOut(pb),FadeOut(labels),FadeOut(p),FadeOut(q),seconds=3)
        combined=field('vortex',w=9,h=2.5)
        self.cue(5,Transform(a,combined),FadeOut(b),FadeIn(txt('같은 공간에서 동시에 작용',26).move_to([0,2.3,0])),seconds=4)
        factors=VGroup(*[txt(s,23,c) for s,c in [('흐름의 속도 U',GOLD),('흐름의 크기 L',CYAN),('점성 ν',GREEN),('구조의 스케일 ℓ',GOLD)]]).arrange(RIGHT,buff=.5).move_to([0,-2.2,0])
        self.cue(6,FadeIn(factors),Transform(a,field('vortex',2,w=9,h=2.5)),seconds=5)

    def scene7(self):
        a=field('uniform',w=9,h=2.8); self.add(a)
        self.cue(1)
        water=ribbons().scale(.72)
        self.cue(2,Transform(a,field('vortex',1,w=9,h=2.8)),FadeIn(water),seconds=4)
        self.cue(3,water.animate.set_stroke(color=GREEN,opacity=.4).set_fill(opacity=0),Transform(a,field('vortex',2,w=9,h=2.8,scale=.75)),seconds=3)
        question=txt('점성은 언제나 충분할까?',33,GOLD).move_to([0,2.2,0])
        self.cue(4,FadeIn(question),seconds=2)
        self.cue(5,Transform(question,txt('매끄러움은 계속 유지될까?',33,GOLD).move_to([0,2.2,0])),seconds=3)
        self.cue(6,FadeOut(a),water.animate.set_stroke(opacity=.65).set_fill(opacity=0),seconds=2)
        self.cue(7,Transform(question,txt('다음 막  /  왜 3차원인가?',33,CYAN).move_to([0,2.2,0])),water.animate.scale(.9),seconds=2)
