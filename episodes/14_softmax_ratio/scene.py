"""Softmax 03 — input differences become output ratios. 80 seconds."""
import os
import numpy as np
from manim import *

config.pixel_width = int(os.getenv('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#091119'
INK, MUTED, MINT = '#EDF3F7', '#94A7B7', '#61E4CF'
BLUE, GOLD, PINK = '#68D9F0', '#F3CF75', '#FF8C9D'
DURATION = 80
CAPTIONS = [
 (0, '앞에서 Softmax는 숫자의 절대적인 크기보다\n값들 사이의 차이를 본다고 했습니다.'),
 (5.5, '그렇다면 그 차이는\n결과에 얼마나 큰 영향을 줄까요?'),
 (9, '두 개의 입력값 xᵢ와 xⱼ를 생각해보겠습니다.'),
 (13, 'Softmax를 적용한 결과를\n각각 pᵢ, pⱼ라고 하면,'),
 (17, '두 출력의 비율은\ne의 xᵢ제곱을 e의 xⱼ제곱으로 나눈 값입니다.'),
 (22.5, '분모에 있던 전체 합은\n서로 약분되기 때문입니다.'),
 (26, '지수법칙을 이용하면, 두 입력의 차이가\n그대로 e의 지수가 됩니다.'),
 (32, '즉 두 입력의 차이가 1이라면,\n출력의 비율은 약 2.7배가 됩니다.'),
 (37, '차이가 2라면\n약 7.4배가 됩니다.'),
 (40.5, '차이가 3이라면\n약 20배까지 벌어집니다.'),
 (44, '입력에서는 단지\n1, 2, 3만큼의 차이였지만,'),
 (48, 'Softmax 안에서는 이 차이가\n지수적인 비율로 바뀝니다.'),
 (52.5, '그래서 Softmax는 단순히 값들을\n합이 1이 되도록 나누는 함수가 아닙니다.'),
 (58, '입력값 사이의 차이를\n상대적인 비중의 차이로 변환합니다.'),
 (62.5, '그리고 이 성질 때문에\n입력값들을 같은 배율로 조절하면,'),
 (67, '값 사이의 간격이 바뀌면서\n분포의 모양도 크게 달라질 수 있습니다.'),
 (72, '다음에는 이 성질을 이용해서\nSoftmax의 분포를 더 뾰족하게 만들거나\n더 평평하게 만드는 방법을 살펴보겠습니다.'),
]

def txt(s, size=29, color=INK):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if m.width>7.5: m.scale_to_fit_width(7.5)
    return m

def exp(power,color=INK):
    base=txt('e',40,color)
    exponent=txt(power,23,color).next_to(base,UR,buff=.02).shift(DOWN*.1)
    return VGroup(base,exponent)

def frac(top,bottom):
    line=Line(LEFT,RIGHT,color=INK).set_width(max(top.width,bottom.width)+.3)
    top.next_to(line,UP,buff=.14);bottom.next_to(line,DOWN,buff=.14)
    return VGroup(top,line,bottom)

def inline(*parts): return VGroup(*parts).arrange(RIGHT,buff=.25)

def ratio(): return frac(txt('pᵢ',38,BLUE),txt('pⱼ',38,PINK))

def probability_bars(d):
    p=1/(1+np.exp(-d))
    bars=VGroup()
    for y,v,c,label in [(0,p,BLUE,'pᵢ'),(-1.05,1-p,PINK,'pⱼ')]:
        bars.add(txt(label,28,c).move_to([-3.25,y,0]))
        bars.add(Rectangle(width=5.2*v,height=.42,stroke_width=0,fill_color=c,fill_opacity=.9).move_to([-2.65+2.6*v,y,0]))
        bars.add(txt(f'{v:.3f}',25,c).move_to([3.2,y,0]))
    return bars

class SoftmaxRatio(Scene):
    def until(self,t):
        if self.time>t+.05: raise ValueError(f'Timing overrun {self.time} > {t}')
        if t>self.time: self.wait(t-self.time)
    def cue(self,i):
        self.until(CAPTIONS[i][0])
        new=txt(CAPTIONS[i][1]).move_to(DOWN*5.85)
        self.play(FadeOut(self.sub),FadeIn(new),run_time=.2);self.sub=new
    def heading(self,s):
        self.play(Transform(self.head,txt(s,31,MINT).move_to(UP*3.65)),run_time=.3)
    def construct(self):
        self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.85)
        self.head=txt('입력의 차이가 만드는 비중',31,MINT).move_to(UP*3.65)
        self.add(txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85),txt('Softmax',66).move_to(UP*5.65),
                 txt('03  /  차이가 비율이 되는 이유',25,MINT).move_to(UP*4.65),self.head,self.sub)
        intro=VGroup(txt('입력의 차이',38,BLUE),txt('↓  Softmax',28,MUTED),txt('출력의 비율',38,GOLD)).arrange(DOWN,buff=.5).move_to(UP*.4)
        self.play(FadeIn(intro),run_time=.6)
        self.cue(1);self.heading('차이가 1 커지면, 비율은?')
        self.cue(2)
        self.play(FadeOut(intro),run_time=.3)
        inputs=VGroup(txt('xᵢ',48,BLUE).move_to(LEFT*2+UP*2),txt('xⱼ',48,PINK).move_to(RIGHT*2+UP*2))
        self.play(FadeIn(inputs),run_time=.4)
        self.cue(3)
        outputs=VGroup(txt('↓',30,MUTED).move_to(LEFT*2+UP*.9),txt('↓',30,MUTED).move_to(RIGHT*2+UP*.9),
                       txt('pᵢ',48,BLUE).move_to(LEFT*2),txt('pⱼ',48,PINK).move_to(RIGHT*2))
        self.play(FadeIn(outputs),run_time=.4)
        self.cue(4)
        self.play(FadeOut(inputs),FadeOut(outputs),run_time=.3)
        short=inline(ratio(),txt('=',36),frac(exp('xᵢ',BLUE),exp('xⱼ',PINK))).move_to(UP*.7)
        self.play(FadeIn(short),run_time=.5)
        self.cue(5)
        self.heading('같은 전체 합 S가 약분됩니다')
        self.play(FadeOut(short),run_time=.2)
        fi=frac(exp('xᵢ',BLUE),txt('S',33,GOLD))
        fj=frac(txt('S',33,GOLD),exp('xⱼ',PINK))
        expanded=inline(ratio(),txt('=',36),fi,txt('×',33),fj).move_to(UP*.6)
        sumdef=inline(txt('S = Σₖ',30,GOLD),exp('xₖ')).move_to(DOWN*2.1)
        self.play(FadeIn(expanded),FadeIn(sumdef),run_time=.4)
        slashes=VGroup(*[Line(m.get_corner(DL),m.get_corner(UR),color=PINK,stroke_width=4) for m in [fi[2],fj[0]]])
        self.play(Create(slashes),run_time=.45)
        self.play(FadeOut(slashes),FadeOut(expanded),FadeIn(short),run_time=.4)
        self.cue(6)
        self.heading('입력의 차이 → 지수적인 비율')
        result=inline(ratio(),txt('=',36),exp('xᵢ − xⱼ',GOLD)).move_to(UP*.7)
        self.play(ReplacementTransform(short,result),FadeOut(sumdef),run_time=.5)
        difference=txt('Δ = xᵢ − xⱼ',32,BLUE).move_to(DOWN*1.3)
        self.play(FadeIn(difference),run_time=.3)
        self.cue(7)
        self.play(FadeOut(result),FadeOut(difference),run_time=.3)
        self.heading('차이 1 → 약 2.7배')
        rule=inline(txt('pᵢ / pⱼ =',32),exp('1',GOLD),txt('≈ 2.7',38,GOLD)).move_to(UP*2.2)
        chart=probability_bars(1)
        note=txt('두 입력만 있는 예: [Δ, 0]',23,MUTED).move_to(DOWN*2.1)
        sumone=txt('막대: 출력 비중 · 두 출력의 합 = 1',22,MUTED).move_to(DOWN*2.9)
        self.play(FadeIn(rule),FadeIn(chart),FadeIn(note),FadeIn(sumone),run_time=.5)
        self.cue(8)
        self.heading('차이 2 → 약 7.4배')
        self.play(Transform(rule,inline(txt('pᵢ / pⱼ =',32),exp('2',GOLD),txt('≈ 7.4',38,GOLD)).move_to(rule)),Transform(chart,probability_bars(2)),run_time=.7)
        self.cue(9)
        self.heading('차이 3 → 약 20배')
        self.play(Transform(rule,inline(txt('pᵢ / pⱼ =',32),exp('3',GOLD),txt('≈ 20.1',38,GOLD)).move_to(rule)),Transform(chart,probability_bars(3)),run_time=.7)
        self.cue(10)
        self.play(*[FadeOut(m) for m in [rule,chart,note,sumone]],run_time=.3)
        self.heading('차이는 일정하게, 비율은 지수적으로')
        table=VGroup()
        table.add(txt('입력 차이 Δ',27,BLUE).move_to([-1.8,2.3,0]),txt('출력 비율',27,GOLD).move_to([1.8,2.3,0]))
        for y,d,v in [(1.2,1,'2.7배'),(0,2,'7.4배'),(-1.2,3,'20.1배')]:
            table.add(txt(str(d),38,BLUE).move_to([-1.8,y,0]),txt('→',29,MUTED).move_to([0,y,0]),txt(v,38,GOLD).move_to([1.8,y,0]))
        self.play(FadeIn(table),run_time=.5)
        self.cue(11)
        growth=txt('차이 +1마다, 비율은 ×e',31,MINT).move_to(DOWN*3)
        self.play(FadeIn(growth),run_time=.4)
        self.cue(12)
        self.play(FadeOut(table),FadeOut(growth),run_time=.3)
        self.heading('지수함수 적용 후, 합으로 나눕니다')
        flow=VGroup(txt('입력 점수',34,BLUE),txt('↓  지수함수',29,GOLD),txt('양수 가중치',34,GOLD),txt('↓  전체 합으로 나누기',29,MUTED),txt('합이 1인 분포',34,MINT)).arrange(DOWN,buff=.32).move_to(UP*.2)
        self.play(FadeIn(flow),run_time=.5)
        self.cue(13)
        self.play(Indicate(flow[1]),run_time=.6)
        self.cue(14)
        self.play(FadeOut(flow),run_time=.3)
        self.heading('같은 배율을 곱하면, 간격이 달라집니다')
        scale=txt('[0, 1, 2]  × 2  →  [0, 2, 4]',32,BLUE).move_to(UP*2)
        gaps=txt('인접한 차이 1 → 2',29,GOLD).move_to(UP*.8)
        self.play(FadeIn(scale),FadeIn(gaps),run_time=.5)
        self.cue(15)
        distributions=VGroup()
        for y,values,label in [(-.6,[0.,1.,2.],'×1'),(-2.,[0.,2.,4.],'×2')]:
            p=np.exp(values-np.max(values));p/=p.sum();left=-2.7
            distributions.add(txt(label,24,MUTED).move_to([-3.3,y,0]))
            for v,c in zip(p,[BLUE,GOLD,PINK]):
                w=5.8*v
                distributions.add(Rectangle(width=w,height=.55,stroke_width=0,fill_color=c,fill_opacity=.9).move_to([left+w/2,y,0]));left+=w
        self.play(FadeIn(distributions),run_time=.5)
        self.cue(16)
        self.play(*[FadeOut(m) for m in [scale,gaps,distributions]],run_time=.3)
        self.heading('NEXT  /  분포의 뾰족함을 조절하기')
        end=VGroup(txt('더 뾰족하게',38,PINK),txt('↕',32,MUTED),txt('더 평평하게',38,BLUE)).arrange(DOWN,buff=.5).move_to(UP*.3)
        self.play(FadeIn(end),run_time=.5)
        self.until(DURATION)
