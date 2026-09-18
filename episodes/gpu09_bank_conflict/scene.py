"""GPU 09: shared memory banks, padding and broadcast, 174 seconds."""
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
# Exact captions and fixed screen transition times.
CAPTIONS = [
 (0, 'recap', 'Shared Memory는 같은 Block의\nThread들이 데이터를 재사용하는 공간입니다. 하지만\n사용한다고 언제나 빠른 것은 아닙니다.'),
 (6, 'structure', 'Shared Memory 안에서도 어떤 위치를 함께\n읽느냐가 중요합니다. 내부 저장 공간은 여러 Bank로\n나뉩니다.'),
 (12, 'banks32', 'NVIDIA GPU의 일반적인 구조에서는 Bank가\n32개입니다. 여러 통로로 나눠 요청을 처리하는 모습으로\n생각해봅시다.'),
 (18, 'warp32', 'Warp도 Thread 32개입니다. 여기서는 각\nThread가 4바이트 원소 하나를 읽는 경우를\n보겠습니다.'),
 (24, 'contiguous', 'Thread 0은 0번 원소, Thread 1은 1번,\nThread 2는 2번 원소를 읽습니다. 연속된 원소에\n접근합니다.'),
 (30, 'spread', '이 조건에서는 요청이 서로 다른 Bank로 나뉩니다. 여러\n요청을 함께 처리하기 좋은 패턴입니다.'),
 (36, 'stride', '이번에는 간격을 32개 원소로 바꿉니다. Thread들이\n0번, 32번, 64번, 96번 원소를 읽습니다.'),
 (42, 'mapping', '주소는 서로 다르지만, Bank 번호는 모두 같습니다. 이\n예제에서는 Bank 0으로 몰립니다.'),
 (48, 'conflict', 'Warp의 여러 Thread가 같은 Bank의 서로 다른\n주소를 함께 요청합니다. 이런 상황을 Bank\nConflict라고 합니다.'),
 (54, 'serialized', '같은 Bank가 요청들을 한 번에 처리하지 못하면, 요청을\n나눠 처리해야 합니다. 접근이 여러 단계로 나뉘는\n것입니다.'),
 (60, 'same_work', '같은 Shared Memory, 같은 Thread 수,\n같은 데이터 양입니다. 그래도 Bank 매핑에 따라 처리\n비용이 달라질 수 있습니다.'),
 (66, 'look_bank', '따라서 주소가 다른지만 볼 것이 아니라, 그 주소가 어느\nBank에 연결되는지를 함께 봐야 합니다.'),
 (72, 'matrix', 'Shared Memory를 행마다 32개의 원소가 있는\n배열로 사용해봅시다. 화면에는 일부 행과 열만 펼쳐\n보겠습니다.'),
 (78, 'row', '같은 행의 옆 원소들을 읽으면, Bank 번호도 차례로\n달라집니다. Warp의 요청이 여러 Bank로 분산됩니다.'),
 (84, 'column', '반대로 같은 열을 읽으면 원소 번호가 32씩 증가합니다.\n서로 다른 주소가 다시 같은 Bank에 몰립니다.'),
 (90, 'transpose', '그래서 행렬 전치처럼 읽는 방향이 바뀌는 계산에서는,\nShared Memory 접근에도 Bank\nConflict가 생길 수 있습니다.'),
 (96, 'padding', '해결 방법 하나는 Padding입니다. 32×32 대신\n32×33으로 저장 공간을 만들고, 각 행 끝에 한 칸을\n더 둡니다.'),
 (102, 'shift', '계산할 값은 그대로지만 다음 행의 시작 위치가 달라집니다.\n첫 열의 원소 번호가 0, 33, 66, 99가 됩니다.'),
 (108, 'scatter', '이제 첫 열의 Bank 번호도 0, 1, 2, 3으로\n달라집니다. 이 패턴에서는 Warp 전체가 서로 다른\nBank를 사용합니다.'),
 (114, 'unchanged', 'Padding은 필요한 계산 값을 바꾸지 않습니다. 저장\n간격을 바꿔 Bank 매핑을 바꾸는 것입니다.'),
 (120, 'broadcast', '한 가지 예외도 있습니다. 여러 Thread가 정확히 같은\n주소를 읽는 경우입니다.'),
 (126, 'same_address', '이때는 하나의 값을 여러 Thread에 전달하는\nBroadcast가 가능합니다. 서로 다른 주소가 충돌하는\n경우와 구분해야 합니다.'),
 (132, 'distinguish', '핵심은 같은 Bank의 서로 다른 주소입니다. 같은\nBank를 본다는 이유만으로 모든 읽기를\nConflict라고 부르지는 않습니다.'),
 (138, 'global_memory', '앞에서 Coalesced Memory Access는\nGlobal Memory의 요청을 어떻게 묶는지에 관한\n이야기였습니다.'),
 (144, 'shared', 'Bank Conflict는 Shared Memory 안의\n문제입니다. Warp의 서로 다른 주소 요청이 Bank에\n어떻게 분산되는지를 봅니다.'),
 (150, 'compare', 'Global Memory에서는 메모리 트랜잭션을,\nShared Memory에서는 Bank 매핑을 봅니다.\n분석하는 대상이 다릅니다.'),
 (156, 'design', '즉, 빠른 저장 공간을 고르는 것만으로는 충분하지\n않습니다. Warp가 어떤 주소를 함께 읽고 쓰는지도\n설계해야 합니다.'),
 (162, 'scope', '오늘의 Padding 효과는 이 자료형과 접근 패턴의\n예입니다. 자료형과 명령, 배치가 바뀌면 Bank 매핑도\n다시 확인해야 합니다.'),
 (168, 'ending', '데이터를 어디에 둘지, 그리고 Thread들이 어떤\n패턴으로 접근할지. GPU 최적화에서는 두 가지를 함께\n봐야 합니다.'),
]

