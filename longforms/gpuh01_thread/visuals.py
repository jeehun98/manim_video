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
def stack(*items,buff=.35):return VGroup(*items).arrange(DOWN,buff=buff)
def thread(t=1):
    fields=VGroup(*(box(s,4.7,.72,c,24) for s,c in [('Instruction  /  LOAD → ADD → STORE',BLUE),(f'Index  /  threadIdx.x = {t}',GREEN),('State  /  intermediate values',ORANGE)])).arrange(DOWN,buff=.22)
    return stack(text(f'Thread {t}',38,BLUE),fields,text('논리적인 실행 문맥',24,MUTED))
def block(b=0,selected=None):
    cards=VGroup(*(box(f'T{t}',1.35,.85,COLS[t],28,fill=.3 if t==selected else .08) for t in range(4))).arrange(RIGHT,buff=.17)
    border=SurroundingRectangle(cards,buff=.3,color=MUTED,corner_radius=.14)
    return stack(text(f'Block {b}',27,MUTED),VGroup(border,cards),text('threadIdx.x     0        1        2        3',20,MUTED,width=6.2))
def arrays(active=None,results=0,threads=False):
    rows=[]
    for name,values,c in [('A',[1,2,3,4],BLUE),('B',[10,20,30,40],GREEN),('C',[11,22,33,44],ORANGE)]:
        cells=VGroup(*(box(str(v) if name!='C' or k<results else '?',1.1,.7,COLS[k] if active==k else c,27,fill=.3 if active==k else .08) for k,v in enumerate(values))).arrange(RIGHT,buff=.17)
        label=text(name,27,c).next_to(cells,LEFT,buff=.3);rows.append(VGroup(label,cells))
    g=VGroup(*rows).arrange(DOWN,buff=.65,aligned_edge=RIGHT)
    links=VGroup()
    if active is not None:
        for r in range(2):links.add(Arrow(rows[r][1][active].get_bottom(),rows[r+1][1][active].get_top(),buff=.08,color=COLS[active],stroke_width=3,max_tip_length_to_length_ratio=.25))
    out=VGroup(g,links)
    if threads:
        ts=VGroup(*(box(f'T{k}',1.1,.58,COLS[k],22,fill=.3 if active==k else .08) for k in range(4))).arrange(RIGHT,buff=.17).next_to(rows[0][1],UP,buff=.65)
        out.add(ts)
        if active is not None:out.add(Arrow(ts[active].get_bottom(),rows[0][1][active].get_top(),buff=.08,color=COLS[active],stroke_width=3,max_tip_length_to_length_ratio=.25))
    return out
