from pathlib import Path
import json, textwrap
from manim import *
R=Path(__file__).resolve().parent
config.background_color='#0B1020'
config.frame_width=128/9
config.frame_height=8
FONT='Malgun Gothic'
WHITE_INK='#F3F5FA'; MUTED='#8C9AB5'; TEAL='#20D6B0'; BLUE='#8199C9'; ORANGE='#FFAC55'; PURPLE='#A78BFA'
def txt(s,size=25,color=WHITE_INK):return Text(s,font=FONT,font_size=size,color=color)
def math(s,size=60,color=WHITE_INK):return MathTex(s,font_size=size,color=color)
def title(s):return txt(s,22,MUTED).move_to([0,3.35,0])
def ops():
    return VGroup(math('3',100).move_to([-2.7,.5,0]),math('5',100).move_to([2.7,.5,0]),VGroup(*[math(s,48,TEAL) for s in ['+','-',r'\times',r'\div']]).arrange(RIGHT,buff=.35).move_to([0,.5,0]))
def zbox():
    box=RoundedRectangle(width=8.5,height=3.25,corner_radius=.25,color=BLUE,fill_color=BLUE,fill_opacity=.06).move_to([-1.4,.15,0])
    label=VGroup(math(r'\mathbb Z',40,BLUE),txt('정수',23,BLUE)).arrange(RIGHT,buff=.2).move_to([-4.65,1.3,0])
    dots=math(r'\ldots,-2,-1,0,1,2,\ldots',33,MUTED).move_to([-1.4,-1,0])
    return VGroup(box,label,dots)
def rows(count=3):
    formulas=['3+5=8',r'3\times5=15','3-5=-2']
    result=VGroup(*[VGroup(math(s,40),SurroundingRectangle(math(s,40),color=TEAL,buff=.13,corner_radius=.08)) for s in formulas[:count]]).arrange(RIGHT,buff=.3)
    if result.width>7.5:result.scale_to_fit_width(7.5)
    return result.move_to([-1.4,.35,0])
def qstate():
    q=RoundedRectangle(width=12.5,height=4.65,corner_radius=.3,color=PURPLE,fill_color=PURPLE,fill_opacity=.035).move_to([0,.15,0])
    ql=VGroup(math(r'\mathbb Q',38,PURPLE),txt('유리수',23,PURPLE)).arrange(RIGHT,buff=.2).move_to([4.9,1.95,0])
    frac=math(r'\frac35',66,ORANGE).move_to([4.45,.2,0])
    return VGroup(q,ql,zbox(),rows().scale(.85).shift(LEFT*.15),frac,math(r'\mathbb Z\subset\mathbb Q',36,PURPLE).move_to([0,-2.55,0]))
def marked(angle=0,size=2.2,center=ORIGIN):
    s=Square(side_length=size,color=BLUE,fill_color=BLUE,fill_opacity=.1,stroke_width=4)
    d=Dot(s.get_corner(UL),radius=.075,color=TEAL)
    g=VGroup(s,d);g.rotate(angle,about_point=ORIGIN);g.shift(np.array(center));return g
# The dot tracks orientation; it does not restrict the square's symmetry group.
def rotation_state():
    return VGroup(marked(center=[-3,.3,0]),math(r'360^\circ\equiv0^\circ',58,TEAL).move_to([2.1,.7,0]),txt('한 바퀴 돌아 원래 상태로',25,MUTED).move_to([2.1,-.45,0]))
def rotation_bank():
    bank=VGroup()
    for k,x in enumerate([-4.5,-1.5,1.5,4.5]):
        bank.add(VGroup(marked(k*PI/2,1.3,[x,1.15,0]),math(str(k*90)+r'^\circ',30,BLUE).move_to([x,-.05,0]),math(str(k),58,TEAL).move_to([x,-1.1,0])))
    return bank

def modstate(k=1):
    # 1+2=3, then 3+2=1 (mod 4); same transform, fixed centre.
    a,result=(1,3) if k==0 else (3,1)
    pic=marked(result*PI/2,2.0,[-3,.45,0])
    deg=math(f'{a*90}'+r'^\circ+180^\circ\equiv'+str(result*90)+r'^\circ\ (\mathrm{mod}\ 360^\circ)',37,BLUE).move_to([2,.9,0])
    eq=math(f'{a}+2\\equiv{result}\\pmod4',55,TEAL).move_to([2,-.4,0])
    return VGroup(pic,deg,eq)
