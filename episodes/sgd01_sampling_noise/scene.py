"""Twelve independent claims, with numerical gradients and actual sampled paths."""
import json
import os
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT, BG, INK, MUTED, GOOD, PRUNE, SPARSE, ACCENT, pill, configure_vertical
configure_vertical()
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import math_model as model
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
BLUE='#56B4FF';ORANGE='#FFAE70';PURPLE=SPARSE;YELLOW=ACCENT

def text(s,y=0,x=0,size=28,color=INK,width=7.6):
    obj=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.15)
    if obj.width>width:obj.scale_to_fit_width(width)
    return obj.move_to([x,y,0])

def block(s,x=0,y=0,w=2,color=BLUE):return pill(s,color,w).move_to([x,y,0])

def arrow(a,b,color=BLUE):
    return Arrow(a,b,buff=0,color=color,stroke_width=3,tip_length=.15,max_tip_length_to_length_ratio=.22)

def wrap(s,limit=27):
    lines=[];line=''
    for word in s.split():
        if line and len(line)+len(word)+1>limit:lines.append(line);line=word
        else:line=(line+' '+word).strip()
    if line:lines.append(line)
    return '\n'.join(lines)

def grid(y=2.3):
    return VGroup(*[Square(side_length=.33,color=BLUE,fill_color=BLUE,fill_opacity=.18,stroke_width=1) for _ in range(48)]).arrange_in_grid(rows=6,cols=8,buff=.13).move_to([0,y,0])

def axes(y=.5,w=6.6,h=5):
    return Axes(x_range=[-2,2,1],y_range=[-1,2,1],x_length=w,y_length=h,tips=False,axis_config=dict(color=MUTED,stroke_width=1,include_ticks=False)).move_to([0,y,0])

def vec(ax,g,color=GOOD):return arrow(ax.c2p(0,0),ax.c2p(*g),color)

def endpoint_cloud(ax,values,color=PURPLE,radius=.033):
    return VGroup(*[Dot(ax.c2p(*p),radius=radius,color=color,fill_opacity=.6) for p in values])

def ellipse(ax,cov,center=model.MEAN,color=PURPLE):
    eig,U=np.linalg.eigh(cov)
    pts=[ax.c2p(*(center+U@(np.sqrt(np.maximum(eig,0))*np.array([np.cos(t),np.sin(t)]))*1.5)) for t in np.linspace(0,TAU,100)]
    return VMobject(color=color,stroke_width=2,stroke_opacity=.8).set_points_as_corners(pts)

def loss_panel():
    ax=Axes(x_range=[-1.55,1.55,1],y_range=[-.85,1.55,1],x_length=6.5,y_length=5.2,tips=False,axis_config=dict(color=MUTED,stroke_width=1,include_ticks=False)).move_to([0,.7,0])
    contours=VGroup()
    xs=np.linspace(-1.5,1.5,400)
    for level in [.035,.09,.18,.3,.5,.8,1.15]:
        z=2*(level-(xs*xs-1)**2/4)
        valid=z>=0
        edges=np.flatnonzero(np.diff(np.r_[False,valid,False]))
        for a,b in zip(edges[::2],edges[1::2]):
            for sign in [-1,1]:
                coords=[ax.c2p(float(x),float(y)) for x,y in zip(xs[a:b],sign*np.sqrt(z[a:b])) if -.82<=y<=1.5]
                if len(coords)>1:contours.add(VMobject(color=MUTED,stroke_width=1,stroke_opacity=.35).set_points_as_corners(coords))
    gd=VMobject(color=BLUE,stroke_width=4).set_points_as_corners([ax.c2p(*p) for p in model.trajectory()])
    paths=VGroup(*[VMobject(color=c,stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in model.trajectory(seed)]) for seed,c in [(4,GOOD),(9,ORANGE),(14,PURPLE)]])
    return ax,contours,gd,paths


