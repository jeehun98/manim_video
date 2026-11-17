from pathlib import Path
import importlib.util,json,textwrap
from manim import *
R=Path(__file__).resolve().parent
_spec=importlib.util.spec_from_file_location('algebra_ch04_shared',R.parent/'chapter_04'/'visuals.py')
previous=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(previous)
shared=previous.shared
txt,math,title,marked=shared.txt,shared.math,shared.title,shared.marked
WHITE_INK,MUTED,TEAL,BLUE,ORANGE,PURPLE=shared.WHITE_INK,shared.MUTED,shared.TEAL,shared.BLUE,shared.ORANGE,shared.PURPLE
def header():return title('군 · 환 · 체')
def fit(m,w):
    if m.width>w:m.scale_to_fit_width(w)
    return m

def group_state():
    left=VGroup(RoundedRectangle(width=5.8,height=3.8,corner_radius=.2,color=TEAL,fill_color=TEAL,fill_opacity=.025).move_to([-3.2,.1,0]),txt('정사각형의 회전',27,TEAL).move_to([-3.2,1.35,0]),marked(PI/2,1.25,[-3.2,.05,0]))
    right=VGroup(RoundedRectangle(width=5.8,height=3.8,corner_radius=.2,color=TEAL,fill_color=TEAL,fill_opacity=.025).move_to([3.2,.1,0]),math(r'(\mathbb Z,+)',58,TEAL).move_to([3.2,.85,0]),math('3+(-3)=0',44).move_to([3.2,-.2,0]))
    labels=VGroup(*[txt('닫힘 · 항등원 · 역원 · 결합법칙',20,MUTED).move_to([x,-1.35,0]) for x in [-3.2,3.2]])
    return VGroup(txt('군 · Group  |  하나의 연산',34,TEAL).move_to([0,2.6,0]),left,right,labels)
def detailed_cards():
    out=VGroup()
    for x,c,ko,en,formula,lines in [(-4.2,TEAL,'군','Group',r'(\mathbb Z,+)',['하나의 연산','닫힘 · 항등원 · 역원','결합법칙']),(0,BLUE,'환','Ring',r'(\mathbb Z,+,\times)',['덧셈 : 아벨 군','곱셈 : 결합법칙','두 연산 : 분배법칙']),(4.2,PURPLE,'체','Field',r'(\mathbb Q,+,\times)',['가환환','0이 아닌 모든 원소에','곱셈 역원 존재'])]:
        card=VGroup(RoundedRectangle(width=3.8,height=4.8,corner_radius=.2,color=c,fill_color=c,fill_opacity=.025).move_to([x,.35,0]),txt(ko,41,c).move_to([x,2.15,0]),txt(en,28,c).move_to([x,1.35,0]),fit(math(formula,43,c),3.35).move_to([x,.45,0]))
        for j,s in enumerate(lines):card.add(fit(txt(s,22,c),3.35).move_to([x,-.4-j*.6,0]))
        out.add(card)
    return out

def inclusion_state():
    outer=RoundedRectangle(width=12.3,height=4.15,corner_radius=.25,color=BLUE,fill_color=BLUE,fill_opacity=.025).move_to([0,.1,0])
    ring=txt('환 · Ring',30,BLUE).move_to([-4.7,1.5,0])
    inner=RoundedRectangle(width=5.4,height=3.1,corner_radius=.2,color=PURPLE,fill_color=PURPLE,fill_opacity=.045).move_to([2.7,.05,0])
    field=txt('체 · Field',28,PURPLE).move_to([2.7,1.1,0])
    q=math(r'(\mathbb Q,+,\times)',43,PURPLE).move_to([2.7,.15,0]);f=math(r'\mathbb F_5',41,PURPLE).move_to([2.7,-.85,0])
    z=math(r'(\mathbb Z,+,\times)',47,BLUE).move_to([-3,.5,0]);why=math(r'1\div2=\frac12\notin\mathbb Z',43,ORANGE).move_to([-3,-.75,0])
    relation=math(r'\mathrm{Field}\subsetneq\mathrm{Ring}',42,PURPLE).move_to([0,2.7,0])
    return VGroup(outer,ring,inner,field,q,f,z,why,relation)
