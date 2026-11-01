from pathlib import Path
import json,shutil
r=Path('longforms/minimal01_07_finale');shutil.copytree('longforms/_template',r,dirs_exist_ok=True)
shutil.rmtree(r/'scenes/01_example')
raw='''지금까지 우리는 서로 다른 분야에서 하나의 질문을 살펴봤습니다.|4
모든 것이 정말 필요할까요?|6
처음에는 단순한 구조에서 출발했습니다.|8
여러 지점을 연결한 그래프에서 일부 연결을 제거하더라도, 모든 지점 사이의 이동 가능성은 유지할 수 있었습니다.|16
하지만 최단거리까지 보존하려면 이야기는 달라졌습니다.|19
같은 그래프에서도 무엇을 유지하려는지에 따라 필요한 연결이 달라진 것입니다.|23
생명체에서도 비슷한 질문을 던졌습니다.|26
어떤 유전자는 제거해도 생존할 수 있었지만, 다른 유전자의 존재나 주변 환경이 달라지면 필수적인 유전자가 될 수도 있었습니다.|33
통계학에서는 수많은 관측값을 하나의 숫자로 줄이더라도, 특정 조건에서는 모수에 대한 추론 정보를 모두 보존할 수 있었습니다.|41
제어이론에서는 여러 내부 상태를 더 적은 수의 상태로 표현하면서도, 동일한 입출력 동작을 유지할 수 있었습니다.|48
그리고 물리학에서는 서로 다른 미시적 구조를 가진 물질들이 같은 거시적 법칙을 따를 수 있다는 사실을 확인했습니다.|55
마지막으로 신경망에서는 수많은 연결 중 일부만을 선택해도, 원래 모델에 필적하는 성능으로 학습할 수 있는 경우가 있었습니다.|63
이 사례들은 모두 무언가를 줄이거나 단순화한다는 점에서 닮아 있습니다.|67
하지만 자세히 보면, 서로 다른 것을 보존하고 있습니다.|71
그래프에서는 연결성과 같은 구조적 성질을, 생명체에서는 특정 환경에서의 생존을, 통계학에서는 추론에 필요한 정보를 보존합니다.|80
제어이론에서는 입출력 동작을, 물리학에서는 특정한 거시적 법칙을, 신경망에서는 학습 성능을 살펴봤습니다.|87
그렇다면 여기서 하나의 공통된 원리를 발견할 수 있을까요?|90
전체를 이루는 모든 부분이, 우리가 관찰하려는 결과에 똑같이 중요한 것은 아니라는 것입니다.|96
그러나 어떤 부분이 불필요한지는 그 자체만 보고 결정할 수 없습니다.|100
먼저 무엇을 유지할 것인지 정해야 합니다.|103
그리고 그 결과를 유지하면서 어디까지 줄일 수 있는지 확인해야 합니다.|107
여기에는 또 하나의 중요한 구분이 있습니다.|109
어떤 구조를 줄일 수 있다는 사실과, 그것이 가능한 가장 작은 구조라는 사실은 다릅니다.|115
일부 연결을 제거해도 결과가 유지된다고 해서, 더 제거할 수 있는 연결이 없다는 뜻은 아닙니다.|121
또한 정확히 같은 결과를 만드는 것과, 충분히 비슷한 결과를 만드는 것도 서로 다른 문제입니다.|127
결국 최소 구조를 찾는다는 것은 단순히 많은 것을 지우는 작업이 아닙니다.|131
무엇을 같은 것으로 볼 것인지 정의하고, 그 조건 아래에서 필요한 부분을 찾아가는 과정입니다.|137
이제 우리는 다시 신경망으로 돌아갑니다.|139
신경망의 연결을 줄일 수 있다는 사실은 확인했습니다.|143
그런데 더 근본적인 질문이 남아 있습니다.|146
서로 다른 파라미터를 가진 두 신경망이, 사실은 완전히 같은 함수를 표현하고 있다면 어떨까요?|152
그렇다면 우리가 줄여야 할 것은 연결의 개수만이 아닐지도 모릅니다.|156
신경망이 가진 수많은 파라미터 속에서, 실제로 서로 다른 표현이 몇 개나 존재하는지부터 다시 살펴봐야 할 것입니다.|163'''
rows=[];start=0
for line in raw.splitlines():
 t,e=line.split('|');e=int(e);rows.append(dict(start=start,end=e,text=t));start=e
