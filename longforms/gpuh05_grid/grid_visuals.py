"""Logical Grid and physical GPU stay separate; assignments are illustrative."""
import json
from pathlib import Path
from manim import *
from shared_style import StyleScene,text,box,stack,SHORT,INK,MUTED,BLUE,GREEN,ORANGE,PURPLE,PANEL
P=Path(__file__).resolve().parent
LAUNCH=['int blockSize = 128;','int gridSize = 12;','vectorAdd<<<gridSize, blockSize>>>(', '  d_A, d_B, d_C, N);']
INDEX=['int i = blockIdx.x * blockDim.x','      + threadIdx.x;','if (i < N)','  C[i] = A[i] + B[i];']
IMAGE=['dim3 block(16, 16);','dim3 grid((width + 15) / 16,','          (height + 15) / 16);','imageKernel<<<grid, block>>>(', '  d_in, d_out, width, height);']
ORDER_A=[7,2,9,5,0,8,3,11,4,1,10,6]
ORDER_B=[5,2,8,0,11,1,9,4,10,3,6,7]
def color(b):return GREEN if b==5 else BLUE if b==0 else PURPLE if b==1 else MUTED
class GridBase(StyleScene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start'];self.bounds=[];self.trace=[]
        self.gc=np.array([0,4.35,0]) if SHORT else np.array([-3.65,1.42,0]);self.gw=7.65 if SHORT else 7.1;self.gh=2.6 if SHORT else 2.25
        self.dc=np.array([0,1.08,0]) if SHORT else np.array([-3.65,-1.1,0]);self.dw=7.65 if SHORT else 7.1;self.dh=3 if SHORT else 2.55
        self.cc=np.array([0,-2.85,0]) if SHORT else np.array([4.15,.1,0]);self.cw=7.65 if SHORT else 6.15;self.ch=4.05 if SHORT else 4.7
        self.add(text('GPU HIERARCHY  /  LEVEL 05',19,MUTED).move_to([0,7.35 if SHORT else 4,0]),text(self.meta['title'],33,width=8 if SHORT else 14).move_to([0,6.45 if SHORT else 3.2,0]))
        self.logical();self.physical();self.code();self.note('Grid: 논리 작업 / GPU·SM: 물리 실행 장치')
        self.assign(0,0,animate=False)
        self.shot();self.to(self.meta['end'])
        self.record(self.grid_group)
        assert len(self.blocks)==12
        for b,sm in self.mapping.items():assert 0<=b<12 and 0<=sm<4
        suffix='shorts' if SHORT else 'longform'
        for name,data in [('geometry',self.bounds),('states',self.trace)]:
            (P/f'{name}_{suffix}_{self.INDEX:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    def record(self,g):self.bounds.append(dict(time=round(self.start+self.time,4),left=float(g.get_left()[0]),right=float(g.get_right()[0]),bottom=float(g.get_bottom()[1]),top=float(g.get_top()[1])))
    def logical(self):
        border=RoundedRectangle(width=7.65,height=2.6,corner_radius=.14,stroke_color=PURPLE,stroke_width=2,fill_color=PANEL,fill_opacity=.55)
        self.grid_title=text('Logical Grid · 1D / 12 Blocks',23,PURPLE,width=7.1).move_to([0,1.02,0]);g=VGroup(border,self.grid_title);self.blocks=[];self.dotgroups=[]
        for b in range(12):
            x=(b%4-1.5)*1.77;y=.49-b//4*.5
            r=RoundedRectangle(width=1.57,height=.41,corner_radius=.06,stroke_color=color(b),stroke_width=1.4,fill_color=color(b),fill_opacity=.1).move_to([x,y,0])
            label=text(f'B{b}',21,color(b)).move_to([x-.4,y,0])
            dots=VGroup(*(Rectangle(width=.043,height=.043,stroke_width=.3,color=color(b),fill_color=color(b),fill_opacity=.35) for _ in range(16))).arrange_in_grid(rows=4,cols=4,buff=.021).move_to([x+.34,y,0])
            group=VGroup(r,label,dots);self.blocks.append(group);self.dotgroups.append(dots);g.add(group)
        g.add(text('1D 번호표 줄바꿈 · 각 Block의 16점 = 128 Thread 축약',16,MUTED,width=7.15).move_to([0,-1.02,0]))
        self.place(g,self.gc,self.gw,self.gh);self.grid_group=g;self.add(g)
        self.trace.append(dict(kind='logical_layout',time=self.start,block_count=12,threads_per_block=128,logical_threads=1536,block_centers=[b.get_center().tolist() for b in self.blocks],block5_color=GREEN,scope='vectorAdd 1D'))
    def physical(self):
        border=RoundedRectangle(width=7.65,height=3,corner_radius=.14,stroke_color=BLUE,stroke_width=2,fill_color=PANEL,fill_opacity=.4)
        title=text('Physical GPU · 4 SM 예시',23,BLUE).move_to([0,1.21,0]);g=VGroup(border,title);self.sm_slots=[];self.sm_frames=[]
        for sm in range(4):
            x=(-1 if sm%2==0 else 1)*1.81;y=.53-(sm//2)*1.02
            frame=RoundedRectangle(width=3.35,height=.88,corner_radius=.07,stroke_color=BLUE if sm==0 else MUTED,stroke_width=1.4).move_to([x,y,0])
            label=text(f'SM {sm}',18,BLUE if sm==0 else MUTED).move_to([x,y+.27,0]);slots=VGroup(*(box('—',1.35,.34,MUTED,17).move_to([x+(k-.5)*1.48,y-.1,0]) for k in range(2)))
            self.sm_slots.append(slots);self.sm_frames.append(frame);g.add(frame,label,slots)
        g.add(text('상주 수·배치 순서는 설명용 · 실측 스케줄링 아님',15,MUTED,width=7.2).move_to([0,-1.22,0]))
        self.place(g,self.dc,self.dw,self.dh);self.gpu_group=g;self.add(g)
        self.mapping={};self.done=set();self.resident={sm:[] for sm in range(4)}
    def code(self,active=(),lines=None,label='vectorAdd.cu  ·  발췌'):
        lines=LAUNCH if lines is None else lines;self.active_code=[lines[n] for n in active];super().code(active,lines,label)
    def selected(self,b):
        for k,node in enumerate(self.blocks):node[0].set_stroke(color(k),width=3 if k==b else 1.4).set_fill(color(k),opacity=.28 if k==b else .08)
        self.trace.append(dict(kind='selected',time=round(self.start+self.time,4),block=b,color=color(b)))
    def assignment_state(self):
        self.trace.append(dict(kind='assignment',time=round(self.start+self.time,4),mapping={str(k):v for k,v in self.mapping.items()},completed=sorted(self.done),pending=[b for b in range(12) if b not in self.mapping and b not in self.done],capacity_per_sm=2,illustrative=True))
    def redraw_slots(self):
        for sm,slots in enumerate(self.sm_slots):
            for k,slot in enumerate(slots):
                b=self.resident[sm][k] if k<len(self.resident[sm]) else None
                slot.become(box('—' if b is None else f'B{b} · 4W',slot.width,slot.height,MUTED if b is None else color(b),17).move_to(slot))
    def assign(self,b,sm,animate=True):
        assert b not in self.mapping and b not in self.done and len(self.resident[sm])<2
        self.mapping[b]=sm;self.resident[sm].append(b);self.redraw_slots();self.selected(b)
        target=self.sm_slots[sm][len(self.resident[sm])-1]
        if animate:
            packet=box(f'B{b}',.7,.36,color(b),17).move_to(self.blocks[b]);self.add(packet)
            self.play(packet.animate.move_to(target),run_time=.65);self.remove(packet)
            self.play(Indicate(target,color=color(b),scale_factor=1.03),run_time=.25)
        self.assignment_state()
    def finish(self,b):
        sm=self.mapping.pop(b);self.resident[sm].remove(b);self.done.add(b);self.redraw_slots();self.blocks[b][0].set_fill(MUTED,opacity=.04);self.blocks[b][1].set_color(MUTED)
        self.trace.append(dict(kind='complete',time=round(self.start+self.time,4),block=b,freed_sm=sm));self.assignment_state()
    def reset_gpu(self):
        self.mapping={};self.done=set();self.resident={sm:[] for sm in range(4)};self.redraw_slots()
        for b,node in enumerate(self.blocks):node[1].set_color(color(b));node[0].set_fill(color(b),opacity=.08)
        self.assignment_state()
    def scenario(self):
        self.reset_gpu()
        for b,sm in [(7,0),(2,1),(9,2),(5,3)]:self.assign(b,sm,animate=False)
    def detail(self,g):
        self.remove(self.gpu_group)
        if hasattr(self,'dg'):self.remove(self.dg)
        self.place(g,self.dc,self.dw,self.dh);self.dg=g;self.add(g);return g
    def show_gpu(self):
        if hasattr(self,'dg'):self.remove(self.dg)
        self.add(self.gpu_group)
    def block_detail(self,b=0,t=5):
        cells=VGroup(*(Rectangle(width=.14,height=.19,stroke_width=.5,color=GREEN if k==t else color(b),fill_color=GREEN if k==t else color(b),fill_opacity=.8 if k==t else .12) for k in range(128))).arrange_in_grid(rows=4,cols=32,buff=(.035,.1))
        return stack(text(f'Block {b} · 128 Thread / 4 Warp',23,color(b)),cells,text(f'threadIdx.x = {t} · blockDim.x = 128',21,GREEN),buff=.2)
    def index_detail(self,b):
        idx=b*128+5
        nodes=VGroup(box(f'Block {b}',2.1,.55,color(b),25),box('Thread 5',2.1,.55,GREEN,25)).arrange(RIGHT,buff=.4)
        return stack(nodes,text(f'i = {b} × 128 + 5',32,INK),text(f'i = {idx}   →   C[{idx}]',36,GREEN),text(f'Block {b}: C[{b*128}…{b*128+127}]',21,MUTED),buff=.22)
    def index_example(self,b):
        self.selected(b);self.detail(self.index_detail(b));self.code([0,1],INDEX)
        self.trace.append(dict(kind='index',time=round(self.start+self.time,4),block=b,thread=5,block_dim=128,index=b*128+5,output=f'C[{b*128+5}]'))
    def sm_detail(self):
        rows=VGroup(*(box(f'Warp {w} · 32 Thread',3,.38,BLUE if w==0 else MUTED,19) for w in range(4))).arrange(DOWN,buff=.1)
        return stack(text('Grid B5 → SM 3 → 4 Warp',26,GREEN),rows,text('상주 Block의 Warp가 SM에서 명령 실행',18,MUTED),buff=.15)
    def image_grid(self):
        self.remove(self.grid_group)
        outer=RoundedRectangle(width=7.65,height=2.6,corner_radius=.13,stroke_color=PURPLE,stroke_width=2,fill_color=PANEL,fill_opacity=.5)
        self.tiles=VGroup(*(box(f'({x},{y})',1.18,.34,GREEN if (x,y)==(2,1) else MUTED,16).move_to([(x-2)*1.34,.5-y*.4,0]) for y in range(4) for x in range(5)))
        self.image_group=VGroup(outer,text('별도 2D 예제 · Grid 5 × 4 Blocks',22,PURPLE).move_to([0,1.03,0]),self.tiles,text('이미지 80 × 64 · Block당 16 × 16 Thread',17,MUTED).move_to([0,-1.06,0]))
        self.place(self.image_group,self.gc,self.gw,self.gh);self.add(self.image_group)
        self.trace.append(dict(kind='image_layout',time=round(self.start+self.time,4),grid=[5,4],block=[16,16],image=[80,64],selected=[2,1],separate_kernel='imageKernel'))
    def pixel_detail(self):
        pixels=VGroup(*(Rectangle(width=.09,height=.09,stroke_width=.3,color=GREEN,fill_color=GREEN,fill_opacity=.15+((x+y)%8)*.07) for y in range(16) for x in range(16))).arrange_in_grid(rows=16,cols=16,buff=.012)
        right=stack(text('Block (2, 1)',28,GREEN),text('16 × 16 pixels',23,INK),text('x: 32…47',24,BLUE),text('y: 16…31',24,BLUE),buff=.2)
        return VGroup(pixels,right).arrange(RIGHT,buff=.65)
    def shot(self):
        i=self.INDEX
        if i==0:
            self.remove(self.grid_group);intro=stack(text('SM 0 · Block 0',28,BLUE),VGroup(*(box(f'W{w}',1.2,.55,BLUE if w==0 else MUTED,20) for w in range(4))).arrange(RIGHT,buff=.12),text('Scheduler → Execution Units',22,GREEN),text('Register File · Shared Memory',19,PURPLE),buff=.25)
            self.detail(intro);self.code(lines=['Block → SM','Warp → Instruction'],label='실제 실행 공간에서 출발');self.to(5);self.remove(self.dg);self.play(FadeIn(self.gpu_group),run_time=.9)
            self.to(10);self.play(FadeIn(self.grid_group,shift=UP*.1),run_time=.9);self.to(12);self.code([1],LAUNCH);self.note('Grid = 하나의 kernel 실행에 속한 Block 전체',PURPLE);self.pulse(self.grid_group[0])
        elif i==1:
            self.code(lines=['12 Blocks','128 Threads / Block','12 * 128 = 1536'],label='논리적인 작업 수');self.note('각 Block의 작은 16점은 128 Thread의 축약 표시');self.to(19);self.pulse(self.grid_group[0]);self.to(23);self.detail(stack(text('12 × 128',40,INK),text('1,536 Logical Threads',35,GREEN),text('이번 vectorAdd: N = 1536',23,MUTED),buff=.25));self.pulse(self.dg)
        elif i==2:
            self.code(lines=['1536 logical threads','Concurrent execution?','Limited SM resources'],label='논리적인 수와 동시 실행 수');self.note('1,536 Thread를 정의했다고 동시에 실행되는 것은 아니다',ORANGE)
            self.to(34);self.reset_gpu();self.assign(5,3);self.to(37);self.assign(2,1);self.to(39);self.assign(7,0)
        elif i==3:
            self.code([2],LAUNCH);self.note('<<< Grid 크기, Block 크기 >>>');self.to(43);self.pulse(self.cg)
        elif i==4:
            self.selected(0);self.detail(self.block_detail(0));self.code([0],LAUNCH);self.note('Block = 128 Threads');self.to(51);self.pulse(self.dg)
            self.to(54);self.show_gpu();self.code([1],LAUNCH);self.note('Grid = 12 Blocks',PURPLE);self.pulse(self.grid_group[0])
        elif i==5:
            self.selected(0);self.detail(self.block_detail(0));self.code([0,1],INDEX);self.note('Block 번호와 Block 내부 Thread 번호가 함께 필요')
            self.to(64);self.code([0],INDEX);self.detail(stack(box('blockIdx.x = 0',5.5,.57,BLUE,27),box('blockDim.x = 128',5.5,.57,ORANGE,27),box('threadIdx.x = 5',5.5,.57,GREEN,27),buff=.2));self.to(68);self.code([1],INDEX)
        elif i==6:
            self.selected(0);self.detail(stack(text('i = Block 시작점 + 내부 위치',27,INK),text('i = blockIdx.x × 128',29,BLUE),text('    + threadIdx.x',29,GREEN),text('논리적인 데이터 인덱스',22,MUTED),buff=.2));self.code([0,1],INDEX);self.note('blockDim.x = 128인 현재 예제');self.to(74);self.pulse(self.cg)
        elif i==7:
            self.index_example(0);self.note('같은 threadIdx.x = 5');self.to(82);self.index_example(1);self.note('Block이 바뀌면 전체 데이터 위치도 달라진다',PURPLE)
        elif i==8:
            self.code([2,3],INDEX);self.detail(stack(box('B0 → C[0…127]',6,.55,BLUE,26),box('B1 → C[128…255]',6,.55,PURPLE,26),box('B5 → C[640…767]',6,.55,GREEN,26),buff=.23));self.selected(1);self.note('이 kernel에서는 Block별 출력 주소가 겹치지 않는다');self.to(90);self.selected(5);self.pulse(self.blocks[5])
        elif i==9:
            self.reset_gpu();self.code([2],LAUNCH);self.note('Grid의 ID를 유지하며 가용 SM에 배치 · 개념 예시');self.to(97)
            for b,sm in [(7,0),(2,1),(9,2),(5,3)]:self.assign(b,sm)
            self.to(101);self.selected(5);self.detail(self.sm_detail());self.note('같은 초록색 B5 · SM 3에서 Warp 단위 명령 실행',GREEN)
        elif i==10:
            self.scenario();self.code([2],LAUNCH);self.note('자원이 허용하면 한 SM에 여러 Block 상주');self.assign(0,0);self.to(108);self.selected(4);self.blocks[4][0].set_fill(ORANGE,opacity=.28);self.note('B4는 아직 미배치 · 자원 확보를 기다림',ORANGE)
            self.to(111);self.finish(7);self.assign(4,0);self.note('B7 완료 → 자원 확보 → B4 배치',GREEN)
        elif i==11:
            self.reset_gpu();self.code(lines=['// Block order is not guaranteed','// blockIdx.x is a logical ID','// no ordering dependency'],label='번호순 실행을 가정하지 않는다');self.note('배치 A · 7 → 2 → 9 → 5 (설명용)',ORANGE);self.to(117)
            for b,sm in zip(ORDER_A[:4],range(4)):self.assign(b,sm)
            self.to(121);self.reset_gpu();self.note('배치 B · 5 → 2 → 8 → 0 (설명용)',ORANGE)
            for b,sm in zip(ORDER_B[:4],range(4)):self.assign(b,sm)
            self.trace.append(dict(kind='order_examples',order_a=ORDER_A,order_b=ORDER_B,illustrative=True))
        elif i==12:
            self.detail(stack(text('순서 A · 7 → 2 → 9 → …',27,BLUE),text('순서 B · 5 → 2 → 8 → …',27,GREEN),text('C_A = C_B',38,GREEN),text('각 Block이 서로 다른 출력 영역을 쓰는 이 예제',20,MUTED),buff=.25));self.code([2,3],INDEX);self.note('독립적인 출력 영역 · Block 간 실행 순서 의존 없음');self.to(129);self.pulse(self.dg)
        elif i==13:
            self.code(lines=['dim3 grid(x, y, z);','// logical dimensions','// not physical SM positions'],label='Grid는 최대 3차원');self.detail(stack(text('Grid (x)',30,INK),text('Grid (x, y)',30,PURPLE),text('Grid (x, y, z)',30,GREEN),text('데이터 작업 공간의 논리적인 좌표',21,MUTED),buff=.2));self.note('Grid의 차원은 데이터 표현 방식');self.to(137);self.pulse(self.dg)
        elif i==14:
            self.image_grid();self.detail(self.pixel_detail());self.code([0,1,2,3],IMAGE,label='imageKernel.cu · 별도 2D 예제');self.note('80×64 이미지 · 20 Blocks · 256 Threads/Block');self.to(148);self.pulse(self.tiles[7]);self.code(lines=['int x = blockIdx.x * 16','      + threadIdx.x;','int y = blockIdx.y * 16','      + threadIdx.y;'],active=[0,2],label='imageKernel.cu · 픽셀 위치');self.note('Block (2,1) → x 32…47 / y 16…31',GREEN)
        elif i==15:
            self.image_grid();self.reset_gpu();self.code(lines=['blockIdx.x = 2','blockIdx.y = 1','// logical tile coordinates','// not an SM coordinate'],label='논리적인 이미지 좌표');self.note('Logical ≠ Physical · 이 좌표는 SM 위치가 아니다',ORANGE)
            self.marker=box('Tile (2,1)',1.2,.35,GREEN,17).move_to(self.tiles[7]);self.add(self.marker);self.play(self.marker.animate.move_to(self.sm_slots[3][0]),run_time=.9);self.to(153);self.note('Block (2,1)이 SM 3에서 실행되는 것도 가능한 배치 예시',GREEN)
            self.trace.append(dict(kind='image_assignment',tile=[2,1],sm=3,illustrative=True))
        elif i==16:
            self.code(lines=['Thread → Block → Grid','Warp → SM → GPU'],label='논리 구조와 하드웨어 실행 관계');self.detail(stack(box('Thread · 개별 실행 문맥',6.2,.55,BLUE,26),box('Block · 협력 그룹',6.2,.55,GREEN,26),box('Grid · kernel 작업 전체',6.2,.55,PURPLE,26),buff=.22));self.note('Warp는 명령 실행 단위 · SM은 실행 하드웨어');self.to(159);self.pulse(self.blocks[0]);self.to(162);self.pulse(self.grid_group[0])
        elif i==17:
            self.reset_gpu();self.code([0,1,2],LAUNCH);self.note('Grid = Logical Workload / SM = Physical Execution',GREEN)
            for b,sm in [(5,3),(2,1),(9,2),(0,0)]:self.assign(b,sm)
            self.to(171);self.pulse(self.grid_group[0]);self.pulse(self.gpu_group[0]);self.to(174);self.finish(2);self.assign(8,1);self.to(177);self.note('Grid는 우리가 정의한 작업 · SM은 그 작업을 실행',GREEN)
