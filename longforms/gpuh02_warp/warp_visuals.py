"""One persistent 32-lane Warp: source, active mask and map change together."""
import json
from pathlib import Path
from manim import *
from shared_style import StyleScene,text,box,stack,SHORT,INK,MUTED,BLUE,GREEN,ORANGE,PURPLE,PANEL,COLS
P=Path(__file__).resolve().parent
ADD=['int i = threadIdx.x;','C[i] = A[i] + B[i];']
BRANCH=['int i = threadIdx.x;','if (i < 16) {','  A[i] = A[i] * 2.0f;','} else {','  A[i] = A[i] + 1.0f;','}']
class WarpBase(StyleScene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start']
        self.dc=np.array([0,1.5,0]) if SHORT else np.array([-3.65,-1.05,0]);self.dw=7.65 if SHORT else 7.1;self.dh=2.7 if SHORT else 2.15
        self.cc=np.array([0,-2.7,0]) if SHORT else np.array([4.15,.15,0]);self.cw=7.65 if SHORT else 6.15;self.ch=4.35 if SHORT else 4.7
        self.bounds=[];self.trace=[];self.selected=1;self.active_code=[];self.grid=None;self.mode='all'
        self.add(text('GPU HIERARCHY  /  LEVEL 02',19,MUTED).move_to([0,7.35 if SHORT else 4.,0]),text(self.meta['title'],34,width=8 if SHORT else 14).move_to([0,6.45 if SHORT else 3.2,0]))
        self.add(Line([-3.9,5.85,0],[3.9,5.85,0],color=MUTED,stroke_opacity=.25) if SHORT else Line([-7.3,2.7,0],[7.3,2.7,0],color=MUTED,stroke_opacity=.25))
        self.world_map()
        if self.INDEX>0:self.warp_grid(states=self.INDEX==16)
        self.shot();self.to(self.meta['end'])
        layout='shorts' if SHORT else 'longform'
        (P/f'geometry_{layout}_{self.INDEX:02}.json').write_text(json.dumps(self.bounds,indent=2),encoding='utf-8')
        (P/f'states_{layout}_{self.INDEX:02}.json').write_text(json.dumps(self.trace,ensure_ascii=False,indent=2),encoding='utf-8')
    def record_bounds(self,m):
        self.bounds.append(dict(time=self.start+self.time,left=float(m.get_left()[0]),right=float(m.get_right()[0]),bottom=float(m.get_bottom()[1]),top=float(m.get_top()[1])))
    def world_map(self):
        center=np.array([0,4.5,0]) if SHORT else np.array([-3.65,1.48,0]);scale=1 if SHORT else .86
        gpu=RoundedRectangle(width=7.65,height=2.5,corner_radius=.15,stroke_color=BLUE,stroke_width=1.8,fill_color=PANEL,fill_opacity=.45)
        sm=RoundedRectangle(width=7.1,height=1.68,corner_radius=.1,stroke_color='#7086A3',stroke_width=1.5).shift(DOWN*.18)
        nodes=VGroup(gpu,sm,text('GPU',19,BLUE).move_to([-3.2,1.02,0]),text('SM 0',20,INK).move_to([-2.95,.48,0]),text('실행 배치 개념도',16,MUTED).move_to([2.5,1.02,0]))
        self.mini=VGroup()
        for b,x in [(0,-1.78),(1,1.78)]:
            border=DashedVMobject(RoundedRectangle(width=3.16,height=.75,corner_radius=.08),num_dashes=30).set_color(MUTED).move_to([x,-.15,0])
            label=text(('Block 0' if self.INDEX==0 else 'Block 0 · Warp 0') if b==0 else '다른 Block',16,MUTED).move_to([x,.08,0])
            slots=VGroup(*(Square(side_length=.075,stroke_width=1,color=COLS[k%4],fill_color=BLUE,fill_opacity=.2) for k in range(32))).arrange_in_grid(rows=4,cols=8,buff=.025).move_to([x,-.29,0])
            if b==0:self.mini=slots;self.block_label=label
            else:border.set_opacity(.2);label.set_opacity(.35);slots.set_opacity(.15)
            nodes.add(border,label,slots)
        nodes.add(box('Register File',5.95,.38,PURPLE,17,fill=.07).move_to([0,-.73,0]))
        self.mini_warp=SurroundingRectangle(self.mini,buff=.035,color=GREEN,stroke_width=1.5)
        if self.INDEX==0:self.mini_warp.set_opacity(0)
        nodes.add(self.mini_warp);nodes.scale(scale).move_to(center)
        self.map_group=nodes;self.add(nodes);self.record_bounds(nodes)
        self.map_caption=text('GPU / SM 0 / Block 0',17,MUTED,width=7).move_to([center[0],3.12 if SHORT else .22,0]);self.add(self.map_caption)
        self.mini_ring=SurroundingRectangle(self.mini[1],buff=.025,color=GREEN,stroke_width=2);self.add(self.mini_ring)
    def warp_grid(self,states=False):
        border=RoundedRectangle(width=7,height=2.65,corner_radius=.14,stroke_color=GREEN,stroke_width=2)
        self.warp_title=text('Warp 0  ·  Lane 0–31',22,GREEN).move_to([0,1.1,0])
        cells=VGroup()
        for k in range(32):
            cell=box(str(k),.67,.44,COLS[k%4],21,fill=.13)
            cell.move_to([(k%8-3.5)*.82,.65-(k//8)*.53,0]);cells.add(cell)
        grid=VGroup(border,self.warp_title,cells)
        self.dots=VGroup()
        if states:
            self.dots=VGroup(*(Dot(c.get_center()+np.array([.23,-.12,0]),radius=.035,color=BLUE) for c in cells));grid.add(self.dots)
        factor=min(self.dw/grid.width,self.dh/grid.height,1);grid.scale(factor).move_to(self.dc)
        self.cells=cells;self.warp_border=border
        if self.grid is None:
            self.add(grid)
        else:self.remove(self.grid);self.add(grid)
        self.grid=grid;self.record_bounds(grid)
        self.trace.append(dict(kind='layout',time=round(self.start+self.time,4),lane_centers=[c.get_center().tolist() for c in cells],map_centers=[c.get_center().tolist() for c in self.mini]))
        if hasattr(self,'selection'):self.remove(self.selection)
        self.selection=SurroundingRectangle(cells[self.selected],buff=.035,color=COLS[self.selected%4],stroke_width=2)
        self.add(self.selection)
        if self.INDEX==0:
            border.set_opacity(0);self.warp_title.set_opacity(0)
    def select_lane(self,k,visible=True):
        self.selected=k
        self.mini_ring.become(SurroundingRectangle(self.mini[k],buff=.025,color=COLS[k%4],stroke_width=2)).set_fill(opacity=0).set_stroke(opacity=1 if visible else 0)
        if self.grid is not None:self.selection.become(SurroundingRectangle(self.cells[k],buff=.035,color=COLS[k%4],stroke_width=2)).set_fill(opacity=0).set_stroke(opacity=1 if visible else 0)
        self.trace.append(dict(time=round(self.start+self.time,4),selected_lane=k,kind='selection'))
    def code(self,active=(),lines=None,label='kernel.cu  /  CUDA C++'):
        lines=ADD if lines is None else lines
        self.active_code=[lines[n].strip() for n in active]
        super().code(active,lines,label)
    def active(self,mode='all',animate=False):
        self.mode=mode
        enabled=[k for k in range(32) if mode!='mul' and mode!='add' or mode=='mul' and k<16 or mode=='add' and k>=16]
        updates=[]
        for k in range(32):
            on=k in enabled;col=BLUE if mode in ['split','mul','add'] and k<16 else ORANGE if mode in ['split','mul','add'] else BLUE
            rect,label=self.cells[k];mini=self.mini[k]
            if animate:
                updates.extend([rect.animate.set_fill(col,opacity=.34 if on else .035).set_stroke(COLS[k%4] if on else MUTED,opacity=1 if on else .25),label.animate.set_opacity(1 if on else .27),mini.animate.set_fill(col,opacity=.65 if on else .02).set_stroke(COLS[k%4] if on else MUTED,opacity=1 if on else .2)])
            else:
                rect.set_fill(col,opacity=.34 if on else .035).set_stroke(COLS[k%4] if on else MUTED,opacity=1 if on else .25);label.set_opacity(1 if on else .27)
                mini.set_fill(col,opacity=.65 if on else .02).set_stroke(COLS[k%4] if on else MUTED,opacity=1 if on else .2)
        if updates:self.play(*updates,run_time=.4)
        mask=sum(1<<k for k in enabled)
        status='0–15: ×2  /  16–31: +1' if mode=='split' else f'Mask 0x{mask:08X} · {len(enabled)}/32 (개념도)'
        self.map_caption.become(text(status,17,MUTED,width=7).move_to(self.map_caption))
        self.select_lane(self.selected,False)
        self.trace.append(dict(time=round(self.start+self.time,4),kind='mask',mode=mode,mask=f'0x{mask:08X}',active_lanes=enabled,active_code=self.active_code))
    def emit(self):
        self.play(Indicate(self.warp_border,color=BLUE,scale_factor=1.012),*(Indicate(c,color=BLUE,scale_factor=1.02) for c in self.cells),run_time=.8)
    def result(self,k):
        self.select_lane(k);self.note(f'Thread {k}  ·  C[{k}] = {k+1} + {(k+1)*10} = {(k+1)*11}',COLS[k%4])
        self.play(Indicate(self.cells[k],color=COLS[k%4],scale_factor=1.04),run_time=.6)
    def branch_code(self,line=None):self.code([1] if line is None else [line],BRANCH,'branchExample.cu  ·  경로 개념도')
    def shot(self):
        i=self.INDEX
        if i==0:
            card=stack(box('Thread 1',3.4,.7,GREEN),text('Index · Data · State',29,GREEN),text('독립적인 실행 문맥',24,MUTED))
            self.place(card,self.dc,self.dw,self.dh);self.add(card)
            self.code(lines=['Thread 1','Index  /  Data  /  State'],label='선택한 실행 문맥');self.note('같은 GPU · SM 0 · Block 0')
            self.to(3);self.warp_grid();self.remove(self.grid,self.selection);self.play(FadeOut(card),TransformFromCopy(self.mini,self.grid),run_time=1.2);self.add(self.selection)
            self.note('이 Thread들은 실제로 어떻게 실행될까?',BLUE)
        elif i==1:
            self.active();self.code(lines=['32 Threads','1 Warp','Scheduling + Instruction'],label='Warp 0  ·  실행 그룹');self.note('Warp는 개별 물리 코어가 아닌 Thread 실행 그룹')
            self.play(Create(self.warp_border),Indicate(self.mini_warp,color=GREEN,scale_factor=1.03),run_time=1.2);self.to(12);self.emit()
        elif i==2:
            self.active();self.code(lines=['Warp 0 = 32 Threads','Lane Index = 0 ... 31'],label='Thread의 Warp 내부 위치');self.note('번호는 Lane Index · 칸은 같은 Thread의 실행 문맥')
            self.to(19);self.emit();self.to(22)
            for k in [0,7,15,23,31]:self.select_lane(k);self.play(Indicate(self.cells[k],scale_factor=1.04,color=COLS[k%4]),run_time=.6)
            self.to(27);self.note('Lane  =  Warp 안에서의 Thread 위치',GREEN)
        elif i==3:
            self.active();self.select_lane(6)
            self.code(lines=['Thread 6','Lane 6','Lane = threadIdx.x % 32'],label='1D Block의 Warp 내부 위치');self.note('이번 예시: 1 Block × 32 Thread · threadIdx.x = Lane')
            self.pulse(self.cells[6]);self.to(35)
            self.code(lines=['Thread 6  :  index = 6','A[6] = 7;  B[6] = 70;','Own data + own state','Warp 0    :  instruction'],label='개별 상태 · 같은 Warp');self.emit()
        elif i==4:
            self.active();self.code(lines=['SIMT','Single Instruction,','Multiple Threads'],label='실행 모델');self.note('같은 명령 · 서로 다른 데이터',GREEN);self.emit();self.to(46)
            self.code([0,1],ADD,'vectorAdd.cu  ·  발췌');self.note('vectorAdd<<<1, 32>>>(A, B, C);')
        elif i==5:
            self.active();self.code([1],ADD,'vectorAdd.cu  ·  발췌');self.note('한 Block의 32 Thread · 배열 길이 32 이상');self.to(51)
            self.code([0],ADD,'vectorAdd.cu  ·  발췌')
            for k in [0,1,31]:self.result(k)
        elif i==6:
            self.active();self.code([1],ADD,'vectorAdd.cu  ·  발췌');self.result(0);self.to(59);self.result(1);self.to(61)
            self.active('all',True);self.emit();self.note('같은 ADD 명령에 32개 Lane이 서로 다른 데이터로 참여',BLUE)
        elif i==7:
            self.active();self.code([1],ADD,'vectorAdd.cu  ·  발췌');self.note('같은 Warp 안에서 경로가 달라진다면?',ORANGE);self.to(70);self.branch_code();self.pulse(self.cg)
        elif i==8:
            self.branch_code();self.active('split',True);self.note('Lane 0–15: ×2   /   Lane 16–31: +1')
            self.pulse(self.cg);self.to(76);self.pulse(self.warp_border)
        elif i==9:
            self.branch_code(2);self.active('split');self.note('×2와 +1이 필요해도 Warp 0은 하나',ORANGE);self.to(85)
            self.branch_code(4);self.pulse(self.warp_border)
        elif i==10:
            self.branch_code();self.active('split');self.note('실행할 명령의 경로에 참여하는 Lane을 선택');self.to(92)
            self.code([0],['Active Mask','Participating lanes','One Warp / one instruction'],label='마스크의 의미');self.pulse(self.warp_border)
        elif i==11:
            self.branch_code(2);self.active('mul');self.note('곱셈: 0–15 활성 · 나머지는 자리 유지',BLUE)
            self.to(98);self.pulse(self.cg);self.to(100);self.note('작은 if는 compiler가 조건부 명령으로 바꿀 수 있음')
        elif i==12:
            self.branch_code(4);self.active('add');self.note('덧셈: 16–31 활성 · 나머지는 자리 유지',ORANGE);self.pulse(self.cg)
        elif i==13:
            self.branch_code(2);self.active('mul');self.note('Warp Divergence  ·  같은 Warp 안의 서로 다른 경로',ORANGE)
            self.to(109);self.branch_code(4);self.active('add',True);self.to(113)
            self.branch_code(2);self.active('mul',True);self.note('명령별 활성 16/32 예시 · 속도가 반드시 절반인 것은 아님');self.to(116)
            self.branch_code(4);self.active('add',True)
        elif i==14:
            self.branch_code();self.active('split');self.note('조건문이 있으면 항상 분기 발산일까?',ORANGE);self.to(123)
            self.code([0],['if (i < 32) {','  A[i] *= 2.0f;','}'],label='한 Block = 32 Thread');self.active('all',True);self.note('32개 모두 같은 조건을 만족할 수 있다',GREEN)
        elif i==15:
            self.code([0,1],['if (i < 32) {','  A[i] *= 2.0f;','}'],label='예시 A  ·  모두 같은 경로');self.active('all');self.note('Thread 0–31 모두 같은 경로',GREEN);self.emit();self.to(129)
            self.branch_code();self.active('split',True);self.note('조건문 자체보다 같은 Warp 안의 경로 차이가 중요',ORANGE)
        elif i==16:
            self.active('split');self.code(lines=['Before Volta: warp-level PC','Volta+: per-thread PC/state','Instruction issue: Warp'],label='실행 상태 관리  ·  개념도');self.note('개별 상태 관리 ≠ 32개의 독립 명령 발행 장치')
            self.to(138)
            self.play(LaggedStart(*(d.animate.set_color(COLS[k%4]) for k,d in enumerate(self.dots)),lag_ratio=.025),run_time=2)
            self.to(142);self.pulse(self.warp_border)
        elif i==17:
            self.code(lines=['Per-thread state','Warp instruction + active mask'],label='서로 다른 두 층위');self.active('all');self.note('개별 실행 상태를 유지해도 Warp와 활성 Lane은 중요',GREEN);self.emit()
        elif i==18:
            self.active();self.select_lane(6);self.code(lines=['Thread 6','Index  /  Data  /  State'],label='Thread  ·  논리적인 실행 문맥');self.note('같은 Thread 6을 같은 위치에서 선택',ORANGE);self.pulse(self.cells[6]);self.to(155)
            self.code(lines=['Warp 0 = 32 Threads','Instruction + Active Mask'],label='Warp  ·  하드웨어 실행 그룹');self.active('all',True);self.emit()
        elif i==19:
            self.code([1],ADD,'같은 Warp 0  ·  함께 실행하는 경로');self.active();self.note('개수뿐 아니라 함께 실행하는 명령 경로를 본다',GREEN);self.to(162)
            self.branch_code();self.active('split',True);self.to(164)
            self.branch_code(2);self.active('mul',True);self.to(165)
            self.branch_code(4);self.active('add',True);self.to(166)
            self.code(lines=['Warp 0','32 Threads / Lane 0–31','Instruction + Active Mask'],label='GPU / SM 0 / Block 0');self.active('all',True);self.note('한 Warp 안의 Thread들이 어떤 경로에 참여하는가?',GREEN)
