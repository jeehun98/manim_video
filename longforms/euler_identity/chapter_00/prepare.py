"""Materialize approved narration and user-supplied sentence boundaries."""
from pathlib import Path
import json, shutil

R = Path(__file__).resolve().parent
T = R.parents[1] / '_template'
ends = [3,8,10,13,17,19,23,26,28,30,31,35,39,42,45,53,57,58]
spoken = [
'수학에는 수없이 많은 숫자와 공식이 존재합니다.',
'그런데 그중에는 수학의 서로 다른 영역에서 특별한 역할을 하는 숫자들이 있습니다.',
'아무것도 더하지 않는 수, 영.',
'어떤 수에 곱해도 그 값을 바꾸지 않는 수, 일.',
'원의 둘레와 지름 사이에서 발견되는 수, 파이.',
'제곱하면 마이너스 일이 되는 수, 아이.',
'그리고 연속적인 변화를 설명할 때 등장하는 수, 자연상수 이.',
'이 숫자들은 서로 다른 수학적 개념에서 등장합니다.',
'영과 일은 기본적인 연산에서,',
'파이는 원과 기하학에서,',
'아이는 복소수에서,',
'그리고 이는 지수함수와 미적분에서 중요한 역할을 합니다.',
'그런데 놀랍게도, 이 다섯 숫자는 단 하나의 식으로 연결됩니다.',
'이의 아이 파이 제곱, 더하기 일은 영.',
'이것이 바로 오일러의 항등식입니다.',
'어떻게 원을 설명하는 파이와, 연속적인 변화를 나타내는 이, 그리고 제곱하면 음수가 되는 허수가 하나의 식에서 만날 수 있을까요?',
'이 관계를 이해하기 위해, 가장 익숙한 두 숫자부터 시작해 보겠습니다.',
'영과 일입니다.']
screen = spoken.copy()
screen[2]='아무것도 더하지 않는 수, 0.'
screen[3]='어떤 수에 곱해도 그 값을 바꾸지 않는 수, 1.'
screen[4]='원의 둘레와 지름 사이에서 발견되는 수, π.'
screen[5]='제곱하면 −1이 되는 수, i.'
screen[6]='그리고 연속적인 변화를 설명할 때 등장하는 수, 자연상수 e.'
screen[8]='0과 1은 기본적인 연산에서,'
screen[9]='π는 원과 기하학에서,'
screen[10]='i는 복소수에서,'
screen[11]='그리고 e는 지수함수와 미적분에서 중요한 역할을 합니다.'
screen[13]='e의 iπ제곱, 더하기 1은 0.'
screen[15]='어떻게 원을 설명하는 π와, 연속적인 변화를 나타내는 e, 그리고 제곱하면 음수가 되는 허수가 하나의 식에서 만날 수 있을까요?'
screen[17]='0과 1입니다.'
records=[dict(start=a,end=b,text=s,spoken=t) for a,b,s,t in zip([0]+ends[:-1],ends,screen,spoken)]
scenes=[('world',0,8,'수많은 수학적 기호에서 다섯 상수에 초점을 맞춘다.'),('zero',8,10,'0을 더하면 값이 유지된다.'),('one',10,13,'1을 곱하면 값이 유지된다.'),('pi',13,17,'π는 원의 둘레와 지름의 비율이다.'),('imaginary',17,19,'i를 두 번 곱하면 −1이 된다.'),('exponential',19,23,'e는 지수함수와 연속적인 변화에 등장한다.'),('domains',23,35,'다섯 상수는 서로 다른 개념에서 중요한 역할을 한다.'),('identity',35,45,'다섯 상수가 오일러 항등식으로 모인다.'),('question',45,53,'기하학·변화·복소수가 하나의 식에서 만나는 이유를 묻는다.'),('transition',53,58,'0과 1을 중심에 남겨 본문으로 연결한다.')]
manifest=[]
for k,(slug,a,b,claim) in enumerate(scenes,1):
    d=R/'scenes'/f'{k:02}_{slug}'; d.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(T/'scenes'/'01_example'/'spec.md',d/'spec.md')
    lines=[x for x in records if a<=x['start']<b]
    (d/'script.txt').write_text('\n\n'.join(x['spoken'] for x in lines)+'\n',encoding='utf-8')
    (d/'timing.json').write_text(json.dumps(dict(start=a,duration=b-a,lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
    (d/'spec.md').write_text(f'# {k:02} — {slug}\n\n## 핵심 주장\n{claim}\n\n## 확정 시간\n{a}–{b}초, {b-a}초. 사용자 문장 종료 시각 기준. TTS 음원 미제공.\n\n## TTS\n'+ '\n\n'.join(x['spoken'] for x in lines)+f'\n\n## 화면과 전환\n16:9, #10151F 배경. scene.py의 {slug} 메서드가 구현 기준. 하단 자막 영역 y≤−2.8을 확보한다. '+('이전 장면의 종료 상태를 받아 이어간다.' if k>1 else '남색 암전에서 수학 기호가 등장한다.')+'\n\n## 정확성\nπ=C/d. i²=−1이며 i의 곱셈은 반시계 90° 회전. e 곡선은 exp(x)의 실제 좌표. 이 장에서는 항등식의 증명을 제시하지 않는다.\n',encoding='utf-8')
    (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import IntroScene\nclass Shot{k:02}(IntroScene):\n    index={k}\n',encoding='utf-8')
    manifest.append(dict(id=f'{k:02}',directory=f'scenes/{k:02}_{slug}',class_name=f'Shot{k:02}',start=a,duration_seconds=b-a))
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'timing.json').write_text(json.dumps(dict(duration=58,source='user sentence end times',lines=records),ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['README.md','master_script.md','scenes.yaml']:
    if not (R/name).exists():shutil.copyfile(T/name,R/name)
(R/'master_script.md').write_text('# 0장 확정 대본 — 58초\n\n'+'\n\n'.join(f"{x['start']:02}–{x['end']:02}초｜{x['text']}" for x in records)+'\n',encoding='utf-8')
(R/'narration.md').write_text((R/'master_script.md').read_text(encoding='utf-8'),encoding='utf-8')
(R/'tts_script.txt').write_text('\n\n'.join(spoken)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: euler_identity_ch00\nvideo: {width: 1920, height: 1080, fps: 30}\nscenes:\n'+''.join(f"  - {{id: '{x['id']}', directory: '{x['directory']}', class: {x['class_name']}, duration_seconds: {x['duration_seconds']}}}\n" for x in manifest),encoding='utf-8')
def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(R/'captions.srt').write_text('\n\n'.join(f"{k}\n{stamp(x['start'])} --> {stamp(x['end'])}\n{x['text']}" for k,x in enumerate(records,1))+'\n',encoding='utf-8')