def operation_state(mode=0):
    c=[TEAL,BLUE,PURPLE][mode];symbol=r'\mathbb Q' if mode==2 else r'\mathbb Z'
    formula=math('('+symbol+(','+r'+,\times' if mode else ',+')+')',82,c).move_to([0,1.25,0])
    name=txt(['군 · Group','환 · Ring','체 · Field'][mode],35,c).move_to([0,2.6,0])
    box=RoundedRectangle(width=11.8,height=2.1,corner_radius=.2,color=BLUE if mode<2 else PURPLE,fill_color=BLUE if mode<2 else PURPLE,fill_opacity=.025).move_to([0,-.95,0])
    setlabel=math(symbol,39,c).move_to([-5.15,-.35,0]);numbers=VGroup()
    for k in [-2,-1,0,1,2]:numbers.add(math(str(k),37,BLUE).move_to([k*1.5,-1.05,0]))
    numbers.add(math(r'\ldots',35,MUTED).move_to([-4.6,-1.05,0]),math(r'\ldots',35,MUTED).move_to([4.6,-1.05,0]))
    fractions=VGroup()
    if mode==2:
        for x,s in [(-2.25,r'-\frac32'),(-.75,r'-\frac12'),(.75,r'\frac12'),(2.25,r'\frac32')]:fractions.add(math(s,31,PURPLE).move_to([x,-1.05,0]))
    footer=txt(['같은 정수 집합에서 덧셈을 고려','원소 집합은 그대로, 곱셈도 함께 고려','유리수로 집합을 확장'][mode],25,c).move_to([0,-2.5,0])
    return VGroup(formula,name,box,setlabel,numbers,fractions,footer)
def correspondence_state():
    left=VGroup(RoundedRectangle(width=5.8,height=4.25,corner_radius=.2,color=BLUE,fill_color=BLUE,fill_opacity=.025).move_to([-3.2,.15,0]),txt('정사각형의 네 회전',27,BLUE).move_to([-3.2,1.7,0]),marked(3*PI/2,1.3,[-3.2,.4,0]),fit(math(r'R_{180}\circ R_{90}=R_{270}',39,BLUE),5.2).move_to([-3.2,-1,0]))
    right=VGroup(RoundedRectangle(width=5.8,height=4.25,corner_radius=.2,color=TEAL,fill_color=TEAL,fill_opacity=.025).move_to([3.2,.15,0]),txt('4로 나눈 나머지 덧셈',27,TEAL).move_to([3.2,1.7,0]),math(r'\{0,1,2,3\}',48,TEAL).move_to([3.2,.55,0]),math(r'1+2\equiv3\pmod4',44,TEAL).move_to([3.2,-1,0]))
    link=DoubleArrow([-2.1,.35,0],[1.7,.35,0],buff=0,color=PURPLE,stroke_width=2,tip_length=.13)
    rule=math(r'R_{90k}\longleftrightarrow k\pmod4',39,PURPLE).move_to([0,2.7,0])
    note=txt('연산을 보존하는 대응 · 연산 구조의 일치',26,PURPLE).move_to([0,-2.45,0])
    return VGroup(left,right,link,rule,note)
def closing_state():
    return VGroup(math(r'(S,\star)',104,PURPLE).move_to([0,1.15,0]),txt('추상대수학',40,PURPLE).move_to([0,-.1,0]),txt('Abstract Algebra',31,PURPLE).move_to([0,-.85,0]),txt('서로 다른 대상, 공통된 수학적 구조',30).move_to([0,-2,0]))

