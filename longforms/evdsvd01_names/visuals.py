"""Native aspect-ratio layouts; exact local scene clocks and approved captions."""
import os,json,textwrap
from pathlib import Path
from manim import *

ROOT=Path(__file__).resolve().parent
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
CUES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
SHORT=os.environ.get('BATTLE_LAYOUT','shorts')=='shorts'
config.frame_width=8 if SHORT else 128/9
config.frame_height=128/9 if SHORT else 8
config.background_color='#080F21'
config.disable_caching=True
BLUE='#6B9FFF';TEAL='#48DFCD';WHITE='#EFF4FF';MUTED='#98A9C7';GOLD='#FFDA82';PANEL='#111D35'

def pos(x,y):return np.array([x,y,0.])
def label(s,x=0,y=0,size=30,color=WHITE,width=7):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.1)
    if m.width>width:m.scale_to_fit_width(width)
    return m.move_to(pos(x,y))

def card(name,formula,color,x,y,w=3.1):
    return VGroup(RoundedRectangle(width=w,height=2.25,corner_radius=.18,stroke_color=color,stroke_width=1.5,fill_color=PANEL,fill_opacity=1).move_to(pos(x,y)),label(name,x,y+.4,47,color,w-.3),label(formula,x,y-.55,27,WHITE,w-.3))

