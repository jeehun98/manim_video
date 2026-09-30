"""GMM likelihood is unbounded along a single-component variance collapse."""
import sys
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT,GOOD,INK,MUTED,PRUNE,WEIGHT,txt
from episodes.dist17_gmm_singularity.content import CUES,DURATION

DATA=np.array([-2,-1.5,-1,-.7,-.2,.15,.4,.65,.9,1.2,1.6,2])
MU=.4
PI=1/12


def normal(x,mu,sigma):
    return np.exp(-.5*((np.asarray(x)-mu)/sigma)**2)/(np.sqrt(2*np.pi)*sigma)


def mixture(x,sigma):
    return PI*normal(x,MU,sigma)+(1-PI)*normal(x,0,1.3)


def score(sigma):
    return float(np.log(mixture(DATA,sigma)).sum())


class GMMSingularityDiscovery(Scene):
    DURATION=DURATION

    def construct(self):
        self.stage,self.head,self.caption=VGroup(),VGroup(),VGroup()
        self.add(VGroup(
            txt('PART IV  /  DISTRIBUTION MATHEMATICS 17',18,MUTED).move_to(UP*7.3),
            txt('학습 점수를 무한히 올릴 수 있다면? | GMM Singularity',27,INK,7.7).move_to(UP*6.48),
            Line([-3.8,5.83,0],[3.8,5.83,0],color=MUTED,stroke_opacity=.35),
        ))
        self.progress=Rectangle(width=.01,height=.035,fill_color=ACCENT,fill_opacity=1,stroke_width=0).move_to([-3.8,-7.36,0])
        self.add(self.progress)

        self.copy('점수가 높을수록 좋은 모델?', 'Likelihood ↑')
        graph=self.density_graph(.6,kind='mixture')
        self.show(graph,FadeIn(graph),run_time=.6)
        self.to(CUES[0][1])

        self.copy('한 성분의 평균을 한 점에 맞춥니다','μ = xᵢ')
        self.clear_stage()
        graph=self.density_graph(1)
        self.show(graph,FadeIn(graph),run_time=.6)
        self.to(CUES[1][1])

        self.copy('거리 때문에 생기는 감소가 사라집니다','xᵢ − μ = 0')
        self.clear_stage()
        formula=VGroup(
            txt('xᵢ − μ = 0',43,ACCENT).move_to([0,2,0]),
            txt('exp[ −(xᵢ−μ)² / (2σ²) ]',37,INK,7.2).move_to([0,.1,0]),
            txt('= 1',46,GOOD).move_to([0,-1.7,0]),
        )
        self.show(formula,FadeIn(formula),run_time=.6)
        self.to(CUES[2][1])

        self.copy('폭은 좁아지고 높이는 커집니다','σ는 표준편차  /  분산은 σ²')
        self.clear_stage()
        graph=self.density_graph(1)
        self.show(graph,FadeIn(graph),run_time=.3)
        for sigma in (.3,.1,.01):
            self.play(Transform(graph,self.density_graph(sigma)),run_time=.6)
        self.to(CUES[3][1])

        self.copy('이 한 점의 밀도는 끝없이 커집니다','σ → 0⁺  ⇒  component density → ∞')
        self.clear_stage()
        peak=VGroup(
            txt('N(xᵢ | xᵢ, σ²)',39,GOOD).move_to([0,2.2,0]),
            txt('= 1 / (√(2π) σ)',41,INK).move_to([0,.4,0]),
            txt('σ → 0⁺     높이 → ∞',37,ACCENT).move_to([0,-1.8,0]),
        )
        self.show(peak,FadeIn(peak),run_time=.6)
        self.to(CUES[4][1])

        self.copy('밀도와 확률은 다릅니다','전체 면적은 1  /  밀도의 높이는 1을 넘을 수 있음')
        self.clear_stage()
        graph=self.density_graph(.3,area=True)
        self.show(graph,FadeIn(graph),run_time=.6)
        self.to(CUES[5][1])

        self.copy('다른 성분은 나머지 데이터를 설명','한 성분만 xᵢ 위로 붕괴')
        self.clear_stage()
        graph=self.density_graph(.03,kind='mixture')
        self.show(graph,FadeIn(graph),run_time=.6)
        self.play(Transform(graph,self.density_graph(.01,kind='mixture')),run_time=.9)
        self.to(CUES[6][1])

        self.copy('전체 학습 점수도 올라갑니다','log L = Σⱼ log p(xⱼ)')
        self.clear_stage()
        scores=self.score_panel(.03)
        self.show(scores,FadeIn(scores),run_time=.6)
        for sigma in (.01,.0001,1e-12):
            self.play(Transform(scores,self.score_panel(sigma)),run_time=.6)
        self.to(CUES[7][1])

        self.copy('폭을 잃어버렸는데 점수는 좋아집니다','점 하나를 붙잡은 해')
        self.clear_stage()
        trap=VGroup(
            txt('한 성분: 한 점에 붕괴',37,PRUNE).move_to([0,2,0]),
            txt('σ² → 0',45,PRUNE).move_to([0,.2,0]),
            txt('학습 log likelihood → ∞',37,ACCENT,7.2).move_to([0,-2,0]),
        )
        self.show(trap,FadeIn(trap),run_time=.6)
        self.to(CUES[8][1])

        self.copy('목적함수 자체가 위로 열려 있습니다','GMM Singularity')
        self.clear_stage()
        pathological=VGroup(
            txt('Overfitting',32,MUTED).move_to([0,3,0]),
            txt('학습 데이터에 맞아도 새 데이터에 약함',29,INK,7.2).move_to([0,1.8,0]),
            Line([-3.3,.75,0],[3.3,.75,0],color=MUTED,stroke_opacity=.35),
            txt('GMM Singularity',39,PRUNE).move_to([0,-.25,0]),
            txt('유한한 최대 likelihood가 없음',32,ACCENT,7.2).move_to([0,-1.8,0]),
            txt('더 높은 점수, 더 작은 분산, 또 더 높은 점수…',26,INK,7.2).move_to([0,-3.5,0]),
        )
        self.show(pathological,FadeIn(pathological),run_time=.6)
        self.to(CUES[9][1])

        self.copy('붕괴하지 못하도록 제약을 둡니다','분산 하한  /  붕괴를 막는 Regularization·Prior')
        self.clear_stage()
        remedies=VGroup(
            txt('σ² ≥ ε > 0',47,GOOD).move_to([0,2.5,0]),
            txt('Minimum Variance',31,INK).move_to([0,1.2,0]),
            txt('Regularization',35,WEIGHT).move_to([0,-.7,0]),
            txt('Prior',35,ACCENT).move_to([0,-2.4,0]),
        )
        self.show(remedies,FadeIn(remedies),run_time=.6)
        self.to(CUES[10][1])

        self.copy('Likelihood만 높이면 충분할까?','다음 이야기 : MLE · Regularization · Prior')
        self.clear_stage()
        ending=VGroup(
            txt('점수 ↑',48,ACCENT).move_to([0,2.5,0]),
            txt('좋은 모델 ?',42,INK).move_to([0,.3,0]),
            txt('좋은 모델의 기준은 무엇일까?',35,WEIGHT,7.2).move_to([0,-2.2,0]),
        )
        self.show(ending,FadeIn(ending),run_time=.6)
        self.to(DURATION)

    def plot_pos(self,x,density):
        return np.array([1.05*x,-2.2+1.6*density,0])

    def density_graph(self,sigma,kind='component',area=False):
        mixture_mode=kind=='mixture'
        func=(lambda x:mixture(x,sigma)) if mixture_mode else (lambda x:normal(x,MU,sigma))
        # Keep a fixed linear density scale. Split the curve at the top of the
        # visible window instead of flattening or rescaling a tall peak.
        xs=np.unique(np.r_[np.linspace(-3,3,301),MU+sigma*np.linspace(-8,8,161)])
        xs=xs[(xs>=-3)&(xs<=3)]
        curves=VGroup();segment=[]
        for x in xs:
            y=float(func(x))
            if y<=2.5:
                segment.append(self.plot_pos(x,y))
            else:
                if len(segment)>1:curves.add(VMobject(stroke_color=GOOD,stroke_width=3).set_points_as_corners(segment))
                segment=[]
        if len(segment)>1:curves.add(VMobject(stroke_color=GOOD,stroke_width=3).set_points_as_corners(segment))
        axes=VGroup(Line([-3.3,-2.2,0],[3.3,-2.2,0],color=MUTED),
                    Line([-3.3,-2.2,0],[-3.3,2,0],color=MUTED),
                    DashedLine([-3.3,-.6,0],[3.3,-.6,0],color=MUTED,stroke_opacity=.35),
                    txt('1',23,MUTED).move_to([-3.55,-.6,0]))
        dots=VGroup(*[Dot(self.plot_pos(x,0),radius=.067,color=ACCENT if x==MU else INK) for x in DATA])
        labels=VGroup(txt(f'σ = {sigma:g}',32,ACCENT).move_to([0,3.45,0]),
                      txt('p(x)' if mixture_mode else 'component density',26,GOOD).move_to([-1.45,2.65,0]),
                      txt('xᵢ',27,ACCENT).move_to([1.05*MU,-2.8,0]))
        overflow=VGroup()
        peak=float(func(MU))
        if peak>2.5:
            overflow.add(Arrow([1.05*MU,.4,0],[1.05*MU,2.15,0],buff=0,color=ACCENT),
                         txt(f'높이 {peak:.2f} ↑',26,ACCENT).move_to([2,1.45,0]))
        else:
            labels.add(txt(f'높이 {peak:.2f}',26,ACCENT).move_to([2,1.45,0]))
        backdrop=VGroup()
        if mixture_mode:
            backdrop.add(ParametricFunction(lambda x:self.plot_pos(x,(1-PI)*normal(x,0,1.3)),t_range=[-3,3],color=WEIGHT,stroke_width=2,stroke_opacity=.65))
            labels.add(txt('나머지 성분의 밀도는 유지',26,WEIGHT).move_to([0,-3.8,0]))
        if area:
            verts=[self.plot_pos(-3,0)]+[self.plot_pos(x,float(func(x))) for x in np.linspace(-3,3,181)]+[self.plot_pos(3,0)]
            backdrop.add(Polygon(*verts,fill_color=GOOD,fill_opacity=.18,stroke_width=0))
            labels.add(txt('∫ N(x | μ, σ²) dx = 1',34,INK,7.2).move_to([0,-3.9,0]))
        return VGroup(backdrop,axes,curves,dots,labels,overflow)

    def score_panel(self,sigma):
        return VGroup(
            txt('σ = 10⁻¹²' if sigma==1e-12 else f'σ = {sigma:g}',36,INK).move_to([0,3,0]),
            txt(f'log p(xᵢ) = {np.log(mixture(MU,sigma)):.2f}',35,GOOD).move_to([0,1.25,0]),
            txt(f'Σⱼ log p(xⱼ) = {score(sigma):.2f}',35,ACCENT,7.2).move_to([0,-.65,0]),
            txt('σ → 0⁺   ⇒   log L → ∞',34,PRUNE,7.2).move_to([0,-2.8,0]),
        )

    def copy(self,heading,caption):
        self.play(FadeOut(self.head),FadeOut(self.caption),run_time=.2)
        self.head=txt(heading,30,INK,7.25).move_to([0,4.95,0])
        self.caption=txt(caption,26,INK,7.25).move_to([0,-5.8,0])
        self.play(FadeIn(self.head),FadeIn(self.caption),run_time=.2)

    def show(self,stage,*animations,run_time=.6):
        self.stage=stage
        self.play(*animations,run_time=run_time)

    def clear_stage(self):
        if len(self.stage):
            self.play(FadeOut(self.stage),run_time=.2)
            self.remove(*self.stage)
        self.stage=VGroup()

    def to(self,target):
        remain=target-self.time
        if remain<-.04:raise ValueError(f'Timeline overrun {target}: {self.time:.2f}')
        width=max(.01,7.6*target/DURATION)
        if remain>0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2,-7.36,0]),run_time=min(.2,remain))
            if target-self.time>.001:self.wait(target-self.time)
