"""One-time generation of approved narration, exact timings and shot contracts."""
import json, shutil
from pathlib import Path
P=Path(__file__).resolve().parent
shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
shutil.copy2(P.parent/'gpuh03_block'/'shared_style.py',P/'shared_style.py')
build=(P.parent/'gpuh03_block'/'build.py').read_text(encoding='utf-8').replace('gpuh03','gpuh04').replace('gpuh04_block','gpuh04_sm')
(P/'build.py').write_text(build,encoding='utf-8')
raw='''GPU에서는 여러 스레드가 블록을 구성하고, 블록 내부의 스레드들은 워프 단위로 명령을 실행합니다.|5
그렇다면 이러한 블록과 워프는 실제 GPU 하드웨어의 어디에서 실행될까요?|10
바로 에스엠, Streaming Multiprocessor입니다.|13
에스엠은 GPU에서 스레드들의 명령을 실제로 실행하는 핵심 하드웨어 장치입니다.|19
하나의 에스엠을 살펴보겠습니다.|21
에스엠 내부에는 명령을 실행하는 연산 유닛과 데이터를 저장하는 레지스터, 공유 메모리, 그리고 워프 스케줄러가 있습니다.|29
쿠다에서 정의한 블록은 실행될 때 하나의 에스엠에 배치됩니다.|33
그리고 해당 블록에 속한 워프들은 에스엠의 실행 자원을 사용합니다.|38
에스엠에는 여러 블록이 동시에 배치될 수도 있습니다.|42
그렇다면 에스엠은 수많은 워프의 명령을 어떻게 처리할까요?|45
여기서 중요한 역할을 하는 것이 워프 스케줄러입니다.|48
워프 스케줄러는 실행할 준비가 된 워프를 선택해 명령을 발행합니다.|52
실제 쿠다 코드를 살펴보겠습니다.|55
화면의 커널은 배열에서 값을 읽고, 두 배로 만든 다음, 결과를 저장하는 프로그램입니다.|60
먼저 스레드는 메모리에서 자신의 데이터를 읽어옵니다.|63
그리고 읽어온 값에 2를 곱해야 합니다.|66
그런데 메모리에서 요청한 데이터가 아직 도착하지 않았다면 어떻게 될까요?|70
해당 값을 필요로 하는 곱셈 명령은 바로 실행할 수 없습니다.|74
이때 워프 전체의 계산이 끝날 때까지 에스엠이 멈추는 것은 아닙니다.|78
워프 0이 데이터를 기다리고 있다고 가정해 보겠습니다.|82
워프 스케줄러는 실행할 준비가 된 다른 워프를 선택할 수 있습니다.|86
워프 1의 명령을 실행하고, 이후 워프 2의 명령을 실행하는 식입니다.|90
그사이 워프 0이 요청한 데이터가 준비되면, 워프 0도 다시 계산을 진행할 수 있습니다.|95
이처럼 한 워프가 기다리는 동안 다른 워프의 명령을 실행해 대기 시간을 숨기는 방식을 레이턴시 하이딩이라고 합니다.|103
그렇다면 에스엠에 워프를 많이 배치할수록 무조건 빠를까요?|107
그렇지는 않습니다.|108
에스엠이 사용할 수 있는 레지스터와 공유 메모리의 용량은 제한되어 있습니다.|113
하나의 블록이 많은 레지스터나 공유 메모리를 사용하면, 동시에 배치할 수 있는 블록과 워프의 수가 줄어들 수 있습니다.|119
여기서 등장하는 개념이 오큐펀시입니다.|122
오큐펀시는 에스엠에 최대로 상주시킬 수 있는 워프 수에 비해, 실제로 몇 개의 워프가 상주하고 있는지를 나타내는 비율입니다.|130
하지만 오큐펀시가 높다고 반드시 실행 속도가 빠른 것은 아닙니다.|134
이미 충분한 워프로 대기 시간을 숨기고 있다면, 워프를 더 늘려도 성능이 개선되지 않을 수 있습니다.|140
한 가지 더 중요한 점이 있습니다.|142
일반적인 쿠다 코드에서는 스레드와 블록의 개수를 지정할 수 있지만, 각 블록이 실행될 에스엠을 직접 지정하지는 않습니다.|149
실제 블록의 배치는 GPU의 하드웨어 스케줄링에 의해 결정됩니다.|154
결국 스레드는 개별 실행 문맥이고, 워프는 스레드들을 묶어 명령을 실행하는 단위이며, 블록은 스레드들이 협력하는 논리적인 그룹입니다.|162
그리고 에스엠은 이러한 블록들을 배치받아 워프의 명령을 실제 하드웨어에서 실행하는 장치입니다.|169
GPU의 높은 처리량은 단순히 연산 장치가 많기 때문만이 아니라, 여러 워프를 활용해 계산과 대기 시간을 효율적으로 관리하는 구조에서도 나옵니다.|178'''
def caption(s):
    for a,b in [('에스엠','SM'),('쿠다','CUDA'),('오큐펀시','Occupancy'),('레이턴시 하이딩','Latency Hiding')]:s=s.replace(a,b)
    return s
cues=[];start=0
for line in raw.splitlines():
    s,e=line.rsplit('|',1);e=int(e);cues.append(dict(start=start,end=e,caption=caption(s),tts=s));start=e
