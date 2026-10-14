"""Different positions, shared nearest-neighbor spacing statistics."""
import json
from pathlib import Path
import numpy as np
from manim import *
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from episodes.discover03_prime_waves.scene import PrimeWavesDiscovery
from episodes.discover02_euler_product.scene import math,ORANGE
from episodes.prune_series.visuals import txt,INK,MUTED,WEIGHT,GOOD,SPARSE


class SpacingPatternsDiscovery(PrimeWavesDiscovery):
    def construct(self):
        self.d=json.loads(Path(__file__).with_name('spacing_data.json').read_text(encoding='utf-8'))
        self.meta=self.d['metadata'];self.cues=[];self.cap=VGroup()
        self.chrome=VGroup(txt('수학적 발견  /  04',22,MUTED).move_to(UP*7.25),
            txt('불규칙한 점들 사이에',37).move_to(UP*6.5),
            txt('같은 질서가 숨어 있다면?',35).move_to(UP*5.8))
        self.add(self.chrome)
        self.subtitle('숫자선 위에 점들을 흩뿌려보겠습니다','어떤 점은 멀리, 어떤 점은 아주 가까이')
        rng=np.random.default_rng(20261014)
        random_positions=np.sort(rng.uniform(0,24,24))
        random_positions=(random_positions-random_positions[0])/np.mean(np.diff(random_positions))
        # A fixed, disclosed data window, not a hand-designed repulsive arrangement.
        import re
        source=Path(__file__).with_name('zeros3.txt').read_text(encoding='ascii').splitlines()
        offsets=np.array([float(line) for line in source if re.fullmatch(r'\s*\d+\.\d+\s*',line)])
        raw=np.diff(offsets[100:124])
        mid=(offsets[101:124]+offsets[100:123])/2+self.meta['base_height']
        normalized=raw*np.log(mid/(2*np.pi))/(2*np.pi)
        normalized/=normalized.mean()
        zero_positions=np.r_[0,np.cumsum(normalized)]
        scale=6.8/23
        def row(values,y,color):
            return VGroup(Line([-3.4,y,0],[3.4,y,0],color=MUTED),
                VGroup(*[Dot([-3.4+float(v)*scale,y,0],radius=.06,color=color) for v in values]))
        random_row=row(random_positions,2.2,SPARSE)
        zero_row=row(zero_positions,-.4,WEIGHT)
        random_name=txt('독립적인 무작위 점',27,SPARSE).move_to(UP*3.2)
        other_name=txt('또 다른 배열',27,WEIGHT).move_to(UP*.6)
        self.play(Create(random_row[0]),FadeIn(random_name),run_time=.5)
        self.play(LaggedStart(*[FadeIn(m) for m in random_row[1]],lag_ratio=.06),run_time=1.8)
        self.to(3)
        closest=np.argsort(np.diff(random_positions))[:2]
        markers=VGroup(*[SurroundingRectangle(VGroup(random_row[1][j],random_row[1][j+1]),color=GOOD,buff=.11) for j in closest])
        self.play(Create(markers),run_time=.6)
        mean_note=txt('배열 예시 · 두 배열의 평균 간격을 1로 맞춰 비교',21,MUTED).move_to(DOWN*3.9)
        self.play(FadeIn(mean_note),run_time=.5)
        self.to(7)
        self.subtitle('이번에는 다른 점들을 놓아보겠습니다','겉보기에는 역시 불규칙합니다')
        self.play(Create(zero_row[0]),FadeIn(other_name),run_time=.5)
        self.play(LaggedStart(*[FadeIn(m) for m in zero_row[1]],lag_ratio=.06),run_time=1.8)
        self.to(11)
        self.subtitle('그런데, 아주 가까이 붙은 경우가 상대적으로 드뭅니다','점들의 위치보다 점들 사이의 관계를 봅니다')
        small=txt('짧은 간격에 주목',29,GOOD).move_to(DOWN*2.2)
        self.play(FadeIn(small),run_time=.5)
        self.to(18)
        self.subtitle('점들이 실제로 서로 밀어내는 것은 아닙니다','간격에 특별한 통계적 규칙이 있는 것입니다')
        self.to(24.5)
        self.play(FadeOut(random_row),FadeOut(random_name),FadeOut(markers),FadeOut(small),FadeOut(mean_note),run_time=.5)
        self.subtitle('이 점들의 정체를 공개하겠습니다','바로, 리만 제타 함수의 영점입니다')
        name=txt('리만 제타 함수의 영점',32,WEIGHT).move_to(UP*2.7)
        self.play(ReplacementTransform(other_name,name),zero_row.animate.shift(UP*1.6),run_time=1)
        self.play(FadeIn(txt('실제 영점 데이터 · 10¹²번째 부근',24,MUTED).move_to(DOWN*.2)),run_time=.5)
        link=VGroup(txt('영점의 위치',28,WEIGHT),txt('↓',30,MUTED),txt('소수 분포의 불규칙한 흔들림',28,INK)).arrange(DOWN,buff=.3).move_to(DOWN*2.2)
        self.to(29)
        self.subtitle('지난 영상: 영점의 위치와 소수 분포의 흔들림','이번에는 영점들 사이의 관계를 바라봅니다')
        self.play(FadeIn(link),run_time=.7)
        self.transition(35)

        self.subtitle('영점 사이의 간격을 모아보면','위치는 달라도, 간격에는 질서가 나타납니다')
        a,labels=self.distribution_axes()
        bars=self.histogram(a,self.d['zero_hist'],WEIGHT,.52)
        self.play(Create(a),FadeIn(labels),LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.06),run_time=1.5)
        legend=txt('● 실제 영점 · 9,999개 간격',24,WEIGHT).move_to(UP*3.9)
        self.play(FadeIn(legend),run_time=.5)
        normalization=txt('평균 간격 = 1로 정규화',25,GOOD).move_to(DOWN*3.8)
        self.play(FadeIn(normalization),run_time=.5)
        self.to(40)
        self.subtitle('전혀 다른 대상의 간격을 겹쳐보겠습니다','무작위 행렬의 고유값들입니다')
        model=self.histogram(a,self.d['gue_hist'],ORANGE,0,stroke=2.4)
        self.play(LaggedStart(*[Create(m) for m in model],lag_ratio=.06),run_time=1.5)
        legend2=VGroup(txt('● 실제 제타 영점  9,999개 간격',23,WEIGHT),
                       txt('● GUE 고유값  9,500개 간격',23,ORANGE)).arrange(DOWN,buff=.2).move_to(UP*3.9)
        self.play(ReplacementTransform(legend,legend2),run_time=.5)
        self.play(Create(self.theory_curve(a,INK)),run_time=1.2)
        self.play(FadeIn(txt('흰 점선: GUE 이론의 수치 계산',22,MUTED).move_to(DOWN*4.55)),run_time=.5)
        self.to(46)
        self.subtitle('같은 기준으로 보면, 비슷한 분포가 드러납니다','개별 숫자가 아니라, 그 사이의 간격을 비교한 결과')
        self.to(51)
        self.subtitle('일부 양자계의 에너지 준위에도 쓰이는 통계','GUE는 특정한 양자 혼돈계를 설명하는 통계 모형')
        self.play(FadeIn(txt('GUE 표본은 양자계 실측이 아님 · 모든 양자계에 적용되지 않음',20,MUTED).move_to(UP*4.85)),run_time=.5)
        self.to(57)
        self.subtitle('소수와 연결된 영점, 양자계에 쓰이는 통계 모형','서로 다른 두 세계의 간격을 비교합니다')
        self.transition(62)

        self.subtitle('서로 다른 세계에서 발견한 작은 간격의 억제','아주 가까운 간격이 드물게 나타나는 비슷한 질서')
        a,labels=self.distribution_axes()
        t=np.linspace(0,3,500)
        independent=self.polyline(a,t,np.exp(-t),SPARSE)
        gue=self.theory_curve(a,ORANGE,dashed=False)
        self.play(Create(a),FadeIn(labels),Create(independent),Create(gue),run_time=1.4)
        legend=VGroup(txt('● 독립적인 점 배치 · 이론',23,SPARSE),txt('● GUE · 이론 수치 계산',23,ORANGE)).arrange(DOWN,buff=.2).move_to(UP*3.8)
        self.play(FadeIn(legend),FadeIn(self.small_region(a)),run_time=.5)
        self.play(FadeIn(txt('아주 작은 간격이 상대적으로 드뭅니다',27,GOOD).move_to(DOWN*3.9)),run_time=.5)
        zpercent=self.meta['zero_small_gap_fraction']*100
        ppercent=self.meta['poisson_small_gap_fraction']*100
        numbers=txt(f'간격 < 0.3: 영점 자료 {zpercent:.1f}% / 독립 이론 {ppercent:.1f}%',22,MUTED).move_to(DOWN*4.75)
        self.play(FadeIn(numbers),run_time=.5)
        self.to(68)
        self.subtitle('이 특징을 레벨 반발이라고 부릅니다','아주 작은 간격이 상대적으로 억제되는 통계적 성질')
        self.to(71)
        self.subtitle('레벨 반발은 통계적 성질입니다','실제로 힘을 주고받는다는 뜻은 아닙니다')
        self.transition(78)

        self.subtitle('비슷한 통계가 동일한 대상을 뜻하지는 않습니다','리만 가설이 증명된 것도 아닙니다')
        rows=self.point_rows()
        self.play(FadeIn(rows),run_time=1)
        a,labels=self.distribution_axes(height=2.6)
        a.shift(DOWN*1.45);labels.shift(DOWN*1.45)
        bars=self.histogram(a,self.d['zero_hist'],WEIGHT,.4)
        theory=self.theory_curve(a,ORANGE,dashed=False)
        self.play(Create(a),FadeIn(labels),FadeIn(bars),Create(theory),run_time=1.2)
        self.play(FadeIn(txt('통계적 유사성 ≠ 동일성 · 수치적 관찰',23,MUTED).move_to(DOWN*4.5)),run_time=.5)
        self.to(84)
        self.subtitle('왜 닮았는지는 아직 완전히 이해하지 못합니다','영점 통계와 GUE의 관계에는 미해결 문제가 남습니다')
        self.to(88)
        self.subtitle('닮은 패턴을 발견한 순간, 새로운 관점이 생깁니다','서로 다른 문제를 같은 관점에서 바라볼 수 있게 됩니다')
        self.to(94)
        self.subtitle('숫자 자체를 넘어, 숫자들 사이의 관계로','관계를 보기 시작했을 때 새로운 규칙이 드러났습니다')
        self.to(99)
        self.write_captions()

    def distribution_axes(self,height=4.4):
        a=Axes(x_range=[0,3,.5],y_range=[0,1.2,.2],x_length=6.6,y_length=height,
               tips=False,axis_config={'color':MUTED}).move_to(DOWN*.3)
        labels=VGroup(*[txt(f'{x:g}',21,MUTED).next_to(a.c2p(x,0),DOWN,buff=.12) for x in np.arange(0,3.01,.5)],
            txt('정규화 간격',23,MUTED).next_to(a,DOWN,buff=.5),
            txt('확률 밀도',20,MUTED).next_to(a.c2p(0,1.2),UP,buff=.12))
        return a,labels

    def histogram(self,a,density,color,opacity,stroke=1):
        edges=np.array(self.d['edges']);bars=VGroup()
        for lo,hi,h in zip(edges[:-1],edges[1:],density):
            bottom=a.c2p(lo,0);top=a.c2p(hi,h)
            b=Rectangle(width=top[0]-bottom[0],height=max(.002,top[1]-bottom[1]),
                        color=color,stroke_width=stroke,fill_color=color,fill_opacity=opacity)
            b.move_to((bottom+top)/2);bars.add(b)
        return bars

    def theory_curve(self,a,color,dashed=True):
        t=np.array(self.d['theory_x']);p=np.array(self.d['theory_y']);keep=t<=3
        path=self.polyline(a,t[keep],p[keep],color,2.4)
        return DashedVMobject(path,num_dashes=55) if dashed else path

    def small_region(self,a):
        return Polygon(a.c2p(0,0),a.c2p(.3,0),a.c2p(.3,1.2),a.c2p(0,1.2),
                       stroke_width=0,fill_color=GOOD,fill_opacity=.12)

    def point_rows(self):
        zg=np.array(self.d['zero_row']);gg=np.array(self.d['gue_row'])
        zs=np.r_[0,np.cumsum(zg)];gs=np.r_[0,np.cumsum(gg)]
        scale=6.6/max(zs[-1],gs[-1])
        group=VGroup()
        for values,y,color,name in ((zs,3.5,WEIGHT,'실제 영점'),(gs,2.25,ORANGE,'GUE 모형')):
            group.add(txt(name,23,color).move_to([0,y+.45,0]),Line([-3.3,y,0],[3.3,y,0],color=MUTED),
                      VGroup(*[Dot([-3.3+float(v)*scale,y,0],color=color,radius=.055) for v in values]))
        return group

    def write_captions(self):
        self.cues[-1]['end']=self.time
        def stamp(t):
            ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
            return f'{h:02}:{m:02}:{s:02},{ms:03}'
        out='\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(self.cues,1))+'\n'
        Path(__file__).with_name('screen_captions.srt').write_text(out,encoding='utf-8')
        timeline=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
        narration='\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(timeline,1))+'\n'
        Path(__file__).with_name('captions.srt').write_text(narration,encoding='utf-8')
        Path(__file__).with_name('screen_timing.json').write_text(json.dumps(self.cues,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
