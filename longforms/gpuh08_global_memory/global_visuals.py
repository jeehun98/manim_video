import json
from pathlib import Path
from manim import *
from shared_style import *
P=Path(__file__).resolve().parent
GOLD='#F4C96B';TEAL='#48DED0'
CODE=['float a = A[i];','float b = B[i];','C[i] = a + b;']
class GlobalBase(StyleScene):
 INDEX=0
 def construct(self):
  self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start'];self.bounds=[];self.trace=[];self.sc=1 if SHORT else .87
  self.dc=np.array([0,1.08,0]) if SHORT else np.array([-3.65,-1.07,0]);self.dw=7.65 if SHORT else 7.1;self.dh=3.2 if SHORT else 2.65
  self.cc=np.array([0,-2.85,0]) if SHORT else np.array([4.15,.1,0]);self.cw=7.65 if SHORT else 6.15;self.ch=4.05 if SHORT else 4.7
  self.add(text('GPU HIERARCHY / LEVEL 08',19,MUTED).move_to([0,7.35 if SHORT else 4,0]),text(self.meta['title'],32,width=8 if SHORT else 14).move_to([0,6.45 if SHORT else 3.2,0]))
  self.world();self.code();self.note('Global은 논리 주소 공간 · 데이터는 캐시에서 처리될 수도 있음')
  self.shot();self.to(self.meta['end'])
  layout='shorts' if SHORT else 'longform'
  for name,data in [('geometry',self.bounds),('states',self.trace)]: (P/f'{name}_{layout}_{self.INDEX:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 def code(self,active=(),lines=None,label='vectorAdd.cu · 핵심 발췌'):super().code(active,CODE if lines is None else lines,label)
 def world(self):
  outer=RoundedRectangle(width=7.65,height=2.5,corner_radius=.14,color=GOLD,fill_color=PANEL,fill_opacity=.4)
  chip=RoundedRectangle(width=4.9,height=1.68,corner_radius=.1,color=BLUE).move_to([-1.15,-.02,0]);sm=RoundedRectangle(width=2.7,height=1.12,corner_radius=.08,color=BLUE).move_to([-2.04,-.12,0])
  self.warp=box('Warp 0',1.12,.32,BLUE,16).move_to([-2.72,.08,0]);self.reg=box('Register',1.12,.32,PURPLE,16).move_to([-1.38,.08,0]);self.shared=box('Shared',1.12,.32,TEAL,16).move_to([-2.72,-.37,0]);self.l1=box('L1 Cache',1.12,.32,ORANGE,16).move_to([-1.38,-.37,0])
  self.sms=VGroup(*(box(f'SM {i}',.75,.35,BLUE,15).move_to([-.12,.42-(i-1)*.49,0]) for i in range(1,4)))
  self.l2=box('L2',.76,.5,ORANGE,19).move_to([.82,-.12,0]);self.dram=box('',1.86,1.35,GOLD).move_to([2.57,-.05,0]);self.arrays=VGroup(*(box(s,1.35,.23,GOLD,14).move_to([2.57,.16-i*.32,0]) for i,s in enumerate(['A [ ... ]','B [ ... ]','C [ ... ]'])))
  links=VGroup(DashedLine(self.l1.get_right(),self.l2.get_left(),color=MUTED,stroke_width=1),DashedLine(self.l2.get_right(),self.dram.get_left(),color=MUTED,stroke_width=1))
  self.footer=text('Global 데이터의 일반적 물리 저장: Device DRAM · 캐시 가능',13,MUTED,width=7.1).move_to([0,-1.05,0])
  self.map=VGroup(outer,chip,sm,links,self.warp,self.reg,self.shared,self.l1,self.sms,self.l2,self.dram,self.arrays,text('GPU DEVICE · 메모리 관계도',18,GOLD).move_to([0,1.03,0]),text('GPU CHIP',15,BLUE).move_to([-2.9,.66,0]),text('SM 0',13,BLUE).move_to([-2.9,.32,0]),text('Global 데이터',16,GOLD).move_to([2.57,.88,0]),text('Device DRAM',14,GOLD).move_to([2.57,.49,0]),self.footer)
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
 def kernel_load(self):
  self.code([0]);self.flow(6,[self.l2,self.l1,self.reg],GREEN,'A[5]=6 · L2 적중을 가정한 Load')
  self.code([1]);self.flow(60,[self.l2,self.l1,self.reg],ORANGE,'B[5]=60 · L2 적중을 가정한 Load')
 def kernel_store(self):self.code([2]);self.flow(66,[self.reg,self.l2],GOLD,'C[5]=66 · Global Store 요청 · DRAM 기록 완료를 뜻하지 않음')
 def board(self,stride=1,reverse=False):
  # Same 32 sectors / 256 float32 words at every scale and every access pattern.
  self.lanes=VGroup(*(box(f'L{k}',.74,.22,BLUE,12,fill=.08).move_to([(k%8-3.5)*.9,.93-(k//8)*.25,0]) for k in range(32)))
  self.sectors=VGroup();self.words=[]
  for s in range(32):
   cells=VGroup(*(Rectangle(width=.075,height=.13,stroke_width=.4,stroke_color=MUTED,fill_color=MUTED,fill_opacity=.08).move_to([(j-3.5)*.083,0,0]) for j in range(8)))
   border=RoundedRectangle(width=.8,height=.32,corner_radius=.035,stroke_width=1,stroke_color=MUTED,fill_color=PANEL,fill_opacity=.5)
   title=text(f'S{s}',10,MUTED).move_to([0,.1,0]);cells.shift(DOWN*.055)
   sec=VGroup(border,title,cells).move_to([(s%8-3.5)*.9,-.32-(s//8)*.37,0]);self.sectors.add(sec);self.words.extend(list(cells))
  head=text('Warp 0 · 32개 활성 Lane · 각 4B',18,BLUE).move_to([0,1.35,0]);sub=text('A[0..255] · 32B Sector × 32 · 격자 위치 고정',16,GOLD).move_to([0,-.035,0])
  self.stats=text('유효 128B 고정 | 4 Sectors | 섹터 기준 128B',18,GOLD);self.stats.move_to([0,-1.9,0]);self.addresslabel=text('L0→A[0] · L1→A[1] · … · L31→A[31]',17,BLUE).move_to([0,-2.2,0])
  group=VGroup(head,self.lanes,sub,self.sectors,self.stats,self.addresslabel);self.detail(group);self.connections=VGroup();self.pattern(stride,reverse,animate=False);return group
 def pattern(self,stride=1,reverse=False,animate=True):
  ids=[31-l if reverse else l*stride for l in range(32)];ss=sorted({a//8 for a in ids});changes=[]
  for s,sec in enumerate(self.sectors):
   col=GOLD if s in ss else MUTED;opacity=.18 if s in ss else .025
   changes.extend([sec[0].animate.set_stroke(col,width=1.6 if s in ss else .7).set_fill(col,opacity=opacity),sec[1].animate.set_color(col)])
  for n,w in enumerate(self.words):changes.append(w.animate.set_fill(GREEN if n in ids else MUTED,opacity=.95 if n in ids else .04).set_stroke(GREEN if n in ids else MUTED,width=.5))
  count=len(ss);stats=text(f'유효 128B 고정  |  {count} Sectors  |  섹터 기준 {count*32:,}B',18,GOLD,width=self.dg.width*.98).move_to(self.stats)
  desc='L0→A[31] · L1→A[30] · … · L31→A[0]' if reverse else f'L0→A[0] · L1→A[{stride}] · … · L31→A[{31*stride}]'
  lab=text(desc,16,BLUE,width=self.dg.width*.98).move_to(self.addresslabel)
  if animate:
   self.play(*changes,Transform(self.stats,stats),Transform(self.addresslabel,lab),run_time=1)
  else:
   for s,sec in enumerate(self.sectors):sec[0].set_stroke(GOLD if s in ss else MUTED,width=1.6 if s in ss else .7).set_fill(GOLD,opacity=.18 if s in ss else .025);sec[1].set_color(GOLD if s in ss else MUTED)
   for n,w in enumerate(self.words):w.set_fill(GREEN if n in ids else MUTED,opacity=.95 if n in ids else .04)
   self.stats.become(stats);self.addresslabel.become(lab)
  self.ids=ids;self.trace.append(dict(kind='pattern',time=round(self.start+self.time,3),stride=stride,reverse=reverse,indices=ids,sectors=ss,useful_bytes=128,sector_footprint=count*32,base_aligned=32))
 def connect(self,selected=(0,1,7,8,16,31),duration=.8):
  if len(self.connections):self.remove(self.connections)
  # A selected lane's identity follows its exact addressed word; all32 identities remain visible.
  self.connections=VGroup(*(Line(self.lanes[k].get_bottom(),self.words[self.ids[k]].get_center(),stroke_color=[GREEN,ORANGE,BLUE,PURPLE][j%4],stroke_width=1.7,stroke_opacity=.75) for j,k in enumerate(selected)))
  self.play(Create(self.connections),run_time=duration)
  self.play(*(Indicate(self.lanes[k],color=GREEN,scale_factor=1.08) for k in selected),*(Indicate(self.words[self.ids[k]],color=GREEN,scale_factor=1.3) for k in selected),run_time=.5)
  self.remove(self.connections);self.connections=VGroup()
  self.msg('Lane → 요청 원소 → 포함된 32B Sector · 주소 대응 예시')
  self.trace.append(dict(kind='lane_links',time=self.start+self.time,links=[dict(lane=k,word=self.ids[k],byte=self.ids[k]*4,sector=self.ids[k]//8) for k in selected]))
 def top_requests(self,stride):
  self.msg(f'Warp 0 · Stride {stride} · 주소 집합 → {4 if stride==1 else 32}개 Sector')
  self.flow('주소',[self.warp,self.l1,self.l2],GOLD,f'Stride {stride} 주소 요청 · 캐시 계층에서 처리 가능')
 def shot(self):
  i=self.INDEX
  if i==0:
   self.detail(self.cards('값의 사용 범위',['Register','Shared'],PURPLE));self.play(Indicate(self.reg,color=PURPLE),run_time=.6);self.to(4);self.play(Indicate(self.shared,color=TEAL),run_time=.6);self.to(8)
   # Zoom emphasis preserves exact SM identity while opening the device-wide view.
   self.play(self.map.animate.scale(.9),run_time=.7);self.play(self.map.animate.scale(1/.9),Indicate(self.dram,color=GOLD),run_time=.7);self.detail(self.cards('대규모 배열은 Global Memory에',['A','B','C']));self.to(12);self.flow('주소',[self.warp,self.l2],GOLD,'Global Memory · GPU 전체에서 접근하는 주소 공간')
  elif i==1:
   self.detail(self.cards('여러 SM · 같은 Global 배열',['SM 0','SM 1','SM 2','SM 3']));self.flow('접근',[self.warp,self.l2],GOLD,'SM 0의 Global 접근')
   for node in self.sms:self.flow('접근',[node,self.l2],GOLD,'여러 SM이 같은 Global 주소 공간에 접근')
   self.to(21);self.detail(stack(text('정성적 비교 · 수치나 비율 아님',22,MUTED),text('Register / Shared: 제한된 온칩 자원',26,TEAL),text('Global: 대용량 · 상대적으로 큰 접근 지연',26,GOLD)));self.play(Indicate(self.dram,color=GOLD),run_time=.6)
  elif i==2:
   self.detail(self.cards('Thread 5의 배열 원소 계산',['A[5]=6','B[5]=60','C[5]=66']));self.to(28);self.kernel_load();self.to(34);self.code([2]);self.play(Indicate(self.reg,color=GREEN),run_time=.6);self.msg('Thread 5 · 6 + 60 = 66');self.to(37);self.note('지역 변수와 물리 Register가 1:1로 대응하는 것은 아님');self.to(39);self.kernel_store()
  elif i==3:
   self.detail(self.cards('Load → Compute → Store',['6 + 60','66','C[5]']));self.kernel_load();self.to(44);self.play(Indicate(self.reg,color=PURPLE),run_time=.6);self.to(46);self.kernel_store()
  elif i==4:
   self.board();self.code([],['int i = threadIdx.x;','float x = A[i];'],label='patternRead.cu · 별도 1-Warp 예제');self.note('이후 비교: NVIDIA CC 6.0+ · 기준 주소 32B 정렬 · float32 Load')
   self.to(50);self.msg('같은 데이터량이어도 주소 패턴은 다를 수 있다');self.to(56);self.play(LaggedStart(*(Indicate(n,color=BLUE,scale_factor=1.1) for n in self.lanes),lag_ratio=.025),run_time=1.5);self.to(60);self.msg('32 Lanes × 4B = 유효 데이터 128B');self.detail(self.cards('하나의 Warp · 각 Lane의 4B Load',['32 × 4B','128B']))
  elif i==5:
   self.board();self.code([1],['int i = threadIdx.x;','float x = A[i];'],label='patternRead.cu · Stride 1');self.note('기준 주소 32B 정렬 · 32개 활성 Lane의 float32 읽기')
   self.connect();self.top_requests(1);self.to(70);self.connect((0,7,8,15,24,31));self.msg('A[0..31] · byte 0..127 · 연속된 128B 영역');self.to(76);self.play(LaggedStart(*(Indicate(self.sectors[k],color=GOLD,scale_factor=1.05) for k in range(4)),lag_ratio=.2),run_time=1.2);self.msg('8개 float32 × 4B = 32B · 네 개 Sector')
  elif i==6:
   self.board();self.code([1],['int i = threadIdx.x;','float x = A[i];'],label='patternRead.cu · 주소 패턴 비교');self.note('Lane 수 32 · Lane당 4B · 유효 데이터 128B는 변하지 않음')
   self.to(83);self.code([1],['int i = threadIdx.x;','float x = A[i * 8];'],label='patternRead.cu · Stride 8');self.pattern(8);self.connect((0,1,2,3,30,31));self.to(86);self.msg('선택 원소: 0, 8, 16, …, 248 · 여전히 32개');self.to(89);self.top_requests(8)
  elif i==7:
   self.board(8);self.code([0],['float x = A[i * 8];','// 4 * i * 8 = 32 * i bytes'],label='patternRead.cu · Stride 8');self.note('각 Lane이 다른 32B Sector · 같은 값이 아니라 같은 데이터량 비교')
   for t,lanes in [(92,(0,1,2,3)),(95,(8,9,10,11)),(98,(28,29,30,31))]:self.to(t);self.connect(lanes)
   self.to(100);self.play(LaggedStart(*(Indicate(sec,color=GOLD,scale_factor=1.025) for sec in self.sectors),lag_ratio=.02),run_time=1);self.msg('Stride 1: 4개 → Stride 8: 32개 Sector')
  elif i==8:
   self.board(8);self.code([],['// useful: 32 * 4 = 128 B','// stride 1:  4 * 32 = 128 B','// stride 8: 32 * 32 = 1024 B'],label='유효 데이터량과 Sector Footprint');self.note('Sector Footprint · 실제 DRAM 전송량/시간을 뜻하지 않음')
   self.to(104);self.pattern(1);self.to(106);self.pattern(8);self.msg('유효 128B 유지 · 섹터 기준 데이터량 128B → 1,024B')
  elif i==9:
   self.board(8);self.code([],['// address = base + 4 * i * stride','// sector = address / 32'],label='Memory Coalescing · 개념 모형');self.connect((0,1,2,8,16,31));self.to(112);self.pattern(1);self.connect((0,1,2,7));self.to(115);self.msg('Warp 주소들을 필요한 Sector 접근으로 처리 · 항상 1개로 합쳐지는 것은 아님')
  elif i==10:
   self.board();self.code([1],['int i = threadIdx.x;','float x = A[31 - i];'],label='patternRead.cu · 주소 순서를 뒤집어도');self.note('추가 검증: Lane 순서가 달라도 같은 4개 Sector에 모일 수 있음');self.to(119);self.pattern(1,True);self.connect((0,1,7,8,24,31));self.to(122);self.msg('역순 A[31..0]도 동일한 4개 Sector · 주소 집합이 핵심');self.play(*(Indicate(self.sectors[k],color=GOLD) for k in range(4)),run_time=.8)
  elif i==11:
   self.detail(stack(text('8× Sector Footprint',34,GOLD),text('≠ 8× Execution Time',34,ORANGE)));self.code([],['// sectors: 4 -> 32','// timing: requires measurement'],label='요청 모델과 실측 성능을 구분');self.note('섹터 수로 실행시간 배수를 단정하지 않음');self.to(132)
   self.flow('Hit',[self.warp,self.l1,self.reg],GREEN,'L1 적중을 가정한 데이터 경로');self.flow('Hit',[self.l2,self.l1,self.reg],ORANGE,'L2 적중을 가정한 데이터 경로');self.to(135);self.play(Indicate(self.dram,color=GOLD),run_time=.5);self.msg('캐시 · 메모리 대역폭 · 다른 연산도 실제 실행시간에 영향')
  elif i==12:
   self.detail(stack(text('Shared: Bank 접근 경합',27,TEAL),text('서로 다른 주소 → 같은 Bank',23,MUTED),text('Global: 요청 주소의 Sector 분산',27,GOLD),text('4 Sector ↔ 32 Sector',23,MUTED),buff=.18));self.code([],['// Shared: word % 32 -> bank','// Global: byte / 32 -> sector'],label='서로 다른 하드웨어 메커니즘');self.note('Bank 예시는 32-bit word 기준 · 동일 주소 Broadcast는 별도 예외');self.flow('Bank',[self.warp,self.shared],TEAL,'Shared의 서로 다른 주소가 같은 Bank로 집중');self.to(143);self.flow('Sector',[self.warp,self.l1,self.l2],GOLD,'Global 주소 집합이 여러 Sector에 분산');self.play(Indicate(self.shared,color=TEAL),Indicate(self.dram,color=GOLD),run_time=.7)
  else:
   self.board(8);self.code([0],['float x = A[i];','// same amount, different address pattern'],label='Global Memory · Address Pattern Matters');self.note('같은 계산량 · 같은 유효 데이터량 · 달라지는 메모리 효율');self.to(151);self.pattern(1);self.to(154);self.detail(self.cards('GPU 전체가 접근하는 Global Memory',['SM 0','SM 1','SM 2','SM 3']));self.flow('주소',[self.warp,self.l2],GOLD,'SM 0 Warp의 Global 주소 요청');self.to(158)
   for node in self.sms:self.flow('주소',[node,self.l2],GOLD,'여러 SM · 각 Warp의 주소 패턴이 접근 효율을 결정')
   self.msg('Global Memory — Address Pattern Matters');self.detail(stack(text('Global Memory',33,GOLD),text('Address Pattern Matters',30,INK),text('같은 계산 · 달라지는 메모리 효율',26,TEAL)))
