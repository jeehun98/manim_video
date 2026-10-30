"""One-time setup from user-approved narration and exact sentence end times."""
import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
for n in ['shared_style.py','build.py']:
    s=(P.parent/'gpuh04_sm'/n).read_text(encoding='utf-8').replace('gpuh04_sm','gpuh05_grid').replace('gpuh04','gpuh05')
    (P/n).write_text(s,encoding='utf-8')
raw='''GPU에서는 여러 스레드가 블록을 구성하고, 각 블록은 에스엠에 배치되어 실행됩니다.|5
그렇다면 수많은 블록을 GPU 전체에 실행하려면 어떻게 해야 할까요?|10
여기서 등장하는 것이 그리드입니다.|12
그리드는 하나의 쿠다 커널 실행에 속하는 모든 블록을 묶은 논리적인 작업 공간입니다.|17
하나의 그리드를 살펴보겠습니다.|19
이번에는 12개의 블록으로 구성된 그리드를 생각해 보겠습니다.|23
각 블록에는 128개의 스레드가 있으므로, 전체 그리드에는 1,536개의 스레드가 존재합니다.|29
하지만 이 스레드들이 모두 같은 순간에 실행된다는 뜻은 아닙니다.|34
그리드는 실행할 작업 전체를 정의하고, 실제 하드웨어는 사용 가능한 자원에 따라 블록들을 나누어 실행합니다.|41
실제 쿠다 코드를 살펴보겠습니다.|43
커널을 호출할 때 사용하는 세 개의 꺾쇠괄호 안에는 그리드의 크기와 블록의 크기를 지정할 수 있습니다.|48
블록 크기를 128로 설정하면, 하나의 블록에는 128개의 스레드가 배치됩니다.|54
그리고 그리드 크기를 12로 설정하면, 총 12개의 블록이 만들어집니다.|59
그렇다면 각 스레드는 전체 데이터에서 자신이 담당할 위치를 어떻게 알 수 있을까요?|64
여기서 사용하는 것이 blockIdx.x, blockDim.x, 그리고 threadIdx.x입니다.|71
블록의 인덱스에 블록 크기를 곱하고, 블록 내부의 스레드 인덱스를 더하면 전체 데이터에서의 위치를 계산할 수 있습니다.|78
예를 들어 블록 0의 스레드 5는 5번 원소를 처리합니다.|82
반면 블록 1의 스레드 5는 128에 5를 더한 133번 원소를 처리합니다.|87
같은 스레드 인덱스를 가지더라도 블록이 다르면 담당하는 데이터가 달라지는 것입니다.|93
그렇다면 이렇게 정의된 블록들은 실제 GPU에서 어떻게 실행될까요?|97
GPU에는 여러 개의 에스엠이 존재합니다.|100
그리드에 포함된 블록들은 실행 가능한 에스엠에 배치됩니다.|104
에스엠의 자원이 허용하면 여러 블록이 동시에 상주할 수도 있습니다.|108
반대로 그리드에 포함된 블록이 많다면, 일부 블록은 앞선 블록의 실행이 끝나 자원이 확보될 때까지 기다려야 합니다.|115
여기서 중요한 점이 있습니다.|117
블록들은 반드시 인덱스 순서대로 실행되지 않습니다.|120
어떤 블록이 먼저 실행될지는 GPU의 하드웨어 스케줄링에 따라 달라질 수 있습니다.|126
따라서 일반적인 쿠다 커널에서는 서로 다른 블록이 특정한 순서로 실행된다고 가정해서는 안 됩니다.|132
그렇다면 그리드는 반드시 일차원으로 구성해야 할까요?|135
그렇지는 않습니다.|137
쿠다에서는 그리드를 최대 삼차원으로 구성할 수 있습니다.|140
예를 들어 이미지를 처리할 때는 그리드를 이차원 격자로 구성하고, 각 블록이 이미지의 서로 다른 영역을 담당하도록 만들 수 있습니다.|148
이때 blockIdx.x와 blockIdx.y는 각 블록이 담당하는 논리적인 위치를 나타냅니다.|150
하지만 이 좌표가 실제 GPU 칩에서 블록이 실행되는 물리적 위치를 뜻하는 것은 아닙니다.|156
결국 스레드는 개별 명령을 실행하는 논리적인 단위이고, 블록은 스레드들이 협력하는 그룹이며, 그리드는 하나의 커널 실행에 속한 블록 전체를 정의하는 작업 공간입니다.|166
그리고 실제 GPU에서는 여러 에스엠이 이 블록들을 배치받아 실행합니다.|171
즉, 그리드는 우리가 정의한 병렬 작업의 구조이고, 에스엠은 그 작업을 실제로 수행하는 하드웨어입니다.|178'''
def display(s):
    for a,b in [('에스엠','SM'),('쿠다','CUDA')]:s=s.replace(a,b)
    return s
