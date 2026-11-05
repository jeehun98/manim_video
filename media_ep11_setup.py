from pathlib import Path
import json,re
root=Path.cwd();ep=root/'quantum_series/episodes/ep11_uncertainty';ep.mkdir(exist_ok=True)
raw=Path('C:/Users/as042/.codex/attachments/78ce94bd-38e5-443b-ba4e-b6767c4c20f2/붙여넣은 텍스트.txt').read_text(encoding='utf-8-sig');texts=re.findall(r'나레이션\s+"([^"]+)"',raw);assert len(texts)==42,len(texts)
ends=[7,9,15,19,22,26,31,35,38,42,46,50,52,57,60,65,69,73,78,82,86,89,94,97,101,106,110,116,120,126,131,136,141,145,149,151,155,159,166,170,174,177]
headings=['1927 · 하이젠베르크의 질문','불확정성 원리','파동처럼 회절 · 한 점에서 검출','위치와 운동량을 동시에 정확히?','하나의 파장을 가진 진행파','어디까지 가도 반복되는 파동','파장이 정해지면 운동량도 정해진다','넓게 퍼진 위치 분포','파동을 한곳에 모으려면?','서로 다른 파수의 성분들','중앙에서는 보강 · 바깥에서는 상쇄','국소화된 파동묶음','한 상태의 두 가지 표현','폭을 좁히면 더 많은 파수 성분이 필요하다','운동량과 파수 · pₓ = ℏk','위치가 좁아지면 운동량이 넓어진다','운동량을 좁히면 위치가 넓어진다','두 분포의 폭이 서로 제약된다','Δx Δpₓ ≥ ℏ / 2','두 폭을 동시에 임의로 줄일 수 없다','역사적 설명 · 측정 과정','감마선 현미경 사고실험','짧은 파장과 광학적 분해능','광자도 운동량을 가진다','산란으로 전달되는 운동량','관측 과정에서의 운동량 교란','이 설명만으로 충분할까?','측정 장비를 제거해도','준비된 상태 자체의 제약','동일한 상태의 위치와 운동량 분포','행렬역학과의 연결','위치와 운동량 연산의 비가환성','파동의 중첩과 푸리에 변환','다른 표현 · 같은 불확정성 관계','미래는 전혀 예측할 수 없을까?','예측은 여전히 가능하다','파동함수의 시간 변화는 계산한다','개별 측정은 확률로 예측한다','양자상태의 변화와 측정 확률','간섭하는 상태 · 국소적인 검출','경로 정보와 간섭을 동시에?','1927 · 보어의 상보성 원리']
sections=[('question',0,19,0,4,'파동성을 가진 전자의 위치와 운동량을 묻는다'),('plane',19,38,4,9,'단일 운동량 진행파는 국소화되지 않는다'),('superposition',38,52,9,13,'서로 다른 파수의 중첩으로 파동묶음이 형성된다'),('tradeoff',52,82,13,20,'동일 가우스 상태의 위치·운동량 폭이 역으로 변한다'),('microscope',82,106,20,26,'감마선 현미경은 측정 교란을 설명하는 사고실험이다'),('intrinsic',106,126,26,30,'측정 장비가 없어도 상태의 불확정성은 남는다'),('equivalence',126,145,30,34,'비가환성과 푸리에 구조는 같은 관계를 준다'),('prediction',145,166,34,39,'상태의 시간 변화와 개별 측정 확률을 구분한다'),('complementarity',166,177,39,42,'국소 검출과 간섭을 경로 정보의 질문으로 연결한다')]
data={'id':'quantum11','title':'하이젠베르크의 불확정성 원리','duration':177,'audio':None,'narrator_note':'연우 (사용자 표기; 음원 미제공)','timing_source':'사용자 제공 확정 문장 종료 시각','sentences':[{'start':ends[i-1] if i else 0,'end':e,'text':texts[i],'heading':headings[i]} for i,e in enumerate(ends)],'scenes':[{'id':sid,'class':sid.title()+'Chapter','start':start,'end':end,'claim':claim} for sid,start,end,a,b,claim in sections]}
(ep/'script.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');(ep/'storyboard.md').write_text(raw,encoding='utf-8')
(ep/'narration.md').write_text('# EP.11 확정 대본 · 177초\n\n'+'\n\n'.join(f'{s["start"]}–{s["end"]}초\n{s["text"]}' for s in data['sentences']),encoding='utf-8')
tts='\n\n'.join(' '.join(texts[a:b]) for _,_,_,a,b,_ in sections);tts=tts.replace('1927년','천구백이십칠 년');(ep/'tts_script.txt').write_text(tts+'\n',encoding='utf-8')
(ep/'brief.md').write_text('''# EP.11 제작 기준

177초 · 42문장 · 사용자 제공 대본과 종료 시각 유지. 연우는 화자 메모이며 읽을 대본에 포함하지 않는다. 음원 미제공이므로 무음·전체 문장 자막.

핵심은 동일 가우스 상태의 위치와 운동량 분포를 하나의 σx로 연동하는 것이다. ħ=1인 무차원 단위, σp=1/(2σx). 모든 분포는 정규화하고 고정 축을 사용한다. Δ는 표준편차로 설명한다. 파동함수 실수부와 확률밀도를 구분하며, 단일 진행파의 화면 끝은 물리적 경계가 아니다. 유한 행렬로 정준교환관계를 정확히 구현했다고 주장하지 않는다.

감마선 현미경은 역사적 사고실험으로, 광학적 분해능과 산란 운동량 전달을 표시한다. 장치를 제거한 뒤에도 두 분포의 폭 관계를 유지한다. 마지막 경로 정보 아이콘은 실제 측정이 켜진 검출기로 묘사하지 않고 질문 대상으로 표시한다. 확정 대본의 직접 연결 문장은 임의 수정하지 않는다.

9개 독립 씬. shorts/longform은 애니메이션 공유·별도 layout. standalone/join의 본문과 길이는 같다. 176–177초 정지 프레임.
''',encoding='utf-8')
for sid,start,end,a,b,claim in sections:
 d=ep/'scenes'/sid;d.mkdir(parents=True,exist_ok=True)
 (d/'spec.md').write_text(f'# {sid}\n\n{start}–{end}초 · 문장 {a+1}–{b}.\n\n주장: {claim}.\n\n사용자 확정 대본·시각 유지. 위치 그래프는 청록, 운동량은 금색, ψ 실수부는 파랑. 그래프·범례·자막을 분리하고 두 화면비 독립 검수.\n',encoding='utf-8')
 (d/'scene.py').write_text(f"import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[5]))\nfrom quantum_series.episodes.ep11_uncertainty.direction import {sid.title()}Direction\nclass {sid.title()}Chapter({sid.title()}Direction):pass\n",encoding='utf-8')
s=(root/'quantum_series/episodes/ep10_davisson_germer/build.py').read_text(encoding='utf-8').replace('171','177').replace('5130','5310').replace('quantum10','quantum11');s=re.sub(r"assert \[s\['end'\] for s in sentences\]==\[[^\n]+",f"assert [s['end'] for s in sentences]=={ends}",s);(ep/'build.py').write_text(s,encoding='utf-8')
base=(root/'quantum_series/episodes/ep10_davisson_germer/direction.py').read_text(encoding='utf-8');base=base[base.index('def wrap'):base.index(' def centers')].replace('데이비슨–거머','하이젠베르크')
(ep/'direction.py').write_text('''import json
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,configure,INK,MUTED,GOLD
from quantum_series.episodes.ep11_uncertainty.layouts import UncertaintyLayout
from quantum_series.shared.uncertainty import *
D=json.loads(Path(__file__).with_name('script.json').read_text(encoding='utf-8'));L=UncertaintyLayout(configure().portrait)
'''+base,encoding='utf-8')
print('Created EP.11 scripts and nine specifications')
