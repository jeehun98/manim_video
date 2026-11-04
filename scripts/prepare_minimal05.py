from pathlib import Path
import json,shutil
r=Path('longforms/minimal05_realization');old=Path('longforms/minimal04_sufficiency/revisions/v2_intuition_158s')
for name in ['build.py','caption_pass.py','inspect_frames.py','verify_caption_boundaries.py']:
 s=(old/name).read_text(encoding='utf-8').replace('ROOT.parents[3]','ROOT.parents[1]').replace('minimal04_v2_158s','minimal05_154s').replace('minimal04_v2','minimal05').replace('158','154').replace('4740','4620').replace('4739','4619')
 if name=='inspect_frames.py':s=s.replace('2,5,17,24,32,39,45,48,54,60,66,72,79,85,89,94,103,120,141,156','3,9,18,27,36,43,50,57,64,69,78,87,94,102,111,120,128,137,145,152')
 if name=='verify_caption_boundaries.py':s=s.replace('[779,780,781,2489,2490,2491,2699,2700,2701,3659,3660,3661]','[989,990,991,1409,1410,1411,3149,3150,3151,3899,3900,3901]')
 (r/name).write_text(s,encoding='utf-8')
raw='''6|어떤 시스템에 내부 상태가 두 개 있다면, 그 시스템을 설명하는 데도 반드시 두 개의 상태가 필요할까요?
11|예를 들어 외부에서 입력을 받으면 움직이고, 그 결과를 출력하는 시스템을 생각해 보겠습니다.
16|시스템 내부에는 두 개의 상태, 엑스 원과 엑스 투가 있습니다.
21|두 상태는 입력을 받으면 같은 방식으로 변화하고, 출력은 두 상태를 더한 값으로 결정됩니다.
24|그런데 여기서 이상한 점이 발견됩니다.
30|우리가 외부에서 관찰하는 것은 두 상태 각각의 값이 아니라, 두 상태의 합이라는 것입니다.
33|그렇다면 두 상태를 따로 추적할 필요가 있을까요?
35|새로운 상태 제트를 정의해 보겠습니다.
38|제트는 엑스 원과 엑스 투를 더한 값입니다.
41|이제 원래 두 상태의 변화 방정식을 더해 보겠습니다.
45|그러면 제트의 변화는 제트 자신과 입력만으로 표현됩니다.
47|출력 역시 제트 하나로 결정됩니다.
54|원래는 두 개의 상태를 가진 시스템이었지만, 이제 하나의 상태만으로 동일한 출력 변화를 재현할 수 있습니다.
61|실제로 두 시스템에 같은 입력을 주면, 같은 초기 출력에서 출발하는 한 시간에 따른 출력도 정확히 일치합니다.
65|여기서 중요한 것은 단순히 상태 하나를 삭제한 것이 아니라는 점입니다.
71|두 상태를 결합해 새로운 상태를 만들었고, 그 상태만으로 외부 동작을 설명할 수 있게 된 것입니다.
76|이것이 제어이론에서 다루는 최소 실현, Minimal Realization의 핵심 아이디어입니다.
82|시스템의 외부 입출력 관계를 유지하면서, 이를 표현하는 데 필요한 상태 차원을 최소화하는 것입니다.
86|그렇다면 어떤 상태가 정말 필요한지는 어떻게 판단할까요?
89|여기에는 두 가지 중요한 개념이 등장합니다.
92|첫 번째는 제어 가능성, Controllability입니다.
97|외부 입력을 이용해 시스템의 상태를 원하는 방향으로 움직일 수 있는지를 나타냅니다.
100|두 번째는 관측 가능성, Observability입니다.
105|시스템의 출력을 관찰해서 서로 다른 내부 상태를 구별할 수 있는지를 나타냅니다.
108|앞의 예시에서는 두 상태의 차이를 생각해 볼 수 있습니다.
114|엑스 원에서 엑스 투를 뺀 값은 외부 입력으로 변화시킬 수 없고, 출력에도 나타나지 않습니다.
118|반면 두 상태의 합은 입력에 반응하고 출력에도 직접 나타납니다.
124|따라서 외부 입출력 동작을 재현하려면 합에 해당하는 상태 하나만 남기면 됩니다.
130|선형 시불변 시스템에서는 제어 가능성과 관측 가능성을 모두 만족하는 실현이 최소 실현입니다.
135|다만 여기서 보존하는 것은 일반적으로 초기 상태를 영으로 둔 입력과 출력의 관계입니다.
141|모든 내부 상태를 복원하거나, 임의의 초기 상태까지 같은 방식으로 표현한다는 뜻은 아닙니다.
146|결국 시스템 내부에 존재하는 모든 변수가 외부 동작을 설명하는 데 필요한 것은 아닙니다.
154|중요한 것은 상태를 몇 개 가지고 있느냐가 아니라, 동일한 입출력 관계를 유지하기 위해 최소 몇 개의 독립적인 상태가 필요한가입니다.'''
rows=[];st=0
for line in raw.splitlines():
 en,text=line.split('|',1);en=int(en);rows.append(dict(start=st,end=en,text=text));st=en
