"""Materialize the user's approved 175-second narration before producing visuals."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
SCRIPT='''5|앞서 우리는 논리 게이트를 연결해 실제 숫자의 덧셈을 구현하는 방법을 살펴봤습니다.
10|그렇다면 뺄셈이나 비교처럼 다른 연산이 필요할 때는 어떻게 해야 할까요?
14|가장 단순한 방법은 연산마다 새로운 회로를 만드는 것입니다.
19|하지만 연산의 종류가 늘어날수록 더 많은 트랜지스터와 배선이 필요하게 됩니다.
23|그렇다면 이미 만들어 놓은 회로를 다른 연산에도 활용할 수는 없을까요?
25|먼저 뺄셈을 생각해 보겠습니다.
30|우리는 두 숫자의 차이를 구할 때, 덧셈과는 다른 연산이라고 생각합니다.
33|그런데 이진수에서는 뺄셈을 덧셈의 형태로 바꿀 수 있습니다.
39|일정한 비트 수를 정하고, 빼려는 숫자의 각 비트를 반전한 다음 1을 더하는 것입니다.
41|이것을 2의 보수라고 합니다.
44|예를 들어 4비트에서 5에서 3을 빼보겠습니다.
47|5는 0101, 3은 0011입니다.
51|3의 비트를 반전하면 1100이고, 여기에 1을 더하면 1101이 됩니다.
57|이 값을 0101에 더하고 하위 4비트만 남기면 0010, 즉 2가 됩니다.
61|결국 별도의 뺄셈 회로 없이도 기존 덧셈 회로를 활용할 수 있는 것입니다.
69|더 나아가 입력 비트를 반전할지 결정하는 제어 신호를 추가하면, 하나의 가산기로 덧셈과 뺄셈을 모두 수행할 수 있습니다.
73|그렇다면 비교 연산도 기존 회로를 활용할 수 있을까요?
78|두 숫자가 같은지 확인하려면, 두 숫자를 뺀 결과가 0인지 살펴보면 됩니다.
83|크기 비교 역시 뺄셈에서 발생하는 결과와 상태 신호를 활용해 구현할 수 있습니다.
89|이처럼 새로운 연산이 필요하다고 해서 언제나 완전히 독립적인 계산 회로를 추가할 필요는 없습니다.
93|이미 구현한 연산을 다른 방식으로 활용할 수 있는 것입니다.
97|하지만 모든 연산을 하나의 덧셈 회로로 처리할 수 있는 것은 아닙니다.
101|AND나 OR 같은 논리 연산에는 다른 논리 구조를 사용할 수 있습니다.
106|그렇다면 이런 여러 연산 기능을 하나의 장치 안에 모아두면 어떨까요?
111|덧셈과 뺄셈을 수행하는 회로, 논리 연산을 수행하는 회로를 미리 구성하는 것입니다.
115|그리고 어떤 연산의 결과를 사용할지 선택하는 회로를 추가합니다.
120|이때 여러 입력 중 하나를 선택해 출력하는 회로를 멀티플렉서, 줄여서 MUX라고 합니다.
129|예를 들어 제어 신호가 00이면 덧셈, 01이면 뺄셈, 10이면 AND, 11이면 OR의 결과를 선택하도록 설계할 수 있습니다.
135|이러한 산술 연산과 논리 연산을 수행하는 장치를 ALU, 산술논리장치라고 합니다.
141|여기서 중요한 것은 제어 신호가 바뀐다고 트랜지스터의 물리적인 연결이 바뀌는 것은 아니라는 점입니다.
148|연산에 필요한 회로들은 미리 설계되어 있고, 입력 신호에 따라 그 회로들의 동작이나 결과 선택이 달라지는 것입니다.
156|이렇게 하면 매번 새로운 계산 장치를 만드는 대신, 기존의 회로를 재사용하고 여러 연산 기능을 하나의 장치에서 활용할 수 있습니다.
161|물론 지원할 수 있는 연산과 성능은 실제로 구현된 회로 구조에 따라 제한됩니다.
167|결국 컴퓨터의 연산 장치를 설계한다는 것은 가능한 모든 회로를 무작정 추가하는 일이 아닙니다.
175|어떤 연산을 공통된 회로로 처리하고, 어떤 기능을 별도로 구현하며, 그중 필요한 결과를 어떻게 선택할지 결정하는 과정입니다.'''
# One claim per independent, replaceable scene.
SCENES=[
 (0,14,'newcircuits','연산마다 회로가 필요할까?','독립 회로를 나열하는 초기 설계 가정을 보여준다.'),
 (14,23,'cost','기존 회로를 활용할 수 있다면','기능마다 독립 회로를 복제하면 소자와 배선이 늘어난다.'),
 (23,41,'complement','뺄셈을 덧셈으로 바꾸기','고정 n비트에서 A−B ≡ A+NOT(B)+1 mod 2ⁿ이다.'),
 (41,57,'example','4비트로 5 − 3을 계산하면','0101+1101=1|0010에서 하위 4비트와 별도 carry를 분리한다.'),
 (57,69,'shared','하나의 가산기로 ADD와 SUB','SUB를 B의 각 XOR와 최초 Cin에 함께 공급한다.'),
 (69,83,'compare','뺄셈 결과를 비교에 활용하기','결과·플래그와 추가 판단 논리를 이용해 동등·크기를 비교한다.'),
 (83,93,'reuse','계산 경로를 공유하는 설계','하나의 가산기에 입력 변환과 비교 판단 논리를 더해 기능을 재사용한다.'),
 (93,101,'logic','다른 기능에는 다른 논리 구조','AND·OR는 산술 공유 경로와 별도 논리 경로로 구현한다.'),
 (101,111,'integrate','여러 기능을 한 장치 안에','공통 입력이 산술·논리 경로에 분기된다.'),
 (111,120,'mux','여러 결과 중 하나를 선택','출력을 직접 단락하지 않고 별도의 MUX로 선택한다.'),
 (120,129,'select','같은 입력, 다른 선택 신호','예시 코드 00/01/10/11은 ADD/SUB/AND/OR 결과를 선택한다.'),
 (129,135,'name','산술논리장치 ALU','공유 산술·논리·결과 선택을 통합한 장치를 ALU라 부른다.'),
 (135,148,'fixed','배선은 고정, 신호는 변화','같은 토폴로지에서 제어·값·선택 경로만 바뀐다.'),
 (148,156,'overview','회로 재사용과 기능 통합','가산기·비교 판단·논리·선택이 하나의 구조를 이룬다.'),
 (156,161,'limits','구현된 기능에는 범위가 있다','이 예시 ALU에는 DIV 직접 경로가 구현되지 않았다.'),
 (161,175,'conclusion','재사용하고, 통합하고, 선택한다','공유할 연산·별도 기능·결과 선택을 함께 설계한다.'),
]
CUES=[
 [(0,5,'4개 FA를 하나의 ADDER로 정리'),(5,10,'SUBTRACT?·COMPARE? 빈 블록 추가'),(10,14,'각 블록에 독립 소자·배선 표시')],
 [(14,19,'세 블록과 소자·배선이 차지하는 영역 증가'),(19,23,'ADDER의 구조를 유지하며 재사용 강조')],
 [(23,25,'A−B와 기존 가산기'),(25,30,'A+(−B)로 변환'),(30,33,'고정 4비트·mod16 조건'),(33,36,'0011을 1100으로 반전'),(36,39,'1100+1=1101'),(39,41,'Two’s Complement 명명')],
 [(41,44,'5−3 질문과 4비트 프레임'),(44,47,'A0101·B0011'),(47,49,'B의 네 비트 반전1100'),(49,51,'+1로1101'),(51,54,'같은 ADDER에0101·1101 공급'),(54,57,'Cout1과 4비트 R0010 분리')],
 [(57,61,'기존 ADDER와 A·B 입력 유지'),(61,65,'B 비트별 XOR 네 개와 공통 SUB→Cin 배선 추가'),(65,67,'SUB0:0101+0011+0=1000'),(67,69,'SUB1:0101+1100+1=1|0010')],
 [(69,73,'공유 뺄셈과 COMPARE?'),(73,78,'5−5=0000, ZERO 검출→EQ1'),(78,83,'5−6=1111; N,V,C와 별도 비교 판단, signed N⊕V / unsigned NOT Cout')],
 [(83,89,'독립 세 회로와 공유 가산기·작은 보조 논리 비교'),(89,93,'ADD·SUB·COMPARE 기능이 같은 가산기를 활용')],
 [(93,97,'산술 공유 경로 강조'),(97,101,'별도 AND·OR 논리 경로 추가')],
 [(101,106,'통합 프레임과 공통 A·B'),(106,111,'A·B가 미리 설계된 세 계산 경로로 분기')],
 [(111,115,'세 결과선을 각각 별도 입력 핀으로 연결'),(115,120,'사다리꼴 MUX와 SEL, 선택한 경로만 최종 출력으로 전달')],
 [(120,123,'A0101·B0011 고정, ADD/SUB 공유 표시'),(123,124.5,'00 ADD→1000'),(124.5,126,'01 SUB→0010'),(126,127.5,'10 AND→0001'),(127.5,129,'11 OR→0111')],
 [(129,132,'통합 테두리와 내부 구성 유지'),(132,135,'ALU 외부 블록과 Arithmetic Logic Unit 명명')],
 [(135,141,'고정된 게이트·배선에서 선택00→01→10→11'),(141,148,'구조는 그대로, 입력·제어·값과 선택 강조만 변화')],
 [(148,152,'공유 가산기·플래그 판단·AND/OR·MUX 전체 구조'),(152,156,'공통 입력·선택 결과·통합 테두리 강조')],
 [(156,161,'ADD/SUB/AND/OR 지원; DIV: 이 예시 ALU에 미구현')],
 [(161,167,'독립 기능 나열과 공유·통합 설계 비교'),(167,171,'공통 산술 경로와 별도 논리 경로 강조'),(171,173,'REUSE→INTEGRATE→SELECT'),(173,175,'ALU와 세 키워드로 완결')],
]
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def phonetic(s):
 for a,b in [('AND','앤드'),('OR','오어'),('MUX','먹스'),('ALU','에이 엘 유')]:s=s.replace(a,b)
 return s
def main():
 rows=[];start=0
 for line in SCRIPT.splitlines():
  e,s=line.split('|',1);e=int(e);rows.append(dict(start=start,end=e,text=s));start=e
 assert len(rows)==35 and start==175
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
 manifest=[];narr=['# GPU 개론 05 — 하나의 회로로 여러 연산을 수행하는 방법','','확정 원문 35문장·사용자 문장 종료 시각 175초. 음원 미제공.','']
 for i,(a,b,slug,title,claim) in enumerate(SCENES,1):
  directory=f'scenes/{i:02}_{slug}';p=R/directory;p.mkdir(parents=True,exist_ok=True)
  selected=[r for r in rows if a<=r['start']<b];script='\n\n'.join(r['text'] for r in selected)
  (p/'script.txt').write_text(phonetic(script)+'\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=directory,**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title,method=slug))
  table='| 전체 초 | 화면 |\n| --- | --- |\n'+'\n'.join(f'| {x}–{y} | {s} |' for x,y,s in CUES[i-1])
  (p/'spec.md').write_text(f'''# {i:02} · {title}

## 목적·핵심 주장
{claim}

## 앞 장면·시작 상태
{SCENES[i-2][4] if i>1 else '4비트 ADDER와 논리 게이트에서 시작한다.'}

## 확정 TTS·길이
사용자 문장 종료 시각 {a}–{b}초, {b-a}초. 추정 발화시간이 아닌 확정 시각을 사용한다.

{script}

## 화면·타임라인
{table}

화면 텍스트는 위 용어·비트·수식. 하단은 원문 전체 자막을 한 번에 하나만 표시한다. 가로 1920×1080, 세로 1080×1920, 30fps. 사용자 콘티는 ../../storyboard_reference.md. 독립 씬 내 ADDER는 동일 객체를 유지하며 제어값만 갱신하고, 컷 뒤에도 동일한 공통 도형·배선으로 재현한다.

## 종료 상태·시각 연결
{claim} {'세 키워드와 ALU로 완결한다.' if i==16 else '다음 씬은 '+SCENES[i][3]+'로 구조를 확장한다.'} 영상에 추가 복습·다음 편 예고는 삽입하지 않는다.

## 수학 조건·과장 방지
고정 4비트·mod16. Cout은 결과 버스와 별도 핀이다. SUB는 B의 네 XOR 및 Cin 양쪽에 연결한다. 공유 ADD/SUB의 결과는 하나이며 ADD와 SUB 결과가 동시에 별도 가산기에서 계산되는 구조로 그리지 않는다. 00/01은 같은 산술 MUX 핀을 사용하고 01에서만 SUB1, 10/11은 AND/OR 핀을 선택한다. 선택 코드는 이 영상의 예시다. 비교에는 별도 판단 논리가 필요하며 EQ=Z, signed LT=N XOR V, unsigned LT=NOT Cout(본 회로 carry 관례)이다. 결과 신호선을 직접 단락하지 않는다. 배선 토폴로지는 선택 시 고정한다. DIV는 이 예시 ALU에 직접 구현되지 않았다는 뜻이다. 성능·면적 절감의 보편적 수치나 모든 회로의 비활성화를 주장하지 않는다.

검증: ../../check_alu.py. 참고: Berkeley CS61C adder/subtractor, Cornell CS3410 ALU, ANU ALU lab (프로젝트 README 링크).
''',encoding='utf-8')
  (p/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import ALUScene\nclass Scene{i:02}(ALUScene):\n    index={i-1}\n',encoding='utf-8')
  narr.extend([f'## {a}–{b}초 · {title}','']+[f'{r["start"]}–{r["end"]}초: {r["text"]}\n' for r in selected])
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('id: gpui05_alu_reuse\nduration_seconds: 175\naudio: null\nfps: 30\nlayouts: {longform: [1920, 1080], shorts: [1080, 1920]}\nscenes:\n'+'\n'.join(f'  - {{id: "{m["id"]}", directory: {m["directory"]}, class: {m["class"]}, start_seconds: {m["start"]}, duration_seconds: {m["duration_seconds"]}}}' for m in manifest)+'\n',encoding='utf-8')
 for name in ['master_script.md','narration.md']:(R/name).write_text('\n'.join(narr),encoding='utf-8')
 (R/'tts_script.txt').write_text('\n\n'.join(phonetic(r['text']) for r in rows)+'\n',encoding='utf-8')
 old=R.parent/'gpui04_binary_adder'
 for name in ['build.py','inspect_frames.py','inspect_caption_boundaries.py']:
  s=(old/name).read_text(encoding='utf-8').replace('gpui04_adder_143s','gpui05_alu_175s').replace('gpui04_binary_adder','gpui05_alu_reuse').replace('gpui04_{suffix}','gpui05_{suffix}').replace('==143','==175').replace('-143','-175').replace('duration_seconds=143','duration_seconds=175')
  if name=='inspect_frames.py':
   a=s.index('TIMES=');b=s.index('\n',a);s=s[:a]+'TIMES=[3,8,12,17,21,24,28,32,35,38,40,45,48,50,53,56,60,64,66,68,72,76,81,87,91,96,100,105,109,114,118,123,125,126,128,131,134,138,145,151,155,159,165,169,174]'+s[b:]
  (R/name).write_text(s,encoding='utf-8')
 print('Prepared 35 sentences / 16 scenes / 175 seconds')
if __name__=='__main__':main()
