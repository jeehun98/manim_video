"""Dynamic inference 03: MoE separates total and active parameters."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, WEIGHT, ZERO, pill, txt


def expert(label, color=WEIGHT, width=1.15, height=.82):
    box = RoundedRectangle(width=width, height=height, corner_radius=.12,
                           stroke_color=color, stroke_width=1.7,
                           fill_color=color, fill_opacity=.09)
    return VGroup(box, txt(label, 18, color, weight=BOLD))


def expert_row(n=8, active=(), width=.72):
    row = VGroup()
    active = set(active)
    for i in range(n):
        color = GOOD if i in active else ZERO
        e = expert(f"E{i+1}", color, width, .7)
        if i not in active:
            e.set_opacity(.42)
        row.add(e)
    row.arrange(RIGHT, buff=.13)
    return row


def dense_block(width=5.6, height=2.6, color=WEIGHT):
    frame = RoundedRectangle(width=width, height=height, corner_radius=.18,
                             stroke_color=color, stroke_width=2,
                             fill_color=color, fill_opacity=.06)
    nodes = VGroup(*[Dot(radius=.075, color=color) for _ in range(48)])
    nodes.arrange_in_grid(6, 8, buff=(.38,.25)).move_to(frame)
    return VGroup(frame, nodes, txt("DENSE FFN", 24, color, weight=BOLD))


def arrow_between(a, b, color=ACCENT, width=2.5):
    return Arrow(a.get_bottom(), b.get_top(), buff=.12, color=color,
                 stroke_width=width, tip_length=.11)


class MixtureOfExperts(Scene):
    DURATION = 96

    def construct(self):
        self.head=VGroup(); self.sub=VGroup(); self.note=VGroup()
        self.chrome=VGroup(
            txt("DYNAMIC INFERENCE  /  03",20,MUTED).move_to(UP*7.25),
            txt("모델은 커졌는데 계산량도 같은 비율로 커질까?",28).move_to(UP*6.45),
            Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress=Rectangle(width=.01,height=.035,fill_color=ACCENT,
                                fill_opacity=1,stroke_width=0).move_to([-3.8,-7.35,0])
        self.add(self.progress)

        # 0-6: enlarge one FFN.
        self.text("모델 용량을 키우는 가장 단순한 방법",
                  "Layer의 폭을 넓히고\n더 많은 Parameter를 추가합니다.",
                  "MORE PARAMETERS  →  MORE CAPACITY")
        small=dense_block(2.6,1.8).move_to([0,.35,0]); large=dense_block(5.7,3.0).move_to(small)
        p1=pill("PARAMETERS  1×",MUTED,2.7).move_to([0,-1.65,0])
        p2=pill("PARAMETERS  4×",ACCENT,2.7).move_to(p1)
        self.play(FadeIn(small),FadeIn(p1),run_time=.65)
        self.play(Transform(small,large),Transform(p1,p2),run_time=.95)
        self.keep(small,p1); self.to(5)

        # 6-12: dense input lights the whole FFN.
        self.text("Dense Layer에서는 입력이 전체 블록을 통과합니다",
                  "모델을 크게 만들면 한 Token이 거치는\nParameter와 계산도 함께 커집니다.",
                  "ONE TOKEN  →  MOST DENSE PARAMETERS ACTIVE")
        tok=pill("TOKEN",ACCENT,1.75).move_to([0,2.35,0]); block=dense_block(5.7,2.8).move_to([0,.05,0])
        enter=arrow_between(tok,block); glow=block.copy().set_color(GOOD)
        stage=VGroup(tok,block,enter)
        self.play(FadeOut(VGroup(small,p1)),FadeIn(tok),FadeIn(block),GrowArrow(enter),run_time=.8)
        self.play(FadeIn(glow),FadeOut(glow),run_time=.65)
        self.keep(stage); self.to(10)

        # 12-18: parameters and compute grow together.
        self.text("Dense에서는 두 막대가 함께 커집니다",
                  "Parameter 수를 늘릴수록\n한 Token의 활성 계산도 비슷한 방향으로 증가합니다.",
                  "PARAMETERS ↑    ACTIVE COMPUTE ↑")
        axes=VGroup(Line([-2.8,-1.7,0],[-2.8,2.1,0],color=MUTED),
                    Line([.5,-1.7,0],[.5,2.1,0],color=MUTED))
        bars=VGroup(Rectangle(width=1.55,height=3.2,fill_color=WEIGHT,fill_opacity=.55,stroke_width=0).move_to([-1.8,-.1,0]),
                    Rectangle(width=1.55,height=3.2,fill_color=ACCENT,fill_opacity=.55,stroke_width=0).move_to([1.5,-.1,0]))
        labs=VGroup(txt("PARAMETERS",18,WEIGHT).next_to(bars[0],DOWN,buff=.3),
                    txt("COMPUTE",18,ACCENT).next_to(bars[1],DOWN,buff=.3))
        chart=VGroup(axes,bars,labs)
        self.play(FadeOut(stage),GrowFromEdge(bars[0],DOWN),GrowFromEdge(bars[1],DOWN),FadeIn(axes),FadeIn(labs),run_time=.9)
        self.keep(chart); self.to(15)

        # 18-24: split the FFN into experts.
        self.text("하나의 거대한 FFN 대신 여러 Expert를 둡니다",
                  "Transformer block의 FFN sublayer를\n여러 개의 작은 신경망으로 나눕니다.",
                  "FFN  →  E₁  E₂  ···  E₈")
        giant=dense_block(5.8,2.5).move_to([0,1.15,0]); experts=expert_row(8,width=.72).move_to([0,-.8,0])
        split=VGroup(*[Arrow(giant.get_bottom(),e.get_top(),buff=.1,color=MUTED,stroke_width=1.3,tip_length=.07) for e in experts])
        moe_parts=VGroup(giant,experts,split)
        self.play(FadeOut(chart),FadeIn(giant),run_time=.55)
        self.play(FadeIn(experts),LaggedStart(*[GrowArrow(a) for a in split],lag_ratio=.04),run_time=.85)
        self.keep(moe_parts); self.to(23)

        # 24-30: all experts would still be expensive.
        self.text("모든 Expert를 실행하면 달라질 것이 없습니다",
                  "Token마다 여덟 Expert를 전부 사용하면\n모든 Parameter가 다시 계산에 참여합니다.",
                  "ALL EXPERTS ACTIVE  →  LARGE COMPUTE")
        token=pill("TOKEN",ACCENT,1.7).move_to([0,2.0,0]); all_e=expert_row(8,tuple(range(8)),.72).move_to([0,-.2,0])
        all_paths=VGroup(*[Arrow(token.get_bottom(),e.get_top(),buff=.08,color=ACCENT,stroke_width=1.5,tip_length=.07) for e in all_e])
        all_stage=VGroup(token,all_e,all_paths)
        self.play(FadeOut(moe_parts),FadeIn(token),FadeIn(all_e),run_time=.55)
        self.play(LaggedStart(*[GrowArrow(a) for a in all_paths],lag_ratio=.04),run_time=.75)
        self.keep(all_stage); self.to(27)

        # 30-37: router scores experts.
        self.text("Router가 Token별 Expert 점수를 만듭니다",
                  "현재 Token의 표현을 보고\n어느 Expert로 보낼지 점수를 계산합니다.",
                  "TOKEN  →  ROUTER  →  EXPERT SCORES")
        token2=pill("TOKEN",ACCENT,1.7).move_to([0,2.25,0]); router=pill("ROUTER",WEIGHT,2.1).move_to([0,1.0,0])
        vals=(.04,.71,.12,.09,.18,.22,.63,.07)
        score_boxes=VGroup(*[VGroup(expert(f"E{i+1}",WEIGHT,.72,.62),txt(f"{v:.2f}",15,INK).shift(DOWN*.48)) for i,v in enumerate(vals)])
        score_boxes.arrange(RIGHT,buff=.14).move_to([0,-.65,0])
        routes=VGroup(*[Arrow(router.get_bottom(),s[0].get_top(),buff=.08,color=MUTED,stroke_width=1.2,tip_length=.06) for s in score_boxes])
        routing=VGroup(token2,router,score_boxes,routes,arrow_between(token2,router))
        self.play(FadeOut(all_stage),FadeIn(token2),FadeIn(router),GrowArrow(routing[-1]),run_time=.65)
        self.play(FadeIn(score_boxes),LaggedStart(*[GrowArrow(a) for a in routes],lag_ratio=.04),run_time=.75)
        self.keep(routing); self.to(33)

        # 37-43: top-2.
        self.text("Top-2 Routing은 점수가 높은 두 개만 고릅니다",
                  "이 예시에서는 E2와 E7을 선택하고\n나머지 경로는 닫습니다.",
                  "TOP-2  →  E2 + E7")
        inactive=(0,2,3,4,5,7)
        self.play(*[score_boxes[i].animate.set_opacity(.13) for i in inactive],
                  *[routes[i].animate.set_opacity(.08) for i in inactive],
                  score_boxes[1].animate.set_color(GOOD),score_boxes[6].animate.set_color(GOOD),run_time=.85)
        top2=pill("SELECT  E2  +  E7",GOOD,3.3).move_to([0,-2.2,0])
        self.play(FadeIn(top2),run_time=.4)
        self.keep(routing,top2); self.to(39)

        # 43-50: exact Transformer sublayer path.
        self.text("이번 Token에서는 두 Expert만 실제 계산합니다",
                  "Attention 뒤 FFN 구간에서 Router가 선택하고\n결과를 합쳐 다음 Layer로 보냅니다.",
                  "ATTENTION  →  ROUTER  →  E2,E7  →  NEXT LAYER")
        attn=pill("ATTENTION",ACCENT,2.5).move_to([0,2.35,0]); r=pill("ROUTER",WEIGHT,2.0).move_to([0,1.15,0])
        e2=expert("E2",GOOD,1.5,1.0).move_to([-1.25,-.25,0]); e7=expert("E7",GOOD,1.5,1.0).move_to([1.25,-.25,0])
        nxt=pill("NEXT LAYER",ACCENT,2.8).move_to([0,-2.0,0])
        path=VGroup(arrow_between(attn,r),Arrow(r.get_bottom(),e2.get_top(),buff=.1,color=GOOD,tip_length=.1),
                    Arrow(r.get_bottom(),e7.get_top(),buff=.1,color=GOOD,tip_length=.1),
                    Arrow(e2.get_bottom(),nxt.get_top(),buff=.1,color=GOOD,tip_length=.1),
                    Arrow(e7.get_bottom(),nxt.get_top(),buff=.1,color=GOOD,tip_length=.1))
        active_path=VGroup(attn,r,e2,e7,nxt,path)
        self.play(FadeOut(VGroup(routing,top2)),FadeIn(attn),FadeIn(r),FadeIn(e2),FadeIn(e7),FadeIn(nxt),run_time=.75)
        self.play(LaggedStart(*[GrowArrow(a) for a in path],lag_ratio=.08),run_time=.8)
        self.keep(active_path); self.to(45)

        # 50-57: total versus active parameters.
        self.text("모델 크기를 두 가지로 나누어 볼 수 있습니다",
                  "전체 Expert가 가진 Total Parameters와\n현재 Token이 사용한 Active Parameters입니다.",
                  "TOTAL PARAMETERS  ≠  ACTIVE PARAMETERS")
        total=expert_row(8,(1,6),.72).move_to([0,.85,0]); total_box=SurroundingRectangle(total,color=WEIGHT,buff=.25,corner_radius=.14)
        active=VGroup(total[1].copy(),total[6].copy()).arrange(RIGHT,buff=.5).move_to([0,-1.35,0])
        active_box=SurroundingRectangle(active,color=GOOD,buff=.25,corner_radius=.14)
        labels=VGroup(txt("TOTAL: 8 EXPERTS",21,WEIGHT).next_to(total_box,UP,buff=.3),
                      txt("ACTIVE: 2 EXPERTS",21,GOOD).next_to(active_box,DOWN,buff=.3))
        counts=VGroup(total,total_box,active,active_box,labels)
        self.play(FadeOut(active_path),FadeIn(total),Create(total_box),FadeIn(labels[0]),run_time=.65)
        self.play(TransformFromCopy(VGroup(total[1],total[6]),active),Create(active_box),FadeIn(labels[1]),run_time=.75)
        self.keep(counts); self.to(53)

        # 57-66: more experts, still top-2.
        self.text("Expert를 늘려도 선택 수는 두 개로 유지할 수 있습니다",
                  "전체 모델은 4, 8, 16 Expert로 커져도\n한 Token에는 계속 Top-2를 사용할 수 있습니다.",
                  "TOTAL ↑↑    ACTIVE EXPERTS = 2")
        rows=VGroup(expert_row(4,(0,2),.9),expert_row(8,(1,6),.55),expert_row(16,(4,12),.22))
        rows.arrange(DOWN,buff=.55).move_to([0,.55,0])
        row_labels=VGroup(*[txt(t,15,MUTED).move_to([-3.25,row.get_center()[1],0])
                            for t,row in zip(("4 TOTAL","8 TOTAL","16 TOTAL"),rows)])
        active_tags=VGroup(*[txt("2 ACTIVE",15,GOOD).move_to([3.22,row.get_center()[1],0]) for row in rows])
        growing=VGroup(rows,row_labels,active_tags)
        self.play(FadeOut(counts),LaggedStart(*[FadeIn(row) for row in rows],lag_ratio=.15),FadeIn(row_labels),run_time=.9)
        self.play(FadeIn(active_tags),run_time=.5)
        self.keep(growing); self.to(59)

        # 66-74: chart the decoupling, with caveat.
        self.text("활성 계산은 전체 Parameter와 같은 비율로 늘 필요가 없습니다",
                  "Router·통신·배치 비용은 생기지만\n전체 크기와 활성 계산의 증가율을 분리할 수 있습니다.",
                  "NOT FREE  ·  ROUTING AND COMMUNICATION STILL COST")
        x0=-2.9; base=-1.5
        total_bars=VGroup(*[Rectangle(width=.75,height=h,fill_color=WEIGHT,fill_opacity=.55,stroke_width=0).move_to([x0+i*1.8,base+h/2,0]) for i,h in enumerate((.7,1.45,2.9))])
        active_bars=VGroup(*[Rectangle(width=.38,height=.55,fill_color=GOOD,fill_opacity=.8,stroke_width=0).next_to(b,RIGHT,buff=.12).align_to(b,DOWN) for b in total_bars])
        xs=VGroup(*[txt(t,17,MUTED).next_to(total_bars[i],DOWN,buff=.25) for i,t in enumerate(("4E","8E","16E"))])
        legend=VGroup(pill("TOTAL",WEIGHT,1.8),pill("ACTIVE",GOOD,1.9)).arrange(RIGHT,buff=.4).move_to([0,2.15,0])
        decouple=VGroup(total_bars,active_bars,xs,legend)
        self.play(FadeOut(growing),LaggedStart(*[GrowFromEdge(b,DOWN) for b in total_bars],lag_ratio=.12),run_time=.75)
        self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in active_bars],lag_ratio=.12),FadeIn(xs),FadeIn(legend),run_time=.65)
        self.keep(decouple); self.to(65)

        # 74-81: dense versus MoE.
        self.text("더 큰 모델이어도 일부 경로만 밝힐 수 있습니다",
                  "Dense는 큰 블록 전체가 활성화되지만\nMoE는 더 많은 Parameter 중 선택된 일부만 활성화합니다.",
                  "DENSE: ALL ACTIVE    MoE: CONDITIONAL ACTIVE")
        dense=dense_block(2.9,2.8,ACCENT).move_to([-2.0,.4,0]); moe=expert_row(8,(1,6),.58).arrange_in_grid(2,4,buff=.18).move_to([2.0,.4,0])
        compare=VGroup(dense,moe,pill("DENSE",ACCENT,1.8).next_to(dense,DOWN,buff=.4),pill("MoE",GOOD,1.7).next_to(moe,DOWN,buff=.4))
        self.play(FadeOut(decouple),FadeIn(dense),FadeIn(moe),FadeIn(compare[2:]),run_time=.85)
        self.keep(compare); self.to(72)

        # 81-88: token-dependent choices.
        self.text("Router의 선택은 Token마다 달라질 수 있습니다",
                  "같은 Expert 집합을 두고도\nToken의 표현에 따라 다른 두 경로를 고릅니다.",
                  "cat → E2,E7    car → E1,E5    tree → E3,E7")
        token_rows=VGroup()
        for word,active,color in (("cat",(1,6),GOOD),("car",(0,4),ACCENT),("tree",(2,6),PRUNE)):
            er=expert_row(8,active,.55); label=pill(word,color,1.25)
            token_rows.add(VGroup(label,er).arrange(RIGHT,buff=.45))
        token_rows.arrange(DOWN,buff=.45).move_to([0,.35,0])
        self.play(FadeOut(compare),LaggedStart(*[FadeIn(r,shift=RIGHT*.1) for r in token_rows],lag_ratio=.16),run_time=.9)
        self.keep(token_rows); self.to(76)

        # 88-95: multiple tokens and expert queues.
        self.text("한 문장 안에서도 계산 경로가 갈라집니다",
                  "각 Token은 Router를 지나\n선택된 Expert의 작업 묶음으로 이동합니다.",
                  "TOKEN-LEVEL CONDITIONAL COMPUTATION")
        words=VGroup(*[pill(w,ACCENT,1.15) for w in ("The","cat","sat","down")]).arrange(DOWN,buff=.32).move_to([-2.7,.45,0])
        router2=pill("ROUTER",WEIGHT,1.9).move_to([0,.45,0]); queues=VGroup(*[expert(f"E{i}",GOOD,1.05,.72) for i in (1,2,3,4)]).arrange(DOWN,buff=.3).move_to([2.7,.45,0])
        lines1=VGroup(*[Arrow(w.get_right(),router2.get_left(),buff=.08,color=MUTED,stroke_width=1.2,tip_length=.06) for w in words])
        lines2=VGroup(*[Arrow(router2.get_right(),q.get_left(),buff=.08,color=(GOOD if i!=1 else ACCENT),stroke_width=1.5,tip_length=.07) for i,q in enumerate(queues)])
        queues_stage=VGroup(words,router2,queues,lines1,lines2)
        self.play(FadeOut(token_rows),FadeIn(words),FadeIn(router2),FadeIn(queues),run_time=.65)
        self.play(LaggedStart(*[GrowArrow(a) for a in (*lines1,*lines2)],lag_ratio=.04),run_time=.8)
        self.keep(queues_stage); self.to(82)

        # 95-101: load imbalance.
        self.text("선택만으로 효율이 보장되지는 않습니다",
                  "특정 Expert에 Token이 몰리면\n대기열과 계산 부하가 불균형해질 수 있습니다.",
                  "LOAD IMBALANCE")
        qs=VGroup(*[expert(f"E{i+1}",WEIGHT,1.1,.8) for i in range(4)]).arrange(RIGHT,buff=.45).move_to([0,-.6,0])
        piles=VGroup()
        counts_q=(1,7,2,1)
        for q,n,c in zip(qs,counts_q,(MUTED,PRUNE,GOOD,MUTED)):
            stack=VGroup(*[Dot(radius=.1,color=c) for _ in range(n)]).arrange(UP,buff=.08).next_to(q,UP,buff=.25)
            piles.add(stack)
        imbalance=VGroup(qs,piles,pill("BOTTLENECK",PRUNE,2.4).next_to(piles[1],UP,buff=.3))
        self.play(FadeOut(queues_stage),FadeIn(qs),LaggedStart(*[FadeIn(p) for p in piles],lag_ratio=.13),run_time=.85)
        self.remove(queues_stage)
        self.play(FadeIn(imbalance[-1]),Indicate(piles[1],color=PRUNE),run_time=.6)
        self.keep(imbalance); self.to(87)

        # 101-107: conclusion.
        self.text("많이 가지고, 지금 필요한 일부만 사용합니다",
                  "MoE는 모델을 작게 만드는 대신\n큰 모델 안에서 Token별 활성 경로를 선택합니다.",
                  "TOTAL PARAMETERS  ≠  ACTIVE PARAMETERS")
        outline=RoundedRectangle(width=6.4,height=3.3,corner_radius=.25,stroke_color=WEIGHT,stroke_width=2)
        final_e=expert_row(8,(1,6),.62).arrange_in_grid(2,4,buff=.22).move_to([0,.55,0])
        formula=pill("TOTAL  ≠  ACTIVE",GOOD,4.2).move_to([0,-2.2,0])
        finale=VGroup(outline,final_e,formula)
        self.play(FadeOut(imbalance),Create(outline),LaggedStart(*[FadeIn(e) for e in final_e],lag_ratio=.06),run_time=.85)
        self.play(FadeIn(formula),run_time=.45)
        self.keep(finale); self.to(96)

    def text(self,head,sub,note):
        old=VGroup(self.head,self.note,self.sub)
        if len(old): self.play(FadeOut(old,shift=UP*.06),run_time=.14)
        self.head=txt(head,29).move_to(UP*5.15); self.note=txt(note,20,ACCENT).move_to(DOWN*4.72)
        self.sub=txt(sub,25).move_to(DOWN*6.08)
        self.play(FadeIn(self.head),FadeIn(self.note),FadeIn(self.sub),run_time=.28)
        self.add(self.chrome,self.progress); self.bring_to_front(self.chrome,self.progress,self.head,self.note,self.sub)

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
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2,-7.35,0]),run_time=min(.22,remain))
            self.wait(max(0,target-self.time))
