"""Binary decisions locate reality; entropy bounds achievable mean depth."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,INK,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info04_expected_information.content import CUES,DURATION,PROBABILITIES,DEPTHS,CODES

class ExpectedInformation(Scene):
    DURATION=DURATION
    def construct(self):
        self.stage=VGroup();self.caption=VGroup()
        self.add(txt('INFORMATION THEORY  /  04',20,MUTED).move_to(UP*7.25),txt('현실 하나를 특정하려면 몇 번 나눌까?',31).move_to(UP*6.4),Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        self.progress=Rectangle(width=.01,height=.04,stroke_width=0,fill_color=ACCENT,fill_opacity=1).move_to([-3.8,-7.35,0]);self.add(self.progress)
        captions=['8개의 같은 확률, 실제는 하나','예 / 아니오: 8 → 4 → 2 → 1','3 bits = 최적 질문 트리의 깊이 3','log₂ 8 = 3','후보 개수보다, 확률 구조','같은 깊이: 평균 2번','자주 나오는 결과를 짧은 경로에','평균 질문 수: 2 → 1.75','이 분포에서는 평균 깊이 = H(X)','일반 분포: 실제 질문 수와 구별','엔트로피: 구분에 필요한 평균 깊이의 하한','짧은 경로 → 짧은 코드']
        for i,(start,end,display,spoken) in enumerate(CUES):
            keep=i==1
            if i:self.play(FadeOut(self.caption),*([] if keep else [FadeOut(self.stage)]),run_time=.2)
            self.caption=txt(captions[i],27,INK).move_to(DOWN*5.9);self.play(FadeIn(self.caption),run_time=.2)
            if i==0:
                self.worlds=VGroup(*[self.world(s) for s in 'ABCDEFGH']).arrange_in_grid(2,4,buff=.28).move_to(UP*.4)
                title=txt('같은 확률 1/8',31,MUTED).move_to(UP*3.4)
                self.stage=VGroup(self.worlds,title);self.play(FadeIn(self.stage),run_time=.4)
            elif i==1:
                for indices,label in (((4,5,6,7),'A–D인가?'),((2,3),'A 또는 B인가?'),((1,),'A인가?')):
                    question=txt(label,33,ACCENT).move_to(DOWN*3.4);self.stage.add(question)
                    self.play(FadeIn(question),run_time=.2)
                    self.play(*[self.worlds[j].animate.set_opacity(.1) for j in indices],run_time=.45)
                    self.play(FadeOut(question),run_time=.15);self.stage.remove(question)
            elif i==2:
                tree,paths=self.balanced(8)
                self.stage=tree;self.play(FadeIn(tree),run_time=.4)
                self.highlight(paths['A'],.5)
                note=txt('어느 결과도 깊이 3',29,ACCENT).move_to(DOWN*3.4);tree.add(note);self.play(FadeIn(note),run_time=.3)
            elif i==3:
                self.stage=VGroup(txt('8 → 4 → 2 → 1',45,WEIGHT).move_to(UP*2),txt('log₂ 8 = 3',52,ACCENT).move_to(DOWN*.1),txt('가능성의 개수 → 구분의 깊이',30,GOOD).move_to(DOWN*2.5))
                self.play(FadeIn(self.stage),run_time=.4)
            elif i==4:
                bar=self.probability_bar()
                numbers=VGroup(*[txt(f'P({s}) = {p:g}',28,c) for s,p,c in zip('ABCD',PROBABILITIES,(WEIGHT,GOOD,PRUNE,ACCENT))]).arrange(DOWN,buff=.4).move_to(DOWN*.9)
                title=txt('같은 4개, 다른 무게',33,ACCENT).move_to(UP*3.6)
                self.stage=VGroup(bar,numbers,title);self.play(FadeIn(self.stage),run_time=.4)
            elif i==5:
                tree,paths=self.balanced(4);self.stage=tree;self.play(FadeIn(tree),run_time=.4)
                note=txt('모두 깊이 2 → 평균 2번',32,ACCENT).move_to(DOWN*3.1);tree.add(note);self.play(FadeIn(note),run_time=.3)
                self.highlight(paths['A'],.4)
            elif i in (6,7,8,11):
                tree,paths=self.biased(codes=i==11)
                self.stage=tree;self.play(FadeIn(tree),run_time=.4)
                if i==6:
                    self.highlight(paths['A'],.35)
                    self.highlight(paths['D'],.35)
                    note=txt('깊이: A 1 / B 2 / C 3 / D 3',28,ACCENT).move_to(DOWN*3.8)
                elif i==7:
                    note=txt('0.5×1 + 0.25×2 + 0.125×3 + 0.125×3',25,INK).move_to(DOWN*3.1)
                    result=txt('= 1.75번',39,ACCENT).move_to(DOWN*4);tree.add(result)
                elif i==8:
                    note=txt('H(X) = Σₓ p(x)[−log₂ p(x)] = 1.75',27,ACCENT).move_to(DOWN*3.5)
                    small=txt('이 예시: 깊이 = −log₂ p(x)',25,MUTED).move_to(DOWN*4.3);tree.add(small)
                else:
                    note=txt('A → 0   B → 10   C → 110   D → 111',27,ACCENT).move_to(DOWN*3.6)
                tree.add(note);self.play(FadeIn(note),run_time=.3)
            elif i==9:
                self.stage=VGroup(txt('실제 질문 횟수: 정수',34,WEIGHT).move_to(UP*3.1),txt('정보량: 실수일 수 있음',34,GOOD).move_to(UP*1.7),txt('H(X) ≤ L최적 < H(X) + 1',35,ACCENT).move_to(DOWN*.1),txt('L최적: 결과 하나를 찾는 최적 평균 질문 수',23,MUTED).move_to(DOWN*1.3),txt('여러 결과를 묶으면\n결과당 평균 깊이는 H(X)에 접근',28).move_to(DOWN*3))
                self.play(FadeIn(self.stage),run_time=.4)
            else:
                tree,paths=self.biased();tree.scale(.7).shift(UP*.8)
                headline=txt('현실 하나를 특정하는\n평균 구분의 한계',37,ACCENT).move_to(DOWN*3)
                self.stage=VGroup(tree,headline);self.play(FadeIn(self.stage),run_time=.4)
            self.to(end)
    def world(self,label):
        return VGroup(RoundedRectangle(width=1.45,height=1.2,corner_radius=.12,stroke_color=WEIGHT,fill_color=WEIGHT,fill_opacity=.1),txt(label,35,WEIGHT))
    def balanced(self,n):
        depth=3 if n==8 else 2
        group=VGroup();positions={};edges={}
        for level in range(depth+1):
            count=2**level
            for j in range(count):
                pos=np.array([7*((j+.5)/count-.5),3.4-level*1.45,0]);positions[(level,j)]=pos
                if level:
                    line=Line(positions[(level-1,j//2)],pos,color=MUTED,stroke_width=2.2);group.add(line);edges[(level,j)]=line
                if level<depth:group.add(Dot(pos,radius=.07,color=INK))
                else:
                    group.add(txt(chr(65+j),27,WEIGHT).move_to(pos+DOWN*.15))
                    if n==4:group.add(txt(f'p={PROBABILITIES[j]:g}',21,MUTED).move_to(pos+DOWN*.85))
        paths={}
        for j in range(n):
            paths[chr(65+j)]=[edges[(level,j//2**(depth-level))] for level in range(1,depth+1)]
        return group,paths
    def biased(self,codes=False):
        group=VGroup();positions={'root':np.array([0,3.4,0]),'A':np.array([-2.7,1.6,0]),'qB':np.array([1.1,1.6,0]),'B':np.array([-.8,-.2,0]),'qC':np.array([2.3,-.2,0]),'C':np.array([1.1,-2,0]),'D':np.array([3.35,-2,0])}
        edges={}
        for parent,child,mass,bit in (('root','A',.5,'0'),('root','qB',.5,'1'),('qB','B',.25,'0'),('qB','qC',.25,'1'),('qC','C',.125,'0'),('qC','D',.125,'1')):
            line=Line(positions[parent],positions[child],color=WEIGHT,stroke_width=2+7*mass);edges[child]=line;group.add(line)
            if codes:group.add(txt(bit,23,ACCENT).move_to(line.get_center()+UP*.17))
        for key,text in (('root','A인가?'),('qB','B인가?'),('qC','C인가?')):
            # Questions above branch nodes avoid covering edges.
            group.add(Dot(positions[key],radius=.08,color=INK),txt(text,22,INK).move_to(positions[key]+UP*.35+(RIGHT*.65 if key!='root' else ORIGIN)))
        for j,s in enumerate('ABCD'):
            pos=positions[s]
            group.add(txt(s,31,GOOD).move_to(pos+DOWN*.15),txt(f'p={PROBABILITIES[j]:g}',21,MUTED).move_to(pos+DOWN*.7))
        paths={'A':[edges['A']],'B':[edges['qB'],edges['B']],'C':[edges['qB'],edges['qC'],edges['C']],'D':[edges['qB'],edges['qC'],edges['D']]}
        return group,paths
    def highlight(self,lines,duration):
        for line in lines:self.play(Indicate(line,color=ACCENT,scale_factor=1),run_time=duration)
    def probability_bar(self):
        group=VGroup();left=-3.6
        for s,p,c in zip('ABCD',PROBABILITIES,(WEIGHT,GOOD,PRUNE,ACCENT)):
            width=7.2*p;box=Rectangle(width=width,height=1,stroke_width=0,fill_color=c,fill_opacity=.8).move_to([left+width/2,2,0]);group.add(box,txt(s,28,INK).move_to(box));left+=width
        return group
    def to(self,target):
        remain=target-self.time
        if remain<-.025:raise ValueError(f'Timeline overrun: {self.time} > {target}')
        width=max(.01,7.6*target/self.DURATION)
        if remain>0:self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2,-7.35,0]),run_time=min(.1,remain))
        if target-self.time>.001:self.wait(target-self.time)
