from pathlib import Path
import importlib.util, json, textwrap
from manim import *
R=Path(__file__).resolve().parent
# Reuse the established chapter without mutating its sources or module globals.
_spec=importlib.util.spec_from_file_location('algebra_ch01_shared',R.parent/'chapter_01'/'visuals.py')
shared=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(shared)
txt,math,marked,title,structure_cards=shared.txt,shared.math,shared.marked,shared.title,shared.structure_cards
WHITE_INK,MUTED,TEAL,BLUE,ORANGE,PURPLE=shared.WHITE_INK,shared.MUTED,shared.TEAL,shared.BLUE,shared.ORANGE,shared.PURPLE
KO=['닫힘','항등원','역원','결합법칙'];EN=['Closure','Identity Element','Inverse Element','Associativity'];AC=[TEAL,BLUE,ORANGE,PURPLE]
def header():return title('군 · Group')
def fit(m,width):
    if m.width>width:m.scale_to_fit_width(width)
    return m
def label(k,y=-2.25):return VGroup(txt(KO[k],28,AC[k]),txt(EN[k],23,AC[k])).arrange(RIGHT,buff=.3).move_to([0,y,0])
def plain(size=2.2,center=[0,.3,0]):
    return Square(side_length=size,stroke_color=BLUE,stroke_width=4,fill_color=BLUE,fill_opacity=.1).shift(np.array(center))
def symmetry_end():
    return VGroup(plain(),VGroup(txt('대칭',33,TEAL),txt('Symmetry',25,TEAL)).arrange(RIGHT,buff=.3).move_to([0,2.25,0]),txt('이 정사각형을 보존하는 변환',26,MUTED).move_to([0,-1.65,0]))
def bank():
    b=VGroup()
    for k,x in enumerate([-4.5,-1.5,1.5,4.5]):
        b.add(VGroup(marked(k*PI/2,.78,[x,1.85,0]),math(r'R_{'+str(k*90)+'}',31,BLUE).move_to([x,.95,0])))
    box=RoundedRectangle(width=12,height=2.1,corner_radius=.2,color=BLUE,stroke_opacity=.6).move_to([0,1.5,0])
    return VGroup(box,b,math('G',30,TEAL).move_to([-5.55,1.8,0]))
def closure_end():
    b=bank();b[0].set_stroke(TEAL,opacity=1)
    b[1][3][1].set_color(TEAL)
    return VGroup(b,math(r'R_{180}\circ R_{90}=R_{270}\in G',49,TEAL).move_to([0,-.75,0]),label(0))
def identity_end():
    return VGroup(bank(),marked(PI/2,1.2,[-3,-.8,0]),math(r'R_0\circ R_{90}=R_{90}\circ R_0=R_{90}',39,BLUE).move_to([1.5,-.8,0]),label(1))
def inverse_end():
    return VGroup(bank(),marked(0,1.2,[-3,-.8,0]),math(r'R_{-90}\circ R_{90}=R_0',46,ORANGE).move_to([1.7,-.8,0]),label(2))
def assoc_diagram():
    seq=math(r'A=R_{90},\quad B=R_{180},\quad C=R_{270}',36,BLUE).move_to([0,2.55,0])
    order=txt('적용 순서 : A → B → C',23,MUTED)
    order.move_to([0,1.9,0])
    left=VGroup(txt('먼저 A와 B를 합성',23,PURPLE).move_to([-3.2,1.2,0]),MathTex(r'C\circ(',r'B\circ A',r')',font_size=40,color=PURPLE).move_to([-3.2,.5,0]),marked(PI,1.45,[-3.2,-.9,0]))
    right=VGroup(txt('먼저 B와 C를 합성',23,PURPLE).move_to([3.2,1.2,0]),MathTex(r'(',r'C\circ B',r')\circ A',font_size=40,color=PURPLE).move_to([3.2,.5,0]),marked(PI,1.45,[3.2,-.9,0]))
    return VGroup(seq,order,left,right,label(3))
def condition_grid():
    fs=[r'a\star b\in G',r'e\star a=a\star e=a',r'a^{-1}\star a=a\star a^{-1}=e',r'(a\star b)\star c=a\star(b\star c)']
    out=VGroup()
    for k,(x,y) in enumerate([(-3.25,1.6),(3.25,1.6),(-3.25,-.65),(3.25,-.65)]):
        bg=RoundedRectangle(width=5.8,height=1.85,corner_radius=.18,color=AC[k],stroke_opacity=.7,fill_color=AC[k],fill_opacity=.035).move_to([x,y,0])
        lab=VGroup(txt(KO[k],26,AC[k]),txt(EN[k],20,AC[k])).arrange(RIGHT,buff=.2).move_to([x,y+.42,0])
        eq=fit(math(fs[k],31,WHITE_INK),5.3).move_to([x,y-.4,0])
        out.add(VGroup(bg,lab,eq))
    return out

