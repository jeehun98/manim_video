"""One shear matrix throughout: exact shape deformation, eigenline and singular lengths."""
import sys,json,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=ROOT.parents[1];sys.path.insert(0,str(WORK))
from manim import *
from longforms.evdsvd01_names.visuals import BattleScene,label,pos,SHORT,BLUE,TEAL,WHITE,MUTED,GOLD
from longforms.evdsvd02_conditions.visuals import matrix
from longforms.evdsvd03_structure.revisions.v2_153s.visuals import arr,grid
ORANGE='#FFB066';PURPLE='#B49AFF'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
CUES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
PROJECT=json.loads((ROOT/'project.json').read_text(encoding='utf-8'))
A=np.array([[1.,2.],[0.,1.]])
SIGMA=np.array([1+np.sqrt(2),np.sqrt(2)-1])
V=np.column_stack(([np.cos(67.5*DEGREES),np.sin(67.5*DEGREES)],[np.cos(-22.5*DEGREES),np.sin(-22.5*DEGREES)]))
U=np.column_stack(([np.cos(22.5*DEGREES),np.sin(22.5*DEGREES)],[np.cos(-67.5*DEGREES),np.sin(-67.5*DEGREES)]))
SQUARE=np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]])

def world():
    o=pos(-.55,-.6) if SHORT else pos(-.4,-.4);s=1. if SHORT else .9
    return dict(o=o,s=s,grid=grid(o,s,bounds=(-2.7,3.3,-1.5,1.5)))

def polygon(w,points,color=BLUE):
    return Polygon(*[w['o']+pos(*(w['s']*v)) for v in points],color=color,stroke_width=3,fill_color=color,fill_opacity=.1)

def original_square(w):
    return DashedVMobject(polygon(w,SQUARE,MUTED).set_fill(opacity=0),num_dashes=28).set_stroke(opacity=.45)

def pair_world():
    s=.86 if SHORT else .73
    ci=pos(-2.,-.45) if SHORT else pos(-3.5,-.15)
    co=pos(1.3,-.45) if SHORT else pos(3.2,-.15)
    axes=VGroup(Line(ci+pos(-1.3*s,0),ci+pos(1.3*s,0),color=MUTED,stroke_opacity=.3),Line(ci+pos(0,-1.3*s),ci+pos(0,1.3*s),color=MUTED,stroke_opacity=.3),Line(co+pos(-2.55*s,0),co+pos(2.55*s,0),color=MUTED,stroke_opacity=.3),Line(co+pos(0,-1.3*s),co+pos(0,1.3*s),color=MUTED,stroke_opacity=.3))
    circle=Circle(radius=s,color=BLUE,stroke_width=2).move_to(ci)
    ellipse=Ellipse(width=2*SIGMA[0]*s,height=2*SIGMA[1]*s,color=TEAL,stroke_width=2).rotate(22.5*DEGREES).move_to(co)
    names=VGroup(label('입력 · 길이 1',ci[0],1.7 if SHORT else 1.3,21,BLUE,3),label('출력',co[0],1.7 if SHORT else 1.3,21,TEAL,3))
    return dict(s=s,ci=ci,co=co,circle=circle,ellipse=ellipse,axes=axes,names=names,base=VGroup(axes,circle,ellipse,names))

def ellipse_at(w):
    return Ellipse(width=2*SIGMA[0]*w['s'],height=2*SIGMA[1]*w['s'],color=TEAL,stroke_width=2).rotate(22.5*DEGREES).move_to(w['o'])

