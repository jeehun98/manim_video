"""100-second sequel: preserved facts and downstream computation.

Real-valued mathematical identities; finite logits, same class axis and tie
rule. Floating-point softmax can create numerical ties. No audio or LaTeX.
"""
import os
from manim import *

config.pixel_width = int(os.getenv("VIDEO_WIDTH", "1080"))
config.pixel_height = int(os.getenv("VIDEO_HEIGHT", "1920"))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = "#091119"
INK, MUTED, ACCENT = "#EDF3F7", "#94A7B7", "#61E4CF"
COLORS = ["#FF8C9D", "#68D9F0", "#D3A5FF", "#F3CF75"]


def text(s, size=32, color=INK):
    obj = Text(s, font="Arial", font_size=size, color=color)
    if obj.width > 7.5:
        obj.scale_to_fit_width(7.5)
    return obj


def pipeline(names, y=1.5):
    xs = np.linspace(-2.65, 2.65, len(names))
    nodes = VGroup()
    for x, name in zip(xs, names):
        box = RoundedRectangle(width=1.9, height=1.2, corner_radius=.16,
                               stroke_color=ACCENT, stroke_width=2,
                               fill_color=ACCENT, fill_opacity=.06).move_to([x, y, 0])
        label = text(name, 27)
        if label.width > 1.65:
            label.scale_to_fit_width(1.65)
        nodes.add(VGroup(box, label.move_to(box)))
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=.1, color=MUTED,
                           stroke_width=2) for a, b in zip(nodes, list(nodes)[1:])])
    return VGroup(nodes, arrows)


def chart(values, heading, probability=False):
    # Each chart's maximum is 2.5 units tall; absolute heights are not compared
    # between charts. Values and explicit scale labels prevent that ambiguity.
    bars, labels, classes = VGroup(), VGroup(), VGroup()
    for i, v in enumerate(values):
        x, h = (i-1)*1.8, float(v/max(values))*2.5
        bars.add(Rectangle(width=.85, height=h, stroke_width=0,
                           fill_color=ACCENT if i == 1 else COLORS[i], fill_opacity=.9).move_to([x, -.1+h/2, 0]))
        labels.add(text(f"{v:.3f}" if probability else f"{v:g}", 28).move_to([x, h+.2, 0]))
        classes.add(text("ABC"[i], 29, ACCENT if i == 1 else MUTED).move_to([x, -.55, 0]))
    return VGroup(bars, labels, classes, text(heading, 29, MUTED).move_to(UP*3.25),
                  text("Heights normalized to the largest value", 21, MUTED).move_to(DOWN*1.2))


