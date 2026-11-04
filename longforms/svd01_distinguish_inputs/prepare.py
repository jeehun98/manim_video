import json
from pathlib import Path
R=Path('longforms/svd01_distinguish_inputs')
raw='''8|서로 다른 두 입력이 있습니다. 그런데 우리는 이 입력 자체를 관찰할 수 없고, 어떤 행렬을 통과한 결과만 볼 수 있다고 가정해보겠습니다.
11|두 입력이 서로 달랐다는 사실을 출력만으로 알아낼 수 있을까요?
19|먼저 실험을 위해 입력 공간을 공개하겠습니다. 화면 왼쪽에는 실제 입력을, 오른쪽에는 관찰자가 볼 수 있는 출력만 표시합니다.
25|가로 방향의 값은 그대로 전달하고, 세로 방향의 값은 10분의 1로 줄이는 행렬을 사용하겠습니다.
31|첫 번째 실험에서는 두 입력을 가로 방향으로 1만큼 떨어뜨립니다. 출력에서도 두 점은 1만큼 떨어져 있습니다.
39|두 번째 실험에서는 두 입력을 세로 방향으로 1만큼 떨어뜨립니다. 입력에서 두 점 사이의 거리는 앞선 실험과 정확히 같습니다.
43|하지만 출력에서는 두 점 사이의 거리가 0.1로 줄어듭니다.
49|두 실험 모두 입력은 같은 거리만큼 달라졌습니다. 그런데 출력에 남은 차이는 10배나 다릅니다.
51|왜 이런 차이가 생겼을까요?
56|바뀐 것은 두 입력 사이의 거리가 아니라, 두 입력이 서로 떨어진 방향입니다.
59|이제 세로 방향을 더 강하게 압축해보겠습니다.
63|0.1이었던 배율을 0.01로, 다시 0.001로 줄입니다.
69|입력에서 두 점은 여전히 1만큼 떨어져 있습니다. 하지만 출력에서는 두 점이 점점 가까워집니다.
71|여기서 한 가지를 구분해야 합니다.
79|출력의 차이가 아무리 작아도, 그 차이가 정확히 남아 있고 출력값을 정확하게 관측할 수 있다면 두 입력이 다르다는 사실은 구별할 수 있습니다.
82|0.001은 0이 아닙니다.
85|그렇다면 배율이 정확히 0이 되면 어떻게 될까요?
89|이제 세로 방향으로 떨어진 모든 점은 출력에서 같은 위치에 놓입니다.
94|입력에서는 서로 다른 두 점이었지만, 관찰자에게 주어지는 출력은 완전히 같습니다.
98|아무리 정확하게 측정하더라도 출력만으로는 두 입력을 구별할 수 없습니다.
106|이것은 단순히 차이가 작아진 상황과 다릅니다. 입력에 존재하던 차이가 출력에서는 완전히 사라진 것입니다.
109|우리는 지금까지 가로와 세로, 두 방향만 비교했습니다.
115|하지만 입력은 그 사이의 대각선 방향으로도 달라질 수 있고, 다른 모든 방향으로도 변할 수 있습니다.
120|그렇다면 입력 사이의 거리를 똑같이 고정한 채 방향만 바꾸면 어떨까요?
125|어떤 방향의 차이가 출력에서 가장 크게 나타나고, 어떤 방향의 차이가 가장 작게 나타날까요?
133|그리고 그 방향들을 찾을 수 있다면, 우리는 행렬이 무엇을 구별하고 무엇을 구별하지 못하는지 하나의 지도로 나타낼 수 있지 않을까요?'''
records=[]; start=0
for line in raw.splitlines():
 end,text=line.split('|',1); end=int(end);records.append(dict(start=start,end=end,text=text));start=end
