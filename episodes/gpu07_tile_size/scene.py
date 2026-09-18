"""GPU 07: tile size, resource budgets and hierarchical mapping, 174 seconds."""
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
# Screen time is authoritative; subtitles and narration share these exact words.
CAPTIONS = [
 (0, 'recap', '앞에서는 Tile을 Shared Memory에 올리고,\n여러 Thread가 함께 재사용하는 Tiled GEMM을\n봤습니다.'),
 (6, 'question', '그렇다면 Tile은 얼마나 커야 할까요? 예제의\n16×16이나 32×32가 특별한 정답일까요?'),
 (12, 'balance', '그렇지는 않습니다. Tile 크기는 데이터 재사용과 GPU\n자원 사용 사이의 균형으로 결정됩니다.'),
 (18, 'tile16', '먼저 Thread 하나가 출력 하나를 맡는 단순한\n구조입니다. 16×16 출력 Tile은 Thread\n256개가 됩니다.'),
 (24, 'warps16', 'NVIDIA GPU에서 Warp 하나는 Thread\n32개입니다. 따라서 Thread 256개는 Warp\n8개로 나뉩니다.'),
 (30, 'tile32', '같은 방식으로 32×32 출력 Tile을 맡기면,\nThread는 1024개가 필요합니다.'),
 (36, 'warps32', '이것은 Warp 32개입니다. Tile의 가로와 세로를 두\n배로 키우면 출력과 Thread 수는 네 배가 됩니다.'),
 (42, 'limit', '1024개는 현재 NVIDIA GPU의 Block당 최대\nThread 수이기도 합니다. 다른 자원 제한도 만족해야\n합니다.'),
 (48, 'reuse16', '큰 Tile의 장점은 재사용입니다. 16×16 예제에서\nA의 한 값은 같은 출력 행의 계산 16곳에 쓰입니다.'),
 (54, 'reuse32', '32×32라면 같은 A의 값을 출력 32곳에 쓸 수\n있습니다. B의 값도 같은 출력 열에서 재사용됩니다.'),
 (60, 'reuse_math', '한 번 가져온 데이터로 더 많은 곱셈과 덧셈을 합니다.\n하지만 재사용만 보고 크기를 계속 늘릴 수는 없습니다.'),
 (66, 'shared16', 'A와 B를 각각 정사각 Tile로 한 번씩 저장한다고\n합시다. 같은 자료형에서 Shared Memory 사용량을\n비교하겠습니다.'),
 (72, 'shared32', '16×16에서 32×32로 바꾸면, 두 입력 Tile의\n원소 수와 저장 용량은 네 배가 됩니다.'),
 (78, 'register', '한 Thread가 여러 출력을 맡는 설계라면, 출력마다\n중간 합이 필요합니다. Register 사용량도 늘어날 수\n있습니다.'),
 (84, 'sm', 'SM은 Block들이 올라가 실행되는 GPU의 계산\n장치입니다. Shared Memory와 Register\n자원은 한정되어 있습니다.'),
 (90, 'resident', 'Block의 자원 사용량이 커지면, 한 SM에 동시에\n유지할 수 있는 Block이나 Warp 수가 줄어들 수\n있습니다.'),
 (96, 'small', '작은 Tile은 자원 부담이 적을 수 있습니다. 더 많은\n작업을 유지하기 쉽지만, 데이터 재사용 기회는 줄 수\n있습니다.'),
 (102, 'large', '큰 Tile은 재사용에 유리할 수 있지만 자원 부담이\n커집니다. 어느 쪽이 빠른지는 이것만으로 정할 수\n없습니다.'),
 (108, 'summary', '동시에 유지하는 작업이 많다고 항상 빠른 것도 아닙니다.\n재사용과 자원 사용을 함께 봐야 합니다.'),
 (114, 'numbers', '그래서 16과 32는 마법의 숫자가 아닙니다. Warp\n크기와 작업 배치, 자원 제한을 고려할 때 등장하는\n선택지입니다.'),
 (120, 'hierarchy', '실제 고성능 GEMM에서는 Tile이 한 종류만 있는 것도\n아닙니다. 여러 단계의 Tile을 함께 사용합니다.'),
 (126, 'block128', '전체 행렬에서 Block이 맡는 출력 영역을 Block\nTile이라고 합니다. 예를 들어 128×128 영역을\n맡을 수 있습니다.'),
 (132, 'warp_tiles', '그 안을 다시 Warp들이 나눠 맡습니다. 이 예에서는\nBlock Tile을 더 작은 Warp Tile 여덟 개로\n나눴습니다.'),
 (138, 'thread_tiles', '각 Warp 안에서도 Thread마다 여러 출력값을 맡길\n수 있습니다. 한 Thread가 담당하는 작은 영역이\nThread Tile입니다.'),
 (144, 'not_threads', '따라서 128×128 Block Tile이 Thread\n16384개를 뜻하지는 않습니다. 출력 영역과 Thread\n수를 구분해야 합니다.'),
 (150, 'design', 'Tile 크기를 정할 때는 재사용, Shared\nMemory, Thread와 Warp 배치,\nRegister 사용량을 함께 결정합니다.'),
 (156, 'hardware', '좋은 선택은 행렬의 크기와 자료형, GPU 자원에 따라\n달라집니다. 다른 계산에서는 다른 Tile이 유리할 수\n있습니다.'),
 (162, 'measure', '후보를 비교할 때는 실제 실행 시간도 측정해야 합니다.\n재사용이나 자원 수치 하나만으로 성능을 단정할 수\n없습니다.'),
 (168, 'ending', '좋은 Tile 크기는 언제나 하나로 정해져 있지 않습니다.\n계산과 하드웨어 자원 사이에서 좋은 균형을 만드는\n크기입니다.'),
]

