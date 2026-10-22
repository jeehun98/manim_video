from pathlib import Path
import json,textwrap
R=Path('longforms/svd02_direction_map')
raw='''9|지난 실험에서 우리는 같은 거리만큼 떨어진 두 입력이라도, 그 차이가 어느 방향에 놓였는지에 따라 출력에서 서로 다르게 나타난다는 사실을 확인했습니다.
12|그렇다면 행렬이 가장 잘 구별하는 방향은 어디일까요?
21|이번에는 두 입력 사이의 거리를 정확히 1로 고정하겠습니다. 첫 번째 입력은 원점에 두고, 두 번째 입력은 원점에서 거리 1인 위치를 따라 움직입니다.
27|이렇게 하면 입력의 변화 크기는 항상 같습니다. 달라지는 것은 오직 방향뿐입니다.
32|먼저 가로 방향에 두 번째 입력을 놓겠습니다. 행렬을 통과한 두 출력 사이의 거리를 측정합니다.
35|이제 입력의 방향을 조금씩 회전시켜 보겠습니다.
40|입력에서는 두 점 사이의 거리가 계속 1이지만, 출력에서는 그 거리가 점점 달라집니다.
45|어떤 방향에서는 출력의 차이가 커지고, 다른 방향에서는 작아집니다.
49|우리가 찾으려는 것은 바로 이 거리의 최댓값과 최솟값입니다.
57|모든 방향을 비교했을 때 출력의 차이가 가장 크게 나타나는 입력 방향이 있습니다. 반대로 가장 작게 나타나는 방향도 있습니다.
62|이 방향들은 행렬이 입력의 차이를 가장 강하게 드러내고, 가장 약하게 드러내는 방향입니다.
66|그런데 지금까지는 각 방향에서 출력의 거리만 측정했습니다.
70|이번에는 거리뿐 아니라 출력이 어디에 놓이는지도 기록해 보겠습니다.
74|입력 방향을 한 바퀴 회전시키면서 출력 벡터의 끝점을 계속 남깁니다.
78|그러면 놀랍게도, 이 점들은 하나의 타원 궤적을 만듭니다.
86|우리가 처음부터 타원을 그리려고 했던 것은 아닙니다. 같은 크기의 입력 변화를 모든 방향에서 시험했더니 타원이 나타난 것입니다.
93|이 타원의 긴 축은 출력의 차이가 가장 크게 나타나는 방향을, 짧은 축은 가장 작게 나타나는 방향을 보여줍니다.
96|하지만 한 가지 주의할 점이 있습니다.
102|타원의 축은 출력 공간의 방향입니다. 우리가 처음 찾으려던 것은 그 축을 만들어내는 입력 공간의 방향입니다.
108|따라서 가장 긴 출력 벡터가 나타났을 때, 그 벡터를 만들어낸 입력 방향도 함께 기록해야 합니다.
114|이렇게 찾은 특별한 입력 방향이 오른쪽 특이벡터, 그에 대응하는 출력 방향이 왼쪽 특이벡터입니다.
120|그리고 길이가 1인 입력 변화가 출력에서 얼마나 커졌는지를 나타내는 값이 특잇값입니다.
126|입력 방향을 브이, 출력 방향을 유, 특잇값을 시그마라고 하면, 행렬은 브이를 시그마 배의 유로 보냅니다.
129|이것이 에이 브이는 시그마 유라는 관계입니다.
132|여기서 중요한 것은 타원이라는 모양 자체가 아닙니다.
140|우리는 행렬에 같은 크기의 변화를 여러 방향으로 넣었고, 그 결과를 비교해 가장 강한 반응과 가장 약한 반응을 찾아냈습니다.
145|그런데 실제 입력이 이 특별한 방향들 중 하나에 정확히 놓이지 않는다면 어떨까요?
149|임의의 입력은 여러 방향의 성분을 동시에 가지고 있습니다.
154|그렇다면 행렬은 그 성분들을 어떻게 읽고, 하나의 출력으로 만들어낼까요?'''
sentences=[];start=0
for line in raw.splitlines():
 e,t=line.split('|',1);e=int(e);sentences.append(dict(start=start,end=e,text=t));start=e
