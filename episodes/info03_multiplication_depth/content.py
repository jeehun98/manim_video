"""Narration and speech-estimated timing for the logarithmic coordinate episode."""
TEXT=[
'확률은 곱해지는데, 정보는 왜 더해질까요?',
'서로 독립인 공정한 두 동전에서, 앞면과 뒷면을 하나씩 확인합니다.',
'각 결과의 확률은 1/2. 둘이 함께 나올 확률은 곱해서 1/4입니다.',
'정보량은 두 관측에서 얻은 양을 더할 수 있게 정하고 싶습니다.',
'필요한 건 번역기입니다. 확률의 곱셈을 정보의 덧셈으로 옮기는 함수죠.',
'확률을 계속 반으로 줄여봅시다. 1/2, 1/4, 1/8이 됩니다.',
'값은 곱해져 줄지만, 반으로 줄인 횟수는 1, 2, 3으로 쌓입니다.',
'로그는 곱셈의 깊이를 세는 좌표계입니다. 곱한 뒤 옮겨도, 옮긴 뒤 더해도 같습니다.',
'다만 로그 값은 음수가 됩니다. 마이너스를 붙이면 드문 결과일수록 커집니다.',
'밑을 2로 정하면, 반으로 줄어들 때마다 1 bit가 늘어납니다.',
'두 동전의 확률은 곱해서 1/4. 정보량은 더해서 2 bits입니다.',
'공식보다 구조를 보세요. 마이너스 로그는 곱셈을 덧셈으로 번역합니다.',
'다음 질문입니다. 결과가 나오기 전, 얻을 정보량의 평균은 얼마일까요?',
]
REPLACEMENTS=[('1/8','팔분의 일'),('1/4','사분의 일'),('1/2','이분의 일'),('2 bits','이 비트'),('1 bit','일 비트'),('2','이'),('1','일'),('3','삼')]
SPOKEN=[]
for text in TEXT:
    for old,new in REPLACEMENTS:text=text.replace(old,new)
    SPOKEN.append(text)
CUES=[]
frames=0
for i,(display,spoken) in enumerate(zip(TEXT,SPOKEN)):
    seconds=max(2.6,len(''.join(spoken.split()))/7.0+.18*(spoken.count('.')+spoken.count('?')))+(.5 if i==len(TEXT)-1 else 0)
    count=round(seconds*30)
    CUES.append((frames/30,(frames+count)/30,display,spoken));frames+=count
DURATION=frames/30
