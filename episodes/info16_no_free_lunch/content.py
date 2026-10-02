"""Finite binary worlds make the uniform-prior NFL comparison explicit."""
from itertools import product

TRAIN = (0, 1, 1)
COMPLETIONS = list(product((0, 1), repeat=4))
DISPLAY = [
    '세 점의 정답을 봤습니다. 그런데 다음 점의 정답은 아직 모릅니다.',
    '여기 두 세계가 있습니다. 본 세 점은 같지만, 다음 점의 정답은 서로 다릅니다.',
    '보지 못한 네 점을 채우는 방법은 열여섯 가지입니다. 모두 같은 학습 데이터에 맞습니다.',
    '다음 답을 1로 고르면 여덟 세계에서 맞고, 0으로 골라도 여덟 세계에서 맞습니다.',
    '가능한 모든 정답 함수를 똑같이 평균내면, 보지 못한 점에서는 어느 학습법도 평균적으로 더 잘 맞히지 못합니다. 이것이 No Free Lunch 정리입니다.',
    '그렇다면 실제로는 왜 맞힐까요? 우리는 가까운 점의 답이 비슷할 것이라고 가정합니다.',
    '그 가정이 맞는 세계에서는 새 점도 잘 맞힙니다. 답이 제멋대로 바뀌는 세계에서는 실패합니다.',
    '이처럼 보지 못한 곳을 추측하게 하는 선호와 가정이 귀납 편향입니다.',
    'CNN도 같은 필터를 다른 위치에 씁니다. 반복되는 지역 패턴이라는 가정이 이미지와 잘 맞습니다.',
    '구조는 압축도 돕습니다. 반복을 짧게 적듯, 학습도 관측한 패턴을 새로운 곳으로 이어갑니다.',
    '훈련 정답을 외우는 것만으로는 부족합니다. 새 정답이 독립적인 반반이라면, 예측은 절반만 맞습니다.',
    'No Free Lunch는 좋은 알고리즘이 없다는 뜻이 아닙니다. 어떤 세계에서나 통하는 만능 학습법은 없다는 뜻입니다.',
    '일반화하려면 세계에 대한 가정이 필요합니다. 그 가정이 실제 구조와 맞아야 합니다. 학습은 그 만남에서 시작됩니다.',
]
READINGS = [('No Free Lunch', '노 프리 런치'), ('CNN', '씨 엔 엔'), ('1로', '일로'), ('0으로', '영으로')]
SPOKEN=[]
CUES=[]
frames=0
for display in DISPLAY:
    spoken=display
    for original,reading in READINGS:
        spoken=spoken.replace(original,reading)
    SPOKEN.append(spoken)
    count=round(max(4.5,len(''.join(spoken.split()))/7+.18*spoken.count('.'))*30)
    CUES.append((frames/30,(frames+count)/30,display,spoken))
    frames+=count
DURATION=frames/30
TITLES=['본 데이터와 새 점','같은 증거 / 다른 세계','가능한 16개 세계','어느 예측도 8/16','No Free Lunch의 조건','가까운 것은 비슷하다','가정과 세계의 일치','귀납 편향','CNN의 구조적 가정','압축과 학습의 닮은점','암기와 일반화의 차이','정리의 핵심 의미','구조와 가정의 만남']
