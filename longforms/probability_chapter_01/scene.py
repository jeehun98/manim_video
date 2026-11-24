"""Bernoulli-to-binomial chapter, timed to the supplied narration."""
import importlib.util
import json
import math
from itertools import combinations
from pathlib import Path

from manim import *

HERE = Path(__file__).resolve().parent
intro_spec = importlib.util.spec_from_file_location(
    'probability_intro', HERE.parent / 'probability_chapter_00' / 'scene.py')
intro = importlib.util.module_from_spec(intro_spec)
intro_spec.loader.exec_module(intro)
DATA = json.loads((HERE / 'timing.json').read_text(encoding='utf8'))
axes, bars, curve, label = intro.axes, intro.bars, intro.curve, intro.label
GOLD, TEAL, BLUE, VIOLET, ORANGE, MUTED = (
    intro.GOLD, intro.TEAL, intro.BLUE, intro.VIOLET, intro.ORANGE, intro.MUTED)
RECORD = '1101011011'
SECOND = '1111111000'


def line(words, y, size=34, color=WHITE):
    return label(words, size, color).move_to(UP*y)


def record(values, y, gap=.13):
    tokens = VGroup()
    for value in values:
        color = GOLD if value == '1' else MUTED
        box = RoundedRectangle(width=.57, height=.62, corner_radius=.1, color=color,
                               stroke_width=1.6, fill_color='#141D33', fill_opacity=1)
        tokens.add(VGroup(box, label(value, 26, color)))
    return tokens.arrange(RIGHT, buff=gap).move_to(UP*y)


def pmf(values, ymax, color=TEAL, width=8, spacing=.55):
    ax = axes(-.55, len(values)-.45, ymax, width, 2.8, y=-.34)
    ticks = VGroup(*(label(str(k), 21).next_to(ax.c2p(k,0), DOWN, buff=.1)
                     for k in range(len(values))))
    return VGroup(ax, bars(ax, list(enumerate(values)), spacing, color), ticks)


def likelihood(mu, m=7, n=10):
    return mu**m * (1-mu)**(n-m)


def log_likelihood(mu):
    return 7*math.log(mu)+3*math.log1p(-mu)


class ProbabilityChapter(intro.ChapterScene):
    def setup(self):
        self.shot = next(shot for shot in DATA['scenes'] if shot['class'] == type(self).__name__)
        cues = [cue for cue in DATA['cues'] if self.shot['start'] <= cue['start'] < self.shot['end']]
        self.cues = iter(cues)
        self.caption = None
        self.times = [cue['start'] for cue in cues]

    def title(self):
        left = label('CHAPTER 01 / PROBABILITY DISTRIBUTIONS', 16, TEAL).to_edge(LEFT, buff=.75).set_y(3.72)
        right = label(self.shot['title'], 18, MUTED).to_edge(RIGHT, buff=.75).set_y(3.72)
        rule = Line(LEFT*6.35, RIGHT*6.35, color=TEAL, stroke_width=1).move_to(UP*3.46)
        self.add(left, right, rule)

    def run_stages(self, stages, initial=None, actions=None):
        """Change the board at narration boundaries and keep captions frame-aligned."""
        self.title()
        assert set(stages) <= set(self.times)
        board = initial
        if board is not None:
            self.add(board)
        actions = actions or {}
        for time in self.times:
            if time in actions:
                self.beat(actions[time](board), seconds=3)
                continue
            if time not in stages:
                self.beat()
                continue
            target = stages[time]()
            if board is None:
                self.beat(FadeIn(target, shift=UP*.08), seconds=1)
            else:
                self.beat(FadeOut(board), FadeIn(target, shift=UP*.08), seconds=1)
            board = target

    def formula(self, title, *expressions):
        heading = line(title, 2.42, 32, TEAL)
        group = VGroup(*(label(expr, 31 if len(expr)>38 else 37, GOLD if i == len(expressions)-1 else WHITE)
                         for i,expr in enumerate(expressions))).arrange(DOWN, buff=.38)
        if group.width > 12.7:
            group.scale_to_fit_width(12.7)
        return VGroup(heading, group.move_to(DOWN*.19))


