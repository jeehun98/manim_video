from pathlib import Path
import json
from manim import *

ROOT = Path(__file__).resolve().parent
config.background_color = '#081622'
config.frame_width = 14.222222222
config.frame_height = 8
INK = '#EAF5FB'
MUTED = '#8FAABD'
CYAN = '#51D8EE'
GREEN = '#8BE0B1'
GOLD = '#F4C978'
RED = '#FF8B8B'


def txt(s, size=26, color=INK, width=12):
    o = Text(s, font='Malgun Gothic', font_size=size, color=color, line_spacing=1.15)
    if o.width > width:
        o.scale_to_fit_width(width)
    return o


def formula(s, pos, size=34, color=INK, width=12):
    o = MathTex(s, font_size=size, color=color)
    if o.width > width:
        o.scale_to_fit_width(width)
    return o.move_to(pos)


def card(s, pos, color=CYAN, w=3.4, h=.9):
    return VGroup(RoundedRectangle(width=w, height=h, corner_radius=.12,
                                  color=color, fill_color=color, fill_opacity=.08),
                  txt(s, 24, color, w-.25)).move_to(pos)


def blocks(count, pos, color=CYAN, cell=.5, cols=4):
    rows = (count+cols-1)//cols
    return VGroup(*[Square(cell, color=color, fill_color=color, fill_opacity=.12)
                   .move_to([pos[0]+(i % cols-(cols-1)/2)*(cell+.16),
                             pos[1]+((rows-1)/2-i//cols)*(cell+.16), 0]) for i in range(count)])


def bundle(pos=(0, 0, 0), scale=1):
    # Same block palette as Act 7; this remains an illustrative source tensor.
    cells = blocks(9, pos, CYAN, .55, 3)
    links = VGroup(*[Line(cells[i].get_center(), cells[j].get_center(), color=MUTED,
                          stroke_opacity=.4) for i, j in [(0,4),(1,5),(2,3),(3,7),(4,8)]])
    return VGroup(cells, links).scale(scale)


class BoundScene(Scene):
    index = 1

    def construct(self):
        rec = json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
        self.add(txt('행렬곱의 계산량 · 08 · 최적화와 AlphaEvolve', 16, MUTED).move_to([-3.5, 3.65, 0]),
                 txt(rec['title'], 31).move_to([0, 3.03, 0]))
        getattr(self, f'part{self.index}')()
        d = rec['duration_seconds'] or rec['storyboard_seconds']
        if self.time > d+.05:
            raise ValueError((self.index, self.time, d))
        if d > self.time:
            self.wait(d-self.time)

    def to(self, t):
        if self.time > t+.05:
            raise ValueError((self.index, self.time, t))
        if t > self.time:
            self.wait(t-self.time)

    def foot(self, s):
        self.play(FadeIn(txt(s, 18, MUTED).move_to([0, -3.45, 0])), run_time=.5)

    def part1(self):
        original = bundle([0, 1.1, 0], .85)
        self.play(FadeIn(original), FadeIn(txt('7막: 낮은 비용의 거대한 구조', 23, CYAN).move_to([0, 2.3, 0])))
        self.to(5)
        a = blocks(8, [-3.8, -1, 0], CYAN, .42, 4)
        b = blocks(3, [3.8, -1, 0], GREEN, .8, 3)
        self.play(Create(Arrow(original.get_bottom(), [-3.8, -.3, 0], color=MUTED)),
                  Create(Arrow(original.get_bottom(), [3.8, -.3, 0], color=MUTED)),
                  FadeIn(a), FadeIn(b))
        self.play(FadeIn(txt('선택 A', 25, CYAN).move_to([-3.8, -2, 0])),
                  FadeIn(txt('선택 B', 25, GREEN).move_to([3.8, -2, 0])))
        self.to(8); self.play(FadeIn(txt('무엇을 남겨야 가장 좋은 상한을 얻을까?', 29, GOLD).move_to([0, -2.75, 0])))
        self.to(14); self.foot('가상의 추출 비교 · 많이 남긴다는 사실만으로 우열을 정하지 않음')

    def part2(self):
        a = blocks(8, [-3.5, .9, 0], CYAN, .45, 4)
        b = blocks(3, [3.5, .9, 0], GREEN, .9, 3)
        self.play(FadeIn(a), FadeIn(b))
        self.add(txt('작은 행렬곱 여러 개', 26, CYAN).move_to([-3.5, 2.1, 0]),
                 txt('큰 행렬곱 몇 개', 26, GREEN).move_to([3.5, 2.1, 0]))
        self.to(2); self.play(FadeIn(card('활용할 구조 · 구성 비율', [-3.5, -.6, 0], CYAN, 5.4)),
                             FadeIn(card('활용할 구조 · 구성 비율', [3.5, -.6, 0], GREEN, 5.4)))
        self.to(11); self.play(FadeIn(txt('활용 방식과 분석 조건에 따라 상한이 달라진다', 28, GOLD).move_to([0, -1.8, 0])))
        self.to(15); self.play(FadeIn(txt('평가 기준: 증명할 수 있는 지수 상한', 29).move_to([0, -2.6, 0])))
        self.foot('개념도 · 블록 수와 크기는 실제 논문의 최적해가 아님')

    def part3(self):
        self.to(4)
        self.play(FadeIn(txt('조합 손실 분석', 31, GOLD).move_to([0, 2.1, 0])),
                  FadeIn(txt('Combination Loss Analysis', 23, MUTED).move_to([0, 1.55, 0])))
        panels = [card('분포·비율 선택', [-4.5, .1, 0], CYAN, 3.6, 1.2),
                  card('수학적 조건·손실', [0, .1, 0], GOLD, 3.6, 1.2),
                  card('상한 평가', [4.5, .1, 0], GREEN, 3.6, 1.2)]
        self.to(9)
        for i, panel in enumerate(panels):
            self.play(FadeIn(panel), run_time=.6)
            if i:
                self.play(Create(Arrow(panels[i-1].get_right(), panel.get_left(), buff=.1)), run_time=.4)
        knobs = VGroup()
        for i, label in enumerate(['α', 'β', 'γ']):
            y = -.95-i*.45
            line = Line([-5.5, y, 0], [-3.5, y, 0], color=MUTED)
            dot = Dot([-5.1+i*.4, y, 0], color=CYAN, radius=.08)
            knobs.add(VGroup(line, dot, txt(label, 20, CYAN).move_to([-5.9, y, 0])))
        self.to(12); self.play(FadeIn(knobs), Write(formula(r'\omega\leq U(\theta)', [4.5, -1.5, 0], 34, GREEN, 4)))
        self.to(16); self.play(*[knob[1].animate.shift(RIGHT*.45) for knob in knobs], FadeIn(txt('서로 얽힌 조건을 함께 만족시키며 개선', 26, GOLD).move_to([0, -2.65, 0])))
        self.to(20); self.foot('어떤 허용된 θ가 더 낮은 U(θ)를 주는가? · 기호와 조절 막대는 설명용')

    def part4(self):
        axes = Axes(x_range=[-2, 2, 1], y_range=[0, 3, 1], x_length=10, y_length=3,
                    axis_config={'color': MUTED, 'include_ticks': False}).move_to([0, .3, 0])
        f = lambda x: .65*(x*x-1)**2+.22*x+.45
        curve = axes.plot(f, x_range=[-1.65, 1.65], color=CYAN)
        self.play(Create(axes), Create(curve))
        self.add(txt('상한 평가값 · 낮을수록 좋음', 23, GOLD).move_to([0, 2.3, 0]))
        a = Dot(axes.c2p(1.6, f(1.6)), color=RED, radius=.1)
        b = Dot(axes.c2p(-1.6, f(-1.6)), color=GREEN, radius=.1)
        coupling=txt('하나의 선택이 다른 조건에도 영향을 준다',26,GOLD).move_to([0,-2.1,0])
        self.to(9);self.play(FadeIn(coupling))
        self.to(12);self.play(Transform(coupling,txt('조건들을 함께 만족시키며 개선해야 한다',26,GOLD).move_to(coupling)))
        self.to(16); self.play(FadeIn(a))
        path_a = axes.plot(f, x_range=[.96, 1.6], color=RED).reverse_points()
        self.play(MoveAlongPath(a, path_a), run_time=2)
        self.to(20); self.play(FadeIn(b))
        path_b = axes.plot(f, x_range=[-1.6, -1.04], color=GREEN)
        self.play(MoveAlongPath(b, path_b), run_time=2)
        self.to(24); self.play(Transform(coupling,txt('주변에서의 개선이 가장 좋은 선택을 보장하지 않는다',26,GOLD).move_to(coupling)))
        self.to(26); self.foot('비유를 위한 가상 지형 · 실제 논문의 고차원 목적함수나 최적화 로그가 아님')

    def part5(self):
        panels = [card('문제 재구성', [-4.5, 1.4, 0], CYAN, 3.7, 1.1),
                  card('현대적인 최적화', [0, 1.4, 0], GOLD, 3.7, 1.1),
                  card('AlphaEvolve\n최적화 코드 개선', [4.5, 1.4, 0], GREEN, 3.7, 1.1)]
        self.add(txt('2026년 연구 · 결합된 접근', 24, MUTED).move_to([0, 2.3, 0]))
        for i, t in enumerate([4, 7, 12]):
            self.to(t); self.play(FadeIn(panels[i]))
            if i:
                self.play(Create(Arrow(panels[i-1].get_right(), panels[i].get_left(), buff=.1)), run_time=.4)
        region = RoundedRectangle(width=10.8, height=2, corner_radius=.25,
                                  color=MUTED, fill_color=CYAN, fill_opacity=.025).move_to([0, -.7, 0])
        self.to(17); self.play(Create(region), FadeIn(txt('고정된 수학적 조건 안에서', 24, GOLD).move_to([0, .1, 0])))
        old = VMobject(color=RED).set_points_as_corners([[-4,-1,0],[-2.8,-.7,0],[-2,-1.1,0],[-1.3,-.9,0]])
        new = VMobject(color=GREEN).set_points_as_corners([[-4,-1,0],[-2.2,-1.3,0],[0,-.8,0],[2,-1.3,0],[4,-.9,0]])
        self.play(Create(old), run_time=1)
        self.to(19); self.play(Create(new), run_time=2)
        self.to(22); self.play(FadeIn(txt('바뀐 것은 더 좋은 선택을 찾는 계산 과정', 28, GREEN).move_to([0, -2.35, 0])))
        self.foot('최적화 프로그램을 수정·평가 · 경로는 개념도 · AlphaEvolve 단독 성과가 아님')

    def part6(self):
        self.add(txt('2026년 논문이 보고한 이론적 상한', 25, GOLD).move_to([0, 2.25, 0]))
        self.play(FadeIn(txt('기존 상한', 26, CYAN).move_to([-3.6, 1.2, 0])),
                  Write(formula(r'\omega<2.371339', [-3.6, .25, 0], 54, CYAN, 5.8)))
        self.to(6); self.play(FadeIn(txt('개선 상한', 26, GREEN).move_to([3.6, 1.2, 0])),
                             Write(formula(r'\omega<2.371177', [3.6, .25, 0], 54, GREEN, 5.8)),
                             Create(Arrow([-.7,.25,0],[.7,.25,0],color=GOLD,buff=.1)))
        self.to(8); self.play(FadeIn(txt('찾은 후보 → 유효한 상한인지 검증', 29, GOLD).move_to([0, -1.1, 0])))
        self.to(13); self.play(FadeIn(txt('거대한 행렬곱의 성장률에 대한 더 낮은 상한', 27).move_to([0, -2, 0])))
        self.to(21); self.foot('GPU 실행 속도 개선 수치가 아님 · 출처: arXiv:2608.16884v1, §1·§4')

    def part7(self):
        panels = [card('Strassen\n새로운 분해', [-4.5, .8, 0], CYAN, 3.8, 1.3),
                  card('텐서·레이저 방법\n수학적 분석', [0, .8, 0], GOLD, 3.8, 1.3),
                  card('현대 최적화 + AI\n선택을 개선', [4.5, .8, 0], GREEN, 3.8, 1.3)]
        for i, panel in enumerate(panels):
            self.play(FadeIn(panel))
            if i:
                self.play(Create(Arrow(panels[i-1].get_right(),panel.get_left(),buff=.1)),run_time=.4)
        self.to(11); self.play(FadeIn(txt('ω의 정확한 값을 알아낸 것은 아니다', 27, MUTED).move_to([0, -.75, 0])))
        self.to(14); self.play(Write(formula(r'\omega<2.371177', [0, -1.65, 0], 48, GREEN)))
        self.to(15); self.play(FadeIn(txt('하지만 이전보다 더 낮은 상한을 증명했다', 28, GOLD).move_to([0, -2.65, 0])))
        self.to(18); self.foot('수학적 구조의 이해 + 더 좋은 선택의 탐색')
