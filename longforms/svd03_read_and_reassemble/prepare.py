from pathlib import Path
import json,textwrap
R=Path('longforms/svd03_read_and_reassemble')
raw='''7|지난 실험에서 우리는 행렬이 가장 강하게 반응하는 입력 방향과 가장 약하게 반응하는 입력 방향을 찾아냈습니다.
13|각 방향에 길이 1의 벡터를 넣으면, 행렬은 그에 대응하는 출력 방향으로 특잇값만큼 크기를 바꿨습니다.
18|그런데 실제 입력이 이 특별한 방향들 중 하나에 놓이지 않는다면 어떻게 될까요?
22|두 방향 사이에 놓인 임의의 입력 벡터를 생각해보겠습니다.
26|이 벡터에는 우리가 찾아낸 두 방향의 성분이 함께 들어 있습니다.
33|먼저 첫 번째 방향으로 얼마나 뻗어 있는지 측정해보겠습니다. 입력 벡터를 그 방향에 투영하면 하나의 값이 나옵니다.
36|이번에는 두 번째 방향에 투영합니다. 또 다른 값이 나옵니다.
42|두 방향은 서로 직교하기 때문에, 이 두 값만 알면 원래 입력 벡터를 정확히 표현할 수 있습니다.
46|우리는 입력을 바꾸지 않았습니다. 같은 입력을 다른 기준으로 읽어낸 것입니다.
50|그렇다면 이렇게 읽어낸 값들을 행렬에 통과시키면 어떻게 될까요?
55|첫 번째 방향의 성분은 그 방향에 대응하는 특잇값만큼 확대됩니다.
58|두 번째 방향의 성분에도 또 다른 특잇값이 적용됩니다.
62|중요한 것은 두 방향이 서로 다른 배율을 가진다는 사실입니다.
67|하지만 여기까지는 각 성분이 얼마나 커지거나 작아지는지만 계산했습니다.
70|행렬은 이 성분들을 출력 공간의 방향으로도 바꿉니다.
77|첫 번째 값은 첫 번째 출력 특이벡터 방향으로, 두 번째 값은 두 번째 출력 특이벡터 방향으로 나타납니다.
80|이제 두 출력 벡터를 더해보겠습니다.
87|서로 다른 방향에서 만들어진 두 벡터가 하나로 합쳐지면서, 처음 입력에 행렬을 직접 곱했을 때와 정확히 같은 출력이 만들어집니다.
91|복잡해 보였던 하나의 행렬곱을 세 과정으로 나누어 본 것입니다.
99|입력을 특별한 방향들의 성분으로 읽고, 각 성분에 서로 다른 배율을 적용하고, 그 결과를 출력 공간에서 다시 조립합니다.
103|이 세 과정을 각각 브이 전치, 시그마, 유로 나타낼 수 있습니다.
108|그리고 이를 하나로 합치면, 에이는 유, 시그마, 브이 전치의 곱이 됩니다.
110|이것이 특잇값 분해, 에스브이디입니다.
113|그런데 여기서 한 가지 흥미로운 사실이 있습니다.
119|어떤 방향의 특잇값이 매우 크더라도, 입력에 그 방향의 성분이 없다면 그 방향이 만드는 출력은 0입니다.
125|반대로 특잇값이 작더라도 입력에 해당 성분이 충분히 있다면 출력에 기여할 수 있습니다.
131|따라서 특잇값만 보고 특정 입력의 출력에서 어떤 성분이 가장 크게 기여하는지 결정할 수는 없습니다.
138|행렬이 어떤 방향에 강하게 반응하는지와, 실제 입력이 어떤 방향의 성분을 가지고 있는지는 서로 다른 문제입니다.
141|그렇다면 반대로 생각해보겠습니다.
146|행렬이 어떤 방향의 성분을 아주 작게 전달했다면, 출력만 보고 그 성분을 다시 알아낼 수 있을까요?
152|특히 출력에 작은 오차가 섞여 있다면, 원래 입력을 복원하는 과정에서는 어떤 일이 벌어질까요?'''
sentences=[];start=0
for line in raw.splitlines():
 e,t=line.split('|',1);e=int(e);sentences.append(dict(start=start,end=e,text=t));start=e
