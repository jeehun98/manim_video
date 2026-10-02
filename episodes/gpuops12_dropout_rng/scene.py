"""Mask first: the selection table connects dropout forward and backward."""
import sys
from pathlib import Path
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, BG, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt

config.disable_caching = True
XS = [-2.4, -.8, .8, 2.4]
KEEP = [1, 0, 1, 0]
RANDOM = ["0.73", "0.14", "0.91", "0.32"]


def pos(x, y):
    return np.array([x, y, 0.0])


def text(value, size=27, tint=INK, width=7.6):
    return txt(value, size, tint, width)


def color(i, masked=False):
    return ACCENT if i == 0 else (PRUNE if masked and not KEEP[i] else WEIGHT)


def dot(value, tint=ACCENT, radius=.43, size=28):
    return VGroup(Circle(radius=radius, color=tint, stroke_width=2.2,
                         fill_color=BG, fill_opacity=1),
                  text(value, size, INK, radius*1.75))


def row(values, y, masked=False, xs=XS, radius=.43):
    return VGroup(*[dot(v, color(i, masked), radius).move_to(pos(xs[i], y))
                    for i,v in enumerate(values)])


def path(points, tint=MUTED):
    obj = VMobject(stroke_color=tint, stroke_width=2, stroke_opacity=.55)
    obj.set_points_as_corners([np.array(p, dtype=float) for p in points])
    return obj


def card(title, detail, center, width=3.3, tint=SPARSE):
    frame = RoundedRectangle(width=width, height=1.25, corner_radius=.13,
                             color=tint, stroke_width=1.6, fill_color=BG, fill_opacity=1).move_to(center)
    return VGroup(frame, text(title, 21, tint, width-.15).move_to(center+UP*.4),
                  text(detail, 23, INK, width-.22).move_to(center+DOWN*.16))


class MaskTable(VGroup):
    """Binary choices are a separate, repeatedly reused visual object."""
    def __init__(self, y=.35, values=KEEP, width=6.5):
        super().__init__()
        self.cells = VGroup()
        spacing = width/4
        for i, v in enumerate(values):
            tint = ACCENT if i==0 else (GOOD if v else PRUNE)
            center = pos((i-1.5)*spacing, y)
            box = RoundedRectangle(width=spacing*.85, height=2.1, corner_radius=.1,
                                   color=tint, stroke_width=2,
                                   fill_color=BG, fill_opacity=1).move_to(center)
            bit = text(v, 40, tint, 1.0).move_to(center+UP*.55)
            meaning = text("남김" if v else "지움", 20, tint, spacing*.75).move_to(center+UP*.2)
            self.cells.add(VGroup(box, bit, meaning))
        self.caption = text("MASK = 남김 / 지움 선택표", 28, GOOD).move_to(pos(0, y+1.55))
        self.add(self.cells, self.caption)


def small_mask(center, title="Mask 선택표", values=KEEP):
    frame = RoundedRectangle(width=3.2, height=1.12, corner_radius=.12,
                             color=GOOD, stroke_width=1.7, fill_color=BG, fill_opacity=1).move_to(center)
    bits = row(values, center[1]-.12, True, [center[0]-1.05+i*.7 for i in range(4)], .26)
    return VGroup(frame, text(title, 21, GOOD, 3.0).move_to(center+UP*.34), bits)


