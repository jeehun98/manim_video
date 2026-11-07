"""Four-bit registers, input selection and non-destructive datapath reads."""
import os,json,textwrap
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
R=Path(__file__).resolve().parent;VERT=os.getenv('GPUI_LAYOUT','longform')=='shorts'
config.frame_width=9 if VERT else 16;config.frame_height=16 if VERT else 9;config.background_color='#0B1020'
INK='#F8FAFC';BLUE='#60A5FA';PURPLE='#A78BFA';GREEN='#34D399';GRAY='#64748B';ORANGE='#F59E0B';EDGE='#29374D';PANEL='#142037'
TIMING=json.loads((R/'timing.json').read_text(encoding='utf-8'));MANIFEST=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
def txt(s,size=29,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m
def pill(s,w=2,h=.65,color=INK,size=25):return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,stroke_color=color,stroke_width=1.3,fill_color=PANEL,fill_opacity=1),txt(s,size,color,w-.22))
def ln(a,b,c=GRAY,w=2.3):return Line([*a,0],[*b,0],color=c,stroke_width=w)
def route(*pts,c=GRAY,w=2):return VMobject(color=c,stroke_width=w).set_points_as_corners([np.array([*p,0]) for p in pts])
def label_update(m,s,c=INK):
 if getattr(m,'_word',None)!=s:
  new=txt(s,26,c);new.scale_to_fit_height(m.height);new.move_to(m);m.become(new);m._word=s
 return m
def setlabel(m,s,color=INK,size=27,width=None):
 key=(s,str(color))
 if getattr(m,'_labelkey',None)==key:return m
 pos=m.get_center();oldh=m.height;oldw=m.width;new=txt(s,size,color)
 new.scale_to_fit_height(oldh)
 limit=width if width else max(oldw*1.5,.6)
 if new.width>limit:new.scale_to_fit_width(limit)
 m.become(new.move_to(pos));m._labelkey=key;return m




INITIAL={1:5,2:3,3:0,4:9,5:2,6:0}
A=dict(op='ADD',src=(1,2),dest=3,owner='A')
B=dict(op='SUB',src=(4,5),dest=6,owner='B')
def alu(op,a,b):return a+b if op=='ADD' else a-b if op=='SUB' else None
def execute(regs,commands,read_ports=4,units=2):
 snapshot=dict(regs);results=[];reads=0
 for cmd in commands[:units]:
  if reads+len(cmd['src'])>read_ports:break
  reads+=len(cmd['src']);a,b=(snapshot[r] for r in cmd['src']);results.append(dict(value=alu(cmd['op'],a,b),dest=cmd['dest'],owner=cmd['owner'],valid=True))
 return results
def write_edge(regs,results,ports=2):
 chosen=[r for r in results if r['valid']][:ports]
 assert len({r['dest'] for r in chosen})==len(chosen)
 nextregs=dict(regs)
 for r in chosen:nextregs[r['dest']]=r['value']
 return nextregs,[r for r in results if r not in chosen]
def independent(a,b):
 return a['dest'] not in b['src'] and b['dest'] not in a['src'] and a['dest']!=b['dest']
def validate():
 assert independent(A,B)
 assert not independent(A,dict(op='SUB',src=(3,5),dest=4,owner='B'))
 assert independent(A,dict(op='SUB',src=(1,2),dest=6,owner='B')) # shared reads alone aren't a RAW dependency
 assert alu('ADD',5,3)==8 and alu('SUB',9,2)==7
 assert alu('SUB',5,3)==2 and alu('ADD',9,2)==11 # both units support either operation
 result=execute(INITIAL,[A,B]);assert [(r['dest'],r['value']) for r in result]==[(3,8),(6,7)]
 regs,left=write_edge(INITIAL,result);assert regs[3]==8 and regs[6]==7 and not left
 assert all(regs[i]==INITIAL[i] for i in [1,2,4,5])
 regs1,left=write_edge(INITIAL,result,1);assert regs1[3]==8 and regs1[6]==0 and left[0]['dest']==6
 regs2,left=write_edge(regs1,left,1);assert regs2==regs and not left
 assert len(execute(INITIAL,[A,B],2,2))==1
 assert len(execute(INITIAL,[A,B],4,1))==1
 for commands in [[A,B],[B,A]]:
  state=dict(INITIAL)
  for c in commands:state,_=write_edge(state,execute(state,[c]),1)
  assert state==regs
 return True


