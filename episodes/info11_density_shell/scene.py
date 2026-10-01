"""Point density, available space, and actual high-dimensional Gaussian distances."""
import sys,math
from pathlib import Path
from manim import *
from scipy.stats import chi
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,BG,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info11_density_shell.content import CUES,DURATION,RADII,ANGLES,HIST,BINS,MASS_8_12,INNER_MASS,OUTER_MASS,AVG_DENSITY_RATIO,SAMPLES

class DensityShell(Scene):
    DURATION=DURATION

    def label(self,text,y,size=30,color=WHITE):
        return txt(text,size,color).move_to([0,y,0])

    def swap(self,stage):
        if len(self.stage):self.play(FadeOut(self.stage),run_time=.2)
        self.stage=stage;self.play(FadeIn(stage),run_time=.4)

    def to(self,target):
        remaining=target-self.time
        if remaining < -1/30:raise RuntimeError(f'Cue overrun {remaining}')
        frames=round(remaining*30)
        if frames>0:self.wait(frames/30)

    def radial_plot(self,histogram=False,shade=False):
        group=VGroup();base=-1.2;left=-3.55;scale=7.1/14
        group.add(Line([left,base,0],[3.55,base,0],color=MUTED))
        for r in (0,5,8,10,12,14):
            x=left+r*scale
            group.add(Line([x,base,0],[x,base-.12,0],color=MUTED),txt(str(r),21,MUTED).move_to([x,base-.4,0]))
        group.add(self.label('원점으로부터 거리 r = ‖x‖',-2.05,25,MUTED))
        if histogram:
            for count,a,b in zip(HIST,BINS[:-1],BINS[1:]):
                if not count:continue
                height=3*count/max(HIST)
                group.add(Rectangle(width=(b-a)*scale*.85,height=height,stroke_width=0,fill_color=GOOD,fill_opacity=.85).move_to([left+(a+b)/2*scale,base+height/2,0]))
        else:
            peak=float(chi.pdf(math.sqrt(99),100))
            def point(r):return [left+r*scale,base+3*float(chi.pdf(r,100))/peak,0]
            if shade:
                points=[[left+8*scale,base,0]]+[point(r) for r in np.linspace(8,12,81)]+[[left+12*scale,base,0]]
                group.add(Polygon(*points,stroke_width=0,fill_color=GOOD,fill_opacity=.22))
            curve=VMobject(color=GOOD,stroke_width=3).set_points_as_corners([point(r) for r in np.linspace(0,14,281)]);group.add(curve)
        return group

    def shell(self):
        center=np.array([0,.8,0]);scale=.22
        band=Annulus(inner_radius=8*scale,outer_radius=12*scale,stroke_width=0,fill_color=GOOD,fill_opacity=.14).move_to(center)
        boundaries=VGroup(*(Circle(radius=r*scale,color=GOOD,stroke_opacity=.45).move_to(center) for r in (8,12)))
        dots=VGroup(*(Dot(center+np.array([r*scale*math.cos(a),r*scale*math.sin(a),0]),radius=.024,color=GOOD) for r,a in zip(RADII[:160],ANGLES)))
        return VGroup(self.label('Typical region / 전형적인 영역',4.9,30,GOOD),self.label('100차원: 거리 10 근처의 껍질',3.95,28,MUTED),
            band,boundaries,dots,Dot(center,radius=.065,color=PRUNE),txt('최고 밀도',23,PRUNE).move_to([0,.2,0]),
            self.label('한 점이 아니라, 넓게 모인 영역',-2.65,31,GOOD),self.label('전형적인 샘플은 여기에서 만난다',-3.8,29,ACCENT),
            self.label('실제 거리 + 도식적 방향 / 100차원 샘플의 2차원 투영 아님',-4.85,19,MUTED))

    def construct(self):
        self.add(self.label('INFORMATION THEORY / 11',7.25,20,MUTED),self.label('가장 밀도가 높은 곳에 샘플이 모일까?',6.4,29),
            Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        captions=['곡선의 높이는 밀도 / 샘플도 중심에 모일까?','차원이 커져도, 점의 밀도는 원점에서 최대','실제 100차원 샘플: 거리는 10 근처에 모인다','좌표 제곱의 평균 1 × 100개 → 거리 약 10','원점은 여전히 최대 밀도 / 거리 10의 점은 더 낮다','같은 거리 폭이어도, 바깥 고리의 공간은 더 많다','칸의 확률을 더하면 영역 전체의 확률이 된다','차원이 높을수록, 바깥 공간의 증가가 더 빠르다','밀도 감소 × 공간 증가 → 거리 10 근처에 질량 집중','이론상 거리 8~12에 전체 확률의 99.54%','최고 밀도의 점과, 전형적인 영역은 다르다','한 점의 밀도와 영역 전체의 확률을 구분하자']
        self.stage=VGroup();cap=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            if i:self.play(FadeOut(cap),run_time=.2)
            cap=self.label(captions[i],-5.95,24);self.play(FadeIn(cap),run_time=.2)
            if i==0:
                base=-1
                axis=Line([-3.6,base,0],[3.6,base,0],color=MUTED)
                curve=VMobject(color=WEIGHT,stroke_width=3).set_points_as_corners([[x,base+4*math.exp(-x*x/2),0] for x in np.linspace(-3.5,3.5,181)])
                peak=Dot([0,3,0],radius=.075,color=PRUNE)
                self.swap(VGroup(self.label('1차원 표준 가우시안',4.9,30,MUTED),self.label('p(x) = exp(−x²/2) / √(2π)',3.95,29,WEIGHT),axis,curve,peak,
                    txt('밀도 최대',25,PRUNE).move_to([1.3,2.8,0]),self.label('x = 0',-1.6,28,PRUNE),self.label('샘플도 중심에 가장 많이 모일까?',-3.2,32,ACCENT),
                    self.label('연속분포: 점 하나의 확률은 0 / 곡선 높이는 밀도',-4.7,20,MUTED)))
                self.play(Indicate(peak,color=PRUNE,scale_factor=1.3),run_time=.5)
            elif i==1:
                heat=VGroup();center=UP*1.7
                for j in range(48):
                    lo=j*.055;hi=(j+1)*.055;opacity=.75*math.exp(-((lo+hi)/2)**2/2)
                    if j==0:ring=Circle(radius=hi,stroke_width=0,fill_color=WEIGHT,fill_opacity=opacity)
                    else:ring=Annulus(inner_radius=lo,outer_radius=hi,stroke_width=0,fill_color=WEIGHT,fill_opacity=opacity)
                    heat.add(ring.move_to(center))
                self.swap(VGroup(self.label('2차원 밀도 지도',4.9,29,MUTED),heat,Dot(center,radius=.075,color=PRUNE),self.label('d = 2 → 10 → 100',-1.8,35,ACCENT),
                    self.label('어느 차원에서도 원점이 최대 밀도',-3.3,29,PRUNE),self.label('이 그림은 2차원 밀도 / 고차원의 실제 투영이 아님',-4.75,20,MUTED)))
            elif i==2:
                self.swap(VGroup(self.label('100차원에서 실제로 뽑아보면',4.85,30),self.label('N(0, I₁₀₀) 샘플 2,000개',3.9,29,WEIGHT),self.radial_plot(histogram=True),
                    self.label('0 근처가 아니라, 10 근처',-3.1,35,GOOD),self.label(f'이번 샘플의 평균 거리: {np.mean(RADII):.2f}',-4.55,25,MUTED)))
                marks=VGroup(*(Dot([-3.55+r*7.1/14,-1.02+(j%5)*.12,0],radius=.04,color=ACCENT) for j,r in enumerate(RADII[:40])))
                self.stage.add(marks)
                self.play(LaggedStart(*(FadeIn(mark) for mark in marks),lag_ratio=.025),run_time=.8)
                self.play(FadeOut(marks),run_time=.2);self.stage.remove(marks)
            elif i==3:
                squares=VGroup()
                for j,value in enumerate(SAMPLES[0]**2):
                    squares.add(Square(side_length=.27,stroke_width=.4,stroke_color=MUTED,fill_color=WEIGHT,fill_opacity=.1+.75*min(float(value)/3,1)).move_to([((j%20)-9.5)*.33,3.3+(2-j//20)*.33,0]))
                self.swap(VGroup(self.label('100개 좌표의 제곱을 더하면',4.85,29),squares,self.label('각 좌표: E[xᵢ²] = 1',1.65,33,WEIGHT),
                    self.label('r² = x₁² + x₂² + … + x₁₀₀²',.15,32,ACCENT),self.label('r² ≈ 100',-1.35,41,GOOD),self.label('r ≈ √100 = 10',-2.95,41,GOOD),
                    self.label('각 칸의 값은 매번 다름 / 평균적으로 1씩 기여',-4.55,22,MUTED)))
            elif i==4:
                stage=VGroup(self.label('그런데 점의 밀도만 비교하면?',4.9,30))
                for x,color,title,sub in [(-1.85,PRUNE,'원점','밀도 최고'),(1.85,WEIGHT,'거리 10의 한 점','밀도는 더 낮음')]:
                    stage.add(Dot([x,2.4,0],radius=.13,color=color),txt(title,25,color,max_width=3.3).move_to([x,1.3,0]),txt(sub,27,color,max_width=3.3).move_to([x,.35,0]))
                stage.add(self.label('거리 10의 밀도 / 원점 밀도 = e⁻⁵⁰',-1.4,28,MUTED),self.label('왜 낮은 밀도 쪽에서 샘플을 만날까?',-3.2,31,ACCENT),
                    self.label('밀도는 한 점의 높이 / 영역의 확률과 구별',-4.7,22,MUTED))
                self.swap(stage)
            elif i==5:
                center=UP*.8;scale=1.6
                inner=Circle(radius=.25*scale,stroke_color=PRUNE,fill_color=PRUNE,fill_opacity=.45).move_to(center)
                outer=Annulus(inner_radius=1.5*scale,outer_radius=1.75*scale,color=GOOD,fill_opacity=.3,stroke_width=1).move_to(center)
                self.swap(VGroup(self.label('폭은 같아도, 공간량은 다르다',4.9,30),self.label('2차원에서 거리 폭 0.25 비교',4.15,24,MUTED),inner,outer,
                    txt('작은 원',24,PRUNE).move_to([-1.25,.8,0]),txt('바깥 고리',24,GOOD).move_to([1.35,1.55,0]),Line([2.1,1.55,0],[2.52,1.8,0],color=GOOD),
                    self.label('원: r=0~0.25 / 고리: r=1.5~1.75',-2.7,25,MUTED),self.label('바깥 고리의 면적은 13배',-3.8,34,ACCENT),
                    self.label('공간 크기의 2차원 예시 / 100차원 투영 아님',-4.85,20,MUTED)))
                self.play(Indicate(outer,color=GOOD,scale_factor=1.04),run_time=.6)
            elif i==6:
                tiles=VGroup(Square(side_length=.56,stroke_color=PRUNE,fill_color=PRUNE,fill_opacity=.85).move_to([-2.9,2.6,0]))
                for j in range(13):tiles.add(Square(side_length=.56,stroke_color=GOOD,stroke_width=1,fill_color=GOOD,fill_opacity=.85*AVG_DENSITY_RATIO).move_to([1.2+(j%7-3)*.62,2.9-j//7*.67,0]))
                self.swap(VGroup(self.label('같은 크기의 작은 칸으로 보면',4.9,30),txt('높은 밀도',24,PRUNE).move_to([-2.9,3.8,0]),txt('낮은 밀도',24,GOOD).move_to([1.2,3.8,0]),tiles,
                    txt('적은 칸',25,PRUNE).move_to([-2.9,1.3,0]),txt('많은 칸',25,GOOD).move_to([1.2,1.3,0]),
                    self.label('칸의 확률 ≈ 밀도 × 칸의 면적',-.1,31,ACCENT),self.label('칸들의 확률을 모두 더한다',-1.5,30,GOOD),
                    self.label(f'2차원 예시: 작은 원 {INNER_MASS*100:.2f}% < 고리 {OUTER_MASS*100:.2f}%',-3.15,26,GOOD),
                    self.label('동일 면적 칸으로 나눈 개념도 / 색은 지역 평균 밀도 비교',-4.7,19,MUTED)))
                self.play(Indicate(tiles,color=ACCENT,scale_factor=1.06),run_time=.6)
            elif i==7:
                stage=VGroup(self.label('같은 아주 얇은 껍질의 공간량',4.9,28),self.label('거리 r=1 → r=2로 옮기면',3.95,27,MUTED))
                for y,d,ratio in [(2.6,2,'2배'),(.95,10,'512배'),(-.7,100,'2⁹⁹배')]:
                    box=RoundedRectangle(width=6.6,height=1.1,corner_radius=.15,stroke_color=ACCENT).move_to(UP*y)
                    stage.add(box,txt(f'd = {d}',30,MUTED).move_to([-2.05,y,0]),txt(ratio,34,ACCENT).move_to([1.4,y,0]))
                stage.add(self.label('얇은 껍질의 공간량 ∝ rᵈ⁻¹',-2.6,31,ACCENT),self.label('동일한 미세 거리 폭 / 부피 증가율의 비교',-4.3,23,MUTED))
                self.swap(stage)
            elif i==8:
                cards=VGroup()
                for x,text,color in [(-1.85,'밀도 ↓',PRUNE),(1.85,'공간량 ↑',ACCENT)]:cards.add(RoundedRectangle(width=3.1,height=1,corner_radius=.15,stroke_color=color).move_to([x,3.5,0]),txt(text,32,color).move_to([x,3.5,0]))
                self.swap(VGroup(self.label('둘을 함께 보면 거리 분포가 된다',4.9,29),cards,txt('×',30).move_to([0,3.5,0]),self.radial_plot(),
                    txt('10 근처에서 최대',24,GOOD).move_to([1.45,2.2,0]),self.label('거리별 확률밀도 ∝ r⁹⁹ × exp(−r²/2)',-3.2,27,GOOD),
                    self.label('밀도와 공간량의 효과가 합쳐진 실제 χ₁₀₀ 분포',-4.65,21,MUTED)))
            elif i==9:
                self.swap(VGroup(self.label('100차원: 거리 8~12를 합치면',4.85,30),self.radial_plot(shade=True),self.label('이 영역 전체의 확률',3.9,27,MUTED),
                    self.label(f'{MASS_8_12*100:.2f}%',-3.1,47,GOOD),self.label('샘플 개수의 실측 비율이 아니라, 분포의 이론값',-4.65,21,MUTED)))
            elif i==10:
                self.swap(self.shell())
                self.play(Indicate(self.stage[2],color=GOOD,scale_factor=1.04),run_time=.6)
            else:
                stage=VGroup(self.label('한 점의 높이와, 영역 전체의 확률',4.9,28))
                stage.add(Dot([-1.85,2.55,0],radius=.1,color=PRUNE),Annulus(inner_radius=.6,outer_radius=.85,stroke_color=GOOD,fill_color=GOOD,fill_opacity=.2).move_to([1.85,2.55,0]),
                    txt('최고 밀도',28,PRUNE).move_to([-1.85,1.15,0]),txt('전형적인 영역',28,GOOD).move_to([1.85,1.15,0]),txt('≠',35,ACCENT).move_to([0,1.15,0]),
                    self.label('생성모델에서도 다를 수 있다',-.65,30,MUTED),self.label('중요한 것은',-2.1,33),self.label('영역 전체에 쌓인 확률',-3.45,37,GOOD),
                    self.label('최고 likelihood를 찾기와 전형적으로 샘플링하기를 구분',-4.85,20,MUTED))
                self.swap(stage)
            self.to(end)
