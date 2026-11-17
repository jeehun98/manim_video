from pathlib import Path
import importlib.util,json,textwrap
from manim import *
R=Path(__file__).resolve().parent
_spec=importlib.util.spec_from_file_location('algebra_ch03_shared',R.parent/'chapter_03'/'visuals.py')
previous=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(previous)
shared=previous.shared
txt,math,title=shared.txt,shared.math,shared.title
WHITE_INK,MUTED,TEAL,BLUE,ORANGE,PURPLE=shared.WHITE_INK,shared.MUTED,shared.TEAL,shared.BLUE,shared.ORANGE,shared.PURPLE
def header():return title('체 · Field')
def fit(m,w):
    if m.width>w:m.scale_to_fit_width(w)
    return m

def rational_state(expanded=True):
    g=previous.div_end();g[3].set_color(TEAL)
    g[4].scale(.67).move_to([-1.65,.7,0])
    g[5].become(math(r'\frac12\in\mathbb Q',50,PURPLE).move_to([4.4,.1,0]))
    eq=math(r'1\div2',50,BLUE).move_to([-1.65,-.5,0])
    arrow=Arrow([-.3,-.5,0],[3.2,.1,0],buff=0,color=PURPLE,stroke_width=2,tip_length=.14)
    g.add(eq,arrow)
    if expanded:
        for i in [2,3,4,5,7,8]:g[i].set_opacity(0)
    return VGroup(g,math(r'\frac23\div\frac45=\frac56\in\mathbb Q',58,PURPLE).move_to([0,.6,0]),txt('나누는 수는 0이 아닐 때',24,ORANGE).move_to([0,-1.1,0]))
def pair_equation():return math(r'2\times\frac12=1',92,BLUE).move_to([0,.45,0])
def inverse_state():
    nodes=VGroup()
    for x,s in [(-2.5,'2'),(2.5,r'\frac12')]:nodes.add(VGroup(Circle(radius=.72,color=TEAL,fill_color=TEAL,fill_opacity=.035),math(s,60,TEAL)).move_to([x,.65,0]))
    link=DoubleArrow([-1.7,.65,0],[1.7,.65,0],color=TEAL,buff=0,stroke_width=3,tip_length=.16)
    label=VGroup(txt('곱셈 역원',32,TEAL),txt('Multiplicative Inverse',25,TEAL)).arrange(RIGHT,buff=.25).move_to([0,2.3,0])
    eq=math(r'2\times\frac12=1',50,BLUE).move_to([0,-.75,0])
    return VGroup(nodes,link,label,eq,txt('덧셈 역원',22,MUTED).move_to([-3,-1.7,0]),math('2+(-2)=0',35,TEAL).move_to([-3,-2.25,0]),txt('곱셈 역원',22,MUTED).move_to([3,-1.7,0]),math(r'2\times\frac12=1',35,BLUE).move_to([3,-2.25,0]))
def condition_state():
    out=VGroup()
    for x,c,head,formula,desc,eq in [(-3.2,TEAL,'덧셈',r'(\mathbb Q,+)','모든 원소에 덧셈 역원',r'a+(-a)=0'),(3.2,BLUE,'곱셈',r'(\mathbb Q\setminus\{0\},\times)','0이 아닌 원소에 곱셈 역원',r'a\cdot a^{-1}=1')]:
        card=VGroup(RoundedRectangle(width=5.8,height=3.5,corner_radius=.2,color=c,fill_color=c,fill_opacity=.025).move_to([x,.35,0]),txt(head,29,c).move_to([x,1.65,0]),fit(math(formula,46,c),5.1).move_to([x,.9,0]),txt('아벨 군',25,c).move_to([x,.2,0]),txt(desc,22,MUTED).move_to([x,-.4,0]),math(eq,40,c).move_to([x,-1,0]))
        out.add(card)
    out.add(math(r'a(b+c)=ab+ac',37,PURPLE).move_to([0,-1.95,0]),txt('분배법칙',22,PURPLE).move_to([-4.5,-1.95,0]),math(r'0\ne1',30,ORANGE).move_to([5,-1.95,0]),txt('체 · Field',37,PURPLE).move_to([0,2.7,0]))
    return out

