"""LA01 revised: a directed network and its receiving-row adjacency matrix."""
import os
import numpy as np
from manim import *
config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#0B1220'
BLUE,GOLD,PINK,INK,MUTED='#66D9EF','#F6CA78','#EF9DCA','#EDF2FA','#93A5BF'
COLORS=[BLUE,GOLD,PINK]
VALUES=[[0,.8,.1],[.3,0,.5],[.2,.7,0]]
DURATION=154
CAPTIONS=[
(0,'intro','행렬을 처음 보면, 그냥 숫자를\n네모 모양으로 배열한 것처럼 보입니다.'),
(6,'numbers','하지만 이 숫자들은\n단순히 나열되어 있는 것이 아닙니다.'),
(11,'objects','이번에는 행렬을 지우고,\n세 개의 대상을 놓아보겠습니다.'),
(17,'cycle','각 대상은 서로 영향을 줄 수 있습니다.\n첫 번째에서 두 번째로, 두 번째에서 세 번째로.'),
(24,'complex','세 번째에서 첫 번째로. 반대 방향도 연결하면\n그림은 금방 복잡해집니다.'),
(31,'weight','각각의 연결에\n숫자를 하나씩 붙이면 어떨까요?'),
(37,'edge08','예를 들어 두 번째 대상이\n첫 번째 대상에 주는 영향은 영 점 팔.'),
(43,'edge01','세 번째 대상이\n첫 번째 대상에 주는 영향은 영 점 일입니다.'),
(49,'convention','이제 기록하는 위치를 정하겠습니다.\n행은 받는 대상, 열은 주는 대상입니다.'),
(57,'place08','두 번째가 첫 번째에게 주는 영향은\n첫 번째 행, 두 번째 열에 놓습니다.'),
(64,'place01','세 번째가 첫 번째에게 주는 영향은\n첫 번째 행, 세 번째 열에 놓습니다.'),
(71,'fill','나머지 관계도 같은 규칙으로 정리하면,\n전체 연결 구조가 하나의 행렬이 됩니다.'),
(79,'diagonal','이 예에서 대각선은 모두 영입니다.\n자기 자신에게 주는 직접 영향은 없다고 정한 겁니다.'),
(86,'meaning','이제 숫자 하나는 단순한 숫자가 아니라,\n두 대상 사이의 관계 하나를 나타냅니다.'),
(93,'neural','이 방식은 여러 분야에 쓰입니다.\n신경망에서는 뉴런 사이의 가중치를 담을 수 있고,'),
(101,'graph','그래프에서는 노드 사이의 연결과\n그 연결의 가중치를 담을 수 있습니다.'),
(108,'probability','확률에서는 한 상태에서 다른 상태로\n이동할 가능성을 담을 수 있습니다.'),
(115,'prob_rule','이때는 확률에 맞는 별도 규칙이 필요합니다.\n열을 출발 상태로 정하면, 각 열의 합은 일입니다.'),
(123,'common','서로 다른 문제지만, 누가 누구에게\n얼마나 영향을 주는가라는 구조로 볼 수 있습니다.'),
(131,'summary','행렬은 많은 관계를\n하나의 숫자표 안에 체계적으로 담는 방법입니다.'),
(138,'input','그렇다면 이 행렬에 어떤 값을 넣으면,\n그 관계들은 실제 계산에 어떻게 사용될까요?'),
(146,'next','행렬의 숫자 하나는 결과에 어떤 영향을 줄까요?\n다음에는 행렬과 벡터의 곱을 살펴보겠습니다.'),
]

def txt(s,size=28,color=INK,width=7.7):
    m=Text(str(s),font='Malgun Gothic',font_size=size,color=color,line_spacing=1.25)
    if m.width>width:m.scale_to_fit_width(width)
    return m

class RelationTable(VGroup):
    def __init__(self,values=VALUES,show_values=True):
        super().__init__();self.cells=VGroup();self.entries=VGroup()
        for i in range(3):
            for j in range(3):
                center=np.array([(j-1)*1.05,(1-i)*.83,0])
                cell=RoundedRectangle(width=.98,height=.75,corner_radius=.08,stroke_color=MUTED,stroke_width=.8,fill_color=COLORS[j],fill_opacity=.07).move_to(center)
                value=txt(f'{values[i][j]:g}',33,COLORS[j]).move_to(center)
                if not show_values:value.set_opacity(0)
                self.cells.add(cell);self.entries.add(value)
        self.labels=VGroup(txt('주는 대상 (열)',24,MUTED).move_to([0,2.05,0]),txt('받는\n대상\n(행)',22,MUTED).move_to([-2.65,0,0]))
        for i in range(3):
            self.labels.add(txt(str(i+1),24,COLORS[i]).move_to([(i-1)*1.05,1.47,0]))
            self.labels.add(txt(str(i+1),24,COLORS[i]).move_to([-1.97,(1-i)*.83,0]))
        self.add(self.cells,self.entries,self.labels)