class TileGrid(VGroup):
    """Grid lines represent individual outputs without thousands of cell objects."""
    def __init__(self,rows,cols,width=5.6,color=MINT):
        super().__init__();self.rows,self.cols=rows,cols
        h=width*rows/cols
        self.border=Rectangle(width=width,height=h,color=color,stroke_width=2)
        self.lines=VGroup(*[Line([-width/2+i*width/cols,-h/2,0],[-width/2+i*width/cols,h/2,0],color=color,stroke_width=.6) for i in range(1,cols)],*[Line([-width/2,-h/2+i*h/rows,0],[width/2,-h/2+i*h/rows,0],color=color,stroke_width=.6) for i in range(1,rows)])
        self.add(self.border,self.lines)
    def region(self,row,col,rows=1,cols=1,color=GOLD):
        w,h=self.border.width,self.border.height
        return Rectangle(width=w*cols/self.cols,height=h*rows/self.rows,color=color,stroke_width=2,fill_color=color,fill_opacity=.15).move_to(self.border.get_corner(UL)+RIGHT*w*(col+cols/2)/self.cols+DOWN*h*(row+rows/2)/self.rows)

class TileSizeIntroduction(Scene):
    def construct(self):
        self.stage,self.head,self.note,self.sub=VGroup(),VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('GPU COMPUTATION SERIES',19,MUTED).move_to(UP*6.85),txt('Choosing a Tile',47).move_to(UP*5.65),txt('07  /  왜 16 × 16, 32 × 32일까?',23,MINT).move_to(UP*4.65))
        self.add(self.chrome)
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub);self.sub=txt(caption,27).move_to(UP*SUB_Y);self.add(self.sub)
            # Narration and meaningful visual change occupy this same interval.
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
        return [Succession(LaggedStart(*[FadeIn(m) for m in items],lag_ratio=.1,run_time=.7),Succession(*[Circumscribe(m,color=MINT,run_time=5.3/max(len(items),1)) for m in items]))]
    def reveal(self,*items):
        self.stage.add(*items);return [LaggedStart(*[FadeIn(m) for m in items],lag_ratio=.2)]
    def flow(self,start,end,color=BLUE):
        arrow=DataArrow(start,end,color);token=Dot(start,radius=.07,color=color)
        group=VGroup(arrow,token).set_opacity(0)
        def update(m,a):
            m.set_opacity(min(1,a*8,(1-a)*8));token.move_to((1-a)*start+a*end)
        return UpdateFromAlphaFunc(group,update,remover=True,rate_func=linear)


    def card(self,title,body,y,color):
        box=MemoryBox(title,7,1.65,color).move_to(UP*y)
        value=txt(body,27,color).move_to(UP*(y-.2))
        return VGroup(box,value)
    def recap(self):
        self.heading('가져오기 → 함께 재사용')
        a=self.card('Global Memory','A Tile + B Tile',1.7,BLUE)
        b=self.card('Shared Memory','Block의 Thread들이 재사용',-1.1,MINT)
        self.annotation('Tiled GEMM · 지난 편의 핵심')
        return self.replace(a,b)
    def question(self):
        self.heading('Tile 크기에 정답이 있을까?')
        self.left=TileGrid(16,16,2.8,BLUE).move_to([-1.85,.5,0]);self.right=TileGrid(32,32,2.8,MINT).move_to([1.85,.5,0])
        labels=VGroup(txt('16 × 16',32,BLUE).move_to([-1.85,-1.6,0]),txt('32 × 32',32,MINT).move_to([1.85,-1.6,0]))
        self.annotation('어느 크기도 모든 계산의 정답은 아닙니다')
        return self.replace(self.left,self.right,labels)
    def balance(self):
        self.heading('재사용 ↔ 자원 사용')
        self.annotation('더 많이 다시 쓰기 · 제한된 자원 안에서 실행하기')
        self.reuse=self.card('데이터 재사용','가져온 값으로 얼마나 계산할까?',1.6,BLUE)
        self.cost=self.card('자원 사용','Shared · Register · Thread',-1,MINT)
        return self.replace(self.reuse,self.cost)
    def tile16(self):
        self.heading('16 × 16 = 256 Threads')
        self.grid=TileGrid(16,16,4.3,BLUE).move_to(UP*.35)
        self.formula=txt('출력 한 칸 ↔ Thread 하나',28,GOLD).move_to(DOWN*2.5)
        self.annotation('단순 매핑을 가정 · Block 하나가 출력 Tile 하나 담당')
        return self.replace(self.grid,self.formula)
    def warps16(self):
        self.heading('256 ÷ 32 = 8 Warps')
        self.bands=VGroup(*[self.grid.region(r*2,0,2,16,GOLD) for r in range(8)])
        self.annotation('색 띠 하나 = 연속 32개 Thread = Warp 하나')
        self.stage.add(self.bands)
        return [LaggedStart(*[FadeIn(b) for b in self.bands],lag_ratio=.18)]
    def tile32(self):
        self.heading('32 × 32 = 1024 Threads')
        self.grid=TileGrid(32,32,4.3,MINT).move_to(UP*.35)
        self.formula=txt('같은 조건: 출력 한 칸 ↔ Thread 하나',25,GOLD).move_to(DOWN*2.5)
        self.annotation('Tile 면적이 네 배 → 이 단순 매핑의 Thread 수도 네 배')
        return self.replace(self.grid,self.formula)
    def warps32(self):
        self.heading('1024 ÷ 32 = 32 Warps')
        self.bands=VGroup(*[self.grid.region(r,0,1,32,GOLD) for r in range(32)])
        self.annotation('행 하나 = 32개 Thread = Warp 하나')
        self.stage.add(self.bands)
        return [LaggedStart(*[FadeIn(b) for b in self.bands],lag_ratio=.04)]
    def limit(self):
        self.heading('1024 Threads · Block당 상한')
        self.annotation('상한에 맞는다고 빠르거나 항상 실행 가능한 것은 아닙니다')
        return [Circumscribe(self.grid,color=PINK),Indicate(self.formula,color=PINK)]
    def reuse_board(self,n):
        self.outputs=TileGrid(n,n,4.5,MINT).move_to(DOWN*.8)
        self.source=DataCell('A 값',.8,BLUE).move_to(UP*2.3)
        self.row=self.outputs.region(0,0,1,n,BLUE)
        self.stage.add(self.row)
        return self.source,self.outputs,self.row
    def reuse16(self):
        self.heading('16 × 16 · A 한 값 → 출력 16곳')
        self.annotation('한 합산 단계에서 같은 출력 행에 재사용')
        anim=self.replace(*self.reuse_board(16))
        return [Succession(AnimationGroup(*anim,run_time=1),self.flow(self.source.get_bottom(),self.row.get_top()).set_run_time(2),Circumscribe(self.row,color=BLUE,run_time=3))]
    def reuse32(self):
        self.heading('32 × 32 · A 한 값 → 출력 32곳')
        self.annotation('B도 같은 출력 열의 32곳에 재사용')
        anim=self.replace(*self.reuse_board(32))
        return [Succession(AnimationGroup(*anim,run_time=1),Circumscribe(self.row,color=BLUE,run_time=2),Circumscribe(self.outputs.region(0,0,32,1,PINK),color=PINK,run_time=3))]
    def reuse_math(self):
        self.heading('재사용 기회 ↑ · 자원도 함께 확인')
        self.annotation('재사용 횟수가 곧 실행 속도의 배수는 아닙니다')
        return [Succession(Indicate(self.source,color=BLUE),Circumscribe(self.outputs,color=GOLD))]
    def shared16(self):
        self.heading('A와 B 각각 T × T · 단일 버퍼')
        self.mem16=self.card('T = 16 · 4 byte 원소','2 × 16² × 4 B = 2 KiB',1.5,BLUE)
        self.mem32=self.card('비교 조건','같은 자료형 · A/B 두 Tile',-1,MUTED)
        self.annotation('합산 Tile 길이도 T · 패딩/추가 버퍼는 제외')
        return self.replace(self.mem16,self.mem32)
    def shared32(self):
        self.heading('가로 2배 × 세로 2배 → 용량 4배')
        new=self.card('T = 32 · 4 byte 원소','2 × 32² × 4 B = 8 KiB',-1,PINK)
        anim=self.replace(self.mem16,new)
        return [Succession(AnimationGroup(*anim,run_time=1),Circumscribe(new,color=PINK,run_time=5))]
    def register(self):
        self.heading('Thread당 출력 여러 개 → 여러 중간 합')
        self.single=VGroup(DataCell('합',.7,GOLD)).move_to([-2,0,0])
        self.multi=VGroup(*[DataCell('합',.7,GOLD) for _ in range(4)]).arrange_in_grid(rows=2,cols=2,buff=.14).move_to([1.8,0,0])
        labels=VGroup(txt('출력 1개',26,GOLD).move_to([-2,1.5,0]),txt('출력 4개',26,GOLD).move_to([1.8,1.5,0]))
        self.annotation('중간 합 외에도 피연산자·주소 등에 Register가 필요')
        return self.replace(self.single,self.multi,labels)
    def sm(self):
        self.heading('SM · Block들이 올라가는 계산 장치')
        self.sm_box=MemoryBox('SM · 제한된 Shared / Register 자원',7.2,5,MINT).move_to(DOWN*.3)
        self.blocks=VGroup(*[MemoryBox(f'Block {i}',2.7,1.5,BLUE) for i in range(4)]).arrange_in_grid(rows=2,cols=2,buff=.3).move_to(DOWN*.45)
        self.annotation('개념도 · 실제 하드웨어 수용량 수치를 나타내지 않습니다')
        return self.replace(self.sm_box,self.blocks)
    def resident(self):
        self.heading('Block당 자원 ↑ → 상주 작업 수가 줄 수도')
        self.annotation('Shared · Register · Thread/Block 상한이 함께 제한')
        big=VGroup(*[MemoryBox(f'Block {i} · 큰 자원 할당',5.7,1.5,PINK) for i in range(2)]).arrange(DOWN,buff=.3).move_to(DOWN*.45)
        return self.replace(self.sm_box,big)
    def small(self):
        self.heading('작은 Tile의 선택')
        self.smallcard=self.card('자원 부담 ↓ 가능','더 많은 작업을 유지할 여지',1.5,BLUE)
        downside=self.card('재사용 기회 ↓ 가능','입력을 더 자주 가져올 수 있음',-1,GOLD)
        self.annotation('낮은 자원 사용만으로 속도가 결정되지는 않습니다')
        return self.replace(self.smallcard,downside)
    def large(self):
        self.heading('큰 Tile의 선택')
        a=self.card('재사용 기회 ↑ 가능','가져온 값으로 더 많은 계산',1.5,MINT)
        b=self.card('자원 부담 ↑ 가능','동시에 유지할 작업 수에 제약',-1,PINK)
        self.annotation('큰 Tile이 항상 빠른 것은 아닙니다')
        return self.replace(a,b)
    def summary(self):
        self.heading('상주 작업 수만으로도 판단할 수 없습니다')
        self.annotation('재사용 · 자원 사용 · 실제 실행 시간을 함께 보기')
        return [Succession(*[Circumscribe(item,color=GOLD) for item in self.stage])]
    def numbers(self):
        self.heading('16 · 32는 후보 크기')
        cards=VGroup(*[self.card(t,b,y,c) for t,b,y,c in [('16 × 16','단순 매핑: 256 Threads / 8 Warps',1.5,BLUE),('32 × 32','단순 매핑: 1024 Threads / 32 Warps',-1,MINT)]])
        self.annotation('Warp 크기 · 매핑 · 자료형 · 자원 한계가 선택에 영향')
        return self.replace(cards)
    def hierarchy(self):
        self.heading('Matrix → Block Tile → Warp Tile → Thread Tile')
        self.levels=VGroup(*[MemoryBox(t,6.3,1,c) for t,c in [('Matrix',BLUE),('Block Tile',MINT),('Warp Tile',GOLD),('Thread Tile',PINK)]]).arrange(DOWN,buff=.25)
        self.annotation('고성능 GEMM의 한 계층적 구성 · 구현마다 매핑은 다름')
        return self.replace(self.levels)
    def block128(self):
        self.heading('Block Tile · 출력 128 × 128')
        self.blockgrid=TileGrid(4,2,5.4,MINT).stretch_to_fit_height(5.4).move_to(DOWN*.15)
        # Macro grid: four rows by two columns of future warp tiles, not elements.
        self.label=txt('출력 영역: 16,384개 원소',26,MINT).move_to(DOWN*3.4)
        self.annotation('내부 선은 다음 단계의 Warp 분할 경계')
        return self.replace(self.blockgrid,self.label)
    def warp_tiles(self):
        self.heading('예: 8 Warp Tiles · 각각 32 × 64 출력')
        self.warp_regions=VGroup(*[self.blockgrid.region(i,j,1,1,GOLD) for i in range(4) for j in range(2)])
        labels=VGroup(*[txt(f'Warp {k}',21,GOLD).move_to(r) for k,r in enumerate(self.warp_regions)])
        self.annotation('8 Warps × 32 Threads = 256 Threads · 예시 구성')
        self.stage.add(self.warp_regions,labels)
        return [LaggedStart(*[FadeIn(r) for r in self.warp_regions],lag_ratio=.12),FadeIn(labels)]
    def thread_tiles(self):
        self.heading('Warp Tile 안의 Thread Tile · 확대')
        self.threadgrid=TileGrid(4,8,6,GOLD).move_to(UP*.25)
        self.threadregion=self.threadgrid.region(0,0,1,1,PINK)
        self.detail=txt('32 × 64 출력 / 32 Threads\n예: Thread마다 8 × 8 = 64개 출력',26,PINK).move_to(DOWN*2.5)
        self.annotation('소유 출력 영역의 개념도 · 실제 Register 배치는 구현에 따름')
        return self.replace(self.threadgrid,self.threadregion,self.detail)
    def not_threads(self):
        self.heading('출력 원소 수 ≠ Thread 수')
        a=self.card('Block Tile: 128 × 128','출력 16,384개',1.5,MINT)
        b=self.card('예시: 256 Threads × 출력 64개','같은 출력 영역을 나눠 계산',-1,GOLD)
        self.annotation('큰 출력 Tile도 Thread당 여러 결과로 분담 가능')
        return self.replace(a,b)
    def design(self):
        self.heading('Tile 크기와 작업 배치를 함께 설계')
        self.designs=VGroup(*[MemoryBox(t,6.8,1.1,c) for t,c in [('데이터 재사용',BLUE),('Shared Memory',MINT),('Thread · Warp 배치',GOLD),('Register',PINK)]]).arrange(DOWN,buff=.2)
        self.annotation('선택들이 서로 연결되어 있습니다')
        return self.replace(self.designs)
    def hardware(self):
        self.heading('문제와 하드웨어가 바뀌면 선택도 변화')
        a=self.card('계산 조건','행렬 크기 · 모양 · 자료형',1.5,BLUE)
        b=self.card('GPU 조건','자원 용량 · 지원 연산 · 제한',-1,MINT)
        self.annotation('행렬 경계 처리와 GPU 전체 활용도도 고려')
        return self.replace(a,b)
    def measure(self):
        self.heading('후보 구현 → 실행 시간 측정 → 비교')
        a=self.card('후보 A / 후보 B','같은 입력과 조건에서 실행',1.5,GOLD)
        b=self.card('실행 시간으로 확인','예측만으로 우열을 단정하지 않기',-1,MINT)
        self.annotation('이 영상의 도형과 숫자는 성능 벤치마크가 아닙니다')
        return self.replace(a,b)
    def ending(self):
        self.heading('좋은 Tile = 계산과 자원의 좋은 균형')
        self.annotation('재사용을 늘리고 · 자원 한계를 고려하고 · 측정하기',MINT)
        return [Succession(*[Circumscribe(m,color=MINT) for m in self.stage])]
