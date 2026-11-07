import json
from pathlib import Path
R=Path(__file__).resolve().parent
TITLE='GPU 개론 11 — 레지스터에 없는 데이터는 어떻게 계산할까?'
SCRIPT='''6|앞서 우리는 명령어를 순서대로 가져오고, 해독하고, 실행하는 기본적인 프로세서 구조를 만들었습니다.
10|이제 레지스터에 저장된 숫자를 이용해 여러 계산을 수행할 수 있습니다.
15|그런데 지금까지는 계산할 숫자가 이미 레지스터에 저장되어 있다고 가정했습니다.
19|만약 계산해야 할 숫자가 수백 개, 수천 개라면 어떨까요?
23|레지스터의 개수와 저장할 수 있는 데이터의 양은 제한되어 있습니다.
30|그렇다면 모든 숫자를 레지스터에 보관하는 대신, 별도의 저장 공간에 두고 필요한 값만 가져오면 어떨까요?
34|예를 들어 여러 숫자가 저장된 공간을 생각해 보겠습니다.
38|첫 번째 위치에는 5가, 두 번째 위치에는 3이 저장되어 있습니다.
43|여기서 특정한 숫자를 가져오려면, 어느 위치에 있는 값인지 지정할 수 있어야 합니다.
47|이처럼 저장 공간의 각 위치를 구분하는 값을 주소라고 합니다.
51|주소를 전달하면 해당 위치에 저장된 데이터를 선택해 읽어 올 수 있습니다.
57|이렇게 주소를 이용해 데이터를 보관하고 읽고 쓸 수 있는 저장 공간을 데이터 메모리라고 합니다.
61|그런데 메모리에서 숫자를 읽어 왔다고 해서 바로 계산이 끝나는 것은 아닙니다.
66|지금까지 우리가 만든 ALU는 레지스터에서 전달된 값을 이용해 계산했습니다.
71|따라서 메모리에서 읽은 값도 레지스터에 저장할 수 있도록 새로운 연결이 필요합니다.
75|기존에는 ALU의 계산 결과가 레지스터로 돌아갔습니다.
80|여기에 메모리에서 읽은 데이터가 돌아오는 경로를 하나 더 추가하면 어떨까요?
84|그리고 두 경로 중 하나를 선택해 레지스터에 기록하도록 만드는 것입니다.
88|여기서 앞서 살펴본 MUX를 다시 사용할 수 있습니다.
93|이제 레지스터에는 ALU의 결과뿐 아니라 메모리에서 가져온 값도 저장할 수 있게 되었습니다.
99|하지만 실제로 어떤 주소의 데이터를 읽고, 어느 레지스터에 기록할지는 여전히 결정해야 합니다.
103|앞서 우리는 이러한 동작을 명령어로 표현하는 방법을 만들었습니다.
109|그렇다면 메모리의 특정 위치에서 값을 읽어 레지스터에 저장하라는 명령도 만들 수 있겠지요.
111|이것이 Load 명령어의 기본적인 역할입니다.
116|예를 들어 주소 100에 저장된 숫자 5를 첫 번째 레지스터로 가져올 수 있습니다.
122|반대로 계산한 결과를 레지스터에만 보관하지 않고, 메모리에 다시 기록하고 싶을 수도 있습니다.
126|이번에는 레지스터의 값을 메모리로 전달하고, 기록할 주소를 지정하면 됩니다.
132|이처럼 레지스터의 값을 메모리의 지정된 위치에 기록하는 동작을 Store라고 합니다.
137|이제 우리는 메모리에 저장된 5와 3을 각각 레지스터로 가져올 수 있습니다.
140|ALU로 두 값을 더하면 결과인 8이 만들어집니다.
143|그리고 이 결과를 다시 메모리에 기록할 수도 있습니다.
148|기존에는 계산할 숫자가 레지스터에 미리 저장되어 있어야 했습니다.
153|하지만 이제는 별도의 메모리에서 데이터를 가져오고, 계산한 뒤 다시 저장할 수 있게 된 것입니다.
156|그런데 여기서 새로운 문제가 생깁니다.
161|ALU의 계산과 달리, 메모리에서 데이터를 읽어 오는 데에는 시간이 걸릴 수 있습니다.
168|그동안 프로세서는 어떤 명령어를 수행하고 있었는지, 읽어 온 결과를 어디에 저장해야 하는지 기억해야 합니다.
174|다음에는 하나의 명령어가 여러 단계에 걸쳐 실행될 때, 그 과정의 정보를 어떻게 유지하는지 살펴보겠습니다.'''
SCENES=[(0,15,'hook','계산할 숫자는 어디에 있을까?','기존 프로세서는 계산할 피연산자가 레지스터에 준비되어 있다고 가정했다.'),(15,30,'capacity','모든 데이터를 레지스터에 담을 수 없다','빠른 내부 저장 장소의 용량 한계 때문에 별도 저장 공간이 필요하다.'),(30,43,'locations','필요한 값의 위치를 고르려면?','첫 두 예시 위치100/101의 데이터5/3과 위치 선택을 구별한다.'),(43,57,'address','주소로 고르는 데이터 메모리','주소입력100/101에 대응하는 데이터5/3을 비파괴적으로 읽는다.'),(57,71,'connection','읽어 온 값을 계산에 사용하려면?','기존 레지스터→ALU 경로에 메모리 결과를 레지스터로 전달할 경로가 필요하다.'),(71,80,'candidates','레지스터로 돌아오는 두 결과','ALU8과 메모리5의 별도 후보 배선을 추가하되 직접 단락하지 않는다.'),(80,93,'writeback','쓰기 입력에 MUX를 추가한다','데이터 출처 선택과 목적지·RegWE·저장에지는 별도다.'),(93,109,'controls','새 데이터 이동도 명령어로 지정한다','메모리주소·읽기동작·결과출처·목적지 제어를 한 동작으로 지정한다.'),(109,116,'load','Load : Memory → Register','주소100의5를 읽어R1에 기록해도 메모리100의5는 유지된다.'),(116,132,'store','Store : Register → Memory','R3의8을 주소102에 MemWE가 유효할 때 기록하고 레지스터는 바꾸지 않는다.'),(132,143,'program','읽기 → 더하기 → 다시 저장','LOAD R1[100]→LOAD R2[101]→ADD R3,R1,R2→STORE R3[102] 순서로 실행한다.'),(143,153,'expanded','계산할 수 있는 데이터의 범위가 넓어진다','기존 프로세서의 계산 경로를 유지하며 외부 데이터의 왕복 경로를 완성한다.'),(153,168,'latency','데이터를 기다리는 동안 무엇을 기억할까?','응답이 준비되지 않은 동안 RegWE=0, 주소·목적지·수행 동작을 유지해야 한다.'),(168,174,'state','명령 실행 중 유지해야 할 정보','주소100·목적지R1·LOAD진행상태를 묶어 유지할 필요를 질문으로 남긴다.')]
def phonetic(s):
 for a,b in [('ALU','에이 엘 유'),('MUX','먹스'),('Load','로드'),('Store','스토어')]:s=s.replace(a,b)
 return s

