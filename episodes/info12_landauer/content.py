"""Narration timing and standard symmetric-memory Landauer constants."""
import math
KB=1.380649e-23
TEMPERATURE=300
QMIN=KB*TEMPERATURE*math.log(2)
DISPLAY=[
 '두 칸짜리 상자에 공 하나가 있습니다. 왼쪽이면 0, 오른쪽이면 1입니다.',
 '처음에는 어디 있는지 모릅니다. 두 위치는 반반의 확률로 가능합니다.',
 '이제 어디에 있었든 왼쪽에 모읍니다. 칸막이를 열고, 공간을 좁힌 뒤 장치를 되돌립니다.',
 '왼쪽에서 시작해도, 오른쪽에서 시작해도 끝은 같습니다. 지금 모습만 보고 처음 위치를 알 수 있을까요?',
 '공은 사라지지 않았습니다. 사라진 것은 처음 어느 쪽에 있었는지의 구분입니다.',
 '가능한 위치는 두 개에서 하나로 줄었습니다. 메모리의 엔트로피가 줄어든 것입니다.',
 '하지만 전체 엔트로피까지 줄일 수는 없습니다. 메모리의 감소를 주변 환경의 증가가 보상해야 합니다.',
 '그래서 초기화하며 환경으로 열을 내보냅니다. 공을 한쪽에 모으는 데 물리적인 대가가 있는 것입니다.',
 '이때 환경으로 내보내는 평균 열에는 최소값이 있습니다. 이것이 란다우어 한계입니다.',
 '실온 300켈빈에서는 한 비트당 약 3 곱하기 10의 마이너스 21승 줄입니다. 작지만 영은 아닙니다.',
 '이것은 컴퓨터의 전체 소비 에너지가 아닙니다. 실제 소비는 더 크고, 이 값은 정보 삭제의 최소 비용입니다.',
 '두 위치를 맞바꾸기만 하면 처음 위치를 되찾을 수 있습니다. 이런 가역적 계산에는 삭제 비용이 필수는 아닙니다.',
 '물론 실제 장치의 소비가 영이라는 뜻은 아닙니다. 그렇다면 입력을 보존하는 계산은 이 비용을 어디까지 피할까요?',
]
READINGS=[('300','삼백'),('21','이십일'),('10','십'),('3','삼'),('1','일'),('0','영')]
SPOKEN=[]
for value in DISPLAY:
    for a,b in READINGS:value=value.replace(a,b)
    SPOKEN.append(value)
CUES=[];frames=0
for i,(display,spoken) in enumerate(zip(DISPLAY,SPOKEN)):
    duration=max(3.5,len(''.join(spoken.split()))/7+.18*(spoken.count('.')+spoken.count('?')))
    if i==len(DISPLAY)-1:duration+=.5
    count=round(duration*30)
    CUES.append((frames/30,(frames+count)/30,display,spoken));frames+=count
DURATION=frames/30
