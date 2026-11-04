import json
from pathlib import Path
R=Path(__file__).resolve().parent
SCRIPT='''6|앞서 우리는 논리 게이트로 값을 기억하는 회로를 만들고, 클럭을 이용해 저장 시점을 제어하는 방법을 살펴봤습니다.
11|그렇다면 저장한 값을 실제 계산에 다시 사용하려면 어떻게 해야 할까요?
14|먼저 우리가 만들었던 저장 회로를 생각해 보겠습니다.
18|하나의 저장 회로는 0 또는 1, 즉 하나의 비트를 기억할 수 있습니다.
24|그런데 ALU가 계산하는 숫자는 하나의 비트로 표현되지 않을 수도 있습니다.
27|예를 들어 숫자 5를 이진수로 나타내면 0101입니다.
31|이 값을 저장하려면 네 개의 비트를 각각 기억해야 합니다.
35|그렇다면 하나의 비트를 저장하는 회로 네 개를 나란히 배치하면 어떨까요?
41|각 회로가 하나의 비트를 담당하고, 공통된 클럭을 이용해 값을 갱신하도록 만드는 것입니다.
45|이렇게 여러 비트를 하나의 값으로 묶어 저장하는 회로를 레지스터라고 합니다.
50|이제 우리는 계산 결과인 숫자 8도 레지스터에 보관할 수 있습니다.
52|그런데 여기서 새로운 문제가 생깁니다.
60|앞서 살펴본 것처럼 하나의 ALU로 여러 단계의 계산을 수행하려면, 저장된 값을 다시 ALU의 입력으로 가져와야 합니다.
65|예를 들어 5와 3을 더한 다음, 그 결과에 다시 2를 더한다고 생각해 보겠습니다.
69|먼저 ALU가 5와 3을 계산하면 결과인 8이 나옵니다.
72|이 값을 레지스터에 저장합니다.
77|이제 두 번째 계산에서는 처음 입력했던 5 대신, 레지스터에 저장된 8을 사용해야 합니다.
81|그렇다면 ALU의 입력에 연결할 값을 어떻게 바꿀 수 있을까요?
86|여기서 앞서 살펴본 멀티플렉서, 즉 MUX를 다시 사용할 수 있습니다.
91|MUX는 여러 입력 중 제어 신호로 지정한 하나를 선택해 출력으로 전달하는 회로입니다.
97|처음에는 숫자 5를 선택하고, 다음 계산에서는 레지스터에 저장된 8을 선택하는 것입니다.
102|이렇게 하면 ALU 자체를 변경하지 않고도 서로 다른 데이터를 이용해 계산할 수 있습니다.
107|하지만 실제 계산에서는 하나의 값만 저장하는 것으로 충분하지 않을 수 있습니다.
112|5와 3, 그리고 계산 결과인 8을 동시에 보관하려면 여러 레지스터가 필요합니다.
118|이때 어느 레지스터의 값을 읽고, 계산 결과를 어느 레지스터에 기록할지도 결정해야 합니다.
127|이처럼 저장된 데이터를 선택해 연산 회로로 전달하고, 계산 결과를 다시 저장하는 연결 구조를 데이터 경로, 즉 Datapath라고 합니다.
134|여기서 중요한 것은 ALU가 계산을 담당하고, 레지스터가 값을 보관하며, 데이터 경로가 이들을 연결한다는 점입니다.
139|이제 우리는 계산하는 회로와 기억하는 회로를 하나의 구조로 연결할 수 있게 되었습니다.
142|하지만 아직 한 가지 문제가 남아 있습니다.
148|어떤 값을 선택하고, 어떤 연산을 수행하며, 결과를 어디에 저장할지는 누가 결정하는 걸까요?
153|다음에는 명령어가 실제 회로의 동작을 어떻게 제어하는지 살펴보겠습니다.'''
SCENES=[(0,11,'hook','저장한 값을 다시 계산하려면?','기억과 클럭에서 저장값의 재사용 문제를 도출한다.'),(11,24,'onebit','하나의 저장 회로는 1비트','단일 플립플롭과4비트 ALU값의 폭을 구분한다.'),(24,31,'bits','숫자 5를 네 비트로','고정4비트 예시0101의 각 자리는 따로 저장해야 한다.'),(31,45,'register','네 개의 저장 요소를 하나로','각자의 비트를 공통 클럭 기준으로 갱신하는4비트레지스터다.'),(45,60,'stored','저장된 결과를 다음 입력으로','1000을 저장한 레지스터의 출력을 ALU에 공급한다.'),(60,77,'sequence','5+3의 결과를 다시 사용한다','5+3=8을 기록한 뒤8+2=10의 입력으로 재사용한다.'),(77,91,'mux','여러 값 중 하나를 선택','두 후보는고정배선된MUX의별도입력이며Select만바뀐다.'),(91,102,'reuse','같은 ALU, 다른 데이터','먼저5를선택해8저장후8을선택해10계산한다.'),(102,112,'many','여러 값에는 여러 레지스터','5·3·8을동시에보관할별도레지스터가필요하다.'),(112,118,'readwrite','어디서 읽고, 어디에 쓸까?','읽기는기존값을유지하고쓰기만선택한목적지를갱신한다.'),(118,127,'datapath','선택 · 연산 · 다시 저장','A/B두읽기선택과결과쓰기경로로연결된데이터경로다.'),(127,139,'roles','계산·저장·연결의 역할','같은구조에서ALU·레지스터·MUX와배선의역할을구분한다.'),(139,148,'control','누가 이 동작을 결정할까?','읽기선택·연산종류·쓰기목적지와허용은별도제어다.'),(148,153,'instruction','회로의 동작을 정하는 신호','명령어와제어신호의관계를열린질문으로남긴다.')]
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def phonetic(s):
 for a,b in [('ALU','에이 엘 유'),('MUX','먹스'),('Datapath','데이터패스')]:s=s.replace(a,b)
 return s
