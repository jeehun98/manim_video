from pathlib import Path
import json,shutil
r=Path('longforms/minimal07_lottery');old=Path('longforms/minimal06_universality')
for name in ['build.py','caption_pass.py','inspect_frames.py','verify_caption_boundaries.py']:
 s=(old/name).read_text(encoding='utf-8').replace('minimal06','minimal07').replace('160','170').replace('4800','5100').replace('4799','5099')
 if name=='caption_pass.py':s=s.replace('(540,1708)','(540,1608)') # Preserve the reserved caption position; 1608 is not a duration.
 if name=='inspect_frames.py':s=s.replace('3,13,18,30,41,49,54,59,68,74,79,87,96,102,109,115,121,132,139,157','3,9,15,23,30,37,45,61,72,82,85,90,97,107,112,125,131,141,153,167')
 if name=='verify_caption_boundaries.py':s=s.replace('[1679,1680,1681,1919,1920,1921,2429,2430,2431,3149,3150,3151]','[2579,2580,2581,2819,2820,2821,3029,3030,3031,3689,3690,3691]')
 (r/name).write_text(s,encoding='utf-8')
raw='''4|지금까지 우리는 서로 다른 분야에서 하나의 질문을 던졌습니다.
5|모든 것이 정말 필요할까요?
11|그래프에서는 수많은 연결을 제거해도 연결성이나 특정 수학적 성질을 유지할 수 있었습니다.
18|생명체에서는 어떤 유전자가 필수적인지 살펴봤지만, 그 답은 생존 환경과 다른 유전자들의 존재에 따라 달라졌습니다.
26|통계학에서는 수많은 데이터를 하나의 숫자로 줄이더라도, 특정 모수를 추론하는 데 필요한 정보를 모두 보존할 수 있었습니다.
33|제어이론에서는 여러 내부 상태를 하나의 새로운 상태로 표현하면서도 동일한 입출력 동작을 유지할 수 있었습니다.
39|그리고 물리학에서는 미시적인 구조가 다른 물질들이 같은 거시적 법칙을 공유할 수 있다는 사실을 살펴봤습니다.
43|이 사례들은 서로 다른 문제를 다루지만, 공통된 질문을 남깁니다.
47|우리가 원하는 결과를 유지하기 위해, 실제로 무엇이 필요한가?
51|이제 이 질문을 인공지능의 신경망에 적용해 보겠습니다.
57|신경망에는 수많은 뉴런과 연결이 존재하고, 학습 과정에서 각 연결의 가중치가 조정됩니다.
59|그렇다면 이 연결들이 모두 필요할까요?
65|큰 신경망을 학습한 다음 일부 연결을 제거해도, 성능이 크게 떨어지지 않는 경우가 있습니다.
68|하지만 여기서 더 흥미로운 질문이 생깁니다.
75|학습을 마친 신경망에서 연결을 제거하는 것이 아니라, 처음부터 그 작은 신경망만 학습해도 같은 성능에 도달할 수 있을까요?
80|2018년 발표된 복권 가설, Lottery Ticket Hypothesis는 바로 이 질문을 다룹니다.
84|먼저 많은 연결을 가진 신경망을 무작위로 초기화합니다.
86|그리고 전체 신경망을 학습시킵니다.
92|학습이 끝나면 일부 연결을 제거하고, 남은 연결만으로 이루어진 작은 신경망을 선택합니다.
94|그런데 여기서 특이한 작업을 수행합니다.
101|남아 있는 가중치들을 학습이 끝난 값으로 유지하는 것이 아니라, 학습을 시작하기 전의 초기값으로 되돌리는 것입니다.
104|이제 선택된 연결만 다시 학습시킵니다.
114|놀랍게도 특정 조건에서는 이렇게 얻은 작은 신경망이 원래의 큰 신경망에 필적하는 성능을 달성하고, 비슷하거나 더 적은 학습 반복으로 목표 성능에 도달할 수 있습니다.
117|이러한 부분 신경망을 위닝 티켓, Winning Ticket이라고 부릅니다.
121|그렇다면 중요한 것은 단순히 어떤 연결을 남겼는가일까요?
123|반드시 그렇지는 않습니다.
129|같은 연결 구조를 유지하더라도, 가중치를 새롭게 무작위 초기화하면 학습 결과가 달라질 수 있습니다.
135|즉, 어떤 연결을 선택했는지뿐 아니라, 그 연결들이 어떤 초기값에서 출발하는지도 중요할 수 있습니다.
139|물론 이것이 모든 신경망에서 대부분의 연결을 제거할 수 있다는 뜻은 아닙니다.
144|또한 작은 신경망을 찾기 위해 먼저 큰 신경망을 학습해야 할 수도 있습니다.
149|복권 가설이 보여주는 것은 단순히 신경망을 압축할 수 있다는 사실만이 아닙니다.
158|큰 신경망의 학습 능력이 모든 연결에 고르게 의존하는 것은 아닐 수 있으며, 특정한 연결 구조와 초기 조건의 조합이 중요한 역할을 할 수 있다는 것입니다.
161|그렇다면 신경망의 크기는 무엇으로 결정해야 할까요?
167|연결의 개수일까요, 아니면 실제로 학습에 필요한 독립적인 자유도의 수일까요?
170|신경망에서 무엇이 정말 필요한지에 대한 질문은 이제 시작입니다.'''
rows=[];st=0
for line in raw.splitlines():
 en,t=line.split('|',1);en=int(en);rows.append(dict(start=st,end=en,text=t));st=en
