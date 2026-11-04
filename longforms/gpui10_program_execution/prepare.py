import json
from pathlib import Path
R=Path(__file__).resolve().parent
TITLE='GPU 개론 10 — 컴퓨터는 어떻게 프로그램을 실행할까?'
SCRIPT='''6|앞서 우리는 0과 1로 명령어를 표현하고, 이를 해독해 실제 회로의 동작을 제어하는 방법을 살펴봤습니다.
10|이제 컴퓨터는 하나의 명령어에 따라 계산을 수행할 수 있습니다.
14|하지만 실제 프로그램은 하나의 명령어로 끝나지 않습니다.
18|그렇다면 컴퓨터는 다음에 실행할 명령어를 어떻게 알 수 있을까요?
22|먼저 여러 명령어를 미리 저장해 놓는다고 생각해 보겠습니다.
27|명령어도 결국 0과 1로 이루어진 정보이므로, 메모리에 보관할 수 있습니다.
34|예를 들어 첫 번째 위치에는 두 값을 더하는 명령어를, 두 번째 위치에는 두 값을 빼는 명령어를 저장할 수 있습니다.
37|이제 명령어를 하나씩 외부에서 전달하지 않아도 됩니다.
40|하지만 메모리에는 여러 명령어가 존재합니다.
43|그렇다면 그중 어떤 명령어를 가져와야 할까요?
47|여기서 앞서 살펴본 레지스터를 다시 활용할 수 있습니다.
51|이번에는 계산 결과가 아니라, 가져올 명령어의 위치를 저장하는 것입니다.
57|이렇게 명령어의 주소를 기억하는 레지스터를 프로그램 카운터, 즉 PC라고 합니다.
63|예를 들어 PC에 0이 저장되어 있다면, 명령어 메모리의 0번 위치에 있는 명령어를 가져옵니다.
66|가져온 명령어는 앞서 만든 해독 회로로 전달됩니다.
72|해독 회로는 어떤 데이터를 선택하고, 어떤 연산을 수행할지 결정하는 제어 신호를 만듭니다.
76|그리고 ALU가 계산을 수행하고, 필요한 경우 결과를 레지스터에 기록합니다.
80|이제 다음 명령어를 실행하려면 PC에 저장된 주소를 갱신해야 합니다.
85|명령어가 순서대로 배치되어 있다면, PC를 다음 위치로 증가시키면 됩니다.
91|이렇게 명령어를 가져오고, 해독하고, 실행하는 과정을 인출, 해독, 실행이라고 합니다.
94|영어로는 Fetch, Decode, Execute입니다.
98|그런데 컴퓨터가 항상 다음 위치의 명령어만 실행해야 할까요?
103|예를 들어 어떤 계산 결과가 0일 때, 특정 명령어를 건너뛰고 싶을 수도 있습니다.
107|이때는 PC를 단순히 증가시키는 대신, 다른 주소로 변경하면 됩니다.
114|앞서 살펴본 MUX를 이용하면 순서대로 이어지는 주소와 이동하려는 주소 중 하나를 선택할 수 있습니다.
120|이처럼 조건에 따라 다음에 실행할 명령어의 위치를 바꾸는 것이 분기의 기본적인 원리입니다.
126|이제 컴퓨터는 단순히 정해진 연산을 반복하는 것을 넘어, 조건에 따라 실행 순서를 바꿀 수 있게 되었습니다.
132|지금까지 우리는 전기 신호에서 출발해 논리 게이트와 가산기, ALU를 만들었습니다.
137|그리고 값을 기억하는 회로와 클럭을 추가하고, 레지스터와 데이터 경로를 연결했습니다.
141|여기에 명령어를 해독하는 회로와 프로그램 카운터까지 더했습니다.
148|이렇게 우리는 계산하는 회로가 여러 명령어를 실행하는 기본적인 프로세서 구조로 발전하는 과정을 살펴봤습니다.
153|물론 이것만으로 현대적인 CPU나 GPU의 모든 기능이 완성된 것은 아닙니다.
156|하지만 이제 새로운 질문을 던질 수 있습니다.
159|같은 명령어들을 더 빠르게 실행하려면 무엇을 바꿔야 할까요?
165|다음에는 컴퓨터가 계산 속도를 높이기 위해 어떤 구조를 발전시켜 왔는지 살펴보겠습니다.'''
SCENES=[(0,18,'hook','다음 명령어는 어떻게 알까?','단일 명령의 실행에서 다음 명령어 선택 문제로 연결한다.'),(18,34,'memory','명령어도 메모리에 저장한다','주소0 ADD54,주소1 SUB125를 고정된 메모리에 보관한다.'),(34,43,'address','어느 위치의 명령어를 가져올까?','저장된 여러 명령어 중 하나를 고르는 주소 입력이 필요하다.'),(43,57,'pc','명령어의 위치를 기억하는 레지스터','PC는 명령어 자체가 아니라 인출할 주소를 기억한다.'),(57,63,'fetch','PC = 0 → 주소 0 인출','PC Q가 메모리 주소를 선택하고 그 위치의 비트열이 출력된다.'),(63,76,'decode_execute','인출한 명령어로 계산한다','해독 제어로5+3을 계산하고 유효한 에지에서R3=8을 기록한다.'),(76,85,'advance','PC도 갱신해야 한다','PC+1=1을 D로 제공한 뒤 갱신 에지에서PC0→1로 이동한다.'),(85,94,'stages','인출 · 해독 · 실행','PC1의SUB를 인출·해독·실행해R3=8−5=3을 기록한다.'),(94,107,'condition','항상 다음 위치만 실행할까?','별도의 분기 예시로 순차 후보2와 목표3을 구별한다.'),(107,120,'branch','MUX로 다음 PC를 선택한다','고정배선된두후보를조건으로선택하고에지에서PC1→3으로갱신한다.'),(120,126,'paths','같은 메모리, 다른 실행 경로','분기는 명령어를 삭제하지 않고 다음 주소 선택을 바꾼다.'),(126,137,'assemble','계산과 저장을 하나의 구조로','신호→게이트→가산기→ALU와저장회로·클럭·데이터경로를연결한다.'),(137,148,'processor','여러 명령어를 실행하는 기본 구조','PC·메모리·해독·데이터경로와PC갱신을하나의시스템으로보여준다.'),(148,156,'limits','기본 구조에서 더 복잡한 시스템으로','현재모델은기본프로세서의교육용개념도임을명시한다.'),(156,165,'speed','같은 명령어를 더 빠르게 실행하려면?','성능수치를주장하지않고실행시간을줄일구조의질문으로끝낸다.')]
def phonetic(s):
 for a,b in [('ALU','에이 엘 유'),('MUX','먹스'),('PC','피 씨'),('CPU','씨 피 유'),('GPU','지 피 유'),('Fetch','페치'),('Decode','디코드'),('Execute','엑시큐트')]:s=s.replace(a,b)
 return s

