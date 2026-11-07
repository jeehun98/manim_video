"""20 replaceable shots; exact narration times; shared animation for two layouts."""
import json
import os
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text, p as raw_point, FONT, INK, MUTED
from quantum_series.shared.components import wave
from longforms.qcs01_speed.layouts import Layout

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE/'script.json').read_text(encoding='utf-8'))
PORTRAIT = os.getenv('QCS_LAYOUT', 'shorts') == 'shorts'
PREVIEW = os.getenv('QCS_PREVIEW') == '1'
FPS = 60
config.frame_width, config.frame_height = (9,16) if PORTRAIT else (16,9)
config.pixel_width, config.pixel_height = ((360,640) if PORTRAIT else (640,360)) if PREVIEW else ((1080,1920) if PORTRAIT else (1920,1080))
config.frame_rate = FPS
config.background_color = '#0D1526'
BLUE, PURPLE, GREEN, ORANGE = '#55B8FF', '#B794F6', '#40D6B0', '#FFB36B'
L=Layout(PORTRAIT)
p=L.point

def label(s, x=0, y=0, size=30, color=INK, width=7.5):
    return text(s,x,L.y(y),size,color,width)

def tile(s, color=BLUE, width=1.25, height=.8):
    return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.12,
        stroke_color=color,stroke_width=2,fill_color=color,fill_opacity=.10),
        text(s,size=27,color=color,width=width-.14))

def grid(n=16, columns=4, size=.95, labels=True):
    bits=max(1,int(np.log2(n)))
    cells=VGroup(*[tile(format(i,f'0{bits}b') if labels else '',PURPLE,size,size*.72) for i in range(n)])
    cells.arrange_in_grid(cols=columns,buff=.12)
    return cells

def grover_states(n, target, steps):
    state=np.ones(n)/np.sqrt(n)
    result=[state.copy()]
    for _ in range(steps):
        state=state.copy();state[target]*=-1
        result.append(state.copy())
        state=2*np.mean(state)-state
        result.append(state.copy())
    return result


def oracle_phase(phi):
    state=np.ones(4,dtype=complex)/2
    state[3]*=np.exp(1j*phi)
    return state

class AmplitudeChart(VGroup):
    """Real-part bars and separate Born probabilities, calculated from normalized states."""
    def __init__(self,state,probability=False):
        super().__init__();self.probability=probability;self.xs=np.linspace(-2.6,2.6,4);self.base=-.4;self.unit=2.4
        self.axis=Line(p(-3.45,self.base),p(3.45,self.base),color=MUTED,stroke_width=1.3)
        self.add(self.axis);self.rects=[];self.values=[];self.probs=[]
        for i,x in enumerate(self.xs):
            r=Rectangle(width=.72,height=.01,stroke_width=0,fill_opacity=.85)
            val=label(' ',size=22);prob=label(' ',size=22)
            self.rects.append(r);self.values.append(val);self.probs.append(prob)
            self.add(r,val,label('|'+format(i,'02b')+'⟩',x,-2.4,23,BLUE),prob)
        self.set_state(state)
    def endpoint(self,i,value):return p(self.xs[i],self.base+self.unit*value)
    def set_state(self,state):
        state=np.asarray(state,dtype=complex);assert np.isclose(np.vdot(state,state),1)
        self.state=state.copy();probs=np.abs(state)**2
        for i,x in enumerate(self.xs):
            value=float(probs[i] if self.probability else state[i].real)
            h=max(abs(value)*self.unit,.006);c=ORANGE if value<-.001 else GREEN if i==3 else PURPLE
            self.rects[i].become(Rectangle(width=.72,height=L.y(h),stroke_width=0,fill_color=c,fill_opacity=.85).move_to(p(x,self.base+np.sign(value)*h/2)))
            shown=f'{probs[i]*100:.0f}%' if self.probability else f'{value:+.2f}'
            key=(shown,c)
            if getattr(self.values[i],'key',None)!=key:
                self.values[i].become(label(shown,size=22,color=c));self.values[i].key=key
            self.values[i].move_to(p(x,self.base+(h+.25 if value>=0 else -h-.25)))
            shown=f'P = {probs[i]*100:.0f}%'
            if getattr(self.probs[i],'key',None)!=shown:
                self.probs[i].become(label(shown,size=21,color=GREEN if i==3 else MUTED));self.probs[i].key=shown
            self.probs[i].move_to(p(x,-3.0))
        return self
    def mean_line(self):
        mean=float(np.mean(self.state).real)
        return DashedLine(p(-3.4,self.base+self.unit*mean),p(3.4,self.base+self.unit*mean),color=ORANGE,stroke_width=2)