class Network(VGroup):
    def __init__(self):
        super().__init__();self.nodes=VGroup();self.edges=VGroup();self.weights=VGroup();self.lookup={}
        positions=[np.array([0,2.05,0]),np.array([-2.3,-1.3,0]),np.array([2.3,-1.3,0])]
        for source in range(3):
            for target in range(3):
                if source==target:continue
                delta=positions[target]-positions[source];direction=delta/np.linalg.norm(delta)
                arrow=CurvedArrow(positions[source]+direction*.5,positions[target]-direction*.5,angle=.75,color=COLORS[source],stroke_width=3,tip_length=.15)
                middle=arrow.point_from_proportion(.5)
                label=txt(f'{VALUES[target][source]:g}',25,COLORS[source]).move_to(middle)
                label.add_background_rectangle(color=config.background_color,opacity=1,buff=.07)
                self.lookup[(source,target)]=(arrow,label)
                self.edges.add(arrow);self.weights.add(label)
        for i,p in enumerate(positions):
            node=VGroup(Circle(radius=.44,color=COLORS[i],fill_color=config.background_color,fill_opacity=1,stroke_width=3),txt(str(i+1),29,COLORS[i])).move_to(p)
            self.nodes.add(node)
        self.add(self.edges,self.weights,self.nodes)