class RecoveryBoard(VGroup):
    def __init__(self, detailed=False):
        super().__init__()
        self.source = VGroup(*[dot(v, color(i, True), .27, 24).move_to(pos(-3.25,.9-i*.6))
                               for i,v in enumerate(KEEP)])
        self.conditions = card("만든 조건", "seed S\noffset 100" if detailed else "RNG 정보",
                               pos(-3.25,-1.8), 1.6).scale(.85)
        self.result = VGroup(*[dot("?", color(i, True), .27, 24).move_to(pos(3.15,.9-i*.6))
                               for i in range(4)])
        self.upper = path([pos(-2.9,0),pos(-2.25,0),pos(-2.25,1.8),pos(3.15,1.8),pos(3.15,0)])
        self.lower = path([pos(-2.55,-1.8),pos(3.15,-1.8),pos(3.15,0)])
        self.memory = RoundedRectangle(width=3.75, height=1.4, corner_radius=.14,
                                       color=PRUNE, stroke_width=2, fill_color=PRUNE,
                                       fill_opacity=.06).move_to(pos(.15,3.35))
        self.top_hint = text("선택표를 저장",25,PRUNE,3.4).move_to(pos(.15,1.8))
        self.low_hint = text("같은 선택표를 다시 만들기",24,SPARSE,3.4).move_to(pos(.15,-1.8))
        self.meta = card("생성 조건", "seed S · offset 100" if detailed else "같은 조건을 다시 사용",
                         pos(.15,-1.8), 3.2)
        self.add(self.upper,self.lower,self.memory,self.source,self.conditions,self.result,
                 self.top_hint,self.low_hint,
                 text("GPU Memory",24,PRUNE).move_to(pos(.15,4.35)),
                 text("저장",24,PRUNE,1.5).move_to(pos(-3.25,2.65)),
                 text("재생성",24,SPARSE,1.5).move_to(pos(-3.25,-2.75)),
                 text("Forward",23,WEIGHT,1.55).move_to(pos(-3.25,1.5)),
                 text("같은 Mask",23,GOOD,1.55).move_to(pos(3.15,2.65)))


