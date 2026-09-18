"""GPU 08: register pressure, occupancy and latency hiding, 174 seconds."""
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
# One visual action per exact subtitle/narration interval.
CAPTIONS = [
 (0, 'recap', '앞에서는 Tile과 Thread당 출력이 커지면\nRegister 사용량도 늘어날 수 있다고 했습니다.\n이번에는 그 영향을 보겠습니다.'),
 (6, 'register', 'Register는 각 Thread가 계산에 필요한 값을\n보관하는 가까운 저장 공간입니다.'),
 (12, 'one_output', 'Thread 하나가 출력 하나를 계산한다면, 그 중간 합을\nRegister에 둘 수 있습니다.'),
 (18, 'many_outputs', '여러 출력을 동시에 계산하면, 여러 중간 합을 보관해야 할\n수 있습니다. 필요한 Register도 늘어날 수\n있습니다.'),
 (24, 'pressure', '이처럼 한 Thread가 많은 Register를 필요로\n하는 상황을 Register Pressure가 높다고\n표현합니다.'),
 (30, 'sm', '하지만 Register는 무한하지 않습니다. Block들이\n실행되는 SM 안에는 Register의 총량이 정해져\n있습니다.'),
 (36, 'budget', '여기서는 최대 Warp 64개와 Register\n65536개를 가진 SM을 가정하겠습니다. Block당\nThread는 256개입니다.'),
 (42, 'sixteen', 'Thread마다 Register 16개를 쓰면, 이 단순\n모델에서는 Warp 64개를 유지할 수 있습니다.'),
 (48, 'sixtyfour', 'Thread마다 64개를 쓰면 같은 작업 수에 네 배의\nRegister가 필요합니다. Register 용량이 먼저\n한계에 닿습니다.'),
 (54, 'resident', '이 조건에서는 상주 Block이 여덟 개에서 네 개로,\nWarp는 64개에서 32개로 줄어듭니다.'),
 (60, 'occupancy', 'Occupancy는 SM의 최대 상주 Warp 수에 대한\n현재 상주 Warp 수의 비율입니다. 모두가 같은 순간\n명령을 실행한다는 뜻은 아닙니다.'),
 (66, 'half', '최대 Warp 64개 중 32개가 올라가 있다면\nOccupancy는 50퍼센트입니다.'),
 (72, 'full', '64개가 모두 올라가 있다면 100퍼센트입니다. 최대\nWarp 수는 GPU 종류에 따라 달라집니다.'),
 (78, 'question', '그렇다면 Occupancy가 높으면 항상 빠를까요?\n그렇지는 않습니다. 먼저 왜 중요한지 보겠습니다.'),
 (84, 'waiting', '어떤 Warp가 Global Memory의 데이터를\n기다리고 있습니다. 이 Warp는 아직 다음 계산을 진행할\n수 없습니다.'),
 (90, 'ready', '그동안 다른 준비된 Warp의 명령을 실행할 수 있다면,\n계산 장치를 계속 사용할 수 있습니다.'),
 (96, 'hiding', '이렇게 준비된 Warp들의 명령을 번갈아 실행해 대기\n시간을 숨기는 것을 Latency Hiding이라고\n합니다.'),
 (102, 'few', '상주 Warp가 너무 적으면, 기다리는 작업을 대신할\n준비된 Warp가 부족해질 수 있습니다.'),
 (108, 'not_max', '하지만 Occupancy 100퍼센트가 최고 성능을\n보장하지는 않습니다. Thread 안의 계산 효율도\n중요합니다.'),
 (114, 'more_work', 'Register를 더 써서 필요한 값을 유지하면, 메모리\n접근을 줄이거나 여러 계산을 효율적으로 이어갈 수\n있습니다.'),
 (120, 'benefit', '이런 이득이 크다면 Occupancy가 조금 낮아져도 전체\n실행 시간은 더 짧아질 수 있습니다.'),
 (126, 'cap', '반대로 Occupancy를 높이려고 Register를\n지나치게 제한하면, 필요한 값을 모두 보관하지 못할 수도\n있습니다.'),
 (132, 'spill', '일부 값이 메모리로 밀려나 저장되는 것을 Register\nSpill이라고 합니다. 보통 Local Memory를\n사용합니다.'),
 (138, 'reload', '밀려난 값이 다시 필요하면 메모리에서 읽어야 합니다. 이런\n추가 읽기와 쓰기가 실행 비용을 늘릴 수 있습니다.'),
 (144, 'balance', '따라서 Register를 적게 쓰는 것도, 많이 쓰는 것도\n무조건 좋지는 않습니다. 재사용과 상주 작업 사이의 균형이\n필요합니다.'),
 (150, 'tile', 'Tile 설계에서 Thread당 출력을 늘리면 중간 합도\n늘어납니다. Register Pressure와\nOccupancy가 함께 달라질 수 있습니다.'),
 (156, 'chain', 'Tile 크기, Thread당 계산량, Register\n사용량, Occupancy는 서로 연결된 선택입니다.'),
 (162, 'measure', '목표는 Occupancy 숫자의 최대화가 아닙니다. 충분한\nRegister와 준비된 Warp를 확보하고 실제 실행\n시간을 확인해야 합니다.'),
 (168, 'ending', '한 Thread에 얼마나 많은 일을 맡길지, 대신 얼마나\n많은 Warp를 함께 유지할지. GPU 성능은 이 균형에\n달려 있습니다.'),
]