class QCSScene(Scene):
    data=DATA
    shot=0
    def setup(self):
        self.info=self.data['scenes'][self.shot]
        self.offset=self.info['start']
        self.always_update_mobjects=True
        self.head_y=L.heading_y
        self.note_y=L.note_y
        self.max_width=7.7 if PORTRAIT else 14.4
        self.add(text('과학 한조각  /  양자컴퓨터',y=L.brand_y,size=18,color=MUTED))
        self.add(Line(raw_point(-3.8 if PORTRAIT else -7.2,6.65 if PORTRAIT else 3.67),
                      raw_point(3.8 if PORTRAIT else 7.2,6.65 if PORTRAIT else 3.67),color=MUTED,stroke_width=1,stroke_opacity=.3))
        self.title=text(self.info['title'],y=self.head_y,size=34,width=self.max_width)
        self.add(self.title)
        self.bounds=[]
        self.caption_records=[]
        self.caption_index=-2
        self.caption=VGroup().set_z_index(40)
        panel=Rectangle(width=8.25 if PORTRAIT else 15,height=2.5 if PORTRAIT else 1.65,
                        stroke_width=0,fill_color=config.background_color,fill_opacity=1)
        panel.move_to(raw_point(0,L.caption_y)).set_z_index(39)
        self.add(panel,self.caption)
        self.caption_panel=panel
        self.update_caption(self.caption)
        self.caption.add_updater(self.update_caption)

    def update_caption(self,mob,dt=0):
        now=self.offset+self.time
        starts=[s['start'] for s in self.data['sentences']]
        index=bisect_right(starts,now+1e-7)-1
        if index==self.caption_index:return
        self.caption_index=index
        sentence=self.data['sentences'][index]
        lines=[];line=''
        for word in sentence['text'].split():
            if line and len(line)+len(word)+1>L.caption_chars:lines.append(line);line=word
            else:line=(line+' '+word).strip()
        lines.append(line)
        caption=Text('\n'.join(lines),font=FONT,font_size=30 if PORTRAIT else 29,
                     color=INK,line_spacing=1.1)
        if caption.width>L.caption_width:caption.scale_to_fit_width(L.caption_width)
        if caption.height>L.caption_height:caption.scale_to_fit_height(L.caption_height)
        caption.move_to(raw_point(0,L.caption_y))
        assert caption.get_top()[1] < (-4.9 if PORTRAIT else -2.6)
        assert caption.get_bottom()[1] > (-7.5 if PORTRAIT else -4.25)
        self.caption_records.append({'sentence':index+1,'at':round(now,6),'lines':len(lines),
                                     'width':caption.width,'height':caption.height})
        mob.become(caption).set_z_index(40)

    def to(self,target):
        frames=round((target-self.offset-self.time)*FPS)
        if frames < 0:raise RuntimeError(f'{self.shot+1}: overrun {self.offset+self.time} > {target}')
        if frames:self.wait(frames/FPS-1e-8)

    def show(self,*objects,run_time=.6):
        self.play(*[FadeIn(o,shift=UP*.08) for o in objects],run_time=run_time)

    def note(self,s,color=MUTED):
        if hasattr(self,'footnote'):self.remove(self.footnote)
        o=text(s,y=self.note_y,size=21,color=color,width=self.max_width)
        self.show(o,run_time=.3)
        self.footnote=o
        return o

    def replace(self,o,s,color=INK,size=36):
        self.play(Transform(o,text(s,*o.get_center()[:2],size,color,self.max_width)),run_time=.5)

    def bars(self,values,probability=False):
        g=VGroup(); xs=np.linspace(-2.6,2.6,len(values)); base=-.6
        g.add(Line(p(-3.45,base),p(3.45,base),color=MUTED,stroke_width=1.4))
        for i,(x,v) in enumerate(zip(xs,values)):
            height=max(abs(float(v))*2.7,.012)
            c=GREEN if i==len(values)-1 and v>=0 else ORANGE if v<0 else PURPLE
            r=Rectangle(width=.72,height=L.y(height),stroke_width=0,fill_color=c,fill_opacity=.85)
            r.move_to(p(x,base+np.sign(v)*height/2))
            g.add(r,label(f'{v*100:.0f}%' if probability else f'{v:+.2f}',x,base+(height+.32 if v>=0 else -height-.32),22,c),
                  label('|'+format(i,'02b')+'⟩',x,-2.85,23,BLUE))
        return g

    def mark_grid(self,g,probs):
        return [g[i][0].animate.set_fill(GREEN if i==len(g)-1 else PURPLE,opacity=.06+.90*float(probs[i])) for i in range(len(g))]

    def construct(self):
        getattr(self,f's{self.shot+1:02}')()
        self.to(self.info['end'])
        self.caption.remove_updater(self.update_caption)
        # Narration subtitles occupy an independent lower band.
        for m in self.mobjects:
            if m is self.caption or m is self.caption_panel:continue
            if not m.has_points() and len(m)==0:continue
            if m.width>0 and m.height>0:
                assert m.get_left()[0]>=-config.frame_width/2+.12 and m.get_right()[0]<=config.frame_width/2-.12, (self.shot,m)
                assert m.get_bottom()[1]>=(-4.9 if PORTRAIT else -2.6) and m.get_top()[1]<=config.frame_height/2-.1,(self.shot,m)
        audit=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE.parents[1]/'media/qcs01_captioned/manual_audit')))
        audit.mkdir(parents=True,exist_ok=True)
        (audit/(self.info['id']+'.json')).write_text(json.dumps(self.caption_records),encoding='utf-8')

    def chart(self,state=None,probability=False):
        return AmplitudeChart(np.ones(4)/2 if state is None else state,probability)

    def phase_flip(self,chart,duration=1.2):
        self.play(UpdateFromAlphaFunc(chart,lambda m,a:m.set_state(oracle_phase(PI*a))),run_time=duration,rate_func=linear)
        chart.set_state(grover_states(4,3,1)[1])

    def s01(self):
        b=tile('0',width=2,height=1.6).move_to(p(0,.8));self.show(b)
        self.to(1.3);self.play(Transform(b,tile('1',width=2,height=1.6).move_to(b)),run_time=.4)
        self.to(2);self.play(Transform(b,tile('0',width=2,height=1.6).move_to(b)),run_time=.4)
        self.to(3)
        row=VGroup(*[tile(c,width=.76,height=.85) for c in '01011010']).arrange(RIGHT,buff=.12).move_to(p(0,1.4))
        self.play(Transform(b,row),run_time=.7)
        self.show(label('같은 0과 1\n다른 정보의 표현',y=-1.1,size=37,color=PURPLE))
        self.note('일반적인 컴퓨터  →  양자컴퓨터')

    def s02(self):
        centers=[p(0,2.1),p(0,-.9)] if PORTRAIT else [p(-3.7,.3),p(3.7,.3)]
        classic=VGroup(text('BIT',y=1,size=22,color=BLUE),tile('0  또는  1',width=3,height=1.1)).move_to(centers[0])
        quantum=VGroup(text('QUBIT',y=1,size=22,color=PURPLE),tile('α |0⟩ + β |1⟩',PURPLE,5,1.1)).move_to(centers[1])
        self.show(classic);self.show(quantum);self.play(Circumscribe(quantum,color=PURPLE),run_time=.8)
        self.note('중첩 = 기저 상태 + 각각의 확률 진폭')

    def s03(self):
        self.show(label('|ψ⟩ = α |0⟩ + β |1⟩',y=2.3,size=40,color=PURPLE))
        self.show(label('|0⟩     α     →     |α|²',y=.8,size=34),label('|1⟩     β     →     |β|²',y=-.1,size=34))
        self.show(label('α = β = 1/√2',y=-1.7,size=30,color=PURPLE),label('50%                 50%',y=-2.7,size=27,color=GREEN))
        self.note('실수 진폭의 예 · |α|² + |β|² = 1')

    def s04(self):
        g=grid(2,2,1.7);self.show(g)
        count=label('n 큐비트  →  2ⁿ개',y=3.4,size=32,color=PURPLE);self.show(count)
        self.to(26);self.replace(count,'1 큐비트  →  2개',PURPLE,31)
        for t,n in [(27.5,4),(29.2,8)]:
            self.to(t);self.play(Transform(g,grid(n,4,1.35)),run_time=.55)
            self.replace(count,f'{int(np.log2(n))} 큐비트  →  {n}개',PURPLE,31)
        self.note('개수는 계산 기저 상태의 수')

    def s05(self):
        dots=VGroup(*[Dot(radius=.026,color=PURPLE).move_to(p((i%16-7.5)*.35,(i//16-7.5)*.22)) for i in range(256)])
        self.show(dots)
        f=label('2²⁰ = 1,048,576',y=3.4,size=42,color=PURPLE);self.show(f)
        self.note('기저 상태에 대한 진폭 · 도형 수는 축약 표시')

    def s06(self):
        g=grid(64,8,L.dense_grid_size,False);self.show(g)
        self.show(label('수많은 답을\n동시에 읽을 수 있을까?',y=3.4 if PORTRAIT else 3.8,size=31))
        self.to(42);self.show(label('그렇지 않습니다',y=-2.8 if PORTRAIT else -3.3,size=34,color=ORANGE))

    def s07(self):
        g=grid().move_to(p(0,.5));self.add(g)
        self.show(label('한 번의 측정 → 하나의 비트열',y=3.6 if PORTRAIT else 3.9,size=30))
        self.to(45)
        self.play(*[g[i].animate.set_opacity(0) for i in range(16) if i!=5],g[5].animate.set_color(GREEN),run_time=.7)
        self.show(label('측정 결과의 예:  |0101⟩',y=-2.2 if PORTRAIT else -3,size=31,color=GREEN))
        self.to(49);self.note('중첩만으로 원하는 정답을 얻을 수는 없음')

    def s08(self):
        panels=[]
        for opposite,title,c in [(False,'A + A = 2A',GREEN),(True,'A − A = 0',ORANGE)]:
            w=2.8 if PORTRAIT else 4.5
            group=VGroup(wave(w,.22,2,BLUE).shift(UP*.65),wave(w,.22,2,PURPLE,PI if opposite else 0),
                         wave(w,0 if opposite else .44,2,c).shift(DOWN*.9),text(title,y=1.4,size=25,color=c))
            panels.append(group)
        if PORTRAIT:panels[0].move_to(p(0,1.9));panels[1].move_to(p(0,-1.7))
        else:panels[0].move_to(p(-3.5,.2));panels[1].move_to(p(3.5,.2))
        self.show(*panels);self.note('일반 파동의 비유 · 같은 위치에서 값이 더해짐')

    def s09(self):
        nodes=VGroup(tile('|0⟩',BLUE),tile('|1⟩',BLUE)).arrange(DOWN,buff=2 if PORTRAIT else 1.3).move_to(p(-2.5,0))
        out=tile('|0⟩',GREEN).move_to(p(2.4,0));self.show(nodes,out)
        paths=VGroup(*[Arrow(n.get_right(),out.get_left(),buff=.15,color=c,stroke_width=3) for n,c in zip(nodes,[BLUE,PURPLE])])
        self.play(Create(paths),run_time=.7)
        self.show(label('a₁',0,1.15,31,BLUE),label('a₂',0,-1.15,31,PURPLE),label('a₁ + a₂',y=3.2,size=43,color=GREEN))
        self.note('경로 = 같은 출력에 기여하는 수학적 전이 항')

    def s10(self):
        x=0 if PORTRAIT else -3.3
        self.show(label('+0.5 + 0.5 = 1',x,2.7,32,GREEN),label('+0.5 − 0.5 = 0',x,1.5,32,ORANGE))
        cx,cy=(0,-.6) if PORTRAIT else (3.8,.8)
        origin=p(cx,cy);plane=VGroup(Line(origin+LEFT*1.1,origin+RIGHT*1.1,color=MUTED,stroke_width=1),Line(origin+DOWN*1.1,origin+UP*1.1,color=MUTED,stroke_width=1),
            Arrow(origin,origin+RIGHT*.9,buff=0,color=PURPLE),Arrow(origin,origin+UP*.9,buff=0,color=BLUE),text('복소 진폭 · 방향은 위상',size=20,color=MUTED).move_to(origin+DOWN*1.4))
        self.show(plane)
        self.to(72);self.show(label('P(x) = |a₁ + a₂|²',y=-2.9 if PORTRAIT else -2.6,size=38,color=PURPLE))
        self.note('±0.5는 한 출력에 기여하는 경로의 예')

    def s11(self):
        self.show(label('간섭을 계산에 이용한다',y=2.8,size=34,color=PURPLE))
        self.to(79);g=grid(4,4,1.5);self.show(g)
        self.to(82);self.play(g[3][0].animate.set_stroke(GREEN,width=3),run_time=.5)
        self.note('정답 표시는 시청자용 · 알고리즘의 사전 지식이 아님')

    def s12(self):
        g=grid(4,4,1.1).move_to(p(0,3.3));self.show(g)
        chart=self.chart();self.show(chart)
        for i in range(4):self.play(Indicate(g[i],color=BLUE),run_time=.35)
        self.play(FadeOut(g),run_time=.4)

    def s13(self):
        self.add(self.chart())
        self.add(label('진폭 +0.5  →  확률 25%',y=3.7,size=29,color=PURPLE))
        self.note('막대: 진폭의 실수부 · 아래: 관측 확률')

    def s14(self):
        chart=self.chart();self.add(chart)
        stage=label('오라클: 정답 판별 규칙',y=3.7,size=30,color=PURPLE);self.show(stage)
        self.to(94.5)
        self.note('막대는 실수부 · 위상 회전 중에는 허수부도 존재')
        self.phase_flip(chart,1.5)
        self.to(99);self.replace(stage,'부호 반전 ≠ 확률 증가',ORANGE,31)
        self.note('진폭은 −0.5 · 관측 확률은 여전히 25%',ORANGE)

    def s15(self):
        before,after=grover_states(4,3,1)[1:]
        chart=self.chart(before);self.add(chart)
        mean=chart.mean_line();self.show(mean)
        self.show(label('평균 ā = 0.25',y=2.8,size=28,color=ORANGE),label('aᵢ′ = 2ā − aᵢ',y=3.8,size=32,color=ORANGE))
        dots=VGroup(*[Dot(chart.endpoint(i,float(v)),radius=.065,color=GREEN if i==3 else PURPLE) for i,v in enumerate(before)])
        routes=VGroup(*[DashedLine(chart.endpoint(i,float(v)),chart.endpoint(i,float(after[i])),color=GREEN if i==3 else PURPLE,stroke_width=2) for i,v in enumerate(before)])
        self.show(routes,dots)
        self.note('점의 이동은 평균 반사의 작도 · 중간 계산 상태가 아님')
        self.to(104.5)
        self.play(*[d.animate.move_to(chart.endpoint(i,float(after[i]))) for i,d in enumerate(dots)],run_time=1.4,rate_func=linear)
        chart.set_state(after);self.play(FadeOut(dots),FadeOut(routes),run_time=.3)
        self.note('+0.5 → 0     −0.5 → +1',GREEN)

    def s16(self):
        chart=self.chart(probability=True);self.add(chart)
        stage=label('연산 전 · 각각 25%',y=3.7,size=30,color=PURPLE);self.show(stage)
        self.to(114)
        chart.probability=False;chart.set_state(np.ones(4)/2)
        self.replace(stage,'① 오라클: 부호 반전',ORANGE,30)
        self.note('막대: 실수부 · 회전 중에도 각 확률은 25%')
        self.phase_flip(chart,1.2)
        mean=chart.mean_line();self.show(mean)
        self.to(117);self.replace(stage,'② 확산: 평균 반사',GREEN,30)
        chart.set_state(grover_states(4,3,1)[2])
        self.note('확산 후 · 정답 진폭 +1 · 관측 확률 100%',GREEN)
        self.play(FadeOut(mean),run_time=.3)
        self.to(119);chart.probability=True;chart.set_state(grover_states(4,3,1)[2])
        self.replace(stage,'정답 관측 확률 100%',GREEN,32)
        self.note('막대: 관측 확률 · 모든 확률의 합 100%',GREEN)
        self.to(121);self.note('그로버 반복 1회 = 오라클 1회 + 확산 1회',GREEN)

    def s17(self):
        g=grid(64,8,L.dense_grid_size,False);self.show(g)
        states=grover_states(64,63,6)
        status=label('N = 64 · 초기 정답 확률 1.56%',y=3.6,size=28,color=PURPLE);self.show(status)
        for k in range(1,7):
            self.play(*self.mark_grid(g,states[2*k]**2),run_time=.48)
        self.replace(status,'6회 반복 · 정답 확률 99.66%',GREEN,28)
        self.to(129);self.play(FadeOut(g),FadeOut(status),run_time=.4)
        box=tile('f(x) = 정답 여부',BLUE,4.6,1.3)
        box[0].set_fill(config.background_color,opacity=1)
        self.show(box,label('|x⟩',y=2.2,size=32,color=PURPLE),label('(−1)ᶠ⁽ˣ⁾ |x⟩',y=-2,size=34,color=ORANGE))
        self.note('판별 규칙을 회로로 구현 · 적절한 횟수만 반복')
        self.to(136);self.show(label('규칙 → 간섭 → 높은 정답 확률',y=3.7,size=27,color=GREEN))
        self.to(138);self.note('적절한 반복 횟수 필요 · 과도하면 확률 감소')

    def s18(self):
        size=label('정답 하나인 비구조적 검색',y=3.6,size=30,color=MUTED);self.show(size)
        self.show(label('고전 검색',-1.95,1.8,29,BLUE,width=3.5),label('그로버 검색',1.95,1.8,29,PURPLE,width=3.5))
        self.show(label('O(N)',-1.95,.2,44,BLUE,width=3.5),label('O(√N)',1.95,.2,44,GREEN,width=3.5))
        self.note('조회 횟수의 규모 비교 · 실제 실행시간과 구별')
        self.to(151)
        self.replace(size,'N = 1,000,000',INK,40)
        self.show(label('최대 10⁶',-1.95,-1.2,35,BLUE,width=3.5),label('10³ 규모',1.95,-1.2,35,GREEN,width=3.5))
        self.show(label('이상적 반복 수 ≈ (π/4)√N',y=-2.7,size=27,color=MUTED))

    def s19(self):
        f=label('조회 횟수 ≠ 실행시간',y=2.7,size=38,color=ORANGE);self.show(f)
        self.note('오라클 구현 비용 · 게이트 수 · 오류 정정 등')
        self.to(163);self.replace(f,'중첩 ≠ 속도 향상',ORANGE,43)
        self.show(self.chart())

    def s20(self):
        chart=self.chart();self.add(chart)
        self.phase_flip(chart,.7)
        chart.set_state(grover_states(4,3,1)[2])
        self.to(170)
        self.play(chart.animate.scale(.45).move_to(p(0,2.5)),run_time=.7)
        result=label('더 적은 조회',y=-.3,size=54,color=GREEN);self.show(result)
        self.show(label('중첩 → 연산 → 간섭 → 조회 감소',y=-2.7,size=27,color=PURPLE))
        self.to(174.5)
        if os.getenv('QCS_ENDING','standalone')=='standalone':
            self.play(FadeOut(chart),FadeOut(result),run_time=.5)
