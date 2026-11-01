"""Episode 03: approved 163-second narration and reproducible production scaffold."""
import json,shutil
from pathlib import Path
W=Path(__file__).resolve().parents[1];P=W/'longforms/minimal03_sparsification';P.mkdir(exist_ok=True)
shutil.copytree(W/'longforms/_template',P,dirs_exist_ok=True)
rows=[
(4,'수많은 점들이 서로 복잡하게 연결된 네트워크가 있습니다.'),
(8,'이 연결들을 대부분 제거하더라도, 원래 네트워크의 중요한 성질을 유지할 수 있을까요?'),
(12,'먼저 가장 간단한 조건부터 생각해 보겠습니다.'),
(15,'모든 점 사이를 이동할 수 있기만 하면 된다고 가정해 보죠.'),
(20,'점이 여덟 개라면, 수많은 연결 중 일곱 개만 남겨도 모든 점을 연결할 수 있습니다.'),
(25,'이렇게 모든 점을 연결하면서 순환 경로가 없는 구조를 신장 트리, Spanning Tree라고 합니다.'),
(27,'하지만 여기에는 문제가 있습니다.'),
(32,'모든 점이 여전히 연결되어 있다고 해서, 원래 네트워크와 같은 것은 아니기 때문입니다.'),
(38,'어떤 점 사이의 최단거리는 훨씬 길어질 수 있고, 연결 구조의 다른 성질도 달라질 수 있습니다.'),
(42,'그렇다면 연결을 줄이면서도, 네트워크의 더 많은 특성을 유지할 방법은 없을까요?'),
(47,'여기서 등장하는 것이 그래프 희소화, Graph Sparsification입니다.'),
(54,'특히 스펙트럴 희소화는 그래프의 연결 구조를 나타내는 수학적 양을 거의 유지하면서, 간선의 수를 줄이는 방법입니다.'),
(57,'각 점에 하나의 숫자를 놓아 보겠습니다.'),
(61,'그리고 연결된 두 점의 숫자가 얼마나 다른지 살펴보겠습니다.'),
(66,'두 숫자의 차이를 제곱하고, 연결의 가중치를 곱한 뒤, 모든 연결에 대해 더합니다.'),
(68,'이 값은 그래프의 에너지라고 부를 수 있습니다.'),
(74,'강하게 연결된 점들의 값이 크게 다르면 에너지가 커지고, 서로 비슷하면 작아집니다.'),
(78,'이제 연결들을 일부 제거하고, 남은 연결의 가중치를 조정해 보겠습니다.'),
(85,'목표는 어떤 숫자들을 점들에 배치하더라도, 새로운 그래프의 에너지가 원래 그래프와 거의 같도록 만드는 것입니다.'),
(88,'이것이 스펙트럴 희소화의 핵심 아이디어입니다.'),
(91,'중요한 것은 단순히 몇 개의 연결이 남았느냐가 아닙니다.'),
(96,'남은 연결들이 원래 네트워크의 구조를 얼마나 잘 대표하느냐입니다.'),
(98,'그렇다면 어떤 연결을 남겨야 할까요?'),
(100,'두 개의 촘촘한 집단을 생각해 보겠습니다.'),
(104,'각 집단 내부에는 수많은 연결과 대체 경로가 있습니다.'),
(108,'하지만 두 집단 사이에는 단 하나의 연결만 존재합니다.'),
(111,'집단 내부의 연결 하나를 제거해도 다른 길로 이동할 수 있습니다.'),
(116,'반면 두 집단을 잇는 유일한 연결을 제거하면, 네트워크가 둘로 분리됩니다.'),
(120,'모든 연결이 똑같이 중요한 것은 아니라는 뜻입니다.'),
(126,'스펙트럴 희소화에서는 유효 저항, Effective Resistance와 같은 개념을 이용해 연결의 중요도를 평가할 수 있습니다.'),
(132,'대체 경로가 풍부한 연결과, 네트워크 전체를 이어 주는 연결은 서로 다른 영향을 미칩니다.'),
(141,'그리고 중요한 연결을 선택하고 가중치를 조정하면, 원래보다 훨씬 적은 간선으로도 그래프의 에너지 구조를 근사적으로 보존할 수 있습니다.'),
(146,'물론 이것이 모든 최단거리나 모든 성질을 그대로 유지한다는 뜻은 아닙니다.'),
(150,'우리가 선택한 수학적 조건을 일정한 오차 범위 안에서 유지하는 것입니다.'),
(155,'결국 그래프 희소화는 단순히 연결을 많이 제거하는 기술이 아닙니다.'),
(163,'수많은 연결 중 어떤 관계가 중요한지를 찾아내고, 더 작은 네트워크로도 원래의 핵심 성질을 유지할 수 있는지 탐구하는 방법입니다.'),
]
bounds=[0,12,25,42,54,61,68,74,88,96,108,120,132,141,150,163]
titles=['무엇을 지워도 남을까?','연결만 유지한다면','연결성과 거리는 다르다','그래프 희소화','두 점의 값이 다르면','차이의 제곱을 모두 더한다','값이 비슷해지면','간선 삭제와 가중치 조정','모든 값 배치에서의 조건','두 집단과 하나의 연결','대체 경로와 유일한 다리','유효 저항으로 보는 중요도','28개 간선을 8개로','에너지를 근사적으로 보존','어떤 관계를 남길 것인가?']
claims=[
'32개 고정 노드와 96개 간선의 연결된 무방향 개념 그래프. 삭제 가능성은 질문이며 아직 보존 보장을 주장하지 않음.',
'연결된 무방향 K8에서 경로형 신장 트리 선택. 노드 8, 간선 7, 연결·비순환을 실제 검증. 임의의 7개가 아님.',
'단위 길이 정사각형 AB 삭제 후 A-B 거리 1→3. 연결 유지와 최단거리 유지는 다름.',
'가중 무방향 그래프에서 간선 선택과 남은 가중치 조정. 굵기는 가중치이며 간선 추가를 뜻하지 않음.',
'두 노드 값 1과3, 가중치2. 차이 -2. 노드의 값과 간선 가중치를 구분.',
'한 간선 2×(1−3)²=8. 무방향 간선을 한 번씩 합산. 여러 간선에서 E(x)=Σw_ij(x_i−x_j)²=xᵀLx.',
'같은 가중치2에서 값3→1로 변화하면 기여8→0. 중간값과 에너지 실제 계산.',
'삼각형 값0,1,2의 에너지6. 차이1인 밑변을 삭제하고 나머지 두 가중치1.5, 에너지7.5. 전체 배치의 최악 상대 오차50%인 원리 예시.',
'모든 실수 벡터 x에 대해 (1−ε)E_G≤E_H≤(1+ε)E_G. 몇 개 표본은 전칭 보장의 증명이 아님.',
'K4 두 집단과 단일 다리. 내부 간선6+6, 다리1, 총13. 모든 간선 가중치1.',
'내부 한 간선 삭제 시 대체 경로 존재. 다리까지 삭제하면 두 연결 성분. 위치 고정과 단절의 관계를 유지.',
'전기적 저항 r=1/w. K4 내부 간선 양끝 유효저항0.5, 다리1. 중요도 예시 wR; 확률적 표본추출·재가중의 일부 원리임.',
'검증용 G: 8노드 완전그래프, 순환8간선 가중치4/그외20간선0.1. H: 순환8간선만 남기고 가중치4.6. 모든 x에서 ε=0.15 보장.',
'선택한 에너지 이차형식의 상대 오차 보장이지 모든 거리 보존이 아님. 가중치는 전도도이며 최단거리 길이와 혼동하지 않음.',
'간선 수 감소보다 보존 조건을 대표하는 관계의 선택. 전편 복습·다음 편 예고 없음.',
]
events=[
'0–4초 점·간선 등장; 4–8초 복잡한 연결 관찰; 8–12초 일부 간선을 빨강 강조.',
'12–15초 K8 소개; 15–20초 7개 경로 간선만 남김; 20–25초 이동 점으로 순회하고 신장 트리 명칭.',
'25–32초 단위 길이 정사각형; 32–38초 AB 삭제와 우회 A-D-C-B; 38–42초 1→3과 연결성/거리 차이.',
'42–47초 Graph Sparsification; 47–54초 Spectral Sparsification과 가중치·에너지 관점.',
'54–57초 두 값1,3; 57–61초 1−3=−2.',
'61–66초 제곱4·가중치2·기여8; 66–68초 전체 합과 에너지 식.',
'68–74초 두 번째 노드 값을3에서1로 변화하며 실제 에너지8→0.',
'74–78초 삼각형 3→2간선, 에너지6→7.5; 78–85초 값 배치 변경과 양쪽 에너지; 85–88초 최악 ±50%를 명시.',
'88–96초 모든 x에 대한 상대 오차 식과 조건 선택.',
'96–100초 K4 두 집단; 100–104초 내부 대체 경로; 104–108초 유일한 다리 강조.',
'108–111초 내부 간선 삭제와 대체 경로; 111–116초 다리 삭제와 단절; 116–120초 성분2개.',
'120–126초 저항1 회로 비유, 유효저항0.5/1; 126–132초 wR 점수와 표본 선택·가중치 조정.',
'132–136초 같은 8노드에서28→8간선; 136–141초 재가중과 복수 배치 에너지 비교.',
'141–146초 에너지 근사와 거리 보존 구분; 146–150초 ε=0.15 전칭 오차 범위.',
'150–155초 선택·재가중·검증 세 단계; 155–163초 고정 노드·줄어든 간선과 보존 조건으로 결론.',
]
timing=[];s=0
for e,t in rows:timing.append(dict(start=s,end=e,text=t));s=e
(P/'narration_timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(timing))+'\n',encoding='utf-8')
manifest=[];narr=[];tts=[]
for i,(a,b,title,claim,event) in enumerate(zip(bounds,bounds[1:],titles,claims,events),1):
 d=P/f'scenes/{i:02}';d.mkdir(parents=True,exist_ok=True)
 body=' '.join(r['text'] for r in timing if a<=r['start']<b)
 (d/'script.txt').write_text(body+'\n',encoding='utf-8')
 (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import SparsificationScene\nclass Scene{i:02}(SparsificationScene):\n    index={i-1}\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02} · {title}\n\n## 목적·핵심 주장\n{claim}\n\n## 前 장면·연결\n절대 시각 {a}초에서 시작. 같은 노드 배치를 이어받거나 명시적으로 다른 예제로 전환. 다음 편 예고 없음.\n\n## TTS 원문과 길이\n{body}\n\n{a}–{b}초, 확정 길이 {b-a}초. 사용자 발화 시각 기준, 음원 없음.\n\n## 화면·애니메이션\n{event}\n\nscene_engine.py part_{i-1:02}. 세로·가로 별도 배치.\n\n## 화면 텍스트\n제목 {title}. 노드 값/간선 가중치/에너지 구분.\n\n## 시작·종료 상태\n해당 대상에서 시작하여 검증한 결과 또는 보존 조건으로 종료.\n\n## 정확성 확인\n{claim}\n',encoding='utf-8')
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title));narr.append(f'## {a}–{b}초 · {title}\n\n{body}');tts.append(body)
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
master='# 모든 것이 필요할까? 03 — 그래프 희소화\n\n사용자 확정 대본·163초.\n\n'+'\n\n'.join(narr)+'\n'
for name in ['narration.md','master_script.md']:(P/name).write_text(master,encoding='utf-8')
spoken='\n\n'.join(tts).replace('Spanning Tree','스패닝 트리').replace('Graph Sparsification','그래프 스파시피케이션').replace('Effective Resistance','이펙티브 리지스턴스')
(P/'tts_script.txt').write_text(spoken+'\n',encoding='utf-8')
(P/'scenes.yaml').write_text('id: minimal03_sparsification\ntitle: 모든 것이 필요할까? 03 — 그래프 희소화\nvideo:\n  fps: 30\n  variants:\n    shorts: [1080, 1920]\n    longform: [1920, 1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
(P/'brief.md').write_text('# 제작 기준\n\n163초, 사용자 제공 문장 종료 시각. 세로1080×1920·가로1920×1080,30fps,무음·전체 발화 자막.\n\n신장 트리의 연결성과 스펙트럴 에너지 근사를 구별. 모든 계산은 data_model.py에서 실제 검증. 삼각형은 최악오차50%의 원리 예시. 후반8노드28→8간선은 ε=0.15를 모든 x에서 만족하는 별도 검증예시. 점 몇 개의 값 대입만으로 전칭 보장을 주장하지 않음.\n\nLaplacian의 양의 가중치는 전도도, 저항은 역수. 거리 사례의 길이와 혼동하지 않음. 유효저항 점수는 wR이고 표본추출·재가중을 함께 언급.\n\n자막은 concat 이후 단일 ASS 트랙으로 합성. 이전문장 잔상 없는지 모든 문장 경계 프레임 검증.\n',encoding='utf-8')
example=P/'scenes/01_example'
if example.exists():
 assert example.resolve().is_relative_to(P.resolve());shutil.rmtree(example)
for name in ['build.py','caption_pass.py','inspect_frames.py','verify_caption_boundaries.py']:
 body=(W/'longforms/minimal02_genome'/name).read_text(encoding='utf-8').replace('minimal02','minimal03').replace('164','163').replace('4920','4890').replace('4919','4889')
 (P/name).write_text(body,encoding='utf-8')
shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\aa044f2a-465f-46f7-ba9b-89bb152b1263\붙여넣은 텍스트.txt'),P/'storyboard_user.md')
print(P,len(rows),len(manifest),sum(m['duration_seconds'] for m in manifest))
