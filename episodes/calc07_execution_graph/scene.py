"""Separate computation semantics, execution plans, and CUDA graph replay."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.calc01_transpose.scene import TransposeCost,p,label
from episodes.calc04_arithmetic_intensity.scene import card
from visual_library.manim import BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True


def node(s,x,y,c=WEIGHT,w=2.2,h=.95):
    text=label(s,x,y,24,INK,w-.2)
    if text.height>h-.2:text.scale_to_fit_height(h-.2)
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.1,color=c,
                                   fill_color=BG,fill_opacity=1,stroke_width=1.7).move_to(p(x,y)),text)


class ExecutionGraph(TransposeCost):
    DURATION=122

    def construct(self):
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(label('계산의 두 얼굴  /  07',y=7.35,size=21,color=MUTED),
                 label('같은 신경망인데\n실행 그래프는 왜 다를까?',y=6.4,size=31),
                 Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),
                 label('Computation Graph · Execution Plan · Runtime',y=-7.45,size=17,color=MUTED))

        self.section('01  수식이 같으면 실행도 같을까?', '같은 신경망을 같은 GPU에서 실행합니다.\n수식도, 가중치도, 입력도 같습니다.')
        self.show(label('Y = ReLU(XW + b)',y=3.8,size=38,color=ACCENT))
        plans=VGroup(*[node('Plan '+s,x,1.3,c) for s,x,c in zip('ABC',[-2.7,0,2.7],[WEIGHT,SPARSE,GOOD])])
        self.show(VGroup(plans,*[Arrow(p(0,3.1),pl.get_top(),color=MUTED,buff=.1) for pl in plans]))
        self.to(6);self.sub('그렇다면 실행되는 커널의 구성과 순서도\n항상 같을까요?')
        self.show(VGroup(label('하나의 출력 목표 · 여러 실행 계획',y=-.55,size=29,color=ACCENT),
                         label('구현을 선택하는 프레임워크·컴파일러·라이브러리',y=-2,size=23,color=MUTED)));self.to(10)

        self.section('02  연산 그래프는 무엇을 계산할까?', '프레임워크는 연산들의 연결 관계를\n그래프로 표현할 수 있습니다.')
        self.show(label('Computation Graph · 연산과 데이터 의존성',y=4.35,size=24,color=WEIGHT))
        mm=node('MatMul',0,2.9,WEIGHT,2.5);bias=node('Bias Add',0,.65,SPARSE,2.5);relu=node('ReLU',0,-1.6,GOOD,2.5)
        self.show(VGroup(mm,bias,relu,Arrow(mm.get_bottom(),bias.get_top(),color=MUTED,buff=.1),
                         Arrow(bias.get_bottom(),relu.get_top(),color=MUTED,buff=.1),
                         label('X, W',-2.8,2.9,25,WEIGHT,2),Arrow(p(-1.9,2.9),mm.get_left(),color=WEIGHT,buff=.05),
                         label('b',-2.8,.65,28,SPARSE),Arrow(p(-2,.65),bias.get_left(),color=SPARSE,buff=.05)))
        self.to(14);self.sub('행렬곱의 결과가 바이어스 덧셈으로,\n이어서 ReLU로 전달됩니다.')
        value=Dot(mm.get_bottom(),color=ACCENT,radius=.1);self.add(value)
        self.play(value.animate.move_to(bias),run_time=.65);self.play(value.animate.move_to(relu),run_time=.65);self.remove(value)
        for y in [2.9,.65,-1.6]:self.show(label('[M, N]\nFP32\nLayout 후보',2.7,y,20,MUTED,2.3),.2)
        self.to(18);self.sub('어떤 값이 어떤 계산에 필요한지는 알지만,\n각 노드가 별도 GPU 커널인지는 아직 정하지 않았습니다.')
        self.show(label('연산 노드 ≠ GPU 커널',y=-3.35,size=30,color=ACCENT));self.to(24)

        self.section('03  노드와 커널의 대응을 선택한다', '각 연산을 따로 실행하거나,\n여러 연산을 하나의 커널에 포함할 수 있습니다.')
        self.show(label('Execution Plan · 커널 구성 선택',y=4.3,size=24,color=SPARSE))
        self.show(label('Plan A · 세 커널',y=3.45,size=27,color=WEIGHT))
        self.chain(['MatMul\nKernel','Bias\nKernel','ReLU\nKernel'],2.35,[WEIGHT,SPARSE,GOOD])
        self.show(label('중간 텐서 → 중간 텐서 → 출력',y=1.25,size=23,color=MUTED))
        self.to(29);self.sub('같은 연산 그래프가 세 커널이 될 수도,\n하나의 Fused GEMM 커널이 될 수도 있습니다.')
        self.show(VGroup(label('Plan B · 한 커널',y=.1,size=27,color=GOOD),
                         card('Fused GEMM Kernel','MatMul + Bias + ReLU',0,-1.35,GOOD,7.1,1.8)))
        self.to(34);self.sub('이것은 연산 노드와 하드웨어 커널의\n대응 관계를 선택하는 문제입니다.')
        self.show(VGroup(label('중간 텐서 저장을 생략할 수 있음',y=-3,size=25,color=GOOD),
                         label('같은 수학적 출력 목표 · bitwise 보장은 별도 수치 계약',y=-4.25,size=20,color=MUTED)));self.to(38)

        self.section('04  실행 계획은 커널 수보다 넓다', '중간값을 어느 메모리에 둘지,\n어떤 배치와 순서로 전달할지도 선택해야 합니다.')
        self.show(label('Kernel · Tile · Layout · Buffer · Dependency',y=4.2,size=25,color=ACCENT))
        root=node('같은 MatMul',0,2.95,WEIGHT,3.6);self.show(root)
        options=VGroup(card('후보 B','Tile P · Layout P\nRegister / Shared 사용 P',-2,.4,SPARSE,3.65,2.5),
                       card('후보 C','Tile Q · Layout Q\nRegister / Shared 사용 Q',2,.4,GOOD,3.65,2.5))
        self.show(VGroup(options,*[Arrow(root.get_bottom(),o.get_top(),color=MUTED,buff=.1) for o in options]))
        self.to(43);self.sub('하나의 행렬곱 노드도 타일과 메모리 배치가 다른\n여러 커널 구현으로 이어질 수 있습니다.')
        self.show(label('라이브러리 커널 선택 · 커널 생성 · 버퍼와 의존성 결정',y=-1.8,size=24,color=MUTED))
        self.to(48);self.sub('이 선택들이 모여, 실제 GPU에서\n어떻게 실행할지에 대한 계획이 됩니다.')
        self.show(label('연산 그래프 → 실행 계획',y=-3.5,size=31,color=ACCENT));self.to(53)

        self.section('05  독립 분기는 겹칠 수도 있다', '연산들이 서로 독립적이라면,\n항상 같은 순서로 실행할 필요는 없습니다.')
        self.show(label('분기를 설명하는 별도 예: Y = f(X) + g(X)',y=4.2,size=25,color=ACCENT))
        x=node('X',0,3.1,WEIGHT,1.3,.7);f=node('f(X)',-2.2,1.8,SPARSE);g=node('g(X)',2.2,1.8,GOOD);add=node('Add',0,.35,ACCENT)
        self.show(VGroup(x,f,g,add,Arrow(x.get_bottom(),f.get_top(),color=MUTED,buff=.1),Arrow(x.get_bottom(),g.get_top(),color=MUTED,buff=.1),
                         Arrow(f.get_bottom(),add.get_top(),color=MUTED,buff=.1),Arrow(g.get_bottom(),add.get_top(),color=MUTED,buff=.1)))
        self.to(57);self.sub('의존성이 없는 작업은 서로 다른 Stream에서\n겹쳐 실행할 수도 있습니다.')
        self.timeline()
        self.to(61);self.sub('하지만 Add는 두 결과를 모두 기다립니다.\n다른 Stream이 실제 동시 실행을 보장하지는 않습니다.')
        self.show(label('자원·의존성에 따른 가능한 중첩 · 시간 비율은 개념 모형',y=-4.5,size=20,color=MUTED));self.to(67)

        self.section('06  선택된 작업을 CUDA Graph로 구성', '선택한 커널과 실행 의존성을\n런타임 그래프로 구성할 수도 있습니다.')
        self.show(label('Runtime / CUDA Graph · 선택된 작업과 의존성',y=4.3,size=23,color=GOOD))
        self.chain(['Kernel A','Kernel B','Kernel C'],2.95,[WEIGHT,SPARSE,GOOD])
        graph=node('Instantiate',-2,1.1,ACCENT,3.1);exe=node('GraphExec',2,1.1,GOOD,3.1)
        self.show(VGroup(graph,exe,Arrow(graph.get_right(),exe.get_left(),color=GOOD,buff=.1),
                         Arrow(p(0,2.35),graph.get_top(),color=MUTED,buff=.1,stroke_width=1.5)))
        self.to(73);self.sub('CUDA Graph는 작업을 미리 정의하고 재사용해,\n반복 실행의 호스트 요청 비용을 줄일 수 있습니다.')
        launches=VGroup(*[node(f'Launch {i+1}',x,-.9,GOOD,2.2,.8) for i,x in enumerate([-2.7,0,2.7])])
        self.show(VGroup(launches,*[Arrow(exe.get_bottom(),v.get_top(),color=GOOD,buff=.1,stroke_width=1.5) for v in launches]))
        for launch in launches:self.play(Indicate(launch,color=ACCENT),run_time=.3)
        self.show(label('같은 GraphExec의 순차 반복 실행',y=-1.85,size=23,color=GOOD))
        self.to(79);self.sub('CUDA Graph 자체가 신경망을 해석해\n최적 커널을 고르는 컴파일러는 아닙니다.')
        self.show(VGroup(label('연산 해석·계획 최적화와 CUDA Graph 구성은 다른 작업',y=-2.8,size=23,color=ACCENT),
                         label('Shape·분기·주소·Graph 호환성에 따라 재사용·갱신 가능 여부 달라짐',y=-4.2,size=19,color=MUTED)));self.to(84)

        self.section('07  어떤 계획이 실제로 유리할까?', '커널 수가 적은 경로가\n항상 빠른 것은 아닙니다.')
        self.show(VGroup(card('Plan A','분리된 커널',-2.6,2.9,WEIGHT,2.3,1.7),
                         card('Plan B','결합된 커널',0,2.9,SPARSE,2.3,1.7),
                         card('Plan C','다른 Tile·배치',2.6,2.9,GOOD,2.3,1.7)))
        self.to(87);self.sub('데이터 이동, 레지스터 사용, 의존성과 입력 크기가\n전체 실행 비용을 바꿉니다.')
        self.show(label('Launch · Memory Traffic · Resources · Synchronization',y=1.35,size=24,color=ACCENT))
        self.show(label('비용 모델 · 선택 규칙 · 지원되는 설정의 실제 측정',y=.35,size=23,color=MUTED))
        self.to(93);self.sub('프레임워크는 비용 모델이나 실제 측정으로\n후보를 평가할 수 있습니다.')
        guard=node('입력 조건 / Guard',0,-.9,ACCENT,4.1,.8);self.show(guard)
        self.to(97);self.sub('입력 크기나 조건이 바뀌면, 다른 계획을 선택하거나\n새로 컴파일할 수도 있습니다.')
        self.show(VGroup(node('캐시된 계획',-2,-2.7,GOOD,3.2,.9),node('새 계획 생성',2,-2.7,SPARSE,3.2,.9),
                         Arrow(guard.get_bottom(),p(-2,-2.2),color=GOOD,buff=.1),Arrow(guard.get_bottom(),p(2,-2.2),color=SPARSE,buff=.1),
                         label('예: torch.compile · 동적 Shape는 재컴파일을 줄일 수도 있음',y=-4.1,size=20,color=MUTED)));self.to(109)

        self.section('08  하나의 계산, 여러 실행 구조', '연산 그래프는 무엇을 계산할지 나타냅니다.\n실행 계획은 그것을 어떻게 구현할지 결정합니다.')
        self.show(VGroup(node('Computation Graph',0,3.45,WEIGHT,6,.9),
                         node('Execution Planning',0,1.85,SPARSE,6,.9),
                         Arrow(p(0,2.9),p(0,2.4),color=MUTED,buff=.05)))
        plans=VGroup(*[node('Plan '+s,x,.1,c) for s,x,c in zip('ABC',[-2.7,0,2.7],[WEIGHT,SPARSE,GOOD])])
        self.show(VGroup(plans,*[Arrow(p(0,1.3),n.get_top(),color=MUTED,buff=.1) for n in plans]))
        self.to(115);self.sub('성능은 커널, 메모리 배치와 실행 순서에 달려 있습니다.\n같은 신경망의 실행 구조는 하나로 정해져 있지 않습니다.')
        self.show(VGroup(label('One Computation Graph',y=-1.6,size=29,color=WEIGHT),
                         label('Multiple Execution Plans',y=-2.65,size=29,color=ACCENT),
                         label('GPU 실행 · 필요할 때 CUDA Graph 활용',y=-4,size=24,color=GOOD)));self.to(122)

    def chain(self,names,y,colors):
        nodes=VGroup(*[node(s,x,y,c) for s,x,c in zip(names,[-2.7,0,2.7],colors)])
        self.show(VGroup(nodes,*[Arrow(nodes[i].get_right(),nodes[i+1].get_left(),color=MUTED,buff=.08) for i in range(2)]))

    def timeline(self):
        # Toy time axis: f=2 units, g=2 units, add=1 unit. No hardware timing claim.
        group=VGroup(label('직렬',-3.25,-1.15,22,MUTED,1),
                     label('중첩 가능',-3.1,-2.6,21,MUTED,1.4))
        for x,w,s,c in [(-1.55,1.5,'f',SPARSE),(.05,1.5,'g',GOOD),(1.35,.8,'Add',ACCENT)]:group.add(node(s,x,-1.15,c,w,.55))
        group.add(node('f',-1.55,-2.25,SPARSE,1.5,.5),node('g',-1.55,-2.95,GOOD,1.5,.5),
                  Line(p(-.7,-2),p(-.7,-3.2),color=ACCENT),node('Add',-.15,-2.6,ACCENT,.8,.55),
                  label('두 결과 준비 후 Add',1.8,-2.6,22,ACCENT,3.1),
                  Arrow(p(-2.4,-3.65),p(2.7,-3.65),color=MUTED,buff=0),label('시간 →',1.8,-3.95,20,MUTED))
        self.show(group)