def group_word():return txt('군  /  GROUP',46,TEAL).move_to([0,.25,0])
def numline():
    line=NumberLine(x_range=[-4,10,1],length=11.8,include_numbers=False,include_tip=True,color=MUTED,tick_size=.075).move_to([0,-.55,0])
    labels=VGroup(*[math(str(k),23,BLUE if k==0 else MUTED).move_to(line.n2p(k)+DOWN*.4) for k in range(-4,11)])
    return VGroup(line,labels)
def integer_base():
    return VGroup(math(r'\mathbb Z=\{\ldots,-2,-1,0,1,2,\ldots\}',42,BLUE).move_to([0,2.3,0]),numline())
def integer_closure_end():
    g=integer_base();point=Dot(g[1][0].n2p(8),radius=.09,color=TEAL)
    return VGroup(g,point,math(r'3+5=8\in\mathbb Z',50,TEAL).move_to([0,.7,0]),label(0))
def integer_inverse_end():
    g=integer_base();point=Dot(g[1][0].n2p(0),radius=.09,color=ORANGE)
    return VGroup(g,point,math(r'a+(-a)=0',54,ORANGE).move_to([0,.7,0]),label(2))
def compare_end():
    result=VGroup()
    for x,c in [(-3.2,BLUE),(3.2,TEAL)]:
        result.add(RoundedRectangle(width=5.8,height=3.9,corner_radius=.2,color=c,stroke_opacity=.6,fill_color=c,fill_opacity=.025).move_to([x,.45,0]))
    result.add(txt('정사각형의 네 회전',28,BLUE).move_to([-3.2,1.85,0]),txt('정수의 덧셈',28,TEAL).move_to([3.2,1.85,0]),marked(PI/2,1.15,[-3.2,.65,0]),math(r'(\mathbb Z,+)',57,TEAL).move_to([3.2,.65,0]))
    for x in [-3.2,3.2]:
        labels=VGroup(*[txt(t,19,c) for t,c in zip(KO,AC)]).arrange(RIGHT,buff=.2).move_to([x,-.55,0])
        result.add(labels,txt('Group',27,TEAL).move_to([x,-1.05,0]))
    result.add(txt('같은 군의 조건을 만족하는, 서로 다른 군',26,PURPLE).move_to([0,-2.25,0]))
    return result

def preserve_base():
    left=RoundedRectangle(width=5.8,height=3.9,corner_radius=.2,color=BLUE,stroke_opacity=.6).move_to([-3.2,.45,0])
    right=RoundedRectangle(width=5.8,height=3.9,corner_radius=.2,color=PURPLE,stroke_opacity=.6).move_to([3.2,.45,0])
    geom=VGroup(txt('기하학적 대칭',27,BLUE).move_to([-3.2,1.85,0]),plain(1.45,[-3.2,.5,0]),txt('회전과 반사 · 형태 보존',22,MUTED).move_to([-3.2,-.85,0]))
    alg=VGroup(txt('대수적 대칭',27,PURPLE).move_to([3.2,1.85,0]),math(r'x^2-2=0',39).move_to([3.2,1.05,0]),math(r'\sqrt2',40,TEAL).move_to([1.8,.2,0]),math(r'-\sqrt2',40,ORANGE).move_to([4.6,.2,0]),DoubleArrow([2.5,.2,0],[3.8,.2,0],buff=0,color=PURPLE,stroke_width=2,tip_length=.12),txt('대수적 관계를 보존하는 치환',21,MUTED).move_to([3.2,-.85,0]))
    return VGroup(left,right,geom,alg)
def preserve_end():
    p=preserve_base()
    rule=math(r'a+b\sqrt2\longmapsto a-b\sqrt2\quad(a,b\in\mathbb Q)',33,PURPLE).move_to([0,-1.95,0])
    badge=txt('GROUP · 구조를 보존하는 모든 가역적 변환',25,TEAL).move_to([0,2.7,0])
    return VGroup(p,rule,badge)

