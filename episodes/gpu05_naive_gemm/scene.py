"""GPU 05: naive C=AB and redundant logical loads, 174 seconds."""
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
# Fixed screen transitions, exact subtitle/narration, corresponding visual method.
CAPTIONS=[
 (0,'recap','앞에서는 Global Memory, Shared Memory, Register가\n서로 다른 역할을 가진다고 했습니다.'),
 (6,'matrices','이번에는 실제 계산으로 보겠습니다.\n두 행렬 A와 B를 곱해 행렬 C를 만드는 행렬곱입니다.'),
 (12,'row_column','C의 한 원소를 계산하려면\nA의 한 행과 B의 한 열이 필요합니다.'),
 (18,'first_output','첫 번째 출력은 A의 첫 행과 B의 첫 열에서\n같은 위치의 값들을 곱해서 더합니다.'),
 (24,'dot_product','즉, 출력 원소 하나는\n여러 번의 곱셈과 덧셈으로 만들어집니다.'),
 (30,'thread_intro','GPU에서는 이 작업을 여러 Thread에 나눌 수 있습니다.\n단순하게 Thread 하나가 출력 원소 하나를 맡습니다.'),
 (36,'mapping','Thread 0은 첫 번째 출력, Thread 1은 그 옆의 출력.\n각 Thread가 자신이 맡은 결과 하나를 계산합니다.'),
 (42,'read_pair','각 Thread는 자신에게 필요한\nA의 행과 B의 열을 따라 값을 하나씩 읽습니다.'),
 (48,'accumulator','읽은 두 값을 곱하고, 결과를 계속 더합니다.\n이 중간 합은 Register에 둘 수 있습니다.'),
 (54,'first_terms','첫 두 곱셈의 결과는 각각 2입니다.\nRegister의 중간 합은 0에서 2, 다시 4가 됩니다.'),
 (60,'last_terms','나머지 곱셈의 결과 0과 8도 더합니다.\n모든 항을 더한 최종 값은 12입니다.'),
 (66,'write_result','계산이 끝나면 Register의 최종 결과를\n자신이 담당한 C의 위치에 씁니다.'),
 (72,'independent','각 Thread가 출력 하나를 독립적으로 계산합니다.\n구조는 단순하고 자연스럽습니다.'),
 (78,'neighbor','하지만 옆의 Thread를 보겠습니다.\n다른 출력을 계산하려고 이 Thread도 A와 B를 읽습니다.'),
 (84,'repeat_a','같은 출력 행을 맡은 Thread들은\n같은 A의 값을 반복해서 읽습니다.'),
 (90,'repeat_b','같은 출력 열을 맡은 Thread들은\n같은 B의 값도 다시 읽습니다.'),
 (96,'growth','행렬이 커지면 한 입력값을 사용하는 출력도 많아집니다.\n여러 Thread의 반복 읽기도 늘어납니다.'),
 (102,'necessary_work','곱셈과 덧셈 자체는 필요한 연산입니다.\n하지만 같은 입력값을 여러 Thread가 다시 요청하고 있습니다.'),
 (108,'logical_loads','즉, 연산 수뿐 아니라 같은 데이터를 몇 번 읽는지도 중요합니다.\n실제 메모리 이동 비용은 캐시 등에도 영향을 받습니다.'),
 (114,'reuse_a','A의 한 값을 여러 출력에 쓴다면,\n한 번 가져와 여러 Thread가 재사용할 수 있으면 좋겠습니다.'),
 (120,'reuse_b','B의 원소도 마찬가지입니다.\n여러 출력이 필요로 하는 값을 함께 재사용할 수 있습니다.'),
 (126,'naive','지금의 단순한 Kernel은 각 Thread가\n필요한 값을 Global Memory에서 직접 읽습니다.\n이것이 Naive GEMM입니다.'),
 (132,'correct','수학적으로는 올바른 행렬곱입니다.\n하지만 빠른 메모리와 명시적인 공유 재사용은 충분히 활용하지 못합니다.'),
 (138,'shared','여기서 Shared Memory가 다시 등장합니다.\n같은 Block의 Thread들이 쓸 데이터를 함께 준비하는 공간입니다.'),
 (144,'tile','행렬 전체 대신 필요한 작은 영역만 가져오면 어떨까요?\nA와 B에서 작은 조각, Tile을 선택합니다.'),
 (150,'stage_tile','선택한 조각들을 Shared Memory에 가져옵니다.\n데이터 준비가 끝났는지 필요한 동기화도 맞춥니다.'),
 (156,'reuse_tile','이제 같은 Block의 Thread들이 조각 안의 값을 함께 재사용합니다.\nGlobal Memory에서 반복해서 읽는 일을 줄일 수 있습니다.'),
 (162,'tiling','작은 조각을 가져와 여러 계산에 사용하는 방식.\n이것이 다음 단계인 Tiling의 출발점입니다.'),
 (168,'ending','같은 계산이라도 데이터를 몇 번 읽고 얼마나 재사용하느냐에 따라,\nGPU의 실행 비용은 달라질 수 있습니다.'),
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

class NaiveGEMMIntroduction(Scene):
    def construct(self):
        self.stage,self.head,self.note,self.sub=VGroup(),VGroup(),VGroup(),VGroup()
        self.add(txt('GPU COMPUTATION SERIES',19,MUTED).move_to(UP*6.85),txt('Naive GEMM',51).move_to(UP*5.65),txt('05  /  같은 값을 몇 번 다시 읽을까',23,MINT).move_to(UP*4.65))
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub);self.sub=txt(caption,27).move_to(UP*SUB_Y);self.add(self.sub)
            # This action and its exact narration share the same screen interval.
            self.play(*getattr(self,action)(),run_time=end-start-EPS)
            if abs(self.time-end)>1/30+.001: raise ValueError(f'Timeline drift: {action}')
    def heading(self,text):
        self.remove(self.head);self.head=txt(text,28,MINT).move_to(UP*HEAD_Y);self.add(self.head)
    def annotation(self,text,color=MUTED):
        self.remove(self.note);self.note=txt(text,21,color).move_to(UP*NOTE_Y);self.add(self.note)
    def replace(self,*items):
        old=self.stage;self.stage=VGroup(*items)
        return [Succession(FadeOut(old,run_time=.15),FadeIn(self.stage,run_time=.85))]
    def reveal(self,*items):
        self.stage.add(*items);return [LaggedStart(*[FadeIn(m) for m in items],lag_ratio=.2)]
    def flow(self,start,end,color=BLUE):
        arrow=DataArrow(start,end,color);token=Dot(start,radius=.07,color=color)
        group=VGroup(arrow,token).set_opacity(0)
        def update(m,a):
            m.set_opacity(min(1,a*8,(1-a)*8));token.move_to((1-a)*start+a*end)
        return UpdateFromAlphaFunc(group,update,remover=True,rate_func=linear)
    def matrix_set(self):
        self.a=MatrixCells('A',A).move_to([-2.1,1.7,0]);self.b=MatrixCells('B',B).move_to([2.1,1.7,0])
        self.c=MatrixCells('C',[['·']*4 for _ in range(4)],.5,MINT).move_to([0,-1.35,0])
        return self.a,self.b,self.c
    def recap(self):
        self.heading('데이터의 위치와 재사용')
        cards=VGroup(*[MemoryBox(t,6,1.2,c) for t,c in [('Global Memory',BLUE),('Shared Memory',MINT),('Register',GOLD)]]).arrange(DOWN,buff=.55)
        self.annotation('이전 편의 메모리 구조를 실제 계산에 적용')
        return self.replace(cards)
    def matrices(self):
        self.heading('C = A × B')
        self.annotation('설명을 위한 4 × 4 예제')
        return self.replace(*self.matrix_set())
    def row_column(self):
        self.annotation('C의 한 칸 ← A의 한 행 · B의 한 열')
        return [Circumscribe(self.a.row(0),color=GOLD),Circumscribe(self.b.col(0),color=PINK),Indicate(self.c.at(0,0),color=MINT)]
    def first_output(self):
        self.heading('첫 행 × 첫 열 → 첫 번째 출력')
        return [Succession(*[AnimationGroup(Indicate(self.a.at(0,k),color=GOLD),Indicate(self.b.at(k,0),color=PINK)) for k in range(4)])]
    def dot_product(self):
        self.formula=txt('1×2 + 2×1 + 3×0 + 4×2 = 12',27,GOLD).move_to(DOWN*3.3)
        self.annotation('같은 위치끼리 곱한 뒤, 모든 항을 더합니다')
        return self.reveal(self.formula)
    def thread_intro(self):
        self.heading('Thread 하나 → 출력 원소 하나')
        self.annotation('교육용 단순 매핑 · 실제 고성능 구현은 다를 수 있음')
        return [LaggedStart(*[cell.change(f'T{i}',GOLD) for i,cell in enumerate(self.c.cells)],lag_ratio=.07)]
    def mapping(self):
        return [Succession(*[Indicate(self.c.at(0,j),color=GOLD) for j in range(4)])]
    def read_pair(self):
        self.heading('T0 · A의 행과 B의 열을 읽기')
        self.annotation('A와 B는 Global Memory에 저장된 입력')
        return [Succession(*[AnimationGroup(self.flow(self.a.at(0,k).get_bottom(),self.c.at(0,0).get_left(),BLUE),self.flow(self.b.at(k,0).get_bottom(),self.c.at(0,0).get_right(),PINK)) for k in range(4)])]
    def accumulator(self):
        self.heading('T0 · Register에 중간 합 누적')
        self.stage.remove(self.formula);self.remove(self.formula)
        self.acc=DataCell(0,.7,GOLD).move_to([-1.55,-3.4,0]);self.acc_title=txt('T0 Register · 합',20,GOLD).next_to(self.acc,LEFT,buff=.25)
        self.operation=txt('합 = 0',25,GOLD).move_to([1.35,-3.4,0])
        self.annotation('읽기 → 곱하기 → 중간 합에 더하기')
        return self.reveal(self.acc,self.acc_title,self.operation)
    def term(self,k,total):
        new=txt(f'+ {A[0][k]} × {B[k][0]}  →  {total}',25,GOLD).move_to(self.operation)
        return Succession(AnimationGroup(Indicate(self.a.at(0,k),color=GOLD),Indicate(self.b.at(k,0),color=PINK),Transform(self.operation,new),run_time=1),self.acc.change(total,GOLD).set_run_time(.4),Indicate(self.acc,color=GOLD,run_time=1.6))
    def first_terms(self): return [Succession(self.term(0,2),self.term(1,4))]
    def last_terms(self): return [Succession(self.term(2,4),self.term(3,12))]
    def write_result(self):
        self.heading('Register → C에 최종 결과 쓰기')
        self.annotation('C도 Global Memory의 출력 배열')
        return [Succession(self.flow(self.acc.get_top(),self.c.at(0,0).get_bottom(),GOLD),self.c.at(0,0).change(12,MINT))]
    def independent(self):
        self.heading('각 Thread는 자신의 출력 하나를 완성')
        self.annotation('다른 출력도 같은 곱셈·덧셈 규칙 적용')
        return [LaggedStart(*[cell.change(C[i//4][i%4],MINT) for i,cell in enumerate(self.c.cells)],lag_ratio=.09)]
    def neighbor(self):
        self.heading('이웃한 출력에서 다시 필요한 입력')
        self.annotation('첫 행의 옆 출력도 A의 첫 행을 사용')
        return [Circumscribe(self.a.row(0),color=GOLD),Circumscribe(self.b.col(1),color=PINK),Indicate(self.c.at(0,1),color=GOLD)]
    def reuse_board(self):
        self.sa=DataCell(1,.8,BLUE).move_to([-2,2.05,0]);self.sb=DataCell(2,.8,PINK).move_to([2,2.05,0])
        self.la=txt('A₀₀ = 1',24,BLUE).next_to(self.sa,UP,buff=.2);self.lb=txt('B₀₀ = 2',24,PINK).next_to(self.sb,UP,buff=.2)
        self.out=MatrixCells('C · 각 칸을 맡은 Thread',[[f'T{i*4+j}' for j in range(4)] for i in range(4)],.62,GOLD).move_to([0,-1.55,0])
        # Keep the output title out of data-transfer routes.
        self.out.title.scale(.8).next_to(self.out.cells,DOWN,buff=.2)
        return self.sa,self.sb,self.la,self.lb,self.out
    def repeat_a(self):
        self.heading('같은 A 원소 → 여러 출력 열에서 사용')
        self.annotation('첫 행: T0 · T1 · T2 · T3이 A₀₀을 읽음',BLUE)
        anim=self.replace(*self.reuse_board())
        return [Succession(AnimationGroup(*anim,run_time=1),LaggedStart(*[self.flow(self.sa.get_bottom(),self.out.at(0,j).get_top(),BLUE) for j in range(4)],lag_ratio=.3,run_time=5))]
    def repeat_b(self):
        self.heading('같은 B 원소 → 여러 출력 행에서 사용')
        self.annotation('첫 열: T0 · T4 · T8 · T12가 B₀₀을 읽음',PINK)
        return [LaggedStart(*[self.flow(self.sb.get_bottom(),self.out.at(i,0).get_left(),PINK) for i in range(4)],lag_ratio=.3)]
    def growth(self):
        self.heading('더 큰 행렬 → 더 많은 출력이 입력을 공유')
        self.annotation('한 입력값의 재사용 기회도 함께 커집니다')
        tiles=VGroup(*[Rectangle(width=.3,height=.3,color=GOLD,fill_color=GOLD,fill_opacity=.15) for _ in range(64)]).arrange_in_grid(rows=8,cols=8,buff=.09).move_to(DOWN*.5)
        title=txt('출력이 늘어나도 · 같은 입력을 여러 번 사용',25).move_to(UP*2.4)
        return self.replace(tiles,title)
    def necessary_work(self):
        self.heading('필요한 계산과 반복 읽기를 구분')
        self.annotation('연산을 없애는 것이 아니라 입력의 재사용을 늘리기')
        self.work=MemoryBox('곱셈 + 덧셈 · 필요한 계산',6.8,1.6,GOLD).move_to(UP*1.6)
        self.reads=MemoryBox('같은 입력 · 여러 Thread의 읽기 요청',6.8,1.6,BLUE).move_to(DOWN*1)
        return self.replace(self.work,self.reads)
    def logical_loads(self):
        self.annotation('화살표 수 ≠ 실제 DRAM 접근 횟수 · 캐시 효과는 별도')
        return [Succession(Circumscribe(self.work,color=GOLD),Circumscribe(self.reads,color=BLUE))]
    def reuse_a(self):
        self.heading('A의 값도 한 번 가져와 함께 쓰면?')
        self.annotation('첫 행의 여러 출력에 같은 A 원소 재사용')
        anim=self.replace(*self.reuse_board())
        return [Succession(AnimationGroup(*anim,run_time=1),AnimationGroup(Circumscribe(self.sa,color=BLUE),Circumscribe(self.out.row(0),color=BLUE),run_time=5))]
    def reuse_b(self):
        self.heading('B의 값도 여러 출력이 함께 사용')
        self.annotation('첫 열의 여러 출력에 같은 B 원소 재사용')
        return [Circumscribe(self.sb,color=PINK),Circumscribe(self.out.col(0),color=PINK)]
    def naive(self):
        self.heading('Naive GEMM · 단순한 행렬곱 Kernel')
        self.annotation('이 영상은 C = A × B 형태를 사용')
        return [Succession(self.flow(self.sa.get_bottom(),self.out.at(0,0).get_top()),self.flow(self.sa.get_bottom(),self.out.at(0,1).get_top()),self.flow(self.sb.get_bottom(),self.out.at(1,0).get_left(),PINK))]
    def correct(self):
        self.heading('올바른 결과 ≠ 충분한 공유 재사용')
        self.annotation('수학은 맞습니다 · 데이터 이동에 개선 여지가 있습니다')
        return [LaggedStart(*[cell.change(C[i//4][i%4],MINT) for i,cell in enumerate(self.out.cells)],lag_ratio=.08)]
    def shared(self):
        self.heading('같은 Block에서 함께 준비하는 데이터')
        self.annotation('Global Memory → Shared Memory → 함께 계산')
        self.ta=MatrixCells('A · Global',A,.42,BLUE).move_to([-2,2.15,0]);self.tb=MatrixCells('B · Global',B,.42,PINK).move_to([2,2.15,0])
        self.block=MemoryBox('Block · 출력 Tile을 함께 계산',7.3,4.3,MINT).move_to(DOWN*1.8)
        self.sm=MemoryBox('Shared Memory',6.4,1.4,MINT).move_to(DOWN*.95)
        self.jobs=VGroup(*[DataCell(f'T{i}',.65,GOLD) for i in range(4)]).arrange(RIGHT,buff=.6).move_to(DOWN*2.85)
        return self.replace(self.ta,self.tb,self.block,self.sm,self.jobs)
    def tile(self):
        self.heading('행렬의 작은 조각 · Tile')
        self.annotation('예: A와 B에서 각각 2 × 2 조각 선택')
        self.ra=SurroundingRectangle(self.ta.tile(),color=BLUE,buff=.04);self.rb=SurroundingRectangle(self.tb.tile(),color=PINK,buff=.04)
        self.stage.add(self.ra,self.rb)
        return [Create(self.ra),Create(self.rb)]
    def stage_tile(self):
        self.heading('조각 적재 → 필요한 동기화')
        self.annotation('준비 완료를 맞춘 다음 공유 데이터를 사용')
        self.copy_a=self.ta.tile().copy().move_to([-1.4,-1.1,0]);self.copy_b=self.tb.tile().copy().move_to([1.4,-1.1,0])
        self.stage.add(self.copy_a,self.copy_b)
        return [Succession(AnimationGroup(TransformFromCopy(self.ta.tile(),self.copy_a),TransformFromCopy(self.tb.tile(),self.copy_b),run_time=3),Circumscribe(self.sm,color=MINT,run_time=3))]
    def reuse_tile(self):
        self.heading('가져온 조각 → Block 안에서 여러 번 사용')
        self.annotation('작은 출력 Tile의 부분 합을 함께 계산')
        return [LaggedStart(*[AnimationGroup(self.flow(self.copy_a.get_bottom(),job.get_top(),BLUE),self.flow(self.copy_b.get_bottom(),job.get_top(),PINK)) for job in self.jobs],lag_ratio=.3)]
    def tiling(self):
        self.heading('Tiling · 작은 조각을 반복해서 재사용')
        self.annotation('이 조각은 부분 합 · 나머지 조각도 이어서 처리')
        return [Succession(Circumscribe(self.copy_a,color=BLUE),Circumscribe(self.copy_b,color=PINK),Circumscribe(self.jobs,color=GOLD))]
    def ending(self):
        self.heading('같은 계산 · 다른 데이터 재사용')
        self.annotation('몇 번 읽는가 + 얼마나 다시 쓰는가',MINT)
        return [Succession(*[self.flow(self.sm.get_bottom(),job.get_top(),MINT) for job in self.jobs])]
