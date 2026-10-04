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

class Act01Hook(Scene):
    def construct(self):
        timing=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
        ends=[row[1] for row in timing['map'][1:]]
        def until(n):
            frames=round(ends[n-1]*30)-round(self.time*30)
            if frames>0:self.wait(frames/30)
        def play(*a,rt=.75):self.play(*a,run_time=round(rt*30)/30)
        def heading(s):return text(s,30).move_to([0,3.3,0])
        def footer(s):return text(s,25,width=12).move_to([0,-3.25,0])
        def clear():
            if self.mobjects:play(*[FadeOut(m) for m in list(self.mobjects)],rt=.3)
        def start(n):self.next_section(f'cue_{n:02}')

        start(1)
        p=photo(width=4.6,height=4.4)
        h=heading('고양이를 알아본다는 것은 무슨 뜻일까?')
        play(FadeIn(p,scale=.95),FadeIn(h),rt=.7)
        until(1)

        start(2)
        human=box('사람',-4.8,1.05,GOLD)
        ans_h=text('CAT',48,GOLD).move_to([-4.8,-.55,0])
        arrow_h=Arrow(p.get_left(),[-3.4,0,0],color=GOLD,buff=.15)
        q=footer('이 사진에 무엇이 있나요?')
        play(FadeIn(human),FadeIn(q))
        play(GrowArrow(arrow_h),Write(ans_h),rt=.7)
        until(2)

        start(3)
        ai=box('AI',4.8,1.05,BLUE)
        ans_a=text('CAT',48,BLUE).move_to([4.8,-.55,0])
        arrow_a=Arrow(p.get_right(),[3.4,0,0],color=BLUE,buff=.15)
        play(FadeIn(ai),GrowArrow(arrow_a),Write(ans_a))
        play(Transform(q,footer('사람도 CAT · AI도 CAT')))
        play(Circumscribe(ans_h,color=GOLD),Circumscribe(ans_a,color=BLUE))
        until(3)

        start(4)
        play(Transform(h,heading('같은 답이면, 같은 이유일까?')))
        clues=VGroup(box('무엇을 봤을까?',-4.8,-1.9,GOLD,w=3),box('무엇을 봤을까?',4.8,-1.9,BLUE,w=3))
        play(FadeIn(clues,shift=UP*.2),Transform(q,footer('결과는 같지만, 판단의 기준은 아직 모릅니다.')))
        until(4)

        start(5)
        play(FadeOut(p),FadeOut(arrow_h),FadeOut(arrow_a),FadeOut(clues))
        equals=text('=',55,MUTED)
        play(FadeIn(equals),human.animate.move_to([-3.5,1,0]),ai.animate.move_to([3.5,1,0]),
             ans_h.animate.move_to([-3.5,0,0]),ans_a.animate.move_to([3.5,0,0]))
        bracket=Line([-3.5,-1.2,0],[3.5,-1.2,0],color=MUTED)
        play(Create(bracket),Transform(q,footer('입력과 출력만 보면, 두 결과를 구분하기 어렵습니다.')))
        until(5)

        start(6);clear()
        h=heading('사진을 조금 바꿔보겠습니다')
        p=photo(width=4.6,height=4.4)
        play(FadeIn(p),FadeIn(h))
        mask=SurroundingRectangle(p[0],color=BLUE,buff=.06)
        play(Create(mask),rt=.5)
        until(6)

        start(7)
        play(FadeOut(mask),p.animate.shift(LEFT*2.5))
        p2=photo(x=2.5,color='#875065',width=4.6,height=4.4)
        play(FadeIn(p2))
        same=text('고양이 동일',23,GOLD).move_to([0,-2.65,0])
        bglabels=VGroup(text('배경 A',20,MUTED).move_to([-2.5,2.5,0]),text('배경 B',20,MUTED).move_to([2.5,2.5,0]))
        play(FadeIn(same),FadeIn(bglabels),Transform(h,heading('바꾼 것은 배경, 남겨둔 것은 고양이')))
        until(7)

        start(8)
        # Bars illustrate a possible change, without invented measured probabilities.
        play(p.animate.scale(.75).shift(UP*.45),p2.animate.scale(.75).shift(UP*.45),FadeOut(same),FadeOut(bglabels))
        base1=Rectangle(width=3.1,height=.24,stroke_width=0,fill_color='#293A49',fill_opacity=1).move_to([-2.5,-1.65,0])
        base2=base1.copy().move_to([2.5,-1.65,0])
        bar1=Rectangle(width=2.8,height=.24,stroke_width=0,fill_color=BLUE,fill_opacity=1).align_to(base1,LEFT).set_y(-1.65)
        bar2=bar1.copy().align_to(base2,LEFT)
        bar2.set_y(-1.65)
        bl=VGroup(text('고양이 점수',20,BLUE).move_to([-2.5,-2.12,0]),text('고양이 점수',20,BLUE).move_to([2.5,-2.12,0]))
        play(FadeIn(base1),FadeIn(base2),FadeIn(bar1),FadeIn(bar2),FadeIn(bl),Transform(h,heading('그런데 AI의 점수가 낮아진다면?')))
        play(bar2.animate.stretch_to_fit_width(.8).align_to(base2,LEFT),rt=.7)
        until(8)

        start(9)
        why=footer('고양이는 같은데, 왜 판단이 달라졌을까요?')
        play(FadeIn(why),Circumscribe(p[1],color=GOLD),Circumscribe(p2[1],color=GOLD))
        play(Indicate(bar2,color=PINK))
        until(9)

        start(10);clear()
        h=heading('다른 정보도 하나씩 바꿔봅니다')
        cards=Group(*[photo(x=x,width=3.7,height=3.7) for x in [-4.6,0,4.6]])
        labels=VGroup(*[text(s,22,MUTED).move_to([x,-2.4,0]) for s,x in [('털 무늬',-4.6),('얼굴 가림',0),('작은 패턴',4.6)]])
        play(FadeIn(h),FadeIn(cards),FadeIn(labels))
        until(10)

        start(11)
        tex=cat(True,3.45).move_to(cards[0][1])
        play(FadeOut(cards[0][1]),FadeIn(tex),Circumscribe(cards[0][0],color=GOLD),rt=.75)
        cards[0].remove(cards[0][1]);cards[0].add(tex)
        play(Transform(h,heading('전체 윤곽은 유지하고, 털 무늬를 바꿉니다')))
        until(11)

        start(12)
        cover=Rectangle(width=1.5,height=.55,fill_color='#162331',fill_opacity=1,stroke_width=0).shift(UP*.95)
        play(FadeIn(cover),labels[1].animate.set_color(GOLD),rt=.55)
        until(12)

        start(13)
        patch=VGroup(*[Square(side_length=.14,fill_opacity=1,stroke_width=0,color=BLUE if (r+c)%2 else GOLD)
                      .move_to([5.3+c*.14,-1+r*.14,0]) for r in range(4) for c in range(4)])
        play(FadeIn(patch),labels[2].animate.set_color(GOLD))
        play(Transform(h,heading('작은 패턴도 새로운 단서가 될 수 있습니다')))
        play(Circumscribe(patch,color=GOLD))
        until(13)

        start(14);clear()
        h=heading('변화에 대한 반응은 서로 다를 수 있습니다')
        left=box('사람',-3.8,1.8,GOLD);right=box('AI',3.8,1.8,BLUE)
        inp=photo(width=2.7,height=2.8)
        cover=Rectangle(width=1,height=.4,fill_opacity=1,fill_color='#162331',stroke_width=0).shift(UP*.6)
        lh=text('CAT 유지',31,GOLD).move_to([-3.8,0,0]);rh=text('판단 흔들림',31,PINK).move_to([3.8,0,0])
        play(FadeIn(h),FadeIn(inp),FadeIn(cover),FadeIn(left),FadeIn(right),FadeIn(lh),FadeIn(rh))
        play(Indicate(rh,color=PINK))
        halfway=(ends[13]+ends[12])/2
        if self.time<halfway:self.wait(round((halfway-self.time)*30)/30)
        grid=VGroup(*[Square(side_length=.33,stroke_width=0,fill_opacity=1,
                  fill_color=[BLUE,GOLD,'#426570','#8B6980'][(r*7+c*3)%4]).move_to([(c-3)*.33,(r-3)*.33,0])
                  for r in range(7) for c in range(7)])
        play(FadeOut(inp),FadeOut(cover),FadeIn(grid),Transform(lh,text('알아보기 어려움',28,MUTED).move_to(lh)),
             Transform(rh,text('CAT로 강하게 반응?',28,BLUE).move_to(rh)))
        until(14)

        start(15);clear()
        h=heading('이 반응을 모든 AI에 일반화할 수는 없습니다')
        inp=photo(width=2.6,height=2.8).move_to([-4.8,0,0])
        models=VGroup(*[box('모델 '+s,1.3,y,BLUE,w=2.1) for s,y in [('A',1.5),('B',0),('C',-1.5)]])
        arrows=VGroup(*[Arrow(inp.get_right(),m.get_left(),color=MUTED,stroke_width=2,buff=.15) for m in models])
        play(FadeIn(h),FadeIn(inp),LaggedStart(*[FadeIn(m) for m in models],lag_ratio=.2))
        play(Create(arrows))
        tags=VGroup(*[text(s,21,c).move_to([4,y,0]) for s,y,c in [('유지',1.5,GOLD),('변화?',0,PINK),('다른 반응?',-1.5,BLUE)]])
        play(FadeIn(tags))
        factors=VGroup(*[box(s,x,-2.9,MUTED,w=3.2) for s,x in [('모델 구조',-4),('학습 데이터',0),('변형 방식',4)]])
        play(LaggedStart(*[FadeIn(m,shift=UP*.15) for m in factors],lag_ratio=.3),rt=1.2)
        until(15)

        start(16);clear()
        h=heading('누가 더 잘 맞히는가?')
        human=box('사람',-3,0,GOLD);ai=box('AI',3,0,BLUE)
        vs=text('VS',42,MUTED)
        play(FadeIn(h),FadeIn(human),FadeIn(ai),FadeIn(vs))
        cross=VGroup(Line([-1,-.5,0],[1,.5,0],color=PINK),Line([-1,.5,0],[1,-.5,0],color=PINK))
        play(Create(cross),rt=.5)
        until(16)

        start(17);clear()
        h=heading('우리가 확인하려는 것은 판단의 기준입니다')
        result=box('CAT',4.9,0,BLUE,w=2)
        inp=photo(width=2.4,height=2.8).move_to([-5,0,0])
        sources=VGroup(*[box(s,0,y,MUTED,w=3.6) for s,y in [('형태?',1.45),('털 무늬?',0),('배경?',-1.45)]])
        paths=VGroup(*[DashedLine(inp.get_right(),b.get_left(),color=MUTED) for b in sources],
                     *[DashedLine(b.get_right(),result.get_left(),color=MUTED) for b in sources])
        play(FadeIn(h),FadeIn(inp),FadeIn(result),FadeIn(sources),Create(paths))
        play(Indicate(sources[0]),Indicate(sources[1]),Indicate(sources[2]),rt=1)
        until(17)

        start(18)
        play(Transform(h,heading('정답을 맞혔다 = 고양이를 알아봤다?')))
        ring=SurroundingRectangle(result,color=BLUE,buff=.12)
        play(Create(ring))
        q=footer('‘맞혔다’에서 ‘알아봤다’로 넘어가도 될까요?')
        play(FadeIn(q))
        until(18)

        start(19)
        play(FadeOut(ring),Transform(h,heading('‘알아봤다’고 말하려면 무엇까지 확인해야 할까?')))
        play(Transform(q,footer('출력의 이름만 같으면 충분할까요?')))
        until(19)

        start(20)
        play(Circumscribe(result,color=BLUE))
        play(Transform(q,footer('정답 → 실제로 사용한 정보')))
        play(Circumscribe(sources,color=GOLD),rt=1)
        until(20)

        start(21)
        play(Transform(h,heading('기대한 특징과, 사용한 특징은 다를 수 있습니다')))
        play(sources[0].animate.set_color(GOLD),sources[2].animate.set_color(PINK))
        imagined=text('기대',19,GOLD).move_to([2.5,1.45,0]);unknown=text('사용했을까?',19,PINK).move_to([2.5,-1.45,0])
        play(FadeIn(imagined),FadeIn(unknown),Transform(q,footer('정답 하나만으로는 이 경로를 확정할 수 없습니다.')))
        until(21)

        start(22)
        play(FadeOut(imagined),FadeOut(unknown),FadeOut(inp),FadeOut(paths),FadeOut(sources),FadeOut(q))
        calc=box('내부 계산',-1.8,0,BLUE,w=5.2)
        link=Arrow(calc.get_right(),result.get_left(),color=BLUE,buff=.1)
        play(FadeIn(calc),GrowArrow(link),Transform(h,heading('이제 결과를 만든 계산을 살펴봅니다')))
        until(22)

        start(23)
        nodes=VGroup(*[Circle(radius=.13,stroke_color=BLUE,fill_color=BLUE,fill_opacity=.5).move_to([-3.4+i*.8,.0,0]) for i in range(5)])
        play(FadeOut(calc[1]),LaggedStart(*[FadeIn(n) for n in nodes],lag_ratio=.2))
        question=footer('판단을 지탱한 정보는 무엇이었을까?')
        play(FadeIn(question),Indicate(nodes[2]))
        until(23)

        start(24)
        play(Transform(question,footer('그 정보를 바꿔보면, 무엇을 확인할 수 있을까?')),
             nodes[2].animate.set_color(GOLD),Transform(h,heading('다음: 입력을 바꿔보면 차이가 보인다')),rt=.7)
        until(24)
