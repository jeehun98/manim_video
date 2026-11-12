import json
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
raw=[s.strip() for s in (P/'narration_source.txt').read_text(encoding='utf-8').splitlines() if s.strip()]
sentences=[];start=0
for i in range(0,len(raw),2):
    end=int(raw[i+1]);assert end>start
    sentences.append(dict(start=start,end=end,text=raw[i].replace('**','')));start=end
assert start==167
names=['흑체복사','광전효과','프랑크–헤르츠','슈테른–게를라흐','콤프턴 산란','전자 회절','전자 이중슬릿','벨 부등식','양자 지우개']
short=['흑체복사','광전효과','프랑크–헤르츠','슈테른–게를라흐','콤프턴','전자 회절','이중슬릿','벨 실험','양자 지우개']
years=[1900,1905,1914,1922,1923,1927,1961,1972,1992]
tiers=['C','A','B','A','B','A','S','S','C']
cuts=[0,5,24,41,57,71,86,103,122,146,167]
grades=[18,37,56,70,83,102,116,140,159]
exps=[dict(name=a,short=b,year=y,tier=t,grade=g) for a,b,y,t,g in zip(names,short,years,tiers,grades)]
scenes=[dict(id=f'{i+1:02}',**{'class':f'Shot{i+1:02}'},start=cuts[i],end=cuts[i+1],title='양자역학 티어리스트' if i==0 else names[i-1]) for i in range(10)]
data=dict(title='양자역학 실험 티어리스트',revision='v1_167s',duration=167,timing_source='사용자 제공 문장 종료 시각',sentences=sentences,scenes=scenes,experiments=exps)
for n in ['script.json','timing.json']:(P/n).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
def wrap(s,n=27):
    out=[];line=''
    for w in s.split():
        if line and len(line)+len(w)+1>n:out.append(line);line=w
        else:line=(line+' '+w).strip()
    return '\n'.join(out+[line])
