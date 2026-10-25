"""Finale: same signed map, nonnegative SVD, declared separate examples and final questions."""
import sys,json,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT.parents[1]))
from manim import *
from longforms.evdsvd01_names.visuals import BattleScene,label,pos,SHORT,BLUE,TEAL,WHITE,MUTED,GOLD
from longforms.evdsvd03_structure.revisions.v2_153s.visuals import arr,grid
from data import A,U,SIGMA,V,LOSS,ORIGINAL,APPROX,COMPONENTS,ERROR,RESULTS
ORANGE='#FFB066';PURPLE='#B49AFF';LOST='#FF7688'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));CUES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
def axes(o,s,b=(-2.5,2.5,-1.4,1.4)):
    return VGroup(grid(o,s,bounds=b),Line(o+pos(b[0]*s,0),o+pos(b[1]*s,0),color=MUTED,stroke_opacity=.4),Line(o+pos(0,b[2]*s),o+pos(0,b[3]*s),color=MUTED,stroke_opacity=.4))
def world():
    o=pos(0,-.3);s=1.25 if SHORT else 1.05;return dict(o=o,s=s,base=axes(o,s))
def arrow(o,x,s,color=BLUE):
    return Dot(o,radius=.02,color=color) if abs(x)<.005 else arr(o,[x,0],s,color,6)
def pair():
    ci=pos(-1.85,-.25) if SHORT else pos(-3.3,-.2);co=pos(1.8,-.25) if SHORT else pos(3.3,-.2);s=1 if SHORT else .9
    base=VGroup(axes(ci,s,(-1.3,1.3,-1.2,1.2)),axes(co,s,(-2.2,1.3,-1.2,1.2)),label('입력 방향 v₁',ci[0],2 if SHORT else 1.25,23,BLUE,3),label('출력 방향 u₁',co[0],2 if SHORT else 1.25,23,TEAL,3))
    return ci,co,s,base
def heat(values,width,center):
    n=len(values);cell=width/n;g=VGroup(Square(side_length=width,stroke_color=MUTED,stroke_width=1,fill_color='#142139',fill_opacity=1).move_to(center))
    for i in range(n):
        for j in range(n):
            v=float(values[i,j])
            if abs(v)>1e-10:
                col=interpolate_color(ManimColor('#142139'),ManimColor(TEAL if v>=0 else PURPLE),min(abs(v)/6,1))
                g.add(Square(side_length=cell,stroke_width=0,fill_color=col,fill_opacity=1).move_to(center+pos((j-(n-1)/2)*cell,((n-1)/2-i)*cell)))
    for k in range(1,n):
        g.add(Line(center+pos(-width/2+k*cell,-width/2),center+pos(-width/2+k*cell,width/2),color=MUTED,stroke_opacity=.2,stroke_width=.5),Line(center+pos(-width/2,-width/2+k*cell),center+pos(width/2,-width/2+k*cell),color=MUTED,stroke_opacity=.2,stroke_width=.5))
    return g
def trophy():
    cup=Polygon(pos(-.65,.65),pos(.65,.65),pos(.45,-.15),pos(0,-.4),pos(-.45,-.15),color=GOLD,fill_color=GOLD,fill_opacity=.17,stroke_width=3)
    handles=VGroup(ArcBetweenPoints(pos(-.65,.5),pos(-.45,-.1),angle=PI,color=GOLD),ArcBetweenPoints(pos(.45,-.1),pos(.65,.5),angle=PI,color=GOLD))
    return VGroup(cup,handles,Line(pos(0,-.4),pos(0,-.8),color=GOLD,stroke_width=4),Rectangle(width=.9,height=.17,color=GOLD,fill_color=GOLD,fill_opacity=.4).move_to(pos(0,-.88)))

