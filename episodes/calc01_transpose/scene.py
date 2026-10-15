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
    DURATION = 107

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.add(label('계산의 두 얼굴  /  01', y=7.35, size=21, color=MUTED),
                 label('Transpose는 정말\n행렬을 뒤집을까?', y=6.4, size=32),
                 Line(p(-3.9, 5.65), p(3.9, 5.65), color=MUTED, stroke_opacity=.35),
                 label('1부 · 계산하지 않아도 비용이 발생한다', y=-7.45, size=18, color=MUTED))

        # Segment: all 12 values keep their identity while changing coordinates.
        self.section('01  행과 열을 바꾸면', '행렬의 행과 열을 바꾸는 Transpose.')
        a = matrix(y=1.5)
        a_name = label('A · 3 × 4', y=3.65, color=WEIGHT)
        self.show(VGroup(a, a_name))
        self.to(2)
        self.sub('숫자를 더하거나 곱하지 않습니다.\n원소의 위치 관계만 바뀌는 연산입니다.')
        b = matrix(True, y=1.5)
        self.play(*[a[k].animate.move_to(b[k]) for k in range(12)],
                  Transform(a_name,label('B · 4 × 3', y=3.65, color=ACCENT)),run_time=2.2)
        self.show(VGroup(label('B · 4 × 3', y=-1.05, color=ACCENT),
                         label('Bᵢⱼ = Aⱼᵢ', y=-2.35, size=40),
                         label('숫자는 그대로 · 위치 관계만 변경', y=-3.5, size=26, color=GOOD)))
        self.to(6)

        # Segment: reveal row-major storage, with each row mapped to consecutive offsets.
        self.section('02  메모리에서는 한 줄로', '컴퓨터의 메모리는\n우리가 보는 행렬 모양과 다릅니다.')
        a = matrix(y=2.2)
        mem = memory(['']*12, -1.7)
        self.show(VGroup(a, mem, label('A · 행 우선 배열', y=4, color=WEIGHT),
                         label('원소 위치  0 → 11', y=-2.6, size=23, color=MUTED)))
        self.to(11)
        self.sub('일반적인 행 우선 배열에서는\n숫자들이 한 줄로 이어져 저장됩니다.')
        for row in range(3):
            moving = VGroup(*[a[row*4+j].copy() for j in range(4)])
            self.add(moving)
            self.play(*[moving[j].animate.scale(.55/.78).move_to(mem[row*4+j]) for j in range(4)], run_time=.8)
            self.stage.add(moving)
            self.play(Circumscribe(VGroup(*[mem[row*4+j] for j in range(4)]), color=ACCENT), run_time=.25)
        self.show(label('2차원 좌표 → 1차원 주소', y=-3.65, color=GOOD))
        self.to(15)

        # Segment: 4 illustrated lanes, actual 32-byte segments / 8 FP32 elements.
        self.section('03  같은 개수, 다른 주소', 'GPU의 여러 스레드는\n메모리에 동시에 접근합니다.')
        self.show(label('Warp · 함께 실행되는 32개 스레드', y=4.3, size=25, color=WEIGHT))
        self.show(label('그중 4개 스레드의 요청만 표시', y=3.65, size=21, color=MUTED))
        self.access_panel(1.45, [0, 1, 2, 3], 'Coalesced Access', GOOD)
        self.to(18)
        self.sub('가까운 주소를 함께 읽으면 효율적이지만,')
        self.to(22)
        self.sub('주소가 멀리 떨어져 있으면\n더 많은 메모리 트랜잭션이 필요할 수 있습니다.')
        self.access_panel(-2.0, [0, 8, 16, 24], 'Strided Access', PRUNE)
        self.show(label('FP32 · 정렬된 32B 구간 · 캐시 효과 생략', y=-4.65, size=20, color=MUTED))
        self.to(26)

        # Segment: concrete 3x4 -> 4x3 materialized row-major transpose.
        self.section('04  읽기는 연속, 쓰기는 간격', '별도의 전치 행렬을\n만든다고 생각해 보겠습니다.')
        self.show(label('별도의 행 우선 출력 배열 · 단순 전치 커널', y=4.3, size=22, color=ACCENT))
        a = memory(range(1, 13), 2.7, range(4))
        order = [1,5,9,2,6,10,3,7,11,4,8,12]
        b = memory(['']*12, -2.0, [0,3,6,9], PRUNE)
        self.show(VGroup(a, b, label('입력 A · 3 × 4', y=3.5, size=25, color=WEIGHT),
                         label('출력 B · 4 × 3', y=-3.1, size=25, color=PRUNE)))
        threads = VGroup(*[cell(f'T{j}', .68, SPARSE, 22).move_to(p(-2.7+j*1.8, .65)) for j in range(4)])
        reads = VGroup(*[Arrow(a[j].get_bottom(), threads[j].get_top(), buff=.12, color=WEIGHT, stroke_width=2) for j in range(4)])
        self.show(VGroup(threads, reads))
        self.to(29)
        self.sub('원본 행을 연속으로 읽더라도,')
        moving = VGroup(*[a[j].copy() for j in range(4)])
        self.add(moving)
        self.play(*[moving[j].animate.move_to(threads[j]) for j in range(4)], run_time=1.1)
        self.to(31)
        self.sub('전치된 행렬에 기록할 때는\n주소가 멀리 떨어질 수 있습니다.')
        writes = VGroup(*[Arrow(threads[j].get_bottom(), b[j*3].get_top(), buff=.13, color=PRUNE, stroke_width=2) for j in range(4)])
        self.show(writes)
        self.play(*[moving[j].animate.scale(.8).move_to(b[j*3]) for j in range(4)], run_time=1.5)
        self.stage.add(moving)
        self.show(VGroup(*[label(f'+{j*3}', b[j*3].get_x(), -2.6, 18, PRUNE) for j in range(4)]))
        rest = VGroup(*[label(v, b[k].get_x(), -2, 21, MUTED, .48) for k,v in enumerate(order) if k not in [0,3,6,9]])
        self.show(rest)
        self.show(label('출력 위치: 0, 3, 6, 9  ·  작은 주소 예시', y=-4.05, size=22, color=MUTED))
        self.to(35)

        # Segment: no movement: swap shape/stride descriptors of the same storage.
        self.section('05  반드시 숫자를 옮겨야 할까?', '그런데 반드시\n숫자들을 옮겨야 할까요?')
        storage = memory(range(1,13), .1, [0,4,8])
        self.show(VGroup(storage,label('동일한 저장 공간 · 원소는 움직이지 않음',y=1.05,size=25,color=GOOD)))
        meta=VGroup(label('shape  (3, 4)',y=3.55,size=31,color=WEIGHT),
                    label('stride  (4, 1)',y=2.65,size=31,color=WEIGHT))
        self.show(meta)
        self.to(38)
        self.sub('행렬의 원소는 그대로 두고,\n행과 열을 해석하는 방법만 바꿀 수도 있습니다.')
        self.play(Transform(meta,VGroup(label('shape  (4, 3)',y=3.55,size=31,color=ACCENT),
                                      label('stride  (1, 4)',y=2.65,size=31,color=ACCENT))),run_time=1.3)
        self.to(42)
        self.sub('일부 텐서 연산에서는\nTranspose가 데이터를 복사하지 않습니다.')
        self.show(label('View · 같은 데이터, 새로운 주소 해석',y=-1.1,size=27,color=SPARSE))
        self.show(label('B[i, j] → 원소 위치 i + 4j',y=-2.2,size=29,color=ACCENT))
        self.to(47)
        self.sub('행렬의 크기와 메모리 간격을 나타내는\n정보만 바꾸는 것입니다.')
        self.show(label('stride는 각 축에서 한 칸 이동할 때의 원소 간격',y=-3.35,size=21,color=MUTED))
        self.show(label('PyTorch · 일반적인 strided tensor의 transpose()',y=-4.3,size=20,color=MUTED))
        self.to(50)

        # Segment: compare equal logical rows, different physical addresses.
        self.section('06  비용은 나중에 나타날 수도', '실제 재배열과 기존 배열을 다르게 읽는 경우는\n이후의 메모리 접근 패턴이 달라질 수 있습니다.')
        ordered=[1,5,9,2,6,10,3,7,11,4,8,12]
        packed=memory(ordered,2.2,[0,1,2],GOOD)
        shared=memory(range(1,13),-1.25,[0,4,8],SPARSE)
        self.show(VGroup(packed,shared,
                         label('실제 데이터 재배열 · 별도 출력 배열',y=3.2,size=26,color=GOOD),
                         label('메타데이터만 변경 · 원본 저장소 공유',y=-.25,size=26,color=SPARSE)))
        top=VGroup(*[cell(v,.8,GOOD).move_to(p(-1.2+j*1.2, .9)) for j,v in enumerate([1,5,9])])
        bottom=VGroup(*[cell(v,.8,SPARSE).move_to(p(-1.2+j*1.2,-2.6)) for j,v in enumerate([1,5,9])])
        self.show(VGroup(*[Arrow(packed[j].get_bottom(),top[j].get_top(),color=GOOD,buff=.1,stroke_width=2) for j in range(3)]))
        self.show(VGroup(*[Arrow(shared[j*4].get_bottom(),bottom[j].get_top(),color=SPARSE,buff=.1,stroke_width=2) for j in range(3)]))
        self.play(*[TransformFromCopy(packed[j][1],top[j]) for j in range(3)],run_time=.8)
        self.stage.add(top)
        self.play(*[TransformFromCopy(shared[j*4][1],bottom[j]) for j in range(3)],run_time=.8)
        self.stage.add(bottom)
        self.show(label('동일한 B의 첫 행 [1, 5, 9] · 다른 읽기 주소',y=-3.65,size=25,color=ACCENT))
        self.to(60)
        self.sub('전치할 때 미리 정리할지,\n사용할 때 다른 주소 순서로 읽을지의 차이입니다.')
        self.show(label('후속 연산에 따라 유리한 방식은 달라짐',y=-4.6,size=22,color=MUTED))
        self.to(66)

        # Segment: three logical execution choices for the same product.
        self.section('07  Transpose 다음에 MatMul이 있다면', '예를 들어 Y = XWᵀ.\n같은 결과를 만드는 경로는 여러 가지입니다.')
        self.show(label('Y = XWᵀ',y=3.95,size=42))
        for y,tag,detail,c in [(2.55,'A · 실제 재배열','W → 별도 전치 배열 → MatMul',GOOD),
                               (.7,'B · View','W → stride 변경 → MatMul',SPARSE),
                               (-1.15,'C · MatMul이 직접 처리','W → 전치 operand 지원 → MatMul',WEIGHT)]:
            panel=RoundedRectangle(width=7.5,height=1.5,corner_radius=.12,color=c).move_to(p(0,y))
            self.show(VGroup(panel,label(tag,y=y+.4,size=25,color=c),label(detail,y=y-.3,size=25)))
        self.to(71)
        self.sub('별도 배열, View, 전치 배치를 지원하는 행렬곱.\n중간 저장과 커널 지원에 따라 비용이 달라집니다.')
        self.to(77)
        self.sub('View와 직접 처리는 실제 구현에서\n같은 접근이 될 수도 있습니다.')
        self.show(label('B와 C는 실제 구현에서 같은 접근이 될 수도 있음',y=-2.65,size=23,color=MUTED))
        self.show(label('Transpose만 따로 재면 전체 비용은 보이지 않는다',y=-3.8,size=27,color=ACCENT))
        self.to(81)

        # Segment: an explicitly hypothetical amortization model, not a benchmark.
        self.section('08  한 번 쓸까, 여러 번 쓸까?', '한 번만 쓴다면 재배열을 생략하는 편이\n유리할 수 있습니다.')
        self.show(label('같은 W를 유지하며 k번 사용',y=4.05,size=27,color=ACCENT))
        self.show(VGroup(label('View:  T ≈ k × T_strided',y=3.05,size=29,color=SPARSE),
                         label('Copy:  T ≈ T_transpose + k × T_contiguous',y=2.15,size=26,color=GOOD)))
        self.show(label('가상 비용 모형 · 실측 아님 · 단위 없음',y=1.3,size=22,color=MUTED))
        # Toy costs: transpose=3, strided use=2, contiguous use=1.
        self.show(label('가정: 재배열 3 · View 사용 2 · 재배열 후 사용 1',y=.6,size=22,color=MUTED))
        def costs(k,y):
            return VGroup(label(f'k = {k}',-3.05,y,26,ACCENT,1.3),
                          label(f'View  {2*k}',-.8,y,27,SPARSE,2),
                          label(f'Copy  {3+k}',2.1,y,27,GOOD,2.5))
        self.show(costs(1,-.55))
        self.to(85)
        self.sub('반복해서 쓴다면 한 번 재배열하고,\n이후의 접근 비용을 줄이는 편이 유리할 수도 있습니다.')
        self.show(costs(6,-1.75))
        self.show(label('한 번: 2 < 4     반복: 12 > 9',y=-2.8,size=28,color=ACCENT))
        self.to(90)
        self.sub('이 비교는 단순화한 모형입니다.\n캐시와 데이터 크기, 커널의 레이아웃 지원도 영향을 줍니다.')
        self.show(label('실제 MatMul에서는 전치 operand가 불리하지 않을 수도 있음',y=-4.0,size=21,color=MUTED))
        self.to(96)

        # Segment: choose an execution path for the whole computation.
        self.section('09  가장 싼 전치가 가장 빠른 계산일까?', '중요한 것은 Transpose 하나의 비용이 아닙니다.\n그 결과를 어떻게 사용할지가 선택을 바꿉니다.')
        self.show(label('Transpose + 후속 연산 전체',y=3.4,size=34,color=ACCENT))
        nodes=VGroup(*[RoundedRectangle(width=2.15,height=1.3,corner_radius=.12,color=c).move_to(p(x,.9))
                       for x,c in [(-2.8,WEIGHT),(0,SPARSE),(2.8,GOOD)]])
        self.show(VGroup(nodes,label('표현 선택',-2.8,.9,26,WEIGHT,1.9),
                         label('사용 방식',0,.9,26,SPARSE,1.9),label('전체 비용',2.8,.9,26,GOOD,1.9),
                         Arrow(p(-1.65,.9),p(-1.15,.9),buff=0,color=MUTED),
                         Arrow(p(1.15,.9),p(1.65,.9),buff=0,color=MUTED)))
        self.to(102)
        self.sub('수학적으로 같은 여러 경로 중,\n이후의 계산까지 고려해 전체 비용을 낮추는 경로를 고릅니다.')
        self.show(label('지금 가장 싼 연산보다\n전체 계산에 유리한 실행 경로',y=-1.6,size=33,color=GOOD))
        self.show(label('컴파일러가 연산들의 연결 관계를 보는 이유',y=-3.7,size=27,color=ACCENT))
        self.to(107)

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
