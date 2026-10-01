"""KL is the signed event-price difference averaged under the source."""
import math

P = (.7, .1, .1, .1)
Q = (.1, .3, .3, .3)

def entropy(p):
    return -sum(a*math.log2(a) for a in p if a > 0)

def cross_entropy(p, q):
    return sum(-a*math.log2(b) if b > 0 else math.inf for a,b in zip(p,q) if a > 0)

def kl(p, q):
    return sum(a*math.log2(a/b) if b > 0 else math.inf for a,b in zip(p,q) if a > 0)

def model(t):
    return tuple((1-t)*a+t*b for a,b in zip(P,Q))

BASE = entropy(P)
TOTAL = cross_entropy(P,Q)
EXTRA = kl(P,Q)
REVERSE = kl(Q,P)
DELTAS = tuple(math.log2(a/b) for a,b in zip(P,Q))
CONTRIBUTIONS = tuple(a*d for a,d in zip(P,DELTAS))

TEXT = [
    "청구서에서, 틀린 예측 때문에 더 낸 비용만 떼어낼 수 있을까요?",
    "실제 확률을 알아도, 나온 결과는 표현해야 합니다. 이 본래 비용은 남습니다.",
    "총비용에서 본래 비용을 빼면, 예측이 틀려서 추가된 부분이 남습니다.",
    "이 평균 추가비용이 KL Divergence입니다.",
    "사건 하나에서는, 모형의 정보 가격에서 실제 확률에 맞는 가격을 뺍니다.",
    "어떤 사건은 오히려 할인받습니다. 하지만 실제 빈도로 평균내면, 추가비용은 0 이상입니다.",
    "방향을 바꾸면 비용도 달라집니다. 데이터를 만드는 세계와 가격표의 역할이 바뀌니까요.",
    "그래서 KL은 보통의 거리와 다릅니다. 어느 쪽에서 평균내는지가 중요합니다.",
    "모형이 실제 분포와 같아지면, 추가비용만 사라집니다. 본래 비용은 그대로입니다.",
    "실제 분포가 고정된 학습에서는, 모델이 줄이는 것은 이 추가분입니다.",
    "이제 하나를 알아서 다른 하나의 비용을 줄여봅시다. 얼마나 덜 모르게 될까요?",
]
REPLACEMENTS = [("KL Divergence","케이엘 다이버전스"),("KL","케이엘"),("0","영")]
SPOKEN = []
for display in TEXT:
    spoken = display
    for old,new in REPLACEMENTS:
        spoken = spoken.replace(old,new)
    SPOKEN.append(spoken)
CUES = []
frames = 0
for index,(display,spoken) in enumerate(zip(TEXT,SPOKEN)):
    seconds = max(2.6,len("".join(spoken.split()))/7.0+.18*(spoken.count(".")+spoken.count("?")))
    if index == len(TEXT)-1:
        seconds += .5
    count = round(seconds*30)
    CUES.append((frames/30,(frames+count)/30,display,spoken))
    frames += count
DURATION = frames/30
