from pathlib import Path
from manim import *
import json

config.background_color = '#101923'
config.frame_width = 14.222222
config.frame_height = 8
FONT='Malgun Gothic'
INK, MUTED, BLUE, GOLD, PINK = '#EDF3F7','#94A7B7','#68D9F0','#F3CF75','#FF8C9D'
ASSETS=Path(__file__).resolve().parents[2]/'assets'

def text(s,size=28,color=INK,width=12):
    t=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.2)
    if t.width>width:t.scale_to_fit_width(width)
    return t

def cat(texture=False,height=3.5):
    c=ImageMobject(str(ASSETS/('cat_texture.png' if texture else 'cat_photo.png')))
    c.height=height
    return c

def photo(x=0,texture=False,color='#385563',width=3.8,height=3.8):
    bg=RoundedRectangle(width=width,height=height,corner_radius=.15,stroke_width=0,fill_color=color,fill_opacity=1)
    c=cat(texture,height-.25)
    return Group(bg,c).move_to([x,0,0])

def box(s,x,y,color=BLUE,w=2.6):
    b=RoundedRectangle(width=w,height=.95,corner_radius=.12,stroke_color=color,fill_color=color,fill_opacity=.08)
    return VGroup(b,text(s,25,color,w-.2)).move_to([x,y,0])