(R/'timing.json').write_text(json.dumps({'source':'user_sentence_end_times','duration_seconds':133,'sentences':records},ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02d}:{t%3600//60:02d}:{t%60:02d},000'
# Keep supplied sentence boundaries; line breaks do not change timing.
import textwrap
(R/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(r['start'])} --> {stamp(r['end'])}\n"+'\n'.join(textwrap.wrap(r['text'],width=43)) for i,r in enumerate(records))+'\n',encoding='utf-8')
(R/'narration.md').write_text('# 1막 — 서로 다른 입력을 행렬은 구별할 수 있을까?\n\n사용자 제공 원문과 문장 종료 시각. 총 133초. 음원 미제공.\n\n'+'\n\n'.join(f"## {r['start']}–{r['end']}초\n\n{r['text']}" for r in records),encoding='utf-8')
ends=[8,11,19,25,31,43,56,63,71,82,89,98,106,115,125,133]
titles=['관찰할 수 없는 입력','출력만으로 구별할 수 있을까','실험 공간 공개','행렬의 규칙','가로 방향 실험','세로 방향 실험','같은 거리 다른 방향','배율을 줄인다','작지만 남은 차이','0.001은 0이 아니다','배율이 정확히 0','관찰자는 구별할 수 없다','축소와 소실','모든 방향으로 확장','같은 거리로 방향 탐색','방향별 반응의 지도']
claims=['관찰자는 입력에 접근할 수 없다','출력으로 입력 차이를 추론한다','시청자와 관찰자의 접근 범위를 구분한다','가로는 보존하고 세로는 0.1배 전달한다','가로 입력 거리 1은 출력 거리 1이다','세로 입력 거리 1은 출력 거리 0.1이다','입력 거리가 같아도 방향에 따라 출력 차이가 다르다','입력을 고정하고 행렬의 세로 배율만 줄인다','화면에서 겹쳐 보여도 좌표값은 다를 수 있다','정확한 출력 관측이면 0.001 차이도 구별한다','같은 x좌표의 세로 입력들은 같은 출력이 된다','동일한 출력에서는 해당 입력들을 구별할 수 없다','작아진 차이와 정확히 사라진 차이는 다르다','입력 차이는 모든 방향에 존재한다','s=0.1로 복귀해 입력 거리 1을 유지하며 방향만 바꾼다','출력 차이를 비교하는 방향별 지도를 질문한다']
manifest=[];start=0;script=[]
for i,(end,title,claim) in enumerate(zip(ends,titles,claims),1):
 d=R/f'scenes/{i:02d}';d.mkdir(parents=True,exist_ok=True)
 local=[r for r in records if start<=r['start']<end]
 text='\n\n'.join(r['text'] for r in local);script.append(text)
 pronunciation=text.replace('0.001','영 점 영 영 일').replace('0.01','영 점 영 일').replace('0.1','영 점 일').replace('10분의 1','십분의 일').replace('10배','열 배').replace('1만큼','일만큼').replace('0이','영이')
 (d/'script.txt').write_text(pronunciation+'\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02d} — {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('없음' if i==1 else claims[i-2])+f'\n\n## TTS 원문과 길이\n{text}\n\n사용자 발화시간: {start}–{end}초, 길이 {end-start}초. 음원 미제공.\n\n## 화면·타임라인·텍스트\n공통 scene_engine.py의 절대시간 실험 상태 사용. 상세 콘티: ../../storyboard_source.md 장면 {i:02d}. 입력/출력 축 단위 1.65 동일, 카메라 고정. 자막은 사용자 문장 시각으로 표시.\n\n## 시작·종료 상태\n절대시간 {start}초와 {end}초의 실험 상태를 독립 재현한다.\n\n## 다음 장면 연결\n같은 실험 화면을 유지하며 다음 주장으로 이동한다. 후속 영상 예고 문구 없음.\n\n## 정확성 조건\nA_s=diag(1,s), x_A=(0,0), x_B=(cosθ,sinθ). 출력 B=(cosθ,s sinθ). 0.001 확대는 별도 명시, 본 좌표 척도 불변. 배율 0에서 x좌표가 같은 점들만 겹친다. 115초부터 s=0.1.\n',encoding='utf-8')
 (d/'scene.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import ExperimentScene\nclass Scene"+f'{i:02d}'+f'(ExperimentScene):\n    start_time={start}\n    end_time={end}\n',encoding='utf-8')
 manifest.append(dict(id=f'{i:02d}',directory=f'scenes/{i:02d}',**{'class':f'Scene{i:02d}'},start=start,end=end,duration_seconds=end-start,title=title));start=end
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'tts_script.txt').write_text('\n\n'.join((R/m['directory']/'script.txt').read_text(encoding='utf-8').strip() for m in manifest)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: svd01_distinguish_inputs\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\nscenes:\n'+''.join(f"  - id: '{m['id']}'\n    directory: {m['directory']}\n    class: {m['class']}\n    duration_seconds: {m['duration_seconds']}\n" for m in manifest),encoding='utf-8')
print('26 supplied sentences; 16 independent scenes; duration',sum(m['duration_seconds'] for m in manifest))
