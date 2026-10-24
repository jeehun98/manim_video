"""Approved revised narration, exact user clocks, and animation-first scene specs."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LINES=[
('행렬 분해 이상형 월드컵!',1),('EVD 대 SVD.',3),('대결 기준, 분해 구조입니다.',5),
('먼저 EVD. 고유값 분해입니다.',7),('EVD는 A를 P, D, P 역행렬의 곱으로 표현합니다.',11),
('왜 이런 구조가 만들어질까요?',12),('좌표평면에 두 고유벡터를 표시해 보겠습니다.',15),
('고유벡터에 행렬 A를 적용하면, 길이가 변하거나 방향이 반전되더라도 원래 직선 위에 남습니다.',22),
('이것이 A 곱하기 V는 람다 곱하기 V라는 관계입니다.',25),
('이제 두 고유벡터를 새로운 좌표축으로 사용해 보겠습니다.',29),
('입력 벡터를 이 좌표축의 성분으로 나누고, 각 성분에 고윳값을 곱합니다.',34),
('그리고 변환된 성분들을 원래 좌표계로 표현합니다.',37),
('이것이 P 역행렬, D, P가 수행하는 과정입니다.',40),
('여기서 고유기저의 두 축은 반드시 직교할 필요가 없습니다.',44),
('따라서 일반적으로 좌표를 변환할 때 고유벡터와의 내적만으로는 충분하지 않고, P 역행렬을 사용합니다.',50),
('중요한 것은 변환 전과 후에 같은 고유기저를 사용한다는 점입니다.',54),
('그렇다면 SVD는 어떨까요?',57),('이번에는 단위원에 행렬 A를 적용해 보겠습니다.',60),
('원 위의 벡터들이 변환되면서 타원이 만들어집니다.',63),
('그런데 원 위의 어떤 방향이 타원의 가장 긴 축으로 변환될까요?',67),
('SVD는 바로 그 입력 방향을 찾아냅니다.',70),
('이 방향을 첫 번째 오른쪽 특이벡터, V 원이라고 하겠습니다.',74),
('변환된 결과가 향하는 타원의 긴 축 방향은 첫 번째 왼쪽 특이벡터, U 원입니다.',80),
('입력 벡터의 길이는 1이고, 변환된 결과의 길이는 첫 번째 특이값, 시그마 원입니다.',85),
('따라서 A 곱하기 V 원은 시그마 원 곱하기 U 원입니다.',89),
('이제 입력 방향을 90도 돌려 보겠습니다.',91),
('두 번째 입력 특이방향은 타원의 짧은 축에 대응합니다.',95),
('여기서 중요한 특징이 나타납니다.',97),
('입력의 두 특이방향은 서로 직교하고, 변환된 출력 방향들도 서로 직교합니다.',102),
('하지만 입력과 출력의 기저는 서로 다른 방향을 향할 수 있습니다.',106),
('그렇다면 이 두 기저로 임의의 벡터를 어떻게 변환할까요?',109),
('입력 벡터를 두 특이방향으로 나누어 보겠습니다.',112),
('특이벡터들은 정규직교하므로, 각 방향으로의 내적이 바로 그 방향의 좌표 성분이 됩니다.',118),
('이것이 V 전치가 수행하는 역할입니다.',120),
('이제 시그마를 적용하면 각 성분의 길이가 달라집니다.',123),
('마지막으로 U를 적용하면, 이 성분들이 출력의 직교기저 방향으로 조합됩니다.',128),
('이 전체 과정이 A는 U, 시그마, V 전치의 곱이라는 분해식입니다.',133),
('결국 EVD는 하나의 고유기저로 변환을 표현하고,',136),
('SVD는 입력과 출력의 서로 다른 직교기저 사이에서 변환을 표현합니다.',141),
('그렇다면 분해 구조 대결의 승자는?',143),('EVD!',144),
('하나의 고유기저로 변환을 설명하는 구조적 간결함에 한 표를 주겠습니다.',149),
('현재 스코어, EVD 2 대 SVD 1.',152),('EVD가 다시 앞서갑니다!',153)]
SCENES=[
('01_open',0,5,'GraphOpen','ROUND 03 · 분해 구조','타이틀→후보→기준. 시작1:1. EVD 공통 좌표평면을 준비'),
('02_evd',5,12,'GraphEVD','A = PDP⁻¹','5–7초 EVD,7–11초 기호만 강조. 숫자 행렬 없음. 같은 좌표평면 유지'),
('03_eigenlines',12,25,'GraphEigenlines','Apᵢ = λᵢpᵢ','p1=(1,0),p2=(1,-1), A_E=[[2,1],[0,1]]. 두 고유직선 고정. p1배율2,p2배율1. 방향반전은 보조 설명만'),
('04_oblique',25,29,'GraphOblique','P⁻¹','직교격자→고유기저 격자. 입력x=(2,-1)는 고정. 숫자 좌표는 표시하지 않음'),
('05_evd_scale',29,40,'GraphEVDScale','P⁻¹ → D → P','29–31초성분 분리,31–34초수평성분배율2,34–37초표준좌표 복원,37–40초역할 정리'),
('06_projections',40,50,'GraphProjections','P⁻¹','고유축은 비직교. 독립 직교투영 합은 x와 다름을 회색으로, 올바른 평행사변형 분해는 파랑·보라로. 수치 비교 없음'),
('07_same_basis',50,54,'GraphSameBasis','하나의 고유기저','동일한 방향의 고유축 두 세트, 입력·출력 화살표만 다름'),
('08_morph',54,63,'GraphMorph','단위원 → 선형변환 → 타원','SVD 새 예시 A=R30 diag(2,1) R(-25). 48점 각각 (1-t)x+tAx로 이동. 중심좌표평면 하나'),
('09_scan',63,70,'GraphScan','어떤 입력 방향일까?','원·타원 분리 후 동일한 A로 대응하는 화살표를 회전. 입력25도에서 정지, 출력30도 장축. 각도·수치 표시 금지'),
('10_first_pair',70,89,'GraphFirstPair','Av₁ = σ₁u₁','v1 입력단위25도, u1 출력단위30도, 실제출력길이2. 단위방향과 실선출력 구분'),
('11_second_pair',89,95,'GraphSecondPair','두 번째 특이방향','v1 유지, 탐색 입력90도 회전. v2=115도, u2=120도. 실제 Av2=σ2u2, σ2=1'),
('12_two_bases',95,106,'GraphTwoBases','입력도 직교 · 출력도 직교','95–102초양쪽직각,102–106초윤곽제거 후 같은원점에 입력25/115와 출력30/120 겹침. 각도숫자 없음'),
('13_coordinates',106,120,'GraphCoordinates','Vᵀx','원·타원제거, 입력x=V(1.15,-.75) 고정. 부호있는 두 투영성분을 보여주고 머리·꼬리 합으로 x 복원'),
('14_sigma',120,123,'GraphSigma','Σ','같은 성분 유지. 첫 길이2배, 둘째유지, 특이기저상 방향유지. 이는 기저좌표상의 배율'),
('15_output',123,133,'GraphOutput','U → A=UΣVᵀ','입력축희미하게,출력축강조. 조정성분을 U방향으로 조합해 실제Ax. 128초 전체분해식. 내부 중간임베딩 VΣc→UΣc를 구분'),
('16_compare',133,141,'GraphCompare','하나의 고유기저 vs 두 직교기저','133–136초 EVD 같은축강조,136–141초 SVD 다른두기저강조. 수치 없음'),
('17_verdict',141,149,'GraphVerdict','ROUND 03 · EVD 승','143초승자,144–149초하나의기저라는 취향평가. 수학적우월성X표시 없음'),
('18_score',149,153,'GraphScore','EVD 2 : 1 SVD','149–151초점수갱신,152초EVD리드,153초종료')]

def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    cues=[];start=0
    for caption,end in LINES:cues.append(dict(start=start,end=end,caption=caption));start=end
    (ROOT/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    script='\n\n'.join(' '.join(c['caption'] for c in cues if a<=c['start']<b) for _,a,b,*_ in SCENES)+'\n'
    (ROOT/'master_script.md').write_text('# 3편 수정 확정 대본 · 153초\n\n사용자 수정 원문·종료 시각 그대로. 이전149초 타이밍 사용 안 함.\n\n'+script,encoding='utf-8')
    (ROOT/'narration.md').write_text('\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues),encoding='utf-8')
    tts=script.replace('EVD','이 브이 디').replace('SVD','에스 브이 디').replace('P','피').replace('D','디').replace('V','브이').replace('U','유').replace('A','에이')
    (ROOT/'tts_script.txt').write_text(tts,encoding='utf-8')
    manifest=[]
    for directory,a,b,cls,title,claim in SCENES:
        folder=ROOT/'scenes'/directory;folder.mkdir(parents=True,exist_ok=True)
        words=' '.join(c['caption'] for c in cues if a<=c['start']<b)
        (folder/'script.txt').write_text(words+'\n',encoding='utf-8')
        (folder/'spec.md').write_text(f'# {title}\n\n## 목적·핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n공통 원점·격자·색과 해당 벡터 상태를 그대로 재구성해 컷 경계에서 연속성을 유지한다.\n\n## TTS 원문·확정 길이\n{words}\n\n사용자 확정 {a}–{b}초, {b-a}초. 콘티의 예상 구간보다 이 시각을 우선한다.\n\n## 화면·시간대별 애니메이션\n{claim}\n9:16과16:9 각각 배치. 숫자행렬·수치대입·내적값비교 제거. 주요수식 하나와 주요움직임 하나만 표시.\n\n## 화면 텍스트\n{title}\n\n## 시작·종료 상태\n전장면의 그림을 이어받아 현재 연산을 강조하고 다음 단계 상태를 남긴다.\n\n## 다음 장면 연결\n같은 시각객체의 위치·색을 유지한다. 물리적벡터변환과 좌표표현변경을 구분. 회상·예고 없음.\n\n## 정확성\n{claim}\nSVD는 동일한 가역행렬의 계산값 사용. 투영은 부호를 보존한다. 승패는 구조적간결성에 대한 취향판정.\n',encoding='utf-8')
        (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import GraphStructure\nclass {cls}(GraphStructure):\n    INDEX={len(manifest)}\n',encoding='utf-8')
        manifest.append(dict(id=directory[:2],directory='scenes/'+directory,start=a,end=b,duration_seconds=b-a,**{'class':cls},title=title))
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'scenes.yaml').write_text('title: EVD vs SVD — 분해 구조 v2\nduration_seconds: 153\ntiming_source: user_revised_sentence_ends\nlayouts: [shorts_1080x1920, longform_1920x1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    example=ROOT/'scenes/01_example'
    if example.exists():
        for name in ['script.txt','spec.md']:(example/name).unlink()
        example.rmdir()
if __name__=='__main__':main()
