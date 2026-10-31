"""SM-owned register resources; source variables are not physical slot labels."""
import json
from pathlib import Path
from manim import *
from shared_style import StyleScene,text,box,stack,SHORT,INK,MUTED,BLUE,GREEN,ORANGE,PURPLE,PANEL
P=Path(__file__).resolve().parent
CODE=['float a = A[i];','float b = B[i];','float sum = a + b;','C[i] = sum;']
class RegisterBase(StyleScene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start'];self.bounds=[];self.trace=[]
        self.dc=np.array([0,1.08,0]) if SHORT else np.array([-3.65,-1.07,0]);self.dw=7.65 if SHORT else 7.1;self.dh=3.1 if SHORT else 2.6
        self.cc=np.array([0,-2.85,0]) if SHORT else np.array([4.15,.1,0]);self.cw=7.65 if SHORT else 6.15;self.ch=4.05 if SHORT else 4.7
        self.add(text('GPU HIERARCHY  /  LEVEL 06',19,MUTED).move_to([0,7.35 if SHORT else 4,0]),text(self.meta['title'],33,width=8 if SHORT else 14).move_to([0,6.45 if SHORT else 3.2,0]))
        self.world_map();self.resource_board();self.code();self.note('Register File은 SM의 자원 · Thread별 할당')
        self.shot();self.to(self.meta['end'])
        self.trace.append(dict(kind='final_identity',thread=2,block=0,sm=0,register_location='SM 0',mini_thread_center=self.thread_node.get_center().tolist(),register_center=self.register_bar.get_center().tolist()))
        layout='shorts' if SHORT else 'longform'
        for name,data in [('geometry',self.bounds),('states',self.trace)]:
            (P/f'{name}_{layout}_{self.INDEX:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    def record(self,g):self.bounds.append(dict(time=round(self.start+self.time,4),left=float(g.get_left()[0]),right=float(g.get_right()[0]),bottom=float(g.get_bottom()[1]),top=float(g.get_top()[1])))
    def world_map(self):
        if self.INDEX==0:self.execution_map();return
        self.memory_map()
    def memory_map(self,add=True):
        center=np.array([0,4.4,0]) if SHORT else np.array([-3.65,1.45,0]);sc=1 if SHORT else .87
        outer=RoundedRectangle(width=7.65,height=2.5,corner_radius=.14,stroke_color=BLUE,stroke_width=1.6,fill_color=PANEL,fill_opacity=.5)
        self.sm_frame=RoundedRectangle(width=4.7,height=1.68,corner_radius=.1,stroke_color=BLUE,stroke_width=1.8).move_to([-1.15,-.03,0])
        self.thread_node=box('Thread 2',1.28,.4,BLUE,20).move_to([-2.65,.25,0])
        self.register_bar=box('Register File',2.5,.5,PURPLE,24,fill=.22).move_to([-.45,.25,0])
        self.shared_node=box('Shared Memory',2.22,.4,MUTED,18,fill=.04).move_to([-2.15,-.48,0])
        self.l1_node=box('L1 Cache',1.62,.4,ORANGE if self.INDEX in [12,13] else MUTED,18,fill=.07).move_to([.0,-.48,0])
        self.l2_node=box('L2 Cache',1.78,.48,BLUE if self.INDEX in [12,13] else MUTED,21,fill=.07).move_to([2.4,.23,0])
        self.dram_node=box('Device DRAM',1.93,.48,MUTED,19,fill=.05).move_to([2.4,-.5,0])
        alloc=Arrow(self.thread_node.get_right(),self.register_bar.get_left(),buff=.055,color=PURPLE,stroke_width=2,max_tip_length_to_length_ratio=.25)
        link=DashedLine(self.l1_node.get_right(),self.l2_node.get_left(),color=ORANGE if self.INDEX in [12,13] else MUTED,stroke_width=1.5,dash_length=.06)
        offchip=DoubleArrow(self.l2_node.get_bottom(),self.dram_node.get_top(),buff=.04,color=MUTED,stroke_width=1.5,max_tip_length_to_length_ratio=.25)
        labels=VGroup(text('GPU DEVICE · 메모리 관계도',19,BLUE).move_to([0,1.02,0]),text('SM 0',18,BLUE).move_to([-3.08,.64,0]),text('사용',13,PURPLE).move_to([-1.86,.56,0]),text('소유 범위 개념도 · Shared/L1 물리 자원 공유 가능',15,MUTED,width=7.1).move_to([0,-1.06,0]))
        g=VGroup(outer,self.sm_frame,link,offchip,self.thread_node,self.register_bar,self.shared_node,self.l1_node,self.l2_node,self.dram_node,alloc,labels)
        g.scale(sc).move_to(center);self.map_group=g;self.warp_nodes=[self.thread_node];self.map_scale=sc;self.map_footer=labels[-1];self.ledger=None;self.budget_strip=None;self.status_badge=None;self.loaded_values=[]
        if add:self.add(g)
        self.record(g)
        identity=dict(kind='identity',time=round(self.start+self.time,4),thread=2,block=0,sm=0,register_location='SM 0',mini_thread_center=self.thread_node.get_center().tolist(),register_center=self.register_bar.get_center().tolist(),sm_bounds=[float(self.sm_frame.get_left()[0]),float(self.sm_frame.get_right()[0]),float(self.sm_frame.get_bottom()[1]),float(self.sm_frame.get_top()[1])])
        self.trace.append(identity)
        def bounds(n):return [float(n.get_left()[0]),float(n.get_right()[0]),float(n.get_bottom()[1]),float(n.get_top()[1])]
        self.trace.append(dict(kind='memory_layout',time=round(self.start+self.time,4),thread=2,mini_thread_center=identity['mini_thread_center'],register_center=identity['register_center'],sm=bounds(self.sm_frame),register=bounds(self.register_bar),shared=bounds(self.shared_node),l1=bounds(self.l1_node),l2=bounds(self.l2_node),dram=bounds(self.dram_node),register_parent='SM 0',l2_scope='GPU-wide',dram_location='device memory outside SM',register_to_shared_serial_path=False))
    def execution_map(self):
        center=np.array([0,4.4,0]) if SHORT else np.array([-3.65,1.45,0]);sc=1 if SHORT else .87
        gpu=RoundedRectangle(width=7.65,height=2.5,corner_radius=.14,stroke_color=BLUE,stroke_width=1.6,fill_color=PANEL,fill_opacity=.4)
        self.sm_frame=RoundedRectangle(width=7.1,height=1.85,corner_radius=.1,stroke_color=BLUE,stroke_width=2).shift(DOWN*.12)
        g=VGroup(gpu,self.sm_frame,text('GPU',19,BLUE).move_to([-3.15,1.02,0]),text('SM 0',19,BLUE).move_to([-2.95,.62,0]),text('실행 구조와 저장 자원',16,MUTED).move_to([1.9,1.02,0]))
        self.warp_nodes=[]
        for b,x in [(0,-1.72),(1,1.72)]:
            border=DashedVMobject(RoundedRectangle(width=3.15,height=.88,corner_radius=.07),num_dashes=25).set_color(MUTED).move_to([x,.05,0])
            label=text(f'Block {b} · 128 Thread',15,MUTED).move_to([x,.21,0])
            warps=VGroup(*(box(f'W{w+b*4}',.6,.26,BLUE if b==0 and w==0 else MUTED,12).move_to([x+(w-1.5)*.67,-.02,0]) for w in range(4)))
            g.add(border,label,warps)
            if b==0:self.warp_nodes=warps
        self.register_bar=box('SM Register File · Thread별 할당',6.1,.38,PURPLE,18).move_to([0,-.67,0]);g.add(self.register_bar)
        self.thread_node=box('T2',.46,.16,BLUE,10).move_to([-2.76,-.29,0]);g.add(self.thread_node)
        g.scale(sc).move_to(center);self.map_group=g;self.add(g);self.record(g)
        self.trace.append(dict(kind='identity',time=self.start,thread=2,block=0,sm=0,register_location='SM 0',mini_thread_center=self.thread_node.get_center().tolist(),register_center=self.register_bar.get_center().tolist(),sm_bounds=[float(self.sm_frame.get_left()[0]),float(self.sm_frame.get_right()[0]),float(self.sm_frame.get_bottom()[1]),float(self.sm_frame.get_top()[1])]))
    def code(self,active=(),lines=None,label='vectorAdd.cu  ·  발췌'):
        lines=CODE if lines is None else lines;self.active_code=[lines[k] for k in active];super().code(active,lines,label)
    def detail(self,g):
        old=getattr(self,'dg',None);self.place(g,self.dc,self.dw,self.dh)
        if old is not None and self.time>.01:self.play(ReplacementTransform(old,g),run_time=.4)
        else:
            if old is not None:self.remove(old)
            self.add(g)
        self.dg=g;return g
    def map_message(self,s,col=MUTED):
        self.map_footer.become(text(s,14,col,width=7.1*self.map_scale).move_to(self.map_footer))
    def ledger_value(self,s,col=GREEN,animate=True):
        target=text(s,16,col,width=2.3*self.map_scale).move_to(self.register_bar.get_bottom()+DOWN*.14*self.map_scale)
        if self.budget_strip is not None:self.remove(self.budget_strip);self.budget_strip=None
        if self.ledger is not None:
            if animate:self.play(ReplacementTransform(self.ledger,target),run_time=.25)
            else:self.remove(self.ledger);self.add(target)
        else:
            if animate:self.play(FadeIn(target,shift=UP*.04),run_time=.2)
            else:self.add(target)
        self.ledger=target
    def map_transfer(self,operation,value,nodes,label,col=GREEN):
        begin=round(self.start+self.time,4);self.map_message(label,col)
        packet=box(str(value),.55*self.map_scale,.34*self.map_scale,col,18*self.map_scale).move_to(nodes[0]);packet[0].set_fill(PANEL,opacity=1);packet[1].set_color(INK)
        self.add(packet)
        for node in nodes[1:]:
            self.play(packet.animate.move_to(node),Indicate(node,color=col,scale_factor=1.025),run_time=.3)
        self.play(FadeOut(packet),run_time=.1)
        names={id(self.register_bar):'Register',id(self.l1_node):'L1',id(self.l2_node):'L2',id(self.dram_node):'DRAM'}
        self.trace.append(dict(kind='map_motion',operation=operation,value=value,start=begin,end=round(self.start+self.time,4),route=[names.get(id(n),'Thread') for n in nodes],active_code=self.active_code.copy(),conceptual=True))
    def map_load(self,value,name):
        self.map_transfer('load',value,[self.l2_node,self.l1_node,self.register_bar],f'{name} Load · L2 적중을 가정한 접근 경로',BLUE if value==3 else PURPLE)
        self.loaded_values.append(value);self.ledger_value('값 '+', '.join(str(v) for v in self.loaded_values),BLUE)
    def map_compute(self):
        self.ledger_value('3 + 4',BLUE,False);self.map_message('Thread 2의 계산 값 3 + 4 → 7 · 물리 슬롯 배치 아님',GREEN)
        new=text('7',21,GREEN).move_to(self.ledger)
        self.play(ReplacementTransform(self.ledger,new),Indicate(self.thread_node,color=GREEN,scale_factor=1.06),Indicate(self.register_bar,color=GREEN,scale_factor=1.025),run_time=.6);self.ledger=new
        self.trace.append(dict(kind='map_motion',operation='add',value=7,start=round(self.start+self.time-.6,4),end=round(self.start+self.time,4),active_code=self.active_code.copy(),conceptual=True))
    def map_store(self):
        self.map_transfer('store',7,[self.register_bar,self.l2_node],'C[2] Store 요청 → L2 · DRAM 쓰기 완료를 뜻하지 않음',GREEN)
    def map_budget(self,r,animate=True):
        if self.ledger is not None:self.remove(self.ledger);self.ledger=None
        n=32768//(128*r);width=2.25*self.map_scale;gap=.025*self.map_scale
        strip=VGroup(*(Rectangle(width=(width-gap*(n-1))/n,height=.105*self.map_scale,color=BLUE if k==0 else PURPLE,stroke_width=.6,fill_color=BLUE if k==0 else PURPLE,fill_opacity=.72) for k in range(n))).arrange(RIGHT,buff=gap).move_to(self.register_bar.get_bottom()+DOWN*.14*self.map_scale)
        badge=text(f'{r}R/T · {n}B / {n*4}W',12,ORANGE,width=2.6*self.map_scale).move_to(self.register_bar.get_center()+UP*.41*self.map_scale)
        animations=[]
        for name,target in [('budget_strip',strip),('status_badge',badge)]:
            old=getattr(self,name,None)
            if animate:animations.append(ReplacementTransform(old,target) if old is not None else FadeIn(target))
            else:
                if old is not None:self.remove(old)
                self.add(target)
            setattr(self,name,target)
        self.map_message('가상 예산: 한 Block의 할당 폭 증가 → 상주 Block·Warp 감소',ORANGE)
        if animate:self.play(*animations,run_time=.7)
        self.trace.append(dict(kind='map_budget',time=round(self.start+self.time,4),registers_per_thread=r,block_count=n,warp_count=n*4,segments=n,segment_fraction=1/n,hypothetical=True))
    def map_private_allocation(self):
        cells=VGroup(*(box(f'T{k}',.48*self.map_scale,.18*self.map_scale,BLUE if k==2 else PURPLE,10*self.map_scale) for k in range(4))).arrange(RIGHT,buff=.05*self.map_scale).move_to(self.register_bar.get_bottom()+DOWN*.14*self.map_scale)
        if self.ledger is not None:self.remove(self.ledger);self.ledger=None
        self.map_message('같은 SM 자원 · Thread마다 전용 할당 · 물리 주소 배열은 개념도',PURPLE)
        self.budget_strip=cells
        for cell in cells:self.play(FadeIn(cell,shift=UP*.05),run_time=.18)
        self.play(Indicate(cells[2],color=GREEN,scale_factor=1.12),Indicate(self.thread_node,color=BLUE,scale_factor=1.04),run_time=.4)
        self.trace.append(dict(kind='map_motion',operation='private_allocation',value=2,start=round(self.start+self.time-1.12,4),end=round(self.start+self.time,4),conceptual=True))
    def resource_board(self):
        left=stack(box('Block 0 · Warp 0',2.7,.45,BLUE,20),box('Thread 2',2.7,.58,BLUE,28),text('논리적인 실행 문맥',18,MUTED),buff=.22)
        regions=VGroup(*(box(f'Thread {t} 할당 영역',3.5,.38,BLUE if t==2 else PURPLE,18,fill=.23 if t==2 else .07) for t in [0,1,2,3])).arrange(DOWN,buff=.12)
        right=stack(text('SM Register File',25,PURPLE),regions,text('Thread별 할당 · 물리 배열 단순화',16,MUTED),buff=.15)
        group=VGroup(left,right).arrange(RIGHT,buff=.55)
        link=Arrow(left.get_right(),right.get_left(),buff=.07,color=PURPLE,stroke_width=2)
        self.detail(VGroup(group,link));self.alloc_regions=regions
    def values(self,stage):
        cards=VGroup()
        data=[('A[2] → a','3',BLUE),('B[2] → b','4',PURPLE),('a + b → sum','7' if stage>=2 else '?',GREEN)]
        for label,value,col in data:
            cards.add(stack(text(label,22,col),box(value,1.55,.72,col,38),buff=.15))
        cards.arrange(RIGHT,buff=.5)
        self.detail(stack(text('Block 0 / Warp 0 / Thread 2',25,BLUE),cards,text('C[2] = 7' if stage>=3 else '소스 변수와 계산 값 · 물리 Register 슬롯 아님',25 if stage>=3 else 18,GREEN if stage>=3 else MUTED),buff=.25))
        self.trace.append(dict(kind='values',time=round(self.start+self.time,4),thread=2,a=3,b=4,sum=7 if stage>=2 else None,stored=stage>=3,physical_slot_mapping=False))
    def demand(self,r):
        demand=128*r
        cells=VGroup(*(Rectangle(width=.20,height=.21,stroke_width=.7,color=PURPLE,fill_color=PURPLE,fill_opacity=.52 if k<(8 if r==32 else 16) else .055) for k in range(16))).arrange_in_grid(rows=2,cols=8,buff=.08)
        self.detail(stack(text('가상 요구량 · 실제 vectorAdd 사용량 아님',21,ORANGE),text(f'128 Thread × {r} Registers',30,INK),text(f'{demand:,} Registers / Block',37,PURPLE),cells,text('32-bit Register 개수 · 할당 단위는 생략',17,MUTED),buff=.17))
        self.trace.append(dict(kind='demand',time=round(self.start+self.time,4),threads=128,registers_per_thread=r,total_registers=demand,hypothetical=True,register_bits=32))
    def residency(self,r):
        n=32768//(128*r);warps=n*4
        blocks=VGroup(*(box(f'B{k}',.62,.37,GREEN if k<n else MUTED,18,fill=.24 if k<n else .03) for k in range(8))).arrange_in_grid(rows=2,cols=4,buff=.13)
        self.detail(stack(text('가상 SM · Register 예산 32,768개',22,ORANGE),blocks,text(f'{r} Registers/Thread → {n} Blocks',27,PURPLE),text(f'{warps} Resident Warps / max 32',28,GREEN),text('Register만 고려 · 다른 제약과 할당 단위는 생략',17,MUTED),buff=.17))
        self.trace.append(dict(kind='residency',time=round(self.start+self.time,4),register_budget=32768,registers_per_thread=r,block_threads=128,resident_blocks=n,resident_warps=warps,max_warps=32,hypothetical=True,performance_ratio=None))
    def compiler(self):
        actual=json.loads((P/'cuda_trace.json').read_text())
        stages=VGroup(*(box(s,2.1,.67,col,20) for s,col in [('CUDA Source',BLUE),('Compiler',ORANGE),('SM Registers',PURPLE)])).arrange(RIGHT,buff=.3)
        self.detail(stack(stages,text('변수 하나 ≠ Register 하나',30,ORANGE),text('유효 수명 · 최적화 · 재사용에 따라 달라짐',20,MUTED),buff=.32))
        self.code(lines=['nvcc -Xptxas=-v ...',f'Used {actual["registers_per_thread"]} registers','0 bytes spill stores','0 bytes spill loads'],label='실제 컴파일 로그 · sm_86 / -O3')
        self.trace.append(dict(kind='compiler',registers=actual['registers_per_thread'],spill_stores=0,spill_loads=0,source_variables_equal_registers=False))
    def spill_diagram(self,phase=0):
        # Local memory is an address space. It is not drawn as an SM storage box.
        sm=box('SM · Register File',3.2,.58,PURPLE,24).move_to([-1.85,.8,0])
        scope=box('Thread 2 · Local 주소 공간',3.2,.58,ORANGE,20).move_to([1.85,.8,0])
        arrow=Arrow(sm.get_right(),scope.get_left(),buff=.05,color=ORANGE,stroke_width=2)
        row=VGroup(*(box(s,1.9,.55,c,21) for s,c in [('L1 Cache',BLUE),('L2 Cache',BLUE),('DRAM',MUTED)])).arrange(RIGHT,buff=.4).move_to([0,-.53,0])
        path=Arrow(scope.get_bottom(),row[0].get_top(),buff=.07,color=ORANGE,stroke_width=2)
        g=VGroup(sm,scope,arrow,row,path,text('Local = Thread 전용 범위 · 물리적 위치 이름 아님',19,ORANGE).move_to([0,1.43,0]),text('캐시 적중 시 DRAM 접근 없이 처리 가능',18,MUTED).move_to([0,-1.2,0]))
        self.detail(g)
        for k in range(2):g.add(Arrow(row[k].get_right(),row[k+1].get_left(),buff=.05,color=BLUE,stroke_width=2))
        if phase:
            packet=Dot(sm.get_center(),radius=.08,color=ORANGE);self.add(packet)
            self.play(packet.animate.move_to(scope),run_time=.45);self.play(packet.animate.move_to(row[0]),run_time=.45)
            self.play(packet.animate.move_to(sm),run_time=.55);self.remove(packet)
        self.trace.append(dict(kind='spill',time=round(self.start+self.time,4),scope='Thread 2 private local address space',backing=['L1','L2','DRAM'],cache_hit_possible=True,all_accesses_reach_dram=False,conceptual=True,not_actual_vectorAdd_spill=True))
    def tradeoff(self):
        left=stack(text('Register 사용 제한',25,BLUE),box('더 많은 Warp 상주 가능',3.25,.58,GREEN,20),box('Spill 접근 증가 가능',3.25,.58,ORANGE,20),buff=.2)
        right=stack(text('충분한 Register 활용',25,PURPLE),box('중간값을 빠르게 유지',3.25,.58,GREEN,20),box('상주 Warp 감소 가능',3.25,.58,ORANGE,20),buff=.2)
        return stack(VGroup(left,right).arrange(RIGHT,buff=.4),text('Register Usage ↔ Parallelism',29,INK),text('어느 쪽이 항상 빠른지는 사용량만으로 결정 못 함',18,MUTED),buff=.3)
    def shot(self):
        i=self.INDEX
        if i==0:
            self.code(lines=['Thread → Warp → Block','Block → SM','Execution → Memory'],label='같은 GPU 구조 · 저장 자원으로 이동');self.note('계산 중에 사용하는 값은 어디에 있을까?')
            self.to(5);self.pulse(self.warp_nodes[0]);self.to(9)
            previous=self.map_group;self.memory_map(add=False);self.play(ReplacementTransform(previous,self.map_group),run_time=1.2)
            self.to(14);self.note('실행 구조 → 메모리 계층',PURPLE);self.to(18);self.map_private_allocation()
        elif i==1:
            self.code([0,1,2]);self.note('Register: 연산 값과 중간 결과를 빠르게 보관');self.map_private_allocation();self.to(27);self.values(0);self.to(30);self.pulse(self.cg)
        elif i==2:
            self.values(0);self.code([0]);self.note('Thread 2 → A[2]=3 / B[2]=4');self.map_load(3,'A[2]');self.code([1]);self.map_load(4,'B[2]')
            self.to(36);self.code([2]);self.values(2);self.map_compute()
            self.to(39);self.code([3]);self.values(3);self.map_store();self.note('Thread 2의 출력 C[2] = 7',GREEN)
        elif i==3:
            self.values(2);self.ledger_value('계산 값 3, 4 → 7',GREEN,False);self.code([0,1,2]);self.note('이 값들은 Register에 보관될 수 있다',PURPLE);self.to(44);self.note('소스 변수 3개가 물리 Register 3개라는 뜻은 아니다',ORANGE);self.map_compute()
        elif i==4:
            self.compiler();self.note('컴파일러가 Register 할당을 결정');self.to(51);self.ledger_value('12 Registers / Thread · 실측',PURPLE);self.pulse(self.cg);self.map_private_allocation()
        elif i==5:
            self.resource_board();self.code(lines=['Thread 2: private values','SM 0: Register File','Compiler assigns resources'],label='논리 실행 문맥과 물리 저장 자원');self.note('Thread 안에 별도의 물리 메모리를 설치한 구조가 아님');self.to(59);self.map_private_allocation();self.pulse(self.alloc_regions[2])
        elif i==6:
            self.resource_board();self.code(lines=['T0 → assigned resources','T1 → assigned resources','T2 → assigned resources'],label='Thread별 전용 할당 · 개념도');self.note('같은 SM 자원이지만 다른 Thread의 값을 임의로 직접 접근하지 않음');self.map_private_allocation();self.pulse(self.alloc_regions[2]);self.to(67);self.note('실제 Register File의 주소·물리 배열을 그린 그림은 아님',ORANGE)
        elif i==7:
            self.code(lines=['SM Register File','Limited Capacity','Block: 128 Threads'],label='빠르지만 한정된 자원');self.note('여러 상주 Block이 제한된 Register 자원을 나누어 사용');self.to(71);self.pulse(self.register_bar);self.to(75);self.detail(stack(text('Block 0',30,BLUE),text('128 Threads / 4 Warps',34,INK),text('Thread 수는 이후 비교에서도 동일',22,MUTED),buff=.25))
        elif i==8:
            self.demand(32);self.code(lines=['// Hypothetical compiled kernel','128 threads * 32 registers','4096 registers / block'],label='가상 요구량 · 소스 변수 수 아님');self.note('실제 vectorAdd 로그와는 별도 예시',ORANGE);self.map_budget(32)
        elif i==9:
            self.map_budget(32,False);self.demand(64);self.code(lines=['// Same 128-thread block','128 threads * 64 registers','8192 registers / block'],label='가상 요구량 · 32-bit Register 수');self.note('4,096 → 8,192 · 요구량 2배',PURPLE);self.map_budget(64);self.to(91);self.pulse(self.dg)
        elif i==10:
            self.residency(32);self.map_budget(32,False);self.code(lines=['// Register-only budget model','32768 / 4096 = 8 blocks','32768 / 8192 = 4 blocks'],label='실제 GPU 사양이 아닌 설명용 예산');self.note('Block마다 128 Thread · 4 Warp');self.to(99);self.residency(64);self.map_budget(64);self.to(102);self.note('Register Pressure · 동시 상주 규모를 제한할 수 있음',ORANGE)
        elif i==11:
            self.residency(64);self.map_budget(64,False);self.code(lines=['Register Pressure','Resident Warps','Occupancy / Latency Hiding'],label='자원과 명령 발행 기회의 연결');self.note('상주 Warp 감소가 실제 성능 하락을 항상 뜻하지는 않음');self.to(108)
            rows=VGroup(*(box(s,6,.48,c,24) for s,c in [('Warp 0 · Waiting for Data',ORANGE),('Warp 1 · Ready → Issue',GREEN),('더 적은 상주 Warp → 선택 기회 제약 가능',MUTED)])).arrange(DOWN,buff=.2)
            self.detail(stack(text('SM 0 · Warp Scheduler',28,BLUE),rows,buff=.25));self.map_message('Warp 0 데이터 대기 → Ready Warp 1의 명령 발행',GREEN);self.play(self.thread_node.animate.set_color(ORANGE),Indicate(self.register_bar,color=GREEN,scale_factor=1.03),run_time=.55);self.play(self.thread_node.animate.set_color(BLUE),run_time=.3)
        elif i==12:
            self.code(lines=['// Compiler-level concept','spill_store(value);','...','value = spill_load();'],label='컴파일된 명령의 개념 · CUDA 원문 아님');self.note('Pressure가 높다고 반드시 Spilling이 생기는 것은 아님',ORANGE);self.to(117);self.spill_diagram();self.map_transfer('spill_store','값',[self.register_bar,self.l1_node,self.l2_node],'별도 가정: Spill Store 경로 · 실제 vectorAdd는 Spill 0',ORANGE);self.to(121);self.note('Register Spilling · 일부 값을 메모리에 보관',ORANGE)
        elif i==13:
            self.spill_diagram();concept=['// Compiler-level concept','spill_store(value);','...','value = spill_load();'];self.code([1],concept,label='개념적 Spill Load / Store · 실제 trace 아님');self.note('Local Memory는 Thread 전용 주소 공간');self.to(127);self.map_transfer('spill_store','값',[self.register_bar,self.l1_node,self.l2_node],'별도 Spill Store 예시 · Local은 Thread 전용 주소 공간',ORANGE)
            self.to(133);self.code([3],concept,label='개념적 Spill Load / Store · 실제 trace 아님');self.map_transfer('spill_load','값',[self.l2_node,self.l1_node,self.register_bar],'별도 Spill Load 예시 · L2 적중 시 DRAM 접근 없음',ORANGE);self.spill_diagram(1);self.note('추가 메모리 접근 · 캐시 적중 여부에 따라 경로가 달라짐',ORANGE)
        elif i==14:
            self.detail(self.tradeoff());self.map_budget(64,False);self.code(lines=['More registers ?','Fewer registers ?','No universal winner'],label='Register 개수만으로 성능을 정할 수 없다');self.note('Spilling과 상주 Warp 제한은 서로 다른 제약');self.to(140);self.map_budget(32)
        elif i==15:
            self.detail(self.tradeoff());self.map_budget(32,False);self.code(lines=['Register Usage','    ↕','Parallelism / Memory Access'],label='사용량과 병렬 실행의 균형');self.note('충분한 중간값 보관과 상주 규모를 함께 고려');self.to(147);self.map_budget(64);self.to(150);self.note('실제 실행 성능은 다른 병목과 코드 구조에도 영향받는다',ORANGE)
        elif i==16:
            self.resource_board();self.code([0,1,2,3]);self.note('빠른 계산 값 보관 ↔ SM의 병렬 실행 규모',PURPLE);self.map_private_allocation();self.pulse(self.alloc_regions[2]);self.to(162);self.pulse(self.sm_frame)
        elif i==17:
            self.detail(stack(text('SM 0 · Thread 2',28,BLUE),box('3 + 4 = 7',5,.58,GREEN,33),box('SM Register File',5,.58,PURPLE,27),text('Register Usage ↔ Warp Scheduling',24,INK),text('Memory Resources Affect Parallel Execution',20,MUTED),buff=.2));self.note('연산 속도와 함께 데이터의 저장 위치·사용량을 본다',GREEN);self.code([0]);self.map_load(3,'A[2]');self.code([1]);self.map_load(4,'B[2]');self.to(170);self.code([2]);self.map_compute();self.to(172);self.code([3]);self.map_store()