(P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(n):return f'{n//3600:02}:{n//60%60:02}:{n%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
ends=[19,29,42,52,66,78,82,95,103,119,130,140,154,162,169,178]
titles=['블록과 워프의 실제 실행 공간','SM 내부의 실행 자원','한 SM에 상주하는 Block','준비된 Warp의 명령 발행','Load → Compute → Store','데이터가 도착하지 않았다면','Warp 0은 SM 안에서 대기','다른 Warp 발행 · Warp 0 재개','Latency Hiding','상주 수를 제한하는 자원','Occupancy = 상주 Warp 비율','높은 Occupancy와 실행 성능','Block 배치는 하드웨어가 결정','Thread · Warp · Block','SM에서 실제로 명령 실행','계산과 대기를 겹치는 구조']
claims=['논리적인 Block과 Warp는 물리적 SM에서 실행된다','SM에는 여러 종류의 실행·저장 자원이 있다','자원이 허용하면 여러 Block이 같은 SM에 상주한다','스케줄러는 준비된 Warp의 발행 가능한 명령을 고른다','곱셈은 Load 결과 x에 의존한다','데이터가 준비되지 않으면 의존 명령은 대기한다','기다리는 Warp도 SM 안에 상주한다','Warp 0 대기 중 Warp 1·2가 명령을 발행할 수 있다','다른 작업을 겹쳐 지연을 숨긴다','자원 점유량이 크면 동시 상주 수가 줄 수 있다','상주 Warp 수를 최대 상주 Warp 수로 나눈 비율이다','높은 Occupancy가 높은 성능을 보장하지 않는다','일반 launch 인자로 SM 번호를 지정하지 않는다','논리적 실행 문맥·명령 실행 단위·협력 그룹을 구분한다','SM은 Warp의 명령을 실행하는 물리적 장치다','여러 Warp를 활용해 명령 발행을 이어간다']
manifest=[];start=0;paragraphs=[]
for i,(end,title,claim) in enumerate(zip(ends,titles,claims)):
    d=P/f'scenes/{i+1:02}_scene';d.mkdir(parents=True,exist_ok=True)
    script='\n'.join(c['tts'] for c in cues if c['start']>=start and c['end']<=end)
    paragraphs.append(script);(d/'script.txt').write_text(script+'\n',encoding='utf-8')
    m=dict(id=f'{i+1:02}',directory=d.relative_to(P).as_posix(),title=title,start=start,end=end,duration_seconds=end-start,**{'class':f'SM{i+1:02}'})
    manifest.append(m)
    (d/'spec.md').write_text(f'# {title}\n\n目的: {claim}\n\n## 핵심 주장\n{claim}\n\n## TTS / 확정 길이\n사용자 문장 종료 시각 {start}–{end}초, {end-start}초. 음원 미제공.\n\n{script}\n\n## 화면·타임라인\nGPU → SM 0 → Block 0 → Warp 0–3의 좌표를 고정한다. 사용자 콘티의 해당 {start}–{end}초 동작을 구현한다. 코드 발췌와 상태 변경을 동시에 표시한다.\n\n## 시작·종료 상태\n전후 씬은 동일한 SM 외곽선과 Warp 좌표를 사용한다. 다음 편 예고 없음.\n\n## 정확성\n스케줄링은 가정한 개념도이며 측정된 실행 순서나 cycle 수가 아니다. Warp를 SM 밖으로 내보내지 않는다. Occupancy 예시는 최대 32 Warp인 가상 SM이며 실제 사양 아님. 발행과 완료는 구분한다.\n',encoding='utf-8')
    (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom sm_visuals import SMBase\nclass SM{i+1:02}(SMBase):\n    INDEX={i}\n',encoding='utf-8')
    start=end
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'scenes.yaml').write_text('title: GPU 계층 구조 LEVEL 04 — SM\nduration_seconds: 178\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    duration_seconds: {m["duration_seconds"]}\n    class: {m["class"]}\n' for m in manifest),encoding='utf-8')
(P/'tts_script.txt').write_text('\n\n'.join(paragraphs)+'\n',encoding='utf-8')
(P/'narration.md').write_text('# SM — 확정 대본 / 사용자 제공 178초\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues)+'\n',encoding='utf-8')
shutil.copy2(P/'narration.md',P/'master_script.md')
source=Path(r'C:\Users\as042\.codex\attachments\bbc77224-f430-4bf5-a2d6-f771a872ff5f\붙여넣은 텍스트.txt')
shutil.copy2(source,P/'storyboard.md')
(P/'brief.md').write_text('# 제작 기준\n\n178초 / 30fps / 독립 완결 / 9:16와 16:9. 사용자 확정 문장 및 종료 시각 준수. 음원 미제공, 무음·전체 대본 자막.\n\n기존 GPU/SM/Block 관계도 유지. SM을 확대하고 Warp 좌표를 유지한다. Warp 0 파랑, 대기 주황, 발행 초록. 66–103초 코드·명령 발행·대기 겹침 연결. CPU식 문맥 저장·복원 금지. 스케줄러 하나만 그린 개념도, 실제 개수·배치는 세대별 차이. 자원 예시와 16/32=50%는 가상 설명 수치. 성능 숫자·배속 비교를 만들지 않는다.\n\n출처: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#occupancy\n',encoding='utf-8')
(P/'README.md').write_text('# GPU 계층 구조 LEVEL 04 — SM\n\n사용자 문장 종료 시각 기준 178초, 독립 씬 16개. 세로1080×1920·가로1920×1080 / 30fps / 무음·전체 자막.\n\n```powershell\npython longforms/gpuh04_sm/build.py --preview\npython longforms/gpuh04_sm/build.py\npython longforms/gpuh04_sm/verify.py\n```\n\nSM 관계도와 상주 Warp 위치를 고정한다. Latency Hiding은 실행 순서를 가정한 개념 애니메이션으로 실제 하드웨어 트레이스가 아니다. Occupancy의 최대32Warp는 가상 예시이며 성능비를 뜻하지 않는다. compute.cu는 실제 CUDA 검증용.\n',encoding='utf-8')
print('Prepared',len(cues),'cues and',len(manifest),'shots')
