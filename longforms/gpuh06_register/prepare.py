"""One-time initial setup only; do not rerun over the revised memory-v2 project."""
import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
for name in ['shared_style.py','build.py']:
    s=(P.parent/'gpuh05_grid'/name).read_text(encoding='utf-8').replace('gpuh05_grid','gpuh06_register').replace('gpuh05','gpuh06').replace('178','175')
    (P/name).write_text(s,encoding='utf-8')
raw='''GPU에서는 스레드가 워프와 블록을 구성하고, 에스엠에 배치되어 명령을 실행합니다.|5
지금까지는 이러한 GPU의 실행 구조를 살펴봤습니다.|9
그렇다면 스레드가 계산하는 동안 사용하는 데이터는 어디에 저장될까요?|14
이번에는 GPU의 실행 구조에서 메모리 계층으로 관점을 옮겨보겠습니다.|18
가장 먼저 살펴볼 것은 레지스터입니다.|21
레지스터는 GPU에서 연산에 필요한 값과 중간 결과를 빠르게 저장하는 하드웨어 자원입니다.|27
하나의 스레드가 두 숫자를 더하는 계산을 생각해 보겠습니다.|30
실제 쿠다 코드를 살펴보겠습니다.|32
스레드는 배열 A와 B에서 각각 하나의 값을 읽어옵니다.|36
그리고 두 값을 더해 중간 결과를 만든 다음, 출력 배열 C에 저장합니다.|41
이 과정에서 입력값과 중간 결과를 보관하기 위해 레지스터가 사용될 수 있습니다.|46
하지만 코드에 등장하는 지역 변수 하나가 반드시 레지스터 하나에 대응하는 것은 아닙니다.|51
실제 레지스터의 할당은 컴파일러가 결정합니다.|55
그렇다면 레지스터는 스레드 안에 존재하는 메모리일까요?|58
그렇지는 않습니다.|59
레지스터는 실제 하드웨어 실행 장치인 에스엠의 레지스터 파일에 존재합니다.|64
각 스레드는 이 자원의 일부를 할당받아 자신만의 계산 값을 유지합니다.|69
그런데 여기서 문제가 발생합니다.|71
에스엠이 보유한 레지스터의 총량은 제한되어 있습니다.|75
예를 들어 하나의 블록에 128개의 스레드가 있다고 생각해 보겠습니다.|79
스레드마다 레지스터를 32개 사용하면, 블록 하나에는 4,096개의 레지스터가 필요합니다.|85
하지만 스레드마다 64개를 사용하면, 필요한 레지스터는 8,192개로 증가합니다.|91
같은 블록이라도 레지스터 사용량이 두 배가 된 것입니다.|95
이처럼 레지스터 사용량이 많아지면, 하나의 에스엠에 동시에 배치할 수 있는 블록과 워프의 수가 줄어들 수 있습니다.|102
이러한 자원 제약과 관련된 개념이 레지스터 프레셔입니다.|105
이전 영상에서 살펴본 오큐펀시와도 연결됩니다.|108
상주할 수 있는 워프가 줄어들면, 메모리 대기 시간을 숨기는 데 불리해질 수 있기 때문입니다.|114
그렇다면 레지스터가 부족할 때는 어떻게 될까요?|117
컴파일러는 일부 값을 레지스터 대신 다른 메모리 공간에 저장할 수 있습니다.|121
이를 레지스터 스필링이라고 합니다.|124
일반적으로 이러한 값은 로컬 메모리에 저장됩니다.|127
하지만 로컬 메모리라는 이름과 달리, 실제 저장에는 디바이스 메모리 계층이 사용됩니다.|133
따라서 값을 읽고 저장하기 위한 추가적인 메모리 접근이 발생할 수 있습니다.|137
결국 레지스터를 많이 사용하는 것이 항상 좋은 것도, 적게 사용하는 것이 항상 좋은 것도 아닙니다.|143
충분한 레지스터는 중간값을 빠르게 처리하는 데 유리하지만, 과도한 사용은 동시에 실행할 수 있는 워프의 수를 제한할 수 있습니다.|150
여기서 중요한 점은 레지스터 사용량이 단순히 저장 공간의 문제가 아니라, GPU 전체의 실행 효율에도 영향을 준다는 사실입니다.|158
결국 레지스터는 스레드의 계산을 빠르게 지원하는 저장 공간이면서, 에스엠의 병렬 실행 규모를 제한할 수도 있는 하드웨어 자원입니다.|166
GPU 최적화에서는 연산을 얼마나 빠르게 수행하는지만큼, 그 연산에 필요한 데이터를 어디에 저장하고 얼마나 효율적으로 사용하는지도 중요합니다.|175'''
def caption(s):
    for a,b in [('에스엠','SM'),('쿠다','CUDA'),('레지스터 프레셔','Register Pressure'),('오큐펀시','Occupancy'),('레지스터 스필링','Register Spilling')]:s=s.replace(a,b)
    return s
