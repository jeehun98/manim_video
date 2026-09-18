"""GPU 06: shared-memory tiling and persistent register accumulation, 174 seconds."""
import os
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from gpu_series.components import DataCell, MemoryBox, DataArrow
from gpu_series.style import label as txt
config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#091119'
BLUE,GOLD,MINT,PINK,MUTED='#68D9F0','#F3CF75','#61E4CF','#FF8C9D','#94A7B7'
HEAD_Y,SUB_Y,NOTE_Y,EPS=3.8,-5.85,-4.6,1e-6
DURATION=174
A=[[1,2,3,4],[2,1,0,3],[4,0,1,2],[1,3,2,0]]
B=[[2,1,3,0],[1,2,0,1],[0,1,2,3],[2,0,1,1]]
C=[[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
# Exact screen captions and transition times; narration uses the same words.
CAPTIONS = [
 (0, 'recap', '앞에서는 Thread 하나가 출력 하나를 계산하는\nNaive GEMM을 살펴봤습니다.'),
 (6, 'repeat', '계산은 맞지만 여러 Thread가 같은 A와 B의 값을\nGlobal Memory에서 반복해서 읽었습니다.'),
 (12, 'intro', '한 번 가져온 데이터를 함께 재사용할 수는 없을까요?\n여기서 Tiling이 등장합니다.'),
 (18, 'tiles', '행렬을 작은 영역으로 나눠 계산합니다. A와 B에서 잘라낸\n작은 사각형을 Tile이라고 부릅니다.'),
 (24, 'block', '하나의 Block이 C의 작은 영역을 맡습니다. 이\nBlock의 Thread들은 필요한 A와 B의 Tile을\n함께 사용합니다.'),
 (30, 'cooperative', '먼저 각 Thread가 Tile의 일부를 나눠 가져옵니다.\nGlobal Memory에서 읽은 값을 Shared\nMemory에 저장합니다.'),
 (36, 'loaded', '이제 필요한 두 Tile이 Block 안에 있습니다.\n가져온 데이터는 같은 Block의 Thread들이 함께 쓸\n수 있습니다.'),
 (42, 'ready', '단, 함께 읽기 전에 적재가 끝났는지 맞춰야 합니다.\n필요한 동기화 뒤에 계산을 시작합니다.'),
 (48, 'reuse_a', 'A의 한 값은 여러 출력에 필요합니다. Shared\nMemory에 한 번 올려두면 여러 Thread가\n재사용합니다.'),
 (54, 'reuse_b', 'B의 값도 마찬가지입니다. 다른 출력 행을 맡은\nThread들이 같은 값을 함께 사용합니다.'),
 (60, 'multiply', '각 Thread는 Shared Memory의 A와 B 값을\n곱하고, 자신의 중간 합에 더합니다.'),
 (66, 'accumulate', '첫 Tile의 부분 합이 만들어졌습니다. 중간 합은 각\nThread의 Register에 유지합니다.'),
 (72, 'before_overwrite', '다음 Tile을 가져오기 전에는, 모든 Thread가 현재\nTile을 다 읽었는지 동기화로 맞춥니다.'),
 (78, 'next_tile', '이제 A에서는 오른쪽 조각으로, B에서는 아래쪽 조각으로\n이동합니다. 출력 영역은 그대로이고, 합산할 입력 구간만\n바뀝니다.'),
 (84, 'reload', '새 Tile을 Shared Memory에 올리고, 적재\n완료를 맞춥니다. Register에 있던 중간 합은 지우지\n않습니다.'),
 (90, 'add_next', '새 조각에서도 곱셈과 덧셈을 이어갑니다. 첫 출력의 중간\n합 4에 8을 더하면 12가 됩니다.'),
 (96, 'write', '모든 입력 구간의 계산이 끝나면 각 Thread가 최종\n결과를 C의 담당 위치에 씁니다.'),
 (102, 'all_blocks', '다른 출력 영역도 각 Block이 같은 방식으로\n계산합니다. 이 과정을 통해 전체 행렬곱 결과를\n완성합니다.'),
 (108, 'same_math', '수학적 계산은 바뀌지 않았습니다. 여전히 A의 한 행과\nB의 한 열을 곱해서 더합니다.'),
 (114, 'contrast', 'Naive GEMM은 각 Thread가 직접 입력을\n읽습니다. Tiled GEMM은 함께 쓸 데이터를 가져와\nBlock 안에서 재사용합니다.'),
 (120, 'reuse_count', '이 예제의 한 출력 Tile에서는 입력 읽기 요청을 줄일\n수 있습니다. 실제 메모리 이동과 속도 차이는 캐시 등에도\n영향을 받습니다.'),
 (126, 'meaning', '핵심은 단순히 작은 사각형으로 자르는 것이 아닙니다.\n데이터 이동의 단위를 바꾸고, 여러 계산이 재사용하는\n구조입니다.'),
 (132, 'small', '그렇다고 Tile이 작을수록 좋은 것은 아닙니다. 너무\n작으면 함께 재사용할 기회가 충분하지 않을 수 있습니다.'),
 (138, 'large', '너무 크면 Shared Memory 사용량이 늘어납니다.\n설계에 따라 Register 사용량과 Thread 배치에도\n영향을 줍니다.'),
 (144, 'choices', '그래서 Tile 크기, Thread당 출력 수,\nShared Memory와 Register 사용량을 함께\n고민합니다.'),
 (150, 'execution', '이제 Thread와 Block, Warp가 한 계산에\n모입니다. Block 안의 Thread들은 Warp 단위로\n실행됩니다.'),
 (156, 'coalescing', 'Tile을 가져올 때도 Warp의 접근 주소가 중요합니다.\nCoalesced Memory Access를 고려해 읽기\n작업을 나눕니다.'),
 (162, 'together', 'Shared Memory는 함께 쓰는 Tile을,\nRegister는 개인의 중간 합을 맡습니다. 이 구조들이\n함께 데이터 재사용을 만듭니다.'),
 (168, 'ending', 'GPU 최적화에서 중요한 질문은 연산 수뿐만이 아닙니다.\n한 번 가져온 데이터를 얼마나 많이 다시 사용할 수\n있을까요?'),
]
class MatrixCells(VGroup):
    def __init__(self,name,values,size=.5,color=BLUE):
        super().__init__()
        self.cells=VGroup(*[DataCell(v,size,color) for row in values for v in row]).arrange_in_grid(rows=len(values),cols=len(values[0]),buff=.07)
        self.title=txt(name,24,color).next_to(self.cells,UP,buff=.18)
        self.add(self.cells,self.title)
    def at(self,i,j): return self.cells[i*4+j]
    def row(self,i): return VGroup(*[self.at(i,j) for j in range(4)])
    def col(self,j): return VGroup(*[self.at(i,j) for i in range(4)])
    def tile(self): return VGroup(*[self.at(i,j) for i in range(2) for j in range(2)])


class TiledGEMMIntroduction(Scene):
    def construct(self):
        self.stage,self.head,self.note,self.sub=VGroup(),VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('GPU COMPUTATION SERIES',19,MUTED).move_to(UP*6.85),txt('Tiled GEMM',51).move_to(UP*5.65),txt('06  /  한 번 가져와, 함께 다시 쓰기',23,MINT).move_to(UP*4.65))
        self.add(self.chrome)
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub);self.sub=txt(caption,27).move_to(UP*SUB_Y);self.add(self.sub)
            # This visual action corresponds to this exact narration interval.
            self.play(*getattr(self,action)(),run_time=end-start-EPS)
            if abs(self.time-end)>1/30+.001: raise ValueError(f'Timeline drift: {action}')
    def heading(self,text):
        self.remove(self.head);self.head=txt(text,28,MINT).move_to(UP*HEAD_Y);self.add(self.head)
    def annotation(self,text,color=MUTED):
        self.remove(self.note);self.note=txt(text,21,color).move_to(UP*NOTE_Y);self.add(self.note)
    def replace(self,*items):
        # Remove outgoing scene objects explicitly. Reusing a Register object in
        # FadeOut/FadeIn groups can restore old parent groups in Manim cleanup.
        keep=(self.chrome,self.head,self.note,self.sub)
        for obj in list(self.mobjects):
            if not any(obj is fixed for fixed in keep): self.remove(obj)
        self.stage=VGroup(*items)
        return [LaggedStart(*[FadeIn(m) for m in items],lag_ratio=.1)]
    def reveal(self,*items):
        self.stage.add(*items);return [LaggedStart(*[FadeIn(m) for m in items],lag_ratio=.2)]
    def flow(self,start,end,color=BLUE):
        arrow=DataArrow(start,end,color);token=Dot(start,radius=.07,color=color)
        group=VGroup(arrow,token).set_opacity(0)
        def update(m,a):
            m.set_opacity(min(1,a*8,(1-a)*8));token.move_to((1-a)*start+a*end)
        return UpdateFromAlphaFunc(group,update,remover=True,rate_func=linear)

    def overview(self):
        self.a=MatrixCells('A',A,.45,BLUE).move_to([-2,1.9,0]);self.b=MatrixCells('B',B,.45,PINK).move_to([2,1.9,0])
        self.c=MatrixCells('C · Thread 하나가 한 칸',[['–']*4 for _ in range(4)],.48,MINT).move_to([0,-1.4,0])
        return self.a,self.b,self.c
    def recap(self):
        self.heading('Naive GEMM · Thread 하나 → 출력 하나')
        self.annotation('앞에서 사용한 4 × 4 행렬을 그대로 사용')
        return self.replace(*self.overview())
    def repeat(self):
        self.heading('여러 출력이 같은 입력을 다시 요청')
        return [LaggedStart(*[self.flow(self.a.at(0,0).get_bottom(),self.c.at(0,j).get_top()) for j in range(4)],lag_ratio=.3)]
    def intro(self):
        self.heading('Tiling · 작은 조각을 함께 재사용')
        self.annotation('행렬을 나누는 목적: 데이터 재사용')
        return [Circumscribe(self.a.tile(),color=BLUE),Circumscribe(self.b.tile(),color=PINK)]
    def tiles(self):
        self.ra=SurroundingRectangle(self.a.tile(),buff=.04,color=BLUE);self.rb=SurroundingRectangle(self.b.tile(),buff=.04,color=PINK)
        self.stage.add(self.ra,self.rb);self.annotation('입력 Tile: 2 × 2 · 합산 구간을 둘로 나눕니다')
        return [Create(self.ra),Create(self.rb)]
    def block(self):
        self.heading('Block 하나 → C의 2 × 2 출력 영역')
        self.rc=SurroundingRectangle(self.c.tile(),buff=.1,color=GOLD);self.stage.add(self.rc)
        self.annotation('교육용 Block: Thread 4개 · 각각 출력 한 칸')
        return [Create(self.rc),Circumscribe(self.ra,color=BLUE),Circumscribe(self.rb,color=PINK)]
    def diagram(self):
        self.a=MatrixCells('A · Global',A,.42,BLUE).move_to([-2,1.95,0]);self.b=MatrixCells('B · Global',B,.42,PINK).move_to([2,1.95,0])
        self.ra=SurroundingRectangle(self.a.tile(),buff=.04,color=BLUE);self.rb=SurroundingRectangle(self.b.tile(),buff=.04,color=PINK)
        self.box=MemoryBox('Block 0 · C 왼쪽 위 2 × 2 담당',7.4,4.5,MINT).move_to(DOWN*1.65)
        self.sm=MemoryBox('Shared Memory · A Tile / B Tile',6.7,1.65,MINT).move_to(DOWN*.7)
        self.sa=VGroup(*[DataCell('–',.42,BLUE) for _ in range(4)]).arrange_in_grid(rows=2,cols=2,buff=.07).move_to([-1.5,-.85,0])
        self.sb=VGroup(*[DataCell('–',.42,PINK) for _ in range(4)]).arrange_in_grid(rows=2,cols=2,buff=.07).move_to([1.5,-.85,0])
        self.regs=VGroup(*[DataCell(0,.64,GOLD).move_to([x,-2.7,0]) for x in [-2.4,-.8,.8,2.4]])
        self.tags=VGroup(*[txt(f'T{i} → C{r}{c}',18,GOLD).next_to(self.regs[i],UP,buff=.25) for i,(r,c) in enumerate([(0,0),(0,1),(1,0),(1,1)])])
        self.reglabel=txt('Register · 각 Thread의 중간 합',21,GOLD).move_to(DOWN*3.4)
        return self.a,self.b,self.ra,self.rb,self.box,self.sm,self.sa,self.sb,self.regs,self.tags,self.reglabel
    def load(self,phase):
        # Thread q loads one A element and one B element for this 2x2 example.
        return LaggedStart(*[AnimationGroup(self.flow(self.a.at(i,phase*2+j).get_bottom(),self.sa[q].get_top(),BLUE),self.flow(self.b.at(phase*2+i,j).get_bottom(),self.sb[q].get_top(),PINK)) for q,(i,j) in enumerate([(0,0),(0,1),(1,0),(1,1)])],lag_ratio=.25)
    def fill(self,phase):
        return AnimationGroup(*[self.sa[q].change(A[i][phase*2+j],BLUE) for q,(i,j) in enumerate([(0,0),(0,1),(1,0),(1,1)])],*[self.sb[q].change(B[phase*2+i][j],PINK) for q,(i,j) in enumerate([(0,0),(0,1),(1,0),(1,1)])])
    def cooperative(self):
        self.heading('Thread들이 나눠 적재 · Global → Shared')
        self.annotation('T0–T3: A와 B에서 각각 한 원소씩 읽기')
        old=self.replace(*self.diagram())
        return [Succession(AnimationGroup(*old,run_time=1),self.load(0).set_run_time(3),self.fill(0).set_run_time(2))]
    def loaded(self):
        self.heading('한 Block에서 공유하는 두 입력 Tile')
        return [Circumscribe(self.sa,color=BLUE),Circumscribe(self.sb,color=PINK)]
    def ready(self):
        self.heading('동기화 ① · 적재 완료 후 함께 읽기')
        self.annotation('모든 필요한 쓰기가 끝난 다음 공유 데이터 사용')
        return [Succession(Circumscribe(self.sm,color=MINT),Circumscribe(self.tags,color=GOLD))]
    def reuse_a(self):
        self.heading('A의 같은 값 → 같은 출력 행의 Thread')
        self.annotation('Shared의 A₀₀ = 1 → T0와 T1')
        return [Succession(*[self.flow(self.sa[0].get_bottom(),self.regs[q].get_top(),BLUE) for q in [0,1]])]
    def reuse_b(self):
        self.heading('B의 같은 값 → 같은 출력 열의 Thread')
        self.annotation('Shared의 B₀₀ = 2 → T0와 T2')
        return [Succession(*[self.flow(self.sb[0].get_bottom(),self.regs[q].get_top(),PINK) for q in [0,2]])]
    def sums(self,stop):
        return [sum(A[i][k]*B[k][j] for k in range(stop)) for i,j in [(0,0),(0,1),(1,0),(1,1)]]
    def update_sums(self,stop):
        return AnimationGroup(*[r.change(v,GOLD) for r,v in zip(self.regs,self.sums(stop))])
    def multiply(self):
        self.heading('Shared에서 읽기 → 곱하기 → Register에 더하기')
        self.annotation('T0: 1×2 + 2×1 = 4',GOLD)
        return [Succession(AnimationGroup(self.flow(self.sa[0].get_bottom(),self.regs[0].get_top(),BLUE),self.flow(self.sb[0].get_bottom(),self.regs[0].get_top(),PINK),run_time=2),self.update_sums(1).set_run_time(1),self.update_sums(2).set_run_time(1),Circumscribe(self.regs,color=GOLD,run_time=2))]
    def accumulate(self):
        self.heading('첫 입력 구간의 부분 합 · 4, 5, 5, 4')
        self.annotation('출력은 아직 미완성 · 다음 구간에서도 합을 이어갑니다')
        return [LaggedStart(*[Indicate(r,color=GOLD) for r in self.regs],lag_ratio=.2)]
    def before_overwrite(self):
        self.heading('동기화 ② · 모두 읽은 뒤 덮어쓰기')
        self.annotation('Shared Memory를 재사용하기 전, 현재 계산 완료 확인')
        return [Succession(Circumscribe(self.regs,color=GOLD),Circumscribe(self.sm,color=MINT))]
    def next_tile(self):
        self.heading('A는 오른쪽 · B는 아래쪽 · C 영역은 그대로')
        self.annotation('합산 구간: k = 0,1 → k = 2,3')
        a=VGroup(*[self.a.at(i,j) for i in range(2) for j in range(2,4)])
        b=VGroup(*[self.b.at(i,j) for i in range(2,4) for j in range(2)])
        return [Transform(self.ra,SurroundingRectangle(a,buff=.04,color=BLUE)),Transform(self.rb,SurroundingRectangle(b,buff=.04,color=PINK))]
    def reload(self):
        self.heading('새 조각 적재 · Register의 합은 유지')
        self.annotation('적재 → 준비 완료 동기화 → 다음 계산')
        return [Succession(self.load(1).set_run_time(2),self.fill(1).set_run_time(1),Circumscribe(self.sm,color=MINT,run_time=3))]
    def add_next(self):
        self.heading('부분 합에 다음 입력 구간을 더하기')
        self.annotation('T0: 4 + 3×0 + 4×2 = 12',GOLD)
        return [Succession(self.update_sums(3).set_run_time(1),self.update_sums(4).set_run_time(1),Circumscribe(self.regs,color=GOLD,run_time=4))]
    def write(self):
        self.heading('최종 합 → C의 담당 위치에 저장')
        self.annotation('Register 값 12, 8, 11, 4를 출력 Tile에 쓰기')
        self.result=MatrixCells('C · Global',[['–']*4 for _ in range(4)],.57,MINT).move_to(UP*.5)
        values=self.sums(4)
        old=self.replace(self.result,self.regs,self.tags,self.reglabel)
        return [Succession(AnimationGroup(*old,run_time=1),LaggedStart(*[Succession(self.flow(self.regs[q].get_top(),self.result.at(i,j).get_bottom(),GOLD),self.result.at(i,j).change(values[q],MINT)) for q,(i,j) in enumerate([(0,0),(0,1),(1,0),(1,1)])],lag_ratio=.3,run_time=5))]
    def all_blocks(self):
        self.stage.remove(self.regs,self.tags,self.reglabel);self.remove(self.regs,self.tags,self.reglabel)
        self.heading('다른 Block도 다른 출력 Tile을 계산')
        self.annotation('Block별 출력 영역은 다릅니다 · 전체 C 완성')
        return [LaggedStart(*[cell.change(C[q//4][q%4],MINT) for q,cell in enumerate(self.result.cells)],lag_ratio=.1)]
    def same_math(self):
        self.heading('수학은 그대로 · C = A × B')
        self.annotation('첫 출력: 1×2 + 2×1 + 3×0 + 4×2 = 12')
        return [Circumscribe(self.result.row(0),color=MINT),Indicate(self.result.at(0,0),color=GOLD)]
    def contrast(self):
        self.heading('달라진 것은 데이터를 가져오는 방식')
        self.naive=MemoryBox('Naive · 각 Thread가 입력을 직접 읽기',7,1.7,BLUE).move_to(UP*1.5)
        self.tiled=MemoryBox('Tiled · 함께 적재하고 Block 안에서 재사용',7,1.7,MINT).move_to(DOWN*1)
        self.annotation('같은 수학적 연산 · 다른 공유 재사용 구조')
        return self.replace(self.naive,self.tiled)
    def reuse_count(self):
        self.heading('예: 출력 2 × 2 · 합산 길이 4')
        self.annotation('논리적 입력 원소 읽기 수 · DRAM 트랜잭션/속도 비율 아님')
        n=txt('Naive: 4 outputs × 4 × 2 = 32',23,BLUE).move_to(UP*1.1)
        t=txt('Tiled: 2 stages × (4 + 4) = 16',23,MINT).move_to(DOWN*1.4)
        return self.reveal(n,t)
    def meaning(self):
        self.heading('적재 단위 + 함께 재사용하는 계산')
        self.annotation('사각형 자체가 아니라 데이터 재사용이 핵심')
        return [Succession(Circumscribe(self.naive,color=BLUE),Circumscribe(self.tiled,color=MINT))]
    def small(self):
        self.heading('작은 Tile · 재사용 기회가 적을 수 있음')
        self.tiny=VGroup(*[DataCell('·',.48,MINT) for _ in range(4)]).arrange_in_grid(rows=2,cols=2,buff=.08).move_to(UP*.4)
        self.caption=txt('작은 조각 · 적은 공유 범위',28,MINT).move_to(DOWN*1.6)
        self.annotation('Tile 크기에도 균형이 필요합니다')
        return self.replace(self.tiny,self.caption)
    def large(self):
        self.heading('큰 Tile · 더 많은 자원이 필요할 수 있음')
        big=VGroup(*[DataCell('·',.48,PINK) for _ in range(36)]).arrange_in_grid(rows=6,cols=6,buff=.08).move_to(UP*.5)
        self.annotation('Shared 용량 ↑ · Register/Thread 구성은 설계에 따라 변화')
        label=txt('더 큰 공유 범위 · 더 큰 저장 공간',26,PINK).move_to(DOWN*2)
        return self.replace(big,label)
    def choices(self):
        self.heading('크기 · Thread당 출력 · 자원 사용량')
        self.cards=VGroup(*[MemoryBox(t,6.7,1.2,c) for t,c in [('Tile 크기',BLUE),('Thread당 출력 수',GOLD),('Shared Memory + Register',MINT)]]).arrange(DOWN,buff=.45)
        self.annotation('한 가지 설정만으로 최적화를 결정하지 않습니다')
        return self.replace(self.cards)
    def execution(self):
        self.heading('Thread → Warp → Block')
        self.lanes=VGroup(*[Rectangle(width=.15,height=.4,color=GOLD,fill_color=GOLD,fill_opacity=.3) for _ in range(32)]).arrange(RIGHT,buff=.035).move_to(UP*.2)
        self.warp=SurroundingRectangle(self.lanes,buff=.2,color=GOLD)
        self.execblock=MemoryBox('Block · Warp를 포함',7.4,4.1,MINT).move_to(DOWN*.1)
        self.warplabel=txt('1 Warp = 32 Threads',28,MINT).move_to(UP*1.05)
        self.annotation('실제 실행 구조 · 앞의 Thread 4개는 축소 계산 예제')
        return self.replace(self.execblock,self.lanes,self.warp,self.warplabel)
    def coalescing(self):
        self.heading('Tile 적재도 Warp의 주소 패턴을 고려')
        self.addresses=VGroup(*[Rectangle(width=.15,height=.3,color=BLUE) for _ in range(32)]).arrange(RIGHT,buff=.035).move_to(DOWN*1.8)
        self.annotation('인접 Thread → 인접 주소가 되도록 적재 작업 배치')
        self.stage.add(self.addresses)
        return [FadeIn(self.addresses),LaggedStart(*[self.flow(t.get_bottom(),c.get_top()) for t,c in zip(self.lanes,self.addresses)],lag_ratio=.06)]
    def together(self):
        self.heading('Shared는 공동 입력 · Register는 개인 합')
        self.annotation('적재 → 동기화 → 계산 → 동기화 → 다음 조각')
        cards=VGroup(MemoryBox('Shared Memory · 함께 쓸 Tile',7,1.7,MINT),MemoryBox('Register · 각 Thread의 누적 합',7,1.7,GOLD)).arrange(DOWN,buff=1)
        return self.replace(cards)
    def ending(self):
        self.heading('한 번 가져온 데이터 · 얼마나 다시 쓸까?')
        self.annotation('Tiling의 핵심: 데이터 이동을 줄이는 재사용',MINT)
        return [Succession(*[Circumscribe(m,color=MINT) for m in self.stage])]
