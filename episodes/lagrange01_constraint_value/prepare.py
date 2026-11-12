import json
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
lines=[x.strip() for x in (P/'narration_source.txt').read_text(encoding='utf-8').splitlines() if x.strip()]
ss=[];start=0
for i in range(0,len(lines),2):
    end=int(lines[i+1]);assert end>start
    ss.append(dict(start=start,end=end,text=lines[i]));start=end
assert start==160
cuts=[0,13,26,37,58,68,89,113,131,146,160]
titles=['조건을 바꾸면 최댓값은?','둘레 20, 넓이는 얼마나?','움직일 수 있는 범위','같은 넓이를 잇는 곡선','직선과 곡선이 접하는 순간','접선이 아닌, 기울기의 방향','두 벡터의 배율 λ','둘레 20 → 20.1','같은 2.5, 새로운 의미','최적점과 제약의 민감도']
details=[
 'Amax(P)=P²/16의 동일 값함수 그래프를 도입·후반 재사용. 제약 완화와 최적값 증가, λ 미지수.',
 '실제 가로·세로 비율을 고정배율 .5로 표현. x+y=10인 2×8,4×6,3×7을 비교. A=xy. 최댓값은 접점 장면에서 확정.',
 'g=2x+2y=20. 가로만 늘려 위반한 뒤 세로를 줄여 복귀. g를 x+y로 재정의하지 않음. 수평·수직 실제 비율 유지.',
 '등간격 양축 0–11. (2,8)→(4,4)는 정확히 xy=16 곡선을 따라 이동. 등고선9,16,25,36. 제약 직선2x+2y=20을 추가하고 허용점은 그 위에서 이동.',
 'x 트래커 한 개가 점(x,10−x), 등고선xy=x(10−x), 면적 수치를 동시에 구동. 최적점을 지나면 면적 감소, 다시 (5,5)에서A25. 샘플 곡선에 x5 포함해 정확한 접점.',
 '같은 접점에서 ∇f=(5,5),∇g=(2,2). 두 화살표는 같은 시작점·동일 좌표배율. 공통 접선(1,−1)에 수직. 매끄러운 내부 최적점·∇g≠0이라는 조건. 접선 방향1차미분0은 일반적 최대 충분조건이 아님.',
 'λ는1→2.5. ∇g=(2,2)는 넓고 옅은 원래 화살표로 고정. λ∇g만 보라색으로 길어짐. ∇f 화살표와 정확한 끝점 일치. g=2x+2y라는 제약 정규화를 유지.',
 'P20→20.1, 정사각형 변5→5.025, A25→25.250625. 작은 실제 변화를 과장하지 않고 테두리와 수치로 강조. ΔA=.250625, ΔP=.1.',
 '유한 차분2.50625≈2.5와 도함수P/8|20=2.5를 구별. L=f−λ(g−P)의 부호 관례. 매끄러운 최적해 아래 값함수의 민감도. 도입의 동일 값함수 그래프와 접선 연결.',
 'λ(P)=P/8, P20→24일 때2.5→3으로 달라짐. 최적점 조건과 최적값 민감도 관계를 같은 예제에서 연결. 원문 결론 안에서 마무리, 별도 엔드카드·예고 없음.'
]
scenes=[dict(id=f'{i+1:02}',**{'class':f'Shot{i+1:02}'},start=cuts[i],end=cuts[i+1],title=titles[i]) for i in range(10)]
d=dict(title='라그랑주 승수법 — 제약의 가치',revision='v1_160s',duration=160,timing_source='사용자 제공 문장 종료 시각',sentences=ss,scenes=scenes)
for name in ['script.json','timing.json']:(P/name).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
def wrap(s,n=26):
    a=[];line=''
    for w in s.split():
        if line and len(line)+len(w)+1>n:a.append(line);line=w
        else:line=(line+' '+w).strip()
    return '\n'.join(a+[line])
(P/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(ss))+'\n',encoding='utf-8')
(P/'narration.md').write_text('# '+d['title']+'\n\n사용자 확정 원문·160초·음원 미제공\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in ss)+'\n',encoding='utf-8')
tts=[]
for s in ss:
    t=s['text'].replace('x','엑스').replace('y','와이')
    for a,b in [('25.25','이십오 점 이오'),('20.1','이십 점 일'),('2.5','이 점 오'),('0.25','영 점 이오'),('0.1','영 점 일'),('25','이십오'),('20','이십'),('5','오'),('2','이')]:t=t.replace(a,b)
    tts.append(t)
(P/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
for i,s in enumerate(scenes):
    f=P/'scenes'/s['id'];f.mkdir(parents=True,exist_ok=True)
    (f/'scene.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom episodes.lagrange01_constraint_value.direction import LagrangeScene\n\nclass "+s['class']+'(LagrangeScene):\n    shot='+str(i)+'\n',encoding='utf-8')
    (f/'spec.md').write_text(f"# {s['title']}\n\n{s['start']}–{s['end']}초 · {(s['end']-s['start'])*60}프레임\n\n{details[i]}\n\n시작·종료 상태는 동일 직사각형 문제와 축 위치를 공유. 독립 렌더·교체 가능. 해당 구간 확정 대본과 타이밍은 script.json. 하단 자막 영역을 분리.\n",encoding='utf-8')
(P/'brief.md').write_text('# 제작 기준\n\n확정'+str(len(ss))+'문장·160초·10개 독립 씬. 9:16 1080×1920 60fps, 음원 미제공으로 무음·전체 자막. 사용자 원문·발화시간 유지. 공통 QCS 자막·타이밍·레이아웃 및 hash 검증 빌더 재사용. 요청한 세로 영상만 제작.\n\n'+'\n\n'.join(details)+'\n\n최대성은A=x(10−x)=25−(x−5)²로 검증. 일반적인 승수 조건은 필요조건임을 구별. 민감도·부호는g=2x+2y=P, L=f−λ(g−P) 기준.\n\n출처: https://math.mit.edu/~djk/18_022/chapter04/section03.html ; https://faculty.arts.ubc.ca/pschrimpf/526/optimization-526.pdf\n',encoding='utf-8')
(P/'README.md').write_text('# 라그랑주 승수법 — 제약의 가치\n\n160초·9:16·1080×1920·60fps·무음·전체 자막.\n\n최종 렌더: `py -3.12 scripts/render.py lagrange01`\n\n대표 씬: `py -3.12 episodes/lagrange01_constraint_value/build.py --preview --scene 04 05 07 08 09`\n\n확정 원문 narration_source.txt, 문장 경계 script.json, 장면별 spec·소스 scenes/. g=2x+2y=P. Amax(P)=P²/16, λ=P/8. P20에서순간변화율2.5; P20→20.1의평균변화율2.50625를 구별.\n',encoding='utf-8')
if not (P/'build.py').exists():
    b=(ROOT/'episodes/basis01_fourier_heat/build.py').read_text(encoding='utf-8').replace('basis01','lagrange01').replace('v1_175s','v1_160s').replace('==175','==160').replace("'34 exact user-supplied sentence ends; 13 scenes; no gaps or overlaps'",f"'{len(ss)} exact user-supplied sentence ends; 10 scenes; no gaps or overlaps'")
    (P/'build.py').write_text(b,encoding='utf-8')
print('Prepared',len(ss),'sentences, 160 seconds')
