import json
from pathlib import Path
from manim import *
from shared_style import *
P=Path(__file__).resolve().parent
GOLD='#F4C96B';TEAL='#48DED0'
CODE=['int i = blockIdx.x * blockDim.x','      + threadIdx.x;','if (i < N) {','  C[i] = A[i] + B[i]; }']
class IntegratedBase(StyleScene):
 INDEX=0
 def construct(self):
  self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start'];self.bounds=[];self.trace=[]
  self.cc=np.array([4,-1.15,0]);self.cw=6.9;self.ch=2.9;self.dc=np.array([-3.9,-1.15,0]);self.dw=7.3;self.dh=2.6
  self.add(text('GPU HIERARCHY / LEVEL 11 — FINAL',18,MUTED).move_to([0,4,0]),text(self.meta['title'],31,width=14.6).move_to([0,3.35,0]))
  self.world();self.code();self.note('N=512 · Grid=4 Blocks · 128 Threads/Block · 동일 커널의 실행을 추적')
  self.shot();self.to(self.meta['end'])
  for name,data in [('geometry',self.bounds),('states',self.trace)]: (P/f'{name}_longform_{self.INDEX:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 def code(self,active=(),lines=None,label='vectorAdd.cu · 핵심 발췌'):super().code(active,CODE if lines is None else lines,label)
 def note(self,s,col=MUTED):
  if hasattr(self,'ng'):self.remove(self.ng)
  self.ng=text(s,18,col,width=14.7).move_to([0,-2.87,0]);self.add(self.ng)
 def world(self):
  grid=RoundedRectangle(width=2.8,height=1.85,corner_radius=.1,color=MUTED).move_to([-5.9,0,0]);self.blocks=VGroup(*(box(f'Block {b}',1.12,.39,BLUE,17,fill=.2 if b==1 else .07).move_to([-6.5+(b%2)*1.2,.17-(b//2)*.55,0]) for b in range(4)))
  self.chip=RoundedRectangle(width=8,height=1.85,corner_radius=.1,color=BLUE).move_to([-.1,0,0]);self.sm=RoundedRectangle(width=2.9,height=1.35,corner_radius=.07,color=BLUE).move_to([-2.45,-.08,0])
  self.scheduler=box('Scheduler',1.16,.31,PURPLE,17).move_to([-3.1,.17,0]);self.alu=box('ALU',1.16,.31,BLUE,18).move_to([-1.75,.17,0]);self.reg=box('Register',1.16,.31,PURPLE,17).move_to([-3.1,-.27,0]);self.l1=box('L1',1.16,.31,BLUE,18).move_to([-1.75,-.27,0]);self.shared=box('Shared · unused',2.4,.23,MUTED,13,fill=.03).move_to([-2.45,-.63,0]);self.sms=VGroup(*(box(f'SM {k}',.8,.3,BLUE,14).move_to([-.4,.45-i*.45,0]) for i,k in enumerate([0,2,3])))
  self.l2=box('L2',1,.47,BLUE,21).move_to([.92,0,0]);self.mc=box('Controller',1.4,.6,GOLD,18).move_to([2.6,0,0]);self.dram=box('Device DRAM',2.4,1.24,ORANGE,21).move_to([5.5,-.05,0]);self.dramtag=text('물리 저장 장치',14,ORANGE).move_to([5.5,-.47,0])
  links=VGroup(Line(self.l1.get_right(),self.l2.get_left(),color=MUTED,stroke_width=1),Line(self.l2.get_right(),self.mc.get_left(),color=MUTED,stroke_width=1),Line(self.mc.get_right(),self.dram.get_left(),color=MUTED,stroke_width=1))
  self.footer=text('Block 1 / Thread 5 / Warp 0 / Lane 5 · i = 133',14,TEAL).move_to([-.2,-1.06,0])
  self.map=VGroup(grid,self.chip,self.sm,links,self.blocks,self.scheduler,self.alu,self.reg,self.l1,self.shared,self.sms,self.l2,self.mc,self.dram,self.dramtag,text('LOGICAL · Grid',17,MUTED).move_to([-5.9,.65,0]),text('4 × 128 = 512 Threads',14,MUTED).move_to([-5.9,-.74,0]),text('PHYSICAL · GPU CHIP',17,BLUE).move_to([-.1,.68,0]),text('SM 1 · 배치 예시',14,BLUE).move_to([-2.45,.45,0]),text('Global 주소 공간: A / B / C',17,ORANGE).move_to([5.25,.85,0]),self.footer)
  self.map.move_to([0,1.92,0]);self.add(self.map)
  self.trace.append(dict(kind='identity',block=1,thread=5,warp=0,lane=5,i=133,assumed_sm=1,mapping_guaranteed=False,shared_used=False))
 def msg(self,s,col=TEAL):self.footer.become(text(s,14,col,width=10.8).move_to(self.footer))
 def detail(self,g):
  self.place(g,self.dc,self.dw,self.dh)
  if hasattr(self,'dg'):self.play(FadeTransform(self.dg,g),run_time=.35)
  else:self.add(g)
  self.dg=g;return g
 def cards(self,title,labels,col=TEAL):return stack(text(title,26,col,width=7.2),VGroup(*(box(s,1.65,.58,col,21) for s in labels)).arrange(RIGHT,buff=.2))
 def flow(self,value,nodes,col=GREEN,label='값'):
  self.msg(label,col);p=box(str(value),.53,.29,col,16).move_to(nodes[0]);p[0].set_fill(PANEL,opacity=1);p[1].set_color(INK);self.add(p)
  for n in nodes[1:]:self.play(p.animate.move_to(n),Indicate(n,color=col,scale_factor=1.025),run_time=.25)
  self.play(FadeOut(p),run_time=.1);self.trace.append(dict(kind='flow',time=round(self.start+self.time,3),value=value,label=label,shared_in_route=any(n is self.shared for n in nodes)))
 def logical(self):
  self.warps=VGroup()
  for w in range(4):
   cells=VGroup(*(Rectangle(width=.10,height=.13,stroke_width=.5,stroke_color=TEAL,fill_color=TEAL,fill_opacity=.25 if w==0 else .06) for _ in range(32))).arrange_in_grid(rows=2,buff=.035)
   self.warps.add(VGroup(text(f'W{w}',20,PURPLE).next_to(cells,LEFT,buff=.25),cells))
  self.warps.arrange(DOWN,buff=.2);return stack(text('Block 1 · 128 Threads / 4 Warps',25,BLUE),self.warps,text('Warp는 32 Thread의 하드웨어 실행 묶음',20,MUTED),buff=.22)
 def arrays(self):
  rows=VGroup()
  for name,vs,col in [('A',[1,2,3,4],TEAL),('B',[5,6,7,8],ORANGE),('C',['?']*4,GREEN)]:
   cells=VGroup(*(box(str(v),.82,.43,col,23) for v in vs)).arrange(RIGHT,buff=.15);rows.add(VGroup(text(name,24,col).next_to(cells,LEFT,buff=.3),cells))
  rows.arrange(DOWN,buff=.18);self.arrayrows=rows;return stack(text('같은 위치의 원소끼리 덧셈',25,TEAL),rows,buff=.2)
 def selected(self):return self.cards('Block 1 · Thread 5 · i = 133',['A: 4','B: 7','C: 11'])
 def mapping(self):
  self.flow('B1',[self.blocks[1],self.sm],BLUE,'Block 1 → SM 1 · 한 가지 가능한 배치 · 실제 SM 번호 보장 없음');self.trace.append(dict(kind='mapping',block=1,sm=1,assumed=True))
 def issue(self,w):
  self.flow(f'W{w}',[self.scheduler,self.alu],PURPLE,f'준비된 Warp {w}의 명령 발행 · 선택 순서는 설명용');self.trace.append(dict(kind='issue',warp=w,simultaneous_all_warps=False))
 def shot(self):
  i=self.INDEX
  if i==0:
   self.detail(self.cards('One CUDA Kernel → GPU Execution',['조직','실행','데이터']));self.to(4);self.play(Indicate(self.blocks,color=BLUE),run_time=.7);self.to(8);self.play(Indicate(self.reg,color=PURPLE),Indicate(self.l1,color=BLUE),Indicate(self.dram,color=ORANGE),run_time=.8);self.to(13);self.code([3]);self.msg('동일한 벡터 덧셈 코드를 하나의 시스템에서 추적')
  elif i==1:
   self.detail(self.arrays());self.code([0],['C[i] = A[i] + B[i];']);self.to(21)
   for k,v in enumerate([6,8,10,12]):
    a=self.arrayrows[0][1][k];b=self.arrayrows[1][1][k];c=self.arrayrows[2][1][k];n=text(str(v),22,GREEN).move_to(c[1]);self.play(Indicate(a,color=TEAL),Indicate(b,color=ORANGE),Transform(c[1],n),run_time=.6)
   self.msg('A[0..3]+B[0..3] → C[0..3] · 전체 N은 512')
  elif i==2:
   self.code([0,1],['int blockSize = 128;','int gridSize = 4;','vectorAdd<<<4, 128>>>(A,B,C,512);'],label='Kernel Launch · N=512');self.detail(self.cards('하나의 Grid · 네 개 Block',['B0','B1','B2','B3'],BLUE));self.to(29);self.play(LaggedStart(*(Indicate(b,color=BLUE) for b in self.blocks),lag_ratio=.2),run_time=1);self.to(35);self.detail(self.logical());self.play(LaggedStart(*(Indicate(w,color=PURPLE) for w in self.warps),lag_ratio=.25),run_time=1.5);self.note('4 Warps × 32 Threads = 128 Threads/Block · 전체 512 Threads')
  elif i==3:
   self.detail(self.selected());self.code([0,1]);self.play(Indicate(self.blocks[1],color=TEAL),run_time=.7);self.to(46);self.detail(stack(text('i = 1 × 128 + 5 = 133',34,TEAL),text('Warp 0 · Lane 5 · A[133] / B[133] / C[133]',23,MUTED)));self.to(50);self.msg('논리적 작업 구성과 실제 SM은 구분되는 관점');self.note('Warp 크기는 CUDA Launch 인자가 아님 · Block의 Thread들이 32개씩 실행 묶음을 이룸')
  elif i==4:
   self.detail(self.cards('논리적 Block → 물리적 SM',['Block 1','SM 1'],BLUE));self.to(56);self.play(Indicate(self.sm,color=BLUE),Indicate(self.sms,color=BLUE),run_time=.7);self.to(59);self.mapping();self.to(63);self.detail(self.logical());self.issue(0);self.to(67);self.flow('명령',[self.scheduler,self.alu],PURPLE,'Warp Scheduler → SM Execution Units');self.play(Indicate(self.alu,color=GREEN),run_time=.7);self.note('배치·명령 순서·동시성은 설명용 · 한 SM에 여러 Block이 상주할 수도 있음')
  elif i==5:
   self.detail(self.cards('Thread별 계산값을 Register에',['i = 133','중간값'],PURPLE));self.play(Indicate(self.reg,color=PURPLE),run_time=.7);self.to(76);self.detail(stack(text('Shared Memory — Optional',29,MUTED),text('같은 Block의 Thread 협력에 사용 가능',24,GREEN),text('현재 vectorAdd에는 __shared__가 없음',23,ORANGE)));self.play(Indicate(self.shared,color=GREEN),run_time=.7);self.note('이 커널의 Shared 사용량은 0 bytes · Shared로 데이터를 옮기는 경로는 없음')
  elif i==6:
   self.detail(self.selected());self.code([3]);self.to(85);self.play(Indicate(self.dram,color=ORANGE),run_time=.7);self.msg('A[133], B[133], C[133]은 Global 논리 주소 공간의 원소');self.to(89);self.flow('A[133]',[self.alu,self.l1],TEAL,'Thread 5 · A[133]의 값 요청');self.to(92);self.flow('B[133]',[self.alu,self.l1,self.l2],ORANGE,'Thread 5 · B[133]의 값 요청 · 실제 경로는 캐시 상태/정책에 따라 다름')
  elif i==7:
   self.detail(self.selected());self.code([3]);self.note('캐시 상태는 가정 사례 · A/B 외의 새로운 세 번째 Load가 아님');self.flow(4,[self.l1,self.reg],TEAL,'가정 1 · A[133]은 L1 적중 · 값 4');self.flow(7,[self.l2,self.l1,self.reg],ORANGE,'가정 1 · B[133]은 L2 적중 · 값 7');self.to(100);self.detail(self.cards('같은 B Load의 다른 가능한 상황',['B[133]','Cache Miss'],ORANGE));self.flow('B[133]',[self.l2,self.mc,self.dram],ORANGE,'가정 2 · 같은 B[133] Load가 캐시에 없는 대안 사례');self.flow(7,[self.dram,self.mc,self.l2,self.l1,self.reg],GREEN,'가정 2 · DRAM에서 같은 값 7 반환');self.trace.append(dict(kind='load_cases',inputs=['A[133]','B[133]'],third_load=False,A=4,B=7,alternative='same B load via DRAM'))
  elif i==8:
   self.detail(self.cards('값이 준비된 Thread의 계산',['4 + 7','11'],GREEN));self.code([3]);self.flow('4+7',[self.reg,self.alu],GREEN,'Thread 5 · SM ALU에서 4 + 7');self.flow(11,[self.alu,self.reg],GREEN,'C[133]에 저장할 결과 11');self.to(109);self.detail(self.selected());self.to(111);self.flow('C=11',[self.reg,self.l2],GOLD,'Global Store 요청 · C[133]=11 · DRAM 기록 완료 시점은 별개');self.note('Store에도 캐시·메모리 시스템이 관여 · L1을 반드시 경유한다고 표현하지 않음');self.trace.append(dict(kind='store',i=133,A=4,B=7,C=11,dram_completion_claimed=False))
  elif i==9:
   panels=VGroup();self.results=[]
   for b in range(4):
    cells=VGroup(*(Rectangle(width=.14,height=.13,stroke_width=.4,stroke_color=TEAL,fill_color=TEAL,fill_opacity=.03) for _ in range(128))).arrange_in_grid(rows=8,buff=.035);self.results.append(cells);panels.add(stack(text(f'Block {b}',20,BLUE),cells,buff=.15))
   panels.arrange(RIGHT,buff=.4);self.detail(stack(text('C[0] … C[511] · Block별 128개 결과',25,TEAL),panels,buff=.22));self.code([3]);self.to(117)
   for w in range(4):self.play(*(self.results[b][k].animate.set_fill(GREEN,opacity=.6) for b in range(4) for k in range(w*32,(w+1)*32)),run_time=1)
   self.to(125);self.mapping();self.issue(0);self.issue(2);self.issue(1);self.flow('값',[self.l2,self.reg],TEAL,'다른 Warp의 실행과 메모리 요청은 겹쳐 진행될 수 있음');self.note('결과 채움과 Warp 선택은 설명용 순서 · 512개 Thread의 동시 실행을 뜻하지 않음');self.trace.append(dict(kind='parallel_results',threads=512,blocks=4,per_block=128,all_same_instant=False))
  elif i==10:
   self.detail(self.cards('더 많은 Thread가 항상 더 빠를까?',['Register','Shared','상주 제한'],ORANGE));self.to(137);self.play(Indicate(self.reg,color=ORANGE),run_time=.7);self.to(139);self.detail(stack(text('SM의 유한한 자원이 상주 규모를 제한',27,ORANGE),text('Register / Block 증가 → 상주 Block이 줄 수 있음',23,MUTED),text('Shared 사용량도 제약 · 이 커널은 Shared 0 bytes',23,MUTED)));self.play(Indicate(self.shared,color=MUTED),run_time=.7);self.note('별도의 일반적 자원 제약 설명 · 실제 Occupancy나 성능 배수 측정 아님')
  elif i==11:
   self.code([],['// separate access-pattern example','float x = A[i];','float y = A[i * 8];'],label='별도 접근 패턴 비교 · 원본 vectorAdd 변경 아님');self.detail(self.cards('32 Lanes × float32 · 유효 128B',['Stride 1','4 Sectors']));self.flow('주소',[self.alu,self.l1,self.l2],ORANGE,'정렬된 Stride 1: 네 개 32B Sector');self.to(148);self.detail(self.cards('같은 유효 데이터량 · 다른 주소 패턴',['Stride 8','32 Sectors'],ORANGE));self.note('정렬된 32개 활성 Lane의 32B 섹터 모델 · DRAM 실측 전송량/실행시간이 아님')
  elif i==12:
   self.detail(self.selected());self.code([3]);self.to(156);self.detail(stack(text('Who?  Block 1 · Thread 5',26,TEAL),text('Where?  SM 1 · 한 가지 배치 예시',26,BLUE),text('From Where?  Cache / DRAM',26,ORANGE),buff=.3));self.play(Indicate(self.blocks[1],color=TEAL),Indicate(self.sm,color=BLUE),Indicate(self.l2,color=ORANGE),run_time=.8)
  elif i==13:
   self.detail(stack(text('Logical Execution Organization',27,TEAL),text('Grid → Block → Warp(32T) → Thread',25,MUTED),text('실제 명령 실행: SM의 연산 자원',25,BLUE)));self.code([0,1]);self.play(Indicate(self.blocks,color=BLUE),run_time=.8);self.to(169);self.detail(stack(text('SM · Execution Units',28,BLUE),text('Register / Shared / L1',25,PURPLE),text('L2 → Controller → DRAM',25,ORANGE)));self.play(Indicate(self.alu,color=BLUE),Indicate(self.reg,color=PURPLE),run_time=.7);self.to(174);self.flow('요청',[self.l2,self.mc,self.dram],ORANGE,'캐시 아래에는 Controller와 물리 DRAM이 연결');self.note('Global은 논리 주소 공간 · Shared는 이 커널에서 미사용 · 캐시 경로는 조건에 따라 다름')
  elif i==14:
   self.detail(stack(text('CUDA Kernel → GPU Execution',30,TEAL),text('논리적 조직 → SM 실행 → 데이터 공급',25,MUTED)));self.code([0],['vectorAdd<<<4, 128>>>(A,B,C,512);','// Block 1 / Thread 5 -> i = 133','C[i] = A[i] + B[i];']);self.mapping();self.flow(4,[self.l1,self.reg],TEAL,'같은 Thread · 같은 주소 · 데이터 공급');self.flow(11,[self.alu,self.l2],GOLD,'C[133]=11 · Global Store 요청')
  else:
   self.detail(stack(text('계산을 어디에 배치할 것인가?',28,TEAL),text('데이터를 어떻게 이동시킬 것인가?',28,ORANGE),buff=.4));self.code([0],['C[i] = A[i] + B[i];']);self.play(Indicate(self.blocks,color=TEAL),Indicate(self.sm,color=BLUE),run_time=.8);self.to(187);self.detail(stack(text('GPU HIERARCHY — COMPLETE',31,TEAL,width=7.2),text('계산과 데이터 이동을 더 효율적으로 배치한다',23,MUTED)));self.to(189);self.play(Indicate(self.l2,color=BLUE),Indicate(self.mc,color=GOLD),Indicate(self.dram,color=ORANGE),run_time=.8);self.note('하나의 CUDA 프로그램을 실행하는 논리 조직 · 물리 연산 · 데이터 공급 구조')
