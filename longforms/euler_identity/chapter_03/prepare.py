from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent;T=R.parents[1]/'_template'
ends=[4,8,12,16,20,25,28,32,36,42,49,53,56,60,65,69,73,76,78,81,85,87,91,95,101,105,109,112,116,121,125,132,138,141,147,150,154,160,165,171]
spoken=[
'앞서 우리는 원 위의 점이 회전하는 과정을 각도와 좌표로 표현했습니다.',
'그렇다면 이 회전을 숫자의 곱셈만으로 나타낼 수도 있을까요?',
'이 질문에 답하기 위해, 먼저 익숙한 실수의 세계를 살펴보겠습니다.',
'어떤 실수를 자기 자신과 곱하면 결과는 항상 영 이상입니다.',
'양수를 제곱해도 양수이고, 음수를 제곱해도 양수가 됩니다.',
'따라서 실수 중에는 제곱해서 마이너스 일이 되는 숫자가 존재하지 않습니다.',
'그런데 여기서 새로운 숫자 하나를 도입해 보겠습니다.',
'제곱하면 마이너스 일이 된다는 규칙을 가진 수, 아이입니다.',
'처음에는 단순히 존재하지 않는 숫자를 억지로 만들어낸 것처럼 보일 수도 있습니다.',
'하지만 이 숫자를 도입하면, 이전에는 실수만으로 표현할 수 없었던 계산을 다룰 수 있게 됩니다.',
'예를 들어, 일과 아이를 더한 일 더하기 아이, 또는 이 더하기 삼 아이와 같은 숫자를 생각할 수 있습니다.',
'이처럼 실수와 허수 부분을 결합한 수를 복소수라고 부릅니다.',
'그런데 복소수에는 흥미로운 특징이 있습니다.',
'하나의 복소수는 두 개의 실수로 표현할 수 있다는 것입니다.',
'예를 들어 이 더하기 삼 아이는 가로좌표가 이이고, 세로좌표가 삼인 점으로 나타낼 수 있습니다.',
'이렇게 복소수를 평면 위에 표현한 것을 복소평면이라고 부릅니다.',
'이제 이 평면 위에 숫자 일을 표시해 보겠습니다.',
'실수축에서 오른쪽으로 한 칸 이동한 위치입니다.',
'그렇다면 여기에 아이를 곱하면 어떻게 될까요?',
'일에 아이를 곱하면 아이가 됩니다.',
'복소평면에서는 오른쪽을 가리키던 점이 위쪽으로 이동한 것입니다.',
'이번에는 아이에 다시 아이를 곱해 보겠습니다.',
'아이의 제곱은 마이너스 일이므로, 점은 왼쪽으로 이동합니다.',
'한 번 더 곱하면 마이너스 아이, 다시 곱하면 일로 돌아옵니다.',
'이 과정을 자세히 살펴보면, 아이를 한 번 곱할 때마다 점이 반시계 방향으로 구십 도씩 회전하고 있습니다.',
'그런데 이것은 숫자 일에서만 성립하는 성질이 아닙니다.',
'가로좌표가 에이, 세로좌표가 비인 복소수를 생각해 보겠습니다.',
'이 복소수는 에이 더하기 비아이로 표현할 수 있습니다.',
'여기에 아이를 곱하면, 에이아이 더하기 비아이 제곱이 됩니다.',
'아이의 제곱은 마이너스 일이므로, 결과는 마이너스 비 더하기 에이아이가 됩니다.',
'즉, 원래 좌표가 에이, 비였다면, 새로운 좌표는 마이너스 비, 에이가 됩니다.',
'이것은 평면 위의 점을 원점을 중심으로 반시계 방향 구십 도 회전시킨 결과와 정확히 같습니다.',
'따라서 아이를 곱한다는 것은 복소평면에서 구십 도 회전시키는 연산으로 해석할 수 있습니다.',
'이제 제곱하면 마이너스 일이 된다는 규칙도 조금 다르게 보입니다.',
'구십 도 회전을 두 번 반복하면 백팔십 도 회전하고, 원래 위치의 반대편에 도착하기 때문입니다.',
'그렇다면 여기서 한 가지 질문이 생깁니다.',
'아이를 곱하면 구십 도 회전한다는 사실은 알게 되었습니다.',
'하지만 원 위의 점은 구십 도씩 끊어서 움직이는 것이 아니라, 아주 작은 각도만큼도 연속적으로 회전할 수 있습니다.',
'그렇다면 이러한 연속적인 회전을 숫자의 연산으로 표현하려면 어떻게 해야 할까요?',
'이 질문을 해결하기 위해, 이번에는 또 다른 특별한 숫자, 자연상수 이를 살펴보겠습니다.']
screen=spoken.copy()
replacements={'구십 도':'90도','백팔십 도':'180도','마이너스 일':'−1','마이너스 아이':'−i','아이':'i'}
for k,s in enumerate(screen):
    for a,b in replacements.items():s=s.replace(a,b)
    screen[k]=s