class ClosingScene(Scene):
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
        getattr(self,['group','ring_field','inclusion','operations','correspondence','closing'][self.index-1])()
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
    def group(self):
        h=header();cards=previous.relation_cards();self.add(h,cards);self.to(4)
        end=group_state();end[1][2].rotate(-PI/2,about_point=end[1][2][0].get_center())
        self.play_for(1.1,FadeOut(cards),FadeIn(end[:3]))
        self.play_for(1.4,Rotate(end[1][2],PI/2,about_point=end[1][2][0].get_center()));self.to(9)
        self.play_for(.7,FadeIn(end[3]));self.to(12)
    def ring_field(self):
        self.add(header());old=group_state();self.add(old);cards=detailed_cards()
        self.play_for(1,FadeOut(old),FadeIn(cards[:2]))
        self.play_for(.7,Circumscribe(cards[1][3],color=BLUE));self.to(5)
        self.play_for(1,Circumscribe(cards[1][4],color=TEAL));self.to(8)
        self.play_for(.9,Circumscribe(cards[1][6],color=PURPLE));self.to(11)
        self.play_for(1,FadeIn(cards[2]));self.to(14)
        self.play_for(.9,Circumscribe(cards[2][4],color=PURPLE),Indicate(cards[2][6],color=PURPLE));self.to(18)
    def inclusion(self):
        self.add(header());old=detailed_cards();self.add(old);end=inclusion_state()
        self.play_for(.9,FadeOut(old),FadeIn(end[:6]),FadeIn(end[8]));self.to(4)
        self.play_for(.9,FadeIn(end[6]),FadeIn(end[7]));self.to(9)
    def operations(self):
        self.add(header());old=inclusion_state();self.add(old);g=operation_state(0)
        self.play_for(1.1,FadeOut(old),FadeIn(g))
        self.to(6.5);self.play_for(.7,Indicate(g[3],color=TEAL),Indicate(g[4],color=TEAL));self.to(8)
        ring=operation_state(1)
        # No transforms affect the element array or its region: the set stays fixed.
        self.play_for(1.1,Transform(g[0],ring[0]),Transform(g[1],ring[1]),Transform(g[6],ring[6]))
        self.to(13)
        field=operation_state(2)
        self.play_for(1.7,Transform(g[0],field[0]),Transform(g[1],field[1]),Transform(g[2],field[2]),Transform(g[3],field[3]),Transform(g[6],field[6]),FadeIn(field[5]))
        self.to(16)
    def correspondence(self):
        self.add(header());old=operation_state(2);self.add(old);g=correspondence_state()
        g[0][2].rotate(-3*PI/2,about_point=g[0][2][0].get_center())
        self.play_for(1,FadeOut(old),FadeIn(g[0][:3]));self.to(3)
        self.play_for(.9,FadeIn(g[1][:3]));self.to(7)
        self.play_for(.9,GrowArrow(g[2]),FadeIn(g[3]),FadeIn(g[4]));self.to(10)
        self.play_for(.65,Rotate(g[0][2],PI/2,about_point=g[0][2][0].get_center()))
        self.play_for(1.15,Rotate(g[0][2],PI,about_point=g[0][2][0].get_center()),FadeIn(g[0][3]),FadeIn(g[1][3]));self.to(13)
    def closing(self):
        h=header();g=correspondence_state();self.add(h,g)
        cloud=VGroup(*[math(s,37,c).move_to([x,1.75,0]) for x,s,c in [(-2.7,r'\mathbb Z',BLUE),(-.9,r'\mathbb R[x]',BLUE),(.9,r'\mathbb Q',PURPLE),(2.7,r'\mathbb F_5',PURPLE)]])
        self.play_for(1.1,g[0].animate.scale(.5).move_to([-4.75,.2,0]),g[1].animate.scale(.5).move_to([4.75,.2,0]),FadeOut(g[3:]),FadeIn(cloud));self.to(2)
        rays=VGroup(*[Line([x,1.65,0],[0,.65,0],color=PURPLE,stroke_width=2) for x in [-2.7,-.9,.9,2.7]])
        self.play_for(1.3,FadeOut(g[:2]),FadeOut(cloud),ReplacementTransform(g[2],rays));self.to(4)
        end=closing_state();self.play_for(1.3,FadeOut(rays),FadeOut(h),FadeIn(end[:3],shift=UP*.12));self.to(6)
        self.play_for(.6,FadeIn(end[3]));self.to(7)
