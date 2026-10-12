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


    def region(self,small=False):
        area=Circle(radius=1.9,stroke_opacity=0,fill_color=CYAN,fill_opacity=.14).move_to([-2.1,.1,0])
        edge=DashedVMobject(Circle(radius=1.9,color=CYAN).move_to(area),num_dashes=55)
        label=math(r'\mathcal R_2',[ -2.5,1.2,0],39,CYAN)
        o=VGroup(area,edge,label)
        if small:
            inner=Circle(radius=.65,color=GREEN,fill_color=GREEN,fill_opacity=.1).move_to([-2.8,-.3,0])
            o.add(inner,math(r'\mathcal R_1',[-2.8,-.3,0],30,GREEN))
        return o
    def target(self):
        pt=Circle(radius=.08,color=GOLD,fill_color=config.background_color,fill_opacity=1).move_to([-.2,.1,0])
        return VGroup(pt,math('T',[.2,.4,0],35,GOLD))
    def geofoot(self):self.foot('집합 관계의 개념도 · 실제 텐서 공간의 차원·형상·거리를 나타내지 않음')
    def part1(self):
        question=txt('행렬곱의 계산량을 어디까지 줄일 수 있을까?',29,GOLD).move_to([0,2.05,0])
        self.play(FadeIn(question))
        blocks=VGroup(card('A 입력의 조합',[-4.1,.6,0],CYAN,w=3.1),card('B 입력의 조합',[0,.6,0],CYAN,w=3.1),card('출력 분배 규칙',[4.1,.6,0],GREEN,w=3.1))
        self.play(FadeIn(blocks));self.to(6)
        eq=math(r'T=\sum_i u_i\otimes v_i\otimes w_i',[0,-.7,0],36,CYAN)
        self.play(Write(eq));self.to(10)
        point=Dot([0,.1,0],color=GOLD,radius=.12)
        self.play(FadeOut(blocks),FadeOut(eq),FadeIn(point),run_time=1.2)
        self.play(FadeIn(txt('한 점 = 모든 입력에 적용되는 계산 관계 전체',28).move_to([0,-1.25,0])))
        self.play(FadeIn(txt('특정 숫자 입력의 답을 표시한 점이 아니다',23,MUTED).move_to([0,-2.3,0])))
        self.geofoot()
    def part2(self):
        region=self.region(small=True);self.play(FadeIn(region))
        self.play(FadeIn(txt('한 항 이하 ⊂ 두 항 이하',26,GREEN).move_to([2.9,1.5,0])))
        self.to(6)
        dot=Dot([-1.25,-.5,0],color=CYAN,radius=.1);self.play(FadeIn(dot))
        self.play(Create(Arrow(dot.get_center(),[1.5,-.1,0],buff=.15,color=CYAN)))
        cards=VGroup(card('입력 조합의 곱 ①',[3.3,.25,0],GOLD,w=4.4),card('입력 조합의 곱 ②',[3.3,-.7,0],GOLD,w=4.4))
        self.play(FadeIn(cards));self.to(12)
        self.play(FadeIn(txt('집합 안: 최대 두 곱으로 정확한 관계 표현',25).move_to([0,-2.4,0])))
        self.to(18)
        self.play(FadeIn(txt('정확히 두 항으로 못 만드는 목표에는?',25,GOLD).move_to([0,2.2,0])))
        self.geofoot()
    def part3(self):
        region=self.region();target=self.target();self.play(FadeIn(region),FadeIn(target))
        status=math(r'T\notin\mathcal R_2',[3.4,1.35,0],40,GOLD);self.play(Write(status))
        self.play(FadeIn(txt('목표 T는 집합에 미포함',24,GOLD).move_to([3.4,.55,0])))
        dot=Dot([-3.4,-.9,0],color=GREEN,radius=.055);self.play(FadeIn(dot));self.to(5)
        path=VMobject(color=GREEN,stroke_width=3).set_points_smoothly([[-3.4,-.9,0],[-2.1,-.8,0],[-1.15,-.25,0],[-.55,.06,0],[-.38,.1,0]])
        self.play(Create(path),MoveAlongPath(dot,path),run_time=4)
        self.play(FadeIn(txt('경로의 모든 점: 랭크 ≤2',25,GREEN).move_to([3.3,-.45,0])))
        self.to(13)
        self.play(Write(math(r'P(t)\longrightarrow T',[3.25,-1.3,0],36,GREEN)))
        self.play(FadeIn(txt('정확히 같지는 않지만, 차이는 얼마든지 작아진다',25).move_to([0,-2.4,0])))
        self.to(21)
        self.play(Transform(status,math(r'T\notin\mathcal R_2,\quad T\in\overline{\mathcal R_2}',[2.9,1.35,0],29,GOLD)))
        self.geofoot()
    def part4(self):
        self.play(FadeIn(txt('두 단순항의 기여를 일부 성분에 투영',25,MUTED).move_to([0,2.05,0])))
        origin=[-4,-.6,0];end=[-4,.5,0]
        a=Arrow(origin,[-3.3,.5,0],buff=0,color=CYAN);b=Arrow([-3.3,.5,0],end,buff=0,color=RED)
        result=Arrow(origin,end,buff=0,color=GREEN,stroke_width=6)
        label=txt('큰 공통 성분: +1, −1',27,GOLD).move_to([3.1,1.05,0])
        self.play(Create(a),Create(b),FadeIn(label));self.to(5)
        for n in [2,4,6]:
            middle=[-4+.7*n,.5,0]
            self.play(Transform(a,Arrow(origin,middle,buff=0,color=CYAN)),Transform(b,Arrow(middle,end,buff=0,color=RED)),Transform(label,txt(f'큰 공통 성분: +{n}, −{n}',27,GOLD).move_to(label)),run_time=1.3)
            self.wait(.6)
        self.play(Create(result),FadeIn(txt('반대 성분은 소거\n합은 유한하게 남는다',27,GREEN).move_to([3.1,-.4,0])))
        self.to(15)
        self.play(FadeIn(txt('각 항이 커지는 것과 합이 발산하는 것은 다르다',26).move_to([0,-1.9,0])))
        self.to(19)
        self.foot('성분 소거의 개념도 · 이 평면 그림으로 전체 텐서의 랭크를 판정하지 않음')
    def part5(self):
        self.play(FadeIn(card('정확한 최소 항 수',[-3.55,1.8,0],CYAN,w=5)),FadeIn(card('극한까지 허용한 최소 항 수',[3.55,1.8,0],GREEN,w=5.7)))
        self.play(Write(math(r'R(T)=3',[-3.55,.65,0],47,CYAN)),Write(math(r'\underline R(T)=2',[3.55,.65,0],47,GREEN)))
        self.to(6)
        self.play(FadeIn(txt('보더 랭크 = 낮은 랭크 집합의 폐포에 들어가는 최소 r',27,GOLD).move_to([0,-.65,0])))
        self.to(12)
        self.play(FadeIn(txt('행렬: 낮은 랭크의 집합은 닫혀 있음',25).move_to([0,-1.8,0])))
        self.play(FadeIn(txt('3차 이상 텐서: 닫혀 있지 않은 경우가 존재',25,GREEN).move_to([0,-2.55,0])))
        self.foot('실제로 존재하는 특정 예제의 수치 · 모든 텐서의 값이나 2×2 행렬곱의 값이 아님')
    def part6(self):
        self.play(FadeIn(txt('경계에서 찾은 구조 → 정확한 행렬곱 알고리즘에 활용?',28,GOLD).move_to([0,2.0,0])))
        base=card('목표 계산 관계 T',[-3.4,.8,0],GREEN,w=4.8)
        error=card('매개변수에 따른 다항식 오차',[3.4,.8,0],RED,w=5.5)
        self.play(FadeIn(base),FadeIn(error));self.to(7)
        eq=math(r'P(t)=T+tQ+t^2R',[0,-.1,0],36,CYAN);self.play(Write(eq))
        self.to(11)
        values=VGroup(*[card(s,[x,-1.1,0],CYAN,w=2.8) for s,x in [('P(t₁)',-4.2),('P(t₂)',0),('P(t₃)',4.2)]])
        self.play(FadeIn(values))
        self.to(16)
        output=card('원하는 계수 T 정확히 복원',[0,-2.25,0],GREEN,w=6)
        self.play(TransformFromCopy(values,output),error.animate.set_opacity(.2),run_time=1.5)
        self.to(22)
        self.foot('다항식 형태가 확보된 구성의 예 · 복원 비용과 성장률은 별도 분석')
    def part7(self):
        region=self.region();target=self.target();self.play(FadeIn(region),FadeIn(target))
        label=txt('정확한 분해만 탐색',27,CYAN).move_to([3.4,1.2,0]);self.play(FadeIn(label))
        self.to(4)
        closure=Circle(radius=1.9,color=GREEN,fill_color=GREEN,fill_opacity=.06).move_to([-2.1,.1,0])
        self.play(Create(closure),Transform(target[0],Dot([-.2,.1,0],color=GOLD,radius=.1)),Transform(label,txt('접근 가능한 경계까지 탐색',26,GREEN).move_to(label)))
        self.play(FadeIn(math(r'\mathcal R_2\ \longrightarrow\ \overline{\mathcal R_2}',[3.3,0,0],37,GOLD)))
        self.to(10)
        self.play(FadeIn(txt('다음: 여러 독립적인 행렬곱을 하나의 텐서에 담으면?',25).move_to([0,-2.6,0])))
        self.geofoot()
