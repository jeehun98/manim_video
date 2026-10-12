"""Dynamic inference 02: Token Pruning reduces the sequence for later layers."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, WEIGHT, ZERO, pill, txt

ASSETS = Path(__file__).resolve().parent / "assets"


def patch_photo(name, label, size=3.7, grid=True):
    image = ImageMobject(str(ASSETS / name)).scale_to_fit_width(size)
    frame = Square(size, stroke_color=WEIGHT, stroke_width=2)
    parts = Group(image, frame)
    if grid:
        lines = VGroup()
        for k in range(1, 4):
            x = -size/2 + size*k/4
            lines.add(Line([x, -size/2, 0], [x, size/2, 0], color=INK, stroke_width=1.3))
            y = -size/2 + size*k/4
            lines.add(Line([-size/2, y, 0], [size/2, y, 0], color=INK, stroke_width=1.3))
        parts.add(lines)
    parts.add(txt(label, 18, ACCENT).next_to(frame, DOWN, buff=.17))
    return parts


def tokens(n, color=ACCENT, width=.38):
    row = VGroup()
    for i in range(n):
        box = RoundedRectangle(width=width, height=.62, corner_radius=.07,
                               stroke_color=color, stroke_width=1.2,
                               fill_color=color, fill_opacity=.1)
        row.add(VGroup(box, txt(str(i + 1), 12, color)))
    row.arrange(RIGHT, buff=.08)
    return row


def score_grid(scores):
    grid = VGroup()
    for i, score in enumerate(scores):
        color = GOOD if score >= .5 else PRUNE
        box = RoundedRectangle(width=1.05, height=.85, corner_radius=.1,
                               stroke_color=color, fill_color=color, fill_opacity=.08)
        grid.add(VGroup(box, txt(f"h{i}", 14, MUTED).move_to(box.get_center()+UP*.2),
                        txt(f"{score:.2f}", 19, color).move_to(box.get_center()+DOWN*.17)))
    grid.arrange_in_grid(4, 4, buff=.13)
    return grid


def matrix_grid(n, size, color):
    cells = VGroup(*[Square(size/n, stroke_width=.45, stroke_color=color,
                           fill_color=color, fill_opacity=.1) for _ in range(n*n)])
    cells.arrange_in_grid(n, n, buff=.018)
    return cells


def relation_graph(n, radius, color):
    pts = [radius * np.array([np.cos(TAU*i/n), np.sin(TAU*i/n), 0]) for i in range(n)]
    edges = VGroup(*[Line(pts[i], pts[j], color=color, stroke_width=.55,
                          stroke_opacity=.28) for i in range(n) for j in range(i+1, n)])
    dots = VGroup(*[Dot(p, radius=.07, color=color) for p in pts])
    return VGroup(edges, dots)


class TokenPruning(Scene):
    DURATION = 93

    def construct(self):
        self.head = VGroup(); self.sub = VGroup(); self.note = VGroup()
        self.chrome = VGroup(
            txt("DYNAMIC INFERENCE  /  02", 20, MUTED).move_to(UP*7.25),
            txt("모든 Token을 끝까지 계산해야 할까?", 31).move_to(UP*6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8,-7.35,0])
        self.add(self.progress)

        # 0-8: image patches become tokens.
        self.text("이미지를 작은 Patch로 나누면 각각 Token이 됩니다",
                  "Vision Transformer는 이미지를 일정한 격자로 나누고\n각 조각을 하나의 입력 표현으로 바꿉니다.",
                  "4 × 4 PATCHES  →  16 TOKENS")
        pic = patch_photo("cat.png", "IMAGE PATCHES", 3.55).move_to([0, 1.05, 0])
        row = tokens(16, width=.34).move_to([0, -1.65, 0])
        arrow = Arrow([0,-.95,0], [0,-1.28,0], color=ACCENT, stroke_width=3, tip_length=.12)
        self.play(FadeIn(pic, scale=.96), run_time=.65)
        self.play(GrowArrow(arrow), LaggedStart(*[FadeIn(t, shift=DOWN*.1) for t in row], lag_ratio=.035), run_time=1.0)
        self.keep(pic, row, arrow); self.to(8)

        # 8-15: all tokens stay in the sequence.
        self.text("일반적으로 모든 Token이 함께 다음 Layer로 갑니다",
                  "처음 만들어진 열여섯 Token은\n여러 Layer를 지나며 계속 계산에 참여합니다.",
                  "16  →  16  →  16  →  16")
        rows = VGroup(*[tokens(16, width=.34) for _ in range(4)])
        rows.arrange(DOWN, buff=.62).move_to([0, .45, 0])
        labels = VGroup(*[txt(f"L{i+1}", 17, MUTED).next_to(rows[i], LEFT, buff=.25) for i in range(4)])
        arrows = VGroup(*[Arrow(rows[i].get_bottom(), rows[i+1].get_top(), buff=.12,
                                color=MUTED, stroke_width=2, tip_length=.09) for i in range(3)])
        full_seq = VGroup(rows, labels, arrows)
        self.play(FadeOut(Group(pic,row,arrow)), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=.13),
                  FadeIn(labels), run_time=.9)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.12), run_time=.55)
        self.keep(full_seq); self.to(15)

        # 15-22: foreground and background carry unequal task information.
        self.text("하지만 모든 Patch가 같은 정보를 담지는 않습니다",
                  "얼굴과 몸은 분류에 직접적인 특징을 담지만\n단색 배경은 현재 판단에 덜 기여할 수 있습니다.",
                  "TASK-RELEVANT INFORMATION IS UNEVEN")
        focus = patch_photo("cat.png", "", 4.0).move_to([0,.5,0])
        focus[-1].set_opacity(0)
        hi = VGroup(*[Square(1.0, stroke_color=GOOD, stroke_width=4) for _ in range(4)])
        centers = [(-.5,1.0),(.5,1.0),(-.5,0),(.5,0)]
        for box,(x,y) in zip(hi, centers): box.move_to([x,y+.5,0])
        bg = VGroup(*[Square(1.0, stroke_color=PRUNE, stroke_width=2, fill_color=PRUNE,
                            fill_opacity=.18).move_to([-1.5+x*3, 2.0-y*3, 0])
                      for x,y in ((0,0),(1,0),(0,1),(1,1))])
        tags = VGroup(pill("FEATURE", GOOD, 2.0).move_to([0,-1.95,0]),
                      pill("BACKGROUND", PRUNE, 2.55).move_to([0,-2.75,0]))
        self.play(FadeOut(full_seq), FadeIn(focus), run_time=.65)
        self.play(FadeIn(hi), FadeIn(bg), FadeIn(tags), run_time=.75)
        self.keep(focus, hi, bg, tags); self.to(22)

        # 22-30: score intermediate representations.
        self.text("중간 표현을 이용해 중요도를 평가할 수 있습니다",
                  "중간 표현이나 Attention 등의 정보를 이용해\n이후에도 유지할 Token에 점수를 매깁니다.",
                  "hᵢ  →  IMPORTANCE SCORER  →  sᵢ")
        scores = (.92,.14,.81,.08,.73,.21,.66,.11,.18,.59,.13,.77,.06,.64,.19,.71)
        sg = score_grid(scores).move_to([0,.45,0])
        scorer = pill("SCORER", ACCENT, 2.1).move_to([0,-2.15,0])
        self.play(FadeOut(Group(focus,hi,bg,tags)), LaggedStart(*[FadeIn(c) for c in sg], lag_ratio=.035), run_time=.9)
        self.play(FadeIn(scorer), run_time=.4)
        self.keep(sg, scorer); self.to(30)

        # 30-37: top-k keeps eight tokens.
        self.text("낮은 점수의 Token은 계산 경로에서 제거합니다",
                  "방법은 다양하지만 여기서는 Top-k로\n열여섯 개 중 점수가 높은 여덟 개를 남깁니다.",
                  "TOP-k  ·  KEEP 8 / 16")
        keep_ids = [i for i,s in enumerate(scores) if s >= .5]
        drop_ids = [i for i in range(16) if i not in keep_ids]
        topk = pill("TOP-8", GOOD, 1.9).move_to([0,-2.2,0])
        self.play(FadeOut(scorer), FadeIn(topk),
                  *[sg[i].animate.set_opacity(.12).scale(.88) for i in drop_ids], run_time=.85)
        self.play(*[FadeOut(sg[i], shift=DOWN*.15) for i in drop_ids],
                  *[Indicate(sg[i], color=GOOD, scale_factor=1.03) for i in keep_ids], run_time=.8)
        self.keep(sg, topk); self.to(37)

        # 37-44: later blocks receive a shorter sequence.
        self.text("뒤쪽 Layer의 입력 자체가 짧아집니다",
                  "저장만 생략하는 것이 아니라\n이후 Transformer가 처리할 sequence를 줄입니다.",
                  "16 TOKENS  →  8 TOKENS")
        before = tokens(16, width=.34).move_to([0,1.4,0])
        after = tokens(8, GOOD, .5).move_to([0,-.55,0])
        funnel = Polygon([-3.0,.85,0],[3.0,.85,0],[1.8,.05,0],[-1.8,.05,0],
                         stroke_color=ACCENT, fill_color=ACCENT, fill_opacity=.06)
        blocks = VGroup(pill("EARLY BLOCKS", ACCENT, 2.8).next_to(before,UP,buff=.35),
                        pill("LATER BLOCKS", GOOD, 2.8).next_to(after,DOWN,buff=.4))
        shorter = VGroup(before, after, funnel, blocks)
        self.play(FadeOut(Group(sg,topk)), FadeIn(before), FadeIn(funnel), run_time=.65)
        self.play(FadeIn(after), FadeIn(blocks), run_time=.55)
        self.keep(shorter); self.to(44)

        # 44-53: N x N attention score matrix shrinks.
        self.text("Self-Attention의 score 행렬도 함께 작아집니다",
                  "QKᵀ에서 Token 수가 N이면 score 행렬은 N×N입니다.\n16에서 8로 줄면 이 부분은 256칸에서 64칸이 됩니다.",
                  "ATTENTION SCORE PART  ·  NOT TOTAL MODEL FLOPs")
        m16 = matrix_grid(16, 2.65, ACCENT).move_to([-2.0,.55,0])
        m8 = matrix_grid(8, 2.0, GOOD).move_to([2.15,.55,0])
        stats = VGroup(txt("16 × 16", 22, ACCENT).next_to(m16,UP,buff=.3),
                       txt("256 SCORES", 20, ACCENT).next_to(m16,DOWN,buff=.3),
                       txt("8 × 8", 22, GOOD).next_to(m8,UP,buff=.3),
                       txt("64 SCORES", 20, GOOD).next_to(m8,DOWN,buff=.3),
                       txt("→", 36, MUTED).move_to([.25,.55,0]))
        matrices = VGroup(m16,m8,stats)
        self.play(FadeOut(shorter), FadeIn(m16), FadeIn(stats[:2]), run_time=.7)
        self.play(FadeIn(m8), FadeIn(stats[2:]), run_time=.65)
        self.keep(matrices); self.to(53)

        # 53-61: removing one token removes its pairwise score entries.
        self.text("Token과 연결된 여러 관계가 함께 사라집니다",
                  "Token 하나를 빼면 그 표현의 계산뿐 아니라\n다른 Token과 만들던 score 항목도 제거됩니다.",
                  "REMOVE A TOKEN  →  REMOVE ITS ROW AND COLUMN")
        g12 = relation_graph(12, 1.65, ACCENT).move_to([-2.0,.45,0])
        g6 = relation_graph(6, 1.35, GOOD).move_to([2.15,.45,0])
        rel_labels = VGroup(pill("DENSE RELATIONS", ACCENT, 2.85).next_to(g12,DOWN,buff=.45),
                            pill("FEWER RELATIONS", GOOD, 2.85).next_to(g6,DOWN,buff=.45))
        graphs = VGroup(g12,g6,rel_labels)
        self.play(FadeOut(matrices), FadeIn(g12), run_time=.65)
        self.play(TransformFromCopy(g12[1][:6], g6[1]), FadeIn(g6[0]), FadeIn(rel_labels), run_time=.85)
        self.keep(graphs); self.to(61)

        # 61-69: compare targets of pruning.
        self.text("Weight Pruning과 제거하는 대상이 다릅니다",
                  "Weight Pruning은 모델 파라미터를 줄이고,\nToken Pruning은 입력별 중간 표현을 줄입니다.",
                  "MODEL PARAMETERS  vs  INPUT REPRESENTATIONS")
        weight_grid = VGroup(*[Square(.45, stroke_color=WEIGHT, fill_color=WEIGHT,
                                     fill_opacity=.12) for _ in range(24)])
        weight_grid.arrange_in_grid(4,6,buff=.07).move_to([-2.0,.65,0])
        for i in (1,4,8,11,15,18,22): weight_grid[i].set_opacity(.08)
        seq = VGroup(tokens(12,width=.32), tokens(7,GOOD,width=.42)).arrange(DOWN,buff=.7).move_to([2.0,.65,0])
        compare = VGroup(weight_grid, seq,
                         pill("WEIGHTS", WEIGHT, 2.1).next_to(weight_grid,DOWN,buff=.45),
                         pill("TOKENS", GOOD, 2.0).next_to(seq,DOWN,buff=.45))
        self.play(FadeOut(graphs), FadeIn(compare), run_time=.9)
        self.keep(compare); self.to(69)

        # 69-78: different input, different surviving patches.
        self.text("남는 Token은 입력마다 달라질 수 있습니다",
                  "고양이에서는 얼굴과 몸, 자동차에서는 윤곽처럼\n같은 모델도 입력에 따라 다른 위치를 선택합니다.",
                  "SAME MODEL  ·  DIFFERENT ACTIVE TOKENS")
        cat = patch_photo("cat.png", "CAT TOKENS", 2.75).move_to([-2.0,.55,0])
        car = patch_photo("car.png", "CAR TOKENS", 2.75).move_to([2.0,.55,0])
        cat_keep = (1,2,5,6,9,10,13,14); car_keep = (4,5,6,8,9,10,12,13)
        masks = VGroup()
        for base, live in ((cat,cat_keep),(car,car_keep)):
            c = base[1].get_center(); size=2.75
            for i in range(16):
                if i not in live:
                    r,col=divmod(i,4)
                    masks.add(Square(size/4, stroke_width=0, fill_color=ZERO, fill_opacity=.72)
                              .move_to(c + [(-1.5+col)*size/4,(1.5-r)*size/4,0]))
        examples = Group(cat,car,masks)
        self.play(FadeOut(compare), FadeIn(cat), FadeIn(car), run_time=.75)
        self.play(LaggedStart(*[FadeIn(m) for m in masks], lag_ratio=.025), run_time=.75)
        self.add(self.chrome,self.progress,self.head,self.note,self.sub)
        self.bring_to_front(self.chrome,self.progress,self.head,self.note,self.sub)
        self.keep(examples); self.to(78)

        # 78-86: pruning too aggressively is irreversible downstream.
        self.text("중요한 Token까지 지우면 정보는 되돌릴 수 없습니다",
                  "배경을 줄일 때는 예측이 유지되지만\n얼굴까지 제거하면 뒤쪽 Layer가 그 정보를 사용할 수 없습니다.",
                  "MORE PRUNING  ≠  ALWAYS BETTER")
        stages = VGroup()
        for kept,label,color in ((12,"CAT 96%",GOOD),(8,"CAT 94%",ACCENT),(4,"CAT 61%",PRUNE)):
            r = tokens(kept,color,width=min(.5,4.5/kept))
            stages.add(VGroup(r,pill(label,color,1.9).next_to(r,DOWN,buff=.28)))
        stages.arrange(DOWN,buff=.65).move_to([0,.45,0])
        down_arrows = VGroup(*[Arrow(stages[i].get_bottom(), stages[i+1].get_top(), buff=.12,
                                      color=MUTED, stroke_width=2, tip_length=.09) for i in range(2)])
        self.play(FadeOut(examples), LaggedStart(*[FadeIn(s) for s in stages], lag_ratio=.18), run_time=.9)
        self.play(FadeIn(down_arrows), Indicate(stages[2], color=PRUNE), run_time=.65)
        self.keep(stages,down_arrows); self.to(86)

        # 86-93: dynamic width and Early Exit contrast.
        self.text("모든 입력 표현에 같은 계산량을 쓸 필요는 없습니다",
                  "Early Exit이 입력 전체를 멈췄다면 Token Pruning은\n필요 없어진 일부 표현만 먼저 멈춥니다.",
                  "KEEP THE USEFUL TOKENS  ·  SHRINK LATER COMPUTE")
        funnel_rows = VGroup(tokens(12,ACCENT,.35),tokens(9,ACCENT,.4),
                             tokens(6,GOOD,.48),tokens(3,GOOD,.58))
        funnel_rows.arrange(DOWN,buff=.48).move_to([0,.55,0])
        nums = VGroup(*[txt(x,18,c).next_to(r,LEFT,buff=.3) for x,c,r in
                        zip(("32","24","16","8"),(ACCENT,ACCENT,GOOD,GOOD),funnel_rows)])
        contrast = VGroup(pill("EARLY EXIT: 전체 입력 종료", PRUNE, 4.5),
                          pill("TOKEN PRUNING: 일부 표현 종료", GOOD, 4.9))
        contrast.arrange(DOWN,buff=.25).move_to([0,-2.35,0])
        finale = VGroup(funnel_rows,nums,contrast)
        self.play(FadeOut(Group(stages,down_arrows)), LaggedStart(*[FadeIn(r) for r in funnel_rows], lag_ratio=.12),
                  FadeIn(nums), run_time=.9)
        self.play(FadeIn(contrast), run_time=.55)
        self.keep(finale); self.to(93)

    def text(self, head, sub, note):
        old = VGroup(self.head,self.note,self.sub)
        if len(old): self.play(FadeOut(old,shift=UP*.06),run_time=.14)
        self.head = txt(head,29).move_to(UP*5.15)
        self.note = txt(note,20,ACCENT).move_to(DOWN*4.72)
        self.sub = txt(sub,25).move_to(DOWN*6.08)
        self.play(FadeIn(self.head),FadeIn(self.note),FadeIn(self.sub),run_time=.28)
        self.add(self.chrome,self.progress)
        self.bring_to_front(self.chrome,self.progress,self.head,self.note,self.sub)

    def keep(self,*allowed):
        roots=(self.chrome,self.progress,self.head,self.note,self.sub,*allowed); keep=set()
        for root in roots: keep.update(root.get_family())
        for mob in list(self.mobjects):
            if mob not in keep: self.remove(mob)

    def to(self,target):
        remain=target-self.time
        if remain < -.04: raise ValueError(f"Timeline overrun {target}: {self.time:.2f}")
        width=max(.01,7.6*target/self.DURATION)
        if remain>0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2,-7.35,0]),
                      run_time=min(.22,remain))
            self.wait(max(0,target-self.time))
