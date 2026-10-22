"""Approved narration and exact user sentence endpoints; prepare before visuals."""
from pathlib import Path
import json,textwrap,re,shutil
R=Path(__file__).resolve().parent
raw='''7|지난 실험에서 우리는 행렬이 한 방향의 차이를 완전히 지워버리면, 서로 다른 입력이 같은 출력으로 나타날 수 있다는 사실을 확인했습니다.
11|그렇다면 하나의 출력에 대응하는 입력은 얼마나 많을까요?
17|가로 방향의 값은 그대로 전달하고 세로 방향의 값은 완전히 지우는 행렬을 생각해보겠습니다.
22|입력 하나를 선택하고, 그 입력을 세로 방향으로 조금씩 움직여 보겠습니다.
25|입력의 위치는 계속 바뀌지만 출력은 변하지 않습니다.
30|세로 방향으로 얼마나 이동하든 가로 좌표가 같다면 결과는 항상 같습니다.
37|따라서 하나의 출력에 대응하는 입력은 두세 개가 아닙니다. 세로 방향으로 이어진 직선 전체가 같은 출력을 만들어냅니다.
39|왜 이런 일이 가능할까요?
44|처음 입력에 더해진 세로 방향의 변화가 행렬을 통과하면서 0이 되기 때문입니다.
49|이처럼 행렬을 통과했을 때 0이 되는 모든 입력 벡터들의 공간을 널 스페이스, Null Space라고 합니다.
54|널 스페이스에 속하는 벡터를 원래 입력에 더해도 출력은 달라지지 않습니다.
58|행렬은 그 방향으로 얼마나 움직였는지 구별할 수 없는 것입니다.
63|그렇다면 반대로, 행렬을 통과한 뒤에도 살아남는 독립적인 방향은 몇 개일까요?
65|3차원 공간을 생각해보겠습니다.
70|세 방향의 특잇값이 모두 0이 아니라면, 단위공은 부피를 가진 타원체로 변환됩니다.
76|한 방향의 특잇값이 0이 되면 출력은 평면 위에 놓이고, 두 방향이 사라지면 선분 위에만 남습니다.
80|이렇게 출력이 움직일 수 있는 독립적인 방향의 수가 랭크, Rank입니다.
85|에스브이디에서는 0이 아닌 특잇값의 개수를 세면 랭크를 알 수 있습니다.
87|이제 처음의 복원 문제로 돌아가 보겠습니다.
92|같은 출력을 만드는 입력이 무한히 많다면, 그중 무엇을 원래 입력이라고 선택해야 할까요?
96|출력만으로는 실제 입력이 무엇이었는지 알 수 없습니다.
100|하지만 가능한 입력들 가운데 하나를 선택하는 규칙은 만들 수 있습니다.
103|그중 하나가 의사역행렬, Pseudoinverse입니다.
110|의사역행렬은 0이 아닌 특잇값에 대해서는 역수를 적용하고, 0인 특잇값은 되돌리려 하지 않습니다.
117|그리고 주어진 출력을 정확히 만들어내는 입력이 존재한다면, 가능한 입력들 중 길이가 가장 짧은 것을 선택합니다.
124|정확히 일치하는 입력이 없다면 출력과의 오차를 최소화하고, 그런 입력들 중 길이가 가장 짧은 것을 선택합니다.
127|하지만 이것이 사라진 정보를 복원했다는 뜻은 아닙니다.
131|출력에 드러나지 않은 성분을 0으로 선택했을 뿐입니다.
133|그런데 여기서 생각을 반대로 바꿔보겠습니다.
137|지금까지는 행렬이 정보를 잃어버리는 상황을 문제로 생각했습니다.
141|그렇다면 우리가 일부 정보를 의도적으로 버리는 것은 어떨까요?
147|하나의 행렬을 에스브이디로 분해하면, 서로 다른 특잇값에 대응하는 여러 성분의 합으로 나타낼 수 있습니다.
152|이 가운데 큰 특잇값의 성분만 남기고 작은 성분들을 제거해 보겠습니다.
157|그러면 원래 행렬과 완전히 같지는 않지만, 더 적은 수의 성분으로 비슷한 행렬을 만들 수 있습니다.
161|이것이 저랭크 근사, Low-Rank Approximation입니다.
165|예를 들어 이미지의 픽셀 밝기를 하나의 행렬로 생각해보겠습니다.
169|가장 큰 특잇값의 성분 하나만 남기면 거친 명암 구조가 나타납니다.
176|두 개, 다섯 개, 열 개로 성분을 늘리면 원본 이미지의 윤곽과 세부적인 모습이 점차 돌아옵니다.
178|그런데 왜 가장 큰 특잇값부터 남겨야 할까요?
187|같은 랭크 이하의 행렬들 가운데, 큰 특잇값부터 남기는 절단 에스브이디가 원본과의 제곱 오차를 가장 작게 만들기 때문입니다.
191|버린 특잇값들의 제곱합이 바로 남은 제곱 오차가 됩니다.
195|하지만 이것이 모든 목적에서 가장 중요한 정보를 남긴다는 뜻은 아닙니다.
200|작은 특잇값에 대응하는 성분이 특정 문제에서는 결정적인 특징일 수도 있습니다.
205|에스브이디의 최적성은 우리가 어떤 오차를 최소화하려는지에 관한 수학적 결과입니다.
208|이제 처음의 질문으로 돌아가 보겠습니다.
211|서로 다른 두 입력을 행렬은 구별할 수 있을까요?
217|우리는 같은 크기의 입력 변화라도 방향에 따라 출력에서 다르게 나타난다는 사실을 발견했습니다.
224|그 차이를 가장 강하게, 가장 약하게 드러내는 방향을 찾았고, 그 방향들을 이용해 하나의 행렬곱을 분해했습니다.
231|작게 남은 차이는 복원할 때 오차를 증폭할 수 있었고, 완전히 사라진 차이는 출력만으로 되돌릴 수 없었습니다.
239|그리고 같은 구조를 거꾸로 활용하면, 어떤 성분을 버려야 정해진 랭크 안에서 원본과 가장 가까운 근사를 얻을 수 있는지도 알 수 있었습니다.
243|에스브이디는 단순히 행렬을 세 부분으로 나누는 공식이 아닙니다.
251|행렬이 입력의 어떤 차이를 드러내고, 어떤 차이를 지우며, 우리가 무엇을 복원하거나 포기할 수 있는지를 보여주는 하나의 수학적 지도입니다.'''
sentences=[];start=0
for row in raw.splitlines():
 end,body=row.split('|',1);end=int(end);sentences.append(dict(start=start,end=end,text=body));start=end
