"""A materialized transpose: mathematical relation versus memory traffic."""
import sys
from pathlib import Path
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from visual_library.manim import BG, INK, MUTED, WEIGHT, PRUNE, SPARSE, ACCENT, GOOD, txt, configure_vertical

configure_vertical()
config.disable_caching = True


def p(x, y):
    return np.array([x, y, 0.0])


def label(s, x=0, y=0, size=26, color=INK, width=7.8):
    return txt(s, size, color, width).move_to(p(x, y))


def cell(value, width=.65, color=WEIGHT, size=24):
    return VGroup(RoundedRectangle(width=width, height=.65, corner_radius=.06,
                                  color=color, stroke_width=1.5, fill_color=BG, fill_opacity=1),
                  label(value, size=size, width=width-.08))


def matrix(transposed=False, y=1.5):
    group = VGroup()
    for i in range(3):
        for j in range(4):
            row, col = (j, i) if transposed else (i, j)
            cols, rows = (3, 4) if transposed else (4, 3)
            group.add(cell(i*4+j+1, .78, ACCENT if i == 0 else WEIGHT)
                      .move_to(p((col-(cols-1)/2)*.95, y+((rows-1)/2-row)*.85)))
    return group


def memory(values, y, highlighted=(), color=ACCENT):
    return VGroup(*[cell(v, .55, color if k in highlighted else MUTED, 21)
                   .move_to(p((k-5.5)*.63, y)) for k, v in enumerate(values)])


