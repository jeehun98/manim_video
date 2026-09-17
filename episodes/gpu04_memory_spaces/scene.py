"""GPU 04: memory placement and reuse. Screen timeline is the narration source."""
import os
import sys
from pathlib import Path
from manim import *
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from gpu_series.components import DataCell, ThreadMarker, MemoryBox, DataArrow
from gpu_series.style import label as txt

config.pixel_width = int(os.getenv('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#091119'
BLUE, GOLD, MINT, PINK, MUTED = '#68D9F0', '#F3CF75', '#61E4CF', '#FF8C9D', '#94A7B7'
HEAD_Y, SUB_Y, EPS = 3.8, -5.85, 1e-6
GLOBAL_Y, SHARED_Y, THREAD_Y, REGISTER_Y = 2.35, .05, -1.65, -2.65
DURATION = 174
# Each entry binds its exact spoken caption to one visual action and interval.
CAPTIONS = [
 (0, 'recap', '앞에서는 Warp의 Thread들이 어떤 주소를 함께 읽느냐에 따라,\n메모리 접근 비용이 달라질 수 있다는 것을 봤습니다.'),
 (7, 'spaces', '그런데 GPU에는 메모리가 하나만 있는 것이 아닙니다.\n데이터를 어디에 두느냐에 따라 접근 방식과 비용도 달라집니다.'),
 (14, 'global_intro', '먼저 Global Memory입니다.\n큰 배열이나 Tensor, 입력과 출력은 주로 여기에 저장됩니다.'),
 (20, 'global_users', '많은 Thread가 접근할 수 있고,\n큰 데이터를 저장할 수 있습니다.'),
 (25, 'repeated', '하지만 계산할 때마다 값을 다시 가져오면,\n데이터 이동 자체가 큰 비용이 될 수 있습니다.'),
 (31, 'register_intro', '자주 사용하는 값은 더 가까운 곳에 둘 수 있습니다.\n그중 하나가 Register입니다.'),
 (37, 'register_private', 'Register는 각 Thread가\n자신의 계산에 사용할 값을 보관하는 공간입니다.'),
 (43, 'load_register', 'Thread 하나가 Global Memory에서\n값 3을 읽어 Register에 가져왔다고 해보겠습니다.'),
 (49, 'compute_one', '읽어온 값에 1을 더하면 4가 됩니다.\n계산 중인 값은 Register에 있습니다.'),
 (55, 'compute_two', '여기에 2를 곱하면 8이 됩니다.\n처음 값을 다시 읽지 않고, 계산을 이어갑니다.'),
 (61, 'private_scope', 'Register는 기본적으로 그 Thread 자신의 공간입니다.\n다른 Thread와 데이터를 공유하기 위한 공간은 아닙니다.'),
 (67, 'shared_question', '그렇다면 같은 Block 안의 여러 Thread가\n같은 데이터를 반복해서 사용한다면 어떨까요?'),
 (73, 'shared_intro', '이때 Shared Memory를 사용할 수 있습니다.\n같은 Block 안의 Thread들이 함께 쓰는 공간입니다.'),
 (79, 'shared_repeat', '여기서는 여러 Thread가 같은 값을 재사용합니다.\n매번 Global Memory에서 읽을 수도 있지만,'),
 (85, 'stage_shared', '먼저 필요한 데이터를\nGlobal Memory에서 Shared Memory로 가져올 수 있습니다.'),
 (91, 'ready', '함께 쓰기 전에 데이터 준비가 끝났는지 맞춥니다.\n필요한 동기화 뒤, 다른 Thread도 이 값을 사용할 수 있습니다.'),
 (97, 'reuse_one', '이제 Block 안의 여러 Thread가\nShared Memory에 둔 값을 읽어 계산합니다.'),
 (103, 'reuse_again', '같은 데이터를 다시 사용할 때도,\n가까운 공유 공간에서 가져올 수 있습니다.'),
 (109, 'reuse_message', '한 번 가져온 데이터를 여러 Thread가 함께 재사용합니다.\n반복해서 쓰는 계산에서 특히 중요한 구조입니다.'),
 (115, 'shared_limit', '하지만 Shared Memory도 무한하지 않습니다.\nBlock이 사용할 수 있는 공간에는 한계가 있습니다.'),
 (121, 'register_limit', 'Register도 많이 쓴다고 항상 좋은 것은 아닙니다.\n이 역시 GPU 안의 제한된 자원입니다.'),
 (127, 'occupancy', 'Thread 하나가 너무 많은 Register를 사용하면,\n동시에 유지할 수 있는 Thread 수가 줄어들 수 있습니다.'),
 (133, 'tradeoff', '즉, 가장 빠른 메모리 하나만 사용하는 것이\n최적화의 답은 아닙니다.'),
 (138, 'criteria', '데이터가 얼마나 큰지, 누가 사용하는지,\n얼마나 자주 다시 사용하는지에 따라 저장 위치가 달라집니다.'),
 (144, 'summary_global', '큰 입력과 출력은 Global Memory에 두고,\nThread가 직접 계산하는 값은 Register에 둡니다.'),
 (150, 'summary_shared', '같은 Block의 Thread들이 함께 재사용할 값은\nShared Memory에 둘 수 있습니다.'),
 (156, 'compare', 'Coalesced Memory Access가 어떻게 읽느냐의 문제였다면,\n이번에는 어디에 두고 얼마나 재사용하느냐의 문제입니다.'),
 (162, 'path', 'GPU의 성능을 이해하려면 연산 수뿐 아니라,\n데이터가 어디에 저장되고 어디로 이동하는지도 봐야 합니다.'),
 (168, 'ending', '그리고 그 데이터를 몇 번 다시 사용하는지.\n데이터의 위치와 재사용이 실행 성능을 바꿉니다.'),
]

class MemoryDiagram(VGroup):
    """Conceptual storage scopes; vertical distance is not hardware latency."""
    def __init__(self):
        super().__init__()
        self.global_box = MemoryBox('Global Memory · 큰 입력과 출력',7.2,1.65,BLUE).move_to(UP*GLOBAL_Y)
        self.inputs = VGroup(*[DataCell(v,.55) for v in [3,7,2,9,1,5,6,4]]).arrange(RIGHT,buff=.19).move_to(UP*2.13)
        self.block = Rectangle(width=7.2,height=5.5,color=MINT,stroke_width=2).move_to(DOWN*1.4)
        self.block_title = txt('Block 0 · Thread 4개만 확대 표시',21,MINT).move_to(UP*1.05)
        self.shared = MemoryBox('Shared Memory · Block 공용',6.2,1.25,MINT).move_to(UP*SHARED_Y)
        self.shared_cells = VGroup(*[DataCell('–',.5,MINT) for _ in range(4)]).arrange(RIGHT,buff=.35).move_to(DOWN*.16)
        self.threads = VGroup(*[ThreadMarker(i).move_to([x,THREAD_Y,0]) for i,x in enumerate([-2.5,-.83,.83,2.5])])
        self.regs = VGroup(*[DataCell('–',.62,GOLD).move_to([x,REGISTER_Y,0]) for x in [-2.5,-.83,.83,2.5]])
        self.reg_labels = VGroup(*[txt('Register',16,GOLD).next_to(r,DOWN,buff=.16) for r in self.regs])
        self.add(self.global_box,self.inputs,self.block,self.block_title,self.shared,self.shared_cells,self.threads,self.regs,self.reg_labels)

class MemorySpacesIntroduction(Scene):
    def construct(self):
        self.stage, self.head, self.sub, self.note = VGroup(),VGroup(),VGroup(),VGroup()
        self.add(txt('GPU COMPUTATION SERIES',19,MUTED).move_to(UP*6.85),
                 txt('Memory & Reuse',49).move_to(UP*5.65),
                 txt('04  /  어디에 두고, 얼마나 다시 쓸까',23,MINT).move_to(UP*4.65))
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub)
            self.sub=txt(caption,27).move_to(UP*SUB_Y)
            self.add(self.sub)
            # This action illustrates exactly the caption above, with no silent wait.
            self.play(*getattr(self,action)(),run_time=end-start-EPS)
            if abs(self.time-end)>1/30+.001:
                raise ValueError(f'Timeline drift: {action}: {self.time} != {end}')

    def heading(self,text):
        self.remove(self.head); self.head=txt(text,28,MINT).move_to(UP*HEAD_Y); self.add(self.head)

    def annotation(self,text,color=MUTED):
        self.remove(self.note); self.note=txt(text,22,color).move_to(DOWN*4.65); self.add(self.note)

    def replace(self,*items):
        old=self.stage; self.stage=VGroup(*items)
        return [Succession(FadeOut(old,run_time=.15),FadeIn(self.stage,run_time=.85))]

    def reveal(self,*items):
        self.stage.add(*items)
        return [LaggedStart(*[FadeIn(m) for m in items],lag_ratio=.2)]

    def flow(self,start,end,color=BLUE,via=None):
        # One transient group owns every moving part; no particles survive cleanup.
        points=[start]+(via or [])+[end]
        path=VMobject().set_points_as_corners(points)
        lines=VGroup(*[Line(a,b,color=color,stroke_width=2) for a,b in zip(points[:-2],points[1:-1])])
        lines.add(DataArrow(points[-2],points[-1],color))
        token=Dot(start,radius=.09,color=color)
        group=VGroup(lines,token).set_opacity(0)
        def update(m,alpha):
            m.set_opacity(min(1,alpha*8,(1-alpha)*8))
            token.move_to(path.point_from_proportion(alpha))
        return UpdateFromAlphaFunc(group,update,remover=True,rate_func=linear)

    def recap(self):
        self.heading('Warp의 주소 패턴 → 메모리 접근 비용')
        self.row=VGroup(*[DataCell(i,.6) for i in range(8)]).arrange(RIGHT,buff=.2)
        self.ts=VGroup(*[ThreadMarker(i).next_to(c,UP,buff=1) for i,c in enumerate(self.row)])
        self.annotation('이전 편 · 32개 Thread 중 8개 표시')
        self.stage.add(self.row,self.ts)
        return [FadeIn(self.row),LaggedStart(*[FadeIn(t) for t in self.ts],lag_ratio=.15)]

    def spaces(self):
        self.heading('어떻게 읽을까 → 어디에 둘까')
        self.cards=VGroup(*[MemoryBox(n,6,1.3,c) for n,c in [('Global Memory',BLUE),('Register',GOLD),('Shared Memory',MINT)]]).arrange(DOWN,buff=.6)
        self.annotation('저장 공간마다 역할과 사용 범위가 다릅니다')
        return self.replace(self.cards)

    def global_intro(self):
        self.heading('Global Memory')
        self.d=MemoryDiagram(); self.annotation('배열 · Tensor · 입력 · 출력')
        return self.replace(self.d.global_box,self.d.inputs)

    def global_users(self):
        self.annotation('여러 Thread에서 접근 가능한 저장 공간')
        return self.reveal(self.d.block,self.d.block_title,self.d.threads)

    def repeated(self):
        self.heading('같은 값을 매번 다시 읽는다면?')
        self.annotation('이동 화살표는 논리적 읽기 · 실제 비용은 캐시 등에도 영향')
        return [Succession(*[self.flow(self.d.inputs[0].get_bottom(),self.d.threads[0].get_top()) for _ in range(3)])]

    def register_intro(self):
        self.heading('Register · Thread별 계산 값')
        self.annotation('계산 가까이에 값을 보관')
        return self.reveal(self.d.regs,self.d.reg_labels)

    def register_private(self):
        return [LaggedStart(*[Circumscribe(VGroup(t,r,l),color=GOLD) for t,r,l in zip(self.d.threads,self.d.regs,self.d.reg_labels)],lag_ratio=.25)]

    def load_register(self):
        self.annotation('Global Memory → T0의 Register',BLUE)
        return [Succession(self.flow(self.d.inputs[0].get_left(),self.d.regs[0].get_left()),self.d.regs[0].change(3,GOLD))]

    def compute_one(self):
        self.heading('T0 · Register에서 계산')
        self.annotation('3 + 1 = 4',GOLD)
        return [Succession(self.d.regs[0].change(4,GOLD).set_run_time(1),Indicate(self.d.regs[0],color=GOLD,run_time=5))]

    def compute_two(self):
        self.annotation('4 × 2 = 8 · 처음 입력을 다시 읽지 않음',GOLD)
        return [Succession(self.d.regs[0].change(8,GOLD).set_run_time(1),Indicate(self.d.regs[0],color=GOLD,run_time=5))]

    def private_scope(self):
        self.annotation('기본 사용 범위: 각 Thread 자신')
        return [LaggedStart(*[Circumscribe(VGroup(t,r),color=GOLD) for t,r in zip(self.d.threads,self.d.regs)],lag_ratio=.25)]

    def shared_question(self):
        self.heading('같은 Block이 함께 재사용한다면?')
        self.annotation('개인 계산 값 → 함께 쓰는 데이터')
        return [Circumscribe(self.d.block,color=MINT),LaggedStart(*[Indicate(t,color=MINT) for t in self.d.threads],lag_ratio=.2)]

    def shared_intro(self):
        self.heading('Shared Memory · Block 안의 공용 공간')
        self.annotation('같은 Block의 Thread들이 함께 사용')
        return self.reveal(self.d.shared,self.d.shared_cells)

    def shared_repeat(self):
        self.annotation('예: 여러 Thread가 같은 입력값을 반복해서 사용')
        return [Succession(*[self.flow(self.d.inputs[0].get_left(),t.get_top(),via=[[-3.85,2.13,0],[-3.85,-1.1,0],[t.get_x(),-1.1,0]]) for t in self.d.threads])]

    def stage_shared(self):
        self.heading('필요한 데이터를 먼저 가져오기')
        self.annotation('Thread가 데이터를 Shared Memory에 적재',BLUE)
        return [Succession(self.flow(self.d.inputs[0].get_bottom(),self.d.shared_cells[0].get_top()),self.d.shared_cells[0].change(3,MINT))]

    def ready(self):
        self.heading('준비 완료 후 공유 · 필요한 동기화')
        self.annotation('쓰기 완료 확인 → 함께 읽기',MINT)
        return [Succession(Circumscribe(self.d.shared_cells[0],color=MINT),LaggedStart(*[Indicate(t,color=MINT) for t in self.d.threads],lag_ratio=.15))]

    def reuse_one(self):
        self.heading('Shared Memory → 각 Thread의 계산 값')
        self.annotation('공유 데이터 3을 각자의 Register로 읽기',MINT)
        return [LaggedStart(*[Succession(self.flow(self.d.shared_cells[0].get_bottom(),r.get_top(),MINT),r.change(3,GOLD)) for r in self.d.regs],lag_ratio=.2)]

    def reuse_again(self):
        self.annotation('다시 필요할 때도 Shared Memory에서 읽기',MINT)
        return [LaggedStart(*[self.flow(self.d.shared_cells[0].get_bottom(),r.get_top(),MINT) for r in self.d.regs],lag_ratio=.2)]

    def reuse_message(self):
        self.heading('가져오기 → 준비 → 함께 재사용')
        self.annotation('반복 재사용이 적재 비용을 줄이는 데 도움')
        return [Succession(Circumscribe(self.d.shared,color=MINT),Circumscribe(self.d.regs,color=GOLD))]

    def shared_limit(self):
        self.heading('Shared Memory에도 용량 한계가 있습니다')
        self.annotation('Block별 할당량과 하드웨어 자원에 제한')
        return [LaggedStart(*[c.box.animate.set_fill(PINK,opacity=.45) for c in self.d.shared_cells],lag_ratio=.35),Circumscribe(self.d.shared,color=PINK)]

    def register_limit(self):
        self.heading('Register도 한정된 자원')
        self.annotation('자원을 많이 쓰는 것이 항상 유리하지는 않습니다')
        self.pool=MemoryBox('Register 자원 · 개념도',7,2.5,GOLD).move_to(UP*1.5)
        self.chunks=VGroup(*[Rectangle(width=.65,height=1,color=GOLD,fill_opacity=.3,fill_color=GOLD) for _ in range(8)]).arrange(RIGHT,buff=.12).move_to(UP*1.25)
        self.resident=VGroup(*[txt(f'T{i}',29,GOLD) for i in range(8)]).arrange(RIGHT,buff=.42).move_to(DOWN*1)
        self.resource_note=txt('작은 Thread당 사용량 → 더 많은 작업 유지 가능',23).move_to(DOWN*2.4)
        return self.replace(self.pool,self.chunks,self.resident,self.resource_note)

    def occupancy(self):
        self.heading('Thread당 자원 ↑ → 동시 유지 수가 줄 수도')
        self.annotation('개념적 비교 · 실제 Thread 수나 성능 비율이 아님')
        new=VGroup(*[Rectangle(width=1.42,height=1,color=PINK,fill_opacity=.4,fill_color=PINK) for _ in range(4)]).arrange(RIGHT,buff=.12).move_to(self.chunks)
        note=txt('큰 Thread당 사용량 → 유지할 수 있는 작업 감소 가능',23).move_to(self.resource_note)
        self.stage.remove(self.resource_note); self.stage.add(note)
        return [AnimationGroup(Transform(self.chunks,new,run_time=6),self.resident[4:].animate(run_time=6).set_opacity(.15),Succession(FadeOut(self.resource_note,run_time=.25),FadeIn(note,run_time=.25)))]

    def tradeoff(self):
        self.heading('속도만으로 고를 수는 없습니다')
        self.annotation('저장 공간의 역할과 자원 사용량을 함께 보기')
        self.criteria_cards=VGroup(*[MemoryBox(t,6.2,1.25,c) for t,c in [('크기 · 얼마나 큰 데이터인가?',BLUE),('사용 범위 · 누가 사용하는가?',GOLD),('재사용 · 얼마나 자주 쓰는가?',MINT)]]).arrange(DOWN,buff=.55)
        return self.replace(self.criteria_cards)

    def criteria(self):
        return [Succession(*[Circumscribe(c,color=c.box.get_color()) for c in self.criteria_cards])]

    def summary_global(self):
        self.heading('데이터 역할에 맞게 배치')
        self.annotation('Global Memory: 큰 데이터 / Register: 개인 계산')
        self.d=MemoryDiagram()
        return self.replace(self.d.global_box,self.d.inputs,self.d.block,self.d.block_title,self.d.threads,self.d.regs,self.d.reg_labels)

    def summary_shared(self):
        self.annotation('Shared Memory: 같은 Block 안에서 함께 재사용',MINT)
        return self.reveal(self.d.shared,self.d.shared_cells)

    def compare(self):
        self.heading('접근 패턴 + 저장 위치 + 재사용')
        self.annotation('어떻게 읽는가 → 어디에 두고 다시 쓰는가')
        return [Succession(Circumscribe(self.d.inputs,color=BLUE),Circumscribe(self.d.shared,color=MINT),Circumscribe(self.d.regs,color=GOLD))]

    def path(self):
        self.heading('데이터의 이동 경로를 함께 보기')
        self.annotation('공유가 필요 없는 값은 Global → Register로 바로 읽음')
        return [Succession(self.flow(self.d.inputs[0].get_bottom(),self.d.shared_cells[0].get_top()),self.flow(self.d.shared_cells[0].get_bottom(),self.d.regs[0].get_top(),MINT))]

    def ending(self):
        self.heading('위치와 재사용이 성능을 바꿉니다')
        self.annotation('저장 → 이동 → 계산 → 재사용',MINT)
        return [Succession(*[self.flow(self.d.shared_cells[0].get_bottom(),r.get_top(),MINT) for r in self.d.regs])]
