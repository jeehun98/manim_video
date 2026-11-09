"""Preserve user-supplied narration and sentence end times."""
import json
import shutil
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
raw=(HERE/'narration_source.txt').read_text(encoding='utf-8').strip().splitlines()
lines=[x.strip() for x in raw if x.strip()]
sentences=[];start=0
for i in range(0,len(lines),2):
    end=int(lines[i+1]);assert end>start
    sentences.append(dict(start=start,end=end,text=lines[i]));start=end
assert start==175 and len(sentences)==41, (start,len(sentences))
cuts=[0,16,33,51,67,86,99,118,137,155,175]
titles=['AI의 증명, 누가 검사할까?','무한한 사례 대신 하나의 증명','검사에서 증명 탐색으로','문장과 증명에 번호를 붙이면','증명 검사를 산술로 표현한다','자기 자신의 증명을 말하는 문장','G의 증명이 있다고 가정하면','참과 증명 가능성의 차이','새로운 증명과 새로운 공리','하나의 체계가 닿을 수 있는 범위']
details=[
 'AI → 증명 카드 → 별도 검증기. 답과 풀이를 구별하고 13초부터 도입 질문.',
 'a,b는 정수. 2a+2b → 2(a+b). 정의·분배법칙·짝수 결론을 차례로 검사. 개별 예시는 일반 증명으로 대체.',
 '기호·공리·추론 규칙 → 체계 T. 유효/무효는 증명 후보의 형식 검사 결과이며 진리 판정이 아님. 빠짐없는 열거는 원리적 탐색.',
 '1931 괴델. 동일한 짝수 문장과 증명 카드를 재사용. s와 p는 부호화한 자연수의 기호이며 실제 번호값을 임의로 제시하지 않음.',
 '문장 s(파랑), 증명 p(초록). Proof(p,s)는 p가 s의 증명인지 검사하는 산술 관계. ∃p Proof(p,s) → Prov(s).',
 '대각화로 자기언급하도록 구성하는 중간 단계를 별도 표시. T ⊢ G ↔ ¬Prov(⌜G⌝). 단순 치환만으로 구성했다고 연출하지 않음.',
 '가정 T ⊢ G. 구체적인 증명 번호를 검사하여 T ⊢ Prov(⌜G⌝); G와 고정점 동치로 T ⊢ ¬Prov(⌜G⌝). 두 체계 내부 결론이 모순. 건전성을 일관성으로 대체하지 않음.',
 '일관성 아래 G의 표준 자연수 해석은 참이며 T에서 증명 불가. 128초 별도 화면에서 괴델–로서 정리: 충분한 산술·효과적 공리 열거·일관성. G 자체의 반증 불가로 직접 연결하지 않음.',
 '같은 T에서 미발견 증명을 찾는 일과 T에 공리를 추가하는 일을 분리. T′도 조건을 만족할 때 독립 명제가 존재. 새 공리 채택이 진리를 보장하지 않음.',
 '계산 속도와 체계의 증명 범위 구별. 마지막에도 효과적 공리 열거 조건 유지. 표준 자연수에서의 참과 T의 증명 가능성을 별도 카드로 표현하며 포함 집합 그림 금지. 마지막 1.5초 유지.'
]
scenes=[dict(id=f'{i+1:02}',**{'class':f'Shot{i+1:02}'},start=cuts[i],end=cuts[i+1],title=titles[i]) for i in range(10)]
data=dict(title='AI는 모든 수학적 진리를 증명할 수 있을까?',revision='v1_175s',duration=175,timing_source='사용자 제공 41개 문장 종료 시각',sentences=sentences,scenes=scenes)
(HERE/'script.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'timing.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
def wrap(s,n=26):
    out=[];line=''
    for w in s.split():
        if line and len(line)+len(w)+1>n:out.append(line);line=w
        else:line=(line+' '+w).strip()
    return '\n'.join(out+[line])
(HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
(HERE/'narration.md').write_text('# '+data['title']+'\n\n확정 대본·사용자 제공 종료 시각·175초·음원 미제공\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n',encoding='utf-8')
tts=[]
for s in sentences:
    t=s['text'].replace('2(a+b)','이 곱하기 괄호 에이 더하기 비').replace('2a','이 에이').replace('2b','이 비').replace('2의','이의').replace('1931년','천구백삼십일 년').replace('제1','제일').replace('G','지')
    tts.append(t)
(HERE/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
for i,s in enumerate(scenes):
    folder=HERE/'scenes'/s['id'];folder.mkdir(parents=True,exist_ok=True)
    (folder/'scene.py').write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom episodes.godel01_proof_limits.direction import GodelScene\n\nclass "+s['class']+'(GodelScene):\n    shot='+str(i)+'\n',encoding='utf-8')
    (folder/'spec.md').write_text(f"# {s['title']}\n\n{s['start']}–{s['end']}초 · {(s['end']-s['start'])*60}프레임\n\n{details[i]}\n\n대본: script.json의 해당 구간. 앞 씬의 증명·번호·G 카드를 계승. 시작은 본문 등장, 종료는 해당 주장 유지. 독립 렌더 가능. 하단 자막 영역 분리.\n",encoding='utf-8')
(HERE/'brief.md').write_text('# 제작 기준\n\n175초·41문장·10개 교체 가능 씬. 사용자 확정 대본을 수정하지 않음. 첨부 콘티의 170초 추정 대신 문장 종료 시각 적용. 9:16 1080×1920 60fps, 무음·전체 문장 자막. 공통 QCS 자막·타이밍·레이아웃과 기존 빌더 재사용. 가로 추가 산출물 없음.\n\n'+ '\n\n'.join(details)+'\n\n출처: https://plato.stanford.edu/entries/goedel-incompleteness/ ; https://lean-lang.org/doc/reference/latest/ValidatingProofs/\n',encoding='utf-8')
(HERE/'README.md').write_text('# AI는 모든 수학적 진리를 증명할 수 있을까?\n\n175초·1080×1920·60fps·무음·전체 자막. 확정 원문은 narration_source.txt, 문장별 경계는 script.json.\n\n실행: `py -3.12 scripts/render.py godel01`\n\n대표 씬 미리보기: `py -3.12 episodes/godel01_proof_limits/build.py --preview --scene 02 05 06 07 08`\n\n수학 검수: G의 증명 불가능성과 괴델–로서의 독립성 결론을 별도 화면으로 구별. 마지막 결론에도 효과적 공리 열거 조건 표시. 수학적 직관 영상이며 대각화의 완전한 증명은 생략.\n',encoding='utf-8')
if not (HERE/'build.py').exists():
    b=(ROOT/'episodes/idea01_common_structure/build.py').read_text(encoding='utf-8').replace('idea01_v1_136s','godel01_v1_175s').replace('idea01_','godel01_')
    (HERE/'build.py').write_text(b,encoding='utf-8')
print('Prepared',len(sentences),'sentences,',start,'seconds')
