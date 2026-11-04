import json
from pathlib import Path
R=Path(__file__).resolve().parent
SCRIPT='''6|앞서 우리는 여러 연산 기능을 하나의 ALU에 통합하고, 필요한 연산을 선택하는 방법을 살펴봤습니다.
11|그렇다면 이 장치로 여러 단계의 계산을 수행하려면 어떻게 해야 할까요?
16|예를 들어 5와 3을 더하고, 그 결과에 다시 2를 더한다고 생각해 보겠습니다.
20|가장 간단한 방법은 두 개의 덧셈 회로를 연속으로 연결하는 것입니다.
26|첫 번째 회로에서 나온 8이 두 번째 회로로 전달되면 최종 결과인 10을 얻을 수 있습니다.
31|하지만 계산 단계마다 새로운 회로를 추가해야 한다면, 회로의 규모도 계속 커지게 됩니다.
36|그렇다면 이미 만들어 놓은 하나의 ALU를 반복해서 사용할 수는 없을까요?
42|이를 위해서는 첫 번째 계산의 결과인 8을 다음 계산에 사용할 때까지 보관해야 합니다.
46|그런데 지금까지 살펴본 논리 회로에는 이러한 기능이 없습니다.
52|논리 게이트의 출력은 현재 입력에 따라 결정되기 때문에, 입력이 바뀌면 이전 결과도 달라집니다.
56|그렇다면 기존의 논리 게이트만으로 값을 기억하는 회로를 만들 수 있을까요?
59|여기서 회로의 연결 방식을 조금 바꿔보겠습니다.
63|지금까지는 입력에서 출력으로 신호가 전달되도록 회로를 구성했습니다.
68|하지만 출력된 신호를 다시 다른 게이트의 입력으로 연결하면 어떨까요?
71|이러한 구조를 되먹임, 즉 Feedback이라고 합니다.
75|대표적인 예로 두 개의 NOR 게이트를 생각해 보겠습니다.
79|각 게이트의 출력이 상대방 게이트의 입력에 영향을 주도록 연결하는 것입니다.
84|이때 한쪽 출력이 1이고 다른 쪽 출력이 0인 상태가 만들어졌다고 생각해 보겠습니다.
90|외부 입력을 모두 0으로 유지하면, 두 게이트는 서로의 출력을 통해 이 상태를 계속 유지할 수 있습니다.
95|반대로 한쪽 출력을 0, 다른 쪽 출력을 1로 만든 상태 역시 유지할 수 있습니다.
102|즉, 같은 외부 입력이 주어져도 이전에 어떤 상태였는지에 따라 서로 다른 출력이 유지될 수 있는 것입니다.
106|이렇게 두 가지 안정된 상태를 이용하면 0과 1을 기억할 수 있습니다.
112|그리고 외부 입력을 통해 저장된 상태를 1로 설정하거나, 0으로 초기화할 수도 있습니다.
114|이것이 SR 래치의 기본적인 원리입니다.
122|중요한 것은 새로운 종류의 계산 소자가 필요한 것이 아니라, 이미 알고 있던 논리 게이트를 서로 연결해 기억이라는 기능을 만들었다는 점입니다.
125|하지만 아직 해결하지 못한 문제가 있습니다.
130|기억한 값을 새로운 값으로 바꾸려면, 그 변화는 언제 일어나야 할까요?
135|여러 계산 회로가 서로 연결되어 있다면, 각 회로의 상태를 아무 때나 바꿔도 괜찮을까요?
140|다음에는 저장된 값을 갱신하는 시점을 어떻게 제어하는지 살펴보겠습니다.'''
SCENES=[(0,11,'alu','여러 단계의 계산을 하려면?','ALU의 결과를 다음 계산의 입력으로 사용한다.'),(11,31,'chain','중간 결과는 다음 계산의 입력','두 가산기를 연결하면 (5+3)+2=10이지만 단계별 복제 비용이 있다.'),(31,42,'reuse','하나의 ALU를 반복해서 쓰려면','중간 결과를 다음 계산까지 보관해야 한다.'),(42,56,'combinational','입력이 바뀌면 이전 결과는?','조합논리 회로의 현재 출력만으로 과거 값을 보존하지 못한다.'),(56,71,'feedback','출력이 다시 입력으로 돌아간다면','되먹임은 출력을 다시 입력에 연결한 구조이며 모든 되먹임이 기억은 아니다.'),(71,79,'nor','두 NOR 게이트를 교차 연결','위 Q=NOT(R OR Qbar), 아래 Qbar=NOT(S OR Q)로 연결한다.'),(79,90,'sethold','입력을 내려도 상태가 유지된다','S의 펄스로 Q1을 만든 뒤 S=R=0에서도 유지한다.'),(90,95,'reset','반대 상태 역시 유지된다','R의 펄스로 Q0을 만든 뒤 입력을 내려도 유지한다.'),(95,102,'twostates','같은 입력, 다른 상태','S=R=0에서 Q1과 Q0 모두 안정된 상태다.'),(102,106,'bit','두 안정 상태로 1비트 저장','전원 공급 조건에서 하나의 이진 상태를 기억한다.'),(106,114,'controls','Set · Hold · Reset','S는 설정, R은 초기화, 둘 다0이면 이전 상태를 유지한다.'),(114,122,'samegates','같은 게이트, 새로운 연결 구조','게이트의 되먹임 연결이 기억이라는 기능을 만든다.'),(122,130,'when','새 값을 언제 기록할까?','상태를 유지하는 것과 갱신 시점을 정하는 것은 다른 문제다.'),(130,140,'timing','여러 회로의 갱신 시점','연결된 회로에서 저장 상태의 갱신 시점도 설계해야 한다.')]
CUES=[[(0,6,'A/B·ALU·선택·결과'),(6,11,'다음 계산으로 이어지는 결과 버스')],[(11,16,'(5+3)+2 수식'),(16,20,'ADDER1→ADDER2, n-bit 버스'),(20,23,'첫 출력8'),(23,26,'8+2→10'),(26,31,'단계별 복제 설계의 소자·배선 증가')],[(31,36,'단일 ALU 설계 대안'),(36,39,'5+3→8, 중간 결과 상자'),(39,42,'저장8과2를 ALU에 다시 공급')],[(42,46,'ALU 현재 출력8'),(46,49,'입력5,3→출력8'),(49,52,'입력8,2→출력10, 이전8 없음'),(52,56,'논리 게이트로 기억할 수 있을까?')],[(56,59,'세 개 논리 블록 단방향'),(59,63,'전압 변화의 전파 경로 강조'),(63,68,'출력에서 별도 입력 핀으로 되먹임선 연결'),(68,71,'Feedback 명명, 안정 상태 여부는 별도 문제')],[(71,75,'NOR 두 개, 00→1'),(75,79,'출력을 상대편 입력에 연결, 교차점은 비접합')],[(79,80,'R0S0Q0에서 시작'),(80,81,'S1 입력'),(81,82,'아래 Qbar0 먼저'),(82,84,'위 Q1 후 안정'),(84,90,'S0 복귀, Q1Qbar0 유지')],[(90,91,'R1 입력'),(91,92,'위 Q0 먼저'),(92,93,'아래 Qbar1 후 안정'),(93,95,'R0 복귀, Q0 유지')],[(95,102,'동일 회로 두 개: R0S0, Q1과Q0 비교')],[(102,106,'단일 래치Q1, 전원 공급 조건과1비트')],[(106,108,'S 펄스·설정 후Hold'),(108,110,'R 펄스·초기화 후Hold'),(110,112,'상태표00/10/01,11사용안함'),(112,114,'SR Latch 이름·외곽 기능 단위')],[(114,118,'NOR 두 개와 되먹임 경로 강조'),(118,122,'같은 소자·새 연결 구조→저장 기능')],[(122,125,'언제 바뀌어야 할까?'),(125,130,'추상 데이터 파형과 갱신 시점?, SR의S/R과구분')],[(130,135,'저장A→계산→저장B→계산→저장C, 상태 변화 전달'),(135,140,'공통 시간 기준 물음표, 사용자 마지막 문장 유지·추가 예고 제목 없음')]]
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def phonetic(s):
 for a,b in [('ALU','에이 엘 유'),('Feedback','피드백'),('NOR','노어'),('SR','에스 알')]:s=s.replace(a,b)
 return s
