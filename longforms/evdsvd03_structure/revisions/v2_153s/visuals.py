"""Animation-first revision: persistent coordinate geometry, no numeric calculations onscreen."""
import sys,json,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=next(p for p in ROOT.parents if (p/'scripts/render.py').exists());sys.path.insert(0,str(WORK))
from manim import *
from longforms.evdsvd01_names.visuals import BattleScene,label,pos,SHORT,BLUE,TEAL,WHITE,MUTED,GOLD,PANEL
PURPLE='#B49AFF';GREEN='#A4EBA0'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
CUES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
def rotation(a):return np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
P=np.array([[1.,1.],[0.,-1.]])
AE=np.array([[2.,1.],[0.,1.]])
V=rotation(25*DEGREES);U=rotation(30*DEGREES);SIGMA=np.diag([2.,1.]);AS=U@SIGMA@V.T
XE=np.array([2.,-1.]);YE=AE@XE
CS=np.array([1.15,-.75]);XS=V@CS;SCALED=SIGMA@CS;YS=AS@XS

def arr(o,v,s=1,color=GOLD,width=5):
    return Arrow(o,o+pos(*(np.asarray(v)*s)),buff=0,color=color,stroke_width=width,max_tip_length_to_length_ratio=.14)

def clip_line(a,b,bounds=(-1.3,3.5,-2.,1.45)):
    a=np.asarray(a,dtype=float);b=np.asarray(b,dtype=float);d=b-a;lo=0.;hi=1.
    for k,mn,mx in [(0,bounds[0],bounds[1]),(1,bounds[2],bounds[3])]:
        if abs(d[k])<1e-9:
            if not mn<=a[k]<=mx:return None
        else:
            p,q=sorted([(mn-a[k])/d[k],(mx-a[k])/d[k]]);lo=max(lo,p);hi=min(hi,q)
    return (a+lo*d,a+hi*d) if lo<=hi else None

def grid(o,s,basis=np.eye(2),bounds=(-1.3,3.5,-2.,1.45)):
    g=VGroup()
    for k in range(-5,6):
        for a,b in [(basis@np.array([k,-6.]),basis@np.array([k,6.])),(basis@np.array([-6.,k]),basis@np.array([6.,k]))]:
            clipped=clip_line(a,b,bounds)
            if clipped:
                c,d=clipped;g.add(Line(o+pos(*(s*c)),o+pos(*(s*d)),color=MUTED,stroke_width=1,stroke_opacity=.17))
    return g

def eigen_world(o=None,s=None):
    o=o if o is not None else (pos(-1.15,-.3) if SHORT else pos(-1.2,-.15))
    s=s if s is not None else (1.1 if SHORT else 1.)
    normal=grid(o,s);oblique=grid(o,s,P)
    axes=VGroup(Line(o+pos(-1.1*s,0),o+pos(3.3*s,0),color=BLUE,stroke_opacity=.6),Line(o+pos(-.8*s,.8*s),o+pos(1.8*s,-1.8*s),color=PURPLE,stroke_opacity=.6))
    basis=VGroup(arr(o,P[:,0],s,BLUE,4),arr(o,P[:,1],s,PURPLE,4))
    return dict(o=o,s=s,normal=normal,oblique=oblique,axes=axes,basis=basis)

def components(o,s,basis,coeffs):
    a=basis[:,0]*coeffs[0];b=basis[:,1]*coeffs[1]
    return VGroup(arr(o,a,s,BLUE,5),arr(o+pos(*(s*a)),b,s,PURPLE,5))

def pair_world():
    s=1. if SHORT else .77
    ci=pos(-1.85,-.35) if SHORT else pos(-3.4,-.15)
    co=pos(1.65,-.35) if SHORT else pos(3.25,-.15)
    axes=VGroup(Line(ci+pos(-1.25*s,0),ci+pos(1.25*s,0),color=MUTED,stroke_opacity=.25),Line(ci+pos(0,-1.25*s),ci+pos(0,1.25*s),color=MUTED,stroke_opacity=.25),Line(co+pos(-2.1*s,0),co+pos(2.1*s,0),color=MUTED,stroke_opacity=.25),Line(co+pos(0,-1.6*s),co+pos(0,1.6*s),color=MUTED,stroke_opacity=.25))
    circle=Circle(radius=s,color=BLUE,stroke_width=2).move_to(ci)
    ellipse=Ellipse(width=4*s,height=2*s,color=TEAL,stroke_width=2).rotate(30*DEGREES).move_to(co)
    names=VGroup(label('입력',ci[0],2.05 if SHORT else 1.4,23,BLUE,2.5),label('출력',co[0],2.05 if SHORT else 1.4,23,TEAL,2.5))
    return dict(s=s,ci=ci,co=co,axes=axes,circle=circle,ellipse=ellipse,names=names,base=VGroup(axes,circle,ellipse,names))

