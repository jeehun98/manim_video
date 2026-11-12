"""Persistent tier-board stage, exact narration, nine vector experiment modules."""
import json,os
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,FONT
from quantum_series.shared.components import radiance,H,C,K,wave
from longforms.qcs01_speed.direction import QCSScene

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
config.frame_width,config.frame_height=9,16
config.pixel_width,config.pixel_height=(360,640) if os.getenv('QCS_PREVIEW')=='1' else (1080,1920)
config.frame_rate=60
config.background_color='#0E131E'
INK,BLUE,GREEN,GOLD,RED,MUTED='#F0F3FA','#76CDF2','#77C5AE','#F4D177','#EF7C84','#96A5BE'
TIER_COLORS={'S':'#E16B78','A':'#EFB565','B':'#E9D16B','C':'#91BDAD'}
ROWS={t:6.3-i*.62 for i,t in enumerate('SABC')}
DOCK_X=np.linspace(-3.65,3.65,9)

def label(s,x=0,y=0,size=28,color=INK,width=7.5):return text(s,x,y,size,color,width)
def eq(s,x=0,y=0,size=36,color=INK,width=7.2):
    o=MathTex(s,font_size=size*1.3,color=color)
    if o.width>width:o.scale_to_fit_width(width)
    return o.move_to(p(x,y))
def box(s,x=0,y=0,w=6,h=.9,color=BLUE,size=26):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,stroke_color=color,stroke_width=1.5,fill_color=color,fill_opacity=.07),label(s,size=size,color=color,width=w-.25)).move_to(p(x,y))
def graph(fn,xmin=-3,xmax=3,y=.2,amp=1,width=6,color=BLUE):
    xs=np.linspace(xmin,xmax,161);ys=np.asarray(fn(xs))
    return VMobject(stroke_color=color,stroke_width=3).set_points_as_corners(np.column_stack(((xs-xmin)/(xmax-xmin)*width-width/2,y+amp*ys,np.zeros(len(xs)))))
def icon(i,color=BLUE):
    if i==0:return VGroup(Circle(radius=.3,color=color),wave(.8,.16,1,color))
    if i==1:return VGroup(Line(p(.1,-.35),p(.1,.35),color=color),Arrow(p(-.5,.2),p(.05,0),buff=.01,color=color),Dot(p(.45,.2),color=color,radius=.07))
    if i==2:return VGroup(*[Line(p(-.4,y),p(.4,y),color=color) for y in [-.3,0,.3]],Arrow(p(0,-.25),p(0,.25),buff=0,color=color))
    if i==3:return VGroup(Line(p(-.5,0),p(0,0),color=color),Line(p(0,0),p(.5,.3),color=color),Line(p(0,0),p(.5,-.3),color=color))
    if i==4:return VGroup(Arrow(p(-.5,0),p(0,0),buff=0,color=color),Arrow(p(0,0),p(.4,.35),buff=0,color=color),Arrow(p(0,0),p(.4,-.3),buff=0,color=GOLD))
    if i==5:return VGroup(*[Dot(p(x,y),radius=.045,color=color) for x in [-.25,0,.25] for y in [-.25,0,.25]])
    if i==6:return VGroup(*[Line(p(0,a),p(0,b),color=color,stroke_width=5) for a,b in [(-.4,-.16),(-.06,.06),(.16,.4)]],Line(p(.45,-.4),p(.45,.4),color=color))
    if i==7:return VGroup(Dot(p(-.35,0),radius=.1,color=color),Dot(p(.35,0),radius=.1,color=color),Line(p(-.25,0),p(.25,0),color=color))
    return VGroup(Line(p(-.45,0),p(0,.25),color=color),Line(p(-.45,0),p(0,-.25),color=color),Line(p(0,.25),p(.45,0),color=color),Line(p(0,-.25),p(.45,0),color=color))