def main():
 rows=[];start=0
 for line in SCRIPT.splitlines():
  e,s=line.split('|',1);e=int(e);rows.append(dict(start=start,end=e,text=s));start=e
 assert len(rows)==29 and start==140
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
 manifest=[];narr=['# GPU 개론 06 — 논리 게이트는 어떻게 값을 기억할까?','','확정 원문29문장·종료 시각140초. 음원 미제공.','']
 for i,(a,b,slug,title,claim) in enumerate(SCENES,1):
  directory=f'scenes/{i:02}_{slug}';p=R/directory;p.mkdir(parents=True,exist_ok=True)
  selected=[r for r in rows if a<=r['start']<b];script='\n\n'.join(r['text'] for r in selected)
  (p/'script.txt').write_text(phonetic(script)+'\n',encoding='utf-8')
  (p/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import MemoryScene\nclass Scene{i:02}(MemoryScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=directory,**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title,method=slug))
  table='| 전체 초 | 화면 |\n| --- | --- |\n'+'\n'.join(f'| {x}–{y} | {s} |' for x,y,s in CUES[i-1])
  (p/'spec.md').write_text(f'''# {i:02} · {title}

## 목적·주장
{claim}

## 시작·앞 장면
{SCENES[i-2][4] if i>1 else 'ALU의 공통 계산 구조에서 출발한다.'}

## 확정 대본·길이
사용자 종료 시각 {a}–{b}초, {b-a}초. 실제 제공 시각을 유지하며 길이를 추정하지 않는다.

{script}

## 화면·타임라인
{table}

가로1920×1080·세로1080×1920,30fps. 하단 전체 자막 Text 하나를 문장 경계에서 교체한다. 원본은 ../../storyboard_reference.md. 구현은 ../../scene_engine.py의 {slug}.

## 종료·연결
{claim} {'갱신 시점을 묻는 문제로 끝낸다.' if i==14 else '다음 씬은 '+SCENES[i][3]+'를 보여준다.'}

## 정확성·조건
ALU 재사용의 데이터 버스와 래치 내부 되먹임선을 혼동하지 않는다. 조합논리의 한계를 설명한다. 일반 되먹임만으로 기억을 보장하지 않는다. 위 NOR는 R·Qbar, 아래 NOR는 S·Q를 입력받는다. 교차선에는 접합점을 넣지 않고 브리지로 구분한다. S 설정은 Qbar0→Q1, R 초기화는 Q0→Qbar1 순서. 전파 중에는 지연 모형임을 표시하며 안정 상태에서 두 NOR 식을 모두 검증한다. S=R=1은 실제 시연하지 않고 사용안함으로만 표기한다. 초기 상태는 전원투입 자동 초기화가 아니라 가정된 상태이다. 전원 공급·정상 동작 조건의 휘발성 저장이다. 시간 개념도에 D입력이나 실제 클럭 제어가 이미 구현된 것으로 그리지 않는다. 사용자 도입·마지막 문장은 유지하되 GPU07 추가 예고는 넣지 않는다.

검증: ../../check_latch.py. 근거: Cornell Stateful Logic (README 링크).
''',encoding='utf-8')
  narr.extend([f'## {a}–{b}초 · {title}','']+[f'{r["start"]}–{r["end"]}초: {r["text"]}\n' for r in selected])
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('id: gpui06_sr_latch\nduration_seconds: 140\naudio: null\nfps: 30\nlayouts: {longform: [1920, 1080], shorts: [1080, 1920]}\nscenes:\n'+'\n'.join(f'  - {{id: "{m["id"]}", directory: {m["directory"]}, class: {m["class"]}, start_seconds: {m["start"]}, duration_seconds: {m["duration_seconds"]}}}' for m in manifest)+'\n',encoding='utf-8')
 for name in ['master_script.md','narration.md']:(R/name).write_text('\n'.join(narr),encoding='utf-8')
 (R/'tts_script.txt').write_text('\n\n'.join(phonetic(r['text']) for r in rows)+'\n',encoding='utf-8')
 old=R.parent/'gpui05_alu_reuse'
 for name in ['build.py','inspect_frames.py','inspect_caption_boundaries.py','verify_exports.py']:
  s=(old/name).read_text(encoding='utf-8').replace('gpui05_alu_175s','gpui06_memory_140s').replace('gpui05_alu_reuse','gpui06_sr_latch').replace('gpui05_{suffix}','gpui06_{suffix}').replace('==175','==140').replace('-175','-140').replace('duration_seconds=175','duration_seconds=140').replace('==35','==29').replace('==16','==14').replace('==5250','==4200')
  if name=='inspect_frames.py':
   a=s.index('TIMES=');b=s.index('\n',a);s=s[:a]+'TIMES=[3,8,13,18,22,25,29,34,38,41,45,49,51,54,58,62,66,70,73,78,80,81,83,86,89,91,92,94,98,101,104,107,109,111,113,117,121,124,128,133,138]'+s[b:]
  (R/name).write_text(s,encoding='utf-8')
 print('Prepared 29 sentences / 14 scenes / 140 seconds')
if __name__=='__main__':main()