def banks_for_stride(stride): return [(lane*stride)%32 for lane in range(32)]

class BankArray(VGroup):
    def __init__(self):
        super().__init__()
        self.banks=VGroup(*[DataCell(i,.56,MINT) for i in range(32)]).arrange_in_grid(rows=4,cols=8,buff=.12)
        self.title=txt('Shared Memory · Bank 0–31',24,MINT).next_to(self.banks,UP,buff=.25)
        self.add(self.banks,self.title)

class AccessTable(VGroup):
    """Four representative lanes; bottom strip accounts for all 32 banks."""
    def __init__(self,stride=1,same=False):
        super().__init__();self.words=[0 if same else i*stride for i in range(4)]
        self.threads,self.addresses,self.ids=VGroup(),VGroup(),VGroup()
        for i,word in enumerate(self.words):
            y=2.25-i*.78
            self.threads.add(txt(f'T{i}',24,GOLD).move_to([-2.7,y,0]))
            self.addresses.add(DataCell(word,.56,BLUE).move_to([-.1,y,0]))
            self.ids.add(txt(f'Bank {word%32}',23,MINT if stride==1 else PINK).move_to([2.2,y,0]))
        headings=VGroup(*[txt(t,18,MUTED).move_to([x,3,0]) for t,x in [('Thread',-2.7),('원소 번호',-.1),('Bank 번호',2.2)]])
        self.add(headings,self.threads,self.addresses,self.ids)

