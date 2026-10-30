"""Attention: distinct scores, row-normalized weights, and separate Value vectors."""
import json,os
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('DOT_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16;config.frame_height=16 if SHORT else 9;config.background_color='#0B1220'
INK='#EDF4FF';GRAY='#8B9CB6';BLUE='#55ACFF';GREEN='#55DFA3';PURPLE='#BB97FF';ORANGE='#FFB45F';CYAN='#53D7D0';OUT='#8FD8FF'
Q=np.array([2.,1.]);KEYS=np.array([[1.,1.],[0.,2.]]);VALUES=np.array([[4.,0.],[0.,2.]]);SCORES=KEYS@Q;SCALED=SCORES/np.sqrt(2)
EXP=np.exp(SCALED-SCALED.max());ALPHA=EXP/EXP.sum();OUTPUT=ALPHA@VALUES
def txt(s,size=29,color=INK,width=7.8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if m.width>width:m.scale_to_fit_width(width)
    return m
class AttentionBase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start']
        self.main=np.array([0,1.7,0]) if SHORT else np.array([-4.25,.2,0]);self.panel=np.array([0,-2.55,0]) if SHORT else np.array([3.6,.35,0]);self.content=VGroup()
        self.origin=np.array([-2.15,.55,0]) if SHORT else np.array([-6.,-1.05,0]);self.scale=1.05 if SHORT else .95
        self.a=ValueTracker(1);self.b=ValueTracker(1);self.shift_y=ValueTracker(0);self.klen=ValueTracker(1)
        self.add(txt('DOT PRO   /   LEVEL 09',19,GRAY).move_to([0,7.2 if SHORT else 3.95,0]),txt(self.meta['title'],30,width=8 if SHORT else 14).move_to([0,6.25 if SHORT else 3.15,0]))
        y=5.65 if SHORT else 2.65;self.add(Line([-3.9 if SHORT else -7,y,0],[3.9 if SHORT else 7,y,0],color=GRAY,stroke_opacity=.25))
        for x,s,c in zip([-3,-1,1,3] if SHORT else [-5.8,-2.9,0,2.9],['q Query','k Key','α 가중치','v Value'],[BLUE,GREEN,CYAN,PURPLE]):self.add(txt(s,17,c,width=2.4).move_to([x,5.15 if SHORT else -3.03,0]))
        self.header=list(self.mobjects)
        self.shot();self.to(self.meta['end'])
    def to(self,t):
        self.update_mobjects(0);left=t-self.start-self.time
        if left<-.04:raise RuntimeError((self.INDEX,self.time,t-self.start))
        if left>.001:self.wait(left)
    def loc(self,x,y):return self.main+[x,y*(1 if SHORT else .75),0]
    def card(self,title,desc,where,color=BLUE,width=2.5):
        h=1 if SHORT else .85;g=VGroup(RoundedRectangle(width=width,height=h,corner_radius=.13,stroke_color=color,stroke_width=1.5,fill_color=color,fill_opacity=.08).move_to(where),txt(title,25,color,width=width-.3).move_to(where+[0,.15,0]))
        if desc:g.add(txt(desc,17,GRAY,width=width-.3).move_to(where+[0,-.22,0]))
        self.add(g);return g
    def info(self,s,note='',color=INK,size=30):
        self.remove(self.content);self.content=VGroup(txt(s,size,color,width=7.9 if SHORT else 6.7).move_to(self.panel))
        if note:self.content.add(txt(note,22,GRAY,width=7.8 if SHORT else 6.6).next_to(self.content[0],DOWN,buff=.4))
        self.add(self.content)
    def below(self,s,color=INK,offset=-1.65,size=23):
        m=txt(s,size,color,width=7.8 if SHORT else 6.6).move_to(self.panel+[0,offset,0]);self.add(m);return m
    def diagram(self,numeric=False,values=False,weights=False):
        q=self.loc(0,1.8);ks=[self.loc(-2.1,0),self.loc(2.1,0)];vs=[self.loc(-2.1,-1.5),self.loc(2.1,-1.5)]
        lines=VGroup()
        for i,k in enumerate(ks):
            color=GREEN if i==0 else PURPLE;line=Line(q+[0,-.5,0],k+[0,.5,0],color=color,stroke_width=3 if not weights else 2+8*ALPHA[i]);self.add(line);lines.add(line)
            if weights:self.add(txt(f'{100*ALPHA[i]:.1f}%',21,CYAN,width=1.6).move_to((q+k)/2+[-.45 if i==0 else .45,.05,0]))
        self.card('q = (2, 1)' if numeric else '현재 정보','Query · 비교 기준',q,BLUE)
        self.card('k₁ = (1, 1)' if numeric else '정보 1','Key · 점수 비교',ks[0],GREEN)
        self.card('k₂ = (0, 2)' if numeric else '정보 2','Key · 점수 비교',ks[1],PURPLE)
        if values:
            for i,v in enumerate(vs):
                self.add(DashedLine(ks[i]+[0,-.5,0],v+[0,.5,0],color=GRAY,stroke_width=1.5,dash_length=.06))
                self.card(('v₁ = (4, 0)' if i==0 else 'v₂ = (0, 2)') if numeric else ('Value 1' if i==0 else 'Value 2'),'실제로 결합할 정보',v,GREEN if i==0 else PURPLE)
        return lines
    def pos(self,v):return self.origin+self.scale*np.r_[v,0]
    def arrow(self,a,b,color,width=5):
        p,q=self.pos(a),self.pos(b)
        if np.linalg.norm(p-q)<1e-6:return Dot(q,radius=.015,color=color)
        return Arrow(p,q,buff=0,color=color,stroke_width=width,max_tip_length_to_length_ratio=.12)
    def axes(self,values=False):
        if hasattr(self,'axis'):self.remove(self.axis)
        xmax=4.8 if values else 3.3;ymax=3.2
        self.axis=VGroup(Line(self.pos([-.35,0]),self.pos([xmax,0]),color=GRAY,stroke_width=1.5,stroke_opacity=.6),Line(self.pos([0,-.35]),self.pos([0,ymax]),color=GRAY,stroke_width=1.5,stroke_opacity=.6),txt('0',15,GRAY).move_to(self.pos([-.16,-.2])))
        for x in range(1,5 if values else 4):
            p=self.pos([x,0]);self.axis.add(Line(p+[0,-.05,0],p+[0,.05,0],color=GRAY),txt(str(x),14,GRAY,width=.4).move_to(p+[0,-.2,0]))
        for y in range(1,4):
            p=self.pos([0,y]);self.axis.add(Line(p+[-.05,0,0],p+[.05,0,0],color=GRAY),txt(str(y),14,GRAY,width=.4).move_to(p+[-.18,0,0]))
        self.add(self.axis)
    def qk(self,highlight=None):
        self.axes();g=VGroup(self.arrow([0,0],Q,BLUE))
        for i,k in enumerate(KEYS):g.add(self.arrow([0,0],k,GREEN if i==0 else PURPLE).set_opacity(1 if highlight is None or highlight==i else .2))
        g.add(txt('q = (2, 1)',21,BLUE,width=2.5).move_to(self.pos(Q)+[.65,.15,0]),txt('k₁ = (1, 1)',21,GREEN,width=2.5).move_to(self.pos(KEYS[0])+[-.35,.4,0]).set_opacity(1 if highlight in [None,0] else .2),txt('k₂ = (0, 2)',21,PURPLE,width=2.5).move_to(self.pos(KEYS[1])+[.6,.35,0]).set_opacity(1 if highlight in [None,1] else .2))
        self.add(g);return g
    def score_bars(self,values,normalized=False):
        g=VGroup();base=self.main+[0,-.1,0];w=5.5
        for i,value in enumerate(values):
            y=base[1]+.7-i*1.6;left=base[0]-w/2;length=w*value if normalized else w*value/3
            color=CYAN if normalized else ORANGE
            g.add(Rectangle(width=length,height=.42,stroke_width=0,fill_color=color,fill_opacity=1).move_to([left+length/2,y,0]),txt(f'Key {i+1}',22,GREEN if i==0 else PURPLE,width=2).move_to([left+.5,y+.55,0]),txt(f'{value*100:.1f}%' if normalized else f'{value:.3f}' if abs(value-round(value))>1e-6 else f'{value:.0f}',28,color,width=2).move_to([left+length+.55,y,0]))
        self.add(g);return g
    def combined_bar(self,where=None):
        base=self.main+[0,-1.7,0] if where is None else where;w=6.5 if SHORT else 6.;left=base[0]-w/2;g=VGroup()
        for i,(start,v,c) in enumerate([(0,ALPHA[0],GREEN),(ALPHA[0],ALPHA[1],PURPLE)]):
            length=w*v;g.add(Rectangle(width=length,height=.5,stroke_width=0,fill_color=c,fill_opacity=1).move_to([left+w*start+length/2,base[1],0]),txt(f'{100*v:.1f}%',22,INK,width=2).move_to([left+w*start+length/2,base[1],0]))
        g.add(txt('α₁ + α₂ = 1  ·  전체 100%',21,CYAN,width=6).move_to(base+[0,-.6,0]));self.add(g);return g
    def flow(self,active=None,offset=-1.6):
        g=VGroup()
        for j,(s,n,c) in enumerate([('Q · K','점수',ORANGE),('Softmax','가중치',CYAN),('Weighted V','결합',OUT)]):
            center=self.panel+[(j-1)*(2.7 if SHORT else 2.15),offset,0];color=c if active is None or j==active else GRAY
            g.add(txt(s,24,color,width=2.25 if SHORT else 1.9).move_to(center),txt(n,19,color,width=1.9).move_to(center+[0,-.48,0]))
            if j<2:g.add(txt('→',22,GRAY,width=.4).move_to(center+[1.35 if SHORT else 1.075,0,0]))
        self.add(g);return g
    def value_geometry(self,weighted=True,result=False):
        self.axes(True);a=ALPHA[0] if weighted else 1;b=ALPHA[1] if weighted else 1;p=a*VALUES[0];v=b*VALUES[1]
        g=VGroup(self.arrow([0,0],p,GREEN),self.arrow(p if result else [0,0],p+v if result else v,PURPLE))
        g.add(txt('α₁v₁' if weighted else 'v₁ = (4, 0)',21,GREEN,width=2.5).move_to(self.pos(p/2)+[0,-.48,0]))
        if result:
            g.add(self.arrow([0,0],OUTPUT,OUT),txt('o ≈ (2.68, 0.66)',21,OUT,width=3.5).move_to(self.pos(OUTPUT)+[.55,.35,0]))
        else:g.add(txt('α₂v₂' if weighted else 'v₂ = (0, 2)',21,PURPLE,width=2.5).move_to(self.pos(v)+[.8,.18,0]))
        self.add(g);return g
    def shot(self):
        i=self.INDEX
        if i==0:
            lines=self.diagram();self.info('여러 정보 중 무엇을 참고할까?',color=BLUE);self.to(4);self.info('현재 정보 · 비교 대상 → 점수 ?','내적으로 정보 사이의 점수를 계산',ORANGE);self.to(8)
            self.play(lines[0].animate.set_stroke(width=7),lines[1].animate.set_stroke(width=2),run_time=1.3);self.info('Attention · 어텐션','정보별 가중치를 계산하고 결합');self.below('연결 굵기는 개념적 표현',GRAY,-1.55,20)
        elif i==1:
            self.card('고양이','앞서 등장한 정보',self.loc(-2.1,.5),GREEN);self.card('소파','앞서 등장한 정보',self.loc(2.1,.5),PURPLE);self.card('그것','현재 처리하는 단어',self.loc(0,-1.6),BLUE)
            self.add(txt('고양이가 소파에 앉았고,\n그것이 잠들었다.',27,INK,width=7).move_to(self.loc(0,2.25)));self.info('문장 속 정보를 서로 다르게 참고한다',color=BLUE);self.to(18)
            for x,w,c in [(-2.1,7,GREEN),(2.1,2,PURPLE)]:self.play(Create(Line(self.loc(0,-1.6)+[0,.5,0],self.loc(x,.5)+[0,-.5,0],stroke_width=w,color=c)),run_time=.7)
            self.info('‘그것’ → 고양이 · 소파','서로 다른 비율로 정보를 참고할 수 있다');self.below('개념도 · 실제 토큰 경계나 측정 가중치가 아님',GRAY,-1.6,20)
        elif i==2:
            self.diagram(values=True);self.info('Q · K · V','Query · Key · Value');self.to(29);self.info('Query · 현재 찾는 정보를 나타내는 기준',color=BLUE);self.to(33);self.info('Key: 비교 대상  /  Value: 결합할 정보','같은 정보에서 만들어져도 역할은 다르다');self.below('학습된 변환으로 만들어지는 벡터',GRAY,-1.6,20)
        elif i==3:
            self.diagram();self.info('어떤 정보를 더 참고할까?', 'Query와 Key 사이의 점수를 계산');self.to(42)
            for m in list(self.mobjects):
                if m not in self.header and m is not self.content:self.remove(m)
            self.info('q · k',color=ORANGE,size=45);self.to(44);self.axes();self.info('2차원 가상 예제','문장 예시의 측정값과는 별개의 계산',GRAY);self.to(48);self.qk();self.info('q = (2, 1)','k₁ = (1, 1)  ·  k₂ = (0, 2)',BLUE)
        elif i==4:
            g=self.qk(0);self.info('q · k₁ = 2×1 + 1×1 = 3',color=ORANGE);self.to(59);self.remove(g);g=self.qk(1);self.info('q · k₂ = 2×0 + 1×2 = 2',color=ORANGE);self.to(64);self.remove(g);self.info('내적 점수 = (3, 2)','아직 가중치나 퍼센트가 아니다',ORANGE);self.to(67)
            # Remove plot objects, retaining only the header and current formula.
            for m in list(self.mobjects):
                if m not in self.header and m is not self.content:self.remove(m)
            self.score_bars(SCORES);self.info('첫 번째 정보의 원점수가 더 높다','점수 3 : 2  ≠  가중치 67 : 33',ORANGE)
        elif i==5:
            bars=self.score_bars(SCORES);self.info('원점수 (3, 2)','이 숫자를 그대로 가중치로 쓰지 않는다',ORANGE);self.to(73);self.remove(bars);self.info('dₖ = 2  →  √dₖ = √2','각 점수를 키 차원의 제곱근으로 나눈다',ORANGE);self.score_bars(SCALED);self.to(77);self.info('sᵢ = (q · kᵢ) / √dₖ','(3/√2, 2/√2) ≈ (2.121, 1.414)',ORANGE)
        elif i==6:
            self.card('2.121  ·  1.414','스케일링된 점수',self.loc(0,1.7),ORANGE,width=4.8);self.card('Softmax','αᵢ = exp(sᵢ) / Σⱼ exp(sⱼ)',self.loc(0,.05),CYAN,width=6.0);self.info('스케일링한 점수 → Softmax',color=CYAN);self.to(82);self.combined_bar();self.info('α ≈ (0.6698, 0.3302)','각 가중치는 양수 · 합은 1',CYAN);self.to(85);self.info('정보 1: 약 67%  ·  정보 2: 약 33%','원점수의 비율 3:2를 그대로 쓴 것이 아니다',CYAN)
        elif i==7:
            self.info('이 가중치를 어디에 쓸까?', 'α₁ ≈ 0.67  ·  α₂ ≈ 0.33',CYAN);bar=self.combined_bar(where=self.main+[0,.8,0]);self.to(95);self.remove(bar);self.info('비교한 Key와 별개인 Value','가중치를 적용할 실제 정보 벡터',PURPLE);self.to(97);self.axes(True)
            self.a.set_value(1);self.b.set_value(1)
            first=always_redraw(lambda:self.arrow([0,0],self.a.get_value()*VALUES[0],GREEN));second=always_redraw(lambda:self.arrow([0,0],self.b.get_value()*VALUES[1],PURPLE));self.add(first,second)
            labels=VGroup(txt('v₁ = (4, 0)',21,GREEN,width=2.6).move_to(self.pos([3,0])+[0,-.48,0]),txt('v₂ = (0, 2)',21,PURPLE,width=2.6).move_to(self.pos([0,2])+[.8,.3,0]));self.add(labels);self.info('v₁ = (4, 0)   v₂ = (0, 2)',color=PURPLE);self.to(101)
            self.play(self.a.animate.set_value(ALPHA[0]),self.b.animate.set_value(ALPHA[1]),run_time=2);self.to(104);self.remove(labels);self.info('α₁v₁ ≈ (2.68, 0)','α₂v₂ ≈ (0, 0.66)',CYAN);self.to(109)
            self.remove(second);self.shift_y.set_value(0)
            moved=always_redraw(lambda:self.arrow(self.shift_y.get_value()*ALPHA[0]*VALUES[0],self.shift_y.get_value()*ALPHA[0]*VALUES[0]+ALPHA[1]*VALUES[1],PURPLE));self.add(moved);self.play(self.shift_y.animate.set_value(1),run_time=2);self.to(112)
            output=self.arrow([0,0],OUTPUT,OUT).set_z_index(5);self.play(GrowArrow(output),run_time=1);self.info('o = α₁v₁ + α₂v₂ ≈ (2.68, 0.66)','두 Key가 아닌 두 Value의 가중합',OUT)
        elif i==8:
            self.value_geometry(True,True);self.info('점수 (3, 2) → 가중치 (0.67, 0.33)','o = α₁v₁ + α₂v₂',OUT);self.flow();self.to(120);self.info('Attention(Q,K,V) = softmax(QKᵀ/√dₖ)V','행마다: 내적 → 스케일링·Softmax → Value 결합',OUT,size=27)
        elif i==9:
            self.axes();x=np.array([2.,1.]);u=np.array([1.,1.])/np.sqrt(2);p=(x@u)*u
            projection=VGroup(self.arrow([0,0],x,BLUE),self.arrow([0,0],p,GREEN),DashedLine(self.pos(p),self.pos(x),color=PURPLE,stroke_width=2),Line(self.pos(-.3*u),self.pos(3.2*u),color=GREEN,stroke_width=1,stroke_opacity=.5));self.add(projection);self.info('정사영과 Attention은 역할이 다르다');self.to(126);self.info('p = (x · u)u   ·   ‖u‖ = 1','측정한 같은 방향으로 성분을 추출',GREEN);self.to(131)
            # Replace the geometric projection with the separate-value computation.
            for m in list(self.mobjects):
                if m not in self.header and m is not self.content:self.remove(m)
            self.value_geometry(True,True);self.info('q · kᵢ → αᵢ → o = Σᵢ αᵢvᵢ','학습된 Q,K로 비교하고 별도의 V를 결합',OUT);self.to(137);self.info('Attention 점수 ≠ 정사영 성분','출력에 정사영의 직교 조건이 일반적으로 보장되지 않음',ORANGE);self.to(142)
            for m in list(self.mobjects):
                if m not in self.header and m is not self.content:self.remove(m)
            self.axes();self.add(self.arrow([0,0],Q,BLUE));self.add(always_redraw(lambda:self.arrow([0,0],self.klen.get_value()*KEYS[0],GREEN)));self.info('q · k = ‖q‖ ‖k‖ cosθ','각도는 그대로 · Key 길이만 2배',GREEN)
            label=always_redraw(lambda:txt(f'점수 = {3*self.klen.get_value():.1f}',26,ORANGE,width=4).move_to(self.main+[.6,1.55,0]));self.add(label);self.play(self.klen.animate.set_value(2),run_time=2.8)
        elif i==10:
            self.diagram(numeric=True,values=True,weights=True)
            output=self.loc(0,-2.9)
            for x in [-2.1,2.1]:self.add(Line(self.loc(x,-1.5)+[0,-.5,0],output+[0,.5,0],color=OUT,stroke_width=2))
            self.card('o ≈ (2.68, 0.66)','Value 가중합',output,OUT,width=3.3)
            self.info('내적 점수 → 가중치 → Value 결합','o ≈ (2.68, 0.66)',OUT);self.flow()