def main():
 rows=[];start=0
 for line in SCRIPT.splitlines():
  e,s=line.split('|',1);e=int(e);rows.append(dict(start=start,end=e,text=s));start=e
 assert len(rows)==31 and start==153
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
 manifest=[];narr=['# GPU 개론 08 — 저장된 값은 어떻게 다시 계산에 사용될까?','','확정31문장·사용자종료시각153초. 음원미제공.','']
 for i,(a,b,slug,title,claim) in enumerate(SCENES,1):
  directory=f'scenes/{i:02}_{slug}';p=R/directory;p.mkdir(parents=True,exist_ok=True)
  selected=[r for r in rows if a<=r['start']<b];script='\n\n'.join(r['text'] for r in selected)
  (p/'script.txt').write_text(phonetic(script)+'\n',encoding='utf-8')
  (p/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import DatapathScene\nclass Scene{i:02}(DatapathScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=directory,**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title,method=slug))
  table='| 전체 초 | 대본·화면 변화 기준 |\n| --- | --- |\n'+'\n'.join(f'| {r["start"]}–{r["end"]} | {r["text"]} |' for r in selected)
  (p/'spec.md').write_text(f'''# {i:02} · {title}

## 목적·주장
{claim}

## 앞 장면·시작
{SCENES[i-2][4] if i>1 else '1비트 저장과클럭의기능블록에서시작한다.'}

## 확정 원문·길이
{a}–{b}초, {b-a}초. 사용자문장종료시각을유지하고추정하지않는다.

{script}

## 화면·타임라인
{table}

상세콘티: ../../storyboard_reference.md. 구현: ../../scene_engine.py의 {slug}. 중앙구조를유지하며필요한요소를추가하고값·선택·쓰기시점만변경한다. 가로1920×1080/세로1080×1920,30fps. 원문자막Text하나를문장경계에서교체한다.

## 종료·연결
{claim} {'명령어와제어의관계를남기며끝낸다.' if i==14 else '다음은 '+SCENES[i][3]+'로연결한다.'}

## 기술조건·과장방지
고정4비트예시:2=0010,3=0011,5=0101,8=1000,10=1010. 단일DFF는1비트. 네DFF는각자D를공통클럭기준으로샘플하고지연후Q를갱신한다. 5에항상4비트가최소필요하다는주장은하지않고본예시의고정폭임을표시한다. 읽기로원래값이사라지지않는다. 쓰기는목적지와WriteEnable이정해지고클럭에지에서만반영한다. MUX의두후보는별도입력핀에고정연결되며Select에따라출력값과강조색만변한다. 5선택에서5+3=8을저장한후8선택으로8+2=10을계산한다. 레지스터출력을선택한상태에서쓰기허용을불필요하게계속유지하지않는다. 전체도식은A/B두읽기선택경로와별도쓰기선택·CLK를표시한다. 배선교차는접합이아니며명시된분기점만접합이다. 제어정보와데이터버스를구분한다. 사용자도입과마지막문장은유지하되추가GPU09예고제목은넣지않는다.

검증: ../../check_datapath.py. 참고CornellDatapath자료는README링크.
''',encoding='utf-8')
  narr.extend([f'## {a}–{b}초 · {title}','']+[f'{r["start"]}–{r["end"]}초: {r["text"]}\n' for r in selected])
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('id: gpui08_register_datapath\nduration_seconds: 153\naudio: null\nfps: 30\nlayouts: {longform: [1920, 1080], shorts: [1080, 1920]}\nscenes:\n'+'\n'.join(f'  - {{id: "{m["id"]}", directory: {m["directory"]}, class: {m["class"]}, start_seconds: {m["start"]}, duration_seconds: {m["duration_seconds"]}}}' for m in manifest)+'\n',encoding='utf-8')
 for name in ['master_script.md','narration.md']:(R/name).write_text('\n'.join(narr),encoding='utf-8')
 (R/'tts_script.txt').write_text('\n\n'.join(phonetic(r['text']) for r in rows)+'\n',encoding='utf-8')
 old=R.parent/'gpui07_clock_timing'
 for name in ['build.py','inspect_frames.py','inspect_caption_boundaries.py','verify_exports.py']:
  s=(old/name).read_text(encoding='utf-8').replace('gpui07_clock_135s','gpui08_datapath_153s').replace('gpui07_clock_timing','gpui08_register_datapath').replace('gpui07_{suffix}','gpui08_{suffix}').replace('==135','==153').replace('-135','-153').replace('duration_seconds=135','duration_seconds=153').replace('==4050','==4590')
  if name=='inspect_frames.py':
   a=s.index('TIMES=');b=s.index('\n',a);s=s[:a]+'TIMES=[3,8,13,17,21,26,29,33,37,40,43,48,51,56,63,67,71,75,79,84,88,92,95,99,104,109,114,117,121,125,130,133,136,138,141,145,150,152]'+s[b:]
  (R/name).write_text(s,encoding='utf-8')
 print('Prepared31 sentences /14 scenes /153 seconds')
if __name__=='__main__':main()
