from pathlib import Path
import json, shutil
R=Path(__file__).resolve().parent
T=R.parents[1]/'_template'
ends=[2,7,9,12,16,20,25,30,33,36,40,44,46,48,54,61,68,73,78,82,83]
texts=[
'우리는 0과 1을 가장 익숙한 숫자로 생각합니다.',
'하지만 이 두 숫자는 단순히 수량을 나타내는 것 이상의 의미를 가지고 있습니다.',
'먼저 0을 생각해 보겠습니다.',
'어떤 숫자에 0을 더해도 그 값은 변하지 않습니다.',
'5에 0을 더하면 여전히 5이고, 100에 0을 더해도 100입니다.',
'반대로 어떤 숫자에서 자기 자신을 빼면 0이 됩니다.',
'즉, 0은 덧셈에서 아무런 변화가 없는 상태를 나타내는 기준이 됩니다.',
'수학에서는 이렇게 연산을 수행해도 원래 값을 바꾸지 않는 요소를 항등원이라고 부릅니다.',
'그렇다면 곱셈에서는 어떨까요?',
'곱셈에서 0은 모든 숫자를 0으로 만들어버립니다.',
'하지만 1을 곱하면 어떤 숫자든 원래 값이 그대로 유지됩니다.',
'5에 1을 곱하면 5이고, 100에 1을 곱하면 100입니다.',
'따라서 1은 곱셈의 항등원입니다.',
'여기서 한 가지 흥미로운 사실이 있습니다.',
'우리가 사용하는 숫자와 연산이 달라지더라도, 이런 항등원의 개념은 그대로 적용될 수 있다는 것입니다.',
'예를 들어 벡터를 더할 때는 영벡터가 0과 같은 역할을 하고, 행렬을 곱할 때는 단위행렬이 1과 같은 역할을 합니다.',
'즉, 0과 1의 중요성은 단순히 숫자 자체에만 있는 것이 아니라, 연산 속에서 어떤 역할을 하는가에 있습니다.',
'그렇다면 수학의 다른 영역에서도 이처럼 특별한 역할을 하는 숫자가 존재할까요?',
'이번에는 덧셈과 곱셈을 잠시 벗어나, 원이라는 도형을 살펴보겠습니다.',
'어떤 크기의 원을 그리더라도 변하지 않는 하나의 비율이 있습니다.',
'바로 원주율, 파이입니다.']
def pronunciation(s):
    for a,b in [('100','백'),('5','오'),('0','영'),('1','일')]:s=s.replace(a,b)
    return s
lines=[dict(start=a,end=b,text=s,spoken=pronunciation(s)) for a,b,s in zip([0]+ends[:-1],ends,texts)]
scenes=[('opening',0,7,'0과 1은 수량 이상의 연산적 의미를 갖는다.'),('add_zero',7,16,'0을 더해도 수직선 위의 위치가 유지된다.'),('subtract',16,20,'자기 자신을 빼면 원점으로 돌아온다.'),('add_identity',20,30,'0은 덧셈의 항등원이다.'),('multiply',30,40,'0을 곱하면 사라지고 1을 곱하면 유지된다.'),('mul_identity',40,46,'1은 곱셈의 항등원이다.'),('extend',46,54,'항등원이라는 역할을 다른 수학적 대상으로 확장할 수 있다.'),('vector',54,58,'영벡터를 더해도 벡터는 변하지 않는다.'),('matrix',58,61,'단위행렬을 곱해도 원래 행렬과 도형이 유지된다.'),('roles',61,68,'대상이 달라도 값을 보존하는 연산의 역할이 반복된다.'),('geometry',68,78,'연산에서 원의 기하학으로 관심을 옮긴다.'),('pi',78,83,'유클리드 평면에서 원의 크기와 무관하게 C/d=π다.')]
manifest=[]
for k,(slug,a,b,claim) in enumerate(scenes,1):
    d=R/'scenes'/f'{k:02}_{slug}';d.mkdir(parents=True,exist_ok=True)
    relevant=[x for x in lines if x['start']<b and x['end']>a]
    shutil.copyfile(T/'scenes/01_example/spec.md',d/'spec.md')
    (d/'spec.md').write_text(f'# {k:02} — {slug}\n\n## 핵심 주장\n{claim}\n\n## 확정 시간\n{a}–{b}초, {b-a}초. 사용자 제공 문장 종료 시각. 벡터/행렬의 58초 시각적 전환만 첨부 콘티 기준이며 문장 자막은 54–61초를 유지한다.\n\n## TTS\n'+'\n\n'.join(x['spoken'] for x in relevant)+'\n\n## 화면·애니메이션·연결\n상세 시간별 기준: ../../storyboard.md. 구현: ../../visuals.py의 '+slug+' 메서드. 기존 상태의 수식과 도형을 이동·변형해 연결한다. 마지막 원과 π는 2장 연결 기준이며 2장 소스는 아직 없다.\n\n## 정확성\n실수의 덧셈과 곱셈을 기본으로 설명한다. 항등원은 연산에 상대적이다. 영벡터는 방향 화살표를 그리지 않고 길이 0의 점으로 표시한다. 행렬 예시는 2×2 정사각행렬 A와 I₂를 사용하고 AI₂=I₂A=A다. 도형에 I₂를 적용하는 시각화는 I₂x=x다. 원은 유클리드 평면의 원이다.\n\n## 배치\n주요 시각 요소 y>−2.7, 자막 y≈−3.35. 0·1의 회백색·흰색 유지, 역할 강조선만 파랑·황금색.\n',encoding='utf-8')
    # Do not duplicate or invent a sentence boundary at the vector/matrix cut.
    (d/'script.txt').write_text('\n\n'.join(x['spoken'] for x in lines if a<=x['start']<b)+'\n',encoding='utf-8')
    (d/'timing.json').write_text(json.dumps(dict(start=a,duration=b-a,lines=relevant),ensure_ascii=False,indent=2),encoding='utf-8')
    (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ChapterScene\nclass Shot{k:02}(ChapterScene):\n    index={k}\n',encoding='utf-8')
    manifest.append(dict(id=f'{k:02}',directory=f'scenes/{k:02}_{slug}',class_name=f'Shot{k:02}',method=slug,start=a,duration_seconds=b-a))
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'timing.json').write_text(json.dumps(dict(duration=83,source='user sentence end times',lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
for f in ['README.md','master_script.md','scenes.yaml']:
    if not (R/f).exists():shutil.copyfile(T/f,R/f)
(R/'master_script.md').write_text('# 1장 확정 대본 — 83초\n\n'+'\n\n'.join(f"{x['start']:02}–{x['end']:02}초｜{x['text']}" for x in lines)+'\n',encoding='utf-8')
shutil.copyfile(R/'master_script.md',R/'narration.md')
(R/'tts_script.txt').write_text('\n\n'.join(x['spoken'] for x in lines)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: euler_identity_ch01\nvideo: {width: 1920, height: 1080, fps: 30}\nscenes:\n'+''.join(f"  - {{id: '{x['id']}', directory: '{x['directory']}', class: {x['class_name']}, duration_seconds: {x['duration_seconds']}}}\n" for x in manifest),encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
(R/'captions.srt').write_text('\n\n'.join(f"{k}\n{stamp(x['start'])} --> {stamp(x['end'])}\n{x['text']}" for k,x in enumerate(lines,1))+'\n',encoding='utf-8')