class DualMemory(VGroup):
 def __init__(self,both=False):
  super().__init__();self.im=pill('현재 인출 없음',5.5,1.1,GRAY,29);self.dm=pill('A : [100] → 5',5.5,1.1,BLUE,32)
  if VERT:self.im.move_to([0,2.0,0]);self.dm.move_to([0,-1.8,0])
  else:self.im.move_to([-3.5,0,0]);self.dm.move_to([3.5,0,0])
  self.il=txt('명령어 메모리',29,INK).next_to(self.im,UP,buff=.3);self.dl=txt('데이터 메모리',29,INK).next_to(self.dm,UP,buff=.3)
  self.ia=pill('명령어 주소 PC = 1',4.3,.65,ORANGE,25).next_to(self.im,DOWN,buff=.6);self.da=pill('데이터 주소 = 100',4.3,.65,ORANGE,25).next_to(self.dm,DOWN,buff=.6)
  self.iln=Line(self.ia.get_top(),self.im.get_bottom(),color=GRAY);self.dln=Line(self.da.get_top(),self.dm.get_bottom(),color=BLUE)
  self.add(self.im,self.dm,self.il,self.dl,self.ia,self.da,self.iln,self.dln)
  if both:self.concurrent()
 def concurrent(self):
  value(self.im,'B : LOAD R2, [101]',PURPLE);self.im[0].set_stroke(PURPLE,width=3);self.iln.set_stroke(PURPLE,width=3);self.dm[0].set_stroke(BLUE,width=3)

class FiveStage(VGroup):
 def __init__(self):
  super().__init__();self.stages=[]
  labels=['IF · 명령어 인출','ID · 해독/읽기','EX · ALU','MEM · 데이터 읽기','WB · 결과 기록']
  for i,l in enumerate(labels):
   xy=(-1.2,3.2-i*1.6) if VERT else (-5.6+i*2.8,.3)
   b=pill('—',3.7 if VERT else 2.5,.9,GRAY,27).move_to([*xy,0]);lab=txt(l,22,INK,b.width).next_to(b,UP,buff=.12);self.stages.append(b);self.add(b,lab)
  for a,b in zip(self.stages,self.stages[1:]):self.add(Line(a.get_bottom() if VERT else a.get_right(),b.get_top() if VERT else b.get_left(),color=GRAY).set_z_index(-1))
  self.pc=pill('PC = 2',3,.65,ORANGE,25).move_to([2.4,3.2,0] if VERT else [-4.2,1.9,0]);self.ctrl=pill('제어 비교',3,.7,GREEN,25).move_to([2.4,0,0] if VERT else [0,1.9,0]);self.add(self.pc,self.ctrl)
 def phase(self,stall=False):
  for b in self.stages:value(b,'—',GRAY);b[0].set_stroke(GRAY,width=1)
  for i,who,s in ([(1,'B','ID 유지'),(2,'','BUBBLE'),(3,'A','LOAD · [100]')] if stall else [(1,'B','ADD R3,R1,R2'),(2,'A','LOAD 주소100')]):
   c=BLUE if who=='A' else PURPLE if who=='B' else ORANGE;value(self.stages[i],who+' · '+s if who else s,c);self.stages[i][0].set_stroke(c,width=2.5)
  value(self.pc,'PC 유지' if stall else 'PC = 2',ORANGE);value(self.ctrl,'IF/ID 유지' if stall else '검사: R1 필요',GREEN)
 def completed(self):
  value(self.stages[1],'—',GRAY);value(self.stages[2],'B · 5 + 3 = 8',PURPLE);value(self.stages[3],'BUBBLE',ORANGE);value(self.stages[4],'A · R1 ← 5',BLUE);value(self.pc,'PC 진행',GREEN);value(self.ctrl,'MEM/WB → EX',GREEN)

