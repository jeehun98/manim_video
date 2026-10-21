"""Probe versus intervention: an explicitly schematic research workflow."""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from visual_library.manim import configure_vertical, txt, BG, INK, MUTED, WEIGHT, PRUNE, SPARSE, ACCENT, GOOD, ZERO

configure_vertical()
config.disable_caching = True
HERE = Path(__file__).resolve().parent

def p(x, y):
    return np.array([x, y, 0.0])

def t(s, x=0, y=0, size=28, color=INK, width=7.7):
    return txt(s, size, color, width).move_to(p(x, y))

def card(title, x=0, y=0, w=3.3, h=1.3, color=WEIGHT, size=27):
    return VGroup(RoundedRectangle(width=w, height=h, corner_radius=.16,
                    stroke_color=color, stroke_width=1.6, fill_color=color, fill_opacity=.07).move_to(p(x,y)),
                  t(title,x,y,size,color,w-.3))

def arrow(x1,y1,x2,y2,color=MUTED):
    return Arrow(p(x1,y1),p(x2,y2),buff=.1,color=color,stroke_width=2.2,max_tip_length_to_length_ratio=.15)

def vector(x,y, values=None, color=SPARSE):
    values = values or [.25,.8,.45,.65,.3,.85]
    return VGroup(*[Rectangle(width=.48,height=.5,stroke_color=color,stroke_width=1,
                    fill_color=color,fill_opacity=v).move_to(p(x+(j-2.5)*.53,y)) for j,v in enumerate(values)])

def tokens(s,y=2.8,color=WEIGHT):
    return VGroup(*[card(c, (i-(len(s)-1)/2)*1.2,y,.92,.95,color,40) for i,c in enumerate(s)])

def wrapped(s,limit=29):
    lines=[]; line=''
    for word in s.split():
        if line and len(line)+len(word)+1>limit:
            lines.append(line);line=word
        else:
            line=(line+' '+word).strip()
    if line: lines.append(line)
    return '\n'.join(lines)

