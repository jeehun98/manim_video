"""Save the user's final script, actual sentence clocks, and scene specifications."""
import json,re,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''내적을 이용하면 벡터가 특정 방향으로 얼마나 뻗어 있는지 숫자 하나로 측정할 수 있습니다.|5
그렇다면 이 숫자를 이용해 원래 벡터에서 특정 방향의 성분만 꺼낼 수도 있을까요?|11
가로로 4, 세로로 2만큼 향하는 벡터를 생각해 보겠습니다.|14
이번에는 이 벡터에서 45도 대각선 방향의 성분만 추출해 보겠습니다.|19
먼저 기준 방향을 나타내는 단위벡터가 필요합니다.|22
45도 방향의 단위벡터는 가로와 세로 성분이 모두 1 나누기 루트 2입니다.|27
이제 원래 벡터와 이 단위벡터를 내적해 보겠습니다.|30
4 곱하기 1 나누기 루트 2, 더하기 2 곱하기 1 나누기 루트 2.|35
계산하면 3 루트 2, 약 4.24가 나옵니다.|38
이 숫자는 원래 벡터가 45도 방향으로 얼마나 뻗어 있는지를 나타냅니다.|43
그런데 우리가 구하려는 것은 숫자 하나가 아니라, 실제로 그 방향을 향하는 벡터입니다.|48
어떻게 하면 될까요?|49
앞서 사용한 단위벡터는 길이가 1이고, 우리가 원하는 방향을 가리키고 있습니다.|54
따라서 내적으로 구한 3 루트 2를 이 단위벡터에 곱하면 됩니다.|58
계산하면 가로 성분은 3, 세로 성분도 3이 됩니다.|62
원래 벡터는 4, 2였지만, 대각선 방향의 성분만 추출한 결과는 3, 3입니다.|66
이것을 정사영, 영어로 Orthogonal Projection이라고 합니다.|71
원래 벡터의 끝점에서 기준 직선으로 수선을 내렸을 때, 그 수선의 발까지 향하는 벡터가 바로 정사영 벡터입니다.|78
이 과정을 다시 살펴보겠습니다.|80
먼저 내적으로 특정 방향의 성분을 숫자로 측정합니다.|84
그리고 그 숫자를 기준 단위벡터에 곱해, 실제 공간에서 해당 방향의 벡터로 만듭니다.|89
즉, 내적이 방향 성분의 크기를 측정하는 연산이라면, 정사영은 그 성분을 벡터로 추출하는 연산입니다.|96
이렇게 우리는 내적 하나를 이용해 원래 벡터에서 원하는 방향의 성분만 분리할 수 있습니다.|101'''
CUTS=[
    (0,11,'숫자에서 벡터로','내적값으로 특정 방향의 벡터를 추출할 수 있는가?', '0–5초 내적은 숫자 하나임을 표시. 5–11초 숫자→화살표 질문. 답 3√2는 아직 공개하지 않는다.'),
    (11,19,'45° 방향의 성분을 꺼내려면','고정 벡터 x=(4,2)에서 대각선 방향의 성분을 찾는다.', '11–14초 가로4·세로2의 좌표 보조선. 14–19초 원점을 지나는45° 기준선과 각 표시.'),
    (19,27,'45° 방향 · 길이 1','u=(1/√2,1/√2)는 45도 방향의 단위벡터다.', '19–22초 실제 길이1인 초록 화살표 등장. 22–27초 같은 가로·세로 성분과 길이 확인식.'),
    (27,38,'내적을 계산하면','내적은 6/√2=3√2≈4.24다.', '27–30초 두 벡터 좌표. 30–35초 대응 원소끼리 곱한 두 항을 색으로 연결. 35–38초 최종 스칼라 공개. 아직 정사영 화살표는 없다.'),
    (38,49,'길이를 읽었다면, 방향은?','스칼라와 방향을 가진 벡터는 구별된다.', '38–43초 주황 측정 구간 길이3√2. 43–48초 스칼라3√2와 벡터(?,?) 대비. 48–49초 방향을 결합하는 질문.'),
    (49,62,'측정값 × 단위벡터','길이1인 기준 방향에 내적값을 곱하면 p=(3,3)이다.', '49–54초 초록 u의 길이1·45° 확인. 54–58초 별도 복제 화살표가1→3√2배로 자라며 초록→주황. 58–62초 좌표별 약분 결과3,3과 끝점 확정. 초록 원본u는 고정한다.'),
    (62,78,'정사영 · Orthogonal Projection','계산한(3,3)은 원래 끝점에서 기준선에 내린 수선의 발이다.', '62–66초 x=(4,2)와p=(3,3) 동시 표시. 66–71초 정사영 명칭. 71–78초 (4,2)→(3,3) 수선, 발의 점과90° 기호. 직교성 계산 보조.'),
    (78,89,'측정하고, 방향을 곱한다','숫자를 읽고 같은 방향으로 벡터를 재구성한다.', '78–80초 보조선 정리. 80–84초 STEP01 내적→숫자. 84–89초 STEP02 숫자×단위벡터→p를 같은 좌표계에 재구성.'),
    (89,101,'내적으로 측정하고, 벡터로 추출한다','proj_u(x)=(x·u)u, 단 u는 단위벡터다.', '89–96초 내적 스칼라와 정사영 벡터 비교. 96–101초 최종 공식 하나와 파란x·초록u·주황p. 다음 편 예고 없이 종료.'),
]
def spoken(s):
    s=s.replace('Orthogonal Projection','오쏘거널 프로젝션')
    words={'45':'사십오','4.24':'사 점 이사','0':'영','1':'일','2':'이','3':'삼','4':'사'}
    return re.sub(r'\d+(?:\.\d+)?',lambda m:words.get(m[0],m[0]),s)
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    cues=[];start=0
    for row in RAW.splitlines():
        caption,end=row.rsplit('|',1);end=int(end);cues.append(dict(start=start,end=end,caption=caption));start=end
    assert len(cues)==23 and start==101
    (P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    script='\n\n'.join('\n'.join(c['caption'] for c in cues if s<=c['start']<e) for s,e,*_ in CUTS)+'\n'
    (P/'tts_script.txt').write_text(spoken(script),encoding='utf-8')
    (P/'master_script.md').write_text('# Dot Pro LEVEL 02 — 정사영\n\n사용자 제공 확정 원고와23개 문장 종료 시각. 총101초.\n\n'+script,encoding='utf-8')
    (P/'narration.md').write_text('# 문장별 내레이션 · 사용자 제공 실제 종료 시각\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n{c["caption"]}' for c in cues)+'\n',encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    manifest=[]
    for i,(s,e,title,claim,animation) in enumerate(CUTS):
        directory=f'scenes/{i+1:02}_scene';d=P/directory
        shutil.copytree(P.parent/'_template/scenes/01_example',d,dirs_exist_ok=True)
        original='\n'.join(c['caption'] for c in cues if s<=c['start']<e)
        (d/'script.txt').write_text(spoken(original)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('없음. 본편의 문제 제기로 독립적으로 시작한다.' if i==0 else CUTS[i-1][3])+f'\n\n## TTS 원문과 확정 길이\n사용자 제공 종료 시각 기준{s}–{e}초, {e-s}초. 음원 미제공.\n\n{original}\n\n## 화면 구성\n고정 좌표계. 세로형 상단 개념·중앙 그래프·하단 계산, 가로형 좌측 그래프·우측 계산. 자막은 별도 하단 영역. x=(4,2) 파란색, u 초록색, 측정값과p 주황색.\n\n## 시간대별 애니메이션과 화면 텍스트\n{animation}\n\n## 시작·종료 상태\n원점과 좌표 스케일은 전체 편에서 고정. 앞 컷의 의미를 이어받고, 이 컷의 계산 결과를 다음 컷의 시작 대상으로 사용한다. 컷 사이에 모호한 방향 변경이나 좌표계 이동 없음.\n\n## 다음 연결\n'+(CUTS[i+1][3] if i+1<len(CUTS) else '본편의 질문과 결론으로 완결한다.')+'\n\n## 정확성 조건\n실수 유클리드 내적. u=(1/√2,1/√2), ‖u‖=1. x·u=3√2. p=(x·u)u=(3,3). x−p=(1,−1), (x−p)·u=0. 수선은(4,2)에서(3,3). 측정 구간은 화살촉 없는 선분, 추출한 벡터는 화살표로 구분한다. 실제 길이비 p:u=3√2:1.\n',encoding='utf-8')
        (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ProjectionBase\nclass Projection{i+1:02}(ProjectionBase):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=directory,start=s,end=e,duration_seconds=e-s,title=title,**{'class':f'Projection{i+1:02}'}))
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('duration_seconds: 101\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    (P/'brief.md').write_text('# Dot Pro LEVEL 02 — 제작 기준\n\n## 목표\n내적값이 실제 방향벡터로 재구성되는 과정을 이해한다. 내적은 측정, 정사영은 추출.\n\n## 제작 범위\n사용자 확정 원고와 실제 문장 종료 시각23개, 101초. 9:16 1080×1920 쇼츠와16:9 1920×1080 롱폼, 각각30fps. 음원 미제공으로 무음 자막 영상. 영상 길이를 임의로 늘리지 않는다. 9개 독립 씬으로 교체 가능.\n\n## 핵심 조건\nx=(4,2)와 원점·좌표 스케일 고정. u=(1/√2,1/√2), 실제 길이1. 스칼라3√2는35초에 공개. p=(3,3)은58초에 좌표 공개. 54–58초 숫자 곱셈과 화살표 길이 증가를 동기화. 초록u 원본은 유지하고 복제한 화살표를 주황p로 확대. 71–78초 수선과 직각 표시. 마지막 공식은 단위벡터 조건과 함께 표시.\n\n## 서사\n사용자 원문은 그대로 사용한다. 이전 편을 언급하는 복습·다음 편 예고는 추가하지 않는다. 78–89초는 본편에서 수행한 두 연산의 결합이다.\n\n## 시각 구분\n파란 원래벡터 / 초록 기준 방향 / 주황 스칼라와정사영 / 회색 수선. 선분은 측정 구간, 화살표는 벡터.\n',encoding='utf-8')
if __name__=='__main__':main()