def tiercard(i):
    e=DATA['experiments'][i];t=e['tier'];slot=sum(x['tier']==t for x in DATA['experiments'][:i])
    x=-2.2+slot*2.35
    card=box(e['short'],x=x,y=ROWS[t],w=2.24,h=.48,color=TIER_COLORS[t],size=19)
    return card
def density(y):return np.exp(-y*y/3.4)*(1+np.cos(8*y))/2

class TierScene(QCSScene):
    data=DATA
    def setup(self):
        self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.always_update_mobjects=True
        self.caption_records=[];self.caption_index=-2;self.chrome=[]
        self.add(label('QUANTUM EXPERIMENTS',x=-1.9,y=7.4,size=21,width=4.2),label('1900 — 1992',x=3,y=7.4,size=17,color=MUTED,width=2))
        self.add(RoundedRectangle(width=8.45,height=2.65,corner_radius=.16,stroke_width=0,fill_color='#1D2737',fill_opacity=1).move_to(p(0,5.38)))
        for t in 'SABC':
            self.add(RoundedRectangle(width=7.4,height=.5,corner_radius=.06,stroke_width=0,fill_color='#2A3548',fill_opacity=1).move_to(p(.35,ROWS[t])),box(t,x=-3.78,y=ROWS[t],w=.55,h=.5,color=TIER_COLORS[t],size=25))
        self.add(label('티어는 이 영상의 평가 · 개념적 전환과 고전 설명의 한계',y=3.83,size=15,color=MUTED))
        stage=RoundedRectangle(width=8.45,height=9.45,corner_radius=.16,stroke_width=0,fill_color='#192435',fill_opacity=1).move_to(p(0,-1.1));self.add(stage)
        self.dock=[]
        names=['열','빛','준위','자석','산란','회절','슬릿','얽힘','지우개']
        for i,x in enumerate(DOCK_X):
            tile=RoundedRectangle(width=.82,height=.93,corner_radius=.08,stroke_color='#46546B',stroke_width=1,fill_color='#243044',fill_opacity=1).move_to(p(x,-6.55))
            symbol=icon(i).scale(.4).move_to(p(x,-6.4));symbol.set_opacity(.4)
            dock=VGroup(tile,symbol,label(names[i],x=x,y=-6.87,size=16,width=.75));self.add(dock);self.dock.append(dock)
        self.add(label('9 EXPERIMENTS · CHRONOLOGICAL ORDER',y=-7.38,size=14,color=MUTED))
        for i in range(max(0,self.shot-1)):self.add(tiercard(i));self.dock[i].set_opacity(.35)
        self.chrome=list(self.mobjects)
        self.caption=VGroup().set_z_index(40)
        self.caption_panel=Rectangle(width=8.05,height=1.95,stroke_width=0,fill_color='#192435',fill_opacity=1).move_to(p(0,-4.65)).set_z_index(39)
        self.add(self.caption_panel,self.caption);self.update_caption(self.caption);self.caption.add_updater(self.update_caption)
        if self.shot:
            e=DATA['experiments'][self.shot-1]
            self.add(label(str(e['year']),y=3.25,size=22,color=BLUE),label(e['name'],y=2.65,size=35,width=7.6))
    def update_caption(self,mob,dt=0):
        now=self.offset+self.time
        index=bisect_right([s['start'] for s in DATA['sentences']],now+1e-7)-1
        if index==self.caption_index:return
        self.caption_index=index;s=DATA['sentences'][index]['text'];lines=[];line=''
        for w in s.split():
            if line and len(line)+len(w)+1>27:lines.append(line);line=w
            else:line=(line+' '+w).strip()
        o=Text('\n'.join(lines+[line]),font=FONT,font_size=28,line_spacing=1.05,color=INK)
        if o.width>7.6:o.scale_to_fit_width(7.6)
        if o.height>1.65:o.scale_to_fit_height(1.65)
        o.move_to(p(0,-4.65));assert o.get_top()[1]<-3.7 and o.get_bottom()[1]>-5.6
        self.caption_records.append(dict(sentence=index+1,at=round(now,6),width=o.width,height=o.height,lines=len(lines)+1))
        mob.become(o).set_z_index(40)
    def update_mobjects(self,dt):
        super().update_mobjects(dt)
        for o in self.mobjects:
            if o.width<.001 or o.height<.001:continue
            assert o.get_left()[0]>=-4.39 and o.get_right()[0]<=4.39,('x',self.shot,self.time)
            assert o.get_bottom()[1]>=-7.8 and o.get_top()[1]<=7.9,('y',self.shot,self.time)
            if any(o is x for x in self.chrome) or o is self.caption or o is self.caption_panel:continue
            if not getattr(self,'transferring',False):
                assert o.get_bottom()[1]>=-3.6,('subtitle overlap',self.shot,self.time)
    def construct(self):
        getattr(self,f's{self.shot+1:02}')();self.to(self.info['end']);self.caption.remove_updater(self.update_caption)
        audit=Path(os.environ['QCS_AUDIT_DIR']);audit.mkdir(parents=True,exist_ok=True)
        (audit/(self.info['id']+'.json')).write_text(json.dumps(self.caption_records),encoding='utf-8')
    def note(self,s,color=MUTED):
        if hasattr(self,'footnote'):self.remove(self.footnote)
        self.footnote=label(s,y=-3.05,size=19,color=color,width=7.7);self.show(self.footnote,run_time=.25)
    def begin(self):
        i=self.shot-1;self.dock[i].set_opacity(1)
        self.play(Indicate(self.dock[i],color=BLUE,scale_factor=1.1),run_time=.3)
        self.active_icon=icon(i).scale(1.6).move_to(p(0,.4))
        # The thumbnail travels behind the opaque caption panel, never over its text.
        self.transferring=True
        self.play(TransformFromCopy(self.dock[i][1],self.active_icon),run_time=.45)
        self.transferring=False
        self.play(FadeOut(self.active_icon),run_time=.2)
    def grade(self):
        i=self.shot-1;e=DATA['experiments'][i];self.to(e['grade'])
        target=tiercard(i);large=box(e['tier'],x=3.2,y=1.85,w=.9,h=.85,color=TIER_COLORS[e['tier']],size=44)
        token=icon(i).move_to(p(0,.2))
        self.play(FadeIn(large),TransformFromCopy(token,target),run_time=.65)
        self.dock[i].set_opacity(.35)
    def s01(self):
        self.show(label('양자역학\n티어리스트',y=.75,size=56,color=BLUE))
        self.to(1);self.show(label('9개의 실험 · 역사적 순서',y=-1.25,size=30),label('개념적 전환과 고전 설명의 한계',y=-2.2,size=23,color=MUTED))
    def s02(self):
        self.begin();hot=Circle(radius=.45,color=GOLD,fill_color=GOLD,fill_opacity=.7).move_to(p(-2.9,1.25));self.show(hot)
        self.to(7)
        ax=Axes(x_range=[.2,5,1],y_range=[0,1.3,.5],x_length=5.5,y_length=2.5,tips=False,axis_config={'stroke_width':1,'color':MUTED}).move_to(p(.6,.5))
        temp=5000;peak=float(radiance(2897.77/temp,temperature=temp))
        pl=ax.plot(lambda x:float(radiance(x,temperature=temp)/peak),x_range=[.2,5,.03],color=BLUE)
        rj=DashedVMobject(ax.plot(lambda x:min(1.25,2*C*K*temp/(x*1e-6)**4/peak),x_range=[.2,5,.025],color=RED),num_dashes=38)
        self.show(ax,label('파장 λ →',x=.7,y=-1.35,size=22,color=MUTED));self.play(Create(pl),Create(rj),run_time=1)
        self.show(label('플랑크',x=1.8,y=1.9,size=22,color=BLUE),label('고전 예측',x=-1.2,y=1.9,size=22,color=RED))
        self.to(12);self.show(eq(r'E=nh\nu',y=-2.25,size=40,color=GOLD));self.note('이론 곡선 도식 · 1900은 플랑크의 가정 제안')
        self.grade()
    def s03(self):
        self.begin();metal=Rectangle(width=.45,height=2.5,color=MUTED,fill_color=MUTED,fill_opacity=.4).move_to(p(.6,.1));self.show(metal)
        self.to(26)
        incoming=VGroup(*[wave(2.4,.1,2,RED).move_to(p(-1.2,y)) for y in [-.6,0,.6]])
        self.play(LaggedStart(*[Create(o) for o in incoming],lag_ratio=.15),run_time=1)
        low_labels=VGroup(label('낮은 주파수 · 강한 빛',y=-1.65,size=26,color=RED),label('전자 방출 없음',x=2.3,y=.2,size=23,color=MUTED,width=2.2))
        self.show(low_labels)
        self.to(31);self.play(FadeOut(incoming),FadeOut(low_labels),run_time=.3)
        self.show(label('높은 주파수 · 전자 방출',y=-1.65,size=26,color=BLUE))
        high=wave(2.4,.1,5,BLUE).move_to(p(-1.2,.2));self.play(Create(high),run_time=.6)
        electrons=VGroup(*[Dot(p(.9,.2),radius=.07,color=GOLD) for _ in range(4)])
        self.add(electrons)
        self.play(*[d.animate.move_to(p(2.8,1.2-i*.65)) for i,d in enumerate(electrons)],run_time=1.4)
        self.show(eq(r'K_{\max}=h\nu-\Phi',y=-2.35,size=36,color=GOLD));self.note('1905: 아인슈타인의 설명 · 보통 세기의 단일 광자 모형')
        self.grade()
    def s04(self):
        self.begin();atom=Circle(radius=.6,color=BLUE).move_to(p(1.4,.6));self.show(atom,label('수은 원자',x=1.4,y=1.7,size=23,color=BLUE))
        self.to(44);electron=Dot(p(-3,.6),color=BLUE,radius=.09);self.add(electron)
        self.play(electron.animate.move_to(p(.65,.6)),run_time=1.3)
        self.show(label('4.9 eV 전달',x=-1.2,y=1.7,size=26,color=GOLD))
        self.play(atom.animate.set_color(GOLD),electron.animate.move_to(p(2.7,.6)),run_time=1.2)
        self.to(50)
        level=VGroup(Line(p(-2.5,-1.1),p(-.7,-1.1),color=BLUE),Line(p(-2.5,-.1),p(-.7,-.1),color=GOLD),Arrow(p(-1.6,-1.05),p(-1.6,-.15),color=GOLD,buff=.04))
        self.show(level,label('정해진 에너지 차이',x=1.25,y=-.8,size=25,color=GOLD,width=3.7))
        self.show(graph(lambda x:.25*x-.55*np.exp(-((x-1)/.11)**2)-.55*np.exp(-((x-2)/.11)**2),xmin=0,xmax=3,y=-2.3,amp=.55,width=5.9,color=BLUE))
        self.note('수집 전류–전압: 정성적 도식 · 내부 에너지 여기')
        self.grade()
    def s05(self):
        self.begin();magnets=VGroup(box('N',x=.1,y=1.4,w=2.5,h=.65,color=RED),box('S',x=.1,y=-1.2,w=2.5,h=.65,color=BLUE));self.show(magnets)
        self.to(59)
        paths=VGroup(Line(p(-3,.1),p(-1,.1),color=BLUE),Line(p(-1,.1),p(3,1),color=BLUE),Line(p(-1,.1),p(3,-.8),color=BLUE))
        self.play(Create(paths),run_time=1)
        particles=VGroup(*[Dot(p(-3,.1),radius=.05,color=BLUE) for _ in range(8)]);self.add(particles)
        self.play(LaggedStart(*[MoveAlongPath(d,VMobject().set_points_as_corners([p(-3,.1),p(-1,.1),p(3,1 if i%2 else -.8)])) for i,d in enumerate(particles)],lag_ratio=.08),run_time=3)
        self.to(66);self.show(label('연속 분포가 아닌 두 갈래',y=-2.05,size=29,color=GOLD));self.note('중성 은 원자 · 불균일한 자기장 · 두 검출 분포')
        self.grade()
    def s06(self):
        self.begin();electron=Dot(p(0,.3),radius=.13,color=GOLD);self.show(electron)
        self.to(74)
        photon=wave(2,.12,5,BLUE).move_to(p(-2,.3));self.play(Create(photon),run_time=.6);self.play(photon.animate.move_to(p(-.4,.3)),run_time=.7)
        outgoing=wave(2,.12,3.33,GREEN).rotate(PI/3).move_to(p(.65,.3+.65*np.sqrt(3)))
        self.play(Transform(photon,outgoing),electron.animate.move_to(p(1.8,-1.25885)),run_time=1)
        self.show(Arrow(p(0,.3),p(1.1,.3+1.1*np.sqrt(3)),color=GREEN),Arrow(p(0,.3),p(1.8,-1.25885),color=GOLD))
        self.to(78);self.show(eq(r'\lambda^{\prime}>\lambda',y=-2.2,size=43,color=GREEN));self.note('파형은 파장 표시 · 에너지와 운동량 전달')
        self.grade()
    def s07(self):
        self.begin();lattice=VGroup(*[Dot(p(-.1+i*.38,-.7+j*.38),radius=.06,color=BLUE) for i in range(4) for j in range(4)]);self.show(lattice)
        self.to(89);beam=Arrow(p(-3,.1),p(-.3,.1),color=BLUE,buff=0);self.play(GrowArrow(beam),run_time=.7)
        rays=VGroup(*[Arrow(p(.7,.1),p(3,y),color=BLUE,buff=.1,stroke_opacity=.3 if abs(y)<.8 else 1) for y in [-1.5,-.6,.4,1.6]])
        self.play(Create(rays),run_time=1)
        self.to(94);curve=graph(lambda x:np.exp(-((x-.9)/.2)**2)+.55*np.exp(-((x+1)/.22)**2),y=-2.3,amp=.8,color=BLUE)
        self.play(Create(curve),run_time=1);self.show(label('특정 각도에서 강한 산란',y=-1.2,size=27,color=GOLD));self.note('결정 격자 · 각도별 회절 피크 · 도식')
        self.grade()
    def s08(self):
        self.begin();barrier=VGroup(*[Line(p(-1.3,a),p(-1.3,b),color=MUTED,stroke_width=8) for a,b in [(-1.5,-.5),(-.3,.3),(.5,1.5)]])
        self.show(barrier,Line(p(2.8,-1.65),p(2.8,1.7),color=MUTED))
        self.to(106);self.show(Arrow(p(-3.2,0),p(-1.5,0),color=BLUE,buff=0))
        for sy in [-.4,.4]:
            arcs=VGroup(*[Arc(radius=r,start_angle=-PI/2,angle=PI,color=BLUE,stroke_opacity=.35).move_arc_center_to(p(-1.3,sy)) for r in [.7,1.3,1.9]])
            self.play(Create(arcs),run_time=.5)
        self.note('1961: 전자 이중슬릿 간섭 관측')
        self.to(110)
        self.note('이후 단일 전자 축적 실험 · 확률모형에서 표본추출')
        rng=np.random.default_rng(1961);ys=np.linspace(-1.6,1.6,2001);prob=density(ys);prob/=prob.sum()
        samples=rng.choice(ys,size=230,p=prob);xs=rng.uniform(1.6,2.7,len(samples))
        dots=VGroup(*[Dot(p(x,y),radius=.022,color=BLUE) for x,y in zip(xs,samples)])
        self.play(LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=.012),run_time=4.2)
        self.grade()
    def s09(self):
        self.begin();source=Dot(p(0,.7),radius=.14,color=GOLD);self.show(source)
        self.to(125)
        detectors=VGroup(box('A',x=-2.6,y=.7,w=1.2,h=1.4,color=BLUE),box('B',x=2.6,y=.7,w=1.2,h=1.4,color=GREEN));self.show(detectors)
        analyzers=VGroup(Line(p(-2.95,1.7),p(-2.25,1.7),color=BLUE),Line(p(2.25,1.7),p(2.95,1.7),color=GREEN))
        self.show(analyzers)
        pair=VGroup(Dot(p(0,.7),radius=.075,color=BLUE),Dot(p(0,.7),radius=.075,color=GREEN));self.add(pair)
        self.play(pair[0].animate.move_to(p(-2.6,.7)),pair[1].animate.move_to(p(2.6,.7)),run_time=.9)
        self.show(label('방향을 바꿔 측정 → 상관관계 비교',y=-.6,size=27,color=GOLD))
        self.to(131)
        self.play(Rotate(analyzers[0],PI/4),Rotate(analyzers[1],-PI/8),run_time=.6)
        self.show(eq(r'|S|\leq2',x=-1.7,y=-1.8,size=37,color=MUTED,width=3),eq(r'2\sqrt2>2',x=1.7,y=-1.8,size=37,color=BLUE,width=3))
        self.show(label('CHSH 이론 예시 · 1972 실측 수치가 아님',y=-1.05,size=17,color=MUTED))
        self.note('CHSH 수치는 이론 예시 · 1972 실측값이 아님')
        self.to(136)
        scale=2.2;start=-3;bar=Line(p(start,-2.5),p(start+scale*2*np.sqrt(2),-2.5),color=BLUE,stroke_width=7)
        limit=DashedLine(p(start+scale*2,-2.9),p(start+scale*2,-2.1),color=RED)
        self.play(Create(bar),Create(limit),run_time=1)
        self.note('국소적 숨은변수 한계 위반 · 초광속 통신 아님')
        self.grade()
    def s10(self):
        self.begin()
        paths=VGroup(Line(p(-2.7,.5),p(-.5,1.6),color=BLUE),Line(p(-2.7,.5),p(-.5,-.6),color=GREEN),Line(p(-.5,1.6),p(1.2,.5),color=BLUE),Line(p(-.5,-.6),p(1.2,.5),color=GREEN));self.show(paths)
        self.to(149)
        marks=VGroup(label('H',x=-.5,y=1.9,size=25,color=BLUE),label('V',x=-.5,y=-1.05,size=25,color=GREEN),label('편광으로 경로 표식',x=1.5,y=1.7,size=23,color=GOLD,width=3.5))
        self.show(marks)
        envelope=lambda x:np.exp(-x*x/3)
        total=graph(envelope,y=-2.25,amp=.5,color=MUTED)
        self.show(total,label('전체: 간섭 없음',x=-2.2,y=-1.5,size=23,color=MUTED,width=3))
        self.to(153)
        self.play(paths.animate.scale(.65).move_to(p(-1.7,.8)),FadeOut(marks),run_time=.4)
        plus=graph(lambda x:envelope(x)*(1+np.cos(7*x))/2,y=.9,amp=.5,width=3.2,color=BLUE).shift(RIGHT*1.8)
        minus=graph(lambda x:envelope(x)*(1-np.cos(7*x))/2,y=-.5,amp=.5,width=3.2,color=GREEN).shift(RIGHT*1.8)
        self.show(plus,minus,label('+ 조건',x=-.3,y=1.45,size=21,color=BLUE),label('− 조건',x=-.3,y=.05,size=21,color=GREEN))
        self.note('± 편광 측정 결과별 분류 · 합하면 전체 분포 유지')
        self.grade()
