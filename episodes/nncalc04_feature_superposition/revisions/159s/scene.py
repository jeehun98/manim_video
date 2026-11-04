"""Two coordinate axes, five feature directions; native landscape and portrait."""
import json
import os
import sys
import textwrap
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.nncalc02_induction_heads import scene as shared
from visual_library.manim import BG,INK,MUTED,ACCENT,GOOD,PRUNE,ZERO

config.pixel_width=int(os.environ.get('VIDEO_WIDTH','1920'))
config.pixel_height=int(os.environ.get('VIDEO_HEIGHT','1080'))
PORTRAIT=config.pixel_height>config.pixel_width
config.frame_width=9 if PORTRAIT else 16
config.frame_height=16 if PORTRAIT else 9
config.frame_rate=30;config.background_color=BG;config.disable_caching=True
HERE=Path(__file__).resolve().parent
COLORS=['#55DACA','#B49BFA','#F2CB70','#EF8799','#7EB8F3']
INITIAL=np.deg2rad([20,110,60,215,305])
REGULAR=np.deg2rad(20+72*np.arange(5))
label=shared.label;card=shared.card;p=shared.p

def vectors(angles):return np.array([np.cos(angles),np.sin(angles)])

class FeaturePlane(VGroup):
    """Axes are neurons; columns of W are feature directions, not neurons."""
    def __init__(self,portrait=False):
        side=5.5 if portrait else 4.7
        center=p(0,1.5) if portrait else p(-3.2,-.05)
        self.axes=Axes(x_range=[-2,2,1],y_range=[-2,2,1],x_length=side,y_length=side,
            tips=False,axis_config=dict(color=MUTED,stroke_width=1.7,include_ticks=False)).move_to(center)
        self.origin=self.axes.c2p(0,0)
        self.vectors=VGroup();self.angles=INITIAL.copy()
        self.axis_labels=VGroup(label('Neuron 1',*(self.axes.c2p(1.6,-.3)[:2]),size=17,color=MUTED,width=1.55),
            label('Neuron 2',*(self.axes.c2p(-.5,1.9)[:2]),size=17,color=MUTED,width=1.55))
        self.origin_dot=Dot(self.origin,radius=.045,color=INK)
        super().__init__(self.axes,self.axis_labels,self.origin_dot,self.vectors)
    def point(self,v):return self.axes.c2p(*(np.asarray(v)*1.25))
    def glyph(self,i,angle,length=1):
        v=np.array([np.cos(angle),np.sin(angle)])*length
        end=self.point(v)
        edge=Arrow(self.origin,end,buff=0,color=COLORS[i],stroke_width=4,
            max_tip_length_to_length_ratio=.15)
        xy=end+(end-self.origin)/np.linalg.norm(end-self.origin)*.24
        return VGroup(edge,label(f'F{i+1}',*xy[:2],size=23,color=COLORS[i],width=.6))
    def set_features(self,scene,angles=INITIAL,lengths=None):
        self.angles=np.array(angles)
        lengths=np.ones(5) if lengths is None else lengths
        new=VGroup(*[self.glyph(i,a,l) for i,(a,l) in enumerate(zip(angles,lengths))])
        if len(self.vectors):scene.play(Transform(self.vectors,new),run_time=.7)
        else:
            self.vectors.add(*new);scene.play(LaggedStart(*[GrowArrow(g[0]) for g in self.vectors],lag_ratio=.12),
                *[FadeIn(g[1]) for g in self.vectors],run_time=.9)
    def select(self,scene,indices):
        scene.play(*[g.animate.set_opacity(1 if i in indices else .13) for i,g in enumerate(self.vectors)],run_time=.45)
    def projections(self,i):
        v=vectors(self.angles)[:,i];end=self.point(v);foot=self.point([v[0],0])
        return VGroup(DashedLine(end,foot,color=COLORS[i],dash_length=.08),
            Line(self.origin,foot,color=COLORS[i],stroke_width=7),Dot(foot,color=COLORS[i],radius=.07))