(R/'timing.json').write_text(json.dumps(dict(source='user_sentence_end_times',duration_seconds=154,sentences=sentences),ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02d}:{t%3600//60:02d}:{t%60:02d},000'
(R/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(r['start'])} --> {stamp(r['end'])}\n"+'\n'.join(textwrap.wrap(r['text'],43)) for i,r in enumerate(sentences))+'\n',encoding='utf-8')
(R/'narration.md').write_text('# 2막 — 행렬이 가장 잘 구별하는 방향은 어디일까?\n\n사용자 원문·종료 시각 기준 154초. 음원 미제공. 이번 제공 원문은 이전 실험 언급과 마지막 질문을 포함하며 이를 그대로 적용한다.\n\n'+'\n\n'.join(f"## {s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences),encoding='utf-8')
ends=[9,12,21,27,35,45,49,57,66,70,78,86,93,102,108,120,129,140,149,154]
titles=['같은 거리 다른 반응','가장 잘 구별하는 방향','입력 거리 1 고정','오직 방향만 변화','새로운 행렬의 첫 측정','방향별 거리 그래프','최댓값과 최솟값','극값 입력 방향 발견','길이만 측정했다','출력 위치 기록으로 전환','끝점 기록에서 타원 발견','타원은 실험 결과','출력의 장축과 단축','출력 축과 입력 방향 구분','대응 입력 역추적','특이벡터와 특잇값','Av = σu','발견한 방향과 반응','임의 입력의 성분','성분에서 출력으로 가는 질문']
claims=['같은 입력 거리도 방향에 따라 다르게 나타난다','모든 방향에서 가장 큰 반응을 찾는다','기준점 A 고정, 입력 B의 원점 거리 1','달라지는 것은 방향뿐이다','27초에 새 행렬을 도입하고 이후 변경하지 않는다','단위 입력의 방향별 출력 거리를 실제 계산해 그래프로 기록한다','최대 2, 최소 0.5를 찾는다','입력 30°와 120°가 극값을 만든다','아직 출력 위치 궤적은 기록하지 않았다','같은 행렬에서 기록하는 정보만 변경한다','출력 끝점의 누적 궤적은 타원이다','타원은 모든 단위 입력에 대한 실제 반응의 집합이다','출력의 장축 60°, 단축 150°','출력 축 방향은 대응 입력 방향과 다르다','출력 60°에 대응하는 입력은 30°이다','입력과 출력의 단위 방향 및 배율을 구별한다','Avᵢ=σᵢuᵢ를 최대·최소 쌍에서 확인한다','같은 크기 입력으로 반응의 극값을 찾은 실험이다','임의 입력은 두 직교 입력 방향의 성분을 함께 갖는다','성분들을 하나의 출력으로 조립하는 문제를 남긴다']
manifest=[];start=0;pron=[]
for i,(end,title,claim) in enumerate(zip(ends,titles,claims),1):
 d=R/f'scenes/{i:02d}';d.mkdir(parents=True,exist_ok=True)
 text='\n\n'.join(s['text'] for s in sentences if start<=s['start']<end)
 tts=text.replace('1로','일로').replace('거리 1인','거리 일인').replace('계속 1이지만','계속 일이지만').replace('길이가 1인','길이가 일인')
 (d/'script.txt').write_text(tts+'\n',encoding='utf-8');pron.append(tts)
 (d/'scene.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import DirectionScene\n"+f'class Scene{i:02d}(DirectionScene):\n    start_time={start}\n    end_time={end}\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02d} — {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('이전 실험의 같은 거리 비교' if i==1 else claims[i-2])+f'\n\n## TTS 원문과 확정 길이\n{text}\n\n사용자 제공 {start}–{end}초, {end-start}초.\n\n## 화면·타임라인\n../../storyboard_source.md 장면 {i:02d}. 공통 scene_engine.py의 절대시간 {start}–{end}초를 재현한다. 등장→관찰→변화→해석.\n\n## 화면 텍스트\n{title}. 수식과 극값 조건은 ../../README.md 참조.\n\n## 시작·종료 상태\n절대시간 경계의 동일한 실험 상태. 씬별 독립 렌더 및 교체 가능.\n\n## 다음 장면 연결\n동일한 행렬과 좌표계에서 기록·강조하는 정보만 변경한다.\n\n## 수학적 조건\n27초 이후 A=R(60°)diag(2,0.5)R(−30°). 입력 거리1. 최대 입력30°/출력60°, 최소 입력120°/출력150°. 모든 그래프·궤적·벡터는 실제 행렬곱으로 계산. 오른쪽/왼쪽 특이벡터는 단위벡터이고 실제 출력 길이는 σᵢ이다.\n',encoding='utf-8')
 manifest.append(dict(id=f'{i:02d}',directory=f'scenes/{i:02d}',**{'class':f'Scene{i:02d}'},start=start,end=end,duration_seconds=end-start,title=title));start=end
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'tts_script.txt').write_text('\n\n'.join(pron)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: svd02_direction_map\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\nscenes:\n'+''.join(f"  - id: '{m['id']}'\n    directory: {m['directory']}\n    class: {m['class']}\n    duration_seconds: {m['duration_seconds']}\n" for m in manifest),encoding='utf-8')
print(len(sentences),'sentences;',len(manifest),'scenes;',sum(m['duration_seconds'] for m in manifest),'seconds')
