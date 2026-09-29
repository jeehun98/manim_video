"""Neural Network Mathematics 08: representable, reachable, selected."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=3.0, size=25):
    box = RoundedRectangle(width=width, height=.84, corner_radius=.15,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=.11)
    return VGroup(box, label(value, size, color, width-.2))


class NeuralMathOptimizationImplicitBias(Scene):
    DURATION = 96

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  08", 18, MUTED).move_to(UP*7.3),
            label("좋은 답이 존재해도 학습하지 못할 수 있을까?", 27).move_to(UP*6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 00:00–00:05 — A good answer exists in a large model.
        self.copy("큰 모델 안에는 좋은 답이 있습니다", "θ* ∈ Θ",
                  "큰 모델이 좋은 해를 표현할 수 있다면\n학습도 그 해를 찾을까요?")
        frame = self.space()
        dots = VGroup(*[Dot([x,y,0], radius=.055, color=WEIGHT)
                        for x,y in ((-2.7,-1.2),(-2.1,.9),(-1.3,-.35),(-.2,1.3),
                                    (.45,-1.0),(1.3,.7),(2.25,-.8),(2.8,1.2))])
        star = Star(n=5, outer_radius=.23, color=ACCENT, fill_color=ACCENT,
                    fill_opacity=1).move_to([1.75,1.45,0])
        tag = label("θ*  ·  good solution", 22, ACCENT).next_to(star, DOWN, buff=.25)
        self.show(VGroup(frame,dots,star,tag))
        self.to(5)

        # 00:05–00:13 — Keep capacity and reachability separate.
        self.copy("존재와 도달은 다른 질문", "REPRESENTABLE  ≠  REACHABLE",
                  "모델이 표현할 수 있는가와\n학습이 실제로 도달하는가는 다릅니다.")
        left = self.panel("Representable", WEIGHT, "θ* exists").move_to([-1.9,.15,0])
        right = self.panel("Reachable", ACCENT, "path to θ* ?").move_to([1.9,.15,0])
        divider = Line([0,2.4,0],[0,-2.45,0],color=MUTED,stroke_opacity=.3)
        self.show(VGroup(left,right,divider))
        self.to(13)

        # 00:13–00:18 — The architecture's set includes theta star.
        self.copy("표현력만 보면 문제가 없습니다", "θ* ∈ Θ",
                  "좋은 해가 모델 안에 존재합니다.\n답을 표현하지 못하는 상황이 아닙니다.")
        frame = self.space()
        points = VGroup(*[self.solution(p,name,color)
                          for p,name,color in (([-2.25,.8,0],"θA",WEIGHT),
                                               ([-.5,-.7,0],"θB",SPARSE),
                                               ([1.1,.3,0],"θC",GOOD))])
        star = Star(n=5,outer_radius=.23,color=ACCENT,fill_color=ACCENT,
                    fill_opacity=1).move_to([2.35,1.25,0])
        self.show(VGroup(frame,points,star,
                         label("θ*",25,ACCENT).next_to(star,UP,buff=.2)))
        self.to(18)

        # 00:18–00:23 — Learning proceeds by local steps, not a jump.
        self.copy("학습은 순간이동하지 않습니다", "θ₀ → θ₁ → θ₂ → …",
                  "모든 답을 비교하는 대신\n초기점에서 얻은 정보로 조금씩 이동합니다.")
        start = np.array([-2.7,-1.65,0]); goal = np.array([2.45,1.65,0])
        direct = DashedLine(start,goal,color=PRUNE,dash_length=.16,stroke_opacity=.5)
        cross = label("×",42,PRUNE).move_to([0,.2,0])
        steps = self.path([[-2.7,-1.65,0],[-1.95,-.55,0],[-1.2,-.35,0],
                           [-.45,.35,0],[.5,.15,0],[1.2,.8,0]],GOOD)
        point = Dot(start,radius=.12,color=GOOD)
        self.show(VGroup(self.space(),direct,cross,steps,point,
                         self.solution(goal,"θ*",ACCENT)))
        self.play(MoveAlongPath(point,steps),run_time=1.3,rate_func=linear)
        self.to(23)

        # 00:23–00:28 — Different starts may follow different routes.
        self.copy("같은 모델, 다른 시작점", "θ₀ᴬ → θA     ·     θ₀ᴮ → θB",
                  "같은 데이터와 목적함수여도\n초기값에 따라 경로와 해가 달라질 수 있습니다.")
        path_a = self.path([[-2.8,-1.75,0],[-1.8,-.7,0],[-1.25,.05,0],[-1.7,1.25,0]],WEIGHT)
        path_b = self.path([[2.8,-1.7,0],[1.8,-1.2,0],[.9,-.65,0],[1.35,1.25,0]],SPARSE)
        self.show(VGroup(self.space(),path_a,path_b,
                         self.solution(path_a.get_start(),"start A",WEIGHT),
                         self.solution(path_b.get_start(),"start B",SPARSE),
                         self.solution(path_a.get_end(),"θA",WEIGHT),
                         self.solution(path_b.get_end(),"θB",SPARSE)))
        self.to(28)

        # 00:28–00:34 — A better representable solution is missed by this run.
        self.copy("더 좋은 해는 있지만", "EXISTS  ≠  FOUND BY THIS RUN",
                  "이 학습 경로는 더 좋은 해에 닿지 않습니다.\n표현은 가능하지만 이번에는 찾지 못했습니다.")
        start = [-2.8,-1.6,0]; reached = [-.65,-.25,0]; better = [2.3,1.25,0]
        path = self.path([start,[-2.0,-1.0,0],[-1.25,-.15,0],reached],WEIGHT)
        star = Star(n=5,outer_radius=.23,color=ACCENT,fill_color=ACCENT,
                    fill_opacity=1).move_to(better)
        gap = DashedLine(reached,better,color=PRUNE,dash_length=.13,stroke_opacity=.6)
        self.show(VGroup(self.space(),path,self.solution(reached,"θA",WEIGHT),
                         star,label("better θ*",23,ACCENT).next_to(star,UP,buff=.2),gap))
        self.to(34)

        # 00:34–00:40 — Diagnose optimization versus capacity.
        self.copy("표현력의 한계일까?", "CAPACITY  ?   →   OPTIMIZATION  ?",
                  "학습된 모델만 보고 표현력이 부족하다고\n단정할 수는 없습니다.")
        inside = RoundedRectangle(width=6.8,height=4.1,corner_radius=.2,
                                   stroke_color=WEIGHT,stroke_width=2)
        star = Star(n=5,outer_radius=.2,color=ACCENT,fill_color=ACCENT,
                    fill_opacity=1).move_to([2.0,.9,0])
        route = self.path([[-2.5,-1.35,0],[-1.7,-.8,0],[-1.15,.45,0],[-.3,.5,0]],PRUNE)
        cards = VGroup(card("Model Capacity ?",MUTED,3.2,22).move_to([-1.8,-2.55,0]),
                       card("Optimization ?",ACCENT,3.2,22).move_to([1.8,-2.55,0]))
        self.show(VGroup(inside,star,route,cards))
        self.to(40)

        # 00:40–00:45 — Switch scenario: many reachable zero-loss solutions.
        self.copy("이번에는 좋은 해가 여러 개", "ALL HAVE TRAINING LOSS = 0",
                  "여러 해에 도달할 수 있고\n모두 Training Loss가 0이라고 해봅시다.")
        points = self.solution_row(y=.2)
        self.show(VGroup(self.space()[0],points,
                         card("Ltrain = 0",GOOD,3.2,28).move_to([0,-2.9,0])))
        self.to(45)

        # 00:45–00:50 — Training loss alone cannot break the tie.
        self.copy("Loss만 보면 모두 동률", "L(θA) = L(θB) = L(θC) = L(θD)",
                  "순수 Training Loss가 같다면\n그 값만으로 어느 해를 고를지 알 수 없습니다.")
        baseline = Line([-3.2,-1.15,0],[3.2,-1.15,0],color=GOOD,stroke_width=4)
        points = self.solution_row(y=.0)
        question = label("Which solution?",28,ACCENT).move_to([0,2.3,0])
        self.show(VGroup(baseline,points,question,
                         label("Training Loss = 0",22,GOOD).move_to([0,-2.15,0])))
        self.to(50)

        # 00:50–00:55 — The optimizer's trajectory chooses one of them.
        self.copy("학습 경로는 한 해로 향합니다", "OPTIMIZER TRAJECTORY",
                  "여러 최소값이 있어도 실제 optimizer는\n특정 해에 도달할 수 있습니다.")
        start = np.array([0,-2.0,0]); ends = [np.array([x,1.0,0]) for x in (-2.7,-.9,.9,2.7)]
        candidates = VGroup(*[DashedLine(start,p,color=MUTED,dash_length=.14,
                                          stroke_opacity=.35) for p in ends])
        chosen_path = self.path([start,[-.45,-1.0,0],[-1.15,-.25,0],ends[1]],GOOD)
        dot = Dot(start,radius=.12,color=ACCENT)
        points = VGroup(*[self.solution(p,name,GOOD if i==1 else WEIGHT)
                          for i,(p,name) in enumerate(zip(ends,("θA","θB","θC","θD")))])
        self.show(VGroup(self.space(),candidates,chosen_path,points,dot))
        self.play(MoveAlongPath(dot,chosen_path),run_time=1.2,rate_func=linear)
        self.to(55)

        # 00:55–01:01 — The preference was not written into the bare loss.
        self.copy("시키지 않은 선택", "NOT EXPLICIT IN TRAINING LOSS",
                  "Loss에 선택 기준을 쓰지 않아도\n학습 동역학은 중립적이지 않을 수 있습니다.")
        loss = card("minimize  Ltrain(θ)",WEIGHT,5.2,29).move_to([0,1.7,0])
        absent = VGroup(label("choose θB?",24,MUTED),
                         label("prefer small norm?",24,MUTED),
                         label("prefer simple function?",24,MUTED)).arrange(DOWN,buff=.45)
        absent.move_to([0,-.45,0])
        marks = VGroup(*[label("not specified",17,PRUNE).next_to(item,RIGHT,buff=.16)
                         for item in absent])
        self.show(VGroup(loss,absent,marks))
        self.to(61)

        # 01:01–01:08 — Name implicit bias after the behavior is visible.
        self.copy("학습 과정의 선택 경향", "SAME LOSS  ·  DIFFERENT PREFERENCE",
                  "Optimizer가 특정 종류의 해를 선호하는\n경향을 Implicit Bias라고 합니다.")
        points = self.solution_row(y=.8)
        routes = VGroup(*[Arrow([0,-2.0,0],[x,.55,0],buff=.15,
                                color=GOOD if i==1 else MUTED,
                                stroke_width=4 if i==1 else 1.6,
                                stroke_opacity=1 if i==1 else .3,
                                tip_length=.14) for i,x in enumerate((-2.7,-.9,.9,2.7))])
        title = label("Implicit Bias",38,ACCENT).move_to([0,-2.6,0])
        self.show(VGroup(points,routes,title))
        self.to(68)

        # 01:08–01:16 — Two distinct phenomena, visually side by side.
        self.copy("한계와 편향은 다릅니다", "OPTIMIZATION LIMITATION  vs  IMPLICIT BIAS",
                  "하나는 더 좋은 해에 못 닿는 것.\n다른 하나는 여러 해 중 특정 해를 선호하는 것입니다.")
        left = self.panel("Limitation",PRUNE,"good θ* missed").move_to([-1.9,.25,0])
        right = self.panel("Implicit Bias",GOOD,"one of many chosen").move_to([1.9,.25,0])
        left_marks = VGroup(Dot([-2.6,-.9,0],radius=.1,color=PRUNE),
                            Star(n=5,outer_radius=.14,color=ACCENT,fill_color=ACCENT,
                                 fill_opacity=1).move_to([-1.1,-.2,0]),
                            Line([-2.6,-.9,0],[-2.1,-.45,0],color=PRUNE,stroke_width=3))
        right_marks = VGroup(*[Dot([x,-.65,0],radius=.09,
                                   color=GOOD if i==1 else WEIGHT)
                               for i,x in enumerate((.85,1.55,2.25,2.95))],
                             Arrow([1.9,-1.5,0],[1.55,-.75,0],color=GOOD,
                                   stroke_width=3,tip_length=.14))
        self.show(VGroup(left,right,left_marks,right_marks))
        self.to(76)

        # 01:16–01:22 — Architecture and optimization jointly determine the result.
        self.copy("실제로 얻는 모델의 능력", "ARCHITECTURE  +  OPTIMIZATION",
                  "가능한 답의 공간과 그 안을 탐색하는 방식이\n학습된 모델을 함께 결정합니다.")
        a = card("Architecture",WEIGHT,3.1,25).move_to([-1.9,1.35,0])
        o = card("Optimization",SPARSE,3.1,25).move_to([1.9,1.35,0])
        result = card("Learned Model",GOOD,4.5,30).move_to([0,-1.4,0])
        arrows = VGroup(Arrow(a.get_bottom(),result.get_top()+LEFT*.7,buff=.16,
                              color=WEIGHT,stroke_width=3,tip_length=.15),
                        Arrow(o.get_bottom(),result.get_top()+RIGHT*.7,buff=.16,
                              color=SPARSE,stroke_width=3,tip_length=.15))
        self.show(VGroup(a,o,result,arrows))
        self.to(82)

        # 01:22–01:28 — Add the learning trajectory to episode 07's large set.
        self.copy("7화의 큰 해 집합에 경로를 더하면", "SOLUTION SPACE  +  LEARNING PATH",
                  "가능한 해가 늘어나도\n학습이 어디로 갈지 함께 봐야 합니다.")
        region = Polygon([-3,-1.05,0],[-1.4,1.55,0],[.6,.85,0],[2.4,1.65,0],
                         [3,-.9,0],[.4,-1.8,0],stroke_color=GOOD,
                         fill_color=GOOD,fill_opacity=.12)
        solutions = VGroup(*[Dot([x,y,0],radius=.075,color=WEIGHT)
                             for x,y in ((-2.4,-.5),(-1.7,.55),(-.8,-.45),(.1,.45),
                                         (.8,-.8),(1.6,.6),(2.2,-.25))])
        path = self.path([[-2.85,-2.0,0],[-1.8,-1.2,0],[-.75,.15,0],[.1,.45,0]],ACCENT)
        choice = Star(n=5,outer_radius=.17,color=ACCENT,fill_color=ACCENT,
                      fill_opacity=1).move_to([.1,.45,0])
        self.show(VGroup(region,solutions,path,choice))
        self.to(88)

        # 01:28–01:36 — Searching in a big space, representing compactly.
        self.copy("찾는 공간과 담는 크기", "LARGE SPACE TO FIND  ·  SMALL MODEL TO REPRESENT",
                  "큰 공간에서 찾은 뒤 일부를 줄일 수 있다면\n두 크기는 왜 다른 걸까요?")
        wide = card("100M parameters",WEIGHT,3.6,25).move_to([-1.95,1.7,0])
        small = card("20M parameters",GOOD,3.6,25).move_to([1.95,1.7,0])
        arrow = Arrow(wide.get_right(),small.get_left(),buff=.15,
                      color=ACCENT,stroke_width=4,tip_length=.17)
        find = label("FIND",27,WEIGHT).move_to([-1.95,-.1,0])
        represent = label("REPRESENT",27,GOOD).move_to([1.95,-.1,0])
        similarity = label("performance ≈ maintained  (possible case)",20,MUTED)
        similarity.move_to([0,-1.45,0])
        question = label("찾는 크기와 담는 크기는 왜 다를까?",27,ACCENT)
        question.move_to([0,-2.75,0])
        self.show(VGroup(wide,small,arrow,find,represent,similarity,question))
        self.to(96)

    def space(self):
        box = RoundedRectangle(width=7.25,height=4.65,corner_radius=.23,
                               stroke_color=MUTED,stroke_width=1.7,
                               fill_color=MUTED,fill_opacity=.025)
        return VGroup(box,label("parameter space",20,MUTED).move_to([0,-2.75,0]))

    def solution(self,position,name,color):
        p=np.array(position)
        return VGroup(Dot(p,radius=.11,color=color),
                      label(name,21,color).next_to(p,UP,buff=.17))

    def solution_row(self,y=0):
        return VGroup(*[self.solution([x,y,0],name,
                                      GOOD if name=="θB" else WEIGHT)
                        for x,name in zip((-2.7,-.9,.9,2.7),("θA","θB","θC","θD"))])

    def path(self,points,color):
        line=VMobject(color=color,stroke_width=4)
        line.set_points_smoothly(points)
        return line

    def panel(self,title,color,detail):
        frame=RoundedRectangle(width=3.42,height=4.55,corner_radius=.2,
                               stroke_color=color,stroke_width=2,
                               fill_color=color,fill_opacity=.07)
        top=label(title,25,color,3.0).move_to([0,1.55,0])
        body=label(detail,21,INK,3.0).move_to([0,-1.55,0])
        return VGroup(frame,top,body)

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
