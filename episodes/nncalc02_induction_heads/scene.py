"""Two composed attention heads, rendered in native landscape and portrait layouts."""
import json
import os
import sys
import textwrap
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import txt,BG,INK,MUTED,ACCENT,GOOD,PRUNE,ZERO

config.pixel_width=int(os.environ.get('VIDEO_WIDTH','1920'))
config.pixel_height=int(os.environ.get('VIDEO_HEIGHT','1080'))
PORTRAIT=config.pixel_height>config.pixel_width
config.frame_width=9 if PORTRAIT else 16
config.frame_height=16 if PORTRAIT else 9
config.frame_rate=30;config.background_color=BG;config.disable_caching=True
HERE=Path(__file__).resolve().parent
CURRENT='#4CD9CB';PREVIOUS='#68ACFF';INDUCTION='#F7A65E';QK='#F3CF75';OV='#B39CFF'

def p(x,y):return np.array([x,y,0.])
def label(s,x=0,y=0,size=28,color=INK,width=14.6):return txt(s,size,color,width).move_to(p(x,y))
def card(s,x=0,y=0,w=3,h=.8,color=PREVIOUS,size=26):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,stroke_color=color,stroke_width=1.5,
        fill_color=color,fill_opacity=.06).move_to(p(x,y)),label(s,x,y,size,color,w-.24))
def arrow(a,b,color=MUTED):return Arrow(a,b,buff=.06,color=color,stroke_width=2,max_tip_length_to_length_ratio=.18)

class TokenSequence(VGroup):
    """Exactly five input positions; prediction slots are separate objects."""
    def __init__(self,y=1.8,portrait=False,tokens='ABCDA'):
        self.tokens=tokens;self.xs=[(i-2)*(1.35 if portrait else 2.25) for i in range(5)]
        self.y=y;self.cells=VGroup();self.indices=VGroup()
        for i,(x,s) in enumerate(zip(self.xs,tokens)):
            color=CURRENT if i==4 else OV if i==1 else INK
            self.cells.add(card(s,x,y,.91 if portrait else 1.18,.85,color,36))
            self.indices.add(label(str(i+1),x,y-.65,17,MUTED,1))
        super().__init__(self.cells,self.indices)

class PredictionSlot(VGroup):
    def __init__(self,x,y,w=2.8):
        self.value=label('?',x,y,36,ACCENT,w-.2)
        self.x=x;self.y=y
        super().__init__(DashedVMobject(RoundedRectangle(width=w,height=.95,corner_radius=.12,color=ACCENT),num_dashes=18).move_to(p(x,y)),
            self.value,label('다음 토큰 예측 · 입력 아님',x,y-.85,19,MUTED,max(w,4.4)))
    def predict(self,scene):scene.play(Transform(self.value,label('B',self.x,self.y,36,OV)),run_time=.5)

class AttentionArc(VGroup):
    def __init__(self,points,color=QK):
        self.points_logical=points
        self.line=VMobject(stroke_color=color,stroke_width=2.5).set_points_as_corners(points[:-1])
        self.tip=arrow(points[-2],points[-1],color)
        super().__init__(self.line,self.tip)

class ResidualStreamView(VGroup):
    """Original token identity retained; separate band for preceding-token features."""
    def __init__(self,row,y,portrait=False,revealed=True):
        self.previous=VGroup();self.current=row
        for i,(x,prev) in enumerate(zip(row.xs,['—','A','B','C','D'])):
            text=('앞 '+prev) if portrait else ('앞 토큰: '+prev)
            cell=card(text,x,y,1.2 if portrait else 1.85,.67,PREVIOUS,20 if portrait else 23)
            if not revealed:cell.set_opacity(0)
            self.previous.add(cell)
        super().__init__(self.previous)

