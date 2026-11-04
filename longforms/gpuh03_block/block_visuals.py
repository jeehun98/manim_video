"""One Block, four persistent Warps and a single block-owned shared array."""
import json
from pathlib import Path
from manim import *
from shared_style import StyleScene,text,box,stack,SHORT,INK,MUTED,BLUE,GREEN,ORANGE,PURPLE,PANEL,COLS
from reduction_model import STAGES
P=Path(__file__).resolve().parent
WC=[GREEN,BLUE,ORANGE,PURPLE]
LOAD=['__shared__ float s[128];','int t = threadIdx.x;','s[t] = input[t];','__syncthreads();']
REDUCE=['for (int stride = 64;','     stride > 0; stride >>= 1) {','  if (t < stride)','    s[t] += s[t + stride];','  __syncthreads();','}']
class BlockBase(StyleScene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start']
        self.dc=np.array([0,1.5,0]) if SHORT else np.array([-3.65,-1.05,0]);self.dw=7.65 if SHORT else 7.1;self.dh=2.7 if SHORT else 2.15
        self.cc=np.array([0,-2.7,0]) if SHORT else np.array([4.15,.15,0]);self.cw=7.65 if SHORT else 6.15;self.ch=4.35 if SHORT else 4.7
        self.bounds=[];self.trace=[];self.active_code=[];self.board_group=None
        self.add(text('GPU HIERARCHY  /  LEVEL 03',19,MUTED).move_to([0,7.35 if SHORT else 4.,0]),text(self.meta['title'],34,width=8 if SHORT else 14).move_to([0,6.45 if SHORT else 3.2,0]))
        self.add(Line([-3.9,5.85,0],[3.9,5.85,0],color=MUTED,stroke_opacity=.25) if SHORT else Line([-7.3,2.7,0],[7.3,2.7,0],color=MUTED,stroke_opacity=.25))
        self.world_map()
        if self.INDEX>0:self.board()
        self.shot();self.to(self.meta['end'])
        layout='shorts' if SHORT else 'longform'
        for name,data in [('geometry',self.bounds),('states',self.trace)]:
            (P/f'{name}_{layout}_{self.INDEX:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    def record(self,m):self.bounds.append(dict(time=self.start+self.time,left=float(m.get_left()[0]),right=float(m.get_right()[0]),bottom=float(m.get_bottom()[1]),top=float(m.get_top()[1])))
    def world_map(self):
        center=np.array([0,4.5,0]) if SHORT else np.array([-3.65,1.48,0]);scale=1 if SHORT else .86
        gpu=RoundedRectangle(width=7.65,height=2.5,corner_radius=.15,stroke_color=BLUE,stroke_width=1.8,fill_color=PANEL,fill_opacity=.45)
        sm=RoundedRectangle(width=7.1,height=1.68,corner_radius=.1,stroke_color='#7086A3',stroke_width=1.5).shift(DOWN*.18)
        nodes=VGroup(gpu,sm,text('GPU',19,BLUE).move_to([-3.2,1.02,0]),text('SM 0',20,INK).move_to([-2.95,.48,0]),text('실행 배치 개념도',16,MUTED).move_to([2.5,1.02,0]))
        self.mini_cells=VGroup();self.mini_blocks=[]
        for b,x in [(0,-1.78),(1,1.78)]:
            border=DashedVMobject(RoundedRectangle(width=3.16,height=.75,corner_radius=.08),num_dashes=30).set_color(MUTED).move_to([x,-.15,0])
            label=text(f'Block {b} · 4 Warp' if b==0 or self.INDEX==17 else '다른 Block',16,MUTED).move_to([x,.08,0])
            cells=VGroup(*(Rectangle(width=.042,height=.05,stroke_width=.4,color=WC[k//32],fill_color=WC[k//32],fill_opacity=.35) for k in range(128))).arrange_in_grid(rows=4,cols=32,buff=(.009,.017)).move_to([x,-.23,0])
            shared=Rectangle(width=2.4,height=.07,stroke_width=1,color=PURPLE,fill_color=PURPLE,fill_opacity=.18).move_to([x,-.43,0])
            group=VGroup(border,label,cells,shared)
            if b==0:self.mini_cells=cells;self.mini_shared=shared;self.mini_border=border
            elif self.INDEX!=17:group.set_opacity(.18)
            self.mini_blocks.append(group);nodes.add(group)
        nodes.add(box('Register File',5.95,.38,PURPLE,17,fill=.07).move_to([0,-.73,0]))
        nodes.scale(scale).move_to(center);self.map_group=nodes;self.add(nodes);self.record(nodes)
        self.map_caption=text('Block 0 · 128 Thread · 4 Warp',17,MUTED,width=7).move_to([center[0],3.12 if SHORT else .22,0]);self.add(self.map_caption)
    def hud(self,s,col=MUTED):self.map_caption.become(text(s,17,col,width=7).move_to(self.map_caption))
    def code(self,active=(),lines=None,label='blockSum.cu  ·  발췌'):
        lines=LOAD if lines is None else lines;self.active_code=[lines[n].strip() for n in active];super().code(active,lines,label)
    def board(self):
        outer=DashedVMobject(RoundedRectangle(width=7.4,height=2.65,corner_radius=.13),num_dashes=65).set_color(MUTED)
        heading=text('Block 0  ·  128 Thread = 4 × 32',22,INK).move_to([0,1.1,0])
        self.thread_cells=VGroup();self.warp_labels=VGroup();rows=VGroup()
        for w in range(4):
            y=.72-w*.40
            label=text(f'W{w}  {w*32}–{w*32+31}',16,WC[w],width=1.35).move_to([-2.9,y,0]);self.warp_labels.add(label)
            cells=VGroup(*(Rectangle(width=.13,height=.23,stroke_width=.65,color=WC[w],fill_color=WC[w],fill_opacity=.16).move_to([-1.7+k*.158,y,0]) for k in range(32)))
            self.thread_cells.add(*cells);rows.add(label,cells)
        self.memory_title=text('Shared Memory · s[0…127] · Block 0 할당',16,PURPLE).move_to([0,-.77,0])
        self.memory=VGroup(*(Rectangle(width=.040,height=.23,stroke_width=.35,color=WC[k//32],fill_color=WC[k//32],fill_opacity=.04).move_to([(k-63.5)*.046,-1.08,0]) for k in range(128)))
        mem_border=SurroundingRectangle(self.memory,buff=.045,color=PURPLE,stroke_width=1.5)
        self.barrier_line=Line([3.45,-.64,0],[3.45,.94,0],color=ORANGE,stroke_width=3).set_stroke(opacity=0)
        g=VGroup(outer,heading,rows,self.memory_title,mem_border,self.memory,self.barrier_line)
        g.scale(min(self.dw/g.width,self.dh/g.height,1)).move_to(self.dc)
        self.board_group=g;self.board_outline=outer;self.add(g);self.record(g)
        self.trace.append(dict(kind='layout',time=round(self.start+self.time,4),total_threads=128,thread_centers=[c.get_center().tolist() for c in self.thread_cells],shared_centers=[c.get_center().tolist() for c in self.memory]))
    def memory_state(self,ready,animate=False):
        ready=set(ready);changes=[]
        for k,m in enumerate(self.memory):
            if animate:changes.append(m.animate.set_fill(WC[k//32],opacity=.75 if k in ready else .035))
            else:m.set_fill(WC[k//32],opacity=.75 if k in ready else .035)
        self.mini_shared.set_fill(PURPLE,opacity=.5 if len(ready)==128 else .15)
        if changes:self.play(*changes,run_time=.32)
    def participants(self,n):
        for k,c in enumerate(self.thread_cells):c.set_fill(WC[k//32],opacity=.55 if k<n else .045).set_stroke(opacity=1 if k<n else .3)
        for k,c in enumerate(self.mini_cells):c.set_fill(WC[k//32],opacity=.65 if k<n else .08)
    def barrier(self,arrivals,animate=False):
        self.barrier_line.set_stroke(opacity=1,color=GREEN if len(arrivals)==4 else ORANGE)
        for w,label in enumerate(self.warp_labels):label.set_opacity(1 if w in arrivals else .35)
        self.memory_state([k for w in arrivals for k in range(w*32,w*32+32)],animate)
        self.hud(f'장벽 도착 {len(arrivals)}/4 Warp · 전체 128 Thread',GREEN if len(arrivals)==4 else ORANGE)
        self.trace.append(dict(kind='barrier',time=round(self.start+self.time,4),arrived_warps=arrivals.copy(),total_threads=128,participants=128,scope='Block 0',active_code=self.active_code.copy()))
    def step(self,stride,animate=True,kind='reduction'):
        stage=next(s for s in STAGES if s['stride']==stride)
        self.code([3],REDUCE,f'blockSum.cu · stride = {stride}');add_code=self.active_code.copy()
        self.participants(stride);self.memory_state(range(stride),animate)
        self.hud(f'부분 합계 {stride}개 · 전체 Thread는 128개',GREEN)
        self.note(f's[0] = {stage["values"][0]}   ·   덧셈 참여 {stride} / 장벽 참여 128')
        self.code([4],REDUCE,f'blockSum.cu · stride = {stride}')
        self.participants(128)
        self.barrier_line.set_stroke(opacity=1,color=GREEN)
        if animate:self.play(Indicate(self.barrier_line,color=GREEN,scale_factor=1),run_time=.20)
        self.barrier_line.set_stroke(opacity=0)
        self.participants(stride)
        self.trace.append(dict(kind=kind,time=round(self.start+self.time,4),stride=stride,count=stride,total_threads=128,add_participants=stride,barrier_participants=128,values=stage['values'],add_code=add_code,barrier_code=self.active_code.copy()))
    def detail(self,g):
        self.place(g,self.dc,self.dw,self.dh)
        if self.board_group is not None:self.remove(self.board_group)
        if hasattr(self,'detail_group'):self.remove(self.detail_group)
        self.detail_group=g;self.add(g);return g
    def pair_example(self):
        self.note('s[0] = 1  ← Thread 0    /    s[64] = 65  ← Thread 64',ORANGE)
        self.play(Indicate(self.memory[0],color=GREEN,scale_factor=1.15),Indicate(self.memory[64],color=ORANGE,scale_factor=1.15),Indicate(self.thread_cells[0],color=GREEN,scale_factor=1.1),Indicate(self.thread_cells[64],color=ORANGE,scale_factor=1.1),run_time=.5)
    def gpu_view(self):
        cards=VGroup()
        for k in range(4):
            inner=stack(text(f'SM {k}',24,INK),box('Block 0 · W0–W3' if k==0 else '가용 실행 자원',2.9,.55,GREEN if k==0 else MUTED,18),text('Shared · Register',15,PURPLE),buff=.15)
            border=SurroundingRectangle(inner,buff=.12,color=GREEN if k==0 else MUTED,corner_radius=.1)
            cards.add(VGroup(border,inner))
        cards.arrange_in_grid(rows=2,cols=2,buff=.23)
        return cards
    def shot(self):
        i=self.INDEX
        if i==0:
            old=VGroup(*(box(str(k),.67,.44,COLS[k%4],21).move_to([(k%8-3.5)*.82,.65-k//8*.53,0]) for k in range(32)))
            old.add(text('Warp 0 · 32 Thread',22,GREEN).move_to([0,1.1,0]));self.place(old,self.dc,self.dw,self.dh);self.add(old)
            self.code(lines=['Warp 0','32 Threads','Instruction + Active Mask'],label='같은 Warp 0에서 시작');self.note('다른 Warp의 Thread와 협력하려면?')
            self.to(5);self.board();self.remove(self.board_group);self.play(FadeOut(old),TransformFromCopy(self.mini_blocks[0],self.board_group),run_time=1.2)
            self.to(10);self.code(lines=['Block 0','Warp 0 + 1 + 2 + 3','One logical thread group'],label='Block · 논리적인 실행 그룹');self.pulse(self.board_outline)
        elif i==1:
            self.code(lines=['blockSum<<<1, 128>>>(', '  d_input, d_output);'],active=[0],label='한 Block · 128 Thread');self.note('이 교육용 kernel의 실행 조건: 정확히 128 Thread')
            self.to(17);self.pulse(self.board_outline);self.to(19);self.participants(128);self.hud('Block 0 · 128 Thread',GREEN)
        elif i==2:
            self.participants(128);self.code(lines=['4 Warps × 32 Threads','128 Threads'],label='현재 Block 설정');self.note('4 × 32 = 128',GREEN);self.to(28)
            self.code(lines=['// Other block configurations','<<<1, 64>>>   // 2 Warps','<<<1, 128>>>  // 4 Warps','<<<1, 256>>>  // 8 Warps'],active=[2],label='Block 크기 선택의 일반적 예시');self.note('뒤의 blockSum kernel은 128 Thread 고정 · 다른 크기 지원 아님')
        elif i==3:
            self.code(lines=['Block 0','Shared data','Synchronization'],label='협력 범위');self.note('한 Block의 Thread들이 하나의 결과를 만든다');self.to(38)
            self.memory_state(range(128),True);self.pulse(self.memory_title);self.note('한 공유 배열 · Block 내부 동기화',PURPLE)
        elif i==4:
            self.participants(128);self.code(lines=['input[t] = t + 1;','// input: 1 ... 128','// one final sum'],label='입력 128개 → 결과 하나');self.note('각 Thread가 입력 하나를 담당');self.to(48)
            self.memory_state(range(32),True);self.to(51);self.code(lines=['// 128 values','// output[0] = ?'],label='협력이 필요한 이유');self.note('각자 읽어온 값을 합쳐야 output[0] 하나가 된다',ORANGE)
        elif i==5:
            self.code([0],LOAD);self.memory_title.set_color(PURPLE);self.pulse(self.memory_title);self.note('한 Block의 네 Warp가 함께 사용하는 s[128]',PURPLE);self.to(60);self.pulse(self.cg)
        elif i==6:
            self.code([0],LOAD);self.note('Shared 배열은 Block에 귀속 · 물리 자원은 SM에 존재');self.to(67)
            self.code([1,2],LOAD)
            for w in range(4):
                self.memory_state(range((w+1)*32),True);self.play(Indicate(self.warp_labels[w],color=WC[w],scale_factor=1.02),run_time=.3)
            self.note('Thread 0 → s[0]=1   /   Thread 64 → s[64]=65',GREEN)
        elif i==7:
            self.memory_state(range(128));self.participants(128);self.code([2],LOAD);self.hud('s[128] · 128개 값의 공동 적재');self.note('s[0]=1   …   s[127]=128');self.pulse(self.memory_title)
        elif i==8:
            self.memory_state(range(64));self.code([2],LOAD);self.hud('동기화 전 가능한 진행 상태 · 설명용 예시',ORANGE);self.note('기록 완료와 기록 전인 Thread가 함께 있을 수 있음');self.to(79);self.pulse(self.warp_labels[2]);self.to(83)
            self.code(lines=['// Thread 0 needs s[64]','// s[64] not written yet','// barrier needed before read'],active=[1],label='다른 Thread의 기록을 읽기 전');self.note('아직 준비되지 않은 s[64]를 읽으면 올바른 합산 불가',ORANGE)
        elif i==9:
            self.code([0],['__syncthreads();'],'Block 내부 장벽 · 메모리 순서 보장');self.barrier([0]);self.note('도착 순서는 설명용 · 같은 하드웨어 사이클 맞춤이 아님');self.to(92)
            self.barrier([0,3],True);self.to(94);self.barrier([0,3,1],True);self.to(96);self.barrier([0,3,1,2],True);self.to(97)
            self.barrier_line.set_stroke(opacity=0);self.hud('모든 128 Thread 도착 · 이전 기록이 보이는 상태',GREEN);self.note('동기화 이전의 기록을 Block의 다른 Thread가 확인',GREEN);self.pulse(self.memory_title)
        elif i==10:
            self.memory_state(range(128));self.participants(128);self.code([0,1,2,3],LOAD);self.hud('초기 부분 합계 128개 · 전체 Thread 128개');self.note('입력 1…128 · 최종 합계는 8256');self.to(106);self.code([0],REDUCE)
        elif i==11:
            self.memory_state(range(128));self.pair_example();self.step(64);self.to(111)
            self.note('Thread 0: s[0] + s[64] = 1 + 65 = 66',GREEN);self.code([2,3],REDUCE,'stride 64 · Thread 0–63 합산');self.to(113);self.code([4],REDUCE,'stride 64 · 장벽에는 128개 모두 참여')
        elif i==12:
            for at,stride in [(115,32),(117,16),(119,8),(120,4),(121,2),(122,1)]:self.to(at);self.step(stride)
        elif i==13:
            self.memory_state([0]);self.participants(1);self.code([0,1],['if (t == 0) {','  output[0] = s[0];','}']);self.hud('s[0] = 8256 → output[0]',GREEN);self.note('Reduction · 128개 값에서 합계 하나로',GREEN);self.pulse(self.thread_cells[0])
            self.trace.append(dict(kind='output',time=self.start+self.time,thread=0,output=8256,source='s[0]'))
        elif i==14:
            self.memory_state(range(128));self.participants(128);self.code([2],LOAD);self.hud('네 Warp가 기록한 같은 s[128]');self.note('공유 배열의 32개씩 구간은 기록한 Warp의 색');self.to(131)
            self.pair_example();self.step(64,kind='cross_warp_example');self.code(lines=['// Written by Thread 0 and 64','s[0] = s[0] + s[64];','// 1 + 65 = 66'],active=[1],label='첫 합산 단계의 연결 관계');self.note('Warp 간 직접 전송이 아니라 같은 Shared 배열을 읽음',ORANGE)
        elif i==15:
            self.detail(self.gpu_view());self.code(lines=['GPU','  SM 0','    Block 0: Warp 0–3'],label='실행 배치 · 개념도');self.note('Block 전체는 어디에서 실행될까?');self.to(139)
            self.pulse(self.detail_group[0]);self.hud('Block 0의 모든 Warp → 같은 SM 0',GREEN);self.note('Block 하나의 Warp들을 여러 SM에 흩어 배치하지 않음')
        elif i==16:
            self.detail(self.gpu_view());self.code(lines=['SM 0','  Warp Scheduler','  Register File','  Shared Memory'],label='같은 SM의 실행 자원');self.note('Shared Memory의 Block별 할당 · 상주 수는 자원 제약에 따름');self.pulse(self.detail_group[0])
        elif i==17:
            cards=VGroup()
            for b in range(2):
                inside=stack(text(f'Block {b}',28,GREEN if b==0 else BLUE),text('Warp 0–3',22,MUTED),box(f'Shared: Block {b}',2.65,.5,PURPLE,18),buff=.25)
                edge=DashedVMobject(SurroundingRectangle(inside,buff=.18),num_dashes=35).set_color(GREEN if b==0 else BLUE);cards.add(VGroup(edge,inside))
            cards.arrange(RIGHT,buff=.5);self.detail(cards);self.code([0],['__syncthreads();'],'일반적 장벽의 범위 · 같은 Block');self.hud('Block 0의 장벽 ≠ Block 1의 장벽',ORANGE);self.note('설명용 배치 · 여러 Block의 동시 상주는 SM 자원에 따름');self.pulse(cards[0]);self.to(152)
            self.code(lines=['// Per-block allocation','__shared__ float s[128];'],active=[1],label='Block마다 별도 공유 배열');self.note('같은 SM이어도 다른 Block의 일반적 s 배열은 공유하지 않음')
        elif i==18:
            self.memory_state(range(128));self.code(lines=['Thread: own data + state','Warp: 32-thread execution','Block: share + synchronize'],label='같은 구조의 서로 다른 역할');self.note('선택 Thread 1 → Warp 0 → Block 0');self.pulse(self.thread_cells[1]);self.to(162)
            self.pulse(self.warp_labels[0]);self.to(166);self.pulse(self.board_outline)
        elif i==19:
            self.memory_state(range(128));self.code([0,2,3],LOAD);self.note('협력을 구성해 하나의 계산을 완성한다',GREEN)
            for at,stride in [(170,64),(171,32),(172,16),(173,8),(174,4),(175,2),(176,1)]:self.to(at);self.step(stride,kind='final_reduction')
            self.to(177);self.code([1],['if (t == 0) {','  output[0] = s[0];','}']);self.hud('Block 0 · 128 Thread · 최종 합계 8256',GREEN);self.note('같은 Shared Memory · 동기화 · 하나의 결과',GREEN)
