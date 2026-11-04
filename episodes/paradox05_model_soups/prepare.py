"""The user's 25 narration paragraphs and cumulative end times."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ENDS=[5,11,15,20,24,29,37,39,43,47,53,58,61,67,71,76,80,83,89,95,101,104,108,112,118]
TEXT=[
'신경망을 학습한다는 것은, 수많은 파라미터 중에서 좋은 값을 찾아가는 과정입니다.',
'우리는 흔히 경사하강법이 손실 지형의 골짜기 아래에서 하나의 최솟값을 찾는다고 생각합니다.',
'그런데 좋은 해가 하나의 점이 아니라, 넓은 영역에 존재한다면 어떨까요?',
'같은 사전학습 신경망에서 출발해, 서로 다른 설정으로 두 모델을 학습했습니다.',
'두 모델 모두 좋은 성능을 보이지만, 최종 파라미터는 서로 다릅니다.',
'그렇다면 이 두 모델의 파라미터를 절반씩 평균내면 어떻게 될까요?',
'놀랍게도 이렇게 만들어진 모델이 별도의 추가 학습 없이도 좋은 성능을 보이고, 때로는 개별 모델보다 더 정확할 수 있습니다.',
'이것이 모델 수프입니다.',
'왜 단순히 가중치를 평균냈는데 좋은 모델이 만들어지는 걸까요?',
'파라미터 공간에서 두 모델을 각각 하나의 점으로 표현해 보겠습니다.',
'두 점 사이를 직선으로 연결하면, 그 위의 모든 점은 서로 다른 가중치를 가진 하나의 신경망이 됩니다.',
'보통은 두 모델이 모두 좋은 해라고 해도, 그 중간이 좋은 해라는 보장은 없습니다.',
'중간에 높은 손실의 장벽이 존재할 수도 있기 때문입니다.',
'하지만 같은 초기 모델에서 출발한 일부 파인튜닝 결과에서는 다른 현상이 나타납니다.',
'두 모델 사이의 직선 경로에서도 손실이 낮게 유지되는 것입니다.',
'마치 서로 떨어진 두 최솟값이 사실은 하나의 넓은 골짜기 안에 있는 것처럼 보입니다.',
'그렇다면 두 점의 중간에서도 좋은 해를 얻을 수 있습니다.',
'모델 수프는 이러한 기하학적 성질을 이용합니다.',
'여러 모델의 예측을 평균내는 대신, 파라미터 자체를 평균내 하나의 새로운 모델을 만드는 것입니다.',
'이 방법은 적절한 조건에서 추가적인 추론 비용 없이 일반화 성능을 개선할 수 있습니다.',
'물론 모든 신경망의 평균이 좋은 것은 아닙니다. 두 모델이 호환되는 낮은 손실 영역에 놓여 있는지가 중요합니다.',
'여기서 흥미로운 사실이 드러납니다.',
'경사하강법으로 찾아낸 각각의 해가 유일하게 좋은 지점일 필요는 없습니다.',
'그 해들 사이에도 좋은 성능을 유지하는 영역이 존재할 수 있습니다.',
'좋은 해는 고립된 하나의 점이 아니라, 파라미터 공간에 펼쳐진 영역일 수도 있는 것입니다.'
]
segments=[dict(start=a,end=b,text=s.replace('모델 수프','Model Soups')) for a,b,s in zip([0]+ENDS[:-1],ENDS,TEXT)]
(ROOT/'timing.json').write_text(json.dumps(dict(duration_seconds=118,basis='user-provided cumulative utterance end times; audio not supplied',sentence_end_seconds=ENDS,segments=segments),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'narration.md').write_text('# 신경망의 역설 05 — 좋은 해는 점이 아니라 영역이다?\n\n사용자 확정 대본 · 25구간 · 118초 · TTS 음원 미제공\n\n'+'\n\n'.join(f'## {s["start"]}–{s["end"]}초\n\n{s["text"]}' for s in segments)+'\n',encoding='utf-8')
(ROOT/'tts_script.txt').write_text('\n\n'.join(TEXT)+'\n',encoding='utf-8')
def stamp(n):return f'00:{n//60:02}:{n%60:02},000'
(ROOT/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(segments,1))+'\n',encoding='utf-8')
