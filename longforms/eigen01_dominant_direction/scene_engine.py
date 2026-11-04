"""Exact user scene durations; shared mathematical model, two native layouts."""
import os
import numpy as np
from manim import *
VERT=os.environ.get('EIGEN_LAYOUT','longform')=='shorts'
config.frame_height=14.222222 if VERT else 8
config.frame_width=8 if VERT else 14.222222
config.background_color='#09121F'
BLUE='#458EFA';TEAL='#20BCA5';ORANGE='#F0A34E';INK='#EDF4FC';MUTED='#91A4BA'
A=np.array([[2.,1.],[1.,2.]])
BOUNDS=[0,3,12,19,26,34,45,55,74,80,84,96,105,114,119]
TITLES=['벡터 하나에서 시작하는 실험','같은 행렬을 반복하면','점점 드러나는 하나의 방향','길이를 맞추고 방향만 관찰','서로 다른 시작, 같은 직선','원래의 직선 위에 남는 방향','같은 행렬, 서로 다른 배율','고유방향 · 고유벡터 · 고윳값','행렬이 결정하는 방향과 배율','하나의 벡터, 두 고유성분','정규화 전: 고유성분의 실제 성장','성장률의 차이가 방향을 바꾼다','시작 벡터에 그 성분이 없다면','반복되는 변환 속에서 드러나는 방향']
def text(s,size=28,color=INK,width=None):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if width and m.width>width:m.scale_to_fit_width(width)
    return m

def transformed(k,x=(1,0)):
    return np.linalg.matrix_power(A,k)@np.array(x,dtype=float)