screen[3]='어떤 실수를 자기 자신과 곱하면 결과는 항상 0 이상입니다.'
screen[10]='예를 들어, 1과 i를 더한 1+i, 또는 2+3i와 같은 숫자를 생각할 수 있습니다.'
screen[14]='예를 들어 2+3i는 가로좌표가 2이고, 세로좌표가 3인 점으로 나타낼 수 있습니다.'
screen[16]='이제 이 평면 위에 숫자 1을 표시해 보겠습니다.'
screen[19]='1에 i를 곱하면 i가 됩니다.'
screen[23]='한 번 더 곱하면 −i, 다시 곱하면 1로 돌아옵니다.'
screen[25]='그런데 이것은 숫자 1에서만 성립하는 성질이 아닙니다.'
screen[26]='가로좌표가 a, 세로좌표가 b인 복소수를 생각해 보겠습니다.'
screen[27]='이 복소수는 a+bi로 표현할 수 있습니다.'
screen[28]='여기에 i를 곱하면, ai+bi²이 됩니다.'
screen[29]='i의 제곱은 −1이므로, 결과는 −b+ai가 됩니다.'
screen[30]='즉, 원래 좌표가 (a,b)였다면, 새로운 좌표는 (−b,a)가 됩니다.'
lines=[dict(start=a,end=b,text=s,spoken=t) for a,b,s,t in zip([0]+ends[:-1],ends,screen,spoken)]
scenes=[('opening',0,12,'2장 끝의 단위원에서 실수선으로 이동한다.'),('real_square',12,25,'실수 x에 대해 x²≥0이므로 x²=−1의 실수해는 없다.'),('imaginary_unit',25,42,'i²=−1인 수를 도입하고 새로운 축을 추가한다.'),('complex_numbers',42,53,'복소수는 a+bi이며 a,b는 실수다.'),('complex_plane',53,69,'a+bi를 좌표 (a,b)와 대응시킨다.'),('one',69,76,'숫자 1은 복소평면의 (1,0)이다.'),('first_turn',76,85,'1에 i를 곱하면 반시계 90° 회전하여 i가 된다.'),('four_turns',85,101,'i의 네 번의 곱셈으로 원래 위치에 돌아온다.'),('general',101,112,'임의의 복소수 a+bi를 준비한다.'),('algebra',112,125,'i(a+bi)=ai+bi²=−b+ai이므로 좌표는 (−b,a)다.'),('rotation',125,132,'좌표 변환 (a,b)→(−b,a)는 원점 중심 반시계 90° 회전이다.'),('half_turn',132,147,'i를 두 번 곱하는 180° 회전은 부호 반전과 같다.'),('continuous',147,165,'정수 거듭제곱의 90° 단위 회전에서 연속적인 각도의 표현으로 질문을 확장한다.'),('e_transition',165,171,'자연상수 e와 지수곡선의 일부를 연결 화면으로 남긴다.')]
manifest=[]
for k,(slug,a,b,claim) in enumerate(scenes,1):
    d=R/'scenes'/f'{k:02}_{slug}';d.mkdir(parents=True,exist_ok=True)
    relevant=[x for x in lines if a<=x['start']<b]
    shutil.copyfile(T/'scenes/01_example/spec.md',d/'spec.md')
    (d/'spec.md').write_text(f'# {k:02} — {slug}\n\n## 핵심 주장\n{claim}\n\n## 확정 시간\n{a}–{b}초, {b-a}초. 사용자 문장 종료 시각 기준.\n\n## TTS\n'+'\n\n'.join(x['spoken'] for x in relevant)+'\n\n## 화면·전환\n../../storyboard.md의 동일 시간 구간을 구현한다. ../../visuals.py의 '+slug+' 메서드가 실제 시간별 애니메이션 기준이다. 원·축·벡터의 상태를 이어받고 하단 y≤−2.75를 자막에 확보한다. 첫 씬은 2장 끝 화면, 마지막 씬은 e와 희미한 지수곡선으로 마친다. 4장 소스·음원은 아직 없다.\n\n## 정확성\n실수 제곱은 0 이상이다. i²=−1이며 허수부는 실수 계수 b다. 복소수의 두 축 축척은 같다. 복소수 곱셈의 끝점은 정확히 (−b,a)이며 보간 경로는 원점 중심 90° 원호다. 원점인 복소수 0은 곱해도 그대로다. 정수 거듭제곱 iⁿ만 네 방향을 반복한다고 명시하고 임의 복소수 곱셈으로 작은 회전이 불가능하다고 주장하지 않는다.\n',encoding='utf-8')
    (d/'script.txt').write_text('\n\n'.join(x['spoken'] for x in relevant)+'\n',encoding='utf-8')
    (d/'timing.json').write_text(json.dumps(dict(start=a,duration=b-a,lines=relevant),ensure_ascii=False,indent=2),encoding='utf-8')
    (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ChapterScene\nclass Shot{k:02}(ChapterScene):\n    index={k}\n',encoding='utf-8')
    manifest.append(dict(id=f'{k:02}',directory=f'scenes/{k:02}_{slug}',class_name=f'Shot{k:02}',method=slug,start=a,duration_seconds=b-a))
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'timing.json').write_text(json.dumps(dict(duration=171,source='user sentence end times',lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
for f in ['README.md','master_script.md','scenes.yaml']:
    if not (R/f).exists():shutil.copyfile(T/f,R/f)
(R/'master_script.md').write_text('# 3장 확정 대본 — 171초\n\n'+'\n\n'.join(f"{x['start']:03}–{x['end']:03}초｜{x['text']}" for x in lines)+'\n',encoding='utf-8')
shutil.copyfile(R/'master_script.md',R/'narration.md')
(R/'tts_script.txt').write_text('\n\n'.join(spoken)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: euler_identity_ch03\nvideo: {width: 1920, height: 1080, fps: 30}\nscenes:\n'+''.join(f"  - {{id: '{x['id']}', directory: '{x['directory']}', class: {x['class_name']}, duration_seconds: {x['duration_seconds']}}}\n" for x in manifest),encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
(R/'captions.srt').write_text('\n\n'.join(f"{k}\n{stamp(x['start'])} --> {stamp(x['end'])}\n{x['text']}" for k,x in enumerate(lines,1))+'\n',encoding='utf-8')