class WarpSlots(VGroup):
    """64 residency slots, not execution units or a scheduling simulation."""
    def __init__(self,active=32):
        super().__init__()
        self.slots=VGroup(*[Rectangle(width=.57,height=.32,color=MINT if i<active else MUTED,stroke_width=1,fill_color=MINT,fill_opacity=.65 if i<active else .02) for i in range(64)]).arrange_in_grid(rows=8,cols=8,buff=.11)
        self.add(self.slots)

class RegisterOccupancyIntroduction(Scene):
    def construct(self):
        self.stage,self.head,self.note,self.sub=VGroup(),VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('GPU COMPUTATION SERIES',19,MUTED).move_to(UP*6.85),txt('Registers & Occupancy',39).move_to(UP*5.65),txt('08  /  한 Thread에 얼마나 맡길까?',23,MINT).move_to(UP*4.65))
        self.add(self.chrome)
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub);self.sub=txt(caption,27).move_to(UP*SUB_Y);self.add(self.sub)
            # Meaningful animation and the corresponding caption share this interval.
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
        self.heading('Thread당 출력 ↑ → 중간 합도 증가 가능')
        a=self.card('Thread당 작은 출력','적은 중간 합',1.5,BLUE)
        b=self.card('Thread당 큰 출력','더 많은 중간 합',-1,GOLD)
        self.annotation('앞선 Tile 크기 선택에서 이어지는 질문')
        return self.replace(a,b)
    def register_board(self,n=1):
        self.thread=txt('Thread 0',32,GOLD).move_to(UP*2)
        self.regbox=MemoryBox('Register · Thread 자신의 계산 값',6.6,2.5,GOLD).move_to(DOWN*.1)
        self.sums=VGroup(*[DataCell(0,.68,GOLD) for _ in range(n)]).arrange(RIGHT,buff=.35).move_to(DOWN*.3)
        return self.thread,self.regbox,self.sums
    def register(self):
        self.heading('Register · 계산 가까이의 저장 공간')
        self.annotation('각 Thread의 중간값 · 실제 배치는 컴파일러가 결정')
        return self.replace(*self.register_board())
    def one_output(self):
        self.heading('출력 하나 · 중간 합 하나')
        self.annotation('예: 중간 합 0 → 4 → 12',GOLD)
        return [Succession(self.sums[0].change(4,GOLD).set_run_time(1),Indicate(self.sums[0],color=GOLD,run_time=2),self.sums[0].change(12,GOLD).set_run_time(1),Indicate(self.sums[0],color=GOLD,run_time=2))]
    def many_outputs(self):
        self.heading('출력 여러 개 · 여러 중간 합')
        self.annotation('여기서는 네 개 출력의 중간 합을 유지')
        return self.replace(*self.register_board(4))
    def pressure(self):
        self.heading('Register Pressure')
        self.annotation('동시에 유지해야 할 값이 많아지는 상황')
        return [LaggedStart(*[Indicate(r,color=PINK) for r in self.sums],lag_ratio=.3)]
    def sm(self):
        self.heading('SM 안의 Register 자원은 유한합니다')
        self.pool=MemoryBox('SM · 여러 Block이 사용하는 Register 자원',7.2,4.8,MINT).move_to(DOWN*.2)
        self.blocks=VGroup(*[MemoryBox(f'Block {i}',2.8,1.2,GOLD) for i in range(4)]).arrange_in_grid(rows=2,cols=2,buff=.35).move_to(DOWN*.35)
        self.annotation('각 Thread의 전용 값 · 물리적 자원 총량은 SM에서 공유')
        return self.replace(self.pool,self.blocks)
    def budget(self):
        self.heading('계산 예제의 가정')
        a=self.card('SM 자원','65,536개의 32-bit Registers',1.65,MINT)
        b=self.card('SM 상주 상한 / Block 크기','64 Warps / 256 Threads per Block',-1,GOLD)
        self.annotation('다른 자원 제한·할당 단위는 생략한 단순 모델')
        return self.replace(a,b)
    def sixteen(self):
        self.heading('Thread당 16 Registers')
        a=self.card('Block당 Register','256 × 16 = 4,096',1.65,GOLD)
        b=self.card('8 Blocks = 64 Warps','8 × 4,096 = 32,768 Registers',-1,MINT)
        self.annotation('Register는 여유 · 이 가정에서는 Warp 상한에 먼저 도달')
        return self.replace(a,b)
    def sixtyfour(self):
        self.heading('Thread당 64 Registers')
        a=self.card('Block당 Register','256 × 64 = 16,384',1.65,GOLD)
        b=self.card('4 Blocks = 32 Warps','4 × 16,384 = 65,536 Registers',-1,PINK)
        self.annotation('같은 Thread 수에 4배 자원 · 이번에는 Register가 한계')
        return self.replace(a,b)
    def resident(self):
        self.heading('상주 가능 작업 수가 줄어드는 경우')
        a=self.card('16 Registers / Thread','8 Blocks · 64 Warps',1.65,BLUE)
        b=self.card('64 Registers / Thread','4 Blocks · 32 Warps',-1,PINK)
        self.annotation('앞의 가정에 한정 · 실제 값은 GPU와 Kernel마다 다름')
        return self.replace(a,b)
    def occupancy(self):
        self.heading('Occupancy = 상주 Warp / 최대 상주 Warp')
        self.slots=WarpSlots(32).move_to(UP*.5)
        self.value=txt('Resident Warps / Maximum Resident Warps',23,MINT).move_to(DOWN*2)
        self.annotation('상주 = 실행 상태를 SM에 유지 · 모두 동시 명령 실행은 아님')
        return self.replace(self.slots,self.value)
    def half(self):
        self.heading('32 / 64 = 50% Occupancy')
        self.annotation('칸 하나 = Warp 하나 · 채워진 칸 = 상주 Warp')
        return [Circumscribe(VGroup(*self.slots.slots[:32]),color=MINT)]
    def full(self):
        self.heading('64 / 64 = 100% Occupancy')
        self.annotation('64개 상한은 이 예제의 가정 · GPU마다 다름')
        return [Succession(LaggedStart(*[r.animate.set_fill(MINT,opacity=.65).set_stroke(MINT) for r in self.slots.slots[32:]],lag_ratio=.06,run_time=1.5),Circumscribe(self.slots,color=MINT,run_time=4.5))]
    def question(self):
        self.heading('Occupancy ↑ = 언제나 더 빠름?')
        self.annotation('비율 자체는 성능 점수가 아닙니다')
        return [Circumscribe(self.slots,color=GOLD),Indicate(self.value,color=GOLD)]
    def scheduler(self):
        self.warps=VGroup(*[MemoryBox(f'Warp {i}',4.4,1.4,GOLD if i else PINK).move_to([-1.3,y,0]) for i,y in enumerate([1.8,0,-1.8])])
        self.status=VGroup(*[txt('데이터 대기' if i==0 else '준비 완료',24,PINK if i==0 else MINT).move_to([-1.3,y-.16,0]) for i,y in enumerate([1.8,0,-1.8])])
        self.engine=MemoryBox('계산 장치',1.85,2.4,MINT).move_to([2.5,0,0])
        self.engine_text=txt('명령\n실행',25,MINT).move_to([2.5,-.2,0])
        return self.warps,self.status,self.engine,self.engine_text
    def waiting(self):
        self.heading('Warp 0 · Global Memory 데이터 대기')
        self.annotation('상주 Warp 중 세 개만 확대 · 실제 스케줄 순서의 재현은 아님')
        anim=self.replace(*self.scheduler())
        return [Succession(AnimationGroup(*anim,run_time=1),Circumscribe(self.warps[0],color=PINK,run_time=5))]
    def ready(self):
        self.heading('준비된 다른 Warp의 명령 실행')
        self.annotation('대기 중인 Warp가 있어도 준비된 일을 진행')
        return [Succession(self.flow(self.warps[1].get_right(),self.engine.get_left(),MINT),Circumscribe(self.engine,color=MINT))]
    def hiding(self):
        self.heading('Latency Hiding · 대기 시간 숨기기')
        self.annotation('준비된 Warp의 명령 발행으로 계산 장치 활용')
        return [Succession(self.flow(self.warps[2].get_right(),self.engine.get_left(),MINT),self.flow(self.warps[1].get_right(),self.engine.get_left(),MINT))]
    def few(self):
        self.heading('대신 실행할 준비된 Warp가 없다면?')
        self.annotation('상주 수가 적으면 대기를 숨길 선택지가 부족할 수 있음')
        return [AnimationGroup(self.warps[1:].animate.set_opacity(.15),self.status[1:].animate.set_opacity(.15),self.engine.animate.set_color(MUTED),self.engine_text.animate.set_color(MUTED),Circumscribe(self.warps[0],color=PINK))]
    def not_max(self):
        self.heading('100%는 최고 성능 보장이 아닙니다')
        a=self.card('상주 Warp 수','준비된 작업의 여유',1.5,MINT)
        b=self.card('Thread 내부 계산 효율','재사용 · 독립적인 계산 · 메모리 접근',-1,GOLD)
        self.annotation('둘을 함께 봐야 실제 실행 비용을 이해할 수 있습니다')
        return self.replace(a,b)
    def more_work(self):
        self.heading('값을 Register에 두고 여러 계산에 재사용')
        self.annotation('같은 입력을 다시 읽는 일을 줄일 수 있습니다')
        anim=self.replace(*self.register_board(4))
        return [Succession(AnimationGroup(*anim,run_time=1),LaggedStart(*[r.change(v,GOLD) for r,v in zip(self.sums,[4,8,12,16])],lag_ratio=.2,run_time=2),Circumscribe(self.sums,color=GOLD,run_time=3))]
    def benefit(self):
        self.heading('낮아진 Occupancy보다 재사용 이득이 클 수도')
        self.annotation('실행 시간으로 확인할 문제 · 속도 비율을 예측한 그림이 아님')
        return [LaggedStart(*[Indicate(r,color=GOLD) for r in self.sums],lag_ratio=.2)]
    def cap(self):
        self.heading('Register를 과도하게 제한하면?')
        self.regbox=MemoryBox('Register · 필요한 값 네 개 / 보관 여유 두 개',7,1.7,GOLD).move_to(UP*1.5)
        self.vals=VGroup(*[DataCell(v,.65,GOLD) for v in [3,7,2,9]]).arrange(RIGHT,buff=.45).move_to(UP*1.25)
        self.local=MemoryBox('Local Memory · Thread 전용 주소 공간',7,1.8,PINK).move_to(DOWN*1.65)
        self.local.title.next_to(self.local.box,DOWN,buff=.14)
        self.annotation('값과 공간의 개념도 · 실제 Register 제한 수치를 나타내지 않음')
        return self.replace(self.regbox,self.vals,self.local)
    def spill(self):
        self.heading('Register Spill · 일부 값을 메모리에 저장')
        self.annotation('일반적으로 device memory에 저장 · 캐시가 개입할 수 있음')
        return [LaggedStart(*[self.vals[i].animate.move_to([x,-1.85,0]).set_color(PINK) for i,x in [(2,-.65),(3,.65)]],lag_ratio=.3)]
    def reload(self):
        self.heading('필요할 때 다시 읽기 · 추가 메모리 접근')
        self.annotation('추가 저장·읽기 비용 · 실제 지연은 캐시 등에도 영향')
        return [Succession(self.flow(self.vals[2].get_top(),self.regbox.get_bottom(),PINK),self.flow(self.vals[3].get_top(),self.regbox.get_bottom(),PINK))]
    def balance(self):
        self.heading('Register를 충분히 · 준비된 Warp도 충분히')
        a=self.card('Thread당 필요한 값','재사용과 계산 효율',1.5,GOLD)
        b=self.card('SM에 유지할 Warp','대기를 숨길 수 있는 작업',-1,MINT)
        self.annotation('너무 적어도 · 너무 많아도 · 무조건 좋지는 않습니다')
        return self.replace(a,b)
    def tile(self):
        self.heading('Thread당 출력 ↑ → 중간 합 ↑ 가능')
        self.annotation('Tile 설계의 Register 요구량이 상주 Warp 수에 영향을 줄 수 있음')
        return self.replace(*self.register_board(4))
    def chain(self):
        self.heading('서로 연결된 설계 선택')
        self.links=VGroup(*[MemoryBox(t,6.5,1,c) for t,c in [('Tile / Thread당 계산량',BLUE),('Register 사용량',GOLD),('상주 Warp / Occupancy',MINT),('재사용 + Latency Hiding',PINK)]]).arrange(DOWN,buff=.25)
        self.annotation('하나를 바꾸면 다른 요소도 달라질 수 있습니다')
        return self.replace(self.links)
    def measure(self):
        self.heading('숫자의 최대화보다 실제 실행 시간')
        self.annotation('Register · Spill · 준비된 Warp · 실행 시간을 함께 확인')
        return [Succession(*[Circumscribe(m,color=MINT) for m in self.links])]
    def ending(self):
        self.heading('한 Thread의 일 ↔ 함께 유지할 Warp')
        a=self.card('Thread당 작업','필요한 값을 유지하며 효율적으로 계산',1.5,GOLD)
        b=self.card('함께 유지할 작업','준비된 Warp로 대기를 숨기기',-1,MINT)
        self.annotation('Register Pressure와 Occupancy · 균형의 문제')
        return self.replace(a,b)
