import json
from pathlib import Path
from manim import *
from shared_style import *
P=Path(__file__).resolve().parent
GOLD='#F4C96B';TEAL='#48DED0'
CODE=['float x = A[i];','B[i] = x * 2.0f;']
class DramBase(StyleScene):
 INDEX=0
 def construct(self):
  self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start'];self.bounds=[];self.trace=[];self.sc=1 if SHORT else .87
  self.dc=np.array([0,1.08,0]) if SHORT else np.array([-3.65,-1.07,0]);self.dw=7.65 if SHORT else 7.1;self.dh=3.2 if SHORT else 2.65
  self.cc=np.array([0,-2.85,0]) if SHORT else np.array([4.15,.1,0]);self.cw=7.65 if SHORT else 6.15;self.ch=4.05 if SHORT else 4.7
  self.add(text('GPU HIERARCHY / LEVEL 10',19,MUTED).move_to([0,7.35 if SHORT else 4,0]),text(self.meta['title'],32,width=8 if SHORT else 14).move_to([0,6.45 if SHORT else 3.2,0]))
  self.world();self.code();self.note('Global은 주소 공간 · Controller와 DRAM은 물리 하드웨어')
  self.shot();self.to(self.meta['end'])
  layout='shorts' if SHORT else 'longform'
  for name,data in [('geometry',self.bounds),('states',self.trace)]: (P/f'{name}_{layout}_{self.INDEX:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 def code(self,active=(),lines=None,label='readData.cu · 핵심 발췌'):super().code(active,CODE if lines is None else lines,label)
 def world(self):
  outer=RoundedRectangle(width=7.65,height=2.5,corner_radius=.14,color=GOLD,fill_color=PANEL,fill_opacity=.4)
  chip=RoundedRectangle(width=5.5,height=1.65,corner_radius=.1,color=BLUE).move_to([-1,-.08,0]);sm=RoundedRectangle(width=2.45,height=1.08,corner_radius=.08,color=BLUE).move_to([-2.34,-.18,0])
  self.warp=box('Warp 0',1,.3,BLUE,15).move_to([-2.92,.02,0]);self.reg=box('Register',1,.3,PURPLE,15).move_to([-1.76,.02,0]);self.shared=box('Shared',1,.3,TEAL,15).move_to([-2.92,-.4,0]);self.l1=box('L1',1,.3,PURPLE,15).move_to([-1.76,-.4,0])
  self.sms=VGroup(*(box(f'SM {i}',.65,.28,BLUE,12).move_to([-.65,.36-(i-1)*.4,0]) for i in range(1,4)))
  self.l2=box('L2',.64,.45,PURPLE,18).move_to([.14,-.2,0]);self.mc=box('MC',.82,.69,ORANGE,22).move_to([1.04,-.2,0]);self.dram=box('DRAM',1.45,1.13,GOLD,20).move_to([2.75,-.18,0])
  self.logical=text('Global Memory: A[5] · 논리 주소 공간',15,GOLD).move_to([0,.99,0]);self.footer=text('GPU 다이와 DRAM 구분 · 실제 채널·컨트롤러 수와 배치는 다름',13,MUTED,width=7.1).move_to([0,-1.05,0])
  links=VGroup(DashedLine(self.l1.get_right(),self.l2.get_left(),color=MUTED,stroke_width=1),Line(self.l2.get_right(),self.mc.get_left(),color=ORANGE,stroke_width=1),Line(self.mc.get_right(),self.dram.get_left(),color=GOLD,stroke_width=1))
  self.map=VGroup(outer,chip,sm,links,self.warp,self.reg,self.shared,self.l1,self.sms,self.l2,self.mc,self.dram,self.logical,text('GPU CHIP',15,BLUE).move_to([-2.9,.63,0]),text('SM 0',12,BLUE).move_to([-3.05,.27,0]),text('Controller',12,ORANGE).move_to([1.02,.32,0]),text('Device DRAM',14,GOLD).move_to([2.72,.59,0]),self.footer)
  self.map.scale(self.sc).move_to([0,4.4,0] if SHORT else [-3.65,1.45,0]);self.add(self.map)
 def msg(self,s,col=GOLD):self.footer.become(text(s,13,col,width=7.1*self.sc).move_to(self.footer))
 def detail(self,g):
  self.place(g,self.dc,self.dw,self.dh)
  if hasattr(self,'dg'):self.play(ReplacementTransform(self.dg,g),run_time=.4)
  else:self.add(g)
  self.dg=g;return g
 def cards(self,title,labels,col=GOLD):return stack(text(title,27,col,width=7.3),VGroup(*(box(s,1.75,.68,col,22) for s in labels)).arrange(RIGHT,buff=.2))
 def flow(self,value,nodes,col=GOLD,label='데이터 이동'):
  self.msg(label,col);packet=box(str(value),.55*self.sc,.31*self.sc,col,17*self.sc).move_to(nodes[0]);packet[0].set_fill(PANEL,opacity=1);packet[1].set_color(INK);self.add(packet)
  for n in nodes[1:]:self.play(packet.animate.move_to(n),Indicate(n,color=col,scale_factor=1.04),run_time=.3)
  self.play(FadeOut(packet),run_time=.1);self.trace.append(dict(time=round(self.start+self.time,3),kind='flow',value=value,label=label))
 def logical_physical(self):
  a=stack(text('Global Memory',29,GOLD),box('A[0] · A[1] · … · A[5]',3.25,.68,GOLD,22),text('CUDA의 논리 주소 공간',21,MUTED),buff=.2)
  b=stack(text('Device DRAM',29,GOLD),box('Bank / Row / Column',3.25,.68,GOLD,22),text('데이터를 저장하는 물리 장치',21,MUTED),buff=.2)
  return VGroup(a,b).arrange(RIGHT,buff=.5)
 def bank_view(self,active=None):
  from dram_model import BankModel
  self.bankmodel=BankModel(active);self.cells=VGroup();self.rowlabels=VGroup();self.colheads=VGroup()
  for c in range(8):self.colheads.add(text(f'C{c}',14,MUTED).move_to([-.0+(c-3.5)*.65,.96,0]))
  for r in range(4):
   row=VGroup(*(box('',.56,.3,GOLD,15,fill=.04).move_to([(c-3.5)*.65,.62-r*.39,0]) for c in range(8)));self.cells.add(row);self.rowlabels.add(text(f'R{r}',16,MUTED).move_to([-3.04,.62-r*.39,0]))
  self.buffer=box('Row Buffer: 닫힘' if active is None else f'Row Buffer: R{active} 활성',5.6,.4,ORANGE,21).move_to([0,-1.12,0]);self.command=text('대기' if active is None else '열린 Row 접근 준비',22,ORANGE).move_to([0,-1.63,0])
  g=VGroup(text('DRAM Bank 0 · Row / Column',25,GOLD).move_to([0,1.36,0]),self.colheads,self.cells,self.rowlabels,self.buffer,self.command,text('4×8 설명용 모형 · 실제 A[i] 주소 매핑 아님',17,MUTED).move_to([0,-2.03,0]));self.detail(g)
  if active is not None:
   for cell in self.cells[active]:cell[0].set_fill(GOLD,opacity=.3)
 def set_active(self,row):
  anim=[]
  for r,cells in enumerate(self.cells):
   for cell in cells:anim.append(cell[0].animate.set_fill(GOLD,opacity=.3 if r==row else .04))
  label='Row Buffer: 닫힘' if row is None else f'Row Buffer: R{row} 활성'
  target=text(label,19,ORANGE,width=self.buffer.width-.15).move_to(self.buffer[1]);self.play(*anim,Transform(self.buffer[1],target),run_time=.3)
 def bank_read(self,row,col):
  e=self.bankmodel.read(row,col)
  for cmd in e['commands']:
   target=text(cmd+(f' R{row}' if cmd=='ACTIVATE' else f' C{col}' if cmd=='READ' else ''),22,ORANGE,width=self.dw-.5).move_to(self.command)
   self.play(Transform(self.command,target),run_time=.2);self.flow(cmd,[self.mc,self.dram],ORANGE,'설명용 DRAM 명령: '+cmd)
   if cmd=='PRECHARGE':self.set_active(None)
   elif cmd=='ACTIVATE':self.set_active(row)
   else:
    self.play(Indicate(self.cells[row][col],color=GREEN,scale_factor=1.12),run_time=.3)
    p=box(str(e['value']),.45,.28,GREEN,17).move_to(self.buffer);p[0].set_fill(PANEL,opacity=1);self.add(p);self.play(p.animate.move_to(self.dram),run_time=.35);self.play(FadeOut(p),run_time=.1)
  self.trace.append(dict(kind='bank_read',time=round(self.start+self.time,3),read_value_source='Row Buffer',**e));self.msg('Bank 0 · 열린 Row는 하나 · 명령 순서의 개념 모형')
 def banks_overview(self):
  banks=VGroup()
  for b in range(4):
   grid=VGroup(*(Rectangle(width=.23,height=.13,stroke_width=.5,stroke_color=GOLD,fill_color=GOLD,fill_opacity=.05) for _ in range(32))).arrange_in_grid(rows=4,buff=.035)
   banks.add(stack(text(f'Bank {b}',19,GOLD),grid,buff=.12))
  banks.arrange_in_grid(rows=2,buff=(.5,.35));return stack(text('DRAM 내부 · 여러 Bank',27,GOLD),banks,text('각 Bank 안에 Row와 Column',21,MUTED),buff=.18)
 def gddr(self):
  board=RoundedRectangle(width=6.7,height=2.1,corner_radius=.1,color=TEAL,fill_color=TEAL,fill_opacity=.07);gpu=box('GPU',1.7,.9,BLUE,27).move_to(board)
  chips=VGroup(*(box('GDDR',1,.42,GOLD,16).move_to([x,y,0]) for x,y in [(-2.35,.6),(-2.35,-.6),(2.35,.6),(2.35,-.6)]))
  wires=VGroup(*(Line(gpu.get_center()+RIGHT*(.85 if c.get_x()>0 else -.85),c.get_center(),color=GOLD,stroke_width=2) for c in chips))
  g=stack(text('GDDR · 그래픽카드 기판의 개념 배치',26,GOLD),VGroup(board,wires,gpu,chips),text('GPU 주변의 개별 메모리 칩 · 고속 인터페이스',21,MUTED),buff=.17);self.detail(g);self.packgpu=gpu;self.packchips=chips;self.packwires=wires
  self.trace.append(dict(kind='packaging',technology='GDDR',diagram='board',memory_on_gpu_die=False,performance_ranking=False))
 def hbm(self):
  base=Polygon([-3.25,-.65,0],[2.7,-.65,0],[3.25,-.15,0],[-2.7,-.15,0],color=TEAL,fill_color=TEAL,fill_opacity=.15)
  gpu=box('GPU die',2.15,.7,BLUE,25).move_to([-1.65,.12,0]);layers=VGroup(*(Polygon([.35,-.15+k*.18,0],[2.25,-.15+k*.18,0],[2.6,.15+k*.18,0],[.7,.15+k*.18,0],stroke_color=GOLD,stroke_width=1.5,fill_color=GOLD,fill_opacity=.18) for k in range(4)))
  links=VGroup(*(Line([-.55,-.28+j*.035,0],[.45,-.28+j*.035,0],color=GOLD,stroke_width=1.4) for j in range(8)))
  labels=VGroup(text('HBM stack',21,GOLD).move_to([1.45,1.04,0]),text('Interposer / Package · 개념도',17,TEAL).move_to([0,-.9,0]))
  g=stack(text('HBM · 수직 적층 DRAM + 넓은 인터페이스',26,GOLD,width=7.3),VGroup(base,gpu,layers,links,labels),text('GPU 다이 옆의 스택 · 같은 패키지에 배치 가능',21,MUTED),buff=.17);self.detail(g);self.hbmlayers=layers;self.hbmlinks=links
  self.trace.append(dict(kind='packaging',technology='HBM',diagram='same_package_example',memory_on_gpu_die=False,stacked_dram=True,wide_interface=True,performance_ranking=False))
 def shot(self):
  i=self.INDEX
  if i==0:
   self.detail(self.cards('GPU 전체에서 접근하는 Global 공간',['SM 0','SM 1','배열 A']));self.flow('A[5]',[self.warp,self.l2],ORANGE,'SM 0의 Global 주소 요청');self.to(5);self.detail(self.logical_physical());self.to(10);self.play(Indicate(self.logical,color=GOLD),Indicate(self.dram,color=GOLD),run_time=.8);self.msg('논리적 메모리 공간 ≠ 물리적 저장 장치')
  elif i==1:
   self.detail(self.logical_physical());self.note('주소 변환·물리 배치 결정은 메모리 시스템에 걸친 과정 · 실제 주소 매핑 생략');self.to(17);self.flow('A[5]',[self.warp,self.l2,self.mc,self.dram],ORANGE,'논리 주소 → 주소 변환을 포함한 메모리 시스템 → 물리 저장');self.to(21);self.msg('A[5]가 곧바로 특정 Bank·Row·Column 번호인 것은 아님')
  elif i==2:
   self.detail(self.cards('SM 요청은 메모리 시스템에서 처리',['SM','Cache','Controller']));self.flow('요청',[self.warp,self.l1,self.l2],ORANGE,'SM의 요청이 캐시 계층으로');self.to(28);self.play(Indicate(self.map,color=BLUE,scale_factor=1.01),run_time=.6);self.to(30);self.flow('요청',[self.sms[0],self.l2],ORANGE,'여러 SM에서 발생하는 메모리 요청');self.to(35);self.detail(self.cards('이 사례는 두 캐시 모두 Miss',['L1 Miss','L2 Miss'],ORANGE));self.flow('요청',[self.l2,self.mc],ORANGE,'캐시에 데이터가 없어 DRAM 접근이 필요한 상황 가정')
  elif i==3:
   self.detail(self.cards('Memory Controller',['Read','Write','Timing'],ORANGE));self.play(Indicate(self.mc,color=ORANGE),run_time=.7);self.to(45);self.flow('READ',[self.mc,self.dram],ORANGE,'DRAM 읽기 요청 조정');self.to(47);self.flow('WRITE',[self.mc,self.dram],ORANGE,'DRAM 쓰기 요청 조정 · 별도 기능 설명');self.to(49);self.msg('명령과 DRAM 타이밍 제약을 고려 · 발생 순서 실행을 보장하지 않음',ORANGE);self.note('컨트롤러 수·요청 처리 순서·타이밍은 하드웨어에 따라 달라짐')
  elif i==4:
   self.detail(self.cards('Thread 5 · A[5]를 읽는다',['A[5]','값 6']));self.code([0]);self.to(53);self.play(Indicate(self.warp,color=BLUE),run_time=.6);self.to(58);self.detail(self.cards('Cache Miss를 가정한 Load',['L1 Miss','L2 Miss'],ORANGE));self.flow('A[5]',[self.warp,self.l1,self.l2],ORANGE,'캐시 Miss 가정 · 실제 GPU 캐시 상태 측정 아님');self.trace.append(dict(kind='load_request',address='A[5]',cache_miss_assumed=True,measured=False))
  elif i==5:
   self.detail(self.cards('메모리 시스템 → Controller → DRAM',['A[5]','MC','DRAM'],ORANGE));self.code([0]);self.flow('A[5]',[self.l2,self.mc],ORANGE,'L2 아래 메모리 시스템을 통해 컨트롤러로 전달');self.to(67);self.flow('READ',[self.mc,self.dram],ORANGE,'컨트롤러가 필요한 DRAM 읽기 명령 처리');self.trace.append(dict(kind='controller_request',request='A[5]',role='DRAM read/write and timing',virtual_translation_only_here=False));self.note('CUDA Load 하나와 DRAM 명령 하나가 1:1로 대응하는 것은 아님')
  elif i==6:
   self.detail(self.cards('DRAM의 값이 요청한 SM으로',['값 6','Thread 5']));self.code([0]);self.flow(6,[self.dram,self.mc,self.l2,self.l1,self.reg],GREEN,'DRAM → Controller → 캐시/메모리 시스템 → SM · 값 6');self.trace.append(dict(kind='load_return',value=6,route=['DRAM','Controller','L2','L1','Register'],conceptual=True));self.to(76);self.code([1]);self.detail(self.cards('값이 준비되면 계산 재개',['6 × 2.0f','12'],GREEN));self.play(Indicate(self.reg,color=GREEN),run_time=.7);self.trace.append(dict(kind='compute',input=6,multiplier=2,result=12));self.msg('Thread 5의 계산값 6 × 2 = 12 · 이후 Global Store')
  elif i==7:
   self.detail(self.cards('주소 전달을 넘어 DRAM 동작 제어',['Controller','DRAM'],ORANGE));self.play(Indicate(self.mc,color=ORANGE),run_time=.7);self.to(86);self.detail(self.banks_overview());self.msg('Bank 내부는 Row와 Column으로 구성 · 설명용 모형');self.to(92);self.bank_view();self.note('4 Bank / 4 Row / 8 Column은 구조 설명용 · 실제 칩 크기 아님')
  elif i==8:
   self.bank_view();self.code([],['// Closed bank: ACTIVATE -> READ','// Open same row: READ'],label='DRAM 명령 · 동작 상태 설명');self.note('Row 명령 모형 · 실제 사이클·주소 매핑·프로파일러 추적 아님');self.bank_read(1,2);self.to(100);self.bank_read(1,5);self.msg('Row Buffer Hit · 같은 R1은 유지하고 다른 Column 읽기')
  elif i==9:
   self.bank_view(1);self.code([],['// Different open row:','// PRECHARGE -> ACTIVATE -> READ'],label='DRAM 명령 · 다른 Row 접근');self.note('실제 명령·타이밍은 Bank 상태와 메모리 종류에 따라 다름');self.bank_read(3,2);self.to(110);self.detail(stack(text('같은 데이터 크기 · 달라지는 명령 절차',27,GOLD),text('같은 Row: READ',25,GREEN),text('다른 Row: PRECHARGE → ACTIVATE → READ',23,ORANGE,width=7.2),text('명령 수를 실제 지연시간 배수로 환산하지 않음',20,MUTED)));self.msg('컨트롤러가 DRAM 상태와 타이밍 제약을 고려한다',ORANGE)
  elif i==10:
   self.detail(self.cards('서로 다른 물리적 DRAM 구현',['GDDR','HBM']));self.to(120);self.gddr();self.code([],['// GDDR / HBM: physical DRAM','// packaging and interface differ'],label='구현 구조 · CUDA 메모리 공간은 Global');self.to(124);self.play(LaggedStart(*(Indicate(c,color=GOLD) for c in self.packchips),lag_ratio=.15),run_time=1);self.play(Indicate(self.packwires,color=GOLD),run_time=.7);self.msg('GDDR · GPU 주변 기판의 메모리 칩과 연결')
  elif i==11:
   self.hbm();self.code([],['// GDDR / HBM: physical DRAM','// packaging and interface differ'],label='HBM · 적층과 넓은 인터페이스');self.play(LaggedStart(*(Indicate(l,color=GOLD,scale_factor=1.035) for l in self.hbmlayers),lag_ratio=.2),run_time=1.2);self.to(133);self.play(Indicate(self.hbmlinks,color=GREEN),run_time=.8);self.msg('HBM · 수직 적층 DRAM 다이와 넓은 데이터 인터페이스');self.to(136);self.detail(self.cards('둘 다 Global 데이터를 보관하는 DRAM',['GDDR','HBM']));self.note('구조의 차이 · 단순한 빠름/느림 또는 지연시간 순위가 아님')
  elif i==12:
   self.detail(self.logical_physical());self.code([0]);self.to(144);self.play(Indicate(self.logical,color=GOLD),Indicate(self.dram,color=GOLD),run_time=.8);self.to(149);self.detail(self.cards('Memory Controller · DRAM 접근 제어',['Read','Write','Timing'],ORANGE));self.flow('명령',[self.mc,self.dram],ORANGE,'컨트롤러는 읽기·쓰기와 DRAM 동작을 조정')
  else:
   self.detail(self.cards('SM → Cache → Controller → DRAM',['요청','접근 제어','저장 장치']));self.code([0]);self.flow('A[5]',[self.warp,self.l1,self.l2,self.mc,self.dram],ORANGE,'캐시 Miss를 가정한 단순화된 요청 경로');self.to(157);self.flow(6,[self.dram,self.mc,self.l2,self.l1,self.reg],GREEN,'값은 물리 DRAM에서 메모리 시스템을 거쳐 SM으로');self.to(160);self.detail(stack(text('Memory Controller — DRAM Access Control',27,ORANGE,width=7.3),text('DRAM — Physical Data Storage',27,GOLD),text('Global Memory — Logical Address Space',25,MUTED,width=7.3)));self.play(Indicate(self.mc,color=ORANGE),Indicate(self.dram,color=GOLD),run_time=.8)
