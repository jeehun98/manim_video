"""One continuous visual vocabulary: proof card → code → arithmetic → G."""
import json
from pathlib import Path
from manim import *
from longforms.qcs01_speed.direction import QCSScene, label, text, p, L

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
config.background_color='#10141C'
INK,BLUE,GREEN,RED,GOLD,MUTED='#F2F4F8','#4EA8DE','#50C79A','#EF7272','#F2C66D','#8995AA'

def eq(s,x=0,y=0,size=42,color=INK,width=7.4):
    o=MathTex(s,font_size=size*1.35,color=color)
    if o.width>width:o.scale_to_fit_width(width)
    return o.move_to(p(x,y))

def card(title,x=0,y=0,color=BLUE,w=3.15,h=1.2,size=28):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.16,stroke_color=color,stroke_width=2,fill_color=color,fill_opacity=.07),label(title,size=size,color=color,width=w-.35)).move_to(p(x,y))

def proof(x=0,y=0,scale=1):
    box=RoundedRectangle(width=5.7,height=3.4,corner_radius=.15,stroke_color=GREEN,fill_color=GREEN,fill_opacity=.035)
    rows=VGroup(label('증명',y=1.1,size=24,color=GREEN),
                eq(r'2a+2b',y=.35,size=33),eq(r'=2(a+b)',y=-.4,size=33),label('2의 배수 → 짝수',y=-1.15,size=25,color=GREEN))
    return VGroup(box,rows).scale(scale).move_to(p(x,y))

def arrow(a,b,color=MUTED):return Arrow(a.get_bottom(),b.get_top(),buff=.15,color=color,stroke_width=2)

