import json
from pathlib import Path
from manim import *
from shared_style import *
P=Path(__file__).resolve().parent
TEAL='#48DED0'
CODE=['__shared__ float s[128];','s[t] = A[t];','__syncthreads();','B[t] = s[(t+1)%128];']
class SharedBase(StyleScene):
 INDEX=0
 def construct(self):
  self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start'];self.bounds=[];self.trace=[]
  self.dc=np.array([0,1.08,0]) if SHORT else np.array([-3.65,-1.07,0]);self.dw=7.65 if SHORT else 7.1;self.dh=3.1 if SHORT else 2.6
  self.cc=np.array([0,-2.85,0]) if SHORT else np.array([4.15,.1,0]);self.cw=7.65 if SHORT else 6.15;self.ch=4.05 if SHORT else 4.7
  self.add(text('GPU HIERARCHY / LEVEL 07',19,MUTED).move_to([0,7.35 if SHORT else 4,0]),text(self.meta['title'],32,width=8 if SHORT else 14).move_to([0,6.45 if SHORT else 3.2,0]))
  self.world();self.code();self.note('Shared Memory는 SM의 자원 · 같은 Block 안에서 공유')
  if 7<=self.INDEX<=11:
   for node,label in [(self.t5,'C[0,0]'),(self.t6,'C[0,1]')]:node[1].become(text(label,17,GREEN if node is self.t5 else ORANGE,width=node.width-.1).move_to(node))
   for node,label in zip(self.slots,['A Tile','B Tile','재사용']):node[1].become(text(label,12,TEAL,width=node.width-.1).move_to(node))
  if self.INDEX==13:
   self.t5[1].become(text('Lane 0–3',16,GREEN,width=self.t5.width-.1).move_to(self.t5));self.t6[1].become(text('주소 요청',16,ORANGE,width=self.t6.width-.1).move_to(self.t6))
   for node,label in zip(self.slots,['Bank 0','Bank 1','… Bank 31']):node[1].become(text(label,12,TEAL,width=node.width-.1).move_to(node))
  self.shot();self.to(self.meta['end'])
  layout='shorts' if SHORT else 'longform'
  for name,data in [('geometry',self.bounds),('states',self.trace)]: (P/f'{name}_{layout}_{self.INDEX:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 def code(self,active=(),lines=None,label='neighborRead.cu · 핵심 발췌'):
  super().code(active,CODE if lines is None else lines,label)
 def world(self):
  self.sm=RoundedRectangle(width=4.7,height=1.65,corner_radius=.1,color=BLUE).move_to([-1.15,-.02,0])
  self.t5=box('Thread 5',1.1,.36,GREEN,19).move_to([-2.75,.3,0]);self.t6=box('Thread 6',1.1,.36,ORANGE,19).move_to([-1.4,.3,0]);self.reg=box('Register',1.25,.36,PURPLE,17).move_to([.1,.3,0])
  self.shared=box('',4.25,.69,TEAL).move_to([-1.2,-.4,0]);self.slots=VGroup(*(box(f'{k}: {100+k}',1.1,.23,TEAL,13).move_to([-2.6+j*1.3,-.55,0]) for j,k in enumerate([5,6,7])))
  self.globalmem=box('Global / L2',1.9,.48,BLUE,19).move_to([2.4,.22,0]);dram=box('Device DRAM',1.9,.44,MUTED,17).move_to([2.4,-.5,0])
  self.footer=text('SM 내부 자원 · Block 0에 할당',14,MUTED).move_to([0,-1.04,0])
  self.map=VGroup(RoundedRectangle(width=7.65,height=2.5,corner_radius=.14,color=BLUE,fill_color=PANEL,fill_opacity=.5),self.sm,self.shared,self.t5,self.t6,self.reg,self.slots,self.globalmem,dram,text('GPU DEVICE · 메모리 관계도',18,BLUE).move_to([0,1.02,0]),text('SM 0',16,BLUE).move_to([-3.1,.65,0]),text('Shared Memory · Block 0',16,TEAL).move_to([-1.2,-.24,0]),self.footer)
  self.map.scale(1 if SHORT else .87).move_to([0,4.4,0] if SHORT else [-3.65,1.45,0]);self.add(self.map)
 def msg(self,s):self.footer.become(text(s,14,TEAL,width=7*(1 if SHORT else .87)).move_to(self.footer))
 def detail(self,g):
  self.place(g,self.dc,self.dw,self.dh)
  if hasattr(self,'dg'):self.play(ReplacementTransform(self.dg,g),run_time=.35)
  else:self.add(g)
  self.dg=g;return g
 def cards(self,title,labels,col=TEAL):return stack(text(title,27,col),VGroup(*(box(s,1.5,.65,col,23) for s in labels)).arrange(RIGHT,buff=.18))
 def move_value(self,value,nodes,col=TEAL,label='데이터 이동'):
  self.msg(label);p=box(str(value),.56,.32,col,17).move_to(nodes[0]);p[0].set_fill(PANEL,opacity=1);p[1].set_color(INK);self.add(p)
  for n in nodes[1:]:self.play(p.animate.move_to(n),Indicate(n,color=col,scale_factor=1.04),run_time=.35)
  self.play(FadeOut(p),run_time=.1);self.trace.append(dict(time=self.start+self.time,value=value,label=label))
 def read(self,t=5):self.move_value(106 if t==5 else 107,[self.slots[1 if t==5 else 2],self.t5 if t==5 else self.t6],GREEN if t==5 else ORANGE,f'동기화 후 · Thread {t}가 이웃 값 읽기')
 def tiles(self,second=False):
  vals=([3,4,7,8],[9,10,13,14]) if second else ([1,2,5,6],[1,2,5,6]);groups=[]
  for name,vs in zip(['Shared A','Shared B'],vals):
   cells=VGroup(*(box(str(v),.68,.52,TEAL,24) for v in vs)).arrange_in_grid(rows=2,buff=.08);groups.append(stack(text(name,21,TEAL),cells,buff=.15))
  g=VGroup(*groups).arrange(RIGHT,buff=.7);return stack(text('별도 GEMM · N=4 / TILE=2 / Block=2×2',21,MUTED),g,buff=.2)
 def shot(self):
  i=self.INDEX
  if i==0:
   self.detail(self.cards('각 Thread의 계산 값', ['T5: 105','T6: 106'],PURPLE));self.to(5);self.move_value('?', [self.t6,self.t5],MUTED,'일반 지역 변수는 다른 Thread에서 직접 공유하지 않음');self.to(10);self.play(Indicate(self.shared,color=TEAL),run_time=.7);self.detail(self.cards('공유할 공간을 따로 둔다',['Shared','Block 0']))
  elif i==1:
   self.detail(self.cards('같은 Block의 Thread들이 접근',['T5','Shared','T6']));self.to(19);self.move_value('개별',[self.t5,self.reg],PURPLE,'Register · Thread별 할당');self.to(23);self.move_value('공유',[self.t6,self.shared,self.t5],TEAL,'Shared · 같은 Block에서 공유 가능')
  elif i==2:
   self.detail(self.cards('128개의 float · 512 bytes',['s[0]','…','s[127]']));self.to(29);self.code([0]);self.play(Indicate(self.shared),run_time=.5);self.to(35);self.code([1]);self.move_value(105,[self.globalmem,self.t5,self.slots[0]],GREEN,'A[5] → Thread 5 → s[5]');self.move_value(106,[self.globalmem,self.t6,self.slots[1]],ORANGE,'A[6] → Thread 6 → s[6]')
  elif i==3:
   self.detail(self.cards('쓰기 위치와 읽기 위치가 다르다',['s[5]=105','s[6]=106']));self.code([1]);self.move_value(105,[self.t5,self.slots[0]],GREEN,'Thread 5가 s[5]에 기록');self.move_value(106,[self.t6,self.slots[1]],ORANGE,'Thread 6이 s[6]에 기록');self.to(45);self.code([3]);self.note('이 읽기는 모든 쓰기와 동기화가 완료된 상태를 가정');self.read()
  elif i==4:
   b=self.detail(self.cards('Block마다 별도의 배열',['Block 0: s','Block 1: s']));self.msg('Block 1은 Block 0의 Shared 배열을 직접 읽을 수 없음');self.play(Indicate(b[1][0]),run_time=.6);self.to(51);self.play(Indicate(b[1][1],color=ORANGE),run_time=.6)
  elif i==5:
   self.slots[1][1].become(text('6: ?',13,ORANGE).move_to(self.slots[1]));self.detail(self.cards('쓰기 완료 전의 읽기 · 설명용',['s[6] = ?','결과 보장 X'],ORANGE));self.to(57);self.move_value('?', [self.slots[1],self.t5],ORANGE,'쓰기 완료 전이라면 읽기 결과를 보장할 수 없음');self.to(59);self.code([2]);self.msg('__syncthreads() · 올바른 순서를 만든다')
  elif i==6:
   self.code([2]);self.note('도착 순서는 설명용 · 실제 Warp 실행 추적 아님')
   for at,n in [(62,32),(64,64),(66,96),(69,128)]:
    self.to(at);self.detail(self.cards('Block 동기화 지점 도착',[f'{n} / 128','대기' if n<128 else '읽기 허용']));self.play(Indicate(self.shared,color=TEAL),run_time=.35);self.msg(f'{n}/128 도착 · '+('아직 읽기 대기' if n<128 else '이전 Shared 쓰기 관찰 보장'))
   self.to(70);self.code([3]);self.read();self.to(72);self.read(6)
  elif i==7:
   self.detail(self.cards('데이터 전달을 넘어',['한 번 로드','여러 번 사용']));self.to(79);self.detail(self.tiles());self.code([0],['__shared__ float As[2][2];','__shared__ float Bs[2][2];'],label='tiledGemm.cu · 별도 예제');self.move_value('Tile',[self.globalmem,self.shared],TEAL,'이제 별도 행렬곱 예제 · 2×2 Thread Block')
  elif i==8:
   self.detail(self.cards('출력은 달라도 입력은 겹친다',['C[0,0]','C[0,1]']));self.code([],['sum += A[row*4+k]','     * B[k*4+col];'],label='단순 GEMM · 발췌');self.to(86);self.move_value('A00=1',[self.globalmem,self.t5],GREEN,'같은 A[0,0]을 첫 번째 출력에 사용');self.move_value('A00=1',[self.globalmem,self.t6],ORANGE,'같은 입력을 두 번째 출력에서도 사용');self.note('상단 Thread 노드는 데이터 경로 설명용 · 이 GEMM은 별도 2×2 Block')
  elif i==9:
   g=self.detail(self.tiles());self.code([0,1],['As[ty][tx] = A[row*4+m*2+tx];','Bs[ty][tx] = B[(m*2+ty)*4+col];','__syncthreads();'],label='tiledGemm.cu · Tile Load');self.move_value('A tile',[self.globalmem,self.shared],GREEN,'Global → Shared A · 4개 원소');self.to(95);self.move_value('B tile',[self.globalmem,self.shared],ORANGE,'Global → Shared B · 4개 원소');self.play(Indicate(g,color=TEAL),run_time=.6);self.note('K 방향 첫 Tile · A 4개 + B 4개 입력 원소 요청')
  elif i==10:
   self.detail(self.tiles());self.code([0],['sum += As[ty][k] * Bs[k][tx];','// k = 0, 1','__syncthreads();'],label='tiledGemm.cu · 재사용 / 다음 Tile 전 동기화');self.move_value('A00=1',[self.shared,self.t5],GREEN,'같은 Shared 입력 → 출력 C[0,0]');self.move_value('A00=1',[self.shared,self.t6],ORANGE,'같은 Shared 입력 → 출력 C[0,1]');self.to(103);self.detail(self.tiles(True));self.move_value('다음 Tile',[self.globalmem,self.shared],TEAL,'K 방향 두 번째 Tile로 교체 · 누적 계산');self.to(106);self.detail(self.cards('두 Tile 누적 · 출력 4개',['90','100','202','228']));self.msg('입력 Tile은 공유 · 각 출력 누적값은 Thread별 Register')
  elif i==11:
   self.detail(self.cards('같은 출력 4개 · 입력 원소 요청',['단순 32개','Tile 16개']));self.code([],['// 4 outputs × 4 K × 2 = 32','// 2 tiles × (4 A + 4 B) = 16'],label='소스 수준의 요청 원소 수');self.move_value('16',[self.globalmem,self.shared],TEAL,'Global 요청의 중복 감소 · 실측 DRAM 전송량 아님');self.note('캐시·트랜잭션·속도 2배를 뜻하지 않음')
  elif i==12:
   self.code([],['// Hypothetical SM budget: 64 KiB','// Per Block: 8 -> 16 KiB'],label='자원 제약 · 가상 수치');self.detail(self.cards('Shared 예산 64 KiB · 다른 제약 제외',['8 KiB/Block','8 Blocks']));self.to(116);self.move_value('8→16',[self.globalmem,self.shared],ORANGE,'Block당 Shared 사용량 증가');self.to(119);self.detail(self.cards('같은 예산에서 상주 Block 감소',['16 KiB/Block','4 Blocks'],ORANGE));self.note('가상 예산 예시 · neighborRead의 실제 Shared는 512 bytes')
  elif i==13:
   self.code([],['// 32-bit word: bank = address % 32','// 4 active lanes: stride 1 or 32'],label='bankRead.cu · 32개 Bank 모델');self.note('32개 Bank 중 4개만 표시 · 서비스 단계는 설명용')
   self.detail(self.cards('Shared 내부 Bank · 서로 다른 주소',['B0','B1','B2','B3']));self.to(126)
   for k in range(4):self.move_value(k,[self.t5,self.shared],TEAL,f'Lane {k} · word {k} → Bank {k} · 충돌 없음')
   self.to(129);self.detail(self.cards('서로 다른 주소가 같은 Bank로',['0','32','64','96'],ORANGE))
   for k in range(4):self.move_value(k*32,[self.t6,self.shared],ORANGE,f'word {k*32} → Bank 0 · 분할 처리 단계 {k+1}/4')
   self.to(133);self.msg('Bank Conflict · 같은 주소를 읽는 Broadcast는 별도 예외');self.note('동일 주소 Broadcast는 이 충돌 예제에 해당하지 않음')
  elif i==14:
   self.detail(self.cards('재사용의 이점과 비용',['재사용','동기화','접근 패턴']));self.code([],['// reuse benefit','// synchronization cost','// bank access pattern'],label='성능은 함께 측정해야 한다');self.move_value('재사용',[self.shared,self.t5,self.shared,self.t6],TEAL,'한 번 가져온 데이터를 다시 사용');self.to(139);self.play(Indicate(self.shared,color=ORANGE),run_time=.7);self.msg('Shared 사용만으로 성능 향상을 보장하지 않음')
  elif i==15:
   self.detail(self.cards('값의 사용 범위를 구분한다',['Register: 개별','Shared: Block']));self.move_value(105,[self.t5,self.reg],PURPLE,'Register · Thread별 계산값');self.to(148);self.move_value(106,[self.t6,self.slots[1],self.t5],TEAL,'쓰기·동기화 후 · 같은 Block의 다른 Thread가 읽기')
  else:
   self.detail(self.cards('효율적인 데이터 이동과 재사용',['Global','Shared','Thread']));self.code([1,2,3]);self.move_value(106,[self.globalmem,self.t6,self.slots[1]],ORANGE,'필요한 데이터를 Shared에 가져오기');self.to(155);self.read();self.to(157);self.move_value(106,[self.slots[1],self.t6],TEAL,'같은 Block의 계산에 다시 사용');self.note('많은 Thread + 필요한 데이터의 효율적인 이동과 재사용')
