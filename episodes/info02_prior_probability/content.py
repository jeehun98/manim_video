"""Narration and estimated, frame-aligned speech timing."""
TEXT=[
'같은 A. 얻은 정보도 같을까요?',
'한 사람은 A의 확률을 0.5로, 다른 사람은 0.99로 예측했습니다.',
'여기서 믿음은 관측 전의 예측입니다. 확률분포는 그 예측을 수치로 표현합니다.',
'확률은 사건에 부여한 수치입니다. 반드시 개인의 믿음을 뜻하는 것은 아닙니다.',
'첫 사람은 A를 보고, 절반을 차지하던 B를 제외합니다.',
'두 번째 사람도 B를 제외하지만, 그 확률은 겨우 0.01이었습니다.',
'결과도, 지운 후보 수도 같습니다. 다른 것은 관측 전에 A에 부여한 확률입니다.',
'이제 두 번째 사람이 B를 봅니다. 0.99를 부여했던 A가 제외됩니다.',
'관측 전 확률이 낮을수록, 그 결과의 자기정보량은 큽니다. 감정적인 놀라움과는 구별합니다.',
'정보량은 관측한 결과와, 그 결과에 부여했던 확률로 정합니다.',
'그렇다면 확률을 어떻게 정보량으로 바꿀까요? 다음 편에서 숫자로 재봅니다.',
]
SPOKEN=[s.replace('0.99','영 점 구 구').replace('0.01','영 점 영 일').replace('0.5','영 점 오').replace('A','에이').replace('B','비') for s in TEXT]
CUES=[]
frames=0
for i,(display,spoken) in enumerate(zip(TEXT,SPOKEN)):
    seconds=max(2.2,len(''.join(spoken.split()))/7.0+.18*(spoken.count('.')+spoken.count('?')))+(.5 if i==len(TEXT)-1 else 0)
    n=round(seconds*30)
    CUES.append((frames/30,(frames+n)/30,display,spoken));frames+=n
DURATION=frames/30
