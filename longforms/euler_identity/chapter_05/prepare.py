from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent;T=R.parents[1]/'_template'
ends=[5,11,15,19,25,28,32,36,38,42,46,53,58,62,67,71,74,79,85,88,93,98,100,104,108,112,118,122,125,130,133,137,144,151,156,160,165,169,173,178,182,186,190,194,200,209,215,217,224]
texts=[
'앞서 우리는 지수함수를 아주 작은 변화의 반복으로 이해할 수 있다는 사실을 살펴봤습니다.',
'그리고 허수 아이를 곱하면, 복소평면에서 숫자의 방향이 90도 회전한다는 것도 알게 되었습니다.',
'그렇다면 이 두 성질을 하나로 결합하면 어떻게 될까요?',
'먼저 자연상수 이를 밑으로 하는 지수함수의 극한식을 다시 살펴보겠습니다.',
'이의 엑스제곱은, 1 더하기 엑스 나누기 엔을 엔 번 곱하고, 엔을 무한히 크게 만든 결과입니다.',
'여기서 엑스 대신 아이 세타를 넣어보겠습니다.',
'그러면 1 더하기 아이 세타 나누기 엔을 엔 번 곱하는 식이 됩니다.',
'이 식이 실제로 어떤 계산을 의미하는지 살펴보겠습니다.',
'먼저 복소평면 위의 숫자 1에서 출발합니다.',
'여기에 아주 작은 허수 성분을 더한 수를 곱해 보겠습니다.',
'실수 성분은 1이고, 허수 성분은 세타 나누기 엔인 복소수입니다.',
'이 수를 곱하면 원래 숫자에, 현재 숫자를 90도 회전시키고 크기를 세타 나누기 엔만큼 줄인 변화가 더해집니다.',
'따라서 처음에는 오른쪽을 가리키던 벡터가 조금 위쪽으로 기울어집니다.',
'이번에는 방금 얻은 새로운 복소수에 같은 수를 다시 곱해 보겠습니다.',
'그러면 새로운 위치에서도 현재 벡터에 수직인 방향으로 작은 변화가 추가됩니다.',
'이 과정을 반복하면 벡터는 조금씩 방향을 바꾸며 움직이기 시작합니다.',
'그런데 여기서 한 가지 이상한 점이 있습니다.',
'각 단계에서 수직인 성분을 더하면 벡터의 길이도 아주 조금 증가합니다.',
'따라서 반복 횟수가 유한할 때는 정확히 원을 그리지 않고, 바깥쪽으로 조금씩 퍼지는 경로가 만들어집니다.',
'그렇다면 반복 횟수를 늘리면 어떻게 될까요?',
'예를 들어 전체 회전의 기준을 파이로 고정하고, 먼저 이 변화를 네 번 반복해 보겠습니다.',
'벡터는 여러 번 방향을 바꾸지만, 원보다 바깥쪽으로 크게 벗어납니다.',
'이번에는 변화를 열 번으로 나눠보겠습니다.',
'한 번에 더해지는 변화는 작아지고, 경로는 원에 조금 더 가까워집니다.',
'반복 횟수를 백 번, 천 번으로 늘리면 어떻게 될까요?',
'각 단계에서 증가하는 길이는 점점 작아지고, 전체 경로는 원에 가까워집니다.',
'결국 반복 횟수를 무한히 늘리는 극한에서는 길이의 증가가 사라지고, 방향의 변화만 남습니다.',
'이것이 허수를 지수에 넣었을 때 회전이 나타나는 이유입니다.',
'하지만 여기서 한 가지를 더 확인해야 합니다.',
'이 움직임이 단순히 원을 따라가는 것뿐 아니라, 정확히 세타만큼 회전한다는 사실입니다.',
'이를 위해 지수함수의 변화율을 다시 생각해 보겠습니다.',
'이의 엑스제곱을 미분하면 자기 자신이 됩니다.',
'그리고 복소수까지 확장한 지수함수에서, 이의 아이 세타 제곱을 세타에 대해 미분하면 아이가 곱해진 자기 자신이 됩니다.',
'즉, 현재 위치를 나타내는 복소수를 제트라고 하면, 그 순간의 변화율은 아이 곱하기 제트입니다.',
'여기서 아이를 곱한다는 것은 현재 벡터를 90도 회전시킨다는 뜻이었습니다.',
'따라서 현재 위치와 순간적인 이동 방향은 항상 수직입니다.',
'원점에서 바깥쪽으로 멀어지는 방향이 아니라, 원을 따라 움직이는 방향으로 변화하는 것입니다.',
'그리고 이때 이동하는 속력은 원점에서의 거리와 같습니다.',
'처음 위치가 1이므로, 원점에서의 거리는 계속 1로 유지됩니다.',
'따라서 세타가 1만큼 증가하면 원을 따라 이동한 길이도 1이 됩니다.',
'앞서 라디안은 호의 길이를 반지름으로 나눈 값이라고 설명했습니다.',
'반지름이 1인 원에서는 호의 길이가 곧 회전한 각도입니다.',
'따라서 이 움직임은 정확히 세타 라디안만큼 회전하는 운동입니다.',
'그렇다면 원 위에서 세타만큼 회전한 점의 좌표는 무엇이었을까요?',
'앞서 단위원에서 살펴본 것처럼, 가로좌표는 코사인 세타이고 세로좌표는 사인 세타입니다.',
'복소평면에서는 가로좌표가 실수 부분이고, 세로좌표가 허수 부분이므로 이 점은 코사인 세타 더하기 아이 사인 세타로 표현할 수 있습니다.',
'결국 이의 아이 세타 제곱과 코사인 세타 더하기 아이 사인 세타는 정확히 같은 움직임을 나타냅니다.',
'이것이 바로 오일러 공식입니다.',
'지수함수로 표현한 연속적인 변화가 복소평면에서는 회전이 되고, 그 회전의 위치는 삼각함수로 표현되는 것입니다.']
def pronounce(s):
    for a,b in [('90','구십'),('1','일')]:s=s.replace(a,b)
    return s
