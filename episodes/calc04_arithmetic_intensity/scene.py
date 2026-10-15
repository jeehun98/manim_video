"""Data reuse, a conceptual DRAM Roofline, and token-dependent GEMM intensity."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.calc01_transpose.scene import TransposeCost,p,label,cell
from visual_library.manim import BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True


def card(title,detail,x,y,c=WEIGHT,w=3.5,h=2.1):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,color=c,fill_color=BG,fill_opacity=1).move_to(p(x,y)),
                  label(title,x,y+h*.26,26,c,w-.25),label(detail,x,y-h*.18,25,INK,w-.25))


class ArithmeticIntensity(TransposeCost):
    DURATION=132

    def construct(self):
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(label('계산의 두 얼굴  /  04',y=7.35,size=21,color=MUTED),
                 label('같은 행렬곱인데 왜\nGPU의 병목이 달라질까?',y=6.4,size=30),
                 Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),
                 label('Arithmetic Intensity · Roofline Model',y=-7.45,size=18,color=MUTED))

        # Segment: reveal the changed bottleneck before introducing terminology.
        self.section('01  같은 W인데 기다리는 것이 다르다', '같은 GPU에서 같은 가중치로\n행렬곱을 수행합니다.')
        self.show(label('Y = XW · 같은 계산식, 같은 가중치',y=4.05,size=31,color=ACCENT))
        self.show(VGroup(card('입력 한 개','메모리 공급을 기다릴 수 있음',0,2.1,PRUNE,7,1.65),
                         card('입력 여러 개','계산 장치가 한계가 될 수 있음',0,-.2,GOOD,7,1.65)))
        self.to(3);self.sub('입력이 하나일 때와 여러 개일 때,\nGPU가 기다리는 대상이 달라질 수 있습니다.')
        self.to(8);self.sub('수식도 가중치도 그대로인데,\n무엇이 달라진 걸까요?')
        self.show(label('달라진 것은 한 번에 처리하는 입력의 수',y=-2.55,size=29,color=ACCENT))
        self.show(label('가능한 병목의 비교 · 실제 조건에 따라 달라짐',y=-3.9,size=21,color=MUTED));self.to(11)

        # Segment: fixed W, grow M from 1 to 4 to 14. Count mathematical participation.
        self.section('02  한 가중치가 몇 번 계산에 참여할까?', '한 번 가져온 가중치를\n입력 하나의 계산에 사용합니다.')
        self.show(VGroup(label('입력 X',-2.4,3.8,27,WEIGHT),label('같은 가중치 W',1.7,3.8,27,SPARSE,3.5)))
        w=Rectangle(width=2.4,height=2.4,color=SPARSE,fill_color=SPARSE,fill_opacity=.12).move_to(p(1.7,1.4))
        grid=VGroup(*[Line(p(.5+i*.6,.2),p(.5+i*.6,2.6),color=SPARSE,stroke_width=1) for i in range(1,4)],
                    *[Line(p(.5,.2+i*.6),p(2.9,.2+i*.6),color=SPARSE,stroke_width=1) for i in range(1,4)])
        weight=cell('w',.42,ACCENT,22).move_to(p(.8,2.3))
        rows=VGroup(*[Rectangle(width=2,height=.21,color=WEIGHT,fill_color=WEIGHT,fill_opacity=.18).move_to(p(-2.4,2.75-i*.25)) for i in range(14)])
        counter=label('입력 1개 · 가중치 원소당 참여 1회',y=-1.8,size=30,color=ACCENT)
        self.show(VGroup(w,grid,weight,rows[0],counter))
        self.show(Arrow(weight.get_left(),rows[0].get_right(),color=ACCENT,buff=.12,stroke_width=2))
        self.to(15);self.sub('입력의 행을 늘려도 가중치 W는 그대로입니다.\n같은 원소가 더 많은 입력의 계산에 참여합니다.')
        self.show(VGroup(*rows[1:4]),.6)
        self.show(VGroup(*[Line(weight.get_left(),rows[i].get_right(),color=ACCENT,stroke_width=1,stroke_opacity=.45) for i in range(1,4)]),.3)
        self.play(Transform(counter,label('입력 4개 · 가중치 원소당 참여 4회',y=-1.8,size=30,color=ACCENT)),run_time=.4)
        self.to(18)
        self.play(LaggedStart(*[FadeIn(rows[i]) for i in range(4,14)],lag_ratio=.12),run_time=1.4)
        self.stage.add(*rows[1:])
        self.show(VGroup(*[Line(weight.get_left(),rows[i].get_right(),color=ACCENT,stroke_width=1,stroke_opacity=.45) for i in range(4,14)]),.4)
        self.play(Transform(counter,label('입력 14개 · 가중치 원소당 참여 14회',y=-1.8,size=30,color=ACCENT)),run_time=.4)
        self.to(21);self.sub('입력이 열네 개라면, 밀집 행렬곱에서\n각 가중치는 열네 행의 계산에 사용됩니다.')
        self.show(label('W는 그대로 · X의 행 수만 1 → 4 → 14',y=-2.95,size=27,color=GOOD))
        self.to(26);self.sub('중요한 것은 사용 횟수입니다.\n실제로 메모리에서 읽는 횟수는 구현에 따라 다릅니다.')
        self.show(label('14회는 수학적 참여 횟수 · 병목 전환점이나 DRAM 읽기 횟수 아님',y=-4.2,size=20,color=MUTED));self.to(31)

        # Segment: show one-use vs retained data before bytes and ratios.
        self.section('03  한 번 쓰고 끝낼까, 다시 쓸까?', '원소별 덧셈은 두 값을 가져와 더하고,\n결과를 저장하면 그 계산이 끝납니다.')
        self.show(VGroup(card('원소별 덧셈','읽기 → 덧셈 → 저장',0,2.8,WEIGHT,7,1.6),
                         card('재사용하는 행렬곱','한 번 가져온 값 → 여러 곱셈·누산',0,.35,GOOD,7,1.6)))
        self.to(36);self.sub('행렬곱은 가져온 값을 여러 계산에 쓸 수 있습니다.\n이동 비용을 더 많은 계산에 나눠 부담하는 겁니다.')
        self.show(label('먼저 볼 것: 가져온 뒤 몇 번 사용하는가?',y=-1.5,size=28,color=ACCENT))
        self.to(42);self.sub('예를 들어 FP32 덧셈은 한 값을 네 바이트로 셉니다.\n두 값 읽기와 결과 쓰기로 열두 바이트입니다.')
        self.show(VGroup(label('FP32: 읽기 4B + 4B, 쓰기 4B → 덧셈 1회',y=-2.85,size=25,color=WEIGHT),
                         label('FP32 · 캐시 재사용 제외 · 추가 트래픽 생략',y=-4.1,size=22,color=MUTED)));self.to(49)

        self.section('04  이제 이 비율에 이름을 붙이면', '옮긴 데이터 한 바이트로 얼마나 계산하는가.\n이 비율을 Arithmetic Intensity라고 합니다.')
        self.show(label('Arithmetic Intensity',y=3.75,size=36,color=ACCENT))
        self.show(label('AI = FLOPs / Bytes transferred',y=2.7,size=32))
        self.show(VGroup(card('같은 데이터','적게 사용 → 낮은 AI',0,.8,PRUNE,7,1.6),
                         card('재사용 증가','많이 사용 → 높은 AI 가능',0,-1.55,GOOD,7,1.6)))
        self.to(54);self.sub('같은 행렬곱도 재사용 없이 반복해서 읽으면 느립니다.\n재사용을 실현한 실행 방식이 중요합니다.')
        self.show(label('이 영상의 Bytes는 DRAM 이동량 기준',y=-3.3,size=25,color=MUTED))
        self.to(60);self.sub('높은 비율은 계산 장치를 더 활용할 여지입니다.\n실행 시간이 언제나 짧아진다는 뜻은 아닙니다.');self.to(66)

        # Segment: visualize limits, then name them.
        self.section('05  기다리던 이유를 그림으로 보면', '가져온 데이터로 조금만 계산한다면,\n계산 장치는 다음 데이터를 기다리기 쉽습니다.')
        curve,coord=self.roofline();self.show(curve)
        low=Dot(coord(.5),radius=.11,color=PRUNE);self.show(low)
        self.show(label('작은 입력 · 낮은 AI의 예',-1.3,-.25,22,PRUNE,3.7))
        self.to(71);self.sub('이렇게 메모리 공급 속도가 한계인 상태를\nMemory-bound라고 부릅니다.')
        self.show(label('Memory-bound',-1.85,.9,23,PRUNE,3.2))
        self.to(76);self.sub('같은 데이터를 더 많이 재사용하면 상한이 올라갑니다.\n충분히 크면 계산 장치의 한계에 닿을 수도 있습니다.')
        high=Dot(coord(64),radius=.11,color=GOOD);self.show(high)
        self.show(label('충분히 큰 입력의 예',1.8,3.35,23,GOOD,3.5))
        self.to(82);self.sub('계산 처리량이 한계인 상태가 Compute-bound입니다.\n그 뒤에는 비율만 높여도 지붕이 올라가지 않습니다.')
        self.show(label('두 점은 개념적 상한 위치 · 실측이나 14행의 수치가 아님',y=-4.5,size=20,color=MUTED));self.to(88)

        self.section('06  Roofline은 답이 아니라 설명 도구', '이 그림이 Roofline Model입니다.\n실행 시간이 아닌 가능한 처리량의 상한을 보여줍니다.')
        self.show(label('P ≤ min(P_peak, BW × AI)',y=3.7,size=36,color=ACCENT))
        self.show(VGroup(card('기울어진 지붕','메모리 대역폭 한계',0,1.65,PRUNE,7,1.6),
                         card('평평한 지붕','산술 처리량 한계',0,-.65,GOOD,7,1.6)))
        self.to(94);self.sub('실제 성능은 이 지붕 아래에 놓입니다.\n캐시, 커널 실행 비용과 자원 활용도도 영향을 줍니다.')
        self.show(label('같은 dtype·연산 경로·메모리 계층으로 비교',y=-2.4,size=25,color=MUTED))
        self.to(100);self.sub('그래서 AI가 높다는 사실만으로\n모든 커널이 빠르다고 말할 수는 없습니다.')
        self.show(label('연산량만큼 중요한 것: 공급과 재사용',y=-3.75,size=27,color=ACCENT));self.to(105)

        self.section('07  LLM에서는 이 차이가 어떻게 나타날까?', '작은 배치로 한 토큰씩 생성하는 Decode는\n가중치 이동당 계산이 적어지기 쉽습니다.')
        self.show(VGroup(card('작은 배치 Decode','가중치·KV Cache 접근에 민감할 수 있음',0,2.95,PRUNE,7.4,1.8),
                         card('충분히 큰 Prefill','여러 토큰에서 같은 가중치 재사용',0,.4,GOOD,7.4,1.8)))
        self.to(110);self.sub('여러 토큰을 함께 처리하는 Prefill은\n재사용을 높여 계산 처리량이 중요해질 수 있습니다.')
        self.show(label('같은 GPU · 같은 W · 입력 행 수와 실행 조건의 차이',y=-1.8,size=25,color=ACCENT))
        self.to(115);self.sub('배치 크기와 커널 구성에 따라 달라집니다.\n두 단계의 병목이 항상 고정된 것은 아닙니다.')
        self.show(label('KV 읽기는 선형층 GEMM과 별도인 Attention 비용',y=-3.3,size=21,color=MUTED));self.to(121)

        self.section('08  계산량보다 먼저 던질 질문', '같은 수식도 입력의 모양이 바뀌면\n유리한 최적화의 목표가 달라질 수 있습니다.')
        self.show(VGroup(label('한 번 가져온 데이터로',y=3.4,size=34,color=WEIGHT),
                         label('얼마나 많은 계산을 하는가?',y=2.3,size=35,color=ACCENT)))
        self.show(card('같은 W, 다른 입력 개수','데이터 재사용 → 병목 → 최적화 목표',0,-.05,GOOD,7.4,2))
        self.to(126);self.sub('GPU 성능을 이해하려면 계산량뿐 아니라,\n데이터를 어떻게 공급하고 재사용하는지 살펴봐야 합니다.')
        self.show(label('수식은 같아도 실행 조건은 다르다',y=-2.8,size=30,color=GOOD));self.to(132)

    def roofline(self):
        # log2 axes, conceptual P_peak=128, BW=16 in normalized performance units.
        xy=lambda ai,perf:p(-3.2+(np.log2(ai)+4)*6.4/12,-1.8+np.log2(perf)*.6)
        coord=lambda ai:xy(ai,min(128,16*ai))
        axes=VGroup(Line(p(-3.2,-1.8),p(3.4,-1.8),color=MUTED),Line(p(-3.2,-1.8),p(-3.2,2.65),color=MUTED))
        bounds=VMobject(color=GOOD,stroke_width=4).set_points_as_corners([coord(1/16),coord(8),coord(256)])
        ticks=VGroup(*[label(v,xy(ai,1)[0],-2.25,19,MUTED,1.2) for ai,v in [(1/16,'1/16'),(1,'1'),(8,'8'),(256,'256')]],
                     *[label(v,-3.7,xy(1,perf)[1],19,MUTED,.7) for perf,v in [(1,'1'),(8,'8'),(128,'128')]])
        return VGroup(axes,bounds,ticks,label('처리량 상한 · 가상 하드웨어 모형',y=4.15,size=24,color=ACCENT),
                      label('Peak compute',1.75,2.7,22,GOOD,3),
                      label('AI · FLOP/B  (log₂)',y=-3,size=24,color=INK),
                      label('개념 Roofline · log₂ 축 · 정규화 처리량 · DRAM 기준',y=-3.75,size=20,color=MUTED)),coord
