from pathlib import Path
import json,textwrap,re
R=Path('longforms/svd04_inverse_sensitivity')
raw='''6|지난 실험에서는 하나의 입력을 여러 방향의 성분으로 나누고, 각 성분에 특잇값을 곱해 출력을 만들었습니다.
9|그렇다면 이번에는 그 과정을 거꾸로 되돌려보겠습니다.
16|입력은 보이지 않고, 행렬과 출력만 알고 있다고 가정하겠습니다. 우리는 이 출력으로부터 원래 입력을 알아내야 합니다.
20|먼저 한 방향의 성분이 1인 입력을 생각해보겠습니다.
26|행렬이 이 방향을 0.001배로 줄인다면, 출력에 남는 성분은 0.001입니다.
34|행렬이 이 방향을 얼마나 압축했는지 알고 있으므로, 정확한 출력값을 얻었다면 0.001로 나누어 원래 성분 1을 복원할 수 있습니다.
41|입력의 차이가 아주 작게 전달되었더라도, 정확히 0이 아니라면 수학적으로는 그 차이를 되돌릴 수 있는 것입니다.
44|그런데 우리가 관찰한 출력이 정확하지 않다면 어떨까요?
50|실제 출력은 0.001이지만, 측정 과정에서 0.0001의 오차가 더해졌다고 생각해보겠습니다.
53|관찰자가 얻은 값은 0.0011입니다.
58|원래 성분을 복원하려면 이 값도 0.001로 나누어야 합니다.
60|그 결과는 1.1입니다.
64|원래 입력 성분은 1이었지만, 복원한 값은 1.1이 되었습니다.
70|출력에서는 0.0001에 불과했던 절대 오차가, 입력을 복원한 뒤에는 0.1로 커진 것입니다.
72|왜 이런 일이 일어났을까요?
78|역변환은 출력에 남아 있는 값이 원래 신호인지, 측정 과정에서 더해진 오차인지 구분하지 못합니다.
85|행렬이 0.001배로 줄였던 방향을 복원하기 위해 1000배 확대하면, 그 방향에 포함된 오차도 똑같이 1000배 확대됩니다.
91|그렇다면 모든 방향을 0.001배로 줄이는 행렬도 똑같이 불안정한 걸까요?
93|여기에는 중요한 차이가 있습니다.
98|모든 방향이 같은 비율로 줄어든다면, 복원할 때 모든 방향을 같은 비율로 확대합니다.
107|반대로 한 방향은 그대로 전달하고 다른 방향만 0.001배로 줄인다면, 출력의 오차가 어느 방향에 놓였는지에 따라 복원 결과가 크게 달라집니다.
114|입력의 두 방향은 처음에 같은 크기의 차이를 가지고 있었지만, 출력에서는 1000배나 다른 크기로 나타납니다.
123|이처럼 행렬이 방향마다 서로 다른 배율을 가지면, 출력의 작은 상대적인 변화가 복원된 입력에서는 훨씬 큰 상대적인 변화로 나타날 수 있습니다.
126|이 차이를 판단하는 기준이 조건수, Condition Number입니다.
134|역행렬이 존재하는 정사각행렬에서, 2-노름 기준 조건수는 가장 큰 특잇값을 가장 작은 특잇값으로 나눈 값입니다.
140|가장 큰 특잇값이 1이고 가장 작은 특잇값이 0.001이라면 조건수는 1000입니다.
144|여기서 조건수 1000이 모든 오차를 반드시 1000배 확대한다는 뜻은 아닙니다.
153|입력과 출력의 상대적인 오차를 비교했을 때, 특정 방향의 오차가 얼마나 민감하게 작용할 수 있는지를 나타내는 최악의 경우에 대한 기준입니다.
156|그런데 아직 한 가지 질문이 남아 있습니다.
161|특잇값이 0.001처럼 아주 작은 것이 아니라, 정확히 0이라면 어떻게 될까요?
163|그 방향의 차이는 출력에서 완전히 사라집니다.
166|이제는 오차를 얼마나 확대하는지가 문제가 아닙니다.
170|되돌려야 할 차이 자체가 출력에 남아 있지 않기 때문입니다.
176|그렇다면 하나의 출력에 서로 다른 입력들이 대응할 때, 우리는 무엇을 복원할 수 있을까요?'''
sentences=[];start=0
for line in raw.splitlines():
 end,body=line.split('|',1);end=int(end);sentences.append(dict(start=start,end=end,text=body));start=end