def unit(v,length=2):return np.array(v)*length/np.linalg.norm(v)
class EigenScene(Scene):
    index=0
    def construct(self):
        i=self.index; duration=BOUNDS[i+1]-BOUNDS[i]
        self.elapsed=0
        top=6.1 if VERT else 3.35
        self.add(text('고윳값과 고유벡터  /  01',16,MUTED).move_to([0,top+.48,0]),text(TITLES[i],30,width=7.2 if VERT else 13).move_to([0,top,0]))
        self.add(Line([-3.6 if VERT else -6.6,top-.45,0],[3.6 if VERT else 6.6,top-.45,0],color='#2A3D54',stroke_width=1))
        self.footer=None
        if i==0:
            p=self.plane();self.play(Create(p),run_time=.8);self.play(GrowArrow(self.arrow(p,[1,0])),run_time=1);self.note('x₀ = (1, 0)')
        elif i in [1,2]:
            # A single fixed scale per shot: all arrows are actual A^k x0.
            ks=[0,1,2] if i==1 else [2,3,4,5]
            maxcoord=max(transformed(ks[-1]));p=self.plane(unit_scale=2.6/maxcoord,extent=maxcoord*1.12)
            self.add(p);v=self.arrow(p,transformed(ks[0]));self.add(v)
            for k in ks[1:]:
                self.add(v.copy().set_opacity(.18));self.play(Transform(v,self.arrow(p,transformed(k))),run_time=1.25);self.note(f'A 적용 {k}회  ·  x{k} = ({int(transformed(k)[0])}, {int(transformed(k)[1])})');self.wait(.3)
            if i==2:self.play(Create(self.diagonal(p,1,2.5,TEAL).set_opacity(.3)),run_time=.7)
        elif i==3:
            centers=self.centers();ps=[self.plane(c,unit_scale=.32,extent=5) for c in centers]
            self.add(*ps);self.labels(['실제 변환 · 길이 증가','방향만 관찰 · 길이 일정'],centers)
            vs=[self.arrow(ps[0],[1,0]),self.arrow(ps[1],unit([1,0],4))];self.add(*vs)
            for k in [1,2]:self.play(Transform(vs[0],self.arrow(ps[0],transformed(k))),Transform(vs[1],self.arrow(ps[1],unit(transformed(k),4))),run_time=1)
            self.note('같은 Aᵏx₀  /  표시하는 길이만 조정')
        elif i==4:
            p=self.plane();self.add(p)
            seeds=[np.array([np.cos(t),np.sin(t)]) for t in np.deg2rad([0,30,80,125,180,210,260,305])]
            vs=[self.arrow(p,unit(v,2.4)) for v in seeds];self.add(*vs)
            for k in range(1,6):self.play(*[Transform(m,self.arrow(p,unit(transformed(k,v),2.4))) for m,v in zip(vs,seeds)],run_time=.8)
            self.play(Create(self.diagonal(p,1,2.9,TEAL)),run_time=.6);self.note('반대쪽을 향해도 같은 직선으로 정렬')
        elif i==5:
            p=self.plane(unit_scale=.7);self.add(p);self.note('A = [[2, 1], [1, 2]]')
            seeds=[np.array([np.cos(t),np.sin(t)])*.9 for t in np.linspace(0,TAU,16,endpoint=False)]
            ghosts=[self.arrow(p,v).set_opacity(.2) for v in seeds];vs=[self.arrow(p,v) for v in seeds];self.add(*ghosts,*vs);self.wait(1)
            self.play(*[Transform(m,self.arrow(p,A@v)) for m,v in zip(vs,seeds)],run_time=2)
            self.play(*[m.animate.set_opacity(.14) for j,m in enumerate(vs) if j not in [2,6,10,14]],Create(self.diagonal(p,1,2.8,TEAL)),Create(self.diagonal(p,-1,2.8,ORANGE)),run_time=1.5)
            self.note('변환 후에도 같은 직선 위에 남는다')
        elif i==6:
            centers=self.centers();ps=[self.plane(c,unit_scale=.52,extent=3.5) for c in centers];self.add(*ps);self.labels(['첫 번째 방향  ×3','두 번째 방향  ×1'],centers)
            vs=[self.arrow(ps[0],[1,1],TEAL),self.arrow(ps[1],[1,-1],ORANGE)];self.add(*vs)
            self.play(Transform(vs[0],self.arrow(ps[0],[3,3],TEAL)),Indicate(vs[1],color=ORANGE),run_time=2)
            self.note('(1, 1) → (3, 3)     /     (1, −1) → (1, −1)')
        elif i==7:
            p=self.plane(unit_scale=.8);self.add(p);d=self.diagonal(p,1,3,TEAL);self.play(Create(d),run_time=.7);self.note('고유방향: 변환 후에도 같은 직선');self.until(5)
            v=self.arrow(p,[1,1],TEAL);self.play(GrowArrow(v),run_time=.8);self.note('고유벡터: 그 직선 위의 영벡터가 아닌 벡터');self.until(9)
            self.play(Transform(v,self.arrow(p,[2.5,2.5],TEAL)),run_time=1);self.note('Av = λv,  v ≠ 0   ·   λ: 고윳값');self.until(14)
            self.add(self.diagonal(p,-1,2.8,ORANGE),self.arrow(p,[1,-1],ORANGE));self.note('v₁ = (1, 1): λ₁ = 3\nv₂ = (1, −1): λ₂ = 1')
        elif i==8:
            p=self.plane(unit_scale=.8);self.add(p,self.diagonal(p,1,3,TEAL),self.diagonal(p,-1,3,ORANGE));v=self.arrow(p,[1,1],TEAL);w=self.arrow(p,[1,-1],ORANGE);self.add(v,w)
            self.note('A = [[2, 1], [1, 2]]\n행렬 A → 고유방향과 고윳값')
            self.play(Transform(v,self.arrow(p,[2,2],TEAL)),Transform(w,self.arrow(p,[2,-2],ORANGE)),run_time=1.5);self.note('대표 벡터의 길이를 바꿔도  λ₁ = 3, λ₂ = 1')
        elif i==9:
            p=self.plane(unit_scale=2);self.add(p,self.arrow(p,[1,0]));self.play(GrowArrow(self.arrow(p,[.5,.5],TEAL)),run_time=.8)
            self.play(GrowArrow(self.arrow(p,[.5,-.5],ORANGE,start=[.5,.5])),Create(DashedLine(p.c2p(0,0),p.c2p(.5,-.5),color=ORANGE)),Create(DashedLine(p.c2p(.5,-.5),p.c2p(1,0),color=TEAL)),run_time=.8);self.note('x₀ = ½v₁ + ½v₂')
        elif i==10:
            x=-2.4 if VERT else -4.7; length=4.8 if VERT else 9.4
            ys=[1.2,-.2];bars=[]
            self.add(text('初期 크기 대비 배율'.replace('初期','초기'),23,MUTED).move_to([0,2.4,0]))
            for y,c,l in zip(ys,[TEAL,ORANGE],['λ₁ = 3','λ₂ = 1']):
                self.add(text(l,25,c).move_to([x+.6,y+.48,0]),Line([x,y-.12,0],[x+length,y-.12,0],color='#314355'))
                b=Rectangle(width=length/27,height=.25,fill_color=c,fill_opacity=1,stroke_width=0).move_to([x+length/54,y,0]);bars.append(b)
            self.add(*bars)
            for n,k in enumerate([1,2,3]):
                val=3**k;new=Rectangle(width=length*val/27,height=.25,fill_color=TEAL,fill_opacity=1,stroke_width=0).move_to([x+length*val/54,ys[0],0]);self.play(Transform(bars[0],new),run_time=1);self.note(f'A 적용 {k}회   ·   첫 성분 {val}배 / 둘째 성분 1배\n동일 척도 · 정규화 이전');self.until((n+1)*4)
        elif i==11:
            p=self.plane(unit_scale=.5);self.add(p,self.diagonal(p,1,2.9,TEAL));v=self.arrow(p,[1,0]);a=self.arrow(p,[.5,.5],TEAL);b=self.arrow(p,[.5,-.5],ORANGE,start=[.5,.5]);self.add(a,b,v)
            for k in [1,2]:
                c=3**k/2;self.play(Transform(a,self.arrow(p,[c,c],TEAL)),Transform(b,self.arrow(p,[.5,-.5],ORANGE,start=[c,c])),Transform(v,self.arrow(p,transformed(k))),run_time=1.2)
            self.note('xₖ = (3ᵏ/2)v₁ + ½v₂');self.until(5)
            # Normalize the entire sum with one common factor, including both components.
            for k in [3,4,5]:
                norm=np.linalg.norm(transformed(k));c=np.array([3**k/2]*2)*5/norm;d=np.array([.5,-.5])*5/norm
                self.play(Transform(a,self.arrow(p,c,TEAL)),Transform(b,self.arrow(p,d,ORANGE,start=c)),Transform(v,self.arrow(p,c+d)),run_time=.7)
            self.note('전체를 같은 비율로 정규화 → 방향은 유지')
        elif i==12:
            p=self.plane();self.add(p,self.diagonal(p,1,2.8,TEAL),self.diagonal(p,-1,2.8,ORANGE));v=self.arrow(p,[1,-1],ORANGE);self.add(v)
            for k in [1,2,3]:self.play(Indicate(v,color=ORANGE),run_time=.8);self.note(f'A 적용 {k}회 · 변하지 않는 v₂');self.wait(.5)
            self.note('첫 번째 고유성분 = 0\nAᵏv₂ = v₂')
        else:
            p=self.plane();self.add(p,self.diagonal(p,1,2.8,TEAL));v=self.arrow(p,unit([1,0],2.5));self.add(v)
            for k in [1,2,4,6]:self.play(Transform(v,self.arrow(p,unit(transformed(k),2.5))),run_time=.45)
            self.play(p.animate.set_opacity(.18),run_time=.4);self.note('더 크게 증폭되는 고유성분이\n전체 방향을 결정한다')
        self.until(duration)
    def until(self,t):
        if self.time<t:self.wait(t-self.time)
        elif self.time>t+1e-6:raise RuntimeError(f'Scene {self.index+1} exceeds {t}: {self.time}')
    def note(self,s):
        if self.footer:self.remove(self.footer)
        self.footer=text(s,21 if VERT else 25,color=MUTED if VERT else INK,width=6.9 if VERT else 12.5).move_to([0,-4.25 if VERT else -2.85,0]);self.add(self.footer)
    def centers(self):return [np.array([0,2.15,0]),np.array([0,-1.9,0])] if VERT else [np.array([-3.5,.05,0]),np.array([3.5,.05,0])]
    def labels(self,ss,centers):
        for s,c in zip(ss,centers):self.add(text(s,23,width=6).move_to(c+[0,1.85 if VERT else 2.1,0]))
    def plane(self,center=None,unit_scale=1,extent=3):
        center=np.array([0,.3 if VERT else 0,0]) if center is None else center
        extent=min(extent,3/unit_scale)
        p=NumberPlane(x_range=[-extent,extent,max(extent/4,.5)],y_range=[-extent,extent,max(extent/4,.5)],x_length=2*extent*unit_scale,y_length=2*extent*unit_scale,background_line_style={'stroke_color':'#28394D','stroke_width':1,'stroke_opacity':.55},axis_config={'stroke_color':'#718298','stroke_width':1.2,'include_ticks':False}).move_to(center)
        return p
    def arrow(self,p,v,color=BLUE,start=None):
        start=np.zeros(2) if start is None else np.array(start);v=np.array(v)
        return Arrow(p.c2p(*start),p.c2p(*(start+v)),buff=0,color=color,stroke_width=4,max_tip_length_to_length_ratio=.16)
    def diagonal(self,p,sign,length,color):
        o=p.c2p(0,0);d=np.array([1,sign,0])/np.sqrt(2)*length
        return DashedLine(o-d,o+d,color=color,stroke_width=2,dash_length=.12)
