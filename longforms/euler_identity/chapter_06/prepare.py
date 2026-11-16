from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent;T=R.parents[1]/'_template'
ends=[7,12,14,18,24,27,31,35,40,42,45,48,52,54,56,60,63,65,67,70,73,76,83,89,92,96,100,104,111,116,120,126,134,138,141,143]
texts='''앞서 우리는 지수함수와 허수의 성질을 결합하면, 복소평면에서 연속적인 회전을 표현할 수 있다는 사실을 살펴봤습니다.
이의 아이 세타 제곱은 코사인 세타 더하기 아이 사인 세타와 같습니다.
이것이 바로 오일러 공식이었습니다.
그렇다면 이 회전을 정확히 반 바퀴만큼 진행하면 어떻게 될까요?
앞서 우리는 원의 한 바퀴가 2파이 라디안이고, 반 바퀴는 파이 라디안이라는 사실을 배웠습니다.
따라서 세타에 파이를 넣어보겠습니다.
그러면 이의 아이 파이 제곱은 코사인 파이 더하기 아이 사인 파이가 됩니다.
복소평면에서 숫자 1은 실수축의 오른쪽에 위치합니다.
이 점이 반시계 방향으로 반 바퀴 회전하면, 실수축의 왼쪽에 도착합니다.
그 위치는 바로 마이너스 1입니다.
삼각함수로 계산해도 같은 결과가 나옵니다.
코사인 파이는 마이너스 1이고, 사인 파이는 0입니다.
따라서 이의 아이 파이 제곱은 마이너스 1이 됩니다.
이제 양변에 1을 더하면,
이의 아이 파이 제곱, 더하기 1은 0.
마침내 영상의 처음에 등장했던 오일러 항등식이 완성되었습니다.
이 식에는 다섯 개의 특별한 숫자가 등장합니다.
덧셈에서 원래 값을 유지하는 0.
곱셈에서 원래 값을 유지하는 1.
원의 기하학과 회전의 각도를 연결하는 파이.
복소평면에서 90도 회전을 나타내는 허수 아이.
그리고 연속적인 변화와 관련된 자연상수 이입니다.
이 숫자들은 서로 다른 수학적 개념에서 등장했지만, 오일러 항등식에서는 하나의 관계로 연결됩니다.
그렇다면 이 공식이 특별한 이유는 단순히 유명한 숫자 다섯 개가 한 식에 등장하기 때문일까요?
우리가 지금까지 살펴본 내용을 다시 생각해 보겠습니다.
지수함수는 현재 값에 비례하는 연속적인 변화를 표현했습니다.
허수는 숫자의 곱셈을 평면의 회전으로 해석할 수 있게 했습니다.
파이는 원의 회전을 각도로 나타내는 과정에서 등장했습니다.
그리고 이 개념들을 결합하자 지수함수와 삼각함수가 같은 회전을 표현한다는 사실을 발견했습니다.
오일러 항등식은 이러한 관계에서 특별한 각도 하나를 선택한 결과입니다.
이 공식이 아름다운 이유는 서로 다른 숫자가 우연히 모였기 때문만은 아닙니다.
서로 다른 수학적 개념들이 사실은 하나의 구조로 연결될 수 있다는 것을 보여주기 때문입니다.
우리가 처음에는 전혀 다른 것으로 생각했던 성장과 회전, 지수함수와 삼각함수는 복소수라는 관점에서 하나로 이어집니다.
그리고 그 관계가 가장 간결하게 드러나는 순간,
우리는 다시 처음의 식으로 돌아오게 됩니다.
이의 아이 파이 제곱, 더하기 1은 0.'''.splitlines()
assert len(texts)==len(ends)==36
screen=texts.copy()
replacements={1:'e의 iθ제곱은 cosθ+i sinθ와 같습니다.',4:'앞서 우리는 원의 한 바퀴가 2π 라디안이고, 반 바퀴는 π 라디안이라는 사실을 배웠습니다.',5:'따라서 θ에 π를 넣어보겠습니다.',6:'그러면 e의 iπ제곱은 cosπ+i sinπ가 됩니다.',11:'cosπ는 −1이고, sinπ는 0입니다.',12:'따라서 e의 iπ제곱은 −1이 됩니다.',14:'e의 iπ제곱, 더하기 1은 0.',19:'원의 기하학과 회전의 각도를 연결하는 π.',20:'복소평면에서 90도 회전을 나타내는 허수 i.',21:'그리고 연속적인 변화와 관련된 자연상수 e입니다.',35:'e의 iπ제곱, 더하기 1은 0.'}
for k,s in replacements.items():screen[k]=s
def pronounce(s):
    return s.replace('90','구십').replace('2파이','이 파이').replace('마이너스 1','마이너스 일').replace('숫자 1','숫자 일').replace('더하기 1','더하기 일').replace('유지하는 0','유지하는 영').replace('유지하는 1','유지하는 일').replace('은 0','은 영')
