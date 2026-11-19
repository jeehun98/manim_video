"""Materialize approved 168-second narration and scene specifications."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
SOURCE='''9|앞서 우리는 행렬식의 절댓값이 공간의 넓이와 부피의 변화율을 나타내며, 그 부호는 공간의 방향을 나타낸다는 사실을 살펴봤습니다.
14|그렇다면 이러한 기하학적 성질은 행렬식의 계산 공식에 어떻게 반영되어 있을까요?
18|먼저 두 벡터가 만드는 평행사변형을 생각해 보겠습니다.
22|한 벡터의 길이를 두 배로 늘리면, 평행사변형의 넓이도 두 배가 됩니다.
31|또한 하나의 벡터를 두 벡터의 합으로 표현하면, 부호 있는 넓이도 각각의 벡터가 만드는 부호 있는 넓이의 합으로 나누어 표현할 수 있습니다.
35|이처럼 행렬식은 각각의 열벡터에 대해 선형적인 성질을 갖습니다.
38|이번에는 두 벡터의 순서를 바꿔보겠습니다.
44|평행사변형의 모양과 넓이는 그대로 유지되지만, 꼭짓점의 순환 방향은 반대로 바뀝니다.
47|따라서 행렬식의 부호도 반대로 바뀌게 됩니다.
51|이 두 가지 성질을 이용하면 행렬식의 계산 구조를 이해할 수 있습니다.
56|먼저 행렬의 첫 번째 열벡터를 가로 방향과 세로 방향의 성분으로 나누어 보겠습니다.
60|두 번째 열벡터도 같은 방식으로 나눌 수 있습니다.
66|행렬식의 선형적인 성질을 이용하면, 두 벡터가 만드는 부호 있는 넓이를 네 가지 조합으로 나누어 계산할 수 있습니다.
72|그런데 두 벡터가 모두 가로 방향이거나 모두 세로 방향이라면, 평행사변형의 넓이는 영이 됩니다.
76|결국 서로 다른 방향의 성분을 선택한 두 가지 경우만 남습니다.
82|첫 번째 벡터에서 가로 성분을, 두 번째 벡터에서 세로 성분을 선택하면 에이 디가 됩니다.
88|반대로 첫 번째 벡터에서 세로 성분을, 두 번째 벡터에서 가로 성분을 선택하면 비 씨가 됩니다.
93|하지만 두 번째 경우에는 기본 벡터의 순서가 뒤바뀌어 있으므로 부호가 반대가 됩니다.
96|결국 행렬식은 에이 디 마이너스 비 씨가 되는 것입니다.
100|그렇다면 이러한 규칙을 삼차원으로 확장하면 어떻게 될까요?
104|이번에는 세 개의 열벡터를 각각 세 방향의 성분으로 나누어 보겠습니다.
109|각 벡터에서 하나의 방향을 선택하면 모두 스물일곱 가지 조합이 만들어집니다.
114|하지만 같은 방향이 두 번 이상 선택된 경우에는 삼차원 부피가 영이 됩니다.
118|따라서 서로 다른 세 방향을 하나씩 선택한 여섯 가지 경우만 남게 됩니다.
123|이것은 일, 이, 삼이라는 세 숫자를 서로 다른 순서로 배열하는 것과 같습니다.
125|이러한 배열을 순열이라고 합니다.
133|그리고 두 원소의 위치를 교환할 때마다 공간의 방향이 반전되므로, 교환 횟수가 짝수인지 홀수인지에 따라 각 항의 부호가 결정됩니다.
137|일반적인 엔 행 엔 열 행렬에서도 동일한 원리가 적용됩니다.
145|각 행과 열에서 원소를 하나씩 선택해 곱하고, 순열의 홀짝성에 따라 부호를 결정한 뒤, 모든 항을 더하는 것입니다.
147|이러한 표현을 라이프니츠 공식이라고 합니다.
153|즉, 행렬식에 등장하는 순열과 부호는 임의로 만들어진 계산 규칙이 아닙니다.
158|공간의 부피와 방향을 계산하는 과정에서 자연스럽게 나타나는 수학적 구조인 것입니다.
163|그런데 행렬의 크기가 커지면 가능한 순열의 개수도 폭발적으로 증가합니다.
168|그렇다면 이러한 모든 조합을 직접 계산하지 않고도 행렬식을 구할 수 있을까요?'''
lines=[];phonetic=[];start=0
for row in SOURCE.splitlines():
 end,s=row.split('|',1);end=int(end);phonetic.append(s)
 for old,new in [('에이 디 마이너스 비 씨','ad−bc'),('에이 디','ad'),('비 씨','bc'),('일, 이, 삼','1, 2, 3'),('엔 행 엔 열','n행 n열'),('스물일곱 가지','27가지'),('삼차원','3차원'),('넓이는 영','넓이는 0'),('부피가 영','부피가 0')]:s=s.replace(old,new)
 lines.append(dict(start=start,end=end,text=s));start=end
def write(name,s): (R/name).write_text(s,encoding='utf-8')
write('timing.json',json.dumps(dict(duration=168,source='사용자 제공 34개 문장 종료 시각',lines=lines),ensure_ascii=False,indent=2))
def stamp(s):return f'{s//3600:02}:{s%3600//60:02}:{s%60:02},000'
write('captions.srt','\n\n'.join(f'{i+1}\n{stamp(l["start"])} --> {stamp(l["end"])}\n{l["text"]}' for i,l in enumerate(lines))+'\n')
write('tts_script.txt','\n\n'.join(phonetic)+'\n')
write('narration.md','# 3장 · 행렬식의 계산 규칙 — 순열과 방향\n\n사용자 확정 34문장·168초\n\n'+'\n\n'.join(f'{l["start"]}–{l["end"]}초\n\n{l["text"]}' for l in lines)+'\n')
shots=[(0,14,'넓이와 방향은 계산 규칙으로 이어진다'),(14,22,'한 열의 배수는 부호 있는 넓이를 같은 배수로 바꾼다'),(22,35,'벡터 합은 부호 있는 넓이의 합으로 분해된다'),(35,51,'열 교환은 같은 도형의 방향만 뒤집는다'),(51,66,'각 열의 한 성분씩 선택하면 네 조합이 나온다'),(66,76,'같은 기본 방향을 선택하면 넓이는 0이다'),(76,96,'정규화와 교대성으로 ad−bc가 도출된다'),(96,109,'세 열에서 세 방향을 선택하면 27개 성분 조합이 생긴다'),(109,118,'중복 기본 방향을 제거하면 여섯 조합만 남는다'),(118,133,'남은 조합은 순열이며 교환 홀짝성이 부호를 정한다'),(133,147,'열마다 서로 다른 행을 선택한 곱의 합이 라이프니츠 공식이다'),(147,158,'성분 분해와 방향이 대수적 계산 구조를 만든다'),(158,168,'순열 항은 팩토리얼로 증가한다')]
manifest=[]
for i,(start,end,claim) in enumerate(shots,1):
 d=R/'scenes'/f'{i:02}';d.mkdir(parents=True,exist_ok=True)
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',class_name=f'Shot{i:02}',start=start,duration_seconds=end-start,claim=claim))
 (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import RuleScene\nclass Shot'+f'{i:02}'+'(RuleScene):\n    index='+str(i)+'\n',encoding='utf-8')
 if i in [8,11]:
  p=d/'scene.py';s=p.read_text(encoding='utf-8').replace('from visuals import RuleScene','from visuals import RuleScene,Matrix,PURPLE')
  s+='''    def add(self,*objects):
        for obj in objects:
            if isinstance(obj,Matrix) and len(obj.get_columns())==3:
                obj.get_columns()[2].set_color(PURPLE)
        return super().add(*objects)
'''
  p.write_text(s,encoding='utf-8')
 if i==6:
  (d/'scene.py').write_text('''import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import RuleScene,combo,VGroup,Indicate,Transform,MUTED,GREEN
class Shot06(RuleScene):
    index=6
    def shot_06(self):
        panels=VGroup(*[combo(p,x,y) for p,x,y in [((0,0),-3.4,1),((0,1),3.4,1),((1,0),-3.4,-1.3),((1,1),3.4,-1.3)]])
        panels.scale(.85).move_to([0,.25,0]);self.add(panels)
        self.act(.6,Indicate(panels[0],color=MUTED),Indicate(panels[3],color=MUTED))
        note=self.note('det(e₁,e₁) = det(e₂,e₂) = 0',MUTED);self.show(note,d=.4);self.to(72)
        self.act(.6,panels[0].animate.set_opacity(.12),panels[3].animate.set_opacity(.12))
        self.act(.5,Transform(note,self.note('같은 방향은 0 · 서로 다른 두 방향만 남는다',GREEN)));self.to(76)
''',encoding='utf-8')
 if i==10:
  (d/'scene.py').write_text('''import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import RuleScene,tx
class Shot10(RuleScene):
    index=10
    def show(self,*objects,d=.5):
        for obj in objects:
            if '기준순서'==getattr(obj,'text','').replace(' ',''):
                obj.become(tx('순서와 부호',-4.9,.8,25,w=2.4))
        return super().show(*objects,d=d)
''',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02} · {claim}\n\n- 사용자 확정 구간 {start}–{end}초.\n- 16:9 1920×1080 30fps. 무음·전체 문장 자막.\n- storyboard.md와 visuals.py shot_{i:02} 기준.\n- 자막 전용 패널 y=-3.3, 본문 하단 y>-2.65.\n- 순열 j번째 값은 j열에서 선택한 행 번호. 열 색과 방향 번호를 구별한다.\n',encoding='utf-8')
 (d/'script.txt').write_text('\n\n'.join(phonetic[j] for j,l in enumerate(lines) if start<=l['start'] and l['end']<=end)+'\n',encoding='utf-8')
write('manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
