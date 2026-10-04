"""Silent visual prototype. Durations are editorial placeholders, not TTS timings."""
from manim import *
from pathlib import Path
import json

config.background_color = "#101923"
config.frame_width = 14.222222
config.frame_height = 8
FONT = "Malgun Gothic"
INK, MUTED, BLUE, GOLD = "#EDF3F7", "#94A7B7", "#68D9F0", "#F3CF75"


def label(s, size=28, color=INK, width=12):
    t = Text(s, font=FONT, font_size=size, color=color, line_spacing=1.2)
    if t.width > width:
        t.scale_to_fit_width(width)
    return t


ASSETS = Path(__file__).resolve().parents[2] / "assets"


def cat(texture=False):
    image = ImageMobject(str(ASSETS / ("cat_texture.png" if texture else "cat_photo.png")))
    image.height = 3.25
    return image


class Act01Hook(Scene):
    def construct(self):
        timing = json.loads(Path(__file__).with_name("timing.json").read_text(encoding="utf-8"))
        knots = np.array(timing["map"])
        original_play = self.play
        logical_time = 0.0

        def duration_to(old_duration):
            nonlocal logical_time
            logical_time += old_duration
            target = round(float(np.interp(logical_time, knots[:, 0], knots[:, 1])) * config.frame_rate) / config.frame_rate
            return max(1 / config.frame_rate, target - self.time)

        def timed_play(*animations, **kwargs):
            kwargs["run_time"] = duration_to(kwargs.get("run_time", 1))
            return original_play(*animations, **kwargs)

        def timed_wait(duration=1):
            actual = duration_to(duration)
            return original_play(Wait(actual), run_time=actual)

        self.play = timed_play
        self.wait = timed_wait
        # Named sections keep later timing and shot replacement straightforward.
        def note(s):
            return label(s, 27, width=12).move_to([0,-3.25,0])

        self.next_section("title")
        kicker = label("EXPLAINABLE AI  /  01",18,BLUE).move_to([0,1.65,0])
        title = label("고양이를 알아본다는 것은\n무슨 뜻일까?",44,width=11)
        self.play(FadeIn(kicker),Write(title),run_time=2)
        self.wait(3)
        self.play(FadeOut(kicker),FadeOut(title))

        self.next_section("same_answer")
        header = label("같은 사진, 같은 정답",30).move_to([0,3.25,0])
        backdrop = RoundedRectangle(width=4.3,height=3.6,corner_radius=.18,
                                    fill_color="#385563",fill_opacity=1,stroke_width=0)
        kitty = cat()
        picture = Group(backdrop,kitty)
        human = VGroup(label("사람",23,MUTED),label("CAT",48,GOLD)).arrange(DOWN,.35).move_to([-4.6,0,0])
        ai = VGroup(label("AI",23,MUTED),label("CAT",48,BLUE)).arrange(DOWN,.35).move_to([4.6,0,0])
        caption = note("둘 다 맞혔습니다.")
        self.play(FadeIn(header),FadeIn(picture),run_time=1.5)
        self.play(FadeIn(human,shift=UP*.2),run_time=1)
        self.wait(2)
        self.play(FadeIn(ai,shift=UP*.2),FadeIn(caption),run_time=1)
        self.wait(3)
        q = note("같은 것을 보고, 같은 이유로 판단했을까요?")
        self.play(Transform(caption,q),Indicate(human[1]),Indicate(ai[1]))
        self.wait(4)

        self.next_section("background")
        self.play(Transform(header,label("고양이는 그대로, 배경만 바꾼다면",30).move_to(header)),
                  Transform(caption,note("입력의 작은 변화가 판단을 바꿀 수도 있습니다.")))
        self.play(backdrop.animate.set_fill("#875065"),run_time=2)
        lower = label("점수 하락?",30,"#FF8C9D").move_to(ai[1])
        self.play(Transform(ai[1],lower),Circumscribe(kitty,color=GOLD),run_time=1.5)
        self.wait(4)
        self.play(Transform(caption,note("고양이는 그대로인데, 판단은 왜 달라졌을까요?")))
        self.wait(4)

        self.next_section("variants")
        self.play(FadeOut(human),FadeOut(ai),Transform(header,label("어떤 변화에 흔들릴까?",30).move_to(header)))
        cards = Group()
        for x, text, color in [(-4.6,"털 무늬", "#385563"),(0,"얼굴 가림","#385563"),(4.6,"작은 패턴","#385563")]:
            bg = RoundedRectangle(width=3.7,height=3.5,corner_radius=.16,fill_color=color,fill_opacity=1,stroke_width=0)
            c = cat().scale(.85)
            card = Group(bg,c,label(text,23,MUTED).shift(DOWN*2.05)).shift(RIGHT*x)
            cards.add(card)
        self.play(FadeOut(picture),FadeIn(cards),run_time=1.5)
        texture = cat(texture=True).scale(.85).move_to(cards[0][1])
        self.play(FadeOut(cards[0][1]),FadeIn(texture),run_time=1.5)
        cards[0].remove(cards[0][1])
        cards[0].add(texture)
        cover = Rectangle(width=1.25,height=.45,fill_color="#1B2836",fill_opacity=1,stroke_width=0).shift(UP*.78)
        patch = VGroup(*[Square(side_length=.13,fill_opacity=1,color=BLUE if (r+c)%2 else GOLD,stroke_width=0)
                          .move_to([4.6+.95+c*.13,-.95+r*.13,0]) for r in range(4) for c in range(4)])
        self.play(FadeIn(cover),run_time=1.5)
        self.play(FadeIn(patch),run_time=1.5)
        self.play(Transform(caption,note("사람과 AI는 변화에 다르게 반응할 수 있습니다.")))
        self.wait(4)
        self.play(Transform(caption,note("반응은 모델, 학습 데이터, 변형 방식에 따라 달라집니다.")))
        self.wait(4)
        self.play(*[FadeOut(m) for m in [cards,cover,patch,caption,header]])

        self.next_section("different_criteria")
        h = label("사람  CAT",38,GOLD).move_to([-3.5,1.3,0])
        a = label("AI  CAT",38,BLUE).move_to([3.5,1.3,0])
        same = label("같은 정답",30).move_to([0,2.6,0])
        hidden = label("판단의 기준은?",35).move_to([0,-.65,0])
        boxes = VGroup(*[RoundedRectangle(width=3.2,height=1.4,corner_radius=.15,
                           stroke_color=MUTED,fill_color="#1B2836",fill_opacity=1).move_to([x,-.65,0]) for x in [-3.5,3.5]])
        qs = VGroup(*[label("?",42,MUTED).move_to(b) for b in boxes])
        self.play(FadeIn(h),FadeIn(a),FadeIn(same))
        self.play(FadeIn(boxes),FadeIn(qs),run_time=1.5)
        cap = note("정답이 같아도, 사용한 정보는 다를 수 있습니다.")
        self.play(FadeIn(cap))
        self.wait(5)
        self.play(FadeOut(boxes),FadeOut(qs),FadeIn(hidden))
        self.wait(4)
        self.play(*[FadeOut(m) for m in [h,a,same,hidden,cap]])

        self.next_section("question")
        end = label("‘고양이를 알아봤다’고 말하려면\n무엇을 확인해야 할까요?",38,width=11)
        self.play(Write(end),run_time=2)
        self.wait(5)
        next_q = label("그 판단을 지탱한 정보는 무엇일까?\n그리고 어떻게 확인할 수 있을까?",32,width=11)
        self.play(Transform(end,next_q),run_time=1.5)
        self.wait(5)
        self.play(FadeOut(end))