(R/'timing.json').write_text(json.dumps(dict(source='user_sentence_end_times',duration_seconds=176,sentences=sentences),ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02d}:{t%3600//60:02d}:{t%60:02d},000'
(R/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n"+'\n'.join(textwrap.wrap(s['text'],43)) for i,s in enumerate(sentences))+'\n',encoding='utf-8')
(R/'narration.md').write_text('# 4편 — 출력에 남은 정보를 되돌리면 왜 오차가 커질까?\n\n사용자 원문과 문장 종료 시각 기준176초. 음원 미제공.\n\n'+'\n\n'.join(f"## {s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences),encoding='utf-8')
ends=[9,16,26,34,41,53,60,70,78,85,93,98,107,114,126,140,153,161,170,176]
titles=['순방향에서 역방향으로','알고 있는 것과 모르는 것','새 행렬과 작은 출력','정확한 출력 복원','작은 값은 0이 아니다','오차가 섞인 관측값','같은 역변환 두 경로','복원된 절대 오차','신호와 오차를 구분하지 못한다','절대 오차가 1000배','균일 압축과 비균일 압축','동일한 역배율','방향별 절대 오차 차이','같은 입력 거리 다른 출력','상대 오차가 커지는 별도 사례','조건수의 정의','모든 오차가 최악인 것은 아니다','0.001에서 정확히 0으로','출력에 차이가 남지 않는다','하나의 출력 여러 입력']
claims=['이전 계산 흐름을 역방향 질문으로 바꾼다','행렬과 출력만 알고 입력은 모른다','16초에 A=diag(1,0.001)로 전환, x=(0,1)','정확한 출력0.001을0.001로 나누면1이다','0.001은0이 아니므로 이 가역 예시에서는 정확 복원이 가능하다','출력0.001에0.0001 오차를 더하면0.0011','관측값에도 같은÷0.001을 적용하면1.1','절대 출력 오차0.0001이 절대 입력 오차0.1이 된다','역변환은 신호와 오차에 동일하게 작용한다','절대증폭1000배, 이 실험의 상대오차는 출력과 입력 모두10%','A₁=0.001I와 A₂=diag(1,0.001)를 비교한다','A₁은 모든 방향의 역배율이1000이다','A₂의 같은 절대 출력 오차도 방향에 따라×1 또는×1000','단위 입력의 반응은 가로1, 세로0.001이다','새 기준 x=y=(1,0), 세로δy=(0,0.001)에서 상대0.1%→100%','가역 정사각행렬의2-노름 조건수는최대/최소 특잇값','같은 y와 같은 오차크기에서 가로상대증폭1, 세로1000','161초에 정확히 A₀=diag(1,0)로 전환한다','x₁=(1,0),x₂=(1,1)의 출력은 모두(1,0)','x=(1,t) 전체가 같은 출력에 대응한다']
manifest=[];start=0;pron=[]
for i,(end,title,claim) in enumerate(zip(ends,titles,claims),1):
 d=R/f'scenes/{i:02d}';d.mkdir(parents=True,exist_ok=True)
 body='\n\n'.join(s['text'] for s in sentences if start<=s['start']<end)
 words={'0.0001':'영 점 영 영 영 일','0.0011':'영 점 영 영 일 일','0.001':'영 점 영 영 일','0.1':'영 점 일','1.1':'일 점 일','1000':'천','2-노름':'이 노름','Condition Number':'컨디션 넘버'}
 tts=body
 for a,b in words.items():tts=tts.replace(a,b)
 tts=re.sub(r'(?<![\d.])1(?![\d.])','일',tts);tts=re.sub(r'(?<![\d.])0(?![\d.])','영',tts)
 (d/'script.txt').write_text(tts+'\n',encoding='utf-8');pron.append(tts)
 (d/'scene.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import InverseScene\n"+f'class Scene{i:02d}(InverseScene):\n    start_time={start}\n    end_time={end}\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02d} — {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('3편의 방향별 계산 구조' if i==1 else claims[i-2])+f'\n\n## TTS 원문과 확정 길이\n{body}\n\n사용자 종료 시각 기준 {start}–{end}초, {end-start}초. 음원 미제공.\n\n## 화면·타임라인\n../../storyboard_source.md 장면{i:02d}. scene_engine.py의 동일 절대시간 상태를 독립 재현한다. 입력·출력은 동일 척도이고 확대는 별도 프레임으로 구분한다.\n\n## 화면 텍스트\n{title}. 정확한 수치와 수식은 ../../README.md 참조.\n\n## 시작·종료 상태\n절대시간{start}초와{end}초의 실험 상태를 연속해서 이어간다.\n\n## 다음 장면 연결\n절대오차→방향별 차이→상대오차→조건수→완전한 소실로 전개한다. 사용자 원문 외의 예고는 추가하지 않는다.\n\n## 정확성 조건\n16초 새 행렬,85초 두 행렬 비교,114초 별도 상대오차 사례,161초 정확히0인 행렬. 0.001을0으로 그리거나 조건수를 모든 절대오차의 증폭률로 표현하지 않는다.\n',encoding='utf-8')
 manifest.append(dict(id=f'{i:02d}',directory=f'scenes/{i:02d}',**{'class':f'Scene{i:02d}'},start=start,end=end,duration_seconds=end-start,title=title));start=end
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'tts_script.txt').write_text('\n\n'.join(pron)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: svd04_inverse_sensitivity\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\nscenes:\n'+''.join(f"  - id: '{m['id']}'\n    directory: {m['directory']}\n    class: {m['class']}\n    duration_seconds: {m['duration_seconds']}\n" for m in manifest),encoding='utf-8')
for name in ['build.py','sync_preview.py']:
 s=(Path('longforms/svd03_read_and_reassemble')/name).read_text(encoding='utf-8-sig').replace('svd03_','svd04_').replace('svd04_read_and_reassemble_152s','svd04_inverse_sensitivity_176s').replace('152*fps','176*fps').replace('-152)','-176)').replace('152 seconds','176 seconds');(R/name).write_text(s,encoding='utf-8')
print(len(sentences),'sentences;',len(manifest),'scenes;',sum(s['duration_seconds'] for s in manifest),'seconds')
