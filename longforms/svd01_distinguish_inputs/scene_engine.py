"""One continuous, deterministic experiment; each scene renders its own time interval."""
import json, math, textwrap
from pathlib import Path
import numpy as np
from manim import *
config.background_color='#09121F'
config.frame_width=128/9
config.frame_height=8
FONT='Malgun Gothic'; BLUE_A='#64AEFF'; ORANGE_B='#FFB36B'; TEAL='#51D9C5'; MUTED='#8EA3BA'; WHITE_INK='#EDF4FC'
ROOT=Path(__file__).resolve().parent
TIMES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))['sentences']

def txt(s,size=24,color=WHITE_INK):
    return Text(s,font=FONT,font_size=size,color=color,line_spacing=1.1)
def mix(a,b,t):return a+(b-a)*np.clip(t,0,1)
def phase(t):
    # Exact coordinates at the poles: never represent cos(pi/2) as a tiny positive value.
    if t<25: theta=0
    elif t<31: theta=0
    elif t<35:theta=mix(0,PI/2,smooth((t-31)/4))
    elif t<52:theta=PI/2
    elif t<56:theta=mix(0,PI/2,smooth((t-52)/4))
    elif t<106:theta=PI/2
    elif t<109:theta=mix(PI/2,0,(t-106)/3)
    elif t<115:theta=mix(0,PI/2,(t-109)/6)
    elif t<131.8:theta=PI/2+(t-115)*TAU/12
    else:theta=PI/2+(131.8-115)*TAU/12
    if t<59:s=.1
    elif t<61:s=mix(.1,.01,smooth((t-59)/2))
    elif t<63:s=mix(.01,.001,smooth((t-61)/2))
    elif t<85:s=.001
    elif t<115:s=0
    else:s=.1
    x,y=math.cos(theta),math.sin(theta)
    if abs(x)<1e-12:x=0.
    if abs(y)<1e-12:y=0.
    return x,y,s

def num(x):
    if abs(x)<1e-10:return '0'
    return f'{x:.3f}'.rstrip('0').rstrip('.') if abs(x)>=.001 else f'{x:.6f}'.rstrip('0').rstrip('.')

