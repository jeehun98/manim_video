"""Materialize the approved narration, sentence timing, and independent scene specs."""
import json, shutil
from pathlib import Path
R=Path(__file__).resolve().parent
ROOT=R.parents[2]
rows=[
(2,'두 개의 일차방정식을 생각해 보겠습니다.'),
(8,'첫 번째 방정식은 2x+y=5이고, 두 번째 방정식은 x+y=3입니다.'),
(13,'이 두 방정식을 좌표평면에 나타내면, 두 직선은 하나의 점에서 만납니다.'),
(18,'그리고 그 교점의 좌표가 두 방정식을 동시에 만족하는 해가 됩니다.'),
(23,'그런데 방정식을 직접 풀지 않고도, 해가 유일하게 결정되는지 알아낼 방법은 없을까요?'),
(27,'이를 알아보기 위해 조금 더 일반적인 연립방정식을 생각해 보겠습니다.'),
(33,'첫 번째 식은 ax+by=e이고, 두 번째 식은 cx+dy=f입니다.'),
(39,'여기서 y를 없애기 위해 첫 번째 식에 d를 곱하고, 두 번째 식에 b를 곱한 다음 두 식을 빼보겠습니다.'),
(45,'그러면 y항이 사라지고, x 앞에는 ad−bc라는 계수가 남습니다.'),
(51,'흥미로운 점은 이 값이 미지수 x나 y가 아니라, 방정식의 계수들만으로 결정된다는 것입니다.'),
(55,'그렇다면 이 값이 0인지 아닌지에 따라 어떤 차이가 생길까요?'),
(62,'먼저 ad−bc가 0이 아니라면, 양변을 이 값으로 나누어 x를 유일하게 결정할 수 있습니다.'),
(64,'그리고 y 역시 유일하게 구할 수 있습니다.'),
(66,'반대로 이 값이 0이라면 어떻게 될까요?'),
(71,'이번에는 두 번째 방정식을 4x+2y=3으로 바꿔보겠습니다.'),
(76,'이 경우 두 방정식의 계수로 계산한 ad−bc는 0이 됩니다.'),
(80,'좌표평면에서는 두 직선이 서로 평행하므로 교점이 존재하지 않습니다.'),
(86,'그런데 두 번째 방정식의 오른쪽을 10으로 바꾸면, 이번에는 두 직선이 완전히 일치합니다.'),
(90,'이때는 두 방정식을 동시에 만족하는 해가 무한히 많아집니다.'),
(97,'즉, ad−bc가 0이라면 해가 없거나 무한히 많아질 수 있으며, 유일한 해는 존재하지 않습니다.'),
(103,'이처럼 방정식의 계수들만으로 해가 유일하게 결정될 수 있는지를 구별하는 특별한 값이 등장합니다.'),
(106,'이제 이 계수들을 2행 2열 행렬로 배열해 보겠습니다.'),
(112,'그리고 이 행렬에서 ad−bc로 계산되는 값을 행렬식이라고 합니다.'),
(120,'중요한 것은 행렬식이 단순히 새로운 계산 공식이 아니라, 연립방정식의 해가 유일하게 결정되는지를 나타내는 값이라는 점입니다.'),
(126,'그런데 방정식의 계수에서 나타난 이 숫자가, 어떻게 공간의 넓이와 부피까지 설명할 수 있는 걸까요?'),
]
ends=[0]+[r[0] for r in rows]
lines=[dict(start=ends[i],end=end,text=s) for i,(end,s) in enumerate(rows)]
(R/'timing.json').write_text(json.dumps(dict(duration=126,source='사용자 제공 문장 종료 시각',lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(s):return f'{s//3600:02}:{s%3600//60:02}:{s%60:02},000'
(R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(l["start"])} --> {stamp(l["end"])}\n{l["text"]}' for i,l in enumerate(lines))+'\n',encoding='utf-8')
(R/'narration.md').write_text('# 1장 · 방정식에서 나타나는 특별한 숫자\n\n사용자 확정 원고 · 126초. 일반식 우변은 숫자 2가 아닌 문자 e.\n\n'+'\n\n'.join(f'{l["start"]}–{l["end"]}초\n\n{l["text"]}' for l in lines)+'\n',encoding='utf-8')
phonetic=['두 개의 일차방정식을 생각해 보겠습니다.','첫 번째 방정식은 이 엑스 더하기 와이는 오이고, 두 번째 방정식은 엑스 더하기 와이는 삼입니다.','이 두 방정식을 좌표평면에 나타내면, 두 직선은 하나의 점에서 만납니다.','그리고 그 교점의 좌표가 두 방정식을 동시에 만족하는 해가 됩니다.','그런데 방정식을 직접 풀지 않고도, 해가 유일하게 결정되는지 알아낼 방법은 없을까요?','이를 알아보기 위해 조금 더 일반적인 연립방정식을 생각해 보겠습니다.','첫 번째 식은 에이 엑스 더하기 비 와이는 이이고, 두 번째 식은 씨 엑스 더하기 디 와이는 에프입니다.','여기서 와이를 없애기 위해 첫 번째 식에 디를 곱하고, 두 번째 식에 비를 곱한 다음 두 식을 빼보겠습니다.','그러면 와이 항이 사라지고, 엑스 앞에는 에이 디 마이너스 비 씨라는 계수가 남습니다.','흥미로운 점은 이 값이 미지수 엑스나 와이가 아니라, 방정식의 계수들만으로 결정된다는 것입니다.','그렇다면 이 값이 영인지 아닌지에 따라 어떤 차이가 생길까요?','먼저 에이 디 마이너스 비 씨가 영이 아니라면, 양변을 이 값으로 나누어 엑스를 유일하게 결정할 수 있습니다.','그리고 와이 역시 유일하게 구할 수 있습니다.','반대로 이 값이 영이라면 어떻게 될까요?','이번에는 두 번째 방정식을 사 엑스 더하기 이 와이는 삼으로 바꿔보겠습니다.','이 경우 두 방정식의 계수로 계산한 에이 디 마이너스 비 씨는 영이 됩니다.','좌표평면에서는 두 직선이 서로 평행하므로 교점이 존재하지 않습니다.','그런데 두 번째 방정식의 오른쪽을 십으로 바꾸면, 이번에는 두 직선이 완전히 일치합니다.','이때는 두 방정식을 동시에 만족하는 해가 무한히 많아집니다.','즉, 에이 디 마이너스 비 씨가 영이라면 해가 없거나 무한히 많아질 수 있으며, 유일한 해는 존재하지 않습니다.','이처럼 방정식의 계수들만으로 해가 유일하게 결정될 수 있는지를 구별하는 특별한 값이 등장합니다.','이제 이 계수들을 이 행 이 열 행렬로 배열해 보겠습니다.','그리고 이 행렬에서 에이 디 마이너스 비 씨로 계산되는 값을 행렬식이라고 합니다.','중요한 것은 행렬식이 단순히 새로운 계산 공식이 아니라, 연립방정식의 해가 유일하게 결정되는지를 나타내는 값이라는 점입니다.','그런데 방정식의 계수에서 나타난 이 숫자가, 어떻게 공간의 넓이와 부피까지 설명할 수 있는 걸까요?']
(R/'tts_script.txt').write_text('\n\n'.join(phonetic)+'\n',encoding='utf-8')
shots=[(0,23,'두 직선의 교점은 동시에 만족하는 해다'),(23,33,'수치 계수를 일반 계수로 확장한다'),(33,45,'y를 소거하면 ad−bc가 남는다'),(45,55,'이 값에는 계수만 참여한다'),(55,66,'0이 아니면 두 미지수가 유일하다'),(66,80,'계수 변화로 평행해져 해가 사라진다'),(80,90,'우변 변화로 일치하면 무한히 많은 해다'),(90,97,'0은 유일해 부재를 뜻한다'),(97,106,'계수의 행과 열을 유지해 배열한다'),(106,112,'이 값에 행렬식이라는 이름을 붙인다'),(112,120,'행렬식은 해의 유일성을 판별한다'),(120,126,'같은 배열을 두 열벡터로 읽는다')]
manifest=[]
for i,(start,end,claim) in enumerate(shots,1):
 d=R/'scenes'/f'{i:02}';d.mkdir(parents=True,exist_ok=True)
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',class_name=f'Shot{i:02}',start=start,duration_seconds=end-start,claim=claim))
 (d/'spec.md').write_text(f'# {i:02} · {claim}\n\n- 확정 구간: {start}–{end}초 ({end-start}초)\n- 16:9 1920×1080 30fps. 하단 자막 전용 영역.\n- 사용자 콘티 storyboard.md와 visuals.py의 shot_{i:02} 기준.\n- 음원 미제공: 무음. 문장 종료 시각 변경 없음.\n',encoding='utf-8')
 (d/'script.txt').write_text('\n\n'.join(phonetic[j] for j,l in enumerate(lines) if l['start']>=start and l['end']<=end)+'\n',encoding='utf-8')
 (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ChapterScene\nclass Shot'+f'{i:02}'+'(ChapterScene):\n    index='+str(i)+'\n',encoding='utf-8')
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
if not (R/'README.md').exists():shutil.copyfile(ROOT/'longforms/_template/README.md',R/'README.md')
