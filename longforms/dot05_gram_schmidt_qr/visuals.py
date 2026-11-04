"""Construct orthonormal directions, preserve span, and recover the original columns."""
import json,os
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('DOT_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16
config.frame_height=16 if SHORT else 9
config.background_color='#0B1220'
INK='#EDF4FF';GRAY='#8B9CB6';BLUE='#55ACFF';GREEN='#55DFA3';ORANGE='#FFB45F';PURPLE='#BB97FF'
A1=np.array([1.,1.]);A2=np.array([2.,0.]);PROJ=A1.copy();V2=np.array([1.,-1.]);Q1=A1/np.sqrt(2);Q2=V2/np.sqrt(2)
def txt(s,size=30,color=INK,width=7.8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.1)
    if m.width>width:m.scale_to_fit_width(width)
    return m
def colored(parts,size=32,width=7.8):
    g=VGroup(*(txt(s,size,c,width) for s,c in parts)).arrange(RIGHT,buff=.12)
    if g.width>width:g.scale_to_fit_width(width)
    return g
class MatrixWidget(VGroup):
    def __init__(self,name,values,colors,center,factor=None,headers=None,width=6,size=32):
        super().__init__();self.cells={};body=VGroup()
        for i in range(2):
            for j in range(2):
                cell=txt(values[i][j],size,colors[j],width=1).move_to([(j-.5)*1.1,(.5-i)*.86,0]);self.cells[i,j]=cell;body.add(cell)
        for sign in [-1,1]:
            x=sign*1.02
            body.add(Line([x,-.9,0],[x,.9,0],color=GRAY,stroke_width=2),Line([x,.9,0],[x-sign*.18,.9,0],color=GRAY,stroke_width=2),Line([x,-.9,0],[x-sign*.18,-.9,0],color=GRAY,stroke_width=2))
        if headers:
            for j,h in enumerate(headers):body.add(txt(h,21,colors[j],width=1.7).move_to([(j-.5)*1.1,1.27,0]))
        self.add(body);left=body.get_left()[0]
        if factor:
            f=txt(factor,26,INK,width=1.6);f.move_to([left-.2-f.width/2,0,0]);self.add(f);left=f.get_left()[0]
        if name:
            n=txt(name+' =',size,INK,width=1.8);n.move_to([left-.25-n.width/2,0,0]);self.add(n)
        if self.width>width:self.scale_to_fit_width(width)
        self.move_to(center)
        self.columns=[VGroup(self.cells[0,j],self.cells[1,j]) for j in range(2)]
class GramBase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start']
        self.origin=np.array([-1.55,1.4,0]) if SHORT else np.array([-5.15,.15,0]);self.unit=2 if SHORT else 1.55
        self.dual=self.INDEX==6
        self.panel=np.array([0,-2.5,0]) if SHORT else np.array([0,-1.9,0]) if self.dual else np.array([3.6,.45,0])
        self.add(txt('DOT PRO   /   LEVEL 05',19,GRAY).move_to([0,7.2 if SHORT else 3.95,0]),txt(self.meta['title'],32,width=8 if SHORT else 14).move_to([0,6.25 if SHORT else 3.15,0]))
        self.add(Line([-3.9,5.65,0],[3.9,5.65,0],color=GRAY,stroke_opacity=.25) if SHORT else Line([-7,2.65,0],[7,2.65,0],color=GRAY,stroke_opacity=.25))
        if self.INDEX not in [6,9]:
            for x,s,c in zip([-3,-1,1,3] if SHORT else [-5.8,-2.9,0,2.9],['a₁ / q₁','a₂ 원래','p 정사영','v₂ / q₂'],[BLUE,GREEN,ORANGE,PURPLE]):self.add(txt(s,18,c,width=2.5).move_to([x,5.15 if SHORT else -3.03,0]))
        if self.INDEX not in [6,9]:self.graph()
        self.shot();self.to(self.meta['end'])
    def pt(self,v):return self.origin+self.unit*np.array([v[0],v[1],0.])
    def arr(self,v,col,origin=None,width=6):
        origin=np.zeros(2) if origin is None else np.array(origin)
        return Arrow(self.pt(origin),self.pt(origin+v),buff=0,color=col,stroke_width=width,max_tip_length_to_length_ratio=.14)
    def graph(self):
        grid=VGroup()
        for i in range(-1,4):
            x=i*.75;grid.add(Line(self.pt([x,-1.3]),self.pt([x,1.6]),color=GRAY,stroke_width=1,stroke_opacity=.09))
        for i in range(-2,3):
            y=i*.6;grid.add(Line(self.pt([-.9,y]),self.pt([2.65,y]),color=GRAY,stroke_width=1,stroke_opacity=.09))
        grid.add(Line(self.pt([-.9,0]),self.pt([2.65,0]),color=GRAY,stroke_width=1.5,stroke_opacity=.45),Line(self.pt([0,-1.3]),self.pt([0,1.6]),color=GRAY,stroke_width=1.5,stroke_opacity=.45))
        self.add(grid,txt('0',16,GRAY).move_to(self.pt([-.13,-.15])))
    def originals(self,first=1,second=1,names=True):
        self.a1=self.arr(A1,BLUE).set_opacity(first).set_z_index(1);self.a2=self.arr(A2,GREEN).set_opacity(second).set_z_index(3);self.add(self.a1,self.a2)
        if names:
            self.a1name=txt('a₁ = (1, 1)',21,BLUE,width=2.5).move_to(self.pt([1.3,1.23])).set_opacity(first)
            self.a2name=txt('a₂ = (2, 0)',21,GREEN,width=2.5).move_to(self.pt([2.05,.2])).set_opacity(second);self.add(self.a1name,self.a2name)
    def basis(self,second=False):
        self.q1=self.arr(Q1,BLUE,width=7).set_z_index(11);self.add(self.q1,txt('q₁',24,BLUE,width=1).move_to(self.pt([.12,.86])))
        if second:
            self.q2=self.arr(Q2,PURPLE,width=7).set_z_index(11);self.add(self.q2,txt('q₂',24,PURPLE,width=1).move_to(self.pt([.12,-.8])))
    def proj(self,label=True):
        self.p=self.arr(PROJ,ORANGE).set_z_index(5);self.add(self.p)
        if label:self.add(txt('p = (1, 1)',22,ORANGE,width=2.5).move_to(self.pt([1.35,1.15])))
        return self.p
    def residual_arrow(self,anchored=False,unit=False):return self.arr(Q2 if unit else V2,PURPLE,origin=PROJ if anchored else None).set_z_index(6)
    def residual_label(self):return txt('v₂ = (1, −1)',22,PURPLE,width=2.2).move_to(self.pt([1.8,-1.05]))
    def square(self,at_tip=False):
        base=PROJ if at_tip else np.zeros(2)
        return RightAngle(Line(self.pt(base),self.pt(base+Q1)),Line(self.pt(base),self.pt(base+Q2)),length=.26,color=GRAY,stroke_width=2)
    def info(self,s,note='',color=INK,size=32):
        width=8 if SHORT else 14 if self.dual else 6.7
        line=txt(s,size,color,width) if isinstance(s,str) else colored(s,size,width)
        line.move_to(self.panel);group=VGroup(line)
        if note:group.add(txt(note,23,GRAY,width).next_to(line,DOWN,buff=.4))
        if hasattr(self,'inf'):self.remove(self.inf)
        self.inf=group;self.add(group);return group
    def to(self,t):
        left=t-self.start-self.time
        if left<-.04:raise RuntimeError(f'Scene {self.INDEX+1}: {self.time} > {t-self.start}')
        if left>.001:self.wait(left)
    def matrix_area(self,title,values,name,factor=None,headers=None):
        center=[0,-3.05,0] if SHORT else [3.6,.15,0]
        self.add(txt(title,27,INK,7.8 if SHORT else 6.7).move_to([0,-1.35,0] if SHORT else [3.6,1.95,0]))
        widget=MatrixWidget(name,values,[BLUE,PURPLE] if name=='Q' else [BLUE,GREEN],center,factor,headers,width=7.4 if SHORT else 6.6)
        self.add(widget);return widget
    def matrix_note(self,s,color=GRAY):
        if hasattr(self,'mnote'):self.remove(self.mnote)
        self.mnote=txt(s,23,color,width=7.8 if SHORT else 6.7).move_to([0,-4.65,0] if SHORT else [3.6,-1.65,0]);self.add(self.mnote)
    def highlight_col(self,widget,j,col):
        rect=SurroundingRectangle(widget.columns[j],color=col,buff=.15,stroke_width=2)
        self.play(Create(rect),run_time=.4);self.play(FadeOut(rect),run_time=.4)
    def comparison(self):
        centers=[np.array([-2.15,1.3,0]),np.array([2.15,1.3,0])] if SHORT else [np.array([-4.15,.35,0]),np.array([3.45,.35,0])]
        scale=.9 if SHORT else 1.35;self.planes=[]
        for j,c in enumerate(centers):
            def point(v):return c+scale*np.array([v[0],v[1],0.])
            plane=Rectangle(width=3.1*scale,height=2.6*scale,fill_color='#32618F',fill_opacity=0,stroke_opacity=0).move_to(point([.45,.2])).set_z_index(-2);self.add(plane);self.planes.append(plane)
            self.add(Line(point([-1.1,0]),point([2.2,0]),color=GRAY,stroke_opacity=.35),Line(point([0,-1.1]),point([0,1.5]),color=GRAY,stroke_opacity=.35))
            vectors=[A1,A2] if j==0 else [Q1,Q2];cols=[BLUE,GREEN] if j==0 else [BLUE,PURPLE]
            for k,(v,col) in enumerate(zip(vectors,cols)):
                self.add(Arrow(point([0,0]),point(v),buff=0,color=col,stroke_width=6,max_tip_length_to_length_ratio=.16))
                offset=np.array([.1,.18]) if k==0 else np.array([.2,-.2])
                self.add(txt(['a₁','a₂'][k] if j==0 else ['q₁','q₂'][k],21,col,width=1).move_to(point(v+offset)))
            self.add(txt('원래 두 벡터' if j==0 else '직교정규기저',26,INK,width=3.9 if SHORT else 6).move_to([c[0],4.1 if SHORT else 2.35,0]))
    def shot(self):
        i=self.INDEX
        if i==0:
            self.originals();self.info('비스듬한 두 방향 → 직교축 ?', '내적과 정사영으로 직접 만든다');self.to(4)
            self.add(Arc(radius=.6*self.unit,start_angle=0,angle=PI/4,arc_center=self.origin,color=GRAY,stroke_width=2),txt('45°',20,GRAY,width=1).move_to(self.pt([.76,.25])))
            self.to(8);self.info('a₁ = (1, 1)', '가로 1 · 세로 1',BLUE);self.to(10)
            self.info('a₂ = (2, 0)', '가로 2 · 세로 0',GREEN);self.to(14)
            self.info('두 벡터는 직교하지 않는다', 'a₁ · a₂ = 2 ≠ 0',ORANGE)
        elif i==1:
            self.originals(.25,.15);copy=self.arr(A1,BLUE).set_z_index(10);self.add(copy)
            self.info('첫 번째 벡터부터', 'a₁ = (1, 1)',BLUE);self.to(18)
            self.info('‖a₁‖ = √(1² + 1²)', '= √2',BLUE);self.to(21)
            self.info('q₁ = (1, 1)/√2', '방향은 그대로 · 길이 √2 → 1',BLUE)
            self.play(Transform(copy,self.arr(Q1,BLUE,width=7).set_z_index(10)),run_time=3.5);self.to(26)
            self.add(txt('q₁',24,BLUE,width=1).move_to(self.pt([.12,.86])))
            self.info('첫 번째 기저벡터 q₁', '‖q₁‖ = 1',BLUE)
        elif i==2:
            self.originals(.12,1,False);self.basis();self.info('두 번째 벡터 a₂', '첫 방향과 겹치는 성분',GREEN);self.to(32)
            self.add(Line(self.pt([-.5,-.5]),self.pt([1.4,1.4]),color=BLUE,stroke_opacity=.3))
            drop=DashedLine(self.pt(A2),self.pt(PROJ),color=GRAY,stroke_width=2);measure=Line(self.pt([0,0]),self.pt(PROJ),color=ORANGE,stroke_width=5)
            self.play(Create(drop),Create(measure),run_time=1.3);self.add(self.square(True));self.to(36)
            self.info('겹치는 성분만 제거하면?', '먼저 내적으로 읽어 본다',ORANGE);self.to(38)
            self.info('a₂ · q₁ = (2, 0) · (1, 1)/√2', '같은 방향에서 측정',ORANGE);self.to(41)
            self.info('a₂ · q₁ = √2', '정사영의 계수',ORANGE);self.to(43)
            self.info('(a₂ · q₁)q₁ = (1, 1)', '측정값 × 기준 단위벡터',ORANGE)
            copy=self.arr(Q1,ORANGE).set_z_index(5);self.add(copy);self.play(Transform(copy,self.arr(PROJ,ORANGE).set_z_index(5)),run_time=2)
            self.add(txt('p = (1, 1)',22,ORANGE,width=2.5).move_to(self.pt([1.35,1.15])))
        elif i==3:
            self.originals(.1,1,False);self.basis();self.proj()
            self.info('v₂ = a₂ − (a₂ · q₁)q₁', '(2, 0) − (1, 1)',PURPLE);self.to(52)
            self.info('가로: 2 − 1 = 1', '첫 번째 성분',PURPLE);self.to(54)
            self.info('세로: 0 − 1 = −1', '두 번째 성분',PURPLE);self.to(57)
            r=self.residual_arrow(True);self.play(GrowArrow(r),run_time=1)
            self.play(Transform(r,self.residual_arrow(False)),run_time=1)
            self.add(self.residual_label());self.info('v₂ = (1, −1)', '두 끝점의 차이 → 원점으로 평행이동',PURPLE)
        elif i==4:
            self.originals(.08,.08,False);self.basis();self.add(self.residual_arrow(),self.residual_label())
            self.info('첫 방향의 성분이 제거됐을까?', '내적으로 확인한다',PURPLE);self.to(62)
            check=self.arr(A1,BLUE,width=4).set_z_index(3);self.add(check)
            self.info('(1, 1) · (1, −1)', '방향이 같으므로 정규화 전 a₁로 검사',BLUE);self.to(64)
            self.info('1 × 1 + 1 × (−1)', '서로 반대인 두 기여',PURPLE)
            terms=VGroup(txt('+1',34,ORANGE).move_to(self.panel+[-1.25,-1.25,0]),txt('−1',34,PURPLE).move_to(self.panel+[1.25,-1.25,0]));self.add(terms)
            self.play(terms[0].animate.move_to(self.panel+[-.5,-1.25,0]),terms[1].animate.move_to(self.panel+[.5,-1.25,0]),run_time=1.4);self.to(67)
            self.remove(terms);self.info('0', '1 − 1 = 0',PURPLE,size=58);self.to(68)
            self.add(self.square());self.info('정확히 직교한다 · 90°', '기존 방향으로 다시 측정하면 0',PURPLE)
        elif i==5:
            self.originals(.08,.08,False);self.basis();r=self.residual_arrow();self.add(r)
            self.info('‖v₂‖ = √(1² + (−1)²)', '= √2',PURPLE);self.to(74)
            self.info('q₂ = (1, −1)/√2', '방향은 그대로 · 길이 √2 → 1',PURPLE)
            self.play(Transform(r,self.residual_arrow(unit=True)),run_time=3);self.to(78)
            self.add(txt('q₂',24,PURPLE,width=1).move_to(self.pt([.12,-.8])));self.info('두 번째 기저벡터 q₂', '‖q₂‖ = 1',PURPLE);self.to(81)
            self.add(self.square());self.info('‖q₁‖ = ‖q₂‖ = 1', 'q₁ · q₂ = 0',BLUE)
        elif i==6:
            self.comparison();self.info('그람–슈미트 직교화', 'Gram–Schmidt Orthogonalization',BLUE);self.to(93)
            self.info('정사영 제거 → 정규화', '기존 방향과 겹치는 부분을 빼고 길이 1로');self.to(95)
            self.play(*(m.animate.set_fill(opacity=.16) for m in self.planes),run_time=1)
            self.info('span(a₁, a₂) = span(q₁, q₂)', '두 집합 모두 같은 2차원 평면 R²',BLUE)
            nuance=txt('첫 방향은 유지 · 둘째 방향을 직교화',21,GRAY,width=7.8 if SHORT else 13).move_to([0,-1.35 if SHORT else -1.2,0]);self.add(nuance);self.to(101)
            self.remove(nuance);self.info('a₂ = (a₂ · q₁)q₁ + v₂', '제거한 성분도 첫 번째 방향 안에 있었다',ORANGE)
        elif i==7:
            self.originals(.1,.1,False);self.basis(True)
            self.info('새 기저로 원래 벡터를 표현하려면?', '두 기저를 열로 묶는다');self.to(110);self.remove(self.inf)
            w=self.matrix_area('Q의 두 열 = 새 단위 방향',[['1','1'],['1','−1']],'Q',factor='1/√2',headers=['q₁','q₂'])
            self.play(TransformFromCopy(self.q1,w.columns[0]),run_time=1)
            self.play(TransformFromCopy(self.q2,w.columns[1]),run_time=1)
            self.matrix_note('QᵀQ = I  /  각 열은 길이 1, 서로 직교',BLUE)
        elif i==8:
            self.originals(.12,.12,False);self.basis(True)
            title='R의 각 열 = 원래 벡터의 계수';w=self.matrix_area(title,[['?','?'],['?','?']],'R',headers=['a₁','a₂']);self.matrix_note('첫 열은 a₁, 둘째 열은 a₂에 대응');self.to(119)
            self.remove(w);w=MatrixWidget('R',[['√2','?'],['0','?']],[BLUE,GREEN],[0,-3.05,0] if SHORT else [3.6,.15,0],headers=['a₁','a₂'],width=7.4 if SHORT else 6.6);self.add(w)
            first=self.arr(Q1,BLUE).set_z_index(6);self.add(first);self.play(Transform(first,self.arr(A1,BLUE).set_z_index(6)),run_time=1)
            self.matrix_note('a₁ = √2 q₁ + 0 q₂',BLUE);self.highlight_col(w,0,BLUE);self.to(122)
            self.remove(w);w=MatrixWidget('R',[['√2','√2'],['0','√2']],[BLUE,GREEN],[0,-3.05,0] if SHORT else [3.6,.15,0],headers=['a₁','a₂'],width=7.4 if SHORT else 6.6);self.add(w)
            p=self.arr(PROJ,ORANGE).set_z_index(5);r=self.residual_arrow();self.add(p,r)
            self.play(Transform(r,self.residual_arrow(True)),run_time=1.3)
            self.matrix_note('a₂ = √2 q₁ + √2 q₂',GREEN);self.highlight_col(w,1,GREEN)
            self.play(Flash(self.pt(A2),color=GREEN,flash_radius=.2),run_time=.6)
        elif i==9:
            centers=[[0,3.,0],[-2.05,-.6,0],[2.1,-.6,0]] if SHORT else [[-5.25,.5,0],[-.3,.5,0],[5.,.5,0]]
            a=MatrixWidget('',[['1','2'],['1','0']],[BLUE,GREEN],centers[0],width=3.4,size=32)
            q=MatrixWidget('',[['1','1'],['1','−1']],[BLUE,PURPLE],centers[1],factor='1/√2',width=3.75 if SHORT else 4.2,size=32)
            r=MatrixWidget('',[['√2','√2'],['0','√2']],[BLUE,GREEN],centers[2],width=3.3 if SHORT else 3.7,size=32)
            self.add(a,q,r)
            for widget,name in zip([a,q,r],['A','Q','R']):
                self.add(txt(name,30,INK,width=1.2).move_to([widget.get_center()[0],widget.get_top()[1]+.45,0]))
            if SHORT:self.add(txt('A = Q R',42,ORANGE,width=8).move_to([0,-3.4,0]),txt('×',31,GRAY).move_to([.1,-.6,0]))
            else:self.add(txt('=',33,INK).move_to([-3.05,.5,0]),txt('×',33,INK).move_to([2.15,.5,0]))
            self.highlight_col(r,0,BLUE);self.highlight_col(a,0,BLUE);self.to(131)
            name=txt('QR 분해 · QR Decomposition',29,ORANGE,width=8 if SHORT else 14).move_to([0,1.35 if SHORT else -1.2,0]);self.add(name);self.to(133)
            self.add(txt('Q: 서로 직교하는\n단위 방향',23,BLUE,width=3.7 if SHORT else 6).move_to([-2.1,-4.55,0] if SHORT else [-1.8,-2.2,0]),txt('R: 원래 열의\n구성 계수',23,ORANGE,width=3.7 if SHORT else 6).move_to([2.1,-4.55,0] if SHORT else [4.8,-2.2,0]))
            self.highlight_col(q,0,BLUE);self.highlight_col(q,1,PURPLE);self.highlight_col(r,1,GREEN)
        else:
            self.originals(.1,.35,False);self.basis();self.info('측정   a₂ · q₁ = √2', '내적으로 첫 방향의 성분을 읽는다',ORANGE);self.to(142)
            self.proj(False);self.info('추출   (a₂ · q₁)q₁ = (1, 1)', '정사영으로 겹치는 성분을 꺼낸다',ORANGE);self.to(144)
            r=self.residual_arrow(True);self.add(r);self.play(Transform(r,self.residual_arrow()),run_time=1)
            self.info('제거   v₂ = a₂ − (a₂ · q₁)q₁', '첫 방향과 직교하는 벡터',PURPLE);self.to(146)
            self.play(Transform(r,self.residual_arrow(unit=True)),run_time=1)
            self.info('정규화   q₂ = v₂ / ‖v₂‖', '길이 1인 두 번째 방향',PURPLE);self.to(148)
            self.add(self.square());self.info('A = QR', '방향 성분의 제거 → 행렬 분해',ORANGE,size=58)
