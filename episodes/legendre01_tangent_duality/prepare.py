import json
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
raw=[x.strip() for x in (P/'narration_source.txt').read_text(encoding='utf-8').splitlines() if x.strip()]
ss=[];start=0
for i in range(0,len(raw),2):
    end=int(raw[i+1]);assert end>start
    ss.append(dict(start=start,end=end,text=raw[i]));start=end
assert start==157
cuts=[0,8,26,43,54,64,73,82,101,117,128,144,157]
titles=['입력과 높이로 보는 함수','점 대신 접선으로 본다면?','접점을 옮기면 기울기도 바뀐다','기울기가 접점의 위치를 정한다','직선의 두 정보: 기울기와 절편','접선 하나가 새로운 점 하나로','왜 절편의 부호를 바꿀까?','x²를 기울기 p로 표현하면','접선의 정보를 다시 변환한다','원래 함수를 되찾는 조건','변수 치환을 넘어, 다른 표현으로','같은 구조를 보는 다른 기준']
details=[
 '동일 파란 포물선 f(x)=x². 접점 트래커가 입력·함수값·점선을 함께 갱신.',
 '8초 접선 질문. 예제 x²의 원점·양쪽 높이를 보여주고 같은 함수·축을 유지.',
 'Y=2aX−a²를 매 프레임 정확히 계산하고 좌표창에서만 표시. x1→1.6→−1.5로 이동. p=2a. 양축 물리 단위 동일.',
 '엄격 볼록한 x²에서는 p=2x가 일대일. p2→4면 접점1→2. 모든 함수에서 성립한다는 주장 아님.',
 '접선의 가로좌표X와 접점x 구별. Y=pX+b; p=2x,b=−x². 기울기 삼각형·절편 점이 같은 트래커에 연동.',
 '9:16 가독성을 위해 원래·새 그래프를 위아래에 배치. 두 축은 같은 배율. 접점x→새좌표(2x,x²), 절편b는 원래 y축 위에 위치. 샘플점이 쌓여보라곡선p²/4 형성.',
 'Y=pX+[f(x)−px]에서 b=f(x)−px. 접점 p=f′(x) 아래 f*(p)=−b=px−f(x). 일반 볼록 켤레 정의는sup_x(px−f(x))임을 화면 보충.',
 'p=2x→x=p/2→f*=p²/2−p²/4=p²/4. 단순 가로 늘리기 연출 없음. 두 그래프는 동일한 축 범위·배율과 서로 다른 가로축x,p.',
 '역변환은 윗 보라 그래프의 접점p를 새 트래커로 사용. 기울기x=p/2, 절편c=−p²/4에서 아래 복원점(x,−c). 실제 역대응 샘플로 파란 포물선 생성.',
 'f**(x)=sup_p(xp−f*(p))=x². 예제는 매끄럽고 엄격히 볼록. 일반 이중 켤레 복원은 적정(proper)·닫힌 볼록함수. 비볼록 함수가 일반적으로 그대로 복원된다는 주장 금지.',
 '같은 파란/보라 구조를 유지하다 응용 두 개. 역학H=pv−L, p=∂L/∂v(정칙 조건). 열역학F=U−TS는 엔트로피에 대한 양의 볼록 켤레와 부호가 반대임을 표기.',
 '동일 축 배율의 파랑·보라 그래프. x,f(x)와p,−b의 정보 기준을 구별. 별도 엔드카드·예고·이전 편 요약 없음. 마지막1.5초본문 유지.'
]
scenes=[dict(id=f'{i+1:02}',**{'class':f'Shot{i+1:02}'},start=cuts[i],end=cuts[i+1],title=titles[i]) for i in range(12)]
d=dict(title='르장드르 변환 — 점의 정보에서 접선의 정보로',revision='v1_157s',duration=157,timing_source='사용자 제공 문장 종료 시각',sentences=ss,scenes=scenes)
for n in ['script.json','timing.json']:(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
def wrap(s,n=26):
    out=[];line=''
    for w in s.split():
        if line and len(line)+len(w)+1>n:out.append(line);line=w
        else:line=(line+' '+w).strip()
    return '\n'.join(out+[line])
(P/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(ss))+'\n',encoding='utf-8')
(P/'narration.md').write_text('# '+d['title']+'\n\n사용자 확정 원문·157초·음원 미제공\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in ss)+'\n',encoding='utf-8')
(P/'tts_script.txt').write_text('\n\n'.join(s['text'].replace('x','엑스').replace('p','피').replace('f','에프').replace('2','이').replace('4','사') for s in ss)+'\n',encoding='utf-8')
for i,s in enumerate(scenes):
    f=P/'scenes'/s['id'];f.mkdir(parents=True,exist_ok=True)
    (f/'scene.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom episodes.legendre01_tangent_duality.direction import LegendreScene\n\nclass "+s['class']+'(LegendreScene):\n    shot='+str(i)+'\n',encoding='utf-8')
    (f/'spec.md').write_text(f"# {s['title']}\n\n{s['start']}–{s['end']}초 · {(s['end']-s['start'])*60}프레임\n\n{details[i]}\n\n앞 장면의 포물선·접선·색 의미를 계승하며 독립 렌더·교체 가능. 시작·종료 상태와 대본은 script.json 해당 구간 및 direction.py 해당 메서드. 하단 자막 전용 영역 분리.\n",encoding='utf-8')
(P/'brief.md').write_text('# 제작 기준\n\n확정'+str(len(ss))+'문장·157초·12개 독립 씬. 9:16 1080×1920 60fps, 무음·전체 자막. 확정 대본·발화시간 유지. QCS 자막·레이아웃·타이밍과 hash 빌더 재사용.\n\n'+'\n\n'.join(details)+'\n\n일반 정의f*=sup_x(px−f(x)). 매끄러운 엄격 볼록 예제에서는 p=f′(x)인 극대점에서 평가. 적정·닫힌 볼록함수의 이중 켤레 복원과 매끄러운 특수 사례를 구별. 열역학F=−U*_S, 고전역학H는속도에대한켤레(정칙성 필요).\n\n출처: https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf (3.3절)\n',encoding='utf-8')
(P/'README.md').write_text('# 르장드르 변환 — 접선의 정보\n\n157초·9:16·1080×1920·60fps·무음·전체 자막.\n\n최종: `py -3.12 scripts/render.py legendre01`\n\n대표 씬: `py -3.12 episodes/legendre01_tangent_duality/build.py --preview --scene 03 06 07 09`\n\n확정 원문narration_source.txt, 타이밍script.json, 장면별spec·소스scenes/. 접선Y=2xX−x², p=2x,b=−x², f*=p²/4, f**=x². 일반 정의·복원 조건·응용의 부호를 구별.\n',encoding='utf-8')
if not (P/'build.py').exists():
    b=(ROOT/'episodes/lagrange01_constraint_value/build.py').read_text(encoding='utf-8').replace('lagrange01','legendre01').replace('v1_160s','v1_157s').replace('==160','==157').replace("'38 exact user-supplied sentence ends; 10 scenes; no gaps or overlaps'",f"'{len(ss)} exact user-supplied sentence ends; 12 scenes; no gaps or overlaps'")
    (P/'build.py').write_text(b,encoding='utf-8')
print('Prepared',len(ss),'sentences; 157 seconds')
