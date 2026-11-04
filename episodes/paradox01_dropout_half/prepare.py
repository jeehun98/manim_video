"""Generate narration artifacts from the user-approved text and boundaries."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENDS = [5,11,20,24,30,35,42,46,53,58,60,66,72,78,82,89,98]
TEXT = [
'신경망을 더 잘 학습시키기 위해 뉴런을 제거한다면, 얼마나 제거하는 것이 좋을까요?',
'놀랍게도 Dropout에서는 뉴런의 절반, 무려 50%를 제거하는 설정이 효과적일 수 있습니다.',
'Dropout은 학습할 때 뉴런의 출력을 무작위로 0으로 만드는 방법입니다. 매번 다른 뉴런이 제거되기 때문에, 신경망은 특정 뉴런에만 의존하기 어려워집니다.',
'그런데 여기에는 조금 더 흥미로운 수학적 원리가 숨어 있습니다.',
'뉴런이 8개라면, 각각을 켜거나 끄는 조합은 무려 256가지입니다.',
'Dropout은 매번 이 조합 중 하나를 선택하고, 그 상태에서 발생하는 손실을 줄이도록 학습합니다.',
'즉, 하나의 고정된 신경망이 아니라, 무작위로 만들어지는 수많은 부분 신경망의 평균 손실을 줄이는 것입니다.',
'더 흥미로운 것은 이 과정이 정규화 효과를 만든다는 점입니다.',
'단순한 선형 모델에서 Dropout을 적용한 평균 제곱오차를 계산하면, 원래 손실에 추가적인 벌점 항이 생깁니다.',
'특정 뉴런의 기여가 지나치게 커질수록 더 큰 벌점을 받는 구조입니다.',
'그렇다면 제거율은 왜 50%일까요?',
'각 뉴런이 제거될 확률을 r이라고 하면, 마스크의 분산은 r 곱하기 1 마이너스 r입니다.',
'이 값은 정확히 50%에서 최대가 됩니다. 뉴런이 살아남을지 사라질지 가장 불확실해지는 지점입니다.',
'이때 8개 뉴런으로 만들 수 있는 256가지 마스크는 모두 같은 확률로 선택됩니다.',
'어떤 뉴런 조합도 다른 조합보다 특별히 자주 선택되지 않는 것입니다.',
'실제로 초기 Dropout 연구에서도 은닉 뉴런을 절반씩 제거하는 설정이 효과적인 기본값으로 사용됐습니다.',
'뉴런의 절반을 제거하는 50%. 이 비율이 수학적으로 특별한 이유는, 가능한 모든 뉴런 조합이 가장 균등한 확률로 선택되는 지점이기 때문입니다.'
]
segments = [dict(start=start,end=end,text=text) for start,end,text in zip([0]+ENDS[:-1],ENDS,TEXT)]
data = dict(duration_seconds=98,basis='user-provided cumulative utterance end times; audio not supplied',sentence_end_seconds=ENDS,scene_end_seconds=[11,20,30,42,58,72,82,98],segments=segments)
(ROOT/'timing.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
title = '신경망의 역설 01 — Dropout 50%가 수학적으로 특별한 이유'
(ROOT/'narration.md').write_text('# '+title+'\n\n사용자 제공 대본 · 문장 종료 시각 확정 · 총 98초 · 음원 미제공\n\n'+'\n\n'.join(f'## {s["start"]}–{s["end"]}초\n\n{s["text"]}' for s in segments)+'\n',encoding='utf-8')
tts = []
for text in TEXT:
    for a,b in [('Dropout','드롭아웃'),('50%','오십 퍼센트'),('256','이백오십육'),('8개','여덟 개'),('0','영'),('r','알'),('1','일')]:
        text=text.replace(a,b)
    tts.append(text)
(ROOT/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
def stamp(n):
    return f'{n//3600:02}:{n//60%60:02}:{n%60:02},000'
(ROOT/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(segments,1))+'\n',encoding='utf-8')
