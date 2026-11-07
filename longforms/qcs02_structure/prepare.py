"""Approved narration and supplied sentence ends; no inferred speech timing."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
LINES='''앞서 우리는 양자컴퓨터가 중첩과 간섭을 이용해, 정답을 찾는 데 필요한 조회 횟수를 줄일 수 있다는 사실을 살펴봤습니다.
7
그렇다면 양자컴퓨터는 모든 문제에서 기존 컴퓨터보다 빠를 수 있을까요?
12
대표적인 그로버 알고리즘을 다시 생각해 보겠습니다.
15
정렬되지 않은 N개의 항목에서 정답 하나를 찾을 때, 일반적인 컴퓨터는 최악의 경우 N개에 비례하는 횟수만큼 확인해야 합니다.
22
하지만 그로버 알고리즘은 약 루트 N에 비례하는 조회만으로 정답을 찾아낼 수 있습니다.
28
그렇다면 이보다 더 빠른 양자 알고리즘을 만들 수도 있을까요?
32
흥미롭게도, 정답 여부만 확인할 수 있는 일반적인 검색 문제에서는 그로버 알고리즘보다 근본적으로 더 적은 조회 횟수로 해결할 수 없다는 사실이 증명되어 있습니다.
41
즉, 중첩과 간섭을 사용하더라도 이러한 검색에서는 제곱근 수준의 가속이 한계인 것입니다.
47
그런데 모든 양자 알고리즘이 이 정도의 속도 향상에 머무르는 것은 아닙니다.
52
대표적인 예가 쇼어 알고리즘입니다.
55
쇼어 알고리즘은 큰 정수를 소인수분해하는 문제를 해결하기 위해 고안되었습니다.
60
약수를 하나씩 확인하는 대신, 정수의 거듭제곱을 특정 숫자로 나눈 나머지가 반복되는 규칙을 이용합니다.
66
예를 들어 15를 소인수분해한다고 생각해 보겠습니다.
69
2의 거듭제곱을 15로 나눈 나머지는 1, 2, 4, 8, 그리고 다시 1, 2, 4, 8로 반복됩니다.
76
즉, 주기는 4입니다.
78
그런데 주기가 4라는 것은 2의 4제곱에서 1을 뺀 값이 15로 나누어떨어진다는 뜻입니다.
84
여기서 2의 4제곱 빼기 1은, 2의 제곱 빼기 1과 2의 제곱 더하기 1의 곱으로 나눌 수 있습니다.
90
각각 계산하면 3과 5가 됩니다.
93
바로 15의 두 소인수입니다.
95
이처럼 특정한 조건에서 주기를 알면, 원래 정수의 약수를 찾을 수 있습니다.
99
쇼어 알고리즘은 소인수분해 문제를 이러한 주기를 찾는 문제로 바꿉니다.
104
그리고 양자 푸리에 변환을 이용해, 주기에 관한 정보가 측정 결과에 나타나도록 만듭니다.
109
반복되는 파동에서 특정 주파수를 찾아내는 것과 비슷한 원리입니다.
113
이렇게 얻은 측정 결과를 고전적인 계산으로 처리하면, 원래 수열의 주기를 복원할 수 있습니다.
119
이 과정은 알려진 고전적인 소인수분해 알고리즘보다 훨씬 효율적으로 수행될 수 있습니다.
124
두 알고리즘 모두 양자 중첩과 간섭을 이용하지만, 속도 향상의 정도는 크게 다릅니다.
130
그로버 알고리즘은 특별한 구조가 없는 검색에서도 제곱근 수준의 가속을 얻을 수 있습니다.
135
반면 쇼어 알고리즘은 문제에 존재하는 주기적인 구조를 활용해 훨씬 큰 속도 향상을 얻습니다.
142
즉, 양자컴퓨터의 속도는 단순히 얼마나 많은 상태를 중첩할 수 있는지만으로 결정되지 않습니다.
149
문제에 어떤 수학적 구조가 존재하고, 그 구조를 얼마나 효율적으로 이용할 수 있는지도 중요합니다.
154
그렇다면 특별한 구조가 없는 무작위 입력에서도, 양자컴퓨터가 지수적으로 빠른 계산을 수행할 수 있을까요?
161'''.splitlines()
BOUNDS=[0,7,12,28,47,60,66,76,78,84,90,99,104,106,113,119,124,130,142,154,161]
TITLES=['간섭으로 조회 횟수를 줄인다','모든 문제에서 더 빠를까?','그로버의 검색','그로버보다 더 빠를 수 있을까?','다른 문제, 쇼어 알고리즘','인수분해를 주기 찾기로','나머지가 만드는 반복 수열','최소 양의 주기 r = 4','주기가 알려주는 나눗셈 관계','제곱의 차로 분해하기','주기에서 인수 3과 5로','찾아야 하는 것은 주기','함수의 반복에서 입력 진폭으로','QFT가 주기 정보를 드러낸다','측정값에서 주기를 복원한다','양자 계산과 고전 후처리','같은 양자 원리, 다른 가속','활용하는 문제 구조의 차이','속도를 결정하는 문제의 구조','무작위 입력에서도 빠를까?']
DETAILS=[
'사용자가 명시한 도입 복습 문장은 그대로 유지한다. 1편의 동일한 네 진폭을 재사용하여 초기→오라클→확산의 정규화된 상태를 시연한다. O(N)→O(√N) 조회 규모로 연결한다.',
'주기·그래프·무작위 점의 서로 다른 모양에서 도입 질문을 제시한다. 모든 문제에 대한 보편적 가속을 주장하지 않는다.',
'12–15초 그로버 이름, 15–22초 고전 검색의 순차 조회, 22–28초 실제 N=64 그로버 분포. 정답 판별 오라클과 확산을 함께 표시한다.',
'28–32초 더 빠른 알고리즘이라는 질문, 32–41초 Ω(√N) 질의 하한, 41–47초 제곱근 가속 한계. 블랙박스 비구조적 검색·정답 1개·고정 성공률 모델에 한정한다.',
'47–52초 다른 문제로 전환, 52–55초 쇼어, 55–60초 소인수분해. 숫자 크기는 난도의 상징이며 실행시간 데이터가 아니다.',
'시행 나눗셈은 단순한 고전 방법의 예로만 표시한다. f(x)=2ˣ mod 15에서 반복되는 나머지를 찾는 방향으로 변환한다.',
'66–69초 예제 정수 15. 69–76초 실제 modular_sequence로 생성한 1,2,4,8,1,2,4,8. 함수 자체를 매끄러운 정현파로 표시하지 않는다.',
'동일한 앞·뒤 네 항을 묶고 f(x+4)=f(x), r=4를 표시한다. 최소 양의 주기는 실제 계산으로 검증한다.',
'2⁴ mod 15=1 → 2⁴−1=15. 이 예제의 정확한 등식과 일반적인 배수 관계를 구별한다.',
'2⁴−1=(2²)²−1²=(2²−1)(2²+1). 올바른 용어인 제곱의 차를 사용한다. 두 인자를 다른 색으로 나눈다.',
'90–93초 3과 5, 93–95초 15=3×5, 95–99초 조건과 gcd. 일반적으로 gcd(a,M)=1, 짝수 최소 주기, a^(r/2)≢−1(mod M)와 비자명 gcd를 확인한다.',
'15=?×?에서 f(x)=2ˣ mod15, r=?로 환원한다. 앞 장면에서 얻은 답이 입력으로 주어진 것처럼 표현하지 않는다.',
'104–106초는 104–109초 문장 내부의 화면 변화다. f(x)=1에 대응하는 입력 위치 0,4를 선택하는 조건부 입력 레지스터 예를 보여준다. 함수 출력값 자체를 진폭으로 사용하지 않는다.',
'8차원 단순 예시 (|0⟩+|4⟩)/√2에 실제 QFT 행렬을 적용한다. 출력 진폭은 짝수 0,2,4,6에서 0.5, 각 확률은 25%. 실제 쇼어의 더 큰 레지스터를 대신하는 개념도임을 표시한다.',
'측정값 k=2를 얻는 성공 사례, 2/8=1/4 → 후보 r=4 → 2⁴ mod15=1 검증. 0이나 4에서는 같은 방법으로 즉시 주기를 알 수 없으며 일반적으로 연분수·검증·반복이 필요하다.',
'정수→주기 찾기→QFT·측정→고전 후처리→인수. 양자 구간은 보라, 고전 계산은 파랑. 입력 비트 수에 대한 다항시간과 실제 장치 실행시간을 구별한다.',
'검색과 인수분해는 서로 다른 문제임을 표시한다. 중첩·간섭이라는 공통 원리와 다른 구조 활용을 비교한다.',
'130–135초 Grover의 비구조적 검색 Θ(√N) 질의, 135–142초 Shor의 주기 구조. N개의 검색 후보와 정수 M의 입력 비트 수를 동일한 성능축으로 비교하지 않는다. 고전 인수분해의 난도가 증명되었다고 주장하지 않는다.',
'142–149초 중첩의 개수만으로 충분하지 않음, 149–154초 문제의 수학적 구조와 효율적 활용이라는 결론. 새로운 연구 결과나 지수 가속을 단정하지 않는다.',
'154–161초 제공된 마지막 물리학적 질문을 유지한다. 시드가 고정된 무작위 비트 격자를 배경에 둔다. 다음 편 제목·예고·엔드카드는 추가하지 않는다. standalone/join 모두 본문과 자막 전체를 보존한다.']

sentences=[];start=0
for i in range(0,len(LINES),2):
    end=int(LINES[i+1]);sentences.append({'start':start,'end':end,'text':LINES[i]});start=end
scenes=[{'id':f'{i+1:02}','class':f'Shot{i+1:02}','start':a,'end':b,'title':TITLES[i]} for i,(a,b) in enumerate(zip(BOUNDS,BOUNDS[1:]))]
data={'title':'양자컴퓨터도 빠르지 못한 문제가 있다','revision':'v1_161s','duration':161,'timing_source':'사용자 제공 확정 대본 및 문장 종료 시각','sentences':sentences,'scenes':scenes}
for name,obj in [('script.json',data),('timing.json',{'fps':60,**data})]:
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def wrap(s,n=32):
    out=[];line=''
    for w in s.split():
        if line and len(line)+len(w)+1>n:out.append(line);line=w
        else:line=(line+' '+w).strip()
    return '\n'.join(out+[line])
(HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
script='# 양자컴퓨터도 빠르지 못한 문제가 있다\n\n사용자 확정 대본 · 161초\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n'
for name in ['master_script.md','narration.md']:(HERE/name).write_text(script,encoding='utf-8')
tts=[]
for sentence in sentences:
    s=sentence['text']
    for a,b in [('1,000','천'),('100만','백만'),('N개','엔 개'),('루트 N','루트 엔'),('15','십오'),('2의','이의'),('4제곱','사 제곱'),('제곱 빼기 1','제곱 빼기 일'),('제곱 더하기 1','제곱 더하기 일'),('3과 5','삼과 오'),('1, 2, 4, 8','일, 이, 사, 팔'),('주기는 4','주기는 사'),('주기가 4','주기가 사'),('1을','일을')]:s=s.replace(a,b)
    tts.append(s)
(HERE/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
for i,scene in enumerate(scenes):
    f=HERE/'scenes'/scene['id'];f.mkdir(parents=True,exist_ok=True)
    (f/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom longforms.qcs02_structure.direction import EpisodeTwoScene\n\nclass '+scene['class']+'(EpisodeTwoScene):\n    shot='+str(i)+'\n',encoding='utf-8')
    text='\n\n'.join(s['text'] for s in sentences if s['end']>scene['start'] and s['start']<scene['end'])
    (f/'script.txt').write_text(text+'\n',encoding='utf-8')
    (f/'spec.md').write_text(f"# {scene['id']} · {scene['title']}\n\n## 목적과 주장\n\n{TITLES[i]}를 도형과 수식으로 설명한다.\n\n## 확정 대본·길이\n\n{scene['start']}–{scene['end']}초, {(scene['end']-scene['start'])*60}프레임. 문장 경계와 겹치는 원문은 아래와 같으며 실제 자막 시각은 timing.json을 따른다.\n\n{text}\n\n## 화면·연산·정확성\n\n{DETAILS[i]}\n\n## 연결\n\n앞 장면: {TITLES[i-1] if i else '사용자가 제공한 1편 도입 연결'}. 다음: {TITLES[i+1] if i<19 else '물리학적 질문으로 종료'}. direction.py의 s{i+1:02}가 독립 렌더 진입점이다. 하단에는 내레이션 자막을 유지한다.\n",encoding='utf-8')
manifest=[{**s,'directory':'scenes/'+s['id'],'duration_seconds':s['end']-s['start']} for s in scenes]
(HERE/'scenes.yaml').write_text(json.dumps({'id':'qcs02','title':data['title'],'video':{'longform':[1920,1080],'shorts':[1080,1920],'fps':60,'duration_seconds':161},'scenes':manifest},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert len(sentences)==31 and sentences[-1]['end']==161 and len(scenes)==20
