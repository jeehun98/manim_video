"""89-second requested series retrospective; horizontal version only."""
import json,shutil
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
RAW='''3|하나의 행렬은 단순히 숫자들을 배열한 것일까요?
8|우리는 QR 분해를 통해, 그 숫자들 뒤에 숨어 있는 기하학적 구조를 살펴봤습니다.
11|처음에는 벡터들이 공간을 만들어가는 과정에서 출발했습니다.
17|하나의 벡터가 직선을 만들고, 새로운 독립적인 벡터가 더해지면 평면이 만들어집니다.
23|QR 분해는 이 과정에서 기존 방향과 겹치는 성분을 분리하고, 새로운 직교 방향을 찾아냅니다.
28|그 결과 만들어지는 위삼각행렬에는 벡터들이 공간을 확장해 온 순서가 기록됩니다.
34|그리고 그 대각 성분들은 단순한 숫자가 아니라, 각 단계에서 새롭게 추가되는 수직 높이를 나타냅니다.
40|이 높이들을 곱하면, 정사각행렬에서는 행렬식의 절댓값, 즉 부피의 확대율과 연결됩니다.
44|하지만 직교하는 방향을 찾는 방법이 QR 분해만 있는 것은 아닙니다.
51|SVD는 원래 벡터들의 순서가 아니라, 선형변환이 공간을 가장 크게 늘리고 줄이는 방향을 찾아냅니다.
56|같은 행렬이라도 어떤 직교 기준을 선택하느냐에 따라 드러나는 구조가 달라지는 것입니다.
63|그리고 QR 분해의 직교 기준을 반복적으로 갱신하면, 적절한 조건에서는 행렬의 고유방향에 가까워질 수 있습니다.
68|고윳값은 유지한 채 행렬을 표현하는 기준이 변화하고, 마침내 그 고유구조가 드러납니다.
75|공간을 구성하는 방향, 부피를 결정하는 높이, 변환을 설명하는 특이방향, 그리고 행렬의 고유방향까지.
79|이 모든 과정에서 우리가 반복해서 사용한 것은 직교성이었습니다.
84|QR 분해가 보여주는 것은 단순히 행렬을 두 개로 나누는 방법이 아닙니다.
89|복잡하게 얽힌 계산 속에서, 서로 독립적인 방향을 찾아 구조를 이해하는 하나의 방법입니다.'''
STARTS=[0,3,8,11,14,17,20,23,26,28,31,34,37,40,44,48,51,56,60,63,68,72,75,79,84]
TITLES=['행렬은 단순한 숫자의 배열일까?','숫자 뒤에 숨어 있는 기하학','공간을 만드는 첫 방향','하나의 벡터가 만드는 직선','독립 방향이 더해지면 평면','기존 방향과 겹치는 성분 분리','새로운 직교 방향의 발견','공간의 확장 순서가 계수로','위삼각행렬의 대각선','대각 성분과 수직 높이','길이 → 넓이 → 부피','높이의 곱과 행렬식','단위 부피가 여덟 배로','직교 방향을 고르는 다른 관점','단위원에서 변환의 특이방향으로','특이값은 타원의 반축 길이','같은 행렬 · 서로 다른 기준','직교 기준을 반복적으로 갱신하면','고유방향에 가까워지는 기준','고윳값은 그대로 · 표현은 변화','공간의 구성 · 부피의 구조','특이방향 · 고유방향','서로 다른 기준을 잇는 직교성','숫자의 분해를 넘어 공간의 구조로','행렬 안의 구조를 발견하는 일']
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    if not (P/'scenes.yaml').exists():shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
    cues=[];start=0
    for line in RAW.splitlines():
        end,s=line.split('|',1);end=int(end);cues.append(dict(start=start,end=end,tts=s,caption=s));start=end
    for name,obj in [('timing.json',cues),('project.json',dict(duration=89,ending_confirmed=True,layout='longform',timing_source='user_sentence_end_times'))]:(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(c['tts'].replace('QR','큐 알').replace('SVD','에스 브이 디') for c in cues)+'\n',encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    n='# QR 기하학 — 마무리 영상\n\n사용자 확정 89초·17문장. 요청한 가로형만 제작한다. 사용자 명시 요청에 따라 시리즈 회고를 포함한다.\n\n| 시작 | 종료 | 내레이션 |\n|---|---|---|\n'+'\n'.join(f'| {c["start"]} | {c["end"]} | {c["caption"]} |' for c in cues)+'\n'
    for name in ['narration.md','master_script.md']:(P/name).write_text(n,encoding='utf-8')
    manifest=[]
    for i,(start,title) in enumerate(zip(STARTS,TITLES)):
        end=STARTS[i+1] if i+1<len(STARTS) else 89;directory=f'scenes/{i+1:02}_scene';d=P/directory;d.mkdir(parents=True,exist_ok=True)
        manifest.append(dict(id=f'{i+1:02}',directory=directory,**{'class':'QRShot'},start=start,end=end,duration_seconds=end-start,title=title))
        (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ClosingBase\nclass QRShot(ClosingBase):\n    INDEX = '+str(i)+'\n',encoding='utf-8')
        (d/'script.txt').write_text('\n\n'.join(c['tts'] for c in cues if c['start']<end and c['end']>start)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} {title}\n\n- 주장: {title}\n- 사용자 확정 전체 시각 {start}–{end}초, 길이 {end-start}초.\n- 입력: 같은 배경·원점·색상 체계를 유지한다.\n- 화면: storyboard.md 컷 {i+1:02}, visuals.py INDEX {i}. 등장→관찰→변화→해석.\n- 문장·TTS는 script.txt 및 timing.json 기준, 컷 경계에서 중복하지 않는다.\n- 공간·부피 예시 A₃=[[2,1,1],[0,2,1],[0,0,2]], Q₃=I, R₃=A₃, det=8.\n- SVD는 xy평면에 제한한 동일 변환 C=[[2,1],[0,2]]의 입력/출력 기저를 구별한다.\n- QR 반복은 별도로 표시한 실대칭 예시 A₀=[[3,1],[1,3]], 실제 누적 Pₖ를 쓴다.\n- 끝 상태는 다음 관점의 같은 시각 언어로 연결한다. 각 목적의 직교 기준을 같은 벡터로 합치지 않는다.\n- 가로형 1920×1080만 제작, 음원 미제공으로 무음·자막 영상.\n',encoding='utf-8')
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('title: QR 기하학 마무리\nduration_seconds: 89\nlayout: longform\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    source: {m["directory"]}/scene.py\n    class: QRShot\n    start: {m["start"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    prev=P.parent/'qr05_eigenvalue_iteration'
    s=(prev/'build.py').read_text(encoding='utf-8').replace('qr05_eigenvalue_iteration','qr_series_closing').replace("choices=['shorts','longform','both'],default='both'","choices=['longform'],default='longform'")
    (P/'build.py').write_text(s,encoding='utf-8')
    s=(prev/'verify_final.py').read_text(encoding='utf-8').replace('qr05_eigenvalue_iteration','qr_series_closing').replace('3720','2670').replace('_124s_','_89s_').replace('-124)','-89)').replace('duration=124','duration=89').replace("choices=['shorts','longform','both'],default='both'","choices=['longform'],default='longform'")
    s=s.replace('TIMES=[3,6,11,17,22,25,30,33,35,39,46,52,55,59,65,69,75,79,85,90,95,97,101,105,109,113,116,120,123]','TIMES=[2,6,10,13,16,19,22,25,27,30,33,36,39,43,47,50,54,59,62,67,71,74,78,83,88]')
    (P/'verify_final.py').write_text(s,encoding='utf-8')
    a=np.array([[3.,1],[1,3]]);basis=np.eye(2);rows=[]
    for k in range(12):
        rows.append(dict(k=k,A=a.tolist(),P=basis.tolist(),angle=float(np.arctan2(basis[1,0],basis[0,0]))))
        q,r=np.linalg.qr(a);d=np.diag(np.where(np.diag(r)<0,-1.,1.));q=q@d;r=d@r;a=r@q;basis=basis@q
    (P/'iterations.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
if __name__=='__main__':main()
