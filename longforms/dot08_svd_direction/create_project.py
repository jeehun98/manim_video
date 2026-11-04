"""Materialize approved narration and scene contracts before making visuals."""
import json,shutil,re
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''하나의 행렬은 모든 방향의 벡터를 똑같이 변환할까요?|3
이번에는 내적을 이용해 행렬이 각 방향에 어떻게 작용하는지 살펴보겠습니다.|8
행렬은 입력 벡터의 크기뿐 아니라 방향도 바꿀 수 있습니다.|12
그런데 복잡한 변환도 특별한 입력 방향들을 기준으로 나누면 단순하게 표현할 수 있습니다.|17
이것이 특이값 분해, 영어로 SVD의 핵심 원리입니다.|21
SVD는 행렬 A를 세 행렬, U와 시그마, V의 전치행렬의 곱으로 분해합니다.|26
그렇다면 이 세 행렬은 각각 무엇을 의미할까요?|29
하나의 예제를 살펴보겠습니다.|31
첫 번째 행에는 0과 음수 1, 두 번째 행에는 3과 0이 있는 행렬입니다.|35
이 행렬에 가로 방향의 단위벡터를 입력하면 세로 방향으로 길이가 3인 벡터가 나옵니다.|41
반대로 세로 방향의 단위벡터를 입력하면 왼쪽으로 길이가 1인 벡터가 나옵니다.|46
즉, 입력 방향에 따라 확대되는 크기와 출력 방향이 달라집니다.|50
이번 행렬에서는 가로와 세로 방향이 바로 특별한 입력 방향입니다.|54
이 두 방향을 열벡터로 가진 행렬이 V입니다.|57
먼저 입력 벡터를 가로로 2, 세로로 1이라고 하겠습니다.|61
V의 각 열벡터와 입력 벡터를 내적하면 첫 번째 방향의 성분은 2, 두 번째 방향의 성분은 1입니다.|68
이렇게 입력 벡터의 방향별 성분을 측정하는 것이 V의 전치행렬이 하는 일입니다.|73
이제 시그마 행렬을 살펴보겠습니다.|75
시그마는 특이값을 대각성분으로 가진 행렬입니다.|78
이번 예제에서는 첫 번째 방향의 특이값이 3, 두 번째 방향의 특이값이 1입니다.|84
따라서 앞에서 측정한 성분 2와 1에 각각 곱하면 6과 1이 됩니다.|89
마지막으로 U 행렬이 등장합니다.|91
U의 열벡터들은 각 성분이 향할 출력 방향을 나타냅니다.|94
첫 번째 출력 방향은 위쪽이고, 두 번째 출력 방향은 왼쪽입니다.|99
따라서 첫 번째 성분 6을 위쪽 방향으로, 두 번째 성분 1을 왼쪽 방향으로 배치합니다.|104
이 두 벡터를 더하면 음수 1과 6인 벡터가 됩니다.|108
실제로 원래 행렬 A에 입력 벡터 2와 1을 직접 곱해도 같은 결과가 나옵니다.|113
즉, 행렬의 변환을 방향별 성분의 측정, 크기 조절, 출력 방향의 결합으로 나누어 계산한 것입니다.|120
이 구조는 다른 행렬에도 적용할 수 있습니다.|123
입력 벡터를 각 입력 특이벡터와 내적하고, 해당 특이값을 곱한 다음, 출력 특이벡터 방향으로 합하면 됩니다.|129
앞서 PCA에서는 데이터가 가장 크게 퍼지는 방향을 찾았습니다.|134
반면 SVD에서는 행렬 자체가 입력 방향에 따라 얼마나 확대하고, 어떤 출력 방향으로 보내는지 분해합니다.|140
결국 내적으로 방향의 성분을 측정하는 원리가, 행렬 전체의 변환을 방향별로 이해하는 방법으로 확장된 것입니다.|147'''
CUTS=[
 (0,17,'같은 행렬 · 방향마다 다른 반응','행렬은 입력 방향에 따라 길이와 방향을 다르게 바꾼다.','0–3초 서로 다른 입력. 3–8초 같은 A에 대한 출력 비교. 8–12초 한 입력과 출력. 12–17초 가로·세로 입력을 강조.'),
 (17,29,'SVD · 세 단계로 읽는 행렬','곱은 A=UΣVᵀ이고 벡터에 작용하는 순서는 Vᵀ→Σ→U다.','17–21초 영문명. 21–26초 분해식과 세 역할. 26–29초 오른쪽부터 적용하는 순서 강조.'),
 (29,50,'예제 행렬의 두 가지 반응','A(1,0)=(0,3), A(0,1)=(−1,0).','29–31초 빈 행렬. 31–35초 행 순서대로 값 등장. 35–41초 가로 입력→위쪽3. 41–46초 세로 입력→왼쪽1. 46–50초 두 반응 비교.'),
 (50,57,'V · 특별한 입력 방향','이 예제에서 V=I₂이며 두 열은 직교 단위벡터다.','50–54초 입력축의 v₁,v₂. 54–57초 두 방향을 V의 열로 묶음. V=I₂는 이 예제의 성질임을 표시.'),
 (57,73,'Vᵀ · 내적으로 성분을 측정','Vᵀx는 두 열과 입력의 내적을 세로로 모은 값이다.','57–61초 x=(2,1). 61–64.5초 c₁=2, 64.5–68초 c₂=1 계산. 68–73초 Vᵀx=(2,1)로 묶음.'),
 (73,89,'Σ · 성분마다 다른 배율','특이값3,1을 적용해 성분(2,1)을(6,1)로 바꾼다.','73–75초 성분 숫자 유지. 75–78초 대각행렬 등장. 78–84초 배율3,1 강조. 84–89초 숫자 막대만2→6,1→1. 출력 방향은 아직 적용하지 않음.'),
 (89,108,'U · 출력 방향으로 조합','6u₁+u₂=(−1,6)이며 음수는 왼쪽 출력 방향에서 나온다.','89–91초 U행렬. 91–94초 U의 열을 출력공간과 연결. 94–99초 위·왼쪽 단위방향. 99–102초 위로6, 102–104초 끝점에서 왼쪽1. 104–108초 원점부터 최종 벡터.'),
 (108,120,'직접 곱해도 같은 결과','Ax와 UΣVᵀx가 모두(−1,6)이다.','108–113초 직접 원소곱 계산. 113–120초 내적→크기조절→출력방향의 계산 흐름과 결과 비교.'),
 (120,129,'한 행렬을 방향별 반응의 합으로','Ax=Σᵢσᵢuᵢ(vᵢᵀx).','120–123초 다른 예제 A′와 회전된 V′를 명시해 일반화. 123–129초 내적·특이값·출력방향을 순서대로 강조. 원래 예제 행렬의 값은 바꾸지 않는다.'),
 (129,140,'데이터의 분포 · 행렬의 작용','PCA는 데이터의 퍼짐, SVD는 입력·출력 방향과 배율을 읽는다.','129–134초 중심화된 점군과 주성분. 134–140초 같은 A에 여러 방향을 입력. 행이 샘플인 중심화X의 오른쪽 특이벡터와 PCA방향 관계를 작은 보조문구로 명시.'),
 (140,147,'내적으로 행렬의 방향별 작용을 읽다','입력 성분 측정·배율 적용·출력 방향 결합으로 완결한다.','140–142초 Vᵀx=(2,1). 142–144초 ΣVᵀx=(6,1). 144–147초 UΣVᵀx=(−1,6)과 출력 재구성. 예고 없이 완결.')]
CONTRACT='A=[[0,−1],[3,0]], x=(2,1), V=I₂, Σ=diag(3,1), U=[[0,−1],[1,0]]. v₁=(1,0),v₂=(0,1),u₁=(0,1),u₂=(−1,0). U,V는 직교정규이고 σ₁≥σ₂≥0. Vᵀx=(2,1), ΣVᵀx=(6,1), 출력(−1,6). Σ단계는 숫자 성분의 배율만 바꾸며 출력공간에 배치하지 않는다. 왼쪽 출력은 음수 특이값이 아니라 u₂의 방향이다. 입력·출력 좌표계의 축은 고정하고 단위길이 표시를 제공. 일반화 예제는 A′로 명시하고 V′≠I. 행이 샘플인 중심화 데이터 X에서 오른쪽 특이벡터가 PCA의 특성공간 방향이다.'
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def spoken(s):
    for a,b in [('SVD','에스 브이 디'),('PCA','피 씨 에이'),('V','브이'),('U','유'),('A','에이')]:s=s.replace(a,b)
    return re.sub(r'\d+',lambda m:{'0':'영','1':'일','2':'이','3':'삼','6':'육'}.get(m[0],m[0]),s)
def main():
    shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\84d7eb5f-5198-43bd-9336-8a8ffc92df98\붙여넣은 텍스트.txt'),P/'storyboard.md')
    cues=[];start=0
    for row in RAW.splitlines():
        caption,end=row.rsplit('|',1);end=int(end);cues.append(dict(start=start,end=end,caption=caption));start=end
    assert len(cues)==33 and start==147
    (P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    script='\n\n'.join('\n'.join(c['caption'] for c in cues if s<=c['start']<e) for s,e,*_ in CUTS)+'\n'
    (P/'master_script.md').write_text('# 내적 LEVEL 08 — SVD\n\n사용자 확정 원고33문장, 제공 종료시각 기준147초.\n\n'+script,encoding='utf-8')
    (P/'tts_script.txt').write_text(spoken(script),encoding='utf-8')
    (P/'narration.md').write_text('# 문장별 내레이션\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n{c["caption"]}' for c in cues),encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    manifest=[]
    for i,(s,e,title,claim,animation) in enumerate(CUTS):
        directory=f'scenes/{i+1:02}_scene';d=P/directory;shutil.copytree(P.parent/'_template/scenes/01_example',d,dirs_exist_ok=True)
        original='\n'.join(c['caption'] for c in cues if s<=c['start']<e)
        (d/'script.txt').write_text(spoken(original)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+(CUTS[i-1][3] if i else '없음. 본편 질문.')+f'\n\n## TTS와 확정 길이\n사용자 제공 {s}–{e}초, {e-s}초. 음원 미제공.\n\n{original}\n\n## 화면 구성\n입력·출력 공간을 별도 좌표평면에 표시. 세로 도형 위·수식 아래, 가로 도형 왼쪽·수식 오른쪽. 각 공간은 고정축과 동일한 단위배율 사용. 성분 확대는 숫자 막대로 표시. 자막 영역 별도.\n\n## 구간별 애니메이션·텍스트\n{animation}\n\n## 시작·종료 상태와 다음 연결\n'+(CUTS[i+1][3] if i+1<len(CUTS) else '예제 출력과 세 단계로 본편 독립 완결.')+'\n\n## 수학적 조건\n'+CONTRACT+'\n',encoding='utf-8')
        (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import SVDBase\nclass SVD{i+1:02}(SVDBase):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=directory,start=s,end=e,duration_seconds=e-s,title=title,**{'class':f'SVD{i+1:02}'}))
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('duration_seconds: 147\ntiming_source: user_sentence_end_times\nlayouts:\n  shorts: [1080, 1920, 30]\n  longform: [1920, 1080, 30]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    (P/'brief.md').write_text('# 내적 LEVEL 08 — 제작 기준\n\n147초, 사용자 확정33문장과 종료시각. 11개 교체 가능한 독립 씬. 세로1080×1920, 가로1920×1080,30fps. 음원 미제공으로 무음·자막.\n\n'+CONTRACT+'\n\n색상: 입력파랑, 입력방향청록, 내적계수주황, 특이값노랑, 출력방향초록·보라, 최종출력밝은파랑. 요청 원문에 있는 PCA 비교만 유지하며 추가 복습·예고 없음.\n',encoding='utf-8')
if __name__=='__main__':main()
