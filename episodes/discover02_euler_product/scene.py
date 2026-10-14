"""Unique factorization reveals Euler's product; then extend the input plane."""
import os
import json
import sys
from pathlib import Path
from manim import *

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
texbin = ROOT / '.tools/TinyTeX/TinyTeX/bin/windows'
if texbin.exists():
    os.environ['PATH'] = str(texbin) + os.pathsep + os.environ.get('PATH', '')
from episodes.prune_series.visuals import txt, INK, MUTED, WEIGHT, GOOD, SPARSE

ORANGE = '#FFAA61'
RED = '#FF8C9D'
ZEROS = (14.134725142, 21.022039639, 25.010857580)


def math(s, size=40, color=INK, width=7.4):
    m = MathTex(s, font_size=size, color=color)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


class EulerProductDiscovery(Scene):
    def construct(self):
        self.chrome = VGroup(
            txt('수학적 발견  /  02', 22, MUTED).move_to(UP*7.25),
            txt('소수를 세는 문제에', 38).move_to(UP*6.5),
            txt('왜 복소수가 등장할까?', 38).move_to(UP*5.8))
        self.cap = VGroup()
        self.cues = []
        self.add(self.chrome)
        self.subtitle('소수만 바라봐야 할까요?', '모든 자연수의 곱셈 구조에서 시작합니다')
        nums = VGroup(*[txt(str(n), 40, WEIGHT if n in (2,3,5,7,11) else INK)
            .move_to([-2.8 + (n-1)%4*1.85, 3.7-(n-1)//4*1.5,0]) for n in range(1,13)])
        self.play(LaggedStart(*[FadeIn(m,shift=UP*.12) for m in nums],lag_ratio=.08),run_time=1.8)
        self.to(3)
        factors={1:'1',4:r'2^2',6:r'2\cdot3',8:r'2^3',9:r'3^2',10:r'2\cdot5',12:r'2^2\cdot3'}
        self.play(*[Transform(nums[n-1],math(v,33,ORANGE,width=1.6).move_to(nums[n-1]))
            for n,v in factors.items()],run_time=1.8)
        note=txt('1은 아무 소수도 곱하지 않은 빈 곱',23,MUTED).move_to(DOWN*2.2)
        self.play(FadeIn(note),run_time=.5)

        self.transition(11)
        self.subtitle('자연수에 가중치를 붙이면', '먼저 s = 2에서, 큰 수의 항은 작아집니다')
        numbers=VGroup(*[math(str(n),40).move_to([-3+(n-1)*1.5,2.8,0]) for n in range(1,6)])
        self.play(FadeIn(numbers),run_time=.7)
        weights=VGroup(*[math('1' if n==1 else rf'\frac1{{{n}^2}}',42,WEIGHT).move_to(numbers[n-1]) for n in range(1,6)])
        self.play(Transform(numbers,weights),run_time=1.5)
        self.to(16)
        numeric=math(r'1+\frac1{2^2}+\frac1{3^2}+\frac1{4^2}+\frac1{5^2}+\cdots',44,WEIGHT).move_to(UP*.8)
        self.play(TransformFromCopy(numbers,numeric),run_time=1.4)
        self.to(19)
        general=math(r'\zeta(s)=1+\frac1{2^s}+\frac1{3^s}+\frac1{4^s}+\cdots',45).move_to(DOWN*1.2)
        self.play(Write(general),run_time=1.6)
        label=txt('리만 제타 함수  ·  지금은 실수 s > 1',25,MUTED).move_to(DOWN*2.8)
        self.play(FadeIn(label),run_time=.5)

        self.transition(25)
        self.subtitle('소수마다 하나씩 선택합니다', '선택한 거듭제곱을 곱하면 자연수 하나가 됩니다')
        colors=(WEIGHT,SPARSE,ORANGE)
        lanes=VGroup(); entries=[]
        for j,p in enumerate((2,3,5)):
            x=(j-1)*2.35
            lane=RoundedRectangle(width=2.05,height=4.8,corner_radius=.15,color=colors[j],
                                  fill_color=colors[j],fill_opacity=.055).move_to([x,1.45,0])
            head=txt(f'소수 {p}',28,colors[j]).move_to([x,3.4,0])
            col=VGroup(*[math('1' if a==0 else rf'{p}^{{{a}}}',38,colors[j]).move_to([x,2.5-a*.9,0]) for a in range(3)])
            ell=math(r'\vdots',32,colors[j]).move_to([x,-.3,0])
            lanes.add(lane,head,col,ell);entries.append(col)
        self.play(FadeIn(lanes),run_time=1)
        remainder=txt('나머지 소수에서는 1을 선택',23,MUTED).move_to(DOWN*1.45)
        self.play(FadeIn(remainder),run_time=.5)
        self.to(34)
        boxes=VGroup(*[SurroundingRectangle(entries[j][a],color=GOOD,buff=.16,corner_radius=.08) for j,a in enumerate((2,1,0))])
        self.play(Create(boxes),run_time=.7)
        result12=MathTex(r'2^2',r'\times',r'3',r'\times',r'1',r'=12',font_size=47,color=GOOD).move_to(DOWN*2.6)
        self.play(*[TransformFromCopy(entries[j][a],result12[2*j]) for j,a in enumerate((2,1,0))],
                  FadeIn(result12[1]),FadeIn(result12[3]),FadeIn(result12[5]),run_time=1.5)
        self.to(37)
        newboxes=VGroup(*[SurroundingRectangle(entries[j][1],color=GOOD,buff=.16,corner_radius=.08) for j in range(3)])
        result30=math(r'2\times3\times5=30',47,GOOD).move_to(result12)
        self.play(Transform(boxes,newboxes),ReplacementTransform(result12,result30),run_time=1)
        unique= txt('소인수분해는 유일합니다',29,GOOD)
        unique.move_to(DOWN*4)
        self.play(FadeIn(unique),run_time=.6)

        self.transition(41)
        self.subtitle('모든 자연수와 일대일 대응', '곱의 순서를 제외하면, 중복되는 선택은 없습니다')
        heads=VGroup(txt('자연수',28,WEIGHT).move_to([-2.7,4.1,0]),txt('소수의 선택',28,ORANGE).move_to([1.3,4.1,0]))
        self.play(FadeIn(heads),run_time=.5)
        mapping=VGroup()
        for n,expression,y in zip((1,2,3,4,6,12,30),('1',r'2',r'3',r'2^2',r'2\cdot3',r'2^2\cdot3',r'2\cdot3\cdot5'),(3.25,2.35,1.45,.55,-.35,-1.25,-2.15)):
            left=math(str(n),34,WEIGHT).move_to([-2.7,y,0])
            right=math(expression,34,ORANGE).move_to([1.3,y,0])
            arrow=DoubleArrow([-1.9,y,0],[-.2,y,0],buff=.1,color=MUTED,stroke_width=2,tip_length=.12)
            row=VGroup(left,arrow,right);mapping.add(row)
            self.play(FadeIn(left),GrowArrow(arrow),FadeIn(right),run_time=.4)
        self.play(FadeIn(txt('일부 예시  ·  1 ↔ 모든 지수 0',23,MUTED).move_to(DOWN*3.25)),run_time=.5)
        self.to(50)
        self.subtitle('이제 같은 항을 두 방식으로 씁니다', '12 ↔ 12⁻ˢ, 30 ↔ 30⁻ˢ')
        newmapping=VGroup()
        for row,n,ex in zip(mapping,(1,2,3,4,6,12,30),('1','2','3','4','6','12','30')):
            y=row[0].get_y()
            left=math('1' if n==1 else rf'\frac1{{{n}^s}}',31,WEIGHT).move_to([-2.7,y,0])
            # Factor exponents come directly from unique factorization.
            factors={1:'1',2:r'2^{-s}',3:r'3^{-s}',4:r'2^{-2s}',6:r'2^{-s}3^{-s}',12:r'2^{-2s}3^{-s}',30:r'2^{-s}3^{-s}5^{-s}'}
            right=math(factors[n],31,ORANGE,width=3.7).move_to([1.3,y,0])
            newmapping.add(VGroup(left,row[1].copy(),right))
        self.play(Transform(mapping,newmapping),run_time=1.5)

        self.transition(55)
        self.subtitle('합과 곱은 같은 구조였습니다', '각 소수의 기하급수를 하나의 분수로 접습니다')
        total=math(r'\zeta(s)=\sum_{n=1}^{\infty}\frac1{n^s}',49,WEIGHT).move_to(UP*3.5)
        self.play(Write(total),run_time=1)
        series=VGroup(*[math(rf'\left(1+{p}^{{-s}}+{p}^{{-2s}}+\cdots\right)',38,c).move_to([0,y,0])
            for p,c,y in zip((2,3,5),colors,(1.7,.2,-1.3))])
        crosses=VGroup(*[math(r'\times',31,MUTED).move_to([0,y,0]) for y in (.95,-.55)])
        self.play(LaggedStart(*[FadeIn(m) for m in series],lag_ratio=.2),FadeIn(crosses),run_time=1.5)
        tail= txt('× …  모든 소수까지',23,MUTED)
        tail.move_to(DOWN*2.5); self.play(FadeIn(tail),run_time=.4)
        self.to(59)
        folded=VGroup(*[math(rf'\frac1{{1-{p}^{{-s}}}}',43,c).move_to(series[j]) for j,(p,c) in enumerate(zip((2,3,5),colors))])
        self.play(*[ReplacementTransform(series[j],folded[j]) for j in range(3)],run_time=1.4)
        self.to(62)
        product=math(r'\zeta(s)=\sum_{n=1}^{\infty}n^{-s}=\prod_{p\,\mathrm{prime}}\frac1{1-p^{-s}}',45).move_to(UP*1.5)
        self.play(FadeOut(total),FadeOut(crosses),FadeOut(tail),ReplacementTransform(folded,product),run_time=1.4)
        self.to(67)
        condition=math(r'\operatorname{Re}(s)>1',39,GOOD).move_to(DOWN*.15)
        name= txt('오일러 곱',36,ORANGE)
        name.move_to(DOWN*1.4)
        self.play(FadeIn(condition),FadeIn(name),run_time=.7)
        self.play(FadeIn(txt('모든 자연수의 가중합 = 소수별 인자의 곱',28,INK).move_to(DOWN*3)),run_time=.6)
        self.transition(73)
        self.subtitle('제타 함수의 또 다른 성질', '급수는 아무 입력에서나 수렴하지 않습니다')
        self.to(77)
        self.subtitle('하지만 이 합은 어디서나 쓸 수 없습니다', 's = 2에서는 수렴하지만, s = 1에서는 발산합니다')
        convergent=VGroup(txt('s = 2',30,WEIGHT),
            math(r'1+\frac14+\frac19+\cdots=\frac{\pi^2}{6}',43,WEIGHT),
            txt('유한한 값으로 수렴',25,GOOD)).arrange(DOWN,buff=.45).move_to(UP*2.2)
        divergent=VGroup(txt('s = 1',30,ORANGE),
            math(r'1+\frac12+\frac13+\cdots',43,ORANGE),
            txt('계속 커짐 · 유한한 값으로 수렴하지 않음',25,ORANGE)).arrange(DOWN,buff=.45).move_to(DOWN*1.7)
        self.play(FadeIn(convergent),run_time=.7)
        self.wait(1.5)
        self.play(FadeIn(divergent),run_time=.7)
        self.transition(85)
        self.subtitle('급수의 한계와 함수의 한계는 다릅니다', '기하급수로 보는 간단한 예')
        geometric=math(r'1+x+x^2+\cdots=\frac1{1-x}',48).move_to(UP*2.8)
        valid=math(r'|x|<1',35,GOOD).move_to(UP*1.55)
        self.play(Write(geometric),FadeIn(valid),run_time=1)
        self.to(94)
        at2=txt('x = 2에서는?',30,ORANGE).move_to(UP*.2)
        badsum=VGroup(math(r'1+2+4+8+\cdots',40,ORANGE),txt('발산',27,ORANGE)).arrange(DOWN,buff=.3).move_to([-1.95,-1.8,0])
        goodfunction=VGroup(math(r'\frac1{1-2}=-1',40,WEIGHT),txt('함수값은 계산 가능',25,WEIGHT)).arrange(DOWN,buff=.3).move_to([1.95,-1.8,0])
        self.play(FadeIn(at2),FadeIn(badsum),FadeIn(goodfunction),run_time=.8)
        warning=txt('발산하는 합이 −1이라는 뜻은 아닙니다',26,INK).move_to(DOWN*3.7)
        self.play(FadeIn(warning),run_time=.5)
        self.transition(102)
        self.subtitle('소수와 연결된 함수를 더 넓게 연구하려면', '입력 s를 복소수로 놓고, 함수의 구조를 살펴봅니다')
        sform=math(r's=\sigma+it',48).move_to(UP*4.2)
        self.play(Write(sform),run_time=.8)
        plane=Axes(x_range=[-1,3,1],y_range=[-3,30,5],x_length=6.7,y_length=6.1,
                   tips=False,axis_config={'color':MUTED}).move_to(DOWN*.2)
        def region(a,b,c):
            return Polygon(plane.c2p(a,-3),plane.c2p(b,-3),plane.c2p(b,30),plane.c2p(a,30),
                           stroke_width=0,fill_color=c,fill_opacity=.16)
        right=region(1,3,GOOD)
        boundary=DashedLine(plane.c2p(1,-3),plane.c2p(1,30),color=GOOD,stroke_width=2)
        labels=VGroup(*[txt(str(k),21,MUTED).next_to(plane.c2p(k,0),DOWN,buff=.13) for k in (0,1,2)],
            txt('Re(s)',22,MUTED).next_to(plane.c2p(3,0),DOWN,buff=.14),
            txt('Im(s)',22,MUTED).next_to(plane.c2p(0,30),UP,buff=.12),
            *[txt(str(k),20,MUTED).next_to(plane.c2p(0,k),LEFT,buff=.1) for k in (10,20,30)])
        self.play(FadeIn(right),Create(plane),Create(boundary),FadeIn(labels),run_time=1.2)
        domain=VGroup(txt('급수 · 곱의 영역',22,GOOD),
                      txt('이 영역에는 영점 없음',20,GOOD)).arrange(DOWN,buff=.25)
        domain.move_to(plane.c2p(2,26))
        dot=Dot(plane.c2p(2,0),radius=.09,color=ORANGE)
        pointlabel=math('s=2',32,ORANGE).next_to(dot,RIGHT,buff=.15)
        self.play(FadeIn(dot),FadeIn(pointlabel),run_time=.5)
        newlabel=math('s=2+8i',29,ORANGE).move_to(plane.c2p(2,8)+RIGHT*.2+DOWN*.45)
        self.play(dot.animate.move_to(plane.c2p(2,8)),ReplacementTransform(pointlabel,newlabel),run_time=1.2)
        self.to(107)
        self.subtitle('처음의 급수와 곱이 성립하는 영역', '실수부가 1보다 크며, 이 영역에는 영점이 없습니다')
        self.play(FadeIn(domain),run_time=.5)
        domainrule=math(r'\operatorname{Re}(s)>1',30,GOOD).move_to(DOWN*4.3)
        self.play(FadeIn(domainrule),run_time=.5)
        self.to(114)
        self.subtitle('급수가 수렴하지 않아도 함수를 연구할 수 있습니다', '급수의 수렴 범위가 함수의 연구 범위는 아닙니다')
        self.to(118)
        self.subtitle('해석적 연속: 같은 함수를 더 넓은 영역으로', '원래 영역의 값과 해석적 성질을 유지하며 이어갑니다')
        extended=region(-1,1,SPARSE)
        self.play(FadeIn(extended),FadeOut(dot),FadeOut(newlabel),run_time=1.5)
        extendedlabel=txt('해석적 연속',23,SPARSE).move_to(plane.c2p(-.05,27))
        pole=VGroup(Line(LEFT*.08+DOWN*.08,RIGHT*.08+UP*.08,color=RED),Line(LEFT*.08+UP*.08,RIGHT*.08+DOWN*.08,color=RED)).move_to(plane.c2p(1,0))
        polelabel=txt('s = 1: 제외',22,RED).move_to(plane.c2p(1,0)+DOWN*.85)
        self.play(FadeIn(extendedlabel),Create(pole),FadeIn(polelabel),run_time=.8)
        footer=VGroup(txt('s = 1을 제외한 복소평면으로 확장',24,SPARSE),
                      txt('확장한 영역에서 원래 급수·곱을 쓰지는 않습니다',21,MUTED)).arrange(DOWN,buff=.22).move_to(DOWN*4.4)
        self.play(ReplacementTransform(domainrule,footer),run_time=.5)
        self.to(127)
        self.subtitle('원래 급수와 곱을 그대로 쓰지는 않습니다', '새 영역에서는 해석적으로 이어진 함수를 다룹니다')
        self.to(131)
        self.subtitle('확장한 함수에서 만나는 영점', '복소수를 대입하는 것만으로 생겨나는 점은 아닙니다')
        strip=region(0,1,ORANGE)
        self.play(FadeIn(strip),FadeOut(domain),run_time=.6)
        critical=DashedLine(plane.c2p(.5,0),plane.c2p(.5,30),color=ORANGE,stroke_width=2)
        clabel=math(r'\sigma=\frac12',28,ORANGE).move_to(plane.c2p(.5,4)+LEFT*.65)
        self.play(Create(critical),FadeIn(clabel),run_time=.6)
        for height in ZEROS:
            point=Dot(plane.c2p(.5,height),color=ORANGE,radius=.085)
            lab=txt(f'{height:.3f}i',22,ORANGE).next_to(point,RIGHT,buff=.16)
            self.play(FadeIn(point,scale=1.8),FadeIn(lab),run_time=.5)
        zeroformula=math(r'\zeta\!\left(\frac12+it\right)=0',38,ORANGE).move_to(UP*4.2)
        self.play(ReplacementTransform(sform,zeroformula),run_time=.8)
        zeronote=VGroup(txt('임계띠  0 < Re(s) < 1',23,ORANGE),
                       txt('양의 허수부를 가진 첫 영점 3개 · 근삿값',22,MUTED)).arrange(DOWN,buff=.2).move_to(DOWN*4.4)
        self.play(ReplacementTransform(footer,zeronote),run_time=.5)
        self.to(136)
        self.subtitle('이 영점의 위치는 소수 분포의 오차와 연결됩니다', '왜 함수가 0인 곳이 소수의 개수와 연결될까요?')
        self.to(143)
        self.write_captions()

    def to(self, target):
        remaining = target - self.time
        if remaining < -.05:
            raise ValueError(f'TTS checkpoint exceeded: {self.time:.3f} > {target}')
        if remaining > 1e-6:
            self.wait(remaining)
        if abs(self.time - target) > .05:
            raise ValueError(f'TTS checkpoint missed: {self.time:.3f} != {target}')

    def transition(self, target):
        # Finish the fade at the supplied narration boundary.
        self.to(target - .7)
        self.wipe()

    def subtitle(self,a,b):
        if self.cues:
            self.cues[-1]['end']=self.time
        new=VGroup(txt(a,29,INK),txt(b,22,MUTED)).arrange(DOWN,buff=.24).move_to(DOWN*6.25)
        self.play(ReplacementTransform(self.cap,new) if self.cap.submobjects else FadeIn(new),run_time=.4)
        self.cap=new
        self.cues.append({'start':self.time-.4,'end':None,'text':a+'\n'+b})

    def wipe(self):
        old=[m for m in self.mobjects if m is not self.chrome and m is not self.cap]
        self.play(*[FadeOut(m) for m in old],run_time=.7)
        self.remove(*old)

    def write_captions(self):
        self.cues[-1]['end']=self.time
        def stamp(t):
            ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
            return f'{h:02}:{m:02}:{s:02},{ms:03}'
        content='\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(self.cues,1))+'\n'
        Path(__file__).with_name('screen_captions.srt').write_text(content,encoding='utf-8')
        timeline=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
        captions='\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(timeline,1))+'\n'
        Path(__file__).with_name('captions.srt').write_text(captions,encoding='utf-8')