class ForwardUnit(VGroup):
 def __init__(self,showpath=False,mux=False,load=False):
  super().__init__();self.load=load
  pos={'reg':(-2,2.8),'saved':(2,2.8),'mux':(0,.7),'alu':(0,-1.3),'other':(-2.8,-1.3),'out':(2.8,-1.3)} if VERT else {'reg':(-4.4,1.2),'saved':(-4.4,-1.1),'mux':(-.9,0),'alu':(2.3,0),'other':(2.3,-1.8),'out':(5.5,0)}
  texts={'reg':'R1 = 0' if load else 'R3 = 0','saved':'데이터 미도착' if load else '결과 8','mux':'선택 전','alu':'계산 대기','other':'R2 = 3' if load else 'R5 = 2','out':'결과 —'}
  labels={'reg':'레지스터 파일','saved':'MEM/WB' if load else 'EX/MEM','mux':'입력 선택','alu':'ALU · 한 개','other':'다른 입력','out':'R3에 기록할 값' if load else 'R4에 기록할 값'}
  self.boxes={};self.labels={}
  for k,xy in pos.items():
   c=BLUE if k=='saved' else GREEN if k=='mux' else PURPLE if k=='out' else GRAY
   w=(3.5 if k in ['reg','saved'] else 2.2) if VERT else (3.2 if k in ['reg','saved'] else 2.35)
   b=pill(texts[k],w,.8,c,26).move_to([*xy,0]);lab=txt(labels[k],21,INK,w).next_to(b,UP,buff=.15);self.boxes[k]=b;self.labels[k]=lab;self.add(b,lab)
  def connect(a,b,color):
   u,v=self.boxes[a],self.boxes[b]
   if VERT and a in ['reg','saved']:st=u.get_bottom();en=v.get_top()+(LEFT if a=='reg' else RIGHT)*.45;mid=np.array([st[0],en[1]+.2,0]);return VMobject(stroke_color=color,stroke_width=2).set_points_as_corners([st,mid,en])
   st=u.get_right();en=v.get_left()+(UP if a=='reg' else DOWN)*.2;mid=np.array([en[0]-.25,st[1],0]);return VMobject(stroke_color=color,stroke_width=2).set_points_as_corners([st,mid,en])
  self.regpath=connect('reg','mux',GRAY);self.forwardpath=connect('saved','mux',GREEN);self.outputpath=connect('alu','out',PURPLE);self.muxpath=Line(self.boxes['mux'].get_bottom() if VERT else self.boxes['mux'].get_right(),self.boxes['alu'].get_top() if VERT else self.boxes['alu'].get_left(),color=GRAY);self.otherpath=Line(self.boxes['other'].get_right() if VERT else self.boxes['other'].get_top(),self.boxes['alu'].get_left() if VERT else self.boxes['alu'].get_bottom(),color=GRAY)
  self.add(self.regpath,self.forwardpath,self.outputpath,self.muxpath,self.otherpath)
  for l in [self.regpath,self.forwardpath,self.outputpath,self.muxpath,self.otherpath]:l.set_z_index(-1)
  if not showpath:self.forwardpath.set_stroke(opacity=0)
  if not mux:self.boxes['mux'].set_opacity(0);self.labels['mux'].set_opacity(0)
 def path(self):self.forwardpath.set_stroke(GREEN,width=3,opacity=1)
 def reveal_mux(self):
  b=self.boxes['mux'];b[0].set_stroke(GREEN,opacity=1);b[0].set_fill(PANEL,opacity=1);b[1].set_opacity(1);self.labels['mux'].set_opacity(1)
 def select(self,ready=True):
  self.reveal_mux();self.path()
  if not ready:
   value(self.boxes['mux'],'선택 보류',ORANGE);value(self.boxes['alu'],'필요한 값 대기',ORANGE);value(self.boxes['out'],'쓰기 없음',GRAY);return
  num=5 if self.load else 8;other=3 if self.load else 2;result=num+other if self.load else num-other
  value(self.boxes['saved'],f'데이터 {num}' if self.load else f'결과 {num}',BLUE);value(self.boxes['mux'],str(num),GREEN);value(self.boxes['alu'],f'{num} + {other}' if self.load else f'{num} − {other}',PURPLE);value(self.boxes['out'],str(result),PURPLE);self.muxpath.set_stroke(GREEN,width=3)