def field_examples():
    out=VGroup()
    for x,s,ko,example in [(-4.2,r'\mathbb Q','유리수',r'\frac12'),(0,r'\mathbb R','실수',r'\sqrt2'),(4.2,r'\mathbb C','복소수',r'1+i')]:
        out.add(VGroup(RoundedRectangle(width=3.7,height=3.4,corner_radius=.2,color=PURPLE,fill_color=PURPLE,fill_opacity=.03).move_to([x,.35,0]),math(s,61,PURPLE).move_to([x,1.25,0]),txt(ko,26,PURPLE).move_to([x,.25,0]),math(example,44).move_to([x,-.7,0])))
    return VGroup(out,math(r'\mathbb Q\subset\mathbb R\subset\mathbb C',38,PURPLE).move_to([0,2.65,0]),txt('모두 무한히 많은 원소를 갖는 체',25,MUTED).move_to([0,-2.2,0]))
def finite_ring():
    c=np.array([-3.15,.1,0]);r=1.6
    outline=Circle(radius=r,color=PURPLE,stroke_opacity=.25).move_to(c)
    nodes=VGroup()
    for k in range(5):
        a=PI/2+TAU*k/5;p=c+np.array([r*np.cos(a),r*np.sin(a),0])
        nodes.add(VGroup(Circle(radius=.34,color=PURPLE,fill_color='#0B1020',fill_opacity=1),math(str(k),37)).move_to(p))
    return VGroup(outline,nodes,math(r'\mathbb F_5=\{0,1,2,3,4\}',44,PURPLE).move_to([0,2.7,0]),txt('5로 나눈 나머지',22,PURPLE).move_to(c+DOWN*.3))
def five_state():
    r=finite_ring();module=VGroup(RoundedRectangle(width=3.3,height=1.25,corner_radius=.18,color=PURPLE,fill_color=PURPLE,fill_opacity=.04),math(r'\mathrm{mod}\ 5',49,PURPLE)).move_to([2.9,.5,0])
    text=VGroup(txt('더한 뒤에도, 곱한 뒤에도',24,MUTED),txt('5로 나눈 나머지를 사용합니다',24,PURPLE)).arrange(DOWN,buff=.2).move_to([2.9,-1.1,0])
    return VGroup(r,module,text)
def pipeline(k=1):
    a,b,total=(2,3,6) if k==0 else (4,4,16)
    eq=math(f'{a}\\times{b}={total}',48,BLUE).move_to([2.9,1.7,0])
    box=VGroup(RoundedRectangle(width=3.1,height=.85,corner_radius=.15,color=PURPLE,fill_color=PURPLE,fill_opacity=.04),math(r'\mathrm{mod}\ 5',37,PURPLE)).move_to([2.9,.3,0])
    arrows=VGroup(Arrow([2.9,1.15,0],[2.9,.8,0],buff=0,color=PURPLE,stroke_width=2,tip_length=.12),Arrow([2.9,-.2,0],[2.9,-.6,0],buff=0,color=TEAL,stroke_width=2,tip_length=.12))
    one=math('1',63,TEAL).move_to([2.9,-1.1,0]);cong=math(f'{a}\\times{b}={total}\\equiv1\\pmod5',37,TEAL).move_to([1.4,-2.3,0])
    return VGroup(eq,box,arrows,one,cong)
def inverse_pair_link(r):
    return DoubleArrow(r[1][2].get_center()+UP*.06,r[1][3].get_center()+UP*.06,buff=.39,color=TEAL,stroke_width=3,tip_length=.13)
def mod_end():
    r=finite_ring();link=inverse_pair_link(r)
    return VGroup(r,link,pipeline(1))