class GroupScene(Scene):
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
        getattr(self,['focus','symmetry','closure','identity','inverse','associativity','axioms','integer_closure','integer_inverse','compare','preserve','two_operations'][self.index-1])()
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
    def focus(self):
        h=title('숫자에서 구조로');cs=structure_cards();cs[1:].set_opacity(.28);cs[0][0].set_stroke(width=4)
        abstract=shared.math(r'(S,\star)',104,PURPLE).scale(.4).move_to([0,2.6,0]);self.add(h,cs,abstract)
        target=VGroup(txt('군',44,TEAL),txt('Group',32,TEAL)).arrange(RIGHT,buff=.3).move_to([0,2.3,0])
        self.play_for(1.3,FadeOut(cs[1:]),FadeOut(abstract),ReplacementTransform(cs[0],target),Transform(h,header()))
        sq=marked(center=[0,.3,0]);self.play_for(.7,FadeIn(sq))
        self.to(2.3)
        eq=math(r'R_{90}\longleftrightarrow1',42,TEAL).move_to([0,-1.7,0])
        self.play_for(1.1,Rotate(sq,PI/2,about_point=sq[0].get_center()),FadeIn(eq))
        self.to(7.7);self.play_for(.7,FadeOut(eq));self.to(9)
        unmarked=plain();self.play_for(1,ReplacementTransform(sq,unmarked),FadeOut(target));self.to(13)
    def symmetry(self):
        h=header();left=plain();self.add(h,left)
        right=plain(center=[3.1,.3,0]);refleft=DashedVMobject(plain(center=[-3.1,.3,0]).set_fill(opacity=0).set_stroke(MUTED,width=2),num_dashes=28);refright=DashedVMobject(right.copy().set_fill(opacity=0).set_stroke(MUTED,width=2),num_dashes=28)
        angles=VGroup(math(r'90^\circ',40,TEAL).move_to([-3.1,2.2,0]),math(r'30^\circ',40,ORANGE).move_to([3.1,2.2,0]))
        self.play_for(.6,left.animate.shift(LEFT*3.1),FadeIn(right),FadeIn(refleft),FadeIn(refright),FadeIn(angles))
        self.play_for(2.7,Rotate(left,PI/2,about_point=left.get_center()))
        self.play_for(.5,left.animate.set_stroke(TEAL));self.to(4)
        right.set_stroke(ORANGE)
        self.play_for(2.5,Rotate(right,PI/6,about_point=right.get_center()))
        self.to(7)
        common=VGroup(txt('강체이동',27,BLUE),txt('Rigid Motion',25,BLUE)).arrange(RIGHT,buff=.3).move_to([0,-1.7,0])
        desc=txt('두 변환 모두 길이와 각도를 보존합니다',23,MUTED).move_to([0,-2.3,0])
        self.play_for(.7,FadeIn(common),FadeIn(desc));self.to(12)
        yes=txt('대칭 · Symmetry',26,TEAL).move_to([-3.1,-1.7,0]);no=txt('이 정사각형의 대칭은 아님',23,ORANGE).move_to([3.1,-1.7,0])
        self.play_for(.7,ReplacementTransform(common,yes),FadeIn(no));self.to(16)
        self.play_for(.8,Rotate(right,-PI/6,about_point=right.get_center()))
        end=symmetry_end()
        self.play_for(1.2,ReplacementTransform(left,end[0]),FadeOut(right),FadeOut(refleft),FadeOut(refright),FadeOut(angles),FadeOut(yes),FadeOut(no),FadeOut(desc),FadeIn(end[1]),FadeIn(end[2]))
        self.to(23)
    def closure(self):
        self.add(header());old=symmetry_end();self.add(old);b=bank()
        self.play_for(1,FadeOut(old),FadeIn(b))
        note=txt('표식은 회전을 추적하는 보조 표시입니다',20,MUTED).move_to([0,-2.45,0])
        self.play_for(.6,FadeIn(note));self.to(3)
        sq=marked(0,1.2,[-3,-.8,0]);eq=math(r'R_{90}',43,BLUE).move_to([1.7,-.8,0]);self.play_for(.45,FadeIn(sq),FadeIn(eq))
        self.play_for(1.45,Rotate(sq,PI/2,about_point=sq[0].get_center()),Indicate(b[1][1][1],color=TEAL))
        self.play_for(.4,Transform(eq,math(r'R_{180}\circ R_{90}',43,BLUE).move_to([1.7,-.8,0])))
        self.play_for(1.9,Rotate(sq,PI,about_point=sq[0].get_center()),Indicate(b[1][2][1],color=TEAL))
        self.play_for(.6,Transform(eq,math(r'R_{180}\circ R_{90}=R_{270}',40,TEAL).move_to([1.7,-.8,0])))
        self.to(8)
        result=math(r'R_{270}',31,TEAL).move_to([4.2,-.8,0]);self.add(result)
        self.play_for(1.2,result.animate.move_to(b[1][3][1]),b[0].animate.set_stroke(TEAL,opacity=1))
        self.remove(result);b[1][3][1].set_color(TEAL)
        final=closure_end();self.play_for(.8,FadeOut(sq),ReplacementTransform(eq,final[1]),FadeOut(note))
        self.to(13);self.play_for(.6,FadeIn(final[2]));self.to(15)
    def identity(self):
        self.add(header());old=closure_end();self.add(old);end=identity_end()
        self.play_for(.8,ReplacementTransform(old[0],end[0]),FadeOut(old[1:]),FadeIn(end[1]))
        self.play_for(.8,Indicate(end[0][1][0][1],color=BLUE),Circumscribe(end[1][0],color=BLUE,time_width=.6))
        short=math(r'R_0\circ R_{90}=R_{90}',45,BLUE).move_to([1.5,-.8,0]);self.play_for(.7,FadeIn(short))
        self.to(4)
        self.play_for(1,Circumscribe(end[1][0],color=BLUE),Transform(short,end[2]))
        self.play_for(.6,FadeIn(end[3]));self.to(10)
    def inverse(self):
        self.add(header());old=identity_end();self.add(old);sq=old[1]
        self.play_for(.6,FadeOut(old[2:]),Rotate(sq,-PI/2,about_point=sq[0].get_center()))
        arc=DashedVMobject(Arc(radius=.6*np.sqrt(2),start_angle=3*PI/4,angle=PI/2,arc_center=[-3,-.8,0],color=ORANGE),num_dashes=14)
        self.play_for(.4,Create(arc))
        eq=math(r'R_{90}',46,BLUE).move_to([1.7,-.8,0]);self.add(eq)
        self.play_for(1.1,Rotate(sq,PI/2,about_point=sq[0].get_center()))
        self.play_for(.4,Transform(eq,math(r'R_{-90}\circ R_{90}',44,ORANGE).move_to([1.7,-.8,0])))
        self.play_for(1.2,Rotate(sq,-PI/2,about_point=sq[0].get_center()))
        self.to(4)
        end=inverse_end();self.play_for(.7,Transform(eq,end[2]),FadeOut(arc),FadeIn(end[3]))
        self.to(9)
    def associativity(self):
        self.add(header());old=inverse_end();self.add(old);g=assoc_diagram()
        # Both diagrams start at the same orientation. Composition acts right-to-left.
        for part in [g[2][2],g[3][2]]:part.rotate(-PI,about_point=part[0].get_center())
        self.play_for(.8,FadeOut(old),FadeIn(g[:4]))
        self.to(1.5)
        leftbrace=SurroundingRectangle(g[2][1][1],color=PURPLE,buff=.12,corner_radius=.08)
        rightbrace=SurroundingRectangle(g[3][1][1],color=PURPLE,buff=.12,corner_radius=.08)
        self.play_for(.5,Create(leftbrace),Create(rightbrace))
        # The computation's parentheses change; the actual A, B, C application order does not.
        for angle,duration in [(PI/2,1.2),(PI,1.6),(3*PI/2,1.8)]:
            self.play_for(duration,Rotate(g[2][2],angle,about_point=g[2][2][0].get_center()),Rotate(g[3][2],angle,about_point=g[3][2][0].get_center()))
        answer=math(r'180^\circ\qquad=\qquad180^\circ',35,TEAL).move_to([0,-1.95,0])
        self.play_for(.6,FadeOut(leftbrace),FadeOut(rightbrace),FadeIn(answer));self.to(8)
        self.play_for(.6,FadeOut(answer),FadeIn(g[4]));self.to(11)
    def axioms(self):
        self.add(header());old=assoc_diagram();self.add(old);grid=condition_grid()
        self.play_for(.6,FadeOut(old),FadeIn(grid[0]))
        for k in range(1,4):self.play_for(.55,FadeIn(grid[k]))
        self.to(4.8)
        word=group_word();self.play_for(1.1,ReplacementTransform(grid,word));self.to(7)
    def integer_closure(self):
        self.add(header());word=group_word();self.add(word)
        self.play_for(.6,word.animate.scale(.6).move_to([0,2.65,0]))
        self.to(4)
        base=integer_base();self.play_for(.8,FadeOut(word),FadeIn(base));self.to(6)
        ln=base[1][0];dot=Dot(ln.n2p(3),radius=.09,color=TEAL)
        arrow=Arrow(ln.n2p(3)+UP*.38,ln.n2p(8)+UP*.38,buff=0,color=TEAL,stroke_width=3,tip_length=.15)
        self.add(dot);self.play_for(1.8,dot.animate.move_to(ln.n2p(8)),GrowArrow(arrow))
        end=integer_closure_end();self.play_for(.6,FadeIn(end[2]),FadeIn(end[3]),FadeOut(arrow));self.to(10)
    def integer_inverse(self):
        self.add(header());old=integer_closure_end();self.add(old);ln=old[0][1][0];point=old[1]
        self.play_for(.6,FadeOut(old[2:]),point.animate.move_to(ln.n2p(3)))
        eq=math('3+0=3',54,BLUE).move_to([0,.7,0]);lab=label(1)
        self.play_for(.6,FadeIn(eq),FadeIn(lab),Circumscribe(point,color=BLUE))
        self.to(4)
        arr=Arrow(ln.n2p(3)+UP*.35,ln.n2p(0)+UP*.35,buff=0,color=ORANGE,stroke_width=3,tip_length=.15)
        self.play_for(1.8,point.animate.move_to(ln.n2p(0)).set_color(ORANGE),GrowArrow(arr),Transform(eq,math(r'3+(-3)=0',54,ORANGE).move_to([0,.7,0])),Transform(lab,label(2)))
        self.to(7)
        self.play_for(.8,Transform(eq,math(r'a+(-a)=0',54,ORANGE).move_to([0,.7,0])),FadeOut(arr));self.to(11)
    def compare(self):
        self.add(header());old=integer_inverse_end();self.add(old)
        eq=math(r'(2+3)+4=2+(3+4)=9',51,PURPLE).move_to([0,.7,0])
        self.play_for(.8,Transform(old[2],eq),Transform(old[3],label(3)))
        first=SurroundingRectangle(old[2][0][:5],color=PURPLE,buff=.1)
        self.play_for(.6,Create(first));self.to(2.5);self.play_for(.5,FadeOut(first));self.to(4)
        group=math(r'(\mathbb Z,+)\quad\mathrm{Group}',54,TEAL).move_to([0,.7,0])
        self.play_for(.7,Transform(old[2],group));self.to(7)
        end=compare_end();self.play_for(1.2,FadeOut(old),FadeIn(end[:-1]));self.to(11)
        self.play_for(.7,FadeIn(end[-1]));self.to(16)
    def preserve(self):
        self.add(header());old=compare_end();self.add(old);base=preserve_base()
        self.play_for(.9,FadeOut(old),FadeIn(base[:3]))
        sq=base[2][1]
        self.play_for(1.8,Rotate(sq,PI/2,about_point=sq.get_center()))
        # A reflection is shown as an isometry of the plane, not a 3D rotation.
        axis=DashedLine([-3.2,-.6,0],[-3.2,1.6,0],color=TEAL,dash_length=.1)
        probe=Dot([-3.8,.8,0],color=TEAL,radius=.06);self.play_for(.5,Create(axis),FadeIn(probe))
        reflection=txt('반사',22,TEAL).move_to([-4.6,.5,0])
        sq.flip(UP,about_point=sq.get_center())
        self.play_for(1.4,probe.animate.move_to([-2.6,.8,0]),FadeIn(reflection))
        self.play_for(.5,FadeOut(axis),FadeOut(probe),FadeOut(reflection));self.to(7)
        self.play_for(.7,FadeIn(base[3]))
        self.play_for(1.5,Swap(base[3][2],base[3][3],path_arc=PI/2))
        self.to(11)
        # Restore label positions after the swap before the shared boundary state.
        self.play_for(1,Swap(base[3][2],base[3][3],path_arc=-PI/2))
        end=preserve_end();self.play_for(.8,FadeIn(end[1]))
        self.to(13)
        self.play_for(1,FadeIn(end[2]),Indicate(base[2][2],color=TEAL),Indicate(base[3][5],color=TEAL))
        self.to(20)
    def two_operations(self):
        self.add(header());old=preserve_end();self.add(old)
        eq=math(r'(\mathbb Z,+)',93,TEAL).move_to([0,.45,0])
        self.play_for(1.2,FadeOut(old),FadeIn(eq,shift=UP*.15))
        one=txt('하나의 연산',27,MUTED).move_to([0,-1.2,0]);self.play_for(.6,FadeIn(one));self.to(4)
        new=math(r'(\mathbb Z,+,\times)',93,TEAL).move_to([0,.45,0])
        self.play_for(1.8,TransformMatchingTex(eq,new),Transform(one,txt('덧셈과 곱셈 · 두 가지 연산',27,PURPLE).move_to([0,-1.2,0])))
        self.to(8.5);self.play_for(.6,FadeOut(one));self.to(10)
