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
        eq=math(r'T=\sum_{i=1}^{r}u_i\otimes v_i\otimes w_i',[0,1.4,0],43,CYAN)
        self.play(Write(eq));self.play(Circumscribe(eq,color=GOLD));self.to(4)
        self.play(FadeIn(txt('모든 계수가 정확히 같아야 한다',29).move_to([0,.1,0])))
        self.to(7)
        self.play(Write(math(r'T_\varepsilon\longrightarrow T',[0,-1.3,0],46,GREEN)))
        self.foot('극한을 허용하면 무엇이 달라질까?')
    def part2(self):
        target=math(r'ad+bc',[0,2.1,0],40,GREEN);self.play(Write(target))
        base=math(r'(a+\varepsilon b)(c+\varepsilon d)',[0,1.05,0],36,CYAN);self.play(Write(base));self.to(4)
        expanded=math(r'ac+\varepsilon ad+\varepsilon bc+\varepsilon^2bd',[0,-.05,0],34)
        self.play(TransformFromCopy(base,expanded))
        self.to(7)
        result=math(r'\frac{(a+\varepsilon b)(c+\varepsilon d)-ac}{\varepsilon}=ad+bc+\varepsilon bd',[0,-1.2,0],33,GOLD)
        self.play(Write(result));self.to(12)
        self.play(FadeOut(base),FadeOut(expanded),result.animate.move_to([0,1.05,0]),target.animate.move_to([-4.6,2.1,0]))
        self.play(FadeIn(txt('a=2, b=1, c=3, d=1 → 목표 5',25,GREEN).move_to([1,2.1,0])))
        line=NumberLine(x_range=[5,5.6,.1],length=8,include_numbers=True,font_size=23).move_to([0,-.4,0])
        dot=Dot(line.n2p(5.5),color=GOLD);label=txt('ε=0.5 → 5.5',27,GOLD).move_to([0,-1.5,0]);self.play(Create(line),FadeIn(dot),FadeIn(label))
        for eps in [.1,.01]:
            self.play(dot.animate.move_to(line.n2p(5+eps)),Transform(label,txt(f'ε={eps} → {5+eps:g}',27,GOLD).move_to(label)),run_time=1.2);self.wait(.7)
        self.to(21)
        self.play(FadeIn(txt('ε≠0: 잔여항 존재 · 곱셈은 여전히 2번',27,RED).move_to([0,-2.5,0])))
        self.foot('계수 ε의 곱셈과 나눗셈은 스칼라 연산 · 쌍선형 곱은 2개')
    def part3(self):
        self.play(Write(math(r'W=e_1\otimes e_1\otimes e_2+e_1\otimes e_2\otimes e_1+e_2\otimes e_1\otimes e_1',[0,2.1,0],30,CYAN)))
        self.play(FadeIn(txt('왼쪽 입력 (a,b) · 오른쪽 입력 (c,d) · 출력 위치 (z₁,z₂)',23,MUTED).move_to([0,1.35,0])))
        nodes=VGroup(*[card(s,[-3.5,y,0],GOLD,w=2) for s,y in [('ac',.4),('ad',-.5),('bc',-1.4)]])
        out=VGroup(card('출력 1: ad+bc',[3.6,-.2,0],GREEN,w=3.8),card('출력 2: ac',[3.6,-1.4,0],GREEN,w=3.8))
        self.play(FadeIn(nodes),FadeIn(out))
        for i,k in [(0,1),(1,0),(2,0)]:
            arrow=Arrow(nodes[i].get_right(),out[k].get_left(),buff=.1,color=GOLD)
            token=txt(['6','2','3'][i],25,GOLD).move_to(nodes[i]);self.play(Create(arrow),token.animate.move_to(out[k]),run_time=.8);self.remove(token)
        self.to(12)
        self.play(Write(math(r'R_{\mathbb C}(W)=3',[0,-2.4,0],37,GOLD)))
        self.foot('W는 행렬곱 텐서가 아님 · 2항 불가능성은 별도 하한 논증')
    def slots(self,vals):
        o=VGroup()
        labels=['111','112','121','122','211','212','221','222']
        for i,(lab,val) in enumerate(zip(labels,vals)):
            x=-4.8+(i%4)*3.2;y=.2-(i//4)*1.25
            o.add(VGroup(txt(lab,19,MUTED).move_to([x,y+.45,0]),card(val,[x,y,0],GREEN if lab in ['112','121','211'] else RED,w=2.4,h=.6)))
        return o
    def part4(self):
        eq=math(r'P(\varepsilon)=\frac{(e_1+\varepsilon e_2)^{\otimes3}-e_1^{\otimes3}}{\varepsilon}',[0,1.95,0],38,CYAN)
        self.play(Write(eq))
        self.play(FadeIn(txt('ε ≠ 0: 단순항 1개 − 단순항 1개',26,GOLD).move_to([0,1,0])))
        self.to(6)
        cells=self.slots(['1/ε − 1/ε','1','1','ε','1','ε','ε','ε²']);self.play(FadeIn(cells))
        self.to(11);self.play(Indicate(cells[0],color=GOLD))
        new=self.slots(['0','1','1','ε','1','ε','ε','ε²']);self.play(Transform(cells,new))
        self.to(15)
        for k in [1,2,4]:self.play(Indicate(cells[k],color=GREEN),run_time=.5)
        self.play(FadeIn(txt('둘째 기저를 1번 선택 → W의 세 계수',25,GREEN).move_to([0,-1.8,0])))
        self.to(22)
        self.play(Transform(cells,self.slots(['0','1','1','0','1','0','0','0'])),run_time=2)
        self.play(Write(math(r'P(\varepsilon)=W+\varepsilon Q+\varepsilon^2R\longrightarrow W',[0,-2.55,0],33,GOLD)))
        self.foot('전개 계수: (0,1,1,ε,1,ε,ε,ε²) · ε→0')
    def part5(self):
        self.play(FadeIn(card('정확한 분해',[-3.6,1.7,0],CYAN,w=4)),FadeIn(card('극한에서 접근',[3.6,1.7,0],GREEN,w=4)))
        self.play(Write(math(r'R(W)=3',[-3.6,.5,0],47,CYAN)),Write(math(r'\underline R(W)=2',[3.6,.5,0],47,GREEN)))
        self.to(5)
        self.play(FadeIn(txt('극한까지 허용한 최소 단순항 개수 = 보더 랭크',28,GOLD).move_to([0,-1,0])))
        self.to(10)
        self.play(FadeIn(txt('가까운 텐서의 랭크와 목표 텐서의 랭크는 다를 수 있다',25).move_to([0,-2.25,0])))
        self.foot('W의 예제 · 2×2 행렬곱의 랭크·보더 랭크는 둘 다 7')
    def part6(self):
        self.play(Write(math(r'P(t)=W+tQ+t^2R',[0,2.05,0],40,CYAN)))
        rows=VGroup()
        for i,(t,pair) in enumerate([(1,'(6,12)'),(2,'(7,20)'),(3,'(8,30)')]):
            x=-4.2+i*4.2;row=VGroup(card(f't={t}',[x,1.1,0],CYAN,w=2.3),card(f'P({t})={pair}',[x,.1,0],GREEN,w=3.5));rows.add(row)
        self.play(FadeIn(rows));self.to(7)
        weights=VGroup(*[card(s,[x,-.85,0],GOLD,w=2.3) for s,x in [('×3',-4.2),('×(−3)',0),('×1',4.2)]])
        self.play(FadeIn(weights))
        self.play(Write(math(r'3P(1)-3P(2)+P(3)=W',[0,-1.9,0],36,GOLD)))
        self.to(14)
        self.play(FadeOut(rows),FadeOut(weights))
        cancel=VGroup(math(r'W:\quad3-3+1=1',[-3.2,.8,0],32,GREEN),math(r'Q:\quad3-6+3=0',[3.2,.8,0],32,RED),math(r'R:\quad3-12+9=0',[0,-.25,0],32,RED))
        self.play(FadeIn(cancel));self.to(21)
        self.play(Write(math(r'3(6,12)-3(7,20)+(8,30)=(5,6)',[0,-2.65,0],29,GREEN)))
        self.to(27)
        self.foot('각 평가 ≤2항 × 3회 → ≤6항의 정확한 계산 · 즉시 2곱이 되는 것은 아님')
    def part7(self):
        self.play(Write(math(r'P(t)^{\otimes k}:\quad\deg\leq2k,\quad R\leq2^k\ (t\ne0)',[0,1.95,0],34,CYAN)))
        self.play(FadeIn(card('평가점 2k+1개',[-3.7,.65,0],GOLD,w=4.1)),FadeIn(card('각 평가 ≤ 2ᵏ항',[3.7,.65,0],GREEN,w=4.1)))
        self.to(8)
        self.play(Write(math(r'R(W^{\otimes k})\leq(2k+1)\,2^k',[0,-.6,0],42,GOLD)))
        self.play(FadeIn(txt('선형 평가 비용 × 지수적으로 늘어나는 항 수',27).move_to([0,-1.65,0])))
        self.to(16)
        self.play(FadeIn(txt('다음: 여러 독립적인 행렬곱을 하나의 텐서에 담으면?',26,GREEN).move_to([0,-2.6,0])))
        self.foot('W에 대한 정확한 상한 · 일반 퇴화도 차수·평가 비용을 함께 분석해야 함')