(r/'narration_timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
def ts(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
(r/'captions.srt').write_text('\n\n'.join(f'{i}\n{ts(x["start"])} --> {ts(x["end"])}\n{x["text"]}' for i,x in enumerate(rows,1))+'\n',encoding='utf-8')
bounds=[0,11,24,33,41,47,61,71,82,89,97,105,114,124,130,141,154]
titles=['상태가 둘이면, 둘 다 필요할까?','같은 입력, 같은 변화 법칙','외부에서 보이는 것은 합','두 상태를 하나로 표현하기','새 상태만으로 변화를 설명한다','상태 수가 달라도 출력은 같다','지운 것이 아니라 결합한 것','동작을 유지하는 가장 작은 상태','어떤 상태가 정말 필요할까?','입력으로 움직일 수 있는가?','출력으로 구별할 수 있는가?','차이는 입력과 출력에 숨는다','합은 입력과 출력을 연결한다','최소 실현을 판단하는 두 조건','무엇을 같게 보존하는가?','필요한 독립 상태는 몇 개인가?']
claims=['상태 수와 필요한 표현 차원은 다를 수 있다','동일한 입력을 받는 두 1차 상태의 합이 출력이다','같은 합을 갖는 서로 다른 상태는 출력으로 구별되지 않는다','z=x₁+x₂로 상태를 결합한다','ż=−z+2u와 y=z로 닫힌 표현을 얻는다','같은 입력 및 대응 초기 상태에서 독립 계산한 출력이 일치한다','단순한 원래 변수 삭제가 아닌 상태 변환이다','최소 실현은 입출력 관계를 유지하는 최소 상태 차원이다','입력과 출력의 관점으로 상태 방향을 살펴본다','입력으로 도달할 수 있는 상태 방향을 구분한다','출력 궤적으로 구별할 수 있는 상태 방향을 구분한다','d=x₁−x₂는 입력항 없이 감쇠하고 출력에 나타나지 않는다','z 방향은 입력에 반응하며 출력에 직접 나타난다','유한차원 LTI 실현은 제어 가능하고 관측 가능할 때 최소이다','일반적 기준은 영 초기 상태의 입출력 관계이다','내부 변수 수와 최소 독립 상태 차원을 구별한다']
manifest=[];blocks=[]
for i,(st,en,title,claim) in enumerate(zip(bounds,bounds[1:],titles,claims)):
 folder=r/'scenes'/f'{i+1:02}';folder.mkdir(parents=True,exist_ok=True);rr=[x for x in rows if st<=x['start']<en];script='\n'.join(x['text'] for x in rr);blocks.append(script)
 (folder/'script.txt').write_text(script+'\n',encoding='utf-8')
 (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import RealizationScene\nclass Scene{i+1:02}(RealizationScene):\n    index={i}\n',encoding='utf-8')
 (folder/'spec.md').write_text(f'# {i+1:02} · {title}\n\n## 목적과 주장\n\n{claim}\n\n## 앞 장면에서 받은 내용\n\n'+('없음' if i==0 else claims[i-1])+f'\n\n## 확정 TTS\n\n- 사용자 제공 구간 {st}–{en}초, 길이 {en-st}초.\n- 음원 미제공: 위 시각을 실제 발화 기준으로 사용, 무음 영상과 TTS 원고 제공.\n\n{script}\n\n## 화면과 시간\n\n'+ '\n'.join(f'- {x["start"]}–{x["end"]}초: {x["text"]}' for x in rr)+'\n\n세로와 가로를 각각 배치. 입력 u 청록, x₁·x₂ 파랑, z·y 노랑, d 빨강. 축과 수식, 실제 모델 계산을 일치시킨다.\n\n## 시작과 종료\n\n첫 문장의 핵심 대상을 받아 마지막 문장의 주장으로 완료. 주요 상태 변환은 두 블록→z, 곡선 비교는 같은 축에서 중첩.\n\n## 다음 장면의 시각적 연결\n\n동일한 시스템과 색상 유지. 영상 내 복습·다음 편 예고 없음.\n\n## 정확성\n\nẋ₁=−x₁+u, ẋ₂=−x₂+u, y=x₁+x₂; ż=−z+2u; ḋ=−d. 차이는 정지 상태가 아니라 자율 감쇠한다. 합과 차이 축은 (1,1), (1,−1)로 직교. 일반 최소 실현은 영 초기 입출력 기준, 이번 예시의 더 강한 초기 출력 일치와 구분한다.\n',encoding='utf-8')
 manifest.append(dict(id=f'{i+1:02}',directory=f'scenes/{i+1:02}',**{'class':f'Scene{i+1:02}'},start=st,end=en,duration_seconds=en-st,title=title))
(r/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(r/'scenes.yaml').write_text('duration_seconds: 154\nlayouts: [9:16, 16:9]\nscenes:\n'+'\n'.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    title: {m["title"]}\n    start: {m["start"]}\n    end: {m["end"]}\n    duration_seconds: {m["duration_seconds"]}' for m in manifest)+'\n',encoding='utf-8')
for name in ['narration.md','master_script.md']:(r/name).write_text('# 최소 실현 — 154초 확정 대본\n\n'+'\n\n'.join(f'## {m["start"]}–{m["end"]}초 · {m["title"]}\n\n{b}' for m,b in zip(manifest,blocks))+'\n',encoding='utf-8')
(r/'tts_script.txt').write_text('\n\n'.join(x['text'] for x in rows).replace('Minimal Realization','미니멀 리얼라이제이션').replace('Controllability','컨트롤러빌리티').replace('Observability','옵저버빌리티')+'\n',encoding='utf-8')
(r/'brief.md').write_text('# 05 최소 실현 제작 기준\n\n사용자 확정 대본·33개 종료 시각·총154초. 핵심은 두 상태 결합→닫힌 1차 방정식→실제 출력 일치, 이후 합/차이 방향으로 설명. 원래 시스템과 축소 시스템을 독립 적분하고 수치 검증한다. 외부 입력은 구간별 일정한 파형이며 초기 상태 (1.5,.5), z₀=2. 제어·관측 가능성 모두 충족하는 1차 LTI 실현의 최소성. 일반 동등성의 영 초기 상태 기준과 본 예시의 대응 초기값 일치를 명확하게 구분. 단일 ASS 자막으로 전환 중복 방지. 음원 없이 무음 세로·가로 최종본.\n',encoding='utf-8')
shutil.copy2(Path(r'C:/Users/as042/.codex/attachments/d27c009c-0a75-44ff-9985-fa76e8ad116b/붙여넣은 텍스트.txt'),r/'storyboard_user.md')
if (r/'scenes/01_example').exists():
 for f in (r/'scenes/01_example').iterdir():f.unlink()
 (r/'scenes/01_example').rmdir()
print('Prepared',len(rows),'sentences,',len(manifest),'scenes')
