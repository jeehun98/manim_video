"""One-time authoring setup; do not rerun over manually edited scripts."""
from pathlib import Path
import json,shutil,ast
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
shutil.copytree(ROOT/'longforms/_template',P,dirs_exist_ok=True,ignore=shutil.ignore_patterns('01_example'))
raw='''3|GPU에서는 수많은 스레드가 계산을 수행합니다.
8|그렇다면 이 스레드들은 실제 하드웨어에서 모두 독립적으로 실행될까요?
12|엔비디아 GPU에서는 32개의 스레드를 하나의 워프, Warp로 묶어 실행합니다.
17|워프는 GPU가 스레드들을 스케줄링하고 명령을 실행하는 기본 단위입니다.
19|하나의 워프를 살펴보겠습니다.
22|워프는 32개의 스레드로 구성됩니다.
27|그리고 각 스레드는 워프 안에서 0부터 31까지의 위치를 가집니다.
29|이 위치를 레인, Lane이라고 부릅니다.
35|즉, 스레드는 명령을 실행하는 논리적인 단위이고, 레인은 워프 안에서 해당 스레드를 구분하는 번호입니다.
42|이 스레드들은 각자 다른 데이터와 실행 상태를 가지지만, 워프 단위로 명령을 실행합니다.
46|이러한 실행 모델을 SIMT, Single Instruction, Multiple Threads라고 합니다.
48|실제 쿠다 코드를 살펴보겠습니다.
51|화면의 커널은 두 배열의 원소를 더하는 프로그램입니다.
57|각 스레드는 threadIdx.x를 이용해 자신이 처리할 원소를 선택합니다.
61|스레드 0은 0번 원소를, 스레드 1은 1번 원소를 계산합니다.
66|이렇게 32개의 스레드가 같은 명령을 실행하면서 서로 다른 데이터를 처리합니다.
70|그런데 모든 스레드가 항상 같은 명령 경로를 따라야 할까요?
73|이번에는 코드에 조건문을 추가해 보겠습니다.
79|스레드의 인덱스가 16보다 작으면 값을 두 배로 만들고, 그렇지 않으면 1을 더하도록 작성합니다.
85|이제 워프 안의 스레드 0부터 15까지는 곱셈을, 16부터 31까지는 덧셈을 수행해야 합니다.
90|문제는 하나의 워프 안에서 서로 다른 명령 경로가 필요하다는 것입니다.
95|GPU는 각 경로를 실행할 때 해당 경로에 참여하는 스레드만 활성화할 수 있습니다.
102|먼저 곱셈 경로에서는 앞의 16개 스레드가 활성화되고, 나머지 스레드는 해당 경로에서 비활성화됩니다.
106|덧셈 경로에서는 반대로 뒤의 16개 스레드만 활성화됩니다.
113|이처럼 하나의 워프에 속한 스레드들이 서로 다른 실행 경로로 나뉘는 현상을 Warp Divergence, 워프 분기 발산이라고 합니다.
118|분기 발산이 발생하면 여러 경로를 처리해야 하므로 실행 효율이 떨어질 수 있습니다.
123|그렇다면 조건문이 있다는 사실만으로 항상 분기 발산이 발생할까요?
124|그렇지는 않습니다.
129|워프 안의 모든 스레드가 같은 조건을 만족한다면 동일한 경로를 실행할 수 있습니다.
134|중요한 것은 조건문의 존재가 아니라, 같은 워프 안에서 서로 다른 경로가 선택되는지입니다.
145|또한 실제 엔비디아 GPU의 실행 방식은 세대에 따라 차이가 있으며, 볼타 이후의 아키텍처에서는 스레드별 실행 상태를 더욱 독립적으로 관리할 수 있습니다.
150|하지만 워프 단위의 명령 실행과 활성 스레드의 개념은 여전히 중요합니다.
159|결국 스레드는 각자의 데이터와 실행 상태를 가진 논리적인 실행 단위이고, 워프는 이러한 스레드 32개를 묶어 명령을 실행하는 하드웨어 단위입니다.
167|GPU의 병렬 계산을 이해하려면 스레드가 몇 개 있는지만이 아니라, 이 스레드들이 어떤 명령 경로를 함께 실행하는지도 살펴봐야 합니다.'''
# Keep the user's approved narration verbatim (including the 'only' wording).
raw=raw.replace('덧셈 경로에서는 반대로 뒤의 16개 스레드만 활성화됩니다.','덧셈 경로에서는 반대로 뒤의 16개 스레드가 활성화됩니다.')
cues=[];start=0
for line in raw.splitlines():
    end,caption=line.split('|',1);end=int(end);cues.append(dict(start=start,end=end,caption=caption));start=end