KERNEL=['__global__ void vectorAdd(', '    const float* A, const float* B,', '    float* C, int N) {','  int i = blockIdx.x * blockDim.x','        + threadIdx.x;','  if (i < N) {','    float a = A[i];','    float b = B[i];','    float sum = a + b;','    C[i] = sum;','  }','}']
class ThreadBase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start']
        self.dc=np.array([0,2.7,0]) if SHORT else np.array([-3.65,.1,0]);self.dw=7.65 if SHORT else 7.1;self.dh=5.5 if SHORT else 4.5
        self.cc=np.array([0,-2.7,0]) if SHORT else np.array([4.15,.15,0]);self.cw=7.65 if SHORT else 6.15;self.ch=4.35 if SHORT else 4.7
        self.add(text('GPU HIERARCHY  /  LEVEL 01',19,MUTED).move_to([0,7.35 if SHORT else 4.,0]),text(self.meta['title'],34,width=8 if SHORT else 14).move_to([0,6.45 if SHORT else 3.2,0]))
        self.add(Line([-3.9,5.85,0],[3.9,5.85,0],color=MUTED,stroke_opacity=.25) if SHORT else Line([-7.3,2.7,0],[7.3,2.7,0],color=MUTED,stroke_opacity=.25))
        self.bounds=[];self.shot();self.to(self.meta['end'])
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
        self.place(g,self.dc,self.dw,self.dh)
        if hasattr(self,'dg'):
            if animate:self.play(FadeOut(self.dg),FadeIn(g),run_time=.4)
            else:self.remove(self.dg);self.add(g)
        else:self.add(g)
        self.dg=g;return g
    def code(self,active=(),lines=None,label='vector_add.cu  /  CUDA C++'):
        lines=KERNEL if lines is None else lines
        body=VGroup()
        for n,s in enumerate(lines):
            line=text(f'{n+1:02}  '+s,21,INK if n in active else MUTED,mono=True)
            body.add(line)
        body.arrange(DOWN,buff=.13,aligned_edge=LEFT)
        if body.width>self.cw-.5:body.scale_to_fit_width(self.cw-.5)
        if body.height>self.ch-.65:body.scale_to_fit_height(self.ch-.65)
        highlights=VGroup(*(SurroundingRectangle(body[n],buff=.06,color=BLUE,stroke_width=1.5,fill_color=BLUE,fill_opacity=.1) for n in active if n<len(body)))
        group=stack(text(label,19,BLUE),VGroup(highlights,body),buff=.24)
        self.place(group,self.cc,self.cw,self.ch)
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
                self.to(at);self.code(lines);self.diagram(stack(box('Thread 1  /  i = 1',5.4,.85,BLUE),text(s,31,col,width=6.5),box('A[1] = 2    B[1] = 20',5.4,.85,GREEN),box('C[1] = 22' if at>=76 else 'C[1] = ?',5.4,.85,ORANGE)))
            self.to(77);self.note('소스 수준의 동작 · 실제 명령은 최적화될 수 있음');self.pulse(self.dg)
        elif i in (9,10):
            regs=VGroup(*(box(f'r{k}',.75,.62,COLS[k%4],21) for k in range(12))).arrange_in_grid(rows=3,cols=4,buff=.12)
            sm=stack(text('SM  /  physical resource',25,MUTED),text('Register File',31,PURPLE),regs)
            th=box('Thread 1  /  logical context',5.5,.85,BLUE)
            g=stack(th,Arrow(UP*.3,DOWN*.3,color=PURPLE,buff=0),sm)
            self.diagram(g);self.code([6,7,8]);self.note('개념도 · 소스 변수와 물리 Register는 일대일이 아님')
            if i==9:self.to(85);self.pulse(self.dg);self.to(89);self.note('Register File은 SM에 존재하는 공유 물리 자원',PURPLE)
            else:
                self.to(95);self.code(lines=['Source variables','a      b      sum','','Compiler allocation','','Register File on the SM'],active=[3],label='소스와 물리 자원 사이');self.pulse(self.dg);self.note('구체적인 값 배치와 Register 수는 compiler가 결정')
        elif i==11:
            self.diagram(stack(box('Thread 0',3,.85,BLUE),box('C[0]',2,.8,ORANGE)));self.code([4,9]);self.note('Thread 하나 = 원소 하나일까?',ORANGE);self.to(102)
            self.note('원소 수는 코드가 정한다',GREEN);self.to(103)
            self.code(lines=['// one block, four threads','int t = threadIdx.x;','int S = blockDim.x;','for (int j = t; j < N; j += S) {','  C[j] = A[j] + B[j];','}'],active=[3,4],label='한 Thread가 여러 원소 처리')
            row=VGroup(*(box(f'C[{k}]',1.6,.8,ORANGE) for k in [0,4,8])).arrange(RIGHT,buff=.3)
            self.diagram(stack(box('Thread 0',3,.85,BLUE),text('j = 0 → 4 → 8 → …',30,BLUE),row));self.pulse(self.dg)
        elif i==12:
            self.diagram(stack(block(0,2),block(1,2),buff=.45));self.code([4]);self.note('Block마다 threadIdx.x는 다시 0부터');self.to(112);self.pulse(self.dg);self.to(116)
            self.code(lines=['Block 0:  threadIdx.x = 2','Block 1:  threadIdx.x = 2','','Same local index','Different blocks'],active=[0,1],label='두 Block의 Thread 2');self.note('threadIdx.x ≠ GPU 전체의 고유 번호',ORANGE)
        elif i==13:
            self.diagram(stack(block(0,2),block(1,2),text('Block 0:  0 × 4 + 2 = 2',28,ORANGE),text('Block 1:  1 × 4 + 2 = 6',28,ORANGE),buff=.28))
            self.code([3,4]);self.note('i = blockIdx.x × blockDim.x + threadIdx.x',BLUE);self.to(124);self.pulse(self.cg);self.to(126);self.note('같은 내부 위치 2 → 전체 배열 위치 2 또는 6',ORANGE)
        elif i==14:
            grid=VGroup(*(box(f'({x},{y})',1.15,.78,GREEN if (x,y)==(2,1) else BLUE,23,fill=.3 if (x,y)==(2,1) else .08) for y in range(4) for x in range(4))).arrange_in_grid(rows=4,cols=4,buff=.15)
            self.diagram(stack(text('2D Block  /  logical coordinates',27,BLUE),grid,text('x = column     y = row',24,GREEN)))
            self.code(lines=['dim3 threads(4, 4);','','int col = threadIdx.x;','int row = threadIdx.y;','','// Up to x, y, z dimensions'],active=[2,3],label='배열에 대응하는 논리 좌표');self.note('예시 선택: (x, y) = (2, 1)');self.to(134);self.note('논리 좌표 ≠ 실제 칩 위의 물리 위치',ORANGE);self.pulse(self.dg)
        elif i==15:
            self.diagram(thread(1));self.code(lines=['Index  : logical position','State  : per-thread context','Work   : commands and data'],active=[0,1,2],label='THREAD  /  논리적 실행 단위');self.note('자신의 인덱스와 실행 상태로 명령 수행',BLUE);self.to(146)
            self.diagram(stack(block(0),text('동일한 kernel · 서로 다른 작업',29,GREEN)));self.code([4,6,7,8,9]);self.note('GPU 병렬 계산의 출발점: 작업 배정',GREEN);self.pulse(self.dg)