class ValuesScene(BattleScene):
    def setup(self):
        self.spec=MANIFEST[self.INDEX];self.length=self.spec['duration_seconds']
        self.add(label('MATRIX DECOMPOSITION WORLD CUP',y=6.55 if SHORT else 3.55,size=15,color=MUTED,width=7 if SHORT else 12))
        y=5.85 if SHORT else 2.98
        self.add(label('EVD',-1.35,y,29,BLUE,2),label('VS',0,y,17,MUTED,1),label('SVD',1.35,y,29,TEAL,2),Line(pos(-3.5 if SHORT else -6.5,y-.45),pos(3.5 if SHORT else 6.5,y-.45),color=MUTED,stroke_opacity=.22))
        self.score=label('EVD  2 : 1  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)
        self.add(self.score,label('04 / VALUES  ·  같은 행렬, 다른 배율',y=-6.65 if SHORT else -3.65,size=14,color=MUTED,width=7 if SHORT else 12))
        if self.INDEX not in [0,1,16]:
            chip=VGroup(label('A =',x=-.65,size=22,color=MUTED,width=1),matrix([[1,2],[0,1]],MUTED).scale(.47).move_to(pos(.35,0))).move_to(pos(0,3.2) if SHORT else pos(5.25,1.47))
            self.add(chip)
        self.caption=VGroup();self.caption_key=None;self.caption.add_updater(lambda m,dt:self.update_caption());self.add(self.caption);self.update_caption()
    def update_caption(self):
        t=self.spec['start']+self.time+1e-6;cue=next((c for c in CUES if c['start']<=t<c['end']),None)
        key=cue['start'] if cue else None
        if key==self.caption_key:return
        self.caption_key=key;self.caption.remove(*list(self.caption))
        if cue:
            words='\n'.join(textwrap.wrap(cue['caption'],27 if SHORT else 52,break_long_words=False))
            txt=label(words,y=-5.7 if SHORT else -2.98,size=22 if SHORT else 23,width=7.1 if SHORT else 12.5)
            bg=RoundedRectangle(width=7.45 if SHORT else 13,height=max(.65,txt.height+.25),corner_radius=.08,stroke_width=0,fill_color='#080F21',fill_opacity=.97).move_to(txt)
            self.caption.add(bg,txt).set_z_index(100)
    def heading(self,s,color=WHITE):
        m=label(s,y=4.25 if SHORT else 1.98,size=34,color=color,width=7 if SHORT else 9);self.add(m);return m
    def note(self,s,color=MUTED):
        m=label(s,y=-4.2 if SHORT else -2.18,size=22,color=color,width=7 if SHORT else 12);self.reveal(m,d=.2);return m
    def pair_arrows(self,g,v,color):
        return VGroup(arr(g['ci'],v,g['s'],GOLD),arr(g['co'],A@v,g['s'],color,6))
    def axis_lengths(self,g):
        return VGroup(arr(g['co'],SIGMA[0]*U[:,0],g['s'],ORANGE,6),arr(g['co'],SIGMA[1]*U[:,1],g['s'],PURPLE,6))
    def length_label(self,g,index,text):
        color=[ORANGE,PURPLE][index]
        point=g['co']+pos(*(g['s']*SIGMA[index]*U[:,index]))
        center=(pos(g['co'][0],.95) if SHORT else pos(0,.65)) if index==0 else pos(g['co'][0]+.2,-1.75 if SHORT else -1.65)
        number=label(text,center[0],center[1],36,color,width=4)
        leader=Line(point,number.get_bottom() if index==0 else number.get_top(),color=color,stroke_width=1.5,stroke_opacity=.7)
        return VGroup(leader,number)
    def scene_0(self):
        t=label('행렬 분해\n이상형 월드컵!',y=2.4 if SHORT else 1.2,size=40);self.reveal(t)
        self.to(1);self.reveal(self.pair().move_to(pos(0,-.7)),d=.4)
        self.to(3);self.play(FadeOut(t),run_time=.2);self.reveal(label('ROUND 04 · 고윳값 vs 특이값',y=2.8 if SHORT else 1.3,size=30,color=GOLD))
    def scene_1(self):
        self.heading('하나의 행렬을 적용하면',TEAL);w=world();square=polygon(w,SQUARE)
        intro=VGroup(label('A =',x=-1.05,size=32,color=TEAL),matrix([[1,2],[0,1]],TEAL).move_to(pos(.35,0))).move_to(pos(0,2.15) if SHORT else pos(0,1.05))
        self.add(w['grid'],original_square(w),intro);self.reveal(square)
        self.to(2)
        small=VGroup(label('A =',x=-.65,size=22,color=MUTED,width=1),matrix([[1,2],[0,1]],MUTED).scale(.47).move_to(pos(.35,0))).move_to(pos(0,3.2) if SHORT else pos(5.25,1.47))
        self.play(Transform(intro,small),run_time=.4)
        self.play(UpdateFromAlphaFunc(square,lambda m,t:m.become(polygon(w,SQUARE@np.array([[1.,2*t],[0.,1.]]).T,TEAL))),run_time=5)
        self.note('아랫변은 고정 · 윗변은 수평으로 이동',TEAL)
    def scene_2(self):
        self.heading('고윳값이 모두 1인데?',BLUE);w=world()
        self.add(w['grid'],original_square(w),polygon(w,SQUARE@A.T,TEAL))
        self.to(2)
        numbers=label('λ₁ = λ₂ = 1',y=2 if SHORT else .95,size=43,color=BLUE,width=7);self.reveal(numbers)
        self.to(5);self.play(Indicate(numbers,color=GOLD),run_time=.6)
        self.to(6);self.note('같은 고윳값이 두 번 · 독립 고유방향은 수평 하나')
    def scene_3(self):
        self.heading('Av = v',BLUE);w=world()
        shape=polygon(w,SQUARE@A.T,TEAL).set_stroke(opacity=.2).set_fill(opacity=.025)
        self.add(w['grid'],shape)
        line=Line(w['o']+LEFT*1.5*w['s'],w['o']+RIGHT*2.6*w['s'],color=BLUE,stroke_opacity=.5)
        self.to(2);v=arr(w['o'],[1,0],w['s'],BLUE,6);self.reveal(line,v)
        self.to(4);self.play(Indicate(v,color=GOLD),run_time=.8)
        self.note('적용 전과 후의 벡터가 정확히 겹친다',BLUE)
    def scene_4(self):
        self.heading('고유방향에서의 배율 ×1',BLUE);w=world();v=arr(w['o'],[1,0],w['s'],BLUE,6)
        self.add(w['grid'],v)
        self.to(4)
        rays=VGroup(*[arr(w['o'],[np.cos(t),np.sin(t)],w['s'],MUTED,2).set_opacity(.3) for t in [-PI/3,PI/4,PI/2,3*PI/4]])
        self.reveal(rays);self.note('이 숫자만으로 모든 방향의 길이 보존을 뜻하지는 않는다')
    def scene_5(self):
        self.heading('수직 벡터는 어떻게 변할까?',GOLD);w=world()
        previous=DashedLine(w['o'],w['o']+pos(0,w['s']),color=MUTED)
        moving=arr(w['o'],[0,1],w['s'],GOLD,6);self.add(w['grid'],previous,moving)
        self.to(3)
        self.play(UpdateFromAlphaFunc(moving,lambda m,t:m.become(arr(w['o'],[2*t,1],w['s'],GOLD,6))),run_time=2.4)
        self.note('같은 높이로 밀려나며 방향과 길이가 변한다',GOLD)
    def scene_6(self):
        op=self.heading('길이 변화를 어떻게 알 수 있을까?',GOLD);w=world()
        horizontal=arr(w['o'],[1,0],w['s'],BLUE,6);other=arr(w['o'],[2,1],w['s'],GOLD,6)
        self.add(w['grid'],horizontal,other,DashedLine(w['o'],w['o']+pos(0,w['s']),color=MUTED))
        self.reveal(label('길이 유지',x=w['o'][0]+w['s']*.8,y=w['o'][1]-.5,size=22,color=BLUE),label('길이 증가',x=w['o'][0]+w['s']*2.1,y=w['o'][1]+w['s']*1.35,size=22,color=GOLD,width=3))
        self.to(5);self.play(Transform(op,label('특이값',y=4.25 if SHORT else 1.98,size=34,color=TEAL)),run_time=.3)
        self.note('모든 단위 입력 방향의 길이 변화를 살펴보자',TEAL)
    def scene_7(self):
        self.heading('‖x‖ = 1',TEAL);w=world();v=arr(w['o'],[1,0],w['s'],GOLD,5)
        circle=Circle(radius=w['s'],color=BLUE,stroke_width=2).move_to(w['o'])
        self.add(w['grid'],v)
        self.play(Rotate(v,angle=TAU,about_point=w['o']),Create(circle),run_time=2.2,rate_func=linear)
        self.note('모든 입력 방향에서 길이는 1',TEAL)
    def scene_8(self):
        self.heading('같은 행렬 A를 적용',TEAL);w=world();circle=Circle(radius=w['s'],color=BLUE,stroke_width=2).move_to(w['o'])
        ghost=circle.copy().set_stroke(opacity=.25).set_fill(opacity=0)
        points=[np.array([np.cos(t),np.sin(t)]) for t in np.linspace(0,TAU,48,endpoint=False)]
        dots=VGroup(*[Dot(w['o']+pos(*(w['s']*x)),radius=.025,color=GOLD) for x in points])
        self.add(w['grid'],circle,ghost,dots);self.to(1);start=circle.copy()
        def morph(m,t):
            B=np.array([[1.,2*t],[0.,1.]])
            circle.become(start.copy().apply_matrix(B,about_point=w['o']).set_color(TEAL))
            for dot,x in zip(dots,points):dot.move_to(w['o']+pos(*(w['s']*(B@x))))
        self.play(UpdateFromAlphaFunc(dots,morph),run_time=2.4)
    def scene_9(self):
        self.heading('가장 크게 늘어나는 입력 방향',ORANGE);g=pair_world();self.add(g['base'])
        theta0=-22.5*DEGREES;theta1=67.5*DEGREES
        moving=self.pair_arrows(g,V[:,1],ORANGE);self.add(moving)
        def scan(m,t):
            theta=interpolate(theta0,theta1,t);v=np.array([np.cos(theta),np.sin(theta)])
            m.become(self.pair_arrows(g,v,ORANGE))
        self.play(UpdateFromAlphaFunc(moving,scan),run_time=3.2)
        self.to(4);self.reveal(self.length_label(g,0,'2.414배'));self.note('σ₁ = 1 + √2',ORANGE)
    def scene_10(self):
        self.heading('가장 크게 줄어드는 입력 방향',PURPLE);g=pair_world();self.add(g['base'])
        moving=self.pair_arrows(g,V[:,0],PURPLE);self.add(moving)
        def scan(m,t):
            theta=interpolate(67.5*DEGREES,-22.5*DEGREES,t);v=np.array([np.cos(theta),np.sin(theta)])
            m.become(self.pair_arrows(g,v,PURPLE))
        self.play(UpdateFromAlphaFunc(moving,scan),run_time=3.2)
        self.to(4);self.reveal(self.length_label(g,1,'0.414배'));self.note('σ₂ = √2 − 1',PURPLE)
    def scene_11(self):
        self.heading('특이값 = 길이 배율',TEAL);g=pair_world();self.add(g['base'],self.axis_lengths(g))
        self.reveal(self.length_label(g,0,'2.414'),self.length_label(g,1,'0.414'))
        self.note('전체 축이 아니라 원점에서 끝점까지의 반축 길이')
    def scene_12(self):
        self.heading('같은 행렬 · 다른 숫자')
        lo=pos(-2,-.8) if SHORT else pos(-3.7,-.4);ro=pos(1.6,-.8) if SHORT else pos(3,-.4)
        s=.58 if SHORT else .7
        eigen=VGroup(Line(lo+LEFT*.8,lo+RIGHT*1.3,color=BLUE,stroke_opacity=.3),arr(lo,[1,0],s,BLUE,5))
        shape=Ellipse(width=2*SIGMA[0]*s,height=2*SIGMA[1]*s,color=TEAL).rotate(22.5*DEGREES).move_to(ro)
        self.add(eigen,shape)
        self.reveal(label('고윳값',x=lo[0],y=2 if SHORT else 1.2,size=26,color=BLUE,width=3),label('1, 1',x=lo[0],y=.8 if SHORT else .65,size=43,color=BLUE,width=3))
        self.to(2);self.reveal(label('특이값',x=ro[0],y=2 if SHORT else 1.2,size=26,color=TEAL,width=3),label('2.414, 0.414',x=ro[0],y=.8 if SHORT else .65,size=31,color=TEAL,width=4))
        self.note('한 행렬에서 서로 다른 정보를 드러내는 숫자')
    def scene_13(self):
        self.heading('고유직선에서의 배율',BLUE);w=world();v=arr(w['o'],[1,0],w['s'],BLUE,6)
        self.add(w['grid'],Line(w['o']+LEFT*1.6*w['s'],w['o']+RIGHT*2.5*w['s'],color=BLUE,stroke_opacity=.4),v)
        self.play(Indicate(v,color=BLUE),run_time=1)
        self.note('λ = 1  ·  이 고유방향에서는 그대로 유지',BLUE)
    def scene_14(self):
        self.heading('특이방향에서의 길이 배율',TEAL);g=pair_world();self.add(g['base'])
        major=self.pair_arrows(g,V[:,0],ORANGE);minor=self.pair_arrows(g,V[:,1],PURPLE)
        self.reveal(major);self.to(2);self.play(ReplacementTransform(major,minor),run_time=.7)
        self.note('고윳값: 고유방향의 배율 / 특이값: 길이 배율',TEAL)
    def scene_15(self):
        self.heading('ROUND 04 · 고윳값 vs 특이값',GOLD)
        pair=self.pair().move_to(pos(0,1 if SHORT else .1));self.reveal(pair)
        self.to(2);self.reveal(label('SVD 승!',y=-1.3 if SHORT else -1.35,size=53,color=TEAL),d=.2)
        self.play(Circumscribe(pair[2],color=TEAL),run_time=.6)
        self.to(3);self.note('판정 기준: 한 번의 변환에서 길이 변화를 직접 드러냄',GOLD)
    def scene_16(self):
        self.heading('ROUND 04 WINNER · SVD',TEAL)
        score=label('EVD   2 : 1   SVD',y=.6 if SHORT else 0,size=45);self.reveal(score)
        self.to(1);self.play(Transform(score,label('EVD   2 : 2   SVD',y=.6 if SHORT else 0,size=45,color=GOLD)),Transform(self.score,label('EVD  2 : 2  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)),run_time=.5)
        self.to(CUES[-1]['start']-98);self.reveal(label('다시 동점!',y=-1.8 if SHORT else -1.5,size=45,color=TEAL),d=.2)
