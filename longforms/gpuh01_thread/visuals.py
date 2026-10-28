"""Shared CUDA values and responsive layouts for independent exact-duration shots."""
import os,json
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.getenv('GPUH_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16
config.frame_height=16 if SHORT else 9
config.background_color='#0B1220'
INK='#ECF4FF';MUTED='#93A5BD';BLUE='#55B5FF';GREEN='#50E0AE';ORANGE='#FFBD69';PURPLE='#C29BFF';PANEL='#121F33'
COLS=[BLUE,GREEN,ORANGE,PURPLE]
def text(s,size=28,color=INK,width=None,mono=False):
    t=Text(s,font='Consolas' if mono else 'Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if width and t.width>width:t.scale_to_fit_width(width)
    return t
def box(label,w=1.5,h=.85,col=BLUE,size=25,fill=.12):
    r=RoundedRectangle(width=w,height=h,corner_radius=.12,stroke_color=col,stroke_width=2,fill_color=col,fill_opacity=fill)
    return VGroup(r,text(label,size,col,width=w-.15).move_to(r))
def stack(*items,buff=.35):
    g=VGroup(*items).arrange(DOWN,buff=buff)
    for item in items:
        if hasattr(item,'focus'):g.focus=item.focus
    return g
def thread(t=1):
    fields=VGroup(*(box(s,4.7,.72,c,24) for s,c in [('Instruction  /  LOAD → ADD → STORE',BLUE),(f'Index  /  threadIdx.x = {t}',GREEN),('State  /  intermediate values',ORANGE)])).arrange(DOWN,buff=.22)
    g=stack(text(f'Thread {t}',38,COLS[t]),fields,text('논리적인 실행 문맥',24,MUTED));g.focus=t
    return g
def block(b=0,selected=None):
    cards=VGroup(*(box(f'T{t}',1.35,.85,COLS[t],28,fill=.3 if t==selected else .08) for t in range(4))).arrange(RIGHT,buff=.17)
    border=SurroundingRectangle(cards,buff=.3,color=MUTED,corner_radius=.14)
    g=stack(text(f'Block {b}',27,MUTED),VGroup(border,cards),text('threadIdx.x     0        1        2        3',20,MUTED,width=6.2))
    if selected is not None:g.focus=selected
    return g
def arrays(active=None,results=0,threads=False):
    rows=[]
    for name,values,c in [('A',[1,2,3,4],BLUE),('B',[10,20,30,40],GREEN),('C',[11,22,33,44],ORANGE)]:
        cells=VGroup(*(box(str(v) if name!='C' or k<results else '?',1.1,.6,COLS[k] if active==k else c,28,fill=.3 if active==k else .08) for k,v in enumerate(values))).arrange(RIGHT,buff=.17)
        label=text(name,27,c).next_to(cells,LEFT,buff=.3);rows.append(VGroup(label,cells))
    g=VGroup(*rows).arrange(DOWN,buff=.3,aligned_edge=RIGHT)
    links=VGroup()
    if active is not None:
        for r in range(2):links.add(Arrow(rows[r][1][active].get_bottom(),rows[r+1][1][active].get_top(),buff=.08,color=COLS[active],stroke_width=3,max_tip_length_to_length_ratio=.25))
    out=VGroup(g,links)
    # Thread identities stay in the persistent map; do not redraw another set.
    if active is not None:out.focus=active
    return out
KERNEL=['__global__ void vectorAdd(', '    const float* A, const float* B,', '    float* C, int N) {','  int i = blockIdx.x * blockDim.x','        + threadIdx.x;','  if (i < N) {','    float a = A[i];','    float b = B[i];','    float sum = a + b;','    C[i] = sum;','  }','}']
class ThreadBase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start']
        self.dc=np.array([0,1.5,0]) if SHORT else np.array([-3.65,-1.05,0]);self.dw=7.65 if SHORT else 7.1;self.dh=2.7 if SHORT else 2.15
        self.cc=np.array([0,-2.7,0]) if SHORT else np.array([4.15,.15,0]);self.cw=7.65 if SHORT else 6.15;self.ch=4.35 if SHORT else 4.7
        self.add(text('GPU HIERARCHY  /  LEVEL 01',19,MUTED).move_to([0,7.35 if SHORT else 4.,0]),text(self.meta['title'],34,width=8 if SHORT else 14).move_to([0,6.45 if SHORT else 3.2,0]))
        self.add(Line([-3.9,5.85,0],[3.9,5.85,0],color=MUTED,stroke_opacity=.25) if SHORT else Line([-7.3,2.7,0],[7.3,2.7,0],color=MUTED,stroke_opacity=.25))
        self.bounds=[];self.selected=0 if self.INDEX<4 else (3 if self.INDEX==7 else 1)
        if self.INDEX in (12,13):self.selected=2
        if self.INDEX==14:self.selected=6
        self.world_map();self.shot();self.to(self.meta['end'])
        (P/f'geometry_{"shorts" if SHORT else "longform"}_{self.INDEX:02}.json').write_text(json.dumps(self.bounds,indent=2),encoding='utf-8')
    def to(self,t):
        rem=t-self.start-self.time
        if rem<-.04:raise RuntimeError(f'{self.INDEX}: {self.time} exceeds {t-self.start}')
        if rem>.001:self.wait(rem)
    def place(self,g,center,w,h):
        scale=min(w/max(g.width,.001),h/max(g.height,.001),1.25);g.scale(scale).move_to(center)
        self.bounds.append(dict(time=self.start+self.time,left=float(g.get_left()[0]),right=float(g.get_right()[0]),bottom=float(g.get_bottom()[1]),top=float(g.get_top()[1])))
        assert g.get_left()[0]>-config.frame_width/2+.2 and g.get_right()[0]<config.frame_width/2-.2
        return g
    def diagram(self,g,animate=True):
        if hasattr(g,'focus'):self.select_thread(g.focus)
        caption=('같은 SM 0의 자원을 확대' if getattr(g,'scope',None)=='sm' else
                 'Block 0 · 1의 같은 내부 위치 비교' if self.INDEX in (12,13) else
                 'Block의 2D 설정 예시 · 선택 (2, 1)' if self.INDEX==14 else
                 f'SM 0 → Block 0 → Thread {self.selected} · 확대')
        self.map_caption.become(text(caption,17,MUTED,width=7).move_to(self.map_caption))
        self.place(g,self.dc,self.dw,self.dh)
        if hasattr(self,'dg'):
            if animate:
                source=self.map_sm if getattr(g,'scope',None)=='sm' else self.anchor
                self.play(FadeOut(self.dg),TransformFromCopy(source,g),run_time=.4)
            else:self.remove(self.dg);self.add(g)
        else:
            self.add(g)
        self.dg=g;return g
    def world_map(self):
        """The same placement diagram survives every cut; insets come from it."""
        self.map_center=np.array([0,4.5,0]) if SHORT else np.array([-3.65,1.48,0])
        scale=1 if SHORT else .86
        gpu=RoundedRectangle(width=7.65,height=2.5,corner_radius=.15,
                             stroke_color=BLUE,stroke_width=1.8,fill_color=PANEL,fill_opacity=.45)
        sm=RoundedRectangle(width=7.1,height=1.68,corner_radius=.1,
                            stroke_color='#7086A3',stroke_width=1.5).shift(DOWN*.18)
        self.map_sm=sm
        if self.INDEX>=9:sm.set_stroke(PURPLE)
        nodes=VGroup(gpu,sm,text('GPU',19,BLUE).move_to([-3.2,1.02,0]),
                     text('SM 0',20,INK).move_to([-2.95,.48,0]),
                     text('실행 배치 개념도',16,MUTED).move_to([2.5,1.02,0]))
        self.map_threads=[]
        for b,x in [(0,-1.78),(1,1.78)]:
            visible=b==0 or (self.INDEX>=12 and self.INDEX!=14)
            boundary=DashedVMobject(RoundedRectangle(width=3.16,height=.75,corner_radius=.08),num_dashes=30).set_color(MUTED).move_to([x,-.15,0])
            label=text(('Block 0 · 2D 설정 예시' if self.INDEX==14 and b==0 else f'Block {b} · 논리 그룹') if visible else '다른 Block',16,MUTED).move_to([x,.08,0])
            slots=VGroup(*(box(f'T{t}',.55,.35,COLS[t],16,fill=.12) for t in range(4))).arrange(RIGHT,buff=.13).move_to([x,-.29,0])
            if self.INDEX==14 and b==0:
                slots=VGroup(*(Square(side_length=.075,color=GREEN if k==6 else BLUE,fill_opacity=.5 if k==6 else .07,stroke_width=1) for k in range(16))).arrange_in_grid(rows=4,cols=4,buff=.03).move_to([x,-.29,0])
            if not visible:boundary.set_opacity(.2);label.set_opacity(.35);slots.set_opacity(.15)
            nodes.add(boundary,label,slots);self.map_threads.append(slots)
        self.resource=box('Register File' if self.INDEX>=9 else 'SM의 저장 자원',5.95,.38,PURPLE,17,fill=.07).move_to([0,-.73,0]);nodes.add(self.resource)
        nodes.scale(scale).move_to(self.map_center)
        self.map_sm=VGroup(sm,nodes[3],*list(nodes)[5:])
        self.map_group=nodes;self.add(nodes)
        self.bounds.append(dict(time=self.start+self.time,left=float(nodes.get_left()[0]),right=float(nodes.get_right()[0]),bottom=float(nodes.get_bottom()[1]),top=float(nodes.get_top()[1])))
        self.anchor=self.map_threads[0][self.selected]
        self.ring=SurroundingRectangle(self.anchor,buff=.045,color=GREEN if self.INDEX==14 else COLS[self.selected],stroke_width=3)
        self.add(self.ring)
        if self.INDEX in (12,13):
            self.add(SurroundingRectangle(self.map_threads[1][2],buff=.045,color=ORANGE,stroke_width=3))
        self.map_caption=text('선택한 Thread에서 아래 화면을 확대',16,MUTED,width=7).move_to([self.map_center[0],3.12 if SHORT else .22,0])
        self.add(self.map_caption)
    def select_thread(self,t):
        self.selected=t;self.anchor=self.map_threads[0][t]
        self.ring.become(SurroundingRectangle(self.anchor,buff=.045,color=COLS[t],stroke_width=3))
    def sm_detail(self):
        """Enlarge the same SM, retaining Block 0 and its Thread positions."""
        outer=RoundedRectangle(width=6.9,height=2.55,corner_radius=.13,stroke_color=PURPLE,stroke_width=2,fill_color=PANEL,fill_opacity=.3)
        heading=text('SM 0  /  같은 실행 장치',23,INK).move_to([0,1.02,0])
        slots=VGroup(*(box(f'T{t}',.8,.48,COLS[t],22,fill=.35 if t==1 else .07) for t in range(4))).arrange(RIGHT,buff=.19).move_to([0,.15,0])
        block_border=DashedVMobject(RoundedRectangle(width=4.4,height=.9,corner_radius=.08),num_dashes=40).set_color(MUTED).move_to([0,.25,0])
        block_label=text('Block 0 · 논리 그룹',17,MUTED).move_to([0,.53,0])
        regs=VGroup(*(box('',.38,.3,GREEN if 4<=k<7 else PURPLE,16,fill=.4 if 4<=k<7 else .05) for k in range(12))).arrange(RIGHT,buff=.07).move_to([0,-.78,0])
        rlabel=text('Register File  /  SM의 물리 자원',17,PURPLE).move_to([0,-1.10,0])
        arrow=Arrow(slots[1].get_bottom(),[slots[1].get_center()[0],-.58,0],buff=.07,color=GREEN,stroke_width=2)
        alloc=text('Thread 1의 할당 예시',16,GREEN).move_to([1.2,-.36,0])
        g=VGroup(outer,heading,block_border,block_label,slots,regs,rlabel,arrow,alloc);g.focus=1;g.scope='sm'
        return g
    def code(self,active=(),lines=None,label='vector_add.cu  /  CUDA C++'):
        # Show only the current source excerpt, without a numbered gutter.
        # Fixed panel dimensions and padding keep code distinct from diagrams.
        if lines is None:
            if list(active)==[0]:
                lines=['__global__ void vectorAdd(', '  const float* A,', '  const float* B,', '  float* C, int N) {', '  // ...', '}'];active=[0]
            else:
                selected=sorted(set(active))
                if 4 in selected and 3 not in selected:selected=sorted([3]+selected)
                lines=[KERNEL[n].strip() for n in selected]
                active=[k for k,n in enumerate(selected) if n in active]
        # Blank lines consume scarce video space without adding information.
        rows=[(s,n in active) for n,s in enumerate(lines) if s.strip()]
        body=VGroup()
        for s,on in rows:
            line=Text(s,font='Consolas',font_size=32 if SHORT else 30,
                      color=INK,line_spacing=1.2,
                      t2c={'__global__':PURPLE,'float':PURPLE,'int':PURPLE,
                           'threadIdx.x':GREEN,'blockIdx.x':GREEN,'blockDim.x':GREEN,
                           'sum':ORANGE,'for':PURPLE,'if':PURPLE})
            body.add(line)
        body.arrange(DOWN,buff=.21,aligned_edge=LEFT)
        available_w=self.cw-.8;available_h=self.ch-1.05
        factor=min(available_w/max(body.width,.001),available_h/max(body.height,.001),1)
        body.scale(factor)
        panel=RoundedRectangle(width=self.cw,height=self.ch,corner_radius=.16,
                               stroke_color='#48617F',stroke_width=2,
                               fill_color=PANEL,fill_opacity=1).move_to(self.cc)
        title=text(label.replace('  /  CUDA C++','  ·  발췌'),20,BLUE,width=self.cw-.65)
        title.move_to([self.cc[0]-self.cw/2+.32+title.width/2,self.cc[1]+self.ch/2-.35,0])
        separator=Line([self.cc[0]-self.cw/2+.15,self.cc[1]+self.ch/2-.7,0],
                       [self.cc[0]+self.cw/2-.15,self.cc[1]+self.ch/2-.7,0],
                       color='#48617F',stroke_width=1)
        body.move_to([self.cc[0]-self.cw/2+.4+body.width/2,self.cc[1]-.35,0])
        highlights=VGroup()
        for n,(_,on) in enumerate(rows):
            if on:
                r=RoundedRectangle(width=self.cw-.35,height=body[n].height+.16,
                                   corner_radius=.04,stroke_width=0,
                                   fill_color=BLUE,fill_opacity=.14)
                r.move_to([self.cc[0],body[n].get_center()[1],0]);highlights.add(r)
        group=VGroup(panel,highlights,separator,title,body)
        self.bounds.append(dict(time=self.start+self.time,left=float(group.get_left()[0]),right=float(group.get_right()[0]),bottom=float(group.get_bottom()[1]),top=float(group.get_top()[1])))
        if hasattr(self,'cg'):self.remove(self.cg)
        self.cg=group;self.add(group)
    def note(self,s,col=MUTED):
        if hasattr(self,'ng'):self.remove(self.ng)
        self.ng=text(s,23,col,width=7.7 if SHORT else 14).move_to([0,-5.35 if SHORT else -2.7,0]);self.add(self.ng)
    def pulse(self,m):self.play(Indicate(m,color=ORANGE,scale_factor=1.025),run_time=.6)
    def shot(self):
        i=self.INDEX
        if i==0:
            chips=VGroup(*(box('',.65,.5,COLS[k%4]) for k in range(48))).arrange_in_grid(rows=6,cols=8,buff=.12)
            self.diagram(stack(text('GPU',42,BLUE),chips));self.note('수많은 작업을 나누어 처리')
            self.play(LaggedStart(*(Indicate(x,color=GREEN,scale_factor=1.1) for x in chips),lag_ratio=.02),run_time=2.5);self.to(3)
            self.code(lines=['GPU','  SM','    Block','      Thread'],label='실행 범위를 좁혀 보기')
            self.to(7);self.diagram(thread(0));self.note('THREAD',BLUE)
        elif i==1:
            self.diagram(thread(0));self.code(lines=['Instruction : execute commands','Index       : select data','State       : keep own context'],label='Thread  /  logical context')
            self.note('Thread ≠ 물리 연산기 하나');self.to(11);self.pulse(self.dg);self.to(14);self.note('명령 · 데이터 · 실행 상태',BLUE)
        elif i==2:
            self.diagram(arrays());self.code(lines=['A = [1, 2, 3, 4]','B = [10, 20, 30, 40]','','C[i] = A[i] + B[i]'],active=[3],label='같은 위치의 원소를 더한다')
            self.note('C[i] = A[i] + B[i]',ORANGE);self.to(18)
            self.pulse(self.dg);self.to(24)
            for k in range(4):self.diagram(arrays(k,k+1));self.play(Indicate(self.dg,color=COLS[k],scale_factor=1.01),run_time=.35)
        elif i==3:
            self.diagram(arrays(0,1));self.code(lines=['for (int i = 0; i < N; ++i) {','  C[i] = A[i] + B[i];','}'],active=[0],label='CPU 반복문 표현 예시')
            self.note('CPU도 병렬화할 수 있음');self.to(33)
            self.diagram(arrays(None,4,True));self.code([4,8,9]);self.note('CUDA: 서로 다른 Thread에 작업 배정',BLUE)
        elif i==4:
            self.diagram(thread(1));self.code([0]);self.note('__global__  →  GPU에서 실행되는 kernel',BLUE);self.to(40)
            self.pulse(self.cg);self.to(44);self.code([4]);self.note('threadIdx.x  →  Block 내부의 인덱스',GREEN);self.diagram(block(0,1));self.pulse(self.cg)
        elif i==5:
            self.diagram(block());self.code(lines=['// N = 4; one block','vectorAdd<<<1, 4>>>(', '    d_A, d_B, d_C, 4);','','// blockIdx.x = 0','// blockDim.x = 4'],active=[1],label='Host launch  /  발췌')
            self.note('4 Thread는 교육용 축소 예시 · Warp는 32 lane');self.to(52)
            for k in range(4):self.diagram(block(0,k))
        elif i==6:
            self.code([4,6,7,8,9]);self.note('Block 0  ·  i = threadIdx.x')
            for k,t in enumerate([55,57,59,60.5]):
                self.to(t);self.diagram(stack(arrays(k,k+1,True),text(f'Thread {k}   {k+1} + {(k+1)*10} = {(k+1)*11}',29,COLS[k])));self.pulse(self.dg)
        elif i==7:
            self.diagram(arrays(None,4,True));self.code([4,6,7,9]);self.note('같은 코드 · 다른 인덱스 · 다른 데이터',BLUE)
            self.pulse(self.cg);self.to(65)
            for k in range(4):self.diagram(arrays(k,4,True));self.pulse(self.dg)
        elif i==8:
            self.diagram(thread(1));self.code([4]);self.note('선택된 실행 문맥: Thread 1');self.to(72)
            for at,lines,s,col in [(72,[6],'LOAD   A[1] → a = 2',BLUE),(73.3,[7],'LOAD   B[1] → b = 20',GREEN),(74.6,[8],'ADD   2 + 20 → sum = 22',ORANGE),(76,[9],'STORE   sum → C[1] = 22',PURPLE)]:
                self.to(at);self.code(lines);self.diagram(stack(box('Thread 1  /  i = 1',5.4,.85,GREEN),text(s,31,col,width=6.5),box('A[1] = 2    B[1] = 20',5.4,.85,GREEN),box('C[1] = 22' if at>=76 else 'C[1] = ?',5.4,.85,ORANGE)))
            self.to(77);self.note('소스 수준의 동작 · 실제 명령은 최적화될 수 있음');self.pulse(self.dg)
        elif i in (9,10):
            if i==9:
                self.diagram(stack(box('Thread 1  /  i = 1',5.4,.85,GREEN),box('a = 2    b = 20    sum = 22',5.4,.85,GREEN),box('C[1] = 22',5.4,.85,ORANGE)))
                self.diagram(self.sm_detail())
            else:self.diagram(self.sm_detail())
            self.code([6,7,8]);self.note('개념도 · 소스 변수와 물리 Register는 일대일이 아님')
            if i==9:self.to(85);self.pulse(self.resource);self.to(89);self.note('같은 SM 0 안에서 Thread 1에 Register 자원 할당',PURPLE)
            else:
                self.to(95);self.code(lines=['Source variables','a      b      sum','','Compiler allocation','','Register File on the SM'],active=[3],label='소스와 물리 자원 사이');self.pulse(self.dg);self.note('구체적인 값 배치와 Register 수는 compiler가 결정')
        elif i==11:
            self.select_thread(0)
            self.diagram(stack(box('Thread 0',3,.85,BLUE),box('C[0]',2,.8,ORANGE)));self.code([4,9]);self.note('Thread 하나 = 원소 하나일까?',ORANGE);self.to(102)
            self.note('원소 수는 코드가 정한다',GREEN);self.to(103)
            self.code(lines=['// one block, four threads','int t = threadIdx.x;','int S = blockDim.x;','for (int j = t; j < N; j += S) {','  C[j] = A[j] + B[j];','}'],active=[3,4],label='한 Thread가 여러 원소 처리')
            row=VGroup(*(box(f'C[{k}]',1.6,.8,ORANGE) for k in [0,4,8])).arrange(RIGHT,buff=.3)
            self.diagram(stack(box('Thread 0',3,.85,BLUE),text('j = 0 → 4 → 8 → …',30,BLUE),row));self.pulse(self.dg)
        elif i==12:
            left=stack(box('Block 0 · T2',2.9,.65,ORANGE),text('threadIdx.x = 2',24,ORANGE))
            right=stack(box('Block 1 · T2',2.9,.65,ORANGE),text('threadIdx.x = 2',24,ORANGE))
            self.diagram(VGroup(left,right).arrange(RIGHT,buff=.5));self.code([4]);self.note('Block마다 threadIdx.x는 다시 0부터');self.to(112);self.pulse(self.dg);self.to(116)
            self.code(lines=['Block 0:  threadIdx.x = 2','Block 1:  threadIdx.x = 2','','Same local index','Different blocks'],active=[0,1],label='두 Block의 Thread 2');self.note('threadIdx.x ≠ GPU 전체의 고유 번호',ORANGE)
        elif i==13:
            first=VGroup(box('Block 0 · T2',2.5,.65,ORANGE),text('0 × 4 + 2 = 2',29,ORANGE)).arrange(RIGHT,buff=.35)
            second=VGroup(box('Block 1 · T2',2.5,.65,ORANGE),text('1 × 4 + 2 = 6',29,ORANGE)).arrange(RIGHT,buff=.35)
            self.diagram(stack(first,second,text('같은 내부 인덱스 2 · 서로 다른 배열 위치',23,MUTED)))
            self.code([3,4]);self.note('i = blockIdx.x × blockDim.x + threadIdx.x',BLUE);self.to(124);self.pulse(self.cg);self.to(126);self.note('같은 내부 위치 2 → 전체 배열 위치 2 또는 6',ORANGE)
        elif i==14:
            grid=VGroup(*(box(f'({x},{y})',.95,.45,GREEN if (x,y)==(2,1) else BLUE,23,fill=.3 if (x,y)==(2,1) else .08) for y in range(4) for x in range(4))).arrange_in_grid(rows=4,cols=4,buff=.1)
            self.diagram(stack(text('2D Block  /  logical coordinates',27,BLUE),grid,text('x = column     y = row',24,GREEN)))
            self.code(lines=['dim3 threads(4, 4);','','int col = threadIdx.x;','int row = threadIdx.y;','','// Up to x, y, z dimensions'],active=[2,3],label='배열에 대응하는 논리 좌표');self.note('예시 선택: (x, y) = (2, 1)');self.to(134);self.note('논리 좌표 ≠ 실제 칩 위의 물리 위치',ORANGE);self.pulse(self.dg)
        elif i==15:
            self.diagram(thread(1));self.code(lines=['Index  : logical position','State  : per-thread context','Work   : commands and data'],active=[0,1,2],label='THREAD  /  논리적 실행 단위');self.note('자신의 인덱스와 실행 상태로 명령 수행',BLUE);self.to(146)
            self.diagram(stack(block(0),text('동일한 kernel · 서로 다른 작업',29,GREEN)));self.code([4,6,7,8,9]);self.note('GPU 병렬 계산의 출발점: 작업 배정',GREEN);self.pulse(self.dg)
