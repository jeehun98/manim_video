"""One visual vocabulary: fact identity, repetitions, loss gauge and selection."""
from manim import *
from visual_library.manim import FONT,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD
def text(s,x=0,y=0,size=25,color=INK,width=7.6):
    o=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.2)
    if o.width>width:o.scale_to_fit_width(width)
    return o.move_to([x,y,0])
COLORS={'A':WEIGHT,'B':GOOD,'C':PRUNE,'D':SPARSE}
FACTS={'A':'인물 A · 출생지','B':'도시 B · 설립 연도','C':'작품 C · 작가','D':'별 D · 발견 연도'}
class FactCard(VGroup):
    def __init__(self,fact_id='A',loss=.15,frequency=1,selection_probability=None,compact=False,**kwargs):
        super().__init__(**kwargs)
        self.fact_id=fact_id;self.loss=loss;self.frequency=frequency
        self.selection_probability=(loss if loss<=1 else 0) if selection_probability is None else selection_probability
        c=COLORS[fact_id];w,h=(1.3,.78) if compact else (2.1,1.45)
        self.add(RoundedRectangle(width=w,height=h,corner_radius=.09,color=c,fill_color=BG,fill_opacity=1,stroke_width=2),text(fact_id,y=.12 if compact else .38,size=24,color=c))
        if compact:
            self[1].shift(LEFT*.32)
            self.add(text(f'{loss:.2f}',x=.27,y=.12,size=13,color=MUTED))
        else:self.add(text(FACTS[fact_id],y=-.04,size=16,width=w-.2))
        gy=-.2 if compact else -.4
        self.add(Line([-w*.36,gy,0],[w*.36,gy,0],color=MUTED,stroke_width=4),Line([-w*.36,gy,0],[-w*.36+w*.72*min(loss/1.4,1),gy,0],color=c,stroke_width=4))
def stack(fid,n,x,y,loss=.15):
    return VGroup(*[FactCard(fid,loss,n,compact=True).move_to([x+(j%2)*.12,y+j*.16,0]) for j in range(n)])
def feedback():
    cards=stack('A',4,-2.5,2.9)
    model=RoundedRectangle(width=2.1,height=1.3,color=SPARSE,fill_color=BG,fill_opacity=1).move_to([0,2.8,0])
    gauge=VGroup(Line([1.8,2.45,0],[3.6,2.45,0],color=MUTED,stroke_width=10),Line([1.8,2.45,0],[2.8,2.45,0],color=ACCENT,stroke_width=10),text('Loss',2.7,3.2,color=ACCENT))
    gate=RoundedRectangle(width=6.9,height=1.1,color=ACCENT,fill_color=BG,fill_opacity=1).move_to([0,-.1,0])
    moving=FactCard('B',.7,compact=True).move_to([-2.5,1.1,0])
    p=VGroup(cards,model,text('현재 모델',0,2.8,size=23,color=SPARSE),gauge,Arrow([-1.7,2.8,0],[-1.1,2.8,0],buff=.03,color=MUTED),Arrow([1.1,2.8,0],[1.65,2.8,0],buff=.03,color=MUTED),gate,text('손실 기반 필터',0,-.1,color=ACCENT),Arrow([2.7,1.95,0],[2.7,.5,0],color=ACCENT,buff=.05),text('Training Data',-2.5,4,size=22,color=MUTED),moving,text('선택된 카드로 다시 학습',0,-3.25,size=29,color=GOOD),text('카드 = 서로 다른 사실 · 게이지 = 현재 손실',0,-4.4,size=20,color=MUTED))
    route=CubicBezier([-.7,-2.1,0],[-4.1,-2.1,0],[-4.1,2.45,0],[-1.15,2.45,0],color=GOOD,stroke_width=2,fill_opacity=0)
    p.add(route,Arrow([-1.55,2.45,0],[-1.12,2.45,0],color=GOOD,buff=0,stroke_width=2))
    p.moving=moving;p.destination=[0,-2.1,0]
    return p
def comparison():
    p=VGroup(text('같은 크기의 모델',0,4,size=30,color=ACCENT),text('모두 학습',-1.9,3.1,color=WEIGHT),text('선택해 학습',1.9,3.1,color=GOOD))
    for x,c in [(-1.9,WEIGHT),(1.9,GOOD)]:
        p.add(RoundedRectangle(width=2.5,height=1.2,color=c).move_to([x,1,0]),text('모델',x,1,color=c))
    p.add(stack('A',4,-1.9,2.05),stack('B',2,1.9,2.2))
    checks=VGroup()
    for side,ids in [(-1.9,'AB'),(1.9,'ABCD')]:
        for j,fid in enumerate(ids):
            xx=side+(-.65 if j%2==0 else .65);yy=-1-j//2*1.1
            checks.add(text(fid+' ✓',xx,yy,size=30,color=GOOD))
    p.add(checks,text('더 많은 서로 다른 사실',0,-3.5,size=30,color=GOOD),text('비교 원리의 개념도 · 실제 측정 개수가 아님',0,-4.5,size=20,color=MUTED))
    p.checks=checks;return p
