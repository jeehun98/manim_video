"""User-supplied narration and cumulative utterance boundaries."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ENDS=[4,6,14,20,23,31,35,43,47,50,55,61,67,71,79,82,88,94,96]
TEXT=[
'신경망을 더 잘 학습시키기 위해, 정답을 일부러 틀리게 알려주는 방법이 있습니다.',
'바로 레이블 스무딩입니다.',
'고양이 사진의 정답은 고양이입니다. 일반적인 분류 학습에서는 고양이 백 퍼센트, 나머지는 영 퍼센트라는 목표를 부여합니다.',
'그런데 레이블 스무딩은 이를 고양이 구십 퍼센트, 강아지 오 퍼센트, 자동차 오 퍼센트로 바꿉니다.',
'왜 정확한 정답을 일부러 흐리게 만드는 걸까요?',
'세 클래스의 예측 확률을 생각해 보겠습니다. 세 확률의 합은 언제나 일이므로, 가능한 모든 확률분포는 하나의 삼각형 안에 나타낼 수 있습니다.',
'삼각형의 꼭짓점은 한 종류를 백 퍼센트 확신하는 상태입니다.',
'일반적인 분류 학습에서는 이 꼭짓점을 목표로 삼습니다. 그런데 소프트맥스는 유한한 값으로 정확히 백 퍼센트를 만들 수 없습니다.',
'구십구 퍼센트에 도달해도, 목표는 여전히 조금 더 멀리 있습니다.',
'레이블 스무딩은 이 목표를 삼각형 내부로 옮깁니다.',
'그런데 이를 손실 함수로 표현하면 더욱 흥미로운 사실이 나타납니다.',
'원래 정답을 향해 학습하는 손실에, 예측 확률이 균등분포에서 지나치게 멀어지는 것을 억제하는 항이 더해지는 것입니다.',
'하나는 정답에 확률을 집중시키고, 다른 하나는 그 집중이 지나치게 커지는 것을 억제합니다.',
'이 두 목표의 균형이 새로운 목표 확률분포를 만드는 것입니다.',
'실제로 이러한 변화는 일반화 성능뿐 아니라 예측 확률의 신뢰도와 신경망 내부의 특징 표현에도 영향을 줄 수 있습니다.',
'처음에는 정답을 일부러 틀리게 가르치는 것처럼 보였습니다.',
'하지만 레이블 스무딩이 바꾸는 것은 정답 자체가 아니라, 신경망이 학습해야 하는 확률분포입니다.',
'정답을 향해 학습시키는 동시에, 그 정답에 대한 확신이 지나치게 커지는 것을 억제하는 것.',
'이것이 레이블 스무딩의 수학적 원리입니다.'
]
def display(s):
    for a,b in [('레이블 스무딩','Label Smoothing'),('소프트맥스','Softmax'),('구십구 퍼센트','99%'),('구십 퍼센트','90%'),('백 퍼센트','100%'),('영 퍼센트','0%'),('오 퍼센트','5%'),('언제나 일이므로','언제나 1이므로')]:
        s=s.replace(a,b)
    return s
segments=[dict(start=a,end=b,text=display(s)) for a,b,s in zip([0]+ENDS[:-1],ENDS,TEXT)]
(ROOT/'timing.json').write_text(json.dumps(dict(duration_seconds=96,basis='user-provided cumulative utterance end times; audio not supplied',sentence_end_seconds=ENDS,segments=segments),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'tts_script.txt').write_text('\n\n'.join(TEXT)+'\n',encoding='utf-8')
(ROOT/'narration.md').write_text('# 신경망의 역설 02 — AI는 정답을 틀리게 가르쳐야 더 잘 배운다\n\n사용자 확정 대본 · 19구간 · 총 96초 · TTS 음원 미제공\n\n'+'\n\n'.join(f'## {s["start"]}–{s["end"]}초\n\n{s["text"]}' for s in segments)+'\n',encoding='utf-8')
def stamp(n):return f'00:{n//60:02}:{n%60:02},000'
(ROOT/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(segments,1))+'\n',encoding='utf-8')