screen=texts.copy()
for k,s in enumerate(screen):screen[k]=s.replace('허수 아이','허수 i').replace('아이를','i를').replace('엑스','x').replace('세타','θ')
screen[3]=screen[3].replace('자연상수 이를','자연상수 e를')
screen[4]='e의 x제곱은, 1+x/n을 n번 곱하고, n을 무한히 크게 만든 결과입니다.'
screen[5]='여기서 x 대신 iθ를 넣어보겠습니다.'
screen[6]='그러면 1+iθ/n을 n번 곱하는 식이 됩니다.'
screen[10]='실수 성분은 1이고, 허수 성분은 θ/n인 복소수입니다.'
screen[31]='e의 x제곱을 미분하면 자기 자신이 됩니다.'
screen[32]='그리고 복소수까지 확장한 지수함수에서, e의 iθ제곱을 θ에 대해 미분하면 i가 곱해진 자기 자신이 됩니다.'
screen[33]='즉, 현재 위치를 나타내는 복소수를 z라고 하면, 그 순간의 변화율은 i·z입니다.'
screen[45]='복소평면에서는 가로좌표가 실수 부분이고, 세로좌표가 허수 부분이므로 이 점은 cosθ+i sinθ로 표현할 수 있습니다.'
screen[46]='결국 e의 iθ제곱과 cosθ+i sinθ는 정확히 같은 움직임을 나타냅니다.'
lines=[dict(start=a,end=b,text=s,spoken=pronounce(t)) for a,b,s,t in zip([0]+ends[:-1],ends,screen,texts)]
scenes=[('opening',0,15,'4장 끝 화면에서 성장과 허수 회전을 결합한다.'),('complex_limit',15,32,'복소 지수함수의 극한으로 확장한다.'),('start_one',32,42,'z₀=1과 곱셈 인자 1+iθ/n을 준비한다.'),('first_step',42,58,'곱셈을 현재 벡터와 수직 변화량의 덧셈으로 전개한다.'),('repeat_steps',58,71,'새 위치에서도 동일한 수직 변화가 반복된다.'),('finite_growth',71,85,'유한 단계에서는 직각삼각형 빗변의 길이가 증가한다.'),('four_steps',85,98,'θ=π를 고정하고 n=4의 실제 경로를 그린다.'),('refine_steps',98,112,'같은 좌표계에서 n=10,100,1000을 비교한다.'),('limit_circle',112,122,'유한 경로와 구별해 극한에서 단위원을 얻는다.'),('angle_question',122,130,'길이 1과 정확한 회전각 θ는 별도로 확인한다.'),('derivative',130,144,'복소 지수함수의 미분과 연쇄법칙으로 z′=iz를 얻는다.'),('perpendicular',144,160,'현재 위치와 속도 벡터는 수직이다.'),('unit_speed',160,173,'초기값 1에서 반지름과 속력이 1로 유지된다.'),('radians',173,190,'반지름 1과 속력 1로 매개변수 θ가 회전각이 된다.'),('coordinates',190,200,'단위원의 좌표는 (cosθ,sinθ)다.'),('complex_coordinates',200,209,'좌표를 복소수 cosθ+i sinθ로 표현한다.'),('euler_formula',209,217,'동일한 위치를 나타내는 두 표현을 오일러 공식으로 합친다.'),('closing',217,224,'복소 지수·회전·삼각함수의 연결을 한 화면으로 마친다.')]
manifest=[]
for k,(slug,a,b,claim) in enumerate(scenes,1):
    d=R/'scenes'/f'{k:02}_{slug}';d.mkdir(parents=True,exist_ok=True);relevant=[x for x in lines if a<=x['start']<b];shutil.copyfile(T/'scenes/01_example/spec.md',d/'spec.md')
    (d/'spec.md').write_text(f'# {k:02} — {slug}\n\n## 핵심 주장\n{claim}\n\n## 확정 시간\n{a}–{b}초, {b-a}초. 사용자 문장 종료 시각 기준.\n\n## TTS\n'+'\n\n'.join(x['spoken'] for x in relevant)+'\n\n## 화면·전환\n../../storyboard.md의 구간과 ../../visuals.py의 '+slug+' 메서드가 구현 기준이다. 원·수식·좌표 상태를 이어받는다. 시각 요소는 y>−2.7, 자막은 y≈−3.35. 시작은 4장 끝 화면, 마지막은 오일러 공식과 단위원이다. 6장 소스·음원은 아직 없다.\n\n## 정확성\n복소 지수함수는 전 평면에서 수렴하는 멱급수로 확장할 수 있고 그 확장은 극한식과 일치하며 항별 미분을 보존한다. 단순한 실수식의 기호 대입만을 증명으로 삼지 않는다. θ 고정, 실제 점 z_k=(1+iθ/n)^k를 선분으로 연결하고 단위원으로 정규화하지 않는다. n=10의 실제 길이는 약 1.600987이다. 유한 단계의 길이 증가와 각도 부족을 각각 확인한다. z′=iz에서 d|z|²/dθ=2Re(conj(z)iz)=0, z(0)=1, |z′|=|z|=1이다. 반시계 방향과 라디안 정의로 회전각을 확인한다. 삼각함수 좌표는 수학적 논증 후반에 공개하며 내부 애니메이션 좌표 계산을 그 증명으로 사용하지 않는다.\n',encoding='utf-8')
    (d/'script.txt').write_text('\n\n'.join(x['spoken'] for x in relevant)+'\n',encoding='utf-8');(d/'timing.json').write_text(json.dumps(dict(start=a,duration=b-a,lines=relevant),ensure_ascii=False,indent=2),encoding='utf-8')
    (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ChapterScene\nclass Shot{k:02}(ChapterScene):\n    index={k}\n',encoding='utf-8')
    manifest.append(dict(id=f'{k:02}',directory=f'scenes/{k:02}_{slug}',class_name=f'Shot{k:02}',method=slug,start=a,duration_seconds=b-a))
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');(R/'timing.json').write_text(json.dumps(dict(duration=224,source='user sentence end times',lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
for f in ['README.md','master_script.md','scenes.yaml']:
    if not (R/f).exists():shutil.copyfile(T/f,R/f)
(R/'master_script.md').write_text('# 5장 확정 대본 — 224초\n\n'+'\n\n'.join(f"{x['start']:03}–{x['end']:03}초｜{x['text']}" for x in lines)+'\n',encoding='utf-8');shutil.copyfile(R/'master_script.md',R/'narration.md')
(R/'tts_script.txt').write_text('\n\n'.join(x['spoken'] for x in lines)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: euler_identity_ch05\nvideo: {width: 1920, height: 1080, fps: 60}\nscenes:\n'+''.join(f"  - {{id: '{x['id']}', directory: '{x['directory']}', class: {x['class_name']}, duration_seconds: {x['duration_seconds']}}}\n" for x in manifest),encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
(R/'captions.srt').write_text('\n\n'.join(f"{k}\n{stamp(x['start'])} --> {stamp(x['end'])}\n{x['text']}" for k,x in enumerate(lines,1))+'\n',encoding='utf-8')
