import json,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
TITLE='GPU 개론 09 — 명령어는 어떻게 회로를 제어할까?'
SCRIPT='''7|앞서 우리는 레지스터에 저장된 값을 선택해 ALU로 전달하고, 계산 결과를 다시 저장하는 데이터 경로를 만들었습니다.
13|하지만 지금까지는 어떤 값을 선택하고, 어떤 연산을 수행할지 직접 지정해야 했습니다.
16|그렇다면 이러한 선택을 하나의 정보로 표현할 수는 없을까요?
22|예를 들어 첫 번째 레지스터에 5, 두 번째 레지스터에 3이 저장되어 있다고 생각해 보겠습니다.
27|두 값을 더해 세 번째 레지스터에 저장하려면 몇 가지 선택이 필요합니다.
30|먼저 첫 번째와 두 번째 레지스터의 값을 가져와야 합니다.
36|그리고 ALU가 덧셈을 수행하도록 설정하고, 결과는 세 번째 레지스터에 기록해야 합니다.
40|지금까지는 각각의 회로에 제어 신호를 전달해 이러한 동작을 결정했습니다.
46|그런데 우리가 계산할 숫자를 0과 1로 표현했던 것처럼, 수행할 동작도 0과 1로 표현하면 어떨까요?
53|예를 들어 두 비트의 값이 00이면 덧셈, 01이면 뺄셈을 의미하도록 규칙을 정할 수 있습니다.
58|마찬가지로 각 레지스터에도 번호를 부여하고, 이를 이진수로 표현할 수 있습니다.
63|이제 연산 종류와 입력 레지스터, 결과를 저장할 레지스터의 번호를 하나의 비트열로 묶어보겠습니다.
66|이것이 명령어의 기본적인 아이디어입니다.
73|예를 들어 첫 번째와 두 번째 레지스터의 값을 더해 세 번째 레지스터에 저장한다는 명령을 만들 수 있습니다.
78|하지만 비트열을 회로에 전달한다고 해서 ALU가 자동으로 그 의미를 이해하는 것은 아닙니다.
83|각 비트가 어떤 동작을 의미하는지 해석하고, 실제 회로에 필요한 제어 신호로 연결해야 합니다.
86|이를 담당하는 것이 명령어 해독 회로입니다.
95|해독 회로는 명령어의 각 부분을 확인해 어떤 레지스터를 선택할지, 어떤 연산을 수행할지, 결과를 어디에 저장할지 결정하는 신호를 만듭니다.
102|이 신호에 따라 MUX는 필요한 데이터를 ALU로 전달하고, ALU는 지정된 연산을 수행합니다.
105|그리고 계산 결과는 선택된 레지스터에 기록됩니다.
111|여기서 중요한 것은 명령어가 회로의 물리적인 연결을 바꾸는 것은 아니라는 점입니다.
114|연산 회로와 데이터 경로는 이미 설계되어 있습니다.
119|명령어는 그중 어떤 기능을 사용하고, 어떤 데이터를 전달할지 지정하는 것입니다.
126|이제 우리는 여러 제어 신호를 각각 직접 설정하는 대신, 하나의 명령어로 회로의 동작을 지정할 수 있게 되었습니다.
130|하지만 아직 명령어는 하나씩 외부에서 제공해야 합니다.
137|그렇다면 여러 명령어를 미리 저장해 놓고, 컴퓨터가 다음에 실행할 명령어를 스스로 찾아오도록 만들 수는 없을까요?
141|다음에는 여러 명령어가 순서대로 실행되는 구조를 살펴보겠습니다.'''
SCENES=[(0,16,'hook','여러 선택을 하나의 정보로','데이터 경로를 외부에서 지정하던 선택들의 묶음을 도출한다.'),(16,40,'choices','계산 한 번에도 필요한 선택','입력 R1/R2, ADD, 목적지 R3와 쓰기 시점을 각각 정한다.'),(40,46,'encode','동작도 0과 1로 표현한다','숫자뿐 아니라 수행할 동작도 인코딩 규칙을 정할 수 있다.'),(46,53,'opcodes','연산 종류를 비트로','교육용 OP 00 ADD / 01 SUB / 10 AND / 11 OR.'),(53,58,'registers','레지스터 번호를 비트로','R0=00 R1=01 R2=10 R3=11 식별자와 저장값을 구별한다.'),(58,66,'fields','네 선택을 하나의 비트열로','OP|RD|RS1|RS2 = 00|11|01|10 고정 순서로 구성한다.'),(66,73,'meaning','00110110의 의미','ADD R3,R1,R2는 R3←R1+R2를 의미한다.'),(73,83,'roles','비트열에는 연결 규칙이 필요하다','명령어 전체와 ALU의 데이터 입력 A/B는 역할이 다르다.'),(83,95,'decoder','명령어에서 제어 신호로','주소 필드 전달과 OP 해석으로 제어 정보를 생성한다.'),(95,105,'execute','선택 → 계산 → 기록','명령에 맞는 두 독립 읽기 경로와 유효 쓰기 에지에서 R3만 갱신한다.'),(105,119,'fixed','배선은 그대로, 선택만 변경','명령어 변경은 고정된 회로의 기능과 데이터 선택을 바꾼다.'),(119,126,'unified','하나의 명령어, 여러 제어 신호','명령어·해독·데이터 경로의 관계를 통합한다.'),(126,137,'next','다음 명령어는 어디에 있을까?','현재 만든 구조에는 다음 명령어를 자동으로 가져오는 기능이 없다.'),(137,141,'closing','명령어 하나의 실행 구조','완성한 명령어→제어→계산→저장 구조로 끝낸다.')]
def phonetic(s):
 for a,b in [('ALU','에이 엘 유'),('MUX','먹스')]:s=s.replace(a,b)
 return s