class GodelScene(QCSScene):
    data=DATA
    def replace(self,old,new):return Scene.replace(self,old,new)
    def update_mobjects(self,dt):
        super().update_mobjects(dt)
        # Check every rendered state, including intermediate animation frames.
        for o in self.mobjects:
            if o is getattr(self,'caption',None) or o is getattr(self,'caption_panel',None):continue
            if o.width<.001 or o.height<.001:continue
            assert o.get_left()[0]>=-4.38 and o.get_right()[0]<=4.38, ('horizontal',self.shot,self.time)
            assert o.get_bottom()[1]>=-4.9 and o.get_top()[1]<=7.9, ('vertical',self.shot,self.time)
    def setup(self):
        super().setup()
        self.remove(self.mobjects[0])
        self.add(text('수학 · 증명 · 계산',y=L.brand_y,size=18,color=MUTED))
    def clear_body(self):
        keep=[self.title,self.caption,self.caption_panel]
        obs=[o for o in self.mobjects if all(o is not k for k in keep) and o.get_center()[1]<4.9]
        if obs:self.play(*[FadeOut(o) for o in obs],run_time=.4)
    def condition(self):
        self.note('충분한 산술 · 효과적 공리 열거 · 일관성',GOLD)

    def s01(self):
        ai=card('AI',y=3.2,w=2,color=BLUE);doc=proof(y=.5,scale=.72)
        self.show(ai);self.play(GrowArrow(arrow(ai,doc)),FadeIn(doc),run_time=.8)
        self.to(2);self.show(label('답이 맞아도\n풀이를 확인해야 한다',y=-2.5,size=31,color=GOLD))
        self.to(7)
        ver=card('별도 검증기',y=-1.9,w=3.3,color=GREEN)
        self.clear_body();ai=card('AI · 증명 생성',y=3.0,w=4);doc=proof(y=.35,scale=.67)
        self.show(ai,doc,ver);self.play(GrowArrow(arrow(ai,doc)),GrowArrow(arrow(doc,ver)),run_time=.7)
        self.show(label('규칙에 맞는지 검사',y=-3.15,size=25,color=GREEN))
        self.to(13);self.clear_body()
        self.show(label('모든 수학적 진리를\n증명할 수 있을까?',y=.6,size=45,color=GOLD))

    def s02(self):
        examples=VGroup(eq('2+4=6',y=2.5,size=31,color=MUTED),eq('10+8=18',y=1.3,size=31,color=MUTED),eq('28+16=44',y=.1,size=31,color=MUTED))
        self.show(examples)
        self.to(18);self.show(label('두 짝수의 합은 항상 짝수?',y=3.8,size=30,color=GOLD))
        self.to(21);self.play(FadeOut(examples),run_time=.4)
        f=eq('2a+2b',y=.9,size=60);self.play(Write(f),run_time=.8)
        self.show(label('a, b는 정수',y=2.7,size=25,color=MUTED))
        self.play(TransformMatchingTex(f,eq('2(a+b)',y=.9,size=60,color=GREEN)),run_time=1.2)
        self.show(label('2의 배수 → 짝수',y=-.5,size=34,color=GREEN))
        self.to(26)
        checks=VGroup(*[card(t,x=x,y=-2.3,w=2.15,h=.85,color=GREEN,size=22) for x,t in [(-2.5,'정의 ✓'),(0,'식 변형 ✓'),(2.5,'결론 ✓')]])
        self.play(LaggedStart(*[FadeIn(c) for c in checks],lag_ratio=.35),run_time=1.5)
        self.to(31);self.show(label('무한한 사례 → 일반적인 증명 하나',y=-3.6,size=25,color=GOLD))

    def s03(self):
        rules=VGroup(*[card(t,x=x,y=3,w=2.2,h=1,color=BLUE,size=24) for x,t in [(-2.5,'기호'),(0,'공리'),(2.5,'추론 규칙')]])
        self.show(rules);system=card('형식 체계 T',y=1,w=5,color=BLUE)
        self.play(ReplacementTransform(rules.copy(),system),run_time=1)
        self.to(39)
        candidates=VGroup(*[card(t,y=-.5-i*.9,w=5.2,h=.7,color=GREEN if i in [0,3] else MUTED,size=24) for i,t in enumerate(['후보 01    유효 ✓','후보 02    무효 ×','후보 03    무효 ×','후보 04    유효 ✓'])])
        self.play(LaggedStart(*[FadeIn(c,shift=DOWN*.15) for c in candidates],lag_ratio=.3),run_time=2)
        self.to(43);self.note('증명이 있다면, 빠짐없는 탐색은 언젠가 찾는다',GREEN)
        self.to(47);self.clear_body();self.show(label('참인 명제라면\n증명도 반드시 존재할까?',y=.6,size=41,color=GOLD))

    def s04(self):
        self.show(label('1931',y=2.4,size=67,color=GOLD),label('쿠르트 괴델',y=.8,size=40),label('증명 자체를 수학의 대상으로',y=-.8,size=29,color=MUTED))
        self.to(57);self.clear_body()
        sent=card('두 짝수의 합은 짝수',y=3,w=6,color=BLUE);doc=proof(y=-.5,scale=.72)
        self.show(sent,doc)
        s=eq('s',x=2.8,y=1.8,size=50,color=BLUE);pr=eq('p',x=2.8,y=-2.4,size=50,color=GREEN)
        self.play(TransformFromCopy(sent,s),TransformFromCopy(doc,pr),run_time=1.2)
        self.show(label('문장 번호',x=-.7,y=1.8,size=25,color=BLUE),label('증명 번호',x=-.7,y=-2.4,size=25,color=GREEN))
        self.to(61);self.note('문자 · 프로그램도 숫자로 저장한다')
        self.to(65);self.note('괴델 번호화  /  s와 p는 자연수 번호',GOLD)

    def s05(self):
        s=card('문장 번호 s',x=-1.9,y=3,w=3.25,color=BLUE)
        pr=card('증명 번호 p',x=1.9,y=3,w=3.25,color=GREEN)
        self.show(s,pr);self.note('번호 부여 → 증명 검사 관계의 산술화',GOLD)
        self.to(70)
        rel=eq(r'\operatorname{Proof}(p,s)',y=1.2,size=49)
        self.play(Write(rel),run_time=1)
        self.show(label('p가 s의 올바른 증명인가?',y=.05,size=30))
        line=Line(p(-3.3,-.9),p(3.3,-.9),color=MUTED,stroke_width=1);self.show(line)
        self.to(76)
        exists=eq(r'\exists p\;\operatorname{Proof}(p,s)',y=-1.8,size=44,color=GREEN)
        self.play(TransformFromCopy(rel,exists),run_time=1)
        self.show(label('증명 번호 p가 하나라도 존재하는가?',y=-2.9,size=26,color=GREEN))
        self.to(81)
        self.play(ReplacementTransform(exists,eq(r'\operatorname{Prov}(s)',y=-1.8,size=51,color=GREEN)),run_time=1)
        self.note('증명에 관한 질문을 자연수의 식으로',GOLD)

    def s06(self):
        generic=eq(r'\operatorname{Prov}(s)',y=2.7,size=53,color=GREEN);self.show(generic)
        step=card('자기언급하도록 구성 · 대각화',y=.9,w=7,h=1.15,color=GOLD,size=27)
        self.show(step)
        self.play(GrowArrow(arrow(generic,step,GOLD)),run_time=.7)
        g=eq('G',x=-2.2,y=-1,size=63,color=BLUE);code=eq(r'\ulcorner G\urcorner',x=2.2,y=-1,size=50,color=BLUE)
        self.show(g,code);self.play(Create(DoubleArrow(g.get_right(),code.get_left(),buff=.2,color=BLUE)),run_time=.8)
        self.show(label('문장',x=-2.2,y=-2,size=24,color=MUTED),label('자신의 번호',x=2.2,y=-2,size=24,color=MUTED))
        self.to(91);self.clear_body()
        f=eq(r'G\;\longleftrightarrow\;\neg\operatorname{Prov}(\ulcorner G\urcorner)',y=1.8,size=42)
        self.show(f,label('자기 자신의 증명 가능성을 부정',y=3.2,size=27,color=GOLD))
        self.to(94);self.show(card('이 문장은 이 체계 안에서\n증명되지 않는다.',y=-.3,w=7,h=2,color=RED,size=33))
        self.note('동치 관계는 체계 T 안에서 성립하도록 구성')
        self.to(97);self.show(eq('G',y=-2.3,size=57,color=BLUE))

    def s07(self):
        assumption=card('가정: G를 증명할 수 있다',y=3.3,w=7,color=GOLD,size=28);self.show(assumption)
        self.to(101)
        # Replace the even-number content with an abstract G proof, not an invalid concrete derivation.
        doc=VGroup(RoundedRectangle(width=3.4,height=2,corner_radius=.12,color=GREEN),eq(r'\vdots',y=1.2,size=33,color=GREEN),eq(r'\therefore G',y=.5,size=33,color=GREEN)).move_to(p(0,1))
        proof_number=eq('p',x=2.6,y=1,size=48,color=GREEN)
        self.show(doc,proof_number)
        yes=card('G의 증명이 존재함',y=-.7,w=6.5,color=GREEN,size=29)
        self.show(yes);self.show(eq(r'T\vdash\operatorname{Prov}(\ulcorner G\urcorner)',y=-1.7,size=33,color=GREEN))
        self.to(107);self.play(FadeOut(doc),FadeOut(proof_number),run_time=.4)
        no=card('G의 증명이 존재하지 않음',y=1.3,w=6.5,color=RED,size=28)
        self.show(no);self.show(eq(r'T\vdash\neg\operatorname{Prov}(\ulcorner G\urcorner)',y=2.3,size=33,color=RED))
        self.to(110)
        self.play(Indicate(yes,color=RED),Indicate(no,color=RED),run_time=1)
        self.show(label('같은 체계 안에서 모순',y=-2.8,size=35,color=RED))
        self.to(115);self.clear_body()
        self.show(eq(r'T\nvdash G',y=1.5,size=70,color=BLUE),label('모순이 없는 체계라면\nG의 증명은 존재할 수 없다',y=-.5,size=32,color=GOLD))

    def s08(self):
        self.show(eq('G',y=3,size=75,color=BLUE))
        self.show(card('참\n표준 자연수 해석',y=1,w=6,color=GOLD,h=1.5,size=29),card('증명 불가\n현재 형식 체계 T',y=-1.1,w=6,color=BLUE,h=1.5,size=29))
        self.note('체계 T가 일관된다는 가정 아래')
        self.to(123);self.play(Indicate(self.mobjects[-2],color=BLUE),run_time=1)
        self.to(128);self.clear_body()
        self.show(label('제1불완전성 정리',y=3.5,size=39,color=GOLD),label('로서의 강화까지 반영한 결론',y=2.5,size=24,color=MUTED))
        conditions=VGroup(*[card(t,y=1.3-i*1,w=6.7,h=.76,color=BLUE,size=25) for i,t in enumerate(['충분한 산술을 표현','공리를 기계적으로 열거 가능','모순이 없음 · 일관성'])])
        self.play(LaggedStart(*[FadeIn(c) for c in conditions],lag_ratio=.3),run_time=1.3)
        self.show(label('증명도 반증도 할 수 없는\n문장이 존재한다',y=-2.3,size=34,color=GOLD))
        self.note('앞의 G 설명과 구별되는 일반적 정리')

    def s09(self):
        system=RoundedRectangle(width=6.8,height=5.5,corner_radius=.2,color=BLUE).move_to(p(0,.4))
        self.show(system,label('형식 체계 T',y=2.5,size=30,color=BLUE),label('수학적 발전은 멈출까?',y=.4,size=36,color=GOLD))
        self.to(141);self.clear_body();self.show(label('계속 발전할 수 있다',y=3.3,size=35,color=GREEN))
        self.to(142)
        original=card('같은 공리 · 새 증명 발견',y=1.5,w=6.5,color=GREEN,size=28)
        extended=card('새 공리 추가 · 체계 T′',y=-.3,w=6.5,color=BLUE,size=28)
        self.show(original);self.play(ShowPassingFlash(SurroundingRectangle(original,color=GREEN)),run_time=1)
        self.show(extended);self.show(label('이전 체계에서 도출되지 않던 명제도\n확장된 체계에서는 증명 가능할 수 있다',y=-2,size=25))
        self.note('새 공리의 채택이 진리를 자동 보장하지는 않음')
        self.to(149);self.clear_body()
        self.show(card('확장된 형식 체계 T′',y=2.6,w=6.8,color=BLUE,size=31),label('같은 조건을 만족한다면',y=.8,size=29),card('다시 증명도 반증도\n할 수 없는 문장이 존재',y=-1,w=6.8,h=1.8,color=GOLD,size=30))
        self.condition()

    def s10(self):
        self.show(label('계산 속도',y=2.3,size=34,color=MUTED),eq(r'1\times\quad 100\times\quad 10^6\times',y=.9,size=40,color=MUTED))
        self.to(160);self.clear_body()
        system=card('하나의 형식 체계 T',y=2.8,w=6.8,color=BLUE,size=34)
        self.show(system,label('모든 산술적 진리를\n증명할 수는 없다',y=.3,size=39,color=GOLD))
        self.condition()
        self.to(166);self.clear_body()
        self.show(label('AI의 증명 능력은 발전한다',y=3.4,size=31,color=GREEN))
        self.show(VGroup(*[card('증명 ✓',x=x,y=1.8,w=2.1,h=.8,color=GREEN,size=23) for x in [-2.5,0,2.5]]))
        self.to(169)
        self.show(card('참\n표준 자연수에서',x=-1.9,y=-.2,w=3.25,h=1.6,color=GOLD,size=26),card('증명 가능\n정해진 체계 T에서',x=1.9,y=-.2,w=3.25,h=1.6,color=BLUE,size=26))
        self.show(label('참이라는 것과\n증명 가능하다는 것은 다르다',y=-2.5,size=32))
        self.condition()
        self.to(173.5)
