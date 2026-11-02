"""102-second portrait short: digit-level observations versus mechanistic hypotheses."""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from visual_library.manim import txt, configure_vertical, BG, INK, MUTED, ACCENT, GOOD, PRUNE, ZERO

configure_vertical()
CYAN = '#68D9F0'
PURPLE = '#AF9CF5'
HERE = Path(__file__).resolve().parent
TIMING = json.loads((HERE/'timing.json').read_text(encoding='utf-8'))

def p(x, y):
    return np.array([x, y, 0.])

def t(s, x=0, y=0, size=32, color=INK, width=7.5):
    return txt(s, size, color, width).move_to(p(x, y))

def box(s, x=0, y=0, w=6.9, h=1.1, color=CYAN, size=30):
    return VGroup(RoundedRectangle(width=w, height=h, corner_radius=.16, stroke_color=color,
                  stroke_width=1.6, fill_color=color, fill_opacity=.065).move_to(p(x, y)),
                  t(s, x, y, size, color, w-.4))

def arrow(a, b, color=MUTED):
    return Arrow(p(*a), p(*b), buff=.12, color=color, stroke_width=2.3)

def network(y=1, w=5.8, h=2.7):
    nodes = VGroup()
    edges = VGroup()
    layers = []
    for j, n in enumerate((3, 4, 4, 3)):
        layer = VGroup(*[Circle(radius=.11, color=PURPLE, fill_color=BG, fill_opacity=1,
                              stroke_width=2).move_to(p(-w/2+j*w/3, y+(i-(n-1)/2)*h/(n-1))) for i in range(n)])
        if layers:
            for a in layers[-1]:
                for b in layer:
                    edges.add(Line(a.get_center(), b.get_center(), color=PURPLE, stroke_width=1, stroke_opacity=.28))
        layers.append(layer)
        nodes.add(layer)
    return VGroup(edges, nodes)

def wave(y, period, color, phase=0):
    return ParametricFunction(lambda x: p(x, y+.48*np.cos(TAU*(x+3.2)/period+phase)),
                             t_range=[-3.2, 3.2, .025], color=color, stroke_width=3.5)

def number_row(value, y, color=INK):
    return VGroup(*[t(d, (i-1.5)*.8, y, 48, color if i==2 else MUTED, .7) for i,d in enumerate(str(value))])

def parity_example():
    # Deliberately invented digit-level example; never presented as an observed model output.
    return VGroup(t('23 × 47 = 1081', y=3.5, size=35), t('정답', -2.8, 2.2, 23, MUTED),
                  number_row(1081, 2.2, GOOD), t('예시 오답', -2.8, .9, 23, MUTED), number_row(1061, .9, PRUNE),
                  RoundedRectangle(width=.67, height=2.4, corner_radius=.12, color=ACCENT).move_to(p(.4,1.55)),
                  t('십의 자리만 확대', y=-.8, size=26, color=ACCENT),
                  box('8 → 6     둘 다 짝수', y=-2, color=GOOD, size=36),
                  t('교육용 가상 오답 · 실제 모델 출력 아님', y=-3.5, size=19, color=MUTED))

