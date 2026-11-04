"""Initialize episode 02 from the template and supplied, not estimated, timing."""
import json,shutil
from pathlib import Path
W=Path(__file__).resolve().parents[1];P=W/'longforms/minimal02_genome';P.mkdir(exist_ok=True)
shutil.copytree(W/'longforms/_template',P,dirs_exist_ok=True)
rows=[
(4,'생명체에서 유전자를 하나씩 제거한다면, 어디까지 줄여도 살아 있을 수 있을까요?'),
(8,'우리 몸의 세포는 수많은 유전자의 작용으로 유지됩니다.'),
(12,'그런데 생명체가 살아가는 데 이 모든 유전자가 반드시 필요한 것은 아닙니다.'),
(21,'2016년, 미국의 제이 크레이그 벤터 연구소는 단 473개의 유전자를 가진 세포, JCVI-syn3.0을 발표했습니다.'),
(28,'연구진은 기존 세균의 유전체를 바탕으로 유전자를 제거하고 재설계한 뒤, 합성 유전체를 세포에 도입했습니다.'),
(34,'그 결과, 영양분이 충분히 공급되는 특정 환경에서 성장하고 분열할 수 있는 세포를 만들었습니다.'),
(39,'그렇다면 473개가 생명에 필요한 최소 유전자 수일까요?'),
(43,'이 질문에 답하려면 먼저 어떤 유전자가 반드시 필요한지 알아내야 합니다.'),
(47,'가장 간단한 방법은 유전자를 하나씩 제거해 보는 것입니다.'),
(51,'유전자 A를 제거했는데 세포가 살아 있다면, A는 필요 없는 유전자일까요?'),
(54,'이번에는 유전자 B를 제거해 보겠습니다.'),
(56,'세포가 여전히 살아 있습니다.'),
(59,'그렇다면 A와 B를 모두 제거해도 괜찮을까요?'),
(61,'반드시 그렇지는 않습니다.'),
(67,'두 유전자가 서로의 기능을 보완하고 있었다면, 하나가 사라져도 다른 하나가 그 역할을 대신할 수 있습니다.'),
(71,'하지만 둘을 동시에 제거하면 세포가 생존하지 못할 수 있습니다.'),
(79,'이처럼 각각의 변화는 치명적이지 않지만, 두 변화가 결합하면 생존할 수 없게 되는 현상을 합성 치사, Synthetic Lethality라고 합니다.'),
(84,'즉, 유전자가 필요한지는 그 유전자 하나만으로 결정되지 않습니다.'),
(87,'다른 유전자들과 어떤 관계를 맺고 있는지도 중요합니다.'),
(89,'여기서 또 하나의 조건이 있습니다.'),
(91,'바로 세포가 살아가는 환경입니다.'),
(97,'세포가 필요한 영양분을 외부에서 공급받는다면, 그 물질을 직접 합성하는 유전자는 없어도 될 수 있습니다.'),
(102,'반대로 영양분이 부족한 환경에서는 같은 유전자가 생존에 필수적일 수 있습니다.'),
(107,'그리고 단순히 살아남는 것과 안정적으로 성장하고 분열하는 것도 서로 다른 조건입니다.'),
(117,'실제로 JCVI-syn3.0은 세포 분열 형태가 불규칙한 문제가 있었고, 연구진은 이후 일부 유전자를 다시 추가해 분열 특성을 개선했습니다.'),
(119,'더 놀라운 사실도 있습니다.'),
(128,'최초 발표 당시, JCVI-syn3.0에 남겨진 473개 유전자 중 149개는 구체적인 기능이 알려져 있지 않았습니다.'),
(134,'어떤 유전자가 필요하다는 사실을 확인하더라도, 그것이 정확히 어떤 역할을 하는지는 모를 수 있다는 뜻입니다.'),
(138,'그렇다면 이 세포는 정말 가능한 가장 작은 생명체일까요?'),
(145,'473개의 유전자로 살아가는 세포를 만들었다는 사실은, 그보다 적은 유전자로는 생존할 수 없다는 증명이 아닙니다.'),
(151,'더 작은 조합이 존재할 수도 있고, 환경이나 요구하는 기능이 달라지면 필요한 유전자도 달라질 수 있습니다.'),
(157,'결국 생명에 필요한 최소 유전체를 찾는다는 것은 단순히 유전자를 하나씩 제거하는 일이 아닙니다.'),
(164,'유전자 사이의 관계와 생존 조건을 함께 고려하면서, 생명을 유지하는 데 반드시 필요한 조합을 찾아내는 일입니다.'),
]
bounds=[0,12,21,28,34,43,47,56,67,79,87,102,117,128,134,145,151,164]
titles=['어디까지 줄여도 살아 있을까?','473개 유전자의 세포','설계한 유전체를 세포에','특정 환경에서 성장·분열','473개가 최소일까?','하나씩 제거해 보면','각각 지워도 생존한다','서로 보완하는 두 경로','함께 지우면 달라진다','개별 유전자보다 관계','환경이 필수성을 바꾼다','생존과 분열은 다른 조건','기능을 몰랐던 149개','필요성과 역할은 다르다','작은 세포와 최소성의 증명','필요한 조합은 조건에 따라','생명을 유지하는 조합']
claims=[
'블록은 실제 물리적 배치가 아닌 유전체 구성 개념도. 수십 개만 대표 표시하며 인체 유전체를 473개로 줄였다는 뜻이 아님.',
'2016년 JCVI-syn3.0, 유전자 473개. 특정 세균 기반의 실험적 축소 유전체이며 보편적 하한이 아님.',
'기존 세균 유전체의 설계·합성과 수용 세포로의 도입을 구분. 세포 전체를 무에서 만든 것이 아님.',
'영양이 충분한 지정 배양 조건에서 성장과 분열 가능. 불규칙한 분열 형태는 뒤에서 별도 설명.',
'473개로 가능한 구성 발견과 절대 최소의 증명은 다름.',
'원본에서 하나 제거 후 생존을 확인하는 개념 실험.',
'같은 원본에서 출발한 독립 A 제거·B 제거 조건을 비교. 동일 세포에 순차 제거하지 않음.',
'A 또는 B가 생존에 필요한 기능을 보완하는 가상 모델. 합성 치사의 보편 메커니즘은 아님.',
'개념 모델 A∨B에서 양쪽 제거 시 기능 상실. 원본·A 제거·B 제거·동시 제거 4조건 비교.',
'필수성은 남아 있는 다른 유전자와의 관계에 의존할 수 있음. 실제 조절망 재현이 아님.',
'동일한 합성 경로 결손도 외부 물질 공급에 따라 생존 결과가 달라질 수 있음. 대체 경로가 없는 개념 조건.',
'JCVI-syn3.0의 불규칙한 형태와 이후 JCVI-syn3A의 분열 특성 개선. 2021년 연구를 근거로 하며 완전 정상/비정상의 이분법을 피함.',
'실제 블록 473개 중 정확히 149개 강조. 31.5%는 반올림. 2016년 최초 발표 당시 기능 지식 상태.',
'유전자 필요성의 실험적 확인과 분자적 역할 이해를 구분.',
'473개로 생존 가능한 세포를 만들었다는 결과는 472개 이하 불가능의 증명이 아님.',
'더 작은 조합은 가능성으로만 표시. 환경과 요구 기능에 따라 탐색 조건이 달라짐.',
'유전자 관계·환경·요구 기능을 함께 고려하는 결론. 다른 영상 복습·다음 편 예고 없음.',
]
events=[
'0–4초 세포와 30개 대표 블록 등장; 4–8초 일부 선택; 8–12초 제거 후 생존 윤곽 유지.',
'12초 2016년·기관 표시; 16초 JCVI-syn3.0; 18초 473 genes 강조.',
'21–25초 기존 유전체→재설계→합성; 25–28초 합성 유전체가 수용 세포로 이동.',
'28초 풍부한 배지 표시; 29–34초 세포 성장과 불균등한 두 세포로 분열.',
'34–39초 473=최소? 질문; 39–43초 필요성을 확인하는 실험으로 초점 전환.',
'43–47초 원본 복제본에서 A만 제거하고 관찰.',
'47–51초 A 제거 복제본은 생존; 51–54초 다른 원본 복제본에서 B 제거; 54–56초 생존 결과.',
'56–61초 동시 제거 질문; 61–64초 A 제거 시 B 경로 강조; 64–67초 별도 B 제거 상태에서 A 경로 강조.',
'67–71초 A+B 제거와 기능 경로 상실; 71–79초 합성 치사 명칭과 네 조건 진리표.',
'79–84초 A/B 의존 관계 네트워크; 84–87초 연결된 기능 경로 강조.',
'87–91초 같은 결손 세포와 두 환경; 91–97초 외부 공급→필요 물질 확보; 97–102초 공급 제한→필요 물질 결핍.',
'102–107초 생존/안정적인 분열 조건 분리; 107–112초 불규칙 분열 개념도; 112–117초 일부 유전자 보강 후 형태 비교.',
'117–119초 473개 블록; 119–128초 149개 강조와 최초 발표 당시 표기.',
'128–134초 필요성 확인과 기능 이해의 차이.',
'134–138초 생존 가능한 구성; 138–145초 더 작은 구성 불가능을 증명했는지 질문.',
'145–151초 미지 후보와 환경·조합·요구 기능.',
'151–157초 관계·환경·기능 세 요소 등장; 157–164초 생명 유지에 필요한 조합으로 연결.',
]
timing=[];start=0
for end,s in rows:timing.append(dict(start=start,end=end,text=s));start=end
(P/'narration_timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(timing))+'\n',encoding='utf-8')
manifest=[];narr=[];tts=[]
for i,(a,b,title,claim,event) in enumerate(zip(bounds,bounds[1:],titles,claims,events),1):
 d=P/f'scenes/{i:02}';d.mkdir(parents=True,exist_ok=True)
 body=' '.join(r['text'] for r in timing if a<=r['start']<b)
 (d/'script.txt').write_text(body+'\n',encoding='utf-8')
 (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import GenomeScene\nclass Scene{i:02}(GenomeScene):\n    index={i-1}\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02} · {title}\n\n## 목적·핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n절대 시각 {a}초의 설명을 이어받으며 독립 교체 가능.\n\n## TTS 원문·확정 길이\n{body}\n\n구간 {a}–{b}초, {b-a}초. 사용자 문장 종료 시각 기준. 음원 없음.\n\n## 화면·애니메이션\n{event}\n\n세로/가로 별도 배치. scene_engine.py part_{i-1:02}에서 구현.\n\n## 화면 텍스트\n{title}. 개념 모델/실제 연구 구분, 유전자 블록은 추상화.\n\n## 시작·종료 상태와 연결\n해당 주장의 대상을 관찰한 뒤 결과 상태로 종료. 다음 씬은 사용자 발화 시각에 시작하며 예고 문구 없음.\n\n## 정확성 확인\n{claim}\n',encoding='utf-8')
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title))
 narr.append(f'## {a}–{b}초 · {title}\n\n{body}');tts.append(body)
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
script='# 모든 것이 필요할까? 02 — 최소 유전체\n\n사용자 확정 대본·총 164초.\n\n'+'\n\n'.join(narr)+'\n'
for f in ['master_script.md','narration.md']:(P/f).write_text(script,encoding='utf-8')
spoken='\n\n'.join(tts).replace('2016년','이천십육 년').replace('473개','사백칠십삼 개').replace('149개','백사십구 개').replace('JCVI-syn3.0','제이 씨 브이 아이 신 쓰리 포인트 제로').replace('Synthetic Lethality','신세틱 리샐리티').replace('A와 B','에이와 비').replace('A를','에이를').replace('B를','비를').replace('A는','에이는').replace('유전자 A','유전자 에이').replace('유전자 B','유전자 비')
(P/'tts_script.txt').write_text(spoken+'\n',encoding='utf-8')
(P/'scenes.yaml').write_text('id: minimal02_genome\ntitle: 모든 것이 필요할까? 02 — 최소 유전체\nvideo:\n  fps: 30\n  variants:\n    shorts: [1080, 1920]\n    longform: [1920, 1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
(P/'brief.md').write_text('# 제작 기준\n\n사용자 확정 대본 33문장, 164초. 세로 1080×1920 및 가로 1920×1080, 30fps, 무음·전체 발화 자막.\n\nA/B 제거는 가상 기능 보완 모델이며 실제 유전자명 아님. 독립 원본에서 A만/B만/둘 다 제거를 비교. 환경에 따른 필수성과 분열 특성 개선은 별도 조건. 473과149는 2016년 발표 수치이며 절대 최소 또는 현재 기능 미해명 개수라는 주장 없음.\n\n자막은 Manim에서 렌더하지 않고 concat 뒤 단일 ASS 트랙으로 합성. 문장 경계 프레임을 기준 영상과 비교한다.\n',encoding='utf-8')
example=P/'scenes/01_example'
if example.exists():
 assert example.resolve().is_relative_to(P.resolve());shutil.rmtree(example)
for name in ['build.py','caption_pass.py','inspect_frames.py','verify_caption_boundaries.py']:
 text=(W/'longforms/minimal01_preserve'/name).read_text(encoding='utf-8').replace('minimal01','minimal02').replace('154','164').replace('4620','4920')
 if name=='verify_caption_boundaries.py':
  text=text.replace('_final_caption_fixed.mp4','_final.mp4').replace('4619','4919')
 (P/name).write_text(text,encoding='utf-8')
shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\de5d636c-818f-4397-9d3c-9cc3362d2e8f\붙여넣은 텍스트.txt'),P/'storyboard_user.md')
print(P,len(timing),sum(m['duration_seconds'] for m in manifest))
