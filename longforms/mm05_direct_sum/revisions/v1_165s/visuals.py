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
class DirectSumScene(Scene):
    index=1
    def construct(self):
        row=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
        self.add(txt('행렬곱의 계산량 · 05',16,MUTED).move_to([-4.4,3.65,0]),txt(row['title'],32).move_to([0,3.03,0]))
        getattr(self,'part'+str(self.index))()
        d=row['storyboard_seconds']
        if self.time>d+.05:raise ValueError((self.index,self.time,d))
        self.wait(max(0,d-self.time))
    def to(self,t):
        if self.time>t+.1:raise ValueError((self.index,self.time,t))
        self.wait(max(0,t-self.time))
    def foot(self,s):self.play(FadeIn(txt(s,19,MUTED).move_to([0,-3.45,0])),run_time=.5)
    def part1(self):
        rows=VGroup()
        for i,(y,c) in enumerate(zip([1.5,0,-1.5],COLORS),1):
            a=block('A'+str(i),[-4.4,y,0],c,1.3,.8);b=block('B'+str(i),[-2.5,y,0],c,1.3,.8)
            op=block('行列곱'.replace('行列','행렬'),[.1,y,0],c,2,.8);out=block('C'+str(i),[4,y,0],c,1.6,.8)
            arrows=VGroup(Arrow(b.get_right(),op.get_left(),buff=.1,color=c),Arrow(op.get_right(),out.get_left(),buff=.1,color=c))
            rows.add(VGroup(a,b,op,out,arrows));self.play(FadeIn(rows[-1]),run_time=1)
        self.to(8)
        self.play(Indicate(rows[0][0]),Indicate(rows[0][3]),run_time=1.4)
        self.play(FadeIn(txt('첫 입력만 변경 → 나머지 두 입력은 그대로',26,CYAN).move_to([0,-2.6,0])))
        self.to(13);self.foot('서로 다른 계산 사이에 입력·출력 연결 없음 · 모든 입력을 독립적으로 선택')
    def part2(self):
        tiles=VGroup(*[block('계산 '+str(i+1),[x,.4,0],c) for i,(x,c) in enumerate(zip([-4,0,4],COLORS))])
        self.play(FadeIn(tiles));self.to(4)
        grid=bundle([-2.6,.1,0]);self.play(*[Transform(tiles[i],grid[4*i]) for i in range(3)],run_time=2)
        zeros=VGroup(*[grid[k] for k in range(9) if k not in [0,4,8]]);self.play(FadeIn(zeros))
        label=txt('계산 간 교차 계수 = 0',27,GOLD).move_to([3.3,1.3,0]);self.play(FadeIn(label))
        self.to(11)
        for text,y in [('X₁ / X₂ / X₃',.4),('Y₁ / Y₂ / Y₃',-.3),('Z₁ / Z₂ / Z₃',-1)]:self.play(FadeIn(txt(text,25,CYAN).move_to([3.3,y,0])),run_time=.6)
        self.to(16);self.play(Write(math(r'D=T_1\oplus T_2\oplus T_3',[0,-2.35,0],37,GREEN)))
        self.foot('3차 텐서의 블록 분리를 축약한 개념도 · 일반적인 큰 행렬곱 전체와는 다름')
    def part3(self):
        groups=VGroup()
        for i,c in enumerate(COLORS):
            y=1.5-i*1.35
            pieces=VGroup(*[Square(.24,color=c,fill_color=c,fill_opacity=.6).move_to([-4.7+j*.4,y,0]) for j in range(4)])
            groups.add(pieces);self.add(txt('T'+str(i+1),23,c).move_to([-5.6,y,0]))
        self.play(FadeIn(groups));self.foot('작은 사각형은 단순항 묶음의 개념도 · 실제 항 수를 뜻하지 않음')
        box=RoundedRectangle(width=5,height=3.9,color=INK).move_to([3,.2,0]);self.play(Create(box))
        moved=groups.copy().shift(RIGHT*6.5);self.to(5);self.play(TransformFromCopy(groups,moved),run_time=2)
        self.play(FadeIn(txt('같은 분해를 담으면 개수도 그대로',25,GOLD).move_to([0,-2.6,0])))
        self.to(11);self.play(Indicate(box),FadeIn(txt('전체를 다시 분해한다면?',26,GREEN).move_to([3,2.4,0])))
        self.to(16);self.play(Write(math(r'R(D)\le R(T_1)+R(T_2)+R(T_3)',[0,-1.95,0],30,CYAN)))
        self.to(20);self.play(FadeIn(txt('일반 텐서에서 등호는 보장되지 않음 · 이 세 문제의 절약을 주장하지 않음',22,GOLD).move_to([0,-2.9,0])))
    def part4(self):
        d=bundle([-4,.1,0],.8);self.play(FadeIn(d))
        self.play(Create(Arrow([-2.2,.1,0],[-.7,.1,0],color=CYAN)))
        area=Circle(radius=1.5,color=CYAN,fill_color=CYAN,fill_opacity=.08).move_to([2.6,.1,0])
        self.play(Create(DashedVMobject(area,num_dashes=45)))
        target=Dot([4.1,.1,0],color=GOLD);self.play(FadeIn(target),FadeIn(txt('목표 D: 직합 전체',24,GOLD).move_to([3.6,2.05,0])))
        self.to(8)
        dot=Dot([1.6,-.5,0],color=GREEN);self.play(FadeIn(dot))
        path=VMobject(color=GREEN).set_points_smoothly([[1.6,-.5,0],[2.4,-.4,0],[3.3,-.05,0],[3.95,.1,0]])
        self.play(Create(path),MoveAlongPath(dot,path),run_time=3)
        self.to(13);self.play(Write(math(r'\underline R(D)\le R',[0,-2,0],43,GREEN)))
        self.play(FadeIn(txt('R: 묶음 전체에 대한 상한',26).move_to([0,-2.75,0])))
        self.foot('폐포 접근의 개념도 · R은 수치가 정해지지 않은 기호 · 문제별 비용 배분이 아님')
    def part5(self):
        a=VGroup(*[block(str(i+1),[-4.8+i*.8,1.8,0],COLORS[i],.65,.5) for i in range(3)])
        b=a.copy().shift(RIGHT*6.8);self.play(FadeIn(a),FadeIn(b))
        pair_label=txt('3개 × 3개: 모든 쌍',24,GOLD).move_to([0,1.8,0]);self.play(FadeIn(pair_label))
        pairs=VGroup()
        for i in range(3):
            for j in range(3):
                cell=block(f'({i+1},{j+1})',[-3.5+j*1.1,.5-i*.65,0],COLORS[i],.95,.55);pairs.add(cell)
                self.play(TransformFromCopy(VGroup(a[i],b[j]),cell),run_time=.35)
        self.to(8)
        info=VGroup(txt('독립 문제 9개',26,CYAN).move_to([3.5,.55,0]),txt('각 크기: m² × m²',26,GREEN).move_to([3.5,-.25,0]),txt('보더 랭크 상한: R²',26,GOLD).move_to([3.5,-1.05,0]))
        self.play(FadeIn(info));self.to(13)
        self.play(FadeOut(a),FadeOut(b),FadeOut(pairs),FadeOut(info),FadeOut(pair_label))
        columns=VGroup(*[block(t,[x,.55,0],c,3.6,1.25) for t,x,c in [('문제 수  3ᵏ',-4.1,CYAN),('각 한 변  mᵏ',0,GREEN),('분해 상한  Rᵏ',4.1,GOLD)]])
        repeat_label=txt('반복 결합: 개수와 크기가 함께 커진다',27).move_to([0,-.6,0]);self.play(FadeIn(columns));self.play(FadeIn(repeat_label))
        self.to(22)
        theorem=block('쇤하게의 점근적 합 부등식',[0,-1.65,0],GREEN,8,.8);self.play(FadeIn(theorem))
        self.to(27);self.play(FadeOut(columns),FadeOut(repeat_label),theorem.animate.move_to([0,1.2,0]))
        eq=math(r'3m^{\omega}\le R',[0,-.1,0],48,GOLD);self.play(Write(eq))
        self.to(32);self.play(Write(math(r'\omega\le\log_m(R/3)',[0,-1.25,0],40,GREEN)))
        self.play(FadeIn(txt('R이 작을수록 → 더 낮은 지수 상한',25).move_to([0,-2.35,0])))
        self.foot('복소수 · 같은 크기 m≥2인 독립 행렬곱 3개 · 보더 랭크≤R, R>3 · 정리 적용, 증명은 생략')
    def part6(self):
        d=bundle([-3.4,.2,0]);self.play(FadeIn(d))
        tags=VGroup(*[block(t,[3.2,y,0],c,4.5,.75) for t,y,c in [('얼마나 많은 문제?',1.3,CYAN),('각 문제는 얼마나 큰가?',.25,GREEN),('전체 보더 랭크 상한은?',-.8,GOLD)]])
        for tag in tags:self.play(FadeIn(tag))
        self.to(10);self.play(FadeIn(txt('묶기 자체가 아니라, 규모와 분해 비용의 관계를 찾는다',26,GOLD).move_to([0,-2.3,0])))
        self.to(17);self.play(FadeOut(d),FadeOut(tags))
        copies=VGroup(*[block('T',[x,.4,0],CYAN,1.7,1.1) for x in [-4,-2,0,2,4]])
        self.play(FadeIn(copies),run_time=1.5)
        self.play(FadeIn(txt('반복 결합한 구조 안에서 독립적인 행렬곱을 찾을 수 있을까?',25).move_to([0,-.9,0])))
        self.to(25);self.play(FadeIn(txt('다음: 텐서 거듭제곱',30,GREEN).move_to([0,-2.2,0])))
        self.foot('보더 랭크 상한은 실제 실행 시간이 아님 · 정확한 계산으로의 변환 비용을 별도로 분석')
