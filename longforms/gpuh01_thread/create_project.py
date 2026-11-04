from pathlib import Path
import json, shutil, textwrap
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
shutil.copytree(ROOT/'longforms/_template',P,dirs_exist_ok=True)
raw='''3|GPU는 수많은 계산을 병렬로 처리합니다.
7|그렇다면 그 계산을 수행하는 가장 기본적인 실행 단위는 무엇일까요?
8|바로 스레드입니다.
16|스레드는 단순히 덧셈 하나를 수행하는 연산 장치가 아니라, 명령을 실행하고 데이터를 처리하는 논리적인 실행 단위입니다.
18|두 배열을 더하는 연산을 생각해 보겠습니다.
24|첫 번째 배열에는 1, 2, 3, 4가 있고, 두 번째 배열에는 10, 20, 30, 40이 있습니다.
29|같은 위치의 원소를 더하면 11, 22, 33, 44가 됩니다.
33|CPU에서는 반복문으로 이 계산을 작성할 수 있습니다.
36|CUDA에서는 여러 스레드에 계산을 나누어 맡길 수 있습니다.
40|화면의 코드는 GPU에서 실행되는 CUDA 커널입니다.
48|여기서 __global__은 GPU에서 실행할 커널 함수를 정의하고, threadIdx.x는 블록 내부에서 현재 스레드의 인덱스를 나타냅니다.
52|하나의 블록에 네 개의 스레드를 배치했다고 가정하겠습니다.
55|각 스레드의 인덱스는 0, 1, 2, 3입니다.
59|스레드 0은 1과 10을 더하고, 스레드 1은 2와 20을 더합니다.
62|나머지 스레드도 각자 다른 원소를 계산합니다.
70|네 스레드가 실행하는 CUDA 코드는 동일하지만, 인덱스가 다르기 때문에 접근하는 데이터와 계산 결과도 달라집니다.
72|이번에는 스레드 하나를 확대해 보겠습니다.
77|스레드는 메모리에서 값을 읽고, 연산을 수행하고, 결과를 다시 저장합니다.
81|이 과정에서 자신만의 중간값과 실행 상태를 유지합니다.
85|GPU에는 이러한 값을 빠르게 저장하기 위한 레지스터가 있습니다.
92|레지스터는 스레드마다 물리적으로 따로 설치된 것이 아니라, GPU의 실행 장치인 SM에 존재하는 자원입니다.
99|각 스레드는 실행에 필요한 레지스터를 할당받아 사용하며, 실제 값의 배치는 컴파일러에 따라 달라집니다.
102|그렇다면 스레드는 항상 원소 하나만 계산할까요?
103|그렇지는 않습니다.
109|지금은 하나의 원소를 담당하도록 작성했지만, 반복문을 실행하거나 여러 원소를 처리할 수도 있습니다.
112|마지막으로 스레드의 위치를 살펴보겠습니다.
116|CUDA에서 스레드는 블록이라는 논리적인 그룹에 속합니다.
121|threadIdx.x는 GPU 전체의 고유 번호가 아니라 블록 내부의 위치입니다.
128|따라서 전체 배열의 위치를 계산할 때는 blockIdx.x와 blockDim.x를 함께 사용합니다.
134|또한 CUDA에서는 스레드의 인덱스를 최대 3차원으로 표현할 수 있어, 행렬의 행과 열에도 대응시킬 수 있습니다.
140|단, 이 좌표는 실제 하드웨어의 물리적 위치가 아니라 프로그램에서 사용하는 논리적 좌표입니다.
146|결국 CUDA의 스레드는 자신만의 인덱스와 실행 상태를 가지고 명령을 수행하는 논리적인 실행 단위입니다.
152|그리고 GPU의 병렬 계산은 이러한 스레드들에 서로 다른 작업을 배정하는 것에서 시작됩니다.'''
cues=[];start=0
for line in raw.splitlines():
    end,caption=line.split('|',1);end=int(end)
    cues.append(dict(start=start,end=end,caption=caption));start=end
