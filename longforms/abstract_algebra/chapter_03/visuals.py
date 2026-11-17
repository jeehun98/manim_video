from pathlib import Path
import importlib.util,json,textwrap
from manim import *
R=Path(__file__).resolve().parent
_spec=importlib.util.spec_from_file_location('algebra_ch01_shared',R.parent/'chapter_01'/'visuals.py')
shared=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(shared)
txt,math,title=shared.txt,shared.math,shared.title
WHITE_INK,MUTED,TEAL,BLUE,ORANGE,PURPLE=shared.WHITE_INK,shared.MUTED,shared.TEAL,shared.BLUE,shared.ORANGE,shared.PURPLE

def header(ring=False):return title('환 · Ring' if ring else '두 연산과 규칙')
def fit(m,w):
    if m.width>w:m.scale_to_fit_width(w)
    return m

def tuple_z():
    m=MathTex(r'(\mathbb Z,','+',',',r'\times',')',font_size=93,color=WHITE_INK)
    m[1].set_color(TEAL);m[3].set_color(BLUE);return m.move_to([0,.45,0])
def int_area():
    box=RoundedRectangle(width=11.7,height=4.15,corner_radius=.24,color=BLUE,fill_color=BLUE,fill_opacity=.035).move_to([0,.2,0])
    return VGroup(box,math(r'\mathbb Z',43,BLUE).move_to([-5,1.7,0]))
def closure_end():
    box=int_area()
    add=VGroup(txt('덧셈',27,TEAL),math('3+5=8',59,TEAL),math(r'8\in\mathbb Z',34,TEAL)).arrange(DOWN,buff=.35).move_to([-2.7,.3,0])
    mul=VGroup(txt('곱셈',27,BLUE),math(r'3\times5=15',59,BLUE),math(r'15\in\mathbb Z',34,BLUE)).arrange(DOWN,buff=.35).move_to([2.7,.3,0])
    lab=txt('닫힘 · Closure',27,TEAL).move_to([0,-2.25,0])
    return VGroup(box,add,mul,lab)
def dist_formula():
    eq=MathTex('a','(','b','+','c',')','=','a','b','+','a','c',font_size=66)
    for k in [0,7,10]:eq[k].set_color(PURPLE)
    for k in [2,8]:eq[k].set_color(TEAL)
    for k in [4,11]:eq[k].set_color(BLUE)
    return eq

def dist_end():
    left=VGroup(RoundedRectangle(width=2.2,height=1.3,corner_radius=.18,color=TEAL),math('+',57,TEAL)).move_to([-2.8,.5,0])
    right=VGroup(RoundedRectangle(width=2.2,height=1.3,corner_radius=.18,color=BLUE),math(r'\times',57,BLUE)).move_to([2.8,.5,0])
    link=DoubleArrow([-1.6,.5,0],[1.6,.5,0],buff=0,color=PURPLE,stroke_width=3,tip_length=.16)
    return VGroup(dist_formula().scale(.75).move_to([0,2.45,0]),left,right,link,txt('분배법칙 · Distributive Law',30,PURPLE).move_to([0,-1.05,0]),math(r'(a+b)c=ac+bc',36,MUTED).move_to([0,-2.2,0]))
def area_parts():
    # A single geometric unit is .85 Manim units in both x and y.
    s=.85;left=-3.5*s;y=.15
    full=Rectangle(width=7*s,height=2*s,color=PURPLE,fill_color=PURPLE,fill_opacity=.09).move_to([0,y,0])
    a=Rectangle(width=3*s,height=2*s,color=TEAL,fill_color=TEAL,fill_opacity=.18).move_to([left+1.5*s,y,0])
    b=Rectangle(width=4*s,height=2*s,color=BLUE,fill_color=BLUE,fill_opacity=.18).move_to([left+5*s,y,0])
    height=VGroup(Brace(full,LEFT,color=MUTED),math('2',36,BLUE).move_to([-3.7,y,0]))
    widths=VGroup(math('3',35,TEAL).move_to([a.get_center()[0],1.5,0]),math('4',35,BLUE).move_to([b.get_center()[0],1.5,0]))
    return VGroup(full,a,b,height,widths,math('6',55,TEAL).move_to(a),math('8',55,BLUE).move_to(b))