class ActivationPattern(VGroup):
    DENSE=np.array([[1,1,0,1,0],[1,0,1,1,1],[0,1,1,0,1],[1,1,1,0,1],[0,1,0,1,1],[1,0,1,1,0]])
    SPARSE=np.array([[1,0,0,0,0],[0,0,0,1,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,0,1],[1,0,0,0,1]])
    def __init__(self,sparse=False,portrait=False):
        x,y=(0,-3.5) if portrait else (3.85,-.1)
        step=.41 if portrait else .47
        rows=self.SPARSE if sparse else self.DENSE
        self.cells=VGroup()
        for i in range(6):
            for j in range(5):
                active=rows[i,j]
                self.cells.add(Square(side_length=step*.76,color=COLORS[j] if active else ZERO,
                    stroke_width=1,fill_color=COLORS[j] if active else ZERO,fill_opacity=.95 if active else .25)
                    .move_to(p(x+(j-2)*step,y+(2.5-i)*step)))
        names=VGroup(*[label(f'F{j+1}',x+(j-2)*step,y+3.4*step,17,COLORS[j],.4) for j in range(5)])
        super().__init__(self.cells,names,label('입력',x-1.65,y,18,MUTED,1))

class ToyModel(VGroup):
    nonlinear_output=True
    tied_weights=True
    def __init__(self,portrait=False):
        x,y=(0,-3.05) if portrait else (3.85,.1)
        cols=[x-2.25,x,x+2.25];counts=[5,2,5]
        self.nodes=VGroup()
        for cx,count in zip(cols,counts):
            self.nodes.add(VGroup(*[Dot(p(cx,y+(count-1)*.2-j*.4),radius=.085,
                color=COLORS[j] if count==5 else INK) for j in range(count)]))
        edges=VGroup(*[Line(a.get_center(),b.get_center(),color=ZERO,stroke_width=1.2)
            for left,right in zip(self.nodes,self.nodes[1:]) for a in left for b in right])
        super().__init__(edges,self.nodes,*[label(s,cx,y-1.25,19,INK,1.9) for cx,s in zip(cols,['입력 5','내부 2','복원 5'])],
            label('h = Wx   ·   x̂ = ReLU(Wᵀh + b)',x,-4.85 if portrait else y+1.3,20,GOOD,6.5))

class NeuronResponse(VGroup):
    hypothetical=True
    def __init__(self,portrait=False):
        x,y=(0,-3.15) if portrait else (3.8,-.3)
        self.bars=VGroup()
        for j,i in enumerate([0,4]):
            yy=y+.55-j*1.15
            value=float(np.cos(REGULAR[i]))
            bar=Rectangle(width=2.2*value,height=.22,stroke_width=0,fill_color=COLORS[i],fill_opacity=.95)
            bar.move_to(p(x+.05+bar.width/2,yy))
            self.bars.add(bar)
        super().__init__(self.bars,label('고양이 · F1',x-1.55,y+.55,22,COLORS[0],2.5),
            label('다른 특징 · F5',x-1.55,y-.6,22,COLORS[4],2.5),
            label('동일한 Neuron 1의 양의 성분',x,y+1.35,22,INK,6.6),
            label('고양이 예시는 가상 · 실제 뉴런 실측 아님',x,y-1.45,16,MUTED,7))

