from pathlib import Path
import json,shutil
r=Path('longforms/minimal06_universality');old=Path('longforms/minimal05_realization')
for name in ['build.py','caption_pass.py','inspect_frames.py','verify_caption_boundaries.py']:
 s=(old/name).read_text(encoding='utf-8').replace('minimal05','minimal06').replace('154','160').replace('4620','4800').replace('4619','4799')
 if name=='inspect_frames.py':s=s.replace('3,9,18,27,36,43,50,57,64,69,78,87,94,102,111,120,128,137,145,152','3,13,18,30,41,49,54,59,68,74,79,87,96,102,109,115,121,132,139,157')
 if name=='verify_caption_boundaries.py':s=s.replace('[989,990,991,1409,1410,1411,3149,3150,3151,3899,3900,3901]','[1679,1680,1681,1919,1920,1921,2429,2430,2431,3149,3150,3151]')
 (r/name).write_text(s,encoding='utf-8')
raw='''4|서로 다른 물질이, 놀랍게도 같은 수학적 법칙을 따를 수 있습니다.
8|물질을 이루는 입자도 다르고, 입자들이 서로 상호작용하는 방식도 다른데 말입니다.
10|어떻게 이런 일이 가능할까요?
15|물을 가열하면 어느 순간 액체와 기체의 구분이 사라지는 임계점에 도달할 수 있습니다.
19|자석도 온도를 높이면 자성을 잃는 상전이를 겪습니다.
21|두 현상은 전혀 달라 보입니다.
28|그런데 특정 조건에서, 액체와 기체의 임계점과 자석의 임계점은 같은 종류의 수학적 규칙을 따릅니다.
34|예를 들어 임계점에 가까워질 때 어떤 물리량이 변하는 비율을 나타내는 임계 지수가 일치할 수 있습니다.
38|왜 물질의 구체적인 구조가 다른데도 이런 일이 발생할까요?
42|이번에는 작은 자석들이 격자 위에 배열되어 있다고 생각해 보겠습니다.
48|각 자석은 위쪽 또는 아래쪽을 향하고, 이웃한 자석들은 서로 영향을 주고받습니다.
51|온도가 낮으면 많은 자석이 같은 방향으로 정렬됩니다.
56|온도를 높이면 열적 요동 때문에 배열이 점점 불규칙해집니다.
62|특히 임계점 근처에서는 작은 영역부터 큰 영역까지 다양한 크기의 집단적인 패턴이 나타납니다.
64|이제 이 격자를 조금 멀리서 관찰해 보겠습니다.
71|가까이에서는 수많은 개별 자석이 보이지만, 멀리서는 여러 자석을 하나의 블록으로 묶어 표현할 수 있습니다.
76|블록 안의 자석들이 주로 향하는 방향을 새로운 자석 하나로 나타내는 것입니다.
77|그리고 이 과정을 반복합니다.
81|네 개의 블록을 다시 하나로 묶고, 더 큰 규모에서 시스템을 바라봅니다.
92|이렇게 관찰하는 길이 척도를 바꾸면서, 시스템을 설명하는 변수와 상호작용이 어떻게 달라지는지 추적하는 것이 재규격화, Renormalization의 핵심 아이디어입니다.
93|여기서 중요한 사실이 드러납니다.
98|작은 규모에서 존재하던 모든 차이가 큰 규모에서도 똑같이 중요한 것은 아닙니다.
105|어떤 상호작용은 규모를 바꿀수록 영향이 작아지고, 어떤 성질은 계속 남아 전체적인 행동을 결정합니다.
111|임계점 근처에서는 서로 다른 물리계가 재규격화 과정을 거치며 같은 고정점으로 향할 수 있습니다.
117|고정점은 규모를 다시 바꾸어도 시스템을 설명하는 핵심적인 구조가 변하지 않는 지점입니다.
123|그리고 같은 고정점의 지배를 받는 물리계들은 동일한 임계 지수와 스케일링 법칙을 공유할 수 있습니다.
126|이것을 보편성, Universality라고 합니다.
129|물론 모든 물질이 같은 법칙을 따르는 것은 아닙니다.
135|공간의 차원이나 대칭성, 상호작용의 성질 등에 따라 서로 다른 보편성 부류가 나타납니다.
142|또한 모든 미시적 정보가 사라지는 것도 아닙니다. 물질마다 다른 수치나 세부적인 특성은 여전히 남을 수 있습니다.
149|그럼에도 놀라운 점은, 거시적인 현상을 이해하기 위해 미시적인 차이를 전부 알아야 하는 것은 아니라는 사실입니다.
154|서로 다른 물질이 같은 법칙을 따르는 이유는, 처음부터 내부 구조가 같아서가 아닙니다.
160|규모를 바꾸어 바라보았을 때, 서로 다른 구조에서 동일한 핵심적인 성질이 남을 수 있기 때문입니다.'''
rows=[];st=0
for line in raw.splitlines():
 en,t=line.split('|',1);en=int(en);rows.append(dict(start=st,end=en,text=t));st=en