def value(box,s,color=INK):
 t=txt(s,27,color);t.scale_to_fit_height(box[0].height*(.035 if s.strip()=='—' else .42))
 if t.width>box[0].width*.9:t.scale_to_fit_width(box[0].width*.9)
 box[1].become(t.move_to(box[0]))

class DualPath(VGroup):
 def __init__(self,reads=2,writes=1,connected=False,outputs=False):
  super().__init__();self.state=dict(INITIAL);self.results=[];self.ports=[];self.inputs=[];self.controls=[];self.alus=[];self.buffers=[];self.writeports=[];self.wires=[];self.outwires=[];self.labels=[]
  self.rf=pill('R1=5  R2=3  R4=9  R5=2' if VERT else 'R1=5 · R2=3\nR4=9 · R5=2',7.4 if VERT else 3.3,.85 if VERT else 2.6,BLUE,28).move_to([0,3.7,0] if VERT else [-5.8,0,0]);self.add(self.rf,txt('Register File',24,INK).next_to(self.rf,UP,buff=.2))
  for i,(r,v) in enumerate([(1,5),(2,3),(4,9),(5,2)]):
   xy=(-2.7+i*1.8,2.5) if VERT else (-3.1,1.4-i*.9)
   b=pill(f'R{r}:{v}',1.6 if VERT else 1.7,.6,BLUE if i<2 else GREEN,24).move_to([*xy,0]);self.ports.append(b);self.add(b)
   line=Line(self.rf.get_bottom() if VERT else self.rf.get_right(),b.get_top() if VERT else b.get_left(),color=GRAY,stroke_width=1.5);self.add(line.set_z_index(-1));self.inputs.append(line)
  for i in range(2):
   c=BLUE if i==0 else PURPLE;x=-2 if i==0 else 2
   control=pill('Operation ?',3.4 if VERT else 2.9,.6,ORANGE,25).move_to([x,1.3,0] if VERT else [.3,2 if i==0 else -1,0])
   alub=pill('ADD / SUB',3.4 if VERT else 2.9,.9,GREEN if i else BLUE,30).move_to([x,0,0] if VERT else [.3,1 if i==0 else -2,0]);label=txt(f'ALU {i} · ADD/SUB',21,INK,3.4).next_to(alub,UP if VERT else DOWN,buff=.12)
   buf=pill('—',3.4 if VERT else 2.8,.8,GREEN,27).move_to([x,-1.5,0] if VERT else [3.55,1 if i==0 else -2,0]);bl=txt(f'Result {i} · 목적지 보관',20,GREEN,3.2).next_to(buf,UP,buff=.12)
   wp=pill(f'Write {i}',3.4 if VERT else 2.4,.65,BLUE if i==0 else GREEN,25).move_to([x,-2.8,0] if VERT else [6.4,1 if i==0 else -2,0])
   self.controls.append(control);self.alus.append(alub);self.buffers.append(buf);self.writeports.append(wp);self.labels.extend([label,bl]);self.add(control,alub,label,buf,bl,wp)
   for port in self.ports[i*2:i*2+2]:
    st=port.get_bottom() if VERT else port.get_right();en=alub.get_top()+(LEFT if port is self.ports[i*2] else RIGHT)*.5 if VERT else alub.get_left()+(UP if port is self.ports[i*2] else DOWN)*.2
    path=VMobject(stroke_color=c,stroke_width=2).set_points_as_corners([st,np.array([st[0],en[1]+.2,0]) if VERT else np.array([en[0]-.2,st[1],0]),en]);self.wires.append(path);self.add(path.set_z_index(-1))
   ctl=Line(control.get_bottom(),alub.get_top(),color=ORANGE,stroke_width=2);self.add(ctl.set_z_index(-1));self.wires.append(ctl)
   out=Line(alub.get_bottom() if VERT else alub.get_right(),buf.get_top() if VERT else buf.get_left(),color=c,stroke_width=2);write=Line(buf.get_bottom() if VERT else buf.get_right(),wp.get_top() if VERT else wp.get_left(),color=c,stroke_width=2);self.add(out.set_z_index(-1),write.set_z_index(-1));self.outwires.extend([out,write])
   if not outputs:buf.set_opacity(0);bl.set_opacity(0);out.set_stroke(opacity=0);write.set_stroke(opacity=0);wp.set_opacity(0)
  self.summary=pill('R3 = 0   ·   R6 = 0',7.4 if VERT else 6.5,.65,GRAY,27).move_to([0,-4,0] if VERT else [1.9,-3.25,0]);self.add(self.summary)
  self.outputs=outputs;self.set_reads(reads);self.set_writes(writes)
  if not connected:
   for l in self.wires:l.set_stroke(opacity=0)
   for l in self.inputs:l.set_stroke(opacity=0)
  else:self.connect(reads)
 def set_reads(self,n):
  self.read_count=n
  for i,(b,l) in enumerate(zip(self.ports,self.inputs)):
   b[0].set_stroke(opacity=1 if i<n else 0);b[0].set_fill(opacity=1 if i<n else 0);b[1].set_opacity(1 if i<n else 0);l.set_stroke(opacity=1 if i<n else 0)
 def connect(self,reads=4):
  self.set_reads(reads)
  for i,l in enumerate(self.wires):
   lane=i//3;l.set_stroke(opacity=1 if lane==0 or reads>=4 else 0)
  value(self.controls[0],'ADD',ORANGE);value(self.controls[1],'SUB',ORANGE)
 def expose_outputs(self):
  self.outputs=True
  for b in self.buffers:b[0].set_stroke(opacity=1);b[0].set_fill(PANEL,opacity=1);b[1].set_opacity(1)
  for label in [self.labels[1],self.labels[3]]:label.set_opacity(1)
  for l in self.outwires:l.set_stroke(opacity=1)
  self.set_writes(self.write_count)
 def set_writes(self,n):
  self.write_count=n
  for i,b in enumerate(self.writeports):
   active=self.outputs and i<n;b[0].set_stroke(opacity=1 if active else 0);b[0].set_fill(PANEL,opacity=1 if active else 0);b[1].set_opacity(1 if active else 0)
   self.outwires[i*2+1].set_stroke(opacity=1 if active else 0)
 def compute(self):
  self.results=execute(self.state,[A,B],self.read_count)
  for i,b in enumerate(self.alus):
   c=BLUE if i==0 else PURPLE
   if i<len(self.results):value(b,'5 + 3 = 8' if i==0 else '9 − 2 = 7',c)
   else:value(b,'입력 대기',ORANGE)
 def capture(self):
  self.expose_outputs()
  for i,b in enumerate(self.buffers):
   if i<len(self.results):r=self.results[i];value(b,f'{r["value"]} · 목적지 R{r["dest"]}',BLUE if i==0 else PURPLE)
   else:value(b,'—',GRAY)
 def write_edge(self):
  self.state,self.results=write_edge(self.state,self.results,self.write_count);value(self.summary,f'R3 = {self.state[3]}   ·   R6 = {self.state[6]}',GREEN)
  for i,b in enumerate(self.writeports):
   if i<self.write_count:value(b,'CLK ↑ · R3' if i==0 else 'CLK ↑ · R6',BLUE if i==0 else PURPLE)