def correspondence():
    g=VGroup()
    for x,c in [(-3.2,TEAL),(3.2,BLUE)]:
        g.add(RoundedRectangle(width=5.6,height=4.15,corner_radius=.2,stroke_color=c,stroke_opacity=.5,fill_color=c,fill_opacity=.025).move_to([x,.2,0]))
    g.add(txt('4로 나눈 나머지의 덧셈',26,TEAL).move_to([-3.2,1.8,0]),txt('정사각형의 회전 합성',26,BLUE).move_to([3.2,1.8,0]))
    for k,y in enumerate([1,.25,-.5,-1.25]):
        g.add(math(str(k),33,TEAL).move_to([-3.2,y,0]),DoubleArrow([-2.5,y,0],[2.3,y,0],buff=0,stroke_width=1.5,color=PURPLE,tip_length=.1),marked(k*PI/2,.42,[2.9,y,0]),math(str(k*90)+r'^\circ',27,BLUE).move_to([3.8,y,0]))
    return g

def abstract_state():
    return VGroup(math(r'(S,\star)',104,PURPLE).move_to([0,.8,0]),txt('집합과 연산의 구조',30).move_to([0,-.65,0]),txt('추상대수학  /  Abstract Algebra',32,PURPLE).move_to([0,-1.8,0]))
def structure_cards():
    result=VGroup()
    for x,ko,en,sub,c in zip([-4.2,0,4.2],['군','환','체'],['Group','Ring','Field'],['한 연산의 구조','덧셈과 곱셈','0이 아닌 원소의 곱셈 역원'],[TEAL,BLUE,PURPLE]):
        bg=RoundedRectangle(width=3.75,height=3.5,corner_radius=.22,color=c,fill_color=c,fill_opacity=.055).move_to([x,-.1,0])
        subtext=txt(sub,19,MUTED)
        if subtext.width>3.3:subtext.scale_to_fit_width(3.3)
        result.add(VGroup(bg,txt(ko,58,c).move_to([x,.85,0]),txt(en,30,c).move_to([x,-.15,0]),subtext.move_to([x,-1.15,0])))
    return result

