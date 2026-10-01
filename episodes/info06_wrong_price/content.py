"""Cross entropy as frequencies from p and log-cost prices from q."""
import math

P = (.7, .1, .1, .1)
Q = (.1, .3, .3, .3)
SYMBOLS = "ABCD"
COUNTS = (14, 2, 2, 2)
MESSAGE = "".join({3: "B", 7: "C", 11: "D", 15: "B", 17: "C", 19: "D"}.get(i, "A") for i in range(20))

def cross_entropy(p, q):
    return sum(-a * math.log2(b) if b > 0 else math.inf for a, b in zip(p, q) if a > 0)

def interpolated_q(t):
    return tuple((1-t)*a+t*b for a, b in zip(P, Q))

PRICES_P = tuple(-math.log2(p) for p in P)
PRICES_Q = tuple(-math.log2(q) for q in Q)
H_P = cross_entropy(P, P)
H_PQ = cross_entropy(P, Q)
EXTRA = H_PQ - H_P

TEXT = [
    "현실은 그대로인데, 가격표만 틀렸다면 어떤 비용을 낼까요?",
    "실제로는 A가 자주 나옵니다. 그런데 모형은 A를 드물다고 예측합니다.",
    "A의 이상적 비트 비용이 커집니다. 실제 정수 코드 길이와는 구별합니다.",
    "데이터는 실제 분포에서 나옵니다. 자주 나오는 A의 비싼 비용을 계속 냅니다.",
    "실제 분포 p는 얼마나 자주, 모형 q는 얼마씩 내는지를 결정합니다.",
    "등장 확률에 정보 비용을 곱해 더하면, Cross Entropy입니다.",
    "같은 현실인데, 다른 가격표로 평균 비용이 커졌습니다.",
    "실제 분포를 고정하면, 예측이 실제와 같을 때 비용이 최소입니다. Entropy와 같아지죠.",
    "분류에서도 원리는 같습니다. cat이 정답인 관측에서는, cat에 준 확률의 비용만 남습니다.",
    "정답을 거의 확신했다면 작고, 정답을 거의 불가능하게 봤다면 비용은 커집니다.",
    "이 비용을 줄이는 건, 실제로 만나는 결과에 확률의 가격표를 맞추는 일입니다.",
    "그렇다면 본래 필요한 비용을 빼면 무엇이 남을까요? 잘못 예측해서 더 낸 비용입니다.",
]
REPLACEMENTS = [("Cross Entropy", "크로스 엔트로피"), ("Entropy", "엔트로피"), ("cat", "캣"), ("A", "에이"), (" p", " 피"), (" q", " 큐")]
SPOKEN = []
for display in TEXT:
    spoken = display
    for old, new in REPLACEMENTS:
        spoken = spoken.replace(old, new)
    SPOKEN.append(spoken)

CUES = []
frames = 0
for index, (display, spoken) in enumerate(zip(TEXT, SPOKEN)):
    seconds = max(2.6, len("".join(spoken.split()))/7.0 + .18*(spoken.count(".")+spoken.count("?")))
    if index == len(TEXT)-1:
        seconds += .5
    count = round(seconds*30)
    CUES.append((frames/30, (frames+count)/30, display, spoken))
    frames += count
DURATION = frames/30