(R/'timing.json').write_text(json.dumps(dict(source='user_sentence_end_times',duration_seconds=251,sentences=sentences),ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02d}:{t%3600//60:02d}:{t%60:02d},000'
(R/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n"+'\n'.join(textwrap.wrap(s['text'],43)) for i,s in enumerate(sentences))+'\n',encoding='utf-8')
script='# 5편 — 사라진 정보는 복원할 수 있을까?\n\n사용자 확정 원문·종료 시각 251초. 음원 미제공.\n\n'+'\n\n'.join(f"## {s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)
for name in ['narration.md','master_script.md']:(R/name).write_text(script,encoding='utf-8')
ends=[11,17,25,37,44,54,58,65,76,85,96,103,110,117,124,131,141,152,161,176,187,191,205,217,224,231,239,251]
titles=['하나의 출력 여러 입력','세로 차이를 지우는 행렬','입력 이동과 고정된 출력','해 집합은 직선 전체','차이 벡터가 0이 된다','Null Space와 해 집합','관측 불가능한 방향','3차원으로 확장','타원체에서 원판과 선분으로','Rank는 살아남는 차원','원래 입력을 알 수 없다','하나를 선택하는 규칙','특잇값의 의사역수','가능한 해 중 최소 노름','최소제곱과 최소 노름','숨은 성분을 0으로 선택','이번에는 일부러 버린다','랭크 1 성분들의 합','더 적은 성분으로 근사','실제 계산한 이미지 SVD','같은 Rank 2 다른 오차','버린 특잇값의 제곱합','최적성은 목적에 달려 있다','처음의 두 점','방향을 찾고 행렬을 분해','약한 차이와 사라진 차이','손실을 활용하는 근사','하나의 수학적 지도']
claims=['A=diag(1,0), x=(1,t)의 출력은 모두(1,0)','가로 배율1, 세로 배율0을 명시','입력만 세로 이동하고 출력은 고정','해 집합은 x₀+ker(A), 끝없는 직선','원래 입력이 아니라 추가한 차이 v가 Av=0','원점을 지나는 ker(A)와 x=1의 해 집합을 구분','관측 불가능한 세로 자유도','실제 3차원 단위공과 직교 방향','채워진 타원체→원판→선분; 작은 값과 정확한0 구분','Rank는 0이 아닌 특잇값 개수','출력만으로 실제 입력을 특정할 수 없다','복원 대신 선택 규칙을 도입','σ>0은1/σ, σ=0은0; 1/0 계산 금지','정확해 중 길이가 최소인(1,0)','관측(1,0.3)은 치역 밖, 최소 잔차0.3과 최소 노름','숨은 성분0은 가정이 아닌 최소노름 선택','주어진 A와 새로 만드는 Aₖ 구분','실제 계산한6개 rank1 행렬 합','6개에서3개로 줄인 A₃와 잔차','같은 회색조 원본의 실제 rank1,2,5,10','σ=(8,4,2), 8·4유지는오차4, 8·2유지는16','Frobenius 제곱오차=버린σ의 제곱합','별도 검증표식은 작은직교성분, rank1에서사라짐','같은 거리 다른 방향의 출력 반응','입력·출력 특이방향과 배율을 연결','0.001의 오차증폭과0의 불가능성 구분','계산된 절단SVD 재사용','Vᵀ 읽기→Σ 배율→U 조립, 마지막2초 제목유지']
manifest=[];pron=[];start=0
for i,(end,title,claim) in enumerate(zip(ends,titles,claims),1):
 d=R/f'scenes/{i:02d}';d.mkdir(parents=True,exist_ok=True)
 body='\n\n'.join(s['text'] for s in sentences if start<=s['start']<end)
 tts=body.replace('Null Space','널 스페이스').replace('Pseudoinverse','슈도 인버스').replace('Low-Rank Approximation','로우 랭크 어프록시메이션').replace('Rank','랭크')
 for a,b in [('0.001','영 점 영 영 일'),('3차원','삼차원')]:tts=tts.replace(a,b)
 tts=re.sub(r'(?<![\d.])0(?![\d.])','영',tts)
 (d/'script.txt').write_text(tts+'\n',encoding='utf-8');pron.append(tts)
 engine='RankScene' if 8<=i<=10 else 'LossScene'
 (d/'scene.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import "+engine+f'\nclass Scene{i:02d}({engine}):\n    start_time={start}\n    end_time={end}\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02d} — {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('한 출력에 여러 입력이 가능하다는 질문' if i==1 else claims[i-2])+f'\n\n## TTS 원문과 확정 길이\n{body}\n\n사용자 종료 시각 {start}–{end}초, {end-start}초. 음원 미제공.\n\n## 화면 구성과 시간대별 애니메이션\n../../storyboard_source.md 장면{i:02d}. scene_engine.py의 해당 절대시간 상태를 독립 재현.\n\n## 화면 텍스트와 수학적 조건\n{claim}\n\n## 시작·종료 상태와 연결\n절대시간 {start}초에서 {end}초까지 동일 수치 모델로 진행. 다음 씬은 같은 경계 상태에서 재개. 사용자 대본 외 예고 없음.\n\n## 정확성·출처\n실제 NumPy SVD 계산. ../../assets/numerical_checks.json에 오차 검증, 이미지 출처는 ../../README.md 참조.\n',encoding='utf-8')
 manifest.append(dict(id=f'{i:02d}',directory=f'scenes/{i:02d}',**{'class':f'Scene{i:02d}'},start=start,end=end,duration_seconds=end-start,title=title));start=end
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'tts_script.txt').write_text('\n\n'.join(pron)+'\n',encoding='utf-8')
(R/'scenes.yaml').write_text('id: svd05_lost_information\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\nscenes:\n'+''.join(f"  - id: '{m['id']}'\n    directory: {m['directory']}\n    class: {m['class']}\n    duration_seconds: {m['duration_seconds']}\n" for m in manifest),encoding='utf-8')
for name in ['build.py','sync_preview.py']:
 s=(R.parent/'svd04_inverse_sensitivity'/name).read_text(encoding='utf-8').replace('svd04_','svd05_').replace('svd05_inverse_sensitivity_176s','svd05_lost_information_251s').replace('176*fps','251*fps').replace('-176)','-251)').replace('176 seconds','251 seconds')
 (R/name).write_text(s,encoding='utf-8')
shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\d0371cc5-2f35-41c2-9ad0-32b4ccfd72d2\붙여넣은 텍스트.txt'),R/'storyboard_source.md')
print(len(sentences),'sentences',len(manifest),'scenes',start,'seconds')
