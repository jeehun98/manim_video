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

class Act05MeaningAndPaths(Scene):
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
        def heading(s):return text(s,30).move_to([0,3.35,0])
        def footer(s):return text(s,25).move_to([0,-3.3,0])
        def score(x,y,w=2.7):
            bg=Rectangle(width=3,height=.23,stroke_width=0,fill_color='#293A49',fill_opacity=1).move_to([x,y,0])
            bar=Rectangle(width=w,height=.23,stroke_width=0,fill_color=BLUE,fill_opacity=1).align_to(bg,LEFT).set_y(y)
            return VGroup(bg,bar)
        def layer(x,y=0):
            return VGroup(*[Circle(radius=.15,stroke_color=BLUE,fill_color=BLUE,fill_opacity=.28)
                           .move_to([x,y+(1.5-i)*.7,0]) for i in range(4)])

        start(1)
        h=heading('05 / 중요한 방향을 찾았다면, 의미도 찾은 걸까?')
        f=box('내부 방향 v',-3.8,0,GOLD,w=3.2)
        out=box('고양이 점수',3.8,1,BLUE,w=3.2)
        s=score(3.8,-.4)
        link=Arrow(f.get_right(),out.get_left(),color=BLUE,buff=.1)
        play(FadeIn(h),FadeIn(f),FadeIn(out),FadeIn(s),GrowArrow(link))
        play(s[1].animate.stretch_to_fit_width(.85).align_to(s[0],LEFT))
        q=footer('이 방향을 ‘고양이 feature’라고 불러도 될까?')
        play(FadeIn(q))
        until(1)

        start(2);clear()
        h=heading('판단에 중요한 것과, 무엇을 의미하는가는 다릅니다')
        function=box('판정에 영향을 준다',-3.2,0,GOLD,w=4.8)
        meaning=box('고양이라는 개념을 뜻한다',3.2,0,BLUE,w=4.8)
        neq=text('≠',44,PINK)
        play(FadeIn(h),FadeIn(function),FadeIn(meaning),FadeIn(neq))
        q=footer('고양이가 공유하는 일부 특징일 가능성도 있습니다')
        play(FadeIn(q),Circumscribe(meaning,color=BLUE))
        until(2)

        start(3);clear()
        h=heading('판정에 도움이 되는 특징의 후보들')
        p=photo(x=-4.7,width=3,height=3.6)
        traits=VGroup(*[box(s,x,y,MUTED,w=3.7) for s,x,y in [('털 질감 · 귀',-.3,1.3),('눈 · 코 배치',3.9,1.3),('얼굴 형태',-.3,-1.3),('몸의 윤곽',3.9,-1.3)]])
        play(FadeIn(h),FadeIn(p),FadeIn(traits))
        for i,t in enumerate(traits):play(Circumscribe(t,color=GOLD),rt=.6)
        until(3)

        start(4);clear()
        h=heading('고양이에게 자주 나타나지만, 고양이만의 특징은 아닙니다')
        animals=Group(input_photo('cat_photo.png',-4.5),input_photo('dog_photo.png',0),input_photo('fox_photo.png',4.5))
        tags=VGroup(*[text(s,22,MUTED).move_to([x,-2.25,0]) for s,x in [('고양이',-4.5),('강아지',0),('여우',4.5)]])
        play(FadeIn(h),FadeIn(animals),FadeIn(tags))
        fur=footer('털: 여러 동물에게 공유되는 특징')
        play(FadeIn(fur),Circumscribe(animals[0],color=GOLD),Circumscribe(animals[1],color=GOLD))
        play(Transform(fur,footer('뾰족한 귀: 고양이와 비고양이에서 모두 나타날 수 있습니다')),
             Circumscribe(animals[0],color=BLUE),Circumscribe(animals[2],color=BLUE))
        until(4)

        start(5);clear()
        h=heading('‘고양이’라는 이름과, 내부 방향의 의미를 구분합니다')
        name=box('우리가 붙인 이름: 고양이',0,1.35,GOLD,w=6.4)
        candidates=VGroup(*[box(s,x,-.9,BLUE,w=3.6) for s,x in [('공유 특징?',-4.5),('복합 패턴?',0),('다른 단서?',4.5)]])
        play(FadeIn(h),FadeIn(name))
        arrows=VGroup(*[DashedLine(name.get_bottom(),c.get_top(),color=MUTED) for c in candidates])
        play(FadeIn(candidates),Create(arrows))
        until(5)

        start(6);clear()
        h=heading('한 방향 안에 여러 패턴이 섞여 있을 수도 있습니다')
        dots=VGroup(*[Circle(radius=.17,stroke_color=MUTED,fill_color=BLUE,fill_opacity=.15).move_to([-2.5+i*.75,0,0]) for i in range(8)])
        play(FadeIn(h),FadeIn(dots))
        layers=VGroup(*[box(s,x,y,c,w=3.2) for s,x,y,c in [('털 · 귀',-3.5,1.8,GOLD),('자세 · 얼굴',3.5,1.8,BLUE)]])
        play(FadeIn(layers))
        play(*[dots[i].animate.set_fill(GOLD,opacity=.9).set_stroke(GOLD) for i in [0,2,5]])
        play(*[dots[i].animate.set_fill(BLUE,opacity=.9).set_stroke(BLUE) for i in [2,3,6]])
        q=footer('사람의 단어 하나로 분리하기 어려운 복합 패턴일 수 있습니다')
        play(FadeIn(q))
        until(6)

        start(7)
        play(Transform(h,heading('이름은 해석이며, 실제 표현은 확인할 대상입니다')))
        bracket=Brace(dots,DOWN,color=MUTED)
        named=text('‘고양이’ ?',28,GOLD).next_to(bracket,DOWN,.2)
        play(GrowFromCenter(bracket),FadeIn(named),FadeOut(q))
        until(7)

        start(8);clear()
        h=heading('feature를 해석할 때 따라오는 두 질문')
        functional=box('1 / 판단에 영향을 주는가?',-3.3,0,GOLD,w=5.4)
        semantic=box('2 / 무엇을 나타내는가?',3.3,0,BLUE,w=5.4)
        play(FadeIn(h),FadeIn(functional))
        play(FadeIn(semantic))
        sub=VGroup(text('기능적 역할',24,GOLD).move_to([-3.3,-1.25,0]),text('의미',24,BLUE).move_to([3.3,-1.25,0]))
        play(FadeIn(sub))
        until(8)

        start(9)
        play(Transform(h,heading('첫 번째 질문: 개입으로 기능적 역할을 검증합니다')))
        play(functional.animate.move_to([0,1,0]),FadeOut(semantic),FadeOut(sub))
        bars=VGroup(*[score(x,-1.4) for x in [-4.5,0,4.5]])
        labels=VGroup(*[text(s,21,MUTED).move_to([x,-2,0]) for s,x in [('입력 A',-4.5),('입력 B',0),('입력 C',4.5)]])
        play(FadeIn(bars),FadeIn(labels))
        play(*[b[1].animate.stretch_to_fit_width(w).align_to(b[0],LEFT) for b,w in zip(bars,[.8,1,.7])],rt=1)
        q=footer('여러 입력에서 약화 → 점수 하락이 반복되는가?')
        play(FadeIn(q))
        until(9)

        start(10);clear()
        h=heading('두 번째 질문: 의미를 확인하려면 더 많은 비교가 필요합니다')
        animals=Group(input_photo('cat_photo.png',-4.5),input_photo('dog_photo.png',0),input_photo('fox_photo.png',4.5))
        q=footer('다른 털 달린 동물에서도 같은 방향이 반응할까?')
        play(FadeIn(h),FadeIn(animals),FadeIn(q))
        until(10)

        start(11);clear()
        h=heading('고양이의 모습이 달라져도 유지될까?')
        pa=input_photo('cat_photo.png',-2.7,width=3.7,height=3.5)
        pb=input_photo('cat_second.png',2.7,width=3.7,height=3.5)
        play(FadeIn(h),FadeIn(pa),FadeIn(pb))
        until(11)

        start(12)
        lying=input_photo('cat_lying.png',2.7,width=3.7,height=3.5);lying[0].set_fill('#875065')
        play(FadeOut(pb),FadeIn(lying),Transform(h,heading('배경과 자세가 바뀌어도 비슷하게 나타날까?')))
        until(12)

        start(13)
        bars=VGroup(score(-2.7,-2.35),score(2.7,-2.35))
        play(FadeIn(bars),Transform(h,heading('여러 입력에서 개입 효과도 반복될까?')))
        play(*[b[1].animate.stretch_to_fit_width(w).align_to(b[0],LEFT) for b,w in zip(bars,[.85,1])])
        until(13)

        start(14);clear()
        h=heading('이름 붙이기에서, 해석의 범위를 좁혀가기로')
        steps=VGroup(*[box(s,x,0,c,w=3.7) for s,x,c in [('나타나는 조건',-4.5,GOLD),('연결된 정보',0,BLUE),('판단에서의 역할',4.5,BLUE)]])
        arrows=VGroup(*[Arrow(steps[i].get_right(),steps[i+1].get_left(),color=MUTED,buff=.05) for i in range(2)])
        play(FadeIn(h))
        for i,step in enumerate(steps):
            play(FadeIn(step))
            if i<2:play(GrowArrow(arrows[i]),rt=.45)
        q=footer('어디까지 설명할 수 있는지, 비교와 개입으로 확인합니다')
        play(FadeIn(q))
        until(14)

        start(15);clear()
        h=heading('최종 판단은 feature 하나만으로 만들어질까?')
        one=box('feature 하나',-3.5,0,GOLD,w=3.4);out=box('CAT',3.5,0,BLUE,w=2.6)
        arrow=Arrow(one.get_right(),out.get_left(),color=MUTED,buff=.1)
        play(FadeIn(h),FadeIn(one),FadeIn(out),GrowArrow(arrow))
        other=VGroup(box('다른 정보',-3.5,1.7,MUTED,w=3.4),box('다른 정보',-3.5,-1.7,MUTED,w=3.4))
        paths=VGroup(*[DashedLine(o.get_right(),out.get_left(),color=MUTED) for o in other])
        play(FadeIn(other),Create(paths))
        until(15)

        start(16);clear()
        h=heading('정보는 만들어지고, 결합되고, 다음 층으로 전달됩니다')
        columns=VGroup(*[layer(x) for x in [-4,-1,2]])
        out=box('CAT',5,0,BLUE,w=2.1)
        links=VGroup(*[Line(a.get_center(),b.get_center(),color='#314657',stroke_width=1) for i in range(2) for a in columns[i] for b in columns[i+1]])
        final=VGroup(*[Line(n.get_center(),out.get_left(),color='#314657',stroke_width=1) for n in columns[2]])
        names=VGroup(*[text('Layer '+str(i+1),22,MUTED).move_to([x,2,0]) for i,x in enumerate([-4,-1,2])])
        play(FadeIn(h),Create(links),Create(final),FadeIn(columns),FadeIn(names),FadeIn(out))
        play(columns[0][1].animate.set_fill(GOLD,opacity=1).set_stroke(GOLD))
        play(columns[1][1].animate.set_fill(GOLD,opacity=1).set_stroke(GOLD),columns[1][2].animate.set_fill(BLUE,opacity=1))
        play(columns[2][2].animate.set_fill(GOLD,opacity=1).set_stroke(GOLD),Indicate(out))
        until(16)

        start(17)
        play(Transform(h,heading('어디서 만들어지고, 무엇과 작동하며, 어디로 전달되는가?')))
        route=VGroup(Line(columns[0][1].get_center(),columns[1][1].get_center(),color=GOLD,stroke_width=4),
                     Line(columns[1][1].get_center(),columns[2][2].get_center(),color=GOLD,stroke_width=4),
                     Line(columns[2][2].get_center(),out.get_left(),color=GOLD,stroke_width=4))
        for path in route:play(Create(path),rt=.7)
        side=Line(columns[0][3].get_center(),columns[1][1].get_center(),color=BLUE,stroke_width=4)
        play(Create(side),columns[0][3].animate.set_fill(BLUE,opacity=1))
        q=footer('중요한 feature → 상호작용 → 계산 경로 → 출력')
        play(FadeIn(q))
        until(17)

        start(18);clear()
        h=heading('Explainable AI / 설명은 어디까지 확인했는가?')
        p=photo(x=-4.8,width=2.8,height=3.3)
        region=RoundedRectangle(width=1.1,height=1.2,corner_radius=.15,stroke_color=PINK,
                                fill_color=PINK,fill_opacity=.15).move_to([-4.65,.65,0])
        seen=box('“이 부분을 봤습니다”',0,0,PINK,w=4.4)
        beyond=box('내부의 역할과 연결은?',4.6,0,BLUE,w=3.9)
        play(FadeIn(h),FadeIn(p),FadeIn(region),FadeIn(seen),FadeIn(beyond))
        q=footer('반응한 영역을 보여주는 것만으로 해석이 끝나지는 않습니다')
        play(FadeIn(q))
        until(18)

        start(19);clear()
        h=heading('반응 · 기능 · 연결을 함께 확인합니다')
        checks=VGroup(*[box(s,x,0,c,w=3.8) for s,x,c in [('무엇에 반응했는가',-4.5,GOLD),('판정에 영향을 줬는가',0,BLUE),('어떻게 연결되는가',4.5,BLUE)]])
        play(FadeIn(h))
        for c in checks:play(FadeIn(c),Circumscribe(c,color=c[0].get_color()),rt=.8)
        until(19)

        start(20);clear()
        h=heading('다시, 처음의 고양이 사진으로 돌아갑니다')
        p=photo(width=4.3,height=4.2)
        human=VGroup(text('사람',24,MUTED),text('CAT',48,GOLD)).arrange(DOWN,.4).move_to([-4.8,0,0])
        ai=VGroup(text('AI',24,MUTED),text('CAT',48,BLUE)).arrange(DOWN,.4).move_to([4.8,0,0])
        play(FadeIn(h),FadeIn(p))
        play(FadeIn(human))
        play(FadeIn(ai))
        until(20)

        start(21)
        q=footer('같은 정답 사이에, 이제 더 많은 질문이 보입니다')
        play(FadeIn(q),Transform(h,heading('사람도 CAT · AI도 CAT')))
        play(Circumscribe(human[1],color=GOLD),Circumscribe(ai[1],color=BLUE))
        until(21)

        start(22);clear()
        h=heading('결과 뒤에 남는 네 가지 질문')
        queries=VGroup(*[box(s,x,y,c,w=5.7) for s,x,y,c in [('어떤 특징에 반응했는가?',-3.25,1.1,GOLD),('개입하면 판정이 흔들리는가?',3.25,1.1,BLUE),('그 방향은 무엇을 나타내는가?',-3.25,-1.1,GOLD),('어떤 계산 경로를 거치는가?',3.25,-1.1,BLUE)]])
        play(FadeIn(h))
        for query in queries:play(FadeIn(query),rt=.65)
        until(22)

        start(23);clear()
        h=heading('정답을 맞혔다고, 원하는 것을 배웠다고 단정할 수는 없습니다')
        inp=box('입력',-4.7,0,GOLD,w=2.7)
        internal=box('내부 구조',0,0,BLUE,w=3.6)
        out=box('출력',4.7,0,BLUE,w=2.7)
        arrows=VGroup(Arrow(inp.get_right(),internal.get_left(),buff=.1,color=MUTED),Arrow(internal.get_right(),out.get_left(),buff=.1,color=MUTED))
        play(FadeIn(h),FadeIn(inp),FadeIn(internal),FadeIn(out),Create(arrows))
        probe=box('개입',0,1.8,GOLD,w=2.4)
        down=Arrow(probe.get_bottom(),internal.get_top(),buff=.1,color=GOLD)
        play(FadeIn(probe),GrowArrow(down))
        play(Circumscribe(internal,color=GOLD),Indicate(out,color=BLUE))
        q=footer('무엇을 바꾸면 판단이 달라지는가 / 내부에서 어떻게 만들어지는가')
        play(FadeIn(q))
        until(23)

        start(24);clear()
        title=text('고양이를 알아본다는 것은\n무슨 뜻일까?',43,width=11)
        subtitle=text('EXPLAINABLE AI',20,BLUE).move_to([0,-1.9,0])
        play(Write(title),FadeIn(subtitle),rt=1.2)
        frames=round((ends[-1]-.7)*30)-round(self.time*30)
        if frames>0:self.wait(frames/30)
        play(FadeOut(title),FadeOut(subtitle),rt=.7)
        until(24)