(r/'narration_timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
def ts(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
(r/'captions.srt').write_text('\n\n'.join(f'{i}\n{ts(x["start"])} --> {ts(x["end"])}\n{x["text"]}' for i,x in enumerate(rows,1))+'\n',encoding='utf-8')
bounds=[0,10,21,38,48,62,76,92,105,117,126,135,142,149,160]
titles=['다른 물질, 같은 법칙?','서로 다른 두 임계 현상','같은 임계 지수라는 단서','작은 자석들이 만든 격자','정렬, 요동, 그리고 임계점','관찰하는 규모를 바꾸면','격자와 상호작용을 함께 바꾼다','작아지는 영향, 남는 영향','같은 고정점으로 향하는 흐름','고정점이 정하는 공통 법칙','보편성에도 조건이 있다','같은 법칙에도 차이는 남는다','모든 세부 정보가 필요한가?','서로 다른 구조에 남는 핵심']
claims=['서로 다른 미시 구조가 같은 거시 법칙을 공유할 수 있다','유체 임계점은 온도·압력 조건에서 접근하며 자성 전이와 다르다','같은 보편성 부류의 임계 지수는 같을 수 있다','2D Ising은 두 방향 스핀과 이웃 상호작용의 설명 모형이다','실제 Monte Carlo 표본에서 임계점의 상관된 패턴을 보여준다','2×2 다수결로 블록 스핀을 실제 계산하고 동률은 공정 추첨한다','블록화·길이 재척도화와 함께 유효 상호작용도 변화한다','고정점 부근에서 관련/무관 방향은 반복 척도 변환으로 구분한다','임계면에 맞춘 서로 다른 흐름은 같은 고정점으로 접근할 수 있다','같은 고정점 지배 아래 임계 지수와 스케일링을 공유할 수 있다','차원·대칭성·상호작용 등에 따라 보편성 부류가 달라진다','같은 임계 지수라도 비보편적 진폭·미시 특성은 다를 수 있다','거시 임계 법칙에 모든 미시적 세부가 필요하지는 않다','규모를 바꾸어도 남는 핵심 구조가 보편성을 설명한다']
manifest=[]
for i,(st,en,title,claim) in enumerate(zip(bounds,bounds[1:],titles,claims)):
 folder=r/'scenes'/f'{i+1:02}';folder.mkdir(parents=True,exist_ok=True);rr=[x for x in rows if st<=x['start']<en];script='\n'.join(x['text'] for x in rr)
 (folder/'script.txt').write_text(script+'\n',encoding='utf-8')
 (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import UniversalityScene\nclass Scene{i+1:02}(UniversalityScene):\n    index={i}\n',encoding='utf-8')
 (folder/'spec.md').write_text(f'# {i+1:02} · {title}\n\n## 목적·핵심 주장\n\n{claim}\n\n## 앞 장면에서 받은 내용\n\n'+('없음' if i==0 else claims[i-1])+f'\n\n## 확정 발화\n\n{st}–{en}초, {en-st}초. 사용자 종료 시각 기준. 음원 미제공으로 무음 영상.\n\n{script}\n\n## 화면과 애니메이션\n\n'+'\n'.join(f'- {x["start"]}–{x["end"]}초: {x["text"]}' for x in rr)+'\n\n입자 도식·실제 Ising 표본·블록화·유효 이론 흐름을 구분. 청록 ↑, 분홍 ↓, 노랑 블록과 법칙, 보라 고정점. 세로와 가로 각각 배치.\n\n## 시작·종료 상태와 연결\n\n첫 문장의 대상을 받아 마지막 문장의 주장으로 완료. 공통 색과 격자/고정점 도식 유지. 복습·다음 편 예고 없음.\n\n## 정확성\n\n2D Ising 유한 격자는 설명용이며 3D 유체/자석의 수치 임계 지수 측정이 아님. 동률은 고정 시드의 공정 ±1 추첨. RG는 (r,g)→(2r,g/2)의 고정점 근방 개념 모형이며 Ising 결합상수 실측값이 아님. 임계면 r=0 위 접근과 r≠0 이탈을 구분. 같은 지수와 서로 다른 진폭을 구분.\n',encoding='utf-8')
 manifest.append(dict(id=f'{i+1:02}',directory=f'scenes/{i+1:02}',**{'class':f'Scene{i+1:02}'},start=st,end=en,duration_seconds=en-st,title=title))
(r/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(r/'scenes.yaml').write_text('duration_seconds: 160\nlayouts: [9:16, 16:9]\nscenes:\n'+'\n'.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    title: {m["title"]}\n    start: {m["start"]}\n    end: {m["end"]}\n    duration_seconds: {m["duration_seconds"]}' for m in manifest)+'\n',encoding='utf-8')
for name in ['narration.md','master_script.md']:(r/name).write_text('# 재규격화와 보편성 — 160초 확정 대본\n\n'+'\n\n'.join(f'## {m["start"]}–{m["end"]}초 · {m["title"]}\n\n'+'\n'.join(x['text'] for x in rows if m['start']<=x['start']<m['end']) for m in manifest)+'\n',encoding='utf-8')
(r/'tts_script.txt').write_text('\n\n'.join(x['text'] for x in rows).replace('Renormalization','리노멀라이제이션').replace('Universality','유니버설리티')+'\n',encoding='utf-8')
(r/'brief.md').write_text('# 06 재규격화와 보편성\n\n160초·33개 발화 종료 시각 확정. 격자 축소만이 아닌 변수·상호작용·길이 척도의 변화가 핵심. 2D Ising Wolff Monte Carlo의 실제 상관된 임계 표본과 2×2 공정 동률 블록화를 계산. 이 결과와 RG 고정점 근방의 설명용 선형 흐름을 구분한다. 실제 물질의 수치 임계 지수는 제시하지 않음. 액체–기체는 온도와 압력 조절 표시. 단일 ASS 자막으로 문장 중첩 방지. 세로/가로 자막 포함 무음 영상.\n',encoding='utf-8')
shutil.copy2(Path(r'C:/Users/as042/.codex/attachments/f5e58453-f55f-4e5b-a6da-f6824050c8f2/붙여넣은 텍스트.txt'),r/'storyboard_user.md')
if (r/'scenes/01_example').exists():
 for f in (r/'scenes/01_example').iterdir():f.unlink()
 (r/'scenes/01_example').rmdir()
print('Prepared',len(rows),'sentences,',len(manifest),'scenes')
