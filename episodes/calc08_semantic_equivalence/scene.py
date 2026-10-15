"""Rewrite preconditions, legality versus profitability, and bounded search."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.calc01_transpose.scene import TransposeCost,p,label
from episodes.calc04_arithmetic_intensity.scene import card
from episodes.calc07_execution_graph.scene import node
from visual_library.manim import BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True


class SemanticEquivalence(TransposeCost):
    DURATION=140

    def construct(self):
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(label('계산의 두 얼굴  /  08',y=7.35,size=21,color=MUTED),
                 label('AI 컴파일러는 어떻게\n같은 계산을 알아볼까?',y=6.4,size=31),
                 Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),
                 label('Semantic Equivalence · Legality · Cost Model',y=-7.45,size=17,color=MUTED))

        self.section('01  바꿔도 될까, 바꾸는 게 좋을까?', '컴파일러가 행렬곱과 바이어스 덧셈을\n하나의 커널로 합치려 합니다.')
        self.show(label('Y = (XW) + b',y=4.05,size=38,color=ACCENT))
        self.show(VGroup(node('MatMul',-2,2.5,WEIGHT,3),node('Bias Add',2,2.5,SPARSE,3),
                         Arrow(p(-.4,2.5),p(.4,2.5),color=MUTED,buff=.05),
                         node('GEMM + Bias Epilogue',0,.6,GOOD,7,1.1),Arrow(p(0,1.85),p(0,1.25),color=MUTED,buff=.05)))
        self.to(4);self.sub('하지만 두 질문은 다릅니다.\n바꿔도 되는가, 그리고 바꾸는 편이 유리한가?')
        self.show(VGroup(label('Legality · 허용되는가?',y=-1.25,size=30,color=WEIGHT),
                         label('Profitability · 유리한가?',y=-2.5,size=30,color=GOOD)));self.to(9)

        self.section('02  익숙한 항등식에도 적용 조건이 있다', '실수에서 같은 식이라고 해서,\n컴퓨터 프로그램에서도 자유롭게 바꿀 수는 없습니다.')
        self.show(VGroup(label('(A + B) + C  →  A + (B + C)',y=3.8,size=32,color=ACCENT),
                         label('실수에서는 동치 · FP에서는 반올림 순서가 달라질 수 있음',y=2.85,size=22,color=MUTED)))
        self.to(14);self.sub('엑스에 영을 더하는 항등식도 생각해 보죠.\n부동소수점에는 플러스 영과 마이너스 영이 있습니다.')
        self.show(VGroup(label('X + (+0)  →  X',y=1.75,size=34,color=WEIGHT),
                         card('X = −0일 때','원래: −0 + (+0) = +0',0,.1,PRUNE,7.1,1.7)))
        self.to(19);self.sub('마이너스 영에 플러스 영을 더한 값은 플러스 영이지만,\n엑스만 남기면 마이너스 영입니다.')
        self.show(VGroup(label('FP32 비트: +0 = 0x00000000',y=-1.5,size=25,color=WEIGHT),
                         label('FP32 비트: −0 = 0x80000000',y=-2.4,size=25,color=PRUNE)))
        self.to(25);self.sub('부호 비트까지 보존해야 한다면 같은 변환이 아닙니다.\n어떤 수치 의미를 요구하는지부터 확인해야 합니다.')
        self.show(label('최근접 짝수 반올림 · signed zero 보존이 요구되는 경우',y=-3.8,size=21,color=MUTED));self.to(31)

        self.section('03  연산의 이름보다 성질이 단서다', '함수에 덧셈을 넣는 것과,\n각각 함수에 넣은 결과를 더하는 것은 같을까요?')
        self.show(label('f(a + b)  ?=  f(a) + f(b)',y=3.9,size=34,color=ACCENT))
        self.show(card('f(x) = x² · a = 1, b = −1','f(a+b) = 0   /   f(a)+f(b) = 2',0,1.85,PRUNE,7.4,1.9))
        self.to(36);self.sub('제곱 함수에서는 같지 않습니다.\n하지만 실수에서 선형인 함수라면 분배 성질을 이용할 수 있습니다.')
        self.show(card('L(x) = 2x · 실수에서 선형','L(a+b) = L(a)+L(b) = 0',0,-.55,GOOD,7.4,1.9))
        self.to(41);self.sub('이름이 MatMul인지 CustomOp인지보다,\n증명되거나 선언된 연산의 성질이 변환 후보의 근거가 됩니다.')
        self.show(label('수학적 성질 → 변환 후보 → 프로그램 조건 확인',y=-2.6,size=27,color=WEIGHT))
        self.to(48);self.sub('선형성도 부동소수점 결과의 비트 동일성까지\n자동으로 보장하는 것은 아닙니다.')
        self.show(label('수학적 성질과 실행의 수치 계약을 구분',y=-4.15,size=23,color=MUTED));self.to(53)

        self.section('04  성질만으로 적용을 끝내지는 않는다', '선형성, 결합성, 순수성, 원소별 구조는\n서로 다른 변환의 단서입니다.')
        for y,name,detail,c in [(3.8,'Linear','덧셈에 대한 분배 후보',WEIGHT),(2.35,'Associative','결합 순서 변경 후보',SPARSE),(.9,'Pure','중복 제거·재배치 후보',GOOD),(-.55,'Elementwise','원소 단위 Fusion 후보',ACCENT)]:
            self.show(VGroup(node(name,-2.4,y,c,2.4,.85),label(detail,1.15,y,24,INK,4.1)),.2)
        self.to(58);self.sub('실제 적용에는 Shape와 Dtype, 정밀도,\n난수 상태와 메모리 변경 같은 조건도 확인해야 합니다.')
        self.show(label('Shape · Dtype · Precision · RNG · Mutation · Dependency',y=-2.15,size=23,color=PRUNE))
        self.to(65);self.sub('컴파일러는 규칙뿐 아니라,\n그 규칙을 적용할 수 있는 조건도 관리합니다.')
        self.show(label('실수의 성질·IR 속성·효과 정보·분석 결과에 따른 조건부 변환',y=-3.8,size=21,color=MUTED));self.to(70)

        self.section('05  허용 여부와 비용을 따로 판단한다', '먼저 프로그램이 요구하는 의미를\n보존하는 변환인지 확인합니다.')
        src=node('변환 후보',0,3.6,ACCENT,4);legal=node('Legality Check',0,2,WEIGHT,4)
        reject=node('허용 안 됨\n후보 제외',-2.45,-.2,PRUNE,2.6,1.2);cost=node('허용됨\n비용 평가',2.15,-.2,GOOD,3.2,1.2)
        self.show(VGroup(src,legal,Arrow(src.get_bottom(),legal.get_top(),color=MUTED,buff=.1),reject,cost,
                         Arrow(legal.get_bottom(),reject.get_top(),color=PRUNE,buff=.1),Arrow(legal.get_bottom(),cost.get_top(),color=GOOD,buff=.1)))
        self.to(73);self.sub('허용되지 않으면 후보에서 제외합니다.\n허용된다면 그다음에 적용할 가치가 있는지 따집니다.')
        self.show(label('Profitability Check · 실제 비용은 더 나은가?',y=-1.9,size=28,color=GOOD))
        self.to(79);self.sub('MLIR의 target legality는 허용되는 IR 연산을\n뜻하기도 합니다. 의미 보존의 자동 증명과는 다릅니다.')
        self.show(VGroup(label('의미 보존 조건 ≠ Target IR의 연산 허용 여부',y=-3.25,size=25,color=ACCENT),
                         label('개념적 두 판단 · 실제 pass의 순서와 구현은 다양함',y=-4.45,size=20,color=MUTED)));self.to(86)

        self.section('06  합법적인 변환도 느릴 수 있다', '두 연산을 합치는 변환이 허용된다고 해도,\n반드시 실행이 빨라지는 것은 아닙니다.')
        self.show(VGroup(card('Fusion의 이익','중간 저장·읽기 감소 가능',0,3.25,GOOD,7.2,1.7),
                         card('Fusion의 비용','살아 있는 값·레지스터 사용 증가 가능',0,.8,PRUNE,7.2,1.7)))
        self.to(91);self.sub('줄어든 데이터 이동보다 자원 제약의 비용이 커지면,\n전체 실행 시간이 늘어날 수도 있습니다.')
        self.show(label('Memory Traffic ↓  ↔  Register Pressure ↑',y=-1.25,size=28,color=ACCENT))
        self.to(97);self.sub('허용되는가와 유리한가는,\n서로 다른 질문입니다.')
        self.show(label('Legality 통과 ≠ 성능 향상 보장',y=-3.2,size=31,color=WEIGHT));self.to(100)

        self.section('07  변환을 조합하면 탐색이 커진다', 'Fusion과 Layout, Tile 선택을 조합하면\n후보 실행 경로가 늘어납니다.')
        self.show(label('가상 독립 선택: Fusion 2 × Layout 2 × Tile 2 = 8',y=4.2,size=24,color=ACCENT))
        root=node('원본',0,3.1,WEIGHT,2,.7);self.show(root)
        levels=[[-2,2],[-3,-1,1,3],[(i-3.5)*1.02 for i in range(8)]]
        previous=VGroup(root)
        for level,(xs,y) in enumerate(zip(levels,[1.7,.25,-1.3])):
            nodes=VGroup(*[node(('F'+str(i) if level==0 else 'L'+str(i%2) if level==1 else 'P'+str(i)),x,y,SPARSE if level<2 else GOOD,.8 if level==2 else 1.1,.65) for i,x in enumerate(xs)])
            self.show(VGroup(nodes,*[Line(previous[i//2].get_bottom(),n.get_top(),color=MUTED,stroke_width=1.2) for i,n in enumerate(nodes)]))
            previous=nodes
        self.to(104);self.sub('모든 후보를 실제 GPU에서 실행해 비교한다면,\n탐색 자체의 시간도 커질 수 있습니다.')
        self.show(label('실제 선택은 서로 제약하며, 허용되지 않는 조합도 있음',y=-2.65,size=22,color=MUTED))
        self.to(110);self.sub('그래서 규칙과 휴리스틱, 비용 모델, 오토튜닝으로\n탐색 범위를 줄이기도 합니다.')
        self.show(VGroup(label('후보 생성 → 조건 검사 → 일부 후보 평가',y=-3.65,size=27,color=ACCENT),
                         label('Transform Dialect 등은 변환 조합을 표현 · 전역 최적해 증명은 아님',y=-4.6,size=19,color=MUTED)));self.to(115)

        self.section('08  비용 모델도 완벽한 답은 아니다', '비용 모델은 실행 비용을 예상하고,\n지원되는 후보는 실제 측정으로 비교할 수도 있습니다.')
        self.show(label('가상 후보 비교 · 단위 없음 · 실제 GPU 측정 아님',y=4.2,size=22,color=MUTED))
        self.show(VGroup(label('후보',-2.8,3.1,25,WEIGHT),label('예상 비용',-.55,3.1,25,SPARSE),label('측정된 비용',2.25,3.1,25,GOOD)))
        for y,name,pred,actual in [(1.95,'A',8,10),(.8,'B',6,8),(-.35,'C',7,7)]:
            self.show(VGroup(label(name,-2.8,y,29,WEIGHT),label(pred,-.55,y,29,SPARSE),label(actual,2.25,y,29,GOOD)),.2)
        self.to(120);self.sub('예상과 측정의 순위가 달라질 수 있습니다.\n측정한 후보 중 좋은 경로를 찾았다고 전역 최적해는 아닙니다.')
        self.show(VGroup(label('예상: B가 최저  →  이 가상 측정: C가 최저',y=-1.65,size=26,color=ACCENT),
                         label('입력·하드웨어·측정 잡음·컴파일 시간도 고려',y=-2.9,size=23,color=MUTED)))
        self.to(126);self.sub('컴파일러는 제한된 시간 안에서,\n허용된 경로 중 더 나은 실행 방법을 찾아갑니다.')
        self.show(label('전체 후보의 전역 최적해를 항상 보장하지는 않음',y=-4.15,size=22,color=MUTED));self.to(131)

        self.section('09  수학적 의미와 하드웨어 비용 사이', '컴파일러는 단순히 계산을\n빠르게 바꾸는 도구가 아닙니다.')
        self.show(VGroup(node('Mathematics\n무엇을 계산하는가',-2,3,WEIGHT,3.6,1.6),
                         node('Hardware\n어떻게 계산하는가',2,3,GOOD,3.6,1.6),
                         node('AI Compiler',0,.65,ACCENT,5,1.1),Arrow(p(-2,2.1),p(-.6,1.3),color=WEIGHT,buff=.05),
                         Arrow(p(.6,1.3),p(2,2.1),color=GOOD,buff=.05)))
        self.to(135);self.sub('무엇을 바꿔도 되는지 판단하고,\n그 안에서 더 나은 실행 방법을 찾아가는 시스템입니다.')
        self.show(VGroup(label('의미를 지키는 변환 · 비용을 줄이는 선택',y=-1.4,size=29,color=ACCENT),
                         label('계산의 두 얼굴',y=-3,size=35,color=WEIGHT)));self.to(140)