(R/'timing.json').write_text(json.dumps(dict(source='user_sentence_end_times',duration_seconds=152,sentences=sentences),ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02d}:{t%3600//60:02d}:{t%60:02d},000'
(R/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(r['start'])} --> {stamp(r['end'])}\n"+'\n'.join(textwrap.wrap(r['text'],43)) for i,r in enumerate(sentences))+'\n',encoding='utf-8')
(R/'narration.md').write_text('# 3막 — 행렬은 하나의 입력을 어떻게 읽어낼까?\n\n사용자 원문과 문장 종료 시각 기준 152초. 음원 미제공.\n\n'+'\n\n'.join(f"## {s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences),encoding='utf-8')
ends=[7,13,22,26,33,36,42,46,50,58,62,67,77,80,87,99,108,110,119,125,138,146,152]
titles=['두 특별한 입력 방향','방향과 배율의 대응','고정 입력 x','함께 들어 있는 두 성분','첫 번째 성분 읽기','두 번째 성분 읽기','두 성분의 합은 x','벡터와 좌표의 구분','두 성분의 처리 경로','서로 다른 배율','성분별 크기 변화','아직 스칼라 좌표','출력 방향으로 옮기기','출력 벡터 더하기','직접 계산 Ax와 일치','읽기 배율 조립','SVD 공식 발견','발견의 이름','별도 반례 큰 배율 기여 0','작은 배율의 기여','반응 능력과 실제 기여','복원 방향으로 질문 전환','출력에 작은 오차가 있다면']
claims=['직교하는 입력30°와120°를 고정 기준으로 삼는다','Av₁=2u₁, Av₂=0.5u₂','주 실험 x=v₁+v₂를 끝까지 변경하지 않는다','입력 x는 두 성분을 함께 포함한다','c₁=v₁ᵀx=1은 스칼라 계수다','c₂=v₂ᵀx=1은 별도의 스칼라 계수다','완비 직교 기준에서 x=c₁v₁+c₂v₂','벡터를 움직인 것이 아니라 표현 기준만 바꿨다','서로 다른 방향의 계수를 별도 경로로 처리한다','(1,1)에 각각2와0.5를 적용한다','배율은 방향마다 다르다','(2,0.5)는 아직 출력 기저의 스칼라 좌표다','두 기여를 각각2u₁,0.5u₂로 만든다','두 번째 벡터의 방향과 길이를 유지한 채 평행이동한다','2u₁+0.5u₂는 직접 계산한 Ax와 일치한다','이미 수행한 계산을 세 단계로 정리한다','오른쪽부터 작용하는 A=UΣVᵀ를 발견한다','발견한 구조의 이름만 붙인다','별도 반례 z=v₂에서 c₁=0이므로 첫 기여는0이다','z=v₂의 두 번째 출력 기여는0.5u₂다','특잇값은 고정이지만 입력별 실제 기여는 달라진다','입력을 숨기고 출력에서 성분을 복원하는 문제를 묻는다','출력 기저 성분0.50에0.01 오차를 더하고 질문으로 종료한다']
manifest=[];start=0;pron=[]
for i,(end,title,claim) in enumerate(zip(ends,titles,claims),1):
 d=R/f'scenes/{i:02d}';d.mkdir(parents=True,exist_ok=True)
 text='\n\n'.join(s['text'] for s in sentences if start<=s['start']<end)
 tts=text.replace('길이 1의','길이 일의').replace('출력은 0입니다','출력은 영입니다')
 (d/'script.txt').write_text(tts+'\n',encoding='utf-8');pron.append(tts)
 (d/'scene.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import ReadingScene\n"+f'class Scene{i:02d}(ReadingScene):\n    start_time={start}\n    end_time={end}\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02d} — {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('동일 행렬의 두 특이방향' if i==1 else claims[i-2])+f'\n\n## TTS 원문과 길이\n{text}\n\n사용자 제공 {start}–{end}초, 길이{end-start}초. 음원 미제공.\n\n## 화면과 시간대별 동작\n../../storyboard_source.md 장면{i:02d}. 공통 scene_engine.py에서 절대시간{start}–{end}초를 독립 재현한다. 입력 x는 왼쪽에 고정, 가운데 스칼라 계수, 오른쪽 출력 벡터를 구분한다.\n\n## 화면 텍스트\n{title}. 수식과 정확한 수치는 ../../README.md 기준.\n\n## 시작·종료 상태\n절대시간 경계의 계산 상태. 다음 씬은 같은 상태와 축 척도로 이어간다.\n\n## 다음 장면 연결\n같은 입력의 읽기→배율→조립 흐름을 유지한다. 별도 반례는 z로 명시한다.\n\n## 정확성 및 과장 방지\nA=R(60°)diag(2,0.5)R(−30°), 주 입력 x=v₁+v₂, c=(1,1). 스칼라 계수와 투영 벡터를 구분한다. 직접 행렬곱과 두 출력 기여의 합을 실제 계산한다. 110초 이후 반례 z와 주 입력 x를 혼동하지 않는다.\n',encoding='utf-8')
 manifest.append(dict(id=f'{i:02d}',directory=f'scenes/{i:02d}',**{'class':f'Scene{i:02d}'},start=start,end=end,duration_seconds=end-start,title=title));start=end
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'tts_script.txt').write_text('\n\n'.join(pron)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: svd03_read_and_reassemble\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\nscenes:\n'+''.join(f"  - id: '{m['id']}'\n    directory: {m['directory']}\n    class: {m['class']}\n    duration_seconds: {m['duration_seconds']}\n" for m in manifest),encoding='utf-8')
for name in ['build.py','sync_preview.py']:
 s=(Path('longforms/svd02_direction_map')/name).read_text(encoding='utf-8-sig').replace('svd02_','svd03_').replace('svd03_direction_map_154s','svd03_read_and_reassemble_152s').replace('154*fps','152*fps').replace('-154)','-152)').replace('154 seconds','152 seconds')
 (R/name).write_text(s,encoding='utf-8')
print(len(sentences),'sentences',len(manifest),'scenes',sum(m['duration_seconds'] for m in manifest),'seconds')
