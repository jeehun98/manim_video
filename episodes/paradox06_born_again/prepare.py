"""The user's approved 25 paragraphs and cumulative utterance end times."""
import json
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ENDS=[5,8,14,18,21,26,28,32,40,46,51,53,58,62,67,73,79,83,91,97,103,108,112,117,121]
TEXT=[
'학생이 스승에게 배웠는데, 오히려 스승보다 더 뛰어난 실력을 갖게 된다면 어떨까요?',
'신경망에서도 이러한 청출어람이 발견되었습니다.',
'이미 학습된 신경망을 교사로 두고, 똑같은 구조와 크기의 새로운 신경망을 학생으로 학습시킵니다.',
'그런데 놀랍게도 이 학생이 교사보다 더 높은 정확도를 달성할 수 있습니다.',
'이것이 본 어게인 네트워크입니다.',
'왜 같은 크기의 신경망이 자신을 가르친 모델보다 더 좋은 결과를 얻을 수 있을까요?',
'고양이 사진 하나를 생각해 보겠습니다.',
'일반적인 학습에서는 정답이 고양이라는 사실만 알려줍니다.',
'하지만 교사 신경망은 고양이 칠십 퍼센트, 호랑이 이십 퍼센트, 자동차 십 퍼센트처럼 여러 클래스에 대한 예측 확률을 출력할 수 있습니다.',
'여기에는 정답 외에도, 교사가 다른 클래스들을 어떻게 판단했는지에 대한 정보가 담겨 있을 수 있습니다.',
'학생은 정답뿐 아니라 교사가 만들어낸 이 확률분포도 학습 신호로 활용할 수 있습니다.',
'이것이 지식 증류입니다.',
'그런데 학생이 교사의 판단을 그대로 복사하기만 한다면, 교사를 뛰어넘기는 어려울 것 같습니다.',
'하지만 학생은 교사의 가중치를 복사하지 않습니다.',
'새로운 초기값에서 출발해, 전달받은 확률분포를 목표로 자신만의 파라미터를 학습합니다.',
'수학적으로도 학생이 최소화하는 손실 함수는 교사가 처음 학습했던 손실 함수와 달라집니다.',
'정답만을 향해 학습하는 대신, 교사의 예측 확률까지 고려하도록 학습 목표가 바뀌는 것입니다.',
'여기서 중요한 것은 교사의 판단이 언제나 옳다는 뜻이 아닙니다.',
'교사가 각 문제를 얼마나 확신했는지, 정답이 아닌 클래스들에 어떤 확률을 부여했는지도 학생의 학습에 영향을 줄 수 있습니다.',
'이러한 변화는 학생이 교사와는 다른 해를 찾고, 때로는 더 좋은 일반화 성능을 얻도록 도울 수 있습니다.',
'실제로 본 어게인 네트워크 연구에서는 같은 크기의 학생이 교사를 뛰어넘는 결과가 보고되었습니다.',
'결국 학생이 물려받는 것은 교사의 파라미터도, 교사의 성능 한계도 아닙니다.',
'교사가 학습 과정에서 만들어낸 판단을 새로운 학습 신호로 활용하는 것입니다.',
'스승에게서 배운다는 것이, 반드시 스승과 같은 답에 머무른다는 뜻은 아닙니다.',
'이것이 신경망에서 발견된 청출어람의 역설입니다.'
]
def display(s):
    for a,b in [('본 어게인 네트워크','Born-Again Networks'),('칠십 퍼센트','70%'),('이십 퍼센트','20%'),('십 퍼센트','10%')]:s=s.replace(a,b)
    return s
segments=[dict(start=a,end=b,text=display(s)) for a,b,s in zip([0]+ENDS[:-1],ENDS,TEXT)]
(ROOT/'timing.json').write_text(json.dumps(dict(duration_seconds=121,basis='user-provided cumulative utterance end times; audio not supplied',sentence_end_seconds=ENDS,segments=segments),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'narration.md').write_text('# 신경망의 역설 06 — 신경망에서의 청출어람\n\n사용자 확정 대본 · 25구간 · 121초 · TTS 음원 미제공\n\n'+'\n\n'.join(f'## {s["start"]}–{s["end"]}초\n\n{s["text"]}' for s in segments)+'\n',encoding='utf-8')
(ROOT/'tts_script.txt').write_text('\n\n'.join(TEXT)+'\n',encoding='utf-8')
def stamp(n):return f'00:{n//60:02}:{n%60:02},000'
(ROOT/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(segments,1))+'\n',encoding='utf-8')
(ROOT/'assets').mkdir(exist_ok=True)
shutil.copy2(ROOT.parent/'paradox03_mixup_rules'/'assets'/'cat_photo.png',ROOT/'assets'/'cat_photo.png')
