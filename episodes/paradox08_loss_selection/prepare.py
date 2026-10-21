import json
from pathlib import Path
R=Path('episodes/paradox08_loss_selection')
ends=[4,11,16,22,28,34,41,48,51,55,62,70,76,83,86,93,98]
text='''신경망이 학습할 데이터를, 신경망 자신의 손실값으로 선택한다면 어떨까요?
2026년 발표된 한 연구에서는 이 방법으로 오히려 더 많은 사실을 정확하게 기억하는 신경망을 만들었습니다.
연구진이 주목한 것은 손실이 극단적으로 높거나 낮은 데이터였습니다.
손실이 매우 낮은 사실은 이미 여러 번 등장했거나, 쉽게 예측할 수 있는 정보일 수 있습니다.
반면 손실이 매우 높은 사실은 드물게 등장했거나, 모델이 기억하기 어려운 정보일 수 있습니다.
그렇다면 손실을 기준으로 데이터를 분류하고, 학습에 반영할 비중을 다르게 정하면 어떨까요?
연구진은 높은 손실의 사실을 학습 대상에서 제외하고, 매우 낮은 손실의 사실은 반복 학습되는 비중을 줄였습니다.
일종의 데이터베이스에서 조건에 따라 레코드를 걸러내듯, 신경망의 손실값을 이용해 학습할 사실을 선택하는 것입니다.
그런데 왜 이런 필터링이 기억 성능을 높일까요?
신경망에는 기억할 수 있는 정보량의 한계가 있습니다.
그리고 학습 과정은 각 사실을 몇 개 기억했는지가 아니라, 학습 데이터에서 발생한 손실을 줄이도록 진행됩니다.
따라서 이미 익숙한 사실을 지나치게 반복하거나, 용량을 넘어서는 수많은 어려운 사실을 모두 학습시키는 것이 반드시 효율적인 것은 아닙니다.
연구진은 손실을 이용해 학습할 사실의 수를 제한하고, 남겨진 사실들의 등장 빈도도 조절했습니다.
그 결과 같은 크기의 신경망이 기존보다 약 일 점 삼 배 많은 개체 관련 사실을 정확하게 기억했습니다.
중요한 것은 단순히 데이터를 줄였다는 사실이 아닙니다.
신경망 자신의 손실값으로 어떤 사실을 학습할지 선택하고, 그 선택이 다시 신경망의 기억 성능을 바꿨다는 것입니다.
더 많이 기억하기 위해, 신경망은 무엇을 배우지 않을지부터 결정합니다.'''.splitlines()
def display(s):return s.replace('일 점 삼 배','1.3배')
segments=[dict(start=a,end=b,text=display(s)) for a,b,s in zip([0]+ends[:-1],ends,text)]
(R/'timing.json').write_text(json.dumps(dict(duration_seconds=98,sentence_end_seconds=ends,basis='user-provided; no audio supplied',segments=segments),ensure_ascii=False,indent=2),encoding='utf-8')
(R/'tts_script.txt').write_text('\n\n'.join(text)+'\n',encoding='utf-8')
(R/'narration.md').write_text('# 신경망의 역설 08 — 무엇을 배우지 않을지 고르는 신경망\n\n17구간 · 98초 · 사용자 제공 종료 시각\n\n'+'\n\n'.join(f'## {s["start"]}–{s["end"]}초\n\n{s["text"]}' for s in segments),encoding='utf-8')
def stamp(n):return f'00:{n//60:02}:{n%60:02},000'
(R/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(segments,1))+'\n',encoding='utf-8')
