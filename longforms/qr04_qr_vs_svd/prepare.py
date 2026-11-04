"""New episode 4: approved 108-second QR/SVD script, preserved old episode."""
import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''4|QR 분해는 왜 SVD처럼 대각행렬을 만들지 않을까요?
9|두 분해 모두 직교하는 방향을 찾지만, 그 방향을 선택하는 기준은 완전히 다릅니다.
12|두 개의 선형독립 열벡터를 가진 행렬 A를 생각해 보겠습니다.
14|먼저 QR 분해입니다.
18|QR은 첫 번째 열벡터의 방향을 그대로 기준으로 삼습니다.
24|그리고 두 번째 벡터에서 기존 방향과 겹치는 성분을 제거해, 새로운 직교 방향을 찾습니다.
29|이렇게 만들어진 기준 방향들은 원래 벡터들이 공간을 확장해 온 순서를 유지합니다.
33|하지만 두 번째 벡터는 여전히 첫 번째 방향의 성분을 가지고 있습니다.
39|이 성분이 R의 대각선 위쪽에 남기 때문에, R은 일반적으로 대각행렬이 아닌 위삼각행렬이 됩니다.
42|그렇다면 SVD는 어떨까요?
45|이번에는 행렬 A를 하나의 공간 변환으로 바라보겠습니다.
50|원래 공간에 단위원을 놓고 A를 적용하면, 일반적으로 원은 타원으로 변합니다.
53|타원에는 가장 길게 늘어난 방향과 가장 짧게 늘어난 방향이 존재합니다.
56|SVD는 바로 이 변환의 특별한 방향들을 찾아냅니다.
62|입력 공간에서 가장 크게 늘어나는 방향을 먼저 찾고, 그와 수직인 방향에서 다음 확대율을 찾습니다.
66|각 방향이 얼마나 늘어나는지는 특이값으로 나타냅니다.
70|그리고 변환된 타원의 축 방향을 출력 공간의 새로운 기준으로 사용합니다.
77|이렇게 입력과 출력의 기준을 모두 선택하면, 각 방향의 확대와 축소를 대각행렬 하나로 표현할 수 있습니다.
85|QR은 원래 열벡터의 순서를 따라 직교 기준을 만들고, SVD는 변환이 가장 크게 늘리는 방향부터 새로운 기준을 찾습니다.
90|따라서 두 분해는 같은 행렬에서도 서로 다른 구조를 드러냅니다.
98|QR의 위삼각행렬에는 원래 벡터들의 조합 관계가 남아 있고, SVD의 대각행렬에는 변환의 방향별 확대율이 남아 있습니다.
102|QR이 대각행렬을 만들지 않는 것은 분해가 불완전해서가 아닙니다.
108|QR은 공간이 만들어지는 순서를, SVD는 공간이 변형되는 방식을 보여주기 때문입니다.'''
STARTS=[0,4,9,12,18,24,29,33,39,42,45,50,53,56,62,66,70,74,77,81,85,90,94,98,102,105,107]
TITLES=['QR은 왜 대각행렬을 만들지 않을까?','같은 행렬 · 다른 방향 선택','두 개의 선형독립 열벡터','첫 열벡터의 방향을 그대로','겹치는 성분을 빼면 새 방향','첫 직선에서 평면으로','두 번째 벡터의 첫 방향 성분','위삼각행렬에 남는 조합 관계','SVD는 무엇을 바라볼까?','행렬을 공간 변환으로 보면','단위원 전체에 같은 A를 적용','최대 확대 · 최소 확대','입력 방향과 출력 축의 대응','가장 크게 늘어나는 입력 방향','특이값 = 방향별 확대율','출력 타원의 축도 단위 기준으로','입력 기준 V · 출력 기준 U','두 기준 사이의 작용은 대각행렬','QR: 원래 열벡터의 순서','SVD: 변환의 특이방향','같은 행렬, 서로 다른 구조','R에는 벡터의 조합 관계','Σ에는 방향별 확대율','위삼각과 대각 · 목적의 차이','QR: 공간을 구성하는 순서','SVD: 공간이 변형되는 방식','같은 행렬 · 서로 다른 기하학']
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    if not (P/'scenes.yaml').exists():shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
    cues=[];start=0
    for line in RAW.splitlines():
        end,s=line.split('|',1);end=int(end);cues.append(dict(start=start,end=end,tts=s,caption=s));start=end
    for name,obj in [('timing.json',cues),('project.json',dict(duration=108,ending_confirmed=True,timing_source='user_sentence_end_times',replaces='episode 4 topic; previous 107s least squares kept separately'))]:(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(c['tts'].replace('QR','큐 알').replace('SVD','에스 브이 디').replace('R','알').replace('A','에이') for c in cues)+'\n',encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    n='# QR 기하학 4편 — QR과 SVD의 차이\n\n사용자 확정 108초·23문장. 이전 최소제곱 4편과 별도 소스·출력.\n\n| 시작 | 종료 | 내레이션 |\n|---|---|---|\n'+'\n'.join(f'| {c["start"]} | {c["end"]} | {c["caption"]} |' for c in cues)+'\n'
    for name in ['narration.md','master_script.md']:(P/name).write_text(n,encoding='utf-8')
    manifest=[]
    for i,(start,title) in enumerate(zip(STARTS,TITLES)):
        end=STARTS[i+1] if i+1<len(STARTS) else 108;directory=f'scenes/{i+1:02}_scene';d=P/directory;d.mkdir(parents=True,exist_ok=True)
        manifest.append(dict(id=f'{i+1:02}',directory=directory,**{'class':'QRShot'},start=start,end=end,duration_seconds=end-start,title=title))
        (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ComparisonBase\nclass QRShot(ComparisonBase):\n    INDEX = '+str(i)+'\n',encoding='utf-8')
        (d/'script.txt').write_text('\n\n'.join(c['tts'] for c in cues if c['start']<end and c['end']>start)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} {title}\n\n- 핵심 주장: {title}\n- 사용자 확정 전체 시각 {start}–{end}초, 길이 {end-start}초.\n- 앞 장면과 같은 A, 색상·입력/출력 표기를 유지한다.\n- storyboard.md 컷 {i+1:02}, visuals.py INDEX {i}. 등장→관찰→변화→해석.\n- 기하학: A=Rot(30°)[[2,1],[0,1]], Q=Rot(30°), R=[[2,1],[0,1]].\n- SVD는 같은 A의 실제 계산 결과. vᵢ는 입력, uᵢ와 qᵢ는 출력 기준이며 같은 공간인 것처럼 혼합하지 않는다.\n- 자막은 timing.json의 실제 문장 경계에서 전환한다. 12–18초 컷도 14초 자막 전환을 반영한다.\n- 음원 미제공. 전체 문장을 한 번만 발화하며 컷 경계 문장을 중복하지 않는다.\n- 다음 장면은 같은 A의 다른 구조로 연결하며 복습·예고 발화는 없다.\n',encoding='utf-8')
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('title: QR 기하학 4편 — QR vs SVD\nduration_seconds: 108\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    source: {m["directory"]}/scene.py\n    class: QRShot\n    start: {m["start"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    prev=P.parent/'qr03_diagonal_volume'
    (P/'build.py').write_text((prev/'build.py').read_text(encoding='utf-8').replace('qr03_diagonal_volume','qr04_qr_vs_svd'),encoding='utf-8')
    s=(prev/'verify_final.py').read_text(encoding='utf-8').replace('qr03_diagonal_volume','qr04_qr_vs_svd')
    s=s.replace('TIMES=[2,5,10,14,18,29,33,36,40,47,52,56,61,65,69,76,82,87,91,94,98,104,107]','TIMES=[2,7,11,16,22,27,31,37,44,49,52,55,60,65,69,73,76,80,84,88,93,97,101,104,106,107]')
    (P/'verify_final.py').write_text(s,encoding='utf-8')
if __name__=='__main__':main()
