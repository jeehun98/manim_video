"""Act 11: stability finale."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
SOURCES='- Trefethen et al. (1993), Hydrodynamic Stability Without Eigenvalues: https://people.maths.ox.ac.uk/trefethen/ttrd.pdf\n- Dettmers et al. (2022), LLM.int8(): https://arxiv.org/abs/2208.07339\n- MIT, Forward and Backward Euler Methods: https://web.mit.edu/10.001/Web/Course_Notes/Differential_Equations_Notes/node3.html\n- Stanford, Derivatives and Backpropagation: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf\n- Gunasekar et al. (2018), Optimization Geometry and Implicit Bias: https://proceedings.mlr.press/v80/gunasekar18a.html\n- Kerg et al. (2019), Non-normal Recurrent Neural Network: https://arxiv.org/abs/1905.12080\n- 수학 조건의 상세 설명: 기존 1~10막 spec.md 및 sources.md. 이번 막은 이미 소개한 질문을 회수하며 새로운 특이점이나 학습 성능 주장을 추가하지 않는다.\n'
DATA=[('return', '처음의 물로 돌아가다', 34, '처음에 우리는 물의 움직임을 수많은 속도 화살표로 표현했습니다.\n그리고 이 화살표들이 시간에 따라 어떻게 변하는지 살펴봤습니다.\n유체의 흐름은 새로운 구조를 만들고, 점성은 급격한 속도 차이를 완화했습니다.\n삼차원에서는 소용돌이가 늘어나면서 회전의 강도가 증폭될 수도 있었습니다.\n이렇게 시작한 질문은 결국, 매끄러운 유체가 언제까지 매끄럽게 유지될 수 있는가로 이어졌습니다.\n그런데 이 문제를 따라가면서 우리는 유체역학을 넘어서는 몇 가지 수학적 구조를 발견했습니다.', '속도장 → 점성 완화 → 보티시티 관 늘어남 → 전체 시야', '서로 다른 현상을 같은 방정식으로 취급하지 않는다. 유체 전체 에너지의 유한성만으로 L∞ 상한이 나오지 않는다는 사실과 실제 폭주 해의 존재는 구별한다. 유한한 활성 행렬에는 max≤L2 상한이 있으므로 이상치를 연속체 특이점과 동일시하지 않는다. 유체 순간 강도는 변형률 S와 정렬에, 신경망 국소 입력 반응은 Jacobian 특잇값에 의존한다. 명시적 확산과 양의 곡률 이차 손실 GD 안정성은 수치 조건이며 물리 특이점이 아니다. 존재와 실현은 각 시스템에 다른 제약이 적용된다. 고정 유한차원 연속시간 A=[[-1,10],[0,-1]]의 정확한 P(t)=exp(-t)[[1,10t],[0,1]]를 재사용한다. Reλ<0의 점근 안정성과 Euclidean norm의 일시적 증폭을 구별한다. 다섯 질문은 모두 같은 종류의 안정성 정의가 아니다.'), ('global_local', '첫 번째 구별: 전체와 국소', 46, '첫 번째는 전체와 국소의 차이였습니다.\n유체의 운동에너지는 공간 전체에 걸쳐 속도 제곱을 더한 값입니다.\n하지만 이 값이 유한하다는 사실만으로, 모든 위치의 속도가 제한된다고 말할 수는 없었습니다.\n강한 흐름이 나타나는 영역이 충분히 작아진다면, 전체 에너지는 유한하면서도 최대 속도는 커질 수 있습니다.\n신경망에서도 비슷한 구별이 필요했습니다.\n평균적인 활성값이 작아도, 일부 토큰이나 특징 차원에서는 극단적으로 큰 값이 나타날 수 있었습니다.\n그러한 이상치는 양자화 과정에서 다른 값들의 정밀도까지 제한할 수 있었습니다.\n전체를 하나의 숫자로 요약하면 편리하지만, 그 숫자가 모든 부분을 설명하는 것은 아닙니다.', '속도장과 활성값 행렬 · 전체와 최대값 분리', '서로 다른 현상을 같은 방정식으로 취급하지 않는다. 유체 전체 에너지의 유한성만으로 L∞ 상한이 나오지 않는다는 사실과 실제 폭주 해의 존재는 구별한다. 유한한 활성 행렬에는 max≤L2 상한이 있으므로 이상치를 연속체 특이점과 동일시하지 않는다. 유체 순간 강도는 변형률 S와 정렬에, 신경망 국소 입력 반응은 Jacobian 특잇값에 의존한다. 명시적 확산과 양의 곡률 이차 손실 GD 안정성은 수치 조건이며 물리 특이점이 아니다. 존재와 실현은 각 시스템에 다른 제약이 적용된다. 고정 유한차원 연속시간 A=[[-1,10],[0,-1]]의 정확한 P(t)=exp(-t)[[1,10t],[0,1]]를 재사용한다. Reλ<0의 점근 안정성과 Euclidean norm의 일시적 증폭을 구별한다. 다섯 질문은 모두 같은 종류의 안정성 정의가 아니다.'), ('direction', '두 번째 구별: 크기와 방향', 44, '두 번째는 크기와 방향의 차이였습니다.\n삼차원 유체에서는 보티시티가 주변 흐름의 어떤 방향을 가리키느냐에 따라 증폭되거나 약해질 수 있었습니다.\n속도장의 변화율이 보티시티 벡터에 작용하기 때문입니다.\n신경망에서도 같은 수학적 구조를 발견했습니다.\n야코비안은 작은 입력 변화 벡터에 작용하고, 그 변화가 어느 방향을 가리키느냐에 따라 출력의 증폭 정도가 달라졌습니다.\n같은 크기의 변화라도 결과는 서로 다를 수 있습니다.\n따라서 현재의 값이 얼마나 큰지를 아는 것만으로는 충분하지 않습니다.\n어떤 방향으로 변화하고 있으며, 그 방향에 어떤 변환이 작용하는지도 알아야 합니다.', '회전축의 변형률 정렬과 Jacobian의 원/타원 비교', '서로 다른 현상을 같은 방정식으로 취급하지 않는다. 유체 전체 에너지의 유한성만으로 L∞ 상한이 나오지 않는다는 사실과 실제 폭주 해의 존재는 구별한다. 유한한 활성 행렬에는 max≤L2 상한이 있으므로 이상치를 연속체 특이점과 동일시하지 않는다. 유체 순간 강도는 변형률 S와 정렬에, 신경망 국소 입력 반응은 Jacobian 특잇값에 의존한다. 명시적 확산과 양의 곡률 이차 손실 GD 안정성은 수치 조건이며 물리 특이점이 아니다. 존재와 실현은 각 시스템에 다른 제약이 적용된다. 고정 유한차원 연속시간 A=[[-1,10],[0,-1]]의 정확한 P(t)=exp(-t)[[1,10t],[0,1]]를 재사용한다. Reλ<0의 점근 안정성과 Euclidean norm의 일시적 증폭을 구별한다. 다섯 질문은 모두 같은 종류의 안정성 정의가 아니다.'), ('restrictive', '세 번째 구별: 평균적인 조건과 가장 제한적인 모드', 32, '세 번째는 전체 계산을 제한하는 조건이었습니다.\n유체를 컴퓨터로 계산할 때, 아주 작은 격자 하나가 허용되는 시간 간격을 제한할 수 있었습니다.\n신경망의 학습에서도 비슷한 일이 나타났습니다.\n대부분의 파라미터 방향이 완만하더라도, 유난히 가파른 방향 하나 때문에 학습률을 낮춰야 할 수 있었습니다.\n이는 시스템의 평균적인 상태가 아니라, 가장 제한적인 모드가 전체 업데이트의 안정성을 결정할 수 있다는 뜻입니다.\n그리고 두 경우 모두 업데이트 연산자의 고유값을 통해 수치적인 안정성을 분석할 수 있었습니다.', '작은 격자와 가파른 곡률 · 업데이트 크기 감소', '서로 다른 현상을 같은 방정식으로 취급하지 않는다. 유체 전체 에너지의 유한성만으로 L∞ 상한이 나오지 않는다는 사실과 실제 폭주 해의 존재는 구별한다. 유한한 활성 행렬에는 max≤L2 상한이 있으므로 이상치를 연속체 특이점과 동일시하지 않는다. 유체 순간 강도는 변형률 S와 정렬에, 신경망 국소 입력 반응은 Jacobian 특잇값에 의존한다. 명시적 확산과 양의 곡률 이차 손실 GD 안정성은 수치 조건이며 물리 특이점이 아니다. 존재와 실현은 각 시스템에 다른 제약이 적용된다. 고정 유한차원 연속시간 A=[[-1,10],[0,-1]]의 정확한 P(t)=exp(-t)[[1,10t],[0,1]]를 재사용한다. Reλ<0의 점근 안정성과 Euclidean norm의 일시적 증폭을 구별한다. 다섯 질문은 모두 같은 종류의 안정성 정의가 아니다.'), ('realized', '네 번째 구별: 존재와 실현', 38, '네 번째는 어떤 상태가 존재한다는 것과, 실제로 그 상태가 실현된다는 것의 차이였습니다.\n속도가 폭주하는 모양의 함수를 만드는 것만으로는 나비에 스토크스 문제를 해결할 수 없었습니다.\n그 함수가 실제 운동 방정식과 외력의 조건을 만족해야 했습니다.\n신경망에서도 좋은 해가 존재한다는 사실만으로, 학습이 반드시 그곳에 도달한다고 말할 수는 없었습니다.\n학습은 현재 위치의 정보를 바탕으로 경로를 만들어갑니다.\n초기점과 학습 규칙에 따라 서로 다른 해를 선택할 수도 있습니다.\n서로 다른 종류의 문제이지만, 둘 다 가능한 상태들의 집합만으로는 실제로 나타나는 상태를 충분히 설명할 수 없다는 사실을 보여줬습니다.', '유효한 유체 후보의 조건과 초기점별 학습 경로', '서로 다른 현상을 같은 방정식으로 취급하지 않는다. 유체 전체 에너지의 유한성만으로 L∞ 상한이 나오지 않는다는 사실과 실제 폭주 해의 존재는 구별한다. 유한한 활성 행렬에는 max≤L2 상한이 있으므로 이상치를 연속체 특이점과 동일시하지 않는다. 유체 순간 강도는 변형률 S와 정렬에, 신경망 국소 입력 반응은 Jacobian 특잇값에 의존한다. 명시적 확산과 양의 곡률 이차 손실 GD 안정성은 수치 조건이며 물리 특이점이 아니다. 존재와 실현은 각 시스템에 다른 제약이 적용된다. 고정 유한차원 연속시간 A=[[-1,10],[0,-1]]의 정확한 P(t)=exp(-t)[[1,10t],[0,1]]를 재사용한다. Reλ<0의 점근 안정성과 Euclidean norm의 일시적 증폭을 구별한다. 다섯 질문은 모두 같은 종류의 안정성 정의가 아니다.'), ('transient', '다섯 번째 구별: 장기적 안정성과 순간적인 증폭', 34, '마지막은 안정성 자체에 대한 질문이었습니다.\n어떤 시스템은 모든 고유값이 장기적인 안정성을 나타내더라도, 특정 초기 변화가 일시적으로 크게 증폭될 수 있었습니다.\n비정규 행렬에서는 서로 다른 방향의 변화가 결합되면서 이런 현상이 나타날 수 있었습니다.\n유체의 전단 흐름에서도, 순환 신경망에서도 이러한 일시적인 증폭을 살펴볼 수 있었습니다.\n따라서 충분히 시간이 지나면 변화가 사라진다는 사실과, 그 과정에서 변화가 한 번도 커지지 않는다는 사실은 다릅니다.\n안정적이라는 말을 사용하기 전에, 어떤 시간 범위의 어떤 변화를 측정하는지 구분해야 하는 것입니다.', '정확한 비정규 궤적과 norm 시간 곡선', '서로 다른 현상을 같은 방정식으로 취급하지 않는다. 유체 전체 에너지의 유한성만으로 L∞ 상한이 나오지 않는다는 사실과 실제 폭주 해의 존재는 구별한다. 유한한 활성 행렬에는 max≤L2 상한이 있으므로 이상치를 연속체 특이점과 동일시하지 않는다. 유체 순간 강도는 변형률 S와 정렬에, 신경망 국소 입력 반응은 Jacobian 특잇값에 의존한다. 명시적 확산과 양의 곡률 이차 손실 GD 안정성은 수치 조건이며 물리 특이점이 아니다. 존재와 실현은 각 시스템에 다른 제약이 적용된다. 고정 유한차원 연속시간 A=[[-1,10],[0,-1]]의 정확한 P(t)=exp(-t)[[1,10t],[0,1]]를 재사용한다. Reλ<0의 점근 안정성과 Euclidean norm의 일시적 증폭을 구별한다. 다섯 질문은 모두 같은 종류의 안정성 정의가 아니다.'), ('questions', '안정성은 하나의 성질이 아니다', 42, '이제 처음의 질문으로 돌아가 보겠습니다.\n시스템이 안정적이라는 것은 정확히 무엇을 의미할까요?\n전체 에너지가 제한되어 있다는 뜻일까요?\n가장 극단적인 부분의 크기가 제한되어 있다는 뜻일까요?\n어떤 방향에서도 변화가 크게 증폭되지 않는다는 뜻일까요?\n아니면 충분히 긴 시간이 지난 뒤 모든 변화가 사라진다는 뜻일까요?\n이 질문들은 서로 다른 수학적 조건을 나타냅니다.\n그리고 한 조건이 성립한다고 해서 다른 조건까지 자동으로 성립하는 것은 아닙니다.\n따라서 복잡한 시스템의 안정성을 이해하려면, 먼저 무엇을 측정하고 무엇을 보장하려는지 명확하게 구분해야 합니다.', 'STABILITY를 다섯 가지 질문으로 분해', '서로 다른 현상을 같은 방정식으로 취급하지 않는다. 유체 전체 에너지의 유한성만으로 L∞ 상한이 나오지 않는다는 사실과 실제 폭주 해의 존재는 구별한다. 유한한 활성 행렬에는 max≤L2 상한이 있으므로 이상치를 연속체 특이점과 동일시하지 않는다. 유체 순간 강도는 변형률 S와 정렬에, 신경망 국소 입력 반응은 Jacobian 특잇값에 의존한다. 명시적 확산과 양의 곡률 이차 손실 GD 안정성은 수치 조건이며 물리 특이점이 아니다. 존재와 실현은 각 시스템에 다른 제약이 적용된다. 고정 유한차원 연속시간 A=[[-1,10],[0,-1]]의 정확한 P(t)=exp(-t)[[1,10t],[0,1]]를 재사용한다. Reλ<0의 점근 안정성과 Euclidean norm의 일시적 증폭을 구별한다. 다섯 질문은 모두 같은 종류의 안정성 정의가 아니다.'), ('bridges', '서로 다른 분야에서 같은 질문이 반복된다', 42, '나비에 스토크스는 유체의 움직임을 기술하는 방정식입니다.\n신경망은 입력을 변환하고, 데이터를 통해 파라미터를 학습하는 시스템입니다.\n둘은 서로 다른 목적과 구조를 가지고 있습니다.\n하지만 그 안에서 마주치는 수학적 질문에는 공통점이 있었습니다.\n전체를 하나의 값으로 요약할 때 무엇을 놓치는가.\n어떤 방향에서 변화가 가장 크게 증폭되는가.\n어떤 모드가 전체 계산을 제한하는가.\n그리고 현재의 상태와 실제 동역학은 어떤 관계를 갖는가.\n서로 다른 현상을 같은 것으로 취급하지 않더라도, 이러한 공통 구조를 통해 새로운 관점을 얻을 수 있습니다.', '두 영역에서 다섯 개 질문을 선으로 연결', '서로 다른 현상을 같은 방정식으로 취급하지 않는다. 유체 전체 에너지의 유한성만으로 L∞ 상한이 나오지 않는다는 사실과 실제 폭주 해의 존재는 구별한다. 유한한 활성 행렬에는 max≤L2 상한이 있으므로 이상치를 연속체 특이점과 동일시하지 않는다. 유체 순간 강도는 변형률 S와 정렬에, 신경망 국소 입력 반응은 Jacobian 특잇값에 의존한다. 명시적 확산과 양의 곡률 이차 손실 GD 안정성은 수치 조건이며 물리 특이점이 아니다. 존재와 실현은 각 시스템에 다른 제약이 적용된다. 고정 유한차원 연속시간 A=[[-1,10],[0,-1]]의 정확한 P(t)=exp(-t)[[1,10t],[0,1]]를 재사용한다. Reλ<0의 점근 안정성과 Euclidean norm의 일시적 증폭을 구별한다. 다섯 질문은 모두 같은 종류의 안정성 정의가 아니다.'), ('finale', '마지막으로 남길 질문', 48, '처음에는 물의 움직임을 이해하려고 했습니다.\n그런데 그 과정에서 우리는 신경망의 활성값과 학습 경로, 방향별 증폭과 안정성까지 살펴보게 됐습니다.\n서로 다른 시스템에서 같은 수학적 구조를 발견한다는 것은, 두 시스템이 동일하다는 뜻은 아닙니다.\n오히려 복잡한 현상에서 무엇을 구분해서 바라봐야 하는지 알려줍니다.\n전체와 국소.\n크기와 방향.\n가능한 상태와 실제 경로.\n그리고 장기적인 안정성과 일시적인 증폭.\n어떤 시스템을 이해할 때 중요한 것은 단순히 안정적인지 불안정한지를 묻는 것이 아닐지도 모릅니다.\n무엇이 안정적인가. 어떤 방향에서, 어느 위치에서, 그리고 어느 시간 동안 안정적인가.\n그 질문을 구분하기 시작할 때, 서로 달라 보였던 현상들 사이에서도 공통된 수학적 구조가 드러납니다.', '속도장 → 활성값 → 원과 타원 → 손실 지형 → 최종 질문', '서로 다른 현상을 같은 방정식으로 취급하지 않는다. 유체 전체 에너지의 유한성만으로 L∞ 상한이 나오지 않는다는 사실과 실제 폭주 해의 존재는 구별한다. 유한한 활성 행렬에는 max≤L2 상한이 있으므로 이상치를 연속체 특이점과 동일시하지 않는다. 유체 순간 강도는 변형률 S와 정렬에, 신경망 국소 입력 반응은 Jacobian 특잇값에 의존한다. 명시적 확산과 양의 곡률 이차 손실 GD 안정성은 수치 조건이며 물리 특이점이 아니다. 존재와 실현은 각 시스템에 다른 제약이 적용된다. 고정 유한차원 연속시간 A=[[-1,10],[0,-1]]의 정확한 P(t)=exp(-t)[[1,10t],[0,1]]를 재사용한다. Reλ<0의 점근 안정성과 Euclidean norm의 일시적 증폭을 구별한다. 다섯 질문은 모두 같은 종류의 안정성 정의가 아니다.')]

def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def main():
    manifest=[];master=['# 11막 — 안정적이라는 것은 무엇을 의미할까?'];tts=[];cues=[];offset=0
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
{DATA[i-2][1] if i>1 else '10막의 장기 안정성과 일시적 증폭'}
## TTS 원문과 확정 길이
{spoken}

- TTS: {'사용자 측정 '+str(duration)+'초' if voice else '미확정. 사용자 허용에 따라 화면 제작 우선.'}
- 화면: {duration}초. 원래 화면 기준은 {original}초.
## 화면 구성과 시간대별 애니메이션
{visual}
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
{title}, 속도장, 전체와 국소, 변형률과 Jacobian, 작은 격자와 곡률, 실현 경로, 과도 증폭, 다섯 질문과 분야 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
{DATA[i][1] if i<len(DATA) else '시리즈 종료: 무엇이, 어디서, 어떤 방향으로, 언제까지 안정적인가'}
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
    yaml='id: ns11\ntitle: "11막 — 안정성의 질문"\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\ntiming_basis: '+('user_sentence_end_times' if voice else 'visual_storyboard_without_tts')+'\nscenes:\n'
    for row in manifest:yaml+='  - '+'\n    '.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in row.items())+'\n'
    (ROOT/'scenes.yaml').write_text(yaml,encoding='utf-8')

if __name__=='__main__':main()