(P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
bounds=[0,8,17,29,42,48,57,66,73,79,90,95,102,106,118,124,134,145,150,159,167]
titles=['Thread에서 Warp로','32개 Thread의 실행 그룹','Thread와 Lane','개별 상태 · 같은 Warp','SIMT 실행 모델','코드와 서로 다른 인덱스','같은 명령 · 다른 데이터','조건문이 추가되면','같은 Warp 안의 두 경로','경로가 나뉜 Warp','참여 Lane을 선택하는 마스크','곱셈 경로 · 16개 활성','덧셈 경로 · 16개 활성','Warp Divergence','조건문이면 항상 발산할까?','조건문과 경로의 차이','스레드별 실행 상태','명령 실행은 Warp 단위','Thread와 Warp의 역할','함께 실행하는 경로']
actions=[
'0–3초 같은 SM·Block의 Thread 1을 선택. 3–8초 동일 Block의 32개 Thread로 시야 확장.',
'8–12초 같은 32개 셀을 Warp 0 외곽선으로 묶음. 12–17초 실행 그룹과 명령 발행을 강조.',
'17–22초 같은 Warp의 번호 0–31을 관찰. 22–27초 Lane 번호를 순차 강조. 27–29초 Lane Index 명명.',
'29–35초 같은 셀 6을 선택해 Thread 6과 Lane 6을 대응. 35–42초 개별 데이터·상태와 하나의 Warp 외곽선 유지.',
'42–46초 SIMT와 전체 Lane의 공통 명령 반응. 46–48초 동일 벡터 덧셈 소스로 연결.',
'48–51초 vectorAdd 발췌. 51–57초 threadIdx.x를 강조하고 Lane 0·1·31 선택.',
'57–61초 Lane 0과 1의 실제 입력·출력 대응. 61–66초 같은 ADD에 모든 Lane이 참여.',
'66–70초 공통 경로에서 질문. 70–73초 코드 패널에 if/else를 추가.',
'73–79초 i<16 조건과 0–15/16–31의 경로 색을 같은 고정 좌표에 대응.',
'79–85초 같은 Warp 안에 ×2와 +1 경로 표시. 85–90초 외곽선은 하나인 채 두 경로를 함께 관찰.',
'90–95초 현재 명령의 참여 Lane과 Active Mask 연결.',
'95–102초 곱셈 줄과 앞 16개의 활성 상태를 함께 표시. 나머지 16개는 자리를 유지하며 어둡게 표시.',
'102–106초 덧셈 줄과 뒤 16개의 활성 상태를 함께 표시. 같은 Warp와 번호 고정.',
'106–113초 두 마스크를 같은 Warp에서 번갈아 관찰. 113–118초 여러 경로와 명령별 활성 참여량의 관계. 실측 속도 배율은 주장하지 않음.',
'118–123초 조건문과 발산의 차이 질문. 123–124초 모든 Lane이 같은 경로를 택할 수 있음을 제시.',
'124–129초 i<32인 32개 Thread의 동일 경로. 129–134초 i<16과 비교해 같은 Warp 안의 경로 차이를 강조.',
'134–145초 같은 32개 셀을 유지하며 Volta 이후 Thread별 PC·상태를 개념도로 표시. 독립 명령 발행 장치처럼 그리지 않음.',
'145–150초 Warp 외곽선과 활성 마스크를 강조. 개별 상태와 Warp 명령 실행을 구분.',
'150–159초 Thread 6의 Index·Data·State를 같은 셀에서 확인한 뒤 전체 Warp 외곽선으로 확장.',
'159–167초 같은 Warp에서 공통/서로 다른 경로를 비교하고 전체 구조도·32 Lane 상태로 종료. 후속 예고 없음.'
]
manifest=[]
pronounce={'GPU':'지피유','Warp Divergence':'워프 다이버전스','Warp':'워프','Lane':'레인','SIMT, Single Instruction, Multiple Threads':'심트, 싱글 인스트럭션, 멀티플 스레즈','threadIdx.x':'스레드 인덱스 점 엑스'}
tts=[]
for i,(title,action) in enumerate(zip(titles,actions)):
    slug=f'{i+1:02}_scene';d=P/'scenes'/slug;d.mkdir(parents=True,exist_ok=True)
    m=dict(id=f'{i+1:02}',directory=f'scenes/{slug}',title=title,start=bounds[i],end=bounds[i+1],duration_seconds=bounds[i+1]-bounds[i],**{'class':f'Warp{i+1:02}'})
    manifest.append(m);sc=[c for c in cues if m['start']<=c['start']<m['end']]
    script='\n\n'.join(c['caption'] for c in sc)
    (d/'script.txt').write_text(script+'\n',encoding='utf-8')
    spoken=' '.join(c['caption'] for c in sc)
    for old,new in pronounce.items():spoken=spoken.replace(old,new)
    tts.append(spoken)
    (d/'scene.py').write_text(f"import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom warp_visuals import WarpBase\nclass Warp{i+1:02}(WarpBase):\n    INDEX={i}\n",encoding='utf-8')
    (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n- 목적·핵심 주장: {title}.\n- 앞 장면 입력: '+('같은 GPU·SM 0·Block 0의 Thread 선택' if i==0 else titles[i-1])+f'\n- 확정 구간: {m["start"]}–{m["end"]}초, {m["duration_seconds"]}초. 사용자 문장 종료 시각. 음원 미제공.\n- TTS 원문: [script.txt](script.txt).\n- 화면·타임라인: {action}\n- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.\n- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.\n- 다음 연결: '+(titles[i+1] if i<19 else '동일 GPU 지도와 Warp에서 종료. 후속편 예고 없음.')+'\n- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.\n- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.\n\n## 문장별 확정 시각\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초: {c["caption"]}' for c in sc)+'\n',encoding='utf-8')
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
story='\n\n'.join(f'### {c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues)
for name in ['master_script.md','narration.md']:(P/name).write_text('# GPU 계층 구조 LEVEL 02 — Warp\n\n사용자 확정 원문과 종료 시각. 총 167초.\n\n'+story+'\n',encoding='utf-8')
(P/'scenes.yaml').write_text('id: gpuh02_warp\ntitle: "왜 GPU는 32개의 스레드를 묶어서 실행할까?"\nvideo:\n  fps: 30\n  layouts:\n    shorts: [1080, 1920]\n    longform: [1920, 1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n    transition: cut\n' for m in manifest),encoding='utf-8')
# Snapshot the accepted common drawing and code-panel helpers, excluding ep01 shots.
old=(ROOT/'longforms/gpuh01_thread/visuals.py').read_text(encoding='utf-8');tree=ast.parse(old)
cl=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='ThreadBase')
lines=old.splitlines();prefix='\n'.join(lines[:cl.lineno-1]);methods=[]
for f in cl.body:
    if isinstance(f,ast.FunctionDef) and f.name in ['to','place','code','note','pulse']:
        methods.append('\n'.join(lines[f.lineno-1:f.end_lineno]))
(P/'shared_style.py').write_text(prefix+'\nclass StyleScene(Scene):\n'+'\n'.join(methods)+'\n',encoding='utf-8')
build=(ROOT/'longforms/gpuh01_thread/build.py').read_text(encoding='utf-8').replace('gpuh01_thread','gpuh02_warp').replace('gpuh01','gpuh02').replace('152','167')
(P/'build.py').write_text(build,encoding='utf-8')
shutil.copy2(Path(r'C:/Users/as042/.codex/attachments/567f03ab-a5e5-4dc6-8a91-0628f8857ef4/붙여넣은 텍스트.txt'),P/'storyboard.md')
print('CREATED',len(cues),'cues',len(manifest),'scenes',sum(m['duration_seconds'] for m in manifest),'seconds')
