import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
shutil.copy2(P.parent/'gpuh07_shared_memory'/'shared_style.py',P/'shared_style.py')
s=(P.parent/'gpuh07_shared_memory'/'build.py').read_text(encoding='utf-8').replace('gpuh07_shared_memory_160s','gpuh08_global_memory_165s').replace('gpuh07','gpuh08').replace('160','165')
(P/'build.py').write_text(s,encoding='utf-8')
raw='''GPU에서는 레지스터가 스레드의 계산값을 보관하고, 공유 메모리는 같은 블록의 스레드들이 데이터를 공유하고 재사용하도록 합니다.|8
그렇다면 GPU가 처리하는 대규모 데이터는 어디에 저장될까요?|12
바로 전역 메모리, Global Memory입니다.|15
전역 메모리는 GPU의 여러 에스엠과 블록에서 접근할 수 있는 대용량 메모리 공간입니다.|21
일반적으로 레지스터나 공유 메모리보다 용량이 크지만, 접근 지연도 상대적으로 큽니다.|26
실제 쿠다 코드를 살펴보겠습니다.|28
두 배열을 더하는 커널에서 각 스레드는 전역 메모리의 배열 A와 B에서 값을 읽어옵니다.|34
그리고 두 값을 더한 결과를 배열 C에 저장합니다.|37
이때 읽어온 값과 중간 결과는 레지스터에 보관될 수 있습니다.|41
즉, 전역 메모리에서 데이터를 가져와 계산한 뒤, 결과를 다시 전역 메모리에 저장하는 것입니다.|48
그런데 여기서 흥미로운 문제가 발생합니다.|50
같은 양의 데이터를 읽더라도, 스레드들이 접근하는 메모리 주소에 따라 실제 메모리 요청량이 달라질 수 있습니다.|56
하나의 워프에 속한 32개 스레드를 생각해 보겠습니다.|60
각 스레드가 4바이트의 실수 하나를 읽는다면, 필요한 데이터는 모두 128바이트입니다.|65
먼저 32개 스레드가 연속된 주소의 데이터를 읽는 경우입니다.|70
주소가 적절히 정렬되어 있다면, 필요한 데이터는 연속된 128바이트 영역에 모여 있습니다.|76
이때 GPU는 메모리 접근을 32바이트 단위의 네 개 섹터로 처리할 수 있습니다.|81
그렇다면 스레드들이 서로 여덟 개 원소 간격으로 떨어진 주소를 읽으면 어떻게 될까요?|86
각 스레드가 읽는 데이터는 여전히 4바이트이고, 전체 필요한 데이터도 128바이트로 같습니다.|92
하지만 요청한 주소들이 넓은 범위에 흩어져 있기 때문에, 이 예시에서는 32개의 서로 다른 섹터에 접근해야 합니다.|100
네 개였던 섹터가 32개로 늘어난 것입니다.|103
즉, 실제 계산에 사용하는 데이터는 같지만, 섹터 기준으로 처리해야 하는 데이터 양은 여덟 배로 증가합니다.|109
이처럼 같은 워프의 스레드들이 요청한 메모리 주소를 분석해, 필요한 메모리 접근으로 묶어 처리하는 것을 메모리 코얼레싱이라고 합니다.|117
여기서 중요한 것은 단순히 데이터를 얼마나 많이 읽느냐가 아닙니다.|122
스레드들이 어떤 주소에 접근하는지가 메모리 시스템의 효율을 바꿀 수 있다는 것입니다.|127
물론 섹터 수가 여덟 배로 증가했다고 실행시간까지 여덟 배가 되는 것은 아닙니다.|132
실제 성능은 캐시와 메모리 대역폭, 다른 연산의 실행 시간에도 영향을 받습니다.|137
앞서 살펴본 공유 메모리의 뱅크 컨플릭트가 메모리 뱅크에 접근하는 방식의 문제였다면, 코얼레싱은 워프의 전역 메모리 주소들이 얼마나 효율적으로 처리되는가의 문제입니다.|149
결국 전역 메모리는 GPU 전체가 접근하는 대용량 저장 공간이지만, 그 성능은 단순히 메모리의 용량이나 속도만으로 결정되지 않습니다.|158
GPU 최적화에서는 같은 계산을 수행하더라도, 스레드들이 데이터에 접근하는 주소 패턴을 어떻게 구성하는지가 중요합니다.|165'''
cues=[];start=0
for row in raw.splitlines():
 t,e=row.rsplit('|',1);e=int(e);cap=t
 for a,b in [('쿠다','CUDA'),('에스엠','SM'),('뱅크 컨플릭트','Bank Conflict'),('메모리 코얼레싱','Memory Coalescing')]:cap=cap.replace(a,b)
 cues.append(dict(start=start,end=e,caption=cap,tts=t));start=e
