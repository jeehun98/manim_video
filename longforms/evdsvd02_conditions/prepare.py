"""Approved episode 02 narration and user storyboard timing, including 91/92 correction."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LINES=[
('행렬 분해 이상형 월드컵!',1),('EVD 대 SVD.',3),('대결 기준, 분해 조건입니다.',5),
('먼저 EVD. 고유값 분해입니다.',7),('EVD는 어떤 행렬이든 분해할 수 있을까요?',10),
('첫 번째 조건. 정사각행렬이어야 합니다.',13),
('고유벡터는 행렬을 적용한 결과가 원래 벡터의 스칼라배가 되는 벡터입니다.',18),
('입력과 출력의 차원이 같아야 하므로, 일반적인 고유값 분해는 정사각행렬을 대상으로 합니다.',23),
('하지만 정사각행렬이라고 모두 분해할 수 있는 것은 아닙니다.',27),
('두 번째 조건. 선형독립인 고유벡터가 충분해야 합니다.',31),
('이 행렬을 보겠습니다.',32),
('고윳값은 1이 두 번 등장하지만, 선형독립인 고유벡터는 하나뿐입니다.',37),
('두 개의 독립적인 고유벡터로 기저를 만들 수 없으므로 대각화가 불가능합니다.',42),
('세 번째로, 어떤 수 체계에서 분해하는지도 중요합니다.',45),
('90도 회전행렬은 모든 실수 벡터의 방향을 바꿉니다.',49),
('실수 고유벡터는 존재하지 않지만, 복소수까지 허용하면 고윳값과 고유벡터를 구해 대각화할 수 있습니다.',55),
('그렇다면 SVD는 어떨까요?',58),
('특이값 분해는 정사각행렬뿐 아니라 직사각행렬에도 적용할 수 있습니다.',63),
('선형독립인 고유벡터가 부족하거나, 실수 고유벡터가 없는 행렬도 문제없습니다.',68),
('그 이유는 SVD가 원래 행렬 대신, 전치행렬을 곱해 만든 대칭행렬의 고유벡터를 이용하기 때문입니다.',75),
('이 대칭행렬은 항상 직교하는 고유벡터 기저를 가질 수 있습니다.',79),
('따라서 모든 실수 행렬에는 SVD가 존재합니다.',82),
('그렇다면 분해 조건 대결의 승자는?',84),('SVD!',85),
('분해 가능한 행렬의 범위에서 압도적으로 유리하기 때문입니다.',89),
('현재 스코어, EVD 1 대 SVD 1.',91),('동점입니다!',92)]
SCENES=[
('01_open',0,3,'ConditionsOpen','행렬 분해 이상형 월드컵','후보와 시작 점수 1:0 소개'),
('02_criterion',3,5,'ConditionsCriterion','대결 기준 · 분해 조건','정사각, 직사각, 결손 행렬을 질문으로 제시'),
('03_evd',5,10,'ConditionsEVD','EVD · 고유값 분해','여기서 EVD는 A=PDP⁻¹ 대각화 형태다'),
('04_square',10,13,'ConditionsSquare','조건 1 · 정사각행렬','2×2 체크는 형태 조건만 통과, EVD 확정 아님'),
('05_dimensions',13,23,'ConditionsDimensions','왜 정사각행렬이어야 할까?','고유벡터 v≠0. Av와 λv가 같은 벡터공간에 속해야 한다'),
('06_basis',23,31,'ConditionsBasis','조건 2 · 충분한 고유벡터','n×n 행렬에 선형독립인 고유벡터 n개가 필요'),
('07_shear',31,42,'ConditionsShear','고윳값 두 개 ≠ 독립 방향 두 개','전단 A=[[1,1],[0,1]], 고윳값 1(중복도2), 고유공간 span((1,0))'),
('08_field',42,45,'ConditionsField','조건 3 · 수 체계','실수 대각화와 복소수 대각화를 구분'),
('09_rotation',45,49,'ConditionsRotation','90° 회전행렬','R=[[0,-1],[1,0]]. 0이 아닌 모든 실수 벡터가 직선을 벗어남'),
('10_complex',49,55,'ConditionsComplex','복소수에서는 대각화 가능','고윳값 ±i. 복소 고유벡터는 실수 평면의 화살표로 표시하지 않음'),
('11_svd',55,58,'ConditionsSVD','SVD · 특이값 분해','같은 행렬을 SVD로 심사'),
('12_rectangular',58,63,'ConditionsRectangular','직사각행렬도 가능','B=[[1,0,0],[0,2,0]], 특이값 2,1. 세 번째 입력축은 영공간이며 0 특이값을 추가로 세지 않음'),
('13_pass',63,68,'ConditionsPass','같은 행렬, 다른 분해 조건','전단과 회전행렬 모두 실수 SVD 가능'),
('14_gram',68,75,'ConditionsGram','AᵀA는 항상 대칭','전단 AᵀA=[[1,1],[1,2]]. 존재성의 원리, 실제 알고리즘의 직접 형성을 요구하지 않음'),
('15_orthogonal',75,79,'ConditionsOrthogonal','항상 직교 고유기저를 선택 가능','np.linalg.eigh로 실제 AᵀA 고유벡터를 계산. 양의 준정부호도 표시'),
('16_exists',79,82,'ConditionsExists','모든 실수 행렬에 SVD 존재','직사각, 전단, 회전 사례 모두 통과. 비영 특이벡터 대응 후 영공간 기저 보완'),
('17_verdict',82,89,'ConditionsVerdict','분해 조건의 승자 · SVD','84초 공개. 우위는 분해 가능한 행렬 범위에 한정'),
('18_score',89,92,'ConditionsScore','현재 스코어 · 동점','89–91초 점수 1:1, 91–92초 동점. 마지막 0.5초 유지')]

def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    cues=[];start=0
    for caption,end in LINES:cues.append(dict(start=start,end=end,caption=caption));start=end
    (ROOT/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'timing_source.md').write_text('# 시각 확인\n\n사용자 메시지 마지막 두 종료 시각 81,82는 89초보다 앞선다. 첨부 storyboard.md가 이를 명시적으로 91,92초로 해석하므로 해당 콘티를 적용한다. 전체 92초. 나머지 25개 종료 시각과 내레이션 원문 변경 없음. 음원 미제공.\n',encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    script='\n\n'.join(' '.join(c['caption'] for c in cues if a<=c['start']<b) for _,a,b,*_ in SCENES)+'\n'
    (ROOT/'master_script.md').write_text('# 행렬 분해 이상형 월드컵 ② — 분해 조건\n\n사용자 확정 원문 · 첨부 콘티 기준 92초\n\n'+script,encoding='utf-8')
    (ROOT/'narration.md').write_text('\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues),encoding='utf-8')
    (ROOT/'tts_script.txt').write_text(script.replace('EVD','이 브이 디').replace('SVD','에스 브이 디'),encoding='utf-8')
    manifest=[]
    for directory,a,b,cls,title,claim in SCENES:
        folder=ROOT/'scenes'/directory;folder.mkdir(parents=True,exist_ok=True)
        words=' '.join(c['caption'] for c in cues if a<=c['start']<b)
        (folder/'script.txt').write_text(words.replace('EVD','이 브이 디').replace('SVD','에스 브이 디')+'\n',encoding='utf-8')
        (folder/'spec.md').write_text(f'# {title}\n\n## 목적·핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n동일한 대결 UI와 점수. 독립 씬으로 앞 장면 없이도 렌더 가능.\n\n## TTS 원문과 확정 길이\n{words}\n\n{a}–{b}초, 길이 {b-a}초. 사용자 종료 시각, 마지막 91/92는 첨부 콘티의 명시적 해석.\n\n## 화면·시간대별 애니메이션\n첨부 콘티 SCENE {len(manifest)+1:02}를 따른다. 9:16은 중앙 실험, 16:9는 좌우 배치.\n시작에 제목과 수학 대상을 등장시키고 발화에 맞춰 변환·조건·결과를 표시한다. 정확한 로컬 시각은 visuals.py의 scene_{len(manifest)}에 명시한다.\n\n## 화면 텍스트\n{title}\n\n## 시작·종료 상태\n고정 비교 헤더 → 해당 조건과 결과가 남은 완성 화면.\n\n## 다음 장면 연결\n컷 연결. 별도 연결 내레이션, 이전 편 복습, 다음 편 예고 없음.\n\n## 수학적 조건과 과장 방지\n{claim}\nSVD 존재성 원리를 다루며 AᵀA 직접 형성을 실용 알고리즘으로 권장하지 않는다.\n',encoding='utf-8')
        (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ConditionsScene\nclass {cls}(ConditionsScene):\n    INDEX={len(manifest)}\n',encoding='utf-8')
        manifest.append(dict(id=directory[:2],directory='scenes/'+directory,start=a,end=b,duration_seconds=b-a,**{'class':cls},title=title))
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'scenes.yaml').write_text('title: EVD vs SVD — 분해 조건\nduration_seconds: 92\ntiming_source: user_sentence_ends_and_storyboard_correction\nlayouts: [shorts_1080x1920, longform_1920x1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    example=ROOT/'scenes/01_example'
    if example.exists():
        for name in ['script.txt','spec.md']:(example/name).unlink()
        example.rmdir()
if __name__=='__main__':main()
