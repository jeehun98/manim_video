"""Narration-led explanations sharing the original episode's geometry/layout."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scene import *


class RegularizationExplained(RegularizationGeometry):
    def play(self,*animations,**kwargs):
        if "run_time" in kwargs:
            kwargs["run_time"]=max(1,round(kwargs["run_time"]*config.frame_rate))/config.frame_rate
        return super().play(*animations,**kwargs)

    def wait(self,duration=1,**kwargs):
        frames=round(duration*config.frame_rate)
        if frames>0:
            return super().wait(frames/config.frame_rate,**kwargs)

    def detail(self, message, color=CYAN):
        if hasattr(self, "explanation"):
            self.remove_fixed_in_frame_mobjects(self.explanation)
            self.remove(self.explanation)
        obj = self.label(message, 23, color)
        if obj.width > (8 if PORTRAIT else 6):
            obj.scale_to_fit_width(8 if PORTRAIT else 6)
        obj.move_to([0,4.55,0] if PORTRAIT else [3.5,1.65,0])
        self.explanation = self.fixed(obj)

    def coordinates(self, w):
        if not hasattr(self, "numbers"):
            self.numbers = []
            items = VGroup()
            for i in range(3):
                n = DecimalNumber(w[i], num_decimal_places=2, font_size=34)
                label = MathTex(f"w_{i+1}=", font_size=35, color=[CYAN,ORANGE,VIOLET][i])
                item = VGroup(label,n).arrange(RIGHT,buff=.08)
                self.numbers.append(n)
                items.add(item)
            items.arrange(RIGHT,buff=.5)
            items.move_to([0,-4.5,0] if PORTRAIT else [0,-2.3,0])
            self.readout = self.fixed(items)
        self.readout.set_opacity(1)
        for n, value in zip(self.numbers,w):
            self.camera.remove_fixed_in_frame_mobjects(n)
            n.set_value(float(value))
            n.set_color(VIOLET if abs(value)<1e-8 else INK)
            n.set_z_index(100)
            self.camera.add_fixed_in_frame_mobjects(n)

    def move_weight(self, dot, function, duration=2):
        def update(mob,alpha):
            w = function(alpha)
            mob.move_to(self.axes.c2p(*w))
            self.coordinates(w)
        self.play(UpdateFromAlphaFunc(dot,update),run_time=duration,rate_func=linear)

    def erase(self, *names, duration=.35):
        objects = [getattr(self,n) for n in names if hasattr(self,n)]
        if objects:
            self.play(*[FadeOut(o) for o in objects],run_time=duration)
        for n in names:
            if hasattr(self,n):
                delattr(self,n)

    def mesh(self,p):
        result = VGroup()
        grid = np.linspace(0,PI/2,5)
        for sx in (-1,1):
            for sy in (-1,1):
                for sz in (-1,1):
                    def point(u,v):
                        d=np.array([sx*np.sin(v)*np.cos(u),sy*np.sin(v)*np.sin(u),sz*np.cos(v)])
                        r=np.max(np.abs(d)) if math.isinf(p) else np.sum(np.abs(d)**p)**(1/p)
                        return self.axes.c2p(*(d/r))
                    for u0,u1 in zip(grid[:-1],grid[1:]):
                        for v0,v1 in zip(grid[:-1],grid[1:]):
                            result.add(Polygon(point(u0,v0),point(u1,v0),point(u1,v1),point(u0,v1),
                                               fill_color=CYAN,fill_opacity=.32,
                                               stroke_color=CYAN,stroke_width=.5,stroke_opacity=.6))
        return result

    def morph(self,start,end,duration=2,with_solution=True):
        mesh=self.mesh(start)
        self.remove(self.shape)
        self.shape=mesh
        self.add(mesh)
        # Sample actual constrained solutions before animating; no per-frame optimizer.
        ws=None
        if with_solution:
            ps=np.linspace(start,end,65)
            ws=np.array([optimum(float(p)) for p in ps])
        def update(mob,alpha):
            p=start+(end-start)*alpha
            mob.become(self.mesh(p))
            if with_solution:
                location=alpha*(len(ws)-1)
                i=min(int(location),len(ws)-2)
                w=interpolate(ws[i],ws[i+1],location-i)
                w=w/np.sum(np.abs(w)**p)**(1/p)
                self.solution.move_to(self.axes.c2p(*w))
                self.coordinates(w)
        self.play(UpdateFromAlphaFunc(mesh,update),run_time=duration,rate_func=linear)
        self.remove(mesh)
        self.shape=self.octahedron() if end==1 else self.lp_surface(end)
        self.add(self.shape)
        if with_solution:
            w=optimum(end)
            self.solution.move_to(self.axes.c2p(*w))
            self.coordinates(w)

    def expand_loss(self,p,duration=3):
        self.erase("loss_shell","initial_shells",duration=.25)
        w=optimum(p)
        c=loss(w)
        shell=self.ellipsoid(c)
        center=self.axes.c2p(*A)
        shell.scale(.08,about_point=center)
        self.add(shell)
        self.play(shell.animate.scale(12.5,about_point=center),run_time=duration,rate_func=linear)
        self.loss_shell=shell
        if hasattr(self,"solution"):
            self.remove(self.solution)
        self.solution=Dot3D(self.axes.c2p(*w),radius=.09,color=INK)
        self.play(FadeIn(self.solution),run_time=.3)
        self.coordinates(w)

    def construct(self):
        self.set_camera_orientation(phi=67*DEGREES,theta=-57*DEGREES,
                                    zoom=1.25 if PORTRAIT else 1.12)
        length=5.8 if PORTRAIT else 6.3
        self.axes=ThreeDAxes(x_range=[-2.5,2.5,1],y_range=[-2.5,2.5,1],z_range=[-2.5,2.5,1],
                            x_length=length,y_length=length,z_length=length,tips=False,
                            axis_config={"color":GRID,"stroke_width":1.5})
        self.axes.shift(LEFT*(.95 if PORTRAIT else .7)+DOWN*.1)
        self.origin=Dot3D(self.axes.c2p(0,0,0),radius=.045,color=MUTED)
        self.minimum=Dot3D(self.axes.c2p(*A),radius=.085,color=ORANGE)
        self.add(self.axes,self.origin,self.minimum)
        self.axis_labels=VGroup()
        for i,color in enumerate([CYAN,ORANGE,VIOLET]):
            v=np.zeros(3); v[i]=1.85 if i==2 and not PORTRAIT else 2.45
            label=MathTex(f"w_{i+1}",font_size=23,color=color).move_to(self.axes.c2p(*v))
            self.add_fixed_orientation_mobjects(label)
            self.axis_labels.add(label)
        actions=[self.descent,self.penalty,self.cost,self.idea,self.strength,self.definition,
                 self.axes_intro,self.project_point,self.shells,self.minimum_pulse,
                 self.restrict,self.equivalence,self.question,self.sphere,self.why,
                 self.radius,self.sweep,self.l2_name,self.inside,self.touch2,
                 self.absolute,self.plane,self.assemble,self.l1_name,self.edge,
                 self.zero_plane,self.vertex,self.touch1,self.sparse,self.p_intro,
                 self.p_name,self.to2,self.to4,self.toinf,self.to07,self.nonconvex,
                 self.compare,self.zero_compare,self.finish]
        for i,(end,sentence) in enumerate(SCRIPT["sentences"]):
            self.set_caption(sentence)
            actions[i]()
            if self.time>end+.02:
                raise RuntimeError(f"Sentence {i+1} exceeded {end}: {self.time}")
            if end>self.time:
                self.wait(end-self.time)

    def descent(self):
        self.set_header("학습: 손실이 낮아지는 위치로")
        self.set_formula(r"\min_{\mathbf w}\mathcal L_{\rm data}(\mathbf w)")
        self.detail("주황색 중심 = 데이터 손실의 최소점",ORANGE)
        self.initial_shells=VGroup(self.ellipsoid(.8),self.ellipsoid(.25))
        self.add(self.initial_shells)
        dot=Dot3D(self.axes.c2p(1.1,-.5,.9),radius=.075,color=INK)
        start=np.array([1.1,-.5,.9])
        trail=ParametricFunction(lambda t:self.axes.c2p(*(A+(start-A)*np.exp(-Q*t))),
                                 t_range=[0,4],color=INK,stroke_width=2)
        self.add(dot)
        self.play(Create(trail),run_time=.6)
        self.move_weight(dot,lambda t:A+(start-A)*np.exp(-Q*5*t),2.7)
        self.play(FadeOut(dot),FadeOut(trail),run_time=.3)

    def penalty(self):
        self.set_formula(r"\mathcal L_{\rm data}(\mathbf w)+\lambda R(\mathbf w)")
        self.detail("λ: 규제의 비중    R: 가중치의 크기",CYAN)
        self.play(Indicate(self.formula,color=CYAN),run_time=1)

    def cost(self):
        self.detail("원점에서 멀수록 가중치 비용 증가",CYAN)
        lines=VGroup(*[Line(self.axes.c2p(0,0,0),self.axes.c2p(*(A*s)),
                           color=CYAN,stroke_width=3) for s in (.25,.6,1)])
        points=VGroup(*[Dot3D(self.axes.c2p(*(A*s)),radius=.045+.045*s,color=CYAN)
                        for s in (.25,.6,1)])
        self.play(LaggedStart(*[Create(l) for l in lines],lag_ratio=.35),FadeIn(points),run_time=2)
        self.add(lines,points)
        self.play(FadeOut(lines),FadeOut(points),run_time=.5)

    def idea(self):
        self.set_header("오차와 가중치 크기를 함께 평가")
        self.play(Indicate(self.formula,color=CYAN),run_time=.8)

    def strength(self):
        self.set_header("λ를 높이면 최적해가 움직인다")
        self.detail("L2 예시: λ = 0 → 3",CYAN)
        dot=Dot3D(self.axes.c2p(*A),radius=.09,color=INK)
        self.add(dot)
        path=ParametricFunction(lambda t:self.axes.c2p(*(Q*A/(Q+t))),t_range=[0,3],
                                color=INK,stroke_width=2.5)
        self.play(Create(path),run_time=.8)
        self.move_weight(dot,lambda t:Q*A/(Q+3*t),4.5)
        self.play(FadeOut(dot),FadeOut(path),run_time=.5)

    def definition(self):
        self.detail("같은 손실함수 + 다른 크기 정의",CYAN)
        self.play(Indicate(self.origin,color=CYAN),run_time=1)

    def axes_intro(self):
        self.set_header("세 가중치를 세 좌표축에 대응")
        self.set_formula(r"\mathbf w=(w_1,w_2,w_3)")
        self.detail("청록 w₁ · 주황 w₂ · 보라 w₃",CYAN)
        self.play(LaggedStart(*[Indicate(l) for l in self.axis_labels],lag_ratio=.3),run_time=1.7)

    def project_point(self):
        w=np.array([.8,.55,.65])
        positions=[np.zeros(3),np.array([w[0],0,0]),np.array([w[0],w[1],0]),w]
        self.projections=VGroup(*[Line(self.axes.c2p(*a),self.axes.c2p(*b),color=c,stroke_width=4)
                                 for a,b,c in zip(positions[:-1],positions[1:],[CYAN,ORANGE,VIOLET])])
        self.sample=Dot3D(self.axes.c2p(*w),radius=.085,color=INK)
        self.play(LaggedStart(*[Create(l) for l in self.projections],lag_ratio=.7),FadeIn(self.sample),run_time=2.8)
        self.add(self.projections,self.sample)
        self.coordinates(w)

    def shells(self):
        self.erase("projections","sample",duration=.4)
        self.set_header("같은 손실의 점들을 연결")
        self.set_formula(r"\mathcal L=(\mathbf w-\mathbf a)^TQ(\mathbf w-\mathbf a)")
        self.detail("타원체의 표면에서는 손실값이 같다",ORANGE)
        self.erase("initial_shells",duration=.3)
        self.initial_shells=VGroup(self.ellipsoid(.2),self.ellipsoid(.7),self.ellipsoid(1.45))
        self.play(LaggedStart(*[FadeIn(s) for s in self.initial_shells],lag_ratio=.65),run_time=2.7)
        self.add(self.initial_shells)

    def minimum_pulse(self):
        self.detail("안쪽으로 갈수록 손실 감소 → 중심에서 최소",ORANGE)
        self.play(Indicate(self.minimum,color=ORANGE,scale_factor=1.7),run_time=1.3)

    def restrict(self):
        self.set_header("이제 허용 영역을 제한한다")
        self.set_formula(r"\|\mathbf w\|_p\leq1")
        self.detail("규제 영역의 중심은 원점",CYAN)
        self.play(Indicate(self.origin,color=CYAN,scale_factor=2),run_time=1)

    def equivalence(self):
        self.set_formula(r"\min[\mathcal L+\lambda R]\;\longleftrightarrow\;\min_{R\leq t}\mathcal L")
        self.detail("적절한 조건과 λ ↔ t의 대응에서 성립",MUTED)
        self.play(Write(self.formula),run_time=2)

    def question(self):
        self.detail("가중치의 크기는 어떤 공간을 만드는가?",CYAN)

    def sphere(self):
        self.erase("initial_shells",duration=.3)
        self.set_header("L2: 제곱합으로 구를 만든다")
        self.set_formula(r"w_1^2+w_2^2+w_3^2\leq1")
        self.detail("경계: 원점에서 거리 1",CYAN)
        self.shape=self.lp_surface(2)
        self.play(Create(self.shape),run_time=2.5)

    def why(self):
        self.detail("세 직각 성분 → 피타고라스 정리",CYAN)

    def radius(self):
        d=np.array([.8,0,.6])
        a=self.axes.c2p(0,0,0);b=self.axes.c2p(*d)
        self.radius_line=Line(a,b,color=INK,stroke_width=5)
        self.radius_dot=Dot3D(b,radius=.075,color=INK)
        self.set_formula(r"\sqrt{w_1^2+w_2^2+w_3^2}=1")
        self.play(Create(self.radius_line),FadeIn(self.radius_dot),run_time=1.3)

    def sweep(self):
        self.detail("방향이 바뀌어도 원점까지의 거리는 같다",CYAN)
        def update(mob,t):
            theta=TAU*t
            d=np.array([.8*np.cos(theta),.8*np.sin(theta),.6])
            mob.move_to(self.axes.c2p(*d))
            self.radius_line.put_start_and_end_on(self.axes.c2p(0,0,0),self.axes.c2p(*d))
            self.coordinates(d)
        ring=ParametricFunction(lambda t:self.axes.c2p(.8*np.cos(t),.8*np.sin(t),.6),
                                t_range=[0,TAU],color=INK,stroke_width=2.5)
        self.play(Create(ring),UpdateFromAlphaFunc(self.radius_dot,update),run_time=4,rate_func=linear)
        self.play(FadeOut(ring),run_time=.3)

    def l2_name(self):
        self.set_header("L2 규제")

    def inside(self):
        self.erase("radius_line","radius_dot",duration=.3)
        self.detail("허용되는 점은 구 내부와 표면",CYAN)
        w=np.array([.2,.1,.3]);dot=Dot3D(self.axes.c2p(*w),radius=.08,color=INK)
        self.add(dot)
        self.move_weight(dot,lambda t:np.array([.2+.3*t,.1-.3*t,.3+.2*t]),1.5)
        self.play(FadeOut(dot),run_time=.2)

    def touch2(self):
        self.set_header("확장하다가 처음 닿는 곳 = 최적해")
        self.detail("등손실면이 작을 때는 구에 닿지 않는다",ORANGE)
        self.expand_loss(2,3)
        self.detail("첫 접촉점: 제약 안에서 가능한 최소 손실",INK)

    def absolute(self):
        self.set_header("L1: 제곱합 대신 절댓값 합")
        self.set_formula(r"|w_1|+|w_2|+|w_3|\leq1")
        self.detail("우선 세 좌표가 모두 양수인 영역",CYAN)
        self.erase("shape","solution","loss_shell",duration=.65)

    def plane(self):
        self.move_camera(phi=60*DEGREES,theta=30*DEGREES,run_time=.65)
        self.set_formula(r"w_1+w_2+w_3=1\quad(w_i\geq0)")
        self.face=Polygon(self.axes.c2p(1,0,0),self.axes.c2p(0,1,0),self.axes.c2p(0,0,1),
                          fill_color=CYAN,fill_opacity=.5,stroke_color=CYAN,stroke_width=3)
        self.play(DrawBorderThenFill(self.face),run_time=1.5)
        dot=Dot3D(self.axes.c2p(.2,.3,.5),radius=.08,color=INK);self.add(dot)
        self.detail("평면 위에서 이동해도 세 좌표의 합은 1",CYAN)
        self.move_weight(dot,lambda t:np.array([.2+.4*t,.3-.2*t,.5-.2*t]),2.5)
        self.play(FadeOut(dot),run_time=.3)

    def assemble(self):
        self.set_header("부호를 바꾸면 삼각형 면 8개")
        self.set_formula(r"|w_1|+|w_2|+|w_3|=1")
        self.detail("각 부호 영역의 평면들이 정팔면체를 이룬다",CYAN)
        self.remove(self.face);del self.face
        self.shape=self.octahedron()
        self.play(LaggedStart(*[DrawBorderThenFill(f) for f in self.shape],lag_ratio=.45),run_time=3.8)
        self.add(self.shape)
        self.move_camera(phi=68*DEGREES,theta=-30*DEGREES,run_time=1.1)

    def l1_name(self):
        self.set_header("L1 규제")

    def edge(self):
        self.set_header("모서리 위에서는 한 좌표가 0")
        self.set_formula(r"(w_1,w_2,0),\quad w_1+w_2=1")
        self.detail("보라색 모서리는 w₃ = 0인 평면 위",VIOLET)
        self.edge_line=Line(self.axes.c2p(1,0,0),self.axes.c2p(0,1,0),color=VIOLET,stroke_width=7)
        self.edge_dot=Dot3D(self.axes.c2p(.75,.25,0),radius=.09,color=VIOLET)
        self.play(Create(self.edge_line),FadeIn(self.edge_dot),run_time=.8)
        self.move_weight(self.edge_dot,lambda t:np.array([.75-.4*t,.25+.4*t,0]),2.7)

    def zero_plane(self):
        self.detail("이동하는 동안 w₃는 정확히 0",VIOLET)
        self.play(Indicate(self.edge_line,color=VIOLET),run_time=1.2)

    def vertex(self):
        self.set_header("꼭짓점에서는 두 좌표가 0")
        self.set_formula(r"(w_1,0,0)=(1,0,0)")
        self.detail("모서리를 따라 꼭짓점으로 이동",VIOLET)
        self.move_weight(self.edge_dot,lambda t:np.array([.35+.65*t,.65*(1-t),0]),3.8)
        self.play(Indicate(self.edge_dot,color=VIOLET),run_time=.6)

    def touch1(self):
        self.erase("edge_line","edge_dot",duration=.3)
        self.set_header("L1의 첫 접촉: (1, 0, 0)")
        self.detail("같은 손실함수의 타원체를 다시 확장",ORANGE)
        self.expand_loss(1,4)
        self.set_formula(r"\mathbf w_1^*=(1,0,0)",VIOLET)

    def sparse(self):
        self.detail("이 예시에서는 세 가중치 중 하나만 남는다",VIOLET)
        self.play(Indicate(self.solution,color=VIOLET),run_time=1)

    def p_intro(self):
        self.set_header("지수 p를 바꾸면 경계도 변한다")
        self.set_formula(r"\|\mathbf w\|_p=(|w_1|^p+|w_2|^p+|w_3|^p)^{1/p}")
        self.detail("p ≥ 1: 노름   /   0 < p < 1: 준노름",MUTED)
        self.erase("loss_shell",duration=.35)

    def p_name(self):
        self.play(Indicate(self.formula,color=CYAN),run_time=.8)

    def to2(self):
        self.set_header("p = 1 → 2: 면이 곡면으로")
        self.detail("표면의 모든 방향에서 Lp 경계를 다시 계산",CYAN)
        self.morph(1,2,2.6)

    def to4(self):
        self.set_header("p = 2 → 4: 경계가 부풀어 오른다")
        self.detail("흰 점: 같은 손실함수의 제약 최적해",INK)
        self.morph(2,4,3.3)

    def toinf(self):
        self.set_header("p → ∞: 정육면체로 접근")
        self.set_formula(r"\|\mathbf w\|_\infty=\max_i|w_i|\leq1")
        self.detail("각 좌표를 각각 −1과 1 사이로 제한",CYAN)
        self.morph(4,24,3.3)
        self.remove(self.shape);self.shape=self.lp_surface(math.inf);self.add(self.shape)
        w=optimum(math.inf);self.solution.move_to(self.axes.c2p(*w));self.coordinates(w)

    def to07(self):
        self.set_header("p < 1: 표면이 안쪽으로 들어간다")
        self.set_formula(r"|w_1|^{0.7}+|w_2|^{0.7}+|w_3|^{0.7}\leq1")
        self.detail("축 사이의 허용 영역이 좁아진다",CYAN)
        self.erase("solution",duration=.2)
        self.readout.set_opacity(0)
        self.morph(24,1,1.,with_solution=False)
        self.morph(1,.7,2.8,with_solution=False)

    def nonconvex(self):
        self.set_header("비볼록: 두 점을 잇는 선분이 밖으로")
        self.detail("보라 끝점은 허용 · 주황 중점은 영역 밖",VIOLET)
        self.chord=Line(self.axes.c2p(1,0,0),self.axes.c2p(0,1,0),color=VIOLET,stroke_width=5)
        self.outside=Dot3D(self.axes.c2p(.5,.5,0),radius=.095,color=ORANGE)
        self.play(Create(self.chord),run_time=2)
        self.play(FadeIn(self.outside),run_time=.4)
        self.coordinates(np.array([.5,.5,0]))
        self.play(Indicate(self.outside,color=ORANGE),run_time=.8)
        self.set_formula(r"0.5^{0.7}+0.5^{0.7}\approx1.23>1")

    def compare(self):
        self.erase("chord","outside",duration=.3)
        self.set_header("같은 손실 · 다른 규제 · 다른 최적해")
        self.set_formula(r"\min_{\|\mathbf w\|_p\leq1}\mathcal L(\mathbf w)")
        self.detail("L2의 매끄러운 경계에서 선택한 해",CYAN)
        self.remove(self.shape);self.shape=self.lp_surface(2);self.add(self.shape)
        self.expand_loss(2,2.8)

    def zero_compare(self):
        self.set_header("L2의 세 가중치 → L1의 한 가중치")
        self.detail("같은 손실함수에서 p만 2 → 1로 변경",VIOLET)
        self.erase("loss_shell",duration=.3)
        self.morph(2,1,4)
        self.set_formula(r"(0.90,0.40,0.20)\;\longrightarrow\;(1,0,0)")

    def finish(self):
        self.set_header("정의가 바뀌면 최적해의 성질도 달라진다")
        self.set_formula(r"\min_{\mathbf w}[\mathcal L_{\rm data}(\mathbf w)+\lambda R(\mathbf w)]")
        self.detail("규제의 정의 → 공간의 형태 → 선택되는 가중치",CYAN)
        self.expand_loss(1,2.5)
        self.play(Indicate(self.solution,color=VIOLET),run_time=1)