def main():
 rows=[];start=0
 for line in SCRIPT.splitlines():
  e,s=line.split('|',1);e=int(e);rows.append(dict(start=start,end=e,text=s));start=e
 assert len(rows)==37 and start==174
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
 manifest=[];narr=['# '+TITLE,'','확정37문장·174초. 음원미제공. 사용자 제공 종료 시각을 그대로 반영한다.','']
 for i,(a,b,slug,title,claim) in enumerate(SCENES,1):
  directory=f'scenes/{i:02}_{slug}';p=R/directory;p.mkdir(parents=True,exist_ok=True);rs=[r for r in rows if a<=r['start']<b];script='\n\n'.join(r['text'] for r in rs)
  (p/'script.txt').write_text(phonetic(script)+'\n',encoding='utf-8')
  (p/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import MemoryScene\nclass Scene{i:02}(MemoryScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=directory,**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title,method=slug))
  table='\n'.join(f'- {r["start"]}–{r["end"]}초: {r["text"]}' for r in rs)
  (p/'spec.md').write_text(f'''# {i:02} · {title}

目的: {claim}

시작: {SCENES[i-2][3] if i>1 else 'PC·명령어메모리·해독·레지스터·ALU 기본 구조'}

확정 길이: {a}–{b}초({b-a}초). 사용자 제공 발화시간을 변경하지 않는다.

## 원문 및 주요 화면 변화 시각
{table}

## 화면·연결
상세 콘티 ../../storyboard_reference.md, 구현 ../../scene_engine.py의{slug}. 기존 회로를 유지하고 중반에는 확대된 데이터 경로와 쓰기 MUX를 중심에 둔다. 가로1920×1080/세로1080×1920 별도배치·30fps. 주소·제어주황,레지스터초록,ALU파랑,데이터메모리보라. 주소100과데이터5는색·역할이구분된다. 도식과단일자막전용영역을분리한다. 종료: {claim}

## 기술 조건
LOAD R1,[100]·LOAD R2,[101]·ADD R3,R1,R2·STORE R3,[102]는교육용사람표기다. 기존8비트인코딩을부여하지않는다. 주소경로는100/101/102를표현할폭을가정하며데이터예시와별개다. 이편에서는주소계산회로를추가설명하지않고주소지정을추상화한다. 읽기는메모리를변경하지않는다. 주소만바꿔도쓰기되지않는다. Load는응답유효·목적지·RegWE·갱신에지가갖춰졌을때레지스터를갱신한다. Store는레지스터에서WD입력으로전달하며MemWE와유효갱신시점에서주소102만바꾼다.RegWE=0으로일반레지스터쓰기없음. ALU와메모리출력은MUX의서로다른입력이다. MUX선택은즉시저장이나목적지선택과다르다. 두LOAD는동시에수행하지않는다. ADD피연산자5/3은결과R3과달라피드백오해가없다. 지연은특정사이클수·나노초로단정하지않고Ready=0중에는미완성데이터를기록하지않는다. PC·명령어메모리와DataMemory는역할구분용이며반드시물리적으로분리된다는뜻이아니다. 사용자원문도입·마지막문장은유지하되추가GPU12예고제목·엔드카드는넣지않는다.

검증: ../../check_memory.py,자막영역및전환검사,최종ffprobe. 출처README참조.
'''.replace('目的','목적'),encoding='utf-8')
  narr.extend([f'## {a}–{b}초 · {title}','',table,''])
 for f in ['master_script.md','narration.md']:(R/f).write_text('\n'.join(narr),encoding='utf-8')
 (R/'tts_script.txt').write_text('\n\n'.join(phonetic(r['text']) for r in rows)+'\n',encoding='utf-8')
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('id: gpui11_data_memory\nduration_seconds: 174\naudio: null\nfps: 30\nlayouts: {longform: [1920, 1080], shorts: [1080, 1920]}\nscenes:\n'+'\n'.join(f'  - {{id: "{m["id"]}", directory: {m["directory"]}, class: {m["class"]}, start_seconds: {m["start"]}, duration_seconds: {m["duration_seconds"]}}}' for m in manifest)+'\n',encoding='utf-8')
 old=R.parent/'gpui10_program_execution'
 for f in ['build.py','inspect_frames.py','inspect_caption_boundaries.py','verify_exports.py']:
  s=(old/f).read_text(encoding='utf-8').replace('gpui10_program_165s','gpui11_memory_174s').replace('gpui10_program_execution','gpui11_data_memory').replace('gpui10_{suffix}','gpui11_{suffix}').replace('==165','==174').replace('-165','-174').replace('165*fps','174*fps').replace('duration_seconds=165','duration_seconds=174').replace('==4950','==5220').replace('==35','==37').replace('==15 and sum','==14 and sum')
  if f=='inspect_frames.py':
   a=s.index('TIMES=');b=s.index('\n',a);s=s[:a]+'TIMES=[3,8,12,17,21,26,32,36,41,45,49,54,59,64,69,73,78,82,86,90,96,101,106,110,114,119,124,129,134,136,138,142,146,151,155,159,164,167,170,173]'+s[b:]
  (R/f).write_text(s,encoding='utf-8')
 if not (R/'scene_engine.py').exists():
  s=(old/'scene_engine.py').read_text(encoding='utf-8').split('COLORS=')[0].replace('from check_instruction import decode,alu,execute','from check_memory import Machine,writeback,reg_write,mem_write').replace('class ProgramScene','class MemoryScene').replace(' /  10',' /  11').replace('/165','/174').replace(' / 15',' / 14')
  # Avoid excessive scaling when a dynamic label changes to punctuation or a short word.
  a=s.index('def setlabel(');b=s.index('\nclass MemoryScene',a)
  s=s[:a]+'''def setlabel(m,s,color=INK,size=27,width=None):
 key=(s,str(color))
 if getattr(m,'_labelkey',None)==key:return m
 pos=m.get_center();oldh=m.height;oldw=m.width;new=txt(s,size,color)
 new.scale_to_fit_height(oldh)
 limit=width if width else max(oldw*1.5,.6)
 if new.width>limit:new.scale_to_fit_width(limit)
 m.become(new.move_to(pos));m._labelkey=key;return m

'''+s[b:]
  (R/'scene_engine.py').write_text(s,encoding='utf-8')
 print('Prepared37sentences /14scenes /174seconds')
if __name__=='__main__':main()