def unit_label(s,o,v,scale,color,offset=None):
    p=o+pos(*(np.asarray(v)*scale*1.18))+(offset if offset is not None else ORIGIN)
    return label(s,p[0],p[1],23,color,1.5)

def right_angle(o,a,b,size,color=WHITE):
    return VMobject(color=color,stroke_width=2).set_points_as_corners([o+pos(*(size*a)),o+pos(*(size*(a+b))),o+pos(*(size*b))])

def singular_world():
    o=pos(-.5,-.45) if SHORT else pos(-.5,-.25)
    s=1.25 if SHORT else 1.1
    normal=grid(o,s,bounds=(-2.,2.7,-1.6,1.4))
    axes=VGroup(Line(o-pos(*(s*2*V[:,0])),o+pos(*(s*2.45*V[:,0])),color=BLUE,stroke_opacity=.5),Line(o-pos(*(s*1.4*V[:,1])),o+pos(*(s*1.4*V[:,1])),color=PURPLE,stroke_opacity=.5))
    basis=VGroup(arr(o,V[:,0],s,BLUE,3),arr(o,V[:,1],s,PURPLE,3))
    return dict(o=o,s=s,normal=normal,axes=axes,basis=basis)

class GraphStructure(BattleScene):
    def setup(self):
        self.spec=MANIFEST[self.INDEX];self.length=self.spec['duration_seconds']
        self.add(label('MATRIX DECOMPOSITION WORLD CUP',y=6.55 if SHORT else 3.55,size=15,color=MUTED,width=7 if SHORT else 12))
        y=5.85 if SHORT else 2.98
        self.add(label('EVD',-1.35,y,29,BLUE,2),label('VS',0,y,17,MUTED,1),label('SVD',1.35,y,29,TEAL,2),Line(pos(-3.5 if SHORT else -6.5,y-.45),pos(3.5 if SHORT else 6.5,y-.45),color=MUTED,stroke_opacity=.22))
        self.score=label('EVD  1 : 1  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)
        self.add(self.score,label('03 / STRUCTURE  ·  하나의 기저, 두 직교기저',y=-6.65 if SHORT else -3.65,size=14,color=MUTED,width=7 if SHORT else 12))
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
        m=label(s,y=4.2 if SHORT else 1.96,size=35,color=color,width=7 if SHORT else 12);self.add(m);return m
    def note(self,s,color=MUTED):
        m=label(s,y=-4.15 if SHORT else -2.18,size=22,color=color,width=7 if SHORT else 12);self.reveal(m,d=.2);return m
    def first_pair(self,g,unit=False):
        a=arr(g['ci'],V[:,0],g['s'],BLUE)
        out=arr(g['co'],AS@V[:,0],g['s'],GOLD)
        group=VGroup(a,out,unit_label('v₁',g['ci'],V[:,0],g['s'],BLUE))
        if unit:group.add(arr(g['co'],U[:,0],g['s'],TEAL,7),unit_label('u₁',g['co'],U[:,0],g['s'],TEAL,DOWN*.25))
        return group
    def both_pairs(self,g):
        first=self.first_pair(g,True)
        second=VGroup(arr(g['ci'],V[:,1],g['s'],PURPLE),arr(g['co'],AS@V[:,1],g['s'],GREEN),unit_label('v₂',g['ci'],V[:,1],g['s'],PURPLE),unit_label('u₂',g['co'],U[:,1],g['s'],GREEN))
        return VGroup(first,second)
    def overlay(self):
        w=singular_world();o=w['o'];s=w['s']
        group=VGroup()
        for i in range(2):
            vc=[BLUE,PURPLE][i];uc=[TEAL,GREEN][i]
            group.add(DashedLine(o-pos(*(s*1.15*V[:,i])),o+pos(*(s*1.3*V[:,i])),color=vc,stroke_opacity=.65),arr(o,V[:,i],s,vc,3),arr(o,U[:,i],s,uc,5))
            group.add(unit_label('v₁' if i==0 else 'v₂',o,V[:,i],s,vc,DOWN*.2),unit_label('u₁' if i==0 else 'u₂',o,U[:,i],s,uc,UP*.25))
            group.add(Arc(radius=s*.8,start_angle=(25+90*i)*DEGREES,angle=5*DEGREES,color=GOLD,stroke_width=8).shift(o))
        group.add(right_angle(o,V[:,0],V[:,1],.24*s,BLUE),right_angle(o,U[:,0],U[:,1],.43*s,TEAL))
        return group
    def scene_0(self):
        t=label('행렬 분해\n이상형 월드컵!',y=2.4 if SHORT else 1.2,size=40);self.reveal(t)
        self.to(1);cards=self.pair().move_to(pos(0,-.7));self.reveal(cards,d=.4)
        self.to(3);self.play(FadeOut(t),run_time=.2);self.reveal(label('ROUND 03 · 분해 구조',y=2.8 if SHORT else 1.3,size=32,color=GOLD))
    def scene_1(self):
        self.heading('A = PDP⁻¹',BLUE);w=eigen_world();self.add(w['normal'])
        self.to(2);self.note('왜 이런 구조가 만들어질까?',BLUE)
        self.play(ShowPassingFlash(Line(pos(1,3.6 if SHORT else 1.5),pos(-1,3.6 if SHORT else 1.5),color=GOLD)),run_time=1)
    def scene_2(self):
        self.heading('Apᵢ = λᵢpᵢ',BLUE);w=eigen_world();self.add(w['normal'],w['axes'])
        self.reveal(w['basis'],d=.4)
        self.add(unit_label('p₁',w['o'],P[:,0],w['s'],BLUE),unit_label('p₂',w['o'],P[:,1],w['s'],PURPLE))
        self.to(3);ghost=arr(w['o'],P[:,0],w['s'],GOLD);self.add(ghost)
        self.play(Transform(ghost,arr(w['o'],AE@P[:,0],w['s'],GOLD)),run_time=3)
        self.to(7);self.play(Indicate(w['basis'][1],color=PURPLE),run_time=.7)
        self.to(10);self.play(FadeOut(ghost),run_time=.3)
        self.note('원래 직선에 머문다 · 음의 고윳값에서는 반전 가능')
    def scene_3(self):
        self.heading('P⁻¹',BLUE);w=eigen_world();self.add(w['normal'],w['axes'],w['basis'])
        x=arr(w['o'],XE,w['s'],GOLD);self.add(x)
        self.play(ReplacementTransform(w['normal'],w['oblique']),run_time=2)
        self.note('벡터는 그대로 · 좌표 표현만 바뀐다',GOLD)
    def scene_4(self):
        op=self.heading('D',GOLD);w=eigen_world();back=w['normal'].copy()
        x=arr(w['o'],XE,w['s'],GOLD);self.add(w['oblique'],w['axes'],w['basis'],x)
        comp=components(w['o'],w['s'],P,[1,1]);self.reveal(comp,d=.5)
        self.to(2)
        self.play(Transform(comp,components(w['o'],w['s'],P,[2,1])),Transform(x,arr(w['o'],YE,w['s'],GOLD)),run_time=2.6)
        self.to(5);self.play(ReplacementTransform(w['oblique'],back),Transform(op,label('P',y=4.2 if SHORT else 1.96,size=35,color=BLUE)),run_time=1.4)
        self.to(8);self.play(Transform(op,label('P⁻¹ → D → P',y=4.2 if SHORT else 1.96,size=35,color=BLUE)),run_time=.3)
        self.note('같은 고유방향으로 나누고, 늘리고, 다시 조합')
    def scene_5(self):
        self.heading('P⁻¹',BLUE);w=eigen_world();x=arr(w['o'],YE,w['s'],GOLD)
        self.add(w['normal'],w['axes'],w['basis'],x)
        self.note('고유기저의 두 축은 직교하지 않아도 된다',PURPLE)
        self.to(4)
        feet=[P[:,i]*(YE@P[:,i])/(P[:,i]@P[:,i]) for i in range(2)]
        naive=VGroup(*[DashedLine(w['o']+pos(*(w['s']*YE)),w['o']+pos(*(w['s']*f)),color=MUTED,stroke_opacity=.6) for f in feet],*[arr(w['o'],f,w['s'],MUTED,2).set_opacity(.5) for f in feet])
        self.reveal(naive);self.to(6)
        self.play(FadeOut(naive),FadeOut(w['normal']),FadeIn(w['oblique']),run_time=.7)
        comp=components(w['o'],w['s'],P,[2,1]);self.reveal(comp)
        self.to(8);self.play(Indicate(comp,color=GOLD),run_time=.6)
    def scene_6(self):
        self.heading('하나의 고유기저',BLUE)
        s=.57 if SHORT else .65
        a=eigen_world(pos(-2.4,-.3) if SHORT else pos(-3.6,-.2),s)
        b=eigen_world(pos(1.1,-.3) if SHORT else pos(2.5,-.2),s)
        self.add(a['oblique'],a['axes'],a['basis'],arr(a['o'],XE,s,GOLD),b['oblique'],b['axes'],b['basis'],arr(b['o'],YE,s,GOLD))
        self.note('변환 전과 후에 같은 고유방향을 사용',BLUE)
    def scene_7(self):
        self.heading('SVD',TEAL)
        o=pos(0,-.3) if SHORT else pos(0,-.2);s=1.25 if SHORT else 1.
        g=grid(o,s,bounds=(-2.5,2.5,-1.7,1.5));self.add(g)
        self.to(3)
        circle=Circle(radius=s,color=BLUE).move_to(o);ghost=circle.copy().set_stroke(opacity=.2).set_fill(opacity=0)
        angles=np.linspace(0,TAU,48,endpoint=False);points=[np.array([np.cos(t),np.sin(t)]) for t in angles]
        dots=VGroup(*[Dot(o+pos(*(s*x)),radius=.025,color=GOLD) for x in points])
        self.reveal(circle,ghost,dots,d=.3);self.to(6)
        start=circle.copy()
        def morph(m,alpha):
            B=(1-alpha)*np.eye(2)+alpha*AS
            circle.become(start.copy().apply_matrix(B,about_point=o).set_color(TEAL))
            for dot,x in zip(dots,points):dot.move_to(o+pos(*(s*(B@x))))
        self.play(UpdateFromAlphaFunc(dots,morph),run_time=2.4,rate_func=smooth)
        self.note('단위원 → 선형변환 → 타원',TEAL)
    def scene_8(self):
        self.heading('어떤 입력 방향이 긴 축을 만들까?',TEAL);g=pair_world()
        o=pos(0,-.3) if SHORT else pos(0,-.2);s=1.25 if SHORT else 1.
        ellipse=Ellipse(width=4*s,height=2*s,color=TEAL).rotate(30*DEGREES).move_to(o)
        circle=Circle(radius=s,color=BLUE,stroke_opacity=.2).move_to(o)
        self.add(ellipse,circle)
        self.play(Transform(ellipse,g['ellipse']),Transform(circle,g['circle']),FadeIn(g['axes']),FadeIn(g['names']),run_time=.8)
        start=115*DEGREES;end=25*DEGREES
        arrows=VGroup(arr(g['ci'],V[:,1],g['s'],GOLD),arr(g['co'],AS@V[:,1],g['s'],GOLD))
        self.reveal(arrows,d=.2)
        def scan(m,alpha):
            theta=interpolate(start,end,alpha);v=np.array([np.cos(theta),np.sin(theta)])
            m.become(VGroup(arr(g['ci'],v,g['s'],GOLD),arr(g['co'],AS@v,g['s'],GOLD)))
        self.play(UpdateFromAlphaFunc(arrows,scan),run_time=2.6)
        self.to(4);self.play(Transform(arrows[0],arr(g['ci'],V[:,0],g['s'],BLUE)),run_time=.3)
        self.reveal(unit_label('v₁',g['ci'],V[:,0],g['s'],BLUE));self.note('SVD가 찾아내는 입력 방향',BLUE)
    def scene_9(self):
        op=self.heading('v₁ → u₁',TEAL);g=pair_world();first=self.first_pair(g);self.add(g['base'],first)
        self.to(4)
        unit=arr(g['co'],U[:,0],g['s'],TEAL,7);ul=unit_label('u₁',g['co'],U[:,0],g['s'],TEAL,DOWN*.25)
        self.reveal(unit,ul)
        self.to(10)
        perpendicular=np.array([-U[1,0],U[0,0]])*.22
        a=g['co']+pos(*(g['s']*perpendicular));b=a+pos(*(g['s']*2*U[:,0]))
        measure=VGroup(DashedLine(a,b,color=GOLD),Line(a-pos(*(g['s']*.09*perpendicular/.22)),a+pos(*(g['s']*.09*perpendicular/.22)),color=GOLD),Line(b-pos(*(g['s']*.09*perpendicular/.22)),b+pos(*(g['s']*.09*perpendicular/.22)),color=GOLD))
        self.reveal(measure,label('σ₁',x=(a[0]+b[0])/2-.25,y=(a[1]+b[1])/2+.3,size=25,color=GOLD,width=1))
        self.to(15);self.play(Transform(op,label('Av₁ = σ₁u₁',y=4.2 if SHORT else 1.96,size=35,color=TEAL)),run_time=.3)
        self.note('단위방향 u₁과 실제 출력의 길이는 다르다',TEAL)
    def scene_10(self):
        self.heading('두 번째 입력 특이방향',TEAL);g=pair_world();first=self.first_pair(g,True);self.add(g['base'],first)
        moving=VGroup(arr(g['ci'],V[:,0],g['s'],PURPLE),arr(g['co'],AS@V[:,0],g['s'],GOLD));self.add(moving)
        def turn(m,alpha):
            theta=(25+90*alpha)*DEGREES;v=np.array([np.cos(theta),np.sin(theta)])
            m.become(VGroup(arr(g['ci'],v,g['s'],PURPLE),arr(g['co'],AS@v,g['s'],GOLD)))
        self.play(UpdateFromAlphaFunc(moving,turn),run_time=1.7)
        self.to(2);self.play(Transform(moving[1],arr(g['co'],U[:,1],g['s'],GREEN)),run_time=.3)
        self.reveal(unit_label('v₂',g['ci'],V[:,1],g['s'],PURPLE),unit_label('u₂',g['co'],U[:,1],g['s'],GREEN))
        self.note('두 번째 입력 방향은 타원의 짧은 축에 대응',GREEN)
    def scene_11(self):
        self.heading('입력도 직교 · 출력도 직교',TEAL);g=pair_world();pairs=self.both_pairs(g);self.add(g['base'],pairs)
        self.to(2)
        angles=VGroup(right_angle(g['ci'],V[:,0],V[:,1],.2*g['s']),right_angle(g['co'],U[:,0],U[:,1],.2*g['s']))
        self.reveal(angles);self.to(7)
        overlay=self.overlay()
        self.play(FadeOut(g['base']),ReplacementTransform(pairs,overlay),FadeOut(angles),run_time=1.2)
        self.note('각각 정규직교 · 같은 기저일 필요는 없다',GOLD)
    def scene_12(self):
        self.heading('Vᵀx',TEAL);w=singular_world();x=arr(w['o'],XS,w['s'],GOLD)
        self.add(w['normal'],w['axes'],w['basis'],x)
        a=CS[0]*V[:,0];b=CS[1]*V[:,1]
        self.to(3)
        projection1=DashedLine(w['o']+pos(*(w['s']*XS)),w['o']+pos(*(w['s']*a)),color=BLUE,stroke_opacity=.7)
        part1=arr(w['o'],a,w['s'],BLUE);self.reveal(projection1,part1)
        self.to(6)
        projection2=DashedLine(w['o']+pos(*(w['s']*XS)),w['o']+pos(*(w['s']*b)),color=PURPLE,stroke_opacity=.7)
        part2=arr(w['o'],b,w['s'],PURPLE);self.reveal(projection2,part2)
        self.to(9);self.play(Transform(part2,arr(w['o']+pos(*(w['s']*a)),b,w['s'],PURPLE)),run_time=1)
        self.to(12);self.note('특이기저의 좌표 추출 · 부호를 가진 성분',TEAL)
    def scene_13(self):
        self.heading('Σ',GOLD);w=singular_world();comp=components(w['o'],w['s'],V,CS)
        ghost=arr(w['o'],XS,w['s'],GOLD).set_opacity(.25)
        self.add(w['normal'],w['axes'],w['basis'],ghost,comp)
        self.play(Transform(comp,components(w['o'],w['s'],V,SCALED)),run_time=1.8)
        self.note('성분별 길이 변화 · 아직 출력 기저로 옮기기 전',GOLD)
    def scene_14(self):
        op=self.heading('U',TEAL);w=singular_world();comp=components(w['o'],w['s'],V,SCALED)
        ghost=arr(w['o'],XS,w['s'],GOLD).set_opacity(.25)
        self.add(w['normal'],w['axes'],ghost,comp)
        new_axes=VGroup(Line(w['o']-pos(*(w['s']*2*U[:,0])),w['o']+pos(*(w['s']*2.45*U[:,0])),color=TEAL,stroke_opacity=.6),Line(w['o']-pos(*(w['s']*1.4*U[:,1])),w['o']+pos(*(w['s']*1.4*U[:,1])),color=GREEN,stroke_opacity=.6))
        target=components(w['o'],w['s'],U,SCALED);target[0].set_color(TEAL);target[1].set_color(GREEN)
        self.play(Transform(w['axes'],new_axes),Transform(comp,target),run_time=2.3)
        self.to(3);self.reveal(arr(w['o'],YS,w['s'],GOLD),d=.3)
        self.to(5);self.play(Transform(op,label('A = UΣVᵀ',y=4.2 if SHORT else 1.96,size=35,color=TEAL)),run_time=.3)
        self.note('입력 좌표 추출 → 길이 변화 → 출력 조합',TEAL)
    def scene_15(self):
        self.heading('하나의 고유기저 vs 두 직교기저')
        eo=pos(-2.2,-.35) if SHORT else pos(-4,-.2);so=pos(1.65,-.35) if SHORT else pos(3,-.2)
        s=.6 if SHORT else .75;ev=eigen_world(eo,s)
        self.add(ev['axes'],ev['basis'],arr(eo,XE,s,GOLD).set_opacity(.35),arr(eo,YE,s,GOLD))
        sg=VGroup(arr(so,V[:,0],1.,BLUE,3),arr(so,V[:,1],1.,PURPLE,3),arr(so,U[:,0],1.,TEAL,5),arr(so,U[:,1],1.,GREEN,5))
        self.add(sg,label('EVD',x=eo[0]+.5,y=2 if SHORT else 1.2,size=30,color=BLUE),label('SVD',x=so[0],y=2 if SHORT else 1.2,size=30,color=TEAL))
        self.play(Indicate(ev['axes'],color=GOLD),run_time=1)
        self.to(3);self.play(Indicate(sg,color=GOLD),run_time=1)
        self.note('같은 고유방향 / 서로 다른 입력·출력 직교방향',GOLD)
    def scene_16(self):
        self.heading('ROUND 03 · 분해 구조',GOLD)
        eo=pos(-2.2,-.35) if SHORT else pos(-4,-.2);so=pos(1.65,-.35) if SHORT else pos(3,-.2)
        ev=eigen_world(eo,.6 if SHORT else .75)
        other=VGroup(arr(so,V[:,0],1.,BLUE,3),arr(so,V[:,1],1.,PURPLE,3),arr(so,U[:,0],1.,TEAL,5),arr(so,U[:,1],1.,GREEN,5))
        self.add(ev['axes'],ev['basis'],other,label('EVD',x=eo[0]+.5,y=2 if SHORT else 1.2,size=30,color=BLUE),label('SVD',x=so[0],y=2 if SHORT else 1.2,size=30,color=TEAL))
        self.to(2);self.play(*[m.animate.set_color(GOLD) for m in ev['axes']],run_time=.3)
        self.reveal(label('EVD 승!',y=-2.7 if SHORT else -1.55,size=44,color=BLUE),d=.2)
        self.to(3);self.note('취향 판정 · 하나의 고유기저라는 구조적 간결함',GOLD)
    def scene_17(self):
        self.heading('ROUND 03 WINNER · EVD',BLUE)
        score=label('EVD   1 : 1   SVD',y=.6 if SHORT else 0,size=45);self.reveal(score)
        self.to(1);self.play(Transform(score,label('EVD   2 : 1   SVD',y=.6 if SHORT else 0,size=45,color=GOLD)),Transform(self.score,label('EVD  2 : 1  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)),run_time=.5)
        self.to(3);self.reveal(label('EVD 리드!',y=-1.8 if SHORT else -1.5,size=45,color=BLUE),d=.2)
