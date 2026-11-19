"""Approved introduction: ten sentence endpoints, 71 seconds."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent
SOURCE='''6|오늘날 우리는 행렬을 배우고 난 뒤, 그 행렬에서 하나의 숫자를 계산하는 방법인 행렬식을 배웁니다.
13|하지만 흥미롭게도 수학의 역사에서는 행렬식에 관한 연구가 현대적인 행렬 이론보다 먼저 등장했습니다.
23|십칠 세기 후반, 일본의 수학자 세키 다카카즈와 유럽의 수학자 라이프니츠는 서로 독립적으로 오늘날 행렬식이라고 부르는 수학적 구조를 발견했습니다.
31|그 출발점은 공간의 넓이나 부피를 계산하는 것이 아니라, 여러 방정식에서 미지수를 제거하고 해에 관한 정보를 알아내는 문제였습니다.
40|이후 천칠백오십 년, 수학자 크라메르는 여러 개의 연립방정식의 해를 행렬식에 해당하는 표현들의 비율로 구하는 일반적인 방법을 제시했습니다.
48|그리고 십구 세기에 들어 행렬 이론이 발전하면서, 행렬식은 공간의 변환과도 깊은 관계를 갖는 개념으로 자리 잡았습니다.
54|그런데 어떻게 방정식을 연구하다 발견한 하나의 숫자가 공간의 부피와 방향을 설명할 수 있게 된 것일까요?
57|그리고 그 안에는 어떠한 수학적 구조가 숨어 있을까요?
67|이번 영상에서는 행렬식이 왜 필요한지부터 시작하여, 그 기하학적 의미와 계산 공식이 만들어지는 원리, 그리고 효율적인 계산 방법까지 살펴보겠습니다.
71|먼저 행렬식의 출발점이었던 방정식의 문제로 돌아가 보겠습니다.'''
shots=[(0,6,'현대의 학습 순서: 행렬에서 행렬식으로'),(6,13,'행렬식 연구는 현대 행렬 이론보다 먼저였다'),(13,23,'세키와 라이프니츠의 독립적인 연구'),(23,31,'출발점은 방정식에서 미지수를 제거하는 문제'),(31,40,'크라메르의 일반 규칙은 표현의 비율로 해를 구한다'),(40,48,'현대 행렬 이론과 공간의 변환'),(48,57,'방정식과 공간에 같은 수식이 등장하는 이유'),(57,67,'네 가지 관점의 본편 흐름'),(67,71,'구체적인 연립방정식으로 연결')]
lines=[];tts=[];start=0
for row in SOURCE.splitlines():
 end,s=row.split('|',1);end=int(end);tts.append(s)
 for a,b in [('십칠 세기','17세기'),('천칠백오십 년','1750년'),('십구 세기','19세기')]:s=s.replace(a,b)
 lines.append(dict(start=start,end=end,text=s));start=end
def write(n,s):(R/n).write_text(s,encoding='utf-8')
def stamp(s):return f'{s//3600:02}:{s%3600//60:02}:{s%60:02},000'
write('timing.json',json.dumps(dict(duration=71,source='사용자 제공10개 문장 종료 시각',lines=lines),ensure_ascii=False,indent=2))
write('captions.srt','\n\n'.join(f'{i+1}\n{stamp(l["start"])} --> {stamp(l["end"])}\n{l["text"]}' for i,l in enumerate(lines))+'\n')
write('tts_script.txt','\n\n'.join(tts)+'\n')
write('narration.md','# 0장 · 행렬식은 왜 등장했을까?\n\n사용자 확정10문장·71초\n\n'+'\n\n'.join(f'{l["start"]}–{l["end"]}초\n\n{l["text"]}' for l in lines)+'\n')
manifest=[]
for i,(a,b,claim) in enumerate(shots,1):
 d=R/'scenes'/f'{i:02}';d.mkdir(parents=True,exist_ok=True)
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',class_name=f'Shot{i:02}',start=a,duration_seconds=b-a,claim=claim))
 (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import IntroScene\nclass Shot'+f'{i:02}'+'(IntroScene):\n    index='+str(i)+'\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02} · {claim}\n\n- 확정 구간 {a}–{b}초, 16:9 1920×1080 30fps.\n- storyboard.md와 visuals.py shot_{i:02} 기준.\n- 대본·발화시간 유지, 전체 자막, 음원 미제공으로 무음.\n- 수식은 현대 표기로 재구성하며 역사적 원문으로 묘사하지 않는다.\n- 역사적 인물은 이름·연도·연구 주제 카드로 표현한다.\n- 세키의 다항식 소거와 라이프니츠의 연립방정식 연구를 구별한다.\n- Cramer 공식은 분모가 0이 아닐 때 적용한다.\n- 마지막 71초 종료, 추가 엔드카드 없음.\n',encoding='utf-8')
 (d/'script.txt').write_text('\n\n'.join(tts[j] for j,l in enumerate(lines) if a<=l['start'] and l['end']<=b)+'\n',encoding='utf-8')
write('manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