def area_end():
    g=area_parts()
    return VGroup(dist_formula().scale(.75).move_to([0,2.45,0]),g,math(r'2(3+4)=2\times3+2\times4=6+8=14',46,PURPLE).move_to([0,-1.8,0]))
def rule_cards():
    out=VGroup()
    for x,c,head,sub,formula in [(-4.2,TEAL,'덧셈','아벨 군 · Abelian Group',r'a+b=b+a'),(0,BLUE,'곱셈','결합법칙',r'(ab)c=a(bc)'),(4.2,PURPLE,'두 연산','좌우 분배법칙',r'a(b+c)=ab+ac')]:
        bg=RoundedRectangle(width=3.85,height=2.7,corner_radius=.18,color=c,fill_color=c,fill_opacity=.035).move_to([x,-.45,0])
        lab=txt(head,27,c).move_to([x,.42,0]);subt=fit(txt(sub,21,c),3.5).move_to([x,-.15,0]);eq=fit(math(formula,31),3.45).move_to([x,-.85,0])
        card=VGroup(bg,lab,subt,eq)
        if x==-4.2:card.add(txt('군의 조건 + 교환법칙',19,MUTED).move_to([x,-1.4,0]))
        if x==4.2:card.add(fit(math(r'(a+b)c=ac+bc',29),3.45).move_to([x,-1.4,0]))
        out.add(card)
    return out

def ring_end():
    return VGroup(math(r'(\mathbb Z,+,\times)',59).move_to([0,2.65,0]),txt('환 · Ring',39,PURPLE).move_to([0,1.65,0]),rule_cards(),txt('곱셈의 교환법칙은 일반적인 환의 필수 조건이 아닙니다',22,MUTED).move_to([0,-2.35,0]))
def poly_domains():
    g=VGroup()
    for x,c in [(-3.2,BLUE),(3.2,PURPLE)]:g.add(RoundedRectangle(width=5.8,height=3.8,corner_radius=.2,color=c,fill_color=c,fill_opacity=.025).move_to([x,.4,0]))
    g.add(math(r'\mathbb Z',61,BLUE).move_to([-3.2,1.4,0]),math(r'2,\ 3,\ 5,\ \ldots',43).move_to([-3.2,.3,0]),txt('정수',26,BLUE).move_to([-3.2,-.9,0]),math(r'\mathbb R[x]',56,PURPLE).move_to([3.2,1.4,0]),math(r'x^2+1,\quad2x+3',40).move_to([3.2,.3,0]),txt('실수 계수 다항식',25,PURPLE).move_to([3.2,-.9,0]),txt('다항식환 · Polynomial Ring',26,PURPLE).move_to([0,-2.25,0]))
    return g

def poly_cards():
    out=VGroup()
    for x,c,s in [(-3.1,TEAL,r'f(x)=x^2+1'),(3.1,BLUE,r'g(x)=2x+3')]:
        out.add(VGroup(RoundedRectangle(width=5.5,height=1.25,corner_radius=.16,color=c,fill_color=c,fill_opacity=.035),math(s,42,c)).move_to([x,1.85,0]))
    return out

def calc_end():
    return VGroup(poly_cards(),math(r'f(x)+g(x)=x^2+2x+4',44,TEAL).move_to([0,.35,0]),math(r'f(x)g(x)=2x^3+3x^2+2x+3',43,BLUE).move_to([0,-.75,0]),txt('결합법칙 · 분배법칙',25,PURPLE).move_to([0,-2.2,0]))

def compare_end():
    g=VGroup()
    for x,c,formula,caption in [(-3.2,BLUE,r'(\mathbb Z,+,\times)','정수의 환'),(3.2,PURPLE,r'(\mathbb R[x],+,\times)','다항식의 환')]:
        card=VGroup(RoundedRectangle(width=5.8,height=4.05,corner_radius=.2,color=c,fill_color=c,fill_opacity=.025).move_to([x,.35,0]),txt('Ring',29,PURPLE).move_to([x,1.85,0]),fit(math(formula,48,c),5.2).move_to([x,.95,0]),txt(caption,24,c).move_to([x,.15,0]))
        for j,(s,col) in enumerate([('덧셈 : 아벨 군',TEAL),('곱셈 : 결합법칙',BLUE),('두 연산 : 분배법칙',PURPLE)]):card.add(txt(s,22,col).move_to([x,-.45-j*.46,0]))
        g.add(card)
    g.add(txt('같은 종류의 연산 규칙을 만족하는, 서로 다른 환',26,PURPLE).move_to([0,-2.25,0]));return g

