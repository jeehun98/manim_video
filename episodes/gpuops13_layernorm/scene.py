"""LayerNorm: moving data, merged statistics, and input reuse."""
import sys
from pathlib import Path
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import BG, INK, MUTED, WEIGHT, PRUNE, SPARSE, ACCENT, GOOD, txt
config.disable_caching=True
XS=[-2.4,-.8,.8,2.4]
def p(x,y): return np.array([x,y,0.])
def t(s,size=27,c=INK,w=7.6): return txt(s,size,c,w)
def tone(i): return ACCENT if i==0 else WEIGHT
def token(v,i=0,r=.43):
    return VGroup(Circle(r,color=tone(i),fill_color=BG,fill_opacity=1,stroke_width=2),t(v,27,INK,r*1.8))
def row(vals,y): return VGroup(*[token(v,i).move_to(p(XS[i],y)) for i,v in enumerate(vals)])
def route(points,c=MUTED):
    line=VMobject(stroke_color=c,stroke_width=2,stroke_opacity=.55)
    line.set_points_as_corners([p(*point) for point in points]); return line
def box(title,detail,x,y,w=3.0,h=1.25,c=GOOD):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,color=c,stroke_width=1.7,fill_color=BG,fill_opacity=1).move_to(p(x,y)),
                  t(title,23,c,w-.25).move_to(p(x,y+h*.27)),t(detail,25,INK,w-.25).move_to(p(x,y-h*.13)))
def state(n,mean,m2,x,y,w=3.0):
    return box('통계 카드',f'n {n} · μ {mean}\nM₂ {m2}',x,y,w,1.65,SPARSE)

