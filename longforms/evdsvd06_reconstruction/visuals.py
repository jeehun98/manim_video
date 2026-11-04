"""Actual rank-one matrices, one fixed element color scale, exact approximation errors."""
import sys,json,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT.parents[1]))
from manim import *
from longforms.evdsvd01_names.visuals import BattleScene,label,pos,SHORT,BLUE,TEAL,WHITE,MUTED,GOLD
from longforms.evdsvd03_structure.revisions.v2_153s.visuals import arr
from data import A,B,P,E1,E2,S1,S2,SB,E_COMPONENTS,S_COMPONENTS,E5,S5,MIXED,E_ERR,S_ERR,M_ERR
PURPLE='#B49AFF';ZERO='#142139';POSITIVE='#48DFCD';NEGATIVE='#BB84ED'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));CUES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))

def value_color(v):return interpolate_color(ManimColor(ZERO),ManimColor(POSITIVE if v>=0 else NEGATIVE),min(abs(float(v))/6,1))
def heat(values,width=2.7,center=ORIGIN,numbers=False,outline=MUTED):
    values=np.asarray(values);rows,cols=values.shape;cell=width/cols;height=rows*cell
    g=VGroup(Rectangle(width=width,height=height,stroke_color=outline,stroke_width=1.2,fill_color=ZERO,fill_opacity=1).move_to(center))
    for i in range(rows):
        for j in range(cols):
            p=center+pos((j-(cols-1)/2)*cell,((rows-1)/2-i)*cell)
            if abs(values[i,j])>1e-10:g.add(Square(side_length=cell,stroke_width=0,fill_color=value_color(values[i,j]),fill_opacity=1).move_to(p))
            if numbers:
                v=values[i,j];txt=str(int(round(v))) if abs(v-round(v))<1e-8 else f'{v:.2f}'
                g.add(label(txt,p[0],p[1],26 if cols==2 else 14,WHITE,width=cell*.8))
    for k in range(1,cols):g.add(Line(center+pos(-width/2+k*cell,-height/2),center+pos(-width/2+k*cell,height/2),color='#7384A1',stroke_width=.55,stroke_opacity=.35))
    for k in range(1,rows):g.add(Line(center+pos(-width/2,-height/2+k*cell),center+pos(width/2,-height/2+k*cell),color='#7384A1',stroke_width=.55,stroke_opacity=.35))
    return g
def mark_cell(center,width,i,j,n=2,color=GOLD):
    cell=width/n;return Square(side_length=cell*.96,color=color,stroke_width=3).move_to(center+pos((j-(n-1)/2)*cell,((n-1)/2-i)*cell))
def strip(values,width=6.5,center=ORIGIN):
    return heat(np.asarray(values).reshape(5,20),width=width,center=center)

