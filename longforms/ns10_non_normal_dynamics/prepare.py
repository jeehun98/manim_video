"""Act 10: non-normal transient growth."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
SOURCES='- Trefethen et al. (1993), Hydrodynamic Stability Without Eigenvalues: https://people.maths.ox.ac.uk/trefethen/ttrd.pdf\n- Bondanelli and Ostojic (2020), Coding with transient trajectories in recurrent neural networks: https://pmc.ncbi.nlm.nih.gov/articles/PMC7043794/\n- Kerg et al. (2019), Non-normal Recurrent Neural Network: https://arxiv.org/abs/1905.12080\n'
DATA=[('meaning', '안정적이라는 것은 무엇을 의미할까?', 31, '앞에서는 신경망과 유체에서 변화가 증폭되는 경로와 이를 제어하는 메커니즘을 살펴봤습니다.\n그렇다면 안정적인 시스템에서는 작은 변화가 항상 줄어들까요?\n하나의 시스템에 작은 변화를 주고, 시간이 흐르는 모습을 살펴보겠습니다.\n처음에는 작았던 변화가 조금씩 감소하고, 결국 영에 가까워집니다.\n우리는 보통 이런 움직임을 안정적이라고 생각합니다.\n하지만 변화가 결국 사라진다는 사실과, 그 과정에서 한 번도 커지지 않는다는 사실은 같을까요?', '원점으로 단조 감소하는 벡터 → 장기 감소와 매 순간 감소 구별', 'A=[[-1,10],[0,-1]], 고정 2D 연속시간 선형 시스템. P(t)=exp(-t)[[1,10t],[0,1]], x0=(0,1)→x(t)=exp(-t)(10t,1). 모든 고유값 -1이며 결함 행렬로 독립 고유벡터 둘이 없으므로 두 고유벡터의 분해 그림을 그리지 않는다. Euclidean norm amplitude를 표시하며 에너지 배율은 그 제곱. 유한시간 특이점이나 실제 NS 해/신경망 측정으로 주장하지 않는다.\n-I의 단조 수축과 A의 점근감쇠를 구별.'), ('eigenvalues', '고유값은 모두 안정적인데', 34, '이제 시간이 흐르면서 상태가 변하는 간단한 시스템을 만들어 보겠습니다.\n현재 상태에 행렬을 곱해 변화하는 방향을 결정합니다.\n이 행렬의 고유값은 모두 마이너스 일입니다.\n연속시간 시스템에서는 고유값의 실수부가 모두 음수이면, 작은 변화가 충분히 시간이 지난 뒤 영으로 수렴합니다.\n따라서 이 시스템은 장기적으로 안정적입니다.\n그런데 실제로 한 점에서 출발해 경로를 따라가 보면, 예상과 다른 움직임이 나타납니다.', '고정 A 카드 → 음수 고유값 중복점 → 초기상태', 'A=[[-1,10],[0,-1]], 고정 2D 연속시간 선형 시스템. P(t)=exp(-t)[[1,10t],[0,1]], x0=(0,1)→x(t)=exp(-t)(10t,1). 모든 고유값 -1이며 결함 행렬로 독립 고유벡터 둘이 없으므로 두 고유벡터의 분해 그림을 그리지 않는다. Euclidean norm amplitude를 표시하며 에너지 배율은 그 제곱. 유한시간 특이점이나 실제 NS 해/신경망 측정으로 주장하지 않는다.\n고정 유한차원 선형 연속시간에서만 Reλ<0이면 모든 상태가 점근감쇠. 일반 비선형/시간변화 시스템이나 이산 시스템의 조건 아님.'), ('trajectory', '벡터가 원점에서 멀어졌다가 돌아온다', 38, '처음 상태를 영, 일로 놓겠습니다.\n시간이 흐르면 두 번째 성분은 점점 줄어듭니다.\n그런데 첫 번째 성분에는 두 번째 성분으로부터 전달되는 효과가 있습니다.\n그 영향으로 첫 번째 성분이 처음에는 빠르게 커질 수 있습니다.\n그래서 전체 상태 벡터는 원점에서 멀어졌다가, 충분한 시간이 지난 뒤 다시 원점으로 돌아옵니다.\n모든 고유값이 음수인데도, 상태의 크기가 일시적으로 증폭된 것입니다.', '정확한 해 궤적과 x1/x2/norm 수치 → 증가 후 감소', 'A=[[-1,10],[0,-1]], 고정 2D 연속시간 선형 시스템. P(t)=exp(-t)[[1,10t],[0,1]], x0=(0,1)→x(t)=exp(-t)(10t,1). 모든 고유값 -1이며 결함 행렬로 독립 고유벡터 둘이 없으므로 두 고유벡터의 분해 그림을 그리지 않는다. Euclidean norm amplitude를 표시하며 에너지 배율은 그 제곱. 유한시간 특이점이나 실제 NS 해/신경망 측정으로 주장하지 않는다.\nt=1: x1=10/e≈3.67879, x2=1/e≈.367879, norm≈3.69714. 특정 초기상태 증폭이며 최대특잇값과 별개.'), ('coupling', '고유값만으로 놓친 것은 무엇일까?', 32, '왜 이런 일이 가능했을까요?\n앞에서는 고유값이 모두 음수라는 사실만 확인했습니다.\n하지만 고유값은 시스템의 장기적인 거동을 설명할 뿐, 모든 초기 상태의 크기가 매 순간 감소하는지까지 알려주지는 않습니다.\n이 행렬에서는 두 번째 성분의 변화가 첫 번째 성분으로 전달됩니다.\n그 과정에서 변화의 방향이 계속 달라지고, 일시적인 증폭이 나타납니다.\n이처럼 고유값만으로는 중간의 증폭을 충분히 설명할 수 없는 행렬 구조를 이해하려면, 비정규성이라는 개념이 필요합니다.', 'coupling10 켜기/끄기 · 같은 감쇠율 · 성분 전달', 'A=[[-1,10],[0,-1]], 고정 2D 연속시간 선형 시스템. P(t)=exp(-t)[[1,10t],[0,1]], x0=(0,1)→x(t)=exp(-t)(10t,1). 모든 고유값 -1이며 결함 행렬로 독립 고유벡터 둘이 없으므로 두 고유벡터의 분해 그림을 그리지 않는다. Euclidean norm amplitude를 표시하며 에너지 배율은 그 제곱. 유한시간 특이점이나 실제 NS 해/신경망 측정으로 주장하지 않는다.\n같은 대각−1, coupling0/10을 비교. coupling이 norm증가 보장 조건 전체를 뜻하는 것은 아님.'), ('normality', '비정규 행렬은 무엇이 다른가?', 36, '행렬이 비정규적이라는 것은 정확히 무슨 뜻일까요?\n정규 행렬에서는 행렬과 그 전치행렬이 곱해지는 순서를 바꾸더라도 결과가 같습니다.\n하지만 비정규 행렬에서는 일반적으로 그렇지 않습니다.\n이 차이는 단순히 행렬의 모양에 관한 문제가 아닙니다.\n정규 행렬에서는 복소수까지 허용하면, 서로 직교하는 고유벡터를 기준으로 각 방향의 변화를 분리할 수 있습니다.\n반면 비정규 행렬에서는 서로 다른 방향의 변화가 얽히면서, 고유값만으로 예상하기 어려운 일시적 증폭이 나타날 수 있습니다.\n앞에서 본 행렬은 바로 이런 비정규 행렬입니다.', '정규와 비정규 비교 → 전치 곱 순서 → 모든 비정규가 증폭하지 않음', 'A=[[-1,10],[0,-1]], 고정 2D 연속시간 선형 시스템. P(t)=exp(-t)[[1,10t],[0,1]], x0=(0,1)→x(t)=exp(-t)(10t,1). 모든 고유값 -1이며 결함 행렬로 독립 고유벡터 둘이 없으므로 두 고유벡터의 분해 그림을 그리지 않는다. Euclidean norm amplitude를 표시하며 에너지 배율은 그 제곱. 유한시간 특이점이나 실제 NS 해/신경망 측정으로 주장하지 않는다.\n실수 행렬 normal AᵀA=AAᵀ. 일반적인 고유벡터 정규 대각화는 복소수까지 허용한 unitary basis. 비정규는 일시적 증폭의 필요 구조이나 충분조건 아님. 비정규 B=[[-1,.1],[0,-1]]은 Euclidean norm 단조수축.'), ('singular', '순간적인 증폭과 장기적인 안정성을 따로 측정하다', 40, '그렇다면 이런 시스템의 증폭은 어떻게 측정할 수 있을까요?\n고유값은 충분히 긴 시간이 지난 뒤 시스템이 어떻게 움직이는지 판단하는 데 중요합니다.\n하지만 지금부터 일정 시간이 지난 뒤, 어떤 입력 방향이 가장 크게 증폭되는지 알고 싶다면 다른 양을 살펴봐야 합니다.\n현재 상태를 미래의 상태로 바꾸는 행렬을 생각해 보겠습니다.\n이를 시간 발전 연산자라고 합니다.\n그리고 이 행렬의 가장 큰 특잇값은 해당 시간 동안 가능한 최대 증폭 비율을 나타냅니다.\n즉 장기적인 안정성과 유한한 시간 동안의 최대 증폭은 서로 다른 방식으로 살펴봐야 하는 것입니다.', '단위원 → 정확한 P(t) 타원 → SVD 최대로 늘어난 방향', 'A=[[-1,10],[0,-1]], 고정 2D 연속시간 선형 시스템. P(t)=exp(-t)[[1,10t],[0,1]], x0=(0,1)→x(t)=exp(-t)(10t,1). 모든 고유값 -1이며 결함 행렬로 독립 고유벡터 둘이 없으므로 두 고유벡터의 분해 그림을 그리지 않는다. Euclidean norm amplitude를 표시하며 에너지 배율은 그 제곱. 유한시간 특이점이나 실제 NS 해/신경망 측정으로 주장하지 않는다.\n단위원 변환은 정확한 선형 P(t); ellipse rotated. G(t)=sigma_max P(t). t1에서 G≈3.72, 선택된 x0 norm≈3.70. sup G는 t=sqrt(1−4/100)≈.979796에서 달성. 임의시점 최대 방향과 특정 초기 상태 구별.'), ('liftup', '유체역학에서도 이런 증폭이 일어난다', 40, '이제 다시 유체역학으로 돌아가 보겠습니다.\n일부 유체의 기본 흐름은 작은 교란에 대해 장기적으로 안정적일 수 있습니다.\n그런데 그 흐름에 특정한 방향의 작은 교란을 가하면, 교란의 에너지가 한동안 크게 증가할 수 있습니다.\n대표적인 예가 전단 흐름에서 나타나는 리프트업 메커니즘입니다.\n서로 다른 속도로 흐르는 유체 층 사이에서, 작은 횡방향 움직임이 기존의 속도 차이를 재배치합니다.\n이 과정에서 흐름 방향의 속도 교란이 크게 성장할 수 있습니다.\n교란의 각 고유모드는 결국 감소하더라도, 그 조합은 한동안 증폭될 수 있는 것입니다.', '속도 다른 층 → 작은 위아래 교란 → 빠름/느림 줄무늬', 'A=[[-1,10],[0,-1]], 고정 2D 연속시간 선형 시스템. P(t)=exp(-t)[[1,10t],[0,1]], x0=(0,1)→x(t)=exp(-t)(10t,1). 모든 고유값 -1이며 결함 행렬로 독립 고유벡터 둘이 없으므로 두 고유벡터의 분해 그림을 그리지 않는다. Euclidean norm amplitude를 표시하며 에너지 배율은 그 제곱. 유한시간 특이점이나 실제 NS 해/신경망 측정으로 주장하지 않는다.\nU(y)=Sy 전단의 streamwise constant 교란에서 lift-up결합 u_dot≈−Sv+νΔu. cross-stream rolls가 느린 유체를 위로/빠른유체를 아래로 옮겨 저속/고속 streak 생성. 실제 안정성은 기본흐름·경계·Re·선형화조건에 의존. 그림은 재배치 개념도, 실제 NS 계산이나 특이점연구의 설명 아님.'), ('rnn', '신경망에서도 같은 수학적 구조가 나타난다', 36, '그런데 이 구조는 신경망에서도 나타납니다.\n이번에는 입력을 한 번 통과시키는 신경망이 아니라, 내부 상태를 반복해서 갱신하는 순환 신경망을 생각해 보겠습니다.\n순환 신경망에서는 현재 상태가 다음 순간의 상태를 결정합니다.\n이 반복적인 변화를 어떤 기준 상태 주변에서 선형화하면, 행렬이 현재 상태의 작은 변화에 작용하는 형태로 나타납니다.\n이 행렬이 비정규적이라면, 장기적으로 안정적인 상태에서도 특정 입력 방향의 변화가 일시적으로 증폭될 수 있습니다.\n즉 유체의 전단 흐름과 순환 신경망은 서로 다른 시스템이지만, 비정규 동역학에 의한 일시적인 증폭이라는 수학적 구조를 공유합니다.', '유체 교란과 연속시간 RNN → 같은 선형 형식', 'A=[[-1,10],[0,-1]], 고정 2D 연속시간 선형 시스템. P(t)=exp(-t)[[1,10t],[0,1]], x0=(0,1)→x(t)=exp(-t)(10t,1). 모든 고유값 -1이며 결함 행렬로 독립 고유벡터 둘이 없으므로 두 고유벡터의 분해 그림을 그리지 않는다. Euclidean norm amplitude를 표시하며 에너지 배율은 그 제곱. 유한시간 특이점이나 실제 NS 해/신경망 측정으로 주장하지 않는다.\ncontinuous-time rate RNN의 기준고정점 주변 δh_dot=Aδh 모형. 입력이 끝난 뒤 고정 연산자 선형화. 일반 discrete RNN은 δh(k+1)=Mδh(k), 고정M 장기 안정조건ρ(M)<1. 실제 모델 전부나 모든 비정규가 증폭 보장 아님.'), ('information', '커지는 변화가 항상 나쁜 것은 아니다', 36, '그런데 여기서 흥미로운 질문이 하나 더 생깁니다.\n일시적인 증폭은 반드시 불안정한 현상일까요?\n유체에서는 작은 교란이 크게 증폭되면 다른 비선형적인 변화로 이어질 가능성이 있습니다.\n하지만 신경망에서는 특정 입력에 대한 일시적인 증폭을 유용하게 활용할 수도 있습니다.\n예를 들어 어떤 입력이 들어왔을 때 내부 상태가 잠시 크게 반응한 뒤 다시 원래 상태로 돌아오도록 설계할 수 있습니다.\n이렇게 하면 입력의 흔적을 일시적인 상태 변화로 표현하는 것이 가능합니다.\n즉 증폭은 그 자체로 좋거나 나쁜 것이 아니라, 시스템에서 어떤 역할을 하도록 구성되었는지가 중요합니다.', '두 초기 입력의 다른 궤적 → 입력 흔적의 일시적 표현', 'A=[[-1,10],[0,-1]], 고정 2D 연속시간 선형 시스템. P(t)=exp(-t)[[1,10t],[0,1]], x0=(0,1)→x(t)=exp(-t)(10t,1). 모든 고유값 -1이며 결함 행렬로 독립 고유벡터 둘이 없으므로 두 고유벡터의 분해 그림을 그리지 않는다. Euclidean norm amplitude를 표시하며 에너지 배율은 그 제곱. 유한시간 특이점이나 실제 NS 해/신경망 측정으로 주장하지 않는다.\n같은 A, 초기 입력 e1/e2의 궤적을 비교. e1은 단조감쇠, e2는 transient. finite-time norm readout로 방향을 구별하는 설명용 모형, 훈련된 실제 RNN 또는 긴시간 기억 보장 아님.'), ('metrics', '안정성을 하나의 숫자로 판단할 수 있을까?', 44, '이제 처음의 질문으로 돌아가 보겠습니다.\n우리는 고유값이 모두 안정적인 시스템을 만들었습니다.\n그런데 실제 상태는 한동안 원점에서 멀어졌다가 다시 돌아왔습니다.\n유체에서는 작은 교란이 일시적으로 증폭될 수 있었고, 순환 신경망에서도 비슷한 동역학이 나타날 수 있었습니다.\n여기서 중요한 것은 안정적이라는 말이 여러 의미를 가질 수 있다는 점입니다.\n충분히 긴 시간이 지난 뒤 변화가 사라지는가.\n중간에 변화가 얼마나 커질 수 있는가.\n그리고 어떤 초기 방향에서 가장 큰 증폭이 나타나는가.\n이들은 서로 다른 질문입니다.\n따라서 고유값만으로 시스템의 모든 증폭 특성을 판단할 수는 없습니다.\n우리가 어떤 종류의 안정성을 알고 싶은지 먼저 구분해야 합니다.', '장기 안정/시간별 최댓값/전체시간 최대값 카드', 'A=[[-1,10],[0,-1]], 고정 2D 연속시간 선형 시스템. P(t)=exp(-t)[[1,10t],[0,1]], x0=(0,1)→x(t)=exp(-t)(10t,1). 모든 고유값 -1이며 결함 행렬로 독립 고유벡터 둘이 없으므로 두 고유벡터의 분해 그림을 그리지 않는다. Euclidean norm amplitude를 표시하며 에너지 배율은 그 제곱. 유한시간 특이점이나 실제 NS 해/신경망 측정으로 주장하지 않는다.\nReλ<0:점근안정. sigma_max P(t):고정 t 최대 amplitude. sup_t sigma_max P(t):모든 시간·초기방향 최대 amplitude. 모두norm선택에 의존, 실제 유체 에너지내적에서는 이에맞춰 adjoint/특잇값 해석.'), ('next', '마지막 막으로 연결', 38, '지금까지 나비에 스토크스와 신경망을 오가며 여러 가지 수학적 구조를 살펴봤습니다.\n전체의 크기가 제한되어 있어도 일부 영역에서는 극단적인 값이 나타날 수 있었습니다.\n같은 크기의 변화라도 방향에 따라 증폭되는 정도가 달랐습니다.\n가장 제한적인 모드가 전체 계산의 업데이트 크기를 결정하기도 했습니다.\n그리고 이제는 충분히 시간이 지나면 안정적인 시스템에서도, 중간에는 큰 증폭이 나타날 수 있다는 사실까지 살펴봤습니다.\n이 서로 다른 현상들에는 공통된 질문이 숨어 있습니다.\n시스템이 안정적이라는 말은 정확히 무엇을 측정하고 있다는 뜻일까요?\n이제 처음의 유체로 돌아가, 그 질문을 정리해 보겠습니다.', '5막부터10막의 모티프 → 안정성은 무엇을 측정하는가', 'A=[[-1,10],[0,-1]], 고정 2D 연속시간 선형 시스템. P(t)=exp(-t)[[1,10t],[0,1]], x0=(0,1)→x(t)=exp(-t)(10t,1). 모든 고유값 -1이며 결함 행렬로 독립 고유벡터 둘이 없으므로 두 고유벡터의 분해 그림을 그리지 않는다. Euclidean norm amplitude를 표시하며 에너지 배율은 그 제곱. 유한시간 특이점이나 실제 NS 해/신경망 측정으로 주장하지 않는다.\n이전 통계량/국소집중/입력반응/학습보폭/시간동역학은 서로 다른 양. 실제 유체와 신경망이 같은 PDE라 주장하지 않는다. 11막 통합 질문으로 연결.')]

def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def main():
    manifest=[];master=['# 10막 — 고유값과 일시적 증폭'];tts=[];cues=[];offset=0
    vp=ROOT/'voice_timing.json';voice=json.loads(vp.read_text(encoding='utf-8')) if vp.exists() else None
    if voice:
        assert len(voice['ends'])==sum(len(row[3].splitlines()) for row in DATA)
        assert all(a<b for a,b in zip([0]+voice['ends'][:-1],voice['ends']))
    sentence_index=0
    for i,(slug,title,duration,script,visual,conditions) in enumerate(DATA,1):
        original=duration;directory=ROOT/'scenes'/f'{i:02}_{slug}';directory.mkdir(parents=True,exist_ok=True)
        lines=script.splitlines();weights=[len(s)+12 for s in lines]
        if voice:
            measured=[e-offset for e in voice['ends'][sentence_index:sentence_index+len(lines)]];duration=measured[-1]
        sentence_index+=len(lines)
        current=0;ends=[];local=[]
        for j,(line,w) in enumerate(zip(lines,weights)):
            end=measured[j] if voice else current+duration*w/sum(weights);ends.append(end)
            display=line.replace('암묵적 편향, 임플리시트 바이어스','암묵적 편향, Implicit Bias')
            for a,b in [('이천이십육 년 구월 팔일','2026년 9월 8일'),('오픈에이아이','OpenAI'),('구월 십일','9월 11일'),('나비에 스토크스','Navier–Stokes'),('엘투 노름','L₂ 노름')]: display=display.replace(a,b)
            for a,b in [('엘엘엠 인트 에이트', 'LLM.int8()'), ('스무스 퀀트', 'SmoothQuant'), ('십육 비트', '16비트'), ('팔 비트', '8비트'), ('예순네 개', '64개'), ('예순세 개', '63개'), ('영 점 이오', '0.25'), ('영 점 오', '0.5'), ('영 점 육', '0.6'), ('영 점 이는', '0.2는'), ('영 점 일', '0.1'), ('영 점 사', '0.4'), ('영 점 팔', '0.8'), ('하나만 팔', '하나만 8'), ('최대값은 팔', '최대값은 8'), ('최대 절댓값이 일일 때', '최대 절댓값이 1일 때'), ('백일 때', '100일 때'), ('백까지', '100까지'), ('백 배', '100배'), ('활성값이 팔', '활성값이 8'), ('곱은 이', '곱은 2'), ('활성값을 팔로', '활성값을 8로'), ('가중치를 팔 배', '가중치를 8배'), ('일과 이를', '1과 2를')]: display=display.replace(a,b)
            local.append(f'{j+1}\n{stamp(current)} --> {stamp(end)}\n{display}')
            cues.append(f'{len(cues)+1}\n{stamp(offset+current)} --> {stamp(offset+end)}\n{display}');current=end
        (directory/'captions.srt').write_text('\n\n'.join(local)+'\n',encoding='utf-8')
        (directory/'timing.json').write_text(json.dumps({'duration':duration,'ends':ends,'lines':lines,'basis':voice['basis'] if voice else 'visual storyboard; TTS unmeasured'},ensure_ascii=False,indent=2),encoding='utf-8')
        spoken='\n\n'.join(lines).replace('헤시안, Hessian','헤시안');tts.append(spoken)
        (directory/'script.txt').write_text(spoken+'\n',encoding='utf-8')
        master.append(f'## {i:02} — {title} ({stamp(offset)}–{stamp(offset+duration)})\n\n'+spoken)
        (directory/'spec.md').write_text(f'''# Scene {i:02} — {title}
## 목적과 핵심 주장
{title}를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
{DATA[i-2][1] if i>1 else '9막 마지막의 일시적 증폭 질문'}
## TTS 원문과 확정 길이
{spoken}

- TTS: {'사용자 측정 '+str(duration)+'초' if voice else '미확정. 사용자 허용에 따라 화면 제작 우선.'}
- 화면: {duration}초. 원래 화면 기준은 {original}초.
## 화면 구성과 시간대별 애니메이션
{visual}
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
{title}, 고정 행렬, 고유값, 상태 궤적, norm, 전달 coupling, P(t)의 특잇값, 전단 리프트업, 연속시간 RNN, 안정성 지표, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
{DATA[i][1] if i<len(DATA) else '11막: 안정성이 무엇을 측정하는지 정리'}
## 수학 조건·과장 방지
{conditions}
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
{SOURCES}
''',encoding='utf-8')
        (directory/'scene.py').write_text(f"from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import EnergyScene\n\nclass Scene{i:02}(EnergyScene):\n    index={i}\n",encoding='utf-8')
        manifest.append({'id':f'{i:02}','slug':slug,'directory':f'scenes/{i:02}_{slug}','class':f'Scene{i:02}','duration_seconds':duration if voice else None,'storyboard_seconds':original})
        offset+=duration
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'master_script.md').write_text('\n\n'.join(master)+'\n',encoding='utf-8')
    (ROOT/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(cues)+'\n',encoding='utf-8')
    (ROOT/'sources.md').write_text('# 출처와 확인 기준\n\n확인: 2026-10-08. 논문 관찰과 설명용 수치 모형을 구별한다. 실제 선형 모형의 궤적과 특잇값을 계산한다. 유체 리프트업과 RNN 그림은 선형화 구조의 개념 비교이며 실제 전체 NS 해나 대형 모델의 측정값이 아니다.\n\n'+SOURCES,encoding='utf-8')
    yaml='id: ns10\ntitle: "10막 — 비정규 동역학"\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\ntiming_basis: '+('user_sentence_end_times' if voice else 'visual_storyboard_without_tts')+'\nscenes:\n'
    for row in manifest:yaml+='  - '+'\n    '.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in row.items())+'\n'
    (ROOT/'scenes.yaml').write_text(yaml,encoding='utf-8')

if __name__=='__main__':main()
