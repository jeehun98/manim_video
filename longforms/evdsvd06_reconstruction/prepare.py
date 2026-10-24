"""Approved narration, explicit user sentence endpoints, independent scene specifications."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LINES=[
('행렬 분해 이상형 월드컵!',1),('EVD 대 SVD.',3),('대결 기준, 복원 정확도입니다.',5),
('하나의 행렬을 분해한 뒤, 다시 합치면 원래 행렬을 복원할 수 있습니다.',9),
('그런데 분해한 성분 중 일부를 버려야 한다면 어떨까요?',13),
('이번에는 같은 행렬을 EVD와 SVD로 각각 분해하고, 두 방법 모두 같은 개수의 성분만 남겨 보겠습니다.',19),
('어느 쪽이 원래 행렬을 더 정확하게 복원할까요?',22),('먼저 EVD입니다.',24),
('고유값 분해는 행렬을 여러 고유성분의 합으로 표현할 수 있습니다.',28),
('그렇다면 고윳값이 큰 성분부터 남기면 가장 좋은 복원이 가능할까요?',32),('반드시 그렇지는 않습니다.',34),
('EVD의 고유벡터들은 일반적으로 서로 직교하지 않습니다.',38),
('이 때문에 서로 다른 고유성분들이 일부 효과를 상쇄하면서 원래 행렬을 구성할 수 있습니다.',43),
('그런데 그중 하나를 제거하면, 이러한 상쇄 관계가 깨질 수 있습니다.',47),
('고윳값이 큰 성분을 남겼는데도, 복원한 행렬이 원래 행렬과 크게 달라질 수 있는 것이죠.',52),
('그렇다면 SVD는 어떨까요?',55),('특이값 분해 역시 행렬을 여러 성분의 합으로 표현합니다.',58),
('하지만 여기에는 중요한 차이가 있습니다.',61),
('SVD를 구성하는 랭크 1 성분들은 행렬의 원소들을 하나의 벡터처럼 펼쳐 생각했을 때 서로 직교합니다.',68),
('따라서 성분 하나를 제거하면, 그 성분에 해당하는 특이값의 제곱만큼 복원 오차의 제곱합이 증가합니다.',75),
('이 때문에 큰 특이값의 성분부터 남기는 것이 유리합니다.',79),
('더 나아가 SVD에서는 큰 특이값의 성분을 정해진 개수만큼 남기는 방법이, 같은 랭크 이하의 모든 근사 중 제곱 오차를 최소화합니다.',88),
('이것이 SVD의 최적 저랭크 근사 성질입니다.',91),
('실제로 같은 행렬을 열 개의 성분으로 분해하고, 각각 다섯 개만 남기는 예시를 살펴보겠습니다.',97),
('EVD에서 큰 고윳값의 성분 다섯 개를 남기면, 원래 행렬과의 오차가 상당히 크게 나타날 수 있습니다.',103),
('반면 SVD에서 큰 특이값의 성분 다섯 개를 남기면, 더 작은 오차로 복원할 수 있습니다.',109),
('물론 대칭행렬처럼 EVD도 같은 최적 근사를 얻을 수 있는 경우가 있습니다.',115),
('하지만 일반적인 행렬에서 이런 최적 복원을 보장하는 것은 SVD입니다.',119),
('그렇다면 복원 정확도 대결의 승자는?',122),('SVD!',123),
('같은 개수의 성분으로 원래 행렬을 가장 정확하게 근사할 수 있다는 점에 한 표를 주겠습니다.',128),
('현재 스코어, EVD 3 대 SVD 3.',131),('다시 동점입니다!',133)]
SCENES=[
('open',0,5,'ROUND 06 · 복원 정확도','스코어3:2. 질문 제시.'),
('recombine',5,9,'분해 → 합성 → 원본','같은 크기10×10의 실제 성분을 분리·합성. 이미지 조각으로 자르지 않음.'),
('discard',9,13,'성분 일부만 남긴다면?','실제 성분 카드10개 중5개 비활성화.'),
('fair',13,22,'같은 원본 · 같은 성분 수','A=diag(B,B,B,B,B), B=[[2,3],[0,1]]. 양쪽5/10, 복원은 물음표.'),
('evd',22,28,'EVD · 고유성분의 합','A=Σλᵢpᵢqᵢᵀ, qᵢᵀ는 P⁻¹의 행. 대각화 가능한 예시.'),
('choose',28,34,'큰 고윳값부터 남기면?','λ=2인5개와λ=1인5개. 앞5개를 선택하되 최적 보장은 아님.'),
('oblique',34,38,'고유벡터는 직교하지 않을 수 있다','B의 실제 고유벡터(1,0),(-3,1). 부호 바꾸지 않은 실제 방향.'),
('cancel',38,43,'같은 칸에서 효과가 상쇄','E1=[[2,6],[0,0]], E2=[[0,-3],[0,1]]. 6+(-3)=3. 실제2×2 격자 합성.'),
('break',43,47,'하나를 버리면 상쇄도 사라진다','음수기여 E2 제거. 같은 칸3→6. 고정색상 척도.'),
('evd_result',47,52,'큰 고윳값 ≠ 최적 복원 보장','같은10×10 A와E5 나란히. 실제 차이 칸 외곽선 강조.'),
('svd',52,58,'SVD · 랭크 1 성분의 합','A=Σσᵢuᵢvᵢᵀ. 블록별 고정SVD로10개 성분.'),
('orthogonal',58,68,'행렬을 펼쳤을 때의 직교','실제100원소 성분을 펼침. Frobenius 내적0. 2D축은 개념도임을 명시.'),
('error',68,75,'제거한 성분의 σ²만큼 오차 증가','실제작은특이값성분1개 제거: Δ‖오차‖²=σmin². 5개 제거의 합도 표시.'),
('large',75,79,'큰 특이값을 남기는 이유','실제특이값 큰5개,작은5개. 반대선택의 잔여오차와비교.'),
('optimal',79,88,'같은 랭크 이하에서 최소 오차','EVD5, 혼합5, SVD상위5 후보 실제Frobenius오차 막대. 후보샘플이 증명은 아님; 정리 문구 명시.'),
('best',88,91,'최적 저랭크 근사','Aₖ=Σ(i≤k)σᵢuᵢvᵢᵀ. 상위5개 성분 합성.'),
('experiment',91,97,'10개 중 5개 · 같은 실험','같은 원본 10×10에서 EVD와SVD.5/10.'),
('evd_actual',97,103,'EVD · 큰 고윳값 5개','실제합E5. 오차√50≈7.071. 블록오른쪽위6 강조.'),
('svd_actual',103,109,'SVD · 큰 특이값 5개','실제합S5. 오차약1.208. 동일척도로 결과 비교.'),
('symmetric',109,115,'대칭행렬에서는 같은 최적 근사도 가능','109–111실제오차비교,111–115대칭행렬단서. 절댓값큰고윳값기준 명시.'),
('guarantee',115,119,'일반적인 행렬에서의 최적 보장','EVD는일반보장없음,SVD는Frobenius오차최소.'),
('verdict',119,128,'ROUND 06 · SVD 승','122승자,123이유. 같은랭크이하·제곱오차조건.'),
('score',128,133,'EVD 3 : 3 SVD','128부터스코어갱신,131동점문구.복습·예고없음.')]
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    cues=[];start=0
    for caption,end in LINES:
        assert end>start;cues.append(dict(start=start,end=end,caption=caption));start=end
    assert start==133
    (ROOT/'project.json').write_text(json.dumps(dict(duration=133,ending_confirmed=True,timing_source='user_sentence_end_times',pending=[]),indent=2),encoding='utf-8')
    (ROOT/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    full='\n\n'.join(' '.join(c['caption'] for c in cues if a<=c['start']<b) for _,a,b,*_ in SCENES)
    (ROOT/'master_script.md').write_text('# 6편 확정 대본 — 복원 정확도\n\n사용자 원문·종료 시각. 총133초.\n\n'+full+'\n',encoding='utf-8')
    (ROOT/'narration.md').write_text('\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues)+'\n',encoding='utf-8')
    (ROOT/'tts_script.txt').write_text(full.replace('EVD','이 브이 디').replace('SVD','에스 브이 디')+'\n',encoding='utf-8')
    manifest=[]
    for i,(slug,a,b,title,claim) in enumerate(SCENES):
        directory=f'scenes/{i+1:02}_{slug}';folder=ROOT/directory;folder.mkdir(parents=True,exist_ok=True);cls=f'Reconstruction{i+1:02}'
        words=' '.join(c['caption'] for c in cues if a<=c['start']<b)
        (folder/'script.txt').write_text(words+'\n',encoding='utf-8')
        (folder/'spec.md').write_text(f'# {title}\n\n## 목적·주장\n{claim}\n\n## 앞 장면에서 받은 내용\n같은10×10 원본과고정색상척도. EVD파랑,SVD청록외곽선. 원소색은분해방법과무관.\n\n## TTS 원문·확정 길이\n{words}\n\n{a}–{b}초, {b-a}초. 사용자문장종료시각.\n\n## 화면 구성·시간별 애니메이션\n{claim}\n9:16과16:9 별도배치,visuals.py의scene_{i}가시각별동작정의.\n\n## 화면 텍스트\n{title}\n\n## 시작·종료·연결\n같은원본과성분수를유지하며현재주장을완결. 복습·예고없음.\n\n## 수학적 조건·과장 방지\nEVD는대각화가능. qᵢᵀ는P⁻¹의행. SVD최적성은rank≤k,Frobenius노름. 대칭행렬은고윳값절댓값순. 고차원직교는개념도구분. 모든격자는같은−6..6척도.\n',encoding='utf-8')
        (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ReconstructionScene\nclass {cls}(ReconstructionScene):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=directory,start=a,end=b,duration_seconds=b-a,**{'class':cls},title=title))
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'scenes.yaml').write_text('title: EVD vs SVD — 복원 정확도\nduration_seconds: 133\nlayouts: [9:16,16:9]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
if __name__=='__main__':main()