class SameAnswersDifferentAlgorithms(Scene):
    DURATION = 172

    def construct(self):
        data=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
        self.stage=VGroup();self.caption=VGroup();self.heading=VGroup()
        self.add(t('신경망 내부의 계산  /  01',y=7.4,size=20,color=MUTED),
                 t('같은 정답, 다른 알고리즘',y=6.65,size=34),
                 Line(p(-3.9,6.05),p(3.9,6.05),color=ZERO),
                 t('교육용 개념도 · 실제 모델의 측정 결과 아님',y=-7.5,size=17,color=MUTED),
                 RoundedRectangle(width=8.15,height=2.05,corner_radius=.15,stroke_width=0,
                     fill_color='#101F2B',fill_opacity=.9).move_to(p(0,-6.1)))
        for k,seg in enumerate(data['segments']):
            self.remove(self.caption)
            if self.stage.submobjects:
                self.play(FadeOut(self.stage),FadeOut(self.heading),run_time=.25)
            self.stage=VGroup()
            self.heading=t(f'{k+1:02}  {seg["title"]}',y=5.35,size=27,color=ACCENT)
            self.add(self.heading)
            animations=self.build(k)
            self.play(FadeIn(self.stage,shift=UP*.1),run_time=.35)
            for j,cue in enumerate(seg['cues']):
                self.to(cue['start'])
                self.remove(self.caption)
                self.caption=t(wrapped(cue['text']),y=-6.1,size=25,width=7.5)
                self.add(self.caption)
                if j<len(animations):
                    self.play(*animations[j],run_time=.7)
                self.to(cue['end'])
        self.to(data['duration'])

    def to(self,target):
        frames=round(target*config.frame_rate)-round(self.time*config.frame_rate)
        # Caption boundaries can coincide with the short section transition.
        if frames>0: self.wait(frames/config.frame_rate)
        elif frames < -33: raise RuntimeError(f'timing overflow: {self.time} > {target}')

    def addstage(self,*items):
        self.stage.add(*items)

    def build(self,k):
        a=[]
        if k==0:
            inp=tokens('()()',3.65)
            left=card('모델 A',-2,1.1,color=WEIGHT)
            right=card('모델 B',2,1.1,color=SPARSE)
            out1=card('정답',-2,-1.7,color=GOOD)
            out2=card('정답',2,-1.7,color=GOOD)
            self.addstage(inp,left,right,out1,out2,arrow(-1.4,2.95,-2,1.85),arrow(1.4,2.95,2,1.85),
                          arrow(-2,.35,-2,-.95),arrow(2,.35,2,-.95),
                          t('같은 답 → 같은 계산?',y=-3.65,size=33,color=ACCENT))
            a=[[Indicate(out1),Indicate(out2)],[Circumscribe(left,color=ACCENT),Circumscribe(right,color=ACCENT)]]
        elif k==1:
            self.addstage(card('A · 개수만 비교',y=3.4,w=6.9,color=WEIGHT),
                t('( 개수 = ) 개수',y=2.25,size=34,color=WEIGHT),
                card('B · 순서까지 확인',y=.55,w=6.9,color=SPARSE),
                t('열기 전에 닫지 않는다',y=-.65,size=29),
                t('끝에는 열린 괄호가 남지 않는다',y=-1.65,size=28),
                t('실제 정답 기준 = 올바른 중첩',y=-3.6,size=24,color=GOOD))
            a=[[Indicate(self.stage[1])],[Indicate(self.stage[3]),Indicate(self.stage[4])]]
        elif k==2:
            rows=VGroup(t('훈련 입력       A       B',y=4,size=26,color=MUTED))
            for i,(s,v) in enumerate([('()()','통과'),('(())','통과'),('(()','실패'),('())','실패')]):
                rows.add(t(f'{s}          {v}      {v}',y=3.05-i*.7,size=27,color=GOOD))
            new=tokens('())(',-1.15,color=ACCENT)
            self.addstage(rows,t('훈련 정확도 100% · 둘 다 일치',y=.05,size=25,color=GOOD),new,
                card('A · 통과',-2,-3.05,color=WEIGHT),card('B · 실패',2,-3.05,color=PRUNE))
            a=[[Circumscribe(rows,color=GOOD)],[Indicate(new),Indicate(self.stage[-1])]]
        elif k==3:
            row=tokens('(())',3.35)
            counts=VGroup(*[t(v,(i-1.5)*1.2,1.7,34,GOOD) for i,v in enumerate(['1','2','1','0'])])
            cursor=SurroundingRectangle(row[0],color=ACCENT,buff=.08)
            self.addstage(row,counts,cursor,t('여는 괄호  +1',-1.9,-.15,28,WEIGHT,3.5),
                t('닫는 괄호  −1',1.9,-.15,28,PRUNE,3.5),
                card('누적 깊이 dₜ',y=-2,w=6.6,color=GOOD,size=34),
                t('각 위치까지 열린 수 − 닫힌 수',y=-3.45,size=25,color=MUTED))
            a=[[Indicate(row)],[Indicate(counts)],[Transform(cursor,SurroundingRectangle(row[3],color=ACCENT,buff=.08))]]
        elif k==4:
            axis=Axes(x_range=[0,4,1],y_range=[-1,2,1],x_length=6.5,y_length=3.7,
                axis_config={'color':MUTED,'stroke_width':1.5,'include_tip':False}).move_to(p(0,.5))
            # Labels explicitly mark depth and token position, including t=0.
            labels=VGroup(*[t(str(i),*axis.c2p(i,0)[:2]+np.array([0,-.35]),size=19,color=MUTED) for i in range(5)])
            ys=VGroup(*[t(str(i),*axis.c2p(0,i)[:2]+np.array([-.4,0]),size=19,color=MUTED) for i in [-1,1,2]])
            paths=[];dots=[]
            for vals,color in [([0,1,2,1,0],WEIGHT),([0,1,0,-1,0],PRUNE)]:
                path=VMobject(color=color,stroke_width=4).set_points_as_corners([axis.c2p(i,v) for i,v in enumerate(vals)])
                paths.append(path)
                dots.append(VGroup(*[Dot(axis.c2p(i,v),radius=.07,color=color) for i,v in enumerate(vals)]))
            low=Circle(radius=.22,color=ACCENT).move_to(axis.c2p(3,-1))
            self.addstage(axis,labels,ys,*paths,*dots,low,t('(())',-1.8,3.8,35,WEIGHT),t('())(',1.8,3.8,35,PRUNE),
                t('누적 깊이',-2.6,3.05,22,MUTED,3),
                t('문자 위치 t',2.1,-2.25,22,MUTED,3),
                t('둘 다 마지막 0',y=-3.25,size=30,color=GOOD),t('())( 는 세 번째에서 −1',y=-4.15,size=26,color=PRUNE))
            a=[[Indicate(dots[0][-1]),Indicate(dots[1][-1])],[Indicate(low)],[Circumscribe(self.stage[-1],color=PRUNE)]]
        elif k==5:
            self.addstage(card('개수 규칙',y=3.5,w=6.7,color=WEIGHT),
                t('마지막 깊이 dₙ = 0',y=2.3,size=34,color=WEIGHT),
                card('중첩 규칙',y=.75,w=6.7,color=SPARSE),
                t('dₙ = 0  그리고  모든 dₜ ≥ 0',y=-.55,size=31,color=SPARSE),
                t('중간에 음수가 된 적이 있는가?',y=-1.6,size=26),
                card('깊이를 표현 ≠ 중첩 판별에 사용',y=-3.45,w=7.4,color=ACCENT,size=25))
            a=[[Indicate(self.stage[1])],[Indicate(self.stage[3])],[Indicate(self.stage[-1])]]
        elif k==6:
            self.addstage(tokens('(())',3.9))
            layers=VGroup()
            for layer in range(3):
                for pos in range(4):
                    layers.add(card('',(pos-1.5)*1.55,2.35-layer*1.35,1.05,.65,SPARSE))
            self.addstage(layers,t('층 ℓ',-3.65,1,22,MUTED,1),
                t('각 위치의 활성화 벡터',y=-1.55,size=27,color=SPARSE))
            h=vector(0,-2.85)
            self.addstage(h,t('hₜ · 특정 층, 특정 위치',y=-4,size=27,color=SPARSE))
            a=[[LaggedStart(*[Indicate(o,color=ACCENT) for o in layers],lag_ratio=.03)],
               [Circumscribe(layers[6],color=ACCENT),Indicate(h)]]
        elif k==7:
            v=vector(0,3.4)
            self.addstage(v,t('고정된 신경망의 hₜ',y=4.3,size=25,color=SPARSE),
                arrow(0,2.95,0,1.95),card('선형 Probe',y=1.2,w=5.8,color=WEIGHT,size=32),
                t('d̂ₜ = wᵀ hₜ + b',y=-.15,size=39,color=WEIGHT),
                arrow(0,-.7,0,-1.35),card('목표: 실제 깊이 dₜ',y=-2.1,w=6,color=GOOD),
                t('학습하는 것은 w, b 뿐',y=-3.55,size=28,color=ACCENT),
                t('원래 모델의 가중치는 고정',y=-4.25,size=23,color=MUTED))
            a=[[Indicate(self.stage[3])],[Indicate(self.stage[7])],[Indicate(self.stage[6])]]
        elif k==8:
            self.addstage(card('Probe 학습용 문자열',y=3.7,w=6.9,color=WEIGHT),
                t('()()    (())    (()())',y=2.6,size=31,color=WEIGHT),
                Line(p(-3.4,1.65),p(3.4,1.65),color=ZERO),
                card('별도의 평가용 문자열',y=.65,w=6.9,color=GOOD),
                t('((()))    ()(())',y=-.45,size=32,color=GOOD),
                t('예측 깊이 ↔ 실제 깊이',y=-1.75,size=30),
                card('비교: 위치만 쓰는 기준 모델',y=-3.1,w=7.2,color=ACCENT,size=25),
                t('평가 절차 예시 · 정확도 수치 미제시',y=-4.3,size=20,color=MUTED))
            a=[[Indicate(self.stage[3]),Indicate(self.stage[5])],[Indicate(self.stage[6])]]
        elif k==9:
            v=vector(0,3.4)
            probe=card('Probe',-2,1.3,color=WEIGHT)
            final=card('원래 판별기',2,1.3,color=SPARSE)
            self.addstage(v,probe,final,arrow(-.7,3,-2,2),arrow(.7,3,2,2),
                card('깊이 예측',-2,-1.15,color=WEIGHT),card('정답 판별',2,-1.15,color=SPARSE),
                arrow(-2,.55,-2,-.4),arrow(2,.55,2,-.4),
                t('서로 다른 가중치 · 서로 다른 경로',y=-2.75,size=26,color=MUTED),
                t('읽을 수 있다 ≠ 사용한다',y=-4,size=34,color=ACCENT))
            a=[[Indicate(probe),Indicate(final)],[Indicate(self.stage[-1])]]
        elif k==10:
            before=vector(0,3.3)
            after=vector(0,.35,[.25,.8,.9,.65,.3,.85])
            self.addstage(before,t('원래 활성화 hₜ',y=4.2,size=27,color=SPARSE),
                arrow(0,2.85,0,1.2,PRUNE),after,
                t('h′ₜ = hₜ + δ',y=-.7,size=36,color=PRUNE),
                arrow(0,-1.3,0,-1.95),card('원래 모델의 나머지 계산',y=-2.7,w=7,color=SPARSE),
                t('δ · 깊이 관련 성분을 겨냥한 조작',y=-4.1,size=24,color=ACCENT))
            a=[[Indicate(after[2],color=PRUNE)],[Circumscribe(self.stage[4],color=PRUNE)],[Indicate(self.stage[6])]]
        elif k==11:
            self.addstage(tokens('())(',3.8,color=ACCENT),
                t('입력 문자열은 그대로',y=2.65,size=27,color=ACCENT),
                card('원래 hₜ',-2,.85,color=SPARSE),card('바꾼 h′ₜ',2,.85,color=PRUNE),
                arrow(-2,.1,-2,-.95),arrow(2,.1,2,-.95),
                card('수락 점수 s',-2,-1.7,color=SPARSE),card('수락 점수 s′',2,-1.7,color=PRUNE),
                t('실험 전에: 가설이 예측하는 변화는?',y=-3.3,size=27,color=GOOD),
                t('s′ − s 를 측정 · 방향은 가설에 따라 결정',y=-4.15,size=22,color=MUTED))
            a=[[Indicate(self.stage[3])],[Indicate(self.stage[0])],[Indicate(self.stage[8])]]
        elif k==12:
            self.addstage(t('출력이 바뀐 이유는 무엇일까?',y=4,size=30),
                card('조작 없음',y=2.65,w=6.9,color=MUTED),t('원래 출력과 비교하는 기준',y=1.7,size=23,color=MUTED),
                card('깊이 관련 방향 조작 δ',y=.3,w=6.9,color=PRUNE),
                card('같은 크기 · 무관한 방향 조작',y=-1.75,w=6.9,color=WEIGHT,size=25),
                t('‖δ깊이‖ = ‖δ대조‖',y=-2.85,size=28,color=ACCENT),
                t('일반적인 손상 효과를 구별한다',y=-4.15,size=26,color=GOOD))
            a=[[Indicate(self.stage[3])],[Indicate(self.stage[4])],[Indicate(self.stage[1]),Indicate(self.stage[5])]]
        elif k==13:
            self.addstage(t('여러 입력에서 반복 검증',y=4.05,size=31,color=GOOD))
            for i,s in enumerate(['(())','()()','())(']):
                self.addstage(card(s,-2.6,2.6-i*1.35,1.7,.85,SPARSE,30),
                    arrow(-1.6,2.6-i*1.35,-.75,2.6-i*1.35),
                    card('가설의 예측 ↔ 관찰된 변화',1.25,2.6-i*1.35,4.9,.9,GOOD,23))
            self.addstage(t('대조 조작과도 차이가 있는가?',y=-2.2,size=27,color=WEIGHT),
                card('계산 기여에 관한 더 강한 증거',y=-3.8,w=7.4,color=ACCENT,size=25))
            a=[[Indicate(self.stage[3]),Indicate(self.stage[6]),Indicate(self.stage[9])],[Indicate(self.stage[-1])]]
        elif k==14:
            self.addstage(card('개입의 효과 ≠ 알고리즘 전체의 증명',y=3.6,w=7.6,color=ACCENT,size=25),
                card('깊이 정보',-1.85,1.45,3.2,1.1,PRUNE),card('다른 정보',1.85,1.45,3.2,1.1,WEIGHT),
                t('한 조작이 둘을 함께 바꿀 수도 있다',y=.15,size=26,color=MUTED),
                arrow(-1.85,-.55,-1.85,-1.35,PRUNE),arrow(1.85,-.55,1.85,-1.35,WEIGHT),
                card('평소 경로',-1.85,-2.05,3.2,1.1,SPARSE),card('잠든 경로',1.85,-2.05,3.2,1.1,MUTED),
                t('평소 쓰지 않던 경로를 켰을 가능성',y=-3.65,size=26,color=PRUNE))
            a=[[Indicate(self.stage[0])],[Indicate(self.stage[1]),Indicate(self.stage[2])],[Indicate(self.stage[7])]]
        elif k==15:
            self.addstage(card('Probe',y=3.6,w=6.8,color=WEIGHT,size=36),
                t('무엇을 읽을 수 있는가?',y=2.35,size=32,color=WEIGHT),
                card('Intervention',y=.65,w=6.8,color=PRUNE,size=34),
                t('무엇을 바꾸면 계산이 달라지는가?',y=-.65,size=29,color=PRUNE),
                Line(p(-3.4,-1.85),p(3.4,-1.85),color=ZERO),
                t('정보의 존재',-1.9,-3,30,WEIGHT,3.5),t('≠',0,-3,40,ACCENT,1),
                t('계산의 역할',1.9,-3,30,PRUNE,3.5),
                t('관찰에서 가설로, 가설에서 개입으로',y=-4.2,size=24,color=GOOD))
            a=[[Indicate(self.stage[1])],[Indicate(self.stage[3])],[Indicate(self.stage[6])]]
        # Every artwork item must remain inside the stage safe area.
        for item in self.stage:
            if item.get_left()[0] < -4.05 or item.get_right()[0] > 4.05 or item.get_top()[1] > 4.85 or item.get_bottom()[1] < -4.8:
                raise ValueError(f'Artwork outside safe area, segment {k+1}: {item}')
        return a
