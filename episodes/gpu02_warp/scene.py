"""GPU 02 — Warp란 무엇인가. 164s, silent portrait master + timed script."""
import os
import sys
from pathlib import Path
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from gpu_series.components import DataCell, DataArrow, data_row
from gpu_series.style import label as txt

config.pixel_width = int(os.getenv('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#091119'
INK, MUTED, MINT, BLUE, GOLD, PINK, PURPLE = '#EDF3F7', '#94A7B7', '#61E4CF', '#68D9F0', '#F3CF75', '#FF8C9D', '#AF9CF5'
DURATION = 164
HEAD_Y, SUB_Y = 3.65, -5.85
LANE_STEP, SMALL_CELL = .84, .64
VALUES = [-2, 3, 0, 4, -1, 2, -3, 1]
POSITIVE = [i for i,x in enumerate(VALUES) if x > 0]
OTHER = [i for i,x in enumerate(VALUES) if x <= 0]
EPS = 1e-6

# Single source: (screen transition seconds, visual action, exact subtitle text).
# narration.md, tts_script.txt and captions.srt use this text without rewriting.
CAPTIONS = [
 (0, 'recap', '앞에서는 GPU가 계산을 여러 Thread로 나누고,\nBlock과 Grid로 조직한다고 했습니다.'),
 (6, 'question', '그렇다면 이 Thread들은 실제로\n하나씩 따로 실행될까요?'),
 (11, 'group', 'GPU에서는 여러 Thread를\n일정한 묶음으로 처리합니다.'),
 (16, 'warp32', 'NVIDIA GPU에서는\n32개의 Thread가 하나의 Warp를 이룹니다.'),
 (22, 'warp0', '예를 들어 Thread 0부터 Thread 31까지가\nWarp 0,'),
 (27, 'warp1', 'Thread 32부터 Thread 63까지가\nWarp 1이 됩니다.'),
 (32, 'block_warps', '즉, Block 안의 Thread들은\n다시 Warp 단위로 나뉩니다.'),
 (37, 'instruction', 'Warp는 같은 명령을\n활성화된 Thread들에 실행합니다.'),
 (42, 'add_one', '예를 들어 모든 Thread가\n자신이 맡은 값에 1을 더한다고 해보겠습니다.'),
 (48, 'indices', 'Thread 0은 x₀을, Thread 1은 x₁을,\nThread 2는 x₂를 처리합니다.'),
 (55, 'same_instruction', '다루는 데이터는 서로 다르지만,\n수행하는 명령은 같습니다.'),
 (60, 'simt', '이런 실행 방식을 SIMT라고 부릅니다.\nSingle Instruction, Multiple Threads.'),
 (67, 'simt_meaning', '하나의 명령을 여러 Thread가\n각자의 데이터에 대해 실행하는 구조입니다.'),
 (73, 'programmer', '우리는 Thread 하나하나를\n독립적인 작업처럼 작성합니다.'),
 (78, 'execution', '실제 명령은 Warp 안에서\n활성화된 Thread들을 묶어 실행합니다.'),
 (84, 'different', '그렇다면 Warp 안의 Thread들이\n서로 다른 일을 해야 한다면 어떻게 될까요?'),
 (90, 'condition', '예를 들어 입력이 0보다 크면 한 연산을,\n그렇지 않으면 다른 연산을 한다고 해보겠습니다.'),
 (98, 'paths', '일부 Thread는 위쪽 경로를 선택하고,\n다른 Thread는 아래쪽 경로를 선택합니다.'),
 (104, 'one_instruction', '한 번의 Warp 명령으로는\n서로 다른 두 경로의 명령을 함께 실행하지 않습니다.'),
 (111, 'path_a', '한쪽 경로를 실행하는 동안,\n다른 쪽 Thread는 그 명령에서 비활성화됩니다.'),
 (119, 'path_b', '반대쪽 경로를 실행할 때는,\n이번에는 처음 Thread들이 비활성화됩니다.'),
 (127, 'divergence', '이처럼 하나의 Warp 안에서 실행 경로가 갈라지는\n현상을 Branch Divergence라고 합니다.'),
 (134, 'rejoin', '각 경로의 계산을 마친 Thread들은\n다시 공통된 다음 명령으로 이어질 수 있습니다.'),
 (140, 'performance', 'GPU 성능을 볼 때는\nThread가 몇 개인지만 중요한 것이 아닙니다.'),
 (146, 'similar', 'Warp 안의 Thread들이 얼마나 같은 실행 경로를\n따르는지도 중요합니다.'),
 (152, 'summary', 'Thread는 우리가 작성하는 작업의 단위이고,\nWarp는 명령을 실행하는 중요한 묶음입니다.'),
 (159, 'ending', 'Warp를 이해하면 GPU의 병렬 실행을\n조금 더 실제 모습에 가깝게 볼 수 있습니다.'),
]


class WarpPanel(VGroup):
    """Exactly 32 thread markers, in linear block-thread order."""
    def __init__(self, index, color=GOLD):
        super().__init__()
        self.markers = VGroup(*[VGroup(txt(f'T{i}', 16, color), Dot(radius=.025,color=color).shift(DOWN*.2))
                               for i in range(index*32,(index+1)*32)])
        self.markers.arrange_in_grid(rows=4,cols=8,buff=(.35,.18))
        self.title = txt(f'Warp {index}  /  T{index*32}–T{index*32+31}',25,color).next_to(self.markers,UP,buff=.22)
        self.frame = SurroundingRectangle(VGroup(self.markers,self.title),buff=.22,color=color,stroke_width=2)
        self.add(self.frame,self.title,self.markers)


class WarpIntroduction(Scene):
    def construct(self):
        self.stage = VGroup()
        self.sub, self.head = VGroup(), VGroup()
        self.add(txt('GPU COMPUTATION SERIES',19,MUTED).move_to(UP*6.85),
                 txt('Warp',66).move_to(UP*5.65),
                 txt('02  /  Warp란 무엇인가',23,MINT).move_to(UP*4.65))
        for i,(start,action,sentence) in enumerate(CAPTIONS):
            end = CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub)
            self.sub = txt(sentence,28).move_to(UP*SUB_Y)
            self.add(self.sub)
            # This method illustrates exactly the caption/narration above.
            animations = getattr(self,action)()
            self.play(*animations,run_time=end-start-EPS)
            if abs(self.time-end) > 1/30+.001:
                raise ValueError(f'Timing drift at {action}: {self.time} / {end}')

    def heading(self,text):
        self.remove(self.head)
        self.head=txt(text,30,MINT).move_to(UP*HEAD_Y)
        self.add(self.head)

    def track(self,*items):
        self.stage.add(*items)

    def replace(self,*items):
        old=self.stage
        self.stage=VGroup(*items)
        return [Succession(FadeOut(old,run_time=.15),AnimationGroup(*[FadeIn(m) for m in items],run_time=.85))]

    def recap(self):
        self.heading('Thread → Block → Grid')
        self.recap_threads=VGroup(*[txt(f'T{i}',23,GOLD) for i in range(8)]).arrange_in_grid(rows=2,cols=4,buff=.35)
        block=SurroundingRectangle(self.recap_threads,buff=.45,color=MINT)
        btitle=txt('Block',27,MINT).next_to(block,UP,buff=.15)
        grid=SurroundingRectangle(VGroup(block,btitle),buff=.5,color=PURPLE)
        gtitle=txt('Grid',27,PURPLE).next_to(grid,UP,buff=.15)
        self.track(self.recap_threads,block,btitle,grid,gtitle)
        return [LaggedStart(FadeIn(self.recap_threads),Create(block),FadeIn(btitle),Create(grid),FadeIn(gtitle),lag_ratio=.3)]

    def question(self):
        self.heading('Thread는 하나씩 따로 실행될까?')
        return [LaggedStart(*[Indicate(t,color=GOLD) for t in self.recap_threads],lag_ratio=.25)]

    def group(self):
        self.heading('Thread를 실행하는 묶음')
        self.w0=WarpPanel(0).move_to(UP*.5)
        return self.replace(self.w0.markers)

    def warp32(self):
        self.heading('32 Threads = 1 Warp')
        self.track(self.w0.frame,self.w0.title)
        return [Create(self.w0.frame),Write(self.w0.title),LaggedStart(*[Indicate(m,color=GOLD) for m in self.w0.markers],lag_ratio=.07)]

    def warp0(self):
        return [Succession(Indicate(self.w0.markers[0]),Circumscribe(self.w0.markers,color=GOLD),Indicate(self.w0.markers[-1]))]

    def warp1(self):
        self.w1=WarpPanel(1,BLUE).move_to(DOWN*1.6)
        self.track(self.w1)
        return [self.w0.animate.move_to(UP*1.6),FadeIn(self.w1)]

    def block_warps(self):
        self.heading('하나의 Block 안에 여러 Warp')
        self.block_frame=SurroundingRectangle(VGroup(self.w0,self.w1),buff=.24,color=MINT)
        block_label=txt('Block 0 · 64 Threads',23,MINT).next_to(self.block_frame,DOWN,buff=.16)
        self.track(self.block_frame,block_label)
        return [Create(self.block_frame),Write(block_label)]

    def instruction(self):
        self.heading('같은 명령 · 각자의 데이터')
        self.lanes=VGroup(*[txt(f'T{i}',23,GOLD).move_to([(i-3.5)*LANE_STEP,1.7,0]) for i in range(8)])
        self.warp_frame=SurroundingRectangle(self.lanes,buff=.24,color=GOLD)
        self.detail=txt('Warp 0의 T0–T7 확대 · 전체 32개 중 일부',21,MUTED).move_to(UP*2.7)
        self.command=txt('같은 명령',36,GOLD).move_to(DOWN*.4)
        return self.replace(self.lanes,self.warp_frame,self.detail,self.command)

    def add_one(self):
        self.data=data_row([3,7,2,9,1,5,4,6],SMALL_CELL).move_to(UP*.45)
        # Match centers precisely even if reusable cell spacing changes.
        for c,t in zip(self.data,self.lanes): c.set_x(t.get_x())
        links=VGroup(*[DataArrow(t.get_bottom(),c.get_top(),GOLD) for t,c in zip(self.lanes,self.data)])
        formula=txt('yᵢ = xᵢ + 1',43,GOLD).move_to(DOWN*1.2)
        self.track(self.data,links)
        return [FadeIn(self.data),Create(links),Transform(self.command,formula)]

    def indices(self):
        names=VGroup(*[txt(f'x{i}',21,BLUE).next_to(c,DOWN,buff=.13) for i,c in enumerate(self.data)])
        self.track(names)
        return [FadeIn(names),Succession(*[Indicate(VGroup(self.lanes[i],self.data[i]),color=BLUE) for i in range(3)])]

    def same_instruction(self):
        return [Indicate(self.command,color=GOLD),*[c.change(v+1,PINK) for c,v in zip(self.data,[3,7,2,9,1,5,4,6])]]

    def simt(self):
        self.heading('SIMT')
        self.simt_words=VGroup(txt('Single Instruction',32,GOLD),txt('Multiple Threads',32,BLUE)).arrange(DOWN,buff=.2).move_to(DOWN*2.8)
        self.track(self.simt_words)
        return [Write(self.simt_words)]

    def simt_meaning(self):
        return [Succession(Indicate(self.command,color=GOLD),Indicate(self.lanes,color=BLUE),Indicate(self.data,color=PINK))]

    def programmer(self):
        self.heading('작성할 때는 Thread 하나의 작업')
        return [Circumscribe(VGroup(self.lanes[0],self.data[0]),color=GOLD,buff=.16)]

    def execution(self):
        self.heading('실행할 때는 Warp의 활성 Thread들')
        return [Circumscribe(VGroup(self.lanes,self.data),color=GOLD,buff=.18),Indicate(self.command)]

    def different(self):
        self.heading('서로 다른 경로를 선택한다면?')
        question=txt('같은 Warp, 다른 실행 경로?',37,INK)
        return self.replace(question)

    def condition(self):
        self.heading('조건에 따라 달라지는 연산')
        self.lanes=VGroup(*[txt(f'T{i}',21,GOLD).move_to([(i-3.5)*LANE_STEP,2.4,0]) for i in range(8)])
        self.x=data_row(VALUES,SMALL_CELL).move_to(UP*1.5)
        for c,t in zip(self.x,self.lanes):c.set_x(t.get_x())
        self.test=txt('xᵢ > 0 ?',31,INK).move_to(UP*.7)
        self.a_label=txt('A  /  x > 0     →     x + 1',25,MINT).move_to(DOWN*.2)
        self.b_label=txt('B  /  x ≤ 0     →     x − 1',25,PINK).move_to(DOWN*1.9)
        self.a=data_row(['·']*8,SMALL_CELL,MINT).move_to(DOWN*.95)
        self.b=data_row(['·']*8,SMALL_CELL,PINK).move_to(DOWN*2.65)
        for row in [self.a,self.b]:
            for c,t in zip(row,self.lanes):c.set_x(t.get_x())
            for c in row:c.number.become(VectorizedPoint(c.box.get_center()))
        self.note=txt('Warp 0의 8개 Thread 확대 · 분기 실행 개념도',20,MUTED).move_to(DOWN*4.1)
        return self.replace(self.lanes,self.x,self.test,self.a_label,self.b_label,self.a,self.b,self.note)

    def paths(self):
        # Colored lane markers keep ownership explicit; lane IDs never change.
        return [*[self.lanes[i].animate.set_color(MINT if i in POSITIVE else PINK) for i in range(8)],
                *[self.a[i].box.animate.set_fill(MINT,opacity=.3 if i in POSITIVE else .025).set_stroke(opacity=1 if i in POSITIVE else .18) for i in range(8)],
                *[self.b[i].box.animate.set_fill(PINK,opacity=.3 if i in OTHER else .025).set_stroke(opacity=1 if i in OTHER else .18) for i in range(8)]]

    def one_instruction(self):
        self.heading('경로마다 실행에 참여하는 Thread가 다르다')
        instruction=txt('한 번의 명령 발행 → 활성 Thread에 적용',24,GOLD).move_to(DOWN*3.55)
        self.track(instruction)
        return [Write(instruction),Succession(Indicate(self.a_label),Indicate(self.b_label))]

    def path_a(self):
        self.heading('A 실행  /  양수인 Thread만 활성')
        # Inactive lane cells stay empty: no result is computed on path A for them.
        note=txt('32개 중 8개 확대 · 밝음=활성 / 흐림=비활성',20,MUTED).move_to(DOWN*4.1)
        return [Transform(self.note,note),*[c.box.animate.set_stroke(opacity=.18).set_fill(opacity=.025) for c in self.b],self.b_label.animate.set_opacity(.3),
                *[self.lanes[i].animate.set_opacity(1 if i in POSITIVE else .25) for i in range(8)],
                *[self.a[i].change(VALUES[i]+1,MINT) for i in POSITIVE],Indicate(self.a_label,color=MINT)]

    def path_b(self):
        self.heading('B 실행  /  0 이하인 Thread만 활성')
        # Activate the mask before morphing values; do not transform a parent
        # group and its changing glyph children concurrently in Manim.
        for i,c in enumerate(self.b):
            c.box.set_stroke(opacity=1 if i in OTHER else .18).set_fill(opacity=.12 if i in OTHER else .025)
        self.b_label.set_opacity(1)
        return [*[c.box.animate.set_stroke(opacity=.25).set_fill(opacity=.025) for c in self.a],
                *[c.number.animate.set_opacity(.3) for c in self.a],self.a_label.animate.set_opacity(.3),
                *[self.lanes[i].animate.set_opacity(1 if i in OTHER else .25) for i in range(8)],
                *[self.b[i].change(VALUES[i]-1,PINK) for i in OTHER],Indicate(self.b_label,color=PINK)]

    def divergence(self):
        self.heading('Branch Divergence · Warp 내부의 분기')
        return [*[c.box.animate.set_stroke(opacity=1).set_fill(opacity=.12) for row in [self.a,self.b] for c in row],
                *[c.number.animate.set_opacity(1) for c in self.a],self.a_label.animate.set_opacity(1),
                self.lanes.animate.set_opacity(1),Circumscribe(VGroup(self.a,self.b),color=GOLD,buff=.13)]

    def rejoin(self):
        self.heading('각 경로의 결과 → 공통된 다음 명령')
        values=[x+1 if x>0 else x-1 for x in VALUES]
        result=data_row(values,SMALL_CELL).move_to(DOWN*.3)
        for c,t in zip(result,self.lanes):c.set_x(t.get_x())
        title=txt('y = [−3, 4, −1, 5, −2, 3, −4, 2]',28,INK).move_to(UP*1.3)
        next_step=txt('공통된 다음 명령',32,GOLD).move_to(DOWN*2)
        # Match each output with its originating path, rather than reorder lanes.
        sources=[self.a[i] if i in POSITIVE else self.b[i] for i in range(8)]
        old=self.stage
        self.stage=VGroup(result,title,next_step)
        return [FadeOut(old),*[TransformFromCopy(src,dst) for src,dst in zip(sources,result)],Write(title),FadeIn(next_step)]

    def performance(self):
        self.heading('Thread 수만으로는 실행 효율을 알 수 없다')
        self.same=VGroup(*[Square(.55,color=MINT,fill_opacity=.3) for _ in range(8)]).arrange(RIGHT,buff=.18).move_to(UP*.8)
        self.split=VGroup(*[Square(.55,color=MINT if i%2 else PINK,fill_opacity=.3) for i in range(8)]).arrange(RIGHT,buff=.18).move_to(DOWN*1)
        labels=VGroup(txt('같은 경로',26,MINT).next_to(self.same,UP,buff=.2),txt('나뉜 경로',26,PINK).next_to(self.split,UP,buff=.2))
        note=txt('같은 Thread 수 · 다른 활성 패턴',26,MUTED).move_to(DOWN*2.5)
        return self.replace(self.same,self.split,labels,note)

    def similar(self):
        return [Indicate(self.same,color=MINT),Succession(Indicate(VGroup(*self.split[::2]),color=PINK),Indicate(VGroup(*self.split[1::2]),color=MINT))]

    def summary(self):
        self.heading('Thread와 Warp를 구분해서 보기')
        self.summary_group=VGroup(txt('Thread',45,GOLD),txt('우리가 작성하는 작업 단위',28,INK),
                                 txt('Warp',45,MINT),txt('활성 Thread에 명령을 실행하는 묶음',27,INK)).arrange(DOWN,buff=.45)
        return self.replace(self.summary_group)

    def ending(self):
        conclusion=txt('작업의 관점 → 실행의 관점',30,BLUE).move_to(DOWN*3)
        self.track(conclusion)
        return [Write(conclusion),Circumscribe(self.summary_group,color=MINT,buff=.25)]
