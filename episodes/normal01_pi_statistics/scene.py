"""152s, 26 replaceable native-portrait scenes using approved sentence endpoints."""
import sys,json,math,os
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from episodes.padic01_local_global.scene import PadicScene,txt,eq
import longforms.qcs01_speed.direction as shared
shared.FPS=30
config.frame_rate=30
config.background_color='#10141C'
INK,MUTED,BLUE,GOLD,GREEN,RED,PURPLE='#E5E7EB','#94A3B8','#60A5FA','#FACC15','#4ADE80','#F87171','#A78BFA'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
MODEL=json.loads((HERE/'model_data.json').read_text(encoding='utf-8'))
def e(s,y=0,size=48,color=INK,x=0,width=7.2):return eq(s,y,size,color,x,width)
def t(s,y=0,size=30,color=INK,x=0,width=7.2):return txt(s,y,size,color,x,width)
def box(s,x,y,color=BLUE,w=3.2,h=1.1,size=35):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,color=color,stroke_width=1.4,fill_color=color,fill_opacity=.06),t(s,size=size,color=color,width=w-.25)).move_to([x,y,0])
def row(s,y=0,hi=(),size=44):
    g=VGroup(*[e(c,size=size,color=GOLD if i in hi else INK) for i,c in enumerate(s)]).arrange(RIGHT,buff=.06)
    if g.width>7.1:g.scale_to_fit_width(7.1)
    return g.move_to([0,y,0])
def line(y=0,start=0,end=1,length=6.8,step=.1):
    return NumberLine(x_range=[start,end,step],length=length,include_numbers=False,color=MUTED,stroke_width=1.5).move_to([0,y,0])
def endpoints(n,a=0,b=1,y=None):
    yy=n.get_y()-.48 if y is None else y
    return VGroup(e(str(a),yy,25,MUTED,x=n.n2p(a)[0]),e(str(b),yy,25,MUTED,x=n.n2p(b)[0]))
def bars(values,y=-.7,height=3.2,color=BLUE,top=.15,labels=True,reference=None,percent=True):
    g=VGroup(Line([-3.5,y,0],[3.5,y,0],color=MUTED,stroke_width=1.1))
    for i,v in enumerate(values):
        x=(i-4.5)*.68;h=max(.015,v/top*height)
        g.add(Rectangle(width=.46,height=h,stroke_width=0,fill_color=color[i] if isinstance(color,list) else color,fill_opacity=.83).move_to([x,y+h/2,0]))
        if labels:g.add(e(str(i),y-.38,26,MUTED,x=x))
        if percent:g.add(t(f'{100*v:.1f}%',y+h+.26,17,INK,x=x,width=.65))
    if reference is not None:
        ry=y+reference/top*height
        g.add(DashedLine([-3.6,ry,0],[3.6,ry,0],color=GOLD,stroke_width=1.5),e(r'1/10',ry+.65,26,GOLD,x=3.1))
    return g
def prefix(y=3.8):return row('0.14358261…',y,hi=(4,5),size=53)
def interval_zoom(y=-.4):
    n=line(y,.35,.36,6.6,.002)
    band=Rectangle(width=6.6,height=.65,fill_color=GOLD,fill_opacity=.09,stroke_width=1,color=GOLD).move_to(n)
    ends=endpoints(n,.35,.36)
    closed=Dot(n.n2p(.35),radius=.08,color=GOLD)
    opened=Circle(radius=.08,color=GOLD,fill_color=config.background_color,fill_opacity=1).move_to(n.n2p(.36))
    return n,VGroup(band,n,ends,closed,opened)
