import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True);shutil.copy2(P.parent/'gpuh09_cache'/'shared_style.py',P/'shared_style.py')
s=(P.parent/'gpuh09_cache'/'build.py').read_text(encoding='utf-8').replace('gpuh09_cache_169s','gpuh10_dram_164s').replace('gpuh09','gpuh10').replace('169','164');(P/'build.py').write_text(s,encoding='utf-8')
raw='''GPU에서 전역 메모리는 여러 에스엠과 블록이 접근할 수 있는 대용량 메모리 공간입니다.|5
그런데 전역 메모리라는 공간의 데이터는 실제로 어디에 저장되어 있을까요?|10
여기서 구분해야 할 것이 논리적인 메모리 공간과 물리적인 저장 장치입니다.|15
전역 메모리는 쿠다 프로그램이 접근하는 주소 공간이고, 그 데이터를 실제로 저장하는 장치는 일반적으로 디램, DRAM입니다.|23
그렇다면 에스엠에서 발생한 메모리 요청은 어떻게 디램까지 전달될까요?|28
GPU의 전체 구조를 살펴보겠습니다.|30
여러 에스엠에서 발생한 메모리 요청은 캐시와 메모리 시스템을 통해 처리됩니다.|35
앞서 살펴본 엘원과 엘투 캐시에 필요한 데이터가 없다면, 디램에 접근해야 할 수 있습니다.|40
이때 중요한 역할을 하는 하드웨어가 메모리 컨트롤러, Memory Controller입니다.|45
메모리 컨트롤러는 디램에 대한 읽기와 쓰기 요청을 조정하고, 실제 메모리 동작을 제어합니다.|51
실제 쿠다 코드를 살펴보겠습니다.|53
스레드가 전역 메모리의 배열 A에서 하나의 값을 읽는다고 생각해 보겠습니다.|58
요청한 데이터가 캐시에 존재하지 않아 디램 접근이 필요한 상황을 가정해 보겠습니다.|63
이 요청은 메모리 시스템을 거쳐 해당 메모리 컨트롤러로 전달됩니다.|67
메모리 컨트롤러는 디램에서 필요한 데이터를 읽도록 명령을 처리합니다.|71
그리고 읽어온 데이터는 다시 메모리 시스템을 통해 요청한 에스엠으로 전달됩니다.|76
데이터가 준비되면 스레드는 해당 값을 이용한 계산을 진행할 수 있습니다.|81
그렇다면 메모리 컨트롤러가 단순히 주소를 전달하는 장치일까요?|85
그렇지는 않습니다.|86
디램은 거대한 숫자 배열처럼 보이지만, 실제 내부는 여러 뱅크와 행, 열로 구성되어 있습니다.|92
하나의 뱅크를 살펴보겠습니다.|94
디램은 데이터를 읽기 위해 필요한 행을 활성화하고, 그 안에서 원하는 데이터에 접근합니다.|100
만약 필요한 행이 이미 활성화되어 있다면, 새로운 행을 열어야 하는 경우와 처리 과정이 달라집니다.|105
메모리 컨트롤러는 이러한 디램의 동작과 타이밍을 고려해 메모리 요청을 처리합니다.|110
따라서 같은 양의 데이터를 읽더라도 물리적인 접근 상태에 따라 지연시간이 달라질 수 있습니다.|116
그렇다면 GPU의 디램은 모두 같은 종류일까요?|120
대표적으로 지디디알, GDDR과 에이치비엠이 있습니다.|124
지디디알은 일반적인 그래픽카드에서 널리 사용되는 고속 메모리입니다.|129
반면 에이치비엠은 메모리 칩을 수직으로 적층하고 넓은 데이터 인터페이스를 활용해 높은 대역폭을 제공합니다.|136
두 방식 모두 GPU의 전역 메모리를 구현하는 물리적인 디램 기술입니다.|141
결국 전역 메모리는 쿠다 프로그램에서 사용하는 논리적인 주소 공간이고, 디램은 데이터를 실제로 저장하는 물리적 장치입니다.|149
그리고 메모리 컨트롤러는 이 디램에 대한 읽기와 쓰기를 조정하는 하드웨어입니다.|153
GPU의 메모리 계층은 에스엠과 캐시에서 끝나는 것이 아닙니다.|157
그 뒤에는 메모리 요청을 처리하는 컨트롤러와, 실제 데이터를 보관하는 디램의 물리적 구조가 존재합니다.|164'''
cues=[];start=0
for row in raw.splitlines():
 t,e=row.rsplit('|',1);e=int(e);cap=t
 for a,b in [('쿠다','CUDA'),('에스엠','SM'),('엘원','L1'),('엘투','L2'),('지디디알','GDDR'),('에이치비엠','HBM'),('디램','DRAM')]:cap=cap.replace(a,b)
 # Spoken expansions already followed by the written acronym should not be doubled on screen.
 cap=cap.replace('DRAM, DRAM','DRAM').replace('GDDR, GDDR','GDDR')
 cues.append(dict(start=start,end=e,caption=cap,tts=t));start=e