class BattleScene(Scene):
    INDEX=0
    def to(self,t):
        if self.time>t+1/config.frame_rate+.001:raise RuntimeError(f'Overflow {self.INDEX}: {self.time}>{t}')
        if t-self.time>1e-5:self.wait(t-self.time)
    def reveal(self,*items,d=.35):self.play(*[FadeIn(m,shift=UP*.1) for m in items],run_time=d)
    def setup(self):
        self.spec=MANIFEST[self.INDEX];self.length=self.spec['duration_seconds']
        self.add(label('MATRIX DECOMPOSITION WORLD CUP',y=6.55 if SHORT else 3.55,size=15,color=MUTED,width=7 if SHORT else 12))
        y=5.85 if SHORT else 2.98
        self.add(label('EVD',-1.35,y,29,BLUE,2),label('VS',0,y,17,MUTED,1),label('SVD',1.35,y,29,TEAL,2))
        self.add(Line(pos(-3.5 if SHORT else -6.5,y-.45),pos(3.5 if SHORT else 6.5,y-.45),color=MUTED,stroke_opacity=.25))
        self.add(label('01 / NAME  ·  이름의 직관성',y=-6.65 if SHORT else -3.65,size=15,color=MUTED,width=7))
        self.caption=VGroup();self.caption_key=None
        self.caption.add_updater(lambda m,dt:self.update_caption())
        self.add(self.caption);self.update_caption()
    def update_caption(self):
        t=self.spec['start']+self.time+1e-6
        cue=next((c for c in CUES if c['start']<=t<c['end']),None)
        key=cue['start'] if cue else None
        if key==self.caption_key:return
        self.caption_key=key;self.caption.remove(*list(self.caption))
        if cue:
            # Character wrapping only changes line breaks; text and timing are preserved.
            words='\n'.join(textwrap.wrap(cue['caption'],27 if SHORT else 52,break_long_words=False))
            txt=label(words,y=-5.7 if SHORT else -2.98,size=22 if SHORT else 23,width=7.1 if SHORT else 12.5)
            bg=RoundedRectangle(width=7.45 if SHORT else 13.0,height=max(.65,txt.height+.25),corner_radius=.08,stroke_width=0,fill_color='#080F21',fill_opacity=.96).move_to(txt)
            self.caption.add(bg,txt).set_z_index(100)
    def title(self,s,color=WHITE):
        m=label(s,y=4.55 if SHORT else 1.98,size=32,color=color,width=7 if SHORT else 12)
        self.reveal(m);return m
    def split(self,left,right):
        left.scale_to_fit_width(min(left.width,6.7 if SHORT else 5.6))
        right.scale_to_fit_width(min(right.width,6.5 if SHORT else 5.6))
        if not SHORT and right.height>3.3:right.scale_to_fit_height(3.3)
        left.move_to(pos(0,2.3) if SHORT else pos(-3.5,.0))
        right.move_to(pos(0,-1.25) if SHORT else pos(3.15,-.1))
        return left,right
    def pair(self):
        return VGroup(card('EVD','A = PDP⁻¹',BLUE,-1.8,0,3.2),label('VS',0,0,19,GOLD,.4),card('SVD','A = UΣVᵀ',TEAL,1.8,0,3.2))
    def construct(self):
        getattr(self,f'scene_{self.INDEX}')()
        self.to(self.length)
    def scene_0(self):
        self.reveal(label('행렬분해\n이상형 월드컵!',y=2.5 if SHORT else 1.2,size=41,width=7))
        self.to(1)
        pair=self.pair().move_to(pos(0,-.7 if SHORT else -.7));self.reveal(pair,d=.45)
    def scene_1(self):
        self.reveal(label('ROUND 01',y=2,size=24,color=GOLD),label('NAME',y=.3,size=78),label('대결 기준 · 이름',y=-1.2,size=31),label('이름이 개념을 얼마나 잘 전달할까?',y=-2.5,size=23,color=MUTED))
    def term(self,name,full,korean,word,color):
        self.title(name,color)
        block=VGroup(label(full,y=.6,size=30,color=color,width=6.5),label(korean,y=-.4,size=35))
        block.move_to(pos(0,2) if SHORT else pos(-3.35,.2));self.reveal(block)
        self.to(3 if self.INDEX==2 else 4)
        wordblock=VGroup(label(word,y=.7,size=60,color=color),label('독일어' if self.INDEX==2 else '일상적인 단어의 뜻',y=-.4,size=21,color=MUTED))
        wordblock.move_to(pos(0,-.6) if SHORT else pos(3.2,.3));self.reveal(wordblock)
        self.to(5 if self.INDEX==2 else 6)
        meaning=label('고유한 · 자기 자신의' if self.INDEX==2 else '특이한 · 독특한',x=0 if SHORT else 3.2,y=-2.2 if SHORT else -1.3,size=30,color=color,width=6.2)
        self.reveal(meaning)
    def scene_2(self):self.term('EVD','Eigenvalue Decomposition','고유값 분해','Eigen',BLUE)
    def scene_5(self):self.term('SVD','Singular Value Decomposition','특이값 분해','Singular',TEAL)
    def scene_3(self):
        self.title('자신이 놓인 직선을 벗어나지 않는다',BLUE)
        explanation=VGroup(label('Eigen',y=1,size=47,color=BLUE),label('A = [ 2  1 ]\n      [ 1  2 ]',y=-.2,size=30),label('v = (1, 1)',y=-1.4,size=29))
        plane=NumberPlane(x_range=[-1,4,1],y_range=[-1,4,1],x_length=4.7,y_length=4.7,background_line_style={'stroke_color':MUTED,'stroke_opacity':.17},axis_config={'stroke_opacity':.4,'stroke_width':1})
        line=Line(plane.c2p(-.7,-.7),plane.c2p(3.6,3.6),color=BLUE,stroke_opacity=.5)
        arrow=Arrow(plane.c2p(0,0),plane.c2p(1,1),buff=0,color=BLUE,stroke_width=6)
        ghost=arrow.copy().set_opacity(.28)
        graph=VGroup(plane,line,ghost,arrow)
        explanation,graph=self.split(explanation,graph)
        self.reveal(explanation,graph,d=.4)
        self.to(2)
        self.play(Transform(arrow,Arrow(plane.c2p(0,0),plane.c2p(3,3),buff=0,color=BLUE,stroke_width=6)),run_time=2.3)
        eq=label('Av = 3v',x=0 if SHORT else 3.15,y=-4.3 if SHORT else -2,size=32,color=BLUE)
        self.reveal(eq);self.to(5)
        general=Arrow(plane.c2p(0,0),plane.c2p(1,0),buff=0,color=GOLD,stroke_width=4)
        self.reveal(general,d=.3)
        self.play(Transform(general,Arrow(plane.c2p(0,0),plane.c2p(2,1),buff=0,color=GOLD,stroke_width=4)),run_time=1)
        self.reveal(label('일반 벡터는 방향이 바뀔 수 있다',x=0 if SHORT else -3.4,y=-3.65 if SHORT else -1.9,size=20,color=GOLD,width=6 if SHORT else 5.5))
    def scene_4(self):
        self.title('이름과 성질이 연결된다',BLUE)
        self.reveal(label('Eigen',y=2 if SHORT else .8,size=65,color=BLUE),label('고유한 · 자기 자신의',y=.4 if SHORT else -.2,size=30),label('↓',y=-.7 if SHORT else -.9,size=35,color=BLUE),label('자신의 직선을 유지',y=-2 if SHORT else -1.65,size=32,color=BLUE))
    def scene_6(self):
        self.reveal(label('Singular?',y=1,size=68,color=TEAL),label('무엇이 특이한 걸까?',y=-.8,size=32),label('?  ?  ?',y=-2.1,size=35,color=MUTED))
    def scene_7(self):
        self.title('방향에 따른 길이 변화',TEAL)
        explanation=VGroup(label('A = diag(2, 0.7)',y=1,size=31,color=TEAL),label('σ₁ = 2',y=-.1,size=36,color=TEAL),label('σ₂ = 0.7',y=-1.2,size=36,color=GOLD))
        axes=NumberPlane(x_range=[-2.5,2.5,1],y_range=[-2,2,1],x_length=5,y_length=4,background_line_style={'stroke_opacity':.13,'stroke_color':MUTED},axis_config={'stroke_opacity':.4,'stroke_width':1})
        unit=Circle(radius=1,color=MUTED,stroke_width=2).move_to(axes.c2p(0,0))
        shape=Circle(radius=1,color=TEAL,fill_color=TEAL,fill_opacity=.08).move_to(axes.c2p(0,0))
        arrows=VGroup(*[Arrow(axes.c2p(0,0),axes.c2p(np.cos(t),np.sin(t)),buff=0,color=TEAL,stroke_width=2,max_tip_length_to_length_ratio=.12) for t in np.linspace(0,TAU,8,endpoint=False)])
        graph=VGroup(axes,unit,shape,arrows);explanation,graph=self.split(explanation,graph)
        self.reveal(explanation,graph,d=.35);self.to(.9)
        target=shape.copy().stretch(2,0).stretch(.7,1)
        ends=VGroup(*[Arrow(axes.c2p(0,0),axes.c2p(2*np.cos(t),.7*np.sin(t)),buff=0,color=TEAL if i%2==0 else GOLD,stroke_width=2,max_tip_length_to_length_ratio=.12) for i,t in enumerate(np.linspace(0,TAU,8,endpoint=False))])
        self.play(Transform(shape,target),Transform(arrows,ends),run_time=2.2)
        self.reveal(label('단위원 → 타원',x=0 if SHORT else 3.2,y=-4 if SHORT else -2,size=27,color=TEAL))
    def scene_8(self):
        self.title('이름에서 길이 변화가 떠오를까?')
        self.reveal(label('Singular',y=2 if SHORT else 1,size=58,color=TEAL),label('특이한 · 독특한',y=.7 if SHORT else .1,size=29,color=MUTED))
        self.to(1.3)
        self.reveal(DashedLine(pos(0,-.1),pos(0,-1.4),color=MUTED),label('?',x=.5,y=-.75,size=30,color=GOLD),label('방향별 길이 변화',y=-2 if SHORT else -1.65,size=34,color=TEAL))
        self.to(3.5);self.reveal(label('이름만으로는 연결이 어렵다',y=-3.5 if SHORT else -2.2,size=24,color=MUTED))
    def scene_9(self):
        self.title('이름 대결의 승자는?',GOLD)
        pair=self.pair().move_to(pos(0,1 if SHORT else .1));self.reveal(pair)
        self.to(2)
        self.reveal(label('WINNER · EVD!',y=-2 if SHORT else -1.8,size=49,color=GOLD),d=.25)
        self.play(Circumscribe(pair[0],color=BLUE,fade_out=True),run_time=.5)
    def scene_10(self):
        self.title('ROUND 01 WINNER',GOLD)
        self.reveal(label('EVD',y=2.7 if SHORT else .9,size=90,color=BLUE),label('이름이 수학적 특징을\n더 직관적으로 전달',y=.3 if SHORT else -.6,size=30,width=7))
        score=label('EVD   0 : 0   SVD',y=-2.7 if SHORT else -2,size=35,color=MUTED)
        self.reveal(score);self.to(3)
        self.play(Transform(score,label('EVD   1 : 0   SVD',y=-2.7 if SHORT else -2,size=35,color=GOLD)),run_time=.4)
        self.reveal(label('평가 기준: 이름의 직관성',y=-4 if SHORT else -2.5,size=19,color=MUTED),d=.25)
