"""Save the approved narration, user timings, and independent scene specifications."""
import json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parent
LINES = [
('행렬분해 이상형 월드컵!',1),('EVD 대 SVD.',3),('대결 기준, 이름입니다.',5),
('먼저 EVD. Eigenvalue Decomposition, 고유값 분해입니다.',8),
("Eigen은 독일어로 '고유한', '자기 자신의'라는 의미를 가지고 있습니다.",13),
('실제로 고유벡터는 행렬을 적용해도 원래 자신이 놓인 직선을 벗어나지 않습니다.',18),
('변환 후에도 자기만의 방향을 유지하는 것이죠.',21),
('이름만으로도 수학적 특징을 어느 정도 짐작할 수 있습니다.',24),
('다음은 SVD. Singular Value Decomposition, 특이값 분해입니다.',28),
("Singular는 '특이한', '독특한'이라는 의미를 가지고 있습니다.",32),
('그런데 무엇이 특이하다는 걸까요?',34),
('특이값은 행렬이 특정 방향의 길이를 얼마나 확대하거나 축소하는지 나타냅니다.',39),
("하지만 '특이하다'는 이름만으로 이러한 수학적 특징을 떠올리기는 쉽지 않습니다.",44),
('그렇다면 이름 대결의 승자는?',46),('EVD!',47),
('고유하다는 이름에서 고유벡터의 특징을 보다 직관적으로 이해할 수 있기 때문입니다.',52)]
SCENES = [
('01_open',0,3,'NameOpen','행렬분해 이상형 월드컵','두 분해의 대결을 소개한다.'),
('02_criterion',3,5,'NameCriterion','대결 기준 · 이름','판정은 이름의 직관성에 한정한다.'),
('03_eigen',5,13,'NameEigen','Eigen · 자기 자신의','Eigen의 일상 의미와 전체 명칭을 소개한다.'),
('04_eigenline',13,21,'NameEigenline','같은 직선 위에 머무는 벡터','A=[[2,1],[1,2]], v=(1,1), Av=3v. 양의 고윳값 사례다.'),
('05_connection',21,24,'NameConnection','이름과 성질의 연결','고유하다는 이름이 고유직선의 성질을 연상시킨다.'),
('06_singular',24,32,'NameSingular','Singular · 특이한','일상 의미를 소개하며 역사적 어원은 단정하지 않는다.'),
('07_question',32,34,'NameQuestion','무엇이 특이한 걸까?','이름에서 성질을 추측하도록 질문한다.'),
('08_ellipse',34,39,'NameEllipse','방향에 따른 길이 변화','A=diag(2,0.7), 단위원의 상은 반축 2,0.7인 타원이다.'),
('09_intuition',39,44,'NameIntuition','이름만으로 떠올리기는?','특이값의 정의가 틀렸다는 뜻이 아닌 이름의 직관성 평가다.'),
('10_verdict',44,47,'NameVerdict','이름 대결의 승자는?','46초 EVD를 공개하며 분해법 전체의 우열을 주장하지 않는다.'),
('11_winner',47,52,'NameWinner','이름의 직관성 · EVD','50초 점수 1:0, 마지막 0.5초 유지. 예고 없음.')]

def stamp(t):
    return f'{int(t)//3600:02}:{int(t)//60%60:02}:{int(t)%60:02},000'

def main():
    cues=[];start=0
    for caption,end in LINES:
        cues.append(dict(start=start,end=end,caption=caption));start=end
    (ROOT/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    script='\n\n'.join(' '.join(c['caption'] for c in cues if a<=c['start']<b) for _,a,b,*_ in SCENES)+'\n'
    (ROOT/'master_script.md').write_text('# 행렬분해 이상형 월드컵 01 — 이름\n\n사용자 확정 원문 · 문장 종료 시각 기준 52초\n\n'+script,encoding='utf-8')
    (ROOT/'narration.md').write_text('\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues),encoding='utf-8')
    tts=script.replace('EVD','이 브이 디').replace('SVD','에스 브이 디').replace('Eigenvalue Decomposition','아이겐밸류 디컴포지션').replace('Singular Value Decomposition','싱귤러 밸류 디컴포지션').replace('Eigen','아이겐').replace('Singular','싱귤러')
    (ROOT/'tts_script.txt').write_text(tts,encoding='utf-8')
    manifest=[]
    for directory,a,b,cls,title,claim in SCENES:
        folder=ROOT/'scenes'/directory;folder.mkdir(parents=True,exist_ok=True)
        words=' '.join(c['caption'] for c in cues if a<=c['start']<b)
        (folder/'script.txt').write_text(words+'\n',encoding='utf-8')
        (folder/'spec.md').write_text(f'# {title}\n\n## 목적과 주장\n{claim}\n\n## 앞 장면과 연결\n독립 씬. 동일한 EVD/SVD 헤더와 색상으로 연결한다.\n\n## TTS 원문\n{words}\n\n확정 길이: {b-a}초 ({a}–{b}초). 사용자 문장 종료 시각, 음원 미제공.\n\n## 화면과 애니메이션\n첨부 콘티 SCENE {len(manifest)+1:02} 기준. 블루 EVD, 청록 SVD, 남색 배경. 시작 0.3초 이내 등장, 구간 내 변화 후 종료.\n세로는 제목 아래 중앙 실험, 가로는 왼쪽 설명과 오른쪽 실험으로 재배치.\n\n## 화면 텍스트\n{title}\n\n## 시작·종료 상태\n고정 비교 헤더 → 해당 주장 시각화 완성.\n\n## 다음 장면 연결\n컷으로 연결, 연결 내레이션과 다음 편 예고 없음.\n\n## 정확성\n{claim}\n이름의 직관성은 이번 영상의 평가 관점이다. 수학적 우열이 아니다.\n',encoding='utf-8')
        (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import BattleScene\nclass {cls}(BattleScene):\n    INDEX={len(manifest)}\n',encoding='utf-8')
        manifest.append(dict(id=directory[:2],directory='scenes/'+directory,start=a,end=b,duration_seconds=b-a,**{'class':cls},title=title))
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'scenes.yaml').write_text('title: EVD vs SVD — 이름\nduration_seconds: 52\ntiming_source: user_sentence_end_times\nlayouts: [shorts_1080x1920, longform_1920x1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    example=ROOT/'scenes'/'01_example'
    if example.exists():
        # Only remove the copied, unedited template files.
        for name in ['script.txt','spec.md']:(example/name).unlink()
        example.rmdir()

if __name__=='__main__':main()
