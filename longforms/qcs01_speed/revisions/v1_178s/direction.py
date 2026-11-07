"""18 replaceable shots; exact narration times; shared animation for two layouts."""
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
BLUE, PURPLE, GREEN, ORANGE = '#55B8FF', '#B794F6', '#40D6B0', '#FFAF68'
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

class QCSScene(Scene):
    shot=0
    def setup(self):
        self.info=DATA['scenes'][self.shot]
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
        starts=[s['start'] for s in DATA['sentences']]
        index=bisect_right(starts,now+1e-7)-1
        if index==self.caption_index:return
        self.caption_index=index
        sentence=DATA['sentences'][index]
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

    def s01(self):
        b=tile('0',width=2,height=1.6).move_to(p(0,.8)); self.show(b)
        self.to(1.4);self.play(Transform(b,tile('1',width=2,height=1.6).move_to(b)),run_time=.5)
        self.to(3)
        row=VGroup(*[tile(c,width=1,height=.9) for c in '010110']).arrange(RIGHT,buff=.14).move_to(p(0,1.4))
        self.play(Transform(b,row),run_time=.8)
        q=label('같은 0과 1\n다른 정보의 표현',y=-1.1,size=37,color=PURPLE)
        self.show(q);self.note('일반적인 컴퓨터  →  양자컴퓨터')

    def s02(self):
        centers=[p(0,2.1),p(0,-.9)] if PORTRAIT else [p(-3.7,.3),p(3.7,.3)]
        classic=VGroup(text('BIT',y=1,size=22,color=BLUE),tile('0  또는  1',width=3,height=1.1)).move_to(centers[0])
        quantum=VGroup(text('QUBIT',y=1,size=22,color=PURPLE),tile('α |0⟩ + β |1⟩',PURPLE,5,1.1)).move_to(centers[1])
        self.show(classic);self.show(quantum)
        self.play(Circumscribe(quantum,color=PURPLE),run_time=1)
        self.note('중첩 = 기저 상태 + 각각의 확률 진폭')

    def s03(self):
        f=label('|ψ⟩ = α |0⟩ + β |1⟩',y=2.3,size=40,color=PURPLE);self.show(f)
        rows=VGroup(label('|0⟩     α     →     |α|²',y=.8,size=34),label('|1⟩     β     →     |β|²',y=-.1,size=34))
        self.show(rows);self.note('|α|² + |β|² = 1')
        self.to(21)
        eq=label('α = β = 1/√2',y=-1.8,size=32,color=PURPLE);self.show(eq)
        self.show(label('50%                 50%',y=-2.7,size=28,color=GREEN))

    def s04(self):
        g=grid(2,2,1.7);self.show(g)
        count=label('1 큐비트  →  2개',y=3.2,size=31,color=PURPLE);self.show(count)
        for t,n in [(27,4),(29,8)]:
            self.to(t);self.play(Transform(g,grid(n,4,1.35)),run_time=.65)
            self.replace(count,f'{int(np.log2(n))} 큐비트  →  {n}개',PURPLE,31)
        self.to(33);self.play(Transform(g,grid(64,8,L.dense_grid_size,False)),run_time=.8)
        self.replace(count,'10 큐비트  →  1,024개',PURPLE,31)
        self.to(36.5);self.replace(count,'20 큐비트  →  1,048,576개',PURPLE,30)
        self.note('n 큐비트  →  2ⁿ개 기저 상태의 진폭')

    def s05(self):
        g=grid();self.show(g)
        q=label('모든 경우를 동시에 계산하면\n모든 답을 얻을까?',y=3.4,size=31);self.show(q)
        self.to(46);self.show(label('그렇지 않습니다',y=-2.8 if PORTRAIT else -3.15,size=34,color=ORANGE))

    def s06(self):
        g=grid().move_to(p(0,.5));self.show(g)
        self.note('측정 전 · 16개 상태에 균등한 진폭',PURPLE)
        self.to(54)
        frame=SurroundingRectangle(g,color=INK,buff=.22);self.show(frame)
        self.to(55)
        self.play(*[g[i].animate.set_opacity(.08) for i in range(16) if i!=5],
                  g[5].animate.set_color(GREEN),run_time=.7)
        self.show(label('측정 결과의 예:  |0101⟩',y=-2.2 if PORTRAIT else -3.0,size=31,color=GREEN))
        self.to(58);self.show(label('한 번의 측정 → 하나의 비트열',y=3.6 if PORTRAIT else 3.9,size=30))
        self.note('반복 측정의 결과는 확률적으로 달라질 수 있음')

    def wave_panel(self,opposite=False):
        w=6.2 if PORTRAIT else 9
        a=wave(w,.4,2,BLUE).move_to(p(0,1.8))
        b=wave(w,.4,2,PURPLE,PI if opposite else 0).move_to(p(0,.2))
        c=wave(w,0 if opposite else .8,2,ORANGE if opposite else GREEN).move_to(p(0,-1.7))
        return a,b,c

    def s07(self):
        a,b,c=self.wave_panel();self.show(a,b)
        self.to(67);self.play(Create(c),run_time=1)
        self.note('파동 비유 · 같은 위치에서 값이 더해짐')
        self.show(label('A + A = 2A',y=3.5,size=35,color=GREEN))

    def s08(self):
        a,b,c=self.wave_panel();self.add(a,b,c)
        f=label('마루 + 마루  →  강화',y=3.5,size=33,color=GREEN);self.show(f)
        self.to(73)
        aa,bb,cc=self.wave_panel(True)
        self.play(Transform(b,bb),Transform(c,cc),run_time=1.2)
        self.replace(f,'마루 + 골  →  상쇄',ORANGE,33)
        self.to(76);self.note('양자컴퓨터에서는 확률 진폭이 간섭합니다',PURPLE)

    def s09(self):
        nodes=VGroup(tile('|0⟩',BLUE),tile('|1⟩',BLUE)).arrange(DOWN,buff=2 if PORTRAIT else 1.3).move_to(p(-2.5,0))
        out=tile('|0⟩',GREEN).move_to(p(2.4,0));self.show(nodes,out)
        paths=VGroup(*[Arrow(n.get_right(),out.get_left(),buff=.15,color=c,stroke_width=3) for n,c in zip(nodes,[BLUE,PURPLE])])
        self.play(LaggedStart(*[Create(a) for a in paths],lag_ratio=.3),run_time=1.2)
        self.show(label('a₁',0,1.15,31,BLUE),label('a₂',0,-1.15,31,PURPLE))
        self.to(86);self.show(label('a₁ + a₂',y=3.2,size=43,color=GREEN))
        self.show(label('실수:  +, −     복소수:  위상',y=-2.5 if PORTRAIT else -2.9,size=27,color=PURPLE))
        self.note('경로 = 상태 전이에 기여하는 수학적 항')

    def s10(self):
        top=label('강화     0.5 + 0.5 = 1',y=2,size=34,color=GREEN)
        bottom=label('상쇄     0.5 − 0.5 = 0',y=-.3,size=34,color=ORANGE)
        self.show(top,bottom)
        self.to(97)
        self.show(label('P(x) = |a₁ + a₂|²',y=-2.2,size=40,color=PURPLE))
        self.note('하나의 출력에 기여하는 경로의 예 · 전체 상태가 아님')

    def s11(self):
        f=label('P(x) = |αₓ|²',size=65,color=PURPLE);self.show(f,run_time=.35)
        self.play(Indicate(f,color=GREEN,scale_factor=1.06),run_time=.65)

    def s12(self):
        states=grover_states(4,3,1)
        chart=self.bars(states[0]);self.show(chart)
        stage=label('균등 중첩',y=3.5,size=30,color=PURPLE);self.show(stage)
        self.to(108)
        # Discrete unitary snapshots: no linear morph through unnormalized amplitudes.
        self.remove(chart);chart=self.bars(states[1]);self.add(chart)
        self.play(Indicate(chart[-3],color=ORANGE,scale_factor=1.04),run_time=.8)
        self.replace(stage,'오라클: 정답의 위상 반전',ORANGE,30)
        self.note('진폭의 부호 변화 · 확률은 아직 각각 25%')
        self.to(111.8)
        self.remove(chart);chart=self.bars(states[2]);self.add(chart)
        self.play(Indicate(chart[-3],color=GREEN,scale_factor=1.04),run_time=1)
        self.replace(stage,'확산: 평균에 대한 반사',GREEN,30)
        self.note('연산 후 진폭 · |11⟩의 관측 확률 100%',GREEN)

    def s13(self):
        initial=np.ones(4)/4
        chart=self.bars(initial,True);self.show(chart)
        self.show(label('4개 중 하나를 찾는 예',y=3.5,size=29,color=MUTED))
        self.to(117);self.play(Transform(chart,self.bars(np.array([0,0,0,1]),True)),run_time=1.2)
        self.to(119);self.note('정답 확률 100% · 모든 결과의 확률 합 = 100%',GREEN)

    def s14(self):
        g=grid(64,8,L.dense_grid_size,False);self.show(g)
        self.to(126);self.show(label('정렬되지 않은 N개 항목',y=3.7,size=32))
        self.play(Circumscribe(g[-1],color=GREEN),run_time=.8)
        self.note('정답 하나 · 조건을 판별하는 오라클에 조회')

    def s15(self):
        centers=[p(0,1.7),p(0,-1.8)] if PORTRAIT else [p(-3.8,0),p(3.8,0)]
        grids=[]
        for center,title,color in zip(centers,['고전 검색 · 하나씩 확인','그로버 · 진폭 증폭'],[BLUE,PURPLE]):
            g=grid(64,8,.34,False).move_to(center);grids.append(g)
            self.show(g,text(title,size=24,color=color,width=7).next_to(g,UP,buff=.25))
        for i in range(16):
            self.play(grids[0][i][0].animate.set_fill(BLUE,.6),run_time=.10)
        self.to(136)
        states=grover_states(64,63,6)
        for k in range(1,7):
            self.play(*self.mark_grid(grids[1],states[2*k]**2),run_time=.55)
        self.note('오라클 위상 반전 + 확산을 6회 반복 · N = 64')

    def s16(self):
        self.show(label('1,000,000',y=3.1,size=62,color=INK))
        self.show(label('개 항목 중 정답 하나',y=2.1,size=29,color=MUTED))
        self.show(label('고전 검색',-1.95,.7,27,BLUE,width=3.5),label('그로버 검색',1.95,.7,27,PURPLE,width=3.5))
        self.show(label('10⁶',-1.95,-.3,55,BLUE,width=3.5),label('10³',1.95,-.3,55,GREEN,width=3.5))
        self.show(label('O(N)',-1.95,-1.5,35,BLUE,width=3.5),label('O(√N)',1.95,-1.5,35,GREEN,width=3.5))
        self.note('조회 횟수의 규모 비교 · 실제 실행시간과 구별')
        self.to(153);self.show(label('이상적 반복 수 ≈ (π/4)√N',y=-2.6,size=27,color=MUTED))

    def s17(self):
        f=label('중첩 ≠ 속도 향상',y=2.6,size=43,color=ORANGE);self.show(f)
        self.to(160)
        arrow='↓' if PORTRAIT else '→'
        chain=VGroup(*[label(s,size=31 if PORTRAIT else 26,color=c) for s,c in [('중첩',PURPLE),(arrow,MUTED),('양자 연산 · 상대 위상 조절',PURPLE),(arrow,MUTED),('간섭 · 정답 확률 강화',GREEN)]])
        chain.arrange(DOWN if PORTRAIT else RIGHT,buff=.28 if PORTRAIT else .4).move_to(p(0,-.3));self.show(chain)
        self.to(163);self.note('어떤 결과를 강화할 수 있는가?',GREEN)

    def s18(self):
        # Both endings preserve the complete narration and duration. No end card or episode preview.
        dots=VGroup(*[Dot(p(np.cos(t)*2.5,np.sin(t)*1.5),radius=.065,color=PURPLE) for t in np.linspace(0,TAU,12,endpoint=False)])
        self.show(dots)
        self.to(171)
        q=label('양자컴퓨터는\n모든 문제에서 빠를까?',y=.3,size=40,color=INK)
        self.play(dots.animate.set_opacity(.15),FadeIn(q),run_time=.8)
        self.to(173)
        self.show(label('속도를 결정하는 것은\n문제의 어떤 성질일까?',y=-2.7,size=27,color=PURPLE))

