"""More staging, fewer inefficient accesses: tiled transpose and padding."""
import sys
from pathlib import Path
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.calc01_transpose.scene import TransposeCost, p, label, cell
from visual_library.manim import BG, INK, MUTED, WEIGHT, PRUNE, SPARSE, ACCENT, GOOD, configure_vertical

configure_vertical()
config.disable_caching=True


def grid32(x,y,width=4.8,cols=32):
    step=width/32
    lines=VGroup(*[Line(p(x-width/2+j*step,y+width/2),p(x-width/2+j*step,y-width/2),
                       color=MUTED,stroke_width=.5,stroke_opacity=.6) for j in range(cols+1)],
                 *[Line(p(x-width/2,y+width/2-j*step),p(x-width/2+cols*step,y+width/2-j*step),
                        color=MUTED,stroke_width=.5,stroke_opacity=.6) for j in range(33)])
    return lines


def mini(x,y,empty=False):
    return VGroup(*[cell('' if empty else r*4+c+1,.53,ACCENT if r==0 else WEIGHT,19)
                   .scale(.78).move_to(p(x+(c-1.5)*.45,y+(1.5-r)*.55)) for r in range(4) for c in range(4)])


class SharedMemoryTranspose(TransposeCost):
    DURATION=89

    def construct(self):
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(label('계산의 두 얼굴  /  02',y=7.35,size=21,color=MUTED),
                 label('메모리를 더 사용하는데\n왜 빨라질까?',y=6.4,size=32),
                 Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),
                 label('Shared Memory · 같은 결과, 다른 실행 비용',y=-7.45,size=18,color=MUTED))

        # Segment: compare routes without announcing a winner.
        self.section('01  더 많은 단계가 더 빠를까?', '같은 행렬을 전치하는\n두 가지 방법이 있습니다.')
        self.show(label('A · 직접 전치',y=3.9,color=WEIGHT))
        self.route_nodes(['Global','Output'],[WEIGHT,PRUNE],2.8)
        self.to(2)
        self.sub('하나는 데이터를 바로 옮기고,\n다른 하나는 중간 저장 공간을 한 번 더 거칩니다.')
        self.show(label('B · 중간 저장 공간',y=.7,color=SPARSE))
        self.route_nodes(['Global','Shared','Output'],[WEIGHT,SPARSE,PRUNE],-.55)
        self.show(label('같은 전치 결과 · 추가 저장과 읽기',y=-2.3,size=27,color=ACCENT))
        self.to(7);self.sub('어느 쪽이 더 빠를까요?');self.to(9)

        # Segment: aligned FP32 warp requests cover 4 vs 32 sectors.
        self.section('02  원소 수보다 요청의 묶음', 'GPU에서는 여러 스레드가\n함께 메모리에 접근합니다.')
        self.show(label('32 threads · 각각 FP32 원소 하나',y=4.15,size=26,color=WEIGHT))
        self.to(13)
        self.sub('가까운 주소들을 읽고 쓰면\n요청을 효율적으로 묶을 수 있습니다.')
        self.sectors(1.8,False)
        self.to(17)
        self.sub('주소가 흩어져 있으면 같은 양을 요청해도\n더 많은 메모리 트랜잭션이 필요할 수 있습니다.')
        self.sectors(-1.75,True)
        self.show(label('FP32 · 시작 주소 32B 정렬 · 캐시 효과 생략',y=-4.55,size=20,color=MUTED))
        self.to(24)

        # Segment: actual 32x32 row -> column, with a sparse address inset.
        self.section('03  읽는 행이 쓰는 열이 된다', '전치 행렬을 직접 만든다고\n생각해 보겠습니다.')
        self.show(label('별도 행 우선 출력 배열 · 단순 전치',y=4.2,size=23,color=ACCENT))
        a=grid32(-2,1.6,3.1);b=grid32(2,1.6,3.1)
        self.show(VGroup(a,b,label('A · 32 × 32',-2,3.55,25,WEIGHT,3.3),label('B · 32 × 32',2,3.55,25,PRUNE,3.3)))
        step=3.1/32
        src=VGroup(*[Rectangle(width=step*.85,height=step*.85,fill_color=ACCENT,fill_opacity=1,stroke_width=0)
                     .move_to(p(-2-3.1/2+(j+.5)*step,1.6+3.1/2-.5*step)) for j in range(32)])
        self.show(src)
        self.to(26)
        self.sub('원본 행을 연속으로 읽으면\n읽기는 효율적입니다.')
        movers=src.copy();self.add(movers)
        self.play(*[movers[j].animate.move_to(p(2-3.1/2+.5*step,1.6+3.1/2-(j+.5)*step)) for j in range(32)],run_time=1.4)
        self.stage.add(movers)
        self.to(30)
        self.sub('출력에서는 같은 값들이 열 방향에 놓여\n쓰기 주소가 멀리 떨어질 수 있습니다.')
        self.show(label('B = Aᵀ',y=-.55,size=34))
        offsets=VGroup(*[cell(v,.94,PRUNE,23).move_to(p(-2.7+i*1.35,-2.05)) for i,v in enumerate(['0','32','64','…','992'])])
        self.show(VGroup(offsets,label('출력의 원소 위치 · 간격 32개 = 128B',y=-3.05,size=24,color=PRUNE),
                         label('32개 값 요청 · 서로 다른 32B 구간',y=-4.1,size=23,color=MUTED)))
        self.to(36)

        # Segment: store each row; barrier; reread columns, no internal rearrangement.
        self.section('04  Shared Memory를 거치면', '작은 블록을 중간 저장 공간에\n먼저 모으면 어떨까요?')
        source=mini(-2.5,1.75);tile=mini(0,1.75,True);out=mini(2.5,1.75,True)
        self.show(VGroup(source,tile,out,label('Global',-2.5,3.35,25,WEIGHT,2.2),
                         label('Shared',0,3.35,25,SPARSE,2.2),label('Output',2.5,3.35,25,PRUNE,2.2),
                         label('4 × 4 확대 모형 · 실제 타일은 32 × 32',y=4.2,size=21,color=MUTED)))
        self.to(40)
        self.sub('원본에서는 연속으로 읽고,')
        loaded=VGroup()
        for r in range(4):
            row=VGroup(*[source[4*r+c][1].copy() for c in range(4)])
            self.add(row)
            self.play(*[row[c].animate.move_to(tile[4*r+c]) for c in range(4)],run_time=.3)
            loaded.add(row)
        self.stage.add(loaded)
        sync=label('Block 동기화 · 타일 쓰기 완료',y=-.5,size=26,color=ACCENT)
        self.show(sync)
        self.to(42)
        self.sub('Shared Memory 안에서 접근 방향을 바꾼 뒤,\n출력에도 연속으로 기록합니다.')
        for c in range(4):
            col=VGroup(*[loaded[r][c].copy() for r in range(4)]);self.add(col)
            self.play(*[col[r].animate.move_to(out[4*c+r]) for r in range(4)],run_time=.6)
            self.stage.add(col)
        self.show(VGroup(label('저장된 타일은 그대로 · 열을 읽어 출력의 행으로',y=-2.1,size=26,color=GOOD),
                         label('연속 Global 읽기 → 타일 열 읽기 → 연속 Global 쓰기',y=-3.25,size=23,color=SPARSE),
                         label('추가 Shared 접근·동기화보다 Global 접근 개선이 클 수 있음',y=-4.35,size=20,color=MUTED)))
        self.to(47)

        # Segment: different addresses, same bank; explicitly not broadcast.
        self.section('05  Shared에도 접근 제약이 있다', 'Shared Memory도 아무 주소나\n동시에 접근할 수 있는 것은 아닙니다.')
        self.show(label('FP32 · 32 banks · 4B bank 배치',y=4.25,size=22,color=MUTED))
        board,marks=self.bank_tile(False)
        self.show(board)
        self.to(52)
        self.sub('내부에는 여러 메모리 bank가 있고,')
        self.show(marks)
        self.show(label('같은 열의 원소 위치: 0, 32, 64, …, 992',y=-1.8,size=24,color=PRUNE))
        self.to(54)
        self.sub('서로 다른 주소가 같은 bank에 몰리면\n접근이 나뉘어 처리될 수 있습니다.')
        bankline=self.bank_strip(-3.05,False);self.show(bankline)
        routes=VGroup(*[Line(p(-2.325,3.525-r*.15),p(-3.72,-2.78),color=PRUNE,stroke_width=.65,stroke_opacity=.4) for r in range(32)])
        self.show(routes)
        self.show(VGroup(label('Bank Conflict · 32개 주소 → bank 0',y=-3.85,size=25,color=PRUNE),
                         label('같은 주소를 함께 읽는 broadcast와 다름',y=-4.65,size=20,color=MUTED)))
        self.to(59)

        # Segment: stride 33 changes bank = (row*33 + col) mod 32.
        self.section('06  쓰지 않는 한 칸을 더하면', '해결 법은 의외로 단순합니다.')
        self.show(label('유효 원소는 32 × 32개 그대로',y=4.25,size=25,color=ACCENT))
        before,oldmarks=self.bank_tile(False);self.show(VGroup(before,oldmarks),.25)
        self.to(60)
        self.sub('32칸짜리 행에 사용하지 않는 공간\n하나를 추가합니다.')
        after,newmarks=self.bank_tile(True)
        self.play(ReplacementTransform(before,after),ReplacementTransform(oldmarks,newmarks),run_time=1.4)
        self.stage.remove(before,oldmarks);self.stage.add(after,newmarks)
        pad=VGroup(*[Rectangle(width=.15,height=.15,color=ACCENT,stroke_width=.7,fill_color=ACCENT,fill_opacity=.25)
                    .move_to(p(2.475,3.525-r*.15)) for r in range(32)])
        self.show(VGroup(pad,label('Padding',3.15,1.4,22,ACCENT,1.6),
                         label('미사용 열',3.15,.8,19,ACCENT,1.6)))
        self.to(64)
        self.sub('행의 길이가 33칸이면 다음 행의 시작 주소가\n다른 bank로 밀립니다.')
        self.show(VGroup(label('원소 위치: 0, 33, 66, …, 1023',y=-1.8,size=24,color=GOOD),
                         self.bank_strip(-3.05,True),
                         label('bank = (row × 33 + col) mod 32',y=-3.85,size=25,color=GOOD),
                         label('같은 열의 32개 주소 → 서로 다른 32개 bank',y=-4.65,size=21,color=MUTED)))
        self.to(69)

        # Segment: compare structural costs without invented speed ratios.
        self.section('07  결과는 같고 접근은 달라진다', '전치된 결과는 똑같습니다.')
        for y,name,detail,c in [(3.3,'직접 Transpose','Global 쓰기 비연속',PRUNE),
                                (1.25,'Shared Memory','Global 접근 개선 · bank 충돌 가능',SPARSE),
                                (-.8,'Shared + Padding','Global 접근 개선 · 이 열 접근의 충돌 제거',GOOD)]:
            self.show(VGroup(RoundedRectangle(width=7.5,height=1.65,corner_radius=.12,color=c).move_to(p(0,y)),
                             label(name,y=y+.4,size=27,color=c),label(detail,y=y-.35,size=23)),.2)
        self.to(70)
        self.sub('중간 저장 공간과 사용하지 않는 공간을 추가하자,\n메모리 접근이 더 효율적으로 바뀐 것입니다.')
        self.show(label('접근 구조의 비교 · 성능 향상률은 구현과 GPU에 따라 다름',y=-3,size=21,color=MUTED))
        self.to(78)

        # Segment: one output, three execution routes, no episode teaser.
        self.section('08  이동 횟수만으로 비용을 알 수 없다', '중요한 것은 단순히 데이터를\n얼마나 적게 옮겼느냐가 아닙니다.')
        output=mini(0,1.3)
        vals=[1,5,9,13,2,6,10,14,3,7,11,15,4,8,12,16]
        for k,v in enumerate(vals):output[k][1].become(label(v,size=19,width=.4).scale(.78).move_to(output[k]))
        labels=VGroup(*[label(name,x,3.65,22,c,2.5) for x,name,c in [(-2.7,'직접',PRUNE),(0,'Shared',SPARSE),(2.7,'Padding',GOOD)]])
        self.show(VGroup(labels,output,*[Arrow(p(x,3.2),p(0,2.5),color=c,buff=.05,stroke_width=2) for x,c in [(-2.7,PRUNE),(0,SPARSE),(2.7,GOOD)]]))
        self.to(83)
        self.sub('하드웨어가 그 이동을 어떻게 처리할 수 있는지가\n실제 비용을 결정합니다.')
        self.show(VGroup(label('Same Result',y=-1,size=37,color=WEIGHT),
                         label('Different Execution Cost',y=-2.15,size=32,color=ACCENT),
                         label('같은 결과 · 다른 실행 비용',y=-3.4,size=27,color=GOOD)))
        self.to(89)

    def route_nodes(self,names,colors,y):
        xs=[-2.6,2.6] if len(names)==2 else [-2.7,0,2.7]
        nodes=VGroup(*[cell(n,1.8,c,25).move_to(p(x,y)) for n,c,x in zip(names,colors,xs)])
        self.show(VGroup(nodes,*[Arrow(nodes[i].get_right(),nodes[i+1].get_left(),buff=.1,color=MUTED) for i in range(len(nodes)-1)]))

    def sectors(self,y,strided):
        x=lambda i:(i-15.5)*.235
        lanes=VGroup(*[Dot(p(x(i),y+1),radius=.04,color=WEIGHT) for i in range(32)])
        count=32 if strided else 4
        boxes=VGroup(*[Rectangle(width=.22,height=.5,color=PRUNE if strided else GOOD,
                                stroke_width=1,fill_color=PRUNE if strided else GOOD,
                                fill_opacity=.18 if i<count else 0).move_to(p(x(i),y)) for i in range(32)])
        arrows=VGroup(*[Line(p(x(i),y+.9),p(x(i if strided else i//8),y+.26),color=PRUNE if strided else GOOD,stroke_width=.8) for i in range(32)])
        self.show(VGroup(lanes,boxes,arrows,label('32B 구간 · '+('8원소 간격 → 32구간' if strided else '연속 32원소 → 4구간'),y=y-.65,size=24,color=PRUNE if strided else GOOD)))

    def bank_tile(self,padded):
        cols=33 if padded else 32
        colors=color_gradient([WEIGHT,SPARSE,PRUNE,ACCENT,GOOD],32)
        stripes=VGroup(*[Rectangle(width=.15,height=4.8,stroke_width=0,fill_color=colors[c%32],fill_opacity=.14)
                        .move_to(p(-2.325+c*.15,1.2)) for c in range(cols)]) if not padded else VGroup()
        board=VGroup(stripes,grid32(0,1.2,4.8,cols),label(f'32 × {cols} · Shared Tile',y=3.95,size=26,color=SPARSE))
        marks=VGroup(*[Rectangle(width=.14,height=.14,color=colors[r] if padded else PRUNE,stroke_width=.8,
                                fill_color=colors[r] if padded else PRUNE,fill_opacity=.85)
                      .move_to(p(-2.325,3.525-r*.15)) for r in range(32)])
        # Representative rows connect the diagram to exact bank numbers.
        for r in [0,4,8,16,31]:
            marks.add(label(f'r{r} → b{r if padded else 0}',-3.15,3.525-r*.15,17,colors[r] if padded else PRUNE,1.45))
        return board,marks

    def bank_strip(self,y,padded):
        colors=color_gradient([WEIGHT,SPARSE,PRUNE,ACCENT,GOOD],32)
        return VGroup(*[Rectangle(width=.22,height=.5,color=colors[i] if padded else PRUNE if i==0 else MUTED,
                                 stroke_width=1,fill_color=colors[i] if padded else PRUNE,
                                 fill_opacity=.35 if padded or i==0 else 0).move_to(p((i-15.5)*.24,y)) for i in range(32)],
                      *[label(str(i),(i-15.5)*.24,y-.45,16,MUTED,.4) for i in [0,8,16,24,31]])
