from pathlib import Path
import json
from manim import *
config.background_color='#081622'
config.frame_width=14.222222222
config.frame_height=8
ROOT=Path(__file__).resolve().parent
INK='#EAF5FB'; CYAN='#51D8EE'; GOLD='#F4C978'; GREEN='#8BE0B1'; MUTED='#8FAABD'
def text(s,size=28,color=INK):
    obj=Text(s,font='Malgun Gothic',font_size=size,color=color)
    if obj.width>12.4: obj.scale_to_fit_width(12.4)
    return obj
def card(s,pos,color=CYAN,w=2.6):
    box=RoundedRectangle(width=w,height=.65,corner_radius=.12,color=color,fill_color=color,fill_opacity=.08)
    label=text(s,23,color)
    if label.width>w-.15:label.scale_to_fit_width(w-.15)
    return VGroup(box,label).move_to(pos)
def matrix(values,pos,label):
    rows=len(values); cells=VGroup()
    for i,row in enumerate(values):
        for j,value in enumerate(row):
            box=Square(side_length=.57,color=MUTED,stroke_width=1)
            cells.add(VGroup(box,text(str(value),22)).move_to([pos[0]+(j-(rows-1)/2)*.6,pos[1]+((rows-1)/2-i)*.6,0]))
    return VGroup(cells,text(label,24,CYAN).move_to([pos[0],pos[1]+rows*.3+.4,0]))