class PreviousTokenHead(VGroup):
    def __init__(self,row,residual):
        self.logical_edges=[(i,i-1) for i in range(2,6)]
        self.row=row;self.residual=residual
        super().__init__()
    def transfer(self,scene,positions=(2,3,4,5)):
        for position in positions:
            i=position-1;source=self.row.cells[i-1];target=self.residual.previous[i]
            symbol=self.row.tokens[i-1]
            feature=label(symbol,*source.get_center()[:2],25,PREVIOUS,1)
            self.add(feature);scene.add(feature)
            target_actual=card('앞 '+symbol if scene.portrait else '앞 토큰: '+symbol,
                *target.get_center()[:2],1.2 if scene.portrait else 1.85,.67,PREVIOUS,20 if scene.portrait else 23)
            scene.play(Indicate(source,color=PREVIOUS),feature.animate.move_to(target),run_time=.45)
            scene.play(Transform(target,target_actual),FadeOut(feature),run_time=.18)

class InductionHead(VGroup):
    query_position=5
    selected_position=2
    def __init__(self):super().__init__()

class QKOVVisualizer:
    qk_edge=(5,2)
    ov_edge=(2,5)

class CircuitComposition(VGroup):
    def __init__(self,portrait=False):
        if portrait:
            coords=[(0,3.65),(0,2.0),(0,.3),(0,-1.4),(0,-3.1)]
            widths=[7,7,7,7,6.6]
        else:
            coords=[(-5.05,.8),(-1.7,.8),(2.1,.8),(5.35,.8),(2.1,-1.45)]
            widths=[3,3,3.7,2.5,5.4]
        texts=['Head 1\n이전 토큰 정보 전달','2번 위치\n현재 B + 앞 A','Head 2 · Induction\nQK: 현재 A → 앞 A','OV\nB 정보 전달','다음 토큰 B 예측에 기여']
        colors=[PREVIOUS,PREVIOUS,INDUCTION,OV,OV]
        self.blocks=VGroup(*[card(s,x,y,w,1.12 if not portrait else 1.0,c,22 if not portrait else 25)
            for s,(x,y),w,c in zip(texts,coords,widths,colors)])
        self.edges=VGroup()
        for i in range(4):
            source=self.blocks[i];target=self.blocks[i+1]
            if portrait:start=source.get_bottom();end=target.get_top()
            elif i<3:start=source.get_right();end=target.get_left()
            else:start=source.get_bottom();end=target.get_right()
            self.edges.add(arrow(start,end,QK if i==1 else OV if i>=2 else PREVIOUS))
        super().__init__(self.blocks,self.edges)

class TrainingEvolution(VGroup):
    def __init__(self,portrait=False):
        positions=[(0,3.2),(0,.8),(0,-1.6)] if portrait else [(-4.7,.5),(0,.5),(4.7,.5)]
        self.stages=VGroup()
        for (x,y),title,body,opacity in zip(positions,['초기','학습 중','형성 후'],
            ['회로가 불분명','Head 사이 연결 발달','반복 패턴 활용 개선'],[.2,.55,1]):
            item=VGroup(card(title,x,y+.6,3.7,.75,INDUCTION,27),
                label(body,x,y-.4,24,INK,5 if portrait else 4.1),
                Line(p(x-1.1,y-1),p(x+1.1,y-1),color=QK,stroke_width=3,stroke_opacity=opacity))
            self.stages.add(item)
        super().__init__(self.stages)

class HeadAblation(VGroup):
    def __init__(self,portrait=False):
        if portrait:a=(0,3);b=(0,.1)
        else:a=(-3.8,.8);b=(3.8,.8)
        self.intact=card('Head 출력 유지',*a,6,1.1,OV,29)
        self.removed=card('Head 출력 제거',*b,6,1.1,PRUNE,29)
        self.cut=Line(p(b[0]-2,b[1]-.7),p(b[0]+2,b[1]+.7),color=PRUNE,stroke_width=3)
        super().__init__(self.intact,self.removed,
            label('B 예측에 해당 경로가 기여',a[0],a[1]-1.2,25,OV,6.8),
            label('해당 경로의 기여 제거',b[0],b[1]-1.2,25,PRUNE,6.8))

