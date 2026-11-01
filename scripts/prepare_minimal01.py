"""Create the approved 154-second episode; never infer narration timing."""
import json, shutil
from pathlib import Path

W=Path(__file__).resolve().parents[1]
P=W/'longforms/minimal01_preserve'
P.mkdir(exist_ok=True)
shutil.copytree(W/'longforms/_template',P,dirs_exist_ok=True)
rows=[
(2,'수백 개의 숫자가 나열되어 있습니다.'),
(7,'그런데 이 숫자들이 1과 2를 번갈아 반복하는 규칙으로 만들어졌다면 어떨까요?'),
(13,'우리는 숫자들을 하나씩 기록하는 대신, 1과 2를 반복한다는 규칙과 반복 횟수만 저장할 수 있습니다.'),
(17,'표현은 훨씬 짧아졌지만, 원래의 숫자들을 그대로 복원할 수 있습니다.'),
(21,'복잡해 보이는 대상도, 더 간단한 방법으로 표현할 수 있다는 뜻입니다.'),
(25,'그런데 우리는 왜 이렇게 작은 표현을 찾으려는 걸까요?'),
(32,'저장해야 할 정보를 줄이고, 계산에 필요한 자원을 아끼거나, 복잡한 구조 안에 숨어 있는 규칙을 발견할 수 있기 때문입니다.'),
(34,'하지만 여기에는 중요한 질문이 있습니다.'),
(36,'우리는 무엇을 그대로 유지해야 할까요?'),
(41,'최소 표현을 찾는 문제는 크게 두 가지 관점에서 생각할 수 있습니다.'),
(44,'첫 번째는 원래의 모든 정보를 정확하게 복원하는 것입니다.'),
(51,'앞서 숫자들의 반복 규칙을 저장한 것처럼, 표현을 줄이더라도 원래의 내용을 되찾을 수 있어야 합니다.'),
(54,'두 번째는 특정한 결과나 기능만 유지하는 것입니다.'),
(59,'원래의 모든 정보를 복원할 필요 없이, 우리가 원하는 결과만 같으면 되는 것이죠.'),
(62,'이 차이를 간단한 실험으로 살펴보겠습니다.'),
(65,'네 개의 지점이 정사각형 모양의 도로로 연결되어 있습니다.'),
(71,'우리가 원하는 조건이 모든 지점 사이를 이동할 수 있는 것이라면, 도로 하나를 제거해도 괜찮습니다.'),
(73,'여전히 모든 지점에 도달할 수 있기 때문입니다.'),
(77,'하지만 모든 지점 사이의 최단거리까지 유지해야 한다면 어떨까요?'),
(83,'도로 하나를 제거하는 순간, 원래 직접 연결되었던 두 지점은 다른 도로를 돌아가야 합니다.'),
(88,'같은 도로를 제거했지만, 어떤 조건에서는 문제가 없고 다른 조건에서는 문제가 발생합니다.'),
(91,'이번에는 동전을 열 번 던진 기록을 생각해 보겠습니다.'),
(97,'우리가 알고 싶은 것이 앞면이 나온 횟수뿐이라면, 열 번의 순서를 모두 저장할 필요는 없습니다.'),
(100,'앞면이 다섯 번 나왔다는 숫자 하나면 충분합니다.'),
(102,'그런데 질문을 바꿔 보겠습니다.'),
(106,'앞면이 가장 길게 연속해서 나온 횟수는 몇 번일까요?'),
(109,'앞면이 다섯 번 나왔다는 정보만으로는 답할 수 없습니다.'),
(114,'앞면이 다섯 번 연속으로 나왔을 수도 있고, 한 번씩 번갈아 나왔을 수도 있기 때문입니다.'),
(119,'같은 기록을 요약하더라도, 무엇을 알아내려는지에 따라 필요한 정보가 달라집니다.'),
(123,'이것이 최소 표현을 찾을 때 가장 먼저 생각해야 하는 조건입니다.'),
(127,'단순히 많은 것을 제거했다고 해서 좋은 표현이 되는 것은 아닙니다.'),
(132,'무엇을 보존할 것인지 먼저 정하고, 그 조건을 만족하는 더 작은 표현을 찾아야 합니다.'),
(138,'그리고 더 작은 표현을 발견했다는 사실이, 그것이 가능한 가장 작은 표현임을 의미하지는 않습니다.'),
(143,'우리가 아직 발견하지 못한 더 간단한 방법이 존재할 수도 있기 때문입니다.'),
(147,'결국 최소 표현을 찾는다는 것은 단순히 크기를 줄이는 일이 아닙니다.'),
(154,'무엇을 같다고 볼 것인지 정의하고, 그 같음을 유지하는 데 정말 필요한 것이 무엇인지 찾아내는 일입니다.'),
]
bounds=[0,17,34,41,51,59,65,73,83,88,100,114,123,132,143,154]
titles=['기록에서 규칙으로','작은 표현을 찾는 이유','무엇을 보존할까?','전체 정보 복원','특정 결과 보존','같은 네 지점','연결성은 유지된다','최단거리는 달라진다','같은 삭제, 다른 판단','열 번의 기록, 하나의 요약','같은 요약, 다른 답','질문이 필요한 정보를 정한다','조건부터 정하기','더 작음과 최소는 다르다','같음을 유지하는 데 필요한 것']
notes=['200개 숫자 = [1, 2] × 100. 원본은 짝수 길이이며 복원 가능.','짧은 표현이 계산을 항상 빠르게 하지는 않음.','전체 복원과 지정 기능 보존을 구분.','[1,2] × 3을 정확히 여섯 항으로 펼침.','1의 개수만 같아도 순서는 다를 수 있음.','네 도로는 모두 길이 1인 무방향 간선.','AB 삭제 후 A-D-C-B로 도달 가능.','같은 AB 삭제: 거리 1에서 3으로 변화.','구조는 같고 판단 조건만 다름.','HHHHHTTTTT 고정, H는 앞면.','A=HHHHHTTTTT, B=HTHTHTHTHT. 앞면 모두 5, 최대 연속 5와 1.','요약의 충분성은 질문에 의존. 통계적 충분성 정리로 확대하지 않음.','정확한 보존 사례이며 근사와 혼동하지 않음.','100→30은 가상 예시. 미지 후보를 발견 결과처럼 제시하지 않음.','다음 편 예고 없이 현재 질문으로 완결.']
timing=[];start=0
for end,body in rows:
 timing.append(dict(start=start,end=end,text=body));start=end