class GPUDropoutRNG(Scene):
    DURATION = 147

    def construct(self):
        self.stage=VGroup();self.heading=VGroup();self.note=VGroup()
        self.progress=Rectangle(width=.01,height=.035,fill_color=ACCENT,fill_opacity=1,
                                stroke_width=0).move_to(pos(-3.8,-7.36))
        self.add(text("GPU OPERATIONS / 12",20,MUTED).move_to(UP*7.3),
                 text("Dropout\nGPU가 기억해야 하는 선택표, Mask",29).move_to(UP*6.5),
                 Line(pos(-3.8,5.82),pos(3.8,5.82),color=MUTED,stroke_opacity=.35),self.progress)

        # 0–8: establish a named, visible mask before introducing any RNG.
        self.copy("먼저 남길 곳과 지울 곳을 선택합니다", "그 선택을 기록한 표가 Mask입니다")
        inputs=row([2,5,3,8],3.1)
        mask=MaskTable(.35)
        outputs=row([2,0,3,0],-2.35,True)
        lines=VGroup(*[path([pos(x,3.1),pos(x,-2.35)]) for x in XS])
        self.show(VGroup(lines,inputs,text("입력 x",24,WEIGHT).move_to(pos(0,4.25))))
        self.to(2.0800)
        self.reveal(mask,.5)
        self.to(4.0000)
        legend=text("1 → 남김     0 → 지움",29,GOOD).move_to(pos(0,-4.55))
        self.reveal(legend,.35)
        self.to(8.0000)

        # 8–17: the mask remains stationary while values pass through the table.
        self.copy("Mask는 입력값과 별개의 선택표입니다", "같은 위치의 입력과 Mask를 곱합니다 · 보정 전")
        self.to(8.9000)
        self.play(Indicate(mask.cells[0],color=ACCENT),Indicate(mask.cells[1],color=PRUNE),run_time=.7)
        moving=VGroup(*[v.copy() for v in inputs]);self.add_stage(moving)
        self.to(10.4750)
        self.play(*[moving[i].animate.move_to(pos(XS[i],-.2)) for i in range(4)],run_time=.85)
        self.play(*[Transform(moving[i],dot(v,color(i,True)).move_to(pos(XS[i],-.2)))
                    for i,v in enumerate([2,0,3,0])],run_time=.35)
        self.play(*[moving[i].animate.move_to(outputs[i]) for i in range(4)],run_time=.9)
        result_label=text("선택 결과: [2, 0, 3, 0]",27).move_to(pos(0,-3.8))
        self.reveal(result_label,.25)
        self.to(17.0000)

        # 17–25: retain the same mask and correct the kept outputs.
        self.copy("남긴 값은 크기를 보정합니다", "p=0.5 → ×2 · 출력의 기대값 유지")
        self.reveal(text("×2",30,GOOD).move_to(pos(0,-1.45)),.25)
        self.to(18.9556)
        self.play(*[Transform(moving[i],dot(v,color(i,True)).move_to(pos(XS[i],-2.35)))
                    for i,v in enumerate([4,0,6,0])],
                  Transform(result_label,text("Forward 출력 y = [4, 0, 6, 0]",27,WEIGHT).move_to(result_label)),
                  FadeOut(legend),run_time=.65)
        self.to(25.0000)

        # 25–32: literally keep the earlier mask object, introduce NEW gradient data.
        self.copy("이 선택표는 Forward에서 끝나지 않습니다", "Backward에서도 Forward의 Mask가 필요합니다")
        grad=row([1,2,3,4],3.1)
        self.play(FadeOut(self.stage),run_time=.2)
        self.stage=VGroup(lines,mask,grad,
                          text("새 gradient g = dL/dy",25,SPARSE).move_to(pos(0,4.25)),
                          text("Forward에서 사용한 바로 그 선택표",27,GOOD).move_to(pos(0,-3.8)))
        self.add(self.stage)
        self.play(FadeIn(self.stage),run_time=.4)
        self.to(27.4111)
        self.play(Indicate(mask,color=GOOD),run_time=.65)
        self.to(32.0000)

        # 32–43: use the SAME table to stop the SAME gradient positions.
        self.copy("Forward와 Backward는 같은 선택을 공유", "새 mask를 고르면 이전 Forward의 gradient가 아닙니다")
        grads=VGroup(*[v.copy() for v in grad]);self.add_stage(grads)
        self.to(33.0154)
        self.play(*[grads[i].animate.move_to(pos(XS[i],-.2)) for i in range(4)],run_time=.85)
        self.play(*[Transform(grads[i],dot(v,color(i,True)).move_to(pos(XS[i],-.2)))
                    for i,v in enumerate([1,0,3,0])],run_time=.35)
        self.play(*[grads[i].animate.move_to(pos(XS[i],-2.35)) for i in range(4)],run_time=.85)
        self.to(36.4846)
        self.reveal(text("같은 ×2 보정",27,GOOD).move_to(pos(0,-1.5)),.25)
        self.play(*[Transform(grads[i],dot(v,color(i,True)).move_to(pos(XS[i],-2.35)))
                    for i,v in enumerate([2,0,6,0])],run_time=.55)
        self.to(39.0231)
        self.reveal(text("input gradient = [2, 0, 6, 0]",27,SPARSE).move_to(pos(0,-4.55)),.25)
        self.to(43.0000)

        # 43–49: only after understanding the table introduce its recovery problem.
        self.copy("이 선택표를 어떻게 다시 얻을까요?", "목적은 동일한 Mask를 Backward에 전달하는 것")
        board=RecoveryBoard();self.show(board)
        self.to(44.5750)
        self.play(Indicate(board.source,color=GOOD),Indicate(board.result,color=GOOD),run_time=.7)
        self.to(49.0000)

        # 49–58: first alternative, a whole MASK crosses into GPU memory and back.
        self.copy("방법 1: 선택표 자체를 저장", "Forward에서 WRITE → Backward에서 READ")
        self.to(49.9000)
        self.store_mask(board)
        self.to(58.0000)

        # 58–64: keep the recovered mask visible while introducing the memory cost.
        self.copy("큰 선택표에는 저장·이동 비용이 생깁니다", "Mask는 입력과 같은 수의 선택을 담습니다")
        cost=VGroup(text("저장 공간",26,PRUNE).move_to(pos(-2.35,-3.5)),
                    text("WRITE",26,PRUNE).move_to(pos(0,-3.5)),
                    text("READ",26,PRUNE).move_to(pos(2.35,-3.5)))
        self.reveal(cost,.3)
        self.to(60.2000)
        self.play(Indicate(board.memory,color=PRUNE),run_time=.6)
        self.to(64.0000)

        # 64–75: second alternative creates the same bits from retained conditions.
        self.copy("방법 2: 같은 선택표를 다시 만들기", "Mask 대신 그 선택을 만든 조건을 보존")
        self.play(FadeOut(cost),run_time=.2)
        self.to(65.1000)
        self.regenerate(board)
        self.to(71.3333)
        self.reveal(text("같은 난수 → 같은 비교 → 같은 Mask",26,GOOD).move_to(pos(0,-3.7)),.25)
        self.to(75.0000)

        # 75–83: reveal the position in the random stream, not seed alone.
        self.copy("seed만 같으면 충분할까요?", "seed와 난수열의 어느 위치를 썼는지 함께 필요")
        seed=card("seed", "S",pos(0,3.5),3.2)
        counters=row([100,101,102,103],1.35)
        samples=row(RANDOM,-1.1)
        lines=VGroup(*[path([counters[i].get_center(),samples[i].get_center()]) for i in range(4)])
        self.show(VGroup(seed,text("같은 seed, 위치는?",29,SPARSE).move_to(pos(0,.2))))
        self.to(76.7778)
        self.play(FadeOut(self.stage[1]),run_time=.15)
        self.reveal(VGroup(lines,counters,
                           text("counter / offset",25,SPARSE).move_to(pos(0,2.45))),.3)
        self.to(78.6444)
        self.reveal(samples,.35)
        self.to(83.0000)

        # 83–92: full four-element reproduction, before parallel-thread details.
        self.copy("같은 조건에서 같은 선택표를 복원합니다", "같은 RNG · seed · 원소 매핑 · 난수 위치 · p")
        fwd=row(RANDOM,2.65,radius=.35)
        backward=row(RANDOM,-2.15,radius=.35)
        fm=MaskTable().scale(.55).move_to(pos(0,1.1))
        bm=MaskTable().scale(.55).move_to(pos(0,-3.75))
        ftag=text("Forward: S · 위치 100…103",24,SPARSE).move_to(pos(0,3.95))
        btag=text("Backward: S · 위치 100…103",24,SPARSE).move_to(pos(0,-.85))
        self.show(VGroup(fwd,fm,ftag,btag))
        self.to(84.7182)
        self.reveal(backward,.3)
        self.to(86.2727)
        self.reveal(bm,.4)
        self.play(Indicate(fm,color=GOOD),Indicate(bm,color=GOOD),run_time=.65)
        self.to(92.0000)

        # 92–102: compare both alternatives, now with known RNG conditions.
        self.copy("같은 선택표, 다른 보존 비용", "Mask 저장·이동 ↔ 난수와 Mask 재계산")
        board=RecoveryBoard(True);self.show(board)
        self.to(93.0000)
        self.race(board)
        self.to(98.6667)
        self.reveal(text("항상 빠른 한 가지 방법은 없습니다",26,MUTED).move_to(pos(0,-4.1)),.3)
        self.to(102.0000)

        # 102–108: GPU random generation is introduced as a way to CREATE the mask.
        self.copy("GPU에서 이 선택표를 만들려면", "많은 원소마다 난수와 남김·지움 결정이 필요")
        grid=VGroup(*[Circle(.045,color=WEIGHT,fill_color=WEIGHT,fill_opacity=.45,stroke_width=0)
                       .move_to(pos(-3.6+i*.3,4.35-j*.24)) for j in range(2) for i in range(25)])
        threads=row(["T₀","T₁","T₂","T₃"],2.75)
        numbers=row(RANDOM,.35)
        mask=MaskTable(-2.5).scale(.86)
        lines=VGroup(*[path([threads[i].get_center(),numbers[i].get_center()]) for i in range(4)])
        self.show(VGroup(lines,grid,threads))
        self.to(103.5000)
        self.reveal(numbers,.35)
        self.to(105.0000)
        self.reveal(mask,.4)
        self.to(108.0000)

        # 108–114: shared state serialization is a hypothetical limitation.
        self.copy("공유 상태 하나를 순서대로 갱신한다면?", "같은 상태를 순차 사용한다고 가정한 그림")
        threads=row(["T₀","T₁","T₂","T₃"],3.2)
        rng=card("공유 RNG 상태","한 번에 하나",pos(0,.3),2.4,PRUNE)
        lines=VGroup(*[path([t.get_center(),rng.get_center()],PRUNE) for t in threads])
        self.show(VGroup(lines,threads,rng,text("WAIT",31,PRUNE).move_to(pos(0,-2.5))))
        self.to(108.9750)
        for i in range(4):
            moving=threads[i].copy().scale(.7);self.add_stage(moving)
            self.play(MoveAlongPath(moving,lines[i]),run_time=.4)
            self.play(FadeOut(moving),run_time=.1)
        self.to(114.0000)

        # 114–123: independent counters produce samples, then the familiar mask.
        self.copy("각자 난수를 계산해 Mask를 만듭니다", "counter 기반 병렬 PRNG의 개념도 · Philox 등")
        counters=row([100,101,102,103],2.5)
        numbers=row(RANDOM,-.25)
        mask=MaskTable(-2.9).scale(.86)
        lines=VGroup(*[path([counters[i].get_center(),numbers[i].get_center()]) for i in range(4)])
        self.show(VGroup(lines,counters,
                         text("seed S · 서로 다른 위치",27,SPARSE).move_to(pos(0,3.8)),
                         text("각자 RNG 계산",25,SPARSE).move_to(pos(0,1.05))))
        self.to(115.6364)
        requests=VGroup(*[v.copy() for v in counters]);self.add_stage(requests)
        self.play(*[MoveAlongPath(requests[i],lines[i]) for i in range(4)],run_time=.95)
        self.play(*[Transform(requests[i],numbers[i]) for i in range(4)],run_time=.35)
        self.to(118.5000)
        self.reveal(mask,.4)
        self.to(123.0000)

        # 123–131: a new call uses another range; its backward restores its own range.
        self.copy("다음 Forward는 새 선택을 만듭니다", "Backward는 자신과 짝인 Forward의 구간을 복원")
        first=MaskTable(2.35).scale(.72)
        second=MaskTable(-.95,[0,1,1,0]).scale(.72)
        self.show(VGroup(first,text("Forward 1 · 위치 100…103",24,SPARSE).move_to(pos(0,4.05)),
                         text("Forward 2 · 위치 104…107",24,SPARSE).move_to(pos(0,.75))))
        self.to(124.9556)
        self.reveal(second,.4)
        self.to(127.4444)
        self.reveal(card("Backward 1", "이전 구간 100…103 → 이전 Mask",pos(0,-3.5),6.8,GOOD),.3)
        self.to(131.0000)

        # 131–137: evaluation is identity for the usual inverted dropout.
        self.copy("일반적인 추론에서는 선택표가 필요 없습니다", "학습 중 보정했으므로 평가 모드에서는 입력 그대로")
        train=row([4,0,6,0],2.6,True);eval_values=row([2,5,3,8],-1.45)
        self.show(VGroup(train,eval_values,text("TRAINING",28,SPARSE).move_to(pos(0,3.8)),
                         text("Mask 선택 + 크기 보정",27,GOOD).move_to(pos(0,1.35)),
                         text("INFERENCE",28,WEIGHT).move_to(pos(0,-.2)),
                         text("[2, 5, 3, 8] → 그대로 통과",27,WEIGHT).move_to(pos(0,-3.1))))
        self.to(137.0000)

        # 137–147: the hero object is the MASK, rather than RNG or the memory diagram.
        self.copy("GPU Dropout의 중심에는 Mask가 있습니다", "무작위로 선택하고, 같은 선택을 정확히 다시 얻는다")
        hero=MaskTable(.4,width=6.8)
        fwd=card("Forward", "입력값에 선택표 적용",pos(0,3.55),6.8,WEIGHT)
        bwd=card("Backward", "gradient에 같은 선택표 적용",pos(0,-2.5),6.8,SPARSE)
        lines=VGroup(path([pos(0,2.93),pos(0,2.2)],GOOD),path([pos(0,-.7),pos(0,-1.87)],GOOD))
        self.show(VGroup(lines,hero,fwd,bwd))
        self.to(139.9091)
        self.play(Indicate(hero,color=GOOD),run_time=.7)
        self.to(143.0000)
        self.reveal(VGroup(text("선택표 저장",26,PRUNE).move_to(pos(-1.9,-4.15)),
                           text("또는",23,MUTED).move_to(pos(0,-4.15)),
                           text("선택표 재생성",26,SPARSE).move_to(pos(1.9,-4.15))),.35)
        self.to(147.0000)

    def fill_result(self,board,origins,upper=True,speed=1):
        self.play(*[v[1].animate.set_opacity(0) for v in board.result],run_time=.1*speed)
        traveling=VGroup(*[v.copy().scale(.75) for v in origins]);self.add_stage(traveling)
        moves=[MoveAlongPath(traveling[i],path([traveling[i].get_center(),pos(3.15,1.68 if upper else -1.92),
                                               board.result[i].get_center()])) for i in range(4)]
        self.play(LaggedStart(*moves,lag_ratio=.28),run_time=1.65*speed)
        self.play(FadeOut(traveling),*[Transform(board.result[i],dot(v,color(i,True),.27,24)
                                                .move_to(board.result[i])) for i,v in enumerate(KEEP)],
                  run_time=.25*speed)

    def store_mask(self,board):
        current=small_mask(pos(.15,1.8));self.add_stage(current)
        self.play(FadeOut(board.top_hint),FadeIn(current),run_time=.35)
        self.reveal(text("WRITE",21,PRUNE,1.05).move_to(pos(-2.65,3.45)),.2)
        self.play(current.animate.shift(UP*1.55),run_time=1.0)
        board.stored=current
        restored=current.copy();self.add_stage(restored)
        self.reveal(text("READ",21,PRUNE,1.0).move_to(pos(2.9,3.45)),.2)
        self.play(restored.animate.shift(DOWN*1.55),run_time=.95)
        self.fill_result(board,restored[2])
        self.reveal(text("선택표 전체를 저장·읽기",23,PRUNE,3.6).move_to(pos(.15,.75)),.2)

    def regenerate(self,board):
        condition=board.conditions.copy();self.add_stage(condition)
        self.play(FadeOut(board.low_hint),MoveAlongPath(condition,path([condition.get_center(),pos(.15,-1.8)])),
                  run_time=.8)
        self.play(Transform(condition,board.meta),run_time=.3)
        recreated=small_mask(pos(.15,-1.8),"같은 난수 다시 생성",RANDOM)
        self.stage.add(recreated)
        self.play(FadeOut(condition),FadeIn(recreated),run_time=.45)
        self.play(*[Transform(recreated[2][i],dot(v,color(i,True),.26).move_to(recreated[2][i]))
                    for i,v in enumerate(KEEP)],Transform(recreated[1],text("재생성한 Mask",21,GOOD)
                                                         .move_to(recreated[1])),run_time=.45)
        self.fill_result(board,recreated[2],False)
        self.reveal(text("같은 선택표를 재계산",23,SPARSE).move_to(pos(.15,-2.75)),.2)

    def race(self,board):
        saved=small_mask(pos(.15,1.8));conditions=board.conditions.copy();self.add_stage(saved,conditions)
        self.play(FadeOut(VGroup(board.top_hint,board.low_hint)),FadeIn(saved),run_time=.3)
        self.reveal(VGroup(text("WRITE",21,PRUNE,1.05).move_to(pos(-2.65,3.45)),
                           text("READ",21,PRUNE,1.0).move_to(pos(2.9,3.45))),.2)
        self.play(saved.animate.shift(UP*1.55),
                  MoveAlongPath(conditions,path([conditions.get_center(),pos(.15,-1.8)])),run_time=1)
        self.play(Transform(conditions,board.meta),run_time=.25)
        restored=saved.copy();self.add_stage(restored)
        recreated=small_mask(pos(.15,-1.8),"난수 재생성",RANDOM);self.stage.add(recreated)
        self.play(restored.animate.shift(DOWN*1.55),FadeOut(conditions),FadeIn(recreated),run_time=.8)
        self.play(*[Transform(recreated[2][i],dot(v,color(i,True),.26).move_to(recreated[2][i]))
                    for i,v in enumerate(KEEP)],Transform(recreated[1],text("재생성한 Mask",21,GOOD)
                                                         .move_to(recreated[1])),run_time=.4)
        self.play(*[v[1].animate.set_opacity(0) for v in board.result],run_time=.1)
        top=VGroup(*[v.copy().scale(.75) for v in restored[2]])
        low=VGroup(*[v.copy().scale(.75) for v in recreated[2]]);self.add_stage(top,low)
        a=[MoveAlongPath(top[i],path([top[i].get_center(),pos(3.15,1.68),board.result[i].get_center()])) for i in range(4)]
        b=[MoveAlongPath(low[i],path([low[i].get_center(),pos(3.15,-1.92),board.result[i].get_center()])) for i in range(4)]
        self.play(LaggedStart(*a,lag_ratio=.28),LaggedStart(*b,lag_ratio=.28),run_time=1.65)
        self.play(FadeOut(top),FadeOut(low),*[Transform(board.result[i],dot(v,color(i,True),.27,24)
                                                       .move_to(board.result[i])) for i,v in enumerate(KEEP)],run_time=.25)
        self.reveal(VGroup(text("저장 공간 + WRITE / READ",22,PRUNE,3.7).move_to(pos(.15,.75)),
                           text("RNG + Mask 재계산",22,SPARSE,3.7).move_to(pos(.15,-2.75))),.25)

    def add_stage(self,*objects):
        self.stage.add(*objects);self.add(*objects)

    def copy(self,heading,note):
        self.play(FadeOut(VGroup(self.heading,self.note)),run_time=.1)
        self.heading=text(heading,29).move_to(UP*5.12)
        self.note=text(note,22,ACCENT).move_to(DOWN*5.35)
        self.play(FadeIn(self.heading),FadeIn(self.note),run_time=.22)

    def show(self,obj):
        if len(self.stage):self.play(FadeOut(self.stage),run_time=.18)
        self.stage=obj;self.play(FadeIn(obj),run_time=.4)

    def reveal(self,obj,duration=.22):
        self.stage.add(obj);self.play(FadeIn(obj),run_time=duration)

    def to(self,target):
        remaining=target-self.time
        if remaining<-.04:raise ValueError(f"Timeline overrun at {target}: {self.time:.3f}")
        width=max(.01,7.6*target/self.DURATION)
        if remaining>0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(pos(-3.8+width/2,-7.36)),
                      run_time=min(.12,remaining))
            wait_time=target-self.time
            if wait_time>1e-6:
                self.wait(wait_time)
