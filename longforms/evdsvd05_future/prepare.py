"""User-approved narration and explicit sentence end times; no estimated clocks."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LINES=[
('행렬 분해 이상형 월드컵!',1),('EVD 대 SVD.',3),('대결 기준, 미래 예측입니다.',5),
('어떤 시스템의 현재 상태를 하나의 벡터로 표현해 보겠습니다.',8),
('시간이 한 단계 흐를 때마다 행렬 A에 의해 상태가 변한다고 가정하겠습니다.',13),
('다음 상태는 A 곱하기 X.',15),('그다음 상태는 A를 한 번 더 적용한 결과입니다.',18),
('같은 변화가 반복된다면, 우리는 이 시스템의 미래를 어떻게 예측할 수 있을까요?',23),
('먼저 서로 다른 두 방향의 상태 변화를 살펴보겠습니다.',26),
('한 방향의 벡터는 시간이 지날수록 길어지고, 다른 방향의 벡터는 점점 짧아집니다.',32),
('그런데 두 방향 모두 변환 후에도 원래 직선 위에 남습니다.',36),('바로 고유벡터입니다.',37),
('각 고유벡터는 행렬 A를 적용할 때마다 고윳값만큼 배율이 바뀝니다.',42),
('고윳값이 2라면 한 번 적용할 때 2배, 두 번이면 4배, 세 번이면 8배가 됩니다.',47),
('반대로 고윳값이 0.5라면 반복할수록 해당 성분은 0에 가까워집니다.',52),
('이제 임의의 입력 벡터를 두 고유방향의 성분으로 나누어 보겠습니다.',57),
('각 성분은 서로 다른 배율로 변화하고, 시간이 흐르면서 전체 벡터의 길이와 방향도 달라집니다.',62),
('EVD는 바로 이 과정을 간결하게 표현합니다.',65),('A가 대각화 가능하다면, A는 P, D, P 역행렬의 곱입니다.',69),
('그리고 같은 행렬을 N번 반복하면, 가운데 기저 변환들이 서로 상쇄됩니다.',74),
('결국 A의 N제곱은 P, D의 N제곱, P 역행렬의 곱이 됩니다.',78),
('즉, 고윳값을 각각 N제곱하는 것으로 반복 변환을 계산할 수 있습니다.',83),
('그렇다면 SVD는 어떨까요?',85),
('SVD의 특이값은 한 번의 변환에서 벡터의 길이가 얼마나 늘어나거나 줄어드는지를 알려줍니다.',92),
('하지만 첫 번째 변환에서 가장 크게 늘어난 벡터가, 다음 변환에서도 가장 크게 늘어나는 방향을 향하는 것은 아닙니다.',98),
('따라서 A의 특이값을 단순히 N제곱한다고 해서, 일반적으로 A의 N제곱의 특이값을 얻을 수는 없습니다.',105),
('EVD는 반복 변환에서 각 고유성분이 어떻게 변화하는지를 직접 보여줍니다.',110),
('물론 모든 행렬이 대각화 가능한 것은 아니며, 고윳값만으로 모든 과도 현상을 설명할 수도 없습니다.',116),
('그렇다면 미래 예측 대결의 승자는?',118),('EVD!',119),
('대각화 가능한 행렬에서 반복되는 변화를 고윳값의 거듭제곱으로 표현할 수 있다는 점에 한 표를 주겠습니다.',126),
('현재 스코어, EVD 3 대 SVD 2.',128),('EVD가 다시 앞서갑니다!',130)]
SCENES=[
('open',0,5,'대결 기준 · 미래 예측','현재 스코어 2:2. 질문만 제시.'),
('state',5,13,'상태와 변화 규칙','A_E=diag(2,0.5), x₀=(0.25,1). 현재 상태 t=0 표시.'),
('steps',13,23,'같은 변화를 반복하면?','실제 A_E 거듭제곱으로 t=0..3 궤적. 미래 t=10,100은 질문으로만 표시.'),
('directions',23,32,'늘어나는 방향 · 줄어드는 방향','두 축 위의 고유벡터가 매 단계 2배와0.5배. 동일한 단위 척도 유지.'),
('eigenvectors',32,42,'같은 직선 위에 남는다','고유직선 점선과 Avᵢ=λᵢvᵢ. λ₁=2, λ₂=0.5.'),
('growth',42,47,'고윳값 2 → 2ⁿ','1→2→4→8. 전 구간 고정 확대 축척을 표시, 프레임 이탈 방지.'),
('decay',47,52,'고윳값 0.5 → 0.5ⁿ','1→0.5→0.25→0.125. 유한 단계의 벡터를 0으로 지우지 않는다.'),
('components',52,57,'고유성분으로 나누면','x₀=(0.25,1)을 수평·수직 성분의 합으로 표시.'),
('trajectory',57,62,'성분마다 다른 미래','x_t=(0.25·2ᵗ,0.5ᵗ). 실제 합과 끝점 궤적.'),
('evd',62,69,'A = PDP⁻¹','일반식과 예시를 구분. 이 예시는 P=I, D=A_E.'),
('cancel',69,74,'중간의 기저 변환이 상쇄','(PDP⁻¹)(PDP⁻¹)에서 P⁻¹P=I만 강조 후 PD²P⁻¹.'),
('powers',74,83,'Aⁿ = PDⁿP⁻¹','대각화 가능 조건 표시. D의 대각 원소만 n제곱.'),
('svd',83,92,'SVD · 한 번의 길이 변화','별도 예시 B, A_S=[[0,-1],[2,0]]로 명확히 전환. 원→세로 타원. e₁→2e₂.'),
('twosteps',92,98,'첫 최대 확대 ≠ 매번 최대 확대','같은 A_S로 e₁→2e₂→-2e₁. 첫 배율2, 둘째1.'),
('mismatch',98,105,'특이값의 제곱과 다르다','σmax(A_S)=2, 단순 제곱4와 σmax(A_S²)=2 비교. A_S²=-2I.'),
('structure',105,110,'고유성분의 반복 변화를 드러낸다','예시 A로 전환 표시. 성장·감소와 일반 거듭제곱 식.'),
('limits',110,116,'대각화와 과도 현상의 한계','독립 고유방향 하나인 전단과 B=[[0.8,2],[0,0.7]]의 실제 ‖Bⁿe₂‖ 그래프. 별도 예시 명시.'),
('verdict',116,126,'ROUND 05 · EVD 승','118초 승자,119초 판정이유. 대각화 가능한 행렬 조건 유지.'),
('score',126,130,'EVD 3 : 2 SVD','126초부터 스코어 갱신,128초 리드 문구. 예고 없음.')]
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    cues=[];start=0
    for caption,end in LINES:
        assert end>start;cues.append(dict(start=start,end=end,caption=caption));start=end
    assert start==130
    (ROOT/'project.json').write_text(json.dumps(dict(duration=130,ending_confirmed=True,timing_source='user_sentence_end_times',pending=[]),indent=2),encoding='utf-8')
    (ROOT/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    full='\n\n'.join(' '.join(c['caption'] for c in cues if a<=c['start']<b) for _,a,b,*_ in SCENES)
    (ROOT/'master_script.md').write_text('# 5편 확정 대본 — 미래 예측\n\n사용자 원문과 문장 종료 시각 그대로. 총130초.\n\n'+full+'\n',encoding='utf-8')
    (ROOT/'narration.md').write_text('\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues)+'\n',encoding='utf-8')
    (ROOT/'tts_script.txt').write_text(full.replace('EVD','이 브이 디').replace('SVD','에스 브이 디').replace('A','에이').replace('X','엑스').replace('N','엔')+'\n',encoding='utf-8')
    manifest=[]
    for i,(slug,a,b,title,claim) in enumerate(SCENES):
        directory=f'scenes/{i+1:02}_{slug}';folder=ROOT/directory;folder.mkdir(parents=True,exist_ok=True)
        cls=f'Future{i+1:02}';words=' '.join(c['caption'] for c in cues if a<=c['start']<b)
        (folder/'script.txt').write_text(words+'\n',encoding='utf-8')
        (folder/'spec.md').write_text(f'# {title}\n\n## 목적·주장\n{claim}\n\n## 앞 장면에서 받은 내용\n현재 예시 행렬과 색 유지. 별도 행렬로 변경할 때 화면에 명시.\n\n## TTS 원문·확정 길이\n{words}\n\n{a}–{b}초, {b-a}초. 사용자 제공 문장 종료 시각.\n\n## 화면 구성·애니메이션\n{claim}\n9:16·16:9 각각 원본 배치. 실제 좌표·행렬 연산으로 계산.\n\n## 화면 텍스트\n{title}\n\n## 시작·종료 및 연결\n한 주장씩 완결. 궤적은 이전 끝점만 남기고, 같은 예시는 동일한 축척 사용.\n\n## 수학적 조건·과장 방지\nAⁿ=PDⁿP⁻¹는 대각화 가능할 때. 일반적인 특이값은 거듭제곱 법칙을 만족하지 않으나 특수한 행렬에서는 성립할 수 있다.\n',encoding='utf-8')
        (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import FutureScene\nclass {cls}(FutureScene):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=directory,start=a,end=b,duration_seconds=b-a,**{'class':cls},title=title))
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'scenes.yaml').write_text('title: EVD vs SVD — 미래 예측\nduration_seconds: 130\nlayouts: [9:16,16:9]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
if __name__=='__main__':main()