def balance_bar(mu, y=-.18):
    """A unit probability split into failure and success."""
    width = 8.4
    strip = VGroup()
    for size, left, color in [(1-mu,-width/2,BLUE),(mu,width/2-width*mu,GOLD)]:
        if size > 0:
            strip.add(Rectangle(width=width*size,height=.68,stroke_width=0,
                                fill_color=color,fill_opacity=.88).move_to([left+width*size/2,y,0]))
    return strip


def flow(values,y=.45,converge=False):
    """One row of short labeled cards, linked in the order read."""
    nodes=VGroup(*(intro.roadmap_node(title,detail,0,0,color,width=3.45)
                  for title,detail,color in values)).arrange(RIGHT,buff=.58).set_y(y)
    edges=VGroup(*(Arrow(a.get_right(),b.get_left(),buff=.05,color=MUTED,
                         stroke_width=2,max_tip_length_to_length_ratio=.2)
                   for a,b in zip(nodes,nodes[1:])))
    if converge:
        edges[-1].rotate(PI)
    return VGroup(edges,nodes)


class BernoulliDefinition(ProbabilityChapter):
    def construct(self):
        # Match the outgoing picture from Chapter 00.
        ax = axes(-.55,1.55,.72,7,2.9,y=-.33)
        ending = VGroup(ax,bars(ax,[(0,.4),(1,.6)],.34),
                        VGroup(*(label(str(k),23).next_to(ax.c2p(k,0), DOWN, buff=.12) for k in (0,1))),
                        line('베르누이 분포',1.78,34,GOLD))

        def coin_board():
            coins = VGroup()
            for face,x,color in [('뒷면',0,MUTED),('앞면',1,GOLD)]:
                coin = Circle(radius=.69, color=color, fill_color='#141D33', fill_opacity=1)
                coins.add(VGroup(coin,label(face,25,color),label(f'X = {x}',29).next_to(coin,DOWN,buff=.28)))
            return VGroup(line('동전 한 번을 숫자로 기록한다',2.15,32,TEAL),
                          coins.arrange(RIGHT,buff=2.5))
        def conditional():
            return VGroup(line('앞면이 나올 확률을 읽는 순서',2.28,32,TEAL),
                          flow([('고정한 모수','μ : 앞면 확률',TEAL),
                                ('한 번의 시행','X ∈ {0, 1}',BLUE),
                                ('관심 있는 결과','X = 1 : 앞면',GOLD)]),
                          line('P(X = 1 | μ) = μ',-1.32,36,GOLD))
        def parameter():
            return VGroup(line('μ를 바꾸면 두 결과의 확률이 달라진다',2.25,32,TEAL),
                          pmf([.4,.6],1,width=6),line('예시   μ = 0.6',1.37,29,GOLD))
        self.run_stages({
            3:coin_board,
            12:conditional,
            28:parameter,
        }, ending,actions={21:lambda board:Indicate(board[1][1][0],color=TEAL),
                           34:lambda board:Indicate(board[1][1],color=TEAL)})