class ReconstructionScene(BattleScene):
    def setup(self):
        self.spec=MANIFEST[self.INDEX];self.length=self.spec['duration_seconds']
        self.add(label('MATRIX DECOMPOSITION WORLD CUP',y=6.55 if SHORT else 3.55,size=15,color=MUTED,width=7 if SHORT else 12))
        y=5.85 if SHORT else 2.98
        self.add(label('EVD',-1.35,y,29,BLUE,2),label('VS',0,y,17,MUTED,1),label('SVD',1.35,y,29,TEAL,2),Line(pos(-3.5 if SHORT else -6.5,y-.45),pos(3.5 if SHORT else 6.5,y-.45),color=MUTED,stroke_opacity=.22))
        self.score=label('EVD  3 : 2  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3);self.add(self.score)
        self.add(label('06 / RECONSTRUCTION  ·  같은 성분 수, 다른 오차',y=-6.65 if SHORT else -3.65,size=14,color=MUTED,width=7 if SHORT else 12))
        if 1<=self.INDEX<=19:self.legend()
        self.caption=VGroup();self.caption_key=None;self.caption.add_updater(lambda m,dt:self.update_caption());self.add(self.caption);self.update_caption()
    def update_caption(self):
        t=self.spec['start']+self.time+1e-6;cue=next((c for c in CUES if c['start']<=t<c['end']),None);key=cue['start'] if cue else None
        if key==self.caption_key:return
        self.caption_key=key;self.caption.remove(*list(self.caption))
        if cue:
            words='\n'.join(textwrap.wrap(cue['caption'],27 if SHORT else 52,break_long_words=False))
            txt=label(words,y=-5.7 if SHORT else -2.98,size=22 if SHORT else 23,width=7.1 if SHORT else 12.5)
            bg=RoundedRectangle(width=7.45 if SHORT else 13,height=max(.65,txt.height+.25),corner_radius=.08,stroke_width=0,fill_color='#080F21',fill_opacity=.97).move_to(txt)
            self.caption.add(bg,txt).set_z_index(100)
    def heading(self,s,color=WHITE):
        m=label(s,y=4.25 if SHORT else 2.04,size=32,color=color,width=7 if SHORT else 12);self.add(m);return m
    def note(self,s,color=MUTED):
        m=label(s,y=-4.15 if SHORT else -2.2,size=21,color=color,width=7 if SHORT else 12);self.reveal(m,d=.2);return m
    def legend(self):
        y=-3.2 if SHORT else -1.78
        self.add(label('고정 원소 색상',-2.15,y,14,MUTED,2.3))
        for x,v in [(-.6,-6),(.5,0),(1.6,6)]:
            self.add(Square(side_length=.18,stroke_color=MUTED,stroke_width=.5,fill_color=value_color(v),fill_opacity=1).move_to(pos(x,y)),label(str(v),x+.35,y,14,MUTED,.6))
    def cards(self,method='evd',selected=None,show_values=False):
        comps=E_COMPONENTS if method=='evd' else S_COMPONENTS;color=BLUE if method=='evd' else TEAL
        g=VGroup();w=.57 if SHORT else .8;gap=.12 if SHORT else .3
        for i,c in enumerate(comps):
            x=(i-4.5)*(w+gap);p=pos(x,.2)
            item=heat(c,w,p,outline=color)
            if selected is not None and i not in selected:item.set_opacity(.17)
            g.add(item)
        if show_values:
            vals=[2]*5+[1]*5 if method=='evd' else [SB[0]]*5+[SB[1]]*5
            for i,v in enumerate(vals):
                p=g[i].get_center();g.add(label(f'{v:g}' if method=='evd' else f'{v:.2f}',p[0],1.2 if SHORT else .95,15,color,w+.1))
        return g
    def pair_grids(self,result,title,color):
        centers=[pos(-1.85,-.15),pos(1.85,-.15)] if SHORT else [pos(-3.3,-.25),pos(3.3,-.25)]
        width=2.85 if SHORT else 2.65
        grids=VGroup(heat(A,width,centers[0]),heat(result,width,centers[1],outline=color))
        names=VGroup(label('원본 · 10×10',centers[0][0],2 if SHORT else 1.25,22,MUTED,3),label(title,centers[1][0],2 if SHORT else 1.25,22,color,3.8))
        self.add(names);return grids,centers,width
    def error_bars(self,items,at_y=.7):
        g=VGroup();left=-1.5 if SHORT else -2.3;maxw=4.4 if SHORT else 7.;h=.2
        for i,(name,value,color) in enumerate(items):
            y=at_y-i*.85
            g.add(label(name,left-1.15,y,22,color,2),Rectangle(width=maxw*value/8,height=h,stroke_width=0,fill_color=color,fill_opacity=1).move_to(pos(left+maxw*value/16,y)),label(f'{value:.3f}',left+maxw*value/8+.65,y,25,color,1.2))
        return g
    def scene_0(self):
        t=label('행렬 분해\n이상형 월드컵!',y=2.4 if SHORT else 1.2,size=40);self.reveal(t);self.to(1)
        self.reveal(self.pair().move_to(pos(0,-.7)),d=.4);self.to(3);self.play(FadeOut(t),run_time=.2)
        self.reveal(label('ROUND 06 · 복원 정확도',y=2.8 if SHORT else 1.3,size=32,color=GOLD))
    def scene_1(self):
        self.heading('분해 → 성분 합성 → 원본 복원',TEAL)
        original=heat(A,2.8,pos(0,0));self.reveal(original,d=.3);self.to(1)
        components=VGroup(heat(sum(E_COMPONENTS[:5]),2.8,pos(-1.5,.3),outline=BLUE),heat(sum(E_COMPONENTS[5:]),2.8,pos(1.5,-.3),outline=PURPLE))
        self.play(FadeOut(original),FadeIn(components),run_time=.6);self.to(2)
        self.play(Transform(components,heat(A,2.8,pos(0,0))),run_time=1);self.note('모든 성분을 합치면 정확히 원본',TEAL)
    def scene_2(self):
        self.heading('일부 성분을 버리면?',GOLD);cards=self.cards();self.add(cards)
        self.to(1);self.play(Transform(cards,self.cards(selected=range(5))),run_time=.8)
        self.reveal(label('10개 중 5개만 유지',y=2.2 if SHORT else 1.25,size=32,color=GOLD));self.note('얼마나 정확하게 복원될까?')
    def scene_3(self):
        self.heading('같은 원본 · 같은 성분 수',GOLD)
        original=heat(A,1.65,pos(0,2 if SHORT else .4));self.reveal(original)
        y=-.8 if SHORT else .3;xs=[-1.85,1.85] if SHORT else [-4,4]
        self.to(3)
        for x,name,col in zip(xs,['EVD','SVD'],[BLUE,TEAL]):
            self.reveal(label(name,x,y,36,col,3),label('5 / 10',x,y-.9,40,col,3),label('?',x,y-1.8,35,MUTED,2),d=.3)
        self.to(6);self.note('A = diag(B,B,B,B,B)  ·  B = [2,3; 0,1]')
    def scene_4(self):
        self.heading('EVD · 고유성분의 합',BLUE);self.to(2)
        self.reveal(label('A = Σ λᵢ pᵢ qᵢᵀ',y=2.2 if SHORT else 1.25,size=38,color=BLUE));self.reveal(self.cards(),d=.8)
        self.note('각 항은 랭크 1  ·  qᵢᵀ: P⁻¹의 i번째 행')
    def scene_5(self):
        self.heading('큰 고윳값부터 선택하면?',BLUE);cards=self.cards(show_values=True);self.add(cards)
        self.to(2);self.play(Transform(cards,self.cards(selected=range(5),show_values=True)),run_time=.8)
        self.to(4);self.reveal(label('최적 복원?   항상 그렇지는 않다',y=-1.5 if SHORT else -.85,size=30,color=GOLD,width=7));self.note('λ = 2인 5개를 유지 · λ = 1인 5개를 제거')
    def scene_6(self):
        self.heading('고유벡터는 직교하지 않을 수 있다',BLUE)
        o=pos(.8,-.2) if SHORT else pos(.8,-.2);s=.85
        self.add(Line(o+LEFT*3.1,o+RIGHT*1.8,color=MUTED,stroke_opacity=.3),Line(o+DOWN*1.2,o+UP*1.8,color=MUTED,stroke_opacity=.3))
        self.reveal(arr(o,[1.5,0],s,BLUE,6));self.to(2);self.reveal(arr(o,[-3,1],s,PURPLE,6))
        self.note('B의 고유방향: (1,0), (−3,1)  ·  내적 −3 ≠ 0',GOLD)
    def block_sum(self,removed=False):
        xs=[-2.55,0,2.55] if SHORT else [-4.5,0,4.5];w=1.75 if SHORT else 2.1;y=.2
        a=heat(E1,w,pos(xs[0],y),True,BLUE);b=heat(E2,w,pos(xs[1],y),True,PURPLE);c=heat(E1 if removed else B,w,pos(xs[2],y),True,TEAL)
        self.add(label('큰 고윳값 성분',xs[0],1.8 if SHORT else 1.45,17,BLUE,2.3),label('다른 고유성분',xs[1],1.8 if SHORT else 1.45,17,PURPLE,2.3),label('남은 합' if removed else '원본 블록 B',xs[2],1.8 if SHORT else 1.45,17,TEAL,2.3))
        self.add(label('+',(xs[0]+xs[1])/2,y,24,MUTED,.4),label('=',(xs[1]+xs[2])/2,y,24,MUTED,.4))
        return VGroup(a,b,c),xs,w
    def scene_7(self):
        self.heading('같은 칸의 기여가 서로 상쇄',BLUE);objects,xs,w=self.block_sum();self.add(objects[0]);self.to(2);self.reveal(objects[1])
        self.to(3);self.reveal(objects[2]);self.play(*[Create(mark_cell(pos(x,.2),w,0,1)) for x in xs],run_time=.5)
        self.note('6 + (−3) = 3',GOLD)
    def scene_8(self):
        self.heading('하나를 버리면 상쇄가 깨진다',GOLD);objects,xs,w=self.block_sum();self.add(objects);self.to(1)
        self.play(objects[1].animate.set_opacity(.12),Transform(objects[2],heat(E1,w,pos(xs[2],.2),True,TEAL)),run_time=1.2)
        self.reveal(mark_cell(pos(xs[2],.2),w,0,1));self.note('음수 기여를 제거하자 3 → 6',GOLD)
    def scene_9(self):
        self.heading('큰 고윳값 ≠ 최적 복원 보장',BLUE);grids,cs,w=self.pair_grids(E5,'EVD · 5 / 10',BLUE);self.add(grids[0]);self.to(2);self.reveal(grids[1])
        self.play(*[Create(mark_cell(cs[1],w,2*i,2*i+1,10)) for i in range(5)],run_time=.6);self.note('남긴 성분이 원본보다 큰 값을 만들기도 한다',GOLD)
    def scene_10(self):
        self.heading('SVD · 랭크 1 성분의 합',TEAL);self.reveal(label('A = Σ σᵢ uᵢ vᵢᵀ',y=2.2 if SHORT else 1.25,size=38,color=TEAL))
        self.to(3);self.reveal(self.cards('svd',show_values=True),d=.8);self.note('모든 성분은 원본과 같은 10×10 행렬')
    def scene_11(self):
        self.heading('원소를 펼쳤을 때 서로 직교',TEAL)
        g1=heat(S_COMPONENTS[0],1.7,pos(-1.7,.5),outline=TEAL);g2=heat(S_COMPONENTS[5],1.7,pos(1.7,.5),outline=PURPLE);self.add(g1,g2)
        self.to(3);self.play(Transform(g1,strip(S_COMPONENTS[0],6.3 if SHORT else 5,pos(0,1 if SHORT else .65))),Transform(g2,strip(S_COMPONENTS[5],6.3 if SHORT else 5,pos(0,-.9 if SHORT else -.8))),run_time=2)
        self.reveal(label('100개 원소를 나열한 벡터',y=2.5 if SHORT else 1.65,size=21,color=MUTED));self.to(6)
        self.note('⟨uᵢvᵢᵀ, uⱼvⱼᵀ⟩F = 0  (i ≠ j)',TEAL)
        self.to(8);self.reveal(label('실제 내적 = 0',x=0 if SHORT else 4.5,y=-2.25 if SHORT else 0,size=23,color=GOLD,width=4))
    def scene_12(self):
        self.heading('제거한 성분의 σ²가 오차 기여',TEAL);cards=self.cards('svd',show_values=True);self.add(cards)
        self.to(2);self.play(Transform(cards,self.cards('svd',selected=range(9),show_values=True)),run_time=.6)
        one=label(f'1개 제거: Δ‖오차‖F² = {SB[1]**2:.3f}',y=-1.2,size=29,color=GOLD);self.reveal(one)
        self.to(4);self.play(Transform(cards,self.cards('svd',selected=range(5),show_values=True)),Transform(one,label(f'5개 제거: 5 × {SB[1]**2:.3f} = {S_ERR**2:.3f}',y=-1.2,size=28,color=GOLD)),run_time=.8)
        self.note('‖A − Aₖ‖F² = Σ (i > k) σᵢ²',TEAL)
    def scene_13(self):
        self.heading('큰 특이값부터 남기는 이유',TEAL)
        x0=-3.;w=.42 if SHORT else .6;gap=.2 if SHORT else .35
        bars=VGroup()
        for i,v in enumerate([SB[0]]*5+[SB[1]]*5):
            x=x0+i*(w+gap);height=v*.45
            bars.add(Rectangle(width=w,height=height,stroke_width=0,fill_color=TEAL if i<5 else MUTED,fill_opacity=1).move_to(pos(x,height/2)))
        if not SHORT:bars.move_to(pos(0,.3))
        self.add(bars);self.reveal(label('큰 5개 유지 → 작은 5개를 버림',y=2.3 if SHORT else 1.35,size=26,color=TEAL))
        self.to(2);self.note(f'오차²: 큰 5개 유지 {S_ERR**2:.3f}  /  작은 5개 유지 {5*SB[0]**2:.3f}',GOLD)
    def scene_14(self):
        self.heading('같은 랭크 이하에서 최소 오차',TEAL)
        bars=self.error_bars([('EVD 5',E_ERR,BLUE),('혼합 SVD 5',M_ERR,PURPLE),('상위 SVD 5',S_ERR,TEAL)],at_y=1.2 if SHORT else .9)
        self.reveal(bars[0:3],d=.5);self.to(3);self.reveal(bars[3:6],d=.5);self.to(6);self.reveal(bars[6:9],d=.5)
        self.note('min rank(X)≤k ‖A − X‖F²  ·  절단 SVD가 달성',GOLD)
        self.reveal(label('막대: 실제 후보 3개의 오차  ·  최소성은 정리의 보장',y=2.6 if SHORT else 1.5,size=17,color=MUTED,width=7 if SHORT else 12))
    def scene_15(self):
        self.heading('최적 저랭크 근사',TEAL);self.reveal(label('Aₖ = Σᵢ₌₁ᵏ σᵢ uᵢ vᵢᵀ',y=2.3 if SHORT else 1.25,size=35,color=TEAL))
        cards=self.cards('svd',selected=range(5));self.add(cards);self.play(Transform(cards,heat(S5,2.35,pos(0,-.1),outline=TEAL)),run_time=1.5)
        self.note('BEST RANK-k APPROXIMATION',TEAL)
    def scene_16(self):
        self.heading('10×10 원본 · 10개 중 5개',GOLD);self.reveal(heat(A,2.8,pos(0,.2)))
        self.to(2);self.reveal(label('EVD  5 / 10',x=-1.85 if SHORT else -4,y=-2.25 if SHORT else -.2,size=27,color=BLUE,width=3.5),label('SVD  5 / 10',x=1.85 if SHORT else 4,y=-2.25 if SHORT else -.2,size=27,color=TEAL,width=3.5))
        self.note('같은 행렬 · 같은 성분 수 · 실제 랭크 5')
    def actual_result(self,method):
        is_e=method=='evd';result=E5 if is_e else S5;color=BLUE if is_e else TEAL
        self.heading(('EVD · 큰 고윳값 5개' if is_e else 'SVD · 큰 특이값 5개'),color)
        grids,cs,w=self.pair_grids(result,('EVD' if is_e else 'SVD')+' · 5 / 10',color);self.add(grids[0])
        self.to(2);components=E_COMPONENTS if is_e else S_COMPONENTS
        partial=heat(components[0],w,cs[1],outline=color);self.reveal(partial,d=.3)
        for n in range(2,6):self.play(Transform(partial,heat(sum(components[:n]),w,cs[1],outline=color)),run_time=.4)
        self.to(4.2)
        if is_e:self.play(*[Create(mark_cell(cs[1],w,2*i,2*i+1,10)) for i in range(5)],run_time=.4)
        self.note(f'복원 오차 ‖A − A₅‖F = {E_ERR if is_e else S_ERR:.3f}',GOLD)
    def scene_17(self):self.actual_result('evd')
    def scene_18(self):self.actual_result('svd')
    def scene_19(self):
        self.heading('언제나 차이가 나는 것은 아니다',GOLD)
        bars=self.error_bars([('EVD',E_ERR,BLUE),('SVD',S_ERR,TEAL)],at_y=.7);self.add(bars)
        self.to(2);self.play(FadeOut(bars),run_time=.4)
        self.reveal(label('대칭행렬: A = QΛQᵀ',y=.7,size=37,color=BLUE),label('EVD도 같은 최적 근사 가능',y=-.4,size=31,color=TEAL))
        self.note('조건: 고윳값의 절댓값이 큰 성분부터 선택',GOLD)
    def scene_20(self):
        self.heading('일반적인 행렬에서의 차이',GOLD)
        for x,name,col,text in [(-1.9 if SHORT else -3.3,'EVD',BLUE,'큰 고윳값부터\n일반적인 최적 보장 없음'),(1.9 if SHORT else 3.3,'SVD',TEAL,'큰 특이값부터\n최적 저랭크 근사 보장')]:
            self.reveal(label(name,x,.8,42,col,3),label(text,x,-.7,23,col,3.5 if SHORT else 5),d=.3)
        self.note('기준: 같은 랭크 이하 · 원소별 제곱 오차',GOLD)
    def scene_21(self):
        self.heading('ROUND 06 · 복원 정확도',GOLD);pair=self.pair().move_to(pos(0,1 if SHORT else .1));self.reveal(pair)
        self.to(3);self.reveal(label('SVD 승!',y=-1.3 if SHORT else -1.35,size=53,color=TEAL),d=.2)
        self.play(Circumscribe(pair[2],color=TEAL),run_time=.6);self.to(4);self.note('같은 랭크 이하에서 제곱 오차가 최소',GOLD)
    def scene_22(self):
        self.heading('ROUND 06 WINNER · SVD',TEAL);score=label('EVD   3 : 2   SVD',y=.6 if SHORT else 0,size=45);self.add(score)
        self.play(Transform(score,label('EVD   3 : 3   SVD',y=.6 if SHORT else 0,size=45,color=GOLD)),Transform(self.score,label('EVD  3 : 3  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)),run_time=.6)
        self.to(3);self.reveal(label('다시 동점!',y=-1.8 if SHORT else -1.5,size=42,color=TEAL),d=.3)