class InductionVideo(Scene):
    def construct(self):
        self.portrait=PORTRAIT
        data=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
        assert data['script_approved'] and data['duration']==165
        if self.portrait:
            self.fixed=VGroup(label('신경망 내부의 계산  /  02',y=7.4,size=20,color=MUTED,width=7.6),
                label('AI는 반복 패턴을 찾는\n회로를 스스로 만든다',y=6.5,size=30,width=7.5),
                Line(p(-3.9,5.75),p(3.9,5.75),color=ZERO),
                RoundedRectangle(width=7.9,height=1.85,corner_radius=.1,stroke_width=0,fill_color='#14212D',fill_opacity=.95).move_to(p(0,-6.2)),
                label('대표 회로의 개념도 · Olsson et al., 2022',y=-7.45,size=15,color=MUTED,width=7.5))
        else:
            self.fixed=VGroup(label('신경망 내부의 계산  02',-5.1,4.08,18,MUTED,5),
                label('AI는 반복 패턴을 찾는 회로를 스스로 만든다',2.6,4.08,21,INK,9.5),
                Line(p(-7.4,3.65),p(7.4,3.65),color=ZERO),
                RoundedRectangle(width=15,height=1.04,corner_radius=.1,stroke_width=0,fill_color='#14212D',fill_opacity=.95).move_to(p(0,-3.65)),
                label('도식·학습 변화·제거 효과는 개념도',-4.5,-4.3,15,MUTED,6),
                label('Olsson et al. · Induction Heads (2022)',4.5,-4.3,15,MUTED,6))
        self.add(self.fixed);self.stage=VGroup();self.caption=VGroup()
        for k,seg in enumerate(data['segments']):
            self.to(seg['start'])
            for obj in list(self.mobjects):
                if obj is not self.fixed:self.remove(obj)
            self.stage=VGroup()
            heading=label(f'{k+1:02}  {seg["title"]}',y=5.25 if self.portrait else 3.12,
                size=24 if self.portrait else 30,color=ACCENT,width=7.7 if self.portrait else 14.5)
            self.add(heading)
            callbacks=self.build(k)
            self.caption=self.caption_obj(seg['cues'][0]['text']);self.add(self.caption)
            self.check_layout(k)
            self.play(FadeIn(self.stage,shift=UP*.06),run_time=.2)
            for j,cue in enumerate(seg['cues']):
                self.to(cue['start']);self.remove(self.caption)
                self.caption=self.caption_obj(cue['text']);self.add(self.caption)
                if j in callbacks:callbacks[j]()
                self.to(cue['end'])
        self.to(165)
    def caption_obj(self,s):
        obj=label(textwrap.fill(s,width=29 if self.portrait else 60,break_long_words=False,break_on_hyphens=False),
            y=-6.2 if self.portrait else -3.65,size=25 if self.portrait else 27,width=7.2 if self.portrait else 14.4)
        maxheight=1.5 if self.portrait else .88
        if obj.height>maxheight:obj.scale_to_fit_height(maxheight)
        return obj
    def to(self,target):
        frames=round(target*30)-round(self.time*30)
        if frames>0:self.wait(frames/30)
        elif frames < -10:raise RuntimeError(f'Timing overflow: {self.time} > {target}')
    def show(self,*objs):self.stage.add(*objs)
    def note(self,s):self.show(label(s,y=-4.85 if self.portrait else -2.75,size=17,color=MUTED,width=7.6 if self.portrait else 14.5))
    def pulse(self,*objs,color=ACCENT,duration=.6):self.play(*[Indicate(o,color=color,scale_factor=1.08) for o in objs],run_time=duration)
    def check_layout(self,k):
        for obj in self.stage:
            xmax,ymin,ymax=(4,-5.1,4.85) if self.portrait else (7.6,-3,2.75)
            if obj.get_left()[0]<-xmax or obj.get_right()[0]>xmax or obj.get_bottom()[1]<ymin or obj.get_top()[1]>ymax:
                raise ValueError(f'Scene {k+1} outside safe area: {obj}')
    def row(self,y=None):
        row=TokenSequence(y=y if y is not None else (3.4 if self.portrait else 1.6),portrait=self.portrait)
        self.show(row);return row
    def simple_prediction(self):
        row=self.row()
        slot=PredictionSlot(0,-2.45 if self.portrait else -1.0,3.1)
        self.show(slot);return row,slot
    def residual(self,revealed=True):
        row=self.row(y=3.55 if self.portrait else 1.6)
        view=ResidualStreamView(row,1.9 if self.portrait else .15,self.portrait,revealed)
        self.show(view);return row,view
    def qk_diagram(self):
        row,view=self.residual(True)
        x2,x5=row.xs[1],row.xs[4]
        q=card('Q: 현재 A · 위치 5',y=-1.2 if self.portrait else -1.3,w=6 if self.portrait else 5.3,color=CURRENT,size=25)
        points=[p(x5+.45,row.y),p(3.7 if self.portrait else 6.2,row.y),
            p(3.7 if self.portrait else 6.2,.3 if self.portrait else -.8),
            p(x2,.3 if self.portrait else -.8),p(x2,1.5 if self.portrait else -.2)]
        arc=AttentionArc(points,QK)
        self.show(q,arc,label('QK: 5 → 2',y=-2.75 if self.portrait else -2.15,size=28,color=QK,width=7))
        return row,view,q,arc
    def build(self,k):
        P=self.portrait;cb={}
        if k==0:
            row,slot=self.simple_prediction()
            self.note('입력은 A B C D A까지 · ?는 예측 칸')
            cb={1:lambda:self.play(LaggedStart(*[Indicate(c,color=CURRENT) for c in row.cells],lag_ratio=.16),run_time=1.2),
                2:lambda:self.pulse(slot,duration=.5)}
        elif k==1:
            row,slot=self.simple_prediction()
            link=CurvedArrow(row.cells[4].get_bottom(),row.cells[0].get_bottom(),angle=-PI/4,color=CURRENT)
            self.show(link)
            self.note('B는 반복 완성 예측 · 유일하게 강제되는 정답 아님')
            def predict():self.pulse(row.cells[0],row.cells[4]);self.pulse(row.cells[1],color=OV);slot.predict(self)
            cb={0:predict}
        elif k==2:
            self.row(y=3.4 if P else 1.8)
            first=card('Layer 1 · Attention',y=1.2 if P else .1,w=6,color=PREVIOUS)
            second=card('Layer 2 · Attention',y=-.8 if P else -1.25,w=6,color=INDUCTION)
            self.show(first,second,label('내부에서는 어떤 계산이 일어날까?',y=-3.3 if P else -2.35,size=27,color=ACCENT,width=7.3 if P else 12))
            cb={0:lambda:self.pulse(first,second)}
        elif k==3:
            row,slot=self.simple_prediction()
            link=CurvedArrow(row.cells[4].get_bottom(),row.cells[0].get_bottom(),angle=-PI/4,color=QK)
            self.show(link,label('과거 A를 찾아도 B 정보는 별개',y=.1 if P else -.12,size=27,color=ACCENT,width=7.5 if P else 14))
            self.note('Attention 참조 · 현재 위치 → 과거 위치')
            cb={0:lambda:self.pulse(row.cells[4]),1:lambda:self.pulse(row.cells[0],slot)}
        elif k==4:
            row=self.row()
            target=card('필요한 위치는 2번 B',y=.8 if P else -.1,w=6.5,color=OV,size=30)
            heads=VGroup(card('Head 1',-1.8,-1.2 if P else -1.5,3.1,.9,PREVIOUS),
                card('Head 2',1.8,-1.2 if P else -1.5,3.1,.9,INDUCTION))
            self.show(target,heads,label('현재 A → 과거 A 다음의 B',y=-3.4 if P else -2.4,size=27,color=ACCENT,width=7.3 if P else 14))
            cb={0:lambda:self.pulse(row.cells[1],target,color=OV),1:lambda:self.pulse(heads)}
        elif k==5:
            row,view=self.residual(False)
            head=PreviousTokenHead(row,view)
            self.show(head,card('Layer 1 · Previous Token Head',y=-.2 if P else -1.4,w=7 if P else 9,color=PREVIOUS,size=25),
                label('현재 위치에서 바로 앞 위치를 읽는다',y=-2 if P else -2.3,size=25,color=PREVIOUS,width=7.4 if P else 14))
            self.note('첫 위치는 시작 토큰·경계 처리 필요 · 여기서는 —')
            cb={0:lambda:head.transfer(self,(2,))}
        elif k==6:
            row,view=self.residual(False);head=PreviousTokenHead(row,view)
            self.show(head,label('토큰은 그대로 · 표현에 앞 정보 추가',y=-.1 if P else -1.35,size=27,color=PREVIOUS,width=7.3 if P else 13),
                label('B 위치: 현재 B + 앞 A',y=-2.15 if P else -2.25,size=29,color=OV,width=7.3 if P else 13))
            self.note('원래 토큰 정보가 지워지거나 위치가 옮겨지는 것이 아님')
            cb={0:lambda:head.transfer(self,(2,)),1:lambda:head.transfer(self,(3,4,5))}
        elif k==7:
            self.show(card('Position 2 · B 위치의 표현',y=3.6 if P else 1.85,w=7,color=OV,size=28),
                card('현재 토큰 정보: B',y=1.8 if P else .55,w=6.5,color=OV,size=30),
                card('이전 토큰 정보: A',y=.2 if P else -.65,w=6.5,color=PREVIOUS,size=30),
                card('이제 Layer 2 · Induction Head',y=-2.3 if P else -1.95,w=7.4 if P else 9,color=INDUCTION,size=25))
            cb={0:lambda:self.pulse(self.stage[-1],duration=.65)}
        elif k in (8,9):
            row,view,q,arc=self.qk_diagram()
            self.note('노란 선 = QK 위치 선택 · 현재 5번 → 과거 2번')
            cb={0:lambda:self.pulse(q,view.previous[1],row.cells[1],color=QK,duration=1.0 if k==8 else .6)}
        elif k==10:
            row=self.row(y=3.75 if P else 1.85)
            if P:coords=[(0,1.95),(0,.1),(0,-2.05)]
            else:coords=[(-4.6,-.1),(0,-.1),(4.6,-.1)]
            value=card('2번 B 위치\nV₂ · B 관련 특징',*coords[0],6 if P else 4,1.2,OV,25)
            current=card('W_O → 현재 5번 위치\n출력 표현에 B 정보 기여',*coords[1],7 if P else 4.4,1.2,OV,23)
            pred=card('다음 토큰 B 예측',*coords[2],6 if P else 4,1.0,OV,26)
            self.show(value,current,pred)
            for a,b in [(value,current),(current,pred)]:self.show(arrow(a.get_bottom() if P else a.get_right(),b.get_top() if P else b.get_left(),OV))
            self.note('보라색 = OV 정보 전달 · 2번 → 5번 · 예측 칸은 입력 아님')
            def flow():
                feature=card('B 정보',*coords[0],1.7,.5,OV,20);self.add(feature)
                self.play(feature.animate.move_to(current),run_time=.8);self.remove(feature)
                self.pulse(current,pred,color=OV)
            cb={0:flow}
        elif k==11:
            circ=CircuitComposition(P);self.show(circ)
            self.note('이전 정보 전달 → QK 위치 선택 → OV 정보 전달')
            cb={0:lambda:self.pulse(circ.blocks[1]),1:lambda:self.pulse(circ.blocks[0],color=PREVIOUS),
                2:lambda:self.pulse(circ.blocks[2],circ.blocks[3],color=INDUCTION)}
        elif k==12:
            examples=[('A B C D A','B'),('K M P K','M'),('7 4 9 7','4')]
            ys=[3.3,.7,-1.9] if P else [1.65,.2,-1.25]
            groups=VGroup()
            for (s,out),y in zip(examples,ys):
                groups.add(VGroup(card(s,-.4 if P else -2.3,y,5.7 if P else 7,.95,CURRENT,29),
                    label('→',2.75 if P else 2.2,y,30,MUTED,1),card(out,3.4 if P else 4,y,.75 if P else 1.2,.95,OV,29)))
            self.show(groups);self.note('같은 반복 완성 규칙의 예시 · 개별 모델의 측정 결과 아님')
            def examples_run():
                for group in groups:self.pulse(group,color=OV)
            cb={0:examples_run}
        elif k==13:
            first=card('Previous Token Head',y=3 if P else 1.25,w=7,color=PREVIOUS,size=28)
            second=card('Induction Head',y=.8 if P else -.2,w=7,color=INDUCTION,size=31)
            bracket=VGroup(first,second)
            self.show(bracket,arrow(first.get_bottom(),second.get_top(),QK),
                label('전체: Induction Circuit',y=-1.35 if P else -1.45,size=30,color=ACCENT,width=7.4 if P else 12),
                label('[A][B] … [A] → [B]',y=-3.2 if P else -2.4,size=30,color=OV,width=7.4 if P else 12))
            cb={0:lambda:self.pulse(second,duration=.6)}
        elif k==14:
            circ=CircuitComposition(P);self.show(circ)
            self.note('학습 목표: Next Token Prediction · Head별 역할을 직접 지시하지 않음')
            cb={0:lambda:self.pulse(circ.blocks[0],circ.blocks[2]),1:lambda:self.play(circ.edges.animate.set_stroke(width=4),run_time=1)}
        elif k==15:
            evo=TrainingEvolution(P);self.show(evo)
            self.note('학습 변화의 개념도 · 실제 학습 시점·수치를 재현한 그래프가 아님')
            cb={0:lambda:self.pulse(evo.stages[0],evo.stages[1]),1:lambda:self.pulse(evo.stages[1],evo.stages[2],color=INDUCTION)}
        elif k==16:
            ablation=HeadAblation(P);self.show(ablation)
            self.show(label('다른 Head·경로의 기여는 남을 수 있음',y=-3.4 if P else -2.1,size=25,color=ACCENT,width=7.3 if P else 14))
            self.note('개념적 출력 ablation · 반드시 B 오답이 된다는 뜻은 아님')
            cb={0:lambda:self.play(Create(ablation.cut),Indicate(ablation.removed,color=PRUNE),run_time=1)}
        elif k==17:
            circ=CircuitComposition(P);self.show(circ)
            self.note('모든 모델·모든 문맥 활용 능력에 동일 회로가 필수라는 뜻은 아님')
            cb={0:lambda:self.pulse(circ.blocks[2],color=MUTED),1:lambda:self.pulse(circ.blocks[1]),
                2:lambda:self.pulse(circ.edges,color=ACCENT),3:lambda:self.pulse(circ.blocks[0],circ.blocks[2]),
                4:lambda:self.pulse(circ,duration=.7)}
        elif k==18:
            if P:ys=[3.4,1.45,-.5]
            else:ys=[1.65,.35,-.95]
            blocks=VGroup(card('데이터 분포 변경',y=ys[0],w=7,color=ACCENT,size=28),
                card('새로 학습',y=ys[1],w=7,color=INDUCTION,size=28),
                card('회로 형성 시점·강도 비교?',y=ys[2],w=7.4 if P else 9,color=PREVIOUS,size=26))
            self.show(blocks)
            for a,b in zip(blocks,blocks[1:]):self.show(arrow(a.get_bottom(),b.get_top(),ACCENT))
            self.show(label('데이터로 회로의 형성에\n영향을 줄 수 있을까?' if P else '학습 데이터로 회로의 형성에 영향을 줄 수 있을까?',
                y=-3.2 if P else -2.25,size=29,color=ACCENT,width=7.4 if P else 14))
            cb={0:lambda:self.pulse(blocks[0]),1:lambda:self.pulse(blocks[1],blocks[2],duration=1)}
        return cb

class InductionHeads(InductionVideo):pass
class InductionHeadsShorts(InductionVideo):pass
