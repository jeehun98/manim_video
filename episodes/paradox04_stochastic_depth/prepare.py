"""Store the user's revised narration and exact cumulative utterance timings."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ENDS=[6,8,17,21,27,31,38,44,48,51,57,60,67,71,75,79,85,91,96,100,105,113,119,125,130,133]
TEXT=[
'더 깊은 신경망을 학습시키기 위해, 학습할 때는 일부러 얕은 신경망을 사용하는 방법이 있습니다.',
'바로 스토캐스틱 뎁스입니다.',
'신경망을 깊게 쌓으면 더 복잡한 계산을 표현할 수 있습니다. 하지만 깊어질수록 계산 경로도 길어지고, 학습 과정에서 기울기를 전달하기도 어려워질 수 있습니다.',
'그렇다면 중간의 계산을 통째로 건너뛰면 어떨까요?',
'레지듀얼 블록에는 두 개의 길이 있습니다. 입력을 변환하는 길과, 입력을 그대로 전달하는 지름길입니다.',
'두 길의 결과를 더하면 원래 입력에 새로운 계산 결과가 추가됩니다.',
'스토캐스틱 뎁스는 학습 중 일부 블록의 변환 경로를 무작위로 끄고, 입력을 그대로 전달하는 지름길은 남겨둡니다.',
'변환이 꺼지면 해당 블록의 계산을 건너뛰지만, 입력과 기울기는 항등 경로를 통해 그대로 전달됩니다.',
'이제 여덟 개 블록을 각각 켜거나 끌 수 있다고 생각해 보겠습니다.',
'가능한 조합은 이백오십육 가지입니다.',
'이번 학습에서는 다섯 개의 블록을 사용하고, 다음 학습에서는 다른 조합의 네 개를 사용할 수 있습니다.',
'그런데 왜 이렇게 깊이를 바꾸는 것이 도움이 될까요?',
'항상 같은 블록들이 존재한다면, 뒤쪽 블록은 앞쪽 블록이 만들어내는 특정한 표현에 지나치게 의존할 수 있습니다.',
'하지만 앞쪽 블록이 무작위로 사라진다면 어떨까요?',
'뒤쪽 블록은 그 변환이 없는 입력에서도 작동하도록 학습되어야 합니다.',
'여기서 중요한 것은 신경망의 표현력을 늘리는 것이 아닙니다.',
'전체 신경망이 표현할 수 있는 함수와, 학습 과정에서 실제로 선택되는 함수는 서로 다른 문제입니다.',
'스토캐스틱 뎁스는 하나의 고정된 계산 경로만 잘 작동하도록 학습시키지 않습니다.',
'서로 다른 깊이와 블록 조합에서 발생하는 평균 손실을 줄이도록 학습 목표를 바꿉니다.',
'모든 부분 신경망은 동일한 블록의 가중치를 공유합니다.',
'그 결과 특정 계산 경로에 대한 지나친 의존을 억제하는 정규화 효과가 나타날 수 있습니다.',
'추론할 때는 전체 잔차 블록을 사용합니다. 원래 방법에서는 각 변환 출력을 학습 중 생존 확률에 맞춰 조정합니다.',
'결국 스토캐스틱 뎁스는 더 작은 신경망이 더 뛰어난 표현력을 갖는다는 이야기가 아닙니다.',
'더 작은 부분 신경망에서도 작동하도록 학습시켜, 전체 신경망이 더 좋은 해를 찾도록 유도하는 것입니다.',
'전체 구조는 깊게 유지하면서, 학습할 때는 다양한 깊이의 지름길을 사용하는 것.',
'이것이 스토캐스틱 뎁스의 역설입니다.'
]
def display(s):
    for a,b in [('스토캐스틱 뎁스','Stochastic Depth'),('레지듀얼 블록','Residual Block'),('여덟 개','8개'),('다섯 개','5개'),('네 개','4개'),('이백오십육 가지','256가지')]:s=s.replace(a,b)
    return s
segments=[dict(start=a,end=b,text=display(s)) for a,b,s in zip([0]+ENDS[:-1],ENDS,TEXT)]
(ROOT/'timing.json').write_text(json.dumps(dict(duration_seconds=133,basis='user-provided cumulative utterance end times; audio not supplied',sentence_end_seconds=ENDS,segments=segments),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'narration.md').write_text('# 신경망의 역설 04 — 신경망은 얕게 학습해야 더 깊어진다?\n\n사용자 확정 대본 · 26구간 · 133초 · TTS 음원 미제공\n\n'+'\n\n'.join(f'## {s["start"]}–{s["end"]}초\n\n{s["text"]}' for s in segments)+'\n',encoding='utf-8')
(ROOT/'tts_script.txt').write_text('\n\n'.join(TEXT)+'\n',encoding='utf-8')
def stamp(n):return f'00:{n//60:02}:{n%60:02},000'
(ROOT/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(segments,1))+'\n',encoding='utf-8')