class ExperimentScene(Scene):
    start_time=0;end_time=133
    def construct(self):
        clock=ValueTracker(self.start_time)
        now=lambda:clock.get_value()
        self.add(clock)
        # Fixed frame; all diagrams share the same unit scale throughout.
        top=txt('서로 다른 입력을 행렬은 구별할 수 있을까?',33).move_to([0,3.43,0])
        kicker=txt('관측 실험  /  01     구별 가능성',15,MUTED).move_to([0,3.88,0])
        self.add(top,kicker,Line([-6.65,2.98,0],[6.65,2.98,0],color='#25364B',stroke_width=1))
        O1=np.array([-3.65,.12,0]);O2=np.array([3.65,.12,0]);unit=1.65
        for origin,col in [(O1,BLUE_A),(O2,TEAL)]:
            box=RoundedRectangle(width=5.45,height=4.08,corner_radius=.18,stroke_color='#2A3D54',stroke_width=1.2,fill_color='#101E2D',fill_opacity=1).move_to(origin+[0,.12,0])
            self.add(box)
            grid=VGroup()
            for v in [-1,-.5,0,.5,1]:
                grid.add(Line(origin+[-1.3*unit,v*unit,0],origin+[1.3*unit,v*unit,0],color='#24364A',stroke_width=.7))
                grid.add(Line(origin+[v*unit,-1.05*unit,0],origin+[v*unit,1.15*unit,0],color='#24364A',stroke_width=.7))
            self.add(grid,Arrow(origin+[-2.18,0,0],origin+[2.2,0,0],buff=0,color=MUTED,stroke_width=1.3,max_tip_length_to_length_ratio=.025),Arrow(origin+[0,-1.73,0],origin+[0,1.93,0],buff=0,color=MUTED,stroke_width=1.3,max_tip_length_to_length_ratio=.03))
            self.add(txt('1',16,MUTED).move_to(origin+[unit,-.2,0]),txt('1',16,MUTED).move_to(origin+[-.2,unit,0]))
        self.add(txt('실제 입력  /  시청자에게 공개',21,BLUE_A).move_to([-3.65,2.65,0]),txt('관측 출력  /  관찰자는 이쪽만',21,TEAL).move_to([3.65,2.65,0]))
        # Functional box, deliberately avoiding SVD terminology.
        self.add(RoundedRectangle(width=1.05,height=1.55,corner_radius=.12,color='#425772',fill_color='#142337',fill_opacity=1).move_to([0,.48,0]),txt('행렬',22).move_to([0,.93,0]),txt('가로 ×1',15).move_to([0,.43,0]),Arrow([-.5,-.55,0],[.5,-.55,0],color=TEAL,buff=0,stroke_width=2))
        scale_value=txt('세로 ×0.1',14,TEAL).move_to([0,.08,0])
        scale_cache={}
        def scale_update(m):
            label='세로 ×'+num(phase(now())[2])
            if label not in scale_cache:scale_cache[label]=txt(label,14,TEAL).move_to([0,.08,0])
            m.become(scale_cache[label])
        scale_value.add_updater(scale_update);self.add(scale_value)
        # Dynamic points are computed from a single mathematical model.
        point1=lambda:O1+unit*np.array([phase(now())[0],phase(now())[1],0])
        point2=lambda:O2+unit*np.array([phase(now())[0],phase(now())[1]*phase(now())[2],0])
        circle=Circle(radius=unit,color='#304A65',stroke_width=1.4).move_to(O1)
        circle.add_updater(lambda m:m.set_opacity(.6 if now()>=106 else 0));self.add(circle)
        for o,p in [(O1,point1),(O2,point2)]:
            vector=Line(o,p(),color=ORANGE_B,stroke_width=3)
            vector.add_updater(lambda m,o=o,p=p:m.put_start_and_end_on(o,p() if np.linalg.norm(p()-o)>1e-9 else o+np.array([1e-9,0,0])))
            da=Dot(o,radius=.06,color=BLUE_A);db=Dot(p(),radius=.055,color=ORANGE_B)
            db.add_updater(lambda m,p=p:m.move_to(p()))
            la=txt('A',20,BLUE_A).move_to(o+[-.23,-.27,0]);lb=txt('B',20,ORANGE_B)
            lb.add_updater(lambda m,p=p:m.move_to(p()+[.23,.21,0]).set_opacity(0 if now()>=85 and now()<106 and np.allclose(p(),o) else 1))
            self.add(vector,da,db,la,lb)
        # A ghost of the horizontal result supports the comparison without changing scale.
        ghost=DashedLine(O2,O2+[unit,0,0],color=MUTED,stroke_width=2,dash_length=.08)
        ghost.add_updater(lambda m:m.set_opacity(.7 if 35<=now()<56 else 0));self.add(ghost)
        ghostlabel=txt('가로 실험: 1',17,MUTED).move_to(O2+[.95,-.34,0])
        ghostlabel.add_updater(lambda m:m.set_opacity(1 if 35<=now()<56 else 0));self.add(ghostlabel)
        # Numeric measurements use cached Pango text. They never infer equality from pixel overlap.
        cache={}
        def cached(s,size,color):
            key=(s,size,color)
            if key not in cache:cache[key]=txt(s,size,color)
            return cache[key].copy()
        for o,isout in [(O1,False),(O2,True)]:
            holder=VGroup(txt(' ',18))
            def update_readout(m,o=o,isout=isout):
                x,y,s=phase(now()); yy=y*s if isout else y
                label=f'B = ({num(x)}, {num(yy)})' if now()>=25 else '기준점 A = (0, 0)'
                m.become(cached(label,18,ORANGE_B if isout else MUTED).move_to(o+[0,-1.49,0]))
            holder.add_updater(update_readout);self.add(holder)
        # Input remains private to the observer: only the audience gets the reveal.
        cover=RoundedRectangle(width=5.32,height=3.97,corner_radius=.15,stroke_width=0,fill_color='#0C1625',fill_opacity=.97).move_to(O1+[0,.12,0])
        covertext=VGroup(txt('?',62,MUTED),txt('입력은 관찰할 수 없음',23,MUTED)).arrange(DOWN,buff=.3).move_to(O1)
        for mob in [cover,covertext]:
            mob.add_updater(lambda m:m.set_opacity(1 if (2.5<=now()<11 or 89<=now()<98) else 0));self.add(mob)
        # Extra points all have the same x coordinate, rather than collapsing the whole plane.
        extras=VGroup(*[Dot(O1+unit*np.array([0,v,0]),radius=.035,color=MUTED) for v in [-.9,-.6,-.3,.3,.6,.9]])
        extras.add_updater(lambda m:m.set_opacity(.85 if 85<=now()<89 else 0));self.add(extras)
        streams=VGroup(*[DashedLine(O1+unit*np.array([0,v,0]),O2,color=TEAL,stroke_width=.7,dash_length=.1) for v in [-.9,-.3,.6,1]])
        streams.add_updater(lambda m:m.set_opacity(.3 if 86<=now()<89 else 0));self.add(streams)
        # Lower explanatory band, independent of the full narration subtitles.
        band=RoundedRectangle(width=13,height=.72,corner_radius=.1,stroke_width=0,fill_color='#14273A',fill_opacity=1).move_to([0,-2.27,0]);self.add(band)
        badges=[(0,8,'보이지 않는 입력 → 관측 가능한 출력',MUTED),(8,11,'출력만으로 입력의 차이를 알 수 있을까?',WHITE_INK),(11,19,'왼쪽은 실험 공개 정보 · 관찰자는 오른쪽만 본다',MUTED),(19,25,'가로 ×1   /   세로 ×0.1',TEAL),(25,31,'가로 방향     입력 거리 1  →  출력 거리 1',WHITE_INK),(31,43,'세로 방향     입력 거리 1  →  출력 거리 0.1',WHITE_INK),(43,51,'같은 입력 거리 1     /     출력 차이는 10배',WHITE_INK),(51,56,'입력 거리는 고정 · 달라진 것은 방향',ORANGE_B),(56,71,'입력 거리 1 고정     /     0.1 → 0.01 → 0.001',WHITE_INK),(71,82,'정확한 출력값:   A의 y = 0.000    ≠    B의 y = 0.001',TEAL),(82,89,'세로 배율 0     /     같은 x좌표의 입력들이 같은 출력으로',ORANGE_B),(89,98,'관측값은 동일 · 원래 입력은 구별 불가능',ORANGE_B),(98,106,'차이가 작다  ≠  차이가 없다',WHITE_INK),(106,115,'입력 거리 1 · 방향은 무한히 많다',WHITE_INK),(115,125,'배율 0.1로 복귀 · 같은 거리에서 방향만 바꾼다',TEAL),(125,133,'어떤 방향의 차이가 가장 크게, 가장 작게 남을까?',WHITE_INK)]
        for lo,hi,label,col in badges:
            mob=txt(label,23,col).move_to([0,-2.27,0]);mob.add_updater(lambda m,lo=lo,hi=hi:m.set_opacity(1 if lo<=now()<hi else 0));self.add(mob)
        # Explicitly separate the magnified measurement from the fixed-scale coordinate panels.
        magnify=VGroup(RoundedRectangle(width=2.25,height=1.55,corner_radius=.13,fill_color='#102E39',fill_opacity=1,stroke_color=TEAL),txt('간격 확대 · 별도 척도',12,TEAL).move_to([0,.52,0]),Dot([-.35,-.34,0],color=BLUE_A,radius=.05),Dot([-.35,.23,0],color=ORANGE_B,radius=.05),Line([-.35,-.34,0],[-.35,.23,0],color=TEAL,stroke_width=2),txt('실제 거리 0.001',14).move_to([.35,-.5,0])).move_to([5.05,1.03,0])
        magnify.add_updater(lambda m:m.set_opacity(1 if 71<=now()<82 else 0));self.add(magnify)
        # Actual comparison table; only the zero row signals mathematical loss.
        table=VGroup(RoundedRectangle(width=4.9,height=2.6,corner_radius=.15,fill_color='#102033',fill_opacity=1,stroke_color='#405772'))
        table.add(txt('배율       출력 차이       정확한 구별',18,MUTED).move_to([0,.95,0]))
        for i,(s,ans) in enumerate([('0.1','가능'),('0.01','가능'),('0.001','가능'),('0','불가능')]):
            table.add(txt(f'{s:<7}      {s:<7}      {ans}',20,ORANGE_B if i==3 else MUTED).move_to([0,.45-i*.47,0]))
        table.move_to(O1+[0,.15,0]);table.add_updater(lambda m:m.set_opacity(1 if 98<=now()<106 else 0));self.add(table)
        # Subtitles have exact supplied start/end times. No inferred phrase timings.
        self.add(Rectangle(width=14.23,height=1.06,stroke_width=0,fill_color='#070D16',fill_opacity=1).move_to([0,-3.41,0]))
        for rec in TIMES:
            if rec['end']<=self.start_time or rec['start']>=self.end_time:continue
            lines=textwrap.wrap(rec['text'],width=49)
            cap=txt('\n'.join(lines),21).move_to([0,-3.35,0])
            if cap.width>13.1:cap.scale_to_fit_width(13.1)
            if cap.height>.88:cap.scale_to_fit_height(.88)
            cap.add_updater(lambda m,r=rec:m.set_opacity(1 if r['start']<=now()<r['end'] else 0));self.add(cap)
        # Exact-frame interval rendering; no timing extension and no speed changes.
        self.update_mobjects(0)
        self.play(clock.animate.set_value(self.end_time),run_time=self.end_time-self.start_time,rate_func=linear)
