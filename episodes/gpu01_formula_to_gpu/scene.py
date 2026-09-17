"""GPU 01: 145초 시각 설명 영상. 대본과 타이밍은 timeline.py에서 수정합니다."""
import importlib.util
import os
from pathlib import Path
import sys
import textwrap

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from manim import *
from gpu_series.style import *
from gpu_series.components import *

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('gpu01_timeline', HERE / 'timeline.py')
timing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(timing)
config.pixel_width = int(os.getenv('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = FRAME_WIDTH, FRAME_HEIGHT
config.frame_rate = timing.FPS
config.background_color = BG

# Editable relative phase durations inside each spoken sentence.
PHASE_WEIGHTS = {
    'first_results': (1, 1), 'other_results': (1, 3),
    'load': (1, 3, 1), 'store': (1, 3, 1),
    'compute': (1, 2), 'finish_results': (1, 2),
}
MEMORY_X, BLOCK_X, MEMORY_Y = -2.45, 1.8, -.3
MEMORY_W, MEMORY_H = 2.8, 7.5
INPUT_Y, OUTPUT_Y, REGISTER_Y, COMPUTE_Y = 1.4, -1.5, -.15, -1.1
BLOCK_SPACING_X, BLOCK_SPACING_Y, ZOOM_WIDTH = 7.2, 3.2, 17
SUMMARY_TOP, SUMMARY_GAP = 2.4, .85
MAX_SILENT_HOLD = 1.0
FRAME_EPSILON = 1e-6  # np.arange must not emit an extra frame at a float boundary.


class FormulaToGPU(MovingCameraScene):
    def construct(self):
        self.stage = VGroup()
        self.heading, self.caption = VGroup(), VGroup()
        self.brand = self.hud('GPU COMPUTATION  /  01', TITLE_Y, 21, MUTED)
        self.add(self.brand)
        for cue in timing.CUES:
            duration = cue['end'] - cue['start']
            self.short_gap(cue['start'])
            self.set_caption(cue['text'])
            self.current_action = cue['action']
            animations = getattr(self, 'anim_' + cue['action'])()
            if isinstance(animations, dict):
                # Rebuild Cairo's moving-object list at each transfer phase.
                # A token introduced inside nested Succession can otherwise be
                # cached as a static object while MoveAlongPath is running.
                weights = PHASE_WEIGHTS[self.current_action]
                count = round(duration * timing.FPS)
                counts = [round(count*w/sum(weights)) for w in weights[:-1]]
                counts.append(count-sum(counts))
                for animation, frames in zip(animations['phases'], counts):
                    self.play(animation, run_time=frames/timing.FPS-FRAME_EPSILON)
            else:
                # Preserve each animation's own easing (Indicate returns to rest).
                self.play(*animations, run_time=duration - FRAME_EPSILON)
            if abs(self.time - cue['end']) > 1 / timing.FPS + .001:
                raise ValueError(f"Cue {cue['id']} drifted: {self.time:.6f} vs {cue['end']:.6f}")
        self.short_gap(timing.DURATION)

    def short_gap(self, target):
        delta = target - self.time
        if delta < -.02 or delta > MAX_SILENT_HOLD:
            raise ValueError(f'Unexpected silent hold: {delta:.3f}s')
        if delta > .001:
            self.wait(delta - FRAME_EPSILON, frozen_frame=False)

    def hud(self, text, y, size=28, color=INK):
        obj = label(text, size, color)
        original_width = obj.width
        def pin(m):
            factor = self.camera.frame.width / FRAME_WIDTH
            if original_width:
                m.set(width=original_width * factor)
            m.move_to(self.camera.frame.get_center() + UP * y * factor)
        obj.add_updater(pin)
        obj.set_z_index(20)
        pin(obj)
        return obj

    def set_caption(self, text):
        self.remove(self.caption)
        lines = '\n'.join(textwrap.wrap(text, width=30, break_long_words=False))
        self.caption = self.hud(lines, CAPTION_Y)
        self.add(self.caption)

    def heading_to(self, text):
        self.remove(self.heading)
        self.heading = self.hud(text, HEAD_Y, 32, BLOCK)
        self.add(self.heading)

    def track(self, *objects):
        self.stage.add(*objects)

    def replace_stage(self, *objects):
        old = self.stage
        self.stage = VGroup(*objects)
        return [Succession(FadeOut(old, run_time=.15),
                           AnimationGroup(*[FadeIn(m) for m in objects], run_time=.85))]

    def phases(self, *animations):
        weights = PHASE_WEIGHTS[self.current_action]
        return Succession(*[a.set_run_time(w) for a, w in zip(animations, weights)])

    # 01: 각 원소에 1을 더합니다.
    def anim_formula(self):
        self.formula = label('yᵢ = xᵢ + 1', 72)
        self.track(self.formula)
        return [Write(self.formula)]

    # 02: 수학적으로는 이 한 줄이면 충분합니다.
    def anim_formula_focus(self):
        self.heading_to('수식 하나가 GPU에서 실행되기까지')
        return [Circumscribe(self.formula, color=DATA, buff=.25)]

    # 03: 그런데 이 계산은 GPU에서 어떻게 실행될까요?
    def anim_question(self):
        return [self.formula.animate.move_to(UP * FORMULA_Y)]

    # 04: 먼저 데이터를 펼쳐 보겠습니다.
    def anim_data(self):
        self.heading_to('01  /  수식이 다루는 데이터')
        self.cells = data_row(INPUT).move_to(UP * ARRAY_Y)
        self.indices = VGroup(*[label(f'x{i}', 20, MUTED).next_to(c, DOWN, buff=.2)
                                for i,c in enumerate(self.cells)])
        self.track(self.cells, self.indices)
        return [LaggedStart(*[FadeIn(c, shift=UP*.2) for c in self.cells], lag_ratio=.12), FadeIn(self.indices)]

    # 05: 사각형 하나가 원소 하나입니다.
    def anim_elements(self):
        return [LaggedStart(*[Indicate(c, color=DATA) for c in self.cells], lag_ratio=.3)]

    # 06: 이 데이터를 읽고, 계산하고, 결과를 쓰는 GPU 함수를 Kernel이라고 합니다.
    def anim_kernel(self):
        self.kernel = MemoryBox('KERNEL  /  모든 Thread가 실행할 작업', 7, 1.6, THREAD).move_to(DOWN*2.4)
        rule = VGroup(*[label(s, 25, THREAD) for s in ['읽기', '→', '+1', '→', '쓰기']]).arrange(RIGHT,buff=.35).move_to(DOWN*2.65)
        self.kernel.add(rule)
        self.track(self.kernel)
        return [Succession(FadeIn(self.kernel), LaggedStart(*[Indicate(rule[i]) for i in [0,2,4]],lag_ratio=.65))]

    # 07: 여기서는 Thread 하나가 원소 하나를 맡습니다.
    def anim_threads(self):
        self.heading_to('02  /  하나의 규칙, 여러 독립 작업')
        self.stage.remove(self.indices)
        self.threads = ThreadGroup().move_to(UP * THREAD_Y)
        self.links = VGroup(*[DataArrow(t.get_bottom(),c.get_top(),THREAD) for t,c in zip(self.threads,self.cells)])
        self.track(self.threads,self.links)
        return [FadeOut(self.indices), LaggedStart(*[AnimationGroup(FadeIn(t),Create(a)) for t,a in zip(self.threads,self.links)],lag_ratio=.15)]

    # 08: 같은 Kernel을 실행하지만 담당 위치는 서로 다릅니다.
    def anim_assignments(self):
        return [Succession(Indicate(self.kernel, color=THREAD), LaggedStart(*[Indicate(VGroup(t,c),color=THREAD) for t,c in zip(self.threads,self.cells)],lag_ratio=.2))]

    # 09: 3은 4가 되고, 7은 8이 됩니다.
    def anim_first_results(self):
        self.note = label('값의 대응 관계 · 입력 x는 유지',21,MUTED).move_to(DOWN*.9)
        self.track(self.note)
        return [FadeIn(self.note), self.phases(self.cells[0].change(4),self.cells[1].change(8))]

    # 10: 다른 Thread도 같은 계산을 수행합니다.
    def anim_other_results(self):
        self.plus = VGroup(*[label('+1',24,THREAD).next_to(c,DOWN,buff=.22) for c in self.cells])
        self.track(self.plus)
        return [self.phases(FadeIn(self.plus), AnimationGroup(*[c.change(v) for c,v in zip(self.cells[2:],OUTPUT[2:])]))]

    # 11: 하나의 연산이 독립적인 여러 작업으로 나뉜 것입니다.
    def anim_independent(self):
        lanes = [VGroup(t,a,c) for t,a,c in zip(self.threads,self.links,self.cells)]
        return [LaggedStart(*[Circumscribe(l,color=THREAD,buff=.13) for l in lanes],lag_ratio=.15)]

    # 12: Thread가 많아지면 여러 Thread를 하나의 Block으로 묶습니다.
    def anim_block(self):
        self.heading_to('03  /  Thread를 묶는 Block')
        self.block = GPUBlock(0)
        self.block.shared.set_opacity(0)
        old = self.stage
        self.stage = VGroup(self.block)
        return [Succession(AnimationGroup(FadeOut(old),FadeIn(self.block.threads)),
                           AnimationGroup(Create(self.block.box),FadeIn(self.block.title)))]

    # 13: 시야를 넓혀 보면 여러 Block이 있고,
    def anim_zoom(self):
        self.others = VGroup(*[GPUBlock(i) for i in range(1,4)])
        for b in self.others:
            b.shared.set_opacity(0)
        for b,p in zip(self.others,[RIGHT*BLOCK_SPACING_X,DOWN*BLOCK_SPACING_Y,RIGHT*BLOCK_SPACING_X+DOWN*BLOCK_SPACING_Y]):
            b.move_to(p)
        self.blocks = VGroup(self.block,*self.others)
        self.track(self.others)
        return [self.camera.frame.animate.set(width=ZOOM_WIDTH).move_to(self.blocks.get_center()),FadeIn(self.others)]

    # 14: 각 Block 안에 다시 여러 Thread가 있습니다.
    def anim_block_contents(self):
        return [LaggedStart(*[Indicate(b.threads,color=THREAD) for b in self.blocks],lag_ratio=.3)]

    # 15: 한 번의 Kernel 실행에서 이 Block 전체를 Grid라고 합니다.
    def anim_grid(self):
        self.heading_to('04  /  Block을 묶는 Grid')
        self.boundary = SurroundingRectangle(self.blocks,buff=.5,color=GRID)
        self.grid_title = label('GRID  /  one kernel launch',40,GRID).next_to(self.boundary,UP,buff=.35)
        self.track(self.boundary,self.grid_title)
        return [Create(self.boundary),Write(self.grid_title)]

    # 16: Thread, Block, Grid는 작업을 조직하는 계층 구조입니다.
    def anim_hierarchy(self):
        self.grid = GPUGrid().move_to(UP*.8)
        for b in self.grid.blocks:
            b.shared.set_opacity(0)
        relation = label('Thread ⊂ Block ⊂ Grid',32,GRID).move_to(DOWN*2.1)
        return [self.camera.frame.animate.set(width=FRAME_WIDTH).move_to(ORIGIN),*self.replace_stage(self.grid,relation)]

    # 17: 모든 Block이 반드시 동시에 실행되는 것은 아닙니다.
    def anim_scheduling(self):
        foot = label('논리적 작업 구조 · 동시 실행을 보장하지 않음',21,MUTED).move_to(DOWN*3)
        self.track(foot)
        return [FadeIn(foot),LaggedStart(*[Indicate(b.box,color=BLOCK) for b in self.grid.blocks],lag_ratio=.65)]

    # 18: 계산 구조 옆에는 데이터를 저장하는 구조도 있습니다.
    def anim_memory(self):
        self.heading_to('05  /  계산 구조 옆에는 저장 구조')
        self.global_mem = MemoryBox('GLOBAL MEMORY',MEMORY_W,MEMORY_H,DATA).move_to([MEMORY_X,MEMORY_Y,0])
        self.mem_block = GPUBlock(0,count=3,width=3.8,height=6).move_to([BLOCK_X,MEMORY_Y,0])
        self.mem_block.threads.move_to([BLOCK_X,1.35,0])
        # Shared Memory remains absent until its own narration, cue 26.
        shell = VGroup(self.mem_block.box,self.mem_block.title)
        return self.replace_stage(self.global_mem,shell)

    # 19: 입력과 출력은 Global Memory에 있고,
    def anim_global_memory(self):
        self.xin = data_row(INPUT,.52).arrange_in_grid(cols=2,buff=.12).move_to([MEMORY_X,INPUT_Y,0])
        self.yout = data_row(['·']*6,.52,RESULT).arrange_in_grid(cols=2,buff=.12).move_to([MEMORY_X,OUTPUT_Y,0])
        xlab = label('입력 x',23,DATA).next_to(self.xin,UP,buff=.2)
        ylab = label('출력 y',23,RESULT).next_to(self.yout,UP,buff=.2)
        self.track(self.xin,self.yout,xlab,ylab)
        return [LaggedStart(FadeIn(VGroup(self.xin,xlab)),FadeIn(VGroup(self.yout,ylab)),lag_ratio=.5)]

    # 20: Thread는 계산할 값을 Register에서 사용합니다.
    def anim_registers(self):
        self.registers = VGroup(*[DataCell('·',.6,THREAD).next_to(t,DOWN,buff=.22) for t in self.mem_block.threads])
        reg_label = label('Registers · Thread별 값',19,THREAD).move_to([BLOCK_X,REGISTER_Y,0])
        self.track(self.mem_block.threads,self.registers,reg_label)
        return [FadeIn(self.mem_block.threads),LaggedStart(*[FadeIn(r) for r in self.registers],lag_ratio=.3),Write(reg_label)]

    # 21: Thread 하나를 따라가 보겠습니다.
    def anim_follow_thread(self):
        return [Circumscribe(VGroup(self.mem_block.threads[0],self.registers[0]),color=THREAD,buff=.12)]

    # 22: 입력값 3을 읽어 Register로 가져옵니다.
    def anim_load(self):
        arrow = DataArrow(self.xin[0].get_right(),self.registers[0].get_left())
        token, travel = arrow.transfer(3)
        token.set_z_index(5)
        return {'phases': [AnimationGroup(Create(arrow),FadeIn(token)),travel,
                           AnimationGroup(self.registers[0].change(3,THREAD),FadeOut(token),FadeOut(arrow))]}

    # 23: 여기에 1을 더하면 4가 됩니다.
    def anim_compute(self):
        self.compute = label('+ 1',42,RESULT).move_to([BLOCK_X,COMPUTE_Y,0])
        self.track(self.compute)
        return [self.phases(Write(self.compute),AnimationGroup(self.registers[0].change(4),Indicate(self.compute)))]

    # 24: 계산된 4를 출력 위치에 씁니다.
    def anim_store(self):
        arrow = DataArrow(self.registers[0].get_bottom(),self.yout[0].get_right(),RESULT)
        token, travel = arrow.transfer(4,RESULT)
        token.set_z_index(5)
        return {'phases': [AnimationGroup(Create(arrow),FadeIn(token)),travel,
                           AnimationGroup(self.yout[0].change(4),FadeOut(token),FadeOut(arrow))]}

    # 25: 다른 Thread도 같은 과정을 거쳐 결과를 완성합니다.
    def anim_finish_results(self):
        return [self.phases(AnimationGroup(*[Indicate(t,color=THREAD) for t in self.mem_block.threads[1:]]),
                            LaggedStart(*[c.change(v) for c,v in zip(self.yout[1:],OUTPUT[1:])],lag_ratio=.15))]

    # 26: Block 안에는 Thread들이 함께 사용하는 Shared Memory도 있습니다.
    def anim_shared(self):
        self.track(self.mem_block.shared)
        return [Succession(FadeIn(self.mem_block.shared),Indicate(self.mem_block.shared,color=BLOCK))]

    # 27: 하지만 이 단순한 계산에서는 필요하지 않습니다.
    def anim_shared_optional(self):
        optional = label('이 예제에서는 사용하지 않음',18,BLOCK).next_to(self.mem_block.shared,UP,buff=.14)
        self.track(optional)
        return [Write(optional),self.mem_block.shared.animate.set_opacity(.45)]

    # 28: 다시 처음 수식으로 돌아가 봅시다.
    def anim_return_formula(self):
        self.heading_to('06  /  수식에서 실행까지')
        formula = label('yᵢ = xᵢ + 1',52).move_to(UP*3.6)
        words = ['수식','Kernel','Thread','Block','Grid','Memory Access','Result']
        colors = [INK,THREAD,THREAD,BLOCK,GRID,DATA,RESULT]
        self.nodes = VGroup(*[label(w,28,c).move_to([0,SUMMARY_TOP-i*SUMMARY_GAP,0]) for i,(w,c) in enumerate(zip(words,colors))])
        self.summary_arrows = VGroup(*[DataArrow(a.get_bottom(),b.get_top(),MUTED) for a,b in zip(self.nodes,self.nodes[1:])])
        return self.replace_stage(formula,self.nodes[0])

    # 29: 계산을 Kernel로 표현하고,
    def anim_summary_kernel(self):
        self.track(self.nodes[1],self.summary_arrows[0])
        return [Create(self.summary_arrows[0]),Write(self.nodes[1])]

    # 30: Thread, Block, Grid로 나눈 뒤
    def anim_summary_hierarchy(self):
        brace = Brace(VGroup(*self.nodes[2:5]),RIGHT,color=GRID)
        relation = label('포함 관계\n실행 순서 아님',20,GRID).next_to(brace,RIGHT,buff=.2)
        self.track(*self.nodes[2:5],*self.summary_arrows[1:4],brace,relation)
        return [LaggedStart(*[AnimationGroup(FadeIn(n),Create(a)) for n,a in zip(self.nodes[2:5],self.summary_arrows[1:4])],lag_ratio=.5),FadeIn(brace),FadeIn(relation)]

    # 31: 데이터를 읽고 계산해 결과를 씁니다.
    def anim_summary_memory(self):
        self.track(*self.nodes[5:],*self.summary_arrows[4:])
        return [LaggedStart(*[AnimationGroup(FadeIn(n),Create(a)) for n,a in zip(self.nodes[5:],self.summary_arrows[4:])],lag_ratio=.7)]

    # 32: 같은 수식도 작업을 어떻게 나누고
    def anim_conclusion_work(self):
        return [LaggedStart(*[Indicate(n,color=THREAD) for n in self.nodes[2:5]],lag_ratio=.4)]

    # 33: 데이터를 어떻게 배치하느냐에 따라
    def anim_conclusion_data(self):
        return [Circumscribe(self.nodes[5],color=DATA,buff=.15)]

    # 34: GPU의 실행 방식과 성능은 달라집니다. Complete map; no next-episode teaser.
    def anim_conclusion_performance(self):
        emphasis = label('작업 분할 + 데이터 배치 → 실행 방식과 성능',23,BLOCK).move_to(DOWN*4.3)
        self.track(emphasis)
        return [Write(emphasis),Indicate(self.nodes[6],color=RESULT)]

