"""KV Cache: repeated projection triangle becomes diagonal plus remembered state."""
import sys
from pathlib import Path
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, MUTED, PRUNE, WEIGHT, pill, txt

WORDS = ("THE", "CAT", "IS", "SLEEPING", "ON")


def chips(labels, color=ACCENT, width=1.15):
    return VGroup(*[pill(str(x), color, width) for x in labels]).arrange(RIGHT, buff=.16)


def triangle(n=5, cell=.75, diagonal=False):
    rows = VGroup()
    for r in range(n):
        row = VGroup()
        for c in range(r+1):
            color = GOOD if r == c else PRUNE
            box = RoundedRectangle(width=cell*.82, height=cell*.82, corner_radius=.07,
                stroke_color=color, stroke_width=1.2, fill_color=color, fill_opacity=.55)
            box.move_to([c*cell, -r*cell, 0])
            if diagonal and r != c:
                box.set_opacity(0)
            row.add(box)
        rows.add(row)
    return rows.move_to(ORIGIN)


def cache_rows(n=5):
    return VGroup(*[chips((f"K{i+1}", f"V{i+1}"), GOOD, .72) for i in range(n)]).arrange(DOWN, buff=.13)


class KVCache(Scene):
    DURATION = 100

    def construct(self):
        self.chrome = VGroup(txt("NEURAL NETWORK OPTIMIZATION  /  04",18,MUTED).move_to(UP*7.25),
            txt("Attention은 어떻게 이전 계산을 재사용할까?",30).move_to(UP*6.45),
            Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        self.progress = Rectangle(width=.01,height=.035,stroke_width=0,fill_color=ACCENT,fill_opacity=1)
        self.progress.move_to([-3.8,-7.35,0])
        self.stage = VGroup(); self.copy = VGroup()
        self.add(self.chrome,self.progress)

        self.start("Token이 하나씩 늘어납니다", "지금까지의 Token을 이용해\n다음 Token을 하나씩 예측합니다.", "ONE MORE TOKEN AT EACH STEP")
        history = VGroup(*[chips(WORDS[:r+1],width=1.28).move_to([0,1.8-r*1.1,0]).align_to([-2.8,0,0],LEFT) for r in range(4)])
        self.play(LaggedStart(*[FadeIn(row,shift=RIGHT*.15) for row in history],lag_ratio=.3),run_time=2.4)
        self.finish(6,history)

        self.start("Cache가 없다면 반복이 쌓입니다", "새 Token은 하나인데, 과거 Token의\nKey와 Value도 매번 다시 만듭니다.", "한 칸 = 한 위치의 K,V 생성 / 전체 연산량 아님")
        tri=triangle(cell=.8).move_to([.35,.3,0])
        cols=VGroup(*[txt(w,14).move_to([tri[4][i].get_x(),2.65,0]) for i,w in enumerate(WORDS)])
        steps=VGroup(*[txt(f"STEP {r+1}",17,MUTED).move_to([-2.55,tri[r][0].get_y(),0]) for r in range(5)])
        self.play(FadeIn(cols),FadeIn(steps),run_time=.4)
        for row in tri: self.play(FadeIn(row),run_time=.6)
        self.finish(14,tri,cols,steps)

        self.start("같은 위치를 계속 다시 계산합니다", "THE의 K,V는 이미 만들었는데\n다음 생성 단계에서도 다시 계산합니다.", "SAME POSITION, REPEATED PROJECTIONS")
        tri=triangle(cell=.8).move_to([0,.4,0])
        col=VGroup(*[row[0] for row in tri])
        frame=SurroundingRectangle(col,color=PRUNE,buff=.13)
        label=txt("THE",26,PRUNE).next_to(frame,UP)
        self.play(FadeIn(tri),Create(frame),FadeIn(label),run_time=.5)
        for row in tri: self.play(Indicate(row[0],color=PRUNE),run_time=.45)
        self.finish(20,tri,frame,label)

        self.start("중복을 지우면 대각선만 남습니다", "각 위치의 K,V는 한 번만 계산하고 저장합니다.\n새 Token의 K,V만 추가로 만들면 됩니다.", "Attention 계산은 여전히 필요합니다")
        tri=triangle(cell=.78).move_to([-1.6,.6,0])
        saved=cache_rows().scale(.8).move_to([2.35,.55,0])
        frame=SurroundingRectangle(saved,buff=.2,color=GOOD)
        name=txt("KV CACHE",23,GOOD).next_to(frame,UP)
        self.play(FadeIn(tri),Create(frame),FadeIn(name),run_time=.5)
        for c in range(5):
            self.play(TransformFromCopy(tri[c][c],saved[c]),run_time=.4)
            duplicate=[tri[r][c] for r in range(c+1,5)]
            if duplicate:
                self.play(*[FadeOut(x,scale=.5) for x in duplicate],run_time=.4)
                for x in duplicate: x.set_opacity(0)
        self.finish(30,tri,saved,frame,name)

        self.start("남겨둔 결과가 KV Cache입니다", "대각선에는 새 계산만 남고,\n과거 결과는 각 레이어의 Cache에 남습니다.", "DIAGONAL: NEW COMPUTE  /  CACHE: PAST STATE")
        tri=triangle(cell=.73,diagonal=True).move_to([-1.9,.75,0])
        saved=cache_rows().scale(.8).move_to([2.1,.55,0])
        frame=SurroundingRectangle(saved,buff=.2,color=GOOD)
        name=txt("ONE LAYER'S CACHE",18,GOOD).next_to(frame,UP)
        self.play(FadeIn(tri),Create(frame),FadeIn(name),run_time=.5)
        for i in range(5): self.play(TransformFromCopy(tri[i][i],saved[i]),run_time=.3)
        self.finish(36,tri,saved,frame,name)

        self.start("왜 과거 결과가 그대로일까요?", "Causal Attention에서 과거는 미래를 볼 수 없습니다.\n새 Token이 붙어도 과거 표현과 K,V는 그대로입니다.", "같은 모델·prefix·위치·추론 조건을 가정")
        seq=chips(WORDS,width=1.15).move_to([0,2.15,0])
        arcs=VGroup(*[CurvedArrow(seq[i].get_bottom(),seq[j].get_bottom(),angle=-.7,
            color=MUTED,stroke_width=1.5,tip_length=.1) for i in range(1,4) for j in range(i)])
        frozen=VGroup(*[chips((f"K{i+1}",f"V{i+1}"),GOOD,.62).arrange(DOWN,buff=.14) for i in range(4)]).arrange(RIGHT,buff=.65).move_to([-.65,-.5,0])
        stable=txt("PAST STATES UNCHANGED",23,GOOD).move_to([0,-2.3,0])
        self.play(FadeIn(seq[:4]),Create(arcs),FadeIn(frozen),FadeIn(stable),run_time=.8)
        self.play(FadeIn(seq[4],shift=LEFT*.2),run_time=.5)
        forbidden=Arrow(seq[1].get_bottom()+DOWN*.7,seq[4].get_bottom()+DOWN*.7,color=PRUNE,buff=.1)
        cross=Cross(forbidden,stroke_color=PRUNE,stroke_width=3)
        self.play(GrowArrow(forbidden),Create(cross),run_time=.7)
        self.play(Indicate(frozen,color=GOOD),run_time=.7)
        self.finish(47,seq,arcs,frozen,stable,forbidden,cross)

        self.start("새 위치는 Q, K, V를 모두 계산합니다", "새 Token의 표현에서 세 가지를 만듭니다.\nQ는 지금 묻고, K,V는 이후에도 쓰입니다.", "NEW POSITION: Q_new, K_new, V_new")
        seq=chips(WORDS,width=1.15).move_to([0,2,0])
        self.play(FadeIn(seq),run_time=.4)
        self.play(FadeOut(seq[:4]),seq[4].animate.scale(1.5).move_to([0,2.5,0]),run_time=.65)
        triple=chips(("Q_new","K_new","V_new"),WEIGHT,1.8).move_to([0,.3,0])
        arrows=VGroup(*[Arrow(seq[4].get_bottom(),p.get_top(),buff=.12,color=ACCENT,tip_length=.12) for p in triple])
        labels=VGroup(txt("지금의 질문",21,ACCENT).move_to([-2,-1,0]),txt("다음 단계에도 필요한 정보",21,GOOD).move_to([1.1,-1,0]))
        self.play(FadeIn(triple),*[GrowArrow(a) for a in arrows],FadeIn(labels),run_time=.7)
        self.finish(54,seq[4],triple,arrows,labels)

        self.start("새 Query가 저장된 Key를 훑습니다", "새 K,V를 Cache 뒤에 추가합니다.\n새 Query는 과거와 현재의 Key를 비교합니다.", "Q_new × K_cachedᵀ  →  NEW ATTENTION SCORES")
        keys=chips([f"K{i}" for i in range(1,6)],WEIGHT,1.1).move_to([0,1.65,0])
        values=chips([f"V{i}" for i in range(1,6)],GOOD,1.1).move_to([0,.45,0])
        frame=SurroundingRectangle(VGroup(keys,values),buff=.2,color=GOOD)
        q=pill("Q_new",ACCENT,2).move_to([0,-2.15,0])
        self.play(FadeIn(keys[:4]),FadeIn(values[:4]),Create(frame),FadeIn(q),run_time=.5)
        self.play(FadeIn(keys[4],shift=LEFT*.2),FadeIn(values[4],shift=LEFT*.2),run_time=.65)
        beams=VGroup(*[Polygon(q.get_top(),k.get_bottom()+LEFT*.35,k.get_bottom()+RIGHT*.35,
            stroke_width=0,fill_color=ACCENT,fill_opacity=.09) for k in keys])
        self.play(LaggedStart(*[FadeIn(b) for b in beams],lag_ratio=.15),run_time=1.3)
        self.finish(63,keys,values,frame,q,beams)

        self.start("관계의 강도로 Value를 섞습니다", "새로 구한 가중치로 Value를 합칩니다.\n이 Attention 계산은 매 단계 계속 필요합니다.", "예시: SOFTMAX WEIGHTS  →  WEIGHTED SUM")
        values=chips([f"V{i}" for i in range(1,6)],GOOD,1.1).move_to([0,-.55,0])
        bars=VGroup(); numbers=VGroup()
        for i,p in enumerate((.1,.6,.1,.15,.05)):
            bar=Rectangle(width=.55,height=p*3.6,stroke_width=0,fill_color=ACCENT,fill_opacity=.75).move_to([values[i].get_x(),.1+p*1.8,0])
            bars.add(bar); numbers.add(txt(str(p),20).next_to(bar,UP,buff=.14))
        output=Dot([0,-2.55,0],radius=.25,color=ACCENT)
        label=txt("새 위치의 Attention 출력",23,ACCENT).next_to(output,DOWN,buff=.3)
        self.play(FadeIn(values),*[GrowFromEdge(b,DOWN) for b in bars],FadeIn(numbers),run_time=.8)
        self.play(*[TransformFromCopy(v,output.copy()) for v in values],run_time=1)
        self.add(output); self.play(FadeIn(label),run_time=.3)
        self.finish(70,values,bars,numbers,output,label)

        self.start("Q는 지금 쓰고, K,V는 남깁니다", "과거 Query는 그 위치의 출력을 만들었습니다.\n다음 위치에는 새 Query와 저장된 K,V가 필요합니다.", "과거 Q가 틀린 값이 된 것이 아니라, 다시 필요하지 않음")
        keys=chips([f"K{i}" for i in range(1,5)],WEIGHT,1.3).move_to([0,1.5,0])
        values=chips([f"V{i}" for i in range(1,5)],GOOD,1.3).move_to([0,.3,0])
        q=pill("Q4",ACCENT,1.7).move_to([0,-2,0])
        beam=Polygon(q.get_top(),keys.get_left()+DOWN*.4,keys.get_right()+DOWN*.4,stroke_width=0,fill_color=ACCENT,fill_opacity=.1)
        self.play(FadeIn(keys),FadeIn(values),FadeIn(q),FadeIn(beam),run_time=.6)
        self.play(FadeOut(q),FadeOut(beam),run_time=.6)
        q=pill("Q5",ACCENT,1.7).move_to([0,-2,0])
        beam=Polygon(q.get_top(),keys.get_left()+DOWN*.4,keys.get_right()+DOWN*.4,stroke_width=0,fill_color=ACCENT,fill_opacity=.1)
        self.play(FadeIn(q),FadeIn(beam),Indicate(VGroup(keys,values),color=GOOD),run_time=.8)
        self.finish(78,keys,values,q,beam)

        self.start("삼각형의 반복을 대각선으로 바꿉니다", "Cache가 줄이는 것은 과거 K,V의 재계산입니다.\n대신 기억해둘 데이터가 필요합니다.", "REPEATED PROJECTIONS ↓  /  STORED STATE ↑")
        full=triangle(cell=.58).move_to([-2,.7,0]); diag=triangle(cell=.58,diagonal=True).move_to([2,.7,0])
        labels=VGroup(txt("NO CACHE",23,PRUNE).next_to(full,UP),txt("KV CACHE",23,GOOD).next_to(diag,UP))
        memory=chips(("K1 V1","K2 V2","…","K5 V5"),GOOD,.85).move_to([1.7,-1.8,0])
        plus=txt("+ 저장",22,GOOD).move_to([2,-1.05,0])
        self.play(FadeIn(full),FadeIn(diag),FadeIn(labels),run_time=.6)
        self.play(FadeIn(memory),FadeIn(plus),run_time=.5)
        self.finish(85,full,diag,labels,memory,plus)

        self.start("길어진 Cache도 계속 읽어야 합니다", "전체 문맥을 보관하면 Cache도 계속 커집니다.\n새 Query가 읽어야 하는 K,V도 많아집니다.", "FULL-CONTEXT CACHE: MEMORY + READ COST")
        first=cache_rows().move_to([1.8,.65,0]); name=txt("GROWING KV CACHE",23,GOOD).move_to([1.4,3.15,0])
        self.play(FadeIn(first),FadeIn(name),run_time=.5)
        bank=VGroup(*[VGroup(RoundedRectangle(width=.64,height=.3,corner_radius=.04,stroke_color=GOOD,
            stroke_width=.8,fill_color=GOOD,fill_opacity=.18),txt("K V",10,GOOD)).move_to([.5+c*.82,2.4-r*.4,0]) for c in range(4) for r in range(12)])
        self.play(first.animate.scale(.32).move_to([1.25,2.45,0]),run_time=.65)
        self.play(FadeOut(first),LaggedStart(*[FadeIn(b) for b in bank],lag_ratio=.02),run_time=1.4)
        q=pill("Q_new",ACCENT,1.7).move_to([-2.2,.35,0])
        sweep=Rectangle(width=.7,height=4.9,stroke_width=0,fill_color=ACCENT,fill_opacity=.13).move_to([.5,.3,0])
        self.play(FadeIn(q),FadeIn(sweep),run_time=.3)
        self.play(sweep.animate.shift(RIGHT*2.46),run_time=1.5)
        self.finish(94,bank,name,q,sweep)

        self.start("계산을 아끼는 대신 상태를 기억합니다", "이미 만든 K,V는 저장해서 다시 사용합니다.\n계산과 메모리 사이의 교환입니다.", "COMPUTE ONCE  →  STORE  →  REUSE")
        diag=triangle(cell=.63,diagonal=True).move_to([-1.75,.55,0])
        saved=cache_rows().scale(.8).move_to([2,.55,0]); frame=SurroundingRectangle(saved,buff=.2,color=GOOD)
        name=txt("KV CACHE",23,GOOD).next_to(frame,UP)
        trade=txt("재계산 ↓     저장 상태 ↑",32,ACCENT).move_to([0,-2.4,0])
        self.play(FadeIn(diag),FadeIn(saved),Create(frame),FadeIn(name),run_time=.6)
        self.play(FadeIn(trade),run_time=.4)
        self.finish(100,diag,saved,frame,name,trade)

    def start(self,head,sub,note):
        old=VGroup(self.stage,self.copy)
        if self.time>0: self.play(FadeOut(old),run_time=.2)
        self.remove(old,self.stage,self.copy)
        self.copy=VGroup(txt(head,29).move_to(UP*5.15),txt(sub,25).move_to(DOWN*6.08),txt(note,18,ACCENT).move_to(DOWN*4.72))
        self.play(FadeIn(self.copy),run_time=.3)

    def finish(self,target,*parts):
        self.stage=VGroup(*parts)
        self.add(self.stage,self.chrome,self.progress,self.copy)
        allowed=set()
        for root in (self.stage,self.chrome,self.progress,self.copy): allowed.update(root.get_family())
        for mob in list(self.mobjects):
            if mob not in allowed: self.remove(mob)
        remaining=target-self.time
        if remaining<-.04: raise ValueError(f"Timeline overrun at {target}: {self.time}")
        width=max(.01,7.6*target/self.DURATION)
        if remaining>0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2,-7.35,0]),run_time=min(.2,remaining))
            self.wait(max(0,target-self.time))
