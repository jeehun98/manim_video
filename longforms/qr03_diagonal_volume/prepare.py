"""User's 108-second narration overrides provisional storyboard clocks."""
import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''3|행렬식은 왜 공간의 넓이나 부피와 연결될까요?
6|3차원 공간의 단위 정육면체를 생각해 보겠습니다.
11|행렬 A를 적용하면, 세 개의 좌표축은 각각 A의 열벡터 방향으로 변환됩니다.
15|그 결과 정육면체는 기울어진 평행육면체가 됩니다.
20|행렬식의 절댓값은 바로 이 변환이 부피를 몇 배로 바꾸었는지를 나타냅니다.
24|그런데 이 부피 변화를 더 단순하게 이해할 방법은 없을까요?
26|행렬 A를 QR 분해해 보겠습니다.
30|A는 직교행렬 Q와 위삼각행렬 R의 곱으로 표현됩니다.
34|여기서 Q는 공간을 회전하거나 반사하는 직교변환입니다.
37|이 과정에서는 길이와 각도, 부피가 변하지 않습니다.
42|따라서 A가 만들어내는 부피 변화는 R만 살펴보아도 알 수 있습니다.
44|먼저 R의 첫 번째 열벡터입니다.
49|이 벡터는 첫 번째 좌표축 위에 놓여 있고, 그 길이는 R의 첫 번째 대각 성분의 절댓값입니다.
53|두 번째 열벡터를 추가하면 평행사변형이 만들어집니다.
58|이때 두 번째 벡터가 첫 번째 방향으로 얼마나 기울어져 있는지는 넓이에 영향을 주지 않습니다.
62|넓이를 결정하는 것은 밑변과 수직 높이입니다.
66|그리고 이 높이가 바로 R의 두 번째 대각 성분의 절댓값입니다.
71|따라서 평행사변형의 넓이는 첫 번째와 두 번째 대각 성분의 절댓값을 곱한 값입니다.
73|이제 세 번째 열벡터를 추가해 보겠습니다.
79|평행육면체의 부피는 밑면의 넓이와 그 평면에서 벗어나는 수직 높이의 곱입니다.
84|세 번째 벡터의 수직 높이는 R의 세 번째 대각 성분의 절댓값입니다.
88|따라서 전체 부피는 R의 세 대각 성분의 절댓값을 곱한 값이 됩니다.
95|R의 대각선 위쪽 계수들은 도형의 기울어진 형태를 바꿀 수 있지만, 이 수직 높이들을 바꾸지는 않습니다.
100|결국 A의 행렬식의 절댓값은 R의 대각 성분들의 절댓값을 곱한 값과 같습니다.
108|행렬식이 공간의 부피 변화를 나타낸다면, QR 분해는 그 부피 변화가 각각의 독립 방향에서 어떻게 만들어지는지를 보여줍니다.'''
STARTS=[0,3,6,11,15,20,24,26,30,34,37,42,44,49,53,58,62,66,71,73,79,84,88,92,95,100,106]
TITLES=['행렬식은 왜 부피와 연결될까?','기준 부피 1 · 단위 정육면체','표준기저에서 A의 열벡터로','같은 변환을 도형 전체에','행렬식의 절댓값 = 부피 배율','부피 변화를 더 단순하게','QR로 분리하면','R을 먼저, Q를 나중에','Q는 회전 또는 반사','길이 · 각도 · 부피 보존','A와 R의 부피 배율은 같다','첫 번째 열 · 첫 번째 방향','밑변 길이와 첫 대각 성분','두 번째 열이 만드는 밑면','기울어져도 넓이는 그대로','넓이 = 밑변 × 수직 높이','두 번째 대각 성분은 높이','첫 두 대각 성분의 곱 = 넓이','세 번째 열 · 평면 밖으로','부피 = 밑면 넓이 × 높이','세 번째 대각 성분은 높이','세 대각 성분의 곱 = 부피','기울기 변화 ≠ 부피 변화','세 수직 길이는 그대로','A의 행렬식과 R의 대각선','독립 방향마다 쌓이는 부피','전체 부피와 기하학적 구성']
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    if not (P/'scenes.yaml').exists():shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
    cues=[];start=0
    for line in RAW.splitlines():
        end,s=line.split('|',1);end=int(end);cues.append(dict(start=start,end=end,tts=s,caption=s));start=end
    for name,obj in [('timing.json',cues),('project.json',dict(duration=108,ending_confirmed=True,timing_source='user_sentence_end_times'))]:(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(c['tts'].replace('QR','큐 알').replace('Q','큐').replace('R','알').replace('A','에이') for c in cues)+'\n',encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    n='# QR 3편 — 대각선에 부피가 숨어 있는 이유\n\n사용자 확정 108초·25문장. 콘티의 약 110초 배분 대신 새 종료 시각 사용.\n\n| 시작 | 종료 | 내레이션 |\n|---|---|---|\n'+'\n'.join(f'| {c["start"]} | {c["end"]} | {c["caption"]} |' for c in cues)+'\n'
    for name in ['narration.md','master_script.md']:(P/name).write_text(n,encoding='utf-8')
    manifest=[]
    for i,(start,title) in enumerate(zip(STARTS,TITLES)):
        end=STARTS[i+1] if i+1<len(STARTS) else 108;directory=f'scenes/{i+1:02}_scene';d=P/directory;d.mkdir(parents=True,exist_ok=True)
        manifest.append(dict(id=f'{i+1:02}',directory=directory,**{'class':'QRShot'},start=start,end=end,duration_seconds=end-start,title=title))
        (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import VolumeBase\nclass QRShot(VolumeBase):\n    INDEX = '+str(i)+'\n',encoding='utf-8')
        (d/'script.txt').write_text('\n\n'.join(c['tts'] for c in cues if c['start']<end and c['end']>start)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} {title}\n\n- 주장: {title}\n- 사용자 확정 시각 {start}–{end}초, 길이 {end-start}초.\n- storyboard.md 컷 {i+1:02}의 화면을 새 108초 시각으로 재배치한다.\n- visuals.py INDEX {i}, 모든 꼭짓점에 같은 선형변환 적용.\n- A=[[1,0,1],[1,2,2],[0,0,2]], 부피 배율 4. 양의 대각 QR.\n- R→Q 순서, 전단에서 대각 고정, 직교 높이와 대각 계수 대응.\n- 상위 timing.json의 문장을 한 번만 발화. 컷 경계에서 중복 발화하지 않는다.\n- 음원 미제공으로 무음 visual 및 별도 자막.\n',encoding='utf-8')
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('title: QR 3편 — 대각선과 부피\nduration_seconds: 108\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    source: {m["directory"]}/scene.py\n    class: QRShot\n    start: {m["start"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    prev=P.parent/'qr02_triangular_structure/revisions/v2_96s'
    (P/'build.py').write_text((prev/'build.py').read_text(encoding='utf-8').replace('qr02_triangular_structure_v2','qr03_diagonal_volume'),encoding='utf-8')
    s=(prev/'base.py').read_text(encoding='utf-8').replace('QR / 02     공간의 확장과 위삼각 구조','QR / 03     대각선과 부피').replace('선형독립인 열벡터 · 순서를 보존하는 QR','단위 정육면체 → 부피 배율 → 직교 높이의 곱')
    (P/'base.py').write_text(s,encoding='utf-8')
    s=(prev/'verify_final.py').read_text(encoding='utf-8').replace('qr02_triangular_structure_v2','qr03_diagonal_volume').replace('2880','3240').replace('96','108')
    s=s.replace('TIMES=[2,5,8,11,15,23,28,33,37,42,46,50,56,61,65,68,72,77,80,84,88,94]','TIMES=[2,5,10,14,18,29,33,36,40,47,52,56,61,65,69,76,82,87,91,94,98,104,107]')
    (P/'verify_final.py').write_text(s,encoding='utf-8')
if __name__=='__main__':main()
