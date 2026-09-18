"""Linear algebra 01: a matrix records where the basis goes. No LaTeX."""
import os
import numpy as np
from manim import *

config.pixel_width = int(os.getenv('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#0B1220'
BLUE, GOLD, INK, MUTED, PINK = '#66D9EF', '#F6CA78', '#EDF2FA', '#93A5BF', '#EF9DCA'
A = np.array([[2., -1.], [1., 2.]])
I = np.eye(2)
DURATION = 154
CAPTIONS = [
    (0, 'intro', '행렬을 처음 배우면 보통 이렇게 소개합니다.\n숫자를 가로와 세로로 배열한 것.'),
    (6, 'question', '그런데 이 숫자들은\n왜 이런 모양으로 모여 있을까요?'),
    (11, 'space', '이번에는 숫자보다 먼저,\n공간을 보겠습니다.'),
    (15, 'basis_x', '평면 위에 두 개의 기본 벡터가 있습니다.\n첫 번째는 오른쪽으로 한 칸.'),
    (21, 'basis_y', '두 번째는 위쪽으로 한 칸.\n이 둘을 기저 벡터라고 부릅니다.'),
    (27, 'move_x', '첫 번째 벡터의 끝을\n오른쪽 두 칸, 위쪽 한 칸으로 옮깁니다.'),
    (34, 'move_y', '두 번째 벡터의 끝은\n왼쪽 한 칸, 위쪽 두 칸으로 옮깁니다.'),
    (41, 'condition', '이제 벡터를 더하고 배수로 만드는 조합을\n그대로 보존한다는 규칙을 정해봅시다.'),
    (48, 'whole', '이 규칙이라면 두 벡터의 도착점만으로\n평면 전체의 변화가 정해집니다.'),
    (55, 'reset_point', '왜 그럴까요? 예를 들어,\n이 점은 오른쪽 두 칸, 위쪽 한 칸입니다.'),
    (62, 'combination', '첫 번째 기저 벡터의 두 배에\n두 번째 기저 벡터를 더한 위치죠.'),
    (69, 'point_move', '변환 뒤에도 같은 조합을 사용합니다.\n새 첫 번째 벡터의 두 배에, 새 두 번째 벡터.'),
    (77, 'point_result', '그래서 이 점은 삼, 사로 이동합니다.\n다른 모든 점도 같은 방식으로 따라 움직입니다.'),
    (84, 'columns', '이제 두 기저 벡터의 도착 좌표를\n나란히 적어보겠습니다.'),
    (90, 'column_x', '첫 번째 열은\n첫 번째 기저 벡터가 어디로 갔는지.'),
    (96, 'column_y', '두 번째 열은\n두 번째 기저 벡터가 어디로 갔는지를 기록합니다.'),
    (102, 'meaning', '행렬을 이렇게 읽을 수 있습니다.\n공간을 어떻게 바꿀 것인지 기록한 규칙.'),
    (109, 'rotation', '숫자가 달라지면 공간의 움직임도 달라집니다.\n어떤 행렬은 공간을 회전시키고,'),
    (117, 'stretch', '어떤 행렬은\n한 방향으로 공간을 늘립니다.'),
    (124, 'shear', '어떤 행렬은\n공간을 기울입니다.'),
    (131, 'recall', '앞으로 행렬을 볼 때는, 두 열이 가리키는\n벡터와 공간의 움직임을 함께 떠올려보세요.'),
    (139, 'limit', '그런데 행렬은 정말\n모든 종류의 변화를 표현할 수 있을까요?'),
    (146, 'next', '그 답을 알려면, 왜 이것을\n선형 변환이라고 부르는지 알아야 합니다.'),
]


def txt(s, size=28, color=INK, width=7.7):
    m = Text(s, font='Malgun Gothic', font_size=size, color=color, line_spacing=1.25)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


def matrix(values, size=39):
    cols = VGroup()
    for j in range(len(values[0])):
        col = VGroup(*[txt(str(row[j]), size, [BLUE, GOLD][j % 2]) for row in values]).arrange(DOWN, buff=.3)
        cols.add(col)
    cols.arrange(RIGHT, buff=.58)
    h, w = cols.height + .34, cols.width + .5
    brackets = VGroup(*[VMobject().set_points_as_corners([
        [sign*(w/2-.14), h/2, 0], [sign*w/2, h/2, 0],
        [sign*w/2, -h/2, 0], [sign*(w/2-.14), -h/2, 0]
    ]).set_stroke(INK, 2.5) for sign in [-1, 1]])
    return VGroup(cols, brackets)


class MatrixAsTransformation(Scene):
    origin = np.array([0., -.35, 0.])
    unit = .79

    def p(self, v):
        return self.origin + self.unit*np.array([v[0], v[1], 0.])

    def arrow(self, v, color, start=(0, 0)):
        return Arrow(self.p(start), self.p(np.array(start)+v), buff=0, color=color,
                     stroke_width=5, max_tip_length_to_length_ratio=.16)

    def grid(self, mat):
        # Clip transformed grid lines to the same viewport throughout the motion.
        lines = VGroup()
        for axis in range(2):
            direction = mat[:, axis]*self.unit
            for k in range(-14, 15):
                base = mat[:, 1-axis]*k*self.unit
                lo, hi = -100., 100.
                for d in range(2):
                    bound = [3.65, 3.15][d]
                    if abs(direction[d]) < 1e-8:
                        if abs(base[d]) > bound:
                            lo, hi = 1, 0
                            break
                    else:
                        a, b = sorted(((-bound-base[d])/direction[d], (bound-base[d])/direction[d]))
                        lo, hi = max(lo, a), min(hi, b)
                if lo < hi:
                    ends = [self.origin + np.append(base+t*direction, 0) for t in [lo, hi]]
                    lines.add(Line(*ends, color=MUTED, stroke_width=1.5 if k == 0 else .8,
                                   stroke_opacity=.65 if k == 0 else .23))
        return lines

    def tile(self, mat):
        return Polygon(*[self.p(mat@np.array(v)) for v in [(0, 0), (1, 0), (1, 1), (0, 1)]],
                       stroke_color=PINK, stroke_width=2, fill_color=PINK, fill_opacity=.16)

    def heading(self, s):
        self.remove(self.head)
        self.head = txt(s, 31).move_to(UP*4.6)
        self.add(self.head)

    def formula(self, s):
        self.remove(self.note)
        self.note = txt(s, 28).move_to(DOWN*4.45)
        self.add(self.note)

    def clear_stage(self):
        keep = [self.chrome, self.head, self.note, self.sub]
        self.remove(*[m for m in self.mobjects if all(m is not k for k in keep)])

    def board(self, mat=I):
        self.g = self.grid(mat)
        self.square = self.tile(mat)
        self.ex, self.ey = self.arrow(mat[:, 0], BLUE), self.arrow(mat[:, 1], GOLD)
        self.add(self.g, self.square, self.ex, self.ey, Dot(self.origin, radius=.045, color=INK))

    def warp(self, before, after, point=False):
        def update_grid(m, alpha):
            m.become(self.grid((1-alpha)*before+alpha*after))
        animations = [UpdateFromAlphaFunc(self.g, update_grid),
                      Transform(self.square, self.tile(after)),
                      Transform(self.ex, self.arrow(after[:, 0], BLUE)),
                      Transform(self.ey, self.arrow(after[:, 1], GOLD))]
        if point:
            animations.extend([Transform(self.path, self.path_for(after)),
                               self.dot.animate.move_to(self.p(after@np.array([2, 1])))])
        return animations

    def path_for(self, mat):
        a, b = mat[:, 0], mat[:, 1]
        return VGroup(self.arrow(a, BLUE), self.arrow(a, BLUE, a), self.arrow(b, GOLD, 2*a))

    def construct(self):
        self.head, self.note, self.sub = VGroup(), VGroup(), VGroup()
        self.chrome = VGroup(txt('LINEAR ALGEBRA   /   01', 19, MUTED).move_to(UP*7.0),
                             txt('행렬은 무엇을 기록할까?', 39).move_to(UP*6.05))
        self.add(self.chrome)
        for index, (start, action, caption) in enumerate(CAPTIONS):
            end = CAPTIONS[index+1][0] if index+1 < len(CAPTIONS) else DURATION
            self.remove(self.sub)
            self.sub = txt(caption, 27).move_to(DOWN*6.15)
            self.add(self.sub)
            animations, seconds = getattr(self, action)()
            if animations:
                self.play(*animations, run_time=seconds)
            remaining = end-self.time
            if remaining > 1e-5:
                self.wait(remaining)
            if abs(self.time-end) > .04:
                raise ValueError(f'Timeline drift: {action}: {self.time} != {end}')

    def intro(self):
        self.heading('숫자를 가로와 세로로 배열한 것')
        self.mat = matrix([[2, -1], [1, 2]]).scale(1.65).move_to(UP*.4)
        self.formula('2행 × 2열')
        return [FadeIn(self.mat, shift=UP*.2)], 1.2

    def question(self):
        self.heading('왜 하필 이 배열일까요?')
        self.formula('각 열에는 어떤 의미가 있을까?')
        return [Indicate(self.mat[0][0], color=BLUE), Indicate(self.mat[0][1], color=GOLD)], 1.8

    def space(self):
        self.clear_stage(); self.heading('숫자보다 먼저, 공간'); self.formula('원점에서 출발하는 두 방향')
        self.g = self.grid(I)
        return [Create(self.g)], 1.8

    def basis_x(self):
        self.heading('첫 번째 기저 벡터'); self.formula('e₁ = (1, 0)')
        self.ex = self.arrow([1, 0], BLUE)
        return [GrowArrow(self.ex)], 1.5

    def basis_y(self):
        self.heading('두 번째 기저 벡터'); self.formula('e₁ = (1, 0)     e₂ = (0, 1)')
        self.ey = self.arrow([0, 1], GOLD)
        return [GrowArrow(self.ey)], 1.5

    def move_x(self):
        self.heading('첫 번째 도착점'); self.formula('(1, 0)  →  (2, 1)')
        self.ghostx = self.ex.copy().set_opacity(.25); self.add(self.ghostx)
        self.coordx = txt('u = (2, 1)', 26, BLUE).move_to(self.p([2, 1])+RIGHT*.8)
        return [Transform(self.ex, self.arrow(A[:, 0], BLUE)), FadeIn(self.coordx)], 2.6

    def move_y(self):
        self.heading('두 번째 도착점'); self.formula('(0, 1)  →  (−1, 2)')
        self.ghosty = self.ey.copy().set_opacity(.25); self.add(self.ghosty)
        self.coordy = txt('v = (−1, 2)', 26, GOLD).move_to(self.p([-1, 2])+LEFT*.8+UP*.2)
        return [Transform(self.ey, self.arrow(A[:, 1], GOLD)), FadeIn(self.coordy)], 2.6

    def condition(self):
        self.heading('한 가지 규칙: 조합을 보존하기')
        self.formula('a e₁ + b e₂  →  a u + b v')
        return [Indicate(self.ex), Indicate(self.ey)], 1.5

    def whole(self):
        self.heading('같은 규칙을 평면 전체에')
        self.remove(self.coordx, self.coordy, self.ghostx, self.ghosty)
        self.square = self.tile(I); self.add(self.square)
        self.formula('기저 벡터의 도착점 + 조합 보존')
        return self.warp(I, A), 3.5

    def reset_point(self):
        self.clear_stage(); self.heading('점 하나를 따라가 봅시다'); self.board()
        self.dot = Dot(self.p([2, 1]), color=PINK, radius=.1)
        self.formula('p = (2, 1)')
        return [FadeIn(self.dot, scale=2)], 1.0

    def combination(self):
        self.heading('오른쪽 두 번 + 위쪽 한 번'); self.formula('p = 2 e₁ + 1 e₂')
        self.path = self.path_for(I)
        return [LaggedStart(*[GrowArrow(a) for a in self.path], lag_ratio=.7)], 3

    def point_move(self):
        self.heading('바뀌는 벡터, 그대로인 계수'); self.formula('T(p) = 2 u + 1 v')
        return self.warp(I, A, point=True), 4

    def point_result(self):
        self.heading('모든 점의 도착점이 정해진다'); self.formula('2(2, 1) + (−1, 2) = (3, 4)')
        self.point_label = txt('(3, 4)', 24, PINK).next_to(self.dot, LEFT, buff=.2)
        return [FadeIn(self.point_label), Indicate(self.dot)], 1.4

    def columns(self):
        self.clear_stage(); self.heading('도착 좌표를 열로 기록하면'); self.formula('u = (2, 1)       v = (−1, 2)')
        self.mat = matrix([[2, -1], [1, 2]]).scale(1.5).move_to(DOWN*.2)
        self.left = matrix([[2], [1]]).move_to(LEFT*2+UP*2.5)
        self.right = matrix([[-1], [2]]).move_to(RIGHT*2+UP*2.5)
        self.right[0].set_color(GOLD)
        self.add(self.left, self.right)
        return [TransformFromCopy(self.left[0][0], self.mat[0][0]),
                TransformFromCopy(self.right[0][0], self.mat[0][1]), FadeIn(self.mat[1])], 2.5

    def column_x(self):
        self.heading('첫 번째 열 = 첫 번째 벡터의 도착점'); self.formula('e₁  →  (2, 1)')
        return [Circumscribe(self.mat[0][0], color=BLUE)], 2

    def column_y(self):
        self.heading('두 번째 열 = 두 번째 벡터의 도착점'); self.formula('e₂  →  (−1, 2)')
        return [Circumscribe(self.mat[0][1], color=GOLD)], 2

    def meaning(self):
        self.heading('행렬: 공간의 변화를 기록하는 방법')
        self.formula('이 관점에서, 행렬은 선형 변환을 나타냅니다')
        return [FadeOut(self.left), FadeOut(self.right), self.mat.animate.move_to(UP*.6)], 1.5

    def example(self, name, values, mat):
        self.clear_stage(); self.heading(name); self.formula('옅은 격자: 고정 좌표    분홍 영역: 단위 정사각형')
        self.board()
        reference = self.grid(I).set_opacity(.12); self.add(reference); self.bring_to_back(reference)
        stamp = matrix(values, 26).move_to(UP*3.75); self.add(stamp)
        return self.warp(I, mat), 3.8

    def rotation(self):
        # Exact rotational interpolation avoids shrinking through a linear blend.
        animations, seconds = self.example('회전 · 반시계 방향 90°', [[0, -1], [1, 0]], np.array([[0., -1.], [1., 0.]]))
        def rotate_all(m, alpha):
            t = alpha*PI/2
            r = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
            self.g.become(self.grid(r)); self.square.become(self.tile(r))
            self.ex.become(self.arrow(r[:, 0], BLUE)); self.ey.become(self.arrow(r[:, 1], GOLD))
        moving = VGroup(self.g, self.square, self.ex, self.ey)
        return [UpdateFromAlphaFunc(moving, rotate_all)], seconds

    def stretch(self):
        return self.example('늘이기 · 가로 방향 2배', [[2, 0], [0, 1]], np.diag([2., 1.]))

    def shear(self):
        return self.example('기울이기 · 높이에 비례해 오른쪽으로', [[1, 1], [0, 1]], np.array([[1., 1.], [0., 1.]]))

    def recall(self):
        self.clear_stage(); self.heading('두 열을 보면, 두 벡터가 보입니다'); self.board()
        self.formula('행렬의 열  →  기저 벡터의 도착점  →  공간의 변화')
        self.mat = matrix([[2, -1], [1, 2]], 26).move_to(UP*3.75); self.add(self.mat)
        return self.warp(I, A), 3.5

    def limit(self):
        self.clear_stage(); self.heading('모든 변화도 가능할까요?'); self.formula('원점을 옮기는 변화는?  직선을 휘게 하는 변화는?')
        q = txt('모든 변화 = 행렬 ?', 43).move_to(UP*.5)
        return [FadeIn(q)], 1.2

    def next(self):
        self.clear_stage(); self.heading('다음 이야기'); self.formula('02  /  선형 변환의 두 가지 약속')
        title = txt('왜 ‘선형’ 변환일까?', 44).move_to(UP*.8)
        desc = txt('더하기와 배수를 보존한다는 것', 28, MUTED).move_to(DOWN*.5)
        return [FadeIn(title, shift=UP*.2), FadeIn(desc)], 1.5