class NormalScene(PadicScene):
    data=DATA
    def to(self,target):
        # Freeze static holds, but split exactly at each approved caption boundary.
        # Animations still update captions frame by frame via the inherited updater.
        while True:
            now=self.offset+self.time
            remaining=round((target-now)*30)
            if remaining<0:raise RuntimeError(f'{self.shot+1}: overrun {now} > {target}')
            if not remaining:return
            boundary=min([target]+[r['start'] for r in self.data['sentences'] if now+1/60<r['start']<target])
            frames=round((boundary-now)*30)
            self.update_caption(self.caption)
            self.wait(frames/30-1e-8,frozen_frame=True)
    def setup(self):
        super().setup();self.remove(self.header)
        self.header=VGroup(t('NUMBER THEORY  /  NORMAL NUMBERS',7.15,17,MUTED),Line([-3.8,6.65,0],[3.8,6.65,0],color=MUTED,stroke_width=1,stroke_opacity=.3))
        self.add(self.header)
    def change(self,a,b,run_time=.65):
        self.play(ReplacementTransform(a,b),run_time=run_time);return b
    def s01(self):
        c=Circle(radius=1.1,color=BLUE).move_to([0,3,0]);d=Line([-1.1,3,0],[1.1,3,0],color=GOLD)
        self.play(Create(c),Create(d),run_time=.65)
        self.show(e('C',3.6,30,BLUE,x=1.35),e('d',2.65,30,GOLD),e(r'\pi=\frac Cd',.7,65),run_time=.55);self.to(2)
        digits=MODEL['pi_digits']
        rows=VGroup(*[e(('3.' if i==0 else '')+digits[i*16:(i+1)*16],-1-i*.72,40,BLUE if i==0 else INK) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(r,shift=DOWN*.2) for r in rows],lag_ratio=.15),run_time=2)
        self.show(e(r'\vdots',-4,40,MUTED),run_time=.3)
    def s02(self):
        outer=RoundedRectangle(width=7.25,height=7.4,corner_radius=.16,color=MUTED,stroke_width=1.2).move_to([0,.6,0])
        self.show(outer,t('실수 ℝ',4,29,MUTED),run_time=.4)
        alg=RoundedRectangle(width=4.2,height=6,corner_radius=.12,color=BLUE,fill_color=BLUE,fill_opacity=.04).move_to([-1.2,.35,0])
        tr=RoundedRectangle(width=2.2,height=6,corner_radius=.12,color=PURPLE,fill_color=PURPLE,fill_opacity=.04).move_to([2.2,.35,0])
        self.show(alg,tr,t('대수적 수',2.9,30,BLUE,x=-1.2,width=3.8),t('초월수',2.9,30,PURPLE,x=2.2,width=2),run_time=.5)
        self.show(box('',-1.2,1.5,BLUE,3.5,1.3,30),t('유리수',1.85,26,BLUE,x=-1.2),e(r'\frac12,\;-3,\;\frac27',1.15,32,x=-1.2,width=3.1),run_time=.6)
        self.show(t('대수적 무리수',-.3,29,x=-1.2,width=3.7),e(r'\sqrt2,\;\sqrt3',-1.2,44,x=-1.2,width=3.6),e(r'\pi,\;e',.4,60,PURPLE,x=2.2,width=2),run_time=.6)
        self.show(t('無理數 = 대수적 무리수 + 초월수'.replace('無理數','무리수'),-3.8,25,MUTED))
    def s03(self):
        self.show(e(r'x^2-2=0',3.7,60,BLUE),e(r'x=\sqrt2',2.2,63),t('어떤 관계를 만족하는가?',.95,29,BLUE))
        self.show(e(r'1.414213562373\ldots',-.55,48),run_time=.5)
        b=bars([.1]*10,y=-3.1,height=1.25,color=PURPLE,top=.1,percent=False);b.set_opacity(.3)
        self.show(b,e('?',-1.8,68,PURPLE),t('어떤 분포를 갖는가?',-4.05,29,PURPLE))
    def s04(self):
        g=VGroup()
        for k in range(1,6):
            r=row('1'+'0'*k,4-(k-1)*1.1,size=42);r[0].set_color(BLUE)
            for o in r[1:]:o.set_color(RED)
            r.shift(LEFT*1.4);g.add(r)
            self.show(r,t(f'{k}개의 0',r.get_y(),27,MUTED,x=2.1,width=2),run_time=.5)
        self.show(e(r'x=0.10100100010000\ldots',-2.5,43),t('1 사이의 0이 하나씩 늘어난다',-3.8,27,MUTED),run_time=.5)
    def s05(self):
        self.show(e(r'0.1\underbrace{0}_{1}1\underbrace{00}_{2}1\underbrace{000}_{3}1\underbrace{0000}_{4}\cdots',2.5,48))
        self.show(e(r'1,2,3,4,\ldots\longrightarrow\infty',.1,47,RED),t('0의 연속 길이는 끝없이 증가',-1.4,30))
        self.show(t('결국 반복되는 주기가 없다 → 무리수',-3.1,31,BLUE))
    def s06(self):
        heading=t('완성한 블록 수 m = 5',4.5,30);self.add(heading)
        current=None
        for m in [5,10,30,100]:
            zeros=m*(m+1)//2;total=m*(m+3)//2
            g=bars([zeros/total,m/total]+[0]*8,y=-.7,height=3.5,top=1,color=[RED,BLUE]+[MUTED]*8,percent=False)
            g.add(t(f'0: {zeros/total:.1%}     1: {m/total:.1%}',-1.8,32),t(f'전체 {total:,}자리 · 0 {zeros:,}개 · 1 {m}개',-2.8,26,MUTED))
            if current is None:self.show(g,run_time=.4)
            else:self.change(current,g,.65)
            current=g;self.play(Transform(heading,t(f'완성한 블록 수 m = {m}',4.5,30)),run_time=.2)
        self.show(e(r'\frac{\#0}{N}=\frac{m+1}{m+3}\longrightarrow1',-4.05,40,RED),run_time=.4)
    def s07(self):
        self.show(e(r'x=0.10100100010000\ldots',3.2,49),box('무리수',-1.9,.7,BLUE,3.2,1.6),box('균등한 숫자 분포',1.9,.7,RED,3.2,1.6,27))
        self.show(e(r'\not\Rightarrow',.7,53,RED),e(r'\text{Irrational}\;\not\Rightarrow\;\text{Normal}',-1.7,46),t('무리성과 정규성은 다른 성질',-3.5,30,MUTED))
    def s08(self):
        center=e('x',4.1,70);self.show(center)
        self.show(Line([0,3.3,0],[-1.9,2.4,0],color=BLUE),Line([0,3.3,0],[1.9,2.4,0],color=PURPLE),box('대수적 성질',-1.9,1.5,BLUE,3.3,1.4),box('통계적 성질',1.9,1.5,PURPLE,3.3,1.4))
        self.show(e('P(x)=0',-.4,43,BLUE,x=-1.9,width=3.1),t('빈도 · 분포',-.4,29,PURPLE,x=1.9,width=3.1),t('관계와 표현',-2.1,27,MUTED,x=-1.9,width=3.1),t('숫자 배열의 비율',-2.1,27,MUTED,x=1.9,width=3.1))
    def s09(self):
        self.show(t('정규수',4.1,52,PURPLE),t('Normal in base 10',2.9,26,MUTED),bars([.1]*10,y=-1.9,height=2.4,top=.12,color=GREEN,percent=False,reference=.1))
        self.show(t('모든 유한 숫자 배열의 극한 빈도',-3.6,30),t('아래 그래프는 한 자리 조건만 표시',-4.35,22,MUTED))
    def s10(self):
        tiles=VGroup(*[box(str(i),(i-4.5)*.68,3.9,BLUE,.54,.65,29) for i in range(10)])
        self.show(tiles,bars([.1]*10,y=-.9,height=2.6,top=.12,color=GREEN,percent=False,reference=.1))
        self.play(LaggedStart(*[Indicate(z,color=GREEN) for z in tiles],lag_ratio=.07),run_time=1.2)
        self.show(e(r'\lim_{N\to\infty}\frac{C_d(N)}{N}=\frac1{10}',-2.6,51),e(r'd=0,1,\ldots,9',-3.9,34,MUTED))
    def s11(self):
        grid=VGroup(*[Square(side_length=.17,fill_color=GOLD if i==35 else PURPLE,fill_opacity=.8 if i==35 else .16,stroke_width=.4,color=MUTED).move_to([-2.8+(i%10)*.2,3.65-(i//10)*.2,0]) for i in range(100)])
        self.show(grid,t('두 자리 배열',4.5,28,PURPLE),e(r'10^2=100',3.2,43,x=1.4,width=3.2),e(r'35\ \longrightarrow\ \frac1{100}',1.9,47,GOLD,x=1.2,width=3.6))
        self.to(59);self.show(Line([-3.5,.6,0],[3.5,.6,0],color=MUTED,stroke_opacity=.3),e(r'000,001,\ldots,999',-.6,44,PURPLE),e(r'10^3=1000',-1.9,46),e(r'358\ \longrightarrow\ \frac1{1000}',-3.3,51,GREEN))
    def s12(self):
        self.show(t('長さ k の'.replace('長さ k の','길이 k인')+' 모든 숫자 배열',4.3,32,PURPLE),e(r'w=a_1a_2\cdots a_k',2.8,61,GOLD))
        self.show(e(r'\underbrace{10\times10\times\cdots\times10}_{k\text{ times}}=10^k',.5,48))
        self.show(e(r'\lim_{N\to\infty}\frac{C_w(N)}N=10^{-k}',-1.8,61,GREEN),t('모든 k와 모든 배열 w에 대해',-3.3,29),t('Cw(N): 첫 N개 시작 위치에서 세며 겹침도 허용',-4.2,21,MUTED))
    def s13(self):
        self.show(e(r'x=0.d_1d_2d_3d_4d_5\ldots',3.7,54))
        for i,s in enumerate([r'd_1d_2d_3\ldots',r'd_2d_3d_4\ldots',r'd_3d_4d_5\ldots']):
            self.show(box('',0,1.8-i*1.2,PURPLE,5.5,.85,29),e(s,1.8-i*1.2,38,PURPLE),run_time=.3)
        n=line(-3.3);self.show(n,endpoints(n),run_time=.3)
    def s14(self):
        a=prefix(3.7);self.add(a)
        self.show(e(r'\times10',2.25,40,GOLD),run_time=.3)
        b=row('1.4358261…',.75,hi=(0,),size=55);self.play(TransformFromCopy(a,b),run_time=.6)
        self.show(t('정수 부분 제거',-.7,27,RED),run_time=.3)
        c=row('0.4358261…',-2.15,size=55);self.play(TransformFromCopy(b,c),b[0].animate.set_color(RED),run_time=.6)
        self.show(e(r'\{y\}=y-\lfloor y\rfloor',-3.9,40,MUTED),run_time=.3)
    def s15(self):
        formula=e(r'x_n=\{10^n x_0\}',4.3,53,PURPLE);self.add(formula)
        n=line(-1.2);self.show(n,endpoints(n),run_time=.4)
        current=None;dots=VGroup()
        for i,value in enumerate(MODEL['orbit'][:5]):
            s=MODEL['seed'][i:i+8]
            label=e(f'x_{i}=0.{s}\\ldots',2.55,54,GOLD if i==2 else INK)
            if current is None:self.show(label,run_time=.3)
            else:self.change(current,label,.4)
            current=label;dot=Dot(n.n2p(value),radius=.085,color=GOLD if i==2 else PURPLE);dots.add(dot)
            self.play(TransformFromCopy(label,dot),run_time=.45)
        self.show(t('같은 숫자열의 다음 자리 → 새로운 점',-3.5,28,MUTED),run_time=.3)
    def s16(self):
        self.show(e(r'x_2=0.\underline{35}8261\ldots',4.2,58,GOLD),e(r'0.35\le x_2<0.36',2.75,50))
        n=line(.8);ticks=VGroup(*[Line(n.n2p(i/100)+DOWN*.09,n.n2p(i/100)+UP*.09,color=MUTED,stroke_width=.7) for i in range(101)])
        marker=Rectangle(width=.068,height=.5,fill_color=GOLD,fill_opacity=.9,stroke_width=0).move_to(n.n2p(.355))
        self.show(n,ticks,endpoints(n),marker,run_time=.6);self.to(87)
        z,zg=interval_zoom(-2.3)
        connectors=VGroup(DashedLine(n.n2p(.35),z.n2p(.35)+UP*.45,color=MUTED),DashedLine(n.n2p(.36),z.n2p(.36)+UP*.45,color=MUTED))
        self.show(connectors,zg,run_time=.7)
        dot=Dot(z.n2p(MODEL['orbit'][2]),color=GREEN,radius=.09)
        self.play(TransformFromCopy(marker,dot),run_time=.7)
        self.show(e(r'0.358261\ldots',-1.55,36,GREEN,x=1.3,width=3.5),t('35라는 배열 ↔ 이 구간을 방문',-4.15,29,GOLD),run_time=.4)
    def s17(self):
        n,g=interval_zoom(2.0);self.add(g)
        brace=BraceBetweenPoints(n.n2p(.35)+DOWN*.8,n.n2p(.36)+DOWN*.8,direction=DOWN,color=GREEN)
        self.show(brace,e(r'0.36-0.35=\frac1{100}',-.7,61,GREEN),t('숫자 배열 35에 대응하는 구간의 길이',-3.3,28,MUTED),run_time=.5)
    def s18(self):
        self.show(e(r'x_n=\{10^nx_0\}',4.1,50,PURPLE),t('모든 구간을 길이에 비례해 방문한다면',2.9,29))
        n=line(1.4);self.show(n,endpoints(n),run_time=.4)
        # Stratified midpoints are explicitly a schematic, not pi's orbit.
        pts=VGroup(*[Dot(n.n2p((i+.5)/40)+UP*(.45+(i%4)*.16),radius=.032,color=PURPLE) for i in range(40)])
        self.play(LaggedStart(*[FadeIn(p) for p in pts],lag_ratio=.02),run_time=.9)
        self.show(t('균등분포의 개념도 · π의 실제 궤적 아님',.1,23,MUTED),run_time=.3)
        self.show(e(r'\frac{\#\{0\le n<N:x_n\in[a,b)\}}N',-1.35,45),e(r'\xrightarrow[N\to\infty]{}\ b-a',-2.7,43,GREEN),t('10진법 정규성 ⇔ 이 수열의 균등분포',-4.1,30,PURPLE))
    def s19(self):
        self.show(e(r'\pi',2.4,120,BLUE),t('10진법에서 정규수일까?',-.1,38),e('?',-2.1,93,GOLD),run_time=.5)
    def s20(self):
        heading=t('실제 π 소수점 아래 100자리',4.4,29,BLUE);self.add(heading)
        current=None
        for n in [100,1000,10000]:
            sample=MODEL['samples'][str(n)]
            g=bars(sample['frequencies'],y=-.8,height=3.1,top=.16,color=BLUE,reference=.1)
            if current is None:self.show(g,run_time=.4)
            else:self.change(current,g,.55)
            current=g;self.play(Transform(heading,t(f'실제 π 소수점 아래 {n:,}자리',4.4,29,BLUE)),run_time=.2)
            if n==100:self.to(106)
            if n==1000:self.to(107.5)
        sample=MODEL['samples']['10000']
        self.show(t(f"배열 35: {sample['count35']}회 / 시작 위치 {sample['positions']:,}개",-2.3,27,GOLD),t('고정밀 계산 데이터 · 유한 표본의 관찰',-3.35,27,MUTED),t('이 그래프는 정규성의 증명이 아니다',-4.25,27,RED),run_time=.4)
    def s21(self):
        self.show(t('유한한 관찰',4.4,30,BLUE),e(r'\frac{C_d(N)}N\approx\frac1{10}',2.9,57,BLUE))
        self.show(e(r'\not\Rightarrow',.85,72,RED),t('무한한 자릿수에 관한 증명',-.45,30,GOLD),e(r'\lim_{N\to\infty}\frac{C_d(N)}N=\frac1{10}',-2.0,55))
        self.show(t('π에서는 한 자리의 이 조건도 미해결',-3.8,30,GOLD),t('d = 0, 1, …, 9',-4.5,22,MUTED))
    def s22(self):
        self.show(e('1909',4.4,52,GOLD),t('Émile Borel',3.3,32,MUTED),t('거의 모든 실수는 정규수',1.9,39,GREEN))
        rect=Rectangle(width=6.8,height=2.1,color=GREEN,fill_color=GREEN,fill_opacity=.16).move_to([0,-.1,0]);self.show(rect)
        self.show(e(r'\lambda(\mathcal N\cap[0,1])=1',-.1,51,GREEN),t('정규수가 아닌 실수들의 집합은 측도 0',-1.9,28,MUTED))
        self.show(t('“거의 모든” = 르베그 측도의 의미',-3.2,28),t('특정 상수에 대한 판정은 별개의 문제',-4.25,27,GOLD))
    def s23(self):
        self.show(e(r'\lambda(\mathcal N\cap[0,1])=1',4,52,GREEN),t('전체에 관한 정리',2.8,29,GREEN))
        for x,s,d in [(-2.5,r'\pi','3.14159…'),(0,'e','2.71828…'),(2.5,r'\sqrt2','1.41421…')]:
            self.show(box('',x,-.2,PURPLE,2.15,3.2),e(s,.7,55,x=x,width=1.9),t(d,-.5,23,MUTED,x=x,width=1.9),e('?',-1.3,45,GOLD,x=x),run_time=.4)
        self.show(t('각 수의 10진법 정규성은 미해결',-3.2,31,GOLD),t('측도 1인 집합도 특정 원소의 포함을 보장하지 않는다',-4.25,23,MUTED))
    def s24(self):
        c=Circle(radius=.75,color=BLUE).move_to([0,3.65,0]);d=Line([-.75,3.65,0],[.75,3.65,0],color=GOLD)
        self.show(c,d,e(r'\pi=C/d',2.1,49,BLUE),run_time=.5)
        self.show(e('3.141592653589…',.5,45),bars(MODEL['samples']['10000']['frequencies'],y=-2.5,height=1.4,top=.15,color=PURPLE,percent=False),run_time=.5)
        self.show(t('定義'.replace('定義','정의')+'는 정확하다 · 분포의 증명은 남아 있다',-4,29,MUTED))
    def s25(self):
        center=VGroup(Circle(radius=.85,color=PURPLE),t('정규성',size=31,color=PURPLE)).move_to([0,.4,0]);self.show(center)
        for s,x,y,c in [('정수론',0,3.7,BLUE),('확률론',-2.4,-1.6,GREEN),('동역학계',2.4,-1.6,PURPLE)]:
            node=box(s,x,y,c,2.5,1,29);self.show(Line(center.get_center(),node.get_center(),color=c,stroke_opacity=.5),node,run_time=.4)
        self.show(e(r'\pi,\ e,\ \sqrt2',4.7,35,BLUE),e(r'10^{-k}',-3.1,44,GREEN,x=-2.1,width=3),e(r'T(x)=\{10x\}',-3.1,34,PURPLE,x=2,width=3.4))
    def s26(self):
        self.show(t('수학적 관계',4.1,30,BLUE),e(r'\pi=\frac Cd',2.8,63,BLUE),e('3.141592653589…',1.1,47))
        self.show(Line([-3.4,-.1,0],[3.4,-.1,0],color=MUTED,stroke_opacity=.3),t('표현 속에서 나타나는 성질',-1.1,31,PURPLE),e(r'\lim_{N\to\infty}\frac{C_w(N)}N\ \stackrel{?}{=}\ 10^{-k}',-2.6,52,GOLD))
        self.show(t('수를 표현하는 것에서, 수를 이해하는 것으로',-4.15,28))

# Explicit replaceable scene classes for Manim discovery and content-aware caching.
class Shot01(NormalScene): shot=0
class Shot02(NormalScene): shot=1
class Shot03(NormalScene): shot=2
class Shot04(NormalScene): shot=3
class Shot05(NormalScene): shot=4
class Shot06(NormalScene): shot=5
class Shot07(NormalScene): shot=6
class Shot08(NormalScene): shot=7
class Shot09(NormalScene): shot=8
class Shot10(NormalScene): shot=9
class Shot11(NormalScene): shot=10
class Shot12(NormalScene): shot=11
class Shot13(NormalScene): shot=12
class Shot14(NormalScene): shot=13
class Shot15(NormalScene): shot=14
class Shot16(NormalScene): shot=15
class Shot17(NormalScene): shot=16
class Shot18(NormalScene): shot=17
class Shot19(NormalScene): shot=18
class Shot20(NormalScene): shot=19
class Shot21(NormalScene): shot=20
class Shot22(NormalScene): shot=21
class Shot23(NormalScene): shot=22
class Shot24(NormalScene): shot=23
class Shot25(NormalScene): shot=24
class Shot26(NormalScene): shot=25