cues=[];start=0
for line in raw.splitlines():
    s,e=line.rsplit('|',1);e=int(e);cues.append(dict(start=start,end=e,caption=caption(s),tts=s));start=e
ends=[21,32,41,46,55,64,69,79,85,95,105,114,124,137,143,158,166,175]
titles=['실행 구조에서 저장 공간으로','연산을 지원하는 Register','Thread 2의 Load · Add · Store','지역 변수와 물리 레지스터','Compiler가 결정하는 할당','Register File은 SM의 자원','Thread별로 할당받는 자원','빠르지만 한정된 저장 공간','128 Thread × 32 Registers','같은 Block · 두 배의 요구량','Register Pressure와 상주 수','Occupancy와 Latency Hiding','Register Pressure ≠ Spilling','Local Memory와 추가 접근','많이 써도 적게 써도 제약','Register Usage ↔ Parallelism','저장 자원이 실행 규모에 미치는 영향','계산과 데이터 저장을 함께 본다']
events=[[(0,'GPU·SM·Block·Warp·선택Thread2 유지'),(9,'계산 값이 저장되는 위치로 관점 이동'),(18,'SM Register File을 보라색으로 강조')],[(21,'Thread2의 임시 값과 SM 자원 연결'),(27,'두 입력의 덧셈'),(30,'실제vectorAdd 소스 발췌')],[(32,'Thread2의 A[2]=3과B[2]=4 읽기'),(36,'3+4=7 계산'),(39,'C[2]=7 저장')],[(41,'소스 변수 이름과 계산 값 표시'),(44,'Register에 보관될 수 있으나1:1대응은 아님 표시')],[(46,'Source→Compiler→Register Allocation'),(51,'실제컴파일로그의Register수·Spill0표시')],[(55,'Thread카드와SM자원분리'),(59,'SM0내RegisterFile강조')],[(64,'여러Thread의전용할당영역표시'),(67,'물리배치개념도이며타Thread직접접근아님강조')],[(69,'Limited Capacity'),(75,'128ThreadBlock의고정스레드수')],[(79,'가상32개/Thread에서128×32=4096계산')],[(85,'64개/Thread에서128×64=8192'),(91,'Thread수고정·요구량2배')],[(95,'가상SMRegister예산32768·32개/Thread8Blocks'),(99,'64개/Thread4Blocks로감소'),(102,'Register Pressure표시')],[(105,'상주Warp32→16·다른제약무시한예시'),(108,'대기Warp대신발행할ReadyWarp선택기회')],[(114,'Compiler가일부값을메모리에배치할수있는상황'),(121,'Register Spilling과컴파일명령개념표시')],[(124,'LocalMemory는Thread전용논리주소공간'),(127,'SM/Register와별도로L1/L2/DRAM경로'),(133,'Spill Store·Spill Load추가접근')],[(137,'Register활용의양쪽제약비교')],[(143,'중간값유지와상주Warp규모비교'),(150,'성능을Register수만으로단정하지않음')],[(158,'Thread값과SMRegisterFile을다시연결'),(162,'병렬실행규모와저장자원강조')],[(166,'CUDA코드·중간값·RegisterFile·WarpScheduler연결'),(172,'메모리자원과실행효율의연결로완결')]]
manifest=[];paragraphs=[];start=0
for i,(end,title) in enumerate(zip(ends,titles)):
    d=P/f'scenes/{i+1:02}_scene';d.mkdir(parents=True,exist_ok=True)
    script='\n'.join(c['tts'] for c in cues if c['start']>=start and c['end']<=end);paragraphs.append(script);(d/'script.txt').write_text(script+'\n',encoding='utf-8')
    m=dict(id=f'{i+1:02}',directory=d.relative_to(P).as_posix(),title=title,start=start,end=end,duration_seconds=end-start,**{'class':f'Register{i+1:02}'})
    manifest.append(m);timeline='\n'.join(f'- {t}초: {s}' for t,s in events[i])
    (d/'spec.md').write_text(f'# {title}\n\n## 목적과 핵심 주장\n{title}를 같은GPU구조에서설명한다.\n\n## 앞 장면에서 받은 내용\n선택Thread2·Block0·SM0와보라색RegisterFile의정체성을유지.\n\n## TTS와 확정 길이\n사용자확정종료시각 {start}–{end}초, {end-start}초. 음원미제공.\n\n{script}\n\n## 화면·애니메이션\n{timeline}\n\n## 화면 텍스트\nSM0 / Block0 / Thread2 / Register File. 실제CUDA와개념적컴파일명령패널을명확히구분.\n\n## 시작·종료 상태와 연결\n상단GPU→SM→Block관계도를유지하고선택영역만확대한다. 다음씬에서도동일Thread2와SM0를사용하며다음영상예고는없다.\n\n## 정확성\n소스변수와물리Register의1:1배치금지. Thread2값3·4·7은실제검증입력과대응. 32/64개는별도가상커널의32bitRegister요구량단순계산,할당단위·다른자원제약무시. 가상SM예산32768/max32Warp예시. Pressure와Spilling은별개. Local은Thread전용범위이며L1/L2캐시와DRAM계층사용,매접근이DRAM까지간다고표현하지않음.출처brief.md.\n',encoding='utf-8')
    (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom register_visuals import RegisterBase\nclass Register{i+1:02}(RegisterBase):\n    INDEX={i}\n',encoding='utf-8');start=end
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(n):return f'{n//3600:02}:{n//60%60:02}:{n%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
(P/'tts_script.txt').write_text('\n\n'.join(paragraphs)+'\n',encoding='utf-8')
(P/'narration.md').write_text('# Register — 사용자 확정175초\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues),encoding='utf-8');shutil.copy2(P/'narration.md',P/'master_script.md')
(P/'scenes.yaml').write_text('title: GPU 계층 구조 LEVEL 06 — Register\nduration_seconds: 175\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    duration_seconds: {m["duration_seconds"]}\n    class: {m["class"]}\n' for m in manifest),encoding='utf-8')
shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\1cef53d6-7950-48ca-b764-43cc90d30d5a\붙여넣은 텍스트.txt'),P/'storyboard.md')
(P/'brief.md').write_text('# 제작 기준\n\n175초·30fps·세로1080×1920·가로1920×1080. 사용자확정대본과발화시각유지. 이번사용자대본의복습문장은명시제공원문이므로유지하며별도복습·예고를추가하지않는다. 무음·전체자막.\n\n선택Thread2는Block0·SM0에속하며입력A[2]=3,B[2]=4,결과C[2]=7. RegisterFile은SM자원으로보라색표시. 지역변수a,b,sum을실제3Register슬롯으로그리지않음.\n\n32/64개는32bitRegister요구량의가상비교,실제vectorAdd로그와분리. 128×32=4096,128×64=8192. 가상SM32768Register/max32Warp,다른제약·할당단위무시시8Block/32Warp대4Block/16Warp. 실제GPU사양아님. Pressure가자동Spilling을뜻하지않으며성능비수치없음.\n\nLocalMemory는Thread전용논리주소공간이다. L1/L2/DRAM경로를별도로표시하되캐시적중가능성을보여준다. Spill명령은소스코드와구분한컴파일개념패널.\n\n출처: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#register-pressure 및 #local-memory, #occupancy.\n',encoding='utf-8')
(P/'README.md').write_text('# GPU 계층 구조 LEVEL 06 — Register\n\n사용자문장종료시각175초, 독립씬18개. 가로·세로30fps무음·전체자막.\n\n```powershell\npython longforms/gpuh06_register/build.py --preview\npython longforms/gpuh06_register/build.py\npython longforms/gpuh06_register/verify.py\n```\n\nThread2의3+4=7을SMRegisterFile과연결한다. 실제vectorAdd의컴파일로그와32/64Register가상예시를분리한다. Pressure·Spilling·LocalMemory를구분하며성능을단정하지않는다.\n',encoding='utf-8')
for f in (P/'scenes/01_example').glob('*'):f.unlink()
print('Prepared',len(cues),'cues and',len(manifest),'shots')
