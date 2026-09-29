"""Neural Network Mathematics 09: look beyond the loss at one point."""
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


class NeuralMathBeyondLossValue(Scene):
    DURATION = 93

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  09", 18, MUTED).move_to(UP*7.3),
            label("Loss가 같다면 어떤 해가 더 좋을까?", 29).move_to(UP*6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 00:00–00:06 — Episode 08's equal-loss pair.
        self.copy("똑같은 점수의 두 해", "Ltrain(θA) = Ltrain(θB) = 0",
                  "둘 다 Training Loss는 0입니다.\n어느 해가 더 좋을까요?")
        baseline = Line([-3.3,-1.1,0],[3.3,-1.1,0],color=GOOD,stroke_width=4)
        pair = VGroup(self.point([-2,0,0],"θA",WEIGHT),
                      self.point([2,0,0],"θB",SPARSE))
        self.show(VGroup(baseline,pair,
                         label("same Training Loss",25,GOOD).move_to([0,-2.05,0])))
        self.to(6)

        # 00:06–00:11 — The scalar loss is a tie.
        self.copy("숫자만 보면 알 수 없습니다", "SAME SCORE",
                  "현재 점의 Loss만으로는 구분할 수 없습니다.\n두 해 모두 0점입니다.")
        left = card("Ltrain(θA) = 0",WEIGHT,3.1,24).move_to([-1.85,.65,0])
        right = card("Ltrain(θB) = 0",SPARSE,3.1,24).move_to([1.85,.65,0])
        equals = label("0 = 0",42,ACCENT).move_to([0,-1.2,0])
        self.show(VGroup(left,right,equals))
        self.to(11)

        # 00:11–00:17 — Test a neighborhood rather than only a point.
        self.copy("그럼 주변을 보면 어떨까요?", "θ  →  θ + δ",
                  "점 하나 대신 주변을 봅니다.\n여러 방향으로 조금씩 움직여보는 겁니다.")
        a=np.array([-2,0,0]); b=np.array([2,0,0])
        rings=VGroup(Circle(radius=.82,color=WEIGHT,stroke_opacity=.45).move_to(a),
                     Circle(radius=.82,color=SPARSE,stroke_opacity=.45).move_to(b))
        arrows=VGroup()
        for center,color in ((a,WEIGHT),(b,SPARSE)):
            for angle in np.linspace(0,TAU,8,endpoint=False):
                direction=np.array([np.cos(angle),np.sin(angle),0])
                arrows.add(Arrow(center+.2*direction,center+.68*direction,buff=0,
                                  color=color,stroke_width=2.2,tip_length=.11))
        self.show(VGroup(rings,arrows,self.point(a,"A",WEIGHT),self.point(b,"B",SPARSE)))
        self.to(17)

        # 00:17–00:23 — Same minimum height, different local shape.
        self.copy("같은 Loss, 다른 주변", "SHARP  vs  FLAT",
                  "A는 조금만 움직여도 Loss가 오릅니다.\nB의 주변은 훨씬 안정적입니다.")
        sharp=self.bowl(.58,PRUNE,"A  ·  sharp").move_to([-1.9,.1,0])
        flat=self.bowl(1.35,GOOD,"B  ·  flat").move_to([1.9,.1,0])
        self.show(VGroup(sharp,flat,
                         label("Ltrain = 0",21,MUTED).move_to([0,-2.8,0])))
        self.to(23)

        # 00:23–00:29 — B is a tempting answer under fixed perturbations.
        self.copy("그러면 B가 더 좋아 보입니다", "LOW LOSS  +  STABLE NEIGHBORHOOD",
                  "같은 크기의 변화를 견디는 B는\n안정적인 해처럼 보입니다.")
        sharp=self.bowl(.58,PRUNE,"A").move_to([-1.9,.15,0])
        flat=self.bowl(1.35,GOOD,"B").move_to([1.9,.15,0])
        a_dot=Dot(sharp[2].get_center()+np.array([.38,.77,0]),radius=.08,color=ACCENT)
        b_dot=Dot(flat[2].get_center()+np.array([.38,.14,0]),radius=.08,color=ACCENT)
        tick=label("✓ ?",43,GOOD).move_to([2.8,2.15,0])
        self.show(VGroup(sharp,flat,a_dot,b_dot,tick))
        self.to(29)

        # 00:29–00:35 — The coordinate problem from episode 06 returns.
        self.copy("하지만 좌표를 바꿔보면", "SAME FUNCTION  ·  DIFFERENT FLATNESS",
                  "같은 함수도 파라미터 표현을 바꾸면\n평평함이 달라 보일 수 있습니다.")
        before=card("(w₁,w₂)",WEIGHT,2.8,28).move_to([-1.85,1.25,0])
        after=card("(cw₁,w₂/c)",SPARSE,3.5,27).move_to([1.85,1.25,0])
        arrow=Arrow(before.get_right(),after.get_left(),buff=.12,
                    color=ACCENT,stroke_width=3,tip_length=.16)
        same=card("fθ = fθ′",GOOD,4.0,31).move_to([0,-.65,0])
        flatness=label("shape in parameter coordinates changes",23,PRUNE)
        flatness.move_to([0,-2.15,0])
        self.show(VGroup(before,after,arrow,same,flatness))
        self.to(35)

        # 00:35–00:40 — Replace the question.
        self.copy("질문을 바꿔야 합니다", "STABLE TO WHAT CHANGE?",
                  "단순히 얼마나 Flat한가보다\n어떤 변화에 안정적인가를 물어야 합니다.")
        old=label("얼마나 Flat한가?",31,MUTED).move_to([0,1.15,0])
        strike=Line([-2.3,.85,0],[2.3,1.45,0],color=PRUNE,stroke_width=4)
        new=card("어떤 변화에 안정적인가?",ACCENT,6.7,30).move_to([0,-1.2,0])
        self.show(VGroup(old,strike,new))
        self.to(40)

        # 00:40–00:45 — Parameter perturbation is one specified test.
        self.copy("첫 번째: 파라미터 변화", "PARAMETER PERTURBATION",
                  "정해진 크기의 파라미터 변화에\nLoss가 얼마나 민감한지 잴 수 있습니다.")
        start=card("θ",WEIGHT,2.0,32).move_to([-2.4,.55,0])
        moved=card("θ + δθ",SPARSE,2.8,30).move_to([.2,.55,0])
        arrow=Arrow(start.get_right(),moved.get_left(),buff=.14,
                    color=ACCENT,stroke_width=3,tip_length=.17)
        loss=card("measure  ΔL",GOOD,3.5,27).move_to([0,-1.8,0])
        self.show(VGroup(start,moved,arrow,loss))
        self.to(45)

        # 00:45–00:52 — Shift attention to model output.
        self.copy("하지만 쓰는 것은 모델의 출력", "PARAMETERS  →  FUNCTION",
                  "파라미터 숫자보다\n실제 모델 동작이 어떻게 변하는지가 중요합니다.")
        param=card("θ + δθ",WEIGHT,2.5,26).move_to([-2.2,.55,0])
        fx=card("fθ(x)",GOOD,2.4,28).move_to([1.9,1.35,0])
        changed=card("fθ+δ(x)",SPARSE,3.0,28).move_to([1.9,-.55,0])
        arrows=VGroup(Arrow(param.get_right(),fx.get_left(),buff=.15,
                            color=GOOD,stroke_width=3,tip_length=.15),
                      Arrow(param.get_right(),changed.get_left(),buff=.15,
                            color=SPARSE,stroke_width=3,tip_length=.15))
        self.show(VGroup(param,fx,changed,arrows,
                         label("output change",22,ACCENT).move_to([1.9,-2.3,0])))
        self.to(52)

        # 00:52–00:57 — Equal coordinate distance can mean unequal output change.
        self.copy("같은 거리, 다른 함수 변화", "SAME ‖δθ‖  ·  DIFFERENT Δf",
                  "같은 파라미터 거리라도\n함수 출력은 조금 또는 크게 변할 수 있습니다.")
        left=self.change_panel("A",WEIGHT,"small Δf").move_to([-1.9,.15,0])
        right=self.change_panel("B",PRUNE,"large Δf").move_to([1.9,.15,0])
        left_line=Line([-2.9,-.7,0],[-1.05,.05,0],color=GOOD,stroke_width=4)
        left_shift=Line([-2.9,-.55,0],[-1.05,.2,0],color=SPARSE,stroke_width=3)
        right_line=Line([.95,-.75,0],[2.85,.05,0],color=GOOD,stroke_width=4)
        right_shift=Line([.95,.45,0],[2.85,1.3,0],color=SPARSE,stroke_width=3)
        self.show(VGroup(left,right,left_line,left_shift,right_line,right_shift))
        self.to(57)

        # 00:57–01:03 — Input perturbations ask a different robustness question.
        self.copy("입력을 바꿀 때는 어떨까요?", "x  →  x + ε",
                  "입력 변화에 대한 안정성은 별개입니다.\n원하는 안정성의 종류를 먼저 정해야 합니다.")
        inputs=VGroup(card("x",WEIGHT,1.7,29),label("→",24,MUTED),
                      card("x + ε",ACCENT,2.4,29)).arrange(RIGHT,buff=.3)
        inputs.move_to([0,1.35,0])
        outputs=VGroup(card("output ≈ same",GOOD,3.3,24),
                       card("output changes",PRUNE,3.5,24)).arrange(RIGHT,buff=.4)
        outputs.move_to([0,-.8,0])
        self.show(VGroup(inputs,outputs))
        self.to(63)

        # 01:03–01:09 — Four related but distinct evaluation questions.
        self.copy("하나의 숫자에서 여러 질문으로", "LOSS  ·  PERTURBATION  ·  FUNCTION",
                  "현재 Loss, 주변 민감도,\n실제 함수 변화는 서로 다른 정보입니다.")
        cards=VGroup(card("Current Loss",WEIGHT,5.2,26),
                     card("Parameter sensitivity",SPARSE,5.2,25),
                     card("Functional change",GOOD,5.2,26),
                     card("Input stability",ACCENT,5.2,26))
        cards.arrange(DOWN,buff=.3).move_to([0,.05,0])
        self.show(cards)
        self.to(69)

        # 01:09–01:15 — Revisit episode 08's many zero-loss solutions.
        self.copy("8화의 여러 해를 다시 보면", "Ltrain = 0  FOR ALL",
                  "동률인 해들도 주변 구조와\n실제 동작을 함께 봐야 합니다.")
        x_values=(-2.7,-.9,.9,2.7)
        dots=VGroup(*[self.point([x,.45,0],name,color)
                      for x,name,color in zip(x_values,("θA","θB","θC","θD"),
                                              (WEIGHT,SPARSE,GOOD,ACCENT))])
        rings=VGroup(*[Circle(radius=r,color=c,stroke_opacity=.5).move_to([x,.45,0])
                       for x,r,c in zip(x_values,(.4,.7,.5,.3),(WEIGHT,SPARSE,GOOD,ACCENT))])
        outcomes=VGroup(*[label(text,18,color).move_to([x,-1.15,0])
                          for x,text,color in zip(x_values,("Δf small","Δf large","stable x","sensitive x"),
                                                  (WEIGHT,SPARSE,GOOD,ACCENT))])
        self.show(VGroup(rings,dots,outcomes,
                         label("same Training Loss",23,MUTED).move_to([0,-2.45,0])))
        self.to(75)

        # 01:15–01:21 — Reachability is not the same as evaluation quality.
        self.copy("서로 다른 두 문제", "REACHABILITY  vs  SOLUTION QUALITY",
                  "학습이 어느 해에 닿는가와\n어느 해를 좋다고 부르는가는 다릅니다.")
        left=self.panel("Optimization","Which can we reach?",WEIGHT)
        right=self.panel("Solution Quality","Which should we prefer?",GOOD)
        left.move_to([-1.9,.15,0]);right.move_to([1.9,.15,0])
        divider=Line([0,2.55,0],[0,-2.55,0],color=MUTED,stroke_opacity=.3)
        self.show(VGroup(left,right,divider))
        self.to(81)

        # 01:21–01:27 — The conclusion returns to the original pair.
        self.copy("같은 Loss는 출발점일 뿐", "LOW LOSS  ≠  THE WHOLE STORY",
                  "좋은 해를 판단하려면\nLoss에서 실제 모델 동작으로 시선을 넓혀야 합니다.")
        chain=VGroup(card("Same Loss",WEIGHT,4.2,26),
                     label("↓",24,MUTED),
                     card("Same neighborhood?",SPARSE,4.2,23),
                     label("↓",24,MUTED),
                     card("Same function?",GOOD,4.2,25),
                     label("↓",24,MUTED),
                     card("Same unseen behavior?",ACCENT,4.2,22))
        chain.arrange(DOWN,buff=.16).move_to([0,.1,0])
        self.show(chain)
        self.to(87)

        # 01:27–01:33 — Bridge to finding in a large model, representing compactly.
        self.copy("찾는 크기와 담는 크기", "LARGE TO FIND  ·  SMALL TO REPRESENT",
                  "좋은 동작을 찾는 데 큰 모델이 필요했다면\n왜 작게 줄여도 유지할 수 있을까요?")
        large=card("100M parameters",WEIGHT,3.6,25).move_to([-1.9,1.35,0])
        small=card("20M parameters",GOOD,3.6,25).move_to([1.9,1.35,0])
        arrow=Arrow(large.get_right(),small.get_left(),buff=.12,
                    color=ACCENT,stroke_width=3,tip_length=.16)
        same=card("behavior ≈ maintained  (possible case)",GOOD,6.7,21)
        same.move_to([0,-.75,0])
        question=label("찾는 크기와 표현하는 크기는 왜 다를까?",27,ACCENT)
        question.move_to([0,-2.65,0])
        self.show(VGroup(large,small,arrow,same,question))
        self.to(93)

    def point(self,position,name,color):
        p=np.array(position)
        return VGroup(Dot(p,radius=.11,color=color),
                      label(name,22,color).next_to(p,UP,buff=.18))

    def bowl(self,width,color,name):
        xmax=.65 if width<.7 else 1.3
        curve=VMobject(color=color,stroke_width=5)
        curve.set_points_smoothly([[x,-.65+1.8*(x/width)**2,0]
                                   for x in np.linspace(-xmax,xmax,61)])
        dot=Dot([0,-.65,0],radius=.1,color=ACCENT)
        tag=label(name,23,color).move_to([0,2.05,0])
        baseline=Line([-1.4,-1.25,0],[1.4,-1.25,0],color=MUTED,stroke_opacity=.5)
        return VGroup(baseline,curve,dot,tag)

    def change_panel(self,title,color,detail):
        frame=RoundedRectangle(width=3.4,height=4.1,corner_radius=.2,
                               stroke_color=color,stroke_width=2,
                               fill_color=color,fill_opacity=.06)
        top=label(title,27,color).move_to([0,1.45,0])
        bottom=label(detail,21,color).move_to([0,-1.55,0])
        return VGroup(frame,top,bottom)

    def panel(self,title,detail,color):
        frame=RoundedRectangle(width=3.4,height=4.5,corner_radius=.2,
                               stroke_color=color,stroke_width=2,
                               fill_color=color,fill_opacity=.07)
        top=label(title,24,color,3.0).move_to([0,1.2,0])
        bottom=label(detail,22,INK,3.0).move_to([0,-.75,0])
        return VGroup(frame,top,bottom)

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