def main():
 rows=[];start=0
 for line in SCRIPT.splitlines():
  e,s=line.split('|',1);e=int(e);rows.append(dict(start=start,end=e,text=s));start=e
 assert len(rows)==35 and start==165
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
 manifest=[];narr=['# '+TITLE,'','확정35문장 · 사용자제공165초 · 음원미제공. 발화자표기로 보이는 연우는 대본에 포함하지 않는다.','']
 for i,(a,b,slug,title,claim) in enumerate(SCENES,1):
  directory=f'scenes/{i:02}_{slug}';p=R/directory;p.mkdir(parents=True,exist_ok=True);rs=[r for r in rows if a<=r['start']<b];script='\n\n'.join(r['text'] for r in rs)
  (p/'script.txt').write_text(phonetic(script)+'\n',encoding='utf-8')
  (p/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import ProgramScene\nclass Scene{i:02}(ProgramScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=directory,**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title,method=slug))
  table='\n'.join(f'- {r["start"]}–{r["end"]}초: {r["text"]}' for r in rs)
  (p/'spec.md').write_text(f'''# {i:02} · {title}

目的・主張: {claim}

시작: {SCENES[i-2][3] if i>1 else '명령어·해독·ALU 기존 구조'}

확정길이: {a}–{b}초({b-a}초). 사용자 문장 종료 시각을 그대로 사용한다.

## 확정 대본·화면 변화 시각
{table}

## 화면과 텍스트
../../storyboard_reference.md의해당구간,../../scene_engine.py의{slug}참조. 가로1920×1080/세로1080×1920별도배치.30fps. PC와저장초록,메모리파랑,해독·연산보라,분기·제어주황. PC입출력D/Q·CLK,Address,InstructionMemory,Fetch/Decode/Execute,PC+1,BranchTarget,BranchTaken을일관되게사용한다. 자막한객체를문장경계에서교체하고세로최대높이1.95로제한한다.

## 정확성·전제
가상슬롯주소는명령어1개당+1이며실제ISA의바이트주소증분을일반화하지않는다.명령어형식OP|RD|RS1|RS2각2비트. ADD00110110,SUB01111101.초기R1=5,R2=3,R3=0→ADD후8→SUB후3. PC는주소,메모리는명령어,레지스터는계산데이터를보관한다. PC와일반레지스터쓰기에는해당유효갱신에지가필요하다.단계애니메이션은설명순서이지특정마이크로아키텍처의사이클수주장이아니다. 분기는별도예시로조건판정·목표주소계산후의선택을보여주며8비트산술ISA에분기명령인코딩을임의로추가하지않는다.조건거짓PC1→2,참PC1→3.명령어메모리는변하지않는다.후보두입력과MUX배선은고정한다. 사용자제공요약·마지막문장은유지하되추가GPU11예고·NEXT타이틀은넣지않는다.성능배율·현대CPU/GPU완성주장은없다.

종료: {claim}
연결: {'독립질문과기본구조의결론으로끝낸다.' if i==len(SCENES) else SCENES[i][3]}
검증:../../check_program.py,자막높이검사,최종프레임검토,ffprobe. 기술출처README.
'''.replace('目的・主張','목적·주장'),encoding='utf-8')
  narr.extend([f'## {a}–{b}초 · {title}','',table,''])
 for f in ['master_script.md','narration.md']:(R/f).write_text('\n'.join(narr),encoding='utf-8')
 (R/'tts_script.txt').write_text('\n\n'.join(phonetic(r['text']) for r in rows)+'\n',encoding='utf-8')
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('id: gpui10_program_execution\nduration_seconds: 165\naudio: null\nfps: 30\nlayouts: {longform: [1920, 1080], shorts: [1080, 1920]}\nscenes:\n'+'\n'.join(f'  - {{id: "{m["id"]}", directory: {m["directory"]}, class: {m["class"]}, start_seconds: {m["start"]}, duration_seconds: {m["duration_seconds"]}}}' for m in manifest)+'\n',encoding='utf-8')
 old=R.parent/'gpui09_instruction_control'
 for f in ['build.py','inspect_frames.py','inspect_caption_boundaries.py','verify_exports.py']:
  s=(old/f).read_text(encoding='utf-8').replace('gpui09_instruction_141s','gpui10_program_165s').replace('gpui09_instruction_control','gpui10_program_execution').replace('gpui09_{suffix}','gpui10_{suffix}').replace('==141','==165').replace('-141','-165').replace('141*fps','165*fps').replace('duration_seconds=141','duration_seconds=165').replace('==4230','==4950').replace('==27','==35').replace('==14','==15')
  if f=='inspect_frames.py':
   a=s.index('TIMES=');b=s.index('\n',a);s=s[:a]+'TIMES=[3,8,12,16,20,25,30,35,39,42,45,49,54,60,64,69,74,78,82,84,87,90,93,96,101,105,109,112,116,119,123,129,134,139,143,147,151,155,158,162,164]'+s[b:]
  (R/f).write_text(s,encoding='utf-8')
 (R/'check_instruction.py').write_text((old/'check_instruction.py').read_text(encoding='utf-8'),encoding='utf-8')
 if not (R/'scene_engine.py').exists():
  s=(old/'scene_engine.py').read_text(encoding='utf-8');common=s.split('COLORS=')[0].replace('class InstructionScene','class ProgramScene').replace(' /  09',' /  10').replace('/141','/165').replace(' / 14',' / 15')
  objects='COLORS='+s.split('COLORS=',1)[1].split('class Decoder(VGroup):')[0]
  (R/'scene_engine.py').write_text(common+objects,encoding='utf-8')
 print('Prepared35sentences /15scenes /165seconds')
if __name__=='__main__':main()