ends=[15,23,40,51,63,71,81,94,105,116,129,141,153,164]
titles=['Global 주소 공간과 물리 저장 장치','주소가 가리키는 데이터는 DRAM에','캐시 아래로 이어지는 요청','Memory Controller가 하는 일','같은 CUDA Load · 캐시 미스 가정','컨트롤러가 처리하는 DRAM 읽기','데이터 반환과 계산 재개','DRAM 내부의 Bank · Row · Column','열린 Row와 새로 열어야 하는 Row','명령과 타이밍을 고려하는 컨트롤러','GDDR · GPU 주변의 메모리 칩','HBM · 적층과 넓은 인터페이스','주소 공간 · 제어 장치 · 저장 장치','GPU 메모리 시스템의 물리적 연결']
events=[[(0,'SM들의Global접근'),(5,'논리/물리두관점'),(10,'Global주소공간과DRAM칩분리')],[(15,'A5논리주소→메모리시스템→DRAM개념연결')],[(23,'SM0요청'),(30,'L1/L2경로'),(35,'양쪽캐시Miss를가정')],[(40,'컨트롤러강조'),(45,'Read Write Timing')],[(51,'readData코드'),(53,'Thread5 A5=6'),(58,'L1 L2 Miss가정')],[(63,'컨트롤러요청수신'),(67,'DRAM읽기명령')],[(71,'값6반환'),(76,'6×2=12계산')],[(81,'컨트롤러에서DRAM확대'),(86,'4Bank각자격자'),(92,'Bank0확대')],[(94,'닫힌Bank ACTIVATE R1,READ C2'),(100,'같은R1의C5는READ만')],[(105,'다른R3은PRECHARGE ACTIVATE READ'),(110,'동일크기라도상태별절차차이')],[(116,'두DRAM구현'),(120,'GDDR GPU주변기판칩'),(124,'칩배선강조')],[(129,'HBM수직다이적층'),(133,'같은패키지의GPU와넓은인터페이스'),(136,'둘다물리DRAM')],[(141,'논리주소/물리저장대비'),(149,'컨트롤러제어역할')],[(153,'전체SM Cache Controller DRAM경로'),(157,'컨트롤러DRAM강조')]]
accuracy='사용자 문장 종료시각을 고정한다. Global은 논리 주소 공간, DRAM은 일반적 물리 저장 장치이며 주소 변환은 GPU 메모리 시스템에 걸친 과정이다. A[i]를 Bank/Row/Column에 직접 산술 대응시키거나 컨트롤러만 주소를 변환한다고 표현하지 않는다. 캐시 Miss와 요청 경로는 설명용 가정, 측정된 GPU 트레이스가 아니다. 요청은 주황, 반환 데이터는 초록. 컨트롤러 수·캐시 분할·칩 배치는 아키텍처별로 다르다. DRAM 모형은4Bank×4Row×8Column이며 각Bank의 열린Row는최대하나. 초기닫힘→ACTIVATE→READ,동일행→READ,다른열린행→PRECHARGE→ACTIVATE→READ의단순모형. 실제사이클/ns나정확한타이밍비율을제시하지않으며자동precharge·refresh등은생략한다. GDDR보드배치와HBM동일패키지적층은개념도이며속도/레이턴시순위가아니다. HBM스택은GPU다이위가아니라옆에배치한다. CUDA예제값A5=6,B5=12만실제로검증한다.'
manifest=[];paras=[];start=0
for i,(end,title) in enumerate(zip(ends,titles)):
 d=P/f'scenes/{i+1:02}_scene';d.mkdir(parents=True,exist_ok=True);script='\n'.join(c['tts'] for c in cues if start<=c['start'] and c['end']<=end);paras.append(script);(d/'script.txt').write_text(script+'\n',encoding='utf-8')
 manifest.append(dict(id=f'{i+1:02}',directory=d.relative_to(P).as_posix(),title=title,start=start,end=end,duration_seconds=end-start,**{'class':f'Dram{i+1:02}'}))
 timeline='\n'.join(f'- {t}秒: {s}' for t,s in events[i]).replace('秒','초')
 (d/'spec.md').write_text(f'# {title}\n\n## 주장과 확정 길이\n{start}–{end}초, 사용자 문장 종료시각 기준. 음원 미제공.\n\n## 대본\n{script}\n\n## 화면 타임라인\n{timeline}\n\n## 시작/종료와 지속 요소\n상단 SM0/Warp0/Register·L1·L2·Controller·DRAM을 유지한다. 요청과 값이 실제로 이동하고, DRAM 확대시 같은 Bank0/Row 식별을 유지한다. Global은 물리상자 밖의논리오버레이. 코드줄번호없음,별도자막영역. 다음영상예고없음.\n\n## 정확성\n{accuracy}\n',encoding='utf-8')
 (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom dram_visuals import DramBase\nclass Dram{i+1:02}(DramBase):\n    INDEX={i}\n',encoding='utf-8');start=end
for filename,data in [('manifest.json',manifest),('timing.json',cues)]: (P/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def ts(n):return f'{n//3600:02}:{n//60%60:02}:{n%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
(P/'tts_script.txt').write_text('\n\n'.join(paras)+'\n',encoding='utf-8');(P/'narration.md').write_text('# Memory Controller & DRAM — 확정164초\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues),encoding='utf-8');shutil.copy2(P/'narration.md',P/'master_script.md')
(P/'scenes.yaml').write_text('title: GPU LEVEL 10 Memory Controller & DRAM\nduration_seconds: 164\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    duration_seconds: {m["duration_seconds"]}\n    class: {m["class"]}\n' for m in manifest),encoding='utf-8')
shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\83c4f9ec-ea50-48b2-89c4-47aab0ff5b7f\붙여넣은 텍스트.txt'),P/'storyboard.md');(P/'brief.md').write_text('# 制作基準'.replace('制作基準','제작 기준')+'\n\n164초 · 가로1920×1080/세로1080×1920 · 30fps · 무음·전체 자막. 제공 대본/종료시각 확정. 추가 복습·예고 없음.\n\n'+accuracy+'\n',encoding='utf-8')
(P/'README.md').write_text('# GPU LEVEL 10 — Memory Controller & DRAM\n\n164초 · 독립 씬14개 · 가로/세로 30fps · 무음·전체 자막.\n\n```powershell\npython longforms/gpuh10_dram/build.py --preview\npython longforms/gpuh10_dram/build.py --jobs 4\npython longforms/gpuh10_dram/verify.py\n```\n\n상태 모형은 설명용이며 실제 캐시/DRAM 추적이나 타이밍 측정이 아니다.\n\n기술출처: [Micron HBM2E 동작](https://assets.micron.com/adobe/assets/urn%3Aaaid%3Aaem%3A275edf31-79e3-4b6c-8bbd-a233babe9281/renditions/original/as/micron-hbm2e-memory-wp.pdf), [Micron HBM](https://www.micron.com/products/memory/hbm), [Micron Graphics Memory](https://www.micron.com/products/memory/graphics-memory).\n',encoding='utf-8');print(len(cues),'cues',len(manifest),'shots')