class BankConflictIntroduction(Scene):
    def construct(self):
        self.stage,self.head,self.note,self.sub=VGroup(),VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('GPU COMPUTATION SERIES',19,MUTED).move_to(UP*6.85),txt('Shared Memory Banks',42).move_to(UP*5.65),txt('09  /  같은 Bank로 몰린다면?',23,MINT).move_to(UP*4.65))
        self.add(self.chrome)
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub);self.sub=txt(caption,27).move_to(UP*SUB_Y);self.add(self.sub)
            # Caption and its corresponding visual action share this interval.
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
        self.stage.add(*items);return [Succession(LaggedStart(*[FadeIn(m) for m in items],lag_ratio=.2,run_time=.7),Succession(*[Circumscribe(m,color=MINT,run_time=5.3/max(len(items),1)) for m in items]))]
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
        self.heading('Shared Memory도 접근 패턴이 중요')
        return self.replace(self.card('같은 Block의 Thread들','가져온 데이터를 함께 재사용',1.5,MINT),self.card('이번 질문','Shared 안에서 어디를 읽을까?',-1,GOLD))
    def structure(self):
        self.heading('Shared Memory · 여러 Bank로 분할')
        self.array=BankArray().move_to(UP*.4)
        self.annotation('Bank는 저장 공간을 나눠 요청을 처리하는 구조')
        return self.replace(self.array)
    def banks32(self):
        self.heading('32 Banks')
        self.annotation('4-byte 원소 · 연속 32-bit word가 연속 Bank에 매핑')
        return [LaggedStart(*[Indicate(b,color=GOLD) for b in self.array.banks],lag_ratio=.045)]
    def warp32(self):
        self.heading('1 Warp = 32 Threads · 원소당 4 bytes')
        self.lanes=VGroup(*[txt(f'T{i}',17,GOLD) for i in range(32)]).arrange_in_grid(rows=4,cols=8,buff=.28).move_to(UP*1.6)
        self.array=BankArray().scale(.8).move_to(DOWN*1.75)
        self.annotation('시작 원소는 Bank 0 · 번호는 byte 주소가 아닌 원소 번호')
        return self.replace(self.lanes,self.array)
    def table(self,stride):
        self.table_view=AccessTable(stride)
        self.array=BankArray().scale(.83).move_to(DOWN*2.05)
        return self.table_view,self.array
    def contiguous(self):
        self.heading('연속 접근 · Tᵢ → 원소 i')
        self.annotation('대표 T0–T3 확대 · 같은 규칙을 Warp 32개 Thread에 적용')
        return self.replace(*self.table(1))
    def spread(self):
        self.heading('원소 0–31 → Bank 0–31')
        self.annotation('32개 서로 다른 Bank로 분산')
        return [LaggedStart(*[Indicate(self.array.banks[b],color=GOLD) for b in banks_for_stride(1)],lag_ratio=.045)]
    def stride(self):
        self.heading('간격 32 · Tᵢ → 원소 32i')
        self.annotation('4-byte 원소 32개 간격 = 128 bytes 간격')
        return self.replace(*self.table(32))
    def mapping(self):
        self.heading('Bank 번호 = 원소 번호 mod 32')
        self.annotation('0, 32, 64, 96, …, 992 → 모두 Bank 0')
        return [Succession(*[Indicate(m,color=PINK) for m in self.table_view.ids]),Circumscribe(self.array.banks[0],color=PINK)]
    def conflict(self):
        self.heading('Bank Conflict · 같은 Bank의 서로 다른 주소')
        self.requests=VGroup(*[DataCell(v,.65,BLUE) for v in [0,32,64,96]]).arrange(RIGHT,buff=.8).move_to(UP*1.8)
        labels=VGroup(*[txt(f'T{i}',22,GOLD).next_to(c,UP,buff=.2) for i,c in enumerate(self.requests)])
        self.bank=MemoryBox('Bank 0',5.8,1.5,PINK).move_to(DOWN*.3)
        self.annotation('네 요청만 확대 · 전체 Warp는 32개 서로 다른 원소 요청')
        anim=self.replace(self.requests,labels,self.bank)
        return [Succession(AnimationGroup(*anim,run_time=1),LaggedStart(*[self.flow(c.get_bottom(),self.bank.get_top(),PINK) for c in self.requests],lag_ratio=.15,run_time=5))]
    def serialized(self):
        self.heading('한 Bank의 서로 다른 원소 → 분할 처리')
        self.steps=VGroup(*[Rectangle(width=.44,height=.22,color=PINK,fill_color=PINK,fill_opacity=.3) for _ in range(32)]).arrange_in_grid(rows=4,cols=8,buff=.12).move_to(DOWN*2.25)
        self.annotation('이 scalar 읽기는 32-way conflict · cycle/영상 속도 비율 아님')
        self.stage.add(self.steps)
        return [LaggedStart(*[FadeIn(s) for s in self.steps],lag_ratio=.05)]
    def same_work(self):
        self.heading('같은 양의 데이터 · 다른 Bank 분포')
        self.annotation('두 경우 모두 32 Threads × 4 bytes = 128 bytes 읽기')
        return self.replace(self.card('연속 접근','32개의 Bank',1.5,MINT),self.card('간격 32 접근','1개의 Bank · 32개 서로 다른 원소',-1,PINK))
    def look_bank(self):
        self.heading('주소와 Bank 번호를 함께 보기')
        self.annotation('4-byte 원소 · Bank = 원소 번호를 32로 나눈 나머지')
        return [Succession(*[Circumscribe(m,color=GOLD) for m in self.stage])]
    def matrix_board(self):
        self.values=[[3,7,2,9],[1,5,6,4],[8,2,0,3],[4,9,1,5]]
        self.cells=VGroup(*[VGroup(*[DataCell(v,.57,BLUE).move_to([-2.65+j*.8,1.8-i*1.2,0]) for j,v in enumerate(row)]) for i,row in enumerate(self.values)])
        self.dots=VGroup(*[txt('…',25,MUTED).move_to([.55,1.8-i*1.2,0]) for i in range(4)])
        self.offsets=VGroup(*[txt(f'시작 {i*32}\nBank 0',18,PINK).move_to([2.6,1.8-i*1.2,0]) for i in range(4)])
        self.pad=VGroup(*[DataCell('PAD',.57,GOLD).move_to([1.35,1.8-i*1.2,0]) for i in range(4)])
        self.mt=txt('32 × 32 · 행 우선 저장',25,MINT).move_to(UP*2.9)
        return self.cells,self.dots,self.offsets,self.mt
    def matrix(self):
        self.heading('한 행 = 32개의 4-byte 원소')
        self.annotation('앞 4행·각 행 앞 4개 값만 표시 · …는 나머지 28열')
        return self.replace(*self.matrix_board())
    def row(self):
        self.heading('행 방향 · 옆 원소는 다른 Bank')
        self.annotation('첫 행: 원소 0, 1, 2, 3, …, 31 → Bank 0–31')
        return [Succession(*[Indicate(c,color=GOLD) for c in self.cells[0]])]
    def column(self):
        self.heading('열 방향 · 간격 32 → 같은 Bank')
        self.annotation('첫 열: 원소 0, 32, 64, 96, …, 992 → Bank 0')
        return [Succession(*[AnimationGroup(Indicate(r[0],color=PINK),Indicate(o,color=PINK)) for r,o in zip(self.cells,self.offsets)])]
    def transpose(self):
        self.heading('행렬 전치 · 행과 열 접근의 차이')
        self.annotation('Shared를 사용해도 열 접근에 conflict가 남을 수 있습니다')
        return [Succession(Circumscribe(self.cells[0],color=BLUE),Circumscribe(VGroup(*[r[0] for r in self.cells]),color=PINK))]
    def padding(self):
        self.heading('Padding · 각 행 끝에 한 칸 추가')
        self.annotation('32 × 32 → 32 × 33 · Bank 수는 여전히 32개')
        self.remove(self.mt);self.stage.remove(self.mt)
        self.mt=txt('32 × 33 · 마지막 열은 Padding',25,MINT).move_to(UP*2.9)
        self.stage.add(self.mt,self.pad);self.add(self.mt)
        targets=[txt(f'시작 {i*33}\nBank {i}',18,[MINT,BLUE,GOLD,PINK][i]).move_to(o) for i,o in enumerate(self.offsets)]
        return [Succession(LaggedStart(*[FadeIn(c) for c in self.pad],lag_ratio=.2,run_time=2),AnimationGroup(*[Transform(o,t) for o,t in zip(self.offsets,targets)],run_time=1),Circumscribe(self.pad,color=GOLD,run_time=3))]
    def shift(self):
        self.heading('데이터 값은 그대로 · 행 간격 32 → 33')
        self.annotation('주소는 바뀌지만 왼쪽의 계산 데이터는 그대로입니다')
        targets=[txt(f'시작 {i*33}\nBank {i}',18,[MINT,BLUE,GOLD,PINK][i]).move_to(o) for i,o in enumerate(self.offsets)]
        return [Succession(AnimationGroup(*[Transform(o,t) for o,t in zip(self.offsets,targets)],run_time=1),LaggedStart(*[Indicate(r[0],color=[MINT,BLUE,GOLD,PINK][i]) for i,r in enumerate(self.cells)],lag_ratio=.2,run_time=5))]
    def scatter(self):
        self.heading('33i mod 32 = i · 32개 Bank로 분산')
        self.array=BankArray().move_to(UP*.4)
        self.annotation('첫 열: 0, 33, 66, …, 1023 → Bank 0, 1, 2, …, 31')
        anim=self.replace(self.array)
        return [Succession(AnimationGroup(*anim,run_time=1),LaggedStart(*[Indicate(self.array.banks[b],color=GOLD) for b in banks_for_stride(33)],lag_ratio=.045,run_time=5))]
    def unchanged(self):
        self.heading('Padding으로 배치와 Bank 매핑 변경')
        self.annotation('값은 유지 · 행 간격만 변경 · 추가 저장 공간은 필요')
        return [Circumscribe(self.array,color=MINT)]
    def broadcast(self):
        self.heading('예외 · 정확히 같은 주소를 읽는다면?')
        self.one=DataCell(7,.85,BLUE).move_to(UP*1.75)
        self.one_label=txt('Shared의 원소 0 · 값 7',25,BLUE).next_to(self.one,UP,buff=.3)
        self.receivers=VGroup(*[txt(f'T{i}',27,GOLD) for i in range(4)]).arrange(RIGHT,buff=1.05).move_to(DOWN*1.2)
        self.annotation('같은 주소에 대한 읽기 · 대표 Thread 네 개만 확대')
        return self.replace(self.one,self.one_label,self.receivers)
    def same_address(self):
        self.heading('Broadcast · 같은 값을 여러 Thread에 전달')
        self.annotation('동일 주소 읽기는 서로 다른 주소의 Bank Conflict와 다름')
        return [LaggedStart(*[self.flow(self.one.get_bottom(),t.get_top(),BLUE) for t in self.receivers],lag_ratio=.15)]
    def distinguish(self):
        self.heading('같은 Bank ≠ 항상 Conflict')
        self.annotation('Broadcast 설명은 읽기 기준 · 같은 주소에 쓰는 것과 구분')
        return self.replace(self.card('서로 다른 원소: 0, 32, 64, …','같은 Bank → Conflict',1.5,PINK),self.card('정확히 같은 원소: 0, 0, 0, …','같은 값 읽기 → Broadcast',-1,MINT))
    def global_memory(self):
        self.heading('Global Memory · 요청 주소와 트랜잭션')
        self.annotation('이전 편: Warp 요청이 얼마나 효율적으로 묶이는가')
        self.gc=self.card('Coalesced Memory Access','Global Memory 요청의 묶음',1.5,BLUE)
        return self.replace(self.gc)
    def shared(self):
        self.heading('Shared Memory · 서로 다른 주소의 Bank 분포')
        self.sc=self.card('Bank Conflict','Shared Memory 요청의 Bank 매핑',-1,MINT)
        self.annotation('이번 편: Warp 요청이 같은 Bank에 몰리는가')
        return self.reveal(self.sc)
    def compare(self):
        self.heading('접근 패턴은 비슷한 질문 · 분석 대상은 다름')
        self.annotation('Global: 트랜잭션 / Shared: Bank와 주소')
        return [Succession(Circumscribe(self.gc,color=BLUE),Circumscribe(self.sc,color=MINT))]
    def design(self):
        self.heading('저장 위치 + Warp의 접근 패턴')
        self.annotation('어디에 둘지와 어떻게 접근할지를 함께 설계')
        return [Succession(*[Circumscribe(m,color=GOLD) for m in self.stage])]
    def scope(self):
        self.heading('자료형 · 명령 · 배치가 바뀌면 다시 확인')
        self.annotation('이번 예: 4-byte scalar 읽기 · 32 Banks · 시작 Bank 0')
        return self.replace(self.card('32 × 33 Padding','오늘의 열 접근 패턴에서 Conflict 제거',1.5,MINT),self.card('다른 경우','Bank 매핑과 실제 성능을 다시 확인',-1,GOLD))
    def ending(self):
        self.heading('빠른 메모리도 · 접근 패턴까지 설계')
        self.annotation('Shared Memory의 성능도 Warp 전체의 요청에서 시작')
        return [Succession(*[Circumscribe(m,color=MINT) for m in self.stage])]
