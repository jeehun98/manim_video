"""Materialize the approved narration and exact 164-second, 14-scene plan."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
SCRIPT='''4|앞서 우리는 전압으로 전류의 흐름을 제어하는 트랜지스터를 살펴봤습니다.
9|그런데 단순히 전류가 흐르는 통로를 열고 닫는 것만으로 어떻게 계산이 가능할까요?
12|두 개의 스위치가 있다고 생각해 보겠습니다.
16|먼저 두 스위치를 하나의 통로에 직렬로 연결해 보겠습니다.
19|이 경우 두 스위치가 모두 닫혀야 전류가 흐를 수 있습니다.
22|반대로 두 스위치를 병렬로 연결하면 어떨까요?
26|이번에는 둘 중 하나만 닫혀도 전류가 흐를 수 있습니다.
28|스위치 자체는 달라지지 않았습니다.
33|단지 연결하는 방식만 바꿨을 뿐인데, 전류가 흐를 수 있는 조건이 달라진 것입니다.
36|이것을 논리적인 규칙으로 표현해 보겠습니다.
40|두 입력이 모두 참일 때만 참이 되는 규칙을 AND라고 합니다.
43|둘 중 하나 이상이 참이면 참이 되는 규칙은 OR입니다.
45|그런데 여기서 중요한 점이 있습니다.
50|이러한 규칙을 계산하는 별도의 소프트웨어가 실행되고 있는 것은 아닙니다.
55|스위치의 물리적인 연결 구조가 이미 특정한 입력과 출력의 관계를 결정하고 있는 것입니다.
63|실제 디지털 회로에서는 트랜지스터들을 전원과 접지에 연결해, 입력에 따라 출력 전압이 달라지도록 설계할 수 있습니다.
71|예를 들어 두 개의 nMOS를 직렬로 연결하고, 이에 대응하는 pMOS들을 병렬로 배치하면 NAND라는 논리 게이트를 구현할 수 있습니다.
75|NAND는 두 입력이 모두 1일 때만 0을 출력합니다.
81|이 역시 입력을 분석하는 프로그램이 아니라, 트랜지스터들의 연결 구조와 전기적 특성으로 구현된 결과입니다.
88|그리고 이러한 논리 게이트들을 다시 조합하면 NOT, AND, OR를 비롯한 다양한 논리 연산을 구현할 수 있습니다.
93|실제로 NAND 게이트만으로도 모든 불 논리 함수를 구성할 수 있습니다.
95|이러한 성질을 기능적 완전성이라고 합니다.
100|그렇다면 논리 게이트를 얼마든지 조합해 모든 계산 문제를 해결할 수 있을까요?
106|논리 함수를 구현할 수 있다는 것과, 실제 하드웨어에서 효율적으로 계산할 수 있다는 것은 다른 문제입니다.
111|우선 회로가 구현하는 규칙은 물리적인 연결 구조에 의해 결정됩니다.
119|일반적인 고정 기능 회로에서는 다른 연산을 수행하고 싶다고 해서, 소프트웨어 명령만으로 트랜지스터의 배선이 바뀌지는 않습니다.
124|또한 회로를 복잡하게 구성할수록 더 많은 트랜지스터와 배선이 필요합니다.
129|신호는 물리적인 회로를 통해 전달되기 때문에 출력이 즉시 결정되는 것도 아닙니다.
135|트랜지스터의 전도 상태가 변하고, 회로의 정전용량이 충전되거나 방전되는 데에는 시간이 필요합니다.
139|이 과정에서는 에너지가 소비되고, 일부는 열로 방출됩니다.
145|결국 논리 회로를 설계한다는 것은 단순히 원하는 계산 규칙을 구현하는 것에서 끝나지 않습니다.
152|얼마나 많은 회로가 필요한지, 얼마나 빠르게 동작하는지, 얼마나 많은 에너지를 소비하는지도 함께 고려해야 합니다.
158|우리는 이제 단순한 전기적 스위치의 연결만으로 논리 연산을 구현할 수 있다는 사실을 확인했습니다.
164|그렇다면 이러한 논리 회로들을 조합해 실제 숫자의 덧셈까지 구현하려면 어떻게 해야 할까요?'''
SCENES=[
 (0,12,'switches','스위치 두 개로 무엇을 할까?','동일한 두 스위치에서 연결 조건을 탐구한다.'),
 (12,19,'series','두 조건이 모두 필요한 연결','직렬 경로는 두 스위치가 모두 닫혀야 연결된다.'),
 (19,33,'parallel','하나만 연결되어도 되는 배치','동일한 스위치를 병렬로 재배치하면 한쪽만 닫혀도 경로가 연결된다.'),
 (33,43,'rules','연결 조건에 이름을 붙이면','경로 연결의 참·거짓 조건을 AND·OR로 표현할 수 있다.'),
 (43,55,'physical_rule','연결 구조가 곧 규칙','별도의 소프트웨어가 없어도 연결 구조가 조건을 구현한다.'),
 (55,63,'voltage','경로 조건에서 출력 전압으로','출력의 논리값은 전원·접지 연결이 결정하는 전압이다.'),
 (63,71,'nand_build','실제 CMOS NAND의 구조','pMOS 병렬·nMOS 직렬 네트워크가 출력 노드를 공유한다.'),
 (71,81,'nand_states','NAND의 출력은 왜 반대일까?','네 입력 조합에서 전원·접지 연결을 추적해 NAND 출력을 검증한다.'),
 (81,88,'compose','게이트를 다시 연결하면','NAND 게이트를 연결해 NOT·AND·OR를 구현한다.'),
 (88,95,'complete','NAND만으로 만드는 논리','NAND는 유한 이진 입력의 임의 불 함수를 구성하는 기능적 완전성을 갖는다.'),
 (95,119,'fixed','구현 가능성과 효율은 다르다','고정 단일 기능 회로의 배선과 함수는 입력값만으로 임의 변경되지 않는다.'),
 (119,139,'costs','회로에는 물리적 비용이 있다','회로는 면적·전파 지연·에너지 비용을 갖는다.'),
 (139,152,'tradeoffs','기능과 함께 설계할 세 가지','면적·지연·에너지는 배선·깊이·부하 등과 함께 검토해야 한다.'),
 (152,164,'arithmetic','연결 규칙에서 숫자 계산으로','논리 회로를 조합하는 관점에서 새로운 산술 블록을 질문한다.'),
]
CUES=[
 [(0,4,'MOSFET의 전도 채널 형성'),(4,9,'간단한 전압 제어 스위치로 단순화'),(9,12,'같은 스위치를 복제해 A·B 표시')],
 [(12,16,'하나의 폐회로에 A·B 직렬 배치, 00→10→01'),(16,19,'11에서만 전체 경로가 연결됨')],
 [(19,22,'같은 A·B를 두 갈래로 재배열'),(22,26,'A만 닫아 첫 경로 연결'),(26,28,'부품은 그대로임을 강조'),(28,33,'B만 닫기·둘 다 닫기로 병렬 조건 확인')],
 [(33,36,'직렬·병렬과 연결 여부 비교'),(36,40,'직렬 조건 AND 명명'),(40,43,'병렬 조건 OR 명명')],
 [(43,45,'입력 상태 변화와 두 연결 조건 관찰'),(45,50,'가상 코드 창을 흐리게 제거해도 회로 상태는 변함'),(50,55,'물리 배선과 논리 규칙 강조')],
 [(55,59,'VDD 연결로 출력 HIGH'),(59,63,'GND 연결로 출력 LOW')],
 [(63,66,'출력 아래의 nMOS A·B 직렬'),(66,69,'출력 위의 pMOS A·B 병렬'),(69,71,'두 네트워크와 공통 입력·출력 확인')],
 [(71,75,'A=B=1에서 pMOS 모두 OFF·nMOS 모두 ON·Y=0'),(75,81,'00→01→10→11의 공급 경로와 진리표 동기화')],
 [(81,84,'NAND 기호로 축약'),(84,88,'NAND만 연결한 NOT·AND·OR 네트워크 세 개')],
 [(88,91,'세 네트워크의 NAND 구성과 식 표시'),(91,93,'논리 조합의 범위 확장'),(93,95,'Functional Completeness 명명')],
 [(95,100,'기존 AND 회로의 네 입력 조합'),(100,106,'AND와 XOR의 01 입력 결과를 비교'),(106,111,'고정된 배선을 강조'),(111,119,'네 NAND로 구성한 다른 XOR 배선 표시')],
 [(119,124,'소자·배선이 늘어나는 칩 면적'),(124,129,'네 NAND 단계의 순차적 출력 변화'),(129,135,'출력 부하 정전용량 충전·방전'),(135,139,'스위칭 에너지·열과 누설 주의')],
 [(139,145,'기능 네트워크와 Area·Delay·Energy 통합'),(145,152,'회로 확장 시 면적·깊이·부하·전환을 정성 비교')],
 [(152,158,'트랜지스터→NAND→논리 회로 블록'),(158,161,'새 연산 블록으로 묶기'),(161,164,'A·B 입력과 SUM·CARRY 물음표 출력')],
]
def stamp(t):
 t=int(t*1000);return f'{t//3600000:02}:{t//60000%60:02}:{t//1000%60:02},{t%1000:03}'
def main():
 rows=[];start=0
 for line in SCRIPT.splitlines():
  end,s=line.split('|',1);end=int(end);rows.append(dict(start=start,end=end,text=s));start=end
 assert len(rows)==34 and start==164
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
 manifest=[];narr=['# GPU 개론 03 — 스위치의 연결이 어떻게 논리 연산이 될까?','','사용자 원문 34문장·종료 시각 기준 164초. 음원 미제공.','']
 yaml=['id: gpui03_logic_connections','title: "스위치의 연결이 어떻게 논리 연산이 될까?"','duration_seconds: 164','video:','  fps: 30','  layouts:','    longform: [1920, 1080]','    shorts: [1080, 1920]','audio: null','scenes:']
 for i,(a,b,slug,title,claim) in enumerate(SCENES,1):
  directory=f'scenes/{i:02}_{slug}';folder=R/directory;folder.mkdir(parents=True,exist_ok=True)
  selected=[r for r in rows if a<=r['start']<b];script='\n\n'.join(r['text'] for r in selected)
  (folder/'script.txt').write_text(script+'\n',encoding='utf-8')
  (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import LogicScene\n\nclass Scene{i:02}(LogicScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=directory,**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title))
  yaml.extend([f'  - id: "{i:02}"',f'    directory: {directory}',f'    class: Scene{i:02}',f'    start_seconds: {a}',f'    end_seconds: {b}',f'    duration_seconds: {b-a}','    transition: cut'])
  table='| 전체 시각(초) | 화면 |\n| --- | --- |\n'+'\n'.join(f'| {x}–{y} | {e} |' for x,y,e in CUES[i-1])
  spec=f'''# {i:02} · {title}

## 목적·주장
{claim}

## 시작 상태·앞 장면
{'MOSFET의 채널 형성에서 시작한다.' if i==1 else SCENES[i-2][4]}

## 확정 TTS와 길이
사용자 종료 시각 {a}–{b}초, {b-a}초. 음원 미제공. 추정 길이를 사용하지 않는다.

{script}

## 화면과 타임라인
{table}

구현: ../../scene_engine.py의 {slug} 메서드. 사용자 콘티 원문: ../../storyboard_reference.md. 화면에는 입력 A·B, 경로 상태 또는 OUTPUT Y와 핵심 용어만 표시하고 하단에는 전체 문장 자막을 둔다.

## 종료 상태·연결
{claim}
{'A·B와 SUM·CARRY 출력의 물음표로 종료한다.' if i==14 else '이 상태를 이어 '+SCENES[i][3]+'로 확장한다.'}

## 조건·과장 방지
직렬·병렬의 연결 조건과 CMOS의 출력 전압을 같은 비트로 취급하지 않는다. pMOS는 병렬, nMOS는 직렬이며 각 네트워크가 공통 출력에 연결된다. Gate 입력선은 전도 경로와 분리한다. 정적 논리 상태의 전원·접지 경로는 상보적이다. NAND의 네 입력과 모든 파생 네트워크의 진리표는 check_logic.py로 검증한다. 기능적 완전성은 유한 이진 입력의 불 함수에 관한 성질이다. 고정 기능 회로와 ALU의 기능 선택을 구별한다. 면적·지연·에너지는 정성 모형이며 실측 수치나 선형 비례를 제시하지 않는다. 사용자 도입·마지막 질문은 그대로 유지한다.
'''
  (folder/'spec.md').write_text(spec,encoding='utf-8')
  narr.extend([f'## {a}–{b}초 · {title}','']+[f'{r["start"]}–{r["end"]}초: {r["text"]}\n' for r in selected])
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');(R/'scenes.yaml').write_text('\n'.join(yaml)+'\n',encoding='utf-8')
 for name in ['master_script.md','narration.md']:(R/name).write_text('\n'.join(narr),encoding='utf-8')
 tts=[]
 for r in rows:
  s=r['text']
  for a,b in [('NAND','낸드'),('nMOS','엔모스'),('pMOS','피모스'),('NOT','낫'),('AND','앤드'),('OR','오어'),('0을','영을'),('1일','일일')]:s=s.replace(a,b)
  tts.append(s)
 (R/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
 old=R.parent/'gpui02_transistor'
 for name in ['build.py','inspect_frames.py','inspect_caption_boundaries.py']:
  s=(old/name).read_text(encoding='utf-8').replace('gpui02_transistor_142s','gpui03_logic_164s').replace('gpui02_transistor','gpui03_logic_connections').replace("f'gpui02_{suffix}'","f'gpui03_{suffix}'").replace('==142','==164').replace('-142','-164').replace('duration_seconds=142','duration_seconds=164')
  if name=='inspect_frames.py':
   a=s.index('TIMES=');b=s.index('\n',a);s=s[:a]+'TIMES=[2,7,11,15,18,24,31,38,42,48,57,61,67,73,77,85,91,94,103,110,116,122,127,132,137,143,150,155,162]'+s[b:]
  if name=='inspect_caption_boundaries.py':s=s.replace("expr='+'.join(f'eq(n,{n})' for n in frames)","expr='+'.join(f'between(n,{max(0,int(t*fps)-1)},{int(t*fps)+1})' for t in boundaries)")
  (R/name).write_text(s,encoding='utf-8')
 print('Prepared 34 sentences, 14 independent scenes, 164 seconds.')
if __name__=='__main__':main()
