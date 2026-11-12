"""Eleven independently replaceable shots, synchronized to approved speech."""
import json
import os
import sys
from pathlib import Path
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import BG, FONT, INK, MUTED, GOOD, PRUNE, SPARSE, ACCENT, WeightMatrix, pill, configure_vertical
configure_vertical()
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
BLUE='#56B4FF'; YELLOW='#F3CF75'; PURPLE=SPARSE
INITIAL=[[.30,.80],[.20,.60]]
FINAL=[[.27,.84],[.18,.63]]

def text(s,y=0,x=0,size=28,color=INK,width=7.6):
    o=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.15)
    if o.width>width:o.scale_to_fit_width(width)
    return o.move_to([x,y,0])

def block(label,x=0,y=0,w=2,color=BLUE):
    return pill(label,color,w).move_to([x,y,0])

def arrow(a,b,color=BLUE):
    return Arrow(a,b,buff=.13,color=color,stroke_width=3,tip_length=.15)

def matrix(values=FINAL,y=0,x=0):
    m=WeightMatrix(values,cell_size=.95).set_color(YELLOW).move_to([x,y,0])
    return VGroup(m,text('Model Weights',y+1.35,x,22,YELLOW,3))

def network(y=1.5):
    layers=VGroup(*[VGroup(*[Circle(radius=.13,color=BLUE,fill_opacity=.35,fill_color=BLUE).move_to([x,y+(j-1)*.65,0]) for j in range(3)]) for x in [-2.5,0,2.5]])
    edges=VGroup(*[Line(a.get_center(),b.get_center(),color=BLUE,stroke_width=1.4,stroke_opacity=.35) for l,r in zip(layers,layers[1:]) for a in l for b in r])
    return VGroup(edges,layers)

def gpu(x=0,y=0):
    body=RoundedRectangle(width=3.4,height=2.5,corner_radius=.2,color=BLUE,fill_color=BLUE,fill_opacity=.07)
    units=VGroup(*[Square(side_length=.35,color=BLUE,fill_color=BLUE,fill_opacity=.25,stroke_width=1) for _ in range(24)]).arrange_in_grid(rows=4,cols=6,buff=.12)
    pins=VGroup(*[Line([a,b,0],[a,b+.2,0],color=MUTED) for a in np.linspace(-1.4,1.4,8) for b in [-1.45,1.25]])
    return VGroup(body,units,pins).move_to([x,y,0])

def cache(n=6,y=-1.8):
    keys=VGroup(*[block(f'K{i+1}',w=.8,color=GOOD) for i in range(n)]).arrange(RIGHT,buff=.13)
    vals=VGroup(*[block(f'V{i+1}',w=.8,color=GOOD) for i in range(n)]).arrange(RIGHT,buff=.13).next_to(keys,DOWN,buff=.16)
    return VGroup(keys,vals).move_to([0,y,0])

def wrap(s,limit=27):
    lines=[];current=''
    for word in s.split():
        if current and len(current)+len(word)+1>limit:lines.append(current);current=word
        else:current=(current+' '+word).strip()
    if current:lines.append(current)
    return '\n'.join(lines)