class BernoulliPMF(ProbabilityChapter):
    def construct(self):
        def normalized():
            self.split=ValueTracker(.6)
            strip=always_redraw(lambda:balance_bar(self.split.get_value()))
            bound=Line(LEFT*4.2,RIGHT*4.2,color=MUTED).set_y(-.8)
            ends=VGroup(label('0',22).next_to(bound.get_left(),DOWN),
                        label('1',22).next_to(bound.get_right(),DOWN))
            return VGroup(line('두 확률이 차지하는 전체 길이 = 1',2.38,32,TEAL),
                          line('■ 뒷면  1−μ',1.11,29,BLUE).shift(LEFT*2.4),
                          line('■ 앞면  μ',1.11,29,GOLD).shift(RIGHT*2.4),
                          strip,bound,ends,line('(1−μ) + μ = 1',-1.68,32,GOLD))
        def evaluate():
            chart=pmf([.4,.6],1,width=5.4).shift(LEFT*3)
            chart[1][0].set_fill(BLUE)
            chart[1][1].set_fill(GOLD)
            return VGroup(line('하나의 식이 두 막대를 만든다',2.42,32,TEAL),chart,
                          label('p(x | μ) = μˣ(1−μ)⁽¹⁻ˣ⁾',27).move_to([3.12,1.05,0]),
                          label('x = 0  →  1−μ',28,BLUE).move_to([3.12,.04,0]),
                          label('x = 1  →  μ',28,GOLD).move_to([3.12,-.84,0]))
        def probability_board(mu):
            return VGroup(line('Bernoulli 분포의 두 확률',2.43,32,TEAL),
                          line(f'P(X = 0 | μ) = 1−μ       P(X = 1 | μ) = μ',1.53,28),
                          pmf([1-mu,mu],1.05))
        self.run_stages({
            40:lambda:probability_board(.6),
            51:normalized,
            66:evaluate,
        },actions={55:lambda board:self.split.animate.set_value(.28),
                   61:lambda board:self.split.animate.set_value(.8),
                   75:lambda board:LaggedStart(Indicate(VGroup(board[1][1][0],board[3]),color=BLUE),
                                               Indicate(VGroup(board[1][1][1],board[4]),color=GOLD))})


class BernoulliMoments(ProbabilityChapter):
    def spread(self):
        track=NumberLine(x_range=[0,1,.1],length=8,include_ticks=False).set_y(.27)
        mean=track.n2p(.6)
        return VGroup(line('각 결과에서 평균까지의 거리를 잰다',2.38,32,TEAL),track,
                      Dot(track.n2p(0),color=BLUE),Dot(track.n2p(1),color=GOLD),
                      DashedLine(mean+DOWN*.2,mean+UP*.45,color=TEAL),
                      label('평균  μ = 0.6',28,TEAL).next_to(mean,UP,buff=.5),
                      Arrow(track.n2p(0)+DOWN*.36,mean+DOWN*.36,buff=.04,color=BLUE),
                      Arrow(track.n2p(1)+DOWN*.36,mean+DOWN*.36,buff=.04,color=GOLD),
                      line('Var(X) = E[(X−μ)²]',-1.61,31,GOLD))


    def weighted(self, squared=False, result=False):
        chart = pmf([.4,.6],1.05,width=4.8).shift(LEFT*3.35)
        left = VGroup(line('Bernoulli(0.6) 예시',2.2,30,TEAL).shift(LEFT*3.35),chart)
        sides = VGroup(
            label('결과     ×     그 결과의 확률',25,MUTED),
            label(('0²' if squared else '0') + '     ×     (1−μ)',33,BLUE),
            label(('1²' if squared else '1') + '     ×     μ',33,GOLD),
            label('E[X²] = μ' if squared else 'E[X] = μ',34,TEAL),
        ).arrange(DOWN,buff=.34).move_to(RIGHT*3.1)
        if not result:
            sides[-1].set_opacity(0)
        return VGroup(left,sides)

    def construct(self):
        self.run_stages({
            83:lambda:self.weighted(),
            93:lambda:self.weighted(result=True),
            101:self.spread,
            111:lambda:self.weighted(squared=True,result=True),
            116:lambda:self.formula('두 기댓값을 분산 식에 대입',
                                   'E[X²] = μ          E[X] = μ',
                                   'Var(X) = μ − μ² = μ(1−μ)'),
        }, actions={88:lambda board:Indicate(board[1][1:3],color=GOLD),
                    105:lambda board:Indicate(board[-1],color=TEAL)})