def tts(s):
    for a,b in [('blockIdx.x','블록 인덱스 엑스'),('blockDim.x','블록 디멘션 엑스'),('threadIdx.x','스레드 인덱스 엑스'),('blockIdx.y','블록 인덱스 와이')]:s=s.replace(a,b)
    return s
cues=[];start=0
for line in raw.splitlines():
    s,e=line.rsplit('|',1);e=int(e);cues.append(dict(start=start,end=e,caption=display(s),tts=tts(s)));start=e
(P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(n):return f'{n//3600:02}:{n//60%60:02}:{n%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
ends=[17,29,41,48,59,71,78,87,93,104,115,126,132,140,150,156,166,178]
titles=['SM에서 GPU 전체로','12 Block · 1,536 Thread','작업 전체와 실행 자원','커널의 실행 설정','Block 크기와 Grid 크기','전체 데이터의 인덱스','Block과 Thread를 연결하는 수식','Thread 5 · 다른 데이터','겹치지 않는 출력 영역','Grid의 Block을 SM에 배치','동시 상주와 배치 대기','Block 순서는 보장되지 않는다','순서가 달라도 같은 결과','1D · 2D · 3D Grid','2D Grid와 이미지 타일','논리 좌표와 물리 위치','Thread · Block · Grid','논리 작업을 실행하는 하드웨어']
events=[[(0,'SM 0·Block 0·4 Warp 확대도'),(5,'여러 SM을 가진 GPU 전체로 시야 확장'),(10,'12 Block의 논리적 Grid 등장'),(12,'Grid 외곽선과 SM 영역을 분리')],[(17,'12개의 Block ID 유지'),(23,'12×128=1,536 강조')],[(29,'논리 Thread 수가 동시 실행 수는 아님을 표시'),(34,'가용 SM에 일부 Block을 배치')],[(41,'host launch 코드 발췌'),(43,'<<<gridSize, blockSize>>> 강조')],[(48,'Block당 Thread 128개 확대'),(54,'Grid의 12개 Block 전체 강조')],[(59,'Block과 Thread 선택'),(64,'blockIdx.x, blockDim.x, threadIdx.x 대응')],[(71,'i=b×128+t 표시'),(74,'각 항목과 코드의 대응 강조')],[(78,'Block 0·Thread 5의 i=5'),(82,'Block 1·Thread 5의 i=133')],[(87,'Block별 출력 주소 범위 비교'),(90,'Block 5는 C[640…767] 담당')],[(93,'논리 Grid와 물리 GPU를 나란히 유지'),(97,'SM 0–3 확인'),(100,'B7·B2·B9·B5의 배치와 Warp 확대')],[(104,'한 SM에 두 Block 상주 가능 예시'),(108,'미배치 Block은 자원 대기'),(111,'B7 완료 후 B4가 같은 슬롯에 배치')],[(115,'번호순 Grid는 유지'),(117,'순서 A: 7,2,9,5'),(120,'다른 순서 B: 5,2,8,0')],[(126,'독립 출력 영역을 처리하는 조건'),(129,'전체 두 순서 결과 일치')],[(132,'1차원 Grid 질문'),(137,'dim3와 최대3차원 표시')],[(140,'별도 imageKernel로 전환, 16×16 픽셀 타일'),(148,'Block(2,1)과 이미지 타일 대응')],[(150,'논리 이미지 좌표와 GPU SM 배치 비교'),(153,'Block(2,1)은 특정 SM 좌표가 아님')],[(156,'Thread 실행 문맥'),(159,'Block 협력 그룹'),(162,'Grid 작업 전체')],[(166,'12 Block이 여러 SM에서 실행'),(171,'Grid=논리 작업, SM=물리 실행 장치로 마무리')]]
claims=['Grid는 하나의 kernel 실행에 속한 Block 전체다','12×128=1536개의 논리 Thread를 정의한다','실행할 작업 수와 동시 실행 자원은 다르다','첫 launch 인자는 Grid, 둘째는 Block 크기다','12 Block 각각에128 Thread가 있다','논리 인덱스로 데이터 위치를 찾는다','전체 인덱스는 Block 시작점+Thread 내부 위치다','같은 Thread 5라도 Block에 따라 주소가 다르다','이 vectorAdd의 Block은 서로 다른 출력 영역을 쓴다','Block은 가용 SM에 배치된다','자원이 허용하면 여러 Block이 상주하고 나머지는 대기한다','Block 실행 순서를 인덱스 순서로 가정할 수 없다','독립적인 출력 영역을 쓰는 이 kernel은 순서와 무관하게 같은 결과다','CUDA Grid는 최대3차원의 논리 공간이다','별도2D kernel에서 Block 좌표가 이미지 타일에 대응한다','Grid 좌표는 SM의 물리 위치가 아니다','Thread·Block·Grid는 논리 실행 구조다','SM은 Grid의 작업을 실행하는 물리적 하드웨어다']
manifest=[];paragraphs=[];start=0
for i,(end,title,claim) in enumerate(zip(ends,titles,claims)):
    d=P/f'scenes/{i+1:02}_scene';d.mkdir(parents=True,exist_ok=True)
    script='\n'.join(c['tts'] for c in cues if c['start']>=start and c['end']<=end);paragraphs.append(script)
    (d/'script.txt').write_text(script+'\n',encoding='utf-8')
    m=dict(id=f'{i+1:02}',directory=d.relative_to(P).as_posix(),title=title,start=start,end=end,duration_seconds=end-start,**{'class':f'Grid{i+1:02}'})
    manifest.append(m);timeline='\n'.join(f'- {t}초: {s}' for t,s in events[i])
    (d/'spec.md').write_text(f'# {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n동일한 Block ID와 색상, Grid와 GPU의 분리된 영역을 유지한다. 첫 씬은 SM 0에서 시작한다.\n\n## TTS와 확정 길이\n사용자 문장 종료 시각 {start}–{end}초, {end-start}초. 음원 미제공.\n\n{script}\n\n## 화면·애니메이션\n{timeline}\n\n## 화면 텍스트\nLogical Grid / Physical GPU / Block 0–11 / SM 0–3. Block 5는 양쪽에서 초록색이다. 코드 패널은 배경·테두리·제목을 분리하고 줄 번호는 쓰지 않는다.\n\n## 시작·종료 상태와 연결\nBlock의 논리적 위치는 실제 SM 위치와 분리한다. 확대된 객체는 원래 선택한 Block과 연결한다. 씬별 완료 영상으로 결합하며 복습·다음 편 예고는 없다.\n\n## 정확성\n물리 배치는4SM의 설명용 개념도이며 실측 trace가 아니다. Grid 12Block·128Thread·N1536을 고정한다. 2D 이미지 예시는 별도 kernel, block16×16, image80×64, grid5×4다. 실행 순서 무관성은 각 Block이 겹치지 않는 출력에 기록하는 이 예제의 조건이다. Block1 Thread5=133, Block0 Thread5=5. 출처는 brief.md 참조.\n',encoding='utf-8')
    (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom grid_visuals import GridBase\nclass Grid{i+1:02}(GridBase):\n    INDEX={i}\n',encoding='utf-8');start=end
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'scenes.yaml').write_text('title: GPU 계층 구조 LEVEL 05 — Grid\nduration_seconds: 178\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    duration_seconds: {m["duration_seconds"]}\n    class: {m["class"]}\n' for m in manifest),encoding='utf-8')
(P/'tts_script.txt').write_text('\n\n'.join(paragraphs)+'\n',encoding='utf-8')
(P/'narration.md').write_text('# Grid — 확정 대본 / 사용자 제공178초\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues)+'\n',encoding='utf-8');shutil.copy2(P/'narration.md',P/'master_script.md')
shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\755c790c-5b24-4f7c-97ed-0d96b829372c\붙여넣은 텍스트.txt'),P/'storyboard.md')
(P/'brief.md').write_text('# 제작 기준\n\n178초·30fps·독립 완결·9:16/16:9. 사용자 확정 문장과 종료 시각 준수. 음원 미제공, 무음·전체 대본 자막.\n\nGrid는 SM에 포함시키지 않는다. 12Block×128Thread=N1536. Block5 초록색 ID를 두 영역에서 유지. 실행 배치·상주 수·순서는 설명용 가정으로 표시. Block은 SM 하나에서 실행되고 한 SM에는 여러 Block이 상주할 수 있다. Warp 스케줄링과 Block 배치를 혼동하지 않는다. 독립 출력의 vectorAdd에 한해 순서가 달라도 결과 같음을 제시.\n\n2D 예제는 별도 imageKernel, width80,height64, block16×16, grid5×4, 선택Block(2,1). 원래12Block·128Thread 예제와 혼합 금지. 좌표는 논리적 데이터 공간이며 실제 SM 위치가 아니다.\n\n출처: https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/intro-to-cuda-cpp.html (launch·인덱스·dim3) 및 https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html (독립 Block).\n',encoding='utf-8')
(P/'README.md').write_text('# GPU 계층 구조 LEVEL 05 — Grid\n\n사용자 문장 종료 시각178초, 독립씬18개. 세로1080×1920·가로1920×1080, 30fps, 무음·전체 자막.\n\n```powershell\npython longforms/gpuh05_grid/build.py --preview\npython longforms/gpuh05_grid/build.py\npython longforms/gpuh05_grid/verify.py\n```\n\n논리 Grid12Block과4SM의 물리 배치를 분리한다. vectorAdd는128Thread/Block·N1536. 2D imageKernel은별도80×64이미지·16×16Thread/Block·5×4Grid. CUDA 실행 결과와 논리 인덱스를 검증하며 스케줄링 애니메이션은 실측trace가 아니다.\n',encoding='utf-8')
for f in (P/'scenes/01_example').glob('*'):f.unlink()
print('Prepared',len(cues),'cues;',len(manifest),'shots')
