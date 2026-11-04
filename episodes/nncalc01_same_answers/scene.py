"""User-timed 164s landscape animation: answers, rules, and patterning."""
import json
import os
import sys
import textwrap
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import txt, BG, INK, MUTED, ACCENT, GOOD, PRUNE, ZERO
config.pixel_width=int(os.environ.get('VIDEO_WIDTH','1920'))
config.pixel_height=int(os.environ.get('VIDEO_HEIGHT','1080'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.background_color=BG;config.disable_caching=True
COUNT='#4CD9CB';NEST='#B39CFF';HERE=Path(__file__).resolve().parent

def p(x,y):return np.array([x,y,0.])
def t(s,x=0,y=0,size=28,color=INK,width=14.7):
    return txt(s,size,color,width).move_to(p(x,y))
def card(s,x=0,y=0,w=3,h=.8,color=COUNT,size=26,white=False):
    box=RoundedRectangle(width=w,height=h,corner_radius=.12,stroke_color=color,stroke_width=1.4,
        fill_color=INK if white else color,fill_opacity=.95 if white else .07).move_to(p(x,y))
    return VGroup(box,t(s,x,y,size,BG if white else color,w-.25))
def arr(x1,y1,x2,y2,color=MUTED):
    return Arrow(p(x1,y1),p(x2,y2),buff=.08,color=color,stroke_width=2,max_tip_length_to_length_ratio=.17)

class BracketSequence(VGroup):
    def __init__(self,s,x=0,y=0,color=INK,step=.72,scale=1):
        self.string=s
        cells=[]
        for i,c in enumerate(s):
            cx=x+(i-(len(s)-1)/2)*step*scale
            box=RoundedRectangle(width=.59*scale,height=.7*scale,corner_radius=.07,
                stroke_color=color,stroke_width=1.2,fill_color=color,fill_opacity=.05).move_to(p(cx,y))
            glyph=Text(c,font='Consolas',font_size=35*scale,color=color).move_to(box)
            cells.append(VGroup(box,glyph))
        super().__init__(*cells)

class CountingAlgorithm(VGroup):
    def __init__(self,s='()()',x=-3.8,y=.2):
        self.seq=BracketSequence(s,x,y+1.25,COUNT)
        self.open=t('0',x-1.05,y+.1,42,COUNT)
        self.close=t('0',x+1.05,y+.1,42,COUNT)
        self.answer=t('개수 비교',x,y-1.1,29,COUNT)
        self.x=x;self.y=y
        super().__init__(self.seq,self.open,self.close,self.answer,
            t('여는 괄호',x-1.05,y+.65,20,MUTED,2),t('닫는 괄호',x+1.05,y+.65,20,MUTED,2))
    def run(self,scene):
        opened=closed=0
        for i,c in enumerate(self.seq.string):
            if c=='(':opened+=1;obj=self.open;value=opened
            else:closed+=1;obj=self.close;value=closed
            scene.play(Indicate(self.seq[i],color=COUNT),Transform(obj,t(str(value),*obj.get_center()[:2],42,COUNT)),run_time=.4)
        ok=opened==closed
        scene.play(Transform(self.answer,t(f'{opened} = {closed}  ·  올바름' if ok else '개수 다름 · 실패',self.x,self.y-1.1,28,GOOD if ok else PRUNE)),run_time=.4)

class DepthTracker(VGroup):
    """Signed prefix depth; violation stays flagged even if final depth returns to 0."""
    def __init__(self,s='(())',x=3.8,y=.2):
        self.x=x;self.y=y;self.values=[0]
        for c in s:self.values.append(self.values[-1]+(1 if c=='(' else -1))
        self.seq=BracketSequence(s,x,y+1.25,NEST)
        self.current=t('깊이 0',x,y+.35,32,NEST)
        self.status=t('조건: 음수 금지 · 마지막 0',x,y-1.55,22,MUTED)
        self.depth_labels=VGroup(*[t(str(v),x+(i-1.5)*.72,y+.72,17,PRUNE if v<0 else NEST,1).set_opacity(0)
                                  for i,v in enumerate(self.values[1:])])
        self.path=VGroup()
        self.axes=VGroup(Line(self.point(0,0),self.point(len(s),0),color=ZERO),
            Line(self.point(0,-1),self.point(0,2),color=ZERO))
        self.dot=Dot(self.point(0,0),radius=.055,color=NEST)
        super().__init__(self.seq,self.current,self.status,self.axes,self.path,self.dot,self.depth_labels)
    def point(self,i,v):return p(self.x-1.65+i*.825,self.y-.85+v*.35)
    def run(self,scene,finish=True):
        for i,v in enumerate(self.values[1:],1):
            color=PRUNE if v<0 else NEST
            line=Line(self.point(i-1,self.values[i-1]),self.point(i,v),color=color,stroke_width=3)
            self.path.add(line)
            animations=[Create(line),self.dot.animate.move_to(self.point(i,v)).set_color(color),
                Transform(self.current,t(f'깊이 {v}',self.x,self.y+.35,32,color)),
                self.depth_labels[i-1].animate.set_opacity(1),Indicate(self.seq[i-1],color=color)]
            if v<0:animations.append(Transform(self.status,t('세 번째에서 −1 · 중첩 위반',self.x,self.y-1.55,22,PRUNE)))
            scene.play(*animations,run_time=.55)
            if v<0:
                scene.wait(.5)
        if finish:
            ok=min(self.values)>=0 and self.values[-1]==0
            scene.play(Transform(self.status,t('음수 없음 · 마지막 0  ✓' if ok else '한 번이라도 음수 → 올바르지 않음',
                self.x,self.y-1.55,23,GOOD if ok else PRUNE,width=6.6)),run_time=.35)

class NeuralNetwork(VGroup):
    def __init__(self,x=0,y=0,w=3.4,h=2,color=NEST):
        layers=[];edges=VGroup();nodes=VGroup()
        for layer in range(4):
            points=[p(x-w/2+layer*w/3,y+h/2-i*h/2) for i in range(3)]
            group=VGroup(*[Circle(radius=.085,stroke_color=color,fill_color=BG,fill_opacity=1,stroke_width=1.5).move_to(q) for q in points])
            layers.append(group);nodes.add(group)
            if layer:
                for n1 in layers[layer-1]:
                    for n2 in group:edges.add(Line(n1.get_center(),n2.get_center(),color=color,stroke_width=.8,stroke_opacity=.26))
        self.layers=layers;self.edges=edges
        super().__init__(edges,nodes)
    def pulse(self,scene,color=GOOD):
        for layer in self.layers:scene.play(Indicate(layer,color=color,scale_factor=1.18),run_time=.25)

class ModelPopulation(VGroup):
    """Uncalibrated illustrative icons; counts never represent paper statistics."""
    def __init__(self,x=0,y=0,colors=None):
        colors=colors or [COUNT,NEST,COUNT,NEST,COUNT,COUNT,NEST,COUNT]
        self.models=VGroup(*[card('NN',x+(i%4-1.5)*.78,y+(.5-i//4)*.8,.65,.58,c,19) for i,c in enumerate(colors)])
        super().__init__(self.models)

class DistributionWeighting(VGroup):
    def __init__(self,x=0,y=0):
        self.x=x;self.y=y;self.bars=VGroup();labels=VGroup()
        for i,s in enumerate(['()()','(())','((()']):
            yy=y+.8-i*.8
            labels.add(card(s,x-1.05,yy,1.25,.55,INK,23,True))
            self.bars.add(Rectangle(width=.9,height=.25,stroke_width=0,fill_color=ACCENT,fill_opacity=.85).move_to(p(x+.5,yy)))
        super().__init__(labels,self.bars)
    def reweight(self,scene):
        anim=[]
        for bar,width in zip(self.bars,[1.6,.45,1.2]):
            left=bar.get_left().copy()
            target=bar.copy().stretch_to_fit_width(width).move_to(left+RIGHT*width/2)
            anim.append(Transform(bar,target))
        scene.play(*anim,run_time=1.2)

class SameAnswersDifferentAlgorithms(Scene):
    DURATION=164
    def construct(self):
        data=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
        status=json.loads((HERE/'draft_status.json').read_text(encoding='utf-8'))
        assert status['script_approved'] and status['speech_timing_provided_for_this_revision']
        assert data['timing_basis']=='user_provided_cumulative_sentence_end_times'
        self.fixed=VGroup(t('신경망 내부의 계산  01',-5.25,4.08,18,MUTED,5),
            t('정답만 가르쳤는데, AI는 어떻게 풀이를 배울까?',2.45,4.08,21,INK,10),
            Line(p(-7.4,3.65),p(7.4,3.65),color=ZERO),
            RoundedRectangle(width=15,height=1.04,corner_radius=.1,stroke_width=0,fill_color='#14212D',fill_opacity=.95).move_to(p(0,-3.65)),
            t('내부 연결·모델 수·비율은 개념도',-4.9,-4.3,15,MUTED,6),
            t('Wang & Murfet · Patterning (2026)',4.7,-4.3,15,MUTED,6))
        self.add(self.fixed);self.stage=VGroup();self.heading=VGroup();self.caption=VGroup()
        for index,seg in enumerate(data['segments']):
            self.to(seg['start'])
            # Reset all nonpersistent objects, including completed transient paths.
            for obj in list(self.mobjects):
                if obj is not self.fixed:self.remove(obj)
            self.heading=t(f'{index+1:02}  {seg["title"]}',y=3.12,size=30,color=ACCENT)
            self.stage=VGroup();self.add(self.heading)
            callbacks=self.build(index)
            first=seg['cues'][0];self.caption=self.caption_obj(first['text']);self.add(self.caption)
            self.check_layout(index)
            self.play(FadeIn(self.stage,shift=UP*.08),run_time=.3)
            for local,cue in enumerate(seg['cues']):
                self.to(cue['start'])
                self.remove(self.caption);self.caption=self.caption_obj(cue['text']);self.add(self.caption)
                if local in callbacks:callbacks[local]()
                self.to(cue['end'])
        self.to(data['duration'])
    def caption_obj(self,s):
        lines=textwrap.fill(s,width=62,break_long_words=False,break_on_hyphens=False)
        obj=t(lines,y=-3.65,size=27,width=14.4)
        if obj.height>.88:obj.scale_to_fit_height(.88)
        return obj
    def to(self,target):
        frames=round(target*30)-round(self.time*30)
        if frames>0:self.wait(frames/30)
        elif frames < -12:raise RuntimeError(f'Timing overflow {self.time:.3f} > {target}')
    def show(self,*objs):self.stage.add(*objs)
    def note(self,s):self.show(t(s,y=-2.75,size=18,color=MUTED))
    def check_layout(self,k):
        for obj in self.stage:
            if obj.get_left()[0]<-7.6 or obj.get_right()[0]>7.6 or obj.get_top()[1]>2.7 or obj.get_bottom()[1]<-3.0:
                raise ValueError(f'Scene {k+1} outside content safe area: {obj}')
    def pulse(self,*objs,color=ACCENT):self.play(*[Indicate(o,color=color) for o in objs],run_time=.6)
    def build(self,k):
        cb={}
        if k==0:
            net=NeuralNetwork(0,.25)
            rows=VGroup()
            for i,(s,label,c) in enumerate([('()()','올바름',GOOD),('(())','올바름',GOOD),('(()','틀림',PRUNE)]):
                y=1.65-i*1.35
                rows.add(card(s,-5.2,y,2.2,.8,INK,32,True),card(label,5.2,y,2.2,.8,c,28))
            self.show(net,rows,arr(-3.9,.25,-2,.25),arr(2,.25,3.9,.25),t('입력 문자열',-5.2,2.35,22,MUTED),t('정답 라벨',5.2,2.35,22,MUTED))
            self.note('설명용 훈련 예시 · 중간 풀이 과정은 제공하지 않음')
            cb={0:lambda:net.pulse(self),1:lambda:self.pulse(rows[1],rows[5])}
        elif k==1:
            net=NeuralNetwork(0,.3,w=4.5,h=2.2)
            supplied=card('정답  ✓',-4.9,.3,3.3,1.25,GOOD,35)
            unknown=card('풀이 방법  ?',4.9,.3,3.3,1.25,ACCENT,33)
            self.show(net,supplied,unknown,arr(-3.2,.3,-2.4,.3),arr(2.4,.3,3.2,.3),
                t('개수 비교?',-1.2,-1.75,23,COUNT,3),t('순서 확인?',1.6,-1.75,23,NEST,3))
            self.note('중간 계산을 정답으로 제공하지 않는다')
            cb={0:lambda:self.pulse(unknown)}
        elif k==2:
            net=NeuralNetwork(-4.4,.65,w=3.3,h=1.8)
            pred=card('예측: 틀림',-.5,1.5,3,.8,PRUNE)
            truth=card('정답: 올바름',3.7,1.5,3.3,.8,GOOD)
            error=card('오차',1.6,-.05,2.2,.8,ACCENT)
            loop=CurvedArrow(p(.2,-.4),p(-4.3,-.7),angle=-TAU/5,color=ACCENT)
            rule1=card('계산 경로 A',-.7,-1.65,3.4,.8,COUNT)
            rule2=card('계산 경로 B',4,-1.65,3.4,.8,NEST)
            self.show(net,pred,truth,error,loop,rule1,rule2,t('가중치 업데이트',-5,-1.75,23,ACCENT,3.5))
            self.note('오차 감소와 연결선 변화는 학습 원리의 개념도')
            cb={0:lambda:self.play(Indicate(error),net.edges.animate.set_stroke(width=1.9,opacity=.65),run_time=1),
                1:lambda:net.pulse(self),2:lambda:self.pulse(rule1,rule2)}
        elif k==3:
            counter=CountingAlgorithm(x=0,y=.3)
            self.show(counter,t('알고리즘 A',-4.7,1.45,32,COUNT,4),
                t('순서는 검사하지 않는다',4.5,.3,26,MUTED,4),
                t('Equal-Count',-4.7,.45,24,COUNT,4))
            self.note('수학적으로 정의한 후보 규칙 · 실제 정답 기준은 올바른 중첩')
            cb={0:lambda:counter.run(self)}
        elif k==4:
            tracker=DepthTracker(x=1.7,y=.35)
            self.show(tracker,card('알고리즘 B · Nested',-4.5,1.35,4.4,.8,NEST),
                t('(  →  +1\n)  →  −1',-4.5,-.05,31,NEST,4),
                t('누적 깊이',1.7,2.25,25,NEST),t('모든 dₜ ≥ 0  그리고  dₙ = 0',-3.9,-1.8,26,GOOD,6))
            self.note('깊이를 설명하는 도식이며 신경망의 실제 스택 구현을 뜻하지 않음')
            cb={0:lambda:self.pulse(self.stage[1]),1:lambda:tracker.run(self),2:lambda:self.pulse(self.stage[4])}
        elif k==5:
            left=card('A · 개수 비교',-4.85,1.8,3.8,.8,COUNT)
            right=card('B · 중첩 확인',4.85,1.8,3.8,.8,NEST)
            rows=VGroup()
            for i,(s,result,c) in enumerate([('()()','수락',GOOD),('(())','수락',GOOD),('(()','거부',PRUNE),('())','거부',PRUNE)]):
                y=.9-i*.72
                rows.add(card(s,0,y,2.6,.56,INK,25,True),t(result,-4.85,y,24,c,3),t(result,4.85,y,24,c,3),
                    arr(-1.45,y,-3.2,y,COUNT),arr(1.45,y,3.2,y,NEST))
            common=t('훈련 예시 모두 정답',y=-2.2,size=32,color=GOOD)
            self.show(left,right,rows,common)
            self.note('설명용 훈련 예시 · 논문의 전체 데이터셋 재현 아님')
            cb={0:lambda:self.pulse(rows[0],rows[10]),1:lambda:self.pulse(common),2:lambda:self.pulse(left,right)}
        elif k==6:
            count=CountingAlgorithm('())(',x=-3.65,y=.15)
            depth=DepthTracker('())(',x=3.65,y=.15)
            self.show(count,depth,t('A · Equal-Count',-3.65,2.3,27,COUNT),t('B · Nested',3.65,2.3,27,NEST),
                Line(p(0,2.6),p(0,-2.2),color=ZERO))
            self.note('새 입력 / OOD:  ( ) ) (     ·     실제 정답은 올바르지 않음')
            for seq in (count.seq,depth.seq):
                for token in seq:token[0].set_stroke(color=ACCENT)
            cb={0:lambda:self.pulse(count.seq,depth.seq),1:lambda:count.run(self),2:lambda:depth.run(self)}
        elif k==7:
            top=card('훈련 예시 · 둘 다 정답',y=1.85,w=5.7,color=GOOD,size=30)
            a=card('개수 비교',-4.5,.15,3.8,.9,COUNT)
            b=card('중첩 확인',4.5,.15,3.8,.9,NEST)
            self.show(top,a,b,arr(-1.2,1.35,-4.5,.75,COUNT),arr(1.2,1.35,4.5,.75,NEST),
                card('새 입력: 올바름',-4.5,-1.1,4.3,.75,COUNT),card('새 입력: 올바르지 않음',4.5,-1.1,4.3,.75,PRUNE),
                t('같은 훈련 정답  ≠  같은 일반화 규칙',y=-2.35,size=34,color=ACCENT))
            cb={0:lambda:self.play(Create(self.stage[3]),Create(self.stage[4]),Indicate(self.stage[-1]),run_time=1.2)}
        elif k==8:
            pop=ModelPopulation(0,.4)
            self.show(card('같은 훈련 분포로 학습',y=2.1,w=7,color=GOOD,size=29),pop,
                arr(-1,-.5,-4,-1.2,COUNT),arr(1,-.5,4,-1.2,NEST),
                card('개수 비교에 대응하는 행동',-4.2,-1.8,5.5,.8,COUNT,25),
                card('중첩 판별에 대응하는 행동',4.2,-1.8,5.5,.8,NEST,25),
                t('Patterning · 괄호 분류 실험',-4.9,.4,25,INK,4.2))
            self.note('연구 결과의 개념도 · 모델 수와 색상 비율은 실제 통계가 아님')
            cb={0:lambda:self.pulse(self.stage[0]),1:lambda:self.play(LaggedStart(*[Indicate(m,color=m[0].get_stroke_color()) for m in pop.models],lag_ratio=.1),run_time=2)}
        elif k==9:
            net=NeuralNetwork(0,.5,w=5,h=2)
            codes=t('if    for    count',0,.5,35,MUTED,7)
            self.show(net,codes,card('가중치',-5,.5,2.8,.85,NEST),card('활성화',5,.5,2.8,.85,COUNT),
                t('학습된 계산 규칙',y=-1.5,size=36,color=ACCENT),
                t('입력 신호 → 층별 변환 → 계산된 출력',y=-2.35,size=26,color=INK))
            self.note('내부 연결과 신호는 개념도 · 논문에서 추출한 실제 회로 아님')
            cb={0:lambda:self.pulse(self.stage[4]),1:lambda:self.play(FadeOut(codes),run_time=.8),2:lambda:net.pulse(self)}
        elif k==10:
            net=NeuralNetwork(0,.1,w=2.7,h=1.6)
            boxes=[card('모델 구조',-4.8,1.65,3.4,.8,NEST),card('초기 가중치',4.8,1.65,3.4,.8,NEST),
                card('최적화 과정',-4.8,-1.25,3.4,.8,NEST),card('데이터 분포',4.8,-1.25,3.4,.8,ACCENT)]
            self.show(net,*boxes,arr(-3,1.3,-1.6,.55),arr(3,1.3,1.6,.55),arr(-3,-1,-1.6,-.4),arr(3,-1,1.6,-.4))
            self.note('학습 조건이 규칙 형성에 영향 · 각 요인의 효과를 모두 분리 검증했다는 뜻은 아님')
            def conditions():
                for box in boxes:self.pulse(box)
            cb={0:lambda:net.pulse(self),1:conditions}
        elif k==11:
            weighting=DistributionWeighting(-4.7,.15)
            training=card('다시 학습',0,.2,2.4,1.25,ACCENT,29)
            pop=ModelPopulation(4.45,.2,[COUNT,NEST,NEST,NEST,COUNT,NEST,NEST,COUNT])
            pop_target=pop.copy()
            pop.set_opacity(0)
            self.show(weighting,training,pop,t('정답 라벨은 유지',-4.8,1.9,28,INK,4.5),
                t('샘플 유형별 비중 조절',-4.8,-1.65,24,ACCENT,5),
                t('새로 학습한 모델 집단',4.5,1.9,27,INK,5),
                arr(-2.5,.2,-1.3,.2,ACCENT),arr(1.3,.2,2.7,.2,ACCENT),
                t('새 입력에서의 일반화 경향 변화',4.4,-1.65,23,NEST,5.7))
            self.note('개념도 · 예제별 막대 길이·모델 수·비율은 논문의 정량값이 아님')
            def weigh():
                weighting.reweight(self);self.pulse(training)
            cb={0:lambda:self.pulse(self.stage[3]),1:weigh,
                2:lambda:self.play(Transform(pop,pop_target),Indicate(self.stage[8]),run_time=1.3)}
        elif k==12:
            left=card('정답을 맞히는가?',-4,1.1,6,.95,GOOD,34)
            right=card('어떤 계산을 배우는가?',4,1.1,6,.95,NEST,32)
            self.show(left,right,t('훈련 목표와 예측 성능',-4,-.15,28,GOOD,6),
                t('학습된 규칙과 일반화',4,-.15,28,NEST,6),
                t('입력 · 정답',-4,-1.5,27,INK,5),
                card('데이터 분포 → 학습 → 계산 경향',4,-1.5,6.5,.8,ACCENT,24))
            self.note('데이터는 정답 일치뿐 아니라 어떤 풀이가 형성되는지에도 영향을 줄 수 있다')
            cb={0:lambda:self.pulse(left),1:lambda:self.pulse(right,self.stage[5])}
        elif k==13:
            weighting=DistributionWeighting(-5.2,.15)
            training=card('분포 변경\n다시 학습',-1.4,.2,2.5,1.5,ACCENT,26)
            pop=ModelPopulation(2.1,.2,[NEST,COUNT,NEST,NEST,NEST,COUNT,NEST,NEST])
            pop_target=pop.copy()
            pop.set_opacity(0)
            paths=VGroup(arr(4,.4,6.3,1.35,COUNT),arr(4,-.2,6.3,-1.1,NEST))
            self.show(weighting,training,pop,paths,t('계산 방법의 형성 경향',3.25,2.35,25,NEST,6.5),
                t('Patterning: The Dual of Interpretability',y=-1.85,size=29,color=ACCENT),
                t('정답을 지정하는 것  ≠  풀이까지 지정하는 것',y=-2.65,size=28,color=INK),
                t('개수 비교',6.3,1.75,20,COUNT,2.4),t('중첩 확인',6.3,-1.4,20,NEST,2.4))
            def retrain():
                weighting.reweight(self);self.pulse(training);self.play(Transform(pop,pop_target),run_time=.6)
            cb={0:retrain,1:lambda:self.pulse(self.stage[5]),2:lambda:self.pulse(self.stage[6])}
        return cb