class LikelihoodConstruction(ProbabilityChapter):
    def construct(self):
        def sample_board():
            return VGroup(line('같은 성공 확률 μ를 가진 독립 시행',2.2,32,TEAL),
                          record(RECORD,.39),line('x₁, x₂, …, x₁₀',-.88,32,GOLD))
        def sweep(board):
            ax, dot = board[2], board[-1]
            return UpdateFromAlphaFunc(dot, lambda mob, alpha: mob.move_to(
                ax.c2p(.15+.55*alpha,likelihood(.15+.55*alpha)/likelihood(.7))))

        def plot():
            ax = axes(0,1,1.12,8.5,2.7,y=-.4)
            shape = curve(ax,lambda x:likelihood(x)/likelihood(.7))
            return VGroup(line('관측값 고정  ·  후보 모수 μ 변화',2.36,32,TEAL),
                          record(RECORD,1.55), ax, shape,
                          label('μ',24,TEAL).next_to(ax,RIGHT,buff=.15),
                          line('세로축  L(μ) / L(0.7)',-2.08,22,MUTED),
                          Dot(ax.c2p(.15,likelihood(.15)/likelihood(.7)),color=GOLD))
        self.run_stages({
            129:lambda:self.formula('성공 확률 μ를 모른다면?','한 번의 모형  →  여러 번의 관측'),
            140:sample_board,
            151:lambda:VGroup(line('독립 시행의 확률을 곱한다',2.3,32,TEAL),
                              record(RECORD[:5],1.13),line('μ   ×   μ   ×   (1−μ)   ×   μ   ×   (1−μ)   ×   ⋯',-.03,30),
                              line('P(x₁, …, xₙ | μ) = ∏ᵢ p(xᵢ | μ)',-1.31,32,GOLD)),
            161:plot,
        }, actions={165:sweep,180:lambda board:Indicate(board[-1],color=GOLD)})


class LogLikelihoodSufficient(ProbabilityChapter):
    def shared_peak(self):
        self.peak_x=ValueTracker(.39)
        panels=VGroup()
        for x,title,fn,color in [
            (-3.27,'가능도  L(μ)',lambda u:likelihood(u)/likelihood(.7),TEAL),
            (3.27,'로그가능도  ℓ(μ)',lambda u:(log_likelihood(u)+16)/10.3,BLUE),
        ]:
            ax=axes(.12,.95,1.09,5.25,2.55,y=-.2).shift(RIGHT*x)
            def marker(ax=ax,fn=fn):
                mu=self.peak_x.get_value()
                top=ax.c2p(mu,fn(mu))
                return VGroup(DashedLine(ax.c2p(mu,0),top,color=GOLD),
                              Dot(top,color=GOLD,radius=.075))
            panels.add(VGroup(ax,curve(ax,fn,color),always_redraw(marker),
                              label(title,27,color).move_to([x,1.63,0]),
                              label('μ',21,MUTED).next_to(ax,RIGHT,buff=.08)))
        return VGroup(line('같은 μ에서 두 곡선이 가장 높다',2.54,32,TEAL),panels,
                      line('세로축은 각각 조정  ·  최대점의 가로 좌표는 μ = 0.7',-2.01,22,GOLD))

    def contribution(self):
        tokens=record(RECORD,1.12,gap=.42)
        terms=VGroup(*(label('log μ' if val=='1' else 'log(1−μ)',16,
                            GOLD if val=='1' else BLUE).next_to(tok,DOWN,buff=.34 if val=='1' else .61)
                       for val,tok in zip(RECORD,tokens)))
        return VGroup(line('각 시행이 로그가능도에 더하는 항',2.38,32,TEAL),
                      tokens,terms,line('성공의 항과 실패의 항을 각각 모은다',-1.35,28))

    def two_records(self, emphasize=False):
        upper, lower = record(RECORD,1.02), record(SECOND,.1)
        equal = line('같은 성공 횟수  m = 7  →  같은 가능도  μ⁷(1−μ)³',-1.69,29,GOLD)
        if not emphasize:
            equal.set_opacity(0)
        return VGroup(line('순서를 바꿔도 앞면 7개, 뒷면 3개',2.35,32,TEAL),
                      upper,lower,equal)

    def construct(self):
        self.run_stages({
            192:lambda:self.formula('곱으로 쓰인 가능도를 어떻게 최대화할까?','L(μ) = ∏ᵢ p(xᵢ | μ)'),
            206:lambda:self.formula('같은 기록을 곱과 합으로 표현','L(μ)  =  μ × μ × (1−μ) × ⋯',
                                    'ℓ(μ)  =  log μ + log μ + log(1−μ) + ⋯'),
            211:self.shared_peak,
            223:self.contribution,
            235:lambda:self.formula('같은 항을 성공과 실패 횟수로 묶는다',
                                    '성공 m회                  실패 N−m회',
                                    'ℓ(μ) = m log μ + (N−m) log(1−μ)'),
            254:self.two_records,
            263:lambda:self.two_records(emphasize=True),
            268:lambda:self.formula('충분통계량','전체 기록 (x₁, …, xₙ)  →  성공 횟수 m',
                                    'm으로 μ의 가능도를 표현한다'),
        }, actions={218:lambda board:self.peak_x.animate.set_value(.7),
                    226:lambda board:LaggedStart(*(Indicate(term,
                    color=GOLD if val=='1' else BLUE,scale_factor=1.05)
                    for val,term in zip(RECORD,board[2])),lag_ratio=.13),
                    247:lambda board:Indicate(board[1][-1],color=GOLD),
                    274:lambda board:Indicate(board[1][0],color=GOLD)})