class MultiplicationErrorParity(Scene):
    def to(self, target):
        remaining = target-self.time
        if remaining < -1/30-.0001:
            raise RuntimeError(f'Timing overflow: {self.time:.4f} > {target}')
        if remaining > 1e-6:
            self.wait(remaining)

    def start(self, index, source=''):
        cue = TIMING['cues'][index]
        self.to(cue['start'])
        self.clear()
        self.add(t('AI  /  곱셈의 오답을 읽다', y=7.15, size=20, color=MUTED),
                 Line(p(-3.7,6.65),p(3.7,6.65),color=ZERO,stroke_width=1),
                 t(cue['title'], y=5.65, size=35, color=ACCENT),
                 RoundedRectangle(width=7.8,height=2.4,corner_radius=.15,stroke_width=0,
                                  fill_color='#101E2B',fill_opacity=1).move_to(p(0,-6.0)),
                 t(cue['caption'], y=-6.0, size=25, width=7.2),
                 t(source, y=-4.25, size=17, color=MUTED),
                 Line(p(-3.7,-7.45),p(3.7,-7.45),color=ZERO,stroke_width=2))
        if cue['start']:
            self.add(Line(p(-3.7,-7.45),p(-3.7+7.4*cue['start']/102,-7.45),color=CYAN,stroke_width=3))
        self.layout_check(index)

    def layout_check(self, index):
        for obj in self.mobjects:
            if obj.width and (obj.get_left()[0]<-4.45 or obj.get_right()[0]>4.45 or obj.get_top()[1]>7.9 or obj.get_bottom()[1]<-7.9):
                raise RuntimeError(f'Frame overflow in cue {index+1}')

    def reveal(self, *objects, duration=.65):
        self.play(*[FadeIn(o, shift=UP*.12) for o in objects],run_time=duration)

    def finish(self, i):
        self.layout_check(i)
        self.to(TIMING['cues'][i]['end'])

    def construct(self):
        paper='Bolton et al. · 2026 · 곱셈 행동 분석'
        fourier='Zhou et al. · 2024 · 덧셈 연구 / 개념도'
        helix_source='Kantamneni & Tegmark · 2025 · 덧셈 연구 / 개념도'
        self.start(0)
        net=network(.1)
        self.reveal(t('23 × 47',y=3.65,size=62),net,t('어떤 경로로 계산할까?',y=-2.7,size=38,color=CYAN))
        self.play(ShowPassingFlash(net[0].copy().set_color(CYAN),time_width=.5),run_time=1.1)
        self.finish(0)

        self.start(1,paper)
        self.reveal(t('2026.10',y=4.1,size=27,color=MUTED),t('16,991',y=2.8,size=76,color=CYAN),
                    t('곱셈 문제',y=1.6,size=32),network(-.4,h=1.8),box('외부 계산 도구 없이',y=-2.8,color=ACCENT))
        examples=VGroup(*[t(s,(j%2-.5)*3.5,3.7-j//2*.5,19,MUTED,3) for j,s in enumerate(['7 × 8','24 × 62','351 × 4932','98 × 750'])])
        # Input examples appear below the counter so the counter stays readable.
        examples.move_to(p(0,-3.75))
        self.reveal(examples)
        self.finish(1)

        self.start(2,paper)
        cards=VGroup(*[box(s,y=3.4-j*1.65,color=CYAN if j<2 else PURPLE,size=37) for j,s in enumerate(['7 × 8','23 × 47','351 × 4932'])])
        self.play(LaggedStart(*[FadeIn(c,shift=UP*.2) for c in cards],lag_ratio=.35),run_time=1.5)
        self.reveal(t('1×1자리 → 3×4자리',y=-2.8,size=31,color=MUTED))
        self.finish(2)

        self.start(3,paper)
        self.reveal(box('정답',y=3,color=GOOD),box('오답',y=1.1,color=PRUNE),
                    t('틀린 숫자에도\n규칙이 남아 있다',y=-1.5,size=43,color=ACCENT))
        self.finish(3)

        self.start(4,paper)
        self.reveal(t('Qwen3.5-2B',y=4.1,size=28,color=MUTED),t('92.7%',y=2.65,size=82,color=GOOD),
                    t('틀린 십의 자리 숫자의 홀짝 일치율',y=1.35,size=28,color=ACCENT),
                    t('대상: 틀린 십의 자리 3,542개',y=.55,size=24,color=MUTED))
        bars=VGroup()
        for j,(label,value,color) in enumerate([('관찰값',.927,GOOD),('모델 기반 기준선',.444,MUTED)]):
            y=-.8-j*1.3
            bars.add(t(label,-2.25,y+.4,21,color,2.8),
                     Rectangle(width=6.5*value,height=.35,fill_color=color,fill_opacity=.85,stroke_width=0).move_to(p(-3.25+6.5*value/2,y)),
                     t(f'{value*100:.1f}%',2.8,y+.42,23,color,1.5))
        self.reveal(bars,t('답 전체의 홀짝 일치율이 아님',y=-3.45,size=23,color=ACCENT))
        self.finish(4)

        self.start(5,'십의 자리 홀짝 보존을 설명하는 가상 예시')
        ex=parity_example()
        self.reveal(ex)
        self.play(Indicate(ex[5],color=ACCENT),run_time=.65)
        self.finish(5)

        self.start(6)
        self.reveal(t('8 ≠ 6',y=2.8,size=69,color=PRUNE),t('짝수 = 짝수',y=.8,size=45,color=GOOD),
                    t('값은 달라도\n같은 특징이 남는다?',y=-1.7,size=39,color=ACCENT))
        self.finish(6)

        self.start(7)
        digits=VGroup(t('¹',.8,3.8,33,ACCENT),t('23',.1,3.1,62),t('× 47',-.25,1.9,62),
                      Line(p(-2,.95),p(2,.95),color=MUTED),t('161',y=.25,size=55,color=CYAN),
                      t('920',y=-.85,size=55,color=PURPLE),Line(p(-2,-1.5),p(2,-1.5),color=MUTED),
                      t('1081',y=-2.3,size=61,color=GOOD))
        self.reveal(digits)
        self.play(Indicate(digits[0],color=ACCENT),run_time=.7)
        self.finish(7)

        self.start(8)
        self.reveal(network(1.4),box('자릿수 계산 + 올림?',y=-1.3,color=MUTED),t('내부 계산 규칙은 별개의 질문',y=-3,size=29,color=ACCENT))
        self.finish(8)

        self.start(9,fourier)
        self.reveal(box('선행 연구 · 덧셈',y=3.8,color=PURPLE),t('a + b',y=2.25,size=60),wave(.6,6.4,CYAN),wave(-1.2,1.28,PURPLE),t('푸리에 특징',y=-3,size=42,color=ACCENT))
        self.finish(9)

        self.start(10,fourier)
        self.reveal(t('하나의 숫자',y=4.05,size=31),box('서로 다른 주기의 조합',y=2.85,color=ACCENT),
                    wave(1.1,6.4,CYAN),wave(-.4,2.56,PURPLE),wave(-1.9,1.28,GOOD),t('느린 주기   +   중간 주기   +   빠른 주기',y=-3.35,size=22,color=MUTED))
        self.finish(10)

        self.start(11,fourier)
        self.reveal(t('저주파 · 대략적인 크기',y=3.8,size=31,color=CYAN),wave(2.5,9,CYAN),
                    t('고주파 · 홀짝 같은 나머지 관계',y=.8,size=29,color=PURPLE),wave(-.5,1.28,PURPLE))
        # Discrete integer samples alternate sign: a period-2 feature.
        dots=VGroup(*[Dot(p(-3+i*.6,-2.1+(.3 if i%2==0 else -.3)),radius=.07,color=GOOD if i%2==0 else ACCENT) for i in range(11)])
        self.play(LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=.1),run_time=1.5)
        self.reveal(t('짝  홀  짝  홀  짝  홀 …',y=-3.3,size=29,color=GOOD))
        self.finish(11)

        self.start(12,helix_source)
        curve=ParametricFunction(lambda u:p(1.6*np.cos(u)+.13*u,2.7-.42*u+.35*np.sin(u)),t_range=[0,4*PI,.035],color=PURPLE,stroke_width=4).shift(LEFT*.8)
        self.reveal(t('일반화된 나선 표현',y=4.1,size=31,color=PURPLE))
        self.play(Create(curve),run_time=1.4)
        point=Dot(curve.get_start(),radius=.11,color=ACCENT)
        self.add(point)
        self.play(MoveAlongPath(point,curve),run_time=2.4,rate_func=linear)
        self.reveal(box('a의 표현 + b의 표현 → a+b의 표현',y=-3.25,color=CYAN,size=25))
        self.finish(12)

        self.start(13,'곱셈에 대한 가설 · 이번 연구가 직접 입증하지 않음')
        self.reveal(t('덧셈의 단서',y=3.8,size=33,color=PURPLE),wave(2.3,2.1,PURPLE),
                    arrow((0,1.3),(0,-.2),ACCENT),box('곱셈에서도?',y=-1.4,color=ACCENT,size=45))
        self.finish(13)

        self.start(14,'주기성 해석을 설명하는 개념도 · 곱셈 내부 회로의 재현 아님')
        self.reveal(box('정확한 숫자  8 → 6',y=3.4,color=PRUNE,size=37),
                    box('홀짝 특징  짝수 → 짝수',y=1.6,color=GOOD,size=31),wave(-.1,1.6,GOOD),
                    t('정확한 값은 흔들려도\n주기적 특징은 남을 수 있다',y=-2.7,size=34,color=ACCENT))
        self.finish(14)

        self.start(15,paper)
        self.reveal(box('관찰: 십의 자리 오류의 홀짝 패턴',y=3.4,color=GOOD,size=27),
                    arrow((0,2.6),(0,1.45)),box('해석: 주기적 표현일 가능성',y=.7,color=ACCENT,size=29),
                    box('내부 계산의 직접 입증은 아직',y=-1.8,color=PRUNE,size=29))
        self.finish(15)

        self.start(16)
        self.reveal(t('오답의 구조',y=3.1,size=54,color=PRUNE),arrow((0,2.2),(0,.6),CYAN),
                    box('계산 방식에 대한 단서',y=-.4,color=CYAN,size=35),t('관찰에서 시작하는 다음 질문',y=-2.8,size=27,color=MUTED))
        self.finish(16)

        self.start(17,'교육용 평가 화면 · 실험 정확도 수치 아님')
        grid=VGroup(*[box('✓' if i%4 else '×',(i%5-2)*1.1,3-(i//5)*1.05,w=.8,h=.8,color=GOOD if i%4 else PRUNE,size=29) for i in range(20)])
        self.play(LaggedStart(*[FadeIn(c) for c in grid],lag_ratio=.03),run_time=1.4)
        self.reveal(t('몇 개를 맞혔는가?',y=-2.8,size=43,color=CYAN))
        self.finish(17)

        self.start(18)
        self.reveal(box('같은 입력',y=4,color=MUTED),network(1.5,h=1.7),box('같은 정답',y=-1,color=GOOD),
                    t('그 사이의 계산은?',y=-3.0,size=41,color=ACCENT))
        self.finish(18)

        self.start(19)
        self.reveal(t('정답에 이르는 길',y=3.1,size=45),network(.5,h=2),t('출력 뒤에 숨은 규칙을 찾으려면',y=-2.8,size=29,color=CYAN))
        self.finish(19)

        self.start(20)
        self.reveal(t('어떻게',y=3.25,size=49),t('틀리는가?',y=1.6,size=69,color=PRUNE),
                    Line(p(-2.7,.65),p(2.7,.65),color=PRUNE,stroke_width=3),
                    t('오답에 남은 패턴이\n계산의 단서가 된다',y=-1.5,size=38,color=ACCENT))
        self.finish(20)