class IntroScene(Scene):
    index=1
    def construct(self):
        self.manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
        record=self.manifest[self.index-1]
        self.start=record['start'];self.total_duration=record['duration_seconds']
        self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
        self.caption=VGroup();self.caption_index=-1
        self.caption_audit=[]
        self.bound_violations=[]
        self.last_bound_check=-1
        self.caption_driver=VMobject().add_updater(lambda m,dt:self.update_caption())
        self.add(self.caption_driver)
        getattr(self,['operations','integers','division','square','compose','encode','modulo','correspond','abstract','names'][self.index-1])()
        self.to(self.total_duration)
        self.audit_content(record)
        self.caption_driver.clear_updaters()
        (R/record['directory']/'layout_audit.json').write_text(json.dumps(self.caption_audit,ensure_ascii=False,indent=2),encoding='utf-8')
    def update_caption(self):
        self.check_bounds()
        t=self.start+self.time
        i=next((k for k,x in enumerate(self.lines) if x['start']<=t<x['end']),len(self.lines)-1)
        if i==self.caption_index:return
        self.caption_index=i;self.remove(self.caption)
        s=self.lines[i]['text']
        wrapped=textwrap.fill(s,width=49,break_long_words=False,break_on_hyphens=False)
        caption=txt(wrapped,25)
        if caption.width>12.5:caption.scale_to_fit_width(12.5)
        caption.move_to([0,-3.35,0])
        bg=RoundedRectangle(width=13,height=max(.7,caption.height+.25),corner_radius=.1,stroke_width=0,fill_color='#10151F',fill_opacity=.97).move_to(caption)
        self.caption=VGroup(bg,caption).set_z_index(100)
        self.add(self.caption)
        assert caption.get_bottom()[1]>-3.95 and caption.get_top()[1]<-2.75
        self.caption_audit.append(dict(line=i+1,left=float(caption.get_left()[0]),right=float(caption.get_right()[0]),top=float(caption.get_top()[1]),bottom=float(caption.get_bottom()[1])))
    def to(self,t):
        frames=round(t*config.frame_rate)-round(self.time*config.frame_rate)
        if frames<0:raise ValueError(f'Scene {self.index} overrun {self.time}>{t}')
        if frames:self.wait(frames/config.frame_rate)
    def play_for(self,t,*anims):self.play(*anims,run_time=t)
    def check_bounds(self):
        if self.time-self.last_bound_check<.2:return
        self.last_bound_check=self.time
        for m in self.mobjects:
            if m is self.caption or m is self.caption_driver or not m.has_points() and not m.submobjects:continue
            l,r,b,t=float(m.get_left()[0]),float(m.get_right()[0]),float(m.get_bottom()[1]),float(m.get_top()[1])
            if l< -7.12 or r>7.12 or b< -2.85 or t>3.85:self.bound_violations.append(dict(time=self.time,left=l,right=r,bottom=b,top=t))
    def audit_content(self,record):
        assert not self.bound_violations, self.bound_violations[:5]
        audit=[]
        for m in self.mobjects:
            if m is self.caption or m is self.caption_driver or not m.has_points() and not m.submobjects:continue
            l,r,b,t=float(m.get_left()[0]),float(m.get_right()[0]),float(m.get_bottom()[1]),float(m.get_top()[1])
            audit.append(dict(left=l,right=r,bottom=b,top=t))
            assert l>=-7.11 and r<=7.11 and b>=-2.85 and t<=3.85,(record['id'],l,r,b,t)
        (R/record['directory']/'content_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    def operations(self):
        h=title('숫자에서 구조로');g=ops();self.add(h)
        self.play_for(1.1,FadeIn(g[0],shift=RIGHT*.4),FadeIn(g[1],shift=LEFT*.4))
        sign=math('+',65,TEAL).move_to([0,.5,0]);self.play_for(.4,FadeIn(sign))
        for s in ['-',r'\times',r'\div']:
            self.play_for(.45,Transform(sign,math(s,65,TEAL).move_to([0,.5,0])))
        self.play_for(.65,ReplacementTransform(sign,g[2]));self.to(5)
    def integers(self):
        h=title('숫자에서 구조로');g=ops();self.add(h,g)
        z=zbox();rr=rows()
        self.play_for(.65,FadeOut(g),FadeIn(z))
        for i,(delay,end) in enumerate([(0,2),(0,4),(0,7.1)]):
            self.play_for(.55,FadeIn(rr[i],shift=DOWN*.3))
            self.to(end)
        self.to(8)
    def division(self):
        h=title('숫자에서 구조로');z=zbox();rr=rows();self.add(h,z,rr)
        eq=math(r'3\div5=\frac35',63,ORANGE).move_to([3.8,2.3,0])
        self.play_for(.6,FadeIn(eq))
        self.to(1.5)
        q=qstate();self.play_for(1,FadeOut(eq),Transform(z,q[2]),Transform(rr,q[3]),FadeIn(q[4],shift=RIGHT*.4))
        self.to(3)
        self.play_for(1.1,Create(q[0]),FadeIn(q[1]),FadeIn(q[5]))
        note=txt('집합을 선택하면, 연산의 성질이 달라집니다',27).move_to([0,2.9,0])
        self.play_for(.8,FadeIn(note));self.to(7.9);self.play_for(.6,FadeOut(note));self.to(9)
    def square(self):
        h=title('숫자에서 구조로');q=qstate();self.add(h,q)
        question=txt('연산의 규칙은 숫자에만 있을까요?',35,PURPLE).move_to([0,2.45,0])
        self.play_for(.8,FadeIn(question),q.animate.scale(.7).set_opacity(.25))
        self.to(3.4)
        sq=marked(center=[0,.3,0])
        self.play_for(1,FadeOut(q),FadeIn(sq,scale=.85))
        self.to(5.8);self.play_for(.7,FadeOut(question));self.to(7)
    def compose(self):
        h=title('숫자에서 구조로');sq=marked(center=[0,.3,0]);self.add(h,sq)
        self.play_for(.4,sq.animate.shift(LEFT*3))
        eq=math(r'90^\circ',65,TEAL).move_to([2.1,.7,0]);self.add(eq)
        self.play_for(2.6,Rotate(sq,PI/2,about_point=sq[0].get_center()))
        eq2=math(r'90^\circ+180^\circ',55,TEAL).move_to([2.1,.7,0])
        self.play_for(.4,Transform(eq,eq2))
        self.play_for(3.1,Rotate(sq,PI,about_point=sq[0].get_center()))
        self.play_for(.5,Transform(eq,math(r'90^\circ+180^\circ=270^\circ',42,TEAL).move_to([2.1,.7,0])))
        self.to(8)
        last=rotation_state()
        self.play_for(1.7,Rotate(sq,PI/2,about_point=sq[0].get_center()),Transform(eq,last[1]),FadeIn(last[2]))
        self.to(11)
    def encode(self):
        h=title('숫자에서 구조로');previous=rotation_state();self.add(h,previous)
        bank=rotation_bank()
        self.play_for(.7,FadeOut(previous[1:]),ReplacementTransform(previous[0],bank[0][0]))
        self.add(bank[0][1],bank[0][2])
        for k,end in [(1,2.8),(2,4.5),(3,6.5)]:
            self.play_for(.6,FadeIn(bank[k][0]),FadeIn(bank[k][1]),FadeIn(bank[k][2],shift=UP*.2))
            self.to(end)
        self.to(7)
    def modulo(self):
        h=title('숫자에서 구조로');bank=rotation_bank();self.add(h,bank)
        sq=marked(PI/2,2,[-3,.45,0]);eq=math(r'1+2\equiv3\pmod4',55,TEAL).move_to([2,-.4,0]);deg=modstate(0)[1]
        self.play_for(.5,FadeOut(bank),FadeIn(sq),FadeIn(deg))
        self.play_for(1.25,Rotate(sq,PI,about_point=sq[0].get_center()),Write(eq))
        self.to(2.8)
        target=modstate(1)
        self.play_for(.45,Transform(deg,target[1]),Transform(eq,math(r'3+2\equiv\,?\pmod4',55,TEAL).move_to([2,-.4,0])))
        self.play_for(1.35,Rotate(sq,PI,about_point=sq[0].get_center()),Transform(eq,target[2]))
        self.to(6)
    def correspond(self):
        h=title('숫자에서 구조로');old=modstate(1);self.add(h,old)
        table=correspondence()
        self.play_for(1,FadeOut(old),FadeIn(table[:4]))
        for k in range(4):
            objects=table[4+4*k:8+4*k]
            self.play_for(.5,FadeIn(objects))
        self.to(4)
        self.play_for(.65,Indicate(table[4+4],color=PURPLE),Indicate(table[4+4+2],color=PURPLE))
        self.to(6)
        note=txt('대상은 달라도, 연산 결과가 대응합니다',28,PURPLE).move_to([0,-2.4,0])
        self.play_for(.7,FadeIn(note))
        self.to(9.6);self.play_for(.6,FadeOut(note));self.to(11)
    def abstract(self):
        h=title('숫자에서 구조로');g=correspondence();self.add(h,g)
        mid=abstract_state()
        self.play_for(2,g.animate.scale(.8).set_opacity(.16))
        self.play_for(2.2,FadeOut(g),FadeIn(mid[0],scale=.85),FadeIn(mid[1]))
        annotations=VGroup(txt('S : 원소들의 집합',23,MUTED).move_to([-2.5,2.45,0]),txt('★ : 집합 위의 연산',23,MUTED).move_to([2.5,2.45,0]))
        self.play_for(.7,FadeIn(annotations));self.to(6)
        self.play_for(1.3,FadeIn(mid[2],shift=UP*.12));self.to(8.7)
        self.play_for(.6,FadeOut(annotations));self.to(10)
    def names(self):
        h=title('숫자에서 구조로');g=abstract_state();self.add(h,g)
        self.play_for(.65,FadeOut(g[1:]),g[0].animate.scale(.4).move_to([0,2.6,0]))
        cs=structure_cards()
        for k,end in [(0,2),(1,4),(2,6)]:
            self.play_for(.65,FadeIn(cs[k],shift=UP*.15));self.to(end)
        self.play_for(.6,cs[1:].animate.set_opacity(.28),cs[0][0].animate.set_stroke(width=4))
        self.to(7)
