"""User-approved narration and sentence end times; no inferred speech timing."""
import json,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
LINES='''6|신경망에 뉴런이 4,096개 있다면, 이 뉴런들은 정말 4,096개의 독립적인 정보를 표현하고 있을까요?
12|2019년, 연구진은 학습을 마친 신경망의 내부 표현이 실제로 몇 차원인지 측정했습니다.
16|그 결과, 뉴런의 개수보다 훨씬 낮은 차원이 관찰됐습니다.
18|그런데 여기서 말하는 차원은 무엇일까요?
22|세 개의 뉴런이 각각 하나의 숫자를 출력한다고 생각해 보겠습니다.
27|일반적으로 세 숫자를 독립적으로 변경하려면 세 개의 변수가 필요합니다.
33|하지만 첫 번째 뉴런이 t, 두 번째가 t의 제곱, 세 번째가 t의 세제곱을 출력한다면 어떨까요?
37|세 뉴런의 출력은 모두 하나의 변수 t에 의해 결정됩니다.
42|출력은 세 개지만, 가능한 값들은 3차원 공간 안의 하나의 곡선 위에 놓입니다.
49|이처럼 데이터를 표현하는 데 필요한 독립적인 변수의 수를 내재 차원, Intrinsic Dimension이라고 합니다.
53|연구진은 신경망의 각 층을 분석하면서 흥미로운 현상을 발견했습니다.
59|초기층에서는 측정된 내재 차원이 증가했지만, 더 깊은 층에서는 다시 감소하는 경향이 나타났습니다.
64|신경망이 처음에는 표현을 확장하고, 이후 다시 정리하는 것처럼 보인 것입니다.
71|연구진은 이것이 분류에 필요한 특징을 선택하고 불필요한 변화를 줄이는 과정과 관련될 수 있다고 해석했습니다.
75|그렇다면 실제 표현은 정말 이렇게 작은 차원에 존재하는 걸까요?
79|2026년, 다른 연구진이 이 해석에 중요한 의문을 제기했습니다.
82|문제는 차원을 측정하는 방법에 있었습니다.
87|우리가 관찰할 수 있는 것은 신경망이 만들어낸 데이터의 위치입니다.
91|하지만 이 점들만으로 실제 차원을 정확하게 알아내기는 어렵습니다.
95|예를 들어 하나의 직선 위에 점들이 모여 있다고 생각해 보겠습니다.
101|이 점들이 직선에서 조금씩 벗어나 흩어진다면, 작은 변화만으로도 차원 추정 결과에 영향을 줄 수 있습니다.
105|데이터의 분포나 표본 수에 따라서도 결과가 달라질 수 있습니다.
113|2026년 연구진은 기존 내재 차원 추정 방법이 실제 기하학적 차원의 변화를 제대로 추적하지 못할 수 있음을 보였습니다.
118|그렇다면 초기층에서 차원이 증가하고, 후반층에서 감소한다는 결과도 다시 생각해야 합니다.
125|측정된 숫자가 변했다고 해서 실제 표현의 차원까지 같은 방식으로 변했다고 단정할 수는 없기 때문입니다.
129|하지만 이것이 저차원 표현이 존재하지 않는다는 뜻은 아닙니다.
134|중요한 것은 실제 데이터 표현의 구조와, 관측을 통해 추정한 차원을 구분하는 것입니다.
141|신경망에는 수천 개의 뉴런이 존재하지만, 그 표현은 훨씬 적은 수의 독립적인 변수로 설명될 수도 있습니다.
143|그렇다면 우리는 무엇을 세고 있는 걸까요?
145|뉴런의 개수일까요?
148|데이터가 움직이는 독립적인 방향의 수일까요?
150|아니면 측정 방법이 보여주는 숫자일까요?
153|신경망의 진짜 차원은 과연 몇 개일까요?'''
SCENES=[('opening',0,6,'뉴런 수와 독립적인 정보의 수는 같을까?'),('research2019',6,18,'뉴런 수보다 낮은 측정 차원이 보고되었다'),('three_outputs',18,27,'세 뉴런의 세 출력을 독립적으로 조절한다'),('curve',27,42,'세 출력 t, t², t³는 한 곡선 위에서 움직인다'),('definition',42,49,'좌표 세 개와 독립 변수 하나를 구분한다'),('layers',49,64,'계층별 측정 차원은 증가 후 감소하는 경향을 보였다'),('interpretation',64,75,'표현 확장과 정리라는 해석에 질문을 던진다'),('research2026',75,91,'점들에서 실제 차원을 추정하는 방법을 검토한다'),('sampling',91,105,'변위·분포·표본 수가 관측에 영향을 준다'),('estimated_true',105,125,'측정 차원 변화만으로 실제 차원 변화를 확정하지 않는다'),('structure',125,141,'저차원 구조의 존재와 차원 추정 문제는 구분한다'),('question',141,153,'뉴런 수·실제 차원·추정 차원을 구분하는 질문')]
DETAILS=[
'0–2초 신경망 층 순차 등장, 2–4초 뉴런 수 4,096, 4–6초 독립적인 정보의 수를 묻는다. 출력값은 h로 표기한다.',
'6–12초 Ansuini et al. 논문과 활성화 행렬. 12–16초 뉴런 수와 낮은 측정 차원 대비. 16–18초 차원이란 무엇인가 질문. 4,096에 실험 차원값을 대응시키지 않는다.',
'18–22초 뉴런 3개와 각 출력 h1,h2,h3, 22–27초 값을 독립적으로 바꾸고 자유도 3을 표시한다.',
'27–33초 h1=t,h2=t²,h3=t³, 슬라이더 하나로 제어. 33–37초 출력 동기화. 37–42초 실제 ThreeDAxes의 c2p(t,t²,t³)를 사용한 ParametricFunction과 점 이동.',
'42–45초 3개 좌표축 강조. 45–49초 축을 어둡게 하고 곡선과 내재 차원 1 강조. 이 수학적 예시의 미분은 (1,2t,3t²)로 항상 영벡터가 아니다.',
'49–53초 신경망 계층과 측정 차원 그래프. 53–59초 증가 후 감소 패턴을 층별로 추적. 59–64초 확장과 정리 문구. 정량 축 눈금과 가짜 모델 이름을 넣지 않는다.',
'64–68초 상승 구간과 표현 확장. 68–71초 하강 구간과 특징 선택. 71–75초 정말 차원이 변했을까 질문.',
'75–79초 Schulte & Rügamer AISTATS 2026. 79–82초 추정 방법 강조. 82–87초 곡선 전체를 희미하게 하고 표본점만 유지. 87–91초 차원에 물음표.',
'91–95초 직선과 24개 점. 95–101초 작은 수직 변위와 최근접 거리 연결. 101–105초 표본 수·분포 변경. 고정된 기준선의 차원과 잡음 데이터의 수학적 차원을 동일시하지 않으며 임의 추정 수치를 표시하지 않는다.',
'105–113초 추정 방법에 대한 연구 주장, 노란 측정 곡선. 113–118초 측정된 내재 차원 라벨 강조. 118–125초 측정값에서 실제 차원으로 향하는 화살표를 물음표로 전환. 실제 차원이 특정 경로를 따른다고 그리지 않는다.',
'125–129초 (t,t²,t³) 곡선 재등장. 129–134초 구조와 관측점의 구분. 134–141초 구조를 아는 경우와 표본에서 차원을 추정하는 경우를 가로는 좌우, 세로는 상하로 배치.',
'141–143초 세 카드, 143–145초 뉴런 수, 145–148초 독립 변수, 148–150초 추정 방법 강조. 150–153초 최종 질문만 유지. 후속편 예고 없음.'
]
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
def main():
 rows=[];start=0
 for line in LINES.splitlines():
  end,s=line.split('|',1);end=int(end);rows.append(dict(start=start,end=end,text=s));start=end
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 script='\n\n'.join(r['text'] for r in rows)+'\n'
 for name in ['narration.md','master_script.md']:(R/name).write_text(script,encoding='utf-8')
 tts=script
 for a,b in [('4,096개','사천구십육 개'),('2019년','이천십구 년'),('2026년','이천이십육 년'),('3차원','삼차원'),('Intrinsic Dimension','인트린식 디멘션'),(' t',' 티')]:tts=tts.replace(a,b)
 (R/'tts_script.txt').write_text(tts,encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows,1))+'\n',encoding='utf-8')
 example=R/'scenes'/'01_example'
 if example.exists():shutil.rmtree(example)
 manifest=[]
 for i,(slug,start,end,claim) in enumerate(SCENES,1):
  folder=R/'scenes'/f'{i:02}_{slug}';folder.mkdir(parents=True,exist_ok=True)
  rr=[dict(r,start=max(start,r['start']),end=min(end,r['end'])) for r in rows if r['start']<end and r['end']>start]
  speech='\n\n'.join(r['text'] for r in rr)
  (folder/'script.txt').write_text(speech+'\n',encoding='utf-8')
  (folder/'timing.json').write_text(json.dumps(rr,ensure_ascii=False,indent=2),encoding='utf-8')
  (folder/'spec.md').write_text(f'# {i:02} — {claim}\n\n## 목적·핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('뉴런 수에서 시작하는 독립적인 질문.' if i==1 else SCENES[i-2][3])+f'\n\n## TTS 원문과 확정 길이\n{speech}\n\n사용자 종료 시각 기준 {start}–{end}초, {end-start}초. 전체 timing.json의 문장 경계를 그대로 적용한다. 문장 중간 씬 경계가 있으면 문장을 끊지 않고 자막을 이어 표시한다. 음원 미제공.\n\n## 화면·애니메이션·텍스트\n{DETAILS[i-1]}\n\n## 시작·종료 상태와 연결\n독립 교체 가능한 영상으로 완결하고, 다음 씬에서 같은 곡선 또는 그래프를 동일 배치로 이어받는다.\n\n## 정확성·출처\nAnsuini et al., NeurIPS 2019; Schulte & Rügamer, AISTATS 2026. 층별 곡선은 보고된 경향을 설명하는 정성 도식이며 정량 재현이 아니다. 변위 실험은 해당 논문의 직접 반례 재현이 아니다. 수학적 구조와 표본 추정을 구분한다. 사용자의 최신 요청에 따라 영상 내부에는 도식·원문 데이터 여부에 관한 안내 자막을 넣지 않고 제작 문서에만 기록한다.\n',encoding='utf-8')
  (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import RepresentationScene\nclass Scene{i:02}(RepresentationScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=folder.relative_to(R).as_posix(),start=start,end=end,duration_seconds=end-start,claim=claim,**{'class':f'Scene{i:02}'}))
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('title: 최소 조건 2부 · 신경망 2편 · 표현의 차원\nduration_seconds: 153\nlayouts: [1920x1080, 1080x1920]\nfps: 60\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
 (R/'brief.md').write_text('# 제작 기준\n\n최소 조건 2부 신경망 시리즈 다음 편(2편). 첨부 제목 03편은 원본 콘티의 번호로 보존한다. 사용자 제공 대본과 33개 문장 종료 시각 기준 153초. 롱폼 1920×1080, 쇼츠 1080×1920, 모두60fps·무음·전체 대본 자막.\n\n핵심: 뉴런 수, 표현의 실제 차원, 관측에서 추정한 차원은 서로 다르다. (t,t²,t³) 곡선은 실제 수학적 함수로 구현. 2019년 그래프는 보고된 경향을 보여주는 정성 도식으로 수치 축과 가짜 측정값을 넣지 않는다. 2026년 연구는 모든 저차원 표현을 부정한 것으로 표현하지 않는다. 잡음 추가가 엄밀한 차원 자체를 바꿀 수 있음을 제작상 고려하며, 기준선이 고정돼 있다는 이유로 잡음 데이터 차원도1이라고 표시하지 않는다. 실제 차원을 특정 경로로 단정하는 그래프를 넣지 않는다.\n\n최신 사용자 요청: 영상 내부에 실제·관측·도식 데이터 여부에 관한 안내성 자막은 넣지 않는다. 개념을 구분하는 본문 설명과 실제 대본 자막은 유지한다. 그래프의 제작 방식과 출처는 이 문서와 README에 기록한다. 복습·후속편 예고 없음.\n\n출처:\nhttps://papers.nips.cc/paper_files/paper/2019/hash/cfcce0621b49c983991ead4c3d4d3b6b-Abstract.html\nhttps://proceedings.mlr.press/v300/schulte26a.html\n',encoding='utf-8')
 shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\14c9f834-0edf-4fc6-87b2-cb6acee68c77\붙여넣은 텍스트.txt'),R/'storyboard_reference.md')
if __name__=='__main__':main()
