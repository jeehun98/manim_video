"""Approved revised script; sentence endpoints are supplied by the user."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
RAW=(HERE/"narration_input.txt").read_text(encoding="utf-8").splitlines()
BOUNDS=[0, 8, 16, 30, 41, 52, 66, 82, 94, 104, 120, 136, 150, 160, 168]
TITLES=['문장 하나만 주어진다면', '같은 문장에 상황을 더하면', '상황을 가리키는 표현 · 직시', '문장과 함께 들어오는 정보', '문맥에 따라 가능성을 갱신한다', '같은 말이 다르게 들린다면', '이번에는 괜찮네', '경험과 기대가 바꾸는 해석', '해석은 무제한으로 자유롭지 않다', '해석의 불확실성 · 엔트로피', '어떤 불확실성을 해소하는가?', '짧은 표현과 공유된 정보', '표현에 조건을 더한다면', '같은 기호가 언제나 같은 의미일까?']
DETAILS=['0–8 도입·그거/거기 대상 불명. 원문에서 읽으면→보면 수정.', '8–16 이전 연출 재사용하되 새 대본 자막 반영. 문장 동일성 유지.', '16–22 직시Deixis를 앞 사례와 연결,22–27 문장에 책/책상 없음,27–30 정보 출처 질문.', '30–37 손짓·시선·상황·경험을 입력하고,37–41 설명용 후보분포를 소개. 실측 데이터가 아님.', '41–47 하나의 분포를 보간해 갱신,47–52 P(M|S,C) 및 베이즈 추론. 확률합1, 사전분포와 우도로 실제 사후분포 수학검증.', '52–58 서로 다른 해석 질문,58–62 접시와 두 인물,62–66 말풍선 이번에는 괜찮네 도입. 표정은 중립.', '66–70 칭찬 가능성,70–76 과거에 대한 부정적 평가로 받아들일 가능성,76–82 관계/경험/기대/감정. 두 해석은 배타적 의미의 실험판정이 아님.', '82–90 사전정보에 따른 상대가능성.84초부터 두 개념분포를 병렬 비교,90–94 공통 언어의미 부정 금지. 사람기억을 통계적 사전확률과 일대일 대응시키지 않는다.', '94–100 언어규칙과 관습이 후보를 제한,100–104 문맥은 무엇을 바꾸는지 질문. 관련없는 후보는 이 대화 상황에서만 제외.', '104–109 엔트로피수식과 균등4후보2bits,109–115 한후보유력해지도록 동일그래프보간 및 H실시간연동,115–120 조건의 평균적 성질과 특정사례 구분. 엔트로피는 분포의 불확실성이지 해석 정답률이 아님.', '120–125 길이와 유용성 질문,125–131 긴 무관설명과 짧은 지시손짓 비교,131–136 해결하려는 불확실성에 대한 정보의 관련성. 정보의 양은 문자수/길이로 분리표기하여 Shannon정보량과 혼동하지 않는다.', '136–141 문장만으로 모든정보를 기록할필요없음,141–146 공유정보 결합,146–150 서로다른해석가능성. 조건부상호정보량 수식은 생략하여 본문시간 준수.', '150–155 조금더빠르게와 조건물음표,155–160 v2=v1+delta v 및속력증가량정의(단위m/s,delta v>0). 조금의크기는미정.', '160–165 x+y와실수/벡터의정의차이,165–168 같은기호의해석질문. 별도예고·엔드카드없음.']
sentences=[];start=0
for i in range(0,len(RAW),2):
 end=int(RAW[i+1]);sentences.append(dict(start=start,end=end,text=RAW[i]));start=end
scenes=[dict(id=f'{i+1:02}',**{'class':f'Shot{i+1:02}'},start=a,end=b,title=TITLES[i]) for i,(a,b) in enumerate(zip(BOUNDS,BOUNDS[1:]))]
data=dict(title='같은 문장인데 왜 다른 의미가 만들어질까?',revision='v2_168s',duration=168,timing_source='사용자 제공 문장 종료 시각',sentences=sentences,scenes=scenes)
for name,obj in [('script.json',data),('timing.json',dict(fps=60,**data))]:(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def wrap(s,n=26):
 lines=[];line=''
 for w in s.split():
  if line and len(line)+len(w)+1>n:lines.append(line);line=w
  else:line=(line+' '+w).strip()
 return '\n'.join(lines+[line])
(HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
(HERE/'narration.md').write_text('# 같은 문장인데 왜 다른 의미가 만들어질까?'+'\n\n사용자 확정 대본 · 168초\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n',encoding='utf-8')
(HERE/'tts_script.txt').write_text('\n\n'.join(s['text'].replace('Deixis','다익시스') for s in sentences)+'\n',encoding='utf-8')
for i,s in enumerate(scenes):
 folder=HERE/'scenes'/s['id'];folder.mkdir(parents=True,exist_ok=True)
 (folder/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom episodes.expression01_sentence_meaning.direction import ExpressionScene\n\nclass '+s['class']+'(ExpressionScene):\n    shot='+str(i)+'\n',encoding='utf-8')
 (folder/'spec.md').write_text(f"# {s['title']}\n\n{s['start']}–{s['end']}초 · {(s['end']-s['start'])*60}프레임\n\n{DETAILS[i]}\n\n쇼츠와 가로는 같은 애니메이션 로직,화면비별 독립 위치/폭/배치 사용. 확정대본과 자막경계는 script.json. 무음.\n",encoding='utf-8')
(HERE/'brief.md').write_text('# 수정 제작 기준\n\n사용자 확정37문장,168초·10080프레임·60fps. 가로1920×1080/세로1080×1920,무음·전체내레이션자막. 이전127초 버전 소스와 검사자료는 revisions/v1_127s,완성영상은 exports/*_v1_127s.mp4로 보존. 새파일이 완성된 뒤 현재파일 갱신.\n\n문장·직시→문맥의확률적모형→같은발언의두해석→엔트로피→관련정보→수학기호의정의. 모든확률은설명용가상분포. 사람의실제정신과정을베이즈계산으로단정하지않으며개인기억과사전확률은일대일대응아님. 엔트로피감소는일반적으로평균적성질;특정문맥이항상불확실성을줄이는것아님. 엔트로피와정답률,문자수와Shannon정보량을구분.\n\n검토출처: https://www.problang.org/chapters/01-introduction.html ; https://web.stanford.edu/class/ee276/files/lectures/lecture2.pdf ; https://plato.stanford.edu/entries/indexicals/ . 사용자대본은수정하지않고조건은화면소주석으로보완.\n\n같은애니메이션로직,화면비별독립레이아웃. 색상문장#60A5FA,문맥#34D399,미확정#FBBF24,배경#0B1020. 추가복습·예고·별도엔드카드없음.\n',encoding='utf-8')
assert len(sentences)==37 and sentences[-1]['end']==168
