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

def input_photo(filename,x=0,width=3,height=3.4):
    bg=RoundedRectangle(width=width,height=height,corner_radius=.15,stroke_width=0,fill_color='#385563',fill_opacity=1)
    im=ImageMobject(str(ASSETS/filename));im.height=height-.2
    if im.width>width-.1:im.width=width-.1
    return Group(bg,im).move_to([x,0,0])

class Act03InternalClues(Scene):
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
        def footer(s):return text(s,25).move_to([0,-3.25,0])
        def values(x,y=0,seed=1):
            rng=np.random.default_rng(seed)
            cells=VGroup()
            for r in range(3):
                for c in range(3):
                    v=float(rng.uniform(.1,.9))
                    cell=Square(side_length=.55,stroke_color='#314657',stroke_width=1,fill_color=BLUE,fill_opacity=v*.5)
                    t=text(f'{v:.1f}',15,INK).move_to(cell)
                    cells.add(VGroup(cell,t).move_to([x+(c-1)*.65,y+(1-r)*.65,0]))
            return cells
        def activation(x,height,color,name,base=-1.55):
            axis=Line([x-.75,base,0],[x+.75,base,0],color=MUTED)
            bar=Rectangle(width=.8,height=height,stroke_width=0,fill_color=color,fill_opacity=.9).move_to([x,base+height/2,0])
            title=text(name,23,color).move_to([x,base-.45,0])
            return VGroup(axis,bar,title)

        start(1)
        h=heading('03 / 입력을 고정하고, 내부를 관찰합니다')
        p=photo(width=4,height=4.1)
        lock=box('같은 입력',-4.7,0,GOLD,w=2.7)
        play(FadeIn(h),FadeIn(p),FadeIn(lock))
        play(Circumscribe(p,color=GOLD))
        q=footer('사진을 바꾸는 대신, 계산 안쪽을 살펴봅니다')
        play(FadeIn(q))
        until(1)

        start(2)
        play(p.animate.scale(.6).move_to([-5.4,0,0]),FadeOut(lock),FadeOut(q),Transform(h,heading('각 층의 숫자가 다음 계산으로 전달됩니다')))
        layers=VGroup(*[values(x,seed=i+1) for i,x in enumerate([-2.5,.6,3.7])])
        names=VGroup(*[text('Layer '+str(i+1),22,MUTED).move_to([x,1.6,0]) for i,x in enumerate([-2.5,.6,3.7])])
        arrows=VGroup(*[Arrow([x,0,0],[x+.7,0,0],color=MUTED,buff=0) for x in [-4.1,-1.4,1.7]])
        play(FadeIn(layers),FadeIn(names),Create(arrows))
        for layer in layers:play(Indicate(layer,color=BLUE),rt=.6)
        until(2)

        start(3)
        rep=SurroundingRectangle(layers[1],buff=.2,color=GOLD)
        term=footer('한 층에서 만들어진 숫자 묶음 = 내부 표현 h')
        play(Create(rep),FadeIn(term),Transform(h,heading('내부 표현: 숫자들의 묶음')))
        until(3)

        start(4);clear()
        h=heading('여러 입력에서 같은 내부 패턴을 찾아봅니다')
        inputs=Group(input_photo('cat_photo.png',-4.5),input_photo('cat_second.png',0),input_photo('dog_photo.png',4.5))
        tags=VGroup(*[text(s,22,MUTED).move_to([x,-2.15,0]) for s,x in [('고양이 A',-4.5),('고양이 B',0),('비고양이',4.5)]])
        play(FadeIn(h),LaggedStart(*[FadeIn(i) for i in inputs],lag_ratio=.2),FadeIn(tags))
        dots=VGroup(*[Circle(radius=.15,stroke_width=0,fill_color=GOLD,fill_opacity=o).move_to([x,-2.75,0]) for x,o in [(-4.5,1),(0,.9),(4.5,.2)]])
        play(FadeIn(dots))
        for i in range(3):play(Circumscribe(dots[i],color=GOLD),rt=.5)
        until(4)

        start(5)
        play(inputs.animate.scale(.65).shift(UP*.7),FadeOut(dots),FadeOut(tags),Transform(h,heading('고양이 입력에서 activation이 크게 올라간다면')))
        bars=VGroup(activation(-4.5,1.5,GOLD,'고양이 A'),activation(0,1.35,GOLD,'고양이 B'),activation(4.5,.35,MUTED,'비고양이'))
        # Input positions shrink around the origin with the group; place each explicitly.
        for im,x in zip(inputs,[-4.5,0,4.5]):play(im.animate.move_to([x,1.2,0]),rt=.3)
        play(LaggedStart(*[GrowFromEdge(b[1],DOWN) for b in bars],lag_ratio=.2),FadeIn(VGroup(*[b[0] for b in bars])),FadeIn(VGroup(*[b[2] for b in bars])))
        until(5)

        start(6)
        q=footer('고양이 판정에 중요한 역할을 하는 것처럼 보입니다')
        play(FadeIn(q),Circumscribe(bars[0][1],color=GOLD),Circumscribe(bars[1][1],color=GOLD))
        until(6)

        start(7);clear()
        h=heading('반복적으로 나타나는 반응은 해석의 출발점입니다')
        rows=VGroup(*[box(s,-4.5,y,MUTED,w=3.1) for s,y in [('고양이 A',1.3),('고양이 B',0),('비고양이',-1.3)]])
        cells=VGroup(*[Square(side_length=.6,stroke_color='#314657',stroke_width=1,fill_color=GOLD if c==1 else BLUE,
                    fill_opacity=([.3,.9,.4,.2][c] if r<2 else [.4,.15,.65,.3][c]))
                    .move_to([-1.1+c*.8,1.3-r*1.3,0]) for r in range(3) for c in range(4)])
        col=text('반복되는 패턴',21,GOLD).move_to([-.3,2.35,0])
        target=box('표현된 정보의 단서',4.7,0,BLUE,w=3.7)
        play(FadeIn(h),FadeIn(rows),FadeIn(cells),FadeIn(col),FadeIn(target))
        column=VGroup(cells[1],cells[5],cells[9])
        play(Circumscribe(column,color=GOLD))
        link=Arrow([2.05,0,0],target.get_left(),color=BLUE,buff=.05)
        play(GrowArrow(link))
        until(7)

        start(8);clear()
        h=heading('크게 활성화됨과, 판정에 중요함을 구분해야 합니다')
        left=box('얼마나 크게 켜지는가',-3.2,0,GOLD,w=5.1)
        right=box('답에 얼마나 영향을 주는가',3.2,0,BLUE,w=5.1)
        neq=text('≠',44,PINK)
        play(FadeIn(h),FadeIn(left),FadeIn(right),FadeIn(neq))
        q=footer('함께 나타남 → 관찰 / 역할 확인 → 개입')
        play(FadeIn(q))
        until(8)

        start(9);clear()
        h=heading('두 activation을 비교해보겠습니다')
        A=activation(-2.7,2.6,GOLD,'activation A')
        B=activation(2.7,.75,BLUE,'activation B')
        play(FadeIn(h),FadeIn(VGroup(A[0],A[2],B[0],B[2])))
        until(9)

        start(10)
        play(GrowFromEdge(A[1],DOWN),Transform(h,heading('첫 번째 값: 크게 활성화됩니다')))
        until(10)

        start(11)
        play(GrowFromEdge(B[1],DOWN),Transform(h,heading('두 번째 값: 상대적으로 작게 반응합니다')))
        until(11)

        start(12)
        play(Transform(h,heading('더 밝고 큰 값이, 더 중요할까요?')),Circumscribe(A[1],color=GOLD))
        question=footer('활성화 크기만으로 영향력을 순위 매길 수 있을까?')
        play(FadeIn(question))
        until(12)

        start(13)
        play(FadeOut(question),A.animate.shift(LEFT*1.2),B.animate.shift(LEFT*1.2),Transform(h,heading('큰 반응은 동반 출현을 보여줄 뿐입니다')))
        result=box('CAT',4.5,0,BLUE,w=2.2)
        paths=VGroup(DashedLine(A.get_right(),result.get_left(),color=MUTED),DashedLine(B.get_right(),result.get_left(),color=MUTED))
        play(FadeIn(result),Create(paths))
        qs=VGroup(text('영향?',22,MUTED).move_to([.3,1.2,0]),text('영향?',22,MUTED).move_to([3,-1,0]))
        play(FadeIn(qs))
        q=footer('최종 판단을 얼마나 지탱하는지는 아직 모릅니다')
        play(FadeIn(q))
        until(13)

        start(14)
        play(Transform(h,heading('작은 반응이 더 큰 영향을 줄 가능성도 있습니다')))
        play(Circumscribe(B[1],color=BLUE),paths[1].animate.set_color(BLUE))
        play(Transform(q,footer('가능성을 확인하려면 실제로 바꿔봐야 합니다')))
        until(14)

        start(15);clear()
        h=heading('feature는 뉴런 하나에만 대응하지 않을 수 있습니다')
        dots=VGroup(*[Circle(radius=.25,stroke_color=MUTED,fill_color=BLUE,fill_opacity=.18).move_to([-3.5+i,0,0]) for i in range(8)])
        play(FadeIn(h),FadeIn(dots))
        highlights=[0,2,3,6]
        play(*[dots[i].animate.set_fill(GOLD,opacity=.85).set_stroke(GOLD) for i in highlights])
        brace=Brace(VGroup(*[dots[i] for i in highlights]),DOWN,color=GOLD)
        caption=text('여러 뉴런에 걸친 방향 · 패턴',27,GOLD).next_to(brace,DOWN,.25)
        play(GrowFromCenter(brace),FadeIn(caption))
        weights=VGroup(*[text(v,20,MUTED).move_to([dots[i].get_x(),1,0]) for i,v in enumerate(['+','0','−','+','0','0','+','0'])])
        play(FadeIn(weights))
        until(15)

        start(16)
        play(Transform(h,heading('가장 밝은 뉴런 = 고양이 개념 전체?')))
        play(dots[3].animate.scale(1.4).set_fill(GOLD,opacity=1),Circumscribe(dots[3],color=GOLD))
        q=footer('밝기 하나로 개념의 저장 위치를 단정할 수 없습니다')
        play(FadeIn(q),FadeOut(brace),FadeOut(caption))
        until(16)

        start(17);clear()
        h=heading('반응하는 패턴의 의미도 아직 확정되지 않았습니다')
        p=photo(x=-4.7,width=3,height=3.4)
        candidates=VGroup(*[box(s,x,y,MUTED,w=3.6) for s,x,y in [('고양이 전체?',-.4,1.3),('털 · 귀?',3.8,1.3),('얼굴 배치?',-.4,-1.3),('함께 등장한 특징?',3.8,-1.3)]])
        play(FadeIn(h),FadeIn(p),FadeIn(candidates))
        for i,c in enumerate(candidates):
            play(Circumscribe(c,color=GOLD if i<3 else BLUE),rt=.75)
            if i<3:self.wait(.6)
        q=footer('관찰한 반응에 어떤 이름을 붙일 수 있을까?')
        play(FadeIn(q))
        until(17)

        start(18);clear()
        h=heading('의미를 붙이기 전에, 역할을 확인합니다')
        meaning=box('무엇을 의미하는가?',-3.2,0,MUTED,w=5)
        function=box('바꾸면 판정이 달라지는가?',3.2,0,BLUE,w=5.3)
        play(FadeIn(h),FadeIn(meaning),FadeIn(function))
        play(Circumscribe(function,color=BLUE))
        q=footer('내부 값 h → 개입한 값 h′ → 출력 비교')
        play(FadeIn(q))
        until(18)

        start(19);clear()
        h=heading('질문을 바꿉니다')
        before=box('많이 활성화되는 값',-3.6,0,GOLD,w=4.5)
        after=box('판정을 흔드는 값',3.6,0,BLUE,w=4.5)
        arrow=Arrow(before.get_right(),after.get_left(),color=BLUE,buff=.12)
        play(FadeIn(h),FadeIn(before))
        play(GrowArrow(arrow),FadeIn(after))
        until(19)

        start(20);clear()
        h=heading('두 activation에 같은 방식으로 개입해봅니다')
        A=activation(-3,2.5,GOLD,'activation A')
        B=activation(1,.7,BLUE,'activation B')
        result=box('CAT',5,0,BLUE,w=2.2)
        play(FadeIn(h),FadeIn(A),FadeIn(B),FadeIn(result))
        paths=VGroup(DashedLine(A.get_right(),result.get_left(),color=MUTED),DashedLine(B.get_right(),result.get_left(),color=MUTED))
        play(Create(paths))
        until(20)

        start(21)
        play(Circumscribe(A[1],color=GOLD))
        play(Circumscribe(B[1],color=BLUE))
        switches=VGroup(box('약화?',-3,-2.8,GOLD,w=2.3),box('약화?',1,-2.8,BLUE,w=2.3))
        play(FadeIn(switches))
        until(21)

        start(22)
        play(Transform(h,heading('어느 쪽을 바꾸면, 고양이 판단이 더 흔들릴까요?')))
        mark=text('?',44,BLUE).move_to([5,-1.6,0])
        play(FadeIn(mark),Indicate(result,color=BLUE))
        until(22)
