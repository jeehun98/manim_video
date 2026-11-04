"""Save the approved 0–98s clocks; append the ending only after actual times arrive."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LINES=[
('행렬 분해 이상형 월드컵!',1),('EVD 대 SVD.',3),('대결 기준, 고윳값과 특이값입니다.',6),
('이번에는 하나의 행렬을 살펴보겠습니다.',8),
('정사각형에 이 행렬을 적용하면, 도형이 한쪽으로 기울어진 평행사변형으로 변합니다.',14),
('분명 변형이 일어났습니다.',16),
('그런데 이 행렬의 고윳값을 구하면, 놀랍게도 두 값 모두 1입니다.',20),
('고윳값이 모두 1인데, 도형은 왜 변한 걸까요?',23),
('고유벡터를 살펴보겠습니다.',25),
('수평 방향의 벡터에 이 행렬을 적용하면, 방향도 길이도 그대로 유지됩니다.',30),
('고윳값 1은 바로 이 고유방향에서의 배율이 1이라는 뜻입니다.',34),
('하지만 다른 방향까지 길이가 유지된다는 의미는 아닙니다.',38),
('이번에는 수직 방향의 벡터를 변환해 보겠습니다.',41),
('벡터가 옆으로 밀리면서 방향이 달라지고, 길이도 늘어납니다.',45),
('그렇다면 이 행렬이 벡터의 길이를 얼마나 변화시키는지는 어떻게 알 수 있을까요?',50),
('여기서 특이값이 등장합니다.',52),
('길이가 1인 벡터들을 모아 단위원을 만들어 보겠습니다.',55),
('이 원에 같은 행렬을 적용하면, 기울어진 타원이 만들어집니다.',59),
('타원의 가장 긴 축에 대응하는 입력 방향에서는 벡터의 길이가 약 2.414배로 늘어납니다.',65),
('반대로 가장 짧은 축에 대응하는 입력 방향에서는 약 0.414배로 줄어듭니다.',71),
('이 두 길이 배율이 바로 특이값입니다.',74),
('같은 행렬인데, 고윳값은 1과 1.',76),('특이값은 약 2.414와 0.414입니다.',80),
('고윳값은 변환 후에도 같은 직선 위에 남는 고유방향에서의 배율을 나타냅니다.',85),
('반면 특이값은 특별한 입력 방향들에서 길이가 얼마나 늘어나거나 줄어드는지를 나타냅니다.',90),
('그렇다면 이번 대결의 승자는?',92),('SVD!',93),
('한 번의 변환에서 나타나는 길이 변화의 크기를 더 직접적으로 보여주기 때문입니다.',98)]
TAIL=['현재 스코어, EVD 2 대 SVD 2.','다시 동점입니다!']
SCENES=[
('01_open',0,6,'ValuesOpen','ROUND 04 · 고윳값과 특이값','0–1타이틀,1–3후보,3–6기준. 시작2:1'),
('02_square',6,14,'ValuesSquare','하나의 전단변환','A=[[1,2],[0,1]]. 단위정사각형의 모든 꼭짓점에 [[1,2t],[0,1]] 적용. 아랫변 고정'),
('03_eigenvalues',14,23,'ValuesEigenvalues','고윳값은 1, 1','평행사변형 유지,16–20초중복 고윳값 공개. 독립 고유방향은 수평 하나뿐'),
('04_eigenvector',23,30,'ValuesEigenvector','Av = v','수평 벡터를 적용 전후 정확히 겹침. 도형은 희미한 배경으로 유지'),
('05_meaning',30,38,'ValuesMeaning','고유방향의 배율 ×1','고윳값1만으로 모든 방향의 길이 보존을 결론낼 수 없음. 수평만 고유방향'),
('06_vertical',38,45,'ValuesVertical','수직 벡터는 길어진다','(0,1)→(2,1), 같은 높이를 유지해 옆으로 이동. 입력은 회색점선. sqrt5는 화면 생략'),
('07_question',45,52,'ValuesQuestion','길이 변화를 어떻게 볼까?','수평 유지와 수직 일반 벡터의 길이 증가 대비.50초특이값'),
('08_circle',52,55,'ValuesCircle','‖x‖ = 1','길이1 벡터가 회전하며 단위원 궤적. 모든 입력방향 길이동일'),
('09_ellipse',55,59,'ValuesEllipse','같은 A · 원에서 타원으로','48점 각각 (1-t)x+tAx. 실제 A=[[1,2],[0,1]], 타원 출력장축22.5도, 반축sqrt2±1'),
('10_maximum',59,65,'ValuesMaximum','최대 길이 배율','입력67.5도→출력22.5도, σ1=1+sqrt2. 각도는 내부계산만. 입력길이1'),
('11_minimum',65,71,'ValuesMinimum','최소 길이 배율','입력-22.5도→출력-67.5도, σ2=sqrt2-1. 출력타원비율 그대로, 단축확대왜곡 없음'),
('12_lengths',71,74,'ValuesLengths','특이값 = 길이 배율','장축전체가 아닌 원점부터 반축 끝까지2.414와0.414 연결'),
('13_compare',74,80,'ValuesCompare','같은 행렬 · 다른 숫자','74–76 고윳값1,1.76–80 특이값2.414,.414. 단일 수평 고유방향 vs 타원 반축'),
('14_eigenmeaning',80,85,'ValuesEigenMeaning','고유직선에서의 배율','수평 고유벡터 점등, λ=1. 다른 독립고유방향 추가하지 않음'),
('15_singularmeaning',85,90,'ValuesSingularMeaning','특이방향의 길이 배율','입력·출력 같은 A 대응. 장축·단축 두 출력 길이를 번갈아 강조. σ≥0'),
('16_verdict',90,98,'ValuesVerdict','ROUND 04 · SVD 승','92초승자.93–98 한 번의 변환의 길이변화를 직접 드러낸다는 기준. 범용 수학적우열 아님')]

def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    lines=list(LINES);scenes=list(SCENES)
    ending=ROOT/'end_times.json'
    confirmed=ending.exists()
    if confirmed:
        times=json.loads(ending.read_text(encoding='utf-8'))
        assert 98<times['score_end']<times['end']
        lines.extend(zip(TAIL,[times['score_end'],times['end']]))
        scenes.append(('17_score',98,times['end'],'ValuesScore','EVD 2 : 2 SVD','마지막 두 실제 발화 종료 시각은 end_times.json. 추정배분 금지'))
    cues=[];start=0
    for caption,end in lines:cues.append(dict(start=start,end=end,caption=caption));start=end
    (ROOT/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'project.json').write_text(json.dumps(dict(duration=start,ending_confirmed=confirmed,timing_source='user_sentence_end_times',pending=[] if confirmed else TAIL),ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    full_script='\n\n'.join(' '.join(c['caption'] for c in cues if a<=c['start']<b) for _,a,b,*_ in scenes)
    if not confirmed:full_script+='\n\n'+' '.join(TAIL)
    (ROOT/'master_script.md').write_text('# 4편 확정 원문 — 고윳값과 특이값\n\n'+('전체 발화시간 확정.' if confirmed else '0–98초 확정. 마지막 본문91/93은 시간역행, 콘티103초는 추정배분이므로 마지막 두 실제 종료 시각 대기.')+'\n\n'+full_script+'\n',encoding='utf-8')
    (ROOT/'narration.md').write_text('\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues)+('\n\n종료 시각 미확정:\n\n'+' '.join(TAIL) if not confirmed else ''),encoding='utf-8')
    (ROOT/'tts_script.txt').write_text(full_script.replace('EVD','이 브이 디').replace('SVD','에스 브이 디')+'\n',encoding='utf-8')
    manifest=[]
    for directory,a,b,cls,title,claim in scenes:
        folder=ROOT/'scenes'/directory;folder.mkdir(parents=True,exist_ok=True)
        words=' '.join(c['caption'] for c in cues if a<=c['start']<b)
        (folder/'script.txt').write_text(words+'\n',encoding='utf-8')
        (folder/'spec.md').write_text(f'# {title}\n\n## 목적·주장\n{claim}\n\n## 앞 장면\n동일한 전단행렬과 공통 원점·색·객체 상태를 유지.\n\n## TTS 원문·확정 길이\n{words}\n\n{a}–{b}초, {b-a}초. 사용자 발화 시각.\n\n## 화면·시간별 애니메이션\n{claim}\n9:16과16:9 각각 구성. 한 행렬만 사용.\n\n## 화면 텍스트\n{title}\n\n## 시작·종료\n전장면의 변환 결과 유지→현재 방향과 길이 설명.\n\n## 다음 연결\n전단행렬 고정, 필요시에만 입력·출력 분리. 복습·예고 없음.\n\n## 정확성\n{claim}\n고윳값1의 중복도2와 고유공간차원1 구분. 특이값은 비음수 반축길이이며 실제 Av_i=σ_i u_i로 검증.\n',encoding='utf-8')
        (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ValuesScene\nclass {cls}(ValuesScene):\n    INDEX={len(manifest)}\n',encoding='utf-8')
        manifest.append(dict(id=directory[:2],directory='scenes/'+directory,start=a,end=b,duration_seconds=b-a,**{'class':cls},title=title))
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'scenes.yaml').write_text(f'title: EVD vs SVD — 고윳값과 특이값\nduration_seconds: {start}\nending_confirmed: {str(confirmed).lower()}\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    example=ROOT/'scenes/01_example'
    if example.exists():
        for name in ['script.txt','spec.md']:(example/name).unlink()
        example.rmdir()
if __name__=='__main__':main()
