"""Stable SM relationships; illustrative issue order, not a measured GPU trace."""
import json
from pathlib import Path
from manim import *
from shared_style import StyleScene,text,box,stack,SHORT,INK,MUTED,BLUE,GREEN,ORANGE,PURPLE,PANEL
P=Path(__file__).resolve().parent
CODE=['float x = A[i];','float y = x * 2.0f;','B[i] = y;']
LAUNCH=['int blockSize = 128;','int gridSize =','  (N + blockSize - 1) / blockSize;','compute<<<gridSize, blockSize>>>(', '  d_A, d_B, N);']
class SMBase(StyleScene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start'];self.bounds=[];self.trace=[]
        self.dc=np.array([0,1.18,0]) if SHORT else np.array([-3.65,-1.05,0]);self.dw=7.65 if SHORT else 7.1;self.dh=3.4 if SHORT else 2.65
        self.cc=np.array([0,-2.85,0]) if SHORT else np.array([4.15,.1,0]);self.cw=7.65 if SHORT else 6.15;self.ch=4.05 if SHORT else 4.7
        self.add(text('GPU HIERARCHY  /  LEVEL 04',19,MUTED).move_to([0,7.35 if SHORT else 4,0]),text(self.meta['title'],33,width=8 if SHORT else 14).move_to([0,6.45 if SHORT else 3.2,0]))
        self.world_map();self.board();self.code([0]);self.note('SM 내부 구조 · 개념도')
        self.shot();self.to(self.meta['end'])
        suffix='shorts' if SHORT else 'longform'
        for name,data in [('geometry',self.bounds),('states',self.trace)]:
            (P/f'{name}_{suffix}_{self.INDEX:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    def record(self,m):
        self.bounds.append(dict(time=self.start+self.time,left=float(m.get_left()[0]),right=float(m.get_right()[0]),bottom=float(m.get_bottom()[1]),top=float(m.get_top()[1])))
    def world_map(self):
        center=np.array([0,4.55,0]) if SHORT else np.array([-3.65,1.6,0]);scale=1 if SHORT else .86
        gpu=RoundedRectangle(width=7.65,height=2.1,corner_radius=.15,stroke_color=BLUE,stroke_width=1.6,fill_color=PANEL,fill_opacity=.5)
        self.sm_outline=RoundedRectangle(width=7.08,height=1.4,corner_radius=.1,stroke_color=BLUE,stroke_width=3).shift(DOWN*.15)
        g=VGroup(gpu,self.sm_outline,text('GPU',19,BLUE).move_to([-3.2,.82,0]),text('SM 0',20,BLUE).move_to([-2.98,.28,0]),text('실행 배치 개념도',16,MUTED).move_to([2.42,.82,0]))
        self.mini_warps=VGroup();self.blocks=[]
        for b,x in [(0,-1.68),(1,1.72)]:
            border=DashedVMobject(RoundedRectangle(width=3.1,height=.78,corner_radius=.07),num_dashes=25).set_color(MUTED).move_to([x,-.2,0])
            label=text(f'Block {b} · 128 Thread',15,MUTED).move_to([x,.02,0])
            ws=VGroup(*(box(f'W{w+b*4}',.58,.28,BLUE if w==0 else MUTED,12).move_to([x+(w-1.5)*.66,-.28,0]) for w in range(4)))
            bg=VGroup(border,label,ws);self.blocks.append(bg);g.add(bg)
            if b==0:self.mini_warps=ws
        g.scale(scale).move_to(center)
        if self.start<38:self.blocks[1].save_state();self.blocks[1].set_opacity(.16)
        self.map_group=g;self.add(g);self.record(g)
        self.hud_label=text('Block 0 → SM 0 → Warp 0–3',17,MUTED,width=7).move_to([center[0],3.29 if SHORT else .51,0]);self.add(self.hud_label)
    def hud(self,s,col=MUTED):self.hud_label.become(text(s,17,col,width=7).move_to(self.hud_label))
    def code(self,active=(),lines=None,label='compute.cu  ·  발췌'):
        lines=CODE if lines is None else lines;self.active_code=[lines[n] for n in active];super().code(active,lines,label)
    def board(self):
        outer=RoundedRectangle(width=7.4,height=3.35,corner_radius=.13,stroke_color=BLUE,stroke_width=2,fill_color=PANEL,fill_opacity=.5)
        self.scheduler=box('Warp Scheduler',2.8,.5,BLUE,23).move_to([-1.87,1.18,0])
        self.units=box('Execution Units',2.8,.5,GREEN,23).move_to([1.87,1.18,0])
        arrow=Arrow(self.scheduler.get_right(),self.units.get_left(),buff=.08,color=GREEN,stroke_width=2)
        self.warp_rows=VGroup();self.status=[];self.lanes=VGroup()
        for w in range(4):
            y=.55-w*.42
            name=text(f'Warp {w}',20,BLUE if w==0 else MUTED).move_to([-2.93,y,0])
            cells=VGroup(*(Rectangle(width=.064,height=.16,stroke_width=.45,color=BLUE if w==0 else MUTED,fill_opacity=.14,fill_color=BLUE).move_to([-2.15+k*.075,y,0]) for k in range(32)))
            state=box('Ready',2.3,.31,BLUE if w==0 else MUTED,17).move_to([1.9,y,0])
            self.status.append(state);self.lanes.add(cells);self.warp_rows.add(VGroup(name,cells,state))
        reg=box('Register File · 상주 상태 유지',3.3,.37,PURPLE,17).move_to([-1.8,-1.18,0])
        shared=box('Shared Memory / L1',3.1,.37,PURPLE,17).move_to([1.78,-1.18,0])
        self.register=reg;self.shared=shared
        foot=text('SM 0 확대 · 스케줄러 수와 자원 배치는 단순화',14,MUTED).move_to([0,-1.5,0])
        g=VGroup(outer,self.scheduler,self.units,arrow,self.warp_rows,reg,shared,foot)
        self.place(g,self.dc,self.dw,self.dh);self.bg=g;self.add(g)
        self.trace.append(dict(kind='layout',time=self.start,warp_centers=[r.get_center().tolist() for r in self.warp_rows],resident_warps=[0,1,2,3]))
        self.warp_states=['Ready']*4
    def state(self,w,s,col):
        self.status[w].become(box(s,self.status[w].width,self.status[w].height,col,17).move_to(self.status[w]))
        self.lanes[w].set_fill(col,opacity=.48 if col==GREEN else .22).set_stroke(col)
        self.mini_warps[w].set_color(col);self.warp_states[w]=s
        self.trace.append(dict(kind='warp_state',time=round(self.start+self.time,4),warp=w,state=s,resident=True,center=self.warp_rows[w].get_center().tolist(),active_code=self.active_code.copy()))
    def issue(self,w,op='Compute'):
        self.code([0 if op=='Load' else 1 if op=='Compute' else 2]);self.state(w,'Issue '+op,GREEN)
        self.hud(f'Warp {w} → Scheduler → 명령 발행',GREEN)
        packet=Dot(self.scheduler.get_center(),radius=.06,color=GREEN);self.add(packet)
        self.play(packet.animate.move_to(self.units.get_center()),Indicate(self.status[w],color=GREEN,scale_factor=1.02),run_time=.55);self.remove(packet)
        self.trace.append(dict(kind='issue',time=round(self.start+self.time,4),warp=w,operation=op,resident_warps=[0,1,2,3],states=self.warp_states.copy(),illustrative=True))
    def detail(self,g):
        self.remove(self.bg)
        if hasattr(self,'dg'):self.remove(self.dg)
        self.place(g,self.dc,self.dw,self.dh);self.dg=g;self.add(g);return g
    def timeline(self):
        rows=VGroup()
        for w in range(3):
            label=text(f'Warp {w}',20,BLUE if w==0 else MUTED).move_to([-3,.6-w*.65,0]);r=VGroup(label)
            if w==0:
                for x,width,s,col in [(-1.7,.8,'LD',GREEN),(-.05,2.4,'데이터 대기',ORANGE),(1.85,1,'MUL',GREEN)]:r.add(box(s,width,.4,col,17).move_to([x,.6,0]))
            else:r.add(box('명령 발행',1.25,.4,GREEN,17).move_to([-.9+(w-1)*1.45,.6-w*.65,0]))
            rows.add(r)
        rows.add(text('Warp 0 대기와 Warp 1·2 발행이 겹친다',22,GREEN).move_to([0,1.25,0]),text('Latency Hiding · 시간 간격은 설명용',18,MUTED).move_to([0,-1.35,0]))
        return rows
    def resources(self,heavy=False):
        columns=VGroup()
        for j,(label,n,col) in enumerate([('Block별 자원 적음',4,GREEN),('Block별 자원 많음',1,ORANGE)]):
            cells=VGroup(*(box(f'Block {k}',2.45,.37,col,18).move_to([0,.66-k*.48,0]) for k in range(n)))
            g=VGroup(text(label,22,col).move_to([0,1.32,0]),cells,text(f'{n} Blocks 상주',21,col).move_to([0,-1.32,0]))
            if n==1:g.add(text('Register / Shared 점유',17,PURPLE).move_to([0,.1,0]),text('추가 Block은 대기',18,MUTED).move_to([0,-.6,0]))
            columns.add(g)
        columns.arrange(RIGHT,buff=.6)
        title=text('SM 0 · 제한된 자원을 나누어 사용',21,BLUE).next_to(columns,UP,buff=.2)
        return VGroup(columns,title)
    def occupancy(self,full=False):
        slots=VGroup(*(box(f'{k}',.64,.35,GREEN if k<(32 if full else 16) else MUTED,14,fill=.4 if k<(32 if full else 16) else .04) for k in range(32))).arrange_in_grid(rows=4,cols=8,buff=.1)
        return stack(text('가상 SM 0 · 최대 상주 32 Warp',23,BLUE),slots,text(f'{32 if full else 16} / 32 = {100 if full else 50}%',36,GREEN),text('설명용 수치 · 실제 GPU 사양 아님',18,MUTED),buff=.17)
    def shot(self):
        i=self.INDEX
        if i==0:
            self.code(lines=['Thread → Warp → Block','Block → SM'],label='논리 구조와 실제 실행 공간');self.sm_outline.set_stroke(opacity=.2);self.bg.save_state();self.bg.set_opacity(.2)
            self.to(5);self.play(self.sm_outline.animate.set_stroke(opacity=1),Restore(self.bg),run_time=1.2)
            self.to(10);self.hud('Streaming Multiprocessor',BLUE);self.pulse(self.sm_outline);self.to(13);self.note('SM · 명령을 실제로 실행하는 하드웨어',BLUE)
        elif i==1:
            self.code(lines=['Warp Scheduler','Execution Units','Register File','Shared Memory / L1'],label='SM 내부 자원');self.note('자원 개수·물리적 배치는 아키텍처마다 다르다')
            self.to(21)
            for t,m in [(21,self.units),(23,self.register),(25,self.shared),(27,self.scheduler)]:self.to(t);self.pulse(m)
        elif i==2:
            self.code(lines=['Block 0 → SM 0','Warp 0, 1, 2, 3','Registers + Shared Memory'],label='Block 하나는 SM 하나에서 실행');self.note('같은 Block의 Warp는 해당 SM의 자원을 사용')
            self.to(33);self.pulse(self.warp_rows);self.to(38);self.play(Restore(self.blocks[1]),run_time=.7);self.hud('자원이 허용하면 여러 Block이 상주',GREEN);self.note('상주 Block 수는 자원과 하드웨어 한계에 따른다')
        elif i==3:
            self.note('Ready: 다음 명령을 발행할 조건이 준비됨');self.to(45);self.pulse(self.scheduler);self.to(48);self.issue(1);self.to(50);self.state(1,'Ready',MUTED);self.issue(2)
        elif i==4:
            self.code([0,1,2]);self.note('Load → Compute → Store');self.to(55);self.pulse(self.cg);self.to(60);self.issue(0,'Load');self.to(63);self.code([1]);self.state(0,'x 필요',BLUE);self.note('곱셈은 Load가 가져온 x에 의존한다',ORANGE)
        elif i==5:
            self.issue(0,'Load');self.note('메모리 지연이 발생한 상황을 가정 · 실측 trace 아님');self.to(70);self.code([1]);self.state(0,'Wait: x',ORANGE);self.hud('x 미도착 → 의존 명령 발행 불가',ORANGE)
            self.to(74);self.pulse(self.scheduler);self.note('Warp 0이 기다려도 다른 Warp는 Ready',GREEN)
        elif i==6:
            self.code([1]);self.state(0,'Wait: x',ORANGE);self.note('Warp 0은 SM 안에 그대로 상주',ORANGE);self.pulse(self.register);self.hud('실행 상태 유지 · 저장/복원 이동 없음')
        elif i==7:
            self.code([1]);self.state(0,'Wait: x',ORANGE);self.note('대기 Warp와 Ready Warp가 같은 SM에 상주')
            self.pulse(self.status[1]);self.to(86);self.issue(1);self.to(88);self.state(1,'Ready',MUTED);self.issue(2)
            self.to(90);self.state(2,'Ready',MUTED);self.state(0,'Ready: x 도착',BLUE);self.hud('데이터 도착 → Warp 0 의존성 해소',BLUE)
            self.to(92);self.issue(0);self.note('발행과 연산 완료는 서로 다른 시점',MUTED)
        elif i==8:
            self.state(0,'Ready',BLUE);self.detail(self.timeline());self.code([0,1]);self.hud('Latency Hiding · 방금 일어난 명령 발행 정리',GREEN);self.note('지연을 없애는 대신 다른 작업을 겹친다',GREEN);self.pulse(self.dg)
        elif i==9:
            self.code(lines=['// Resident blocks share','// limited SM resources','Registers','Shared Memory'],label='상주 수를 제한하는 자원');self.note('Warp 수가 많으면 항상 빠를까?');self.to(107);self.hud('항상 그렇지는 않다',ORANGE)
            self.to(108);self.pulse(self.register);self.pulse(self.shared);self.to(113);self.detail(self.resources());self.note('개념 예시 · Thread 수와 하드웨어 한계도 영향')
        elif i==10:
            self.detail(self.occupancy());self.code(lines=['Occupancy =','  resident warps','  / max resident warps','16 / 32 = 50%'],label='상주 Warp 비율');self.hud('Ready 여부와 상주 여부는 다른 개념');self.note('대기 중인 Warp도 상주 Warp에 포함',ORANGE);self.to(122);self.pulse(self.dg)
        elif i==11:
            self.detail(self.occupancy());self.code(lines=['50% → 100% occupancy','Performance × 2 ?','Not guaranteed'],label='상주 수와 성능은 같은 지표가 아니다');self.note('높은 Occupancy ≠ 반드시 높은 성능',ORANGE)
            self.to(134);old=self.dg;self.remove(old);self.detail(self.occupancy(True));self.hud('이미 지연을 충분히 숨겼다면 개선이 없을 수도 있다');self.pulse(self.dg)
        elif i==12:
            self.code([0,1,2,3],LAUNCH);self.note('gridSize: Block 수 · blockSize: Block당 Thread 수');self.to(142);self.pulse(self.cg)
            self.to(149)
            cards=VGroup(*(box(f'SM {k}\nBlock {b}',2.6,1.1,BLUE if k==0 else MUTED,23) for k,b in [(0,2),(1,0),(2,3),(3,1)])).arrange_in_grid(rows=2,cols=2,buff=.25)
            self.detail(stack(text('배치 예시 · 순서/SM 번호 보장 없음',21,ORANGE),cards,buff=.2));self.hud('Block 번호 ≠ SM 번호',ORANGE);self.note('일반적인 launch 설정에는 SM 지정 인자가 없다')
        elif i==13:
            self.code(lines=['Thread: execution context','Warp: instruction issue','Block: cooperation group'],label='논리 구조와 명령 실행 단위');self.note('Thread · Warp · Block의 역할 구분');self.pulse(self.lanes[0][0]);self.to(157);self.pulse(self.warp_rows[0]);self.to(160);self.pulse(self.blocks[0])
        elif i==14:
            self.hud('SM · 물리적 실행 하드웨어',BLUE);self.note('상주한 Warp의 명령을 실행 자원에 발행');self.pulse(self.sm_outline);self.to(164);self.issue(1);self.to(167);self.state(1,'Ready',MUTED);self.issue(2)
        elif i==15:
            self.state(0,'Wait: x',ORANGE);self.note('SM — Scheduling · Execution · Latency Hiding',GREEN);self.hud('여러 Warp를 활용해 계산과 대기를 겹친다',GREEN)
            self.issue(1);self.to(172);self.state(1,'Ready',MUTED);self.issue(2);self.to(174);self.state(2,'Ready',MUTED);self.state(0,'Ready: x 도착',BLUE);self.to(175);self.issue(0);self.to(177);self.hud('SM · GPU 처리량을 만드는 실행 구조',BLUE)