class MLECalculus(ProbabilityChapter):
    def curvature(self):
        ax=axes(.22,.96,10,8.8,2.86,y=-.23).shift(LEFT*.65)
        graph=lambda u:log_likelihood(u)+15
        peak=Dot(ax.c2p(.7,graph(.7)),color=GOLD)
        tangents=VGroup()
        for u in (.38,.7,.87):
            h=graph(u)
            slope=7/u-3/(1-u)
            span=.055
            tangent=Line(ax.c2p(u-span,h-span*slope),ax.c2p(u+span,h+span*slope),color=GOLD)
            tangents.add(tangent)
        return VGroup(line('오른쪽으로 갈수록 접선의 기울기가 감소한다',2.43,32,TEAL),
                      ax,curve(ax,graph),peak,tangents,
                      line('기울기: 양수  →  0  →  음수',-1.94,25,GOLD),
                      label('ℓ″(μ) < 0',29,VIOLET).move_to([4.85,.66,0]))


    def maximum_plot(self):
        ax=axes(.075,.975,17.8,8.2,2.8,y=-.22).shift(LEFT*1.2)
        shift=19
        graph=curve(ax,lambda x:log_likelihood(x)+shift)
        position = self.tangent_position = ValueTracker(.31)
        marker=always_redraw(lambda:Dot(ax.c2p(position.get_value(),
                                  log_likelihood(position.get_value())+shift),color=GOLD))
        def tangent():
            mu=position.get_value()
            slope=7/mu-3/(1-mu)
            h=log_likelihood(mu)+shift
            return Line(ax.c2p(mu-.075,h-.075*slope),ax.c2p(mu+.075,h+.075*slope),color=GOLD)
        tang=always_redraw(tangent)
        note=always_redraw(lambda:label(f'μ = {position.get_value():.2f}',27,GOLD).move_to([4.1,.62,0]))
        return VGroup(line('접선의 기울기가 0이 되는 곳 찾기',2.43,32,TEAL),
                      ax,graph,marker,tang,note,
                      label('가로축  μ',21,MUTED).next_to(ax,DOWN,buff=.12),
                      label('기울기  ℓ′(μ)',24,MUTED).move_to([4.1,.04,0]))

    def construct(self):
        self.run_stages({
            285:lambda:self.formula('로그가능도를 μ에 대해 미분한다','ℓ(μ) = m log μ + (N−m) log(1−μ)'),
            289:lambda:self.formula('두 로그 항의 미분','d(log μ)/dμ = 1/μ','d(log(1−μ))/dμ = −1/(1−μ)'),
            295:lambda:self.formula('일차 미분','ℓ′(μ) = m/μ − (N−m)/(1−μ)'),
            302:self.maximum_plot,
            311:lambda:self.formula('기울기가 0인 지점','m(1−μ) = μ(N−m)','μ̂ = m/N = X̄'),
            318:self.curvature,
            329:lambda:VGroup(line('성공 비율이 최대가능도추정값',2.32,32,TEAL),
                                record(RECORD,.9),
                                line('성공 7회  ÷  전체 10회',-.28,30),
                                line('μ̂ = m/N = 7/10 = 0.7',-1.19,34,GOLD)),
        }, actions={305:lambda board:self.tangent_position.animate.set_value(.7),
                    323:lambda board:LaggedStart(*(Indicate(t,color=GOLD) for t in board[4]),lag_ratio=.3),
                    333:lambda board:Indicate(board[-1],color=GOLD)})