(r/'narration_timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
def ts(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
(r/'captions.srt').write_text('\n\n'.join(f'{i}\n{ts(x["start"])} --> {ts(x["end"])}\n{x["text"]}' for i,x in enumerate(rows,1))+'\n',encoding='utf-8')
bounds=[0,5,11,18,26,33,39,51,65,80,86,101,117,135,144,158,170]
titles=['모든 것이 정말 필요할까?','연결을 줄여도 남는 성질','필수성은 조건에 따라 달라진다','추론에 필요한 정보를 남긴다','같은 동작을 더 적은 상태로','다른 구조가 공유하는 법칙','이제, 신경망에서는?','수많은 연결이 모두 필요할까?','작은 신경망만 처음부터 학습한다면','무작위 초기값을 저장한다','남은 연결을 원래 초기값으로','선택된 연결만 다시 학습한다','같은 연결 구조, 다른 초기값','가능한 범위와 발견 비용','구조와 초기 조건의 조합','신경망에 필요한 자유도는?']
claims=['여러 분야의 보존 질문을 환기한다','트리로 연결성을 보존할 수 있다','필수 유전자는 환경·다른 유전자에 의존한다','알려진 분산의 독립 정규모형에서 표본평균은 평균에 충분하다','닫힌 합 상태로 동일한 출력 동작을 표현할 수 있다','같은 보편성 부류에서 임계 법칙을 공유할 수 있다','원하는 결과의 보존 질문을 신경망으로 옮긴다','학습 후 일부 가중치를 제거할 수 있다','학습 후 가지치기와 초기값 복원 후 재학습은 다른 실험이다','전체 학습 전 W0를 따로 보존한다','마스크를 고정하고 남은 가중치를 M⊙W0로 되돌린다','남은 연결만 학습하고 동일 조건의 성능·반복 수를 비교한다','같은 마스크에서도 다른 초기값은 다른 학습 경로를 만든다','보편적 극단 압축이나 탐색 비용 제거를 증명하지 않는다','연결 구조와 초기 조건의 조합이 학습에 중요할 수 있다','연결 수와 독립 자유도는 다른 질문이며 최소 자유도를 증명한 것은 아니다']
manifest=[]
for i,(st,en,title,claim) in enumerate(zip(bounds,bounds[1:],titles,claims)):
 f=r/'scenes'/f'{i+1:02}';f.mkdir(parents=True,exist_ok=True);rr=[x for x in rows if st<=x['start']<en];script='\n'.join(x['text'] for x in rr)
 (f/'script.txt').write_text(script+'\n',encoding='utf-8');(f/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import LotteryScene\nclass Scene{i+1:02}(LotteryScene):\n    index={i}\n',encoding='utf-8')
 (f/'spec.md').write_text(f'# {i+1:02} · {title}\n\n## 목적·주장\n\n{claim}\n\n## 앞 장면에서 받은 내용\n\n'+('없음' if i==0 else claims[i-1])+f'\n\n## 확정 발화\n\n{st}–{en}초·{en-st}초, 사용자 문장 종료 시각 기준. 음원 미제공으로 무음 영상.\n\n{script}\n\n## 시간별 화면\n\n'+'\n'.join(f'- {x["start"]}–{x["end"]}초: {x["text"]}' for x in rr)+'\n\n신경망의 연결 마스크와 실제 가중치를 일치시킨다. 전체망 청록, 부분망 노랑, 원래 초기값 파랑, 새 초기값 분홍. 곡선은 설명용 XOR 실측으로 표시하며 원논문 수치로 제시하지 않는다.\n\n## 시작·종료와 연결\n\n앞 문장의 대상을 받아 마지막 주장을 완료. 같은 마스크·가중치 순서 유지. 도입의 앞선 사례 요약은 이번 사용자의 확정 대본 요청에 따른다. 이후 영상 예고 없음.\n\n## 정확성\n\nM은 고정, 제거 연결은 모든 학습 스텝에서0. 남긴 값은 학습 후 값이 아니라 W0의 같은 인덱스 값으로 복원. 설명용 실험과 원논문 결과를 구분. 새 초기값이 항상 나쁘다고 표현하지 않음. Winning Ticket은 비교 성능·학습 기준을 충족하는 부분망이며 모든 희소망의 이름이 아님. 최소 독립 자유도를 측정하거나 증명한 것으로 표현하지 않음.\n',encoding='utf-8')
 manifest.append(dict(id=f'{i+1:02}',directory=f'scenes/{i+1:02}',**{'class':f'Scene{i+1:02}'},start=st,end=en,duration_seconds=en-st,title=title))
(r/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(r/'scenes.yaml').write_text('duration_seconds: 170\nlayouts: [9:16, 16:9]\nscenes:\n'+'\n'.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    title: {m["title"]}\n    start: {m["start"]}\n    end: {m["end"]}\n    duration_seconds: {m["duration_seconds"]}' for m in manifest)+'\n',encoding='utf-8')
for name in ['narration.md','master_script.md']:(r/name).write_text('# 복권 가설 — 170초 확정 대본\n\n'+'\n\n'.join(f'## {m["start"]}–{m["end"]}초 · {m["title"]}\n\n'+'\n'.join(x['text'] for x in rows if m['start']<=x['start']<m['end']) for m in manifest)+'\n',encoding='utf-8')
(r/'tts_script.txt').write_text('\n\n'.join(x['text'] for x in rows).replace('Lottery Ticket Hypothesis','로터리 티켓 하이포시시스').replace('Winning Ticket','위닝 티켓')+'\n',encoding='utf-8')
(r/'brief.md').write_text('# 07 복권 가설 제작 기준\n\n사용자 제공35개 문장 종료 시각·170초 확정. 도입39초 사례 요약은 이번 명시적 사용자 요청을 따름. 핵심은 학습→마스크→원래 초기값 복원→고정 마스크 재학습. 새 초기값 비교도 같은 구조와 학습 조건. 실제 설명용 XOR 데이터와 가중치·학습 곡선 사용, 원논문 재현이나 보편적 성능 주장과 구분. 2018년 최초 공개와2019년 ICLR 구분. 성능 기준과 반복 수 표시. 모든 희소망을 위닝 티켓으로 부르지 않으며 독립 자유도 최소 증명으로 연결하지 않음. 단일ASS 자막·무음 세로/가로.\n',encoding='utf-8')
shutil.copy2(Path(r'C:/Users/as042/.codex/attachments/93998718-d376-4850-896a-57c2da3ac443/붙여넣은 텍스트.txt'),r/'storyboard_user.md')
if (r/'scenes/01_example').exists():
 for f in (r/'scenes/01_example').iterdir():f.unlink()
 (r/'scenes/01_example').rmdir()
print(len(rows),'sentences;',len(manifest),'scenes')
