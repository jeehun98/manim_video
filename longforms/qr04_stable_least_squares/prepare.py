"""Approved 107-second speech clock, no estimated timing."""
import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''2|같은 수학 문제를 푸는 두 가지 방법이 있습니다.
6|하나는 정규방정식, 다른 하나는 QR 분해입니다.
8|그런데 컴퓨터는 왜 QR 분해를 더 선호할까요?
14|먼저 두 개의 벡터가 만드는 평면과, 그 평면 밖에 있는 목표 벡터 b를 생각해 보겠습니다.
18|우리는 두 벡터를 조합해 b에 가장 가까운 점을 찾으려고 합니다.
20|이것이 최소제곱 문제입니다.
24|가장 가까운 점에서는 b와의 차이가 평면에 수직이 됩니다.
30|이 조건을 수식으로 정리하면 A의 전치행렬과 A를 곱하는 정규방정식이 등장합니다.
32|수학적으로는 올바른 방법입니다.
35|하지만 컴퓨터에서 계산할 때는 문제가 생길 수 있습니다.
38|두 열벡터가 거의 평행하다고 생각해 보겠습니다.
44|이 경우 두 벡터를 구별하는 방향은 매우 작고, 작은 오차에도 해가 크게 달라질 수 있습니다.
47|이러한 민감성을 나타내는 값이 조건수입니다.
52|그런데 정규방정식에서 A의 전치행렬과 A를 곱하면, 조건수가 제곱됩니다.
56|예를 들어 조건수가 천이었다면, 백만으로 커지는 것입니다.
60|원래도 민감했던 문제를 수치적으로 더 불리한 형태로 바꾸는 셈입니다.
63|그렇다면 QR 분해는 무엇을 다르게 할까요?
67|행렬 A를 직교행렬 Q와 위삼각행렬 R로 분해합니다.
70|Q는 서로 수직인 기준 방향들로 이루어져 있습니다.
74|먼저 목표 벡터 b를 이 직교 방향들에 투영합니다.
79|그리고 위삼각행렬 R에 대한 방정식을 풀어, 원래 벡터들의 조합 계수를 구합니다.
82|이 과정에서는 조건수가 제곱된 행렬을 만들 필요가 없습니다.
86|물론 QR 분해가 원래 문제의 민감성을 제거하는 것은 아닙니다.
92|거의 평행했던 두 벡터는 여전히 거의 평행하고, 해도 작은 오차에 민감할 수 있습니다.
97|다만 안정적인 QR 알고리즘은 계산 과정에서 불필요한 수치적 오차를 줄일 수 있습니다.
101|정규방정식과 QR 분해는 같은 최소제곱 문제를 해결합니다.
107|하지만 수학적으로 같은 해를 구하는 것과, 컴퓨터가 그 해를 정확하게 계산하는 것은 서로 다른 문제입니다.'''
STARTS=[0,2,6,8,14,18,20,24,30,32,35,38,44,47,52,56,60,63,67,70,74,79,82,86,92,97,101,105]
TITLES=['같은 문제, 두 계산 경로','정규방정식과 QR 분해','왜 계산 경로가 중요할까?','평면 밖의 목표 벡터 b','b에 가장 가까운 점 찾기','최소제곱 문제','최적점의 잔차는 평면에 수직','수직 조건에서 정규방정식으로','정확한 산술에서는 올바른 해','컴퓨터는 유한 정밀도로 계산','거의 평행한 두 열벡터','작은 독립 방향 · 큰 계수의 상쇄','민감성의 지표: 조건수','AᵀA를 만들면 조건수 제곱','1,000 → 1,000,000','문제의 민감성 + 계산 경로','QR은 무엇을 다르게 할까?','A = QR · 평면은 그대로','직교하는 두 기준 방향','1단계: 직교 방향에 투영','2단계: 후진대입으로 계수 찾기','조건수가 제곱된 행렬을 피한다','원래 문제의 민감성은 남는다','작은 변화에 민감한 계수','안정적인 QR 계산 경로','같은 최소제곱 해를 향해','수학적 해와 실제 계산 결과','같은 해 · 다른 수치적 안정성']
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    if not (P/'scenes.yaml').exists():shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
    cues=[];start=0
    for line in RAW.splitlines():
        end,s=line.split('|',1);end=int(end);cues.append(dict(start=start,end=end,tts=s,caption=s));start=end
    for name,obj in [('timing.json',cues),('project.json',dict(duration=107,ending_confirmed=True,timing_source='user_sentence_end_times'))]:(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(c['tts'].replace('QR','큐 알').replace('Q','큐').replace('R','알').replace('A','에이').replace('b','비') for c in cues)+'\n',encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    n='# QR 4편 — 정규방정식과 QR의 수치 안정성\n\n사용자 확정 107초·27문장. 음원 미제공.\n\n| 시작 | 종료 | 내레이션 |\n|---|---|---|\n'+'\n'.join(f'| {c["start"]} | {c["end"]} | {c["caption"]} |' for c in cues)+'\n'
    for name in ['narration.md','master_script.md']:(P/name).write_text(n,encoding='utf-8')
    manifest=[]
    for i,(start,title) in enumerate(zip(STARTS,TITLES)):
        end=STARTS[i+1] if i+1<len(STARTS) else 107;directory=f'scenes/{i+1:02}_scene';d=P/directory;d.mkdir(parents=True,exist_ok=True)
        manifest.append(dict(id=f'{i+1:02}',directory=directory,**{'class':'QRShot'},start=start,end=end,duration_seconds=end-start,title=title))
        (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import LeastSquaresBase\nclass QRShot(LeastSquaresBase):\n    INDEX = '+str(i)+'\n',encoding='utf-8')
        overlapping=[c for c in cues if c['start']<end and c['end']>start]
        (d/'script.txt').write_text('\n\n'.join(c['tts'] for c in overlapping)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} {title}\n\n- 핵심 주장: {title}\n- 사용자 확정 전체 시각 {start}–{end}초, 길이 {end-start}초.\n- 입력 상태: 같은 최소제곱 문제와 좌표계·색상을 유지한다.\n- 화면: storyboard.md 컷 {i+1:02}, visuals.py INDEX {i}.\n- 시작→종료: 해당 기하학/수식의 등장→관찰→변화→해석. 끝에는 같은 문제의 다음 계산 단계로 시각적으로 연결한다.\n- TTS: 상위 timing.json의 겹치는 문장; 컷 경계에서 중복 발화하지 않는다.\n- 수학적 조건: ε>0, A는 열 전체 계수, 축약 Q는 QᵀQ=I인 3×2 행렬.\n- 평면은 ε가 작아져도 고정. κ₂(AᵀA)=κ₂(A)²와 κ₂(R)=κ₂(A)는 실제 오차 배율과 구분한다.\n- 안정적인 Householder QR 기준. 실제 음원 미제공으로 무음 영상·별도 자막.\n',encoding='utf-8')
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('title: QR 4편 — 최소제곱의 수치 안정성\nduration_seconds: 107\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    source: {m["directory"]}/scene.py\n    class: QRShot\n    start: {m["start"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    prev=P.parent/'qr03_diagonal_volume'
    (P/'build.py').write_text((prev/'build.py').read_text(encoding='utf-8').replace('qr03_diagonal_volume','qr04_stable_least_squares'),encoding='utf-8')
    s=(prev/'base.py').read_text(encoding='utf-8').replace('QR / 03     대각선과 부피','QR / 04     최소제곱과 수치 안정성').replace('단위 정육면체 → 부피 배율 → 직교 높이의 곱','열 전체 계수 · ε > 0 · 2-노름 조건수')
    (P/'base.py').write_text(s,encoding='utf-8')
    s=(prev/'verify_final.py').read_text(encoding='utf-8').replace('qr03_diagonal_volume','qr04_stable_least_squares').replace('3240','3210').replace('_108s_','_107s_').replace('-108)','-107)').replace('duration=108','duration=107')
    s=s.replace('TIMES=[2,5,10,14,18,29,33,36,40,47,52,56,61,65,69,76,82,87,91,94,98,104,107]','TIMES=[1,4,10,16,22,28,34,37,42,46,50,55,59,65,69,73,77,81,85,90,96,100,104,106]')
    (P/'verify_final.py').write_text(s,encoding='utf-8')
if __name__=='__main__':main()
