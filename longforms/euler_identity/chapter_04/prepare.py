from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent;T=R.parents[1]/'_template'
ends=[5,11,15,18,22,26,29,32,35,38,43,48,53,59,64,69,74,77,82,86,88,91,95,102,105,109,113,118,122,127,132,137,140,146,151,155,158,166,172,176,181,187,194,196,198,202]
texts=[
'앞서 우리는 허수 아이를 곱하면 복소평면에서 90도 회전한다는 사실을 살펴봤습니다.',
'그렇다면 아주 작은 각도만큼의 회전을 연속적으로 만들어내려면 어떻게 해야 할까요?',
'이 질문에 답하기 위해, 먼저 지수의 의미부터 생각해 보겠습니다.',
'2의 3제곱은 2를 세 번 곱한다는 뜻입니다.',
'마찬가지로 2의 4제곱은 2를 네 번 곱한 결과입니다.',
'이처럼 자연수 지수는 같은 수를 반복해서 곱하는 연산으로 이해할 수 있습니다.',
'그런데 지수가 정수가 아니라면 어떨까요?',
'예를 들어 2의 2분의 1제곱은 무엇을 의미할까요?',
'2를 절반만 곱한다는 말로는 설명하기 어렵습니다.',
'대신 우리는 지수의 계산 규칙을 이용할 수 있습니다.',
'2의 2분의 1제곱을 두 번 곱하면, 지수끼리 더해져 2의 1제곱이 됩니다.',
'따라서 2의 2분의 1제곱은 제곱해서 2가 되는 양수, 즉 루트 2입니다.',
'이러한 방식으로 지수를 분수까지 확장하고, 나아가 모든 실수로 확장할 수 있습니다.',
'이제 지수는 단순히 곱셈의 횟수를 나타내는 것이 아니라, 연속적으로 변화하는 값을 표현할 수 있게 됩니다.',
'그렇다면 수많은 지수함수 가운데, 왜 하필 자연상수 이가 특별한 걸까요?',
'2의 엑스제곱, 3의 엑스제곱처럼 밑이 서로 다른 지수함수들을 생각해 보겠습니다.',
'이 함수들은 모두 엑스가 증가할수록 커지지만, 증가하는 속도에는 차이가 있습니다.',
'여기서 함수의 순간적인 변화율을 살펴보겠습니다.',
'일반적인 지수함수는 미분하면 원래 함수에 일정한 상수가 곱해진 형태가 됩니다.',
'그런데 특정한 밑을 선택하면, 그 상수가 정확히 1이 됩니다.',
'바로 자연상수 이입니다.',
'이의 엑스제곱을 미분하면 다시 이의 엑스제곱이 됩니다.',
'이것은 함수의 현재 값과 순간 변화율이 항상 같다는 뜻입니다.',
'예를 들어 현재 값이 1이라면 변화율도 1이고, 값이 2가 되면 변화율도 2가 됩니다.',
'값이 커질수록 그다음 순간의 변화도 함께 커지는 것입니다.',
'이러한 성질은 연속적인 성장을 설명하는 데 매우 유용합니다.',
'하지만 여기서 조금 다른 관점으로 지수함수를 바라보겠습니다.',
'연속적으로 증가하는 값을, 아주 작은 변화의 반복으로 만들어낼 수는 없을까요?',
'예를 들어 처음에 1이라는 값을 가지고 있다고 생각해 보겠습니다.',
'여기에 10퍼센트를 증가시키고, 증가한 값에 다시 10퍼센트를 적용합니다.',
'그러면 처음에는 1이었던 값이 1.1이 되고, 다음에는 1.21이 됩니다.',
'즉, 매번 원래 값이 아니라 바로 이전 단계의 값에 비례해서 증가합니다.',
'이번에는 증가시키는 비율을 더 작게 만들어 보겠습니다.',
'한 번에 10퍼센트씩 증가시키는 대신, 더 작은 비율로 더 자주 증가시키는 것입니다.',
'이러한 과정을 반복 횟수에 맞춰 정리하면, 하나의 극한식으로 표현할 수 있습니다.',
'1 더하기 엑스 나누기 엔을 엔 번 곱하고, 엔을 무한히 크게 만드는 것입니다.',
'이 극한은 이의 엑스제곱과 같습니다.',
'즉, 자연상수 이를 밑으로 하는 지수함수는 아주 작은 비례적 변화를 무한히 잘게 나누어 반복한 결과로도 이해할 수 있습니다.',
'여기서 중요한 것은 매번 같은 양을 더하는 것이 아니라, 현재 값에 비례하는 변화를 적용한다는 사실입니다.',
'그렇다면 이제 앞서 살펴본 허수 아이를 떠올려 보겠습니다.',
'실수에서는 현재 값에 비례하는 변화가 값의 증가나 감소로 나타났습니다.',
'하지만 복소평면에서 현재 값에 아이를 곱하면, 그 값의 방향이 90도 회전합니다.',
'그렇다면 아주 작은 변화의 방향을 아이를 이용해 옆으로 돌린 뒤, 이 과정을 무한히 잘게 나누어 반복한다면 어떻게 될까요?',
'값은 계속 커질까요?',
'아니면 방향만 바뀌며 회전하게 될까요?',
'이제 자연상수 이와 허수 아이가 하나의 식에서 만나게 됩니다.']
def pronounce(s):
    for a,b in [('1.21','일 점 이일'),('1.1','일 점 일'),('90','구십'),('10퍼센트','십 퍼센트'),('1','일'),('2','이'),('3','삼'),('4','사')]:s=s.replace(a,b)
    return s
