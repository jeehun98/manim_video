"""Approved narration and exact user supplied endpoints, before screen production."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
SCRIPT='''5|앞서 우리는 논리 게이트를 연결해 이전 값을 기억하는 회로를 만들었습니다.
7|그렇다면 계산 결과를 언제 저장해야 할까요?
12|예를 들어 ALU에 5와 3을 입력해 덧셈을 수행한다고 생각해 보겠습니다.
15|우리는 결과가 8이라는 사실을 알고 있습니다.
20|하지만 실제 회로에서는 입력이 들어오는 순간 결과가 완성되는 것이 아닙니다.
24|전기 신호가 논리 게이트를 통과하는 데는 시간이 필요하기 때문입니다.
29|앞서 살펴본 덧셈 회로에서도 올림수가 다음 자리로 전달되는 데 시간이 걸렸습니다.
33|또한 서로 다른 경로를 거치는 신호는 도착하는 시간이 다를 수 있습니다.
38|따라서 입력이 바뀐 직후에는 출력이 아직 안정되지 않았을 수도 있습니다.
42|그런데 ALU의 출력에 저장 회로를 연결했다고 생각해 보겠습니다.
45|계산이 끝나기도 전에 값을 저장한다면 어떻게 될까요?
50|우리가 원했던 8이 아니라, 아직 완성되지 않은 중간 상태를 기억할 수도 있습니다.
56|그렇다면 계산 결과가 안정될 시간을 확보하고, 정해진 순간에만 값을 저장하도록 만들면 어떨까요?
59|여기서 새로운 저장 방식이 등장합니다.
65|입력 신호를 계속 따라가는 대신, 특정한 신호 변화 순간의 값을 받아들이고 유지하는 것입니다.
67|이러한 저장 회로를 플립플롭이라고 합니다.
73|대표적인 D 플립플롭은 클럭 신호가 0에서 1로 바뀌는 순간 입력값을 저장합니다.
77|그리고 다음 저장 시점이 올 때까지 이전 값을 유지합니다.
79|그렇다면 클럭은 무엇일까요?
82|클럭은 일정한 주기로 0과 1을 반복하는 전기 신호입니다.
88|이 신호의 특정 변화 순간을 저장 시점으로 사용하면, 회로가 값을 갱신하는 시점을 정할 수 있습니다.
92|그렇다면 클럭이 빠를수록 컴퓨터도 무조건 빨라질까요?
93|그렇지는 않습니다.
98|다음 클럭이 너무 일찍 도착하면 계산 결과가 충분히 안정되지 않았을 수 있기 때문입니다.
105|따라서 클럭 주기는 회로에서 신호가 전달되고 계산이 완료되는 데 필요한 시간을 고려해 결정해야 합니다.
110|여기서 중요한 것은 클럭이 직접 계산을 수행하는 것이 아니라는 점입니다.
116|계산은 여전히 논리 게이트에서 이루어지고, 클럭은 저장된 값을 언제 갱신할지 정하는 기준을 제공합니다.
122|이제 이러한 저장 회로가 여러 개 있다면, 동일한 클럭을 이용해 상태 갱신 시점을 조정할 수도 있습니다.
125|이것이 동기식 회로의 기본적인 아이디어입니다.
130|우리는 이제 계산 결과를 기억하고, 정해진 시점에 새로운 값으로 갱신할 수 있게 되었습니다.
135|그렇다면 여러 저장 회로에 보관된 값들 중 어떤 것을 다음 계산에 사용해야 할까요?'''
SCENES=[(0,7,'memory','기억한 값을 언제 갱신할까?','SR 래치의 상태 유지와 저장 시점이라는 문제를 연결한다.'),(7,20,'delay','수학의 결과와 회로의 시간','5+3=8은 맞지만 물리적 출력은 입력 직후 완성되지 않는다.'),(20,29,'propagation','논리 게이트를 지나는 시간','각 단계의 전파 지연과 올림수 의존 경로가 있다.'),(29,38,'settling','서로 다른 도착 시점','빠른·느린 경로와 출력의 과도 상태를 구분한다.'),(38,56,'sampling','너무 일찍 저장하면?','안정 전의0을 저장하면 출력이8로 안정되어도 저장값은0일 수 있다.'),(56,67,'dff','변화하는 입력, 유지되는 출력','특정 시점의 D를 받아들이고 Q를 유지하는 저장 방식을 소개한다.'),(67,77,'edge','상승 에지에서 받아들인다','D 플립플롭은 상승 에지에서 샘플하고 짧은 지연 후 Q를 갱신한다.'),(77,88,'clock','공통된 갱신 기준, 클럭','주기적인0·1전압 신호의 특정 에지를 갱신 기준으로 사용한다.'),(88,98,'fast','클럭이 너무 빨라진다면','계산 완료 이전 샘플링은 올바른 기록을 보장하지 않는다.'),(98,105,'period','계산과 저장에 필요한 시간 확보','주기는 전파 시간과 저장 요소의 안정 시간 조건을 고려한다.'),(105,116,'roles','계산과 저장의 역할은 다르다','ALU는 계산하고 클럭은 저장 회로의 갱신 기준이다.'),(116,125,'sync','여러 저장 회로, 하나의 기준','공통 클럭에서 각 요소가 자신의 D를 기록한다.'),(125,130,'register','계산 결과를 비트별로 저장','8=1000은 네 개의1비트 플립플롭으로 저장한다.'),(130,135,'choose','다음 계산에 어떤 값을 쓸까?','여러 저장 데이터 중 연산 입력을 고르는 문제를 묻는다.')]
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def phonetic(s):return s.replace('ALU','에이 엘 유').replace('D 플립플롭','디 플립플롭')
def main():
 rows=[];start=0
 for line in SCRIPT.splitlines():
  e,s=line.split('|',1);e=int(e);rows.append(dict(start=start,end=e,text=s));start=e
 assert len(rows)==31 and start==135
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
 manifest=[];narr=['# GPU 개론 07 — 회로는 언제 값을 갱신할까?','','사용자 확정31문장·종료 시각135초. 음원 미제공.','']
 for i,(a,b,slug,title,claim) in enumerate(SCENES,1):
  directory=f'scenes/{i:02}_{slug}';p=R/directory;p.mkdir(parents=True,exist_ok=True)
  selected=[r for r in rows if a<=r['start']<b];script='\n\n'.join(r['text'] for r in selected)
  (p/'script.txt').write_text(phonetic(script)+'\n',encoding='utf-8')
  (p/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import ClockScene\nclass Scene{i:02}(ClockScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=directory,**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title,method=slug))
  table='| 전체 초 | 대본·화면 전환 기준 |\n| --- | --- |\n'+'\n'.join(f'| {r["start"]}–{r["end"]} | {r["text"]} |' for r in selected)
  (p/'spec.md').write_text(f'''# {i:02} · {title}

## 목적·주장
{claim}

## 앞 장면·시작
{SCENES[i-2][4] if i>1 else '두 NOR의 SR 래치에서 저장 기능 블록으로 추상화한다.'}

## 확정 원문·길이
{a}–{b}초, {b-a}초. 사용자 문장 종료 시각을 유지한다.

{script}

## 화면·타임라인
{table}

상세 동작은 ../../storyboard_reference.md의 같은 시각을 따른다. 구현은 ../../scene_engine.py의 {slug}. 중앙 회로·타이밍 도식을 유지하며 시간에 따라 값·색·샘플 시점만 바꾼다. 가로1920×1080/세로1080×1920,30fps. 원문 자막 하나를 하단 경계에서 교체한다.

## 종료·연결
{claim} {'다음 계산의 입력 선택 문제로 종료한다.' if i==14 else '다음 씬은 '+SCENES[i][3]+'를 설명한다.'}

## 기술적 조건·과장 방지
ALU 데이터는4비트, 단일 D 플립플롭은1비트.8=1000 저장은4비트 뱅크로 표시한다. 선택한 예시의 상승 에지 동작이지 모든 플립플롭의 극성이 같은 것은 아니다. Q는 에지보다 먼저 변하지 않으며 clock-to-Q 지연을 분리한다. D가 에지 전후로 안정된 정상 예시만 확정값으로 기록한다. 너무 이른 샘플의?는 보장되지 않는 값이며 무조건0이나 확정적 메타안정으로 단정하지 않는다. 초기0→최종8 변화는 가상 버스값 예시다. 주기 제약은 clock-to-Q·조합 경로·setup 및 불확실성과 관련되고 hold 조건도 별도 존재한다. 본편은 수식 없이 안정 여유를 표현한다. 공통 클럭은 각자 다른 데이터를 기록하며 Q가 완전히 같은 물리 순간에 변한다고 주장하지 않는다. 클럭 배선은 DFF의 CLK핀에만 연결하고 ALU에 연결하지 않는다. SR 래치가 D를 항상 추종한다는 비교는 하지 않는다. 원문 도입과 마지막 질문은 유지하며 추가 예고 제목은 넣지 않는다.

검증: ../../check_timing.py. Cornell Timing Analysis / Stateful Logic 자료는 README 링크.
''',encoding='utf-8')
  narr.extend([f'## {a}–{b}초 · {title}','']+[f'{r["start"]}–{r["end"]}초: {r["text"]}\n' for r in selected])
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('id: gpui07_clock_timing\nduration_seconds: 135\naudio: null\nfps: 30\nlayouts: {longform: [1920, 1080], shorts: [1080, 1920]}\nscenes:\n'+'\n'.join(f'  - {{id: "{m["id"]}", directory: {m["directory"]}, class: {m["class"]}, start_seconds: {m["start"]}, duration_seconds: {m["duration_seconds"]}}}' for m in manifest)+'\n',encoding='utf-8')
 for name in ['master_script.md','narration.md']:(R/name).write_text('\n'.join(narr),encoding='utf-8')
 (R/'tts_script.txt').write_text('\n\n'.join(phonetic(r['text']) for r in rows)+'\n',encoding='utf-8')
 old=R.parent/'gpui06_sr_latch'
 for name in ['build.py','inspect_frames.py','inspect_caption_boundaries.py','verify_exports.py']:
  s=(old/name).read_text(encoding='utf-8').replace('gpui06_memory_140s','gpui07_clock_135s').replace('gpui06_sr_latch','gpui07_clock_timing').replace('gpui06_{suffix}','gpui07_{suffix}').replace('==140','==135').replace('-140','-135').replace('duration_seconds=140','duration_seconds=135').replace('==29','==31').replace('==4200','==4050')
  if name=='inspect_frames.py':
   a=s.index('TIMES=');b=s.index('\n',a);s=s[:a]+'TIMES=[3,6,10,14,18,22,27,31,35,37,40,44,48,53,57,61,64,66,68,70,72,74,76,78,81,85,90,94,97,101,104,108,112,115,119,123,127,129,132,134]'+s[b:]
  (R/name).write_text(s,encoding='utf-8')
 print('Prepared 31 sentences / 14 scenes / 135 seconds')
if __name__=='__main__':main()
