"""Shared portrait layout and numerical illustrations; no LaTeX required."""
import os
import numpy as np
from manim import *
from episodes.svd_series.data import EPISODES

config.pixel_width = int(os.getenv('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#0B1220'
INK, MUTED = '#EDF2FA', '#93A5BF'
COLORS = ['#66D9EF', '#F6CA78', '#EF9DCA', '#8CE3BB']
BLUE, GOLD, PINK, GREEN = COLORS
H = np.array([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]) / 2
S = np.array([4., 2., 1., .3])
CHANNELS = [S[i] * np.outer(H[:,i], H[:,i]) for i in range(4)]
A = sum(CHANNELS)

def txt(s, size=28, color=INK, width=7.7):
    m = Text(str(s), font='Malgun Gothic', font_size=size, color=color, line_spacing=1.25)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m

def heat(a, width=2.8):
    cell = width / len(a)
    g = VGroup()
    for i,row in enumerate(a):
        for j,value in enumerate(row):
            g.add(Square(side_length=cell-.035, stroke_width=.5, stroke_color=MUTED,
                         fill_color=BLUE if value>=0 else PINK,
                         fill_opacity=.05+.9*abs(value)/2).move_to(
                             [(j-1.5)*cell,(1.5-i)*cell,0]))
    return g

def stack(lines, size=30):
    return VGroup(*[txt(s,size,c) for s,c in lines]).arrange(DOWN,buff=.45)

def arrow(start, end, color=BLUE):
    return Arrow(start,end,buff=0,color=color,stroke_width=4,
                 max_tip_length_to_length_ratio=.17)

class SVDEpisode(Scene):
    episode = 1

    def construct(self):
        title, segments = EPISODES[self.episode]
        total = sum(s[0] for s in segments)
        self.add(txt(f'SVD  /  {self.episode:02d} OF 05',20,MUTED).move_to(UP*7.25),
                 txt(title,36).move_to(UP*6.45),
                 Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        progress = Rectangle(width=.01,height=.035,fill_color=BLUE,fill_opacity=1,stroke_width=0).move_to([-3.8,-7.35,0])
        self.add(progress)
        previous = None
        elapsed = 0
        for index,(duration,heading,caption,formula,kind,value) in enumerate(segments):
            header = txt(heading,31).move_to(UP*5.15)
            note = txt(formula,25,GOLD).move_to(DOWN*4.65)
            sub = txt(caption,28).move_to(DOWN*6.1)
            if self.episode in (2,3,5) and sub.height > 1.5:
                sub.scale_to_fit_height(1.5)
            body = getattr(self,kind)(value)
            group = VGroup(header,note,sub,body)
            # Check layout in scene coordinates before spending time rendering.
            for label,obj in [('header',header),('formula',note),('caption',sub),('body',body)]:
                if obj.width > 8.25 or obj.get_top()[1] > 5.6 or obj.get_bottom()[1] < -6.9:
                    raise ValueError(f'Layout overflow: {self.episode}/{index}/{label}')
            if body.get_top()[1]>4.35 or body.get_bottom()[1]<-4.1:
                raise ValueError(f'Body overlaps text: {self.episode}/{index}')
            if previous is not None:
                self.play(FadeOut(previous,shift=UP*.12),run_time=.35)
            self.play(FadeIn(header),FadeIn(note),FadeIn(sub),
                      LaggedStart(*[FadeIn(m,shift=UP*.12) for m in body],lag_ratio=.12),run_time=1.4)
            self.add(group)
            self.animate_diagram(kind,value,body)
            elapsed += duration
            target_width = max(.01,7.6*elapsed/total)
            self.play(progress.animate.stretch_to_fit_width(target_width).move_to([-3.8+target_width/2,-7.35,0]),run_time=.3)
            self.wait(max(0,elapsed-self.time))
            if abs(self.time-elapsed)>.05:
                raise ValueError('Timeline drift')
            previous = group

    def animate_diagram(self,kind,value,body):
        if kind=='compare_errors':
            self.play(Circumscribe(body[1 if value==0 else 2],color=GREEN if value==0 else GOLD),run_time=1.6)
            if value==1:
                self.play(Indicate(body[-1],color=GREEN,scale_factor=1.06),run_time=1.2)
        elif kind=='pattern_weight':
            self.play(Circumscribe(body[0],color=BLUE),run_time=1.3)
            self.play(Circumscribe(body[1],color=GOLD),run_time=1.3)
        elif kind in ('difference','unit_difference'):
            # Differences are drawn relative to each panel's reference output.
            d1,d2 = body[-2],body[-1]
            self.play(d1.animate.shift(RIGHT*.65),
                      d2.animate.shift(np.array([.65*value*np.cos(.45),.65*value*np.sin(.45),0])),run_time=2)
            self.play(Indicate(d2,color=GOLD,scale_factor=1.35),run_time=.8)
        elif kind=='sensitivity':
            if value in (4,5):
                idx=2+(value-4)
                self.play(Indicate(body[0][idx],color=COLORS[value-4],scale_factor=1.08),
                          Indicate(body[1][idx],color=COLORS[value-4],scale_factor=1.08),run_time=1.4)
            elif value in (1,2):
                self.play(Indicate(body[1],color=GOLD,scale_factor=1.035),run_time=1.4)
            else:
                self.play(Indicate(body[-1],color=GOLD,scale_factor=1.06),run_time=1.4)
        elif kind=='rank':
            self.play(Circumscribe(body[1],color=GOLD),run_time=1.5)
        elif kind=='questions':
            self.play(LaggedStart(*[Indicate(m,scale_factor=1.03) for m in body],lag_ratio=.25),run_time=2)
        elif kind=='ellipse_response':
            if value in (1,2,3,7):
                self.play(body.theta.animate.set_value(TAU),run_time=4,rate_func=linear)
            elif value==0:
                self.play(body.theta.animate.set_value(PI/2),run_time=2,rate_func=linear)
            elif value==4:
                self.play(Indicate(body.upper,color=BLUE,scale_factor=1.08),run_time=1.8)
            elif value==5:
                self.play(Indicate(body.lower,color=GREEN,scale_factor=1.08),run_time=1.8)
            elif value==6:
                self.play(Indicate(body.middle,color=PINK,scale_factor=1.08),run_time=1.8)
            elif value==8:
                self.play(Indicate(body.trace,color=GOLD,scale_factor=1.025),run_time=1.1)
                self.play(Indicate(VGroup(body.upper,body.lower),color=GREEN,scale_factor=1.06),run_time=1.1)
        else:
            self.play(Indicate(body[-1],color=GOLD,scale_factor=1.04),run_time=1.4)

    def rank(self,k):
        approx=sum(CHANNELS[:k])
        original=VGroup(heat(A),txt('원래 행렬 A',25).move_to(UP*1.95)).move_to([-2.05,1.45,0])
        reduced=VGroup(heat(approx),txt(f'{k}개 패턴의 합',25,GOLD).move_to(UP*1.95)).move_to([2.05,1.45,0])
        bars=VGroup()
        for i,s in enumerate(S):
            x=-2.7+1.8*i
            b=Rectangle(width=.6,height=s*.55,stroke_width=0,fill_color=COLORS[i],fill_opacity=1 if i<k else .15).move_to([x,-2.3+s*.275,0])
            bars.add(b,txt(f'σ{i+1} = {s:g}',20,COLORS[i]).move_to([x,-2.75,0]))
        error=np.linalg.norm(A-approx,'fro')**2
        return VGroup(original,reduced,bars,txt(f'남긴 패턴 {k}/4     ·     제곱 오차 {error:.2f}',27).move_to(DOWN*3.65))

    def layers(self,k):
        rows=VGroup()
        for i in range(4):
            tile=heat(CHANNELS[i],1.1)
            label=txt(f'σ{i+1} = {S[i]:g}',27,COLORS[i])
            expression=txt('σ'+'₁₂₃₄'[i]+'u'+'₁₂₃₄'[i]+'v'+'₁₂₃₄'[i]+'ᵀ',25)
            row=VGroup(tile,label,expression).arrange(RIGHT,buff=.65).move_to([0,2.5-1.6*i,0])
            if k==1 and i==3: row.set_opacity(.25)
            rows.add(row)
        rows.add(txt('각 타일은 실제 Rank 1 행렬 · 색은 원소의 부호',20,MUTED).move_to(DOWN*3.65))
        return rows

    def pattern_weight(self,_):
        pattern=VGroup(heat(np.outer(H[:,0],H[:,0]),2),
                       txt('기본 Rank 1 패턴',26,BLUE).move_to(UP*1.65),
                       txt('u₁v₁ᵀ',32,BLUE).move_to(DOWN*1.5)).move_to([-2,1.5,0])
        weighted=VGroup(heat(CHANNELS[0],2),
                        txt('가중치를 곱한 패턴',26,GOLD).move_to(UP*1.65),
                        txt('σ₁u₁v₁ᵀ',32,GOLD).move_to(DOWN*1.5)).move_to([2,1.5,0])
        return VGroup(pattern,weighted,txt('× 4',28,GOLD).move_to([0,1.5,0]),
                      txt('‖u₁‖ = ‖v₁‖ = 1',28,BLUE).move_to(DOWN*1.1),
                      txt('σ₁ = 4 : 패턴의 세기를 조절하는 가중치',27,GOLD).move_to(DOWN*2.05),
                      txt('같은 색 척도 · 값이 4배가 되면 더 밝게',22,MUTED).move_to(DOWN*3.1))

    def compare_errors(self,stage):
        title=txt('남긴 항은 제외하고, 버린 항만 제곱해 더합니다',25).move_to(UP*3.65)
        panels=[]
        for row,keep in enumerate([0,1]):
            y=1.8-row*3.1
            color=GREEN if keep==0 else GOLD
            label=txt(f'{S[keep]:g}를 남김',28,color).move_to([-2.25,y+.8,0])
            terms=VGroup()
            for j,s in enumerate(S):
                term=txt(f'{s:g}²',32,COLORS[j]).move_to([-2.5+j*1.48,y,0])
                if j==keep:
                    term.set_opacity(.3)
                    terms.add(term,Line(term.get_left()+DOWN*.18,term.get_right()+UP*.18,color=MUTED,stroke_width=2))
                else:
                    terms.add(term)
            equation='2² + 1² + 0.3² = 5.09' if keep==0 else '4² + 1² + 0.3² = 17.09'
            result=txt(equation,30,color).move_to([0,y-.8,0])
            panel=VGroup(RoundedRectangle(width=7.35,height=2.6,corner_radius=.12,stroke_color=color,stroke_opacity=.45),label,terms,result)
            panel[0].move_to([0,y,0])
            if stage==0 and row==1:panel.set_opacity(.12)
            panels.append(panel)
        conclusion=txt('4를 남김: 5.09  <  2를 남김: 17.09',27,GREEN).move_to(DOWN*3.45)
        if stage==0:conclusion.set_opacity(0)
        return VGroup(title,*panels,conclusion)

    def choices(self,highlight):
        g=VGroup(txt('하나만 남겼을 때의 제곱 오차',28).move_to(UP*3.1))
        for i,s in enumerate(S):
            error=float(S@S-s*s);y=1.7-i*1.3
            g.add(txt(f'σ{i+1} = {s:g}',25,COLORS[i]).move_to([-2.8,y,0]),
                  Rectangle(width=error*.16,height=.4,fill_color=COLORS[i],fill_opacity=.8,stroke_width=0).move_to([-.95+error*.08,y,0]),
                  txt(f'{error:.2f}',25).move_to([3,y,0]))
        if highlight:g.add(SurroundingRectangle(VGroup(*g.submobjects[1:4]),color=GREEN,buff=.2))
        g.add(txt('작을수록 원래 행렬에 가깝습니다',25,GREEN).move_to(DOWN*3.55))
        return g

    def error(self,k):
        errors=[float(S[j:]@S[j:]) for j in range(5)]
        g=VGroup(txt('패턴 수를 늘리면 줄어드는 손실',28).move_to(UP*3.15))
        for j,e in enumerate(errors):
            y=1.8-j*1.05
            g.add(txt(f'k = {j}',24,GOLD if j==k else MUTED).move_to([-3,y,0]),
                  Line([-1.8,y,0],[-1.8+max(.025,e*.18),y,0],color=GOLD if j==k else BLUE,stroke_width=13),
                  txt(f'{e:.2f}',24).move_to([3,y,0]))
        g.add(txt('제곱 오차 = 버린 특잇값들의 제곱합',25,GOLD).move_to(DOWN*3.5))
        return g

    def unit_difference(self,gain):
        return self.difference(gain,unit=True)

    def difference(self,gain,unit=False):
        g=VGroup()
        base1=np.array([-1.2,2.,0]);base2=np.array([-1.2,-1.3,0])
        for center,label in [(base1,'입력 · x를 기준으로'),(base2,'출력 · Ax를 기준으로')]:
            g.add(RoundedRectangle(width=7,height=2.45,corner_radius=.15,stroke_color=MUTED,stroke_opacity=.4).move_to([0,center[1],0]),
                  txt(label,24,MUTED).move_to([0,center[1]+.85,0]),
                  Line(center+LEFT*.6,center+RIGHT*3.2,color=MUTED,stroke_opacity=.3),
                  Dot(center,color=INK,radius=.09))
        end1=base1+RIGHT*.65
        end2=base2+np.array([.65*gain*np.cos(.45),.65*gain*np.sin(.45),0])
        g.add(arrow(base1,end1,BLUE),txt('1' if unit else 'ε',23,BLUE).move_to(base1+np.array([.35,-.4,0])))
        if gain>0:g.add(arrow(base2,end2,GOLD))
        g.add(txt(f'σ = {gain:g}',34,GOLD).move_to([0,.25,0]),
              txt('차이 0 · 두 출력이 겹침' if gain==0 else
                  (f'입력 단위 변화 1 → 출력 변화 {gain:g}' if unit else f'출력 차이 = 입력 차이 × {gain:g}'),25,GOLD).move_to(DOWN*3.35))
        # These dots move from the reference point to the perturbed point.
        g.add(Dot(base1,color=BLUE,radius=.11),Dot(base2,color=GOLD,radius=.11))
        return g

    def gains(self,_):
        g=VGroup()
        for i,(s,label) in enumerate([(3,'잘 드러나는 차이'),(.2,'희미해지는 차이'),(0,'완전히 사라지는 차이')]):
            y=2.5-i*2.2
            g.add(txt(f'σ = {s:g}',32,COLORS[i]).move_to([-2.5,y,0]),
                  Line([-.8,y,0],[-.8+s,y,0],stroke_width=15,color=COLORS[i]) if s>0 else VGroup(),
                  txt(label,26).move_to([0,y-.75,0]))
        return g

    def sensitivity(self,stage):
        theta=.45
        rot=np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
        vrot=np.array([[np.cos(.6),-np.sin(.6)],[np.sin(.6),np.cos(.6)]])
        top=np.array([0,2.25,0]);bottom=np.array([0,-1.9,0]);scale=.85
        def pt(v,c):return c+np.array([v[0],v[1],0])*scale
        incoming=VGroup(Circle(radius=scale,color=BLUE,stroke_opacity=.4).move_to(top),txt('입력 · 길이 1',24,BLUE).move_to([0,3.65,0]))
        outgoing=VGroup(txt('출력 · 같은 좌표 척도',24,GOLD).move_to([0,-.35,0]))
        if stage:
            outgoing.add(ParametricFunction(lambda t:pt(rot@np.array([3*np.cos(t),.5*np.sin(t)]),bottom),t_range=[0,TAU],color=GOLD,stroke_opacity=.55))
        angles=np.linspace(0,TAU,12,endpoint=False) if stage<3 else [0,PI/2]
        if stage==6:angles=[0,PI/2,PI/4]
        for j,t in enumerate(angles):
            c=np.array([np.cos(t),np.sin(t)]);v=vrot@c
            color=COLORS[j%3] if stage>=3 else BLUE
            incoming.add(arrow(top,pt(v,top),color))
            if stage:
                outgoing.add(arrow(bottom,pt(rot@np.diag([3,.5])@c,bottom),color))
        if stage>=3:
            incoming.add(txt('v₁',22,BLUE).move_to(pt(vrot[:,0],top)+RIGHT*.35),txt('v₂',22,GOLD).move_to(pt(vrot[:,1],top)+LEFT*.35))
            outgoing.add(txt('3u₁',22,BLUE).move_to(pt(rot[:,0]*3,bottom)+UP*.3),txt('0.5u₂',22,GOLD).move_to(pt(rot[:,1]*.5,bottom)+LEFT*.65))
        return VGroup(incoming,outgoing,txt('↓  A',30,MUTED).move_to([0,.45,0]))

    def questions(self,stage):
        g=VGroup()
        coeff=[2.,-1.,.5] if stage!=7 else [0.,-1.,.5]
        if stage==3:coeff=[3.,-1.,.5]
        gains=[3.,1.5,.4]
        g.add(txt('입력 x → 직교하는 세 질문',29).move_to(UP*3.65))
        for i,(c,s) in enumerate(zip(coeff,gains)):
            y=2.15-i*1.8;idx='₁₂₃'[i];color=COLORS[i]
            panel=RoundedRectangle(width=7.2,height=1.4,corner_radius=.12,stroke_color=color,fill_color=color,fill_opacity=.06,stroke_opacity=.5).move_to([0,y,0])
            if stage==0:line=f'v{idx}ᵀx  →  × σ{idx}  →  u{idx}'
            elif stage<4:line=f'v{idx}ᵀx = {c:g}'.replace('-','−')
            elif stage==4:line=f'{c:g} × {s:g} = {c*s:g}'.replace('-','−')
            else:line=f'{c*s:g}u{idx}'.replace('-','−')
            g.add(VGroup(panel,txt(line,31,color).move_to([0,y,0])))
        if stage==3:label='v₁ 방향 성분만 +1 → 첫 답만 2에서 3으로'
        elif stage>=5:label='합계: 6u₁ − 1.5u₂ + 0.2u₃' if stage!=7 else '첫 답이 0 → 첫 채널의 기여도 0'
        elif stage==2:label='양수: 같은 방향   /   음수: 반대 방향'
        else:label='읽기 → 배율 적용 → 출력 패턴으로 조립'
        g.add(txt(label,24,GOLD).move_to(DOWN*3.35))
        return g

    def ellipse_response(self,stage):
        """A direction scanner records every response; singular values are its rails."""
        phi=.28
        rot=np.array([[np.cos(phi),-np.sin(phi)],[np.sin(phi),np.cos(phi)]])
        center=np.array([0,1.65,0]);scale=.82
        dial_center=np.array([-3.15,3.25,0]);dial_radius=.48
        initial={4:.001,5:PI/2,6:.72}.get(stage,.001)
        theta=ValueTracker(initial)

        def response(t):
            return float(np.sqrt(9*np.cos(t)**2+.25*np.sin(t)**2))
        def ellipse_point(t):
            p=rot@np.array([3*np.cos(t),.5*np.sin(t)])
            return center+np.array([p[0],p[1],0])*scale
        def dial_point(t):
            return dial_center+dial_radius*np.array([np.cos(t),np.sin(t),0])
        def gx(t):return -3.05+6.1*t/TAU
        def gy(length):return -3.05+1.62*(length-.5)/2.5
        def graph_point(t):return np.array([gx(t),gy(response(t)),0])

        dial=VGroup(Circle(radius=dial_radius,color=BLUE,stroke_opacity=.55).move_to(dial_center),
                    txt('단위 입력',20,BLUE).move_to(dial_center+UP*.78),
                    always_redraw(lambda:arrow(dial_center,dial_point(theta.get_value()),GREEN)),
                    always_redraw(lambda:Dot(dial_point(theta.get_value()),radius=.075,color=GREEN)))

        ellipse=ParametricFunction(ellipse_point,t_range=[0,TAU],color=GOLD,stroke_width=5)
        ray=always_redraw(lambda:arrow(center,ellipse_point(theta.get_value()),PINK))
        scan_dot=always_redraw(lambda:Dot(ellipse_point(theta.get_value()),radius=.105,color=PINK))
        output=VGroup(ellipse,
                      txt('출력점이 타원을 스캔',22,GOLD).move_to([0,3.55,0]),
                      txt('L(θ) = ‖Ax(θ)‖',22,PINK).move_to([0,.35,0]))
        if stage>=1:output.add(ray,scan_dot)
        if stage==0:output.set_opacity(.16)

        meter_x=3.25
        meter=VGroup(Line([meter_x,.75,0],[meter_x,3.25,0],color=MUTED,stroke_width=3),
                     txt('출력 길이',19,MUTED).move_to([meter_x,3.62,0]))
        if stage>=2:
            meter.add(always_redraw(lambda:Dot([meter_x,.75+(response(theta.get_value())-.5),0],radius=.09,color=PINK)))
        else:meter.set_opacity(0)

        axes=VGroup(Line([-3.2,-3.15,0],[3.35,-3.15,0],color=MUTED,stroke_opacity=.45),
                    Line([-3.2,-3.15,0],[-3.2,-1.25,0],color=MUTED,stroke_opacity=.45),
                    txt('0',18,MUTED).move_to([-3.2,-3.42,0]),
                    txt('2π',18,MUTED).move_to([3.15,-3.42,0]),
                    txt('입력 각도 θ',19,MUTED).move_to([0,-3.62,0]))
        trace=ParametricFunction(graph_point,t_range=[0,TAU],color=GOLD,stroke_width=4)
        moving_trace=always_redraw(lambda:ParametricFunction(
            graph_point,t_range=[0,max(.01,min(TAU,theta.get_value()))],color=GOLD,stroke_width=5))
        graph_dot=always_redraw(lambda:Dot(graph_point(theta.get_value()),radius=.085,color=PINK))
        graph=VGroup(axes,trace)
        if stage==3:graph=VGroup(axes,moving_trace,graph_dot)
        elif stage>=4:graph.add(graph_dot)
        else:graph.set_opacity(0)

        upper_line=Line([-3.2,gy(3),0],[3.35,gy(3),0],color=BLUE,stroke_width=3)
        upper=VGroup(upper_line,txt('σ₁ = 3  ·  위쪽 경계',20,BLUE).move_to([1.85,gy(3)+.24,0]))
        lower_line=Line([-3.2,gy(.5),0],[3.35,gy(.5),0],color=GREEN,stroke_width=3)
        lower=VGroup(lower_line,txt('σ₂ = 0.5  ·  아래쪽 경계',20,GREEN).move_to([1.65,gy(.5)+.24,0]))
        if stage<4:upper.set_opacity(0)
        if stage<5:lower.set_opacity(0)

        middle_t=.72
        middle=VGroup(Dot(graph_point(middle_t),radius=.1,color=PINK),
                      txt('일반 방향의 반응',20,PINK).move_to(graph_point(middle_t)+DOWN*.3))
        if stage!=6:middle.set_opacity(0)

        body=VGroup(dial,output,meter,graph,upper,lower,middle)
        body.theta=theta;body.upper=upper;body.lower=lower;body.middle=middle;body.trace=trace
        return body
