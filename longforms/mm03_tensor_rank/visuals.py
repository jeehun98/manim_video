from pathlib import Path
import json
from manim import *
from tensor_data import *
ROOT=Path(__file__).resolve().parent
config.background_color='#081622';config.frame_width=14.222222222;config.frame_height=8
INK='#EAF5FB';MUTED='#8FAABD';CYAN='#51D8EE';GREEN='#8BE0B1';GOLD='#F4C978';RED='#FF8B8B'

def txt(s,size=26,color=INK,width=12.2):
    o=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if o.width>width:o.scale_to_fit_width(width)
    return o
def box(s,pos,color=CYAN,w=1.35,h=.6):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.1,color=color,fill_color=color,fill_opacity=.08),txt(s,23,color,w-.15)).move_to(pos)
def column(values,x,y=1.65,color=CYAN):
    return VGroup(*[box(str(s),[x,y-i*.72,0],color) for i,s in enumerate(values)])
def formula(s,pos,size=34,color=INK):return MathTex(s,font_size=size,color=color).move_to(pos)

class TensorScene(Scene):
    index=1
    def construct(self):
        r=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
        self.add(txt('행렬곱의 계산량 · 새로운 3장',16,MUTED).move_to([-4.4,3.65,0]),txt(r['title'],32).move_to([0,3.03,0]))
        getattr(self,'part'+str(self.index))()
        duration=r['duration_seconds'] or r['storyboard_seconds']
        if self.time>duration:raise ValueError((self.index,self.time,duration))
        self.wait(duration-self.time)
    def to(self,t):
        if self.time>t+.1:raise ValueError((self.index,self.time,t))
        if t>self.time:self.wait(t-self.time)
    def foot(self,s):self.play(FadeIn(txt(s,21,GOLD).move_to([0,-3.45,0])),run_time=.5)

    def part1(self):
        a=column(['a = 1','b = 2','c = 3','d = 4'],-5.1);b=column(['e = 5','f = 6','g = 7','h = 8'],-2.7);c=column(['c₁₁ = ?','c₁₂ = ?','c₂₁ = ?','c₂₂ = ?'],5,color=GREEN)
        self.play(FadeIn(a),FadeIn(b),FadeIn(c))
        self.add(txt('입력 A',22,CYAN).move_to([-5.1,2.3,0]),txt('입력 B',22,CYAN).move_to([-2.7,2.3,0]),txt('출력 C',22,GREEN).move_to([5,2.3,0]))
        self.to(9)
        nodes=VGroup();edges=VGroup()
        for s,(i,j,k) in enumerate(PAIRS):
            y=1.9-s*.47;node=box(f'{X[i]}×{Y[j]}',[1.1,y,0],GOLD,w=1.5,h=.39)
            links=VGroup(Line(a[i].get_right(),node.get_left(),color=CYAN,stroke_width=1.1,stroke_opacity=.5),Line(b[j].get_right(),node.get_left(),color=CYAN,stroke_width=1.1,stroke_opacity=.5),Arrow(node.get_right(),c[k].get_left(),color=GOLD,buff=.08,stroke_width=1.5))
            self.play(FadeIn(node),Create(links),run_time=.5)
            if s<2:
                token=txt(str(X[i]*Y[j]),23,GOLD).move_to(node)
                self.play(token.animate.move_to(c[k]),run_time=.7);self.remove(token)
            if s%2==1:
                value=[19,22,43,50][k]
                self.play(Transform(c[k][1],txt(f'c{["₁₁","₁₂","₂₁","₂₂"][k]}={value}',22,GREEN).move_to(c[k][1])),run_time=.35)
            nodes.add(node);edges.add(links)
        self.to(17)
        self.play(FadeIn(txt('두 입력 위치 → 곱셈 → 해당 출력에 더하기',27,GOLD).move_to([0,-2.45,0])))
        self.foot('8개의 표준 곱셈 연결 · 숫자가 바뀌어도 계수 관계는 동일')

    def part2(self):
        left=box('1 + 4 = 5',[-3.6,1.55,0],w=3);right=box('5 + 8 = 13',[.3,1.55,0],w=3)
        product=box('M₁ = 65',[-1.65,.25,0],GOLD,w=3)
        self.play(FadeIn(left),FadeIn(right));self.play(Create(Arrow(left.get_bottom(),product.get_top(),buff=.1,color=CYAN)),Create(Arrow(right.get_bottom(),product.get_top(),buff=.1,color=CYAN)),FadeIn(product))
        self.to(5)
        out=column(['c₁₁','c₁₂','c₂₁','c₂₂'],4.8,y=1.45,color=GREEN);self.play(FadeIn(out))
        for k in [0,3]:
            arrow=Arrow(product.get_right(),out[k].get_left(),buff=.1,color=GOLD)
            token=txt('+65',25,GOLD).move_to(product)
            self.play(Create(arrow),token.animate.move_to(out[k]),run_time=1);self.remove(token)
        self.to(9)
        self.play(FadeIn(formula(r'(a+d)(e+h)',[-1.65,-1.2,0],37,CYAN)))
        self.play(FadeIn(txt('M₁의 기여: [65, 0, 0, 65]',27,GOLD).move_to([0,-2.05,0])))
        self.to(11)
        self.play(FadeIn(txt('나머지 6곱까지 합친 최종 출력: [19, 22, 43, 50]',24,GREEN).move_to([0,-2.8,0])))
        self.foot('한 중간 곱의 기여분 ≠ 최종 답 · 같은 곱을 여러 출력에서 재사용')

    def part3(self):
        for x,title in [(-4.4,'A 입력 계수 u'),(-.4,'B 입력 계수 v'),(4,'출력 계수 w')]:self.add(txt(title,24,CYAN).move_to([x,2.25,0]))
        cols=[column([1,0,0,1],x) for x in [-4.4,-.4,4]]
        self.play(*[FadeIn(c) for c in cols])
        for c in cols:self.play(Indicate(c[0],color=GOLD),Indicate(c[3],color=GOLD),run_time=.6)
        orders=VGroup(txt('a  b  c  d',20,MUTED).move_to([-4.4,-1,0]),txt('e  f  g  h',20,MUTED).move_to([-.4,-1,0]),txt('c₁₁  c₁₂  c₂₁  c₂₂',20,MUTED).move_to([4,-1,0]))
        self.play(FadeIn(orders));self.to(3.8)
        a=formula(r'u^Tx=a+d=5',[-4.4,-1.65,0],28,CYAN);b=formula(r'v^Ty=e+h=13',[-.4,-1.65,0],28,CYAN)
        self.play(Write(a));self.to(9)
        self.play(Write(b));self.to(14)
        mult=box('5 × 13 = 65',[0,-2.35,0],GOLD,w=3.2);self.play(FadeIn(mult))
        self.play(Create(Arrow(mult.get_right(),cols[2][0].get_left(),buff=.1,color=GOLD)),Create(Arrow(mult.get_right(),cols[2][3].get_left(),buff=.1,color=GOLD)))
        self.to(20)
        self.play(FadeOut(a),FadeOut(b),FadeOut(mult),FadeOut(orders),*[FadeOut(o) for o in list(self.mobjects) if isinstance(o,Arrow)])
        self.play(Write(formula(r'(u^Tx)(v^Ty)w=(65,0,0,65)^T',[0,-1.65,0],36,GREEN)))
        self.play(FadeIn(txt('모든 입력에서: (a+d)(e+h) · (1,0,0,1)ᵀ',25,CYAN).move_to([0,-2.55,0])))
        self.foot('w는 고정 출력 분배 규칙 · 새로운 세 번째 입력이 아님')

    def coefficient_panels(self,tensor):
        panels=VGroup()
        for k in range(4):
            x=-4.7+k*3.1;panel=VGroup()
            panel.add(txt(['c₁₁','c₁₂','c₂₁','c₂₂'][k],24,GREEN).move_to([x,1.65,0]))
            for j,ch in enumerate('efgh'):panel.add(txt(ch,16,MUTED).move_to([x+(j-1.5)*.48,1.1,0]))
            for i,ch in enumerate('abcd'):panel.add(txt(ch,16,MUTED).move_to([x-1.2,.66-i*.48,0]))
            for i in range(4):
                for j in range(4):
                    value=int(tensor[i,j,k]);pos=[x+(j-1.5)*.48,.66-i*.48,0]
                    square=Square(side_length=.46,color=MUTED,stroke_width=.8,fill_color=RED if value<0 else GREEN,fill_opacity=.25 if value else 0).move_to(pos)
                    panel.add(VGroup(square,txt(str(value) if value else '·',19,RED if value<0 else GREEN).move_to(pos)))
            panels.add(panel)
        return panels

    def part4(self):
        panels=self.coefficient_panels(TARGET);self.play(FadeIn(panels))
        caption=txt('행: A 입력 위치 · 열: B 입력 위치 · 표: 출력 위치',23,MUTED).move_to([0,-1.65,0]);self.play(FadeIn(caption))
        detail=formula(r'T_{ijk}\text{ : coefficient of }x_i y_j\text{ in }z_k',[0,-2.35,0],29,CYAN)
        self.play(FadeIn(detail));self.to(13)
        axes=VGroup(*[box(t,[x,2.25,0],c,w=3.6) for t,x,c in [('축 1: A 입력 위치',-4.2,CYAN),('축 2: B 입력 위치',0,CYAN),('축 3: C 출력 위치',4.2,GREEN)]])
        self.play(FadeIn(axes))
        for panel in panels:self.play(Indicate(panel[0],color=GREEN),run_time=.5)
        self.play(Transform(caption,txt('세 번째 축 = 곱이 기여하는 출력 위치 · 추가 입력이 아님',24,GREEN).move_to(caption)))
        self.to(19)
        self.play(FadeOut(axes))
        status=txt('표준 방법: 8개의 단순 항 → 같은 8개 계수',26,GOLD).move_to([0,2.25,0]);self.play(FadeIn(status),run_time=.5)
        self.to(20.5)
        self.play(Transform(panels,self.coefficient_panels(TERMS[0])),Transform(status,txt('Strassen M₁: 아직 최종 텐서가 아님',25,GOLD).move_to(status)),run_time=.5)
        accumulated=TERMS[0].copy()
        for i in range(1,7):
            accumulated+=TERMS[i]
            self.play(Transform(panels,self.coefficient_panels(accumulated)),Transform(status,txt(f'M₁ + … + M{i+1} : 불필요한 기여 소거',25,GOLD).move_to(status)),run_time=.6)
            self.wait(.3)
        self.to(27)
        self.play(Transform(status,txt('표준 8항 = Strassen 7항 · 64개 계수 모두 일치',26,GREEN).move_to(status)),run_time=.5)
        self.play(FadeIn(formula(r'T_{\rm MM}=\sum_{s=1}^{r}u_s\otimes v_s\otimes w_s',[0,-2.95,0],34,GOLD)),run_time=.5)
        self.foot('4×4×4 계수 구조 · 특정 숫자의 답이 아닌 모든 입력의 계산 관계')

    def part5(self):
        # Reconstruct one tensor term as a physical flow before naming rank.
        left=box('a + d = 5',[-4.2,1.7,0],CYAN,w=2.5)
        right=box('e + h = 13',[-.9,1.7,0],CYAN,w=2.5)
        product=box('5 × 13 = 65',[-2.55,.5,0],GOLD,w=3)
        out=box('[65, 0, 0, 65]',[3.6,.5,0],GREEN,w=3.6)
        term=formula(r'u\otimes v\otimes w',[0,-1.3,0],40,GOLD)
        graph=VGroup(left,right,product,out)
        name=txt('세 계수 벡터의 구조 하나 = 단순항',28,GOLD).move_to([0,1.8,0])
        self.play(Write(term),FadeIn(name))
        self.to(5)
        self.play(FadeOut(name))
        self.to(6)
        self.play(FadeIn(left),FadeIn(right))
        arrows=VGroup(Arrow(left.get_bottom(),product.get_top(),buff=.12,color=CYAN),Arrow(right.get_bottom(),product.get_top(),buff=.12,color=CYAN))
        self.play(Create(arrows),FadeIn(product))
        route=Arrow(product.get_right(),out.get_left(),buff=.15,color=GOLD)
        self.play(Create(route),FadeIn(out))
        token=txt('65',26,GOLD).move_to(product)
        self.play(token.animate.move_to(out),run_time=1);self.remove(token)
        self.play(Indicate(term))
        bridge=txt('두 입력 조합 → 곱셈 1번 → 출력 분배 = 단순항 1개',27,GOLD).move_to([0,-2.25,0])
        self.play(FadeIn(bridge));self.to(16)
        self.play(Indicate(product),Indicate(term))
        self.to(21)
        self.play(*[FadeOut(o) for o in [graph,arrows,route,term,bridge]])
        question=txt('7항이면 충분하다. 6항으로도 가능할까?',32,GOLD).move_to([0,1.8,0])
        self.play(FadeIn(question))
        counts=VGroup(*[box(str(i+1),[-3.6+i*1.2,.65,0],GREEN,w=.9) for i in range(7)])
        self.play(FadeIn(counts));self.to(26)
        definition=txt('정확히 같은 텐서를 만드는 최소 항 개수 = 텐서 랭크',26).move_to([0,-.5,0])
        self.play(FadeIn(definition));self.to(31)
        self.play(FadeOut(question),FadeOut(counts),definition.animate.move_to([0,2.1,0]))
        upper=box('7항 공식: 상한',[-3.7,1.15,0],GREEN,w=4)
        lower=box('6항 이하 불가능: 하한',[3.7,1.15,0],CYAN,w=4.6)
        self.play(FadeIn(upper),Write(formula(r'R(T)\leq7',[-3.7,.25,0],39,GREEN)))
        self.to(35)
        self.play(FadeIn(lower),Write(formula(r'R(T)\geq7',[3.7,.25,0],39,CYAN)))
        self.add(txt('別도의 하한 정리 · Winograd'.replace('別','별'),21,MUTED).move_to([3.7,-.4,0]))
        self.to(39)
        self.play(Write(formula(r'\boxed{R_{\mathbb C}(T_{2\times2})=7}',[0,-1.45,0],47,GOLD)))
        self.foot('쌍선형 곱셈 수의 최소값 · 덧셈·뺄셈과 실행시간은 별도')

    def part6(self):
        self.play(Write(formula(r'T=\sum_{s=1}^{r}u_s\otimes v_s\otimes w_s',[0,2,0],37,CYAN)))
        self.to(5)
        axes=Axes(x_range=[-1,5,1],y_range=[-1,3,1],x_length=8,y_length=2.6,tips=False,axis_config={'include_ticks':False,'stroke_opacity':.4}).move_to([0,-.1,0]);self.play(Create(axes))
        target=Dot(axes.c2p(3.6,1),color=GOLD,radius=.09);label=formula('T',target.get_center()+UP*.4,37,GOLD);moving=Dot(axes.c2p(.2,2.2),color=CYAN)
        self.play(FadeIn(target),FadeIn(label),FadeIn(moving))
        path=VMobject(color=CYAN,stroke_width=2).set_points_smoothly([axes.c2p(.2,2.2),axes.c2p(1.2,.3),axes.c2p(2.6,1.2),axes.c2p(3.45,1.03)])
        self.play(Create(path),MoveAlongPath(moving,path),run_time=3)
        self.play(FadeIn(formula(r'T_{\varepsilon}\longrightarrow T\quad(\varepsilon\to0)',[0,-2.05,0],35,GREEN)))
        self.to(14)
        self.play(FadeIn(txt('정확히 같은 분해와 극한에서 같아지는 분해는 어떻게 다를까?',26,GOLD).move_to([0,-2.85,0])))
        self.foot('일반 텐서 공간의 개념도 · 2×2 행렬곱의 7 미만 분해를 주장하지 않음')
