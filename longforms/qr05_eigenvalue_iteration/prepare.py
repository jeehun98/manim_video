"""Approved 124-second finale; actual positive-diagonal QR iterations."""
import json,shutil
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
RAW='''5|행렬을 QR 분해한 뒤, 두 행렬의 곱셈 순서를 뒤집으면 어떤 일이 일어날까요?
7|하나의 정사각행렬 A를 생각해 보겠습니다.
13|QR 분해를 적용하면 A는 직교행렬 Q와 위삼각행렬 R의 곱으로 표현됩니다.
19|보통은 여기서 끝나지만, 이번에는 R과 Q의 순서를 뒤집어 새로운 행렬을 만들어 보겠습니다.
23|이렇게 얻은 행렬은 원래 A와 다른 숫자를 가지고 있습니다.
26|그런데 놀랍게도, 고윳값은 변하지 않습니다.
27|왜 그럴까요?
34|Q는 직교행렬이므로, 새 행렬은 원래 A의 양쪽에 Q의 전치행렬과 Q를 곱한 형태로 표현할 수 있습니다.
35|이것은 직교 유사변환입니다.
41|행렬을 다른 직교 기준에서 다시 표현하는 것이기 때문에, 고윳값은 그대로 유지됩니다.
44|그렇다면 이 과정을 계속 반복하면 어떻게 될까요?
48|새로운 행렬을 다시 QR 분해하고, R과 Q의 순서를 뒤집습니다.
54|이 과정을 반복할 때마다 고윳값은 유지되지만, 행렬을 표현하는 기준은 달라집니다.
56|여기서 흥미로운 현상이 나타납니다.
61|서로 다른 양의 고윳값을 가진 대칭행렬을 생각해 보겠습니다.
66|한 고유방향에서는 벡터가 네 배로 늘어나고, 다른 고유방향에서는 두 배로 늘어납니다.
71|처음에는 우리가 사용하는 좌표축이 이 고유방향들과 일치하지 않습니다.
77|그런데 행렬을 반복해서 적용하면, 더 강하게 확대되는 방향의 영향이 상대적으로 커집니다.
80|QR 반복은 이러한 성질과 연결되어 있습니다.
87|매 단계 직교하는 기준을 다시 구성하면서, 적절한 조건에서는 그 기준들이 고유방향에 점점 가까워집니다.
92|처음에는 두 방향이 섞여 나타나던 행렬의 작용이, 점차 각각의 방향으로 분리되는 것입니다.
98|그 결과 대칭행렬의 비대각 성분은 점점 작아지고, 행렬은 대각행렬에 가까워질 수 있습니다.
103|그리고 그 대각선에 나타나는 값들이 바로 원래 행렬의 고윳값입니다.
106|처음부터 고윳값을 알고 시작한 것은 아닙니다.
110|행렬을 분해하고, 순서를 뒤집고, 다시 분해했을 뿐입니다.
114|하지만 그 반복 과정에서 행렬의 고유구조가 드러난 것입니다.
117|QR 분해는 직교하는 기준을 만드는 방법입니다.
124|그리고 QR 반복은 그 기준을 계속 바꾸면서, 행렬에 숨어 있는 고유방향과 고윳값을 찾아가는 방법이 됩니다.'''
STARTS=[0,5,7,13,19,23,26,27,31,34,35,41,44,48,54,56,61,66,71,77,80,87,92,96,98,103,106,110,114,117]
TITLES=['QR 다음에 RQ를 곱하면?','하나의 정사각행렬 A₀','직교행렬과 위삼각행렬로 분해','두 행렬의 곱셈 순서를 바꾸면','숫자가 달라진 새 행렬','고윳값은 그대로','왜 고윳값이 유지될까?','직교성으로 R₀를 다시 쓰면','A₁ = Q₀ᵀA₀Q₀','직교 유사변환','같은 변환 · 다른 직교 기준','이 과정을 계속 반복하면?','새 행렬을 다시 QR → RQ','변하는 표현 · 변하지 않는 고윳값','비대각 성분에 나타나는 변화','대칭 · 서로 다른 양의 고윳값','두 고유방향 · 4배와 2배','원래 좌표축은 고유방향과 다르다','강한 확대 방향의 영향이 커진다','하나의 벡터에서 직교 기준들로','누적 기준이 고유방향에 가까워진다','방향 사이의 혼합이 줄어든다','점점 작아지는 비대각 성분','대각행렬에 가까워지는 반복','대각선에서 드러나는 고윳값','처음 주어진 것은 행렬의 원소','분해 → 순서 변경 → 다시 분해','반복이 드러낸 고유구조','QR은 직교 기준을 구성한다','고윳값은 그대로 · 달라지는 기준']
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    if not (P/'scenes.yaml').exists():shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
    cues=[];start=0
    for line in RAW.splitlines():
        end,s=line.split('|',1);end=int(end);cues.append(dict(start=start,end=end,tts=s,caption=s));start=end
    for name,obj in [('timing.json',cues),('project.json',dict(duration=124,ending_confirmed=True,timing_source='user_sentence_end_times'))]:(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(c['tts'].replace('QR','큐 알').replace('Q','큐').replace('R','알').replace('A','에이') for c in cues)+'\n',encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    n='# QR 기하학 5편 — QR 반복과 고윳값\n\n사용자 확정 124초·28문장. 실제 양의 대각 QR 반복값을 사용한다.\n\n| 시작 | 종료 | 내레이션 |\n|---|---|---|\n'+'\n'.join(f'| {c["start"]} | {c["end"]} | {c["caption"]} |' for c in cues)+'\n'
    for name in ['narration.md','master_script.md']:(P/name).write_text(n,encoding='utf-8')
    manifest=[]
    for i,(start,title) in enumerate(zip(STARTS,TITLES)):
        end=STARTS[i+1] if i+1<len(STARTS) else 124;directory=f'scenes/{i+1:02}_scene';d=P/directory;d.mkdir(parents=True,exist_ok=True)
        manifest.append(dict(id=f'{i+1:02}',directory=directory,**{'class':'QRShot'},start=start,end=end,duration_seconds=end-start,title=title))
        (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import IterationBase\nclass QRShot(IterationBase):\n    INDEX = '+str(i)+'\n',encoding='utf-8')
        scripts=[c['tts'] for c in cues if c['start']<end and c['end']>start]
        (d/'script.txt').write_text('\n\n'.join(scripts)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} {title}\n\n- 주장: {title}\n- 사용자 확정 시각 {start}–{end}초, 길이 {end-start}초.\n- 앞 장면의 같은 A₀=[[3,1],[1,3]], 회색 원좌표축과 색상 규칙을 유지한다.\n- storyboard.md 컷 {i+1:02}, visuals.py INDEX {i}. 등장→관찰→변화→해석.\n- 시작·종료: 해당 단계의 행렬/누적 기준을 제시하고 같은 변환의 다음 표현으로 연결한다.\n- Pₖ=Q₀…Qₖ₋₁, Aₖ=PₖᵀA₀Pₖ. 실제 반복값은 iterations.json.\n- 61초 이전에는 고유방향을 정답으로 미리 그리지 않는다.\n- 거듭제곱 장면은 고정 A₀의 정규화된 벡터 거듭제곱, QR 장면은 누적 직교 기준으로 구별.\n- 유한 반복은 수치 근사, 정확한 대각형은 k→∞로 표시. 임의 행렬의 일반 수렴을 주장하지 않는다.\n- 발화는 상위 timing.json에 따라 문장당 한 번만 진행하며 컷 경계 중복 없음. 음원 미제공으로 무음 영상.\n',encoding='utf-8')
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('title: QR 기하학 5편 — QR 반복\nduration_seconds: 124\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    source: {m["directory"]}/scene.py\n    class: QRShot\n    start: {m["start"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    prev=P.parent/'qr04_qr_vs_svd'
    (P/'build.py').write_text((prev/'build.py').read_text(encoding='utf-8').replace('qr04_qr_vs_svd','qr05_eigenvalue_iteration'),encoding='utf-8')
    s=(prev/'verify_final.py').read_text(encoding='utf-8').replace('qr04_qr_vs_svd','qr05_eigenvalue_iteration').replace('3240','3720').replace('_108s_','_124s_').replace('-108)','-124)').replace('duration=108','duration=124')
    s=s.replace('TIMES=[2,7,11,16,22,27,31,37,44,49,52,55,60,65,69,73,76,80,84,88,93,97,101,104,106,107]','TIMES=[3,6,11,17,22,25,30,33,35,39,46,52,55,59,65,69,75,79,85,90,95,97,101,105,109,113,116,120,123]')
    (P/'verify_final.py').write_text(s,encoding='utf-8')
    a0=np.array([[3.,1],[1,3]]);a=a0.copy();basis=np.eye(2);rows=[];checks=[]
    for k in range(13):
        q,r=np.linalg.qr(a);signs=np.diag(np.where(np.diag(r)<0,-1.,1.));q=q@signs;r=signs@r
        checks.extend([np.allclose(a,q@r),np.allclose(a,basis.T@a0@basis),np.allclose(np.linalg.eigvalsh(a),[2,4]),np.all(np.diag(r)>0),np.allclose(basis.T@basis,np.eye(2))])
        power=np.linalg.matrix_power(a0,k)@np.array([1.,0]);power/=np.linalg.norm(power)
        checks.append(np.allclose(basis[:,0],power))
        rows.append(dict(k=k,A=a.tolist(),Q=q.tolist(),R=r.tolist(),P=basis.tolist(),angle_degrees=float(np.degrees(np.arctan2(basis[1,0],basis[0,0]))),off_diagonal=float(a[0,1])))
        a=r@q;basis=basis@q
    assert all(checks)
    (P/'iterations.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    (P/'math_verification.json').write_text(json.dumps(dict(all_checks_pass=True,checks=['A_k=Q_kR_k','positive diagonal','A_k=P_k^T A0 P_k','orthogonal P_k','eigenvalues 2,4 at every step'],iterations=13,duration=124,sentences=len(cues),timing_continuous=all(cues[i]['end']==cues[i+1]['start'] for i in range(len(cues)-1))),indent=2),encoding='utf-8')
if __name__=='__main__':main()
