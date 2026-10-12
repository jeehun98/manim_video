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
class PowerScene(Scene):
    index=1
    def construct(self):
        row=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
        self.add(txt('행렬곱의 계산량 · 06',16,MUTED).move_to([-4.4,3.65,0]),txt(row['title'],32).move_to([0,3.03,0]))
        getattr(self,'part'+str(self.index))()
        d=row['duration_seconds'] or row['storyboard_seconds']
        if self.time>d+.05:raise ValueError((self.index,self.time,d))
        self.wait(max(0,d-self.time))
    def to(self,t):
        if self.time>t+.1:raise ValueError((self.index,self.time,t))
        self.wait(max(0,t-self.time))
    def foot(self,s):self.play(FadeIn(txt(s,19,MUTED).move_to([0,-3.45,0])),run_time=.5)
    def part1(self):
        one=bundle([-3.2,.2,0],.85);two=bundle([3.2,.2,0],.85)
        self.play(FadeIn(one));self.to(4);self.play(TransformFromCopy(one,two))
        mark=math(r'\otimes',[0,.2,0],48,GOLD);self.play(Write(mark))
        question=txt('자기 자신과 결합한다는 것은?',28,GOLD).move_to([0,-2.1,0]);self.play(FadeIn(question))
        self.to(10)
        focus=block('2×2 행렬곱의 계산 관계',[0,.3,0],CYAN,7,1.6)
        self.play(TransformFromCopy(one[0],focus),FadeOut(one),FadeOut(two),FadeOut(mark),run_time=1.5)
        self.to(14);self.play(Transform(question,txt('한 블록을 확대해서 직접 확인하자',27,GREEN).move_to(question)))
    def part2(self):
        a=matrix([[1,2],[3,4]],[-4,.2],.85,CYAN);b=matrix([[5,6],[7,8]],[-.4,.2],.85,GREEN)
        c=matrix([[19,22],[43,50]],[3.7,.2],.85,GOLD)
        for t,x in [('A',-4),('B',-.4),('C',3.7)]:self.add(txt(t,27).move_to([x,1.65,0]))
        self.play(FadeIn(a),FadeIn(b),FadeIn(c))
        self.play(FadeIn(txt('행 i=1',25,CYAN).move_to([-4,2.2,0])),FadeIn(txt('열 k=1',25,GOLD).move_to([3.7,2.2,0])))
        self.to(5)
        equation=math(r'C_{11}=1\cdot5+2\cdot7=19',[0,-2.1,0],37,GOLD)
        for j in range(2):
            paths=VGroup(CurvedArrow(a[j].get_bottom(),b[j*2].get_bottom(),angle=.3,color=COLORS[j]),Arrow(b[j*2].get_right(),c[0].get_left(),buff=.15,color=COLORS[j]))
            label=txt('가운데 번호 j='+str(j+1),26,COLORS[j]).move_to([0,-1.3,0])
            self.play(Indicate(a[j]),Indicate(b[j*2]),Create(paths),FadeIn(label),run_time=1.2)
            self.wait(1.2);self.play(FadeOut(paths),FadeOut(label),run_time=.4)
        self.play(Write(equation));self.to(15);self.play(Indicate(c[0]))
        self.foot('행 i · 가운데 j · 열 k의 연결 규칙은 입력 숫자가 바뀌어도 유지')
    def part3(self):
        left=VGroup(*[block(str(i+1),[-3.2+i*1.5,1.7,0],CYAN,1,.65) for i in range(2)])
        right=VGroup(*[block(str(i+1),[1.7+i*1.5,1.7,0],GREEN,1,.65) for i in range(2)])
        self.play(FadeIn(left),FadeIn(right))
        self.play(FadeIn(txt('첫 관계의 번호',22,CYAN).move_to([-2.45,2.35,0])),FadeIn(txt('둘째 관계의 번호',22,GREEN).move_to([2.45,2.35,0])))
        pairs=VGroup()
        self.to(4)
        for index,(i,j) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
            pair=block(f'({i+1},{j+1})',[-4.8+index*3.2,-.05,0],GOLD,2.3,.9);pairs.add(pair)
            self.play(TransformFromCopy(VGroup(left[i],right[j]),pair),run_time=.8)
        self.to(10)
        self.play(FadeOut(left),FadeOut(right))
        grid=matrix([['·']*4 for _ in range(4)],[2,.0],.55,CYAN)
        row_labels=VGroup();col_labels=VGroup()
        for n,text in enumerate(['(1,1)','(1,2)','(2,1)','(2,2)']):
            row_labels.add(txt(text,22,GOLD).move_to([.2,.825-n*.55,0]))
            col_labels.add(txt(text,19,GREEN).move_to([1.175+n*.55,1.45,0]))
        self.play(*[pairs[i].animate.move_to([-4,1.15-i*.75,0]).scale(.65) for i in range(4)],FadeIn(grid),run_time=1.5)
        for i in range(4):self.play(TransformFromCopy(pairs[i],row_labels[i]),TransformFromCopy(pairs[i],col_labels[i]),run_time=.6)
        self.to(18);self.play(FadeIn(txt('2 × 2가지 선택 → 4개의 새 번호',28,GREEN).move_to([0,-2.2,0])))
        self.foot('행 · 열뿐 아니라 가운데 번호도 두 번호의 쌍으로 결합')
    def part4(self):
        a=matrix([[1,2,3,4],['·']*4,['·']*4,['·']*4],[-4.4,.3],.5,CYAN)
        b=matrix([[1,'·','·','·'],[2,'·','·','·'],[3,'·','·','·'],[4,'·','·','·']],[-.5,.3],.5,GREEN)
        c=matrix([['?','·','·','·'],['·']*4,['·']*4,['·']*4],[4,.3],.5,GOLD)
        self.play(FadeIn(a),FadeIn(b),FadeIn(c))
        for label,x,col in [('A',-4.4,CYAN),('B',-.5,GREEN),('C',4,GOLD)]:self.add(txt(label+' 4×4',24,col).move_to([x,1.8,0]))
        route=txt('가운데 번호쌍을 따라 합산',24).move_to([0,2.35,0]);self.play(FadeIn(route))
        self.to(4)
        products=VGroup()
        for j,pair in enumerate(['(1,1)','(1,2)','(2,1)','(2,2)']):
            paths=VGroup(CurvedArrow(a[j].get_bottom(),b[j*4].get_bottom(),angle=.25,color=COLORS[j%3]),Arrow(b[j*4].get_right(),c[0].get_left(),buff=.12,color=COLORS[j%3]))
            term=math(f'{j+1}'+r'\cdot'+f'{j+1}={((j+1)**2)}',[-4.5+j*3,-1.9,0],29,COLORS[j%3]);products.add(term)
            self.play(Transform(route,txt('가운데 번호 '+pair,26,COLORS[j%3]).move_to(route)),Indicate(a[j]),Indicate(b[j*4]),Create(paths),run_time=.7)
            self.play(FadeIn(term),run_time=.5);self.wait(.6);self.play(FadeOut(paths),run_time=.2)
        self.to(14)
        equation=math('1+4+9+16=30',[0,-2.7,0],35,GOLD);self.play(Write(equation))
        self.play(Transform(c[0][1],txt('30',23,GOLD).move_to(c[0][1])))
        self.play(Indicate(c[0]),run_time=.6)
        self.to(18)
        rule=math(r"C_{(i,i'),(k,k')}=\sum_{j,j'=1}^{2} A_{(i,i'),(j,j')}B_{(j,j'),(k,k')}",[0,-1.9,0],27,CYAN)
        self.play(FadeOut(products),Write(rule))
        self.foot('4×4 입력은 자유롭게 선택 · 숫자는 별도 예제 · 행렬곱의 네 항 합산 규칙을 확인')
    def part5(self):
        labels=['2×2','4×4','8×8'];sizes=[2,4,8];grids=VGroup()
        for i,n in enumerate(sizes):
            x=[-4.5,0,4.5][i]
            g=matrix([['']*n for _ in range(n)],[x,.1],2/n,COLORS[i]);grids.add(g)
            self.add(txt(labels[i],30,COLORS[i]).move_to([x,1.8,0]),txt('인자 '+str(i+1)+'개',23,MUTED).move_to([x,-1.5,0]))
        self.play(FadeIn(grids[0]));self.to(3);self.play(TransformFromCopy(grids[0],grids[1]),run_time=1.3)
        self.to(6);self.play(TransformFromCopy(grids[1],grids[2]),run_time=1.3)
        self.to(10);self.play(Write(math(r'M_2^{\otimes k}\cong M_{2^k}',[0,-2.4,0],44,GOLD)))
        self.foot('인자 k개를 결합 · 숫자 결과가 아닌 계산 관계 자체의 거듭제곱')
    def part6(self):
        equation=math('T=P+Q+S',[0,2,0],40,GOLD);self.play(Write(equation))
        pieces=VGroup(*[block(t,[x,.4,0],c,2.4,1) for t,x,c in zip(['P','Q','S'],[-3.2,0,3.2],COLORS)])
        self.play(FadeIn(pieces));self.to(5)
        grid=combo_grid()
        for i in range(3):self.play(*[TransformFromCopy(VGroup(pieces[i],pieces[j]),grid[3*i+j]) for j in range(3)],run_time=1)
        self.play(FadeOut(pieces));self.to(12)
        self.play(FadeIn(txt('3가지 × 3가지 = 9개 조합',28,GREEN).move_to([0,-2.3,0])))
        self.to(17);self.foot('P,Q,S는 부분 텐서 · 독립성 또는 행렬곱 구조를 가정하지 않음 · 보통 합, 직합 아님')
    def part7(self):
        grid=combo_grid().scale(.72).move_to([0,.2,0]);self.play(FadeIn(grid))
        self.play(FadeIn(txt('9개 조합 ≠ 독립 행렬곱 9개',28,GOLD).move_to([0,2.2,0])))
        self.to(4);self.play(FadeOut(grid))
        a=block('공유 a = 2',[-3.8,.15,0],GOLD,3,1)
        p1=block('2 × 3 = 6',[2.7,1.1,0],CYAN,3.8,.8)
        p2=block('2 × 7 = 14',[2.7,-.75,0],GREEN,3.8,.8)
        links=VGroup(Arrow(a.get_right(),p1.get_left(),buff=.12,color=CYAN),Arrow(a.get_right(),p2.get_left(),buff=.12,color=GREEN))
        self.play(FadeIn(a),FadeIn(p1),FadeIn(p2),Create(links))
        self.to(9)
        self.play(Transform(a,block('공유 a = 5',[-3.8,.15,0],GOLD,3,1)),Transform(p1,block('5 × 3 = 15',[2.7,1.1,0],CYAN,3.8,.8)),Transform(p2,block('5 × 7 = 35',[2.7,-.75,0],GREEN,3.8,.8)),run_time=1.5)
        self.play(FadeIn(txt('처음부터 같은 입력을 사용한다',25,GOLD).move_to([0,-2.05,0])))
        self.to(15);self.play(Write(math(r'a b_1 z_1+a b_2 z_2',[0,-2.8,0],31,CYAN)))
        self.foot('공유 변수의 작은 예제 · z는 출력 위치 표식 · 일반 9개 조합 전체와 동일한 구조는 아님')
    def part8(self):
        term1=block('a₁ b₁ z₁',[-4,1,0],CYAN,3.4,1)
        term2=block('a₂ b₂ z₂',[0,1,0],GREEN,3.4,1)
        term3=block('a₁ b₃ z₂',[4,1,0],RED,3.4,1)
        self.play(FadeIn(term1),FadeIn(term2),FadeIn(term3))
        self.play(FadeIn(txt('작은 예제: 세 번째 항이 변수를 공유',25,MUTED).move_to([0,2.1,0])))
        self.to(4);zero=math('b_3=0',[0,-.4,0],44,GOLD);self.play(Write(zero))
        self.play(Indicate(term3),run_time=.7);self.play(FadeOut(term3),FadeIn(txt('0',32,RED).move_to([4,1,0])),run_time=.8)
        self.to(8);self.play(FadeIn(txt('남은 두 항: 입력·출력 변수 모두 분리',26,GREEN).move_to([0,-1.5,0])))
        self.to(12);self.play(FadeIn(txt('다음: Laser Method',32,GOLD).move_to([0,-2.4,0])))
        self.foot('허용된 변수 0 치환의 작은 예제 · 임의 항 삭제나 전체 레이저 방법의 증명이 아님')
