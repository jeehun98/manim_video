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
        d=row['duration_seconds'] or row['storyboard_seconds']
        if self.time>d+.05:raise ValueError((self.index,self.time,d))
        self.wait(max(0,d-self.time))
    def to(self,t):
        if self.time>t+.1:raise ValueError((self.index,self.time,t))
        self.wait(max(0,t-self.time))
    def foot(self,s):self.play(FadeIn(txt(s,19,MUTED).move_to([0,-3.45,0])),run_time=.5)

    def part1(self):
        tiles=VGroup(*[block('2×2 행렬곱 '+str(i+1),[x,.4,0],c,3.4,1.2) for i,(x,c) in enumerate(zip([-4.3,0,4.3],COLORS))])
        self.play(FadeIn(tiles))
        inputs=VGroup(*[txt('A'+str(i+1)+' · B'+str(i+1)+' → C'+str(i+1),24,c).move_to([x,-.8,0]) for i,(x,c) in enumerate(zip([-4.3,0,4.3],COLORS))])
        self.to(5);self.play(FadeIn(inputs));self.to(10)
        grid=bundle([-2.5,.15,0])
        self.play(FadeOut(inputs),*[Transform(tiles[i],grid[4*i]) for i in range(3)],run_time=2)
        self.play(FadeIn(VGroup(*[grid[k] for k in range(9) if k not in [0,4,8]])))
        self.play(FadeIn(txt('독립 계산을 나란히 담은 직합',26,GREEN).move_to([3,1,0])))
        self.play(Write(math(r'D=T_1\oplus T_2\oplus T_3',[2.9,-.2,0],31,GOLD)))
        self.foot('세 변수 그룹이 모두 분리된 텐서의 개념도 · 일반적인 6×6 행렬곱 전체가 아님')
    def part2(self):
        groups=VGroup()
        for i,c in enumerate(COLORS):
            y=1.5-i*1.15
            pieces=VGroup(*[Square(.22,color=c,fill_color=c,fill_opacity=.5).move_to([-2.1+j*.42,y,0]) for j in range(7)])
            groups.add(pieces)
            self.add(txt('T'+str(i+1)+' : 7항',24,c).move_to([-4.7,y,0]))
            self.play(FadeIn(pieces),run_time=.8)
        eq=math('7+7+7=21',[3.4,.4,0],42,GOLD);self.play(Write(eq))
        self.to(6)
        box=RoundedRectangle(width=4,height=3.7,color=INK).move_to([-.8,.4,0]);self.play(Create(box))
        self.play(FadeIn(txt('같은 항을 묶어도 21항',25,GOLD).move_to([0,-2.1,0])))
        self.to(12)
        border=math(r'\underline R(D)\le r',[3.3,-.75,0],35,GREEN);self.play(Write(border))
        self.to(17);self.play(FadeIn(txt('r = 21: 이미 확보한 기준 상한',26,GREEN).move_to([0,-2.8,0])))
        self.foot('21은 세 Strassen 분해로 얻은 상한 · 최소값이라고 주장하지 않음 · r<21은 미제시')
    def part3(self):
        def grid(cols,rows,w,h,spacing,label,center):
            v=VGroup()
            for i in range(rows):
                for j in range(cols):
                    x=(j-(cols-1)/2)*spacing[0]+center[0];y=((rows-1)/2-i)*spacing[1]+center[1]
                    v.add(block(label,[x,y,0],COLORS[i%3],w,h))
            return v
        initial=grid(3,1,2,1,(2.5,0),'2×2',[-1,0])
        badge=txt('1회: 3개의 2×2',29,GOLD).move_to([0,2,0]);self.play(FadeIn(initial),FadeIn(badge))
        self.to(8)
        second=grid(3,3,.9,.6,(1.1,.8),'4×4',[-3.7,0])
        for i in range(3):
            self.play(*[TransformFromCopy(initial[i],second[3*i+j]) for j in range(3)],run_time=1)
        self.play(FadeOut(initial),Transform(badge,txt('2회: 9개의 4×4',29,GOLD).move_to(badge)))
        mapping=VGroup(txt('행 번호의 쌍',25,CYAN),txt('(1,1)  (1,2)  (2,1)  (2,2)',24,CYAN),txt('4개의 행 · 열도 4개',25,GREEN)).arrange(DOWN,buff=.35).move_to([2.8,.1,0])
        self.to(13);self.play(FadeIn(mapping));self.play(Indicate(second),run_time=1.2)
        self.to(21)
        third=grid(9,3,.85,.6,(1.05,.85),'8×8',[0,0])
        self.play(FadeOut(mapping),run_time=.4)
        for i in range(3):
            self.play(*[TransformFromCopy(second[3*i+j],VGroup(*[third[i*9+j*3+k] for k in range(3)])) for j in range(3)],run_time=.6)
        self.play(FadeOut(second),Transform(badge,txt('3회: 27개의 8×8',29,GOLD).move_to(badge)),run_time=.6)
        self.to(24);self.play(FadeIn(txt('문제 수 ×3     |     각 한 변 ×2',28,GREEN).move_to([0,-1.9,0])))
        self.to(28);self.play(FadeIn(txt('3개의 2×2  →  9개의 4×4  →  27개의 8×8',26).move_to([0,-2.65,0])))
        self.foot('계산 관계의 텐서곱 · 결과 행렬끼리 다시 곱하는 과정이 아님')
    def part4(self):
        xs=[-5,-2.8,.1,4]
        heads=['반복','독립 문제 수','각 행렬 크기','보더 랭크 상한']
        for x,t in zip(xs,heads):self.add(txt(t,24,GOLD if x==4 else INK).move_to([x,1.9,0]))
        values=[['1','3',r'2\times2',r'r'],['2','9',r'4\times4',r'r^2'],['3','27',r'8\times8',r'r^3'],['k',r'3^k',r'2^k\times2^k',r'r^k']]
        for i,row in enumerate(values[:3]):
            for j,value in enumerate(row[:3]):self.add(math(value,[xs[j],.95-i*.85,0],32,CYAN if j==1 else GREEN))
        self.to(2)
        for i,row in enumerate(values[:3]):self.play(Write(math(row[3],[4,.95-i*.85,0],35,GOLD)),run_time=1)
        self.to(10)
        for j,value in enumerate(values[3]):self.play(Write(math(value,[xs[j],-1.6,0],32,GOLD if j==3 else GREEN)),run_time=.5)
        self.to(17)
        left=Rectangle(width=6.2,height=4.1,color=CYAN).move_to([-.9,.1,0])
        right=RoundedRectangle(width=3.6,height=4.1,color=GOLD).move_to([4,.1,0])
        self.play(Create(left),Create(right))
        self.play(FadeIn(txt('계산 규모의 성장  ↔  분해 상한의 성장',27,GOLD).move_to([0,-2.7,0])))
        self.foot('r은 첫 직합의 보더 랭크 상한으로 확보된 값 · rᵏ도 상한이며 실행 시간은 아님')
    def part5(self):
        theorem=block('쇤하게의 점근적 합 부등식',[0,2,0],GREEN,9,.65);self.play(FadeIn(theorem))
        self.to(3)
        condition=math(r'\underline R(D)\le r\quad\Longrightarrow\quad 3\cdot2^\omega\le r',[0,.7,0],36,GOLD);self.play(Write(condition))
        self.play(FadeIn(txt('ω: 행렬곱의 최적 성장 지수',24,MUTED).move_to([0,-.15,0])))
        self.to(12);self.play(FadeIn(txt('기준 사례: 각각 Strassen → r = 21',26,CYAN).move_to([0,-1.1,0])))
        self.to(14)
        numerical=math(r'3\cdot2^\omega\le21',[0,-2,0],38,GOLD);self.play(Write(numerical))
        self.to(18);self.play(Transform(numerical,math(r'2^\omega\le7',[0,-2,0],40,GOLD)))
        self.to(20);self.play(Transform(numerical,math(r'\omega\le\log_2 7\approx2.807',[0,-2,0],40,GREEN)))
        self.to(26);self.play(FadeIn(txt('Strassen의 상한 그대로 · 새로운 개선은 없음',27,GREEN).move_to([0,-2.85,0])))
        self.to(30);self.foot('복소수 · 독립적인 2×2 행렬곱 3개 · r>3 · r<21 분해를 발견했다는 주장이 아님')
    def part6(self):
        d=bundle([-3.4,.3,0]);self.play(FadeIn(d))
        tags=VGroup(*[block(t,[3.1,y,0],c,4.6,.7) for t,y,c in [('문제 수',1.35,CYAN),('각 문제의 크기',.3,GREEN),('전체 보더 랭크 상한',-.75,GOLD)]])
        self.play(FadeIn(tags));self.to(6)
        line=txt('묶기 자체보다, 규모를 효율적으로 담는 구조',26,GOLD).move_to([0,-2.3,0]);self.play(FadeIn(line))
        self.to(13);self.play(FadeOut(d),FadeOut(tags),FadeOut(line))
        self.play(Write(math(r'T\otimes T\otimes T\otimes\cdots',[0,.4,0],48,CYAN)))
        self.play(FadeIn(txt('그 안에서 많은 독립적인 행렬곱을 찾을 수 있을까?',26).move_to([0,-.7,0])))
        self.to(18);self.play(FadeIn(txt('다음: 텐서 거듭제곱',29,GREEN).move_to([0,-2.1,0])))
        self.foot('보더 랭크와 실제 실행 시간은 다름 · 정확한 계산으로 변환하는 비용은 별도 분석')
