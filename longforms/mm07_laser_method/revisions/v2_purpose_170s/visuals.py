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
COLORS=[CYAN,GREEN,GOLD]
def block(label,pos,color=CYAN,w=2.8,h=1.1):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,color=color,fill_color=color,fill_opacity=.1),txt(label,25,color,w-.2)).move_to(pos)
def bundle(pos=(0,0,0),scale=1):
    cells=VGroup()
    for i in range(3):
        for j in range(3):
            p=[(j-1)*1.4,(1-i)*1.05,0]
            if i==j: cell=block('T'+str(i+1),p,COLORS[i],1.25,.9)
            else:cell=VGroup(Rectangle(width=1.25,height=.9,color=MUTED,stroke_opacity=.2),txt('0',22,MUTED)).move_to(p)
            cells.add(cell)
    return cells.scale(scale).move_to(pos)

def matrix(values,center,cell=.58,color=CYAN):
    n=len(values);v=VGroup()
    for i,row in enumerate(values):
        for j,value in enumerate(row):
            pos=[center[0]+(j-(n-1)/2)*cell,center[1]+((n-1)/2-i)*cell,0]
            v.add(VGroup(Square(cell,color=color,stroke_width=1.4),txt(str(value),23,color)).move_to(pos))
    return v
def combo_grid():
    labels=['P','Q','S'];v=VGroup()
    for i in range(3):
        for j in range(3):
            v.add(block(labels[i]+' ⊗ '+labels[j],[(j-1)*3,(1-i)*1.05,0],COLORS[i],2.65,.8))
    return v

def network(alternate=False):
    # Explicit support, never inferred from spatial proximity.
    support=[('x1','y1','z1'),('x1','y2','z2'),('x2','y3','z2' if alternate else 'z3')]
    labels=[['x1','x2'],['y1','y2','y3'],['z1','z2'] if alternate else ['z1','z2','z3']]
    nodes={}
    for col,group in enumerate(labels):
        for j,key in enumerate(group):
            nodes[key]=card(key,[(col-1)*4,1.5-j*1.1,0],COLORS[col],1.1,.6)
    edges=[]
    for a,b,c in support:
        edges.append(VGroup(Line(nodes[a].get_right(),nodes[b].get_left(),color=MUTED),Line(nodes[b].get_right(),nodes[c].get_left(),color=MUTED)))
    return nodes,edges,support
