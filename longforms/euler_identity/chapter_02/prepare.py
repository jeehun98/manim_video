from pathlib import Path
import json, shutil
R=Path(__file__).resolve().parent;T=R.parents[1]/'_template'
ends=[5,8,11,15,17,21,25,28,33,38,43,45,50,54,58,63,64,71,75,80,83,86,90,93,95,101,106,112,119,124,126,130,134,138,142]
texts=[
'앞서 우리는 0과 1이 연산 속에서 특별한 역할을 한다는 사실을 살펴봤습니다.',
'이번에는 조금 다른 성질을 가진 숫자를 살펴보겠습니다.',
'크기가 서로 다른 두 개의 원을 생각해 보겠습니다.',
'하나는 작은 원이고, 다른 하나는 그보다 훨씬 큰 원입니다.',
'당연히 큰 원의 둘레가 더 길겠죠.',
'그런데 두 원의 둘레를 각각의 지름으로 나누면 어떻게 될까요?',
'놀랍게도 원의 크기와 관계없이 언제나 같은 비율이 나타납니다.',
'이 비율이 바로 원주율, 파이입니다.',
'파이는 약 3.14159로 시작하는 무한한 소수이지만, 중요한 것은 숫자의 자릿수가 아닙니다.',
'어떤 크기의 원이든, 둘레의 길이가 지름의 파이 배라는 사실입니다.',
'그렇다면 이 비율은 원의 둘레를 계산하는 것 말고도 어디에 사용될까요?',
'원을 따라 움직이는 점 하나를 생각해 보겠습니다.',
'점이 원 위를 따라 움직이면, 중심에서 점을 향하는 선의 방향도 함께 바뀝니다.',
'우리는 이 방향의 변화를 각도로 표현할 수 있습니다.',
'보통 각도는 90도, 180도처럼 도 단위로 나타냅니다.',
'하지만 수학에서는 원의 반지름과 호의 길이를 이용하는 또 다른 방법이 있습니다.',
'바로 라디안입니다.',
'원 위의 두 점 사이에 있는 호의 길이를 반지름으로 나누면, 그 사이의 중심각을 라디안으로 나타낼 수 있습니다.',
'예를 들어 반지름과 호의 길이가 같다면 그 각도는 1라디안입니다.',
'원의 둘레 전체는 반지름의 2파이 배이므로, 한 바퀴는 2파이 라디안이 됩니다.',
'그리고 반 바퀴는 파이 라디안입니다.',
'이제 원의 회전을 하나의 숫자로 표현할 수 있게 되었습니다.',
'그런데 회전하는 점의 위치는 어떻게 나타낼 수 있을까요?',
'좌표평면 위에 반지름이 1인 원을 그려보겠습니다.',
'이 원을 단위원이라고 부릅니다.',
'원이 아닌 원 위의 점 하나를 생각하면, 그 점의 위치는 가로좌표와 세로좌표로 나타낼 수 있습니다.',
'각도가 세타일 때, 가로좌표는 코사인 세타, 세로좌표는 사인 세타가 됩니다.',
'즉, 원 위의 점이 회전하는 과정은 사인과 코사인이라는 두 함수로 표현할 수 있습니다.',
'여기까지 우리는 원의 크기에서 파이라는 일정한 비율을 발견했고, 그 비율을 이용해 회전을 각도로 나타냈습니다.',
'그리고 그 각도를 통해 원 위의 점이 어디에 있는지도 계산할 수 있게 되었습니다.',
'그렇다면 한 가지 질문이 남습니다.',
'지금까지는 회전을 두 개의 좌표와 삼각함수로 표현했습니다.',
'그런데 이 회전을 숫자 하나에 대한 곱셈으로 나타낼 수도 있을까요?',
'이 질문에 답하기 위해, 다음으로 살펴볼 숫자는 조금 특별합니다.',
'바로 제곱하면 마이너스 1이 되는 수, 아이입니다.']
def spoken(s):
    for a,b in [('3.14159','삼 점 일사일오구'),('180','백팔십'),('90','구십'),('0','영'),('1','일'),('2파이','이 파이')]:s=s.replace(a,b)
    return s