class TransposeCost(Scene):
    DURATION = 74

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.add(label('계산의 두 얼굴  /  01', y=7.35, size=21, color=MUTED),
                 label('Transpose는 왜\n계산하지 않아도 느릴까?', y=6.4, size=32),
                 Line(p(-3.9, 5.65), p(3.9, 5.65), color=MUTED, stroke_opacity=.35),
                 label('1부 · 계산하지 않아도 비용이 발생한다', y=-7.45, size=18, color=MUTED))

        # 00–10: all 12 values keep their identity while changing coordinates.
        self.section('01  행과 열을 바꾸면', '행렬의 행과 열을 바꾸는 Transpose.')
        a = matrix(y=1.5)
        a_name = label('A · 3 × 4', y=3.65, color=WEIGHT)
        self.show(VGroup(a, a_name))
        self.to(2)
        self.sub('숫자를 더하거나 곱하지도 않습니다.\n원소의 위치만 서로 바꾸면 됩니다.')
        b = matrix(True, y=1.5)
        self.play(*[a[k].animate.move_to(b[k]) for k in range(12)],
                  Transform(a_name,label('B · 4 × 3', y=3.65, color=ACCENT)),run_time=2.2)
        self.show(VGroup(label('B · 4 × 3', y=-1.05, color=ACCENT),
                         label('Bᵢⱼ = Aⱼᵢ', y=-2.35, size=40),
                         label('숫자는 그대로 · 위치 관계만 변경', y=-3.5, size=26, color=GOOD)))
        self.to(10)

        # 10–22: reveal row-major storage, with each row mapped to consecutive offsets.
        self.section('02  메모리에서는 한 줄로', '컴퓨터의 메모리는\n우리가 보는 행렬 모양과 다릅니다.')
        a = matrix(y=2.2)
        mem = memory(['']*12, -1.7)
        self.show(VGroup(a, mem, label('A · 행 우선 배열', y=4, color=WEIGHT),
                         label('원소 위치  0 → 11', y=-2.6, size=23, color=MUTED)))
        self.to(13)
        self.sub('일반적인 행 우선 배열에서는\n숫자들이 한 줄로 이어져 저장됩니다.')
        for row in range(3):
            moving = VGroup(*[a[row*4+j].copy() for j in range(4)])
            self.add(moving)
            self.play(*[moving[j].animate.scale(.55/.78).move_to(mem[row*4+j]) for j in range(4)], run_time=1.25)
            self.stage.add(moving)
            self.play(Circumscribe(VGroup(*[mem[row*4+j] for j in range(4)]), color=ACCENT), run_time=.45)
        self.show(label('2차원 좌표 → 1차원 주소', y=-3.65, color=GOOD))
        self.to(22)

        # 22–37: 4 illustrated lanes, actual 32-byte segments / 8 FP32 elements.
        self.section('03  같은 개수, 다른 주소', 'GPU의 여러 스레드는\n메모리에 동시에 접근합니다.')
        self.show(label('Warp · 함께 실행되는 32개 스레드', y=4.3, size=25, color=WEIGHT))
        self.show(label('그중 4개 스레드의 요청만 표시', y=3.65, size=21, color=MUTED))
        self.access_panel(1.45, [0, 1, 2, 3], 'Coalesced Access', GOOD)
        self.to(26)
        self.sub('가까운 주소를 함께 읽으면 효율적이지만,')
        self.to(28)
        self.access_panel(-2.0, [0, 8, 16, 24], 'Strided Access', PRUNE)
        self.sub('주소가 멀리 떨어져 있으면\n더 많은 메모리 트랜잭션이 필요할 수 있습니다.')
        self.show(label('FP32 · 정렬된 32B 구간 · 캐시 효과 생략', y=-4.65, size=20, color=MUTED))
        self.to(37)

        # 37–53: concrete 3x4 -> 4x3 materialized row-major transpose.
        self.section('04  읽기는 연속, 쓰기는 간격', 'Transpose는 읽는 위치와 쓰는 위치의\n행과 열을 뒤바꿉니다.')
        self.show(label('별도의 행 우선 출력 배열 · 단순 전치 커널', y=4.3, size=22, color=ACCENT))
        a = memory(range(1, 13), 2.7, range(4))
        order = [1,5,9,2,6,10,3,7,11,4,8,12]
        b = memory(['']*12, -2.0, [0,3,6,9], PRUNE)
        self.show(VGroup(a, b, label('입력 A · 3 × 4', y=3.5, size=25, color=WEIGHT),
                         label('출력 B · 4 × 3', y=-3.1, size=25, color=PRUNE)))
        threads = VGroup(*[cell(f'T{j}', .68, SPARSE, 22).move_to(p(-2.7+j*1.8, .65)) for j in range(4)])
        reads = VGroup(*[Arrow(a[j].get_bottom(), threads[j].get_top(), buff=.12, color=WEIGHT, stroke_width=2) for j in range(4)])
        self.show(VGroup(threads, reads))
        self.to(41)
        self.sub('원본 행을 연속으로 읽더라도,')
        moving = VGroup(*[a[j].copy() for j in range(4)])
        self.add(moving)
        self.play(*[moving[j].animate.move_to(threads[j]) for j in range(4)], run_time=1.1)
        self.to(44)
        self.sub('전치된 행렬에 기록할 때는\n주소가 멀리 떨어질 수 있습니다.')
        writes = VGroup(*[Arrow(threads[j].get_bottom(), b[j*3].get_top(), buff=.13, color=PRUNE, stroke_width=2) for j in range(4)])
        self.show(writes)
        self.play(*[moving[j].animate.scale(.8).move_to(b[j*3]) for j in range(4)], run_time=1.5)
        self.stage.add(moving)
        self.show(VGroup(*[label(f'+{j*3}', b[j*3].get_x(), -2.6, 18, PRUNE) for j in range(4)]))
        rest = VGroup(*[label(v, b[k].get_x(), -2, 21, MUTED, .48) for k,v in enumerate(order) if k not in [0,3,6,9]])
        self.show(rest)
        self.show(label('출력 위치: 0, 3, 6, 9  ·  작은 주소 예시', y=-4.05, size=22, color=MUTED))
        self.to(53)

        # 53–68: distinguish a relation from the physical execution that realizes it.
        self.section('05  계산량과 실행 비용은 다르다', '값을 더하거나 곱하는 일은 없습니다.')
        left = RoundedRectangle(width=3.65, height=4.1, corner_radius=.15, color=WEIGHT).move_to(p(-2, .9))
        right = RoundedRectangle(width=3.65, height=4.1, corner_radius=.15, color=PRUNE).move_to(p(2, .9))
        self.show(VGroup(left,right,label('Mathematics', -2,2.35,24,WEIGHT,3.2),
                         label('B = Aᵀ', -2,1.1,37,INK,3.2),label('원소의 위치 관계',-2,-.45,23,MUTED,3.2),
                         label('Hardware',2,2.35,24,PRUNE,3.2),label('Load → Store',2,1.1,27,INK,3.2),
                         label('실제 데이터 이동',2,-.45,23,MUTED,3.2)))
        self.to(56)
        self.sub('어디에서 읽고 어디에 쓰는지에 따라\n실제 비용은 달라집니다.')
        requests=VGroup(*[Arrow(p(.65+i*.8,-1.65),p(.65+i*.8,-2.65),color=PRUNE,buff=0,stroke_width=3) for i in range(4)])
        self.show(VGroup(Arrow(p(-2.8,-2.1),p(-1.2,-2.1),color=WEIGHT,buff=0),requests))
        self.to(61)
        self.sub('수학적으로 단순한 연산이\nGPU에서도 단순한 작업인 것은 아닙니다.')
        self.show(label('결과의 관계 ≠ 실행 경로의 비용', y=-3.65, size=29, color=ACCENT))
        self.to(68)

        # 68–74: introduce an unnamed intermediate space, reserve explanation for ep02.
        self.section('NEXT  한 번 더 옮긴다면?', '데이터를 한 번 더 옮기는 것이,\n오히려 더 빠른 방법이 될 수도 있을까요?')
        src=cell('A',1.25,WEIGHT,32).move_to(p(-2.6,1.1))
        dst=cell('B',1.25,PRUNE,32).move_to(p(2.6,1.1))
        gpu=RoundedRectangle(width=2.25,height=3.4,corner_radius=.2,color=MUTED).move_to(p(0,1.1))
        store=RoundedRectangle(width=1.35,height=1.1,corner_radius=.1,color=SPARSE,fill_color=SPARSE,fill_opacity=.12).move_to(p(0,1.1))
        self.show(VGroup(src,dst,gpu,label('GPU 내부',y=2.3,size=22,color=MUTED),store,
                         Arrow(src.get_right(),store.get_left(),buff=.12,color=WEIGHT),
                         Arrow(store.get_right(),dst.get_left(),buff=.12,color=PRUNE)))
        dot=Dot(src.get_center(),color=ACCENT,radius=.12)
        self.add(dot)
        self.play(dot.animate.move_to(store),run_time=.8)
        self.play(dot.animate.move_to(dst),run_time=.8)
        self.play(FadeOut(dot),run_time=.2)
        self.show(label('02 · 메모리를 더 사용하면 왜 빨라질까?', y=-2.3,size=27,color=SPARSE))
        self.to(74)

    def access_panel(self, y, indices, title, color):
        width=.235
        x=lambda k: (k-15.5)*width
        cells=VGroup(*[Rectangle(width=width-.015,height=.43,color=MUTED,stroke_width=.7,
                                 fill_color=color if k in indices else BG,
                                 fill_opacity=.7 if k in indices else 1).move_to(p(x(k),y)) for k in range(32)])
        lanes=VGroup(*[cell(f'T{j}',.64,SPARSE,20).move_to(p(-2.8+j*1.85,y+1)) for j in range(4)])
        lines=VGroup(*[Arrow(lanes[j].get_bottom(),p(x(k),y+.23),buff=.05,color=color,stroke_width=1.6,
                            max_tip_length_to_length_ratio=.12) for j,k in enumerate(indices)])
        self.show(VGroup(label(title,y=y+1.65,size=25,color=color),cells,lanes,lines),.55)
        segments=sorted(set(k//8 for k in indices))
        outlines=VGroup(*[Rectangle(width=width*8,height=.58,color=color,stroke_width=2.2).move_to(p(x(s*8+3.5),y)) for s in segments])
        self.show(VGroup(outlines,label(f'4개 값 요청 → {len(segments)}개 32B 구간',y=y-.7,size=23,color=color)),.55)

    def section(self, title, caption):
        old=VGroup(self.stage,self.head,self.caption)
        if self.time:
            self.play(FadeOut(old),run_time=.25)
        self.stage=VGroup()
        self.head=label(title,y=5.05,size=28,color=ACCENT)
        self.caption=label(caption,y=-6.25,size=27)
        self.add(self.head,self.caption)

    def sub(self, caption):
        new=label(caption,y=-6.25,size=27)
        self.play(ReplacementTransform(self.caption,new),run_time=.2)
        self.caption=new

    def show(self, mob, duration=.4):
        self.play(FadeIn(mob),run_time=duration)
        self.stage.add(mob)

    def to(self, target):
        if self.time > target + 1/30:
            raise RuntimeError(f'Timeline overflow: {self.time:.3f} > {target}')
        if target-self.time > .001:
            self.wait(target-self.time)
