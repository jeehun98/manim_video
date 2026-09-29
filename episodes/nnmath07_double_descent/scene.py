"""Neural Network Mathematics 07: model-size double descent."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=3, size=25):
    box = RoundedRectangle(width=width, height=.84, corner_radius=.15,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=.11)
    return VGroup(box, label(value, size, color, width-.2))


class NeuralMathDoubleDescent(Scene):
    DURATION = 106

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  07", 18, MUTED).move_to(UP*7.3),
            label("모델은 클수록 과적합된다?", 29).move_to(UP*6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 00:00–00:07 — A flexible curve can memorize noisy training samples.
        self.copy("우리가 아는 과적합", "MODEL SIZE ↑  ·  CAPACITY ↑",
                  "큰 모델은 실제 패턴뿐 아니라\n훈련 데이터의 잡음까지 외울 수 있습니다.")
        points = [(-2.65,-.9),(-1.95,-.65),(-1.2,-.72),(-.45,.05),
                  (.35,-.4),(1.05,.5),(1.75,.08),(2.55,.85)]
        dots = VGroup(*[Dot([x,y,0], radius=.09, color=ACCENT) for x,y in points])
        smooth = VMobject(color=GOOD, stroke_width=4)
        smooth.set_points_smoothly([[-2.9,-.95,0],[-1.6,-.65,0],[0,-.05,0],[1.5,.3,0],[2.8,.78,0]])
        noisy = VMobject(color=PRUNE, stroke_width=3.5)
        noisy.set_points_smoothly([[x,y,0] for x,y in points])
        self.show(VGroup(dots, smooth, noisy,
                         label("general trend", 20, GOOD).move_to([-1.6, 1.75, 0]),
                         label("fits every point", 20, PRUNE).move_to([1.55, 1.75, 0])))
        self.to(7)

        # 00:07–00:14 — The familiar U-shaped test-error story.
        self.copy("그래서 떠올리는 U자 곡선", "TEST ERROR  vs  MODEL SIZE",
                  "처음엔 성능이 좋아지지만\n너무 커지면 과적합으로 나빠진다고 생각합니다.")
        chart = self.chart(self.u_curve())
        best = Dot([-1.05,-1.1,0], radius=.11, color=GOOD)
        tag = label("sweet spot", 22, GOOD).next_to(best, DOWN, buff=.25)
        self.show(VGroup(chart, best, tag))
        self.to(14)

        # 00:14–00:20 — Extend the x axis and the intuitive forecast.
        self.copy("이보다 더 키우면?", "EXPECTED: TEST ERROR ↑",
                  "이미 과적합이라면 더 큰 모델은\n계속 나빠질 것 같습니다.")
        axes = self.axes()
        early = self.u_curve(x_end=.8)
        expected = DashedLine([.8,.15,0], [3.0,1.8,0],
                              color=PRUNE, dash_length=.18, stroke_width=4)
        question = label("more size  →  more error?", 24, PRUNE).move_to([.75,-2.55,0])
        self.show(VGroup(axes, early, expected, question))
        self.to(20)

        # 00:20–00:27 — Reveal the second descent as the central event.
        self.copy("그런데 다시 좋아질 수 있습니다", "OBSERVED IN SOME SETTINGS",
                  "일부 환경에서는 Test Error가 정점을 지나\n더 큰 모델에서 다시 내려갑니다.")
        axes = self.axes()
        curve = self.double_curve()
        peak = Dot([.65,1.5,0], radius=.12, color=PRUNE)
        second = Dot([2.8,-.95,0], radius=.12, color=GOOD)
        self.show(VGroup(axes, curve, peak, second))
        self.to(27)

        # 00:27–00:33 — Name the pattern once.
        self.copy("두 번째 하강", "DOUBLE DESCENT",
                  "감소, 증가, 그리고 두 번째 감소.\n이 패턴을 Double Descent라고 합니다.")
        axes = self.axes()
        curve = self.double_curve(color=MUTED, width=3)
        first = self.curve_segment([(-3,1.7),(-2.0,-.2),(-1.3,-.9)], GOOD)
        rise = self.curve_segment([(-1.3,-.9),(-.5,-.3),(.65,1.5)], PRUNE)
        second = self.curve_segment([(.65,1.5),(1.25,.15),(2.0,-.7),(3.0,-1.0)], GOOD)
        title = label("Double Descent", 38, ACCENT).move_to([0,2.85,0])
        self.show(VGroup(axes, curve, first, rise, second, title))
        self.to(33)

        # 00:33–00:42 — Train error reaches zero near the peak.
        self.copy("가장 이상한 봉우리", "TRAIN ERROR  →  0",
                  "봉우리 부근에서 훈련 오차는 거의 0.\n훈련 데이터를 모두 맞출 수 있는 경계입니다.")
        axes = self.axes()
        test = self.double_curve(color=PRUNE, width=5)
        train = VMobject(color=GOOD, stroke_width=4)
        train.set_points_smoothly([[-3,1.0,0],[-2,.25,0],[-1,-.6,0],[0,-1.05,0],
                                   [.65,-1.3,0],[1.6,-1.32,0],[3,-1.32,0]])
        threshold = DashedLine([.65,-1.65,0],[.65,1.9,0],
                               color=ACCENT, dash_length=.13, stroke_opacity=.6)
        tags = VGroup(label("Test",21,PRUNE).move_to([2.7,-.4,0]),
                      label("Train",21,GOOD).move_to([2.7,-1.7,0]))
        self.show(VGroup(axes, test, train, threshold, tags))
        self.to(42)

        # 00:42–00:50 — An interpolating model may be unstable between points.
        self.copy("모든 점을 간신히 맞춘다면", "INTERPOLATION CAN BE FRAGILE",
                  "훈련점은 모두 통과하지만\n그 사이에서 크게 흔들릴 수 있습니다.")
        xs = np.linspace(-2.7,2.7,7)
        ys = .32*xs + .18*np.sin(2*xs)
        train_dots = VGroup(*[Dot([x,y,0],radius=.09,color=WEIGHT) for x,y in zip(xs,ys)])
        jagged = VMobject(color=PRUNE,stroke_width=4)
        pts=[]
        for i,(x,y) in enumerate(zip(xs,ys)):
            pts.append([x,y,0])
            if i<len(xs)-1:
                nx=xs[i+1]; ny=ys[i+1]
                pts.append([(x+nx)/2,(y+ny)/2+(.7 if i%2 else -.7),0])
        jagged.set_points_smoothly(pts)
        test_dot = Dot([.45, .16,0],radius=.12,color=GOOD)
        test_tag = label("new point",21,GOOD).next_to(test_dot,DOWN,buff=.25)
        self.show(VGroup(train_dots,jagged,test_dot,test_tag))
        self.to(50)

        # 00:50–00:58 — Parameters can keep growing after train error saturates.
        self.copy("더 키워도 훈련 오차는 이미 낮습니다", "D  →  2D  →  10D",
                  "Training Error는 이미 0 근처.\n추가된 파라미터의 역할을 다시 봐야 합니다.")
        sizes = VGroup(card("D",WEIGHT,1.7,30),card("2D",SPARSE,1.7,30),
                       card("10D",ACCENT,1.7,30)).arrange(RIGHT,buff=.48)
        sizes.move_to([0,.9,0])
        floor = Line([-2.85,-1.5,0],[2.85,-1.5,0],color=GOOD,stroke_width=5)
        tag = label("Training Error ≈ 0",25,GOOD).move_to([0,-2.15,0])
        self.show(VGroup(sizes,floor,tag))
        self.to(58)

        # 00:58–01:06 — A point can become a family of feasible solutions.
        self.copy("같은 훈련 답의 선택 폭", "MORE WAYS TO FIT THE DATA  ·  POSSIBLE",
                  "같은 훈련 데이터를 만족하는\n해의 방향이 더 많아질 수 있습니다.")
        point = VGroup(Dot([-2.45,.15,0],radius=.16,color=ACCENT),
                       label("small",22,MUTED).move_to([-2.45,-1.6,0]))
        line = VGroup(Line([-.85,-1.0,0],[-.85,1.25,0],color=GOOD,stroke_width=6),
                      label("larger",22,MUTED).move_to([-.85,-1.6,0]))
        sheet = Polygon([.6,-1.15,0],[2.9,-.45,0],[2.9,1.35,0],[.6,.65,0],
                        stroke_color=SPARSE,fill_color=SPARSE,fill_opacity=.17)
        wide = VGroup(sheet,label("larger still",22,MUTED).move_to([1.75,-1.6,0]))
        self.show(VGroup(point,line,wide))
        self.to(66)

        # 01:06–01:14 — Split-screen trade-off, neither side alone predicts test error.
        self.copy("크기가 키우는 두 가능성", "CAPACITY TO FIT NOISE  /  FREEDOM AMONG SOLUTIONS",
                  "잡음을 맞출 능력과 해를 고를 자유도.\n둘 다 커질 수 있고, 어떤 해를 택하는지도 중요합니다.")
        left = self.panel("Fit noise ↑",PRUNE).move_to([-1.9,.25,0])
        right = self.panel("Solution freedom ↑",GOOD).move_to([1.9,.25,0])
        left_marks = VGroup(*[Dot([-2.7+.3*i,-.4+(.2 if i%2 else -.2),0],
                                 radius=.055,color=PRUNE) for i in range(6)])
        right_lines = VGroup(*[Line([.75,-.8+.27*i,0],[3.0,-.8+.27*i,0],
                                   color=GOOD,stroke_opacity=.45) for i in range(6)])
        self.show(VGroup(left,right,left_marks,right_lines))
        self.to(74)

        # 01:14–01:22 — The classic U was only a partial observation.
        self.copy("U자 그림은 어디까지 봤을까?", "A PARTIAL VIEW OF MODEL SIZE",
                  "첫 상승까지만 보면 U자입니다.\n축을 더 늘리면 다른 모습이 보일 수 있습니다.")
        axes = self.axes()
        full = self.double_curve(color=GOOD,width=5)
        partial = self.u_curve(x_end=.8,color=WEIGHT,width=6)
        cutoff = DashedLine([.8,-1.7,0],[.8,2.0,0],color=ACCENT,dash_length=.16)
        self.show(VGroup(axes,full,partial,cutoff,
                         label("earlier view",20,WEIGHT).move_to([.1,2.5,0])))
        self.to(82)

        # 01:22–01:28 — Second descent is not a universal bigger-is-better rule.
        self.copy("큰 모델이 언제나 좋을까?", "NO UNIVERSAL GUARANTEE",
                  "그렇지 않습니다. 데이터와 학습 방법에 따라\nDouble Descent의 모습도 달라집니다.")
        claim = card("Bigger Model  =  Better Model",PRUNE,6.8,27)
        claim.move_to([0,.65,0])
        cross = VGroup(Line([-3.1,-.05,0],[3.1,1.35,0],color=PRUNE,stroke_width=6),
                       Line([-3.1,1.35,0],[3.1,-.05,0],color=PRUNE,stroke_width=6))
        caveat = label("data  ·  noise  ·  architecture  ·  training",22,MUTED)
        caveat.move_to([0,-2.0,0])
        self.show(VGroup(claim,cross,caveat))
        self.to(88)

        # 01:28–01:37 — Model size changes both function class and feasible set.
        self.copy("모델 크기가 바꾸는 두 가지", "EXPRESSIVITY  +  SOLUTION GEOMETRY",
                  "크기는 표현 가능한 패턴과\n훈련 조건을 만족하는 해 공간을 함께 바꿀 수 있습니다.")
        root = card("More Parameters",ACCENT,4.1,28).move_to([0,2.0,0])
        left = card("Richer patterns",PRUNE,3.15,24).move_to([-1.9,-.65,0])
        right = card("More solution paths",GOOD,3.5,21).move_to([1.9,-.65,0])
        arrows = VGroup(Arrow(root.get_bottom(),left.get_top(),buff=.15,color=PRUNE,
                              stroke_width=3,tip_length=.16),
                        Arrow(root.get_bottom(),right.get_top(),buff=.15,color=GOOD,
                              stroke_width=3,tip_length=.16))
        self.show(VGroup(root,left,right,arrows))
        self.to(97)

        # 01:37–01:46 — The next puzzle: training size versus representation size.
        self.copy("그런데 학습 후에는 줄일 수도 있습니다", "IF THE TRAINED MODEL IS COMPRESSIBLE",
                  "큰 모델로 답을 찾은 뒤 일부를 제거해도\n성능을 유지할 수 있습니다. 왜 그럴까요?")
        top = VGroup(card("100M",WEIGHT,2.1,27),label("→",25,MUTED),
                     card("50M",SPARSE,2.1,27),label("→",25,MUTED),
                     card("10M",GOOD,2.1,27)).arrange(RIGHT,buff=.17)
        top.move_to([0,1.6,0])
        performance = VGroup(*[Rectangle(width=.72,height=h,fill_color=GOOD,
                                          fill_opacity=.65,stroke_width=0).move_to([x,-.65+h/2,0])
                               for x,h in ((-1.8,1.6),(0,1.55),(1.8,1.48))])
        tag = label("performance ≈ maintained  (possible case)",21,GOOD)
        tag.move_to([0,-1.35,0])
        question = label("찾는 크기와 표현하는 크기는 왜 다를까?",27,ACCENT)
        question.move_to([0,-2.75,0])
        self.show(VGroup(top,performance,tag,question))
        self.to(106)

    def axes(self):
        x = Arrow([-3.2,-1.65,0],[3.35,-1.65,0],buff=0,color=MUTED,
                  stroke_width=2,tip_length=.14)
        y = Arrow([-3.2,-1.85,0],[-3.2,2.1,0],buff=0,color=MUTED,
                  stroke_width=2,tip_length=.14)
        return VGroup(x,y,label("Model Size",19,MUTED).move_to([2.5,-2.05,0]),
                      label("Test Error",19,MUTED).move_to([-2.7,2.4,0]))

    def u_curve(self,x_end=2.5,color=WEIGHT,width=5):
        curve=VMobject(color=color,stroke_width=width)
        pts=[[-3.0,1.75,0],[-2.15,.0,0],[-1.05,-1.1,0],[-.25,-.65,0],
             [.8,.15,0],[2.5,1.4,0]]
        if x_end<=.8:pts=pts[:-1]
        curve.set_points_smoothly(pts)
        return curve

    def double_curve(self,color=GOOD,width=5):
        curve=VMobject(color=color,stroke_width=width)
        curve.set_points_smoothly([[-3,1.7,0],[-2,-.2,0],[-1.3,-.9,0],
                                   [-.5,-.3,0],[.65,1.5,0],[1.25,.15,0],
                                   [2,-.7,0],[3,-1.0,0]])
        return curve

    def curve_segment(self,points,color):
        curve=VMobject(color=color,stroke_width=7)
        curve.set_points_smoothly([[x,y,0] for x,y in points])
        return curve

    def chart(self,curve):
        return VGroup(self.axes(),curve)

    def panel(self,title,color):
        frame=RoundedRectangle(width=3.4,height=4.4,corner_radius=.2,
                               stroke_color=color,stroke_width=2,
                               fill_color=color,fill_opacity=.07)
        heading=label(title,23,color,3.1).move_to([0,1.7,0])
        return VGroup(frame,heading)

    def copy(self,heading,note,caption):
        old=VGroup(self.heading,self.note,self.caption,self.caption_box)
        if len(old):self.play(FadeOut(old),run_time=.1)
        self.heading=label(heading,29).move_to(UP*5.12)
        self.note=label(note,20,ACCENT).move_to(DOWN*4.45)
        self.caption_box=RoundedRectangle(width=7.65,height=1.15,corner_radius=.14,
                                           stroke_color=ZERO,stroke_width=1.2,
                                           fill_color=ZERO,fill_opacity=.32).move_to([0,-5.65,0])
        self.caption=label(caption,19,INK,7.2).move_to(self.caption_box)
        self.play(FadeIn(self.heading),FadeIn(self.note),
                  FadeIn(self.caption_box),FadeIn(self.caption),run_time=.2)

    def show(self,new_stage):
        if len(self.stage):self.play(FadeOut(self.stage),run_time=.18)
        self.stage=new_stage
        self.play(FadeIn(self.stage,shift=UP*.12),run_time=.4)

    def to(self,target):
        remaining=target-self.time
        if remaining<-.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width=max(.01,7.6*target/self.DURATION)
        if remaining>0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8+width/2,-7.36,0]),run_time=min(.25,remaining))
            self.wait(max(0,target-self.time))
