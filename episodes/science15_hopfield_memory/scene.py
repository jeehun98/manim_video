"""Hopfield associative memory as descent in an energy landscape."""
import json,sys
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt,LIGHT,OBS,MASS,GAS
from episodes.science08_density_growth.scene import DensityGrowthDiscovery

ON='#FFD166'; OFF='#17253B'; NODE='#69D9FF'; ENERGY='#9B8CFF'; GOOD='#71E5A5'; BAD='#FF6B7A'; DIM='#496078'
P3=("1111100","0000110","0000110","0111100","0000110","0000110","1111100")
P7=("1111110","0000110","0001100","0011000","0110000","0110000","0110000")
FLIPS=(1,8,17,23,33,46)

def corrupted(pattern=P3):
    bits=list(''.join(pattern))
    for i in FLIPS:bits[i]='0' if bits[i]=='1' else '1'
    return tuple(''.join(bits[i*7:(i+1)*7]) for i in range(7))

def pixels(pattern,center=ORIGIN,cell=.42,on=ON,off=OFF,stroke=DIM):
    c=np.array(center,dtype=float);g=VGroup()
    for r,row in enumerate(pattern):
        for col,b in enumerate(row):
            sq=Square(cell,stroke_color=stroke,stroke_width=1,fill_color=on if b=='1' else off,fill_opacity=.96)
            sq.move_to(c+[(col-3)*cell,(3-r)*cell,0]);g.add(sq)
    return g

def node_grid(pattern=P3,center=ORIGIN,spacing=.48):
    c=np.array(center,dtype=float);bits=''.join(pattern);nodes=VGroup()
    for i,b in enumerate(bits):
        r,col=divmod(i,7);nodes.add(Dot(c+[(col-3)*spacing,(3-r)*spacing,0],radius=.075,color=ON if b=='1' else OBS))
    lines=VGroup()
    for i,j in [(0,8),(3,17),(6,20),(10,24),(14,30),(18,34),(22,38),(28,40),(32,48),(2,44),(12,36),(16,46)]:
        lines.add(Line(nodes[i],nodes[j],color=DIM,stroke_width=1,stroke_opacity=.45))
    return VGroup(lines,nodes)

def energy_y(x):return .065*(x*x-4)**2-1.25
def landscape(center=(0,.3,0),scale=1):
    c=np.array(center,dtype=float)
    return ParametricFunction(lambda x:c+scale*np.array([x,energy_y(x),0]),t_range=[-3.35,3.35],color=ENERGY,stroke_width=5)
def point_on_land(x,center=(0,.3,0),scale=1):
    c=np.array(center,dtype=float);return c+scale*np.array([x,energy_y(x),0])

def spin(pos,up=True,color=NODE):
    d=UP if up else DOWN
    return VGroup(Arrow(np.array(pos)-d*.28,np.array(pos)+d*.28,buff=0,color=color,stroke_width=4),txt('+1' if up else '−1',pos[1]-.58,18,color).shift(RIGHT*pos[0]))

def medal(center=(0,-3.7,0)):
    return VGroup(Circle(radius=.72,color=ON,fill_color='#6B4E1E',fill_opacity=.75),txt('NOBEL',center[1]+.18,21,ON),txt('2024',center[1]-.28,30,ON)).move_to(center)

