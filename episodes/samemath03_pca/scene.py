"""Same Math 03: one centered data set, two PCA objectives, two native layouts."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from manim import *

WIDE='SameMath03Long' in sys.argv
config.frame_width=16 if WIDE else 9
config.frame_height=9 if WIDE else 16
config.background_color='#101B2E'

DATA=json.loads((Path(__file__).parent/'script.json').read_text(encoding='utf-8'))
BG='#101B2E';PANEL='#17263D';EDGE='#344761';INK='#EEF4F8';MUTED='#A9BACC'
RAW='#9CC9EF';KEEP='#2DD4BF';LOSS='#F59E45';GOLD='#F7D776';FONT='Malgun Gothic'
ENDS=(10,27,42,50,62,74,88,95,104,119,138,151)

rng=np.random.default_rng(42)
angle_true=math.radians(30)
rotation=np.array([[math.cos(angle_true),-math.sin(angle_true)],
                   [math.sin(angle_true), math.cos(angle_true)]])
X=rng.standard_normal((42,2))@np.diag([1.75,.48])@rotation.T
X-=X.mean(axis=0)
values,vectors=np.linalg.eigh(X.T@X)
PC=vectors[:,np.argmax(values)]
if PC[0]<0:PC=-PC
PC_ANGLE=math.atan2(PC[1],PC[0])
TOTAL=float(np.sum(X*X))
assert np.allclose(X.mean(axis=0),0)


def txt(s,size=27,color=INK):
    return Text(s,font=FONT,font_size=size,color=color)


def colored(parts,size=43):
    m=MathTex(*[s for s,_ in parts],font_size=size)
    for part,(_,color) in zip(m,parts):part.set_color(color)
    return m


def wrap(s,limit):
    out=[];line=''
    for word in s.split():
        test=(line+' '+word).strip()
        if len(test)>limit and line:out.append(line);line=word
        else:line=test
    if line:out.append(line)
    return out


def metric(theta):
    v=np.array([math.cos(theta),math.sin(theta)])
    z=X@v
    projected=np.outer(z,v)
    retained=float(np.sum(z*z))
    error=float(np.sum((X-projected)**2))
    assert math.isclose(retained+error,TOTAL,rel_tol=1e-12)
    return retained,error,projected


class SameMath03Base(Scene):
    wide=False

    def setup(self):
        self.fw=16 if self.wide else 9
        self.top=3.55 if self.wide else 6.8
        self.caption_y=-3.75 if self.wide else -6.6
        self.center=np.array([-2.65,.05,0]) if self.wide else np.array([0,1.55,0])
        self.scale=.74 if self.wide else .72

    def fit(self,obj,width=None):
        limit=width or self.fw-1
        if obj.width>limit:obj.scale_to_fit_width(limit)
        return obj

    def title(self,name,kicker):
        a=txt(kicker,21 if self.wide else 23,GOLD).move_to([0,self.top,0])
        b=txt(name,32 if self.wide else 29).next_to(a,DOWN,buff=.18)
        self.fit(b)
        return VGroup(a,b)

    def spot(self,obj,y=-1.7,x=3.35):
        obj.move_to([x if self.wide else 0,y if self.wide else y-1.35,0])
        self.fit(obj,6.3 if self.wide else 7.6)
        return obj

    def plot(self,theta,projections=True,residuals=False,pc_mark=False):
        _,_,projected=metric(theta)
        v=np.array([math.cos(theta),math.sin(theta)])
        origin=self.center;scale=self.scale
        p=lambda a:origin+np.array([a[0]*scale,a[1]*scale,0])
        axes=VGroup(Line(p([-4.1,0]),p([4.1,0]),color=EDGE,stroke_width=1),
                    Line(p([0,-3.0]),p([0,3.0]),color=EDGE,stroke_width=1))
        axis=Line(p(-4.15*v),p(4.15*v),color=KEEP,stroke_width=4)
        originals=VGroup(*[Dot(p(x),radius=.045 if self.wide else .055,color=RAW,
                                fill_opacity=.75) for x in X])
        parts=[axes,axis,originals]
        if residuals:
            parts.append(VGroup(*[Line(p(a),p(b),color=LOSS,stroke_width=2,
                                       stroke_opacity=.62) for a,b in zip(projected,X)]))
        if projections:
            parts.append(VGroup(*[Dot(p(x),radius=.046 if self.wide else .056,
                                       color=KEEP) for x in projected]))
        if pc_mark:
            label=txt('PC1',20,KEEP).move_to(p(3.3*v)+UP*.28)
            parts.append(label)
        return VGroup(*parts)

    def meter(self,theta,heading='보존량 + 복원 오차 = 전체',numbers=True):
        retained,error,_=metric(theta)
        ratio=retained/TOTAL
        width=5.25 if self.wide else 6.8
        line=VGroup(Rectangle(width=width*ratio,height=.24,stroke_width=0,
                              fill_color=KEEP,fill_opacity=1),
                    Rectangle(width=width*(1-ratio),height=.24,stroke_width=0,
                              fill_color=LOSS,fill_opacity=1)).arrange(RIGHT,buff=0)
        frame=Rectangle(width=width,height=.24,stroke_color=INK,stroke_width=1)
        frame.move_to(line)
        labels=VGroup(txt(f'보존 {ratio*100:.1f}%',21,KEEP),
                      txt(f'오차 {(1-ratio)*100:.1f}%',21,LOSS)).arrange(RIGHT,buff=.5)
        if numbers:labels.add(txt('합계 100%',20,GOLD));labels.arrange(RIGHT,buff=.5)
        group=VGroup(txt(heading,22,GOLD),VGroup(line,frame),labels).arrange(DOWN,buff=.19)
        group.move_to([3.35,-.35,0] if self.wide else [0,-2.55,0])
        self.fit(group,6.3 if self.wide else 7.7)
        return group

    def triangle(self,theta):
        x=np.array([2.55,1.55])
        v=np.array([math.cos(theta),math.sin(theta)])
        q=float(x@v)*v
        origin=np.array([-2.4,0,0]) if self.wide else np.array([-.9,1.25,0])
        scale=1.05 if self.wide else 1.2
        p=lambda a:origin+np.array([a[0]*scale,a[1]*scale,0])
        base=Line(p(-3.1*v),p(3.1*v),color=KEEP,stroke_width=2,stroke_opacity=.6)
        whole=Arrow(p([0,0]),p(x),buff=0,color=RAW,stroke_width=5)
        kept=Arrow(p([0,0]),p(q),buff=0,color=KEEP,stroke_width=6)
        lost=Arrow(p(q),p(x),buff=0,color=LOSS,stroke_width=6)
        mark=Dot(p(q),color=GOLD,radius=.07)
        labels=VGroup(txt('x',24,RAW).next_to(whole.get_end(),UP,buff=.1),
                      txt('보존',22,KEEP).next_to(kept,DOWN,buff=.15),
                      txt('오차',22,LOSS).next_to(lost,RIGHT,buff=.15))
        return VGroup(base,whole,kept,lost,mark,labels)

    def panel(self,lines,y=None,wide_y=0):
        group=VGroup(*[txt(s,25 if self.wide else 24,c) for s,c in lines]).arrange(DOWN,buff=.24)
        group.move_to([3.4,wide_y,0] if self.wide else [0,-2.4 if y is None else y,0])
        self.fit(group,6.5 if self.wide else 7.5)
        return group

    def phase_scene(self,i):
        if i==0:
            h=self.title('같은 데이터, 다른 목표','두 최적화 문제')
            top=VGroup(txt('분산 최대화',29,KEEP),
                       colored([(r'\max_{\|v\|=1}',KEEP),(r'\|Xv\|^2',GOLD)],39)).arrange(DOWN,buff=.3)
            bottom=VGroup(txt('복원 오차 최소화',29,LOSS),
                          colored([(r'\min_{\|v\|=1}',LOSS),(r'\|X-Xvv^T\|_F^2',GOLD)],36)).arrange(DOWN,buff=.3)
            both=VGroup(top,bottom).arrange(DOWN,buff=.65 if self.wide else 1.4).move_to([0,-.15 if self.wide else .3,0])
            self.fit(both)
            return VGroup(h,both)
        if i in (1,2,3,4,5,8,9,10,11):
            initial={1:PC_ANGLE+.35,2:PC_ANGLE+.45,3:PC_ANGLE,4:PC_ANGLE,
                     5:PC_ANGLE+.8,8:PC_ANGLE+.5,9:PC_ANGLE+.85,
                     10:PC_ANGLE,11:PC_ANGLE}[i]
            self.theta=ValueTracker(initial)
        if i==1:
            h=self.title('2차원 점을 직선 위의 좌표 하나로','직교투영')
            g=always_redraw(lambda:self.plot(self.theta.get_value()))
            info=self.panel([('원본 데이터 xᵢ',RAW),('투영 좌표 zᵢ = xᵢ·v',KEEP),('단위 방향 v를 따라 1차원으로',GOLD)])
            return VGroup(h,g,info)
        if i==2:
            h=self.title('방향이 달라지면 남는 분산도 달라진다','투영 방향')
            g=always_redraw(lambda:self.plot(self.theta.get_value()))
            m=always_redraw(lambda:self.meter(self.theta.get_value(),'투영 방향에 따른 제곱 길이'))
            return VGroup(h,g,m)
        if i==3:
            h=self.title('가장 넓게 퍼지는 방향','분산 최대화')
            g=self.plot(PC_ANGLE,pc_mark=True)
            f=colored([(r'\max_{\|v\|=1}',KEEP),(r'\|Xv\|^2',GOLD)],42)
            self.spot(f,y=-1.2)
            note=self.panel([('X: 중심화된 데이터',RAW),('v: 길이가 1인 투영 방향',KEEP),('PC1: 분산이 최대인 방향',GOLD)],y=-3.5,wide_y=1.0)
            return VGroup(h,g,f,note)
        if i==4:
            h=self.title('투영점과 원래 점 사이의 차이','복원 오차')
            g=self.plot(PC_ANGLE,residuals=True)
            f=colored([(r'\hat x_i=(x_i^Tv)v',KEEP)],37)
            e=colored([(r'e_i=x_i-\hat x_i',LOSS)],39)
            form=VGroup(f,e).arrange(DOWN,buff=.4)
            self.spot(form,y=-1.1)
            note=self.panel([('청록색: 투영된 위치',KEEP),('주황색: 버려지는 오차',LOSS)],y=-3.5,wide_y=1.1)
            return VGroup(h,g,form,note)
        if i==5:
            h=self.title('오차가 최소인 방향은 어디일까?','복원 오차 최소화')
            g=always_redraw(lambda:self.plot(self.theta.get_value(),residuals=True))
            m=always_redraw(lambda:self.meter(self.theta.get_value(),'전체 제곱오차를 비교'))
            return VGroup(h,g,m)
        if i==6:
            h=self.title('한 벡터가 두 수직 성분으로 나뉜다','피타고라스 정리')
            self.theta=ValueTracker(PC_ANGLE+.25)
            tri=always_redraw(lambda:self.triangle(self.theta.get_value()))
            note=self.panel([('원래 벡터 x',RAW),('직선에 남긴 성분',KEEP),('수직으로 버린 성분',LOSS)])
            return VGroup(h,tri,note)
        if i==7:
            h=self.title('남긴 길이² + 버린 길이² = 원래 길이²','직교 분해')
            tri=self.triangle(PC_ANGLE+.25)
            f=colored([(r'\|x\|^2',RAW),('=',INK),(r'\|\hat x\|^2',KEEP),('+',INK),(r'\|x-\hat x\|^2',LOSS)],39)
            self.spot(f,y=-1.4)
            return VGroup(h,tri,f)
        if i==8:
            h=self.title('모든 점에도 같은 관계가 성립한다','전체 데이터')
            g=self.plot(self.theta.get_value(),residuals=True)
            f=colored([(r'\|X\|_F^2',RAW),('=',INK),(r'\|Xv\|^2',KEEP),('+',INK),
                       (r'\|X-Xvv^T\|_F^2',LOSS)],33)
            self.spot(f,y=-1.25)
            note=self.panel([('원래 데이터의 제곱 길이 합은 고정',GOLD)],y=-3.6)
            return VGroup(h,g,f,note)
        if i==9:
            h=self.title('하나의 고정된 양을 나누는 두 방법','같은 최적해')
            g=always_redraw(lambda:self.plot(self.theta.get_value(),residuals=True))
            m=always_redraw(lambda:self.meter(self.theta.get_value()))
            note=self.panel([('보존량 최대  ⇔  오차 최소',GOLD)],y=-4.35,wide_y=-2.0)
            return VGroup(h,g,m,note)
        if i==10:
            h=self.title('가장 큰 고유값의 방향이 PC1','고유값 문제')
            g=self.plot(PC_ANGLE,projections=False,pc_mark=True)
            f=colored([(r'X^TXv',KEEP),('=',INK),(r'\lambda v',GOLD)],43)
            self.spot(f,y=-1.0)
            note=self.panel([('λ: 방향별 분산의 크기',GOLD),('가장 큰 λ의 고유벡터 = PC1',KEEP)],y=-3.5)
            return VGroup(h,g,f,note)
        h=self.title('두 목표가 같아지는 조건','결론')
        g=self.plot(PC_ANGLE,residuals=True,pc_mark=True)
        statement=self.panel([('중심화된 데이터',RAW),('직교투영',KEEP),('제곱 복원 오차',LOSS)],y=-1.7)
        f=txt('분산 최대화  ⇔  복원 오차 최소화',27,GOLD)
        self.spot(f,y=-2.0)
        return VGroup(h,g,statement,f)

    def phase(self,t):
        for i,end in enumerate(ENDS):
            if t<end:return i
        return len(ENDS)-1

    def construct(self):
        footer=Rectangle(width=self.fw,height=1.43 if self.wide else 2.1,
                         fill_color=PANEL,fill_opacity=1,stroke_width=0)
        footer.move_to([0,-3.78 if self.wide else -6.9,0]).set_z_index(-5)
        rule=Line([-self.fw/2+.55,self.top-.9,0],[self.fw/2-.55,self.top-.9,0],
                  color=EDGE,stroke_width=1).set_z_index(-5)
        self.add(footer,rule)
        visual=None;caption=None;last=-1;start=0
        for end,sentence in DATA['sentences']:
            phase=self.phase(start);animations=[]
            if phase!=last:
                new=self.phase_scene(phase)
                if visual is not None:animations.append(FadeOut(visual))
                animations.append(FadeIn(new));visual=new;last=phase
            new_caption=VGroup(*[txt(s,25 if self.wide else 28) for s in wrap(sentence,44 if self.wide else 23)]).arrange(DOWN,buff=.11)
            self.fit(new_caption,self.fw-1)
            new_caption.move_to([0,self.caption_y,0])
            if caption is not None:animations.append(FadeOut(caption))
            animations.append(FadeIn(new_caption));caption=new_caption
            duration=end-start;intro=min(.35,duration*.23)
            self.play(*animations,run_time=intro)
            extra=0
            if phase==2 and start in (31,36):
                extra=min(2.1,duration-intro-.2)
                target=PC_ANGLE+math.pi/2 if start==31 else PC_ANGLE
                self.play(self.theta.animate.set_value(target),run_time=extra)
            elif phase==5 and start==67:
                extra=min(2.4,duration-intro-.2)
                self.play(self.theta.animate.set_value(PC_ANGLE),run_time=extra)
            elif phase==6 and start==82:
                extra=min(2,duration-intro-.2)
                self.play(self.theta.animate.set_value(PC_ANGLE+.55),run_time=extra)
            elif phase==9 and start==109:
                extra=min(2.5,duration-intro-.2)
                self.play(self.theta.animate.set_value(PC_ANGLE),run_time=extra)
            self.wait(duration-intro-extra)
            start=end


class SameMath03Short(SameMath03Base):
    pass


class SameMath03Long(SameMath03Base):
    wide=True