lines=[dict(start=a,end=b,text=s,spoken=pronounce(t)) for a,b,s,t in zip([0]+ends[:-1],ends,screen,texts)]
scenes=[('opening',0,14,'오일러 공식은 복소 지수와 단위원의 같은 위치를 표현한다.'),('half_turn_angle',14,27,'반 바퀴의 각도는 π 라디안이다.'),('half_turn',27,42,'1을 반시계 방향으로 π만큼 회전하면 −1이다.'),('evaluate',42,52,'cosπ=−1, sinπ=0이 기하학적 결과와 일치한다.'),('identity_assembly',52,60,'양변에 1을 더해 오일러 항등식을 얻는다.'),('five_meanings',60,76,'다섯 상수는 서로 다른 수학적 역할을 갖는다.'),('one_relation',76,89,'다섯 상수는 하나의 항등식에 함께 등장한다.'),('principles',89,104,'지수적 변화, 복소수 곱셈, 라디안이 회전 설명의 구성 요소다.'),('special_angle',104,116,'오일러 항등식은 일반적인 오일러 공식에서 θ=π를 선택한 결과다.'),('connected_structure',116,134,'복소수로 확장한 지수함수와 삼각함수는 같은 회전을 표현한다.'),('ending',134,143,'처음의 항등식으로 돌아와 영상의 결론을 완성한다.')]
manifest=[]
for k,(slug,a,b,claim) in enumerate(scenes,1):
    d=R/'scenes'/f'{k:02}_{slug}';d.mkdir(parents=True,exist_ok=True)
    relevant=[x for x in lines if a<=x['start']<b]
    shutil.copyfile(T/'scenes/01_example/spec.md',d/'spec.md')
    (d/'spec.md').write_text(f'# {k:02} — {slug}\n\n## 핵심 주장\n{claim}\n\n## 확정 길이와 TTS\n{a}–{b}초, {b-a}초. 사용자 제공 문장 종료 시각을 그대로 적용한다. 음원 미제공, 무음.\n\n'+'\n\n'.join(x['spoken'] for x in relevant)+f'\n\n## 화면과 타임라인\n../../storyboard.md의 Scene {k:02}를 따른다. 실제 시간은 timing.json과 visuals.py의 {slug} 메서드로 고정한다. 화면 내용은 y>−2.7, 전체 문장 자막은 y≈−3.35.\n\n## 시작·종료 및 연결\n수식과 단위원의 직전 상태를 재구성해 전환한다. 처음에는 5장 마지막 화면을 이어받고 마지막에는 0장과 동일한 색상·크기·위치의 항등식만 남긴다. 별도 예고·엔드카드·길이 연장은 없다.\n\n## 정확성\n양의 각도는 반시계 방향, 원의 가로·세로 단위는 같다. θ=π에서 점은 (−1,0), cosπ=−1, sinπ=0이다. 양변에 같은 1을 더한다. 0과 1은 각각 덧셈·곱셈 항등원이며 회전을 생성하는 별도 인자가 아니다. 실수 지수함수 그래프를 원으로 왜곡하지 않고 복소수 확장 e^(iθ)를 명시한다.\n',encoding='utf-8')
    (d/'script.txt').write_text('\n\n'.join(x['spoken'] for x in relevant)+'\n',encoding='utf-8')
    (d/'timing.json').write_text(json.dumps(dict(start=a,duration=b-a,lines=relevant),ensure_ascii=False,indent=2),encoding='utf-8')
    (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ChapterScene\nclass Shot{k:02}(ChapterScene):\n    index={k}\n',encoding='utf-8')
    manifest.append(dict(id=f'{k:02}',directory=f'scenes/{k:02}_{slug}',class_name=f'Shot{k:02}',method=slug,start=a,duration_seconds=b-a))
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'timing.json').write_text(json.dumps(dict(duration=143,source='user sentence end times',lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
for f in ['README.md','master_script.md','scenes.yaml']:
    if not (R/f).exists():shutil.copyfile(T/f,R/f)
(R/'master_script.md').write_text('# 6장 확정 대본 — 143초\n\n'+'\n\n'.join(f"{x['start']:03}–{x['end']:03}초｜{x['text']}" for x in lines)+'\n',encoding='utf-8')
shutil.copyfile(R/'master_script.md',R/'narration.md')
(R/'tts_script.txt').write_text('\n\n'.join(x['spoken'] for x in lines)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: euler_identity_ch06\nvideo: {width: 1920, height: 1080, fps: 60}\nscenes:\n'+''.join(f"  - {{id: '{x['id']}', directory: '{x['directory']}', class: {x['class_name']}, duration_seconds: {x['duration_seconds']}}}\n" for x in manifest),encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
(R/'captions.srt').write_text('\n\n'.join(f"{k}\n{stamp(x['start'])} --> {stamp(x['end'])}\n{x['text']}" for k,x in enumerate(lines,1))+'\n',encoding='utf-8')
