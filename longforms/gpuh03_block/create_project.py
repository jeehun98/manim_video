"""One-time authoring setup from the user's approved narration and end times."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
shutil.copytree(ROOT/'longforms/_template',P,dirs_exist_ok=True,ignore=shutil.ignore_patterns('01_example'))
raw='''5|GPU에서는 32개의 스레드가 하나의 워프로 묶여 명령을 실행합니다.
10|그렇다면 서로 다른 워프에 속한 스레드들이 하나의 계산을 함께 수행하려면 어떻게 해야 할까요?
12|여기서 등장하는 것이 블록입니다.
17|블록은 여러 스레드를 하나의 그룹으로 묶는 논리적인 실행 단위입니다.
19|하나의 블록을 살펴보겠습니다.
23|이번에는 128개의 스레드로 구성된 블록을 생각해 보겠습니다.
28|워프 하나는 32개의 스레드로 구성되므로, 이 블록에는 네 개의 워프가 포함됩니다.
34|블록의 크기는 쿠다 커널을 실행할 때 지정할 수 있으며, 반드시 128개의 스레드로 구성되어야 하는 것은 아닙니다.
38|그렇다면 스레드들을 하나의 블록으로 묶으면 무엇이 가능해질까요?
43|가장 중요한 특징 중 하나는 데이터를 공유하고 실행을 동기화할 수 있다는 것입니다.
45|간단한 계산을 살펴보겠습니다.
48|128개의 숫자를 모두 더하려고 합니다.
51|각 스레드가 숫자 하나씩을 읽는 것은 어렵지 않습니다.
56|하지만 최종 합계 하나를 만들려면 서로 다른 스레드가 읽어온 값들을 합쳐야 합니다.
60|이때 사용할 수 있는 것이 공유, Shared Memory입니다.
62|실제 쿠다 코드를 살펴보겠습니다.
67|셰어드 로 선언한 배열은 같은 블록에 속한 스레드들이 함께 사용할 수 있는 메모리 공간입니다.
73|각 스레드는 자신의 인덱스를 이용해 입력값을 읽고, 공유 메모리의 서로 다른 위치에 저장합니다.
77|이제 공유 메모리에는 128개의 값이 들어갑니다.
79|그런데 여기서 문제가 발생합니다.
83|모든 스레드가 정확히 같은 순간에 데이터를 기록하는 것은 아닙니다.
89|어떤 스레드가 다른 스레드의 값을 읽으려고 할 때, 해당 값이 아직 기록되지 않았을 수도 있습니다.
92|이 문제를 해결하기 위해 사용하는 것이 싱크 스레드 입니다.
97|이 명령을 만나면 같은 블록의 스레드들은 동기화 지점에 도달할 때까지 기다립니다.
102|그리고 동기화 이전의 메모리 기록을 다른 스레드들이 올바르게 확인할 수 있도록 보장합니다.
106|이제 공유 메모리에 저장된 값들을 합쳐 보겠습니다.
108|처음에는 128개의 값이 있습니다.
115|스레드 0부터 63까지가 각각 다른 위치의 값을 더하면, 64개의 부분 합계가 만들어집니다.
119|다음 단계에서는 32개, 그다음에는 16개로 줄어듭니다.
123|이 과정을 반복하면 마지막에는 하나의 합계가 남습니다.
127|이처럼 여러 값을 단계적으로 하나로 합치는 연산을 리덕션이라고 합니다.
135|여기서 주목할 점은 서로 다른 워프에 속한 스레드들이 같은 공유 메모리를 사용해 하나의 결과를 만들었다는 사실입니다.
139|그렇다면 블록은 실제 GPU 하드웨어에서 어디에 배치될까요?
143|쿠다의 블록은 실행될 때 하나의 에스엠에 배치됩니다.
148|같은 블록의 워프들은 해당 에스엠의 실행 자원과 공유 메모리를 사용합니다.
152|다만 일반적인 블록 내부 동기화 명령은 서로 다른 블록까지 동기화하지는 않습니다.
158|즉, 블록은 내부적으로 협력할 수 있지만, 다른 블록과는 기본적으로 독립적인 실행 그룹입니다.
169|결국 스레드는 각자의 명령과 데이터를 처리하고, 워프는 32개의 스레드를 묶어 명령을 실행하며, 블록은 여러 스레드가 데이터를 공유하고 동기화하며 협력할 수 있는 단위입니다.
178|GPU의 병렬 계산은 단순히 많은 스레드를 실행하는 것뿐 아니라, 필요한 계산을 위해 이 스레드들이 어떻게 협력하도록 구성되는지도 중요합니다.'''
cues=[];start=0
for line in raw.splitlines():
    end,caption=line.split('|',1);end=int(end);cues.append(dict(start=start,end=end,caption=caption));start=end
(P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
bounds=[0,12,23,34,43,56,62,73,77,89,102,108,115,123,127,135,143,148,158,169,178]
titles=['Warp에서 Block으로','128 Thread의 논리 그룹','4 Warp · 128 Thread','공유와 동기화','128개의 입력 · 하나의 결과','Block의 Shared Memory','코드와 공유 배열의 주소','128개 값의 공동 적재','기록 중인 Thread들','Block 전체의 동기화','공유 배열에서 합산 시작','128 → 64 부분 합계','64 → 32 → … → 1','Thread 0의 결과 저장','Shared Memory를 통한 협력','Block 전체를 한 SM에 배치','같은 SM의 실행 자원','Block 내부의 동기화 범위','Thread · Warp · Block','협력으로 만든 하나의 결과']
actions=[
'0–5초 Warp 0의 동일한 32 Lane 보기. 5–10초 Warp 0을 축소해 Warp 1·2·3이 있는 같은 Block으로 확장. 10–12초 Block 외곽선 강조.',
'12–19초 Block 전체 관찰. 19–23초 128 Thread 고정 배치와 launch 설정을 대응.',
'23–28초 4×32=128. 28–34초 일반적인 크기 선택 64·128·256을 코드 패널에서 비교. 현재 reduction kernel은 128 고정이라는 조건을 표시.',
'34–38초 고정 Block 관찰. 38–43초 네 Warp에서 하나의 공유 공간으로 연결하는 경로와 동기화 의미.',
'43–48초 input[t]=t+1의 128개 입력. 48–51초 각 Thread가 자기 위치를 담당. 51–56초 output[0] 하나가 필요함을 강조.',
'56–60초 Block에 귀속된 Shared Memory 영역 등장. 60–62초 __shared__ 소스 대응.',
'62–67초 __shared__ float s[128] 강조. 67–73초 Warp별 공동 적재를 보여주며 s[0]=1, s[64]=65 등 대표 주소를 대응.',
'73–77초 같은 하나의 s[128]이 채워진 상태. Warp당 별도 Shared 배열을 만들지 않음.',
'77–83초 동기화 전 가능한 진행 상태 예시로 일부 기록 전 표시. 83–89초 Thread 0이 아직 기록 전인 s[64]를 읽으려는 위험.',
'89–92초 __syncthreads() 등장. 92–97초 Warp 도착 순서는 설명용으로 제시하고 모든 128 Thread가 장벽에 참여. 97–102초 장벽 해제와 기록 가시성.',
'102–108초 같은 s[128] 유지, 초기 128개 값과 전체 Thread 128 구별.',
'108–115초 stride64. Thread 0–63이 s[t]+s[t+64]를 계산. 64 부분 합계, 모든 128 Thread가 다음 장벽에 참여.',
'115–119초 stride32·16. 119–123초 stride8·4·2·1. 각 단계 뒤 Block 장벽. Shared Memory의 앞부분만 부분 합계로 남고 Thread 수는 계속128.',
'123–127초 s[0]=8256을 Thread0이 output[0]에 기록. 리덕션 명명.',
'127–131초 네 Warp가 같은 배열에 기록했던 범위를 표시. 131–135초 첫 합산의 연결 예시: Thread0이 기록한 s[0]=1과 Thread64가 기록한 s[64]=65를 Shared Memory에서 읽어 66으로 합침. 결과를 되돌린 실제 실행으로 표현하지 않음.',
'135–139초 Block을 감싼 GPU·SM 지도 관찰. 139–143초 네 Warp와 Shared 할당을 포함한 Block0 전체를 SM0에 배치.',
'143–148초 동일 SM0의 Warp Scheduler·Register File·Shared Memory 자원을 연결. 특정 사이클·스케줄을 주장하지 않음.',
'148–152초 Block0의 장벽 범위를 두 Block 지도에서 표시. 152–158초 Block별 독립 Shared 할당, 일반적 __syncthreads()는 다른 Block을 동기화하지 않음.',
'158–169초 동일 구조에서 Thread1→Warp0→Block0 차례로 강조. 개별 계산·명령 실행 그룹·협력 범위를 대응.',
'169–178초 같은 Block과 같은 s[128]에서 reduction 단계를 빠르게 보여주고 8256 결과·GPU/SM0/Block0 지도에서 종료. 후속편 예고 없음.'
]
manifest=[];tts=[]
for i,(title,action) in enumerate(zip(titles,actions)):
    slug=f'{i+1:02}_scene';d=P/'scenes'/slug;d.mkdir(parents=True,exist_ok=True)
    m=dict(id=f'{i+1:02}',directory=f'scenes/{slug}',title=title,start=bounds[i],end=bounds[i+1],duration_seconds=bounds[i+1]-bounds[i],**{'class':f'Block{i+1:02}'})
    manifest.append(m);sc=[c for c in cues if m['start']<=c['start']<m['end']]
    (d/'script.txt').write_text('\n\n'.join(c['caption'] for c in sc)+'\n',encoding='utf-8')
    spoken=' '.join(c['caption'] for c in sc)
    for old,new in {'GPU':'지피유','Shared Memory':'셰어드 메모리'}.items():spoken=spoken.replace(old,new)
    tts.append(spoken)
    (d/'scene.py').write_text(f"import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom block_visuals import BlockBase\nclass Block{i+1:02}(BlockBase):\n    INDEX={i}\n",encoding='utf-8')
    (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n- 목적・主張: {title}.\n- 앞 장면 입력: '+('같은 GPU/SM0/Block0의 Warp0' if i==0 else titles[i-1])+f'\n- 확정 구간: {m["start"]}–{m["end"]}초, {m["duration_seconds"]}초. 사용자 문장 종료 시각. 음원 미제공.\n- TTS 원문: [script.txt](script.txt).\n- 화면·타임라인: {action}\n- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.\n- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.\n- 다음 연결: '+(titles[i+1] if i<19 else '같은 구조도와 결과에서 종료. 후속편 예고 없음.')+'\n- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.\n- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.\n\n## 문장별 시각\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초: {c["caption"]}' for c in sc)+'\n',encoding='utf-8')
    f=d/'spec.md';f.write_text(f.read_text(encoding='utf-8').replace('목적・主張','목적·핵심 주장'),encoding='utf-8')
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
story='\n\n'.join(f'### {c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues)
for name in ['master_script.md','narration.md']:(P/name).write_text('# GPU 계층 구조 LEVEL 03 — Block\n\n사용자 확정 원문·39개 문장 종료 시각 기준 178초.\n\n'+story+'\n',encoding='utf-8')
(P/'scenes.yaml').write_text('id: gpuh03_block\ntitle: "스레드들은 어떻게 서로 협력할까?"\nvideo:\n  fps: 30\n  layouts:\n    shorts: [1080, 1920]\n    longform: [1920, 1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n    transition: cut\n' for m in manifest),encoding='utf-8')
shutil.copy2(ROOT/'longforms/gpuh02_warp/shared_style.py',P/'shared_style.py')
build=(ROOT/'longforms/gpuh02_warp/build.py').read_text(encoding='utf-8').replace('gpuh02_warp','gpuh03_block').replace('gpuh02','gpuh03').replace('167','178')
(P/'build.py').write_text(build,encoding='utf-8')
shutil.copy2(Path(r'C:/Users/as042/.codex/attachments/dc074c44-a22b-4e64-8c3d-5f04f26d6ea4/붙여넣은 텍스트.txt'),P/'storyboard.md')
print('CREATED',len(cues),'cues',len(manifest),'scenes',sum(m['duration_seconds'] for m in manifest),'seconds')
