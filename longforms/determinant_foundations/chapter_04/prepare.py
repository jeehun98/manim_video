"""Approved narration and actual sentence endpoints, without estimated timing."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
SOURCE='''7|앞서 우리는 행렬식의 계산 공식이 공간의 부피와 방향이라는 성질에서 자연스럽게 만들어진다는 사실을 살펴봤습니다.
13|하지만 이 공식을 그대로 이용하면 행렬의 크기가 커질수록 계산해야 할 항의 개수가 급격하게 증가합니다.
21|오 행 오 열 행렬에서는 백이십 개의 항이 등장하고, 십 행 십 열 행렬에서는 삼백육십만 개가 넘는 항이 등장합니다.
26|그렇다면 행렬식의 성질을 이용해 이러한 계산을 단순화할 수는 없을까요?
30|먼저 두 개의 열벡터가 만드는 평행사변형을 다시 생각해 보겠습니다.
34|이번에는 첫 번째 벡터에 두 번째 벡터의 일정한 배수를 더해보겠습니다.
39|평행사변형의 모양은 달라지지만, 밑변과 높이는 그대로 유지됩니다.
42|따라서 부호 있는 넓이도 변하지 않습니다.
47|이러한 성질은 앞서 살펴본 행렬식의 선형성을 이용해서도 설명할 수 있습니다.
53|첫 번째 벡터에 두 번째 벡터의 배수를 더한 행렬식은 두 개의 행렬식의 합으로 분리할 수 있습니다.
59|그런데 추가된 항에는 동일한 방향의 벡터가 두 번 등장하므로, 그 넓이는 영이 됩니다.
61|결국 원래의 행렬식만 남는 것입니다.
66|이러한 성질은 행렬의 열뿐만 아니라 행에 대해서도 동일하게 성립합니다.
71|즉, 한 행에 다른 행의 배수를 더하거나 빼더라도 행렬식은 변하지 않습니다.
74|그렇다면 이 성질을 계산에 활용해 보겠습니다.
79|첫 번째 행에는 이와 일이, 두 번째 행에는 사와 삼이 있는 행렬을 생각해 보겠습니다.
84|두 번째 행에서 첫 번째 행의 두 배를 빼면, 두 번째 행은 영과 일로 바뀝니다.
89|행렬식의 값은 그대로 유지하면서 행렬의 일부 원소를 영으로 만든 것입니다.
94|이 과정을 더 큰 행렬에 반복하면, 대각선 아래의 원소들을 차례대로 영으로 만들 수 있습니다.
99|이처럼 대각선 아래의 원소들이 모두 영인 행렬을 상삼각행렬이라고 합니다.
103|상삼각행렬이 특별한 이유는 앞서 살펴본 순열의 관점에서 이해할 수 있습니다.
111|각 행과 열에서 원소를 하나씩 선택할 때, 대각선 원소들만 선택한 경우를 제외하면 나머지 모든 선택에는 적어도 하나의 영이 포함됩니다.
116|따라서 수많은 곱셈 항이 사라지고, 대각선 원소들의 곱만 남게 됩니다.
120|이것이 가우스 소거법을 이용한 행렬식 계산의 핵심 원리입니다.
123|물론 계산 과정에서 두 행을 교환해야 할 수도 있습니다.
130|하지만 두 행을 교환하면 행렬식의 부호가 반전된다는 사실을 알고 있으므로, 그 변화만 함께 기록하면 됩니다.
135|이러한 구조를 행렬들의 곱으로 표현하는 대표적인 방법이 엘유 분해입니다.
141|복잡한 행렬을 삼각행렬들의 곱으로 표현하면, 행렬식 역시 각 행렬의 행렬식의 곱으로 계산할 수 있습니다.
149|결과적으로 팩토리얼에 비례하여 증가하던 순열 항의 직접 계산을, 행렬 크기의 세제곱에 비례하는 연산량으로 대체할 수 있습니다.
154|여기서 중요한 것은 개별 연산을 더 빠르게 수행한 것이 아니라는 점입니다.
160|우리가 구하려는 값이 어떻게 변하는지 알고 있기 때문에, 문제 자체를 계산하기 쉬운 형태로 바꿀 수 있었던 것입니다.
165|이처럼 수학적 성질에 대한 이해는 새로운 계산 알고리즘을 만들어내는 기반이 됩니다.
171|그런데 행렬식은 과연 행렬이 일으키는 공간의 변화를 얼마나 자세하게 설명할 수 있을까요?'''
lines=[];tts=[];start=0
for line in SOURCE.splitlines():
 end,s=line.split('|',1);end=int(end);tts.append(s)
 for a,b in [('오 행 오 열','5행 5열'),('백이십 개','120개'),('십 행 십 열','10행 10열'),('삼백육십만 개','360만 개'),('차례대로 영으로','차례대로 0으로'),('하나의 영이','하나의 0이'),('넓이는 영','넓이는 0'),('이와 일이','2와 1이'),('사와 삼이','4와 3이'),('영과 일로','0과 1로'),('원소를 영으로','원소를 0으로'),('원소들이 모두 영인','원소들이 모두 0인'),('엘유 분해','LU 분해')]:s=s.replace(a,b)
 lines.append(dict(start=start,end=end,text=s));start=end
def write(name,s): (R/name).write_text(s,encoding='utf-8')
write('timing.json',json.dumps(dict(duration=171,source='사용자 제공33개 문장 종료 시각',lines=lines),ensure_ascii=False,indent=2))
def stamp(s):return f'{s//3600:02}:{s%3600//60:02}:{s%60:02},000'
write('captions.srt','\n\n'.join(f'{i+1}\n{stamp(l["start"])} --> {stamp(l["end"])}\n{l["text"]}' for i,l in enumerate(lines))+'\n')
write('tts_script.txt','\n\n'.join(tts)+'\n')
write('narration.md','# 4장 · 불변성과 가우스 소거법\n\n사용자 확정33문장·171초\n\n'+'\n\n'.join(f'{l["start"]}–{l["end"]}초\n\n{l["text"]}' for l in lines)+'\n')
shots=[(0,26,'순열 직접 전개는 팩토리얼 개수의 항을 갖는다'),(26,42,'다른 열의 배수를 더해도 밑변과 높이는 유지된다'),(42,61,'다중선형성과 중복 벡터의 넓이0이 불변성을 보장한다'),(61,71,'열의 불변성은 행에도 성립한다'),(71,89,'행렬식을 유지하며 4를0으로 만든다'),(89,99,'반복 소거로 상삼각행렬을 만든다'),(99,116,'상삼각행렬은 대각선 순열 항만 남긴다'),(116,120,'가우스 소거법은 같은 행렬식을 쉬운 구조로 계산한다'),(120,130,'행 교환의 부호는 별도로 기록한다'),(130,141,'소거 계수를L에 기록하면 A=LU이다'),(141,149,'직접 전개 대신 O(n³) 산술연산으로 계산한다'),(149,160,'불변성을 알면 계산해야 할 구조를 바꿀 수 있다'),(160,165,'수학적 성질이 계산 알고리즘으로 이어진다'),(165,171,'같은 행렬식이라도 공간 변형은 다를 수 있다')]
manifest=[]
for i,(start,end,claim) in enumerate(shots,1):
 d=R/'scenes'/f'{i:02}';d.mkdir(parents=True,exist_ok=True)
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',class_name=f'Shot{i:02}',start=start,duration_seconds=end-start,claim=claim))
 (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import EliminationScene\nclass Shot'+f'{i:02}'+'(EliminationScene):\n    index='+str(i)+'\n',encoding='utf-8')
 if i==7:
  p=d/'scene.py';s=p.read_text(encoding='utf-8').replace('from visuals import EliminationScene','from visuals import EliminationScene,eq,GREEN')
  s+="    def show(self,*objects,d=.5):\n        objects=[eq(r'\\det(U)=\\prod_i u_{ii}',3,.45,30,GREEN,w=5.7) if '일반형' in getattr(obj,'text','') else obj for obj in objects]\n        return super().show(*objects,d=d)\n"
  p.write_text(s,encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02} · {claim}\n\n- 사용자 확정 구간: {start}–{end}초.\n- 16:9 1920×1080 30fps, 무음·전체자막.\n- storyboard.md와 visuals.py shot_{i:02} 기준.\n- 자막전용영역 y=-3.3. 고정v를 밑변으로 잡는다.\n- 실제 행 연산 상태에서 원소·순열 항·LU를 생성한다. 행 배수 정규화 없음.\n',encoding='utf-8')
 (d/'script.txt').write_text('\n\n'.join(tts[j] for j,l in enumerate(lines) if start<=l['start'] and l['end']<=end)+'\n',encoding='utf-8')
write('manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
