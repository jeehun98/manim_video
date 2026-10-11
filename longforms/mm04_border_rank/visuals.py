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
        self.play(Write(eq));self.to(9)
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
        self.play(FadeIn(txt('두 항 이하로는 못 만드는 목표에도 접근할까?',25,GOLD).move_to([0,2.2,0])))
        self.geofoot()
    def part3(self):
        disk=self.region();disk[2].become(math('D',[-2.5,1.2,0],39,CYAN))
        target=self.target();target[0].scale(.7);target[1].become(math('p',[.2,.4,0],35,GOLD))
        self.play(FadeIn(disk),FadeIn(target))
        status=txt('열린 원판: 내부만 포함\n둘레의 점 p는 미포함',26,GOLD,width=5.4).move_to([3.2,1.0,0])
        self.play(FadeIn(status))
        dot=Dot([-3.4,-.9,0],color=GREEN,radius=.035);self.play(FadeIn(dot));self.to(7)
        path=VMobject(color=GREEN).set_points_smoothly([[-3.4,-.9,0],[-2,-.6,0],[-.9,-.05,0],[-.65,.1,0]])
        self.play(Create(path),MoveAlongPath(dot,path),run_time=2)
        neighborhood=Circle(radius=.9,color=GOLD,stroke_opacity=.7).move_to([-.2,.1,0]);self.play(Create(neighborhood),run_time=.5)
        for eps in [.9,.5,.3]:
            self.play(Transform(neighborhood,Circle(radius=eps,color=GOLD,stroke_opacity=.7).move_to([-.2,.1,0])),dot.animate.move_to([-.2-eps/2,.1,0]),run_time=.7)
            self.wait(.25)
        self.play(Transform(status,txt('어떤 작은 거리를 정해도\n그보다 가까운 내부점 존재',25,GREEN,width=5.4).move_to(status)))
        self.to(15)
        closure=Circle(radius=1.9,color=GREEN,fill_color=GREEN,fill_opacity=.06).move_to([-2.1,.1,0])
        boundary=VGroup(*[Dot(closure.point_at_angle(k*TAU/8),radius=.045,color=GREEN) for k in range(8)])
        self.play(FadeOut(neighborhood),Create(closure),FadeIn(boundary),Transform(target[0],Dot([-.2,.1,0],color=GOLD,radius=.055)))
        self.play(Transform(disk[2],math(r'\overline D',[-2.5,1.2,0],39,GREEN)),Transform(status,txt('빠져 있던 극한점도 포함\n이것이 폐포',27,GREEN,width=5.4).move_to(status)))
        definition=txt('폐포 = 원래 집합을 포함하는 가장 작은 닫힌 집합',25,GOLD).move_to([0,-2.5,0]);self.play(FadeIn(definition))
        self.to(22)
        self.play(FadeOut(closure),FadeOut(boundary),FadeOut(path),FadeOut(dot),FadeOut(definition),Transform(disk,self.region()),Transform(target,self.target()))
        self.play(Transform(status,txt('다시 텐서 공간으로\n집합 안: 랭크 ≤ 2',27,CYAN,width=5.4).move_to([3.2,1.1,0])))
        condition=math(r'T\notin\mathcal R_2',[3.2,-.05,0],38,GOLD);self.play(Write(condition))
        dot=Dot([-3.4,-.9,0],color=GREEN,radius=.055);self.play(FadeIn(dot));self.to(27)
        path=VMobject(color=GREEN,stroke_width=3).set_points_smoothly([[-3.4,-.9,0],[-2.1,-.8,0],[-1.15,-.25,0],[-.55,.06,0],[-.38,.1,0]])
        self.play(Create(path),MoveAlongPath(dot,path),run_time=3)
        self.play(FadeIn(txt('두 항 이하로 정확히 못 만들어도, 한없이 가까워질 수 있다',25).move_to([0,-2.5,0])))
        self.to(32)
        closure=Circle(radius=1.9,color=GREEN,fill_color=GREEN,fill_opacity=.04).move_to([-2.1,.1,0])
        self.play(Create(closure),Transform(target[0],Dot([-.2,.1,0],color=GOLD,radius=.08)),Transform(disk[2],math(r'\overline{\mathcal R_2}',[-2.5,1.2,0],39,GREEN)),Transform(status,txt('집합의 폐포\n보더 랭크 ≤ 2',27,GREEN,width=5.4).move_to(status)))
        self.play(Transform(condition,math(r'T\notin\mathcal R_2,\quad T\in\overline{\mathcal R_2}',[3.15,-.05,0],29,GOLD)))
        self.play(FadeIn(txt('목표 T: 보더 랭크 ≤ 2',26,GREEN).move_to([3.2,-1.1,0])))
        self.geofoot()
    def part4(self):
        self.play(FadeIn(txt('두 단순항의 기여를 일부 성분에 투영',25,MUTED).move_to([0,2.05,0])))
        origin=[-4,-.6,0];end=[-4,1.1,0]
        a=Arrow(origin,[-3.3,1.1,0],buff=0,color=CYAN);b=Arrow([-3.3,1.1,0],end,buff=0,color=RED)
        result=Arrow(origin,end,buff=0,color=GREEN,stroke_width=6)
        label=txt('큰 공통 성분: +1, −1',27,GOLD).move_to([3.1,1.05,0])
        self.play(Create(a),Create(b),Create(result),FadeIn(label));self.to(5)
        for n in [2,4,6]:
            end=[-4,.5+.6/n,0]
            middle=[-4+.7*n,end[1],0]
            self.play(Transform(a,Arrow(origin,middle,buff=0,color=CYAN)),Transform(b,Arrow(middle,end,buff=0,color=RED)),Transform(result,Arrow(origin,end,buff=0,color=GREEN,stroke_width=6)),Transform(label,txt(f'큰 공통 성분: +{n}, −{n}',27,GOLD).move_to(label)),run_time=1.3)
            self.wait(.6)
        self.play(Indicate(result),FadeIn(txt('공통 성분은 소거\n작은 차이는 남는다',27,GREEN).move_to([3.1,-.4,0])))
        self.to(15)
        self.play(FadeIn(txt('각 항이 커지는 것과 합이 발산하는 것은 다르다',26).move_to([0,-1.9,0])))
        self.to(19)
        self.foot('성분 소거의 개념도 · 이 평면 그림으로 전체 텐서의 랭크를 판정하지 않음')
    def part5(self):
        top=VGroup(txt('검증된 특정 사례',22,MUTED).move_to([0,2.2,0]),math(r'R(T)=3\qquad\underline R(T)=2',[0,1.3,0],43,GOLD))
        self.play(FadeIn(top))
        self.to(5)
        definition=txt('보더 랭크: T가 Rᵣ의 폐포에 들어가게 하는 최소 r',27,GREEN).move_to([0,.4,0]);self.play(FadeIn(definition))
        self.to(14)
        self.play(FadeOut(top),definition.animate.move_to([0,2.1,0]))
        left=RoundedRectangle(width=5.2,height=2.9,color=CYAN,fill_color=CYAN,fill_opacity=.08).move_to([-3.3,-.1,0])
        right=DashedVMobject(RoundedRectangle(width=5.2,height=2.9,color=GREEN).move_to([3.3,-.1,0]),num_dashes=45)
        titles=VGroup(txt('행렬의 낮은 랭크 집합',25,CYAN).move_to([-3.3,.75,0]),txt('일부 3차 이상 텐서',25,GREEN).move_to([3.3,.75,0]))
        self.play(Create(left),Create(right),FadeIn(titles))
        self.play(Write(math(r'\overline{\mathcal M_2}=\mathcal M_2',[-3.3,-.25,0],35,CYAN)))
        self.to(19)
        border=RoundedRectangle(width=5.2,height=2.9,color=GREEN).move_to([3.3,-.1,0]);self.play(Create(border))
        new=Dot([5.9,-.1,0],color=GOLD,radius=.09);self.play(FadeIn(new),Write(math(r'\overline{\mathcal R_2}\supsetneq\mathcal R_2',[3.3,-.25,0],35,GREEN)))
        self.play(FadeIn(txt('폐포를 취해도 변화 없음',23,CYAN).move_to([-3.3,-1.1,0])),FadeIn(txt('빠져 있던 극한점 포함',23,GREEN).move_to([3.3,-1.1,0])))
        self.to(23)
        self.play(FadeIn(txt('집합 자체의 최소값과 폐포를 기준으로 한 최소값이 달라질 수 있다',25,GOLD).move_to([0,-2.45,0])))
        self.foot('M₂={M:rank(M)≤2} · 오른쪽은 특정 텐서 공간의 사례 · 도형은 집합 관계 개념도')
    def part6(self):
        self.play(FadeIn(txt('다항식 형태를 확보한다면 → 정확한 계산으로 복원 가능',28,GOLD).move_to([0,2.0,0])))
        base=card('목표 계산 관계 T',[-3.4,.8,0],GREEN,w=4.8)
        error=card('매개변수에 따른 다항식 오차',[3.4,.8,0],RED,w=5.5)
        self.play(FadeIn(base),FadeIn(error));self.to(4)
        eq=math(r'\text{Example:}\quad P(t)=T+tQ+t^2R',[0,-.1,0],36,CYAN);self.play(Write(eq))
        self.to(9)
        values=VGroup(*[card(s,[x,-1.1,0],CYAN,w=2.8) for s,x in [('P(t₁)',-4.2),('P(t₂)',0),('P(t₃)',4.2)]])
        self.play(FadeIn(values))
        self.to(11)
        output=card('원하는 계수 T 정확히 복원',[0,-2.25,0],GREEN,w=6)
        self.play(TransformFromCopy(values,output),error.animate.set_opacity(.2),run_time=1.5)
        self.to(19)
        self.foot('다항식 형태가 확보된 구성의 예 · 복원 비용과 성장률은 별도 분석')
    def part7(self):
        region=self.region();target=self.target();self.play(FadeIn(region),FadeIn(target))
        label=txt('정확한 분해만 탐색',27,CYAN).move_to([3.4,1.2,0]);self.play(FadeIn(label))
        self.to(5)
        closure=Circle(radius=1.9,color=GREEN,fill_color=GREEN,fill_opacity=.06).move_to([-2.1,.1,0])
        self.play(Create(closure),Transform(region[2],math(r'\overline{\mathcal R_2}',[-2.5,1.2,0],39,GREEN)),Transform(target[0],Dot([-.2,.1,0],color=GOLD,radius=.1)),Transform(label,txt('접근 가능한 경계까지 탐색',26,GREEN).move_to(label)))
        self.play(FadeIn(math(r'\mathcal R_2\ \longrightarrow\ \overline{\mathcal R_2}',[3.3,0,0],37,GOLD)))
        self.to(10)
        self.play(FadeIn(txt('다음: 여러 독립적인 행렬곱을 하나의 텐서에 담으면?',25).move_to([0,-2.6,0])))
        self.geofoot()