def loss_axis(focus=None):
    p=VGroup(Line([-3.5,-.1,0],[3.5,-.1,0],color=MUTED),text('Low Loss',-2.7,-.7,color=WEIGHT),text('High Loss',2.7,-.7,color=PRUNE),text('손실 순으로 정렬',0,4,size=29,color=ACCENT))
    cards=VGroup()
    for fid,x,loss,n in [('A',-2.7,.15,4),('B',0,.8,2),('C',2.7,1.3,1)]:
        st=stack(fid,n,x,1.15,loss);cards.add(st)
    p.add(cards,text('낮은 손실',-2.7,-1.8,size=24,color=WEIGHT),text('임계값 이하',0,-1.8,size=24,color=GOOD),text('임계값 초과',2.7,-1.8,size=24,color=PRUNE))
    if focus=='A':p.add(text('반복 등장  또는  쉽게 예측 가능',0,-3,size=29,color=WEIGHT))
    elif focus=='C':p.add(text('드물게 등장  또는  예측하기 어려움',0,-3,size=29,color=PRUNE))
    else:p.add(text('카드의 반복 = 같은 사실의 등장 횟수',0,-3,size=25,color=MUTED))
    p.add(text('손실만으로 빈도나 난도를 확정하지 않음',0,-4.4,size=22,color=MUTED))
    p.cards=cards;p.focus=cards[0 if focus=='A' else 2];return p
def filter_panel():
    p=VGroup(text('일부만 선택',-2.6,4,size=24,color=WEIGHT),text('상대적으로 유지',0,4,size=24,color=GOOD),text('선택 제외',2.6,4,size=24,color=PRUNE))
    cards=VGroup();dest=[];keep=[]
    for fid,x,loss,n,selected in [('A',-2.6,.15,5,1),('B',0,.8,4,3),('C',2.6,1.3,2,0)]:
        for j in range(n):
            c=FactCard(fid,loss,n,compact=True).move_to([x+(j%2)*.14,2+j*.18,0]);cards.add(c)
            keep.append(j<selected);dest.append([x+(j%2)*.14,-1.8+j*.2,0] if j<selected else [x+(j%2)*.14,-.45+j*.1,0])
    p.add(RoundedRectangle(width=7.8,height=.8,corner_radius=.12,color=ACCENT,fill_color=BG,fill_opacity=1).move_to([0,.45,0]),text('LossHF · 확률적 필터',0,.45,color=ACCENT),cards,text('통과한 카드 → 다음 학습',0,-3.2,size=28,color=GOOD),text('동일 사실의 반복 일부만 남음 · 원본 영구 삭제 아님',0,-4.1,size=20,color=MUTED),text('설명용 선택 예시 · 매번 결과는 달라질 수 있음',0,-4.65,size=19,color=MUTED))
    p.cards=cards;p.destinations=dest;p.keep=keep
    return p
def repeat_count():
    p=VGroup(text('반복 학습 횟수',-1.9,4,size=27,color=WEIGHT),text('서로 다른 사실 수',1.9,4,size=27,color=GOOD),text('10회',-1.9,3,size=38,color=WEIGHT),text('+1',1.9,3,size=42,color=GOOD))
    cards=VGroup(*[FactCard('A',.15,10,compact=True).move_to([-2.6+(j%3)*.7,1.6-(j//3)*.8,0]).scale(.65) for j in range(10)])
    target=FactCard('A',.15,compact=True).move_to([1.9,.5,0])
    p.add(cards,target,text('✓',1.9,-.6,size=38,color=GOOD),Arrow([-.35,.5,0],[.9,.5,0],buff=.05,color=ACCENT),text('같은 A를 10번 처리해도',0,-2.7,size=30),text('서로 다른 사실은 A 하나',0,-3.6,size=30,color=GOOD),text('설명용 예시 · 손실 감소량과 정답 사실 수는 다름',0,-4.55,size=20,color=MUTED))
    p.cards=cards;p.destination=target.get_center();return p
def finite_capacity():
    p=VGroup(text('모델 크기 고정',0,4,size=30,color=SPARSE),RoundedRectangle(width=6.7,height=3.5,color=SPARSE).move_to([0,1,0]),text('유한한 정보량',0,1.3,size=34,color=SPARSE),text('같은 용량을 어떻게 쓸까?',0,.2,size=27))
    cards=VGroup(*[FactCard(fid,[.15,.8,1.3][j%3],compact=True).scale(.75).move_to([-2.6+j*1.3,-1.9,0]) for j,fid in enumerate('AABCC')])
    p.add(cards,text('학습할 사실의 범위 + 반복 비중',0,-3.35,size=28,color=ACCENT),text('상자는 정보량의 비유 · 사실별 고정 저장 칸이 아님',0,-4.45,size=20,color=MUTED))
    return p
def ending():
    p=feedback()
    p[11].become(text('손실 → 선택 → 새로운 학습 분포',0,-3.25,size=28,color=GOOD))
    p[12].become(text('무엇을 학습할지 결정하는 신호가 된다',0,-4.4,size=27,color=ACCENT))
    return p