(P/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
(P/'narration.md').write_text('# 양자역학 실험 티어리스트\n\n확정 원문·167초·음원 미제공\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n',encoding='utf-8')
readings={'1900년':'천구백 년','1905년':'천구백오 년','1914년':'천구백십사 년','1922년':'천구백이십이 년','1923년':'천구백이십삼 년','1927년':'천구백이십칠 년','1961년':'천구백육십일 년','1972년':'천구백칠십이 년','1992년':'천구백구십이 년','X선':'엑스선','S 티어':'에스 티어','A 티어':'에이 티어','B 티어':'비 티어','C 티어':'씨 티어'}
tts=[]
for s in sentences:
    t=s['text']
    for a,b in readings.items():t=t.replace(a,b)
    tts.append(t)
(P/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
details=['고정된 상단 티어보드와 9개 하단 벡터 아이콘 소개. 평가 기준은 영상의 관점임을 표시.',
 '플랑크 분포와 레일리–진스 곡선은 이론 도식. 짧은 파장에서 고전 곡선 발산. 플랑크 가정 E=nhν. 1900은 이론 제안 연도.',
 '단일 광자·보통 세기의 모형. 낮은 주파수에서 빛 세기만 증가해도 방출 없음. 높은 주파수에서 Kmax=hν−Φ. 다광자 영역을 일반화하지 않음.',
 '수은의 4.9eV 비탄성 충돌·내부 여기. 전류–전압 도식은 정성적이며 접촉 전위에 따라 최저점 위치가 달라짐.',
 '불균일 자기장 속 중성 은 원자 빔의 두 분리 분포. 처음부터 전자 스핀 측정으로 해석한 역사처럼 그리지 않음.',
 '자유 정지 전자 근사. 산란각60도, ε=1, 광자 에너지 2/3 및 반동 운동량 보존. 파형은 파장 표시이며 물결 궤적 아님.',
 '1927 Davisson–Germer를 반영한 결정 격자와 각도별 회절 피크. 단일 결정에 다결정 동심 고리를 붙이지 않음.',
 '1961 Jönsson 전자 이중슬릿의 간섭. 이후 단일 전자 검출 축적을 별도 시점 라벨로 구별. 도식 확률분포에서 시드 고정 표본추출; 입자가 고전적 두 경로를 동시에 걷는 연출 아님.',
 '1972 Freedman–Clauser. CHSH |S|≤2와2√2는 현대적 이론 설명용, 1972 실측 수치로 표시하지 않음. 원격 신호·초광속 통신 연출 없음. 해당 실험에 보조 가정·허점이 있었음을 작은 주석으로 구별.',
 '1992 Kwiat–Steinberg–Chiao 편광 표식 기반 도식. 전체=간섭 없음, ±측정 결과 분류=상보적인 조건부 무늬. 합하면 원래 전체. 2000 지연선택 실험 도식과 혼동하지 않음. C등급은 요청한 평가. 별도 요약·질문·엔드카드 없음.'
]
for i,s in enumerate(scenes):
    f=P/'scenes'/s['id'];f.mkdir(parents=True,exist_ok=True)
    (f/'scene.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom episodes.qtier01_experiments.direction import TierScene\n\nclass "+s['class']+'(TierScene):\n    shot='+str(i)+'\n',encoding='utf-8')
    (f/'spec.md').write_text(f"# {s['title']}\n\n{s['start']}–{s['end']}초 · {(s['end']-s['start'])*60}프레임\n\n{details[i]}\n\n동일 티어보드·무대를 유지하며 실험별 독립 렌더. 시작 시 이전 실험 등급 배치 상태를 정확히 복원. 해당 실험의 등급 발화 구간에 카드 이동. 문장별 대본·경계는 script.json. 자막은 중앙 무대 하단 전용 영역.\n",encoding='utf-8')
(P/'brief.md').write_text('# 제작 기준\n\n167초·'+str(len(sentences))+'문장·9실험+도입. 사용자 대본·등급·발화시간 유지. 9:16 1080×1920 60fps, 무음·전체 자막. 첨부 화면의 상단 티어보드·중앙 무대·하단9개 아이콘 배치. 상단 카드 상태는 씬 경계에서 동일하게 복원. 일반 물리적 중요도의 객관적 순위가 아니라 영상의 관점임을 표시.\n\n'+'\n\n'.join(details)+'\n\n출처: https://doi.org/10.1103/PhysRevA.45.7729 ; https://doi.org/10.1103/PhysRevLett.28.938 ; https://www.unicamp.br/~chibeni/textosdidaticos/jonsson-electron-diffraction-ajp-1974.pdf\n',encoding='utf-8')
(P/'README.md').write_text('# 양자역학 실험 티어리스트\n\n확정167초·9:16·1080×1920·60fps·무음·전체 자막.\n\n최종: `py -3.12 scripts/render.py qtier01`\n\n대표 씬: `py -3.12 episodes/qtier01_experiments/build.py --preview --scene 02 08 09 10`\n\n첨부 레이아웃에 맞춘 고정 무대와 누적 티어보드. 등급은 사용자 지정 S:이중슬릿·벨/A:광전·SG·회절/B:FH·콤프턴/C:흑체·지우개. 대본 원문은 narration_source.txt, 타이밍은 script.json, 상세 물리 조건은 brief.md 및 씬 spec.\n',encoding='utf-8')
if not (P/'build.py').exists():
    b=(ROOT/'episodes/basis01_fourier_heat/build.py').read_text(encoding='utf-8').replace('basis01','qtier01').replace('v1_175s','v1_167s').replace('==175','==167').replace("'34 exact user-supplied sentence ends; 13 scenes; no gaps or overlaps'",f"'{len(sentences)} exact user-supplied sentence ends; 10 scenes; no gaps or overlaps'")
    b=b.replace("sentence['text']==original[2*i]","sentence['text']==original[2*i].replace('**','')")
    (P/'build.py').write_text(b,encoding='utf-8')
print('Prepared',len(sentences),'sentences, 167 seconds')