(r/'narration_timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(r/'master_script.md').write_text('# 모든 것이 필요할까? 01–07 통합 마무리\n\n사용자 확정 대본·문장 종료 시각 / 163초\n\n'+'\n\n'.join(f'{x["start"]}–{x["end"]}초\n{x["text"]}' for x in rows),encoding='utf-8')
shutil.copy2(r/'master_script.md',r/'narration.md')
bounds=[0,8,23,33,41,48,55,63,87,103,121,127,137,146,163]
titles=['모든 것이 정말 필요할까?','그래프 · 무엇을 보존할까?','최소 유전체 · 조건에 따른 필수성','충분통계량 · 추론 정보 보존','최소 실현 · 같은 입출력','보편성 · 같은 거시적 법칙','복권 가설 · 선택과 초기값','서로 다른 보존 대상','공통 질문 · 무엇을 유지할까?','축소 가능성 ≠ 최소성','정확한 보존과 근사 보존','최소 구조를 찾는 세 가지 질문','다시 신경망으로','다른 파라미터, 같은 함수?']
notes=['여섯 분야의 실제 기존 장면을 축소 카드로 회수하고 중심 질문 제시.','8정점 그래프에서 연결성 유지 / 최단거리 증가를 실제 경로로 비교.','같은 유전자 제거, 영양분 공급 조건별 생존 차이.','독립·동일 정규분포·알려진 분산·고정 표본 수에서 평균 추론.','ż=−z+2u, y=z 예시. 대응 초기값에서 같은 출력.','같은 보편성 부류, 임계점 근방의 점근적 스케일링.','07편 실제 설명용 XOR 실험 재사용. 원논문 수치 아님.','분야별 보존 대상 6개를 서로 구분.','추상 네트워크는 비유이며 통일 정리 아님. 조건 변경으로 필요한 간선 변화.','8정점에 9개→8개→7개 간선. 연결성의 하한 n−1, 현재 예시와 일반 최소성 구별.','정확한 함수 동등성과 오차 허용 보존을 구분. 곡선은 설명용.','보존 기준, 축소 탐색, 최소성 증명을 분리.','압축 가능성은 조건부 관찰이며 모든 신경망에 대한 보편 명제가 아님.','같은 아키텍처, 뉴런 위치와 연결 대응만 달리 배치. 전 입력 함수 동등성은 질문으로 남기며 유한 테스트는 증명 아님. 순열 대칭성은 크기나 연속 차원 감소를 보장하지 않음.']
manifest=[];tts=[]
for i,(a,b,title,note) in enumerate(zip(bounds,bounds[1:],titles,notes),1):
 d=r/f'scenes/{i:02}';d.mkdir(parents=True,exist_ok=True)
 script='\n'.join(x['text'] for x in rows if a<=x['start']<b);tts.append(script)
 (d/'script.txt').write_text(script+'\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02} {title}\n\n目的・주장: {note}\n\n확정 구간: {a}–{b}초 ({b-a}초), 사용자 문장 종료 시각 기준. TTS 음원 미제공, 무음.\n\n입력: 앞 장면의 질문. 시작: 제목과 주제 도형. 종료: 보존 조건과 결론.\n\n화면: 기존 시리즈 팔레트, 청록=보존, 회색=제거, 노랑=질문. 전역 단일 자막 트랙은 하단 전용 영역.\n\n대본\n'+script,encoding='utf-8')
 (d/'scene.py').write_text(f"import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import FinaleScene\nclass Scene{i:02}(FinaleScene):\n index={i-1}\n",encoding='utf-8')
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title))
(r/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
(r/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(r/'scenes.yaml').write_text('title: 모든 것이 필요할까? 01–07 통합 마무리\nresolution: [1920, 1080]\nfps: 30\nduration_seconds: 163\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
def stamp(v):return f'{v//3600:02}:{v//60%60:02}:{v%60:02},000'
(r/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(x["start"])} --> {stamp(x["end"])}\n{x["text"]}' for i,x in enumerate(rows,1))+'\n',encoding='utf-8')
for name in ['build.py','caption_pass.py','verify_caption_boundaries.py']:
 s=(Path('longforms/minimal07_lottery')/name).read_text(encoding='utf-8').replace('minimal07','minimal01_07_finale').replace('170','163').replace('5100','4890').replace('5099','4889')
 if name=='build.py':s=s.replace("default='both'","default='longform'")
 (r/name).write_text(s,encoding='utf-8')
(r/'brief.md').write_text('# 제작 기준\n\n163초 / 16:9만 / 무음·자막 / 확정 대본 그대로. 14개 독립 씬.\n\n이번 사용자 요청은 통합 회고와 마지막 질문을 명시적으로 허용. 기존 개별 영상의 예고 금지 기본 규칙에 대한 이번 영상 한정 예외.\n\n콘티와 발화가 어긋나는 103–137초는 발화 우선: 103–121 최소성,121–127 정확/근사,127–137 세 질문. 마지막 질문은 기능 동등성이지 파라미터 감소 증명이 아님.\n',encoding='utf-8')
(r/'README.md').write_text('# 01–07 통합 마무리\n\n163초, 1920×1080 30fps, 롱폼 전용. 음원 미제공으로 무음·자막. 사용자 확정 문장 종료 시각을 그대로 사용.\n\n실행: `python longforms/minimal01_07_finale/build.py --preview` → `python longforms/minimal01_07_finale/build.py`\n\n검증: `python longforms/minimal01_07_finale/verify_caption_boundaries.py --layout longform`\n\n기존07의 시각 요소·실험 데이터와 기존01–06 화면 프레임 재사용. 각 씬의 spec.md에 조건 기록. 원본 에피소드 소스는 변경하지 않음.\n',encoding='utf-8')
print('Prepared',len(manifest),'scenes',len(rows),'captions')