def finite_state():
    r=finite_ring();r[1][0][0].set_stroke(MUTED);r[1][0][1].set_color(MUTED)
    link=inverse_pair_link(r);loops=VGroup()
    for k in [1,4]:
        loops.add(Arc(radius=.48,start_angle=.2,angle=TAU*.83,color=TEAL).add_tip(tip_length=.12).move_arc_center_to(r[1][k].get_center()))
    table=VGroup()
    for i,(a,b) in enumerate(zip(['0','1','2','3','4'],['없음','1','3','2','4'])):
        x=1.25+i*.85;c=MUTED if i==0 else TEAL
        table.add(VGroup(Rectangle(width=.85,height=.75,color=PURPLE,stroke_width=1).move_to([x,.65,0]),math(a,33,c).move_to([x,.65,0]),Rectangle(width=.85,height=.75,color=PURPLE,stroke_width=1).move_to([x,-.1,0]),txt(b,22,c).move_to([x,-.1,0])))
    legend=txt('위 : 원소   /   아래 : 곱셈 역원',22,MUTED).move_to([2.95,1.55,0])
    label=txt('유한체 · Finite Field',29,PURPLE).move_to([2.95,-1.25,0])
    note=txt('나머지 덧셈과 곱셈도 체의 조건을 만족합니다',23,MUTED).move_to([0,-2.4,0])
    return VGroup(r,link,loops,table,legend,label,note)
def field_compare():
    g=VGroup()
    for x,c,s,ko,desc,eq in [(-3.2,PURPLE,r'\mathbb Q','유리수체','무한히 많은 원소',r'2\cdot\frac12=1'),(3.2,TEAL,r'\mathbb F_5','유한체','다섯 개의 원소',r'2\cdot3\equiv1\pmod5')]:
        g.add(VGroup(RoundedRectangle(width=5.8,height=4.1,corner_radius=.2,color=c,fill_color=c,fill_opacity=.025).move_to([x,.35,0]),txt(ko,28,c).move_to([x,1.85,0]),math(s,63,c).move_to([x,.9,0]),txt(desc,23,MUTED).move_to([x,.05,0]),math(eq,42,c).move_to([x,-.85,0])))
    g.add(txt('서로 다른 원소와 연산, 공통된 체의 공리',26,PURPLE).move_to([0,-2.25,0]));return g

def application_cards():
    g=VGroup()
    for x,c,head in [(-4.2,BLUE,'방정식'),(0,TEAL,'오류정정부호'),(4.2,PURPLE,'암호학')]:
        g.add(VGroup(RoundedRectangle(width=3.8,height=3.7,corner_radius=.18,color=c,fill_color=c,fill_opacity=.025).move_to([x,.15,0]),txt(head,29,c).move_to([x,1.5,0])))
    g[0].add(math(r'x^2-2=0',39,BLUE).move_to([-4.2,.55,0]),math(r'\pm\sqrt2',42,BLUE).move_to([-4.2,-.4,0]),txt('근과 대수적 관계',21,MUTED).move_to([-4.2,-1.25,0]))
    for y,s,c in [(.65,'101',TEAL),(.05,'101  101  101',TEAL),(-.55,'101  001  101',ORANGE),(-1.2,'복원 → 101',TEAL)]:g[1].add(txt(s,20,c).move_to([0,y,0]))
    for y,s,c in [(.65,'데이터 + 키',BLUE),(.05,'유한체 연산',PURPLE),(-.55,'암호 알고리즘',PURPLE),(-1.2,'암호문',PURPLE)]:g[2].add(txt(s,23,c).move_to([4.2,y,0]))
    g.add(txt('부호와 암호의 흐름을 나타낸 개념도',22,MUTED).move_to([0,-2.35,0]));return g

