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

class Act02InputChanges(Scene):
    def construct(self):
        ends=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))['ends']
        def play(*a,rt=.7):self.play(*a,run_time=round(rt*30)/30)
        def until(n):
            frames=round(ends[n-1]*30)-round(self.time*30)
            if frames<0:raise ValueError(f'Cue {n} overrun: {self.time} > {ends[n-1]}')
            if frames:self.wait(frames/30)
        def start(n):self.next_section(f'cue_{n:02}')
        def clear():
            if self.mobjects:play(*[FadeOut(m) for m in list(self.mobjects)],rt=.3)
        def heading(s):return text(s,30).move_to([0,3.3,0])
        def footer(s):return text(s,25).move_to([0,-3.3,0])
        def noise(center=[0,0,0]):
            rng=np.random.default_rng(22)
            return VGroup(*[Square(side_length=.06,stroke_width=0,fill_opacity=.45,color=INK)
                          .move_to(np.array(center)+[rng.uniform(-1.4,1.4),rng.uniform(-1.4,1.4),0]) for _ in range(90)])
        def score(x,y,w=2.6):
            bg=Rectangle(width=3,height=.2,stroke_width=0,fill_opacity=1,fill_color='#293A49').move_to([x,y,0])
            bar=Rectangle(width=w,height=.2,stroke_width=0,fill_opacity=1,fill_color=BLUE).align_to(bg,LEFT).set_y(y)
            return VGroup(bg,bar)
        def grid(x,y,seed):
            rng=np.random.default_rng(seed)
            return VGroup(*[Square(side_length=.25,stroke_width=0,fill_opacity=float(rng.uniform(.15,.85)),fill_color=BLUE)
                    .move_to([x+(c-2)*.31,y+(r-2)*.31,0]) for r in range(5) for c in range(5)])

        start(1)
        h=heading('02 / 입력을 바꿔보면 차이가 보인다')
        p=photo(width=4.1,height=4.1)
        eq=footer('입력 x → 바뀐 입력 x′')
        play(FadeIn(h),FadeIn(p),FadeIn(eq))
        until(1)

        start(2)
        play(p[0].animate.set_fill('#875065'),Transform(h,heading('배경을 바꿉니다')))
        until(2)

        start(3)
        tint=RoundedRectangle(width=4.1,height=4.1,corner_radius=.15,stroke_width=0,fill_color=BLUE,fill_opacity=.25)
        play(FadeIn(tint),Transform(h,heading('색을 바꿉니다')))
        until(3)

        start(4)
        tex=cat(True,3.85)
        play(FadeOut(tint),FadeOut(p[1]),FadeIn(tex),Transform(h,heading('질감을 바꿉니다')))
        p.remove(p[1]);p.add(tex)
        until(4)

        start(5)
        play(p.animate.scale(.75).shift(LEFT*4.5),FadeOut(eq),Transform(h,heading('가림 · 노이즈 · 작은 패턴')))
        other=photo(x=0,width=3.1,height=3.1);third=photo(x=4.5,width=3.1,height=3.1)
        cover=Rectangle(width=1.3,height=.4,fill_color='#162331',fill_opacity=1,stroke_width=0).move_to([-4.5,.75,0])
        ns=noise();patch=VGroup(*[Square(side_length=.14,stroke_width=0,fill_opacity=1,color=GOLD if (r+c)%2 else BLUE)
                     .move_to([5.3+c*.14,-.8+r*.14,0]) for r in range(4) for c in range(4)])
        play(FadeIn(other),FadeIn(third),FadeIn(cover))
        play(FadeIn(ns),FadeIn(patch))
        tags=VGroup(*[text(s,22,MUTED).move_to([x,-2,0]) for s,x in [('가림',-4.5),('노이즈',0),('패턴',4.5)]])
        play(FadeIn(tags))
        until(5)

        start(6)
        scores=VGroup(*[score(x,-2.6,w) for x,w in [(-4.5,2.5),(0,1.7),(4.5,.9)]])
        play(FadeIn(scores),Transform(h,heading('바뀐 입력에서 답이 얼마나 유지될까?')))
        until(6)

        start(7);clear()
        h=heading('변형의 종류별로 답을 비교합니다')
        cards=Group(*[photo(x=x,width=3.3,height=3.3) for x in [-4.5,0,4.5]])
        cards[0][0].set_fill('#875065')
        tx=cat(True,3.05).move_to(cards[1][1]);cards[1].remove(cards[1][1]);cards[1].add(tx)
        cover=Rectangle(width=1.3,height=.4,fill_color='#162331',fill_opacity=1,stroke_width=0).shift(UP*.8+RIGHT*4.5)
        tags=VGroup(*[text(s,22,MUTED).move_to([x,-2.05,0]) for s,x in [('배경',-4.5),('색 · 질감',0),('가림',4.5)]])
        play(FadeIn(h),FadeIn(cards),FadeIn(cover),FadeIn(tags))
        for i in range(3):
            play(Circumscribe(cards[i],color=GOLD),tags[i].animate.set_color(GOLD),rt=.8)
        q=footer('변형마다 유지되는 답과 흔들리는 답을 관찰합니다')
        play(FadeIn(q))
        until(7)

        start(8)
        play(Transform(h,heading('같은 판단을 얼마나 안정적으로 유지하는가?')))
        bars=VGroup(*[score(x,-2.65,w) for x,w in [(-4.5,2.5),(0,1.9),(4.5,1.3)]])
        play(FadeIn(bars),FadeOut(q))
        play(Indicate(bars[0]),Indicate(bars[2]))
        until(8)

        start(9);clear()
        h=heading('정확한 답 하나에서, 조건별 반응으로')
        original=box('원본 → CAT',-4.6,0,GOLD,w=3.4)
        stable=box('잘 버티는 조건',2.5,1,GOLD,w=4)
        fragile=box('흔들리는 조건',2.5,-1,PINK,w=4)
        arrows=VGroup(Arrow(original.get_right(),stable.get_left(),color=MUTED,buff=.1),
                      Arrow(original.get_right(),fragile.get_left(),color=MUTED,buff=.1))
        play(FadeIn(h),FadeIn(original))
        play(GrowArrow(arrows[0]),FadeIn(stable))
        play(GrowArrow(arrows[1]),FadeIn(fragile))
        until(9)

        start(10);clear()
        h=heading('배경만 바꿨는데, 점수가 떨어졌다면?')
        a=photo(x=-2.7,width=3.8,height=3.8);b=photo(x=2.7,color='#875065',width=3.8,height=3.8)
        sa=score(-2.7,-2.4);sb=score(2.7,-2.4)
        play(FadeIn(h),FadeIn(a),FadeIn(b),FadeIn(sa),FadeIn(sb))
        play(sb[1].animate.stretch_to_fit_width(.8).align_to(sb[0],LEFT))
        until(10)

        start(11)
        q=footer('고양이보다 배경을 보고 있었던 걸까?')
        play(FadeIn(q),Circumscribe(b[0],color=PINK))
        play(Transform(h,heading('가능한 설명: 배경을 단서로 사용했을 수 있다')))
        until(11)

        start(12);clear()
        h=heading('학습 데이터에서 자주 함께 나타났다면')
        photos=Group(*[photo(x=x,width=2.6,height=2.8,color='#385563') for x in [-4,0,4]])
        labels=VGroup(*[text('고양이 + 같은 배경',20,MUTED).move_to([x,-1.9,0]) for x in [-4,0,4]])
        play(FadeIn(h),LaggedStart(*[FadeIn(o) for o in photos],lag_ratio=.2),FadeIn(labels))
        q=footer('함께 나타난 패턴이 정답 예측에 유용할 수 있습니다')
        play(FadeIn(q))
        for ph in photos:play(Circumscribe(ph[0],color=BLUE),rt=.5)
        until(12)

        start(13);clear()
        h=heading('사람에게 부수적인 정보도, 모델에게는 단서일 수 있다')
        inp=photo(x=-4.7,width=3,height=3.3)
        options=VGroup(box('대상의 특징',0,1,GOLD,w=3.2),box('함께 나타난 패턴',0,-1,BLUE,w=3.2))
        out=box('정답 예측',4.8,0,BLUE,w=2.7)
        routes=VGroup(*[DashedLine(inp.get_right(),o.get_left(),color=MUTED) for o in options],
                      *[DashedLine(o.get_right(),out.get_left(),color=MUTED) for o in options])
        play(FadeIn(h),FadeIn(inp),FadeIn(options),FadeIn(out),Create(routes))
        play(Indicate(options[1],color=BLUE))
        until(13)

        start(14);clear()
        h=heading('하지만 이 설명을 바로 확정해도 될까요?')
        hypothesis=box('배경에 의존했다?',0,0,PINK,w=6)
        play(FadeIn(h),FadeIn(hypothesis))
        play(Circumscribe(hypothesis,color=PINK),rt=.6)
        until(14)

        start(15);clear()
        h=heading('배경 교체 ≠ 내부 값 하나의 변화')
        inp=photo(x=-3,width=3.6,height=3.8)
        changes=VGroup(*[box(s,3,y,MUTED,w=4) for s,y in [('경계',1.3),('명암 대비',0),('주변과의 관계',-1.3)]])
        play(FadeIn(h),FadeIn(inp),FadeIn(changes))
        until(15)

        start(16)
        edge=SurroundingRectangle(inp[1],color=GOLD,buff=.03)
        play(Create(edge),changes[0].animate.set_color(GOLD),rt=.65)
        play(inp[0].animate.set_fill('#8F697A'),changes[1].animate.set_color(BLUE),rt=.65)
        obj=Circle(radius=.35,fill_color=GOLD,fill_opacity=.8,stroke_width=0).move_to([-1.65,-1.3,0])
        play(FadeIn(obj),changes[2].animate.set_color(PINK),rt=.65)
        until(16)

        start(17);clear()
        h=heading('변화는 여러 층으로 퍼져나갑니다')
        inp=photo(x=-5.5,width=1.8,height=2.2)
        layers=VGroup(*[grid(x,0,seed) for x,seed in [(-2.5,1),(.5,2),(3.5,3)]])
        names=VGroup(*[text('Layer '+str(i+1),21,MUTED).move_to([x,1.5,0]) for i,x in enumerate([-2.5,.5,3.5])])
        arrows=VGroup(*[Arrow([x,-0.0,0],[x+1,0,0],buff=0,color=MUTED) for x in [-4.5,-1.5,1.5]])
        play(FadeIn(h),FadeIn(inp),FadeIn(layers),FadeIn(names),Create(arrows))
        for layer in layers:
            play(*[cell.animate.set_fill(PINK,opacity=.7 if i%3 else .25) for i,cell in enumerate(layer)],rt=.65)
        until(17)

        start(18)
        q=footer('화면의 변화 하나 → 내부 표현의 변화 다수')
        play(FadeIn(q),inp[0].animate.set_fill('#875065'))
        play(Indicate(layers[0]),Indicate(layers[1]),Indicate(layers[2]))
        until(18)

        start(19)
        play(Transform(h,heading('어떤 내부 변화가 실제 판정을 흔들었을까?')))
        marks=VGroup(*[text('?',36,GOLD).move_to([x,-1.6,0]) for x in [-2.5,.5,3.5]])
        play(FadeIn(marks),Transform(q,footer('결과가 달라졌다는 사실만으로 경로를 분리할 수 없습니다')))
        until(19)

        start(20);clear()
        h=heading('입력 변형 실험이 알려주는 것')
        known=box('언제 흔들리는가',0,1.4,GOLD,w=6)
        strong=box('강한 변화',-3,-.5,GOLD,w=3.6);weak=box('취약한 변화',3,-.5,PINK,w=3.6)
        play(FadeIn(h),FadeIn(known))
        play(FadeIn(strong),FadeIn(weak))
        a=VGroup(Arrow(known.get_bottom(),strong.get_top(),buff=.1,color=MUTED),Arrow(known.get_bottom(),weak.get_top(),buff=.1,color=MUTED))
        play(Create(a))
        until(20)

        start(21)
        question=box('무엇이 판단을 지탱했는가?',0,-2.3,BLUE,w=7)
        play(FadeIn(question),Transform(h,heading('반응의 조건과, 내부의 원인은 다른 질문입니다')))
        until(21)

        start(22);clear()
        h=heading('지금까지: 바깥에서 바꾸고, 마지막 답을 관찰')
        inp=box('입력 x → x′',-4.5,0,GOLD,w=3)
        model=box('모델 내부',0,0,MUTED,w=3.5)
        answer=box('출력 변화',4.5,0,BLUE,w=3)
        arrows=VGroup(Arrow(inp.get_right(),model.get_left(),buff=.1,color=MUTED),Arrow(model.get_right(),answer.get_left(),buff=.1,color=MUTED))
        play(FadeIn(h),FadeIn(inp),FadeIn(model),FadeIn(answer),Create(arrows))
        play(Circumscribe(inp,color=GOLD),Circumscribe(answer,color=BLUE))
        until(22)

        start(23)
        play(Transform(h,heading('이제 입력을 고정하고, 내부의 일부를 바꿔본다면?')),
             Transform(inp,box('입력 고정',-4.5,0,GOLD,w=3)))
        play(model.animate.set_color(BLUE))
        nodes=VGroup(*[Circle(radius=.13,stroke_color=BLUE,fill_color=BLUE,fill_opacity=.5).move_to([x,-1.4,0]) for x in [-1,-.5,0,.5,1]])
        play(FadeIn(nodes))
        play(nodes[2].animate.set_color(GOLD),Circumscribe(model,color=BLUE))
        until(23)

        start(24)
        q=footer('언제 틀리는가 → 무엇에 의존하는가')
        play(FadeIn(q),Transform(h,heading('03 / 판단의 근거를 안쪽에서 추적합니다')))
        play(Indicate(nodes[2],color=GOLD))
        until(24)
