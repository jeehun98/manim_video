import json,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
SCRIPT='''4|앞서 우리는 트랜지스터를 연결해 논리 연산을 구현하는 방법을 살펴봤습니다.
9|그렇다면 이러한 논리 회로만으로 실제 숫자의 덧셈도 구현할 수 있을까요?
11|먼저 두 개의 비트를 더해 보겠습니다.
15|0과 0은 0, 0과 1은 1, 1과 0도 1입니다.
18|그런데 1과 1을 더하면 결과는 2가 됩니다.
21|하나의 비트로는 표현할 수 없는 값입니다.
26|그래서 결과를 현재 자리에 남는 값과 다음 자리로 넘어가는 올림수로 나누어 보겠습니다.
31|1과 1을 더하면 현재 자리에는 0, 다음 자리로는 1이 넘어갑니다.
34|이제 이 두 출력을 논리 연산으로 표현해 보겠습니다.
38|현재 자리의 합은 두 입력이 서로 다를 때만 1이 됩니다.
41|이는 XOR 연산과 일치합니다.
46|반면 올림수는 두 입력이 모두 1일 때만 발생하므로 AND 연산과 일치합니다.
52|따라서 XOR와 AND 게이트를 연결하면 두 비트의 합과 올림수를 동시에 만들어낼 수 있습니다.
54|이것이 반가산기입니다.
59|하지만 여러 자리의 숫자를 더하려면 이전 자리에서 발생한 올림수까지 고려해야 합니다.
62|예를 들어 이진수 11과 01을 더해 보겠습니다.
67|오른쪽 자리에서 1과 1을 더하면 합은 0, 올림수는 1입니다.
71|왼쪽 자리에서는 원래의 두 비트에 이 올림수까지 더해야 합니다.
74|즉, 세 개의 입력을 처리하는 회로가 필요합니다.
75|이것이 전가산기입니다.
82|전가산기는 두 비트와 이전 자리의 올림수를 받아, 새로운 합과 다음 자리의 올림수를 출력합니다.
85|이러한 전가산기들을 연결하면 더 큰 이진수도 더할 수 있습니다.
87|이를 리플 캐리 가산기라고 합니다.
89|그런데 여기에는 문제가 있습니다.
95|각 자리의 두 입력은 동시에 주어지지만, 상위 자리의 최종 결과는 이전 자리의 올림수에 의존합니다.
100|따라서 올림수가 여러 자리를 통과해야 한다면, 그만큼 신호 전달을 기다려야 합니다.
105|숫자의 자릿수가 늘어날수록 최악의 경우 지연도 길어지는 것입니다.
108|그렇다면 이 기다림을 줄일 방법은 없을까요?
112|각 자리에서 올림수가 발생하거나 전달되는 조건을 미리 계산하면 어떨까요?
120|이 조건들을 조합하면 올림수가 한 자리씩 전달되기를 기다리지 않고, 여러 자리의 올림수를 더 빠르게 결정할 수 있습니다.
123|이것이 캐리 룩어헤드의 기본적인 아이디어입니다.
127|물론 이를 위해서는 추가적인 논리 회로와 배선이 필요할 수 있습니다.
133|결국 같은 덧셈이라도 회로의 설계에 따라 속도와 면적, 에너지 소비가 달라집니다.
138|우리는 이제 논리 게이트만으로 실제 산술 연산을 구현할 수 있다는 사실을 확인했습니다.
143|그렇다면 덧셈뿐 아니라 뺄셈과 비교까지 하나의 장치에서 수행하려면 어떻게 해야 할까요?'''
SCENES=[(0,11,'question','논리에서 숫자 계산으로','두 비트를 입력으로 덧셈을 질문한다.'),(11,21,'onebit','1 + 1은 한 비트에 담기지 않는다','두 비트의 합은 최대 2이며 두 출력 비트가 필요하다.'),(21,31,'split','현재 자리와 올림수','1+1=10₂에서 CARRY와 SUM을 구분한다.'),(31,41,'xor','현재 자리의 합은 XOR','합의 진리표는 XOR와 일치한다.'),(41,46,'and','올림수는 AND','두 입력이 모두 1일 때만 올림수가 생긴다.'),(46,54,'half','두 출력을 만드는 반가산기','같은 입력 A와 B가 XOR와 AND에 동시에 공급된다.'),(54,62,'columns','이전 자리의 올림수가 있다면?','11₂+01₂에서는 이전 자리 올림수가 다음 자리 입력이다.'),(62,71,'carry','올림수도 다음 자리의 입력','오른쪽 합0·올림수1이 왼쪽1+0의 세 번째 입력이다.'),(71,82,'full','세 입력을 처리하는 전가산기','두 반가산기와 OR로 세 입력의 합과 올림수를 만든다.'),(82,87,'ripple','전가산기들을 연결하면','네 전가산기의 올림수 출력과 입력을 연결한다.'),(87,105,'delay','결과는 올림수를 기다린다','입력이 동시에 도착해도 올림수 의존 경로에는 지연이 있다.'),(105,112,'gp','발생과 전달 조건을 먼저 계산','G=A AND B, P=A XOR B는 각 자리 입력만으로 계산된다.'),(112,120,'lookahead','올림수를 더 일찍 결정하는 구조','전개한 올림수 논리식은 이전 자리 출력을 순차로 기다리지 않는다.'),(120,133,'tradeoff','같은 덧셈, 다른 회로','룩어헤드는 추가 논리·배선과 함께 면적·지연·에너지를 검토한다.'),(133,143,'alu','논리 게이트에서 산술 장치로','논리 회로의 조합이 덧셈을 구현하며 여러 연산 장치를 질문한다.')]
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
 rows=[];start=0
 for line in SCRIPT.splitlines():
  e,s=line.split('|',1);e=int(e);rows.append(dict(start=start,end=e,text=s));start=e
 assert len(rows)==35 and start==143
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
 manifest=[];narr=['# GPU 개론 04 — 논리 게이트는 어떻게 숫자를 더할까?','', '확정 원문 35문장, 사용자 종료 시각 143초. 음원 미제공.','']
 for i,(a,b,slug,title,claim) in enumerate(SCENES,1):
  d=f'scenes/{i:02}_{slug}';p=R/d;p.mkdir(parents=True,exist_ok=True)
  selected=[r for r in rows if a<=r['start']<b];script='\n\n'.join(r['text'] for r in selected)
  (p/'script.txt').write_text(script+'\n',encoding='utf-8')
  (p/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import AdderScene\nclass Scene{i:02}(AdderScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=d,**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title,method=slug))
  cues='\n'.join(f'- {r["start"]}–{r["end"]}초: {r["text"]}' for r in selected)
  (p/'spec.md').write_text(f'# {i:02} {title}\n\n목적·주장: {claim}\n\n## 확정 대본·길이\n{a}–{b}초, {b-a}초. 사용자 문장 종료 시각 기준.\n\n{script}\n\n## 화면·타임라인\n{cues}\n\nscene_engine.py의 {slug} 메서드. 원본 콘티는 ../../storyboard_reference.md. 시작은 앞 씬의 결과이며 종료는 위 주장으로 완결한다. 가로는 넓은 비교, 세로는 중앙 세로 배치. 하단 전체 문장 자막은 하나씩 즉시 교체한다.\n\n## 계산·표현 조건\nLSB는 오른쪽. 합은 초록, 올림수는 주황. 반가산기 S=A XOR B,C=A AND B. 전가산기는 두 HA와 OR의 독립 입력. 11₂+01₂=100₂, 1111₂+0001₂=10000₂. 리플은 모든 A/B가 먼저 제공된 후 carry의 의존성을 보여준다. CLA는 G/P, 논리항, OR 결합 단계가 필요하며 즉시 출력하지 않는다. 속도는 정성 모형으로 실측 배율을 주장하지 않는다. 면적·에너지가 항상 증가한다는 단정은 하지 않는다. 검증은 check_arithmetic.py.\n',encoding='utf-8')
  narr.extend([f'## {a}–{b}초 · {title}','',cues,''])
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('id: gpui04_binary_adder\nduration_seconds: 143\naudio: null\nlayouts: {longform: [1920, 1080], shorts: [1080, 1920]}\nscenes:\n'+'\n'.join(f'  - {{id: "{m["id"]}", directory: {m["directory"]}, class: {m["class"]}, start_seconds: {m["start"]}, duration_seconds: {m["duration_seconds"]}}}' for m in manifest)+'\n',encoding='utf-8')
 for name in ['master_script.md','narration.md']:(R/name).write_text('\n'.join(narr),encoding='utf-8')
 tts=SCRIPT
 for a,b in [('XOR','엑스오어'),('AND','앤드')]:tts=tts.replace(a,b)
 (R/'tts_script.txt').write_text('\n\n'.join(s.split('|',1)[1] for s in tts.splitlines())+'\n',encoding='utf-8')
 old=R.parent/'gpui03_logic_connections'
 for name in ['build.py','inspect_frames.py','inspect_caption_boundaries.py']:
  s=(old/name).read_text(encoding='utf-8').replace('gpui03_logic_164s','gpui04_adder_143s').replace('gpui03_logic_connections','gpui04_binary_adder').replace('gpui03_{suffix}','gpui04_{suffix}').replace('==164','==143').replace('-164','-143').replace('duration_seconds=164','duration_seconds=143')
  if name=='inspect_frames.py':
   a=s.index('TIMES=');b=s.index('\n',a);s=s[:a]+'TIMES=[2,7,13,19,24,29,36,40,44,49,53,57,61,65,69,73,78,81,84,91,97,103,109,114,117,119,122,126,131,136,141]'+s[b:]
  (R/name).write_text(s,encoding='utf-8')
 print('Prepared 35 sentences / 15 scenes / 143 seconds')
if __name__=='__main__':main()