screens=texts.copy()
for k,s in enumerate(screens):screens[k]=s.replace('허수 아이','허수 i').replace('엑스','x')
screens[7]='예를 들어 2의 1/2제곱은 무엇을 의미할까요?'
screens[10]='2의 1/2제곱을 두 번 곱하면, 지수끼리 더해져 2의 1제곱이 됩니다.'
screens[11]='따라서 2의 1/2제곱은 제곱해서 2가 되는 양수, 즉 √2입니다.'
screens[14]='그렇다면 수많은 지수함수 가운데, 왜 하필 자연상수 e가 특별한 걸까요?'
screens[20]='바로 자연상수 e입니다.'
screens[21]='e의 x제곱을 미분하면 다시 e의 x제곱이 됩니다.'
screens[35]='1+x/n을 n번 곱하고, n을 무한히 크게 만드는 것입니다.'
screens[36]='이 극한은 e의 x제곱과 같습니다.'
screens[37]=screens[37].replace('자연상수 이를','자연상수 e를')
screens[41]=screens[41].replace('아이를','i를')
screens[42]=screens[42].replace('아이를','i를')
screens[45]='이제 자연상수 e와 허수 i가 하나의 식에서 만나게 됩니다.'
lines=[dict(start=a,end=b,text=s,spoken=pronounce(t)) for a,b,s,t in zip([0]+ends[:-1],ends,screens,texts)]
scenes=[('opening',0,15,'3장 끝의 e에서 출발해 회전의 질문을 지수로 연결한다.'),('integer_powers',15,26,'자연수 지수는 반복 곱셈이다.'),('fraction_question',26,38,'분수 지수는 곱셈 횟수보다 지수법칙으로 해석해야 한다.'),('square_root',38,48,'양의 실수에서 2^(1/2)=√2다.'),('real_exponents',48,59,'지수법칙과 연속성을 유지하며 실수 지수로 확장한다.'),('bases',59,74,'같은 축에서 밑 2,e,3의 실제 곡선을 비교한다.'),('derivative',74,88,'밑이 e이면 변화율 계수가 1이다.'),('equal_rate',88,105,'e^x의 값과 순간 변화율은 항상 같다.'),('discrete_question',105,118,'연속 성장을 작은 비례 변화의 반복으로 만드는 질문이다.'),('ten_percent',118,137,'이전 값의 10%씩 증가하면 1→1.1→1.21→1.331이다.'),('refinement',137,146,'고정 구간 x=1에서 n과 비율 1/n을 함께 바꾼다.'),('limit_formula',146,158,'고정 x에 대해 (1+x/n)^n의 극한은 e^x다.'),('convergence',158,166,'같은 시간 구간의 계단형 경로가 e^t에 가까워진다.'),('proportional',166,172,'일정한 양의 덧셈과 현재 값에 비례하는 변화는 다르다.'),('direction',172,187,'현재 값 z에 i를 곱하면 수직 방향 iz를 얻는다.'),('complex_question',187,202,'작은 수직 변화의 유한 단계 예시와 e^(iθ)를 제시한다.')]
manifest=[]
for k,(slug,a,b,claim) in enumerate(scenes,1):
    d=R/'scenes'/f'{k:02}_{slug}';d.mkdir(parents=True,exist_ok=True)
    relevant=[x for x in lines if a<=x['start']<b];shutil.copyfile(T/'scenes/01_example/spec.md',d/'spec.md')
    (d/'spec.md').write_text(f'# {k:02} — {slug}\n\n## 핵심 주장\n{claim}\n\n## 확정 시간\n{a}–{b}초, {b-a}초. 사용자 문장 종료 시각 기준.\n\n## TTS\n'+'\n\n'.join(x['spoken'] for x in relevant)+'\n\n## 화면·전환\n../../storyboard.md와 ../../visuals.py의 '+slug+' 메서드를 기준으로 한다. 기존 수식·그래프·벡터를 이어받는다. 하단 y≤−2.75는 자막 영역이다. 3장 마지막의 e와 희미한 곡선으로 시작하며 마지막은 복소평면과 e^(iθ)로 남긴다. 5장 소스·음원은 아직 없다.\n\n## 정확성\n실수 지수의 밑은 양수, 분수 제곱근은 양의 값이다. 2^(1/2)는 2^0과 2^1 사이에 놓는다. 일반 미분식은 a>0. 접선은 데이터 좌표로 계산한다. 극한에서는 x를 고정하고 1+x/n>0인 충분히 큰 n을 사용한다. 예시의 총 시간은 항상 [0,1]이고 계단의 t_k=k/n, y_k=(1+1/n)^k를 사용한다. 유한 n은 e와 같지 않다. 마지막의 세 단계는 z_new=z+h·iz이며 유한 단계의 길이 증가를 숨기지 않고 원이나 나선을 완성하지 않는다. z′=iz는 아직 설명하지 않는다.\n',encoding='utf-8')
    (d/'script.txt').write_text('\n\n'.join(x['spoken'] for x in relevant)+'\n',encoding='utf-8')
    (d/'timing.json').write_text(json.dumps(dict(start=a,duration=b-a,lines=relevant),ensure_ascii=False,indent=2),encoding='utf-8')
    (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ChapterScene\nclass Shot{k:02}(ChapterScene):\n    index={k}\n',encoding='utf-8')
    manifest.append(dict(id=f'{k:02}',directory=f'scenes/{k:02}_{slug}',class_name=f'Shot{k:02}',method=slug,start=a,duration_seconds=b-a))
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'timing.json').write_text(json.dumps(dict(duration=202,source='user sentence end times',lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
for f in ['README.md','master_script.md','scenes.yaml']:
    if not (R/f).exists():shutil.copyfile(T/f,R/f)
(R/'master_script.md').write_text('# 4장 확정 대본 — 202초\n\n'+'\n\n'.join(f"{x['start']:03}–{x['end']:03}초｜{x['text']}" for x in lines)+'\n',encoding='utf-8');shutil.copyfile(R/'master_script.md',R/'narration.md')
(R/'tts_script.txt').write_text('\n\n'.join(x['spoken'] for x in lines)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: euler_identity_ch04\nvideo: {width: 1920, height: 1080, fps: 30}\nscenes:\n'+''.join(f"  - {{id: '{x['id']}', directory: '{x['directory']}', class: {x['class_name']}, duration_seconds: {x['duration_seconds']}}}\n" for x in manifest),encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
(R/'captions.srt').write_text('\n\n'.join(f"{k}\n{stamp(x['start'])} --> {stamp(x['end'])}\n{x['text']}" for k,x in enumerate(lines,1))+'\n',encoding='utf-8')