class ChapterScene(Scene):
    index=1
    def construct(self):
        self.record=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
        self.add(text('행렬곱의 계산량 · 1장',17,MUTED).move_to([-4.9,3.65,0]))
        self.add(text(self.record['title'],32).move_to([0,3.05,0]))
        getattr(self,'scene'+str(self.index))()
        remaining=self.record['duration_seconds']-self.time
        if remaining<0:raise ValueError((self.index,self.time))
        self.wait(remaining)
    def to(self,target):
        if self.time>target+.05:raise ValueError((self.index,self.time,target))
        if target>self.time:self.wait(target-self.time)
    def note(self,s):
        obj=text(s,22,GOLD).move_to([0,-3.35,0]);self.play(FadeIn(obj));return obj
    def inputs(self):
        a=matrix([[1,2],[3,4]],[-4,1.7,0],'A');b=matrix([[5,6],[7,8]],[0,1.7,0],'B')
        self.play(FadeIn(a),FadeIn(b));return a,b
    def scene1(self):
        a=matrix([['a11','a12','a13'],['a21','a22','a23'],['a31','a32','a33']],[-4,1,0],'A')
        b=matrix([['b11','b12','b13'],['b21','b22','b23'],['b31','b32','b33']],[0,1,0],'B')
        c=matrix([['?']*3 for _ in range(3)],[4,1,0],'C')
        self.play(FadeIn(a),FadeIn(b),FadeIn(c))
        self.to(4)
        eq=text('c₁₁ = a₁₁b₁₁ + a₁₂b₂₁ + a₁₃b₃₁',32).move_to([0,-.8,0]);self.play(Write(eq))
        for k in range(3):self.play(Indicate(a[0][k]),Indicate(b[0][3*k]),run_time=.7)
        counter=text('곱셈 0번',36,GOLD).move_to([0,-2,0]);self.add(counter)
        for k,cell in enumerate(c[0]):
            new=text(f'곱셈 {(k+1)*3}번',36,GOLD).move_to(counter)
            self.play(Transform(counter,new),Transform(cell[1],text(f'c{k//3+1}{k%3+1}',18,GREEN).move_to(cell[1])),run_time=.4)
        self.to(12)
        self.note('27번은 표준 방법의 비용입니다 · 최소 횟수라는 뜻은 아닙니다')
    def scene2(self):
        a,b=self.inputs();c=matrix([['?','?'],['?','?']],[4,1.7,0],'C');self.play(FadeIn(c));self.to(6)
        equations=['1 × 5 + 2 × 7 = 19','1 × 6 + 2 × 8 = 22','3 × 5 + 4 × 7 = 43','3 × 6 + 4 × 8 = 50']
        nodes=VGroup()
        for i,eq in enumerate(equations):
            row=i//2;col=i%2
            line=text(eq,30).move_to([0,-.1-i*.6,0]);self.play(Write(line),*[Indicate(a[0][row*2+j]) for j in range(2)],*[Indicate(b[0][j*2+col]) for j in range(2)],run_time=1.1)
            value=text(str([19,22,43,50][i]),22,GREEN).move_to(c[0][i][1]);self.play(Transform(c[0][i][1],value),run_time=.4)
            if i==0:self.to(10)
            for j in range(2):nodes.add(card('×',[-5.1+(i*2+j)*1.45,-2.8,0],w=.7))
        self.to(15)
        self.play(LaggedStart(*[FadeIn(n) for n in nodes],lag_ratio=.12))
        self.note('4칸 × 2곱 = 8곱 · 이 여덟 곱을 꼭 따로 계산해야 할까요?')
    def scene3(self):
        a,b=self.inputs();forms=['(1+4) × (5+8)','(3+4) × 5','1 × (6−8)','4 × (7−5)','(1+2) × 8','(3−1) × (5+6)','(2−4) × (7+8)'];values=[65,35,-2,8,24,22,-30]
        results=VGroup();counter=text('0 / 7 곱셈',25,GOLD).move_to([4,1.7,0]);self.add(counter)
        self.to(4)
        for i,(form,val) in enumerate(zip(forms,values)):
            p=[-3.6+(i%2)*6.5,-.1-(i//2)*.72,0]
            formula=card(f'M{i+1} : {form}',p,w=4.5)
            left_ids=[[0,3],[2,3],[0],[3],[0,1],[2,0],[1,3]][i]
            right_ids=[[0,3],[0],[1,3],[2,0],[3],[0,1],[2,3]][i]
            highlights=VGroup(*[SurroundingRectangle(a[0][j],color=GOLD,buff=.04) for j in left_ids],*[SurroundingRectangle(b[0][j],color=GREEN,buff=.04) for j in right_ids])
            self.play(Create(highlights),run_time=.1)
            self.play(TransformFromCopy(VGroup(*[a[0][j] for j in left_ids],*[b[0][j] for j in right_ids]),formula),run_time=.1)
            self.play(FadeOut(highlights),run_time=.1)
            answer=text(f'= {val}',23,GREEN).next_to(formula,RIGHT,buff=.12)
            self.play(FadeIn(answer),Transform(counter,text(f'{i+1} / 7 곱셈',25,GOLD).move_to(counter)),run_time=.1)
            results.add(formula,answer);self.to([9,12,12.6,13.2,13.8,14.4,15][i])
        self.note('각 줄의 곱셈은 한 번 · 준비 단계의 덧셈과 뺄셈은 별도입니다')
    def scene4(self):
        values=[65,35,-2,8,24,22,-30]
        nodes=VGroup(*[card(f'M{i+1} = {v}',[-5.4+i*1.8,1.8,0],w=1.65) for i,v in enumerate(values)])
        self.play(FadeIn(nodes));c=matrix([['?','?'],['?','?']],[4,-.2,0],'복원한 C');self.play(FadeIn(c))
        forms=['65 + 8 − 24 − 30 = 19','−2 + 24 = 22','35 + 8 = 43','65 − 35 − 2 + 22 = 50'];groups=[[0,3,4,6],[2,4],[1,3],[0,1,2,5]]
        for i,(form,ids) in enumerate(zip(forms,groups)):
            target=card(form,[-2,-.1-i*.65,0],GREEN,w=6)
            arrows=VGroup(*[Arrow(nodes[j].get_bottom(),target.get_top(),buff=.1,color=GOLD,stroke_width=2) for j in ids])
            self.play(Create(arrows),FadeIn(target),run_time=1)
            self.play(Transform(c[0][i][1],text(str([19,22,43,50][i]),22,GREEN).move_to(c[0][i][1])),run_time=.4)
            self.to([9,12,14.5,17][i]);self.play(FadeOut(arrows),run_time=.3)
        self.note('표준 결과와 일치: [19, 22; 43, 50] · 숫자 검산 완료')
    def scene5(self):
        self.to(3)
        formula=text('M₁ + M₄ − M₅ + M₇',32,CYAN).move_to([0,2,0]);self.play(Write(formula))
        expanded=text('(a+d)(e+h) + d(g−e) − (a+b)h + (b−d)(g+h)',27).move_to([0,1.2,0]);self.play(Write(expanded),run_time=1)
        terms=['ae','+ah','+de','+dh','+dg','−de','−ah','−bh','+bg','+bh','−dg','−dh']
        tiles=VGroup(*[card(term,[-4.5+(i%6)*1.8,.1-(i//6)*1.1,0],w=1.3) for i,term in enumerate(terms)])
        self.to(5)
        self.play(LaggedStart(*[FadeIn(t) for t in tiles],lag_ratio=.12))
        for i,j in [(1,6),(2,5),(3,11),(4,10),(7,9)]:
            arrow=DoubleArrow(tiles[i].get_center(),tiles[j].get_center(),buff=.2,color=GOLD)
            self.play(tiles[i].animate.set_color(GOLD),tiles[j].animate.set_color(GOLD),Create(arrow),run_time=.35)
            self.play(FadeOut(tiles[i]),FadeOut(tiles[j]),FadeOut(arrow),run_time=.35)
        self.to(12)
        self.play(tiles[0].animate.move_to([-1,-1.8,0]),tiles[8].animate.move_to([1,-1.8,0]))
        self.play(FadeIn(text('c₁₁ = ae + bg',33,GREEN).move_to([0,-2.65,0])))
        others=text('c₁₂ = af + bh     c₂₁ = ce + dg     c₂₂ = cf + dh',23,GREEN).move_to([0,-3.25,0]);self.play(FadeIn(others))
    def scene6(self):
        self.to(3)
        blocks=matrix([['A₁₁','A₁₂'],['A₂₁','A₂₂']],[-3,1.5,0],'행렬 블록 A');other=matrix([['B₁₁','B₁₂'],['B₂₁','B₂₂']],[3,1.5,0],'행렬 블록 B');self.play(FadeIn(blocks),FadeIn(other))
        subtitle=text('숫자 자리에 행렬 블록 · 곱셈 순서는 유지',24,GOLD).move_to([0,.3,0]);self.play(FadeIn(subtitle))
        roots=VGroup(card('표준: 8갈래',[-3,-.5,0]),card('Strassen: 7갈래',[3,-.5,0],GREEN));self.to(8)
        self.play(FadeIn(roots))
        branches=VGroup()
        for x,count,col in [(-3,8,CYAN),(3,7,GREEN)]:
            for i in range(count):
                end=np.array([x-2+i*4/(count-1),-1.65,0]);branches.add(Line([x,-.8,0],end,color=col),Dot(end,radius=.045,color=col))
        self.play(Create(branches));self.to(14)
        self.play(FadeOut(branches),FadeOut(roots),FadeOut(subtitle),FadeOut(blocks),FadeOut(other))
        rows=VGroup(*[text(s,29,GREEN if i else CYAN).move_to([0,1.8-i*.65,0]) for i,s in enumerate(['단계        표준          Strassen','1               8                   7','2             64                 49','3           512               343','4         4,096            2,401'])]);self.play(LaggedStart(*[FadeIn(r) for r in rows],lag_ratio=.3))
        self.play(Write(text('T(n) = 7T(n/2) + O(n²)',30,GOLD).move_to([0,-1.8,0])))
        self.play(Write(text('T(n) = O(n^(log₂7))   ·   log₂7 ≈ 2.8074',28,GREEN).move_to([0,-2.5,0])))
        self.note('표는 말단 곱셈 수 · 덧셈 비용을 포함해도 위 성장 지수 유지')
    def scene7(self):
        axes=Axes(x_range=[0,32,8],y_range=[0,32768,8192],x_length=9,y_length=3.5,axis_config={'include_numbers':True,'font_size':18}).move_to([0,.3,0])
        self.play(Create(axes));curve=axes.plot(lambda x:x**3,x_range=[1,32],color=CYAN);fast=axes.plot(lambda x:x**np.log2(7),x_range=[1,32],color=GREEN)
        self.play(Create(curve),Create(fast),run_time=3)
        self.play(FadeIn(text('표준 n³',25,CYAN).move_to([4.5,2.1,0])),FadeIn(text('Strassen n^(log₂7)',25,GREEN).move_to([3.2,.5,0])))
        self.note('2의 거듭제곱 크기에서 말단 곱셈 수 비교 · 실행시간 그래프가 아닙니다')
        self.to(17);self.play(FadeOut(axes),FadeOut(curve),FadeOut(fast),*[FadeOut(m) for m in list(self.mobjects) if m not in [axes,curve,fast] and m.get_center()[1]<2.5])
        self.play(Write(text('행렬곱의 계산량은\n어디까지 줄일 수 있을까?',42,GOLD).move_to([0,0,0])),run_time=2)
