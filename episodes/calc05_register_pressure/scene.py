"""Finite registers, resident warps, latency hiding, and conditional spilling tradeoffs."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.calc01_transpose.scene import TransposeCost,p,label,cell
from episodes.calc04_arithmetic_intensity.scene import card
from visual_library.manim import BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True


class RegisterPressure(TransposeCost):
    DURATION=130

    def construct(self):
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(label('계산의 두 얼굴  /  05',y=7.35,size=21,color=MUTED),
                 label('GPU의 병렬성을 높였는데\n왜 느려질까?',y=6.4,size=31),
                 Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),
                 label('Register Pressure · Occupancy · Spilling',y=-7.45,size=18,color=MUTED))

        self.section('01  더 많이 준비하면 더 빠를까?', 'GPU에 더 많은 Warp를 배치하면,\n계산 장치를 더 잘 활용할 수 있을까요?')
        self.show(VGroup(card('적은 활성 Warp','적은 작업을 준비',-2,2.1,WEIGHT),
                         card('많은 활성 Warp','더 많은 작업을 준비',2,2.1,GOOD)))
        self.to(4);self.sub('그런데 병렬성을 높이려던 선택이\n오히려 메모리 접근을 늘릴 수도 있습니다.')
        self.show(label('병렬성 ↑  →  메모리 접근도 ↑ ?',y=-.65,size=34,color=ACCENT))
        self.to(9);self.sub('스레드들이 함께 나눠 쓰는 자원부터\n살펴보겠습니다.')
        self.show(label('Warp = 32 threads · SM에 상주해 실행을 준비',y=-2.5,size=24,color=MUTED));self.to(12)

        self.section('02  스레드마다 중간값을 보관한다', '각 스레드는 계산 중인 값과 변수를\n레지스터에 보관할 수 있습니다.')
        threads=VGroup(*[card(f'Thread {i}','누산값 · 임시값',x,2.8,c,3.2,1.7) for i,(x,c) in enumerate([(-1.9,WEIGHT),(1.9,SPARSE)])])
        regs=VGroup(*[cell(f'r{i}',.72,ACCENT,22).move_to(p((i%4-1.5)*1.5, .7-(i//4)*1.1)) for i in range(8)])
        self.show(VGroup(threads,regs,label('SM의 유한한 Register File',y=-1.6,size=29,color=ACCENT)))
        self.to(16);self.sub('레지스터는 무한하지 않습니다.\n한 스레드가 많이 쓰면 함께 상주할 자리가 줄 수 있습니다.')
        self.show(label('스레드 수와 스레드당 자원 사용을 함께 본다',y=-3,size=28,color=GOOD))
        self.show(label('레지스터는 스레드별 할당 · 그림은 SM 전체 자원 예산',y=-4.2,size=21,color=MUTED));self.to(21)

        self.section('03  같은 SM, 서로 다른 자원 배분', '레지스터가 육만 오천오백서른여섯 개이고,\n한 블록이 이백쉰여섯 스레드인 모형을 보겠습니다.')
        self.show(label('SM당 65,536 registers · 최대 2,048 threads\n256 threads / block · 레지스터만 제약인 교육용 모형',y=4.15,size=21,color=MUTED))
        view=self.budget(32);self.show(view)
        self.to(28);self.sub('스레드마다 서른두 개를 쓰면\n여덟 블록, 이천마흔여덟 스레드를 유지할 수 있습니다.')
        self.to(33)
        nextview=self.budget(64);self.play(ReplacementTransform(view,nextview),run_time=.8);self.stage.remove(view);self.stage.add(nextview);view=nextview
        self.sub('예순네 개를 쓰면 네 블록.\n레지스터 사용량이 늘수록 활성 작업은 줄어듭니다.')
        self.to(38)
        nextview=self.budget(128);self.play(ReplacementTransform(view,nextview),run_time=.8);self.stage.remove(view);self.stage.add(nextview)
        self.sub('백스물여덟 개라면 두 블록, 오백열두 스레드입니다.\n더 요청한 작업도 모두 동시에 상주하는 것은 아닙니다.')
        self.show(label('다른 제약·할당 단위 생략 · 실제 GPU 수치가 아님',y=-4.4,size=21,color=MUTED));self.to(44)

        self.section('04  기다리는 동안 다른 Warp를 실행', '어떤 Warp가 데이터를 기다릴 때,\n실행 가능한 다른 Warp의 명령을 발행할 수 있습니다.')
        self.schedule(2.3,['W0 load','W1 alu','W2 alu','W1 alu','W2 alu','W0 alu'],True)
        self.show(label('W0가 기다리는 동안 다른 Warp의 준비된 명령',y=.9,size=24,color=GOOD))
        self.to(49);self.sub('이것이 Latency Hiding입니다.\n상주한 Warp가 너무 적으면 지연을 가리기 어려울 수 있습니다.')
        self.schedule(-.9,['W0 load','대기','대기','대기','대기','W0 alu'],False)
        self.show(label('같은 W0 대기 · 다른 준비된 명령이 없는 모형',y=-2.3,size=24,color=PRUNE))
        self.show(label('개념 발행 슬롯 · 실제 SM의 여러 scheduler·발행 폭은 생략',y=-3.65,size=20,color=MUTED));self.to(55)

        self.section('05  Occupancy는 활용률이 아니다', 'Occupancy는 SM의 최대 Warp 수 대비\n상주한 활성 Warp 수의 비율입니다.')
        self.show(VGroup(label('Occupancy = 활성 Warp / 최대 활성 Warp',y=3.8,size=29,color=ACCENT),
                         card('상주 Warp 16 / 64','Occupancy 25%',0,1.5,SPARSE,6.8,1.8)))
        self.to(60);self.sub('계산 장치가 실제로 얼마나 바쁜지를\n직접 나타내는 숫자는 아닙니다.')
        self.show(label('상주한 작업의 비율 ≠ 실행 장치 활용률',y=-.4,size=28,color=PRUNE))
        self.to(64);self.sub('독립적인 명령이 충분하면, 낮은 Occupancy에서도\n높은 처리량을 낼 수 있습니다.')
        self.show(label('ILP · 한 스레드 안의 독립적인 명령도 활용',y=-2.1,size=25,color=GOOD))
        self.show(label('높은 Occupancy가 항상 더 빠른 것은 아니다',y=-3.6,size=28,color=ACCENT));self.to(68)

        self.section('06  컴파일러가 레지스터를 제한하면', '그렇다면 레지스터 사용을 제한해서\n더 많은 Warp를 상주시켜 보면 어떨까요?')
        reg=RoundedRectangle(width=5.8,height=1.5,corner_radius=.1,color=ACCENT).move_to(p(0,2.4))
        vals=VGroup(*[cell(v,.75,WEIGHT,24).move_to(p(-2+i,2.4)) for i,v in enumerate(['a','b','c','d','e'])])
        self.show(VGroup(reg,vals,label('컴파일 시 할당 결정 → 실행 시 Store / Reload',y=3.65,size=24,color=ACCENT)))
        self.to(73);self.sub('중간값을 담을 자리가 부족해지면,\n일부 값을 메모리로 내보낼 수 있습니다.')
        mem=VGroup(RoundedRectangle(width=6.7,height=1.8,corner_radius=.12,color=PRUNE).move_to(p(0,-.7)),label('Local Memory · 스레드별 주소 공간',y=-.15,size=25,color=PRUNE));self.show(mem)
        self.play(reg.animate.stretch_to_fit_width(3.2).move_to(p(-1,2.4)),run_time=.6)
        self.play(vals[3].animate.move_to(p(-1,-.8)),vals[4].animate.move_to(p(1,-.8)),run_time=.8)
        self.show(VGroup(Arrow(p(.9,1.8),p(.9,.35),color=PRUNE,buff=.1),label('Spill Store',2.25,1,23,PRUNE,2.5)))
        self.to(78);self.sub('Register Spilling입니다. 다시 쓸 때는\n저장한 값을 읽어오는 명령도 필요할 수 있습니다.')
        self.show(VGroup(Arrow(p(-2.4,.35),p(-2.4,1.8),color=PRUNE,buff=.1),label('Reload',-3.05,1.05,21,PRUNE,1.4)))
        self.to(83);self.sub('Local Memory는 레지스터 같은 온칩 저장소가 아닙니다.\n디바이스 메모리 주소 공간이며 캐시를 통해 접근합니다.')
        self.show(VGroup(label('Local 주소 → 캐시 → 필요 시 디바이스 메모리',y=-2.7,size=26,color=PRUNE),
                         label('일반적인 Local spilling 예시 · 모든 접근이 DRAM miss인 것은 아님',y=-4.15,size=20,color=MUTED)));self.to(89)

        self.section('07  늘어난 Warp와 늘어난 이동을 비교', '레지스터를 충분히 쓰면 활성 Warp는 적어도,\n중간값을 가까이 유지할 수 있습니다.')
        self.show(VGroup(card('A · 레지스터 충분','적은 Warp 가능\n중간값 유지',-2,2.3,WEIGHT,3.6,2.6),
                         card('B · 레지스터 제한','많은 Warp 가능\nSpill Store + Reload 가능',2,2.3,PRUNE,3.6,2.6)))
        self.to(94);self.sub('레지스터를 줄이면 Warp는 늘 수 있지만,\n추가 저장과 읽기의 비용도 생길 수 있습니다.')
        self.show(label('지연 숨기기의 이익  ↔  추가 메모리 접근 비용',y=-.15,size=27,color=ACCENT))
        self.to(100);self.sub('그래서 어느 쪽이 빠른지는 조건에 달렸습니다.\n적은 Spilling을 감수한 편이 이길 수도 있습니다.')
        self.show(label('Occupancy 최대화가 아니라 실행 시간 최소화',y=-2.2,size=29,color=GOOD))
        self.show(label('Spilling 발생과 성능 영향은 컴파일 결과·실측으로 확인',y=-3.8,size=21,color=MUTED));self.to(105)

        self.section('08  GEMM Tile도 같은 자원을 경쟁한다', '행렬곱은 여러 출력의 누산값을\n레지스터에 유지할 수 있습니다.')
        small=self.tile(-2,2.4,2);large=self.tile(2,2.4,4);self.show(VGroup(small,large,
                         label('작은 스레드별 누산 타일',-2,3.9,22,WEIGHT,3.5),label('큰 스레드별 누산 타일',2,3.9,22,SPARSE,3.5),
                         label('한 스레드가 유지하는 누산 원소 수의 증가 예',y=4.45,size=21,color=MUTED),
                         label('4개 누산값',-2,.95,22,WEIGHT,3),label('16개 누산값',2,.95,22,SPARSE,3)))
        self.to(110);self.sub('타일을 키우면 데이터를 더 재사용할 여지가 생깁니다.\n하지만 유지할 중간값과 레지스터 사용도 늘 수 있습니다.')
        self.show(VGroup(label('재사용 증가 가능',y=.35,size=28,color=GOOD),
                         label('살아 있는 누산값 증가 → Register Pressure 증가',y=-1,size=25,color=PRUNE)))
        self.to(117);self.sub('그 결과 Occupancy가 낮아질 수도 있습니다.\n이득과 자원 제약을 함께 따져야 합니다.')
        self.show(label('Tile 종류·확장 방향·스레드 매핑에 따라 달라짐\nTile을 키운다고 register 사용이 반드시 늘지는 않음',y=-2.8,size=22,color=MUTED));self.to(121)

        self.section('09  병렬성과 성능은 같은 목표가 아니다', 'GPU 최적화는 하나의 자원을\n최대한 사용하는 문제가 아닙니다.')
        self.show(VGroup(label('재사용 · 레지스터 · 활성 Warp · 메모리 접근',y=3.45,size=28,color=ACCENT),
                         card('서로 경쟁하는 자원','전체 실행 시간을 최소화하는 균형',0,1.2,GOOD,7.3,2)))
        self.to(125);self.sub('서로 경쟁하는 자원들 사이에서,\n전체 실행 시간을 최소화하는 선택이 중요합니다.')
        self.show(label('병렬성 최대화 ≠ 성능 최대화',y=-1.3,size=33,color=PRUNE))
        self.show(label('같은 계산 · 다른 자원 배분 · 다른 비용',y=-3,size=27,color=WEIGHT));self.to(130)

    def budget(self,r):
        blocks=65536//(256*r);threads=blocks*256;warps=threads//32
        group=VGroup(label(f'{r} registers / thread',y=3.4,size=31,color=ACCENT),
                     label('SM Register 예산 · 각 블록이 차지하는 공간',y=2.65,size=23,color=MUTED))
        for i in range(blocks):
            width=7.2/blocks
            group.add(Rectangle(width=width-.06,height=1.1,color=SPARSE,fill_color=SPARSE,fill_opacity=.25).move_to(p(-3.6+(i+.5)*width,1.7)),
                      label(f'B{i}',-3.6+(i+.5)*width,1.7,24,INK,width-.1))
        group.add(label('작업 목록 · 밝은 블록만 SM에 상주',y=.55,size=23,color=MUTED))
        for i in range(8):
            active=i<blocks
            group.add(cell(f'B{i}',1.2,GOOD if active else MUTED,23).move_to(p((i%4-1.5)*1.65,-.35-(i//4)*.9)))
        group.add(label(f'활성 {threads:,} / 2,048 threads',y=-2.4,size=31,color=GOOD),
                  label(f'{warps} / 64 warps  ·  Occupancy {warps/64:.0%}',y=-3.35,size=28,color=ACCENT))
        return group

    def schedule(self,y,commands,ready):
        group=VGroup(label('다른 준비된 Warp 있음' if ready else '다른 준비된 Warp 없음',y=y+1,size=26,color=GOOD if ready else PRUNE))
        for i,s in enumerate(commands):
            c=GOOD if s!='대기' else PRUNE
            group.add(card(str(i+1),s,-3.05+i*1.22,y,c,1.1,1.25))
        self.show(group)

    def tile(self,x,y,n):
        step=.54
        return VGroup(*[cell('Σ',.46,WEIGHT if n==2 else SPARSE,21).stretch_to_fit_height(.46).move_to(p(x+(c-(n-1)/2)*step,y+((n-1)/2-r)*step)) for r in range(n) for c in range(n)])