(P/'narration_timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):
 return f'{int(t)//3600:02}:{int(t)//60%60:02}:{int(t)%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(timing))+'\n',encoding='utf-8')
manifest=[];narr=[];tts=[]
for i,(a,b,title,note) in enumerate(zip(bounds,bounds[1:],titles,notes),1):
 d=P/f'scenes/{i:02}';d.mkdir(parents=True,exist_ok=True)
 lines=[r['text'] for r in timing if a<=r['start']<b]
 script='\n\n'.join(lines)
 (d/'script.txt').write_text(script+'\n',encoding='utf-8')
 (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import PreserveScene\nclass Scene{i:02}(PreserveScene):\n    index={i-1}\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02} · {title}\n\n## 목적·주장\n{note}\n\n## 앞 장면과 연결\n절대 시각 {a}–{b}초. 이전 종료 상태를 이어받되 독립 렌더 가능. 다음 씬은 같은 대상 또는 같은 보존 질문으로 연결하며 복습·예고 없음.\n\n## TTS 원문\n{script}\n\n- 확정 구간 길이: {b-a}초. 사용자 문장 종료 시각 기준. 음원 미제공.\n\n## 화면·애니메이션\nscene_engine.py의 part_{i-1:02} 참조. 모든 변화는 해당 함수의 절대 시각 at()에 맞춤. 세로와 가로는 같은 데이터, 별도 배치 사용.\n\n## 화면 텍스트\n제목: {title}. 보존=청록, 제거=빨강, 조건=노랑. 전체 발화는 하단 자막.\n\n## 시작·종료 상태\n함수 초기 배치에서 시작해 해당 보존 결과로 종료. 도로 65–88초는 동일 좌표·AB 삭제 상태를 유지.\n\n## 정확성·과장 방지\n{note}\n\n## 길이 제한\n마지막 발화 종료 154초에서 종료. 임의 정적 추가 없음.\n',encoding='utf-8')
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title))
 narr.append(f'## {a:03}–{b:03}s · {title}\n\n'+script)
 tts.append(script)
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'narration.md').write_text('# 모든 것이 필요할까? 01 — 최소 표현의 조건\n\n사용자 확정 원문·문장 종료 시각 154초.\n\n'+'\n\n'.join(narr)+'\n',encoding='utf-8')
(P/'master_script.md').write_text((P/'narration.md').read_text(encoding='utf-8'),encoding='utf-8')
(P/'tts_script.txt').write_text('\n\n'.join(tts).replace('1과 2','일과 이')+'\n',encoding='utf-8')
(P/'scenes.yaml').write_text('id: minimal01_preserve\ntitle: 모든 것이 필요할까? — 최소 표현의 조건\nvideo:\n  fps: 30\n  variants:\n    shorts: [1080, 1920]\n    longform: [1920, 1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
(P/'brief.md').write_text('# 제작 기준\n\n154초, 사용자 확정 문장 종료 시각 36개를 그대로 적용. 세로 1080×1920 및 가로 1920×1080, 30fps. 무음, 전체 발화 자막 내장 및 SRT 별도.\n\n숫자 200개→반복 규칙→복원, 전체 복원/특정 결과 보존, 도로 연결성과 최단거리, 동전 앞면 횟수와 최대 연속, 작은 후보와 최소성 구분.\n\n첨부 콘티의 도로 제거·조건 변경 시각보다 실제 발화 시각 우선: 65–73초 연결성, 73–83초 최단거리. 마지막 정적은 154초 안에서만 허용.\n\n도로 네 간선 길이 모두 1. 동전 A=HHHHHTTTTT, B=HTHTHTHTHT. 가상 100→30은 화면에 가상 예시라고 명시. 반복 규칙 자체의 최소 비트 길이나 보편적 최소성은 주장하지 않는다.\n',encoding='utf-8')
example=P/'scenes/01_example'
# Remove only the untouched copied template example inside this episode.
if example.exists():
 assert example.resolve().is_relative_to(P.resolve())
 shutil.rmtree(example)
print(P)

