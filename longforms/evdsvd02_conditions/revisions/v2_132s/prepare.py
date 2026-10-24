"""Save the user-approved 132-second revision, preserving original narration."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LINES=[
('행렬 분해 이상형 월드컵!',1),('EVD 대 SVD.',3),('대결 기준, 분해 조건입니다.',5),
('먼저 EVD. 고유값 분해입니다.',7),('EVD는 어떤 행렬이든 분해할 수 있을까요?',10),
('첫 번째 조건. 정사각행렬이어야 합니다.',12),
('고유값 분해는 입력과 출력이 같은 공간에 있는 선형변환을 대상으로 합니다.',17),
('하지만 정사각행렬이라고 모두 분해할 수 있는 것은 아닙니다.',21),
('두 번째 조건. 선형독립인 고유벡터가 충분해야 합니다.',25),
('이 행렬을 보겠습니다.',26),
('2차원 행렬이지만, 고유벡터는 수평 방향에서만 찾을 수 있습니다.',30),
('새로운 좌표계를 만들려면 서로 독립적인 두 방향이 필요한데, 하나밖에 없는 것이죠.',35),
('따라서 이 행렬은 대각화할 수 없습니다.',38),
('그런데 고유벡터를 찾을 때, 어떤 수를 허용하는지도 중요합니다.',42),
('90도 회전행렬을 생각해 보겠습니다.',44),
('어떤 0이 아닌 실수 벡터도 회전 후에는 원래 직선 위에 남지 않습니다.',48),
('따라서 실수 범위에서는 고유벡터를 찾을 수 없습니다.',52),
('하지만 고윳값을 계산하면, 두 해는 허수 i와 마이너스 i로 나타납니다.',57),
('복소수까지 허용하면 서로 독립적인 고유벡터를 구할 수 있고, 대각화도 가능해집니다.',62),
('즉, 같은 행렬이라도 실수에서 분해하는지, 복소수에서 분해하는지에 따라 결과가 달라질 수 있습니다.',68),
('그렇다면 SVD는 어떨까요?',70),
('특이값 분해는 정사각행렬뿐 아니라 직사각행렬에도 적용할 수 있습니다.',76),
('이 직사각행렬을 보겠습니다.',77),
('각 열벡터는 입력의 좌표축이 변환 후 어디로 향하는지를 나타냅니다.',82),
('여기에 전치행렬을 곱하면, 새로운 정사각행렬이 만들어집니다.',86),
('그런데 이 행렬의 원소들을 살펴보면 흥미로운 사실이 있습니다.',90),
('대각 원소는 각 열벡터의 길이 제곱입니다.',93),
('비대각 원소는 서로 다른 두 열벡터의 내적입니다.',96),
('즉, 원래 행렬이 입력 방향들의 길이와 상대적인 방향을 어떻게 변화시키는지에 관한 정보가 담겨 있습니다.',103),
('또한 내적의 대칭성 때문에 이 행렬은 항상 대칭행렬이 됩니다.',107),
('대칭행렬에서는 직교하는 고유벡터들로 기저를 만들 수 있습니다.',111),
('따라서 원래 행렬의 고유벡터가 부족하더라도 SVD를 구성할 수 있습니다.',117),
('결국 모든 실수 행렬에는 SVD가 존재합니다.',120),
('그렇다면 분해 조건 대결의 승자는?',123),('SVD!',124),
('분해 가능한 행렬의 범위에서 압도적으로 유리하기 때문입니다.',127),
('현재 스코어, EVD 1 대 SVD 1.',131),('동점입니다!',132)]
SCENES=[
('01_open',0,5,'RevisionOpen','ROUND 02 · 분해 조건','1초 후보, 3초 대결 기준, 점수 1:0'),
('02_evd',5,10,'RevisionEVD','EVD · 고유값 분해','EVD는 대각화 A=PDP⁻¹를 의미'),
('03_square',10,17,'RevisionSquare','조건 1 · 정사각행렬','10–12초 조건, 12–15초 차원 비교, 15–17초 Av=λv'),
('04_basis',17,25,'RevisionBasis','조건 2 · 독립적인 고유벡터','17–21초 정사각형≠대각화, 21–25초 독립 방향의 개념도'),
('05_shear',25,30,'RevisionShear','수평 방향만 고유벡터','A=[[1,1],[0,1]]. 26초 수평, 28초 일반 벡터 변환'),
('06_failure',30,38,'RevisionFailure','하나의 직선으로 기저를 만들 수 없다','P=[[1,2],[0,0]], detP=0. 모든 고유벡터 선택에 대해 가역 P 불가'),
('07_field',38,42,'RevisionField','어떤 수를 허용할까?','실수·복소수 수 체계 비교, 복소수 벡터의 실수 평면 화살표 표현 금지'),
('08_rotation',42,52,'RevisionRotation','90° 회전 · 실수 고유벡터 없음','R=[[0,-1],[1,0]], 0이 아닌 여러 벡터를 실제 90도 회전'),
('09_complex',52,62,'RevisionComplex','복소수에서는 대각화 가능','±i, v1=(1,-i), v2=(1,i), detP=2i≠0'),
('10_same_matrix',62,68,'RevisionSameMatrix','같은 행렬 · 다른 수 체계','동일한 R로 실수 대각화 불가/복소수 가능 비교'),
('11_svd',68,76,'RevisionSVD','SVD · 직사각행렬도 가능','68–70초 SVD, 70–73초 2×2, 73–76초 3×2'),
('12_columns',76,82,'RevisionColumns','행렬의 열 = 좌표축의 도착점','A=[[1,2],[2,0],[0,1]], Ae1=a1, Ae2=a2. 3D 공간 그림 대신 숫자와 색'),
('13_product',82,86,'RevisionProduct','AᵀA · 정사각행렬을 만든다','2×3 × 3×2 → 2×2. 결과는 숫자 대신 빈 칸'),
('14_entries',86,90,'RevisionEntries','각 칸은 열벡터의 내적','a1ᵀa1, a1ᵀa2, a2ᵀa1, a2ᵀa2. 수치 아직 미공개'),
('15_diagonal',90,93,'RevisionDiagonal','대각 원소 = 길이 제곱','1²+2²+0²=5, 2²+0²+1²=5. 대각 칸만 채움'),
('16_offdiagonal',93,96,'RevisionOffdiagonal','비대각 원소 = 두 열의 내적','1·2+2·0+0·1=2. 두 비대각 칸을 채움'),
('17_geometry',96,103,'RevisionGeometry','변환의 길이·내적 정보','기준 좌표축의 길이와 내적. 임의 입력은 ||Ax||²=xᵀAᵀAx로 조합'),
('18_symmetry',103,107,'RevisionSymmetry','내적의 대칭성 → 대칭행렬','a1ᵀa2=a2ᵀa1. 주대각선과 두 비대각 원소 연결'),
('19_orthogonal',107,111,'RevisionOrthogonal','직교 고유벡터로 기저 구성','G=[[5,2],[2,5]], (1,1)/√2와 (1,-1)/√2. 고윳값7,3'),
('20_shear_svd',111,117,'RevisionShearSVD','고유기저가 부족해도 SVD 가능','여기서 전단 A로 전환하며 G도 [[1,1],[1,2]]로 함께 교체. 실제 eigh 방향 사용'),
('21_exists',117,120,'RevisionExists','모든 실수 행렬에 SVD 존재','랭크 부족도 가능. 전체 증명이 아닌 존재성의 핵심 구조 설명'),
('22_verdict',120,127,'RevisionVerdict','분해 조건 대결 · SVD 승','123초 SVD 공개, 124–127초 적용 범위 판정 이유'),
('23_score',127,132,'RevisionScore','현재 스코어 · 1:1','129초 점수 증가, 131초 동점, 마지막 0.5초 유지')]

def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    cues=[];start=0
    for caption,end in LINES:cues.append(dict(start=start,end=end,caption=caption));start=end
    (ROOT/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    script='\n\n'.join(' '.join(c['caption'] for c in cues if a<=c['start']<b) for _,a,b,*_ in SCENES)+'\n'
    (ROOT/'master_script.md').write_text('# 2편 확정 수정 대본 · 132초\n\n사용자 원문·종료 시각 그대로. 이전 92초 타이밍 사용 안 함.\n\n'+script,encoding='utf-8')
    (ROOT/'narration.md').write_text('\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues),encoding='utf-8')
    tts=script.replace('EVD','이 브이 디').replace('SVD','에스 브이 디').replace('마이너스 i','마이너스 아이').replace('허수 i','허수 아이')
    (ROOT/'tts_script.txt').write_text(tts,encoding='utf-8')
    manifest=[]
    for directory,a,b,cls,title,claim in SCENES:
        folder=ROOT/'scenes'/directory;folder.mkdir(parents=True,exist_ok=True)
        words=' '.join(c['caption'] for c in cues if a<=c['start']<b)
        (folder/'script.txt').write_text(words.replace('EVD','이 브이 디').replace('SVD','에스 브이 디').replace('마이너스 i','마이너스 아이').replace('허수 i','허수 아이')+'\n',encoding='utf-8')
        (folder/'spec.md').write_text(f'# {title}\n\n## 목적·핵심 주장\n{claim}\n\n## 앞 장면\n대결 UI와 현재 사례를 받는다. 독립 렌더 시에도 원본 행렬을 함께 표시한다.\n\n## TTS 원문·길이\n{words}\n\n사용자 확정 {a}–{b}초, {b-a}초. 음원 미제공.\n\n## 화면·애니메이션\n첨부 콘티 SCENE {len(manifest)+1:02}. {claim}\n세로: 중앙 실험과 상하 설명. 가로: 왼쪽 설명·오른쪽 수학 대상.\n\n## 화면 텍스트\n{title}\n\n## 시작·종료 상태\n해당 수학 대상 등장 → 주장과 계산 결과를 남긴다.\n\n## 다음 장면 연결\n동일 사례를 유지한 컷 연결. 111초 전단 예시로 명시적 전환. 복습·다음 편 예고 없음.\n\n## 정확성\n{claim}\n고유벡터는 영벡터 제외. AᵀA는 실수 대칭·양의 준정부호. SVD 존재성은 랭크 부족도 포함하며 영공간 기저를 보완할 수 있다.\n',encoding='utf-8')
        (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import RevisedConditions\nclass {cls}(RevisedConditions):\n    INDEX={len(manifest)}\n',encoding='utf-8')
        manifest.append(dict(id=directory[:2],directory='scenes/'+directory,start=a,end=b,duration_seconds=b-a,**{'class':cls},title=title))
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'scenes.yaml').write_text('title: EVD vs SVD — 분해 조건 v2\nduration_seconds: 132\ntiming_source: user_revised_sentence_end_times\nlayouts: [shorts_1080x1920, longform_1920x1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    example=ROOT/'scenes/01_example'
    if example.exists():
        for name in ['script.txt','spec.md']:(example/name).unlink()
        example.rmdir()
if __name__=='__main__':main()
