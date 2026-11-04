import json
from pathlib import Path
from manim import *
from shared_style import *
P=Path(__file__).resolve().parent
GOLD='#F4C96B';TEAL='#48DED0'
CODE=['float x = A[i];','B[i] = x * 2.0f;']
class CacheBase(StyleScene):
 INDEX=0
 def construct(self):
  self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start'];self.bounds=[];self.trace=[];self.sc=1 if SHORT else .87
  self.dc=np.array([0,1.08,0]) if SHORT else np.array([-3.65,-1.07,0]);self.dw=7.65 if SHORT else 7.1;self.dh=3.2 if SHORT else 2.65
  self.cc=np.array([0,-2.85,0]) if SHORT else np.array([4.15,.1,0]);self.cw=7.65 if SHORT else 6.15;self.ch=4.05 if SHORT else 4.7
  self.add(text('GPU HIERARCHY / LEVEL 09',19,MUTED).move_to([0,7.35 if SHORT else 4,0]),text(self.meta['title'],32,width=8 if SHORT else 14).move_to([0,6.45 if SHORT else 3.2,0]))
  self.world();self.code();self.note('메모리 공간 ≠ 하드웨어 캐시 · 요청 경로는 설명용 모형')
  self.shot();self.to(self.meta['end'])
  layout='shorts' if SHORT else 'longform'
  for name,data in [('geometry',self.bounds),('states',self.trace)]: (P/f'{name}_{layout}_{self.INDEX:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 def code(self,active=(),lines=None,label='readArray.cu · 핵심 발췌'):super().code(active,CODE if lines is None else lines,label)
 def world(self):
  outer=RoundedRectangle(width=7.65,height=2.5,corner_radius=.14,color=GOLD,fill_color=PANEL,fill_opacity=.4)
  chip=RoundedRectangle(width=4.9,height=1.68,corner_radius=.1,color=BLUE).move_to([-1.15,-.02,0]);sm=RoundedRectangle(width=2.7,height=1.12,corner_radius=.08,color=BLUE).move_to([-2.04,-.12,0])
  self.warp=box('Warp 0',1.12,.32,BLUE,16).move_to([-2.72,.08,0]);self.reg=box('Register',1.12,.32,PURPLE,16).move_to([-1.38,.08,0]);self.shared=box('Shared',1.12,.32,TEAL,16).move_to([-2.72,-.37,0]);self.l1=box('L1 Cache',1.12,.32,BLUE,16).move_to([-1.38,-.37,0])
  self.sms=VGroup(*(box(f'SM {i} / L1',.9,.35,BLUE,11).move_to([-.12,.42-(i-1)*.49,0]) for i in range(1,4)))
  self.l2=box('L2',.76,.5,'#6D93EB',19).move_to([.82,-.12,0]);self.dram=box('',1.86,1.35,GOLD).move_to([2.57,-.05,0]);self.arrays=VGroup(*(box(s,1.35,.23,GOLD,14).move_to([2.57,.16-i*.32,0]) for i,s in enumerate(['A [ ... ]','B [ ... ]','C [ ... ]'])))
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
 def axes(self):
  left=stack(text('Memory Spaces',27,GOLD),box('Register · Thread',3.35,.51,PURPLE,22),box('Shared · Block',3.35,.51,TEAL,22),box('Global · GPU-wide',3.35,.51,GOLD,22),text('데이터의 저장·접근 범위',20,MUTED),buff=.16)
  right=stack(text('Hardware Caches',27,BLUE),box('L1 · SM-local',3.35,.51,BLUE,22),box('L2 · GPU-wide',3.35,.51,'#6D93EB',22),text('복사본의 보관·교체',23,BLUE),text('데이터의 공급·재사용',20,MUTED),buff=.16)
  return VGroup(left,right).arrange(RIGHT,buff=.48)
 def scenario_board(self,name,status=None):
  from cache_model import CASES
  c=CASES[name];self.casecards=VGroup(*(box(label,1.85,.59,color,23) for label,color in [('L1',BLUE),('L2','#6D93EB'),('DRAM',GOLD)])).arrange(RIGHT,buff=.35)
  self.casestatus=VGroup(*(text(s,22,GREEN if s=='Hit' else ORANGE if s=='Miss' else MUTED,width=1.8).next_to(node,DOWN,buff=.15) for node,s in zip(self.casecards,status or c['status'])))
  body=VGroup(self.casecards,self.casestatus)
  g=stack(text(f'{name} · 독립적으로 가정한 사례',26,BLUE,width=7.2),text('동일한 Global 주소 A[5] · 값 6',23,MUTED),body,text('공급원: '+c['source']+' · 값은 항상 6',24,GREEN),buff=.24)
  self.detail(g)
 def cache_case(self,name):
  from cache_model import CASES
  c=CASES[name];self.scenario_board(name);nodes={'Warp':self.warp,'L1':self.l1,'L2':self.l2,'DRAM':self.dram,'Register':self.reg}
  self.flow('A[5]',[nodes[k] for k in c['request']],ORANGE,f'{name} · 요청 경로 · 측정된 캐시 상태 아님')
  self.flow(6,[nodes[k] for k in c['response']],GREEN,f'{name} · {c["source"]}에서 값 6 공급')
  self.trace.append(dict(kind='cache_case',time=round(self.start+self.time,3),case=name,request=c['request'],response=c['response'],status=c['status'],source=c['source'],value=6,conceptual=True))
 def unified(self,ratio=.25):
  self.resource=RoundedRectangle(width=6.5,height=.95,corner_radius=.08,stroke_color=MUTED)
  self.sharefill=Rectangle(width=6.5*ratio,height=.89,stroke_width=0,fill_color=TEAL,fill_opacity=.35).align_to(self.resource,LEFT)
  self.cachefill=Rectangle(width=6.5*(1-ratio),height=.89,stroke_width=0,fill_color=BLUE,fill_opacity=.35).align_to(self.resource,RIGHT)
  self.sharetext=text('Shared',23,TEAL).move_to(self.sharefill);self.cachetext=text('L1',23,BLUE).move_to(self.cachefill)
  g=stack(text('SM 내부 Unified On-Chip Storage',27,BLUE),VGroup(self.resource,self.sharefill,self.cachefill,self.sharetext,self.cachetext),text('같은 물리 자원 · 구분되는 기능과 접근',23,MUTED),text('개념 비율 예시 · 실제 지원 구성이나 용량 아님',20,ORANGE),buff=.22)
  self.detail(g);self.resource_ratio=ratio
 def repartition(self,ratio):
  w=self.resource.width;h=self.sharefill.height;left=self.resource.get_left();right=self.resource.get_right()
  a=Rectangle(width=w*ratio,height=h,stroke_width=0,fill_color=TEAL,fill_opacity=.35).move_to(left+RIGHT*w*ratio/2)
  b=Rectangle(width=w*(1-ratio),height=h,stroke_width=0,fill_color=BLUE,fill_opacity=.35).move_to(right+LEFT*w*(1-ratio)/2)
  self.play(Transform(self.sharefill,a),Transform(self.cachefill,b),self.sharetext.animate.move_to(a),self.cachetext.animate.move_to(b),Indicate(self.shared,color=TEAL),Indicate(self.l1,color=BLUE),run_time=.8)
  self.trace.append(dict(kind='resource_partition',ratio=ratio,actual_supported_configuration=False,automatic_shared_l1_copy=False));self.resource_ratio=ratio
 def shot(self):
  i=self.INDEX
  if i==0:
   self.detail(self.cards('Register · Shared · Global',['Thread','Block','GPU-wide']));self.play(Indicate(self.reg,color=PURPLE),Indicate(self.shared,color=TEAL),Indicate(self.dram,color=GOLD),run_time=.7);self.to(4);self.detail(self.cards('L1과 L2는 어디에 속할까?',['L1 Cache?','L2 Cache?'],BLUE));self.play(Indicate(self.l1,color=BLUE),Indicate(self.l2,color=BLUE),run_time=.7);self.to(9);self.detail(self.axes());self.to(13);self.msg('한 시스템을 보는 두 관점 · 메모리 공간과 캐시 계층',BLUE)
  elif i==1:
   g=self.detail(self.axes());self.play(Indicate(self.reg,color=PURPLE),run_time=.6);self.to(24);self.play(Indicate(self.shared,color=TEAL),run_time=.6);self.msg('Register: Thread별 계산값 · Shared: 같은 Block의 공유 공간');self.to(28);self.flow('주소',[self.warp,self.l2],GOLD,'Global Memory · 여러 SM에서 접근 가능한 주소 공간');self.flow('주소',[self.sms[0],self.l2],GOLD,'SM 1에서도 같은 Global 배열에 접근 가능')
  elif i==2:
   self.detail(self.axes());self.play(Indicate(self.l1,color=BLUE),Indicate(self.l2,color=BLUE),run_time=.6);self.to(37);self.detail(self.cards('같은 A[5] · 캐시에 보관된 복사본',['Global A[5]','L2 copy','L1 copy'],BLUE));self.flow(6,[self.dram,self.l2,self.l1],GREEN,'설명용 적재 사례 · Global 주소는 그대로 · 캐시 복사본');self.to(42);self.msg('별도의 L1 주소 공간 / L2 주소 공간을 할당하는 것이 아님',BLUE)
  elif i==3:
   self.detail(self.cards('SM별 L1 · 여러 SM이 공유하는 L2',['SM-local L1','GPU-wide L2'],BLUE));self.to(48);self.play(Indicate(self.l1,color=BLUE),run_time=.5)
   for node in self.sms:self.play(Indicate(node,color=BLUE),run_time=.4)
   self.to(53);self.flow('요청',[self.warp,self.l2],BLUE,'SM 0의 요청 → GPU 공용 L2');self.flow('요청',[self.sms[0],self.l2],BLUE,'SM 1의 요청 → 같은 L2');self.play(Indicate(self.l2,color=GREEN),run_time=.6)
  elif i==4:
   self.detail(self.cards('Thread 5의 Global Load',['A[5]','값 6']));self.code([0]);self.note('L1 캐싱을 사용하는 일반적인 Load 경로를 가정한 설명용 모형');self.to(60);self.flow('A[5]',[self.warp,self.l1],ORANGE,'Thread 5의 Global 주소 읽기 요청 · A[5]');self.to(62);self.msg('어디에서 값 6을 가져올 수 있을까?',BLUE)
  elif i==5:
   self.code([0]);self.note('독립 가정: A[5]가 L1에 존재 · 실제 Hit/Miss 측정 아님');self.cache_case('L1 Hit');self.to(70);self.play(Indicate(self.l1,color=GREEN),run_time=.7);self.msg('Cache Hit · 해당 캐시에 필요한 데이터가 존재',GREEN)
  elif i==6:
   self.code([0]);self.note('서로 다른 캐시 상태를 가정한 사례 · 실제 하드웨어 타이밍 아님');self.detail(self.cards('L1에 필요한 데이터가 없다면',['L1 Miss','다음 계층'],ORANGE));self.flow('A[5]',[self.warp,self.l1,self.l2],ORANGE,'L1 Miss · 요청은 L2로 전달될 수 있음');self.to(78);self.cache_case('L2 Hit');self.to(81);self.cache_case('DRAM')
  elif i==7:
   self.code([0]);self.note('명령·캐시 정책·아키텍처에 따라 경로가 달라짐');self.cache_case('L1 Bypass');self.to(89);self.code([0],['float x = __ldcg(&A[i]);','B[i] = x * 2.0f;'],label='readL2Policy.cu · 별도 L2 캐싱 정책 예제');self.flow('A[5]',[self.warp,self.l2],ORANGE,'별도 __ldcg 예제 · L1을 우회하는 Load');self.flow(6,[self.l2,self.reg],GREEN,'이 사례는 L2 적중을 가정 · L1 미사용')
  elif i==8:
   self.unified(.25);self.code([],['// Unified L1 / Shared storage','// architecture dependent'],label='물리적 자원 · 프로그래밍 주소 공간과 구별');self.play(Indicate(self.shared,color=TEAL),Indicate(self.l1,color=BLUE),run_time=.7);self.to(97);self.msg('일부 아키텍처: Shared와 L1이 같은 온칩 자원을 분할 사용',BLUE);self.to(100);self.repartition(.5);self.to(103);self.repartition(.75);self.note('25:75 / 50:50 / 75:25는 개념 비율 · 실제 지원 구성 아님')
  elif i==9:
   self.unified(.5);self.code([],['__shared__ float s[128];','s[threadIdx.x] = A[i];','__syncthreads();'],label='sharedRead.cu · 핵심 발췌');self.note('같은 물리 자원 ≠ 같은 메모리 공간 · 자동 Shared↔L1 이동 아님');self.msg('Shared와 L1 사이에 자동 데이터 복사 경로를 만들지 않음',BLUE);self.to(111);self.code([0,1],['__shared__ float s[128];','s[threadIdx.x] = A[i];','__syncthreads();'],label='sharedRead.cu · 명시적 Shared 저장');self.flow(6,[self.l2,self.l1,self.reg],GREEN,'A[5] Load · 이 사례는 L2 적중을 가정');self.flow(6,[self.reg,self.shared],TEAL,'코드의 Shared Store · s[5] = 6');self.trace.append(dict(kind='shared_store',source='Register',destination='Shared',value=6,explicit=True));self.to(116);self.play(Indicate(self.shared,color=TEAL),run_time=.7)
  elif i==10:
   self.code([0]);self.detail(self.cards('L1의 적재·교체는 일반적으로 하드웨어가',['Line A','Line B'],BLUE));self.note('캐시 Line 교체는 설명용 모형 · 실제 용량·교체 정책을 재현하지 않음');self.flow('Line A',[self.l2,self.l1],GREEN,'하드웨어가 L1에 캐시 Line 적재');self.to(121);self.flow('Line B',[self.l2,self.l1],BLUE,'용량·정책에 따라 기존 Line이 교체될 수 있음');self.to(123);self.detail(stack(text('Shared Hardware Resources',30,BLUE),text('≠ Same Memory Space',30,ORANGE),text('Shared: 명시적 배치·동기화  |  L1: 하드웨어 보관·교체',23,MUTED,width=7.3)));self.play(Indicate(self.shared,color=TEAL),run_time=.6);self.to(127);self.play(Indicate(self.l1,color=BLUE),run_time=.6)
  elif i==11:
   self.detail(self.cards('서로 다른 SM · 공용 L2의 같은 데이터',['SM 0','L2: A[5]','SM 1'],BLUE));self.code([0]);self.note('입력에 쓰기가 없고 A[5]가 L2에 남아 있다고 가정 · SM 배치 추적 아님');self.flow('A[5]',[self.warp,self.l2],ORANGE,'SM 0의 요청 · 해당 L1 Miss를 가정');self.flow(6,[self.l2,self.l1,self.reg],GREEN,'L2에서 SM 0에 값 6 공급');self.to(137);self.flow('A[5]',[self.sms[0],self.l2],ORANGE,'SM 1도 같은 주소 요청 · 해당 L1 Miss 가정');self.flow(6,[self.l2,self.sms[0]],GREEN,'SM 1에도 L2에서 값 6 공급 · DRAM 재접근 없음');self.trace.append(dict(kind='cross_sm_reuse',source='L2',sms=[0,1],value=6,unchanged_input=True,residency_assumed=True,dram_access=False));self.to(141);self.play(Indicate(self.l2,color=GREEN),run_time=.7)
  elif i==12:
   self.detail(self.axes());self.code([0]);self.play(Indicate(self.reg,color=PURPLE),run_time=.6);self.to(146);self.play(Indicate(self.shared,color=TEAL),run_time=.6);self.to(148);self.play(Indicate(self.dram,color=GOLD),run_time=.6);self.to(151);self.flow('A[5]',[self.warp,self.l1],ORANGE,'Global 주소 공간에서 읽기 요청');self.flow(6,[self.l1,self.reg],GREEN,'공급 경로 관점: L1 적중을 가정해 가까운 캐시에서 반환');self.to(155);self.play(Indicate(self.l2,color=BLUE),run_time=.7)
  else:
   self.detail(self.axes());self.code([0]);self.note('저장·접근 범위와 실제 데이터 공급 경로를 함께 본다');self.flow('A[5]',[self.warp,self.l1,self.l2],ORANGE,'Global 주소는 그대로 · L1 Miss / L2 Hit 가정');self.flow(6,[self.l2,self.l1,self.reg],GREEN,'같은 메모리 시스템 · 캐시에서 값 6 공급');self.to(163);self.detail(stack(text('Memory Spaces',30,GOLD),text('≠ Hardware Cache Hierarchy',30,BLUE,width=7.3),text('범위와 경로 · 두 관점으로 함께 이해한다',25,INK)));self.to(166);self.play(Indicate(self.reg,color=PURPLE),Indicate(self.shared,color=TEAL),Indicate(self.l1,color=BLUE),Indicate(self.l2,color=BLUE),run_time=.9)
