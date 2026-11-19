"""Write user-approved 164-second script and independent production specs."""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent
SOURCE='''5|앞서 우리는 연립방정식의 계수들 사이에서 행렬식이라는 특별한 값을 발견했습니다.
8|이번에는 동일한 행렬을 조금 다른 관점에서 바라보겠습니다.
12|지금까지는 행렬의 각 행이 하나의 방정식을 나타냈습니다.
18|하지만 행렬의 각 열을 하나의 벡터로 바라보면, 이 행렬을 공간의 변환으로 해석할 수 있습니다.
22|먼저 좌표평면 위에 두 개의 단위벡터를 생각해 보겠습니다.
27|하나는 가로 방향으로 길이가 일인 벡터이고, 다른 하나는 세로 방향으로 길이가 일인 벡터입니다.
31|이 두 벡터를 이용하면 평면 위의 모든 점을 표현할 수 있습니다.
39|여기에 행렬을 적용하면 첫 번째 단위벡터는 에이, 씨라는 벡터로, 두 번째 단위벡터는 비, 디라는 벡터로 변합니다.
43|그리고 나머지 점들도 이 두 벡터의 변화에 따라 함께 이동합니다.
48|결과적으로 넓이가 일인 정사각형은 두 벡터가 만드는 평행사변형으로 변합니다.
52|그렇다면 이 평행사변형의 넓이는 어떻게 구할 수 있을까요?
56|먼저 평행사변형을 둘러싸는 직사각형을 만들어 보겠습니다.
62|그리고 직사각형에서 평행사변형 바깥쪽에 있는 삼각형과 직사각형의 넓이를 빼보겠습니다.
66|이 계산을 정리하면 에이 디 마이너스 비 씨라는 식이 등장합니다.
71|놀랍게도 앞서 연립방정식의 미지수를 제거할 때 등장했던 식과 동일합니다.
78|일반적으로 이 값의 절댓값은 평행사변형의 넓이이며, 원래 공간의 넓이가 몇 배로 변했는지를 나타냅니다.
82|그렇다면 행렬식이 영이라면 어떤 일이 일어날까요?
85|두 벡터가 점점 평행해지도록 공간을 변형해 보겠습니다.
90|평행사변형의 넓이는 점점 줄어들고, 결국 하나의 선분으로 눌리게 됩니다.
95|이 과정에서 서로 다른 위치에 있던 점들이 하나의 위치로 겹쳐집니다.
99|따라서 변환된 결과만으로는 원래의 위치를 유일하게 알아낼 수 없습니다.
107|이것은 앞서 행렬식이 영일 때 연립방정식의 해가 유일하게 결정되지 않았던 이유를 공간의 관점에서 보여줍니다.
110|그렇다면 행렬식이 음수가 되는 것은 어떤 의미일까요?
114|이번에는 단위 정사각형을 좌우로 뒤집어 보겠습니다.
119|정사각형의 넓이는 그대로 유지되지만, 두 벡터가 이루는 순서는 반대로 바뀝니다.
124|원래 반시계 방향이었던 꼭짓점의 순서가 시계 방향으로 변하는 것입니다.
128|행렬식의 음수 부호는 바로 이러한 공간의 방향 반전을 나타냅니다.
131|이러한 해석은 이차원 평면에만 국한되지 않습니다.
139|삼차원에서는 세 개의 단위벡터가 만드는 정육면체가 변형되며, 행렬식의 절댓값은 그 부피의 변화율을 나타냅니다.
142|더 높은 차원에서도 동일한 원리가 적용됩니다.
147|결국 행렬식은 공간의 부피 변화와 방향에 관한 정보를 하나의 숫자로 압축한 값입니다.
154|방정식에서는 해의 유일성을 결정했던 숫자가, 기하학에서는 공간의 변형과 정보의 손실을 설명하는 것이죠.
160|그런데 이러한 기하학적 성질은 행렬식의 계산 규칙에도 그대로 반영되어 있습니다.
164|그 연결을 이해하기 위해 이번에는 순열이라는 개념을 살펴보겠습니다.'''
lines=[];phonetic=[];start=0
for row in SOURCE.splitlines():
 end,s=row.split('|',1);end=int(end);phonetic.append(s)
 for old,new in [('에이 디 마이너스 비 씨','ad−bc'),('에이, 씨라는','(a,c)라는'),('비, 디라는','(b,d)라는'),('길이가 일인','길이가 1인'),('넓이가 일인','넓이가 1인'),('행렬식이 영','행렬식이 0'),('이차원','2차원'),('삼차원','3차원')]:s=s.replace(old,new)
 lines.append(dict(start=start,end=end,text=s));start=end
