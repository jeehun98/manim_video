"""Heat diffusion and Brownian position density, in two native layouts."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from manim import *

WIDE='SameMath02Long' in sys.argv
config.frame_width=16 if WIDE else 9
config.frame_height=9 if WIDE else 16
config.background_color='#101B2E'

DATA=json.loads((Path(__file__).parent/'script.json').read_text(encoding='utf-8'))
BG='#101B2E';PANEL='#17263D';EDGE='#344761';INK='#EEF4F8';MUTED='#A9BACC'
HEAT='#F59E45';PARTICLE='#38BDF8';COMMON='#2DD4BF';YELLOW='#F7D776';FONT='Malgun Gothic'
RNG=np.random.default_rng(20261111)
PARTICLES=RNG.normal(size=(115,2))
ENDS=(21,32,42,52,63,75,86,98,108,125,131,139,162,167,177)


def txt(s,size=28,color=INK):
    return Text(s,font=FONT,font_size=size,color=color)


def eq(s,size=43,color=INK):
    return MathTex(s,font_size=size,color=color)


def colored_eq(parts,size=43):
    result=MathTex(*[part for part,_ in parts],font_size=size)
    for piece,(_,color) in zip(result,parts):piece.set_color(color)
    return result


def wrap(s,limit):
    lines=[];line=''
    for word in s.split():
        test=(line+' '+word).strip()
        if len(test)>limit and line:
            lines.append(line);line=word
        else:line=test
    if line:lines.append(line)
    return lines


def gaussian(x,sigma):
    return math.exp(-x*x/(2*sigma*sigma))/sigma


class SameMath02Base(Scene):
    wide=False

    def setup(self):
        self.fw=16 if self.wide else 9
        self.top=3.55 if self.wide else 6.8
        self.caption_y=-3.75 if self.wide else -6.6
        self.mid=.25 if self.wide else .55

    def title(self,title,kicker):
        a=txt(kicker,21 if self.wide else 23,YELLOW).move_to([0,self.top,0])
        b=txt(title,32 if self.wide else 29).next_to(a,DOWN,buff=.18)
        if b.width>self.fw-1:b.scale_to_fit_width(self.fw-1)
        return VGroup(a,b)

    def fit(self,obj,width=None):
        limit=width or self.fw-1
        if obj.width>limit:obj.scale_to_fit_width(limit)
        return obj

    def heat_graph(self,t=0,bar=True,width=None,height=None):
        width=width or (6.4 if self.wide else 6.1)
        height=height or (2.3 if self.wide else 3.25)
        ax=Axes(x_range=[-3,3,1],y_range=[0,1.6,.4],x_length=width,y_length=height,
                axis_config={'color':MUTED,'stroke_width':2,'include_tip':False})
        sigma=math.sqrt(.56**2+2*.22*t)
        curve=ax.plot(lambda x:.12+.62*gaussian(x,sigma),x_range=[-3,3],color=HEAT,stroke_width=5)
        objects=[ax,curve]
        if bar:
            strips=VGroup()
            for j in range(30):
                x=-2.9+(j+.5)*5.8/30
                intensity=min(1,gaussian(x,sigma)*.56)
                color=interpolate_color(BLUE,ManimColor(HEAT),intensity)
                rect=Rectangle(width=width/30+.004,height=.32,stroke_width=0,fill_color=color,fill_opacity=1)
                rect.move_to(ax.c2p(x,1.45))
                strips.add(rect)
            objects.append(strips)
        return VGroup(*objects).move_to([0,self.mid,0])

    def tangent(self,graph,x,t=.8):
        ax=graph[0];sigma=math.sqrt(.56**2+2*.22*t)
        y=.12+.62*gaussian(x,sigma)
        slope=-x/(sigma*sigma)*.62*gaussian(x,sigma)
        dx=.45
        a=ax.c2p(x-dx,y-dx*slope);b=ax.c2p(x+dx,y+dx*slope)
        return VGroup(Line(a,b,color=COMMON,stroke_width=4),Dot(ax.c2p(x,y),color=YELLOW,radius=.075))

    def brownian_card(self,extent=1,compact=False):
        # A fixed collision field and a short, advancing sample path keep the
        # random motion legible without implying that the gray particles move.
        width=(4.55 if self.wide else 5.65) if compact else (7.0 if self.wide else 6.65)
        height=(2.15 if self.wide else 2.55) if compact else (3.6 if self.wide else 4.55)
        frame=RoundedRectangle(corner_radius=.2,width=width,height=height,
                               stroke_color='#3B4654',stroke_width=1.4,
                               fill_color='#080C12',fill_opacity=1)
        field=[(-.78,.65),(-.48,.72),(-.15,.77),(.52,.68),(.83,.49),
               (-.77,.13),(.77,.14),(-.79,-.44),(-.43,-.67),(.06,-.74),
               (.64,-.60),(.86,-.19)]
        dots=VGroup(*[Dot([x*width*.47,y*height*.46,0],radius=.046 if compact else .065,
                          color='#586575',fill_opacity=.7) for x,y in field])
        steps=[(-.56,-.15),(-.22,.03),(-.36,.38),(.05,.12),(.22,.55),
               (.43,.22),(.64,.35),(.76,.05)]
        end=max(2,min(len(steps),round(extent*(len(steps)-1))+1))
        coords=[np.array([x*width*.47,y*height*.44,0]) for x,y in steps[:end]]
        trail=VGroup(*[Line(a,b,color=PARTICLE,stroke_width=4.2 if compact else 5.5)
                       for a,b in zip(coords,coords[1:])])
        current=Dot(coords[-1],color=PARTICLE,radius=.14 if compact else .18)
        return VGroup(frame,dots,trail,current)

    def derivative_view(self,order,x_mark=-1.25):
        sigma=math.sqrt(.56**2+2*.22*.8)
        width=6.3 if self.wide else 6.0
        height=1.48 if self.wide else 1.83
        top_axes=Axes(x_range=[-3,3,1],y_range=[0,1.5,.5],x_length=width,y_length=height,
                      axis_config={'color':MUTED,'stroke_width':2,'include_tip':False})
        bottom_axes=Axes(x_range=[-3,3,1],y_range=[-1,1,.5],x_length=width,y_length=height,
                         axis_config={'color':MUTED,'stroke_width':2,'include_tip':False})
        top_axes.move_to([0,1.12 if self.wide else 2.1,0])
        bottom_axes.move_to([0,-.72 if self.wide else -.65,0])
        base=lambda x:.62*gaussian(x,sigma)
        deriv=(lambda x:-x/(sigma*sigma)*base(x)) if order==1 else (lambda x:(x*x/sigma**4-1/sigma**2)*base(x))
        upper=top_axes.plot(lambda x:.12+base(x),x_range=[-3,3],color=HEAT,stroke_width=4)
        lower=bottom_axes.plot(deriv,x_range=[-3,3],color=COMMON,stroke_width=4)
        top_dot=Dot(top_axes.c2p(x_mark,.12+base(x_mark)),color=YELLOW,radius=.07)
        bottom_dot=Dot(bottom_axes.c2p(x_mark,deriv(x_mark)),color=YELLOW,radius=.07)
        guide=DashedLine(top_dot.get_center(),bottom_dot.get_center(),color=YELLOW,dash_length=.07,stroke_opacity=.55)
        captions=VGroup(txt('온도 T(x)',19,HEAT).move_to([-4.35 if self.wide else -2.3,1.95 if self.wide else 3.35,0]),
                        txt('기울기 Tₓ(x)' if order==1 else '기울기 변화 Tₓₓ(x)',19,COMMON).move_to([-4.35 if self.wide else -1.65,.15 if self.wide else .55,0]))
        return VGroup(top_axes,bottom_axes,upper,lower,guide,top_dot,bottom_dot,captions)

    def legend(self,items,y=None,stacked=False):
        chips=[]
        for symbol,meaning,color in items:
            words=VGroup(txt(symbol,20 if self.wide else 21,color),txt(meaning,20 if self.wide else 21,INK)).arrange(RIGHT,buff=.12)
            chips.append(words)
        if stacked:
            group=VGroup(*chips).arrange(DOWN,buff=.11)
        elif self.wide:
            group=VGroup(*chips).arrange(RIGHT,buff=.42)
        else:
            rows=[VGroup(*chips[i:i+2]).arrange(RIGHT,buff=.42) for i in range(0,len(chips),2)]
            group=VGroup(*rows).arrange(DOWN,buff=.17)
        self.fit(group,self.fw-1.0)
        group.move_to([0,(-1.55 if self.wide else -4.55) if y is None else y,0])
        return group

    def cloud(self,spread=.22):
        scale_x=2.2 if self.wide else 1.75
        scale_y=1.25 if self.wide else 1.55
        dots=VGroup(*[Dot([float(x)*spread*scale_x,float(y)*spread*scale_y+self.mid,0],
                          color=PARTICLE,radius=.035 if self.wide else .043,fill_opacity=.85)
                       for x,y in PARTICLES])
        return dots

    def density_graph(self,sigma=.9,hist=False):
        ax=Axes(x_range=[-3,3,1],y_range=[0,1.5,.5],x_length=6.9 if self.wide else 6.1,
                y_length=2.6 if self.wide else 3.3,
                axis_config={'color':MUTED,'stroke_width':2,'include_tip':False})
        curve=ax.plot(lambda x:.75*gaussian(x,sigma),x_range=[-3,3],color=PARTICLE,stroke_width=5)
        bars=VGroup()
        if hist:
            counts,_=np.histogram(PARTICLES[:,0],bins=14,range=(-3,3),density=True)
            for i,c in enumerate(counts):
                x=-3+(i+.5)*6/14
                h=min(1.2,float(c)*1.9)
                bar=Rectangle(width=ax.x_length/14-.035,height=max(.02,h*ax.y_length/1.5),
                              stroke_width=0,fill_color=PARTICLE,fill_opacity=.33)
                bar.move_to(ax.c2p(x,h/2))
                bars.add(bar)
        return VGroup(ax,bars,curve).move_to([0,self.mid,0])

    def paired(self,left,right,left_color=HEAT,right_color=PARTICLE):
        if self.wide:
            left.move_to([-3.5,.1,0]);right.move_to([3.5,.1,0])
        else:
            left.move_to([0,1.7,0]);right.move_to([0,-1.5,0])
        return VGroup(left,right)

    def scene_for(self,i):
        if i==0:
            h=self.title('열과 무작위 운동','두 현상')
            hot=VGroup(txt('열의 확산',25,HEAT),self.heat_graph(t=0,width=4.5 if self.wide else 5.6,height=1.5 if self.wide else 2.1)).arrange(DOWN,buff=.25)
            walk=VGroup(txt('브라운 운동',25,PARTICLE),self.brownian_card(.08,compact=True)).arrange(DOWN,buff=.25)
            return VGroup(h,self.paired(hot,walk))
        if i==1:
            h=self.title('열이 퍼지면 봉우리가 낮아진다','열의 확산')
            g=self.heat_graph(t=0)
            f=colored_eq([(r'\partial_t T',HEAT),('=',INK),(r'\alpha',YELLOW),(r'\partial_{xx}T',COMMON)],42).move_to([0,-2.45 if self.wide else -3.35,0])
            note=self.legend([('∂ₜT','시간에 따른 온도 변화',HEAT),('α','열확산계수',YELLOW),('∂ₓₓT','기울기의 공간 변화',COMMON)],y=-1.55 if self.wide else -4.55)
            return VGroup(h,g,f,note)
        if i==2:
            h=self.title('일차 미분은 공간의 기울기','열방정식 ①')
            g=self.derivative_view(1,-1.4)
            f=colored_eq([(r'\partial_x',COMMON),(r'T',HEAT)],49).move_to([0,-2.3 if self.wide else -3.45,0])
            note=self.legend([('∂ₓ','위치에 따른 미분',COMMON),('T','온도',HEAT)],y=2.26 if self.wide else -4.55)
            return VGroup(h,g,f,note)
        if i==3:
            h=self.title('이차 미분은 기울기의 변화','열방정식 ②')
            g=self.derivative_view(2,-1.4)
            f=colored_eq([(r'\partial_{xx}T',COMMON),('=',INK),(r'\partial_x(\partial_xT)',YELLOW)],41).move_to([0,-2.3 if self.wide else -3.45,0]);self.fit(f)
            note=self.legend([('∂ₓₓT','기울기의 공간 변화',COMMON),('∂ₓ(∂ₓT)','기울기를 다시 미분',YELLOW)],y=2.26 if self.wide else -4.55)
            return VGroup(h,g,f,note)
        if i==4:
            h=self.title('봉우리는 내려가고 골짜기는 올라간다','이차 미분의 부호')
            ax=Axes(x_range=[-3,3,1],y_range=[0,1.7,.5],x_length=7 if self.wide else 6.1,
                    y_length=2.7 if self.wide else 3.7,axis_config={'color':MUTED,'include_tip':False})
            curve=ax.plot(lambda x:.18+.9*math.exp(-(x+1.3)**2/.35)+.85*math.exp(-(x-1.3)**2/.4),x_range=[-3,3],color=HEAT,stroke_width=5)
            graph=VGroup(ax,curve).move_to([0,self.mid,0])
            mark=VGroup(eq(r'T_{xx}<0\ \Rightarrow\ T_t<0',36,HEAT),eq(r'T_{xx}>0\ \Rightarrow\ T_t>0',36,COMMON)).arrange(DOWN,buff=.25)
            mark.move_to([0,-2.28 if self.wide else -3.45,0]);self.fit(mark)
            note=self.legend([('Tₓₓ','기울기의 변화',COMMON),('Tₜ','시간에 따른 온도 변화',HEAT)],y=-1.35 if self.wide else -4.7)
            return VGroup(h,graph,mark,note)
        if i==5:
            h=self.title('한 입자의 경로는 불규칙하다','브라운 운동')
            path=self.brownian_card(.08)
            path.move_to([0,.2 if self.wide else .55,0])
            note=txt('회색 점: 주변 입자  /  청록색 선: 이동 경로  /  큰 점: 현재 위치',23,PARTICLE).move_to([0,-2.3 if self.wide else -3.75,0]);self.fit(note)
            return VGroup(h,path,note)
        if i==6:
            h=self.title('같이 출발해도 서로 다른 곳으로','입자들의 확산')
            cloud=self.cloud(.16)
            note=txt('하나의 출발점  →  넓어지는 입자군',27,PARTICLE).move_to([0,-2.5 if self.wide else -3.8,0]);self.fit(note)
            return VGroup(h,cloud,note)
        if i==7:
            h=self.title('입자의 위치에서 확률밀도로','많은 입자')
            g=self.density_graph(hist=True)
            g[2].set_opacity(0)
            f=colored_eq([(r'p',PARTICLE),(r'(x,t)',YELLOW)],48).move_to([0,-2.45 if self.wide else -3.5,0])
            note=self.legend([('p','위치 확률밀도',PARTICLE),('(x,t)','위치와 시간',YELLOW)])
            return VGroup(h,g,f,note)
        if i==8:
            h=self.title('변하는 것은 달라도 식의 형태는 같다','두 확산방정식')
            a=VGroup(txt('온도',25,HEAT),colored_eq([(r'\partial_tT',HEAT),('=',INK),(r'\alpha',YELLOW),(r'\partial_{xx}T',COMMON)],40)).arrange(DOWN,buff=.25)
            b=VGroup(txt('위치 확률밀도',25,PARTICLE),colored_eq([(r'\partial_tp',PARTICLE),('=',INK),(r'D_B',YELLOW),(r'\partial_{xx}p',COMMON)],40)).arrange(DOWN,buff=.25)
            pair=self.paired(a,b);self.fit(pair)
            note=self.legend([('T','온도',HEAT),('p','확률밀도',PARTICLE),('α·D_B','각각의 확산계수',YELLOW),('∂ₓₓ','공간적 이차 미분',COMMON)],y=-1.85 if self.wide else -4.5)
            return VGroup(h,pair,note)
        if i==9:
            h=self.title('높은 곳에서 낮은 곳으로 흐른다','공통 구조 ①')
            a=VGroup(txt('열',25,HEAT),colored_eq([(r'J_T',HEAT),('=',INK),(r'-k',YELLOW),(r'\partial_xT',COMMON)],41)).arrange(DOWN,buff=.3)
            b=VGroup(txt('확률',25,PARTICLE),colored_eq([(r'J_p',PARTICLE),('=',INK),(r'-D_B',YELLOW),(r'\partial_xp',COMMON)],41)).arrange(DOWN,buff=.3)
            pair=self.paired(a,b)
            arrows=VGroup(Arrow([-1.2,0,0],[-2.8,0,0],color=COMMON,buff=0),Arrow([1.2,0,0],[2.8,0,0],color=COMMON,buff=0))
            arrows.move_to([0,-2.0 if self.wide else -3.5,0])
            if not self.wide:arrows.scale(.8)
            note=self.legend([('J_T','열유속',HEAT),('J_p','확률 흐름',PARTICLE),('−k, −D_B','기울기 반대 방향의 흐름',YELLOW),('∂ₓT, ∂ₓp','공간 기울기',COMMON)],y=2.2 if self.wide else -4.75)
            return VGroup(h,pair,arrows,note)
        if i==10:
            h=self.title('나간 양이 더 크면 안에 남은 양은 감소','공통 구조 ②')
            box=Rectangle(width=3.7,height=1.7,stroke_color=COMMON,fill_color=COMMON,fill_opacity=.12)
            box.move_to([0,.25 if self.wide else .55,0])
            left=Arrow([-4 if self.wide else -3.4,box.get_y(),0],box.get_left(),color=PARTICLE,buff=0,stroke_width=5)
            right=Arrow(box.get_right(),[4.8 if self.wide else 3.8,box.get_y(),0],color=HEAT,buff=0,stroke_width=7)
            labels=VGroup(txt('유입',23,PARTICLE).next_to(left,UP),txt('유출',23,HEAT).next_to(right,UP))
            f=colored_eq([(r'\partial_tu',HEAT),('=',INK),(r'-\partial_xJ',COMMON)],45).move_to([0,-2.2 if self.wide else -3.3,0])
            note=self.legend([('∂ₜu','영역 안의 양이 변하는 속도',HEAT),('−∂ₓJ','흐름의 공간 변화',COMMON)],y=-1.35 if self.wide else -4.55)
            return VGroup(h,box,left,right,labels,f,note)
        if i==11:
            h=self.title('흐름 + 보존 = 확산방정식','같은 수학')
            a=colored_eq([(r'J',PARTICLE),('=',INK),(r'-D',YELLOW),(r'\partial_xu',COMMON)],39)
            b=colored_eq([(r'\partial_tu',HEAT),('=',INK),(r'-\partial_xJ',COMMON)],39)
            c=colored_eq([(r'\partial_tu',HEAT),('=',INK),(r'-\partial_x(-D\partial_xu)',COMMON)],38)
            d=colored_eq([(r'\partial_tu',HEAT),('=',INK),(r'D',YELLOW),(r'\partial_{xx}u',COMMON)],47)
            stack=VGroup(a,b,c,d).arrange(DOWN,buff=.35 if self.wide else .48).move_to([0,.55 if self.wide else 1.05,0])
            self.fit(stack)
            b.set_opacity(0);c.set_opacity(0);d.set_opacity(0)
            note=self.legend([('u','보존되는 양',HEAT),('J','흐름',PARTICLE),('D','일정한 확산계수',YELLOW),('∂ₓₓ','기울기의 공간 변화',COMMON)],y=-2.25 if self.wide else -3.45)
            return VGroup(h,stack,note)
        if i==12:
            h=self.title('두 현상에 나타나는 가우시안 커널','공통된 해')
            ax=Axes(x_range=[-3,3,1],y_range=[0,1.5,.5],x_length=6.7 if self.wide else 6.0,
                    y_length=2.0 if self.wide else 3.2,axis_config={'color':MUTED,'include_tip':False})
            heat=ax.plot(lambda x:.6*gaussian(x,.56),x_range=[-3,3],color=HEAT,stroke_width=5)
            particle=ax.plot(lambda x:.6*gaussian(x,.56),x_range=[-3,3],color=PARTICLE,stroke_width=3)
            g=VGroup(ax,heat,particle).move_to([0,.95 if self.wide else 1.8,0])
            note=txt('정규화한 초과 온도  /  위치 확률밀도',24,COMMON).move_to([0,-.5 if self.wide else -.8,0]);self.fit(note)
            f=colored_eq([(r'G(x,t)',COMMON),('=',INK),(r'\frac{1}{\sqrt{4\pi Dt}}',YELLOW),
                          (r'e^{-x^2/(4Dt)}',PARTICLE)],38).next_to(note,DOWN,buff=.22);self.fit(f)
            meanings=self.legend([('G(x,t)','위치 x·시간 t의 커널',COMMON),
                                  ('1/√(4πDt)','D: 확산계수, 총량 정규화',YELLOW),
                                  ('e⁻ˣ²⁄⁴ᴰᵗ','x: 위치, 멀수록 감소',PARTICLE)],
                                 y=-2.45 if self.wide else -3.55,stacked=True)
            return VGroup(h,g,note,f,meanings)
        if i==13:
            h=self.title('확률적 확산은 AI에도 쓰인다','짧은 연결')
            circle=Circle(radius=.8 if self.wide else 1.15,color=COMMON,stroke_width=5).move_to([-2.5 if self.wide else 0,.4 if self.wide else 1.5,0])
            noise=VGroup(*[Dot([float(x)*1.2+(2.5 if self.wide else 0),float(y)*1.1+(.4 if self.wide else -1.3),0],color=PARTICLE,radius=.035) for x,y in PARTICLES[:65]])
            arrow=Arrow([-1, .4,0],[1,.4,0],color=YELLOW) if self.wide else Arrow([0,.2,0],[0,-.4,0],color=YELLOW)
            note=txt('노이즈 추가  →  학습된 역방향 과정',25,COMMON).move_to([0,-2.4 if self.wide else -4.0,0]);self.fit(note)
            return VGroup(h,circle,noise,arrow,note)
        h=self.title('흐름과 보존이 같은 구조를 만든다','결론')
        a=txt('열의 확산',27,HEAT);b=txt('입자의 확산',27,PARTICLE)
        pair=self.paired(a,b)
        pair.move_to([0,1.25 if self.wide else 2.0,0])
        if not self.wide:pair.arrange(RIGHT,buff=.75).move_to([0,2.0,0])
        f=colored_eq([(r'\partial_tu',HEAT),('=',INK),(r'D',YELLOW),(r'\partial_{xx}u',COMMON)],48).move_to([0,.15 if self.wide else .45,0]);self.fit(f)
        g=txt('서로 다른 문제, 같은 수학',24,YELLOW).move_to([0,-2.55 if self.wide else -3.6,0])
        meanings=self.legend([('∂ₜu','u: 온도·밀도의 시간 변화',HEAT),
                              ('D','확산계수',YELLOW),('∂ₓₓu','x: 위치에 따른 기울기의 변화',COMMON)],
                             y=-1.25 if self.wide else -1.85,stacked=True)
        return VGroup(h,pair,f,g,meanings)

    def phase(self,t):
        for i,end in enumerate(ENDS):
            if t<end:return i
        return 14

    def construct(self):
        footer=Rectangle(width=self.fw,height=1.43 if self.wide else 2.1,fill_color=PANEL,fill_opacity=1,stroke_width=0)
        footer.move_to([0,-3.78 if self.wide else -6.9,0]).set_z_index(-5)
        rule=Line([-self.fw/2+.55,self.top-.9,0],[self.fw/2-.55,self.top-.9,0],color=EDGE,stroke_width=1).set_z_index(-5)
        self.add(footer,rule)
        visual=None;caption=None;last=-1;start=0
        for end,sentence in DATA['sentences']:
            phase=self.phase(start);animations=[]
            if phase!=last:
                new=self.scene_for(phase)
                if visual is not None:animations.append(FadeOut(visual))
                animations.append(FadeIn(new));visual=new;last=phase
            lines=wrap(sentence,44 if self.wide else 23)
            new_caption=VGroup(*[txt(line,25 if self.wide else 28) for line in lines]).arrange(DOWN,buff=.11)
            self.fit(new_caption,self.fw-1)
            new_caption.move_to([0,self.caption_y,0])
            if caption is not None:animations.append(FadeOut(caption))
            animations.append(FadeIn(new_caption));caption=new_caption
            duration=end-start;intro=min(.35,duration*.23)
            self.play(*animations,run_time=intro)
            extra=0
            if phase==0 and start in (3,10):
                extra=1.6 if start==3 else 1.3
                heat_target=self.heat_graph(t=.55 if start==3 else 1.1,
                                            width=4.5 if self.wide else 5.6,height=1.5 if self.wide else 2.1)
                heat_target.move_to(visual[1][0][1].get_center())
                walk_target=self.brownian_card(.40 if start==3 else .70,compact=True)
                walk_target.move_to(visual[1][1][1].get_center())
                self.play(Transform(visual[1][0][1],heat_target),
                          Transform(visual[1][1][1],walk_target),run_time=extra)
            elif phase==1 and start==23:
                extra=1.6;self.play(Transform(visual[1],self.heat_graph(t=.8)),run_time=extra)
            elif phase==2 and start==35:
                extra=2.1;self.play(Transform(visual[1],self.derivative_view(1,1.4)),run_time=extra)
            elif phase==3 and start==47:
                extra=1.9;self.play(Transform(visual[1],self.derivative_view(2,1.4)),run_time=extra)
            elif phase==5 and start in (66,70):
                extra=1.6 if start==66 else 1.8
                walk_target=self.brownian_card(.65 if start==66 else 1.0)
                walk_target.move_to(visual[1].get_center())
                self.play(Transform(visual[1],walk_target),run_time=extra)
            elif phase==6 and start==79:
                extra=2.1;self.play(Transform(visual[1],self.cloud(1)),run_time=extra)
            elif phase==7 and start==91:
                extra=.9;self.play(visual[1][2].animate.set_opacity(1),run_time=extra)
            elif phase==11:
                extra=2.7
                self.play(visual[1][1].animate.set_opacity(1),run_time=.7)
                self.play(visual[1][2].animate.set_opacity(1),run_time=.9)
                self.play(visual[1][3].animate.set_opacity(1),run_time=1.1)
            elif phase==12 and start==149:
                extra=1.8
                target=self.scene_for(12)
                target[1][1].become(target[1][0].plot(lambda x:.6*gaussian(x,1.2),x_range=[-3,3],color=HEAT,stroke_width=5))
                target[1][2].become(target[1][0].plot(lambda x:.6*gaussian(x,1.2),x_range=[-3,3],color=PARTICLE,stroke_width=3))
                self.play(Transform(visual[1],target[1]),run_time=extra)
            if extra:self.add(visual)
            self.wait(duration-intro-extra)
            start=end


class SameMath02Short(SameMath02Base):
    pass


class SameMath02Long(SameMath02Base):
    wide=True
