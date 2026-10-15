"""FP32 rounding, fixed reductions, order-sensitive atomics, and semantic contracts."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.calc01_transpose.scene import TransposeCost,p,label,cell
from episodes.calc04_arithmetic_intensity.scene import card
from visual_library.manim import BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True
VALUES=['10⁸','1','−10⁸','1','1','1','1','1']


class ParallelReduction(Scene):
    DURATION=135
    section=TransposeCost.section
    sub=TransposeCost.sub
    show=TransposeCost.show
    to=TransposeCost.to

    def construct(self):
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(label('계산의 두 얼굴  /  06',y=7.35,size=21,color=MUTED),
                 label('같은 숫자를 더했는데\n왜 결과가 달라질까?',y=6.4,size=31),
                 Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),
                 label('Parallel Reduction · 부동소수점',y=-7.45,size=19,color=MUTED))

        self.section('01  덧셈 순서만 바꿨는데', '같은 숫자 세 개를 더합니다.\n그런데 괄호를 바꾸자 답이 달라집니다.')
        self.show(label('a = 10⁸   b = −10⁸   c = 1',y=4.05,size=29,color=ACCENT))
        self.show(VGroup(card('(a + b) + c','1',-2,1.8,WEIGHT,3.6,2.6),
                         card('a + (b + c)','0',2,1.8,PRUNE,3.6,2.6)))
        self.to(4);self.sub('실수의 덧셈이라면 두 답은 모두 일입니다.\n하지만 여기서는 각 단계를 FP32로 계산했습니다.')
        self.show(VGroup(label('실수에서 동치 ≠ FP32 결과 동일',y=-.8,size=31,color=ACCENT),
                         label('각 덧셈을 FP32로 반올림 · 최근접 짝수 반올림',y=-2.25,size=22,color=MUTED)))
        self.to(12);self.sub('컴퓨터의 덧셈에서는\n무엇이 달라진 걸까요?');self.to(14)

        self.section('02  큰 수 옆에는 표현할 수 없는 틈이 있다', 'FP32는 모든 실수를 정확히 저장하지 못합니다.\n이 큰 수 근처에서는 표현 가능한 값 사이에 틈이 있습니다.')
        self.show(label('−10⁸ 근처의 FP32 값 · 간격 8',y=4.1,size=28,color=ACCENT))
        line=Line(p(-3.2,1.6),p(3.2,1.6),color=MUTED)
        left=Dot(p(-2.8,1.6),color=WEIGHT,radius=.11);right=Dot(p(2.8,1.6),color=WEIGHT,radius=.11)
        exact=Dot(p(-2.1,1.6),color=ACCENT,radius=.11)
        self.show(VGroup(line,left,right,label('−100000000',-2.25,2.45,26,WEIGHT,3.5),
                         label('−99999992',2.25,2.45,26,WEIGHT,3.5)))
        self.to(21);self.sub('마이너스 일억에 일을 더한 정확한 값은,\n저장 가능한 두 값 사이에 놓입니다.')
        self.show(VGroup(exact,label('정확한 합 −99999999',y=.5,size=29,color=ACCENT),
                         label('가까운 FP32 값은 −100000000',y=-.65,size=27,color=PRUNE)))
        self.to(26);self.sub('가까운 값으로 반올림하면 작은 일이 사라집니다.\n반면 큰 수끼리 먼저 상쇄하면 일이 남습니다.')
        self.play(exact.animate.move_to(left),run_time=.9)
        self.show(VGroup(label('FP32(b + 1) = b',y=-2.05,size=34,color=PRUNE),
                         label('(a + b) + 1 = 1    /    a + FP32(b + 1) = 0',y=-3.4,size=26,color=GOOD),
                         label('값의 오류가 항상 마지막 한 비트에만 생기는 것은 아님',y=-4.5,size=20,color=MUTED)))
        self.to(32)

        self.section('03  여덟 값을 왼쪽부터 더하면', '이제 같은 여덟 숫자를 합쳐 보겠습니다.\n먼저 왼쪽부터 차례로 누적합니다.')
        inputs=self.inputs(2.9);self.show(VGroup(inputs,label('실수에서의 정확한 합 = 6',y=4.05,size=27,color=MUTED)))
        acc=card('FP32 누산값','0',0,.55,ACCENT,4.8,2);self.show(acc)
        self.to(37);self.sub('앞선 덧셈 결과를 다음 덧셈에 사용합니다.\n이 순서에서는 첫 번째 작은 일이 사라집니다.')
        results=['10⁸','10⁸','0','1','2','3','4','5']
        for i,value in enumerate(results):
            target=card('FP32 누산값',value,0,.55,ACCENT,4.8,2)
            self.play(Transform(acc,target),Indicate(inputs[i],color=ACCENT),run_time=.35)
        self.show(label('순차 누적 결과 = 5',y=-1.35,size=34,color=WEIGHT))
        self.show(label('CPU와 GPU 모두 순차 또는 병렬 구현을 선택할 수 있음',y=-3,size=21,color=MUTED))
        self.to(43);self.sub('순차 경로의 결과는 오입니다.\n이번에는 여러 부분합을 동시에 만들어 보겠습니다.');self.to(48)

        self.section('04  Tree는 다른 반올림 경로를 만든다', '병렬 Reduction은 부분합을 만든 뒤,\n그 부분합들을 다시 결합할 수 있습니다.')
        inputs=self.inputs(3.4);self.show(inputs)
        pairs=VGroup(*[cell(v,1.3,SPARSE,25).move_to(p(x,1.4)) for x,v in zip([-3,-1,1,3],['10⁸','−10⁸','2','2'])])
        lines=VGroup(*[Line(inputs[i].get_bottom(),p([-3,-1,1,3][i//2],1.75),color=MUTED,stroke_width=1.5) for i in range(8)])
        self.show(VGroup(lines,pairs))
        self.to(53);self.sub('여러 덧셈을 함께 진행할 수 있지만,\n숫자들이 묶이는 순서도 달라집니다.')
        mids=VGroup(cell('0',1.3,WEIGHT,29).move_to(p(-2,-.35)),cell('4',1.3,WEIGHT,29).move_to(p(2,-.35)))
        self.show(VGroup(mids,*[Line(pairs[i].get_bottom(),mids[i//2].get_top(),color=MUTED,stroke_width=1.5) for i in range(4)]))
        final=card('Tree 결과','4',0,-2.4,GOOD,4.5,1.5)
        self.show(VGroup(final,*[Line(m.get_bottom(),final.get_top(),color=GOOD,stroke_width=1.5) for m in mids]))
        self.to(57);self.sub('이 Tree의 결과는 사입니다.\n같은 입력도 반올림 경로가 달라지면 값이 달라질 수 있습니다.')
        self.show(VGroup(label('실수의 합 6 · 순차 5 · 이 Tree 4',y=-3.65,size=28,color=ACCENT),
                         label('매 덧셈 FP32 · Tree가 언제나 더 정확하거나 부정확한 것은 아님',y=-4.6,size=20,color=MUTED)));self.to(63)

        self.section('05  다른 답과 비결정성은 다른 문제', '병렬 Reduction이 반드시\n매번 다른 답을 내는 것은 아닙니다.')
        self.show(VGroup(card('같은 고정 Tree','반복 1 → 4\n반복 2 → 4\n반복 3 → 4',0,2.3,GOOD,6.6,3.1)))
        self.to(67);self.sub('같은 입력과 같은 Tree, 같은 실행 환경이라면\n반복해서 같은 결과를 얻을 수 있습니다.')
        self.show(label('반복 실행의 동일성 ≠ 순차 합과의 동일성',y=-.35,size=28,color=ACCENT))
        self.to(72);self.sub('반복 재현성과 다른 계산 경로와의 일치는\n서로 다른 보장입니다.')
        self.show(label('GPU·컴파일러·버전·정밀도·반올림 환경이 바뀌면 별도 검토',y=-2.6,size=20,color=MUTED));self.to(76)

        self.section('06  Atomic이어도 순서는 고정되지 않는다', '여러 블록이 부분합을 atomicAdd로\n하나의 누산값에 더하는 구현도 있습니다.')
        blocks=VGroup(*[card(f'Block {i}',v,x,3.2,c,2.3,1.6) for i,(x,v,c) in enumerate(zip([-2.7,0,2.7],['10⁸','−10⁸','1'],[WEIGHT,SPARSE,ACCENT]))])
        self.show(blocks)
        acc=card('공유 누산값 · FP32','0',0,.55,GOOD,5.8,1.8);self.show(acc)
        self.to(81);self.sub('Atomic은 각 갱신의 원자성을 보장하지만,\n블록이 누적하는 순서까지 고정하지는 않습니다.')
        # Two admissible serial orders, not measured GPU runs.
        def arrive(order,values):
            for i,v in zip(order,values):
                dot=Dot(blocks[i].get_bottom(),color=ACCENT,radius=.1);self.add(dot)
                self.play(dot.animate.move_to(acc.get_top()),run_time=.35)
                self.remove(dot)
                self.play(Transform(acc,card('공유 누산값 · FP32',v,0,.55,GOOD,5.8,1.8)),run_time=.15)
        arrive([0,1,2],['10⁸','0','1'])
        self.show(label('가능한 순서 A: 10⁸ → −10⁸ → 1   결과 1',y=-1.2,size=25,color=WEIGHT))
        self.to(87);self.sub('도착 순서가 바뀌면 반올림 순서도 달라집니다.\n같은 입력과 같은 GPU에서도 결과가 달라질 수 있습니다.')
        self.play(Transform(acc,card('공유 누산값 · FP32','0',0,.55,GOOD,5.8,1.8)),run_time=.2)
        arrive([1,2,0],['−10⁸','−10⁸','0'])
        self.show(label('가능한 순서 B: −10⁸ → 1 → 10⁸   결과 0',y=-2.35,size=25,color=PRUNE))
        self.to(94);self.sub('이것은 가능한 두 순서의 예시입니다.\n매 실행마다 반드시 값이 달라진다는 뜻은 아닙니다.')
        self.show(VGroup(label('갱신 누락 문제가 아니라 누적 순서와 반올림의 문제',y=-3.5,size=24,color=ACCENT),
                         label('입력 partial sum과 누산값 모두 FP32 · 초기 누산값 0',y=-4.55,size=20,color=MUTED)));self.to(99)

        self.section('07  신경망에서도 합산 순서가 중요하다', '신경망에는 합산이 곳곳에 있습니다.\nSoftmax, LayerNorm, 행렬곱, Gradient Reduction입니다.')
        for y,title,detail,c in [(3.55,'Softmax','지수 값의 합',WEIGHT),(1.75,'LayerNorm','평균·분산 집계',SPARSE),(-.05,'MatMul','곱의 누산',GOOD),(-1.85,'Gradient','여러 기여의 합',ACCENT)]:
            self.show(card(title,detail,0,y,c,7,1.4),.2)
        self.to(105);self.sub('병렬화나 Fusion, 다른 커널 선택으로\n합산 순서와 반올림이 달라질 수 있습니다.')
        self.show(label('그렇다면 최적화는 어떤 의미에서 같아야 할까?',y=-3.5,size=27,color=ACCENT));self.to(110)

        self.section('08  같은 결과에는 서로 다른 기준이 있다', '실수에서 같은 식이라는 것과,\n컴퓨터의 결과가 같다는 것은 같은 조건이 아닙니다.')
        self.show(card('수학적 동치','실수 연산에서 같은 결과',0,3.35,WEIGHT,7.3,1.65))
        self.to(115);self.sub('수치적으로는 허용 오차 안에서 같은지,\n혹은 비트까지 완전히 같은지를 구분해야 합니다.')
        self.show(VGroup(card('허용 오차 내 일치','문제·dtype에 맞는 오차 기준',0,1.05,SPARSE,7.3,1.65),
                         card('비트 단위 동일성','실제 결과의 비트가 모두 동일',0,-1.25,GOOD,7.3,1.65)))
        self.to(120);self.sub('컴파일러의 순서 변경이 허용되는지는\n프로그램이 요구하는 수치 의미와 옵션에 달렸습니다.')
        self.show(label('수학적 동치만으로 변환 허용을 결정할 수 없다',y=-3.35,size=26,color=ACCENT))
        self.show(label('1과 0의 차이가 자동으로 허용 오차라는 뜻은 아님',y=-4.5,size=21,color=MUTED));self.to(126)

        self.section('09  실행 경로는 결과의 보장도 바꾼다', 'GPU 최적화는 계산 시간만 바꾸는 일이 아닙니다.')
        self.show(VGroup(label('계산 순서 → 반올림 경로 → 결과의 보장',y=3.2,size=31,color=ACCENT),
                         card('더 빠른 경로를 선택할 때','어떤 의미에서 같은 결과인가?',0,.8,GOOD,7.3,2.1)))
        self.to(129);self.sub('계산 순서를 바꾸는 순간, 어떤 의미에서 같은 결과를\n보장할 것인지도 함께 결정해야 합니다.')
        self.show(label('성능 · 정확도 · 재현성을 함께 선택',y=-1.8,size=31,color=WEIGHT))
        self.show(label('결정적이라고 정확한 것은 아니고, 다른 답이 곧 버그도 아니다',y=-3.5,size=21,color=MUTED));self.to(135)

    def inputs(self,y):
        return VGroup(*[cell(v,.82,ACCENT if i in [0,2] else WEIGHT,23).move_to(p((i-3.5)*.98,y)) for i,v in enumerate(VALUES)])
