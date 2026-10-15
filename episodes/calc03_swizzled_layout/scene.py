"""Logical tensor identity, XOR physical layouts, and end-to-end layout cost."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.calc01_transpose.scene import TransposeCost, p, label, cell
from visual_library.manim import BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True
COLORS=color_gradient([WEIGHT,SPARSE,PRUNE,ACCENT,GOOD],8)


def tiles(n,x,y,step,values=True):
    return VGroup(*[cell(r*n+c if values else c,step*.86,COLORS[c%8],19 if n==4 else 17)
                   .stretch_to_fit_height(step*.85).move_to(p(x+(c-(n-1)/2)*step,y+((n-1)/2-r)*step))
                   for r in range(n) for c in range(n)])


class SwizzledLayout(TransposeCost):
    DURATION=92

    def construct(self):
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(label('계산의 두 얼굴  /  03',y=7.35,size=21,color=MUTED),
                 label('GPU는 왜 데이터를\n일부러 뒤섞을까?',y=6.4,size=32),
                 Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),
                 label('Swizzled Layout · Tensor Core',y=-7.45,size=19,color=MUTED))

        # Segment: two storage maps, one logical matrix.
        self.section('01  가지런한 순서가 최선일까?', 'GPU에서 행렬을 빠르게 계산하려면\n데이터를 가지런히 정렬해야 할까요?')
        normal=tiles(4,-2,1.4,.72);sw=tiles(4,2,1.4,.72)
        self.show(VGroup(normal,sw,label('일반 저장',-2,3.55,26,WEIGHT,3),label('XOR 저장',2,3.55,26,SPARSE,3)))
        self.to(4)
        self.sub('꼭 그렇지는 않습니다.\n일부러 뒤섞어 저장하는 방법도 있습니다.')
        self.play(*[sw[r*4+c].animate.move_to(p(2+((r^c)-1.5)*.72,1.4+(1.5-r)*.72)) for r in range(4) for c in range(4)],run_time=1.5)
        self.show(VGroup(label('같은 논리적 행렬 A · 다른 물리적 저장 위치',y=-1.25,size=27,color=ACCENT),
                         label('4 × 4 XOR 재배치 모형 · 수학적 원소 순서가 바뀐 것이 아님',y=-2.5,size=21,color=MUTED)))
        self.to(9)

        # Segment: use an explicitly hypothetical 8-bank scalar-word memory.
        self.section('02  충돌하는 것은 값이 아니라 주소', 'GPU의 Shared Memory는\n여러 bank로 나뉩니다.')
        self.show(label('교육용 8-bank 모형 · 한 원소가 한 bank 단위',y=4.25,size=21,color=MUTED))
        a=tiles(8,0,1.5,.55,False);self.show(a)
        chosen=VGroup(*[SurroundingRectangle(a[r*8],color=ACCENT,buff=.015,stroke_width=2) for r in range(8)])
        self.show(chosen)
        self.to(12)
        self.sub('동시에 접근한 서로 다른 주소가\n같은 bank에 몰리면 요청이 충돌할 수 있습니다.')
        banks=self.banks(-2.25,False);self.show(banks)
        lines=VGroup(*[Line(a[r*8].get_bottom(),p(-3.15,-1.95),color=PRUNE,stroke_width=1,stroke_opacity=.5) for r in range(8)])
        self.show(lines)
        self.show(label('Bank Conflict · 위치 0, 8, …, 56 → bank 0',y=-3.25,size=25,color=PRUNE))
        self.to(17)
        self.sub('문제는 원소의 값이 아니라\n주소의 배치입니다.')
        self.show(label('그림 속 숫자 = 논리적 열 번호',y=-4.3,size=22,color=MUTED))
        self.to(20)

        # Segment: each row is a permutation; fixed logical column maps to all banks.
        self.section('03  XOR로 저장 위치를 바꾸면', '행마다 원소를 저장할 위치를\n다르게 정하면 어떨까요?')
        self.show(label('물리 열 = row XOR col',y=4.1,size=29,color=ACCENT))
        a=tiles(8,0,1.5,.55,False);self.show(a)
        self.to(24)
        self.sub('행 번호와 열 번호를 XOR로 결합해\n실제 저장 주소를 바꿀 수 있습니다.')
        self.play(*[a[r*8+c].animate.move_to(p(((r^c)-3.5)*.55,1.5+(3.5-r)*.55)) for r in range(8) for c in range(8)],run_time=1.7)
        marks=VGroup(*[SurroundingRectangle(a[r*8],color=ACCENT,buff=.015,stroke_width=2) for r in range(8)])
        self.show(marks)
        self.show(self.banks(-2.25,True))
        self.to(31)
        self.sub('같은 bank에 몰리던 열 접근을\n서로 다른 bank로 분산시킬 수 있습니다.')
        self.show(VGroup(label('논리 열 0 → 물리 열 / bank 0, 1, …, 7',y=-3.25,size=25,color=GOOD),
                         label('교육용 8 × 8 · 숫자는 논리 열 번호 · 추가 칸 없음',y=-4.3,size=21,color=MUTED)))
        self.to(36)

        # Segment: fetch the same A[3,5] from two different addresses.
        self.section('04  같은 원소, 다른 주소', '행렬의 값이나 수학적 의미는\n변하지 않습니다.')
        self.show(label('논리적 원소 A[3, 5] = 29',y=3.8,size=34,color=ACCENT))
        regular=VGroup(*[cell(24+c,.7,ACCENT if c==5 else WEIGHT,24).move_to(p((c-3.5)*.85,1.65)) for c in range(8)])
        perm=VGroup(*[cell(24+(3^c),.7,ACCENT if c==6 else SPARSE,24).move_to(p((c-3.5)*.85,-1.1)) for c in range(8)])
        self.show(VGroup(regular,perm,label('일반: 8i + j → 주소 29',y=2.65,size=27,color=WEIGHT),
                         label('XOR: 8i + (i XOR j) → 주소 30',y=-.15,size=27,color=SPARSE)))
        self.to(41)
        self.sub('달라진 것은 논리적 좌표를\n실제 메모리 주소에 연결하는 방법입니다.')
        self.play(Circumscribe(regular[5],color=ACCENT),Circumscribe(perm[6],color=ACCENT),run_time=1)
        self.show(VGroup(label('29 = 29 · 같은 값, 같은 논리적 행렬',y=-2.6,size=29,color=GOOD),
                         label('8 × 8 모형 · 주소는 원소 단위 · offset = 0',y=-3.75,size=21,color=MUTED),
                         label('Swizzle은 주소 매핑 · 별도 복사 단계가 항상 필요한 것은 아님',y=-4.6,size=20,color=MUTED)))
        self.to(45)

        # Segment: illustrate alternatives, do not imply a universal shared->TC path.
        self.section('05  Tensor Core에 어떻게 공급할까?', '데이터 배치는 메모리 충돌을\n줄이는 데서 끝나지 않습니다.')
        self.show(label('작은 행렬 조각 · 명령이 요구하는 배치',y=4.15,size=28,color=ACCENT))
        self.to(50)
        self.sub('Tensor Core는 행렬의 작은 조각들을\n정해진 방식으로 받아 계산합니다.')
        self.chain(['Shared Tile','Register\nFragment','MMA'],2.2,[SPARSE,WEIGHT,GOOD])
        self.show(label('레지스터 fragment를 쓰는 경로 예시',y=.95,size=23,color=WEIGHT))
        self.to(55)
        self.sub('어떤 배치로 저장하고,\n어떻게 읽어 전달할지도 중요해집니다.')
        self.chain(['Shared Tile','SMEM\nDescriptor','WGMMA'],-.7,[SPARSE,ACCENT,GOOD])
        self.show(VGroup(label('descriptor로 Shared operand를 지정하는 경로 예시',y=-2.05,size=22,color=ACCENT),
                         label('구현·아키텍처·MMA 명령에 따라 공급 방식이 다름',y=-3.2,size=22,color=MUTED),
                         label('실제 swizzle도 dtype·접근 폭·명령에 맞춰 선택',y=-4.3,size=23,color=MUTED)))
        self.to(59)

        # Segment: writer/reader layouts, conversion and an adjusted writer alternative.
        self.section('06  쓰기 좋은 배치, 읽기 좋은 배치', '앞선 연산이 쓰기 편한 배치와\n다음 연산이 읽기 편한 배치는 다를 수 있습니다.')
        self.chain(['Producer','Layout\nConversion','Consumer'],2.55,[WEIGHT,PRUNE,SPARSE])
        self.show(VGroup(label('출력 Layout P',-2.7,1.35,24,WEIGHT,2.5),label('입력 Layout Q',2.7,1.35,24,SPARSE,2.5)))
        self.to(65)
        self.sub('중간에 데이터를 다시 배치하는\n비용이 필요할 수도 있습니다.')
        self.chain(['Producer\n출력 조정','Layout Q','Consumer'],-.75,[WEIGHT,GOOD,SPARSE])
        self.show(VGroup(label('출력을 Q에 맞추면 중간 변환을 줄일 수 있음',y=-2.1,size=25,color=GOOD),
                         label('변환은 Register 교환·Shared 재배치 등일 수도 있음',y=-3.3,size=22,color=MUTED),
                         label('출력 조정 자체의 비용도 함께 비교',y=-4.3,size=23,color=ACCENT)))
        self.to(69)

        # Segment: sequential additive toy cost model, no benchmark claims.
        self.section('07  누구에게 최적인 배치인가?', '한 연산에 가장 효율적인 배치가\n전체 계산에서도 최선이라는 보장은 없습니다.')
        self.show(label('T_total = T_producer + T_conversion + T_consumer',y=3.95,size=25,color=ACCENT))
        self.show(label('직렬 실행의 단순 가상 모형 · 실측 아님 · 단위 없음',y=3.1,size=21,color=MUTED))
        legend=VGroup(*[label(s,x,2.25,23,c,2.5) for x,s,c in [(-2.7,'Producer',WEIGHT),(0,'Conversion',PRUNE),(2.7,'Consumer',SPARSE)]])
        self.show(legend)
        self.costbar('P', [2,4,3],.7)
        self.to(74)
        self.sub('앞선 저장, 다음 읽기,\n그 사이의 변환 비용까지 함께 고려해야 합니다.')
        self.costbar('Q',[3,0,3],-1.2)
        self.show(VGroup(label('Producer 2 → 3이어도 전체 9 → 6',y=-2.9,size=28,color=GOOD),
                         label('겹쳐 실행되는 실제 커널은 병렬 중첩·동기화도 고려',y=-4.2,size=21,color=MUTED)))
        self.to(80)

        # Segment: equal mathematics realized through multiple physical mappings.
        self.section('08  계산 전체에 맞는 배치를 선택', '같은 행렬도 메모리 배치에 따라\nGPU가 처리하는 방식은 달라집니다.')
        self.show(label('수학적 행렬 A',y=3.8,size=34,color=ACCENT))
        for x,name,c in [(-2.65,'Layout P',WEIGHT),(0,'XOR Layout',SPARSE),(2.65,'Layout Q',GOOD)]:
            self.show(VGroup(cell(name,2.2,c,24).move_to(p(x,1.8)),Arrow(p(0,3.3),p(x,2.2),color=c,buff=.1),
                             Arrow(p(x,1.35),p(0,-.15),color=c,buff=.1)),.2)
        self.show(label('같은 수학적 결과',y=-.65,size=31,color=INK))
        self.to(85)
        self.sub('최적화는 단순히 정렬하는 것이 아니라,\n계산 전체에 맞는 배치를 선택하는 문제입니다.')
        self.show(VGroup(label('Same Tensor',y=-2.1,size=31,color=WEIGHT),
                         label('Different Layout · Different Cost',y=-3.3,size=28,color=ACCENT)))
        self.to(92)

    def banks(self,y,spread):
        return VGroup(*[cell(f'b{i}',.72,COLORS[i] if spread else PRUNE if i==0 else MUTED,23).move_to(p((i-3.5)*.9,y)) for i in range(8)])

    def chain(self,names,y,colors):
        nodes=VGroup()
        for s,c,x in zip(names,colors,[-2.7,0,2.7]):
            text=label(s,x,y,23,INK,1.95)
            if text.height>.85:
                text.scale_to_fit_height(.85)
            nodes.add(VGroup(RoundedRectangle(width=2.15,height=1.15,corner_radius=.08,
                                              color=c,stroke_width=1.5,fill_color=BG,fill_opacity=1).move_to(p(x,y)),text))
        self.show(VGroup(nodes,*[Arrow(nodes[i].get_right(),nodes[i+1].get_left(),buff=.05,color=MUTED,stroke_width=2) for i in range(2)]))

    def costbar(self,name,values,y):
        start=-2.55;parts=VGroup(label(name,-3.45,y,26,ACCENT,1))
        for value,c in zip(values,[WEIGHT,PRUNE,SPARSE]):
            if value:
                w=value*.48
                parts.add(Rectangle(width=w,height=.65,color=c,fill_color=c,fill_opacity=.35).move_to(p(start+w/2,y)),
                          label(value,start+w/2,y,25,INK,w-.05))
                start+=w
        parts.add(label(f'합 {sum(values)}',2.95,y,24,INK,1.8))
        self.show(parts)
