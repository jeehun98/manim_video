"""Scaffold episode 04 from the approved narration and supplied sentence times."""
import json,shutil
from pathlib import Path
W=Path(__file__).resolve().parents[1];P=W/'longforms/minimal04_sufficiency';P.mkdir(exist_ok=True)
shutil.copytree(W/'longforms/_template',P,dirs_exist_ok=True)
rows=[
(3,'데이터가 백만 개 있다면, 그 백만 개를 모두 기억해야 할까요?'),
(7,'어떤 공장에서 생산하는 부품의 길이를 측정한다고 생각해 보겠습니다.'),
(13,'우리가 알고 싶은 것은 개별 부품의 길이가 아니라, 이 공장에서 생산되는 부품의 평균 길이입니다.'),
(19,'측정값이 서로 독립이고, 같은 정규분포를 따르며, 분산은 이미 알려져 있다고 가정하겠습니다.'),
(25,'이 조건에서는 표본평균 하나만으로도 모집단 평균을 추론하는 데 필요한 정보를 모두 보존할 수 있습니다.'),
(33,'이처럼 데이터 전체가 가진 특정 모수에 대한 정보를 빠짐없이 담고 있는 통계량을 충분통계량, Sufficient Statistic이라고 합니다.'),
(38,'그런데 어떻게 백만 개의 숫자를 하나로 줄여도 정보가 사라지지 않을까요?'),
(41,'정규분포에서 모집단 평균을 뮤라고 하겠습니다.'),
(46,'각 측정값은 뮤에서 얼마나 떨어져 있는지에 따라 확률밀도가 달라집니다.'),
(51,'모든 관측값의 확률밀도를 곱하면, 주어진 뮤에 대한 데이터의 우도 함수를 얻습니다.'),
(56,'여기에는 각 측정값과 뮤의 차이를 제곱해 더한 항이 등장합니다.'),
(63,'이 제곱합을 전개하면, 측정값의 제곱합, 뮤와 측정값의 합을 곱한 항, 그리고 뮤의 제곱에 비례하는 항으로 나뉩니다.'),
(69,'여기서 뮤와 데이터가 함께 등장하는 부분에는 개별 측정값이 아니라 측정값의 합만 남습니다.'),
(73,'나머지 데이터 의존 항은 뮤에 따라 변하지 않습니다.'),
(79,'따라서 표본 개수가 정해져 있다면, 표본평균만으로도 뮤에 대한 상대적인 우도의 모양을 결정할 수 있습니다.'),
(81,'두 개의 데이터를 비교해 보겠습니다.'),
(82,'첫 번째는 1, 2, 3, 4, 5입니다.'),
(85,'두 번째는 0, 0, 3, 6, 6입니다.'),
(88,'두 데이터는 서로 다르지만 표본평균은 모두 3입니다.'),
(95,'앞서 가정한 통계 모형에서는 두 데이터가 모집단 평균 뮤에 대해 제공하는 우도 정보가 같습니다.'),
(100,'원본 데이터는 복원할 수 없어도, 평균을 추론하는 데 필요한 정보는 남아 있는 것입니다.'),
(103,'그렇다면 표본평균 하나면 언제나 충분할까요?'),
(104,'그렇지는 않습니다.'),
(107,'이번에는 모집단의 분산도 모른다고 생각해 보겠습니다.'),
(110,'두 데이터는 평균이 같지만 퍼져 있는 정도는 다릅니다.'),
(117,'따라서 정규분포에서 평균과 분산을 함께 추론하려면 측정값의 합과 제곱합이 필요합니다.'),
(122,'즉, 어떤 정보를 남겨야 하는지는 추론하려는 대상과 통계 모형에 따라 달라집니다.'),
(127,'여기서 최소충분통계량, Minimal Sufficient Statistic이라는 개념이 등장합니다.'),
(131,'원본 데이터 전체도 충분통계량이지만, 더 간단한 표현이 존재할 수 있습니다.'),
(138,'최소충분통계량은 다른 충분통계량으로부터 얻을 수 있으면서, 모수에 관한 정보를 불필요하게 구분하지 않는 표현입니다.'),
(144,'다만 최소라는 말이 반드시 저장 용량이나 계산량이 가장 작다는 뜻은 아닙니다.'),
(147,'결국 중요한 것은 데이터를 얼마나 많이 남겼느냐가 아닙니다.'),
(153,'우리가 알고 싶은 대상에 관한 정보를 잃지 않으면서, 어디까지 데이터를 줄일 수 있느냐는 것입니다.'),
]
bounds=[0,7,19,33,38,51,63,73,79,88,100,110,122,138,144,153]
titles=['백만 개를 모두 기억해야 할까?','알고 싶은 것은 모집단 평균','데이터에서 충분통계량으로','어떤 정보가 남는다는 걸까?','고정된 데이터와 움직이는 μ','제곱합을 전개하면','μ와 데이터가 만나는 항','평균이 상대 우도를 결정한다','다른 기록, 같은 평균','두 상대 우도 곡선의 일치','분산도 모른다면','합계와 제곱합을 함께','최소충분통계량','통계적 최소성과 저장량','어떤 정보를 보존할 것인가?']
claims=[
'백만 개는 전체 관측 수, 화면 숫자는 일부를 대표 표시. 저장 비트 수나 실제 백만 객체 표시를 주장하지 않음.',
'모집단 평균 μ는 미지 모수이고 표본평균 x̄와 구별. 독립·동일 정규분포·알려진 분산 조건을 표시.',
'고정 n의 알려진 분산 정규모형에서 x̄는 μ에 충분. 원자료 복원 가능한 압축이 아닌 모수 정보 보존.',
'원자료의 모든 정보와 지정한 모수에 대한 정보를 구별.',
'예시 σ²=4, 관측값1,2,3,4,5는 고정. 후보 μ를 움직여 확률밀도 변화와 우도 곱을 설명.',
'Σ(x_i−μ)²=Σx_i²−2μΣx_i+nμ². 전개 항과 색을 대응. 분산과 n은 고정.',
'Q=Σx_i²는 데이터 의존이지만 μ와 무관. μ와 데이터를 함께 포함하는 항은 −2μS이며 S=Σx_i.',
'고정 n·알려진 σ²에서 최대값1로 정규화한 상대 우도는 exp[−n(μ−x̄)²/(2σ²)]. 절대 우도 높이까지 같다는 뜻이 아님.',
'A=[1,2,3,4,5], B=[0,0,3,6,6], 각 n5·합15·평균3. B 중복 관측은 세로 적층해5개를 모두 표시.',
'두 데이터에 공통인 σ²=4에서 각각 최대 우도로 정규화하면 같은 상대 곡선. 절대 높이는 상수배로 다를 수 있음.',
'모형을 평균과 분산 모두 미지로 변경. 평균3은 같지만 평균에서의 제곱거리 합은10/36으로 다름.',
'고정 n에서 (Σx_i,Σx_i²)는 (μ,σ²)에 충분. A는(15,55), B는(15,81). 원자료나 모집단 분포 자체를 복원한다고 하지 않음.',
'최소충분 T는 임의의 다른 충분통계량 S의 함수 T=g(S). 화살표는 충분통계량에서 T로 향하며 T에서 원자료로 역복원하지 않음.',
'최소성은 통계적 구분의 의미이며 숫자 개수·저장 비트·실행시간 최솟값과 동일시하지 않음.',
'독립·동일 정규분포·분산 알려짐·고정 n 조건으로 돌아와 μ 정보 보존 결론. 전편 복습·다음 편 예고 없음.',
]
events=[
'0–3초 측정 숫자 일부 등장; 3–7초 데이터베이스와 전체1,000,000개 표시.',
'7–13초 길이가 다른 부품과 모집단 평균 μ 질문; 13–19초 독립·정규·분산 알려짐 조건.',
'19–25초 데이터→x̄=(Σx_i)/n; 25–33초 충분통계량 명칭과 μ 정보 보존.',
'33–38초 원자료 복원/μ 추론 정보의 차이를 질문.',
'38–41초 정규 밀도; 41–46초 고정 관측값에서 μ 이동; 46–51초 밀도의 곱으로 L(μ|x).',
'51–56초 Σ(x_i−μ)²; 56–63초 Q−2μS+nμ²의 세 항으로 전개.',
'63–69초 −2μS 강조와 S=Σx_i; 69–73초 μ와 무관한 Q를 C(x)에 포함.',
'73–79초 Σx_i=n x̄와 정규화 상대 우도 식.',
'79–81초 비교 준비; 81–82초 A 등장; 82–85초 B 등장; 85–88초 두 평균3.',
'88–95초 최대값1의 두 상대 우도 곡선 겹침; 95–100초 원자료 복원 불가·μ 정보 보존.',
'100–104초 평균 하나면 충분한지 질문; 104–107초 분산 미지로 모형 변경; 107–110초 퍼짐 비교.',
'110–117초 합15/15·제곱합55/81; 117–122초 추론 대상 μ,σ²와 모형 의존성.',
'122–127초 최소충분통계량 명칭; 127–131초 전체 데이터도 충분; 131–138초 임의 충분 S→T=g(S).',
'138–144초 통계적 최소성과 저장 용량·계산량을 구분.',
'144–147초 데이터 블록; 147–153초 모형 조건 아래 x̄와 μ 정보 보존 결론.',
]
timing=[];s=0
for e,t in rows:timing.append(dict(start=s,end=e,text=t));s=e
(P/'narration_timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(timing))+'\n',encoding='utf-8')
manifest=[];narr=[];tts=[]
for i,(a,b,title,claim,event) in enumerate(zip(bounds,bounds[1:],titles,claims,events),1):
 d=P/f'scenes/{i:02}';d.mkdir(parents=True,exist_ok=True)
 body=' '.join(r['text'] for r in timing if a<=r['start']<b)
 (d/'script.txt').write_text(body+'\n',encoding='utf-8')
 (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import SufficiencyScene\nclass Scene{i:02}(SufficiencyScene):\n    index={i-1}\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02} · {title}\n\n## 목적·핵심 주장\n{claim}\n\n## 앞 장면과 연결\n절대 시각{a}초에서 시작. 같은 데이터와 모형 조건을 유지하거나 조건 변경을 명시한다.\n\n## TTS 원문·확정 길이\n{body}\n\n구간{a}–{b}초, {b-a}초. 사용자 발화 시각, 음원 없음.\n\n## 화면·애니메이션\n{event}\n\nscene_engine.py part_{i-1:02}. 세로·가로 별도 배치.\n\n## 화면 텍스트\n제목 {title}. μ와 x̄, 밀도와 우도, 원자료와 통계량을 구별.\n\n## 시작·종료 상태\n해당 주장의 대상을 관찰하고 보존되는 정보 또는 모형 조건을 남겨 종료. 다음 편 예고 없음.\n\n## 정확성 확인\n{claim}\n',encoding='utf-8')
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title));narr.append(f'## {a}–{b}초 · {title}\n\n{body}');tts.append(body)
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
master='# 모든 것이 필요할까? 04 — 충분통계량\n\n사용자 확정 대본·153초.\n\n'+'\n\n'.join(narr)+'\n'
for name in ['narration.md','master_script.md']:(P/name).write_text(master,encoding='utf-8')
spoken='\n\n'.join(tts).replace('Minimal Sufficient Statistic','미니멀 서피션트 스태티스틱').replace('Sufficient Statistic','서피션트 스태티스틱').replace('1, 2, 3, 4, 5','일, 이, 삼, 사, 오').replace('0, 0, 3, 6, 6','영, 영, 삼, 육, 육').replace('모두 3','모두 삼')
(P/'tts_script.txt').write_text(spoken+'\n',encoding='utf-8')
(P/'scenes.yaml').write_text('id: minimal04_sufficiency\ntitle: 모든 것이 필요할까? 04 — 충분통계량\nvideo:\n  fps: 30\n  variants:\n    shorts: [1080, 1920]\n    longform: [1920, 1080]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
(P/'brief.md').write_text('# 제작 기준\n\n153초, 사용자 문장 종료 시각 기준. 세로1080×1920·가로1920×1080,30fps,무음·전체 발화 자막.\n\n고정 n, 독립·동일 정규분포·알려진 분산에서 평균 충분성을 설명. 비교 예시 σ²=4. 우도는 각 최대값1로 정규화한 곡선만 겹친다. 분산도 미지로 바꾸면 합15/15·제곱합55/81로 두 통계량 필요성을 보여준다.\n\nμ는 미지 모수, x̄는 관측 통계량. 충분성은 원자료 복원이 아니며 최소충분은 비트 수 최적화가 아님. 모든 충분통계량 S에서 T=g(S) 방향을 유지.\n\n자막은 concat 후 단일 ASS 트랙, 모든 문장 경계에서 겹침 검사.\n',encoding='utf-8')
example=P/'scenes/01_example'
if example.exists():
 assert example.resolve().is_relative_to(P.resolve());shutil.rmtree(example)
for name in ['build.py','caption_pass.py','inspect_frames.py','verify_caption_boundaries.py']:
 text=(W/'longforms/minimal03_sparsification'/name).read_text(encoding='utf-8').replace('minimal03','minimal04').replace('163','153').replace('4890','4590').replace('4889','4589')
 (P/name).write_text(text,encoding='utf-8')
shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\950a484c-d7d8-45b8-8381-2c4b4f2bf90c\붙여넣은 텍스트.txt'),P/'storyboard_user.md')
print(P,len(rows),len(manifest),sum(m['duration_seconds'] for m in manifest))
