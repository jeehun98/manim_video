from pathlib import Path
import json
from manim import *

ROOT=Path(__file__).resolve().parent
config.background_color='#081622'
config.frame_width=14.222222222
config.frame_height=8
INK='#EAF5FB';MUTED='#8FAABD';CYAN='#51D8EE';GREEN='#8BE0B1';GOLD='#F4C978';RED='#FF8B8B'

def txt(s,size=28,color=INK,width=12.4):
    obj=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.2)
    if obj.width>width:obj.scale_to_fit_width(width)
    return obj

def box(s,pos,w=3,color=CYAN):
    rect=RoundedRectangle(width=w,height=.65,corner_radius=.12,color=color,fill_color=color,fill_opacity=.09)
    label=txt(s,24,color,width=w-.25)
    return VGroup(rect,label).move_to(pos)

class BoundsScene(Scene):
    index=1
    def construct(self):
        self.record=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
        self.add(txt('행렬곱의 계산량 · 2장',17,MUTED).move_to([-4.8,3.65,0]),txt(self.record['title'],33).move_to([0,3.03,0]))
        getattr(self,'part'+str(self.index))()
        duration=self.record['duration_seconds'] or self.record['storyboard_seconds']
        if self.time>duration:raise ValueError((self.index,self.time,duration))
        self.wait(duration-self.time)

    def to(self,target):
        if self.time>target+.1:raise ValueError((self.index,self.time,target))
        if target>self.time:self.wait(target-self.time)

    def footer(self,s):
        obj=txt(s,21,GOLD).move_to([0,-3.45,0]);self.play(FadeIn(obj),run_time=.5);return obj

    def part1(self):
        roots=VGroup(box('표준',[-3.4,1.9,0]),box('Strassen',[3.4,1.9,0],color=GREEN))
        self.play(FadeIn(roots),run_time=.5)
        branches=VGroup()
        for x,count,color in [(-3.4,8,CYAN),(3.4,7,GREEN)]:
            for j in range(count):
                end=np.array([x-2+j*4/(count-1),.7,0])
                branches.add(Line([x,1.55,0],end,color=color),Dot(end,radius=.055,color=color))
        self.play(Create(branches),run_time=1)
        introductory=VGroup(txt('2 × 2 :  8 곱',27,CYAN).move_to([-3.4,.1,0]),txt('2 × 2 :  7 곱',27,GREEN).move_to([3.4,.1,0]))
        self.play(FadeIn(introductory),run_time=.5)
        self.to(4)
        self.play(FadeOut(branches),FadeOut(roots),FadeOut(introductory),run_time=.5)
        headers=VGroup(txt('행렬 크기',23,MUTED).move_to([-4.7,1.7,0]),txt('표준',23,CYAN).move_to([-1.2,1.7,0]),txt('Strassen',23,GREEN).move_to([3.2,1.7,0]))
        self.play(FadeIn(headers),run_time=.5)
        for i,(n,a,b) in enumerate([(2,8,7),(4,64,49),(8,512,343),(16,4096,2401)]):
            self.to([5,6,10,13.5][i])
            y=1.05-i*.65
            row=VGroup(txt(f'{n} × {n}',26).move_to([-4.7,y,0]),txt(f'{a:,}',29,CYAN).move_to([-1.2,y,0]),txt(f'{b:,}',29,GREEN).move_to([3.2,y,0]))
            self.play(FadeIn(row,shift=UP*.12),run_time=.5)
            if i:self.play(Indicate(row[1]),Indicate(row[2]),run_time=.5)
        self.to(17)
        self.play(FadeIn(box('크기 ×2  →  곱셈 ×8',[-2.7,-2.1,0],w=4.7)),FadeIn(box('크기 ×2  →  곱셈 ×7',[2.7,-2.1,0],w=4.7,color=GREEN)))
        self.to(23)
        note=self.footer('표의 숫자: 재귀 말단의 스칼라 곱셈 횟수 · 덧셈/뺄셈 제외')
        self.to(29)
        formulas=VGroup(MathTex(r'n^3',color=CYAN,font_size=37).move_to([-2.7,-2.85,0]),MathTex(r'n^{\log_2 7}\approx n^{2.8074}',color=GREEN,font_size=37).move_to([2.7,-2.85,0]))
        self.play(Write(formulas))
        self.to(33)
        self.play(Transform(note,txt('덧셈 포함: T(n)=7T(n/2)+O(n²) → 성장 지수 log₂7',21,GOLD).move_to(note)))

    def exponent_axis(self):
        axis=NumberLine(x_range=[1.8,3.15,.2],length=10,include_numbers=False).move_to([0,.2,0])
        self.play(Create(axis))
        for value,label in [(2,'2'),(3,'3')]:self.add(txt(label,24,MUTED).next_to(axis.n2p(value),DOWN,buff=.2))
        self.add(txt('성장 지수',21,MUTED).move_to([0,-.75,0]))
        return axis

    def part2(self):
        axis=self.exponent_axis();point=axis.n2p(np.log2(7))
        boundary=Line(point+DOWN*.6,point+UP*1.35,color=GREEN,stroke_width=4)
        label=txt('Strassen 상한 ≈ 2.8074',27,GREEN).move_to([2.5,2.1,0])
        self.play(Create(boundary),FadeIn(label))
        marker=Dot(point,color=GREEN,radius=.09);self.play(FadeIn(marker))
        self.to(3)
        region=Line(axis.n2p(2),point,color=GOLD,stroke_width=13,stroke_opacity=.35)
        self.play(Create(region),run_time=1)
        self.play(FadeIn(txt('최적값은 이보다 작을 수도 있다',28,GOLD).move_to([0,-1.55,0])))
        self.to(9)
        algorithm=box('계산 공식 + 비용의 증명',[-3.2,1.8,0],w=4.6)
        arrow=Arrow(algorithm.get_right(),boundary.get_top(),color=CYAN,buff=.2)
        self.play(FadeIn(algorithm),Create(arrow))
        self.to(15)
        question=txt('더 낮은 경계를 정당화할 새로운 알고리즘은?',26).move_to([0,-2.5,0]);self.play(FadeIn(question))
        self.footer('상한: 그 비용으로 계산하는 방법의 존재 · 최소성의 증명은 별도')

    def part3(self):
        def grid(n,side=2.8):
            return VGroup(*[Square(side_length=side/n,stroke_color=CYAN,stroke_width=1.5,fill_color=CYAN,fill_opacity=.12).move_to([(j-(n-1)/2)*side/n,((n-1)/2-i)*side/n,0]) for i in range(n) for j in range(n)])
        small=grid(2).move_to([-3.5,.65,0]);self.play(FadeIn(small))
        small_label=txt('2 × 2 = 4칸',29,CYAN).move_to([-3.5,-1.3,0]);self.play(FadeIn(small_label))
        self.to(5)
        big=grid(4).move_to([3,.65,0])
        self.play(TransformFromCopy(small,big),run_time=2)
        self.play(FadeIn(txt('4 × 4 = 16칸',29,GREEN).move_to([3,-1.3,0])))
        arrow=Arrow([-1.6,.65,0],[1.1,.65,0],color=GOLD);self.play(Create(arrow),FadeIn(txt('한 변 ×2\n칸 수 ×4',25,GOLD).move_to([-.25,1.65,0])))
        self.to(12)
        self.play(FadeIn(MathTex(r'n^2\ \longrightarrow\ (2n)^2=4n^2',font_size=36,color=GREEN).move_to([0,-2.1,0])))
        self.to(18)
        self.footer('전체 출력을 명시적으로 만드는 모델의 기본 하한 · 곱셈만의 하한은 아님')
        self.play(FadeIn(txt('전체 작업량은 적어도 출력 크기에 비례',26,GOLD).move_to([0,-2.8,0])))

    def part4(self):
        axis=self.exponent_axis();lo=axis.n2p(2);hi=axis.n2p(np.log2(7))
        segment=Line(lo,hi,color=GOLD,stroke_width=12,stroke_opacity=.3)
        lower=Line(lo+DOWN*.5,lo+UP*1.2,color=CYAN,stroke_width=4);upper=Line(hi+DOWN*.5,hi+UP*1.2,color=GREEN,stroke_width=4)
        self.play(Create(segment),Create(lower),Create(upper))
        labels=VGroup(txt('하한 2',26,CYAN).move_to([-4.2,1.85,0]),txt('Strassen의 상한',26,GREEN).move_to([2.5,1.85,0]))
        self.play(FadeIn(labels))
        omega=MathTex(r'\omega',font_size=55,color=GOLD).move_to(axis.n2p(2.3)+UP*.65)
        self.play(FadeIn(omega));self.to(5)
        definition=txt('가능한 성장 지수들의 하한값 (infimum) · 계수체 ℂ 고정',23).move_to([0,-1.5,0]);self.play(FadeIn(definition))
        self.to(13)
        later=DashedLine(axis.n2p(2.5)+DOWN*.45,axis.n2p(2.5)+UP*.7,color=GREEN)
        self.play(Create(later),FadeIn(txt('후속 연구로 더 낮아진 상한',23,GREEN).move_to([1.4,2.45,0])))
        self.add(txt('점선 위치는 개념도 · 최신 기록 수치 아님',17,MUTED).move_to([0,-2.1,0]))
        self.to(20)
        question=MathTex(r'\omega=2\ ?',color=GOLD,font_size=46).move_to([0,-2.8,0]);self.play(Write(question))
        self.to(24)
        self.play(*[FadeOut(obj) for obj in list(self.mobjects) if obj.get_center()[1]<2.6])
        exact=MathTex(r'\omega=2\quad\not\Rightarrow\quad M(n)=O(n^2)',font_size=36,color=MUTED).move_to([0,1.7,0])
        self.play(Write(exact))
        statement=MathTex(r'\forall\varepsilon>0:\quad M(n)=O_{\varepsilon}(n^{2+\varepsilon})',font_size=40,color=GOLD).move_to([0,.7,0]);self.play(Write(statement))
        epsilon_line=NumberLine(x_range=[2,2.6,.1],length=8,include_numbers=False).move_to([0,-.3,0]);self.play(Create(epsilon_line))
        dot=Dot(epsilon_line.n2p(2.5),color=GREEN,radius=.08);readout=txt('2 + 0.5',25,GREEN).move_to([0,-1,0]);self.add(dot,readout)
        for eps in [.1,.01]:
            self.play(dot.animate.move_to(epsilon_line.n2p(2+eps)),Transform(readout,txt(f'2 + {eps}',25,GREEN).move_to(readout)),run_time=1)
        self.play(FadeIn(txt('ε는 원하는 만큼 작게 · 상수와 알고리즘은 ε에 따라 달라질 수 있음',21,MUTED).move_to([0,-1.8,0])))
        self.to(43)
        self.play(FadeIn(txt('작은 공식에서 곱셈을 줄이면\n성장률도 항상 더 좋아질까?',31,GOLD).move_to([0,-2.85,0])))