class OverfittingExample(ProbabilityChapter):
    def construct(self):
        def endpoints():
            left = axes(0,1,1.12,4.65,2.66,y=-.19).shift(LEFT*3.35)
            right = axes(0,1,1.12,4.65,2.66,y=-.19).shift(RIGHT*3.35)
            graphs = VGroup(left,right,curve(left,lambda u:u,GOLD),curve(right,lambda u:1-u,BLUE),
                            Dot(left.c2p(1,1),color=GOLD),Dot(right.c2p(0,1),color=BLUE))
            return VGroup(graphs,line('한 번의 관측과 경계 최대값',2.45,34,TEAL),
                          label('앞면  ·  L(μ)=μ  ·  μ̂=1',24,GOLD).move_to([-3.35,-2,0]),
                          label('뒷면  ·  L(μ)=1−μ  ·  μ̂=0',24,BLUE).move_to([3.35,-2,0]))
        self.run_stages({
            347:lambda:self.formula('표본이 하나뿐이라면?','N = 1'),
            350:endpoints,
            366:lambda:VGroup(line('앞면 한 번으로 다음 시행을 예측하면',2.38,32,TEAL),
                               record('1',1.1), balance_bar(1),
                               line('앞면 예측 확률 1   ·   뒷면 예측 확률 0',-1.27,29,GOLD)),
            381:lambda:self.formula('표본 적합과 새로운 관측의 예측은 다르다','한 번의 관측이 주는 정보는 제한적','적은 데이터에서는 극단적인 추정이 나올 수 있다'),
            393:lambda:VGroup(line('사전 정보와 관측을 함께 사용한다',2.38,32,TEAL),
                               flow([('사전분포','모수의 불확실성',BLUE),('관측','앞면 1회',GOLD),
                                     ('사후분포','관측을 반영한 불확실성',VIOLET)])),
        })


class BinomialDerivation(ProbabilityChapter):
    def construct(self):
        def arrangements(total=False):
            rows=VGroup()
            for values,y in zip(('110','101','011'),(1.28,.35,-.58)):
                tokens=record(values,y).shift(LEFT*2.65)
                rows.add(VGroup(tokens,label('→',25,MUTED).move_to([-.6,y,0]),
                                label('μ²(1−μ)',27,TEAL).move_to([1.12,y,0])))
            heading=line('세 번 중 정확히 두 번 성공',2.44,32,TEAL)
            result=line('세 순서의 확률을 더한다  →  3μ²(1−μ)',-1.77,30,GOLD)
            result.set_opacity(int(total))
            return VGroup(heading,rows,result)
        def choose_positions():
            tokens=record('11000',.88,gap=.36)
            return VGroup(line('N자리 중 성공으로 표시할 m자리를 고른다',2.35,32,TEAL),
                          line('예시  N = 5, m = 2',1.53,25,MUTED),tokens,
                          line('다른 두 자리를 선택할 때마다 다른 순서가 된다',-.22,27),
                          line('C(5,2) = 10     ·     C(N,m) = N!/[m!(N−m)!]',-1.35,29,GOLD))
        def cycle_choices(board):
            pairs=list(combinations(range(5),2))
            states=[record(''.join('1' if i in pair else '0' for i in range(5)),.88,gap=.36)
                    for pair in pairs[1:]]
            return Succession(*(Transform(board[2],state) for state in states))
        def binomial():
            prob = [math.comb(8,k)*.6**k*.4**(8-k) for k in range(9)]
            return VGroup(line('이항분포  ·  Binomial(8, 0.6)',2.42,32,TEAL),
                          line('P(M = m | N, μ) = C(N,m) μᵐ(1−μ)⁽ᴺ⁻ᵐ⁾',1.58,26),
                          pmf(prob,.32,width=9.8),line('가로축  ·  성공 횟수 M',-2.27,22,MUTED))
        self.run_stages({
            400:lambda:self.formula('한 번의 결과에서 여러 번의 성공 횟수로','Xᵢ ∈ {0, 1}','M = X₁ + ⋯ + Xₙ'),
            414:lambda:self.formula('가능한 성공 횟수','M ∈ {0, 1, …, N}'),
            417:arrangements,
            433:lambda:arrangements(total=True),
            438:choose_positions,
            453:binomial,
        }, actions={421:lambda board:Indicate(board[1],color=GOLD),446:cycle_choices})