class HopfieldMemoryDiscovery(DensityGrowthDiscovery):
    TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'));DURATION=TIMING['duration']
    def construct(self):
        self.brand=txt('과학의 한 장면  /  Nobel 05',7.1,22,'#9BA9C3');self.add(self.brand)

        self.cue('망가진 기억도, 다시 찾을 수 있을까?','일부 픽셀이 사라지고 뒤집힌\n불완전한 숫자 3을 넣어봅니다.')
        clean=pixels(P3,[-1.9,.4,0],.48);noisy=pixels(corrupted(),[1.9,.4,0],.48);self.beat(.25,FadeIn(clean));self.beat(.28,TransformFromCopy(clean,noisy))
        self.add(txt('STORED',-2.05,25,GOOD).shift(LEFT*1.9),txt('CORRUPTED',-2.05,25,BAD).shift(RIGHT*1.9));self.finish()

        self.cue('분류가 아니라, 패턴 자체를 복원한다','라벨 3을 출력하는 대신\n입력의 상태를 기억으로 되돌립니다.')
        noisy=pixels(corrupted(),[-2.2,.65,0],.5);label=txt('3',.65,90,ON).shift(RIGHT*2.2);cross=Cross(label,stroke_color=BAD,stroke_width=8);self.add(noisy,label,cross)
        restored=pixels(P3,[2.2,.65,0],.5);self.beat(.32,FadeOut(label),FadeOut(cross),FadeIn(restored),noisy.animate.set_opacity(.35));self.add(Arrow([-.4,.65,0],[.4,.65,0],color=GOOD),txt('RECONSTRUCT',-2.2,29,GOOD));self.finish()

        self.cue('픽셀 하나를, 두 상태의 노드로 바꾼다','검은 픽셀은 +1, 흰 픽셀은 −1.\n노드들은 서로 연결됩니다.')
        pg=pixels(P3,[0,.8,0],.5);ng=node_grid(P3,[0,.8,0],.5);self.add(pg);self.beat(.3,ReplacementTransform(pg,ng))
        self.add(txt('BLACK  →  +1',-2.4,28,ON),txt('WHITE  →  −1',-3.2,28,OBS),txt('sᵢ ∈ {−1, +1}',-4.05,37,LIGHT));self.finish()

        self.cue('이 구조는, 자석의 스핀과 닮았다','두 상태를 가진 스핀들이\n서로 영향을 주는 물리계입니다.')
        nodes=VGroup(*[Dot([x,y,0],radius=.12,color=ON if (i+j)%2 else OBS) for i,x in enumerate((-2,-.65,.65,2)) for j,y in enumerate((2.2,.7,-.8))]);self.add(nodes)
        magnets=VGroup(*[spin(n.get_center(),k%2==0,ON if k%2==0 else OBS) for k,n in enumerate(nodes)]);self.beat(.35,ReplacementTransform(nodes,magnets));self.add(txt('SPIN MODEL',-2.6,31,ENERGY),txt('sᵢ ∈ {−1, +1}',-3.55,38,LIGHT));self.finish()

        self.cue('연결마다, 선호하는 조합이 있다','양의 연결은 같은 상태를,\n음의 연결은 반대 상태를 선호합니다.')
        same=VGroup(spin([-2.6,1.2,0],True),spin([-.8,1.2,0],True),Line([-2.3,1.2,0],[-1.1,1.2,0],color=GOOD,stroke_width=6),txt('w > 0',.15,25,GOOD).shift(LEFT*1.7))
        diff=VGroup(spin([.8,-1,0],True),spin([2.6,-1,0],False),Line([1.1,-1,0],[2.3,-1,0],color=BAD,stroke_width=6),txt('w < 0',-2.05,25,BAD).shift(RIGHT*1.7))
        self.beat(.3,FadeIn(same),FadeIn(diff));self.add(txt('ALIGN',2.7,28,GOOD).shift(LEFT*1.7),txt('ANTI-ALIGN',-.05,28,BAD).shift(RIGHT*1.7));self.finish()

        self.cue('저장은 복사가 아니라, 안정성을 만드는 일','연결 강도를 조절해 저장 패턴이\n특별히 낮은 에너지를 갖게 합니다.')
        p3=pixels(P3,[-2.5,2.1,0],.28);p7=pixels(P7,[2.5,2.1,0],.28);flat=Line([-3.5,-1,0],[3.5,-1,0],color=DIM,stroke_width=4);self.add(p3,p7,flat)
        valley=landscape([0,-.2,0],.92);self.beat(.45,Transform(flat,valley));self.add(txt('3',-2.55,27,ON).shift(LEFT*1.85),txt('7',-2.55,27,OBS).shift(RIGHT*1.85),txt('CONNECTIONS  →  STABILITY',-3.65,28,GOOD));self.finish()

        self.cue('기억이, 에너지 지형의 골짜기가 된다','모든 네트워크 상태에 값을 붙이면\n저장된 기억은 낮은 안정점이 됩니다.')
        land=landscape([0,.8,0],1);self.beat(.35,Create(land));self.add(pixels(P3,[-2,-2.15,0],.24),pixels(P7,[2,-2.15,0],.24),txt('MEMORY',-3.8,25,LIGHT),txt('LOW-ENERGY STATES',-4.45,31,ENERGY));self.finish()

        self.cue('손상된 입력은, 골짜기 주변에서 시작한다','완전한 기억과 다른 상태이므로\n바닥이 아닌 비탈에 놓입니다.')
        land=landscape([0,.8,0],1);start=point_on_land(-.45,[0,.8,0]);ball=Dot(start,radius=.16,color=BAD);self.add(land,ball,pixels(corrupted(),[-.45,3.1,0],.24));self.beat(.18,Flash(ball,color=BAD,flash_radius=.55));self.add(txt('INITIAL STATE',-3.45,28,BAD));self.finish()

        self.cue('노드 하나를 바꾸며, 에너지를 낮춘다','단일 노드 업데이트가 허용되면\n더 낮은 상태로 이동합니다.')
        before=pixels(corrupted(),[-2,.9,0],.42);after=before.copy();idx=FLIPS[2];target=after[idx];target.set_fill(ON if P3[idx//7][idx%7]=='1' else OFF,opacity=.96);self.add(before)
        self.beat(.28,Transform(before,after),Flash(target,color=GOOD,flash_radius=.35));self.add(txt('+1  →  −1',-1.8,35,LIGHT),txt('E₀  →  E₁',-2.8,40,ENERGY),Arrow([1.2,-3.3,0],[1.2,-4.15,0],color=GOOD),txt('E ↓',-3.75,32,GOOD).shift(RIGHT*2));self.finish()

        self.cue('픽셀 수정과, 지형 하강은 같은 계산이다','왼쪽 상태가 한 단계 복원될 때\n오른쪽 공도 한 단계 내려갑니다.')
        states=[corrupted()]
        bits=list(''.join(states[0]))
        for idx in FLIPS[:4]:bits[idx]=P3[idx//7][idx%7];states.append(tuple(''.join(bits[i*7:(i+1)*7]) for i in range(7)))
        img=pixels(states[0],[-2.25,.5,0],.38);land=landscape([2.0,.6,0],.55);xs=[-.35,-.75,-1.15,-1.55,-2];ball=Dot(point_on_land(xs[0],[2,.6,0],.55),radius=.13,color=BAD);self.add(img,land,ball,Line([0,-3.8,0],[0,3.9,0],color=DIM))
        for k in range(1,5):self.beat(.12,Transform(img,pixels(states[k],[-2.25,.5,0],.38)),ball.animate.move_to(point_on_land(xs[k],[2,.6,0],.55)))
        self.add(txt('STATE UPDATE',-3.7,24,LIGHT).shift(LEFT*2.2),txt('ENERGY DESCENT',-3.7,24,ENERGY).shift(RIGHT*2.1));self.finish()

        self.cue('더 내려갈 수 없을 때, 기억이 복원된다','안정점에서 업데이트가 멈추고\n저장 패턴이 다시 나타납니다.')
        noisy=pixels(corrupted(),[-2.1,.65,0],.45);clean=pixels(P3,[2.1,.65,0],.45);self.add(noisy);self.beat(.4,Transform(noisy,clean));self.add(Arrow([-.3,.65,0],[.3,.65,0],color=GOOD),txt('CORRUPTED PATTERN',-2.15,24,BAD).shift(LEFT*2.1),txt('STABLE STATE',-2.15,24,GOOD).shift(RIGHT*2.1),txt('UPDATE STOPS',-3.3,34,LIGHT));self.finish()

        self.cue('기억에는, 끌어당기는 영역이 있다','서로 다른 초기 상태들이\n같은 안정점으로 흘러듭니다.')
        rings=VGroup(*[Ellipse(width=1.3+i*.95,height=.8+i*.6,color=ENERGY,stroke_opacity=.8-i*.12).move_to([0,.7,0]) for i in range(5)]);center=pixels(P3,[0,.7,0],.2);self.add(rings,center)
        starts=[[-3,2.8,0],[3,2.5,0],[-2.7,-1.6,0],[2.8,-1.9,0]];self.beat(.4,*[GrowArrow(Arrow(p,[np.sign(p[0])*.5,.9 if p[1]>0 else .5,0],color=GOOD)) for p in starts]);self.add(txt('BASIN OF ATTRACTION',-3.75,36,GOOD),txt('거리의 최근접 보장은 아님',-4.55,21,GAS));self.finish()

        self.cue('스핀의 안정성이, 뉴런의 기억이 된다','물리계의 요소와 상호작용을\n신경망의 노드와 가중치로 옮겼습니다.')
        left=VGroup(spin([-2.4,1.6,0],True),spin([-1.2,.3,0],False),Line([-2.2,1.2,0],[-1.4,.65,0],color=ENERGY));right=node_grid(P3,[2,.9,0],.27).scale(.7);self.add(left,right)
        maps=VGroup(txt('spin   ↔   neuron',-1.45,31,LIGHT),txt('interaction   ↔   weight',-2.35,29,LIGHT),txt('low energy   ↔   memory',-3.25,29,GOOD));self.beat(.3,FadeIn(maps));self.finish()

        self.cue('에너지 함수가, 변화의 방향을 정렬한다','비동기 업데이트가 진행될수록\n에너지는 증가하지 않습니다.')
        formula=txt('E = − ½ Σᵢⱼ wᵢⱼ sᵢ sⱼ',1.7,45,LIGHT);self.beat(.25,FadeIn(formula));steps=VGroup(*[Dot([-2.7+i*.9,.2-i*.55,0],radius=.1,color=ENERGY) for i in range(7)]);self.beat(.35,LaggedStart(*[FadeIn(d) for d in steps],lag_ratio=.12))
        self.add(txt('STATE UPDATE',-3.1,29,GAS),Arrow([-1.25,-3.1,0],[1.1,-3.1,0],color=GOOD),txt('E ↓',-3.1,40,GOOD).shift(RIGHT*2));self.finish()

        self.cue('이 지형은, 기억을 찾는 동역학 그 자체다','일반적인 loss landscape와 닮았지만\n같은 개념으로 동일시할 수는 없습니다.')
        hop=landscape([-2,.5,0],.48);loss=ParametricFunction(lambda x:np.array([2+.48*x,.5+.18*np.sin(2*x)+.05*x*x,0]),t_range=[-3,3],color=OBS);self.add(hop,loss)
        self.add(txt('HOPFIELD ENERGY',-1.55,25,ENERGY).shift(LEFT*2),txt('LOSS LANDSCAPE',-1.55,25,OBS).shift(RIGHT*2),DashedLine([0,-2.1,0],[0,2.9,0],color=DIM),txt('related, not identical',-3.35,28,LIGHT));self.finish()

        self.cue('Hopfield에서, Hinton의 확률적 에너지 모델로','안정점의 기억에서 출발해\n에너지와 확률의 학습으로 이어집니다.')
        hop=VGroup(pixels(P3,[-2.2,.8,0],.33),txt('JOHN HOPFIELD',-1.65,28,ENERGY).shift(LEFT*2.2));boltz=VGroup(*[Dot([2.2+np.cos(a),.8+np.sin(a),0],radius=.09,color=GOOD) for a in np.linspace(0,TAU,9)[:-1]],txt('GEOFFREY HINTON',-1.65,28,GOOD).shift(RIGHT*2.15));self.add(hop);self.beat(.32,FadeIn(boltz),GrowArrow(Arrow([-.55,.8,0],[.75,.8,0],color=LIGHT)))
        self.add(txt('HOPFIELD NETWORK',-2.65,24,ENERGY).shift(LEFT*2),txt('BOLTZMANN MACHINE',-2.65,24,GOOD).shift(RIGHT*2));self.finish()

        self.cue('기억을, 안정적인 물리 상태로 바라보다','에너지의 언어가 신경망의\n기억과 학습으로 연결됐습니다.')
        land=landscape([0,1.2,0],1);noisy=pixels(corrupted(),[-1.2,2.7,0],.2);clean=pixels(P3,[-2,-1.4,0],.23);ball=Dot(point_on_land(-.5,[0,1.2,0]),radius=.13,color=BAD);self.add(land,noisy,ball);self.beat(.35,ball.animate.move_to(point_on_land(-2,[0,1.2,0])),Transform(noisy,clean))
        self.add(txt('MEMORY AS A STABLE STATE',-2.7,37,GOOD),txt('JOHN HOPFIELD  ·  GEOFFREY HINTON',-3.45,23,LIGHT),txt('2024 NOBEL PRIZE IN PHYSICS',-4.15,27,ON));self.beat(.12,FadeIn(medal([2.9,-4.0,0]).scale(.72)));self.finish()