def main():
 rows=[];start=0
 for line in SCRIPT.splitlines():
  e,s=line.split('|',1);e=int(e);rows.append(dict(start=start,end=e,text=s));start=e
 assert len(rows)==27 and start==141
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
 manifest=[];narr=['# '+TITLE,'','확정 대본 27문장 · 사용자 제공 종료 시각 141초 · 음원 미제공','']
 for i,(a,b,slug,title,claim) in enumerate(SCENES,1):
  directory=f'scenes/{i:02}_{slug}';p=R/directory;p.mkdir(parents=True,exist_ok=True);rs=[r for r in rows if a<=r['start']<b]
  script='\n\n'.join(r['text'] for r in rs)
  (p/'script.txt').write_text(phonetic(script)+'\n',encoding='utf-8')
  (p/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import InstructionScene\nclass Scene{i:02}(InstructionScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=directory,**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title,method=slug))
  table='\n'.join(f'- {r["start"]}–{r["end"]}초: {r["text"]}' for r in rs)
  (p/'spec.md').write_text(f'''# {i:02} · {title}

주장: {claim}

시작: {SCENES[i-2][3] if i>1 else '레지스터·MUX·ALU 데이터 경로'}

확정 길이: {a}–{b}초, {b-a}초. 사용자 제공 발화시간을 그대로 사용한다.

## 확정 대본 및 화면 변화 시점
{table}

## 화면
상세 콘티 ../../storyboard_reference.md, 구현 ../../scene_engine.py의 {slug}. 가로1920×1080/세로1080×1920 별도 배치,30fps. OP 주황,RD 초록,RS1 파랑,RS2 보라. 중앙의 기존 데이터 경로를 유지하고 필드별 연결과 활성 경로를 강조한다. 자막은 문장 경계에 단일 Text를 교체하며 전환 중 중첩하지 않는다.

## 정확성
8비트는 교육용 가상 ISA이며 GPU/CUDA 기계어가 아니다. OP|RD|RS1|RS2의 네 2비트 필드다. 00110110은 ADD R3,R1,R2. 레지스터 식별자는 번호이고 저장값은 별도의4비트 데이터다. R0도 일반 레지스터로 가정하며 특정 실제ISA의zero레지스터를 암시하지 않는다. 주소 필드는 읽기·쓰기 선택에 전달될 수 있으며 OP는 이미 설계된 해독 논리로 ALU 제어를 만든다. WE는 실행 유효 시점의 제어이며 임의의 특정 명령어 비트 하나로 설명하지 않는다. 쓰기 대상 선택+WE+CLK상승에지에서만 갱신하며 읽기는 비파괴적이다. ADD→SUB 비교 때 WE=0으로 R3=8을 유지한다. 배선·블록 위치는 변경하지 않는다. 후속 명령어는 ???????? 자리 표시자이며 이번 편에서 실행하지 않는다. 사용자 도입·끝 원문은 유지하되 추가 복습 및 GPU10 예고 타이틀은 넣지 않는다.

종료: {claim}
검증: ../../check_instruction.py, 프레임검수 및 ffprobe. 소스: README의 Berkeley 제어논리 자료.
''',encoding='utf-8')
  narr.extend([f'## {a}–{b}초 · {title}','',table,''])
 for f in ['master_script.md','narration.md']:(R/f).write_text('\n'.join(narr),encoding='utf-8')
 (R/'tts_script.txt').write_text('\n\n'.join(phonetic(r['text']) for r in rows)+'\n',encoding='utf-8')
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('id: gpui09_instruction_control\nduration_seconds: 141\naudio: null\nfps: 30\nlayouts: {longform: [1920, 1080], shorts: [1080, 1920]}\nscenes:\n'+'\n'.join(f'  - {{id: "{m["id"]}", directory: {m["directory"]}, class: {m["class"]}, start_seconds: {m["start"]}, duration_seconds: {m["duration_seconds"]}}}' for m in manifest)+'\n',encoding='utf-8')
 old=R.parent/'gpui08_register_datapath'
 for f in ['build.py','inspect_frames.py','inspect_caption_boundaries.py','verify_exports.py']:
  s=(old/f).read_text(encoding='utf-8').replace('gpui08_datapath_153s','gpui09_instruction_141s').replace('gpui08_register_datapath','gpui09_instruction_control').replace('gpui08_{suffix}','gpui09_{suffix}').replace('==153','==141').replace('-153','-141').replace('153*fps','141*fps').replace('duration_seconds=153','duration_seconds=141').replace('==4590','==4230').replace('==31','==27')
  if f=='inspect_frames.py':
   a=s.index('TIMES=');b=s.index('\n',a);s=s[:a]+'TIMES=[3,9,14,19,24,29,33,38,43,48,51,55,59,62,65,69,75,80,85,88,92,97,100,104,108,113,117,122,128,133,136,139]'+s[b:]
  (R/f).write_text(s,encoding='utf-8')
 # Reuse only typography, caption timing and framing helpers; circuit is episode-specific.
 s=(old/'scene_engine.py').read_text(encoding='utf-8').split('class Register(VGroup):')[0].replace('from check_datapath import bits,integer,mux,write,compute','from check_instruction import decode,alu,execute').replace('class DatapathScene','class InstructionScene').replace(' /  08',' /  09').replace('/153','/141')
 if not (R/'scene_engine.py').exists():(R/'scene_engine.py').write_text(s,encoding='utf-8')
 print('Prepared27sentences /14scenes /141seconds')
if __name__=='__main__':main()