class TimedShot(Scene):
    NUMBER=1

    def refresh(self,target=None):
        t=self.offset+self.time if target is None else target
        idx=next((i for i,s in enumerate(DATA['segments']) if s['start']<=t+1e-5<s['end']),len(DATA['segments'])-1)
        if idx<=self.caption_index:return
        self.caption_index=idx
        c=text(wrap(DATA['segments'][idx]['text']),-6.2,size=25,width=7.5)
        assert c.height<2.15,('caption height',idx,c.height)
        self.caption.become(c)
        self.caption.set_z_index(20)
        self.audit.append(dict(sentence=idx+1,at=round(self.offset+self.time,5)))

    def play(self,*args,**kwargs):
        self.refresh()
        result=super().play(*args,**kwargs)
        self.refresh()
        self.check_bounds()
        return result

    def check_bounds(self):
        for item in self.mobjects:
            if item is self.caption or item is self.chrome:continue
            if not item.has_points() and not item.submobjects:continue
            assert item.get_left()[0]>=-4.15 and item.get_right()[0]<=4.15,('horizontal',self.NUMBER,self.time,item.get_left(),item.get_right())
            assert item.get_bottom()[1]>=-4.8 and item.get_top()[1]<=5.05,('caption or header overlap',self.NUMBER,self.time,item.get_bottom(),item.get_top())

    def to(self,target):
        local=target-self.offset
        if self.time>local+1/30+1e-6:raise ValueError(f'Shot {self.NUMBER}: {self.time+self.offset} > {target}')
        boundaries=[s['start']-self.offset for s in DATA['segments'] if self.time+1e-5<s['start']-self.offset<local-1e-5]+[local]
        for end in boundaries:
            if end-self.time>1e-5:self.wait(end-self.time)
            self.refresh(self.offset+end)

    def at(self,t,*animations,duration=.7):
        self.to(t)
        self.play(*animations,run_time=duration)

    def note(self,s,y=-4.1,color=MUTED,size=23):
        o=text(s,y,size=size,color=color)
        self.play(FadeIn(o),run_time=.4)
        return o

    def construct(self):
        spec=DATA['scenes'][self.NUMBER-1];self.offset=spec['start']
        self.audit=[];self.caption_index=-1;self.caption=VGroup()
        self.chrome=VGroup(text('과학 한조각  /  GPU',7.35,size=20,color=MUTED),
                 text('학습과 추론',6.55,size=38),text(spec['title'],5.62,size=26,color=YELLOW),
                 Line([-3.8,5.13,0],[3.8,5.13,0],color=MUTED,stroke_opacity=.25),
                 Line([-3.8,-4.9,0],[3.8,-4.9,0],color=MUTED,stroke_opacity=.25))
        self.add(self.chrome,self.caption)
        self.refresh()
        getattr(self,f's{self.NUMBER:02}')()
        self.to(spec['end'])
        assert abs(self.time-(spec['end']-spec['start']))<1/30+1e-6
        audit_dir=Path(os.environ.get('AIWORK_AUDIT',str(HERE.parents[1]/'media/aiwork01/audit')))
        audit_dir.mkdir(parents=True,exist_ok=True)
        (audit_dir/f'{self.NUMBER:02}.json').write_text(json.dumps(self.audit),encoding='utf-8')

    def s01(self):
        g=gpu(y=.65);mode=block('TRAINING',y=3.4,w=3,color=PURPLE)
        self.play(FadeIn(g),FadeIn(mode),run_time=.8)
        batch=VGroup(*[block(f'DATA {i+1}',x=-2.5+i*.65,y=-2.1,w=1.3,color=PURPLE) for i in range(4)])
        self.at(1, LaggedStart(*[FadeIn(p,shift=UP*.3) for p in batch],lag_ratio=.12))
        self.at(2,*[p.animate.move_to(g.get_center()).scale(.3).set_opacity(0) for p in batch],duration=1)
        self.at(4,mode.animate.move_to([-2,3.4,0]),FadeIn(block('INFERENCE',2,3.4,3,GOOD)))
        q=block('질문',-2.5,-1.5,1.5);answer=VGroup(*[block(w,w=1.5,color=GOOD) for w in ['답변','토큰','생성']]).arrange(RIGHT,buff=.3).move_to([0,-2.8,0])
        self.at(5,FadeIn(q))
        self.at(6,q.animate.move_to(g.get_center()).set_opacity(0),LaggedStart(*[FadeIn(p) for p in answer],lag_ratio=.4),duration=1)
        self.at(7.4,FadeIn(text('같은 GPU · 서로 다른 데이터 흐름',-4,size=26,color=YELLOW)))

    def s02(self):
        net=network(2.2);w=matrix(INITIAL,y=-.35);w[1].move_to([2.3,-.35,0])
        fwd=arrow([-3.1,3.5,0],[3.1,3.5,0]);fl=text('Forward  ·  X × W',4.1,size=25,color=BLUE)
        self.play(FadeIn(net),FadeIn(w),GrowArrow(fwd),FadeIn(fl),run_time=1)
        pulse=Dot([-2.5,2.2,0],color=BLUE,radius=.15)
        self.add(pulse);self.at(11,pulse.animate.move_to([2.5,2.2,0]),duration=1.1)
        self.at(15,Indicate(w,color=YELLOW))
        loss=VGroup(block('예측 0.7',-1.8,-2.3,2.6),block('정답 1.0',1.8,-2.3,2.6,GOOD),text('차이 → Loss L',-3.4,size=28,color=PRUNE))
        self.at(19,FadeIn(loss))
        back=arrow([3.1,1.1,0],[-3.1,1.1,0],PURPLE)
        gradient=text('Backward  ·  ∂L/∂W',-1.65,size=25,color=PURPLE)
        self.at(21,GrowArrow(back),FadeIn(gradient))
        self.at(23,Indicate(w,color=PURPLE))
        self.at(25,FadeOut(loss),FadeIn(text('W ← W − η ∂L/∂W',-2.6,size=34,color=YELLOW)))
        new=matrix(FINAL,y=-.35);new[1].move_to([2.3,-.35,0])
        self.at(27,Transform(w,new),duration=1)
        self.at(28.5,FadeIn(text('0.30 → 0.27     0.80 → 0.84',-3.5,size=25,color=YELLOW)))
        self.at(30,Indicate(net,color=BLUE),Indicate(back,color=PURPLE),duration=.8)
        self.note('순전파 → 역전파 → 가중치 갱신',-4.3,color=INK)

    def s03(self):
        net=network(2.2);w=matrix(y=-.35)
        self.play(FadeIn(net),FadeIn(w),FadeIn(block('WEIGHTS FIXED',y=-2.1,w=4,color=YELLOW)),run_time=.8)
        fwd=arrow([-3.1,3.5,0],[3.1,3.5,0]);self.at(35,GrowArrow(fwd),FadeIn(text('Forward',4.1,size=25,color=BLUE)))
        for t,label,out in [(38,'질문 A','답변 A'),(41,'질문 B','답변 B')]:
            token=block(label,-2.5,2.2,1.7);result=block(out,2.5,2.2,1.7,GOOD)
            self.at(t,FadeIn(token))
            self.at(t+1,token.animate.move_to([0,2.2,0]).set_opacity(0),FadeIn(result))
            self.at(t+2,FadeOut(result))
        self.at(44,FadeIn(text('역전파 없음 · 가중치 갱신 없음',-3.2,size=27,color=GOOD)))
        self.at(48,Indicate(w,color=YELLOW))
        self.at(50,FadeIn(text('대화가 이어져도 같은 W',-4.2,size=27,color=YELLOW)))

    def s04(self):
        w=matrix(y=2.9);w.scale(.8,about_point=[0,2.9,0])
        self.play(FadeIn(w),FadeIn(block('고정',2.6,3,1.3,YELLOW)),run_time=.6)
        msgs=VGroup(block('사용자: 나는 민수야',-.6,.8,5.7),block('AI: 반가워, 민수!',.5,-.4,5.7,GOOD),block('사용자: 내 이름은?',-.6,-1.6,5.7))
        for t,m in zip([56,58,60],msgs):self.at(t,FadeIn(m,shift=UP*.15))
        frame=SurroundingRectangle(msgs,buff=.22,color=BLUE)
        self.at(61,Create(frame),FadeIn(text('이전 대화 + 새 질문 = 입력 문맥',-3,size=26,color=BLUE)))
        self.at(63,GrowArrow(arrow([3.35,-.4,0],[2.1,2.5,0],BLUE)))
        self.note('문맥으로 제공된 내용을 참고한다',-4.15,color=INK)

    def s05(self):
        w=matrix(y=3);w.scale(.7,about_point=[0,3,0]);self.add(w)
        rows=VGroup()
        for r,n in enumerate([4,8,16,32]):
            row=VGroup(*[Square(side_length=.15,color=BLUE,fill_color=BLUE,fill_opacity=.6,stroke_width=.5) for _ in range(n)]).arrange(RIGHT,buff=.035)
            row.move_to([0,1.4-r*1.15,0]);row.add(text(str(n),1.4-r*1.15,-3.5,23,BLUE,1))
            rows.add(row)
        self.play(FadeIn(rows[0]),run_time=.5)
        for t,r in zip([67,68,69],rows[1:]):self.at(t,FadeIn(r))
        repeat=VGroup(*[CurvedArrow([2.7,-2-i*.22,0],[-2.7,-2-i*.22,0],angle=-.3,color=PRUNE,stroke_width=2,tip_length=.12) for i in range(3)])
        self.at(70,Create(repeat))
        self.note('캐시가 없다면 과거 K,V도 다시 계산',-4.15,color=PRUNE)

    def s06(self):
        w=matrix(y=3.1);w.scale(.65,about_point=[0,3.1,0]);self.add(w,block('고정',2.8,3.2,1.2,YELLOW))
        token=block('토큰 A',-2.7,1,1.7);proj=block('Projection',0,1,2.4)
        qkv=VGroup(*[block(s,2.8,y,1.1,c) for s,y,c in [('Q',1.7,BLUE),('K',.7,GOOD),('V',-.3,GOOD)]])
        c=cache(6,-2.2)
        self.play(FadeIn(token),FadeIn(proj),GrowArrow(arrow(token.get_right(),proj.get_left())),run_time=.7)
        self.at(76,FadeIn(qkv),*[GrowArrow(arrow(proj.get_right(),p.get_left(),BLUE if i==0 else GOOD)) for i,p in enumerate(qkv)])
        self.at(77,GrowArrow(arrow([2.8,1.3,0],[1.5,-.6,0])),FadeIn(text('Attention',-.8,1,23,BLUE,2.5)))
        self.at(78,TransformFromCopy(qkv[1],c[0][0]),TransformFromCopy(qkv[2],c[1][0]))
        self.at(79,Transform(token,block('토큰 B',-2.7,1,1.7)),FadeIn(c[0][1]),FadeIn(c[1][1]))
        self.at(80,GrowArrow(arrow([1,-1,0],c[0][0].get_top(),GOOD)))
        self.at(81,FadeIn(text('KV CACHE',-3.7,size=30,color=GOOD)))
        for t,i in [(83,2),(84,3),(85,4),(86,5)]:self.at(t,FadeIn(c[0][i]),FadeIn(c[1][i]),duration=.45)
        self.at(87,FadeIn(text('W 고정  /  저장 토큰 수에 따라 상태 증가',-4.4,size=22,color=YELLOW)),duration=.4)

    def s07(self):
        g=gpu(y=1.7);g.scale(.8,about_point=[0,1.7,0]);c=cache(5,-1.5)
        self.play(FadeIn(g),FadeIn(text('입력 처리 → 답변 생성',4.3,size=29)),run_time=.7)
        tokens=VGroup(*[block(s,w=1.2) for s in ['GPU','는','어떻게','계산','할까?']]).arrange(RIGHT,buff=.14).move_to([0,3.5,0])
        label=text('PREFILL · 입력 토큰 병렬 처리',-.1,size=26,color=BLUE)
        self.at(91,FadeIn(tokens),FadeIn(label))
        self.at(92,*[p.animate.move_to(g.get_center()).scale(.25).set_opacity(0) for p in tokens],duration=1)
        self.at(94,Indicate(g[1],color=BLUE),FadeIn(c),duration=.8)
        self.at(97,Transform(label,text('DECODE · 출력 토큰 사이의 의존성',-.1,size=24,color=GOOD)))
        out=VGroup(*[block(s,w=1.75,color=GOOD) for s in ['GPU는','병렬로','계산해요']]).arrange(RIGHT,buff=.55).move_to([0,-3.35,0])
        for i,t in enumerate([98,100,102]):
            self.at(t,FadeIn(out[i]),Indicate(g[1],color=BLUE),Indicate(c,color=GOOD),duration=.6)
            if i:self.play(GrowArrow(arrow(out[i-1].get_right(),out[i].get_left(),GOOD)),run_time=.3)
        self.note('각 토큰 내부의 연산은 여전히 병렬',-4.4,size=22)

    def s08(self):
        hbm=RoundedRectangle(width=2.7,height=3.7,corner_radius=.15,color=GOOD).move_to([-2.2,1,0])
        wt=block('Weights',-2.2,1.8,2.2,YELLOW);kv=block('KV Cache',-2.2,.4,2.2,GOOD)
        units=VGroup(*[Square(side_length=.52,color=MUTED,fill_color=MUTED,fill_opacity=.12) for _ in range(12)]).arrange_in_grid(rows=4,cols=3,buff=.16).move_to([2.15,1,0])
        channel=VGroup(Line([-.7,.7,0],[.9,.7,0],color=MUTED),Line([-.7,1.3,0],[.9,1.3,0],color=MUTED))
        self.play(FadeIn(hbm),FadeIn(wt),FadeIn(kv),FadeIn(units),Create(channel),FadeIn(text('HBM',3.5,-2.2,27,GOOD)),FadeIn(text('GPU 연산',3.5,2.1,25,BLUE,3)),run_time=.8)
        self.note('적은 동시 요청의 Decode · 개념도',4.45,size=21)
        packets=VGroup(*[Square(side_length=.24,color=YELLOW if i%2==0 else GOOD,fill_color=YELLOW if i%2==0 else GOOD,fill_opacity=.8).move_to([-.55-i*.32,1,0]) for i in range(5)])
        self.at(106,FadeIn(packets))
        for t,i in [(107,0),(109,1),(110.7,2)]:
            self.at(t,packets[i].animate.move_to([1.35,1,0]),duration=.8)
            self.play(units[i].animate.set_fill(BLUE,opacity=.9),FadeOut(packets[i]),run_time=.25)
            self.play(units[i].animate.set_fill(MUTED,opacity=.12),run_time=.25)
        self.at(113,FadeIn(text('WAITING FOR DATA',-2.15,size=33,color=PRUNE)))
        self.at(115,FadeIn(text('데이터 공급 속도가 처리량을 제한',-3.15,size=27,color=PRUNE)))
        self.note('연산 능력 ≠ 실제 처리 속도',-4.2,color=INK)

    def s09(self):
        w=matrix(y=3);w.scale(.7,about_point=[0,3,0]);self.add(w)
        self.play(FadeIn(text('가중치는 공유',4.5,size=26,color=YELLOW)),run_time=.5)
        for i,(label,n) in enumerate([('A',2),('B',4),('C',6)]):
            y=.9-i*1.55
            row=VGroup(*[block('KV',w=.7,color=GOOD) for _ in range(n)]).arrange(RIGHT,buff=.12).move_to([.3,y,0]).align_to([-.9,y,0],LEFT)
            self.at(118.7+i,FadeIn(block(label,-2.8,y,1,BLUE)),FadeIn(row),duration=.5)
        self.note('요청마다 별도의 문맥 상태',-4.15,color=GOOD)

    def s10(self):
        before=VGroup(*[block(s,w=1.7,color=BLUE) for s in ['연산 A','중간값','연산 B']]).arrange(RIGHT,buff=.6).move_to([0,2.7,0])
        links=VGroup(*[arrow(a.get_right(),b.get_left(),PRUNE) for a,b in zip(before,before[1:])])
        n1=text('중간값 쓰기 → 다시 읽기',3.8,size=25,color=PRUNE)
        n2=text('데이터 이동 ↓   실행 횟수 ↓',-1,size=27,color=GOOD)
        n3=text('수학 연산은 유지 · 불필요한 이동 감소',-2.15,size=23,color=MUTED)
        self.play(FadeIn(before),Create(links),FadeIn(n1),run_time=.8)
        fused=block('A + B · 하나의 커널',y=.3,w=5.5,color=GOOD)
        self.at(126,TransformFromCopy(before,fused))
        self.at(128,FadeIn(n2))
        self.at(130,FadeIn(n3))
        cap=VGroup(*[Square(side_length=.28,color=GOOD,fill_color=GOOD,fill_opacity=.4) for _ in range(18)]).arrange_in_grid(rows=3,cols=6,buff=.1).move_to([-2,-2.8,0])
        lanes=VGroup(*[arrow([.7,-2.4-i*.35,0],[3.2,-2.4-i*.35,0],BLUE) for i in range(3)])
        self.at(133,FadeOut(before),FadeOut(links),FadeOut(fused),FadeOut(n1),FadeOut(n2),FadeOut(n3),FadeIn(text('HBM',2,size=40,color=GOOD)),FadeIn(cap),Create(lanes))
        self.at(134,FadeIn(text('용량',-1.5,-2,size=28,color=GOOD)),FadeIn(text('대역폭',-1.5,2,size=28,color=BLUE)))
        self.at(136,FadeIn(text('저장할 수 있는 양',-4,-2,size=22,color=GOOD,width=3.5)),FadeIn(text('시간당 옮기는 양',-4,2,size=22,color=BLUE,width=3.5)))

    def s11(self):
        train=VGroup(text('학습',3.9,-2,size=32,color=PURPLE),block('Forward',-2,2.7,3,PURPLE),block('Backward',-2,1.5,3,PURPLE),block('Update W',-2,.3,3,YELLOW))
        infer=VGroup(text('추론',3.9,2,size=32,color=GOOD),block('Prefill',2,2.7,3,BLUE),block('Decode',2,1.5,3,GOOD),block('KV Cache',2,.3,3,GOOD))
        lead=text('연산 · 메모리 · 실행 지연을 함께 분석',-1.4,size=25,color=MUTED)
        self.play(FadeIn(train),FadeIn(infer),FadeIn(lead),run_time=.9)
        self.at(145,FadeOut(train),FadeOut(infer),FadeOut(lead))
        labels=VGroup();bars=VGroup()
        for i,(s,length,c) in enumerate([('연산',2,BLUE),('데이터 이동',4.8,PRUNE),('실행 오버헤드',1.2,PURPLE)]):
            y=3.4-i*1.5
            labels.add(text(s,y,-2.8,23,c,2.4))
            bars.add(Rectangle(width=length,height=.45,color=c,fill_color=c,fill_opacity=.65).move_to([-.9+length/2,y,0]))
        example=text('예시 실행시간 · 실측값 아님',-1,size=22,color=MUTED)
        priority=text('가장 오래 걸리는 구간부터',-2.2,size=30,color=PRUNE)
        analysis=text('반복되는 연산 · 재사용 데이터 · 소요 시간',-3.4,size=23,color=INK)
        self.at(146,FadeIn(labels),LaggedStart(*[GrowFromEdge(b,LEFT) for b in bars],lag_ratio=.15),FadeIn(example))
        self.at(149,Indicate(bars[1],color=PRUNE),FadeIn(priority))
        self.at(152,FadeIn(analysis))
        self.at(155,FadeOut(labels),FadeOut(bars),FadeOut(example),FadeOut(priority),FadeOut(analysis),FadeIn(text('무엇이 느린지\n먼저 이해하라',2,size=45,color=YELLOW)))
        self.at(157,FadeIn(text('OPTIMIZE THE BOTTLENECK',-.2,size=25,color=GOOD)))

class Shot01(TimedShot):NUMBER=1
class Shot02(TimedShot):NUMBER=2
class Shot03(TimedShot):NUMBER=3
class Shot04(TimedShot):NUMBER=4
class Shot05(TimedShot):NUMBER=5
class Shot06(TimedShot):NUMBER=6
class Shot07(TimedShot):NUMBER=7
class Shot08(TimedShot):NUMBER=8
class Shot09(TimedShot):NUMBER=9
class Shot10(TimedShot):NUMBER=10
class Shot11(TimedShot):NUMBER=11