ends=[15,26,41,48,65,81,92,103,109,117,127,137,149,165]
titles=['대규모 데이터는 어디에 있을까?','여러 SM이 접근하는 메모리','Global Load → 계산 → Store','데이터의 왕복 경로','Warp 하나가 요청하는 128B','연속 주소는 네 개의 Sector로','같은 128B · 달라지는 주소','32개의 서로 다른 Sector','유효 데이터와 Sector Footprint','주소를 필요한 접근으로 묶기','Lane 순서보다 주소 집합','섹터 수와 실행시간은 다르다','Shared Bank와 Global Sector','Global Memory · 주소 패턴이 중요하다']
events=[[(0,'Register와Shared범위강조'),(8,'SM에서GPU전체로줌아웃'),(12,'Global주소공간강조')],[(15,'SM0~3이Global배열참조'),(21,'용량과지연정성비교')],[(26,'vectorAdd커널발췌'),(28,'A5=6 B5=60 Load'),(34,'6+60=66 계산'),(37,'Register보관가능'),(39,'C5=66 Store')],[(41,'Load Compute Store실제값왕복')],[(48,'주소에따른차이질문'),(56,'32개Lane활성'),(60,'32×4B=128B')],[(65,'고정32섹터격자에서연속주소연결'),(70,'주소0..124B정렬'),(76,'S0..3네섹터강조')],[(81,'A[i]→A[i*8]'),(86,'Lane32개유효128B고정'),(89,'선택word0,8,..248로이동')],[(92,'Lane0..31각자Sector0..31'),(100,'4개와32개비교')],[(103,'유효128B고정/섹터128B→1024B')],[(109,'주소집합을섹터에대응시키는과정'),(114,'하나의트랜잭션으로단정하지않음')],[(117,'역순Lane매핑도동일4섹터'),(122,'주소집합이효율을결정')],[(127,'8배섹터≠8배시간'),(132,'L1 L2 DRAM과연산각각강조')],[(137,'SharedBank경합'),(143,'GlobalSector분산과대비')],[(149,'섹터에서GPU전체로복귀'),(158,'주소패턴에따른효율결론')]]
manifest=[];paras=[];start=0
accuracy='32B 경계에 정렬된 기준 주소, NVIDIA CC6.0+의 32B sector 모델, 32개 활성 Lane, float32 Load 한 명령 기준. byteAddress=base+4*lane*stride, sector=floor(byteAddress/32). stride1은 4섹터, stride8은 32섹터. 유효 데이터 모두128B, sector footprint128B/1024B. 동일 데이터량이지 동일 원소값은 아님. 섹터 수는 실측 DRAM 요청이나 실행시간이 아니다. Global은 논리 주소공간, 일반적인 데이터의 물리 저장은 Device DRAM이며 캐시 적중 가능. Global→Shared→Register 필수 직렬 경로를 만들지 않는다. Bank Conflict는 다른 메커니즘.'
for i,(end,title) in enumerate(zip(ends,titles)):
 d=P/f'scenes/{i+1:02}_scene';d.mkdir(parents=True,exist_ok=True);script='\n'.join(c['tts'] for c in cues if start<=c['start'] and c['end']<=end);paras.append(script)
 (d/'script.txt').write_text(script+'\n',encoding='utf-8');manifest.append(dict(id=f'{i+1:02}',directory=d.relative_to(P).as_posix(),title=title,start=start,end=end,duration_seconds=end-start,**{'class':f'Global{i+1:02}'}))
 timeline='\n'.join(f'- {t}초: {s}' for t,s in events[i]);(d/'spec.md').write_text(f'# {title}\n\n## 주장\n{title}\n\n## 확정 길이\n{start}–{end}초. 사용자 문장 종료 시각 기준. 음원 미제공.\n\n## 대본\n{script}\n\n## 타임라인\n{timeline}\n\n## 화면과 연결\n상단 SM·Warp·Global 관계도와 하단 32Lane/32Sector 고정 격자의 식별을 유지한다. 주소 변경시 선택칸·연결선·섹터표시가 실제로 이동한다. Register 보라/Shared 청록/Global 황금. 코드 테두리 유지, 줄번호 없음, 자막 영역 분리.\n\n## 정확성\n{accuracy}\n\n## 시작/종료\n앞뒤 씬의 같은 주소와 색을 유지하며 다음 편 예고 없이 해당 주장을 완결한다.\n',encoding='utf-8')
 (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom global_visuals import GlobalBase\nclass Global{i+1:02}(GlobalBase):\n    INDEX={i}\n',encoding='utf-8');start=end
for filename,data in [('manifest.json',manifest),('timing.json',cues)]: (P/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def ts(n):return f'{n//3600:02}:{n//60%60:02}:{n%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
(P/'tts_script.txt').write_text('\n\n'.join(paras)+'\n',encoding='utf-8')
(P/'narration.md').write_text('# Global Memory — 확정165초\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues),encoding='utf-8');shutil.copy2(P/'narration.md',P/'master_script.md')
(P/'scenes.yaml').write_text('title: GPU LEVEL 08 Global Memory\nduration_seconds: 165\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    duration_seconds: {m["duration_seconds"]}\n    class: {m["class"]}\n' for m in manifest),encoding='utf-8')
shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\b26b562a-db0a-4622-8211-1c5a0b38fe34\붙여넣은 텍스트.txt'),P/'storyboard.md')
(P/'brief.md').write_text('# 제작 기준\n\n165초 · 30fps · 세로1080×1920 / 가로1920×1080 · 무음·전체 자막. 사용자 확정 대본과 종료시각 유지. 추가 복습·다음 편 예고 없음.\n\n'+accuracy+'\n\n시각화는 고정된 32Lane와32Sector×8word 격자를 유지한다. 연속→stride8로 주소 화살표와 유효word 선택이 이동하며4→32섹터가 변한다. 모든 요청이DRAM까지 가는 화살표를 피하고캐시적중과저장요청을구분한다. 실제CUDA로vectorAdd와stride1/8/reverse주소예제결과를검증하되성능실측으로표현하지않는다.\n',encoding='utf-8')
(P/'README.md').write_text('# GPU LEVEL 08 — Global Memory & Coalescing\n\n165초 · 14개 독립 씬 · 가로/세로30fps · 무음·전체자막.\n\n```powershell\npython longforms/gpuh08_global_memory/build.py --preview\npython longforms/gpuh08_global_memory/build.py --jobs 4\npython longforms/gpuh08_global_memory/verify.py\n```\n\n정렬된32개float32 Load의32B섹터 모델. 유효128B를 유지하며4→32섹터로 변경. 섹터수는실측DRAM전송이나실행시간이아니다.\n\n출처: [NVIDIA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html), [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html).\n',encoding='utf-8')
print(len(cues),'cues',len(manifest),'shots')
