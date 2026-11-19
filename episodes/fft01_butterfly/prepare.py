"""Materialize the supplied 177-second narration; no inferred speech times."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROWS='''3|일반적인 푸리에 변환과 고속 푸리에 변환은 무엇이 다를까요?
7|흥미롭게도 고속 푸리에 변환은 새로운 변환 방식이 아닙니다.
12|동일한 이산 푸리에 변환의 결과를, 훨씬 적은 연산으로 계산하는 알고리즘입니다.
16|먼저 8개의 데이터로 이루어진 신호를 생각해 보겠습니다.
23|이산 푸리에 변환은 이 신호를 서로 다른 주파수의 복소 지수함수와 비교하여, 각 주파수의 성분을 계산합니다.
30|하나의 주파수 성분을 계산하려면 8개의 데이터를 사용해야 하고, 이러한 계산을 8개의 주파수에 대해 수행해야 합니다.
36|따라서 데이터의 개수가 엔 개라면, 직접 계산하는 데 필요한 연산량은 엔 제곱에 비례합니다.
40|그런데 이 계산에는 반복되는 수학적 구조가 숨어 있습니다.
45|푸리에 변환에서 사용하는 복소 지수함수는 복소평면 위에서의 회전으로 해석할 수 있습니다.
49|8개의 회전 인자를 원 위에 배치해 보겠습니다.
55|여기서 짝수 번째 회전 인자만 선택하면, 4개의 회전 인자로 이루어진 더 작은 푸리에 변환의 구조가 나타납니다.
60|또한 반 바퀴만큼 떨어진 두 회전 인자는 크기가 같고 부호만 반대입니다.
64|고속 푸리에 변환은 이러한 주기성과 대칭성을 이용합니다.
69|먼저 8개의 입력 데이터를 인덱스가 짝수인 데이터와 홀수인 데이터로 나눕니다.
76|그러면 하나의 8점 푸리에 변환을 두 개의 4점 푸리에 변환과 결과를 결합하는 연산으로 분해할 수 있습니다.
80|그런데 이 결과를 결합하는 과정에서도 흥미로운 성질이 나타납니다.
86|짝수 번째 데이터의 변환 결과와, 홀수 번째 데이터의 변환 결과에 회전 인자를 곱한 값을 생각해 보겠습니다.
90|두 값을 더하면 하나의 주파수 성분을 얻을 수 있습니다.
95|그리고 동일한 두 값에서 홀수 쪽 값을 빼면, 또 다른 주파수 성분을 얻을 수 있습니다.
106|이것이 가능한 이유는 주파수 인덱스를 엔의 절반만큼 이동했을 때, 짝수 항에 적용되는 회전 인자는 그대로 유지되지만, 홀수 항에 적용되는 회전 인자는 부호가 반대로 바뀌기 때문입니다.
112|결국 서로 다른 두 주파수 성분 사이에 상당 부분 동일한 계산이 포함되어 있었던 것입니다.
117|복소 지수함수의 대칭성 덕분에 앞서 계산한 결과를 그대로 재사용할 수 있습니다.
122|이러한 계산 구조를 그림으로 표현하면 나비의 날개와 비슷한 형태가 나타납니다.
125|그래서 이를 버터플라이 연산이라고 부릅니다.
128|고속 푸리에 변환은 이러한 분해를 한 번만 수행하지 않습니다.
134|8개의 데이터를 4개씩, 다시 2개씩 나누고, 마지막에는 하나의 데이터까지 분해합니다.
139|그리고 버터플라이 연산을 통해 작은 변환의 결과들을 순차적으로 결합합니다.
144|매번 문제의 크기를 절반으로 나누기 때문에 필요한 단계의 수는 로그 엔에 비례합니다.
147|그리고 각 단계의 전체 계산량은 엔에 비례합니다.
151|따라서 전체 계산 복잡도는 엔 로그 엔이 됩니다.
157|따라서 데이터의 개수가 많아질수록 이러한 수학적 구조를 활용하는 것이 더욱 중요해지는 것입니다.
164|결과적으로 고속 푸리에 변환은 기존의 이산 푸리에 변환과 동일한 결과를 얻으면서도 필요한 계산량을 크게 줄일 수 있습니다.
169|여기서 중요한 것은 개별 연산을 더 빠르게 수행하도록 만든 것이 아니라는 점입니다.
177|계산에 숨어 있는 수학적 대칭성을 발견하고, 이미 계산한 결과를 재사용함으로써 필요한 연산 자체를 줄인 것입니다.'''
def display(t):
 for a,b in [('엔의 절반','N/2'),('엔 제곱','N²'),('엔 로그 엔','N log N'),('로그 엔','log N'),('엔 개','N개'),('엔에','N에')]:t=t.replace(a,b)
 return t
scenes=[]
for i,(a,b,t) in enumerate([(0,12,'같은 변환, 다른 계산 구조'),(12,36,'직접 계산은 왜 N²일까?'),(36,64,'회전 인자의 주기성과 대칭성'),(64,80,'짝수·홀수 인덱스로 분할'),(80,117,'같은 중간값으로 두 출력'),(117,125,'버터플라이 연산'),(125,139,'작게 나누고 단계별로 결합'),(139,157,'계산 구조에서 N log N으로'),(157,177,'대칭성으로 줄이는 계산')],1):scenes.append(dict(id=f'{i:02}',start=a,end=b,title=t,**{'class':f'Shot{i:02}'}))
sentences=[];spoken=[];start=0
for row in ROWS.splitlines():
 end,t=row.split('|',1);end=int(end);sentences.append(dict(start=start,end=end,text=display(t)));spoken.append((start,t));start=end
data=dict(title='고속 푸리에 변환은 무엇이 다를까? — 버터플라이 연산',duration=177,sentences=sentences,scenes=scenes)
(HERE/'timing.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'tts_script.txt').write_text('\n\n'.join('\n'.join(t for a,t in spoken if s['start']<=a<s['end']) for s in scenes)+'\n',encoding='utf-8')
(HERE/'narration.md').write_text('# '+data['title']+'\n\n확정 대본 · 사용자 문장 종료 시각 · 177초\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초  {s['text']}" for s in sentences)+'\n',encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
(HERE/'captions.srt').write_text('\n\n'.join(f"{i}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{s['text']}" for i,s in enumerate(sentences,1))+'\n',encoding='utf-8')
build=(HERE.parent/'deteff01_gaussian_elimination/build.py').read_text(encoding='utf-8').replace('deteff01','fft01')
build=build.replace("('scene.py', 'timing.json', 'build.py')", "('scene.py', 'model.py', 'timing.json', 'build.py')")
build=build.replace("'episodes/detperm01_permutation_sign/scene.py',", "'episodes/detperm01_permutation_sign/scene.py', 'episodes/detperm01_permutation_sign/timing.json', 'longforms/qcs01_speed/script.json',")
(HERE/'build.py').write_text(build,encoding='utf-8')
(HERE/'brief.md').write_text('''# 제작 기준

177초 · 9:16 · 1080×1920 · 30fps. 확정 대본과 문장 종료 시각을 유지한다. TTS 음원 미제공으로 무음. 실제 기호 자막과 발음 원고를 분리한다.

DFT는 X[k]=sum x[n] exp(−2πikn/N), 정규화하지 않은 순방향이다. FFT는 동일한 DFT를 계산하는 알고리즘. 이번 예시는 N=8, 일반화는 N=2^m인 radix-2 DIT Cooley–Tukey 범위다. 수학적으로 같은 결과이며 부동소수점 연산 순서에 따른 미세 오차는 허용한다.

입력은 cos(2πn/8)+0.5cos(6πn/8). 처음 샘플, 분할, 수치 예시, 마지막 스펙트럼은 같은 값에서 계산한다. 스펙트럼은 비정규화 |X[k]|이고 출력 bin 0~7은 양·음 주파수를 포함한 인덱스다. k=1에서 E1=3, W8 O1=1, X1=4, X5=2이다.

W_N=exp(−2πi/N)이므로 시계방향. W8^(2k)=W4^k, W8^(k+4)=−W8^k. 주파수 k→k+N/2에서 W_N^((k+N/2)n)=W_N^(kn)(−1)^n. 입력 인덱스가 짝수면 유지, 홀수면 반전. E/O는 N/2점 DFT이며 k는 0≤k<N/2. t=W_N^k O_k를 한 번 계산해 E+t와 E−t에서 공유한다.

8점 FFT 그래프 입력은 0,4,2,6,1,5,3,7 순서. 단계별 간격은 1,2,4이고 각 단계 4개 버터플라이가 실제 모델과 일치한다. 연결선은 의존 관계이며 선 개수 자체가 연산 횟수가 아니다. 전체 그래프에서는 회전 인자·+/−를 생략함을 표시한다.

직접 계산 8×8=64는 곱 항의 수이며 전체 연산 수나 최적화 후 곱셈 수가 아니다. 3단계×4버터플라이=12개는 64와 동일 단위가 아니다. 각 버터플라이는 일반적으로 복소 곱 1회와 덧셈/뺄셈 2회, 특수 인자는 단순화 가능. N²와 Nlog₂N 그래프는 증가율 척도이며 실측 시간 아님.
''',encoding='utf-8')
(HERE/'spec.md').write_text('# 장면 설계\n\n파랑 짝수 입력/E, 노랑 홀수 입력/O, 보라 회전 인자, 초록 출력. 입력은 0부터 인덱싱한다. 상단 현재 주장, 중앙 도형과 식, 하단 독립 발화 자막.\n\n'+'\n'.join(f"- {s['start']}–{s['end']}초: {s['title']} ({s['class']})" for s in scenes)+'\n\n대표 검수: Shot03 시계방향·네 점 대응, Shot05 주파수 이동·중간값 공유, Shot06 버터플라이, Shot07 입력 순서와 세 단계. 마지막 출력은 실제 직접 DFT 및 FFT 수치 검산과 연결한다.\n',encoding='utf-8')
