"""Generate production materials from supplied narration, never estimate timings."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
lines=[s.strip() for s in (HERE/'narration_source.txt').read_text(encoding='utf-8').splitlines() if s.strip()]
sentences=[];start=0
for i in range(0,len(lines),2):
    end=int(lines[i+1]);assert end>start
    sentences.append(dict(start=start,end=end,text=lines[i]));start=end
assert start==175 and len(sentences)==34,(start,len(sentences))
cuts=[0,8,22,38,51,75,83,96,104,117,135,144,157,175]
titles=['복잡한 형태의 기본 요소는?','18세기 · 진동하는 줄','합성하고, 다시 분해한다','19세기 · 푸리에와 열전달','같은 곡선, 다른 물리적 의미','가운데의 열은 양옆으로','온도 변화와 곡선의 휘어짐','두 번 미분해도 같은 성분','모양 대신 진폭을 계산한다','성분마다 계산하고 다시 더한다','복잡한 변화가 단순한 계산으로','신호에서 신경망까지','물리적 최소 단위에서 수학적 기저로']
details=[
 '흰 복합 파형에서 청·녹·보라 세 성분으로 분해. 첫 후보 사인·코사인. 실제로 모든 자연현상을 세 성분으로 표현한다는 주장이 아님.',
 '양끝 고정 줄. sin(nx)cos(nτ), n=1,2,3. 성분과 합성의 진동은 동일한 시간 τ. 베르누이 역사 정보는 작게.',
 '같은 x에서 높이를 더해 합성. 모드 2,3의 진폭을 점진적으로 추가. 분해된 세 성분과 합성 곡선을 연결. 31초 이후 정지해 함수 표현을 강조.',
 '푸리에와 금속 막대. u=T−Tref에 대해 양끝 u=0. 온도색은 실제 사인 모드 열방정식 해를 사용. 외부 열원은 초기 분포 설정을 뜻함.',
 '51초부터 같은 곡선을 유지한 채 변위 → 온도 편차 축 이름만 교체. 60초부터 세 사인 성분 분해. 일반 급수는 코사인·상수항도 허용. 움직임과 공간 함수의 구별.',
 '양 끝 Tref 고정. 중앙 열이 주변으로 퍼지며 봉우리 하강·주변 상승. 색상과 그래프는 같은 해와 시간 변수 사용.',
 '열방정식 u_t=αu_xx. 봉우리에서 곡률 음수→감소, 골짜기 곡률 양수→증가. 균질한 1차원 막대, 내부 열원 없음. 곡률의 부호와 온도 변화 방향 연결.',
 'sin(kx)→k cos(kx)→−k²sin(kx). k=1 그래프의 실제 미분을 먼저 보여주고 n=1,2,3의 −1,−4,−9를 표시. 주파수는 미분 전후 유지.',
 '단일 공간 모드 sin x. u=A(t)sin x, A=e^(−αt). 초기 점선 유지. 진폭 표시와 곡선은 동일한 시간. 양끝 온도 편차0 고정.',
 '계수 [1,.15,−.2], L=π, α=.18. n=1,2,3을 모두 같은 t로 갱신. A_n(t)=A_n(0)e^(−α n²t). 각 성분 위에 동일 비율 진폭 지표, 합성은 실제 합. 높은 공간주파수의 더 빠른 감쇠.',
 '이전 성분과 합성의 연결 유지. 복잡한 함수→성분별 진폭→간단한 계산. 일반 급수의 무한합과 데모의 세 성분 유한합을 구별.',
 '소리·빛·신호·이미지. 좌표 x → sin/cos 주파수 특징 → MLP. 일부 좌표 기반 신경망의 예시이며 모든 AI가 같은 방식이라는 주장이 아님.',
 '물리적 최소 단위 아님. 함수공간·경계조건에 맞는 기저. 일반 Fourier 급수 상수·sin·cos. 기저는 유일하지 않음. 별도 엔드카드·예고 없음.'
]
scenes=[dict(id=f'{i+1:02}',**{'class':f'Shot{i+1:02}'},start=cuts[i],end=cuts[i+1],title=titles[i]) for i in range(13)]
data=dict(title='수학의 기본 요소 — 후보 01. 사인과 코사인',revision='v1_175s',duration=175,timing_source='사용자 제공 34문장 종료 시각',sentences=sentences,scenes=scenes)
for name in ['script.json','timing.json']:(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
def wrap(s,n=26):
    lines=[];line=''
    for w in s.split():
        if line and len(line)+len(w)+1>n:lines.append(line);line=w
        else:line=(line+' '+w).strip()
    return '\n'.join(lines+[line])
(HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
(HERE/'narration.md').write_text('# '+data['title']+'\n\n확정 원문·175초·음원 미제공\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n',encoding='utf-8')
tts=[s['text'].replace('18세기','십팔 세기').replace('19세기','십구 세기') for s in sentences]
(HERE/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
for i,s in enumerate(scenes):
    folder=HERE/'scenes'/s['id'];folder.mkdir(parents=True,exist_ok=True)
    (folder/'scene.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom episodes.basis01_fourier_heat.direction import FourierScene\n\nclass "+s['class']+'(FourierScene):\n    shot='+str(i)+'\n',encoding='utf-8')
    (folder/'spec.md').write_text(f"# {s['title']}\n\n{s['start']}–{s['end']}秒 · {(s['end']-s['start'])*60} frames\n\n主張: ".replace('秒','초').replace('主張','핵심 주장')+details[i]+'\n\n확정 대본과 문장 경계는 script.json 해당 구간. 앞 장면의 곡선·성분·온도 축을 이어받고 끝에는 다음 의미 전환을 위한 동일 곡선을 유지. 하단 자막 전용 영역. 독립 렌더·교체 가능.\n',encoding='utf-8')
(HERE/'brief.md').write_text('# 제작 기준\n\n확정 34문장·175초·13개 독립 씬. 9:16 1080×1920 60fps, 음원 미제공으로 무음·전체 자막. 사용자 발화시간 유지, 추가 내레이션 없음. 기존 QCS 공통 자막·타이밍·도형과 hash 검증 빌더 재사용.\n\n'+ '\n\n'.join(details)+'\n\n수학 출처: https://math.mit.edu/~gs/cse/websections/cse41.pdf\nAI 사례: https://bmild.github.io/fourfeat/\n',encoding='utf-8')
(HERE/'README.md').write_text('# 사인과 코사인 · 푸리에 급수\n\n175초·1080×1920·60fps·무음·전체 자막. 확정 대본과 문장 경계: narration.md, script.json.\n\n최종 렌더: `py -3.12 scripts/render.py basis01`\n\n대표 씬: `py -3.12 episodes/basis01_fourier_heat/build.py --preview --scene 05 08 09 10`\n\n열 모델은 L=π, α=.18, 양끝 기준 온도 고정. u=T−Tref, u(0,t)=u(π,t)=0. 사인 모드 진폭의 지수 감쇠를 정확히 계산. 일반 푸리에 급수와 세 성분 예시 구별. 기저의 비유일성 표기.\n',encoding='utf-8')
if not (HERE/'build.py').exists():
    b=(ROOT/'episodes/godel01_proof_limits/build.py').read_text(encoding='utf-8').replace('godel01','basis01').replace("'41 exact user-supplied sentence ends; 10 scenes; no gaps or overlaps'","'34 exact user-supplied sentence ends; 13 scenes; no gaps or overlaps'")
    (HERE/'build.py').write_text(b,encoding='utf-8')
print('Prepared',len(sentences),'sentences,',start,'seconds')