lines=[dict(start=a,end=b,text=s,spoken=spoken(s)) for a,b,s in zip([0]+ends[:-1],ends,texts)]
scenes=[('opening',0,8,'1장 끝의 원과 π를 받아 기하학에 초점을 맞춘다.'),('two_circles',8,17,'반지름이 두 배인 원은 둘레도 두 배다.'),('ratio',17,28,'원의 크기에 관계없이 C/d=π다.'),('relation',28,38,'π의 핵심은 C=πd=2πr라는 관계다.'),('motion',38,54,'원 위의 이동을 중심에서 본 방향의 변화로 표현한다.'),('degrees',54,64,'각도를 호의 길이와 반지름의 비율로 측정할 수 있다.'),('radian',64,75,'θ=s/r이며 s=r이면 정확히 1라디안이다.'),('turns',75,86,'한 바퀴는 2π, 반 바퀴는 π라디안이다.'),('unit',86,95,'반지름 1인 단위원을 좌표평면에 놓는다.'),('coordinates',95,106,'단위원의 좌표는 (cosθ,sinθ)다.'),('functions',106,124,'회전하는 점의 두 좌표는 사분면에 따라 부호까지 변한다.'),('multiplication',124,134,'두 좌표로 표현한 회전을 곱셈으로 나타낼 수 있는지 묻는다.'),('imaginary',134,142,'i²=−1을 제시하며 원과 좌표축을 연결 화면으로 남긴다.')]
manifest=[]
for k,(slug,a,b,claim) in enumerate(scenes,1):
    d=R/'scenes'/f'{k:02}_{slug}';d.mkdir(parents=True,exist_ok=True)
    relevant=[x for x in lines if a<=x['start']<b]
    shutil.copyfile(T/'scenes/01_example/spec.md',d/'spec.md')
    (d/'spec.md').write_text(f'# {k:02} — {slug}\n\n## 핵심 주장\n{claim}\n\n## 확정 시간\n{a}–{b}초, {b-a}초. 사용자 제공 문장 종료 시각.\n\n## TTS\n'+'\n\n'.join(x['spoken'] for x in relevant)+'\n\n## 화면과 전환\n../../storyboard.md의 동일 시간 구간을 구현한다. 실제 구현은 ../../visuals.py의 '+slug+' 메서드. 배경 #10151F, 자막 y≈−3.35, 시각 요소는 y>−2.7. 시작은 앞 씬 종료와 같은 원·각도·좌표 상태이며 기존 도형을 변형한다.\n\n## 정확성\n유클리드 평면의 원. 두 원의 반지름은 정확히 1:2. θ와 호·점·좌표는 하나의 ValueTracker로 계산한다. 1라디안은 θ=1이며 60도로 대체하지 않는다. 단위원의 x·y 축척은 동일하고 음수 성분을 0 기준으로 표시한다. π는 항등원이 아니다. 마지막은 i²=−1의 정의를 제시하며 회전과의 관계는 증명하지 않는다.\n',encoding='utf-8')
    (d/'script.txt').write_text('\n\n'.join(x['spoken'] for x in relevant)+'\n',encoding='utf-8')
    (d/'timing.json').write_text(json.dumps(dict(start=a,duration=b-a,lines=relevant),ensure_ascii=False,indent=2),encoding='utf-8')
    (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ChapterScene\nclass Shot{k:02}(ChapterScene):\n    index={k}\n',encoding='utf-8')
    manifest.append(dict(id=f'{k:02}',directory=f'scenes/{k:02}_{slug}',class_name=f'Shot{k:02}',method=slug,start=a,duration_seconds=b-a))
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'timing.json').write_text(json.dumps(dict(duration=142,source='user sentence end times',lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
for f in ['README.md','master_script.md','scenes.yaml']:
    if not (R/f).exists():shutil.copyfile(T/f,R/f)
(R/'master_script.md').write_text('# 2장 확정 대본 — 142초\n\n'+'\n\n'.join(f"{x['start']:03}–{x['end']:03}초｜{x['text']}" for x in lines)+'\n',encoding='utf-8')
shutil.copyfile(R/'master_script.md',R/'narration.md')
(R/'tts_script.txt').write_text('\n\n'.join(x['spoken'] for x in lines)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: euler_identity_ch02\nvideo: {width: 1920, height: 1080, fps: 30}\nscenes:\n'+''.join(f"  - {{id: '{x['id']}', directory: '{x['directory']}', class: {x['class_name']}, duration_seconds: {x['duration_seconds']}}}\n" for x in manifest),encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
(R/'captions.srt').write_text('\n\n'.join(f"{k}\n{stamp(x['start'])} --> {stamp(x['end'])}\n{x['text']}" for k,x in enumerate(lines,1))+'\n',encoding='utf-8')