def div_end():
    q=RoundedRectangle(width=12.5,height=4.6,corner_radius=.3,color=PURPLE,fill_color=PURPLE,fill_opacity=.025).move_to([0,.15,0])
    ql=VGroup(math(r'\mathbb Q',39,PURPLE),txt('유리수',24,PURPLE)).arrange(RIGHT,buff=.2).move_to([4.85,1.95,0])
    z=RoundedRectangle(width=8.2,height=3.15,corner_radius=.24,color=ORANGE,fill_color=BLUE,fill_opacity=.03).move_to([-1.65,.1,0])
    zl=VGroup(math(r'\mathbb Z',40,BLUE),txt('정수',24,BLUE)).arrange(RIGHT,buff=.2).move_to([-4.7,1.2,0])
    op=math(r'(\mathbb Z,+,\times)',60,TEAL).move_to([-1.65,.2,0])
    frac=math(r'\frac12\notin\mathbb Z',53,ORANGE).move_to([4.4,.1,0])
    subset=math(r'\mathbb Z\subset\mathbb Q',35,PURPLE).move_to([0,-2.5,0])
    return VGroup(q,ql,z,zl,op,frac,subset)

class RingScene(Scene):
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
        getattr(self,['two_operations','closure','distributive','area','ring','polynomials','calculate','compare','division','field'][self.index-1])()
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
    def two_operations(self):
        h=title('군 · Group');old=math(r'(\mathbb Z,+,\times)',93,TEAL).move_to([0,.45,0]);self.add(h,old);self.to(2)
        eq=tuple_z();eq[3].set_opacity(.18)
        group=txt('덧셈에 대해 Group',29,TEAL).move_to([0,1.95,0])
        self.play_for(.8,ReplacementTransform(old,eq),FadeIn(group),Transform(h,header()));self.to(7)
        self.play_for(1,eq[3].animate.set_opacity(1),FadeOut(group));self.to(11)
    def closure(self):
        self.add(header());old=tuple_z();self.add(old);end=closure_end()
        self.play_for(.7,FadeOut(old),FadeIn(end[0]),FadeIn(end[1][0]),FadeIn(end[2][0]))
        self.play_for(.8,FadeIn(end[1][1],shift=DOWN*.25));self.to(2)
        self.play_for(.8,FadeIn(end[2][1],shift=DOWN*.25));self.to(4)
        self.play_for(1,FadeIn(end[1][2]),FadeIn(end[2][2]),FadeIn(end[3]),end[0][0].animate.set_stroke(TEAL));self.to(9)
    def distributive(self):
        self.add(header());old=closure_end();old[0][0].set_stroke(TEAL);self.add(old);end=dist_end()
        self.play_for(1,FadeOut(old),FadeIn(end[1]),FadeIn(end[2]));self.to(4)
        self.play_for(.8,GrowArrow(end[3]));self.to(7)
        eq=dist_formula().move_to([0,-1,0]);lab=txt('분배법칙 · Distributive Law',30,PURPLE).move_to([0,2.3,0])
        self.play_for(1,Write(eq),FadeIn(lab));self.to(8.8)
        self.play_for(1.2,Transform(eq,end[0]),Transform(lab,end[4]),FadeIn(end[5]));self.to(11)
    def area(self):
        self.add(header());old=dist_end();self.add(old);g=area_parts()
        top7=math('7',35,PURPLE).move_to([0,1.5,0]);area14=math('14',58,PURPLE).move_to([0,.15,0])
        eq=math(r'2(3+4)=14',51,PURPLE).move_to([0,-1.8,0])
        self.play_for(.8,FadeOut(old[1:]),FadeIn(g[0]),FadeIn(g[3]),FadeIn(top7),FadeIn(area14),FadeIn(eq));self.to(3)
        self.play_for(1.1,FadeIn(g[1]),FadeIn(g[2]),FadeOut(top7),FadeOut(area14),FadeIn(g[4]))
        self.play_for(.8,FadeIn(g[5]),FadeIn(g[6]));self.to(6)
        expanded=math(r'2(3+4)=2\times3+2\times4',47,PURPLE).move_to([0,-1.8,0])
        self.play_for(.9,TransformMatchingTex(eq,expanded));self.to(9)
        end=area_end();self.play_for(1.1,TransformMatchingTex(expanded,end[2]),Indicate(g[5],color=TEAL),Indicate(g[6],color=BLUE));self.to(15)
    def ring(self):
        h=header();old=area_end();self.add(h,old);end=ring_end()
        self.play_for(1.2,FadeOut(old),FadeIn(end[0]),Transform(h,header(True)))
        self.play_for(1,FadeIn(end[1]));self.to(5)
        self.play_for(1.1,FadeIn(end[2]));self.to(8)
        self.play_for(1,Circumscribe(end[2][0],color=TEAL));self.to(10)
        self.play_for(.9,Circumscribe(end[2][1],color=BLUE));self.to(12)
        self.play_for(.9,Circumscribe(end[2][2],color=PURPLE),FadeIn(end[3]));self.to(14)
        self.play_for(1,Indicate(end[2][0][2],color=TEAL),Indicate(end[2][0][3],color=TEAL));self.to(19)
    def polynomials(self):
        self.add(header(True));old=ring_end();self.add(old);self.to(4)
        end=poly_domains()
        self.play_for(1.2,FadeOut(old),FadeIn(end[:5]));self.to(7)
        self.play_for(.9,FadeIn(end[5:]));self.to(9)
    def calculate(self):
        self.add(header(True));old=poly_domains();self.add(old);end=calc_end();cards=end[0]
        self.play_for(.9,FadeOut(old),FadeIn(cards));self.to(4)
        add=MathTex(r'f(x)+g(x)=',r'x^2','+',r'(1+3)','+2x',font_size=43,color=TEAL).move_to([0,.35,0])
        self.play_for(.7,FadeIn(add))
        self.play_for(.8,Indicate(add[3],color=TEAL))
        self.play_for(.8,TransformMatchingTex(add,end[1]));self.to(8)
        mul=math(r'f(x)g(x)=(x^2+1)(2x+3)',43,BLUE).move_to([0,-.75,0])
        self.play_for(.6,FadeIn(mul));self.to(9)
        products=MathTex(r'x^2(2x)', '+',r'x^2(3)','+',r'1(2x)','+',r'1(3)',font_size=40,color=BLUE).move_to([0,-.75,0])
        self.play_for(.8,TransformMatchingTex(mul,products))
        for k in [0,2,4,6]:self.play_for(.45,Indicate(products[k],color=PURPLE))
        self.play_for(1,TransformMatchingTex(products,end[2]))
        self.play_for(.6,FadeIn(end[3]));self.to(15)
    def compare(self):
        self.add(header(True));old=calc_end();self.add(old);end=compare_end()
        self.play_for(1.1,FadeOut(old),FadeIn(end[0]),FadeIn(end[1]));self.to(5)
        self.play_for(.8,FadeIn(end[2]));self.to(11)
    def division(self):
        self.add(header(True));old=compare_end();self.add(old);end=div_end()
        self.play_for(1.1,FadeOut(old),FadeIn(end[2]),FadeIn(end[3]),FadeIn(end[4]))
        ok=txt('덧셈 · 곱셈은 정수 안에서',25,TEAL).move_to([-1.65,-1,0]);self.play_for(.6,FadeIn(ok));self.to(4)
        div=math(r'1\div2',58,ORANGE).move_to([3.4,2,0]);self.play_for(.7,FadeIn(div));self.to(6)
        frac=math(r'\frac12',65,ORANGE).move_to([-1.65,-1,0]);self.play_for(.5,FadeOut(ok),FadeIn(frac))
        self.play_for(1.1,ReplacementTransform(frac,end[5]),FadeOut(div),FadeIn(end[0]),FadeIn(end[1]),FadeIn(end[6]))
        self.to(10)
    def field(self):
        h=header(True);old=div_end();self.add(h,old)
        qeq=math(r'(\mathbb Q,+,\times)',88,PURPLE).move_to([0,.4,0])
        question=txt('0이 아닌 원소로 나눌 수 있다면?',30,PURPLE).move_to([0,-1.3,0])
        self.play_for(2,FadeOut(old),FadeIn(qeq),FadeIn(question));self.to(4)
        self.play_for(1.2,Indicate(qeq,color=TEAL));self.to(6)
        field=txt('체 · Field',38,PURPLE).move_to([0,2.1,0])
        self.play_for(.9,FadeIn(field),FadeOut(question));self.to(8)