class FinalChoiceScene(BattleScene):
    def setup(self):
        self.spec=MANIFEST[self.INDEX];self.length=self.spec['duration_seconds']
        self.add(label('MATRIX DECOMPOSITION WORLD CUP',y=6.55 if SHORT else 3.55,size=15,color=MUTED,width=7 if SHORT else 12))
        y=5.85 if SHORT else 2.98
        self.add(label('EVD',-1.35,y,29,BLUE,2),label('VS',0,y,17,MUTED,1),label('SVD',1.35,y,29,TEAL,2),Line(pos(-3.5 if SHORT else -6.5,y-.45),pos(3.5 if SHORT else 6.5,y-.45),color=MUTED,stroke_opacity=.22))
        if self.INDEX not in [27,28]:self.add(label('EVD  3 : 4  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3))
        self.add(label('08 / FINAL  ·  같은 행렬, 서로 다른 질문',y=-6.65 if SHORT else -3.65,size=14,color=MUTED,width=7 if SHORT else 12))
        if 3<=self.INDEX<=16 or 18<=self.INDEX<=20:
            self.chip=label('A = diag(−2, 1)',y=3.35 if SHORT else 1.55,size=18,color=MUTED,width=6);self.add(self.chip)
        # Keep the rendered family fixed: changing children during a wait can leave stale Cairo text.
        self.caption_groups=[]
        for cue in CUES:
            if cue['end']<=self.spec['start'] or cue['start']>=self.spec['end']:continue
            txt=label('\n'.join(textwrap.wrap(cue['caption'],27 if SHORT else 52,break_long_words=False)),y=-5.7 if SHORT else -2.98,size=22 if SHORT else 23,width=7.1 if SHORT else 12.5)
            bg=RoundedRectangle(width=7.45 if SHORT else 13,height=max(.65,txt.height+.25),corner_radius=.08,stroke_width=0,fill_color='#080F21',fill_opacity=.97).move_to(txt)
            group=VGroup(bg,txt).set_z_index(100)
            def active(m,dt,a=cue['start'],b=cue['end']):
                m.set_opacity(1 if a<=self.spec['start']+self.time+1e-6<b else 0)
            group.add_updater(active);active(group,0);self.add(group);self.caption_groups.append(group)
    def heading(self,s,color=WHITE):
        m=label(s,y=4.25 if SHORT else 2.08,size=32,color=color,width=7 if SHORT else 12);self.add(m);return m
    def note(self,s,color=MUTED):
        m=label(s,y=-4.15 if SHORT else -2.2,size=21,color=color,width=7 if SHORT else 12);self.reveal(m,d=.2);return m
    def branch(self):
        a=label('A',y=1.4 if SHORT else .65,size=60,color=GOLD)
        xs=[-1.85,1.85] if SHORT else [-3.3,3.3];g=VGroup(a)
        for x,name,col,question in [(xs[0],'EVD',BLUE,'고유방향의 변화'),(xs[1],'SVD',TEAL,'입력·출력의 관계')]:
            g.add(Arrow(a.get_bottom(),pos(x,-.1),buff=.2,color=col,stroke_width=2),label(name,x,-.7,size=38,color=col,width=3),label(question,x,-1.6,size=22,color=col,width=3.5 if SHORT else 5))
        return g
    def flip(self,duration=2):
        w=world();self.add(w['base']);v=arrow(w['o'],1,w['s']);ghost=v.copy().set_opacity(.22);self.add(ghost,v)
        self.play(UpdateFromAlphaFunc(v,lambda m,t:m.become(arrow(w['o'],1-3*t,w['s'],ORANGE))),run_time=duration)
        return w,v
    def svd_arrows(self,length=1):
        ci,co,s,base=pair();self.add(base,arr(ci,[1,0],s,BLUE,6));self.reveal(arr(co,[-length,0],s,TEAL,6));return ci,co,s
    def scene_0(self):
        self.reveal(label('행렬 분해\n이상형 월드컵!',y=2.4 if SHORT else 1.2,size=40));self.to(1)
        self.reveal(self.pair().move_to(pos(0,-.7)),d=.4);self.to(3);self.reveal(label('FINAL EPISODE',y=4 if SHORT else 2.25,size=28 if SHORT else 22,color=GOLD),d=.25)
    def scene_1(self):
        self.heading('일곱 번의 대결',GOLD)
        rows=VGroup()
        for i,(n,title,winner) in enumerate(RESULTS):
            y=2.75-i*.62 if SHORT else 1.35-i*.37;col=BLUE if winner=='EVD' else TEAL
            rows.add(VGroup(label(n,-2.6 if SHORT else -3,y,18,MUTED,1),label(title,0,y,21,WHITE,4),label(winner,2.6 if SHORT else 3,y,21,col,1.5)))
        self.reveal(rows,d=.8);self.to(4);self.play(FadeOut(rows),run_time=.2);self.reveal(label('EVD   3 : 4   SVD',y=.2,size=45,color=GOLD),d=.25)
    def scene_2(self):
        self.heading('SVD가 더 뛰어난 분해일까?',GOLD);self.reveal(label('EVD   3 : 4   SVD',y=.8,size=40,color=MUTED))
        self.to(2);self.reveal(label('점수만으로 답할 수 있을까?',y=-.7,size=32,color=GOLD));self.note('이번 월드컵에서 선택한 일곱 기준의 결과')
    def scene_3(self):
        self.heading('같은 행렬 · 드러나는 정보는 다르다',GOLD);self.reveal(self.branch());self.note('A = P D P⁻¹     /     A = U Σ Vᵀ')
    def scene_4(self):
        self.heading('EVD · 같은 직선 위에 남는 방향',BLUE);w=world();self.add(w['base']);self.to(2)
        self.reveal(arr(w['o'],[1,0],w['s'],BLUE,6));self.to(4);self.reveal(arr(w['o'],[0,1],w['s'],PURPLE,6));self.note('Avᵢ = λᵢvᵢ',BLUE)
    def scene_5(self):
        self.heading('두 고유방향의 배율',BLUE);w=world();self.add(w['base']);h=arrow(w['o'],1,w['s']);v=arr(w['o'],[0,1],w['s'],PURPLE,6);self.add(h,v)
        self.play(UpdateFromAlphaFunc(h,lambda m,t:m.become(arrow(w['o'],1-3*t,w['s'],ORANGE))),run_time=1.8)
        self.to(2);self.play(Indicate(v,color=PURPLE),run_time=.7);self.note('λ₁ = −2: 반전·확대    λ₂ = 1: 그대로',GOLD)
    def scene_6(self):
        self.heading('고윳값은 음수도 가능하다',BLUE);n=label('λ₁ = −2',y=.4,size=77,color=ORANGE);self.reveal(n);self.to(1);self.play(Indicate(n,color=GOLD),run_time=.7)
        self.note('같은 고유직선 · 반대 방향',ORANGE)
    def scene_7(self):
        self.heading('−2 · 반전하면서 길이 두 배',ORANGE);self.to(1);self.flip(3);self.note('(1,0) → (−2,0)  ·  회전이 아닌 고유직선 위의 반전',GOLD)
    def scene_8(self):
        self.heading('부호와 크기에 담긴 정보',BLUE)
        self.reveal(label('−',-1.8,1,90,ORANGE,3),label('2',1.8,1,90,BLUE,3))
        self.to(2);self.reveal(label('부호: 반대 방향',-1.8,-.7,27,ORANGE,3.5),label('절댓값: 길이 2배',1.8,-.7,27,BLUE,3.5));self.note('Av₁ = (−2)v₁',GOLD)
    def scene_9(self):
        self.heading('반복하면 방향도 번갈아 바뀐다',BLUE);o=pos(0,-.2);s=.38 if SHORT else .65
        self.add(Line(o-9*s*RIGHT,o+9*s*RIGHT,color=MUTED,stroke_opacity=.5))
        for x in [-8,-4,-2,0,1,2,4,8]:self.add(label(str(x),x*s,-.8,16,MUTED,.6),Line(pos(x*s,-.28),pos(x*s,-.12),color=MUTED,stroke_width=1))
        v=arrow(o,1,s);clock=label('n = 0',y=1.3,size=30,color=GOLD);self.add(v,clock)
        for n,t in [(1,3),(2,5),(3,7)]:
            self.to(t);self.play(Transform(v,arrow(o,(-2)**n,s,ORANGE)),Transform(clock,label(f'n = {n}',y=1.3,size=30,color=GOLD)),run_time=.8)
        self.note('Aⁿv₁ = (−2)ⁿv₁  ·  축척 고정',GOLD)
    def scene_10(self):
        self.heading('SVD · 서로 직교하는 입력 방향',TEAL);w=world();self.add(w['base']);self.to(2)
        self.reveal(arr(w['o'],[1,0],w['s'],BLUE,6),arr(w['o'],[0,1],w['s'],PURPLE,6))
        marker=VMobject(color=GOLD).set_points_as_corners([w['o']+RIGHT*.23,w['o']+pos(.23,.23),w['o']+UP*.23]);self.to(4);self.reveal(marker)
        self.note('이번 예시는 고유방향과 일치 · 일반적인 일치는 아님')
    def scene_11(self):
        self.heading('특이값은 길이의 배율',TEAL)
        self.reveal(label('σ₁ = 2',-1.8,.8,47,TEAL,3),label('σ₂ = 1',1.8,.8,47,PURPLE,3));self.to(2)
        self.reveal(label('Σ = diag(2, 1)',y=-.7,size=34,color=TEAL));self.note('Σ 단계의 배율  ·  전체 변환에는 U, Vᵀ도 필요',GOLD)
    def scene_12(self):
        self.heading('특이값은 항상 0 이상',TEAL);self.reveal(label('σᵢ ≥ 0',y=.3,size=73,color=TEAL),label('이번 예시: 2, 1',y=-1.3,size=26,color=MUTED))
    def scene_13(self):
        self.heading('그렇다면 반전은 표현하지 못할까?',GOLD)
        self.reveal(label('EVD  λ₁ = −2',-1.85 if SHORT else -3.3,.8,31,BLUE,3.6),label('SVD  σ₁ = 2',1.85 if SHORT else 3.3,.8,31,TEAL,3.6))
        q=label('반전 정보는 어디에?',y=-.8,size=34,color=GOLD);self.reveal(q);self.to(5);self.play(Transform(q,label('같은 변환을 정확히 표현한다',y=-.8,size=30,color=TEAL)),run_time=.3)
    def scene_14(self):
        self.heading('입력과 출력의 단위방향은 다를 수 있다',TEAL);self.svd_arrows(1);self.note('v₁ = (1,0)    /    u₁ = (−1,0)',GOLD)
    def scene_15(self):
        self.heading('같은 변환 · 다른 설명',TEAL);ci,co,s,base=pair();self.add(base,arr(ci,[1,0],s,BLUE,6));out=arr(co,[-1,0],s,TEAL,6);self.add(out)
        self.to(2);self.play(Transform(out,arr(co,[-2,0],s,TEAL,6)),run_time=1.5)
        self.note('EVD: Av₁ = (−2)v₁    /    SVD: Av₁ = 2u₁',GOLD)
    def scene_16(self):
        self.heading('최대 확대 방향 · 정보 소실 방향',TEAL);w=world();self.add(w['base']);shape=Circle(radius=w['s'],color=BLUE).move_to(w['o']);self.add(shape)
        self.play(Transform(shape,Ellipse(width=4*w['s'],height=2*w['s'],color=TEAL).move_to(w['o'])),run_time=1.8)
        self.to(3);self.play(Transform(self.chip,label('별도 예시 · 7라운드 B = diag(2, 0)',y=3.35 if SHORT else 1.55,size=18,color=LOST,width=7 if SHORT else 10)),run_time=.3)
        target=Line(w['o']-RIGHT*2*w['s'],w['o']+RIGHT*2*w['s'],color=TEAL,stroke_width=3)
        self.play(Transform(shape,target),run_time=1.8);self.note('이 B에서는 수직 입력 방향의 특이값이 0',LOST)
    def scene_17(self):
        self.heading('큰 특이값부터 남기면 최적 근사',TEAL)
        self.add(label('별도 예시 · 6라운드의 10×10 행렬',y=3.35 if SHORT else 1.55,size=18,color=MUTED,width=7 if SHORT else 10))
        centers=[pos(-1.85,-.15),pos(1.85,-.15)] if SHORT else [pos(-3.3,-.2),pos(3.3,-.2)];width=2.6
        self.add(heat(ORIGINAL,width,centers[0]),label('원본',centers[0][0],2 if SHORT else 1.2,23,MUTED,3),label('SVD · 5 / 10',centers[1][0],2 if SHORT else 1.2,23,TEAL,3))
        approximation=heat(COMPONENTS[0],width,centers[1]);self.add(approximation)
        for n in range(2,6):self.play(Transform(approximation,heat(sum(COMPONENTS[:n]),width,centers[1])),run_time=.6)
        self.note(f'rank ≤ 5 · Frobenius 오차 최소: {ERROR:.3f}',GOLD)
    def scene_18(self):
        self.heading('서로 다른 질문에 답한다',GOLD);self.reveal(self.branch());self.note('같은 A로 돌아와 무엇을 알고 싶은지 묻는다')
    def scene_19(self):
        self.heading('EVD · 고유방향에서 어떤 변화?',BLUE);self.flip(2.4);self.note('고유방향  /  부호 있는 배율',BLUE)
    def scene_20(self):
        self.heading('SVD · 입력이 어떻게 출력으로?',TEAL);self.svd_arrows(2);self.note('입력·출력 방향  /  길이와 정보의 변화',TEAL)
    def scene_21(self):
        self.heading('적용 가능한 행렬의 범위',GOLD)
        self.reveal(label('EVD',-1.85 if SHORT else -3.3,1,42,BLUE,3),label('SVD',1.85 if SHORT else 3.3,1,42,TEAL,3))
        self.reveal(label('정사각행렬\n고유기저가 충분할 때',-1.85 if SHORT else -3.3,-.5,25,BLUE,3.5 if SHORT else 5));self.to(2)
        self.reveal(label('정사각·직사각행렬\n모든 실수 행렬',1.85 if SHORT else 3.3,-.5,25,TEAL,3.5 if SHORT else 5));self.note('여기서 EVD는 A = PDP⁻¹ 형태의 대각화',GOLD)
    def scene_22(self):
        self.heading('더 넓은 적용 범위 ≠ 모든 질문의 답',GOLD);p=self.pair().move_to(pos(0,0));self.reveal(p)
        self.play(Indicate(p[2],color=TEAL),run_time=.8);self.note('EVD와 SVD는 각자 다른 정보를 직접 드러낸다')
    def scene_23(self):
        self.heading('두 분해가 알려주는 정보가 다르다',GOLD);self.reveal(self.pair().move_to(pos(0,.4)))
        self.note('EVD: 고유방향·고윳값    /    SVD: 특이방향·특이값',GOLD)
    def scene_24(self):
        self.heading('행렬 분해 월드컵 · 최종 승자는?',GOLD);self.reveal(self.pair().move_to(pos(0,.7)));self.to(1)
        self.reveal(trophy().scale(.65).move_to(pos(0,-2 if SHORT else -1.65)),d=.6)
    def scene_25(self):
        self.heading('FINAL SCORE',GOLD);n=label('EVD   3 : 4   SVD',y=.4,size=49,color=GOLD);self.reveal(n);self.to(1)
        self.play(Indicate(n,color=TEAL),run_time=.7);self.note('선정한 일곱 가지 기준의 누적 결과')
    def scene_26(self):
        self.heading('MATRIX DECOMPOSITION WORLD CUP',GOLD);cup=trophy().scale(1.1 if SHORT else .8).move_to(pos(0,1.2 if SHORT else .55));self.reveal(cup,d=.5)
        self.reveal(label('SVD',y=-.5 if SHORT else -.7,size=74,color=TEAL),label('CHAMPION',y=-1.8 if SHORT else -1.6,size=37,color=GOLD),d=.5)
        self.note('FINAL · EVD 3 : 4 SVD',GOLD)
    def scene_27(self):
        self.heading('마지막으로 남기고 싶은 질문',GOLD);self.reveal(label('A',y=.4,size=90,color=GOLD))
        self.to(3)
        for x,y,text in [(-1.9,2,'어떤 방향이 유지될까?'),(1.9,2,'어느 방향이 가장 늘어날까?'),(-1.9,-1.4,'반복하면 어떻게 될까?'),(1.9,-1.4,'어떤 정보가 사라질까?')]:
            self.reveal(label(text,x if SHORT else x*1.8,y if SHORT else y*.65,size=22,color=WHITE,width=3.6 if SHORT else 5.4),d=.25)
        self.note('우리가 알고 싶은 것은 행렬의 어떤 성질일까?',GOLD)
    def scene_28(self):
        self.heading('분해는 바로 그 질문에서 시작된다',GOLD);branch=self.branch();self.reveal(branch);self.to(3)
        self.play(FadeOut(branch),run_time=.4);self.reveal(label('무엇을 알고 싶은가?',y=.1,size=46,color=GOLD,width=7 if SHORT else 12),d=.3)
    def scene_29(self):
        self.heading('행렬 분해 이상형 월드컵',GOLD);self.reveal(self.pair().move_to(pos(0,.4)),d=.4)
        self.reveal(label('FINAL · EVD 3 : 4 SVD',y=-1.5,size=31,color=GOLD));self.note('행렬을 이해하는 두 가지 관점',WHITE);self.to(2)