class Act04Intervention(ThreeDScene):
    def construct(self):
        ends=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))['ends']
        fixed=[]
        def play(*a,rt=.7):self.play(*a,run_time=round(rt*30)/30)
        def until(n):
            frames=round(ends[n-1]*30)-round(self.time*30)
            if frames<0:raise ValueError(f'Cue {n} overrun: {self.time} > {ends[n-1]}')
            if frames:self.wait(frames/30)
        def start(n):self.next_section(f'cue_{n:02}')
        def clear():
            if self.mobjects:play(*[FadeOut(m) for m in list(self.mobjects)],rt=.3)
            if fixed:self.remove_fixed_in_frame_mobjects(*fixed);fixed.clear()
        def heading(s):return text(s,30).move_to([0,3.35,0])
        def fixed_replace(old,new,*animations,rt=.7):
            self.add_fixed_in_frame_mobjects(new);fixed.append(new)
            play(FadeOut(old),FadeIn(new),*animations,rt=rt)
            self.remove_fixed_in_frame_mobjects(old);fixed.remove(old)
            return new
        def footer(s):return text(s,25).move_to([0,-3.3,0])
        def activation(x,height,color,name,base=-1.4):
            axis=Line([x-.7,base,0],[x+.7,base,0],color=MUTED)
            bar=Rectangle(width=.75,height=height,stroke_width=0,fill_color=color,fill_opacity=.9).move_to([x,base+height/2,0])
            t=text(name,22,color).move_to([x,base-.4,0])
            return VGroup(axis,bar,t)
        def score(x,y,w=2.65):
            bg=Rectangle(width=3,height=.24,stroke_width=0,fill_color='#293A49',fill_opacity=1).move_to([x,y,0])
            bar=Rectangle(width=w,height=.24,stroke_width=0,fill_color=BLUE,fill_opacity=1).align_to(bg,LEFT).set_y(y)
            return VGroup(bg,bar)
        def chart():
            axes=Axes(x_range=[0,3,.5],y_range=[0,1,.2],x_length=8,y_length=3.8,tips=False,
                      axis_config={'include_ticks':False,'color':MUTED}).shift(DOWN*.1)
            labels=VGroup(text('개입 크기 α',22,MUTED).move_to([0,-2.55,0]),
                          text('고양이 점수',22,MUTED).move_to([-5.55,1.3,0]))
            return axes,labels

        start(1)
        h=heading('04 / 큰 activation과, 중요한 activation')
        A=activation(-3,2.6,GOLD,'activation A');B=activation(1,.75,BLUE,'activation B')
        out=box('CAT',5,0,BLUE,w=2.1)
        links=VGroup(DashedLine(A.get_right(),out.get_left(),color=MUTED),DashedLine(B.get_right(),out.get_left(),color=MUTED))
        play(FadeIn(h),FadeIn(A),FadeIn(B),FadeIn(out),Create(links))
        play(Circumscribe(A[1],color=GOLD))
        q=footer('활성화 크기만 보면 A가 더 중요해 보입니다')
        play(FadeIn(q))
        until(1)

        start(2);clear()
        h=heading('입력과 가중치를 고정합니다')
        p=photo(x=-4.6,width=2.9,height=3.3)
        locks=VGroup(box('같은 사진',-4.6,-2.3,GOLD,w=2.9),box('가중치 고정',0,2.2,MUTED,w=3.8))
        A=activation(-1.4,2.6,GOLD,'A');B=activation(1.1,.75,BLUE,'B')
        s=score(4.7,.35);st=text('고양이 점수',22,BLUE).move_to([4.7,-.2,0])
        play(FadeIn(h),FadeIn(p),FadeIn(locks),FadeIn(A),FadeIn(B),FadeIn(s),FadeIn(st))
        until(2)

        start(3)
        play(Transform(h,heading('A의 값만 조금 낮춥니다')))
        oldA=DashedLine([-1.95,1.2,0],[-.85,1.2,0],color=GOLD)
        play(Create(oldA),A[1].animate.stretch_to_fit_height(2.25).align_to(A[0],DOWN))
        # Align bottom explicitly; baseline is y=-1.4, not the line's bounding box centre.
        play(A[1].animate.set_y(-1.4+2.25/2),rt=.3)
        until(3)

        start(4)
        play(s[1].animate.stretch_to_fit_width(2.55).align_to(s[0],LEFT),Transform(h,heading('A를 낮춰도 점수는 거의 유지된다면')))
        q=footer('큰 반응 A · 작은 판정 변화')
        play(FadeIn(q),Circumscribe(s,color=BLUE))
        until(4)

        start(5)
        play(A[1].animate.stretch_to_fit_height(2.6).set_y(-1.4+2.6/2),s[1].animate.stretch_to_fit_width(2.65).align_to(s[0],LEFT),
             FadeOut(oldA),FadeOut(q),Transform(h,heading('원래 상태로 돌아가, B만 낮춥니다')))
        play(B[1].animate.stretch_to_fit_height(.4).set_y(-1.4+.4/2))
        until(5)

        start(6)
        play(s[1].animate.stretch_to_fit_width(.9).align_to(s[0],LEFT),Transform(h,heading('B를 낮추자 점수가 크게 떨어진다면')))
        until(6)

        start(7)
        q=footer('작은 반응 B · 큰 판정 변화')
        play(FadeIn(q),Circumscribe(B[1],color=BLUE),Circumscribe(s[1],color=PINK))
        until(7)

        start(8);clear()
        h=heading('활성화의 크기와, 판정에 미치는 영향은 다릅니다')
        cols=VGroup(text('activation 크기',24,MUTED).move_to([-1.5,2.1,0]),text('개입 후 출력 변화',24,MUTED).move_to([3.5,2.1,0]))
        names=VGroup(box('A',-5,1,GOLD,w=1.3),box('B',-5,-1,BLUE,w=1.3))
        av=VGroup(Rectangle(width=3,height=.3,stroke_width=0,fill_color=GOLD,fill_opacity=.9).move_to([-1.5,1,0]),
                  Rectangle(width=.85,height=.3,stroke_width=0,fill_color=BLUE,fill_opacity=.9).move_to([-1.5,-1,0]))
        dv=VGroup(Rectangle(width=.35,height=.3,stroke_width=0,fill_color=GOLD,fill_opacity=.9).move_to([3.5,1,0]),
                  Rectangle(width=2.65,height=.3,stroke_width=0,fill_color=BLUE,fill_opacity=.9).move_to([3.5,-1,0]))
        play(FadeIn(h),FadeIn(cols),FadeIn(names),FadeIn(av),FadeIn(dv))
        play(Indicate(av[0]),Indicate(dv[1]))
        until(8)

        start(9)
        q=footer('값의 크기 → 바꾸었을 때의 출력 변화 Δs')
        play(FadeIn(q),Transform(h,heading('보고 싶은 것은 개입에 대한 반응입니다')))
        play(Circumscribe(dv,color=BLUE))
        until(9)

        start(10);clear()
        h=heading('내부 상태를 점으로, 개입을 방향으로 생각합니다')
        ax=Axes(x_range=[-2,2,1],y_range=[-1.5,1.5,.5],x_length=6,y_length=4,tips=False,
                axis_config={'include_ticks':False,'color':MUTED}).shift(LEFT*1.2)
        point=Dot(ax.c2p(-.8,-.4),color=GOLD,radius=.09)
        newpoint=Dot(ax.c2p(.8,.4),color=BLUE,radius=.09)
        vector=Arrow(point.get_center(),newpoint.get_center(),buff=0,color=BLUE)
        hp=text('h',25,GOLD).next_to(point,DOWN,.15)
        hprime=text('h′',25,BLUE).next_to(newpoint,UP,.15)
        equation=VGroup(text('h′ = h + αv',32,BLUE),text('방향 v / 움직이는 양 α',22,MUTED)).arrange(DOWN,.5).move_to([4.1,0,0])
        play(FadeIn(h),Create(ax),FadeIn(point),FadeIn(hp))
        play(GrowArrow(vector),FadeIn(newpoint),FadeIn(hprime),FadeIn(equation))
        until(10)

        start(11);clear()
        h=heading('아주 작은 개입부터 시작합니다')
        axes,labels=chart()
        f=lambda x:.94*np.exp(-.8*x)
        dot=Dot(axes.c2p(0,f(0)),color=GOLD,radius=.08)
        first=Dot(axes.c2p(.25,f(.25)),color=BLUE,radius=.08)
        step=Line(dot.get_center(),first.get_center(),color=BLUE)
        play(FadeIn(h),Create(axes),FadeIn(labels),FadeIn(dot))
        play(Create(step),FadeIn(first))
        until(11)

        start(12)
        second=Dot(axes.c2p(.6,f(.6)),color=BLUE,radius=.08)
        secondstep=Line(first.get_center(),second.get_center(),color=BLUE)
        play(Create(secondstep),FadeIn(second),Transform(h,heading('조금 더 움직이고, 점수를 다시 봅니다')))
        until(12)

        start(13)
        curve=axes.plot(f,x_range=[0,3],color=BLUE)
        play(Create(curve),Transform(h,heading('한 숫자에서, 방향에 대한 반응 곡선으로')),rt=1.3)
        more=VGroup(*[Dot(axes.c2p(x,f(x)),color=BLUE,radius=.045) for x in [1,1.5,2,2.5,3]])
        play(LaggedStart(*[FadeIn(p) for p in more],lag_ratio=.15))
        until(13)

        start(14)
        steep=axes.plot(lambda x:.94*np.exp(-1.6*x),x_range=[0,3],color=PINK)
        play(FadeOut(curve),FadeOut(first),FadeOut(second),FadeOut(step),FadeOut(secondstep),FadeOut(more),Create(steep),Transform(h,heading('작은 개입에도 빠르게 떨어지는 방향')))
        until(14)

        start(15)
        flat=axes.plot(lambda x:.94-.035*x,x_range=[0,3],color=GOLD)
        play(Create(flat),Transform(h,heading('많이 움직여도 거의 변하지 않는 방향')))
        until(15)

        start(16)
        threshold=axes.plot(lambda x:.94-.76/(1+np.exp(-7*(x-1.6))),x_range=[0,3],color=BLUE)
        play(Create(threshold),Transform(h,heading('처음에는 조용하다가, 중간에서 크게 바뀌는 방향')),rt=1.1)
        names=VGroup(text('빠른 변화',20,PINK).move_to([4.8,1.6,0]),text('완만한 변화',20,GOLD).move_to([4.8,.6,0]),text('구간별 변화',20,BLUE).move_to([4.8,-.4,0]))
        play(FadeIn(names))
        until(16)

        start(17)
        play(Transform(h,heading('지금 위치에서, 어느 방향에 얼마나 민감할까?')))
        point=Dot(axes.c2p(1.6,.94-.76/2),color=INK,radius=.085)
        play(FadeIn(point),Circumscribe(point,color=BLUE))
        until(17)

        start(18);clear()
        h=heading('Gradient / 현재 위치의 국소적 변화율')
        axes,labels=chart()
        f=lambda x:.94*np.exp(-.8*x)
        curve=axes.plot(f,x_range=[0,3],color=BLUE)
        x=.55;deriv=-.8*f(x)
        dot=Dot(axes.c2p(x,f(x)),color=GOLD,radius=.085)
        tangent=Line(axes.c2p(x-.45,f(x)-deriv*.45),axes.c2p(x+.45,f(x)+deriv*.45),color=GOLD,stroke_width=4)
        eq=footer('방향 v의 변화율 = ∇h s · v / ∇h s = 최대 증가 방향')
        play(FadeIn(h),Create(axes),FadeIn(labels),Create(curve),FadeIn(dot),FadeIn(eq))
        play(Create(tangent))
        until(18)

        start(19)
        x2=1.8;d2=-.8*f(x2)
        t2=Line(axes.c2p(x2-.5,f(x2)-d2*.5),axes.c2p(x2+.5,f(x2)+d2*.5),color=GOLD,stroke_width=4)
        play(dot.animate.move_to(axes.c2p(x2,f(x2))),Transform(tangent,t2),Transform(h,heading('이동하면, 기울기도 달라질 수 있습니다')),rt=1.2)
        until(19)

        start(20);clear()
        self.set_camera_orientation(phi=62*DEGREES,theta=-55*DEGREES,zoom=.87)
        surfaxes=ThreeDAxes(x_range=[-1.5,1.5,1],y_range=[-1.5,1.5,1],z_range=[0,4,1],
                           x_length=5.5,y_length=4.5,z_length=2.8,
                           axis_config={'include_ticks':False,'color':MUTED})
        def s(u,v):return 3+.4*u+.2*v-.45*u*u-.15*v*v+.4*u*v
        surface=Surface(lambda u,v:surfaxes.c2p(u,v,s(u,v)),u_range=[-1.5,1.5],v_range=[-1.5,1.5],
                        resolution=(12,12),checkerboard_colors=[BLUE,'#345366'],fill_opacity=.65,stroke_color='#84BDCA',stroke_width=.4)
        h=heading('두 내부 방향을 함께 움직여보면')
        caption=footer('가로 두 축 = 내부 방향 / 높이 = 고양이 점수')
        self.add_fixed_in_frame_mobjects(h,caption);fixed.extend([h,caption])
        play(FadeIn(surfaxes),FadeIn(surface),FadeIn(h),FadeIn(caption),rt=1)
        until(20)

        start(21)
        slice0=ParametricFunction(lambda u:surfaxes.c2p(u,0,s(u,0)),t_range=[-1.5,1.5],color=GOLD,stroke_width=5)
        moving=Sphere(radius=.07,resolution=(8,8),color=GOLD).move_to(surfaxes.c2p(-.8,0,s(-.8,0)))
        h=fixed_replace(h,heading('Hessian / 주변에서 기울기가 달라지는 방식'),Create(slice0),FadeIn(moving))
        travel=ParametricFunction(lambda u:surfaxes.c2p(u,0,s(u,0)),t_range=[-.8,.8])
        play(MoveAlongPath(moving,travel),rt=1.2)
        # Keep the explanatory overlay fixed while the surface is viewed obliquely.
        caption=fixed_replace(caption,footer('Hh s : 내부 표현 h에 대한 고양이 점수의 국소 곡률'))
        until(21)

        start(22)
        low=ParametricFunction(lambda u:surfaxes.c2p(u,-.8,s(u,-.8)),t_range=[-1.5,1.5],color=PINK,stroke_width=5)
        high=ParametricFunction(lambda u:surfaxes.c2p(u,.8,s(u,.8)),t_range=[-1.5,1.5],color=GOLD,stroke_width=5)
        h=fixed_replace(h,heading('다른 방향의 상태에 따라, 같은 방향의 효과도 달라집니다'),FadeOut(slice0),FadeOut(moving),Create(low),Create(high),rt=1.1)
        caption=fixed_replace(caption,footer('같은 방향의 이동 / 다른 출발 상태 / 다른 경사'))
        self.move_camera(theta=-35*DEGREES,run_time=1.2)
        until(22)

        start(23);clear()
        self.set_camera_orientation(phi=0,theta=-90*DEGREES,zoom=1)
        h=heading('한 번의 개입으로 중요성을 단정하지 않습니다')
        single=box('한 입력 · 한 크기 · 한 방향',0,1,GOLD,w=7)
        conclusion=box('중요하다? / 중요하지 않다?',0,-1,PINK,w=7)
        play(FadeIn(h),FadeIn(single),FadeIn(conclusion))
        q=footer('결론의 범위는 조사한 조건 안에서 확인해야 합니다')
        play(FadeIn(q))
        until(23)

        start(24);clear()
        h=heading('개입을 여러 조건에서 반복합니다')
        cards=VGroup(*[box(s,x,0,BLUE,w=3.8) for s,x in [('개입 크기',-4.5),('여러 입력',0),('다른 방향과 함께',4.5)]])
        play(FadeIn(h),LaggedStart(*[FadeIn(c) for c in cards],lag_ratio=.2))
        dots=VGroup(*[Circle(radius=.07,fill_color=GOLD,fill_opacity=1,stroke_width=0).move_to([x+d,-1,0])
                     for x in [-4.5,0,4.5] for d in [-.6,0,.6]])
        play(LaggedStart(*[FadeIn(p) for p in dots],lag_ratio=.1),rt=1)
        until(24)

        start(25);clear()
        h=heading('크게 보이는 값에서, 판정을 흔드는 개입으로')
        a=box('무엇이 크게 켜지는가',-3.5,0,GOLD,w=4.8)
        b=box('바꾸면 출력이 어떻게 달라지는가',3.5,0,BLUE,w=5.4)
        arrow=Arrow(a.get_right(),b.get_left(),color=BLUE,buff=.08)
        play(FadeIn(h),FadeIn(a))
        play(GrowArrow(arrow),FadeIn(b))
        q=footer('내부를 이해하려면, 개입에 대한 반응을 확인해야 합니다')
        play(FadeIn(q))
        until(25)

        start(26);clear()
        h=heading('중요한 방향을 찾았다고, 의미까지 알게 된 걸까요?')
        feature=box('개입한 방향 v',-3.8,0,GOLD,w=3.5)
        result=box('고양이 점수 하락',3.8,0,BLUE,w=3.5)
        arrow=Arrow(feature.get_right(),result.get_left(),buff=.1,color=BLUE)
        play(FadeIn(h),FadeIn(feature),GrowArrow(arrow),FadeIn(result))
        q=footer('이 방향을 정말 ‘고양이 feature’라고 불러도 될까?')
        play(FadeIn(q))
        until(26)