(P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
bounds=[0,8,16,29,36,48,55,62,70,81,92,99,109,121,128,140,152]
titles=['GPU에서 Thread로','논리적인 실행 문맥','같은 위치의 원소 더하기','반복문에서 Thread로','코드와 실행 문맥','Block 안의 네 Thread','서로 다른 데이터','하나의 코드, 네 실행','읽기 · 계산 · 저장','SM의 Register File','변수와 실제 자원','한 Thread, 여러 원소','Block 내부의 위치','전체 배열의 인덱스','좌표는 논리적인 위치','Thread가 맡는 계산']
claims=['Thread는 논리적인 실행 단위다.','Thread는 명령·인덱스·상태를 가진다.','같은 인덱스의 입력끼리 더한다.','CUDA에서는 작업을 여러 Thread에 배정한다.','CUDA 코드 표현은 Thread의 동작과 대응한다.','threadIdx는 Block 내부 인덱스다.','각 Thread가 다른 입력과 출력을 담당한다.','같은 kernel도 Thread index에 따라 다른 데이터를 처리한다.','Thread는 읽기·계산·저장 중 중간 상태를 유지한다.','Register File은 SM의 물리적 자원이다.','소스 변수와 물리적 Register는 일대일이 아니다.','Thread 하나가 여러 원소를 처리할 수 있다.','서로 다른 Block에 같은 threadIdx가 있다.','전역 index는 Block 위치와 내부 위치를 결합한다.','최대 3차원 Thread 좌표는 논리 좌표다.','병렬 계산은 Thread들에 작업을 배정하는 데서 시작한다.']
manifest=[]
for i,title in enumerate(titles):
    slug='01_hook' if i==0 else f'{i+1:02}_scene';d=P/'scenes'/slug;d.mkdir(parents=True,exist_ok=True)
    m=dict(id=f'{i+1:02}',directory=f'scenes/{slug}',title=title,start=bounds[i],end=bounds[i+1],duration_seconds=bounds[i+1]-bounds[i],**{'class':f'Thread{i+1:02}'})
    manifest.append(m)
    script='\n\n'.join(c['caption'] for c in cues if bounds[i]<=c['start']<bounds[i+1])
    (d/'script.txt').write_text(script+'\n',encoding='utf-8')
    (d/'scene.py').write_text(f"import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ThreadBase\nclass Thread{i+1:02}(ThreadBase):\n    INDEX={i}\n",encoding='utf-8')
    (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n- 목적·주장: {claims[i]}\n- 입력 상태: '+('GPU 전체 지도' if i==0 else titles[i-1])+f'\n- 확정 구간: {bounds[i]}–{bounds[i+1]}초 ({m["duration_seconds"]}초), 사용자 문장 종료 시각. 음원 미제공.\n- TTS 원문: [script.txt](script.txt). 실제 음원 길이는 미측정.\n- 화면·타임라인: 공통 visuals.py의 INDEX={i} 분기. 문장 종료 시각에 따라 코드 강조·값·연결 변화.\n- 화면 텍스트: {title}; 해당 CUDA 식과 실제 배열 값.\n- 시작·종료 상태: 해당 주장 대상 등장 → 동작 시각화 → 주장이 드러난 상태 유지.\n- 연결: '+(titles[i+1] if i<15 else '같은 Block 안의 Thread와 서로 다른 index에서 종료; 영상 내 예고 없음')+'\n- 정확성: 논리 실행 문맥과 물리 연산기를 구별. Register 배치는 개념도이며 기계 명령 trace가 아님. 세로·가로 레이아웃 공통 주장.\n',encoding='utf-8')
example=P/'scenes/01_example'
if example.exists():
    # Template-only examples are retained outside the active scene index.
    example.rename(P/'template_example')
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'scenes.yaml').write_text('id: gpuh01_thread\ntitle: "GPU의 스레드 하나는 무엇을 할까?"\nvideo:\n  fps: 30\n  layouts:\n    shorts: [1080, 1920]\n    longform: [1920, 1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n    transition: cut\n' for m in manifest),encoding='utf-8')
story='\n\n'.join(f'### {c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues)
for name in ['narration.md','master_script.md']:(P/name).write_text('# GPU 계층 구조 LEVEL 01 — Thread\n\n사용자 확정 원문·종료 시각 기준 152초.\n\n'+story+'\n',encoding='utf-8')
pronounce={'GPU':'지피유','CPU':'씨피유','CUDA':'쿠다','__global__':'글로벌','threadIdx.x':'스레드 인덱스 점 엑스','blockIdx.x':'블록 인덱스 점 엑스','blockDim.x':'블록 디멘션 점 엑스','SM':'에스엠'}
paras=[]
for m in manifest:
    t=' '.join(c['caption'] for c in cues if m['start']<=c['start']<m['end'])
    for old,new in pronounce.items():t=t.replace(old,new)
    paras.append(t)
(P/'tts_script.txt').write_text('\n\n'.join(paras)+'\n',encoding='utf-8')
(P/'brief.md').write_text('''# GPU 계층 구조 01 — Thread

- 사용자 원문과 33개 문장 종료 시각 기준 152초. 새 대본 추정 타이밍 없음.
- 16개 독립 Manim 씬. 가로 1920×1080·세로 1080×1920, 30fps. 미리보기는 640×360·360×640, 15fps.
- 하드웨어/논리 구조가 주 화면, CUDA 코드는 보조 화면. 선택한 코드에 실제 값·Thread·주소가 반응한다.
- 배열 A=[1,2,3,4], B=[10,20,30,40], C=[11,22,33,44]. 후반 두 Block 예시는 index 공간만 8칸으로 확장한다.
- 4 Thread는 교육용 축소 예시. Warp는 32 lane이며 Thread와 물리 core는 일대일이 아니다.
- Register File은 SM에 그리며 Thread 카드와 연결. 소스 수준 동작이며 실제 명령 순서·Register 배치는 compiler에 따라 다름.
- CPU 반복문은 표현 예시이며 CPU 병렬화를 부정하지 않는다. 2D 좌표는 물리 배치가 아님.
- 음원 미제공: 무음·자막 영상, TTS 원고는 별도 제공. 이전 편 복습·다음 편 예고 없음.
- CUDA: vector_add.cu에 경계 검사·오류 확인·CPU 결과 비교 포함. 실행 검증 결과는 README 참조.
''',encoding='utf-8')
# Adapt the existing exact-frame two-layout pipeline.
build=(ROOT/'longforms/dot04_orthonormal_coordinates/build.py').read_text(encoding='utf-8')
build=build.replace('137','152').replace('DOT_LAYOUT','GPUH_LAYOUT').replace('dot04_orthonormal_coordinates','gpuh01_thread').replace('dot04','gpuh01')
(P/'build.py').write_text(build,encoding='utf-8')
shutil.copy2(Path(r'C:/Users/as042/.codex/attachments/994fce5a-6339-4613-a075-f5c389542600/붙여넣은 텍스트.txt'),P/'storyboard.md')
print('CREATED',P,len(cues),'cues',len(manifest),'scenes')
