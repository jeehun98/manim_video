"""Orthographic 3D vector model; camera angles never alter the model vectors."""
import os,json,textwrap
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('BATTLE_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16
config.frame_height=16 if SHORT else 9
config.background_color='#0B1120'
BG='#0B1120';INK='#EEF4FF';MUTED='#91A4BF';BLUE='#55AEFF';GREEN='#59DFAC';ORANGE='#FFB15A';PURPLE='#BB97FF'
A1=np.array([1.,1,0]);A2=np.array([0.,2,0]);A3=np.array([1.,1,2]);Q1=A1/np.sqrt(2);Q2=np.array([-1.,1,0])/np.sqrt(2);Q3=OUT

def label(s,size=27,color=INK,width=7.5):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=.8)
    if m.width>width:m.scale_to_fit_width(width)
    return m

class QRBase(Scene):
    INDEX=0
    def construct(self):
        self.m=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX]
        self.start=self.m['start'];self.end=self.m['end'];self.clock=self.start
        self.az=ValueTracker(-55*DEGREES);self.el=ValueTracker(28*DEGREES)
        self.center=np.array([-.6,.35,0]) if SHORT else np.array([-3.9,-.4,0])
        self.scale3=1.65 if SHORT else 1.25
        self.stage=VGroup()
        self.add(label('QR / 01     새로운 방향을 찾아서',20,MUTED).move_to([0,7.35 if SHORT else 3.95,0]))
        self.add(label(self.m['title'],34,INK,8 if SHORT else 14).move_to([0,6.35 if SHORT else 3.1,0]))
        self.add(Line([-3.9,5.7,0],[3.9,5.7,0],color=MUTED,stroke_opacity=.22) if SHORT else Line([-7,2.55,0],[7,2.55,0],color=MUTED,stroke_opacity=.22))
        self.add(always_redraw(self.axes))
        cues=json.loads((P/'timing.json').read_text(encoding='utf-8'))
        cap=next(c for c in cues if c['start']<=self.start<c['end'])['caption']
        cap='\n'.join(textwrap.wrap(cap,width=29 if SHORT else 56,break_long_words=True))
        self.add(label(cap,25 if SHORT else 24,INK,8 if SHORT else 14).move_to([0,-6.4 if SHORT else -3.5,0]))
        self.add(label('도입: 평면 위 종속 사례' if self.INDEX<7 else '본 계산: 선형독립인 세 벡터',18,MUTED).move_to([0,-7.4 if SHORT else -4.1,0]))
        self.shot()
        self.to(self.end)

    def proj(self,v):
        x,y,z=np.asarray(v);a=self.az.get_value();e=self.el.get_value()
        return self.center+self.scale3*np.array([-np.sin(a)*x+np.cos(a)*y,-np.sin(e)*(np.cos(a)*x+np.sin(a)*y)+np.cos(e)*z,0])
    def axes(self):
        g=VGroup()
        for v,t in [(RIGHT,'x'),(UP,'y'),(OUT,'z')]:
            if 7<=self.INDEX<=12 and t=='z':continue
            g.add(Line(self.proj(-2.2*v),self.proj(2.6*v),color=MUTED,stroke_width=1,stroke_opacity=.4))
            g.add(label(t,18,MUTED).move_to(self.proj(2.8*v)))
        return g
    def plane(self):
        g=VGroup(Polygon(*[self.proj(v) for v in [(-1.2,-1.2,0),(2,-1.2,0),(2,2,0),(-1.2,2,0)]],fill_color=PURPLE,fill_opacity=.09,stroke_width=1,stroke_color=PURPLE,stroke_opacity=.35))
        for t in [-1,0,1,2]:
            g.add(Line(self.proj((t,-1.2,0)),self.proj((t,2,0)),color=PURPLE,stroke_opacity=.18,stroke_width=1),Line(self.proj((-1.2,t,0)),self.proj((2,t,0)),color=PURPLE,stroke_opacity=.18,stroke_width=1))
        return g
    def vec(self,v,color,name='',origin=ORIGIN,dashed=False,opacity=1):
        a=self.proj(origin);b=self.proj(np.array(origin)+v)
        line=Arrow(a,b,buff=0,color=color,stroke_width=5,max_tip_length_to_length_ratio=.18)
        if dashed:line=DashedVMobject(line,num_dashes=12)
        g=VGroup(line)
        if name:
            offset=np.array([.16,.3,0])
            if name=='q₁':offset=np.array([.05,-.38,0])
            if name.startswith('p'):offset=np.array([.38,-.12,0])
            if name=='u₂':b=(a+b)/2;offset=np.array([-.4,.1,0])
            g.add(label(name,25,color,2).move_to(b+offset))
        return g.set_opacity(opacity)
    def livevec(self,tracker,color,name):return always_redraw(lambda:self.vec(tracker.get_value(),color,name))
    def put(self,*ms):
        for m in ms:self.add(m);self.stage.add(m)
    def animate(self,*anims,d=1):self.play(*anims,run_time=d)
    def to(self,t):
        remaining=t-self.start-self.time
        if remaining<-.04:raise RuntimeError(f'Overflow cut {self.INDEX+1}: {self.time} > {t-self.start}')
        if remaining>.001:self.wait(remaining)
    def equation(self,s,note='',color=INK):
        pos=[0,-3.5,0] if SHORT else [3.65,.6,0]
        eq=label(s,32,color,8 if SHORT else 6.4).move_to(pos)
        g=VGroup(eq)
        if note:g.add(label(note,23,MUTED,7.8 if SHORT else 6.2).next_to(eq,DOWN,buff=.42))
        self.put(g);return g
    def rightmark(self,o,u,v):
        u=np.array(u)/np.linalg.norm(u)*.23;v=np.array(v)/np.linalg.norm(v)*.23;o=np.array(o)
        return VMobject(color=INK,stroke_width=2).set_points_as_corners([self.proj(o+u),self.proj(o+u+v),self.proj(o+v)])
    def bases(self,third=False):
        self.put(self.vec(Q1,BLUE,'q₁'),self.vec(Q2,GREEN,'q₂'))
        if third:self.put(self.vec(Q3,ORANGE,'q₃'))
    def shot(self):
        i=self.INDEX
        if i==0:
            for v,c,n in [(A1,BLUE,'a₁'),(A2,GREEN,'a₂'),(A1+A2,ORANGE,'a₃')]:
                self.animate(GrowArrow(self.vec(v,c,n)[0]),d=.45)
            self.equation('벡터 3개 ≠ 차원 3','새 방향이 추가되어야 차원이 늘어납니다')
        elif i==1:
            v=VectorizedPoint(A1);g=always_redraw(lambda:self.vec(v.get_location(),BLUE,'t a₁'));self.put(g)
            for s in [.5,2,-1,1]:self.animate(v.animate.move_to(A1*s),d=.65)
            self.animate(Create(Line(self.proj(-2*A1),self.proj(2*A1),color=BLUE,stroke_width=2)),d=.6)
            self.equation('span(a₁) = 직선','원점을 지나는 모든 배수')
        elif i in [2,3]:
            self.put(self.vec(A1,BLUE,'a₁'),self.vec(A2,GREEN,'a₂'))
            self.put(always_redraw(self.plane))
            if i==2:
                for s,t in [(1,1),(-.6,1),(.5,-.7)]:
                    p=self.vec(s*A1+t*A2,INK,'');self.animate(FadeIn(p),d=.45);self.animate(FadeOut(p),d=.35)
            else:self.animate(self.az.animate.set_value(-38*DEGREES),d=2.5)
            self.equation('span(a₁, a₂) = 평면','평행하지 않은 두 벡터의 선형결합')
        elif i in [4,5]:
            self.put(always_redraw(self.plane),self.vec(A1,BLUE,'a₁'),self.vec(A2,GREEN,'a₂'))
            if i==4:
                t=ValueTracker(1);g=always_redraw(lambda:self.vec(A1+A2+OUT*t.get_value(),ORANGE,'a₃'));self.put(g);self.animate(t.animate.set_value(0),d=2)
            else:
                self.put(self.vec(A1+A2,ORANGE,'a₃'),self.vec(A2,GREEN,origin=A1,dashed=True))
                self.equation('a₃ = a₁ + a₂','벡터는 3개 · 공간의 차원은 2',ORANGE)
        elif i==6:
            self.put(always_redraw(self.plane),self.vec(A1,BLUE,'a₁'),self.vec(A2,GREEN,'a₂'))
            v=ValueTracker(0);self.put(always_redraw(lambda:self.vec(np.array([1,1,2*v.get_value()]),ORANGE,'a₃')))
            e=self.equation('평면 안 → 차원 2','평면 밖 성분이 생기면 차원 3',ORANGE)
            self.animate(v.animate.set_value(1),Transform(e[0],label('평면 밖 → 차원 3',32,ORANGE).move_to(e[0])),d=2.5)
        elif i in [7,8]:
            self.el.set_value(65*DEGREES)
            self.put(self.vec(A2,GREEN,'a₂',opacity=.45))
            if i==7:
                self.put(self.vec(A1,BLUE,'a₁'));self.equation('기존 방향 + 새로운 방향','본 계산은 선형독립인 벡터로 진행')
            else:
                t=ValueTracker(1);self.put(always_redraw(lambda:self.vec(A1*t.get_value(),BLUE,'q₁' if t.get_value()<.72 else 'a₁')))
                self.animate(t.animate.set_value(1/np.sqrt(2)),d=1.7)
                self.equation('q₁ = a₁ / ‖a₁‖','방향 유지 · 길이는 1',BLUE)
        elif i in [9,10,11,12]:
            self.el.set_value(70*DEGREES);self.az.set_value(-55*DEGREES)
            self.put(self.vec(Q1,BLUE,'q₁'),self.vec(A2,GREEN,'a₂',opacity=.35 if i>=11 else 1))
            if i==9:self.equation('a₂의 성분을 나누면?','q₁에 나란한 부분과 수직인 부분')
            elif i==10:
                self.animate(Create(self.vec(A1,PURPLE,'p₂',dashed=True)),Create(self.vec(np.array([-1.,1,0]),GREEN,'u₂',origin=A1)),d=1.4)
                self.put(self.rightmark(A1,Q1,[-1,1,0]))
                self.equation('a₂ = (q₁ᵀa₂)q₁ + u₂','투영 성분          수직 잔여 성분')
            elif i==11:
                proj=self.vec(A1,PURPLE,'p₂',dashed=True);self.put(proj)
                t=ValueTracker(1);self.put(always_redraw(lambda:self.vec(np.array([-1.,1,0]),GREEN,'u₂',origin=A1*t.get_value())))
                self.animate(FadeOut(proj),t.animate.set_value(0),d=2)
                self.put(self.rightmark(ORIGIN,Q1,Q2));self.equation('u₂ = a₂ − (q₁ᵀa₂)q₁','평행이동으로 방향과 길이는 바뀌지 않습니다',GREEN)
            else:
                t=ValueTracker(np.sqrt(2));self.put(always_redraw(lambda:self.vec(Q2*t.get_value(),GREEN,'q₂' if t.get_value()<1.01 else 'u₂')))
                self.animate(t.animate.set_value(1),d=2)
                self.put(self.rightmark(ORIGIN,Q1,Q2));self.equation('q₂ = u₂ / ‖u₂‖','‖u₂‖ ≠ 0일 때 정규화',GREEN)
        elif i in [13,14,15,16,17]:
            self.put(always_redraw(self.plane));self.bases()
            if i==13:
                self.el.set_value(55*DEGREES)
                self.put(always_redraw(lambda:self.vec(A3,ORANGE,'a₃')))
                self.animate(self.el.animate.set_value(28*DEGREES),d=2)
                self.equation('a₃ = (1, 1, 2)','평면 위 성분과 평면 밖 성분을 함께 가집니다',ORANGE)
            elif i==14:
                self.put(self.vec(A3,ORANGE,'a₃'),self.vec(A1,PURPLE,'p₃',dashed=True))
                self.animate(Create(DashedLine(self.proj(A1),self.proj(A3),color=ORANGE)),d=.7)
                self.equation('p₃ = (q₁ᵀa₃)q₁ + (q₂ᵀa₃)q₂','이 예시에서는 q₂ 방향 계수가 0입니다',PURPLE)
            elif i==15:
                self.put(self.vec(A3,ORANGE,'a₃',opacity=.25))
                t=ValueTracker(1);self.put(always_redraw(lambda:self.vec(2*OUT,ORANGE,'u₃',origin=A1*t.get_value())))
                proj=self.vec(A1,PURPLE,'p₃',dashed=True);self.put(proj)
                self.animate(FadeOut(proj),t.animate.set_value(0),d=1.4)
                self.equation('u₃ = a₃ − p₃','기존 평면에 수직인 잔여 성분',ORANGE)
            elif i==16:
                t=ValueTracker(2);self.put(always_redraw(lambda:self.vec(OUT*t.get_value(),ORANGE,'q₃' if t.get_value()<1.01 else 'u₃')))
                self.animate(t.animate.set_value(1),d=1)
                self.equation('q₃ = u₃ / ‖u₃‖','‖u₃‖ ≠ 0일 때 정규화',ORANGE)
            else:
                self.put(self.vec(Q3,ORANGE,'q₃'))
                for a,b in [(Q1,Q2),(Q1,Q3),(Q2,Q3)]:self.animate(Create(self.rightmark(ORIGIN,a,b)),d=.45)
                self.equation('QᵀQ = I','서로 직교 · 각 벡터의 길이는 1')
        elif i==18:
            self.bases(True)
            eq=self.equation('a₁ = √2 q₁','기준 방향의 배수들을 더해 원래 벡터 복원')
            a=self.vec(A1,BLUE,'a₁');self.animate(FadeIn(a),d=.45);self.animate(FadeOut(a),d=.35)
            self.animate(Create(self.vec(A1,BLUE,'')),Create(self.vec(np.sqrt(2)*Q2,GREEN,'',origin=A1)),d=.6)
            self.animate(Transform(eq[0],label('a₂ = √2 q₁ + √2 q₂',32).move_to(eq[0])),d=.35)
            self.animate(Create(self.vec(A2,GREEN,'a₂',dashed=True)),d=.45)
            self.animate(Create(self.vec(2*Q3,ORANGE,'',origin=A1)),d=.6)
            self.animate(Transform(eq[0],label('a₃ = √2 q₁ + 2q₃',32).move_to(eq[0])),Create(self.vec(A3,ORANGE,'a₃',dashed=True)),d=.55)
        elif i in [19,20]:
            self.bases(True)
            if i==19:
                self.equation('Q = [ q₁  q₂  q₃ ]','직교하는 단위벡터를 열로 모은 행렬')
            else:
                self.equation('R =\n⎡ √2   √2   √2 ⎤\n⎢  0    √2    0  ⎥\n⎣  0     0     2  ⎦','각 열은 a₁, a₂, a₃의 조합 계수')
                self.animate(Create(self.vec(A3,ORANGE,'a₃',dashed=True)),d=.7)
        elif i==21:
            self.bases(True);self.equation('A = QR','원래 벡터 = 직교 기저 × 조합 계수',ORANGE)
        elif i==22:
            self.bases(True)
            for v,c,n in [(A1,BLUE,'a₁'),(A2,GREEN,'a₂'),(A3,ORANGE,'a₃')]:self.put(self.vec(v,c,n,dashed=True,opacity=.6))
            self.equation('기준 방향 + 원래 벡터의 조합법','원래 벡터 사이의 관계를 드러내는 분해')
        else:
            self.bases(True)
            self.animate(Create(Line(self.proj(-1.6*Q1),self.proj(2.5*Q1),color=BLUE)),d=.8)
            pl=self.plane();self.animate(FadeIn(pl),d=.8)
            self.animate(Create(self.vec(2*Q3,ORANGE,'새 방향')),d=.8)
            self.equation('기존 공간의 성분 + 새로운 수직 성분','QR 분해 — 공간에 새롭게 추가되는 방향',ORANGE)
