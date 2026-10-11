from pathlib import Path
import json
from manim import *
ROOT=Path(__file__).resolve().parent
config.background_color='#081622';config.frame_width=14.222222222;config.frame_height=8
INK='#EAF5FB';MUTED='#8FAABD';CYAN='#51D8EE';GREEN='#8BE0B1';GOLD='#F4C978';RED='#FF8B8B'
def txt(s,size=26,color=INK,width=12):
    o=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if o.width>width:o.scale_to_fit_width(width)
    return o
def math(s,pos,size=36,color=INK):
    o=MathTex(s,font_size=size,color=color)
    if o.width>12:o.scale_to_fit_width(12)
    return o.move_to(pos)
def card(s,pos,color=CYAN,w=3,h=.65):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.1,color=color,fill_color=color,fill_opacity=.07),txt(s,25,color,w-.2)).move_to(pos)
class BorderScene(Scene):
    index=1
    def construct(self):
        r=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
        self.add(txt('행렬곱의 계산량 · 04',16,MUTED).move_to([-4.4,3.65,0]),txt(r['title'],32).move_to([0,3.03,0]))
        getattr(self,'part'+str(self.index))()
        d=r['duration_seconds'] or r['storyboard_seconds']
        if self.time>d+.01:raise ValueError((self.index,self.time,d))
        self.wait(max(0,d-self.time))
    def to(self,t):
        if self.time>t+.1:raise ValueError((self.index,self.time,t))
        self.wait(max(0,t-self.time))
    def foot(self,s):self.play(FadeIn(txt(s,20,GOLD).move_to([0,-3.45,0])),run_time=.5)

    def part1(self):
        target=Dot([3,0,0],color=GOLD,radius=.12)
        self.play(FadeIn(target),FadeIn(txt('목표 T',27,GOLD).next_to(target,RIGHT)))
        exact=card('정확히 같은 분해',[-3.5,1.6,0],CYAN,w=4.4)
        near=card('한없이 가까워지는 분해',[-3.5,-1.25,0],GREEN,w=4.4)
        self.play(FadeIn(exact))
        self.play(Create(Arrow(exact.get_right(),target.get_center(),buff=.15,color=CYAN)))
        self.to(5)
        self.play(FadeIn(near))
        dot=Dot([-.8,-1.25,0],color=GREEN)
        path=VMobject(color=GREEN).set_points_smoothly([[-.8,-1.25,0],[.5,-1.1,0],[1.7,-.35,0],[2.83,-.03,0]])
        self.play(Create(path),MoveAlongPath(dot,path),run_time=2)
        self.to(10)
        self.play(FadeIn(txt('두 조건에서 필요한 최소 항 수는 같을까?',29,GOLD).move_to([0,-2.5,0])))
        self.foot('관계의 개념도 · 실행 시간이 아닌 최소 단순항 개수를 비교')
    def part2(self):
        self.play(FadeIn(txt('W의 두 출력: (ad+bc, ac)',29,GREEN).move_to([0,2.05,0])))
        self.play(FadeIn(txt('입력 (a,b), (c,d) · a=2, b=1, c=3, d=1',23,MUTED).move_to([0,1.4,0])))
        nodes=VGroup(*[card(s,[-3.5,y,0],GOLD,w=2) for s,y in [('ac',.45),('ad',-.45),('bc',-1.35)]])
        out=VGroup(card('ad+bc = 5',[3.6,.15,0],GREEN,w=3.8),card('ac = 6',[3.6,-1.15,0],GREEN,w=3.8))
        self.play(FadeIn(nodes),FadeIn(out))
        for i,k in [(0,1),(1,0),(2,0)]:
            arrow=Arrow(nodes[i].get_right(),out[k].get_left(),buff=.1,color=GOLD)
            token=txt(['6','2','3'][i],25,GOLD).move_to(nodes[i])
            self.play(Create(arrow),token.animate.move_to(out[k]),run_time=.8);self.remove(token)
        self.to(11)
        self.play(FadeIn(txt('3항 분해: 상한 ≤3  +  별도의 불가능성 증명: 하한 ≥3',24).move_to([0,-2.35,0])))
        self.to(15)
        self.play(Write(math(r'R_{\mathbb C}(W)=3',[0,-2.95,0],34,GOLD)))
        self.foot('3개의 곱이 보인다는 사실만으로 최소값이 증명되지는 않는다 · W≠행렬곱 텐서')
    def part3(self):
        self.play(Write(math(r'S(t)=(u+tv)^{\otimes3},\quad P(t)=\frac{S(t)-S(0)}{t}',[0,2.1,0],34,CYAN)))
        axes=Axes(x_range=[0,1.4,.5],y_range=[0,1.3,.5],x_length=4.2,y_length=2.6,tips=False).move_to([-3.4,-.2,0])
        origin=axes.c2p(0,0);curve=axes.plot(lambda x:x*x,x_range=[0,1],color=MUTED)
        self.play(Create(axes),Create(curve))
        a=Dot(origin,color=INK);b=Dot(axes.c2p(1,1),color=CYAN)
        self.play(FadeIn(a),FadeIn(b))
        line=Arrow(origin,b.get_center(),buff=0,color=CYAN)
        normalized=Arrow(origin,axes.c2p(1,1),buff=0,color=GREEN)
        coefficient=txt('t=1:  +1 と −1'.replace(' と ',' / '),26,GOLD).move_to([3.5,1,0])
        self.play(Create(line),FadeIn(coefficient))
        self.play(FadeIn(txt('한 자리 변화 성분',18,MUTED).move_to([-3.1,-2.05,0])),FadeIn(txt('두 자리 변화 성분',18,MUTED).move_to([-3.4,1.3,0])))
        self.to(8)
        self.play(Create(normalized),FadeIn(txt('차이 ÷ t',25,GREEN).move_to([3.5,.05,0])))
        for t in [.5,.2,.1]:
            self.play(b.animate.move_to(axes.c2p(t,t*t)),Transform(line,Arrow(origin,axes.c2p(t,t*t),buff=0,color=CYAN)),Transform(normalized,Arrow(origin,axes.c2p(1,t),buff=0,color=GREEN)),Transform(coefficient,txt(f't={t}:  +{1/t:g} / −{1/t:g}',26,GOLD).move_to(coefficient)),run_time=1.3)
            self.wait(.7)
        self.to(18)
        self.play(FadeIn(txt('공통 성분은 소거 · 나눈 차이는 새로운 방향으로 접근',26,GREEN).move_to([0,-2.6,0])))
        self.foot('실제 계수 중 두 성분의 투영: S(t)↦(t,t²), P(t)↦(1,t) · 전체 거리는 아님')
    def positions(self,letters,pos):
        return VGroup(*[card(letter,[pos[0]+(i-1)*1.2,pos[1],0],GREEN if letter=='v' else CYAN,w=.9,h=.65) for i,letter in enumerate(letters)])
    def part4(self):
        self.play(Write(math(r'\frac{(u+tv)\otimes(u+tv)\otimes(u+tv)-u\otimes u\otimes u}{t}',[0,2.05,0],33,CYAN)))
        self.play(FadeIn(txt('세 자리 중 한 자리만 v로 선택',25,GOLD).move_to([0,1.2,0])))
        rows=VGroup()
        for i in range(3):
            row=self.positions(['u','u','u'],[-3.3,.3-i*.95]);self.play(FadeIn(row),run_time=.4)
            replacement=card('v',row[i].get_center(),GREEN,w=.9)
            self.play(Transform(row[i],replacement),run_time=.7)
            formula=math([r'v\otimes u\otimes u',r'u\otimes v\otimes u',r'u\otimes u\otimes v'][i],[2.5,.3-i*.95,0],29,GREEN)
            self.play(Create(Arrow(row.get_right(),formula.get_left(),buff=.15,color=GREEN)),Write(formula),run_time=.6)
            rows.add(row)
        self.to(10)
        self.play(FadeIn(txt('각 경우의 계수: t ÷ t = 1 → 세 항의 합 W',26,GOLD).move_to([0,-2.75,0])))
        self.to(16)
        self.play(*[FadeOut(o) for o in list(self.mobjects)[2:]])
        self.play(Write(math(r'P(t)=\underbrace{vuu+uvu+uuv}_{W}+tQ+t^2R',[0,1.75,0],39,GREEN)))
        self.add(txt('vuu는 v⊗u⊗u의 줄임 표기',20,MUTED).move_to([0,.85,0]))
        counts=VGroup(card('v를 1번 선택: 1',[-4.2,-.1,0],GREEN,w=3.8),card('v를 2번 선택: t',[0,-.1,0],RED,w=3.8),card('v를 3번 선택: t²',[4.2,-.1,0],RED,w=3.8))
        self.play(FadeIn(counts));self.to(22)
        self.play(counts[1].animate.set_opacity(.15),counts[2].animate.set_opacity(.15),run_time=2)
        self.play(Write(math(r'P(t)\longrightarrow W',[0,-1.8,0],43,GOLD)))
        self.foot('u=e₁, v=e₂ · 세 자리: A 입력, B 입력, 출력 분배 · t≠0의 두 항과 극한을 구분')
    def part5(self):
        self.play(FadeIn(card('정확히 만드는 최소값',[-3.6,1.7,0],CYAN,w=5)),FadeIn(card('극한으로 접근하는 최소값',[3.6,1.7,0],GREEN,w=5.7)))
        self.play(Write(math(r'R(W)=3',[-3.6,.5,0],47,CYAN)),Write(math(r'\underline R(W)=2',[3.6,.5,0],47,GREEN)))
        self.to(6)
        self.play(FadeIn(txt('극한까지 허용한 최소 항 수 = 보더 랭크',29,GOLD).move_to([0,-.9,0])))
        self.to(11)
        self.play(FadeIn(txt('정확한 2항 공식이 아니라, 두 최소값을 정하는 조건의 차이',25).move_to([0,-2.2,0])))
        self.foot('보더 랭크 하한 2는 별도 확인 · W와 2×2 행렬곱을 혼동하지 않음')
    def part6(self):
        self.play(Write(math(r'P(t)=\underbrace{W}_{\text{constant}}+\underbrace{tQ+t^2R}_{\text{degree}\leq2}',[0,1.95,0],40,CYAN)))
        self.play(FadeIn(card('변하지 않는 부분 W',[-3.4,.8,0],GREEN,w=4.8)),FadeIn(card('규칙이 있는 오차 tQ+t²R',[3.4,.8,0],RED,w=5.5)))
        self.to(7)
        rows=VGroup(*[card(s,[x,-.3,0],GOLD,w=3.7) for s,x in [('P(1) × 3',-4.2),('P(2) × (−3)',0),('P(3) × 1',4.2)]])
        self.play(FadeIn(rows));self.to(11)
        self.play(Write(math(r'3P(1)-3P(2)+P(3)=(3-3+1)W+(3-6+3)Q+(3-12+9)R',[0,-1.6,0],26)))
        self.to(15)
        self.play(Write(math(r'=W+0Q+0R=W',[0,-2.45,0],37,GREEN)))
        self.to(20)
        self.foot('3번의 추가 평가가 필요 · 정확히 복원되지만 즉시 더 빠르다는 뜻은 아님')
    def part7(self):
        self.play(FadeIn(txt('정확히 만드는 최소 개수 ≠ 극한으로 접근하는 최소 개수',29,GOLD).move_to([0,1.6,0])))
        self.play(FadeIn(txt('탐색할 수 있는 계산 구조가 넓어진다',30,GREEN).move_to([0,.3,0])))
        self.to(5)
        self.play(FadeIn(txt('정확한 계산과의 연결에는 복원 비용 분석이 필요',26).move_to([0,-1,0])))
        self.to(9)
        self.play(FadeIn(txt('다음: 여러 독립적인 행렬곱을 하나의 텐서에 담으면?',26,CYAN).move_to([0,-2.4,0])))
        self.foot('이번 막의 결론은 최소 항 수의 차이 · 실행 속도 개선을 주장하지 않음')
