"""Approved 149-second narration and independent scene specifications."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LINES=[
('행렬 분해 이상형 월드컵!',1),('EVD 대 SVD.',3),('대결 기준, 분해 구조입니다.',5),
('먼저 EVD. 고유값 분해입니다.',7),('EVD는 A를 P, D, P 역행렬의 곱으로 표현합니다.',10),
('왜 하나의 행렬 P와 그 역행렬을 사용할까요?',13),
('고유벡터에 A를 적용하면, 길이가 달라지거나 방향이 반전되더라도 원래 직선 위에 남습니다.',19),
('이것이 A 곱하기 V는 람다 곱하기 V라는 관계입니다.',23),
('선형독립인 고유벡터들을 기저로 모으면, 입력을 고유기저의 좌표로 바꾸고 각 성분에 고윳값을 곱할 수 있습니다.',30),
('그 결과를 원래 좌표계로 되돌리는 것이죠.',32),('이 과정이 P 역행렬, D, P의 역할입니다.',34),
('그런데 좌표를 바꾼다는 것은 무엇일까요?',37),
('행렬과 벡터의 곱에서는 각 행과 입력 벡터의 내적이 출력 성분을 만듭니다.',42),
('P 역행렬도 이러한 내적을 통해 고유기저의 좌표를 구합니다.',46),
('다만 고유벡터들은 일반적으로 직교하지 않으므로, 고유벡터 자체와의 내적만으로는 좌표를 구할 수 없습니다.',53),
('여기서 핵심은 EVD가 입력과 출력에서 같은 고유기저를 사용한다는 점입니다.',58),
('그렇다면 SVD는 어떨까요?',61),
('단위원에 행렬 A를 적용하면, 일반적인 가역 이차원 변환에서는 타원이 만들어집니다.',66),
('원 위의 입력 방향에 따라 출력의 길이와 방향이 달라집니다.',70),
('SVD는 그중 타원의 가장 긴 축에 대응하는 입력 방향을 찾아냅니다.',75),
('이것이 첫 번째 오른쪽 특이벡터, V 원입니다.',77),
('A를 적용한 결과의 단위방향은 왼쪽 특이벡터, U 원입니다.',82),
('입력 길이가 1이므로 출력 길이는 특이값, 시그마 원이 됩니다.',86),
('따라서 A 곱하기 V 원은 시그마 원 곱하기 U 원입니다.',89),
('그런데 임의의 단위벡터도 출력의 길이와 방향으로 표현할 수 있지 않을까요?',94),
('SVD의 특별함은 서로 직교하는 입력 특이방향들이, 변환 후에도 서로 직교하는 출력 방향들과 대응한다는 점입니다.',102),
('두 기저의 방향은 서로 달라도 괜찮습니다.',105),('이제 분해식을 보겠습니다.',106),
('V 전치의 각 행에는 입력 특이벡터가 들어 있습니다.',110),
('따라서 V 전치에 입력 벡터를 곱하면 각 특이벡터와의 내적을 계산합니다.',115),
('특이벡터들은 정규직교하므로, 이 내적값들이 곧 입력의 좌표 성분이 됩니다.',119),
('시그마는 각 성분의 크기를 변화시키고, U는 그 성분들을 출력 특이벡터 방향으로 조합합니다.',125),
('이것이 A는 U, 시그마, V 전치의 곱이라는 분해식입니다.',129),
('결국 EVD는 하나의 고유기저로 변환을 표현하고, SVD는 입력과 출력의 서로 다른 직교기저 사이에서 변환을 표현합니다.',137),
('그렇다면 분해 구조 대결의 승자는?',140),('EVD!',141),
('하나의 고유기저로 변환을 설명하는 구조적 간결함에 한 표를 주겠습니다.',145),
('현재 스코어, EVD 2 대 SVD 1.',148),('EVD가 다시 앞서갑니다!',149)]
SCENES=[
('01_open',0,5,'StructureOpen','ROUND 03 · 분해 구조','0–1초 타이틀,1–3초 후보,3–5초 기준. 시작 점수1:1'),
('02_evd',5,13,'StructureEVD','왜 P와 P⁻¹일까?','P와 P⁻¹은 같은 고유기저의 좌표 변환과 복원'),
('03_eigenline',13,23,'StructureEigenline','고유벡터는 원래 직선을 유지','A_E=[[2,1],[0,1]], p1=(1,0), Ap1=2p1. 음수 배율 반전은 별도 보조 예시'),
('04_coordinates',23,34,'StructureCoordinates','P⁻¹ → D → P','x=(2,-1). 좌표(1,1)→(2,1), 출력(3,-1). 좌표 변경 중 실제 벡터 고정'),
('05_rows',34,42,'StructureRows','행렬곱 = 행별 내적','각 행과 x의 내적은 스칼라 출력 성분. 값들을 모아 벡터 구성'),
('06_dual',42,53,'StructureDual','직접 내적과 기저 좌표는 다르다','P⁻¹x=(1,1), Pᵀx=(2,3). P가 정규직교가 아니므로 P⁻¹≠Pᵀ'),
('07_one_basis',53,58,'StructureOneBasis','EVD · 하나의 고유기저','입력·출력 모두 동일한 p1,p2. 좌표 배율만 D로 변경'),
('08_ellipse',58,66,'StructureEllipse','단위원 → 타원','A_S=[[0,-1],[3,0]], A(x,y)=(-y,3x). 단위원상은 세로 반축3, 가로1'),
('09_scan',66,70,'StructureScan','방향에 따라 길이·방향 변화','x(theta)=(cos,sin), Ax=(-sin,3cos), 실시간 길이는1~3'),
('10_right',70,77,'StructureRight','가장 긴 출력의 입력 방향 v₁','입력수평v1=(1,0), 출력수직Av1=(0,3). v1은 입력에 표시'),
('11_left',77,86,'StructureLeft','출력 단위방향 u₁ · 배율 σ₁','u1=(0,1), σ1=3. 단위 u1과 길이3 Av1을 구분'),
('12_pair',86,89,'StructurePair','Av₁ = σ₁u₁','방향과 크기의 대응을 원과 타원 위에 연결'),
('13_arbitrary',89,94,'StructureArbitrary','이 관계만으로 특별할까?','입력35도 일반단위벡터. 가역 예시이므로 Ax≠0, 크기×단위방향 분해 가능'),
('14_orthogonal',94,102,'StructureOrthogonal','입력도 직교 · 출력도 직교','v1=(1,0),v2=(0,1). u1=(0,1),u2=(-1,0). 두 쌍 동시 표시'),
('15_two_bases',102,105,'StructureTwoBases','입력 기저와 출력 기저는 달라도 된다','V=I, U=90도 회전. 두 기저는 각각 정규직교'),
('16_transition',105,106,'StructureTransition','방향들을 행렬로 모으면','1초 장면: 원·타원을 흐리게 하고 기저 방향들을 행렬 표기로 연결'),
('17_transpose',106,110,'StructureTranspose','V의 열 → Vᵀ의 행','이 예시는 V=I라 수치 불변. 기호와 색으로 열·행 이동을 먼저 표시'),
('18_dots',110,115,'StructureDots','Vᵀx · 각 행과 내적','x=(2,1), 내적값2,1. 아직 A의 최종 출력이 아닌 V기저 좌표'),
('19_orthonormal',115,119,'StructureOrthonormal','정규직교하므로 내적 = 좌표','VᵀV=I. 자기내적1, 교차내적0. EVD의 P⁻¹x와 대비'),
('20_combine',119,125,'StructureCombine','Σ 배율 → U 출력 조합','(2,1)→(6,1)→(-1,6). 6u1+u2를 실제 벡터 합으로 표현'),
('21_formula',125,129,'StructureFormula','A = UΣVᵀ','오른쪽부터 Vᵀ 좌표 추출 → Σ 배율 → U 출력 조합'),
('22_compare',129,137,'StructureCompare','하나의 고유기저 vs 두 직교기저','비교 기준은 기저의 재사용 구조. 두 분해 모두 적용 가능한 상황의 구조 비교'),
('23_verdict',137,145,'StructureVerdict','분해 구조 대결 · EVD 승','140초 EVD,141–145초 하나의 고유기저의 간결성에 대한 취향 판정'),
('24_score',145,149,'StructureScore','현재 스코어 · EVD 2:1 SVD','145–147초 점수 갱신,148초 최종 발화와 EVD리드 표시.149초 종료')]

def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    cues=[];start=0
    for caption,end in LINES:cues.append(dict(start=start,end=end,caption=caption));start=end
    (ROOT/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    script='\n\n'.join(' '.join(c['caption'] for c in cues if a<=c['start']<b) for _,a,b,*_ in SCENES)+'\n'
    (ROOT/'master_script.md').write_text('# 3편 확정 대본 · 분해 구조 · 149초\n\n사용자 원문과 종료 시각 그대로. EVD의 일반 벡터 V 발음은 화면 pᵢ 표기와 대응.\n\n'+script,encoding='utf-8')
    (ROOT/'narration.md').write_text('\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues),encoding='utf-8')
    tts=script.replace('EVD','이 브이 디').replace('SVD','에스 브이 디').replace('P','피').replace('D','디').replace('V','브이').replace('U','유').replace('A','에이')
    (ROOT/'tts_script.txt').write_text(tts,encoding='utf-8')
    manifest=[]
    for directory,a,b,cls,title,claim in SCENES:
        folder=ROOT/'scenes'/directory;folder.mkdir(parents=True,exist_ok=True)
        words=' '.join(c['caption'] for c in cues if a<=c['start']<b)
        (folder/'script.txt').write_text(words+'\n',encoding='utf-8')
        (folder/'spec.md').write_text(f'# {title}\n\n## 목적·핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n현재 예시와 공통 비교 UI. 각 씬에 예시 행렬 또는 명칭을 다시 명시한다.\n\n## TTS 원문·확정 길이\n{words}\n\n사용자 종료 시각 {a}–{b}초, {b-a}초. 음원 미제공.\n\n## 화면·시간대별 애니메이션\n첨부 콘티 SCENE {len(manifest)+1:02}. {claim}\n9:16 중앙·상하, 16:9 좌우 레이아웃을 별도 제작.\n\n## 화면 텍스트\n{title}\n\n## 시작·종료 상태\n예시 등장 → 해당 계산·대응을 설명하는 완성 화면.\n\n## 다음 장면 연결\n현재 예시 유지. 58초 A_E→A_S 전환을 명시. 별도 연결 내레이션·과거 편 복습·예고 없음.\n\n## 수학적 조건·과장 방지\n{claim}\nSVD 기하학은 가역 실수2×2 예시이며 축 길이와 단위벡터를 구분. 좌표 변경은 물리적 벡터 회전과 다르다. 승패는 구조적 간결성에 대한 취향 평가.\n',encoding='utf-8')
        (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import StructureScene\nclass {cls}(StructureScene):\n    INDEX={len(manifest)}\n',encoding='utf-8')
        manifest.append(dict(id=directory[:2],directory='scenes/'+directory,start=a,end=b,duration_seconds=b-a,**{'class':cls},title=title))
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'scenes.yaml').write_text('title: EVD vs SVD — 분해 구조\nduration_seconds: 149\ntiming_source: user_sentence_end_times\nlayouts: [shorts_1080x1920, longform_1920x1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    example=ROOT/'scenes/01_example'
    if example.exists():
        for name in ['script.txt','spec.md']:(example/name).unlink()
        example.rmdir()
if __name__=='__main__':main()