(R/'timing.json').write_text(json.dumps(dict(duration=164,source='사용자 제공 34개 문장 종료 시각',lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(s):return f'{s//3600:02}:{s%3600//60:02}:{s%60:02},000'
(R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(l["start"])} --> {stamp(l["end"])}\n{l["text"]}' for i,l in enumerate(lines))+'\n',encoding='utf-8')
(R/'tts_script.txt').write_text('\n\n'.join(phonetic)+'\n',encoding='utf-8')
(R/'narration.md').write_text('# 2장 · 행렬식의 기하학적 정체\n\n사용자 확정 대본 · 164초 · 34문장\n\n'+'\n\n'.join(f'{l["start"]}–{l["end"]}초\n\n{l["text"]}' for l in lines)+'\n',encoding='utf-8')
shots=[(0,18,'같은 행렬의 행과 열은 서로 다른 해석을 준다'),(18,31,'두 단위벡터의 조합으로 모든 점을 표현한다'),(31,48,'열벡터가 정하는 선형변환은 모든 점에 동일하게 작용한다'),(48,66,'바깥 도형을 빼면 평행사변형 넓이 ad−bc가 나온다'),(66,78,'방정식의 계수 조합은 넓이 배율이기도 하다'),(78,90,'행렬식 0에서는 이 예시의 공간이 직선으로 붕괴한다'),(90,99,'다른 입력이 같은 출력이 되면 유일한 복원이 불가능하다'),(99,107,'상공간의 안팎이 무한해와 해 없음을 구분한다'),(107,119,'좌우 반사는 넓이를 보존하며 방향을 뒤집는다'),(119,128,'꼭짓점의 순서를 유지하면 반전이 드러난다'),(128,142,'3차원 이상에서는 부피 변화율로 확장된다'),(142,154,'유일성과 정보 손실은 같은 선형 구조다'),(154,164,'열 순서 교환은 같은 도형의 방향 부호를 바꾼다')]
manifest=[]
for i,(start,end,claim) in enumerate(shots,1):
 d=R/'scenes'/f'{i:02}';d.mkdir(parents=True,exist_ok=True)
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',class_name=f'Shot{i:02}',start=start,duration_seconds=end-start,claim=claim))
 (d/'spec.md').write_text(f'# {i:02} · {claim}\n\n- 사용자 확정 발화 구간: {start}–{end}초.\n- 16:9 1920×1080 30fps, 무음·전체 발화 자막.\n- storyboard.md와 visuals.py의 shot_{i:02}를 따른다.\n- 자막은 y=-3.3의 전용 패널, 본문은 y>-2.65.\n- 도형·격자·점에 동일한 행렬 적용. 원점과 좌표 단위 고정.\n',encoding='utf-8')
 (d/'script.txt').write_text('\n\n'.join(phonetic[j] for j,l in enumerate(lines) if start<=l['start'] and l['end']<=end)+'\n',encoding='utf-8')
 (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import GeometryScene\nclass Shot'+f'{i:02}'+'(GeometryScene):\n    index='+str(i)+'\n',encoding='utf-8')
 if i==13:
  with (d/'scene.py').open('a',encoding='utf-8') as out:
   out.write("    def show(self,*objects,d=.5):\n        # Keep the label clear of the diagram's orientation arrows.\n        for obj in objects:\n            if '순열' in getattr(obj,'text',''):\n                obj.move_to([3,2.15,0])\n        return super().show(*objects,d=d)\n")
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