class BinomialMoments(ProbabilityChapter):
    def additive_board(self,title,total,color):
        tokens=record(RECORD,1)
        bracket=Brace(tokens,DOWN,buff=.19,color=MUTED)
        return VGroup(line(title,2.35,32,TEAL),tokens,bracket,
                      label('독립 시행 N개',24,MUTED).next_to(bracket,DOWN,buff=.11),
                      line(total,-1.35,33,color))

    def construct(self):
        self.run_stages({
            464:lambda:self.additive_board('개별 시행을 더하면 성공 횟수가 된다', '1 + 1 + 0 + 1 + ⋯ = M', GOLD),
            473:lambda:self.additive_board('각 시행의 기댓값을 더한다', 'μ + μ + ⋯ + μ = Nμ', TEAL),
            485:lambda:self.additive_board('독립 시행에서는 분산도 더한다', 'μ(1−μ) + ⋯ + μ(1−μ) = Nμ(1−μ)', VIOLET),
            497:lambda:VGroup(line('성공 횟수가 생성함수의 지수가 된다',2.38,32,TEAL),
                               flow([('성공 0회','확률 P(M = 0) × z⁰',BLUE),
                                     ('성공 1회','확률 P(M = 1) × z¹',TEAL),
                                     ('성공 m회','확률 P(M = m) × zᵐ',GOLD)]),
                               line('G(z) = E[zᴹ] = (1−μ + μz)ᴺ',-1.27,31,GOLD)),
            503:lambda:self.formula('이차 미분에서 두 번째 계승모멘트를 얻는다','G″(1) = E[M(M−1)]','Var(M) = G″(1) + G′(1) − (G′(1))²'),
            509:lambda:VGroup(line('두 가지 계산이 같은 기댓값과 분산에 도달한다',2.42,32,TEAL),
                               flow([('시행을 더하기','독립 베르누이 변수의 합',BLUE),
                                     ('같은 결과','E[M] = Nμ',GOLD),
                                     ('함수를 미분하기','확률생성함수 G(z)',VIOLET)],converge=True),
                               line('Var(M) = Nμ(1−μ)',-1.28,32,GOLD)),
        })


class ChapterSummary(ProbabilityChapter):
    def construct(self):
        def connections():
            root = intro.roadmap_node('독립 Bernoulli 시행', '각 Xᵢ는 0 또는 1',0,2.05,GOLD,4.8)
            center = intro.roadmap_node('성공 횟수 M = ∑ᵢ Xᵢ', '여러 시행의 결과를 하나의 합으로',0,.76,TEAL,5.15)
            children = VGroup(*(intro.roadmap_node(a,b,x,-1.02,color,3.75) for a,b,x,color in [
                ('이항분포','M의 표본분포',-4.44,TEAL),
                ('충분통계량','가능도에 필요한 관측 정보',0,BLUE),
                ('최대가능도추정','μ̂ = M/N',4.44,VIOLET),
            ]))
            edges=VGroup(Line(root.get_bottom(),center.get_top(),color=MUTED),
                         *(Line(center.get_bottom(),node.get_top(),color=MUTED) for node in children))
            return VGroup(edges,root,center,children)
        self.run_stages({
            517:lambda:self.formula('하나의 시행을 반복하면','Bernoulli 시행  →  관측 기록','성공 횟수 M = ∑ᵢ Xᵢ'),
            532:connections,
            543:connections,
        })

