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
class StyleScene(Scene):
    def to(self,t):
        rem=t-self.start-self.time
        if rem<-.04:raise RuntimeError(f'{self.INDEX}: {self.time} exceeds {t-self.start}')
        if rem>.001:self.wait(rem)
    def place(self,g,center,w,h):
        scale=min(w/max(g.width,.001),h/max(g.height,.001),1.25);g.scale(scale).move_to(center)
        self.bounds.append(dict(time=self.start+self.time,left=float(g.get_left()[0]),right=float(g.get_right()[0]),bottom=float(g.get_bottom()[1]),top=float(g.get_top()[1])))
        assert g.get_left()[0]>-config.frame_width/2+.2 and g.get_right()[0]<config.frame_width/2-.2
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