class LaserScene(Scene):
    index=1
    def construct(self):
        row=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
        self.add(txt('행렬곱의 계산량 · 07',16,MUTED).move_to([-4.4,3.65,0]),txt(row['title'],32).move_to([0,3.03,0]))
        getattr(self,'part'+str(self.index))()
        d=row['storyboard_seconds']
        if self.time>d+.1:raise ValueError((self.index,self.time,d))
        if d-self.time>1e-6:self.wait(d-self.time)
    def to(self,t):
        if self.time>t+.1:raise ValueError((self.index,self.time,t))
        if t-self.time>1e-6:self.wait(t-self.time)
    def foot(self,s):self.play(FadeIn(txt(s,18,MUTED).move_to([0,-3.45,0])),run_time=.5)
    def show_net(self,alternate=False):
        nodes,edges,support=network(alternate)
        self.play(*[Create(e) for e in edges],*[FadeIn(n) for n in nodes.values()])
        self.add(*nodes.values())
        return nodes,edges,support
    def part1(self):
        a=block('작은 텐서',[-4.5,.9,0],GREEN,3.5,1.5)
        b=block('거대한 계산 구조',[0,.9,0],GOLD,3.5,1.5)
        c=block('독립 행렬곱 추출',[4.5,.9,0],CYAN,3.5,1.5)
        self.play(FadeIn(a));self.to(4);self.play(FadeIn(b),Create(Arrow(a.get_right(),b.get_left())))
        self.to(8);self.play(FadeIn(txt('그 안에서 원하는 계산을 골라낼 수 있을까?',29,GOLD).move_to([0,-1,0])))
        self.to(12);self.play(FadeIn(c),Create(Arrow(b.get_right(),c.get_left())))
        self.to(17);self.play(FadeIn(txt('일부를 버려도, 유용한 행렬곱을 남긴다',29,GREEN).move_to([0,-2.2,0])))
        self.foot('목적: 추출한 구조로 더 좋은 계산 복잡도 상한을 증명')
    def part2(self):
        n,e,s=self.show_net()
        self.play(Write(math(r'T=x_1y_1z_1+x_1y_2z_2+x_2y_3z_3',[0,-1.7,0],34)))
        self.to(6);self.play(Indicate(n['x1']),e[0].animate.set_color(RED),e[1].animate.set_color(RED))
        self.play(FadeIn(txt('첫째 · 둘째: X를 공유',26,RED).move_to([0,-2.4,0])))
        self.to(13);self.play(e[0].animate.set_color(GREEN),e[2].animate.set_color(GREEN),Indicate(n['x2']))
        self.to(18);self.play(FadeIn(txt('첫째 · 셋째: X / Y / Z 모두 분리',25,GREEN).move_to([0,2.3,0])))
        self.foot('독립성 모형 · 행렬곱 자체가 아님 · Z는 출력 좌표를 표시')
    def part3(self):
        n,e,s=self.show_net()
        restore_objects=[n['x1'],n['y1'],n['y2'],e[0],e[1]]
        for o in restore_objects:o.save_state()
        caption=txt('먼저 x₁ = 0 ?',30,RED).move_to([0,-1.5,0]);self.play(FadeIn(caption))
        self.to(5);self.play(n['x1'].animate.set_opacity(.15),e[0].animate.set_opacity(.08),e[1].animate.set_opacity(.08),n['y1'].animate.set_opacity(.2),n['y2'].animate.set_opacity(.2))
        failure=txt('첫째 항도 함께 사라진다',26,RED).move_to([0,-2.3,0]);self.play(FadeIn(failure))
        self.to(11);self.play(*[Restore(o) for o in restore_objects],FadeOut(failure),Transform(caption,txt('복원한 뒤 y₂ = 0',30,GOLD).move_to([0,-1.5,0])))
        self.to(16);self.play(n['y2'].animate.set_opacity(.15),e[1].animate.set_opacity(.08),n['z2'].animate.set_opacity(.15),e[0].animate.set_color(GREEN),e[2].animate.set_color(GREEN))
        self.to(21);self.play(Write(math(r"T'=x_1y_1z_1+x_2y_3z_3",[0,2.3,0],32,GREEN)))
        self.foot('변수 제거 → 그 변수를 포함한 모든 항이 사라짐')
    def part4(self):
        cells=VGroup(*[block('계산 블록',[(j-1)*3,(.5-i)*1.2,0],COLORS[(i+j)%3],2.5,.9) for i in range(2) for j in range(3)])
        links=VGroup(*[Line(cells[i].get_center(),cells[j].get_center(),color=MUTED,stroke_opacity=.45) for i,j in [(0,1),(1,2),(0,3),(1,4),(2,5),(3,4),(4,5),(0,4),(1,5)]])
        self.play(Create(links),FadeIn(cells))
        self.to(6);self.play(FadeIn(txt('변수를 제거하면 유용한 블록도 사라질 수 있다',26,RED).move_to([0,-1.6,0])))
        self.to(10);self.play(cells[1].animate.set_opacity(.15),cells[4].animate.set_opacity(.15),links.animate.set_opacity(.15))
        self.to(15);self.play(FadeIn(txt('얼마나 지웠나 → 무엇을 남겼나',32,GOLD).move_to([0,-2.35,0])))
        self.to(22);self.play(FadeOut(cells),FadeOut(links),FadeIn(txt('왜 계산을 버리면서 독립성을 얻을까?',30,GREEN).move_to([0,.8,0])))
        self.foot('얽힌 블록의 개념도 · 특정 변수 제거의 결과를 계산한 예제가 아님')
    def part5(self):
        a=block('원래 텐서 T',[-4.5,.8,0],CYAN,3.4,1)
        b=block('거듭제곱 T⊗k',[0,.8,0],GOLD,3.4,1)
        c=block('변수 제한',[4.5,.8,0],GREEN,3.4,1)
        self.play(FadeIn(a),Write(math(r'\underline R(T)\le r',[-4.5,-.3,0],30)))
        self.to(6);self.play(FadeIn(b),Create(Arrow(a.get_right(),b.get_left())),Write(math(r'\underline R(T^{\otimes k})\le r^k',[0,-.3,0],29)))
        self.to(13);self.play(FadeIn(c),Create(Arrow(b.get_right(),c.get_left())))
        self.play(FadeIn(txt('上限은 증가하지 않음'.replace('上限','상한'),25,GREEN).move_to([4.5,-.35,0])))
        self.to(19);self.play(Write(math(r'D=M_n\oplus\cdots\oplus M_n\quad(q\text{ copies})',[0,-1.5,0],32,GREEN)))
        self.to(24);self.play(Write(math(r'\underline R(D)\le \underline R(T^{\otimes k})\le r^k',[0,-2.4,0],33)))
        self.foot('조건: 잔여 텐서가 정확히 독립적인 행렬곱 직합이어야 함')
    def part6(self):
        role=txt('5막의 점근적 합 부등식: 추출한 구조를 상한으로',28,GOLD).move_to([0,1.65,0])
        self.play(FadeIn(role))
        cards=[block('q\n독립 문제 개수',[-4,.05,0],CYAN,3.5,1.5),block('n\n각 행렬 크기',[0,.05,0],GREEN,3.5,1.5),block('rᵏ\n보더 랭크 상한',[4,.05,0],GOLD,3.5,1.5)]
        for c in cards:self.play(FadeIn(c))
        self.to(9);formula=math(r'q\,n^\omega\le r^k',[0,-1.5,0],44,GOLD);self.play(Write(formula))
        self.to(13);self.play(FadeOut(formula),FadeIn(txt('같은 비용 상한 → 더 크고 많은 독립 행렬곱',27,GREEN).move_to([0,-1.5,0])))
        self.to(16);self.play(FadeIn(txt('추출한 구조 → 더 좋은 ω 상한의 증명',30,GOLD).move_to([0,-2.4,0])))
        self.foot('제거 자체가 상한 개선은 아님 · 확보한 규모와 비용을 비교 · n ≥ 2')
