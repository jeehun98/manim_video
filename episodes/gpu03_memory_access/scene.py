"""GPU 03: identical per-element work, different warp memory access. 175s."""
import os
import sys
from pathlib import Path
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from gpu_series.components import DataCell, DataArrow
from gpu_series.style import label as txt

config.pixel_width = int(os.getenv('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#091119'
INK, MUTED, MINT, BLUE, GOLD, PINK = '#EDF3F7', '#94A7B7', '#61E4CF', '#68D9F0', '#F3CF75', '#FF8C9D'
HEAD_Y, SUB_Y, EPS = 3.65, -5.85, 1e-6
LANE_STEP, ROW_STEP, CELL = .82, 1.48, .57
WARP_SIZE, ELEMENT_BYTES, SECTOR_BYTES = 32, 4, 32
DURATION = 175

# Source of truth: fixed screen transition time, action, exact on-screen words.
# narration.md and captions.srt copy these words; tts_script.txt changes pronunciation only.
CAPTIONS = [
 (0, 'recap', '앞에서는 32개의 Thread가 하나의 Warp를 이루고,\n같은 명령을 함께 실행한다고 했습니다.'),
 (6, 'memory', '이번에는 이 Thread들이\n메모리에서 데이터를 읽는 모습을 보겠습니다.'),
 (10, 'contiguous', '하나의 Warp가\n연속된 배열을 읽는다고 해보겠습니다.'),
 (14, 'neighbors', 'Thread 0은 x₀, Thread 1은 x₁, Thread 2는 x₂.\n각 Thread가 바로 옆의 값을 읽습니다.'),
 (21, 'nearby', 'Thread들이 요청하는 주소도\n메모리에서 서로 가깝게 모여 있습니다.'),
 (25, 'merge_requests', 'GPU는 이렇게 모인 요청을\n효율적인 메모리 접근으로 묶어 처리할 수 있습니다.'),
 (31, 'coalesced', '이런 형태를 보통\nCoalesced Memory Access라고 합니다.'),
 (37, 'change_pattern', '이번에는 계산은 그대로 두고,\nThread들이 읽는 위치만 바꿔보겠습니다.'),
 (42, 'stride_indices', 'Thread 0은 x₀, Thread 1은 x₃₂,\nThread 2는 x₆₄, Thread 3은 x₉₆을 읽습니다.'),
 (49, 'same_compute', '각 Thread가 수행하는 계산은 이전과 같습니다.\n읽은 값에 1을 더합니다.'),
 (53, 'scattered', '하지만 이번에는 요청하는 주소들이\n메모리에서 서로 멀리 떨어져 있습니다.'),
 (57, 'same_work', 'Thread 수는 같고, 계산도 같습니다.\n달라진 것은 데이터를 읽는 위치입니다.'),
 (61, 'few_transactions', '연속된 주소를 읽을 때는 여러 Thread의 요청을\n비교적 적은 메모리 트랜잭션으로 처리할 수 있습니다.'),
 (68, 'many_transactions', '주소가 멀리 흩어지면\n더 많은 메모리 트랜잭션이 필요할 수 있습니다.'),
 (75, 'same_bytes', '같은 양의 값을 읽어도,\n요청이 걸치는 메모리 영역 수는 달라집니다.'),
 (80, 'not_only_compute', '즉, GPU에서 성능을 결정하는 것은\n계산량만이 아닙니다.'),
 (85, 'read_write', 'Thread들이 어떤 주소의 데이터를\n읽고 쓰는지도 중요합니다.'),
 (90, 'matrix_intro', '이 차이는 배열뿐 아니라,\n행렬이나 이미지 같은 큰 데이터를 다룰 때도 중요합니다.'),
 (96, 'row_major', '예를 들어 한 행이 32개인 행렬을\n행 순서대로 메모리에 저장했다고 해보겠습니다.'),
 (102, 'read_row', 'Warp의 Thread들이 같은 행의 옆 원소들을 읽으면,\n연속된 메모리 주소에 접근할 수 있습니다.'),
 (109, 'read_column', '반대로 같은 열을 따라 읽으면,\n이 예제에서는 주소가 32개 원소 간격으로 떨어집니다.'),
 (116, 'same_matrix', '결국 같은 행렬 원소들을 모두 읽더라도,\n한 번의 Warp 요청에 묶이는 주소는 달라질 수 있습니다.'),
 (123, 'warp_view', '여기서는 Thread 하나의 접근만 보지 말고,\nWarp 전체가 어떤 주소들을 함께 요청하는지 봐야 합니다.'),
 (129, 'close_again', 'Warp 안의 Thread들이 가까운 주소를 읽으면,\n메모리 접근을 더 효율적으로 처리할 수 있습니다.'),
 (135, 'far_again', '반대로 접근 주소가 흩어져 있다면,\n같은 양을 읽더라도 더 많은 비용이 들 수 있습니다.'),
 (141, 'no_speed_claim', '실제 속도 차이는 캐시와 정렬 상태 등에도\n영향을 받지만, 접근 패턴은 중요한 출발점입니다.'),
 (147, 'layout', 'GPU 최적화에서는 무엇을 계산하는지만큼\n데이터를 어떤 순서로 배치하는지도 중요합니다.'),
 (153, 'thread_order', '그리고 Warp의 Thread들이\n어떤 순서로 읽고 쓰게 할지도 중요합니다.'),
 (158, 'same_kernel', '같은 Kernel, 같은 Thread 수,\n같은 계산이라도,'),
 (163, 'pattern', 'Warp가 요청하는 주소의 배치가 달라지면\n메모리에서 처리해야 할 일이 달라집니다.'),
 (169, 'ending', '메모리 접근 패턴 하나만으로도\nGPU의 실행 성능은 달라질 수 있습니다.'),
]


def sector_ids(stride):
    """Aligned 4-byte scalar reads; not a DRAM transaction or timing simulator."""
    return [(i * stride * ELEMENT_BYTES) // SECTOR_BYTES for i in range(WARP_SIZE)]


class AccessBoard(VGroup):
    """32 lane/address pairs folded into four rows. Lane identities stay fixed."""
    def __init__(self, stride=1):
        super().__init__()
        self.stride = stride
        self.threads, self.cells, self.arrows = VGroup(), VGroup(), VGroup()
        for i in range(WARP_SIZE):
            r,c = divmod(i,8)
            x,y = (c-3.5)*LANE_STEP, 2.55-r*ROW_STEP
            thread=txt(f'T{i}',17,GOLD).move_to([x,y,0])
            # Fold long address distances, but also separate/stagger targets so
            # changing the pattern visibly redirects the same 32 requesters.
            cell_x=x if stride==1 else x*1.13
            cell_y=y-.7 if stride==1 else y-.7+(.12 if c%2 else -.12)
            cell=DataCell(f'x{i*stride}',CELL,BLUE).move_to([cell_x,cell_y,0])
            arrow=DataArrow(thread.get_bottom(),cell.get_top(),GOLD)
            self.threads.add(thread);self.cells.add(cell);self.arrows.add(arrow)
        self.add(self.threads,self.cells,self.arrows)

    def regions(self, color=MINT):
        groups = {}
        for i,sector in enumerate(sector_ids(self.stride)):
            groups.setdefault(sector,[]).append(self.cells[i])
        return VGroup(*[SurroundingRectangle(VGroup(*cells),buff=self.cells[0].width*.12,color=color,stroke_width=2)
                        for cells in groups.values()])


class MemoryAccessIntroduction(Scene):
    def construct(self):
        self.stage, self.sub, self.head = VGroup(), VGroup(), VGroup()
        self.add(txt('GPU COMPUTATION SERIES',19,MUTED).move_to(UP*6.85),
                 txt('Memory Access',53).move_to(UP*5.65),
                 txt('03  /  같은 계산, 다른 메모리 접근',23,MINT).move_to(UP*4.65))
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub)
            self.sub=txt(caption,28).move_to(UP*SUB_Y)
            self.add(self.sub)
            # The action and narration share this exact screen-time interval.
            self.play(*getattr(self,action)(),run_time=end-start-EPS)
            if abs(self.time-end)>1/30+.001:
                raise ValueError(f'Timeline drift at {action}: {self.time} / {end}')

    def heading(self,text):
        self.remove(self.head)
        self.head=txt(text,29,MINT).move_to(UP*HEAD_Y)
        self.add(self.head)

    def track(self,*items):
        self.stage.add(*items)

    def replace(self,*items):
        old=self.stage
        self.stage=VGroup(*items)
        return [Succession(FadeOut(old,run_time=.12),AnimationGroup(*[FadeIn(m) for m in items],run_time=.88))]

    def recap(self):
        self.heading('32 Threads = 1 Warp')
        self.board=AccessBoard()
        self.warp=SurroundingRectangle(self.board.threads,buff=.25,color=GOLD)
        self.track(self.board.threads,self.warp)
        return [LaggedStart(*[FadeIn(t) for t in self.board.threads],lag_ratio=.035),Create(self.warp)]

    def memory(self):
        self.heading('Warp의 요청 → Global Memory')
        self.note=txt('32개 요청을 4줄로 접어 표시',21,MUTED).move_to(DOWN*3.5)
        self.track(self.board.cells,self.note)
        self.stage.remove(self.warp)
        return [FadeOut(self.warp),FadeIn(self.board.cells),Write(self.note)]

    def contiguous(self):
        self.heading('연속 접근  /  Tᵢ → xᵢ')
        self.track(self.board.arrows)
        self.compute=txt('공통 연산: 읽은 값 + 1',25,GOLD).move_to(DOWN*4.15)
        self.track(self.compute)
        return [LaggedStart(*[GrowArrow(a) for a in self.board.arrows],lag_ratio=.03),Write(self.compute)]

    def neighbors(self):
        return [Succession(*[Indicate(VGroup(self.board.threads[i],self.board.cells[i]),color=BLUE) for i in range(3)])]

    def nearby(self):
        return [LaggedStart(*[Circumscribe(VGroup(*self.board.cells[r*8:(r+1)*8]),color=BLUE,buff=.06) for r in range(4)],lag_ratio=.25)]

    def merge_requests(self):
        self.regions=self.board.regions()
        self.track(self.regions)
        note=txt('예: 4 B 원소 · 32 B 정렬 → 32 B 영역 4개',20,MUTED).move_to(self.note)
        return [LaggedStart(*[Create(r) for r in self.regions],lag_ratio=.35),Transform(self.note,note)]

    def coalesced(self):
        self.heading('Coalesced Memory Access')
        self.envelope=SurroundingRectangle(self.board,buff=.27,color=MINT,stroke_width=1.4)
        note=txt('연속 128 B 범위 · 안쪽 박스는 32 B 영역',20,MINT).move_to(self.note)
        self.track(self.envelope)
        return [Create(self.envelope),Transform(self.note,note)]

    def change_pattern(self):
        self.heading('주소 간격만 변경  /  Tᵢ → x₃₂ᵢ')
        new=AccessBoard(stride=32)
        # Per-lane transforms preserve the identity of all 32 requesters.
        self.stage.remove(self.regions,self.envelope)
        self.board.stride=32
        note=txt('주소 사이의 큰 간격은 축약해서 표시',21,MUTED).move_to(self.note)
        return [FadeOut(self.regions),FadeOut(self.envelope),Transform(self.note,note),
                *[Transform(a,b) for a,b in zip(self.board.cells,new.cells)],
                *[Transform(a,b) for a,b in zip(self.board.arrows,new.arrows)]]

    def stride_indices(self):
        return [Succession(*[Indicate(VGroup(self.board.threads[i],self.board.cells[i]),color=PINK) for i in range(4)])]

    def same_compute(self):
        return [Indicate(self.compute,color=GOLD),Indicate(self.board.threads,color=GOLD)]

    def scattered(self):
        self.heading('떨어진 주소 → 서로 다른 요청 영역')
        self.regions=self.board.regions(PINK)
        self.track(self.regions)
        return [LaggedStart(*[Create(r) for r in self.regions],lag_ratio=.035)]

    def same_work(self):
        note=txt('32 Threads · 32개 값 · 각자 +1',25,GOLD).move_to(self.compute)
        return [Transform(self.compute,note),Indicate(self.regions,color=PINK)]

    def make_comparison(self):
        self.left=AccessBoard(1).scale(.49).move_to(LEFT*1.95+UP*.05)
        self.right=AccessBoard(32).scale(.49).move_to(RIGHT*1.95+UP*.05)
        self.left_regions=self.left.regions(MINT)
        self.right_regions=self.right.regions(PINK)
        self.left_title=txt('연속 주소',28,MINT).move_to([-1.95,2.2,0])
        self.right_title=txt('32개 원소 간격',25,PINK).move_to([1.95,2.2,0])
        self.left_count=txt('32 B 영역 4개',25,MINT).move_to([-1.95,-2.15,0])
        self.right_count=txt('32 B 영역 32개',25,PINK).move_to([1.95,-2.15,0])
        assumption=txt('4 B 원소 · 32 B 정렬 · 한 Warp의 읽기 요청 예시',20,MUTED).move_to(DOWN*3.2)
        qualifier=txt('요청 영역 수 비교 · 실제 시간 비율은 아님',21,MUTED).move_to(DOWN*3.8)
        return [self.left,self.right,self.left_title,self.right_title,assumption,qualifier]

    def few_transactions(self):
        self.heading('같은 32개 값, 다른 요청 묶음')
        items=self.make_comparison()
        return self.replace(*items,self.left_regions,self.left_count)

    def many_transactions(self):
        self.track(self.right_regions,self.right_count)
        return [LaggedStart(*[Create(r) for r in self.right_regions],lag_ratio=.035),Write(self.right_count)]

    def same_bytes(self):
        amount=txt('필요한 데이터는 양쪽 모두 128 B',28,GOLD).move_to(UP*3)
        self.track(amount)
        return [Write(amount),Succession(Indicate(self.left_count),Indicate(self.right_count))]

    def not_only_compute(self):
        self.heading('계산량 + 데이터를 가져오는 방식')
        return [Circumscribe(VGroup(self.left_count,self.right_count),color=GOLD,buff=.2)]

    def read_write(self):
        self.heading('읽기·쓰기 모두 주소 패턴을 보자')
        return [LaggedStart(*[Indicate(self.left.cells[i],color=MINT) for i in [0,1,2,3]],lag_ratio=.25),
                LaggedStart(*[Indicate(self.right.cells[i],color=PINK) for i in [0,1,2,3]],lag_ratio=.25)]

    def matrix_intro(self):
        self.heading('행렬에서 만나는 메모리 접근')
        self.matrix=VGroup(*[DataCell(f'x{r*32+c}',.69,BLUE).move_to([(c-1.5)*.9,2.2-r*.86,0])
                             for r in range(4) for c in range(4)])
        crop=txt('32 × 32 행렬의 왼쪽 위 일부',22,MUTED).move_to(UP*3)
        dots=VGroup(*[txt('…',25,MUTED).move_to([2.35,2.2-r*.86,0]) for r in range(4)],
                    txt('⋮',28,MUTED).move_to([0,-1,0]))
        self.layout_label=txt('한 행은 32개 원소',26,GOLD).move_to(DOWN*1.75)
        return self.replace(self.matrix,crop,dots,self.layout_label)

    def row_major(self):
        self.heading('행 우선 저장  /  행을 이어 붙인 메모리')
        label=txt('행 우선: x₀ … x₃₁ → x₃₂ … x₆₃ → …',24,GOLD).move_to(self.layout_label)
        return [Transform(self.layout_label,label),Succession(*[Indicate(VGroup(*self.matrix[r*4:(r+1)*4]),color=MINT) for r in range(4)])]

    def read_row(self):
        self.heading('같은 행: 이웃한 Thread → 이웃한 주소')
        self.selection=SurroundingRectangle(VGroup(*self.matrix[:4]),buff=.1,color=MINT)
        self.memory_row=VGroup(*[DataCell(f'x{i}',.65,MINT).move_to([(i-1.5)*1.65,-3,0]) for i in range(4)])
        labels=VGroup(*[txt(f'T{i}',20,GOLD).next_to(c,UP,buff=.15) for i,c in enumerate(self.memory_row)])
        self.memory_title=txt('T0–T3의 요청  /  x₀, x₁, x₂, x₃',23,MINT).move_to(DOWN*4)
        self.track(self.selection,self.memory_row,labels,self.memory_title)
        return [Create(self.selection),*[TransformFromCopy(self.matrix[i],self.memory_row[i]) for i in range(4)],FadeIn(labels),Write(self.memory_title)]

    def read_column(self):
        self.heading('같은 열: 이웃한 Thread → 떨어진 주소')
        col=SurroundingRectangle(VGroup(*[self.matrix[r*4] for r in range(4)]),buff=.1,color=PINK)
        target=VGroup(*[DataCell(f'x{i*32}',.65,PINK).move_to(c) for i,c in enumerate(self.memory_row)])
        gaps=VGroup(*[txt('…',22,MUTED).move_to([(i-1)*1.65,-3,0]) for i in range(3)])
        self.track(gaps)
        title=txt('T0–T3의 요청  /  x₀, x₃₂, x₆₄, x₉₆',23,PINK).move_to(self.memory_title)
        return [Transform(self.selection,col),Transform(self.memory_row,target),FadeIn(gaps),Transform(self.memory_title,title)]

    def same_matrix(self):
        self.heading('전체 원소는 같아도, 요청을 묶는 순서는 다르다')
        return [Succession(LaggedStart(*[Indicate(VGroup(*self.matrix[r*4:(r+1)*4]),color=MINT) for r in range(4)],lag_ratio=.35),
                           LaggedStart(*[Indicate(VGroup(*[self.matrix[r*4+c] for r in range(4)]),color=PINK) for c in range(4)],lag_ratio=.35))]

    def warp_view(self):
        self.heading('한 Thread가 아닌, Warp 전체의 요청')
        self.overview=AccessBoard(1)
        self.overview_regions=self.overview.regions(MINT)
        note=txt('32개의 주소를 함께 보자',26,GOLD).move_to(DOWN*3.8)
        return self.replace(self.overview,note)

    def close_again(self):
        self.track(self.overview_regions)
        return [LaggedStart(*[Create(r) for r in self.overview_regions],lag_ratio=.35)]

    def far_again(self):
        items=self.make_comparison()
        return self.replace(*items,self.left_regions,self.right_regions,self.left_count,self.right_count)

    def no_speed_claim(self):
        self.heading('영역 수의 차이 ≠ 실행 시간의 고정 비율')
        return [Succession(Indicate(self.left_count),Indicate(self.right_count))]

    def layout(self):
        self.heading('데이터 배치와 작업 배치를 함께 설계')
        self.final_data=VGroup(*[DataCell(f'x{i}',.65,BLUE) for i in range(8)]).arrange(RIGHT,buff=.18).move_to(DOWN*.4)
        self.final_threads=VGroup(*[txt(f'T{i}',23,GOLD).move_to([c.get_x(),1.2,0]) for i,c in enumerate(self.final_data)])
        label=txt('데이터의 저장 순서',30,BLUE).move_to(DOWN*2)
        detail=txt('32개 Thread 중 T0–T7 확대',20,MUTED).move_to(UP*3.05)
        return self.replace(self.final_data,self.final_threads,label,detail)

    def thread_order(self):
        self.final_arrows=VGroup(*[DataArrow(t.get_bottom(),c.get_top(),MINT) for t,c in zip(self.final_threads,self.final_data)])
        note=txt('Warp 안에서 어떤 주소를 함께 요청할까?',26,MINT).move_to(UP*2.5)
        self.track(self.final_arrows,note)
        return [LaggedStart(*[GrowArrow(a) for a in self.final_arrows],lag_ratio=.2),Write(note)]

    def same_kernel(self):
        self.heading('같은 Kernel · 같은 Thread 수 · 같은 계산')
        formula=txt('읽은 값 + 1',40,GOLD).move_to(DOWN*3.3)
        self.track(formula)
        return [Write(formula),Indicate(self.final_threads,color=GOLD)]

    def pattern(self):
        self.heading('주소의 배치 → 메모리 요청의 차이')
        return [LaggedStart(*[Indicate(VGroup(t,a,c),color=MINT) for t,a,c in zip(self.final_threads,self.final_arrows,self.final_data)],lag_ratio=.2)]

    def ending(self):
        self.heading('같은 계산이어도, 접근 패턴이 성능을 바꾼다')
        conclusion=txt('계산 + 메모리 접근',40,MINT)
        return self.replace(conclusion)