class TimedShot(Scene):
    NUMBER=1

    def refresh(self,target=None):
        t=self.offset+self.time if target is None else target
        idx=next((i for i,s in enumerate(DATA['segments']) if s['start']<=t+1e-5<s['end']),len(DATA['segments'])-1)
        if idx<=self.caption_index:return
        self.caption_index=idx
        c=text(wrap(DATA['segments'][idx]['text']),-6.2,size=25,width=7.5)
        assert c.height<2.15,('caption height',idx,c.height)
        self.caption.become(c)
        self.caption.set_z_index(20)
        self.audit.append(dict(sentence=idx+1,at=round(self.offset+self.time,5)))

    def play(self,*args,**kwargs):
        self.refresh()
        result=super().play(*args,**kwargs)
        self.refresh()
        self.check_bounds()
        return result

    def check_bounds(self):
        for item in self.mobjects:
            if item is self.caption or item is self.chrome:continue
            if not item.has_points() and not item.submobjects:continue
            assert item.get_left()[0]>=-4.15 and item.get_right()[0]<=4.15,('horizontal',self.NUMBER,self.time,item.get_left(),item.get_right())
            assert item.get_bottom()[1]>=-4.8 and item.get_top()[1]<=5.05,('caption or header overlap',self.NUMBER,self.time,item.get_bottom(),item.get_top())

    def to(self,target):
        local=target-self.offset
        if self.time>local+1/30+1e-6:raise ValueError(f'Shot {self.NUMBER}: {self.time+self.offset} > {target}')
        boundaries=[s['start']-self.offset for s in DATA['segments'] if self.time+1e-5<s['start']-self.offset<local-1e-5]+[local]
        for end in boundaries:
            if end-self.time>1e-5:self.wait(end-self.time)
            self.refresh(self.offset+end)

    def at(self,t,*animations,duration=.7):
        self.to(t)
        self.play(*animations,run_time=duration)

    def note(self,s,y=-4.1,color=MUTED,size=23):
        o=text(s,y,size=size,color=color)
        self.play(FadeIn(o),run_time=.4)
        return o

    def construct(self):
        spec=DATA['scenes'][self.NUMBER-1];self.offset=spec['start']
        self.audit=[];self.caption_index=-1;self.caption=VGroup()
        self.chrome=VGroup(text('과학 한조각  /  AI',7.35,size=20,color=MUTED),
                 text('SGD의 잡음',6.55,size=38),text(spec['title'],5.62,size=26,color=YELLOW),
                 Line([-3.8,5.13,0],[3.8,5.13,0],color=MUTED,stroke_opacity=.25),
                 Line([-3.8,-4.9,0],[3.8,-4.9,0],color=MUTED,stroke_opacity=.25))
        self.add(self.chrome,self.caption)
        self.refresh()
        getattr(self,f's{self.NUMBER:02}')()
        self.to(spec['end'])
        assert abs(self.time-(spec['end']-spec['start']))<1/30+1e-6
        audit_dir=Path(os.environ.get('SGD_AUDIT',str(HERE.parents[1]/'media/sgd01/audit')))
        audit_dir.mkdir(parents=True,exist_ok=True)
        (audit_dir/f'{self.NUMBER:02}.json').write_text(json.dumps(self.audit),encoding='utf-8')

    def s01(self):
        tiles=grid(2.3)
        self.play(FadeIn(tiles[:1]),run_time=.5)
        self.at(1,LaggedStart(*[FadeIn(p) for p in tiles[1:]],lag_ratio=.025),duration=1.6)
        compute=block('기울기 계산',y=-.5,w=4,color=GOOD)
        flow=arrow([0,.6,0],[0,.05,0],BLUE)
        self.at(5,FadeIn(compute),GrowArrow(flow))
        self.at(7,FadeIn(text('θ ← θ − ηg',-2,size=36,color=YELLOW)))
        grad=arrow([-.1,-3.15,0],[2.1,-3.15,0],ORANGE)
        update=arrow([-.1,-3.8,0],[-2.3,-3.8,0],GOOD)
        self.at(8.5,GrowArrow(grad),FadeIn(text('기울기 g',-3.15,-2.5,22,ORANGE,2.5)))
        self.at(10,GrowArrow(update),FadeIn(text('업데이트 −ηg',-3.8,2,22,GOOD,3)))
        self.at(12,FadeIn(text('FULL DATASET / EVERY UPDATE',4.5,size=22,color=BLUE)))
        self.at(14,Indicate(tiles,color=BLUE),duration=.9)
        self.note('매번 모든 데이터를 계산한다면?',-4.5,size=24)

    def s02(self):
        tiles=grid(2.8).scale(.75);self.add(tiles)
        selected=[2,13,29,43]
        self.play(*[tiles[i].animate.set_fill(GOOD,opacity=.9).set_color(GOOD) for i in selected],run_time=.7)
        chosen=VGroup(*[tiles[i].copy() for i in selected]).arrange(RIGHT,buff=.7).move_to([0,.8,0])
        self.at(19,*[TransformFromCopy(tiles[i],p) for i,p in zip(selected,chosen)])
        self.at(20,FadeIn(text('선택된 4개 데이터',1.6,size=24,color=GOOD)))
        grads=np.array([[1,.3],[.6,.7],[1.2,.5],[.4,.1]])
        arrows=VGroup(*[arrow(p.get_bottom()+DOWN*.4,p.get_bottom()+DOWN*.4+np.r_[g*.6,0],ORANGE) for p,g in zip(chosen,grads)])
        self.at(21,LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.15))
        avg=arrow([-1.6,-2.1,0],[.8,-.9,0],GOOD)
        self.at(23,GrowArrow(avg),FadeIn(text('기울기의 합 ÷ B = 평균',-2.9,size=27,color=GOOD)))
        self.at(25,FadeIn(text('g_B = (1/B) Σ g_i',-3.7,size=32,color=YELLOW)))
        self.at(27,FadeIn(text('SGD · MINI-BATCH',-4.5,size=24,color=GOOD)))

    def s03(self):
        ax=axes();origin=Dot(ax.c2p(0,0),color=YELLOW,radius=.1)
        self.add(ax,origin,text('기울기 벡터 공간 · 같은 θ',4.3,size=25,color=YELLOW))
        options=[model.WIDE[g].mean(axis=0) for g in model.GROUPS]
        g=vec(ax,options[0],GOOD)
        label=block('미니배치 A',y=-3.5,w=4,color=GOOD)
        self.play(GrowArrow(g),FadeIn(label),run_time=.7)
        self.at(33,Transform(g,vec(ax,options[1],ORANGE)),Transform(label,block('미니배치 B',y=-3.5,w=4,color=ORANGE)))
        self.at(35,Transform(g,vec(ax,options[2],PURPLE)),Transform(label,block('미니배치 C',y=-3.5,w=4,color=PURPLE)))
        self.at(37,FadeIn(text('가중치는 고정 · 선택한 데이터만 변경',-4.4,size=24,color=INK)))

    def s04(self):
        line=NumberLine(x_range=[-6,6,1],length=6.8,include_ticks=False,color=MUTED).move_to([0,1,0])
        dot=Dot(line.n2p(0),color=YELLOW,radius=.11)
        a=arrow(line.n2p(0),line.n2p(5),ORANGE);b=arrow(line.n2p(0),line.n2p(-5),BLUE)
        self.add(text('두 데이터만 있는 예시 · 현재 θ = 0',4.3,size=24,color=MUTED),line,dot)
        self.play(FadeIn(block('데이터 A',-2,3,2.7,ORANGE)),FadeIn(block('데이터 B',2,3,2.7,BLUE)),run_time=.6)
        self.at(40,GrowArrow(a),FadeIn(text('g₁ = +5',2,-2,size=29,color=ORANGE)))
        self.at(42,GrowArrow(b),FadeIn(text('g₂ = −5',2,2,size=29,color=BLUE)))
        self.at(45,FadeIn(text('g = (5 + (−5)) / 2 = 0',-.5,size=32,color=YELLOW)))
        # Translate the second vector into head-to-tail position; the sum closes.
        self.at(46,b.animate.shift(RIGHT*(line.n2p(5)[0]-line.n2p(0)[0])),duration=.8)
        self.at(47.5,FadeOut(a),FadeOut(b),Indicate(dot,color=YELLOW),duration=.7)
        self.at(49,FadeIn(block('FULL-BATCH GD · NO UPDATE',y=-2,w=7,color=BLUE)))
        self.at(51,FadeIn(text('Δθ = −η × 0 = 0',-3.3,size=32,color=BLUE)))
        self.note('전체 기울기만 사용하는 GD',-4.4,size=23)

    def s05(self):
        ax1=NumberLine(x_range=[-1,1,1],length=2.8,include_ticks=False,color=MUTED).move_to([-2,1.5,0])
        ax2=NumberLine(x_range=[-1,1,1],length=2.8,include_ticks=False,color=MUTED).move_to([2,1.5,0])
        d1=Dot(ax1.n2p(0),color=BLUE,radius=.1);d2=Dot(ax2.n2p(0),color=GOOD,radius=.1)
        self.add(ax1,ax2,d1,d2,text('Full-batch',3.2,-2,28,BLUE,3),text('SGD · B = 1',3.2,2,28,GOOD,3),text('동일한 시작 위치 θ = 0',4.4,size=24,color=MUTED))
        select=block('A 선택 · g_A = +5',y=-.1,w=5,color=ORANGE)
        self.play(FadeIn(select),run_time=.7)
        grad_arrow=arrow(ax2.n2p(0)+UP*.45,ax2.n2p(.75)+UP*.45,ORANGE)
        self.at(55,GrowArrow(grad_arrow))
        upd=arrow(ax2.n2p(0),ax2.n2p(-.5),GOOD)
        self.at(56,GrowArrow(upd),d2.animate.move_to(ax2.n2p(-.5)))
        step=text('η = 0.1  →  Δθ = −0.5',-1.3,size=29,color=GOOD)
        self.at(58,FadeIn(step))
        self.at(59,Transform(select,block('다음 B · 새 위치에서 g_B = −4.625',y=-.1,w=7,color=ORANGE)),Transform(grad_arrow,arrow(ax2.n2p(-.5)+UP*.45,ax2.n2p(-1.1)+UP*.45,ORANGE)))
        self.at(60.5,Transform(upd,arrow(ax2.n2p(-.5),ax2.n2p(-.0375),GOOD)),d2.animate.move_to(ax2.n2p(-.0375)),Transform(step,text('다음 업데이트 Δθ = +0.4625',-1.3,size=28,color=GOOD)),duration=.7)
        self.at(61.5,FadeIn(text('θ: 0 → −0.5 → −0.0375',-2.3,size=28,color=YELLOW)),duration=.6)
        self.at(63,FadeIn(text('기울기 0 ≠ 좋은 최소점 보장',-3.5,size=28,color=PRUNE)))
        self.at(66,FadeIn(text('개별 업데이트 가능 ≠ 평균적으로 한 방향 이동',-4.4,size=21,color=MUTED)))

    def s06(self):
        ax=axes();g=vec(ax,model.MEAN,BLUE);gb=vec(ax,[1.65,1.1],GOOD)
        diff=arrow(ax.c2p(*model.MEAN),ax.c2p(1.65,1.1),PURPLE)
        self.add(ax,text('기울기 벡터 공간 · 같은 θ',4.3,size=24,color=MUTED))
        self.play(GrowArrow(g),FadeIn(text('전체 g',3.5,-2,25,BLUE,3)),run_time=.6)
        self.at(70,GrowArrow(gb),FadeIn(text('미니배치 g_B',3.5,1.7,25,GOOD,3.5)))
        self.at(72,GrowArrow(diff),FadeIn(text('ξ_B = g_B − g',-3.3,size=34,color=PURPLE)))
        self.at(75,FadeIn(text('SAMPLING NOISE',-4.3,size=25,color=PURPLE)))
        for t,v in [(76,[-.4,.65]),(78,[1.1,.9])]:
            self.at(t,Transform(gb,vec(ax,v,GOOD)),Transform(diff,arrow(ax.c2p(*model.MEAN),ax.c2p(*v),PURPLE)))

    def s07(self):
        ax=axes();vectors=VGroup(*[vec(ax,g,ORANGE).set_stroke(width=1.7,opacity=.4) for g in model.NARROW])
        self.add(ax,text('기울기 벡터 공간 · 같은 θ',4.3,size=24,color=MUTED))
        self.play(LaggedStart(*[GrowArrow(v) for v in vectors],lag_ratio=.06),run_time=1.3)
        self.at(85,FadeIn(endpoint_cloud(ax,model.NARROW,ORANGE,.055)))
        mean=vec(ax,model.NARROW[model.GROUPS[0]].mean(axis=0),GOOD)
        self.at(88,GrowArrow(mean),FadeIn(text('개별 기울기가 비슷하면',-3.3,size=27,color=ORANGE)))
        for t,group in [(90,1),(92,2)]:self.at(t,Transform(mean,vec(ax,model.NARROW[model.GROUPS[group]].mean(axis=0),GOOD)))
        self.at(93.5,FadeIn(text('미니배치 평균도 비슷하다 · LOW VARIANCE',-4.4,size=22,color=GOOD)),duration=.5)

    def s08(self):
        ax=axes();vectors=VGroup(*[vec(ax,g,ORANGE).set_stroke(width=1.5,opacity=.3) for g in model.WIDE])
        shape=ellipse(ax,model.covariance())
        self.add(ax,text('동일한 θ · 데이터별 기울기 비교',4.3,size=24,color=MUTED))
        self.play(LaggedStart(*[GrowArrow(v) for v in vectors],lag_ratio=.03),run_time=1)
        dots=endpoint_cloud(ax,model.WIDE,PURPLE,.055)
        self.at(97,FadeIn(dots),Create(shape))
        means=[model.WIDE[g].mean(axis=0) for g in model.GROUPS]
        avg=vec(ax,means[0],GOOD)
        self.at(98,GrowArrow(avg))
        self.at(99.5,Transform(avg,vec(ax,means[1],GOOD)),duration=.6)
        self.at(101,Transform(avg,vec(ax,means[2],GOOD)),FadeIn(text('좌우 변동 > 위아래 변동',-3.25,size=28,color=PURPLE)))
        self.at(103,FadeIn(text('ANISOTROPIC NOISE',-4.2,size=25,color=PURPLE)))
        self.at(105,FadeIn(text('타원: 공분산 구조 · 균일한 분포 경계 아님',3.5,size=21,color=MUTED)))

    def s09(self):
        ax=axes(y=.7);self.add(ax,text('같은 데이터 · 같은 θ · 독립 복원추출',4.4,size=23,color=MUTED))
        reference=Dot(ax.c2p(*model.MEAN),color=YELLOW,radius=.09)
        clouds=[endpoint_cloud(ax,model.means(b),c,.035) for b,c in [(1,ORANGE),(4,GOOD),(16,BLUE)]]
        shapes=[ellipse(ax,model.covariance(b),color=c) for b,c in [(1,ORANGE),(4,GOOD),(16,BLUE)]]
        label=block('B = 1',y=-2.85,w=2.5,color=ORANGE)
        count=text('각 배치 크기마다 192회 샘플링',-4.5,size=21,color=MUTED)
        cloud=clouds[0];shape=shapes[0]
        self.play(FadeIn(reference),FadeIn(label),FadeIn(cloud[:24]),run_time=.7)
        self.at(110,FadeIn(cloud[24:]),Create(shape),FadeIn(count))
        self.at(112,Transform(label,block('B = 4',y=-2.85,w=2.5,color=GOOD)),Transform(cloud,clouds[1]),Transform(shape,shapes[1]),duration=.8)
        self.at(116,Transform(label,block('B = 16',y=-2.85,w=2.5,color=BLUE)),Transform(cloud,clouds[2]),Transform(shape,shapes[2]),duration=.8)
        self.at(119,FadeIn(text('평균 기울기 주변으로 밀집',3.5,size=25,color=YELLOW)))
        self.at(123,FadeIn(text('Cov(g_B) = C / B',-3.7,size=31,color=PURPLE)))
        self.at(126,Indicate(shape,color=BLUE),duration=.7)

    def s10(self):
        ax,contours,gd,paths=loss_panel()
        start=Dot(ax.c2p(0,1.15),color=YELLOW,radius=.1)
        self.add(ax,contours,start,text('같은 손실함수 · 같은 출발점',4.35,size=25,color=MUTED))
        self.play(Create(gd),run_time=.8)
        self.at(130,LaggedStart(*[Create(p) for p in paths],lag_ratio=.2),duration=1.6)
        self.at(132,FadeIn(text('Full-batch GD',-3.2,-1.9,25,BLUE,3.4)),FadeIn(text('SGD · 다른 선택 순서',-3.2,1.7,24,GOOD,4)))
        self.note('장난감 손실함수에서 직접 계산한 궤적',-4.4,size=22)

    def s11(self):
        ax,contours,gd,paths=loss_panel()
        panel=VGroup(ax,contours,gd,paths).scale(.64).move_to([0,2.1,0])
        self.add(panel,text('SDE · 확률미분방정식',4.5,size=30,color=YELLOW))
        drift=block('전체 기울기의 흐름',-1.9,-.5,3.5,BLUE)
        noise=block('샘플링의 확률적 변동',1.9,-.5,3.6,PURPLE)
        self.play(FadeIn(drift),run_time=.6)
        self.at(137,FadeIn(noise))
        self.at(140,FadeIn(text('dθ = −∇L dt + G dW',-2,size=34,color=YELLOW)))
        self.at(142,FadeIn(text('결정론적 흐름 + 확률적 움직임',-3.25,size=27,color=INK)))
        self.note('조건 아래의 연속시간 근사 · 학습률·배치 크기 반영',-4.4,size=20)

    def s12(self):
        ax,contours,gd,paths=loss_panel()
        self.add(ax,contours,gd)
        self.play(LaggedStart(*[Create(p) for p in paths],lag_ratio=.15),run_time=1.6)
        caution=text('잡음이 크다고 항상 더 좋은 결과는 아니다',4.4,size=25,color=PRUNE)
        self.at(148,FadeIn(caution))
        key=text('계산의 선택이 학습의 움직임을 바꾼다',-3.4,size=27,color=YELLOW)
        self.at(151,FadeIn(key))
        efficiency=text('일부 데이터를 선택해 계산량을 줄인다',4.4,size=26,color=GOOD)
        self.at(155,FadeOut(caution),FadeIn(efficiency))
        self.at(158,Indicate(paths,color=GOOD),duration=.7)
        final=text('샘플링이 바꾸는\n학습의 경로',1.1,size=43,color=YELLOW)
        self.at(160,FadeOut(ax),FadeOut(contours),FadeOut(gd),FadeOut(paths),FadeOut(key),FadeOut(efficiency),FadeIn(final),duration=.8)
        self.at(162,FadeIn(text('STOCHASTIC GRADIENT DESCENT',-1.5,size=24,color=GOOD)))

class Shot01(TimedShot):NUMBER=1
class Shot02(TimedShot):NUMBER=2
class Shot03(TimedShot):NUMBER=3
class Shot04(TimedShot):NUMBER=4
class Shot05(TimedShot):NUMBER=5
class Shot06(TimedShot):NUMBER=6
class Shot07(TimedShot):NUMBER=7
class Shot08(TimedShot):NUMBER=8
class Shot09(TimedShot):NUMBER=9
class Shot10(TimedShot):NUMBER=10
class Shot11(TimedShot):NUMBER=11
class Shot12(TimedShot):NUMBER=12

