"""User-approved finale: 25 sentences,143 seconds."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent
SOURCE='''7|지금까지 우리는 행렬식이 공간의 부피와 방향을 나타내며, 이러한 성질을 이용해 계산을 단순화할 수도 있다는 사실을 살펴봤습니다.
12|그렇다면 행렬식이 같은 두 행렬은 동일한 공간의 변화를 만들어낼까요?
15|먼저 넓이가 일인 정사각형을 생각해 보겠습니다.
20|이 정사각형을 가로 방향으로 네 배 늘리고, 세로 방향으로 사분의 일로 줄여보겠습니다.
25|정사각형은 길고 얇은 직사각형으로 변하지만, 넓이는 여전히 일입니다.
30|이번에는 가로 방향으로 십 배 늘리고, 세로 방향으로 십분의 일로 줄여보겠습니다.
34|공간의 형태는 더욱 극단적으로 변하지만, 행렬식은 여전히 일입니다.
40|공간을 기울이거나 회전시키는 변환 역시 넓이와 방향성을 유지한다면 동일한 행렬식을 갖습니다.
45|즉, 서로 전혀 다른 공간의 변환이 하나의 숫자로 표현될 수 있는 것입니다.
53|행렬식만으로는 공간이 어느 방향으로 얼마나 늘어났는지, 얼마나 기울어졌는지, 어느 정도 회전했는지 알아낼 수 없습니다.
57|하지만 이러한 한계는 오히려 행렬식이 가진 중요한 특징이기도 합니다.
64|공간의 세부적인 변화는 달라도, 전체 부피와 방향이라는 관점에서는 서로 다른 변환을 동일하게 다룰 수 있기 때문입니다.
67|지금까지의 내용을 다시 돌아보겠습니다.
73|처음에는 연립방정식의 해가 유일하게 결정되는지를 알아보기 위해 방정식의 계수들 사이의 관계를 살펴봤습니다.
80|그리고 그 관계가 공간의 부피와 방향을 계산하는 과정에서도 동일하게 등장한다는 사실을 발견했습니다.
87|공간의 부피와 방향이 갖는 수학적 성질을 분석하자, 순열을 이용한 행렬식의 일반적인 계산 공식이 만들어졌습니다.
94|또한 특정한 변형에도 행렬식이 유지된다는 사실을 이용해, 복잡한 계산을 훨씬 단순한 계산으로 바꿀 수 있었습니다.
99|이 모든 과정에서 우리가 다룬 것은 결국 행렬식이라는 하나의 수학적 대상이었습니다.
110|하지만 어떤 관점에서 바라보느냐에 따라 방정식의 해를 결정하는 기준이 되기도 하고, 공간의 변화를 나타내는 값이 되기도 하며, 효율적인 계산 알고리즘의 기반이 되기도 했습니다.
118|수학에서는 이처럼 복잡한 대상의 모든 정보를 다루는 대신, 그 안에서 중요한 성질을 추출하여 하나의 새로운 대상으로 표현하기도 합니다.
123|그리고 그 성질이 어떤 상황에서 유지되고, 어떤 상황에서 달라지는지를 연구합니다.
127|행렬식은 이러한 수학적 사고방식을 보여주는 대표적인 예시입니다.
135|수많은 원소로 이루어진 행렬에서 공간의 부피와 방향이라는 정보를 추출하고, 그것을 단 하나의 숫자로 표현하는 것.
139|그리고 그 숫자에 담긴 수학적 구조를 이용해 서로 다른 문제를 연결하는 것.
143|이것이 우리가 행렬식을 통해 발견할 수 있는 수학의 또 다른 모습입니다.'''
lines=[];tts=[];start=0
for row in SOURCE.splitlines():
 end,s=row.split('|',1);end=int(end);tts.append(s)
 for a,b in [('넓이가 일인','넓이가 1인'),('네 배','4배'),('사분의 일','1/4'),('여전히 일입니다','여전히 1입니다'),('십 배','10배'),('십분의 일','1/10')]:s=s.replace(a,b)
 lines.append(dict(start=start,end=end,text=s));start=end
def write(name,s):(R/name).write_text(s,encoding='utf-8')
write('timing.json',json.dumps(dict(duration=143,source='사용자 제공25개 문장 종료 시각',lines=lines),ensure_ascii=False,indent=2))
def stamp(s):return f'{s//3600:02}:{s%3600//60:02}:{s%60:02},000'
write('captions.srt','\n\n'.join(f'{i+1}\n{stamp(l["start"])} --> {stamp(l["end"])}\n{l["text"]}' for i,l in enumerate(lines))+'\n')
write('tts_script.txt','\n\n'.join(tts)+'\n')
write('narration.md','# 5장 · 행렬식이 담고 있는 정보와 전체 마무리\n\n사용자 확정25문장·143초\n\n'+'\n\n'.join(f'{l["start"]}–{l["end"]}초\n\n{l["text"]}' for l in lines)+'\n')
shots=[(0,12,'같은 행렬식이 같은 변환을 뜻하는가'),(12,34,'가로k 세로1/k 변형은 넓이1을 유지한다'),(34,45,'항등·크기·전단·회전은 다른 변환이지만 행렬식1이다'),(45,64,'행렬식은 변환의 세부정보를 생략하고 부피와 방향을 추출한다'),(64,73,'방정식의 계수 조합은 유일성을 판단한다'),(73,80,'같은 계수 조합은 부피와 방향을 나타낸다'),(80,87,'성분 조합과 방향이 순열 공식을 만든다'),(87,94,'불변성을 이용하면 소거로 계산을 단순화한다'),(94,110,'네 관점은 하나의 수학적 대상인 행렬식을 해석한다'),(110,118,'행렬에서 관심 있는 성질을 하나의 값으로 추출한다'),(118,127,'값이 보존되고 달라지는 규칙을 연구한다'),(127,135,'행렬과 공간의 부피·방향을 하나의 숫자로 연결한다'),(135,143,'서로 다른 문제를 하나의 수학적 구조로 연결한다')]
manifest=[]
for i,(start,end,claim) in enumerate(shots,1):
 d=R/'scenes'/f'{i:02}';d.mkdir(parents=True,exist_ok=True)
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',class_name=f'Shot{i:02}',start=start,duration_seconds=end-start,claim=claim))
 (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import FinaleScene\nclass Shot'+f'{i:02}'+'(FinaleScene):\n    index='+str(i)+'\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02} · {claim}\n\n- 사용자 확정 구간: {start}–{end}초.\n- 16:9 1920×1080 30fps, 무음·전체자막.\n- storyboard.md와 visuals.py shot_{i:02} 기준.\n- k와1/k·회전각을 직접 계산하고 좌표 단위를 고정한다.\n- 행렬→행렬식의 정보 생략과 비가역 변환의 입력 정보 손실을 구별한다.\n- 마지막 발화는143초 종료. 추가 정지·암전·엔드카드 없음.\n',encoding='utf-8')
 (d/'script.txt').write_text('\n\n'.join(tts[j] for j,l in enumerate(lines) if start<=l['start'] and l['end']<=end)+'\n',encoding='utf-8')
write('manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))

# Scene-specific final layout correction, preserved when preparing sources again.
p=R/"scenes/12/scene.py"
p.write_text(p.read_text(encoding="utf-8")+"\n    def shot_12(self):\n        from visuals import shared, basis, np, tx, eq, Arrow, MUTED, GOLD, GREEN, INK\n        m=shared.symbol_grid(5,-4.5,.6)\n        self.add(m,tx('행렬',-4.5,-1.4,28,MUTED,w=3))\n        volume=basis.cube(np.array([[2,1,0],[0,1,1],[0,0,1]]),[-.3,.5,0],1)\n        volume.scale(.8,about_point=np.array([-.3,.5,0])).shift(np.array([-.5,0,0]))\n        self.show(volume,tx('공간의 부피와 방향',0,-1.4,26,GOLD,w=4),Arrow([-2.8,.5,0],[-2,.5,0],color=MUTED,buff=0,tip_length=.12),d=.8)\n        self.to(131)\n        self.show(Arrow([1.9,.5,0],[2.8,.5,0],color=MUTED,buff=0,tip_length=.12),eq(r'\\det(A)',4.2,.5,62,INK,w=4),tx('하나의 숫자',4.2,-1.4,28,GREEN,w=4),d=.8)\n        self.to(135)\n",encoding="utf-8")