def relation_cards():
    g=VGroup()
    for x,c,ko,en,eq in [(-4.2,TEAL,'군','Group',r'(\mathbb Z,+)'),(0,BLUE,'환','Ring',r'(\mathbb Z,+,\times)'),(4.2,PURPLE,'체','Field',r'(\mathbb Q,+,\times)')]:
        g.add(VGroup(RoundedRectangle(width=3.8,height=3.8,corner_radius=.2,color=c,fill_color=c,fill_opacity=.035).move_to([x,.25,0]),txt(ko,51,c).move_to([x,1.3,0]),txt(en,30,c).move_to([x,.25,0]),fit(math(eq,40,c),3.3).move_to([x,-.85,0])))
    return g

class FieldScene(Scene):
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
        getattr(self,['rational','reinterpret','inverse','conditions','examples','five','mod_inverse','finite','applications','relations'][self.index-1])()
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
    def rational(self):
        h=title('환 · Ring');eq=math(r'(\mathbb Q,+,\times)',88,PURPLE).move_to([0,.4,0]);name=txt('체 · Field',38,PURPLE).move_to([0,2.1,0]);self.add(h,eq,name)
        g=rational_state(False);self.play_for(1,FadeOut(eq),FadeOut(name),FadeIn(g[0]),Transform(h,header()));self.to(5)
        self.play_for(1.3,Circumscribe(g[0][0],color=PURPLE));self.to(7)
        self.play_for(1.1,Indicate(g[0][-2],color=BLUE));self.to(10)
        self.play_for(.9,Indicate(g[0][5],color=PURPLE));self.to(13)
        self.play_for(1.1,FadeOut(g[0][2:6]),FadeOut(g[0][7:]),FadeIn(g[1]),FadeIn(g[2]));self.to(20)
    def reinterpret(self):
        self.add(header());old=rational_state();self.add(old)
        eq=math(r'a\div2',93,BLUE).move_to([0,.45,0]);self.play_for(1,FadeOut(old),FadeIn(eq));self.to(4)
        mul=math(r'a\times\frac12',93,BLUE).move_to([0,.45,0]);self.play_for(1.5,TransformMatchingTex(eq,mul));self.to(7)
        line=math(r'a\div2=a\times\frac12',49,MUTED).move_to([0,2.15,0]);self.play_for(1,FadeIn(line));self.to(11)
        self.play_for(1.1,TransformMatchingTex(mul,pair_equation()),FadeOut(line));self.to(14)
    def inverse(self):
        self.add(header());eq=pair_equation();self.add(eq);end=inverse_state()
        self.play_for(1.1,ReplacementTransform(eq,end[3]),FadeIn(end[0]),GrowArrow(end[1]))
        self.play_for(.8,FadeIn(end[2]));self.to(6)
        oldlabel=txt('군의 역원 · Inverse Element',24,MUTED).move_to([0,-2.05,0]);self.play_for(.6,FadeIn(oldlabel));self.to(10)
        self.play_for(.9,FadeOut(oldlabel),FadeIn(end[4:]));self.to(13)
    def conditions(self):
        self.add(header());old=inverse_state();self.add(old);end=condition_state()
        self.play_for(1.1,FadeOut(old),FadeIn(end[:2]),FadeIn(end[4]));self.to(7)
        checks=VGroup(txt('교환법칙 · 결합법칙',22,TEAL).move_to([-3.2,2.5,0]),txt('교환법칙 · 결합법칙',22,BLUE).move_to([3.2,2.5,0]))
        self.play_for(.8,FadeIn(checks),FadeIn(end[2]),FadeIn(end[3]));self.to(14)
        frame=RoundedRectangle(width=12.6,height=5.25,corner_radius=.24,color=PURPLE,stroke_width=2).move_to([0,.35,0])
        self.play_for(1,Create(frame),FadeIn(end[5]),FadeOut(checks));self.to(16.7)
        self.play_for(.6,FadeOut(frame));self.to(18)
    def examples(self):
        self.add(header());old=condition_state();self.add(old);end=field_examples()
        self.play_for(.7,FadeOut(old),FadeIn(end[0][0]))
        self.play_for(.6,FadeIn(end[0][1]));self.play_for(.6,FadeIn(end[0][2]),FadeIn(end[1]),FadeIn(end[2]));self.to(4)
        zero=math('0',90).move_to([0,.3,0]);self.play_for(1.2,FadeOut(end),FadeIn(zero));self.to(8)
    def five(self):
        self.add(header());zero=math('0',90).move_to([0,.3,0]);self.add(zero)
        digits=VGroup(*[math(str(k),63).move_to([-4+2*k,.3,0]) for k in range(5)])
        self.play_for(.5,ReplacementTransform(zero,digits[0]))
        self.play_for(1.2,LaggedStart(*[FadeIn(digits[k]) for k in range(1,5)],lag_ratio=.25))
        end=five_state();self.play_for(1.3,ReplacementTransform(digits,end[0][1]),FadeIn(end[0][0]),FadeIn(end[0][2]),FadeIn(end[0][3]));self.to(4)
        self.play_for(.9,FadeIn(end[1]),FadeIn(end[2]));self.to(7)
    def mod_inverse(self):
        self.add(header());old=five_state();self.add(old);r=old[0];p=pipeline(0)
        self.play_for(.7,FadeOut(old[1:]),FadeIn(p[0]),FadeIn(p[1]),FadeIn(p[2]))
        self.play_for(.7,Indicate(r[1][2],color=TEAL),Indicate(r[1][3],color=TEAL))
        # Integer results stay outside F5. Only the reduced remainder returns to a node.
        self.play_for(1,FadeIn(p[3],shift=DOWN*.3));self.play_for(.7,FadeIn(p[4]));self.to(5)
        link=inverse_pair_link(r);self.play_for(.8,GrowArrow(link),Circumscribe(r[1][1],color=TEAL));self.to(8)
        target=pipeline(1)
        self.play_for(.6,ReplacementTransform(p[0],target[0]),FadeOut(p[3]),FadeOut(p[4]),Indicate(r[1][4],color=TEAL))
        self.play_for(1.1,FadeIn(target[3],shift=DOWN*.35))
        self.play_for(.7,FadeIn(target[4]),Circumscribe(r[1][4],color=TEAL));self.to(13)
    def finite(self):
        self.add(header());old=mod_end();self.add(old);end=finite_state()
        self.play_for(.8,FadeOut(old[2]),ReplacementTransform(old[0],end[0]),ReplacementTransform(old[1],end[1]))
        self.play_for(1,Create(end[2]),FadeIn(end[3]),FadeIn(end[4]));self.to(4)
        self.play_for(.8,FadeIn(end[6]));self.to(7)
        self.play_for(.8,FadeIn(end[5]),end[0][0].animate.set_stroke(PURPLE,opacity=1,width=3));self.to(10)
    def applications(self):
        self.add(header());old=finite_state();old[0][0].set_stroke(PURPLE,opacity=1,width=3);self.add(old);comparison=field_compare()
        self.play_for(1,FadeOut(old),FadeIn(comparison));self.to(5)
        self.play_for(1.2,comparison[0][4].animate.set_opacity(.25),comparison[1][4].animate.set_opacity(.25))
        self.to(11)
        apps=application_cards();self.play_for(1,FadeOut(comparison),FadeIn(apps))
        self.play_for(1.2,Indicate(apps[1][4],color=ORANGE))
        self.play_for(.8,Indicate(apps[1][5],color=TEAL),Indicate(apps[2][3],color=PURPLE));self.to(17)
    def relations(self):
        h=header();old=application_cards();self.add(h,old);end=relation_cards()
        self.play_for(.8,FadeOut(old),FadeIn(end[0]),Transform(h,title('군 · 환 · 체')));self.to(3)
        self.play_for(.8,FadeIn(end[1]));self.to(5)
        self.play_for(.8,FadeIn(end[2]));self.to(8)