class MatrixRelations(Scene):
    def construct(self):
        self.head,self.note,self.sub=VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('LINEAR ALGEBRA   /   01',19,MUTED).move_to(UP*7),txt('행렬은 관계를 기록한다',40).move_to(UP*6.05))
        self.add(self.chrome)
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub);self.sub=txt(caption,27).move_to(DOWN*6.15);self.add(self.sub)
            animations,duration=getattr(self,action)()
            if animations:self.play(*animations,run_time=duration)
            if end-self.time>1e-5:self.wait(end-self.time)
            if abs(self.time-end)>.04:raise ValueError(f'Timeline drift {action}')
    def heading(self,s):
        self.remove(self.head);self.head=txt(s,30).move_to(UP*4.65);self.add(self.head)
    def formula(self,s):
        self.remove(self.note);self.note=txt(s,26).move_to(DOWN*4.55);self.add(self.note)
    def clear(self,title,note=''):
        self.remove(*[m for m in self.mobjects if all(m is not k for k in [self.chrome,self.head,self.note,self.sub])]);self.heading(title);self.formula(note)
    def intro(self):
        self.heading('숫자로 채워진 작은 표');self.formula('3행 × 3열')
        self.table=RelationTable().scale(1.5);self.table.labels.set_opacity(0)
        return [FadeIn(self.table)],1.5
    def numbers(self):
        self.heading('각 숫자는 무엇을 뜻할까요?');self.formula('0.8은 어떤 관계를 기록한 걸까?')
        return [Indicate(self.table.entries[1],color=GOLD)],1.5
    def objects(self):
        self.clear('세 개의 대상','화살표 방향: 주는 대상 → 받는 대상')
        self.net=Network().scale(1.15);return [FadeIn(self.net.nodes)],1.5
    def cycle(self):
        return [LaggedStart(*[Create(self.net.lookup[k][0]) for k in [(0,1),(1,2)]],lag_ratio=.65)],3
    def complex(self):
        return [LaggedStart(*[Create(self.net.lookup[k][0]) for k in [(2,0),(1,0),(2,1),(0,2)]],lag_ratio=.35)],3
    def weight(self):
        self.heading('연결마다 숫자를 하나씩');self.formula('방향 + 가중치 = 하나의 관계')
        return [FadeIn(self.net.weights)],1.8
    def focus_edge(self,source,target):
        for key,(edge,label) in self.net.lookup.items():
            edge.set_opacity(1 if key==(source,target) else .18)
            label.set_opacity(1 if key==(source,target) else .25)
        edge,label=self.net.lookup[(source,target)]
        return [Indicate(edge),Circumscribe(label,color=COLORS[source])],2
    def edge08(self):
        self.heading('두 번째 → 첫 번째');self.formula('2 → 1 : 0.8')
        return self.focus_edge(1,0)
    def edge01(self):
        self.heading('세 번째 → 첫 번째');self.formula('3 → 1 : 0.1')
        return self.focus_edge(2,0)
    def convention(self):
        self.clear('기록하는 위치를 정합시다','이 영상의 약속: 행 = 받는 대상 / 열 = 주는 대상')
        self.net=Network().scale(.72).shift(UP*1.65)
        self.table=RelationTable(show_values=False).scale(.95).shift(DOWN*2.1)
        return [FadeIn(self.net),FadeIn(self.table)],2
    def place08(self):
        self.heading('받는 1 · 주는 2 → 1행 2열');self.formula('A₁₂ = 0.8     :     2 → 1')
        target=self.table.entries[1];target.set_opacity(1)
        return [TransformFromCopy(self.net.lookup[(1,0)][1],target),Circumscribe(self.table.cells[1],color=GOLD)],2.5
    def place01(self):
        self.heading('받는 1 · 주는 3 → 1행 3열');self.formula('A₁₃ = 0.1     :     3 → 1')
        target=self.table.entries[2];target.set_opacity(1)
        return [TransformFromCopy(self.net.lookup[(2,0)][1],target),Circumscribe(self.table.cells[2],color=PINK)],2.5
    def fill(self):
        self.heading('모든 연결이 하나의 표로');self.formula('Aᵢⱼ : j가 i에게 주는 영향')
        animations=[]
        for source,target in [(0,1),(2,1),(0,2),(1,2)]:
            entry=self.table.entries[target*3+source];entry.set_opacity(1)
            animations.append(TransformFromCopy(self.net.lookup[(source,target)][1],entry))
        for k in [0,4,8]:self.table.entries[k].set_opacity(1);animations.append(FadeIn(self.table.entries[k]))
        return [LaggedStart(*animations,lag_ratio=.25)],3.5
    def diagonal(self):
        self.heading('대각선: 자기 자신과의 관계');self.formula('이 예에서는 직접적인 자기 연결이 없음 → 0')
        return [Circumscribe(self.table.cells[k],color=INK) for k in [0,4,8]],2
    def meaning(self):
        self.heading('숫자 하나 = 방향을 가진 관계 하나');self.formula('0.8은 2 → 1     ·     0.3은 1 → 2')
        return [Circumscribe(self.table.cells[1],color=GOLD),Circumscribe(self.table.cells[3],color=BLUE)],2
    def neural(self):
        self.clear('신경망 · 뉴런 사이의 가중치','가중치: 입력 신호를 얼마나 반영할까?')
        # A separate feed-forward illustration, not the recurrent example graph.
        sources=VGroup(*[VGroup(Circle(radius=.3,color=COLORS[i]),txt(f'x{i+1}',23,COLORS[i])).move_to([-2,1.6-i*1.5,0]) for i in range(3)])
        out=VGroup(Circle(radius=.45,color=INK),txt('y',28)).move_to([2,0,0])
        edges=VGroup(*[Arrow(n.get_right(),out.get_left(),buff=.1,color=COLORS[i],stroke_width=3) for i,n in enumerate(sources)])
        weights=VGroup(*[txt(f'w{i+1}',23,COLORS[i]).move_to([-0.2,.9-i*.65,0]) for i in range(3)])
        return [FadeIn(sources),FadeIn(out),Create(edges),FadeIn(weights)],2.5
    def graph(self):
        self.clear('그래프 · 노드 사이의 연결','방향과 연결의 가중치를 행렬로 기록')
        self.net=Network().scale(1.15);return [FadeIn(self.net)],2
    def probability(self):
        self.clear('확률 · 상태 사이의 이동','별도의 전이확률 예시 · 행: 도착 / 열: 출발')
        self.prob=RelationTable([[0,.6,.4],[.6,0,.6],[.4,.4,0]])
        self.prob.labels[0].become(txt('출발 상태 (열)',24,MUTED).move_to([0,2.05,0]))
        self.prob.labels[1].become(txt('도착\n상태\n(행)',22,MUTED).move_to([-2.65,0,0]))
        self.prob.scale(1.2)
        return [FadeIn(self.prob)],2
    def prob_rule(self):
        self.heading('확률에는 추가 조건이 있습니다');self.formula('각 원소 ≥ 0     ·     각 열의 합 = 1')
        sums=VGroup(*[txt('합 1',24,COLORS[j]).move_to([(j-1)*1.26,-2.04,0]) for j in range(3)])
        return [FadeIn(sums),Circumscribe(VGroup(*[self.prob.cells[k] for k in [0,3,6]]),color=BLUE)],2
    def common(self):
        self.clear('누가 · 누구에게 · 얼마나','분야마다 의미와 조건은 달라도, 기록하는 틀은 같습니다')
        items=VGroup(txt('주는 대상  j',35,GOLD),txt('↓',48,MUTED),txt('관계의 크기  Aᵢⱼ',38),txt('↓',48,MUTED),txt('받는 대상  i',35,BLUE)).arrange(DOWN,buff=.35)
        return [FadeIn(items)],2
    def summary(self):
        self.clear('많은 관계를, 하나의 구조로','행렬: 관계를 위치와 숫자로 체계적으로 기록하는 방법')
        self.table=RelationTable().scale(1.25);return [FadeIn(self.table)],1.5
    def input(self):
        self.clear('관계에 값을 넣으면?','각 대상의 값 → 관계를 반영한 계산 → 새로운 값')
        row=VGroup(txt('A',60,GOLD),txt('×',40,MUTED),txt('x',60,BLUE),txt('=',40,MUTED),txt('?',60,PINK)).arrange(RIGHT,buff=.45).move_to(UP*.6)
        return [FadeIn(row)],1.5
    def next(self):
        self.clear('다음 이야기','02  /  행렬과 벡터의 곱')
        title=txt('숫자 하나가\n결과에 미치는 영향',40).move_to(UP*.5)
        return [FadeIn(title)],1.5