class GPULayerNorm(Scene):
    DURATION=148
    def construct(self):
        self.stage=VGroup(); self.heading=VGroup(); self.note=VGroup()
        self.progress=Rectangle(width=.01,height=.035,fill_color=ACCENT,fill_opacity=1,stroke_width=0).move_to(p(-3.8,-7.36))
        self.add(t('GPU OPERATIONS / 13',20,MUTED).move_to(UP*7.3),
                 t('LayerNorm\n평균과 분산을 따로 모아야 할까?',29).move_to(UP*6.5),
                 Line(p(-3.8,5.82),p(3.8,5.82),color=MUTED,stroke_opacity=.35),self.progress)

        # 1 / 0–10: recenter/rescale, preserve element order.
        self.copy('한 벡터의 중심과 퍼짐을 맞춥니다','원소의 순서를 바꾸는 정렬이 아닙니다')
        inputs=row([2,4,6,8],3.25)
        self.show(VGroup(inputs,t('입력 x · 한 행의 4개 원소',24,WEIGHT).move_to(p(0,4.3))))
        stats=VGroup(box('중심 · 평균','5',-1.75,1.1),box('퍼짐 · 분산','5',1.75,1.1))
        self.to(2.0000);self.reveal(stats)
        out=row(['−1.34','−0.45','0.45','1.34'],-2)
        trails=VGroup(*[route([(x,2.8),(x,-2)]) for x in XS]);self.reveal(trails)
        movers=inputs.copy();self.add_stage(movers)
        self.play(*[movers[i].animate.move_to(out[i]) for i in range(4)],run_time=1.1)
        self.play(ReplacementTransform(movers,out),run_time=.4);self.stage.add(out)
        self.reveal(t('중심을 0 부근으로 · 퍼짐을 일정하게',26,GOOD).move_to(p(0,-3.6)))
        self.reveal(t('정규화 값 · 반올림 예시 · γ=1, β=0',22,MUTED).move_to(p(0,-4.4)))
        self.to(10.0000)

        # 2 / 10–19: mean reduction.
        self.copy('평균은 네 값이 함께 만들어야 합니다','여러 Thread의 부분 결과를 합치는 Reduction')
        src=row([2,4,6,8],3.3)
        labels=VGroup(*[t(f'T{i}',22,tone(i)).move_to(p(XS[i],4.15)) for i in range(4)])
        self.show(VGroup(src,labels))
        self.tree(src,[6,14],20)
        self.reveal(box('합 20 ÷ 개수 4','평균 μ = 5',0,-3.4,4.2))
        self.to(19.0000)

        # 3 / 19–26: mean broadcast and squared deviations.
        self.copy('평균 5를 각 원소에 돌려줍니다','자기 값 − 평균 → 차이를 제곱')
        src=row([2,4,6,8],1.4); shared=box('공유하는 평균','μ = 5',0,3.5,3.1)
        self.show(VGroup(src,shared))
        copies=VGroup(*[token(5,1,.3).move_to(p(0,3)) for _ in XS]);self.add_stage(copies)
        self.play(*[MoveAlongPath(copies[i],route([(0,3),(XS[i],2.35)])) for i in range(4)],run_time=1)
        self.play(FadeOut(copies),run_time=.15)
        dif=row(['−3','−1','1','3'],-.8);squares=row([9,1,1,9],-3)
        self.reveal(t('평균에서 떨어진 거리',24,MUTED).move_to(p(0,.1)))
        self.flow(src,dif);self.reveal(t('차이를 제곱',24,SPARSE).move_to(p(0,-1.9)));self.flow(dif,squares)
        self.to(26.0000)

        # 4 / 26–33: variance reduction.
        self.copy('제곱된 차이를 다시 모읍니다','분산 = 제곱 편차합 ÷ 원소 개수')
        src=row([9,1,1,9],3.3);self.show(VGroup(src,t('제곱된 차이',24,WEIGHT).move_to(p(0,4.2))))
        self.tree(src,[10,10],20)
        self.reveal(box('제곱 편차합 20 ÷ 4','분산 σ² = 5',0,-3.4,4.5))
        self.to(33.0000)

        # 5 / 33–43: output depends on global statistics.
        self.copy('이제 자기 값을 정규화할 수 있습니다','평균과 분산 · 같은 행 전체의 정보가 필요')
        src=row([2,4,6,8],3);out=row(['−1.34','−0.45','0.45','1.34'],-2.8)
        stats=box('모든 원소가 함께 사용','평균 5 · 분산 5',0,.5,5.0,1.6)
        self.show(VGroup(src,stats));self.flow(src,out)
        self.reveal(t('(xᵢ − μ) / √(σ² + ε)',31,SPARSE).move_to(p(0,-4.1)))
        self.reveal(t('ε는 작은 안정화 상수 · 수치는 근삿값',21,MUTED).move_to(p(0,-4.7)))
        self.to(43.0000)

        # 6 / 43–53: computational reuse is not necessarily another memory load.
        self.copy('같은 입력이 세 단계에 쓰입니다','데이터 재사용과 외부 메모리 재읽기는 다릅니다')
        stages=VGroup(box('1 · 평균','x의 합',0,3.1,4.7,c=WEIGHT),box('2 · 분산','x − 평균의 제곱',0,.6,4.7,c=SPARSE),box('3 · 정규화','평균 빼기 · 크기 조정',0,-1.9,4.7,c=GOOD))
        self.show(stages)
        v=token(2);v.move_to(p(-3.2,3.1));self.add_stage(v)
        for yy in [.6,-1.9]:
            line=route([(-3.2,v.get_y()),(-3.2,yy)],ACCENT);self.reveal(line,.15)
            self.play(MoveAlongPath(v,line),run_time=.8)
        self.reveal(t('계산에 다시 사용 ≠ 반드시 다시 LOAD',26,ACCENT).move_to(p(0,-3.8)))
        self.to(53.0000)

        # 7 / 53–63: deliberately naïve three-read implementation.
        self.copy('입력을 보관하지 않는 단순 구현이라면','세 번 읽기 예시 · 실제 구현의 필수 동작은 아님')
        mem=box('GPU Memory','x = [2, 4, 6, 8]',0,3.45,6,1.5,PRUNE)
        dest=VGroup(*[box(f'Read {i+1}',s,0,1-i*1.8,3.8,c=WEIGHT) for i,s in enumerate(['평균','분산','정규화'])])
        self.show(VGroup(mem,dest))
        for i,b in enumerate(dest):
            v=token(2);v.move_to(p(-2.6,3.25));self.add_stage(v)
            line=route([(-2.6,3.25),(-3.0,3.25),(-3,1-i*1.8),(-1.4,1-i*1.8)],PRUNE)
            self.reveal(line,.12);self.play(MoveAlongPath(v,line),run_time=.75);self.play(FadeOut(v),run_time=.1)
        self.reveal(t('입력 보관·캐시·구현에 따라 이동 비용은 달라짐',23,MUTED).move_to(p(0,-4.3)))
        self.to(63.0000)

        # 8 / 63–73: paired sum and sum of squares.
        self.copy('한 번 읽을 때 두 정보를 함께 모으면?','값의 합과 제곱합 · 두 정보를 묶은 집계')
        src=VGroup(*[box(f'T{i}',f'{v}  /  {v*v}',XS[i],3.0,1.4,1.5,tone(i)) for i,v in enumerate([2,4,6,8])])
        self.show(VGroup(src,t('값 x / 제곱 x²',24,MUTED).move_to(p(0,4.3))))
        pairs=VGroup(box('왼쪽 부분합','6 / 20',-1.7,.6,2.6,c=WEIGHT),box('오른쪽 부분합','14 / 100',1.7,.6,2.6,c=WEIGHT))
        lines=VGroup(*[route([(XS[i],2.25),(-1.7 if i<2 else 1.7,1.3)]) for i in range(4)]);self.reveal(lines)
        movers=src.copy();self.add_stage(movers)
        self.play(*[movers[i].animate.scale(.45).move_to(p(-1.7 if i<2 else 1.7,.6)) for i in range(4)],run_time=1)
        self.play(FadeOut(movers),FadeIn(pairs),run_time=.25);self.stage.add(pairs)
        self.to(67.1667)
        final=box('합 / 제곱합','20 / 120',0,-1.75,3.4,c=GOOD);self.flow_cards(pairs,final)
        self.reveal(t('평균 20/4 = 5    분산 120/4 − 5² = 5',25,SPARSE).move_to(p(0,-3.65)))
        self.to(73.0000)

        # 9 / 73–83: cancellation, no invented measured precision claim.
        self.copy('큰 수 두 개의 차이로 작은 분산을 구하면?','제곱합 방식은 반올림 오차에 민감할 수 있습니다')
        self.show(VGroup(t('[10000.1, 10000.2, 10000.3]',30,WEIGHT).move_to(p(0,3.6)),
                         box('제곱의 평균','약 100004000.0467',0,1.8,6,c=PRUNE),
                         box('평균의 제곱','약 100004000.0400',0,-.1,6,c=PRUNE)))
        self.to(75.7273)
        self.reveal(t('두 큰 값을 빼면',28,MUTED).move_to(p(0,-1.45)))
        small=box('실수 산술에서의 작은 분산','약 0.00667',0,-2.7,4.6,c=ACCENT);self.reveal(small)
        self.reveal(t('유효 자릿수 손실 위험 · dtype에 따라 다름',24,PRUNE).move_to(p(0,-4.15)))
        self.to(83.0000)

        # 10 / 83–94: make each state meaningful before introducing its notation.
        self.copy('숫자만 더하지 않고 통계 상태를 합칩니다','Welford 계열 · 부분 통계를 병렬로 병합 가능')
        a=state(2,3,2,-1.85,1.9);b=state(2,7,2,1.85,1.9)
        guide=VGroup(t('n = 개수   μ = 평균',26,SPARSE).move_to(p(0,-.1)),
                     t('M₂ = 각 그룹 평균에서의 제곱 편차합',24,MUTED).move_to(p(0,-.9)))
        self.show(VGroup(a,b,t('그룹 A: [2, 4]     그룹 B: [6, 8]',26,WEIGHT).move_to(p(0,3.6)),guide))
        self.to(86.9286)
        self.play(FadeOut(guide),run_time=.2)
        final=state(4,5,20,0,-2.7,4.5);self.flow_cards(VGroup(a,b),final)
        self.reveal(t('그룹 중심의 차이도 반영 · M₂: 2+2+16=20',24,ACCENT).move_to(p(0,-4.2)))
        self.to(94.0000)

        # 11 / 94–104: parallel merge tree, two statistics in one state.
        self.copy('작은 통계 카드들이 하나로 모입니다','함께 모인 최종 상태에서 평균과 분산을 얻습니다')
        leaves=VGroup(*[state(1,v,0,XS[i],3.1,1.45) for i,v in enumerate([2,4,6,8])])
        self.show(leaves)
        mid=VGroup(state(2,3,2,-1.8,.5),state(2,7,2,1.8,.5))
        for i in range(2):self.flow_cards(VGroup(leaves[2*i],leaves[2*i+1]),mid[i])
        final=state(4,5,20,0,-2.2,4);self.flow_cards(mid,final)
        self.reveal(t('평균 = 5      분산 = M₂ / n = 20 / 4 = 5',27,GOOD).move_to(p(0,-4.1)))
        self.to(104.0000)

        # 12 / 104–115: fused normalization, input retained where feasible.
        self.copy('통계를 얻고, 보관한 입력을 다시 사용합니다','한 행이 내부 자원에 들어가는 경우의 개념도')
        frame=RoundedRectangle(width=7.5,height=7.2,corner_radius=.2,color=GOOD).move_to(p(0,.25))
        src=row([2,4,6,8],2.4);norm=row(['−1.34','−0.45','0.45','1.34'],-.5)
        self.show(VGroup(frame,src,t('Fused kernel · 내부에 입력 보관',24,GOOD).move_to(p(0,3.45)),
                         box('행 통계','μ 5 · σ² 5',0,.95,4.3,.95,SPARSE)))
        self.flow(src,norm)
        affine=row(['−1.68','0.11','1.89','3.68'],-2.65)
        self.reveal(t('정규화 → 원소별 scale γ, bias β',24,MUTED).move_to(p(0,-1.55)))
        self.flow(norm,affine)
        self.reveal(t('예시: γ=2, β=1 · 최종 출력은 반올림',22,ACCENT).move_to(p(0,-4.1)))
        self.to(115.0000)

        # 13 / 115–126: same start and end, visible memory traffic difference.
        self.copy('같은 입력, 같은 출력, 다른 이동 경로','항상 한 kernel·한 번의 LOAD로 끝나는 것은 아닙니다')
        self.show(VGroup(t('Separate · 단계 분리의 예',27,PRUNE).move_to(p(0,4.0)),
                         t('Fused · 내부 재사용이 가능한 예',27,GOOD).move_to(p(0,-.35))))
        upper=VGroup(box('평균','μ',-2.2,2.65,1.65,c=WEIGHT),box('Memory','통계 저장/읽기',0,2.65,2.3,c=PRUNE),box('분산·정규화','출력 y',2.55,2.65,2.2,c=SPARSE))
        lower=box('한 kernel 안에서','행 통계 → 정규화 → γ, β',0,-1.8,6.9,1.8,GOOD)
        self.reveal(VGroup(upper,lower))
        top=token(2,r=.3).move_to(p(-3.5,1.4));low=top.copy().move_to(p(-3.5,-3));self.add_stage(top,low)
        a=route([(-3.5,1.4),(-2.2,1.4),(-2.2,2.65),(0,2.65),(0,1.4),(3.5,1.4)],PRUNE)
        b=route([(-3.5,-3),(0,-3),(3.5,-3)],GOOD);self.reveal(VGroup(a,b))
        self.play(MoveAlongPath(top,a),MoveAlongPath(low,b),run_time=2.1)
        self.play(Transform(top,token('y',r=.3).move_to(top)),Transform(low,token('y',r=.3).move_to(low)),run_time=.3)
        self.reveal(t('큰 입력은 레지스터·공유 메모리 한계도 고려',23,MUTED).move_to(p(0,-4.35)))
        self.to(126.0000)

        # 14 / 126–137: relation to previous videos.
        self.copy('LayerNorm은 같은 행 전체를 봐야 합니다','서로 다른 행은 병렬로 처리할 수 있습니다')
        panels=VGroup(box('ReLU','자기 입력 하나',0,3,6,1.5,WEIGHT),box('Softmax','행 전체의 Max와 Sum',0,.65,6,1.5,SPARSE),box('LayerNorm','행 전체의 평균과 분산',0,-1.7,6,1.5,GOOD))
        self.show(panels)
        for i,c in enumerate([WEIGHT,SPARSE,GOOD]):
            circles=VGroup(*[Dot(p(-2.4+j*1.6,2.02-i*2.35),radius=.065,color=c) for j in range(4)])
            self.reveal(circles,.2)
            if i>0:self.play(*[circles[j].animate.move_to(p(0,2.02-i*2.35)) for j in range(4)],run_time=.65)
        self.to(137.0000)

        # 15 / 137–148: compact visual recall.
        self.copy('통계를 함께 모으고, 입력을 재사용합니다','필요한 통계는 계산하고, 불필요한 이동은 줄입니다')
        src=row([2,4,6,8],3);stats=box('병렬로 모은 행 통계','평균 5 · 분산 5',0,.55,5,1.6,SPARSE)
        out=row(['−1.34','−0.45','0.45','1.34'],-2.25)
        self.show(VGroup(src,stats,t('입력 x',24,WEIGHT).move_to(p(0,4.1))))
        movers=src.copy();self.add_stage(movers)
        self.play(*[movers[i].animate.scale(.5).move_to(stats) for i in range(4)],run_time=1)
        self.play(FadeOut(movers),Indicate(stats,color=ACCENT),run_time=.6)
        self.flow(src,out)
        self.reveal(t('통계 병렬화 + 수치 안정성 + 데이터 재사용',26,GOOD).move_to(p(0,-3.7)))
        self.reveal(t('정규화 예시 · γ=1, β=0',22,MUTED).move_to(p(0,-4.4)))
        self.to(148.0000)

    def tree(self,src,pair_values,total):
        mids=VGroup(token(pair_values[0]).move_to(p(-1.6,.9)),token(pair_values[1],1).move_to(p(1.6,.9)))
        lines=VGroup(*[route([(XS[i],3.3),(-1.6 if i<2 else 1.6,.9)]) for i in range(4)])
        self.reveal(lines,.2);self.bring_to_back(lines)
        movers=src.copy();self.add_stage(movers)
        self.play(*[MoveAlongPath(movers[i],lines[i]) for i in range(4)],run_time=1)
        self.play(FadeOut(movers),FadeIn(mids),run_time=.25);self.stage.add(mids)
        final=token(total,r=.53).move_to(p(0,-1.35))
        self.flow_cards(mids,final)

    def flow_cards(self,src,dest):
        movers=src.copy();self.add_stage(movers)
        lines=VGroup(*[route([(obj.get_x(),obj.get_y()),(dest.get_x(),dest.get_y())]) for obj in src])
        self.reveal(lines,.12);self.bring_to_back(lines)
        self.play(*[MoveAlongPath(movers[i],lines[i]) for i in range(len(src))],run_time=.85)
        self.play(FadeOut(movers),FadeIn(dest),run_time=.25);self.stage.add(dest)

    def flow(self,src,dest):
        lines=VGroup(*[route([(src[i].get_x(),src[i].get_y()),(dest[i].get_x(),dest[i].get_y())]) for i in range(4)])
        self.reveal(lines,.12);self.bring_to_back(lines);movers=src.copy();self.add_stage(movers)
        self.play(*[MoveAlongPath(movers[i],lines[i]) for i in range(4)],run_time=.9)
        self.play(FadeOut(movers),FadeIn(dest),run_time=.25);self.stage.add(dest)

    def add_stage(self,*objs):self.stage.add(*objs);self.add(*objs)
    def copy(self,heading,note):
        self.play(FadeOut(VGroup(self.heading,self.note)),run_time=.1)
        self.heading=t(heading,29).move_to(UP*5.12);self.note=t(note,22,ACCENT).move_to(DOWN*5.35)
        self.play(FadeIn(self.heading),FadeIn(self.note),run_time=.22)
    def show(self,obj):
        if len(self.stage):self.play(FadeOut(self.stage),run_time=.18)
        self.stage=obj;self.play(FadeIn(obj),run_time=.4)
    def reveal(self,obj,d=.22):self.stage.add(obj);self.play(FadeIn(obj),run_time=d)
    def to(self,target):
        remaining=target-self.time
        if remaining<-.04:raise ValueError(f'Timeline overrun at {target}: {self.time:.3f}')
        if remaining>1e-6:
            width=max(.01,7.6*target/self.DURATION)
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(p(-3.8+width/2,-7.36)),run_time=min(.12,remaining))
            remaining=target-self.time
            if remaining>1e-6:self.wait(remaining)