class SuperpositionVideo(Scene):
    def caption_obj(self,s):
        obj=label(textwrap.fill(s,width=29 if self.portrait else 60,break_long_words=False,break_on_hyphens=False),
            y=-6.2 if self.portrait else -3.65,size=25 if self.portrait else 27,width=7.2 if self.portrait else 14.4)
        if obj.height>(1.5 if self.portrait else .88):obj.scale_to_fit_height(1.5 if self.portrait else .88)
        return obj
    def to(self,t):
        n=round(t*30)-round(self.time*30)
        if n>0:self.wait(n/30)
        elif n < -3:raise RuntimeError(f'Timing overflow {self.time} > {t}')
    def panel(self,title,lines=(),colors=None):
        P=self.portrait;x,y=(0,-1.7) if P else (3.8,2.25)
        w=7.3 if P else 6.1
        new=VGroup(label(title,x,y,27,ACCENT,w))
        for j,s in enumerate(lines):new.add(label(s,x,y-.86-j*.8,24,(colors or [INK]*len(lines))[j],w))
        self.remove(self.info);self.info=new;self.add(new)
    def extra(self,*objects):self.aux.add(*objects);self.add(*objects)
    def clear_aux(self):
        self.remove(*self.aux.get_family());self.aux=VGroup()
    def pulse(self,*objects):self.play(*[Indicate(o,scale_factor=1.07) for o in objects],run_time=.65)
    def construct(self):
        self.portrait=PORTRAIT;P=PORTRAIT
        timing=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
        if P:
            fixed=VGroup(label('신경망 내부의 계산  04',y=7.4,size=20,color=MUTED,width=7.5),
                label('뉴런 두 개로\n다섯 특징을 표현할 수 있을까?',y=6.5,size=29,width=7.5),
                Line(p(-3.9,5.75),p(3.9,5.75),color=ZERO))
        else:
            fixed=VGroup(label('신경망 내부의 계산  04',-5.1,4.08,18,MUTED,5),
                label('뉴런 두 개로 다섯 특징을 표현할 수 있을까?',2.5,4.08,22,INK,9.5),
                Line(p(-7.4,3.65),p(7.4,3.65),color=ZERO))
        fixed.add(RoundedRectangle(width=7.9 if P else 15,height=1.85 if P else 1.04,corner_radius=.1,
            stroke_width=0,fill_color='#14212D',fill_opacity=.95).move_to(p(0,-6.2 if P else -3.65)),
            label('설명용 기하·가상 입력 · Elhage et al., 2022',y=-7.45 if P else -4.3,size=15,color=MUTED,width=7.5 if P else 14))
        self.add(fixed);self.plane=FeaturePlane(P);self.add(self.plane)
        self.info=VGroup();self.aux=VGroup();self.caption=VGroup();self.heading=VGroup()
        chapter_starts={s['cues'][0]['index']:(i,s['title']) for i,s in enumerate(timing['segments'],1)}
        for q in timing['cues']:
            self.to(q['start']);i=q['index']
            if i in chapter_starts:
                n,title=chapter_starts[i];self.remove(self.heading)
                self.heading=label(f'{n:02}  {title}',y=5.25 if P else 3.12,size=24 if P else 29,
                    color=ACCENT,width=7.7 if P else 14.5);self.add(self.heading)
            self.remove(self.caption);self.caption=self.caption_obj(q['text']);self.add(self.caption)
            self.event(i);self.to(q['end'])
        self.to(159)
    def event(self,i):
        P=self.portrait;f=self.plane
        if i==0:
            self.panel('뉴런 2개 → 특징 몇 개?', ['Neuron 1     Neuron 2','표현 공간은 2차원'])
            self.play(Create(f.axes),FadeIn(f.axis_labels),run_time=.8)
        elif i==1:
            self.panel('서로 수직인 방향은 두 개',['h = (h₁, h₂) ∈ ℝ²','뉴런 = 좌표축'])
            self.extra(Arrow(f.origin,f.point([1,0]),buff=0,color=INK),Arrow(f.origin,f.point([0,1]),buff=0,color=INK))
            self.pulse(self.aux)
        elif i==2:self.panel('세 번째 특징은?', ['좌표축을 더 늘려야 할까?'])
        elif i==3:
            self.clear_aux();f.set_features(self)
            self.panel('뉴런과 특징을 구별하면',['뉴런 = 좌표축','특징 = 벡터 방향'],[MUTED,GOOD])
        elif i==4:
            rays=VGroup(*[Line(f.origin,f.point([np.cos(a),np.sin(a)]),color=MUTED,stroke_opacity=.35,stroke_width=1)
                for a in np.linspace(0,TAU,16,endpoint=False)])
            self.extra(rays);self.play(Create(rays),run_time=.8)
            self.panel('방향은 얼마든지 만들 수 있다',['서로 다른 방향','≠ 독립적인 정보'])
        elif i==5:
            self.clear_aux();self.panel('다섯 특징 · 다섯 방향',['F1   F2   F3   F4   F5','같은 2차원 공간을 공유'])
            self.pulse(f.vectors)
        elif i==6:
            f.select(self,[0,1,2]);self.panel('다섯 방향은 독립적이지 않다',['v₃ ≈ 0.77 v₁ + 0.64 v₂','임의의 5개 연속값을','무손실 저장할 수는 없다'],[COLORS[2],INK,PRUNE])
        elif i==7:
            self.clear_aux();f.select(self,[0,2]);V=vectors(INITIAL)
            first=f.point(V[:,0]);total=f.point(V[:,0]+V[:,2])
            translated=Arrow(first,total,buff=0,color=COLORS[2],stroke_width=4)
            result=Arrow(f.origin,total,buff=0,color=PRUNE,stroke_width=5)
            self.extra(translated,result);self.play(GrowArrow(translated),GrowArrow(result),run_time=.9)
            self.panel('활성화되면 벡터가 더해진다',['h = x₁v₁ + x₃v₃','F1 + F3 → 하나의 내부 벡터'],[PRUNE,INK])
        elif i==8:
            self.clear_aux();f.select(self,[0,1,2]);V=vectors(INITIAL);a,b=np.linalg.solve(V[:,:2],V[:,2])
            mid=f.point(a*V[:,0]);end=f.point(V[:,2])
            self.extra(Arrow(f.origin,mid,buff=0,color=COLORS[0]),Arrow(mid,end,buff=0,color=COLORS[1]),
                Dot(end,color=PRUNE,radius=.13))
            self.panel('서로 다른 입력 → 같은 점',['F3 하나가 켜진 입력','≈ 0.77·F1 + 0.64·F2','위 계수는 반올림 표시'],[COLORS[2],PRUNE,MUTED])
            self.pulse(self.aux[-1])
        elif i==9:
            self.clear_aux();f.select(self,range(5));self.panel('특징이 드물게 나타난다면?',['희소성 · Sparsity','동시에 켜지는 특징이 적다'],[GOOD,INK])
        elif i==10:
            self.panel('대부분 하나 · 가끔 둘',['','',''])
            grid=ActivationPattern(True,P);self.extra(grid);self.pulse(grid.cells[-5],grid.cells[-1])
            f.select(self,[0])
        elif i==11:
            self.clear_aux();f.select(self,[4]);self.panel('동시 활성화가 줄어든다',['입력마다 다른 특징이 활성화','겹침의 빈도와 비용 감소','교차 투영 간섭은 남을 수 있음'],[INK,GOOD,MUTED])
        elif i==12:
            f.select(self,range(5));self.panel('일부 간섭 ↔ 더 많은 특징',['2차원에 5개 방향을 공유','희소성이 바꾸는 절충'],[INK,GOOD]);self.pulse(f.vectors)
        elif i==13:self.panel('Feature Superposition',['특징의 중첩 표현','차원보다 많은 특징 방향'],[GOOD,INK])
        elif i==14:
            self.panel('Toy Models of Superposition');self.extra(ToyModel(P))
            self.pulse(self.aux[-1].nodes[1])
        elif i==15:
            self.clear_aux();f.set_features(self,INITIAL,[1,1,.12,.12,.12])
            self.panel('자주 활성화되는 조건',['중요한 일부 특징에 집중','조건별로 새로 학습한 결과','기하·길이는 정성적 개념도'],[INK,MUTED,MUTED])
        elif i==16:
            f.set_features(self);self.panel('희소한 조건',['더 많은 특징을 표현','같은 차원 · 다른 학습 결과','가중 재구성 손실 + ReLU'],[GOOD,INK,MUTED])
        elif i==17:
            circle=Circle(radius=np.linalg.norm(f.point([1,0])-f.origin),color=MUTED,stroke_opacity=.45).move_to(f.origin)
            self.extra(circle);self.play(Create(circle),run_time=.7)
            self.panel('방향의 기하에도 구조가 있다',['다섯 방향은 어떻게 배치될까?'])
        elif i==18:
            f.set_features(self,REGULAR)
            polygon=Polygon(*[f.point(v) for v in vectors(REGULAR).T],stroke_color=COLORS[1],stroke_width=2,fill_opacity=0)
            self.extra(polygon);self.play(Create(polygon),run_time=.8)
            self.panel('특정 조건에서 나타난 오각형',['정오각형은 이상화된 개념도','애니메이션 ≠ 실제 학습 궤적'],[COLORS[1],MUTED])
        elif i==19:
            self.panel('제한된 공간의 표현 기하',['특징 사이 간섭의 비용을 절충','조건마다 같은 도형은 아니다'],[INK,MUTED]);self.pulse(self.aux[-1])
        elif i==20:
            self.clear_aux();self.panel('뉴런만 보면 무엇을 놓칠까?',['특징 방향 ≠ 뉴런 좌표축']);self.pulse(f.axes)
        elif i==21:
            f.select(self,[0]);self.extra(f.projections(0));self.panel('하나의 뉴런을 관찰한다',['어떤 입력에 반응하는가?','Neuron 1의 활성화 h₁'])
        elif i==22:
            self.panel('고양이 → Neuron 1 반응',['F1 = 고양이 특징이라고 가정','“고양이 뉴런”이라고 불러도 될까?','가상 설명 예시'],[COLORS[0],INK,MUTED]);self.pulse(self.aux[-1])
        elif i==23:
            self.clear_aux();v=vectors(REGULAR)[:,0];end=f.point(v)
            self.extra(f.projections(0),DashedLine(end,f.point([0,v[1]]),color=COLORS[0],dash_length=.08),
                Line(f.origin,f.point([0,v[1]]),color=COLORS[0],stroke_width=7))
            self.panel('한 특징은 여러 뉴런에 걸친다',['F1 방향의 두 좌표 성분','h₁ ≠ 0     h₂ ≠ 0'],[COLORS[0],INK])
        elif i==24:
            self.clear_aux();f.select(self,range(5));self.extra(*[f.projections(j) for j in range(5)])
            self.panel('한 좌표에 여러 특징이 기여',['h₁ = Σᵢ xᵢ (vᵢ)₁','색 선분은 각 특징의 좌표 기여','양·음 성분을 모두 포함'],[INK,INK,MUTED])
        elif i==25:
            self.clear_aux();f.select(self,[0,4]);self.extra(f.projections(0),f.projections(4))
            self.remove(self.info);self.info=VGroup();self.extra(NeuronResponse(P))
            self.pulse(self.aux[-1].bars)
        elif i==26:
            self.clear_aux();self.panel('Polysemanticity · 다의성',['하나의 뉴런 → 여러 의미','고양이 F1 + 다른 특징 F5'],[INK,GOOD])
            self.extra(f.projections(0),f.projections(4));self.pulse(f.axes.x_axis)
        elif i==27:
            self.clear_aux();f.select(self,range(5));self.panel('다의성이 생기는 한 가지 이유',['Superposition → Polysemanticity','모든 다의성의 유일한 원인은 아님'],[GOOD,MUTED])
        elif i==28:
            self.panel('뉴런 개수 ≠ 특징 개수',['2개의 뉴런 좌표','5개의 특징 방향'],[MUTED,GOOD]);self.pulse(f.vectors)
        elif i==29:
            self.panel('좌표축에서 특징 방향으로',['뉴런별 반응에 더해','여러 뉴런에 걸친 방향을 본다']);self.pulse(f.vectors[0],f.vectors[4])
        elif i==30:
            self.panel('겹친 특징을 다시 분리하려면?',['의미 있는 방향을 찾는 문제','희소성 등 추가 가정이 필요','유일한 복원을 보장하지 않음'],[GOOD,INK,MUTED])
            endpoints=[f.point(v) for v in vectors(REGULAR).T]
            circles=VGroup(*[Circle(radius=.13,color=COLORS[j]).move_to(pt) for j,pt in enumerate(endpoints)])
            self.extra(circles);self.play(LaggedStart(*[Create(c) for c in circles],lag_ratio=.15),run_time=1)

class FeatureSuperposition(SuperpositionVideo):pass
class FeatureSuperpositionShorts(SuperpositionVideo):pass