class ComputationSimplification(Scene):
    def until(self, end):
        if self.time > end+.05:
            raise ValueError(f"Section overrun: {self.time} > {end}")
        if end-self.time > .02:
            self.wait(end-self.time)

    def construct(self):
        series = text("COMPUTATION & INFORMATION / 05", 20, MUTED).move_to(UP*6.6)
        title = text("What can we skip?", 46).move_to(UP*5.3)
        subtitle = text("Known facts meet the next operation", 29, ACCENT).move_to(UP*4)
        flow = pipeline(["Input", "Operation", "Next op"])
        caption = text("Beyond information loss", 34).move_to(DOWN*2.1)
        detail = text("The benefit appears in composition", 27, MUTED).move_to(DOWN*3.3)
        self.play(FadeIn(series), FadeIn(title), FadeIn(subtitle), FadeIn(flow), FadeIn(caption), FadeIn(detail), run_time=1)
        self.play(Indicate(flow[0][1]), Indicate(flow[0][2]), run_time=1)
        self.until(8)

        self.play(Transform(flow, pipeline(["x", "ReLU", "y ≥ 0"])),
                  Transform(title, text("A fact we already know", 39).move_to(title)),
                  Transform(subtitle, text("Every ReLU output is non-negative", 29, ACCENT).move_to(subtitle)),
                  Transform(caption, text("[−2, 3, −5] → [0, 3, 0]", 37).move_to(caption)),
                  Transform(detail, text("This fact can simplify what comes next", 26, MUTED).move_to(detail)), run_time=.8)
        self.until(15)

        self.play(Transform(flow, pipeline(["ReLU", "Abs", "Output"])),
                  Transform(title, text("Now apply absolute value", 38).move_to(title)),
                  Transform(subtitle, text("Abs changes negative values", 31, MUTED).move_to(subtitle)),
                  Transform(caption, text("[0, 3, 0] → [0, 3, 0]", 37).move_to(caption)),
                  Transform(detail, text("No negative inputs remain for Abs", 29, ACCENT).move_to(detail)), run_time=.8)
        self.play(Indicate(flow[0][1], color=COLORS[0]), run_time=.7)
        self.until(22)
        equation = text("Abs(ReLU(x)) = ReLU(x)", 37, ACCENT).move_to(DOWN*.6)
        self.play(FadeIn(equation), Transform(subtitle, text("For y ≥ 0: |y| = y", 33, ACCENT).move_to(subtitle)), run_time=.7)
        self.until(27)
        strike = Cross(flow[0][1], stroke_color=COLORS[0], stroke_width=5)
        self.play(Create(strike), run_time=.5)
        self.play(Transform(flow, pipeline(["ReLU", "Output"])), FadeOut(strike),
                  Transform(title, text("Remove the redundant operation", 34).move_to(title)),
                  Transform(detail, text("Same result. One less operation.", 29, ACCENT).move_to(detail)), run_time=1)
        self.until(33)

        self.play(Transform(flow, pipeline(["ReLU", "max(y, 0)", "Output"])),
                  Transform(title, text("The condition is already satisfied", 34).move_to(title)),
                  Transform(equation, text("max(ReLU(x), 0) = ReLU(x)", 35, ACCENT).move_to(equation)),
                  Transform(subtitle, text("Applying ReLU twice changes nothing", 29, MUTED).move_to(subtitle)),
                  Transform(caption, text("y ≥ 0  →  max(y, 0) = y", 35).move_to(caption)), run_time=.8)
        self.until(37)
        self.play(Transform(flow, pipeline(["ReLU", "Output"])), run_time=1)
        self.until(41)

        self.play(Transform(flow, pipeline(["Logits", "Softmax", "Argmax"])), FadeOut(equation),
                  Transform(title, text("Can we skip an entire layer?", 37).move_to(title)),
                  Transform(subtitle, text("Classification / only the winning class", 28, ACCENT).move_to(subtitle)),
                  Transform(caption, text("Scores → probabilities → class", 32).move_to(caption)),
                  Transform(detail, text("What does Argmax actually need?", 29, MUTED).move_to(detail)), run_time=.9)
        self.until(48)

        z = np.array([1., 3., 2.])
        p = np.exp(z-z.max()); p /= p.sum()
        bars = chart(z, "LOGITS")
        self.play(ReplacementTransform(flow, bars),
                  Transform(subtitle, text("Values change. The winner stays.", 30, ACCENT).move_to(subtitle)),
                  Transform(caption, text("Largest score: class B", 33, ACCENT).move_to(caption)),
                  Transform(detail, text("Softmax preserves ordering", 29, MUTED).move_to(detail)), run_time=.8)
        self.until(51)
        self.play(Transform(bars, chart(p, "SOFTMAX PROBABILITIES", True)), run_time=1.5)
        self.play(Circumscribe(bars[2][1], color=ACCENT), run_time=.7)
        self.until(57)

        identity = VGroup(text("Argmax(Softmax(z))", 38), text("=", 36, MUTED),
                          text("Argmax(z)", 42, ACCENT)).arrange(DOWN, buff=.3).move_to(UP*.9)
        self.play(ReplacementTransform(bars, identity),
                  Transform(title, text("Same winning class", 43).move_to(title)),
                  Transform(caption, text("B = B", 44, ACCENT).move_to(caption)),
                  Transform(detail, text("Only when probabilities are not needed", 27, MUTED).move_to(detail)), run_time=.8)
        scope = text("Finite real logits • same axis and tie rule", 22, MUTED).move_to(DOWN*4.6)
        self.play(FadeIn(scope), run_time=.5)
        self.until(65)

        flow = pipeline(["Logits", "Softmax", "Argmax"])
        self.play(ReplacementTransform(identity, flow),
                  Transform(title, text("Bypass Softmax", 44).move_to(title)),
                  Transform(subtitle, text("Read the winner directly from logits", 29, ACCENT).move_to(subtitle)), run_time=.8)
        strike = Cross(flow[0][1], stroke_color=COLORS[0], stroke_width=5)
        self.play(Create(strike), run_time=.5)
        self.play(Transform(flow, pipeline(["Logits", "Argmax"])), FadeOut(strike),
                  Transform(caption, text("A whole layer can be skipped", 33, ACCENT).move_to(caption)), run_time=1)
        self.until(73)

        cards = VGroup(*[VGroup(text(a, 25, MUTED), text(b, 33, ACCENT), text(c, 25, COLORS[0])).arrange(DOWN,buff=.25)
                         for a,b,c in [("Abs after ReLU", "Non-negative: identity", "The value passes through unchanged"),
                                       ("Argmax after Softmax", "Needs the winner", "Exact probabilities are unused")]])
        cards.arrange(DOWN,buff=.8).move_to(UP*.65)
        self.play(ReplacementTransform(flow,cards), FadeOut(scope),
                  Transform(title,text("What information is needed?",37).move_to(title)),
                  Transform(subtitle,text("Preserved facts + downstream needs",29,ACCENT).move_to(subtitle)),
                  Transform(caption,text("Keep what the next operation uses",30).move_to(caption)),
                  Transform(detail,text("Range is one useful fact. Ordering is another.",25,MUTED).move_to(detail)),run_time=.8)
        self.until(84)

        ending = VGroup(text("Fewer distinctions to consider",33,COLORS[0]),
                        text("↓",36,MUTED), text("More ways to simplify computation",31,ACCENT)).arrange(DOWN,buff=.45).move_to(UP*.8)
        self.play(ReplacementTransform(cards,ending),
                  Transform(title,text("Information guides optimization",35).move_to(title)),
                  Transform(subtitle,text("Prove what stays the same",32,ACCENT).move_to(subtitle)),
                  Transform(caption,text("Same required result. Less computation.",29).move_to(caption)),
                  Transform(detail,text("An opportunity, not an automatic speedup",25,MUTED).move_to(detail)),run_time=1)
        self.until(93)
        self.play(Indicate(ending[-1], color=ACCENT), run_time=.8)
        self.until(100)
