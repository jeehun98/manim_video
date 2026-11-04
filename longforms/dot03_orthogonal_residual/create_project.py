"""Preserve user narration and actual sentence clocks before visual production."""
import json,re,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''하나의 벡터에서 원하는 방향의 성분만 완전히 제거할 수 있을까요?|4
앞서 살펴본 정사영을 이용하면 가능합니다.|7
가로로 4, 세로로 2만큼 향하는 벡터를 생각해 보겠습니다.|10
이번에는 이 벡터에서 45도 대각선 방향의 성분만 제거해 보겠습니다.|15
먼저 해당 방향의 성분을 구해야 합니다.|17
45도 방향의 단위벡터는 가로와 세로 성분이 모두 1 나누기 루트 2입니다.|23
원래 벡터와 이 단위벡터를 내적하면 3 루트 2가 나옵니다.|26
이 값에 다시 단위벡터를 곱하면, 가로로 3, 세로로 3만큼 향하는 정사영 벡터를 얻습니다.|33
이제 원래 벡터에서 이 정사영 벡터를 빼보겠습니다.|36
가로 성분은 4 빼기 3으로 1.|38
세로 성분은 2 빼기 3으로 음수 1입니다.|40
결과는 가로로 1, 세로로 음수 1만큼 향하는 벡터입니다.|44
그런데 정말 45도 방향의 성분이 완전히 제거된 걸까요?|49
이를 확인하기 위해 남은 벡터와 기준 방향을 다시 내적해 보겠습니다.|53
계산을 간단하게 하기 위해, 같은 45도 방향을 향하는 벡터 1, 1을 사용하겠습니다.|58
1 곱하기 1, 더하기 음수 1 곱하기 1.|61
결과는 0입니다.|62
내적이 0이라는 것은 두 벡터가 서로 직교한다는 뜻입니다.|65
즉, 남은 벡터에는 45도 방향으로 측정되는 성분이 전혀 없습니다.|70
이것은 우연이 아닙니다.|71
정사영은 원래 벡터에서 기준 방향과 나란한 성분만 추출합니다.|76
따라서 그 성분을 빼면 기준 방향과 직교하는 부분만 남게 됩니다.|80
이렇게 남은 벡터를 잔차, 영어로 Residual이라고 합니다.|83
결국 하나의 벡터는 기준 방향과 나란한 성분, 그리고 그 방향과 직교하는 성분으로 나눌 수 있습니다.|89
그리고 이 두 성분을 다시 더하면 원래 벡터가 됩니다.|93
내적을 이용해 방향을 측정하고, 정사영으로 추출한 뒤, 그 성분을 제거하면 원하는 방향과 직교하는 성분만 남길 수 있습니다.|101'''
CUTS=[
 (0,15,'원하는 방향만 제거할 수 있을까?','정사영을 이용해 제거할 방향의 성분을 선택한다.','0–4초 파란 x와 제거할 방향 질문. 4–7초 주황 p 암시. 7–10초 가로4·세로2. 10–15초 초록45° 기준선 강조. 잔차는 공개하지 않는다.'),
 (15,33,'제거할 성분을 먼저 추출한다','u에 투영해 p=(3,3)을 얻는다.','15–17초 초록 단위벡터 등장. 17–23초 u=(1/√2,1/√2), 길이1. 23–26초 내적3√2. 26–33초 복제한 기준벡터를 확대해 주황 p=(3,3) 생성. 원본u는 유지.'),
 (33,44,'정사영을 빼면 무엇이 남을까?','잔차 r=x−p=(1,−1)은 두 끝점 사이의 차이다.','33–36초 x−p. 36–38초 가로4−3=1. 38–40초 세로2−3=−1. 40–44초 p의 끝점(3,3)에서 x의 끝점(4,2)으로 보라 화살표를 그린다.'),
 (44,62,'성분이 사라졌는지 다시 측정한다','r·(1,1)=1−1=0으로 제거 여부를 확인한다.','44–49초 보라 r을 원점으로 평행이동, 길이와 방향 유지. x,p는 어둡게. 49–53초 초록 기준 방향. 53–58초 계산용 v=(1,1), 단위벡터가 아님을 명시. 58–61초 +1과−1이 합쳐짐. 61–62초0 강조.'),
 (62,71,'다시 측정했을 때 0','잔차와 기준은 직교하며 해당 방향의 투영은0이다.','62–65초 원점에서r과u가90°임을 표시. 65–70초 r끝점에서 기준선에 내린 수선의 발은원점. 주황 측정 표시는 정확히 원점의 점이며 길이0으로 표시. 70–71초 우연이 아님을 제시.'),
 (71,83,'나란한 성분을 빼면, 직교 성분','잔차는 선택한 방향으로 설명되지 않는 성분이다.','71–76초 주황p가 초록u와 나란함을 관찰. 76–80초p를 제거하고r을 원점에 평행이동. 80–83초 Residual·잔차 명칭.'),
 (83,93,'두 성분을 더하면 원래 벡터','x=p+r은 평행 성분과 직교 성분의 분해다.','83–89초 p와r을 원점에서 구별하고 이름 표시. 89–93초r을p끝점으로 옮겨 연결하면 x끝점(4,2)에 도착한다. x는 움직이지 않는다.'),
 (93,101,'측정 → 추출 → 제거','r=x−(x·u)u이며r·u=0이다.','93–95초 내적x·u. 95–97초 정사영(x·u)u. 97–99초 제거r=x−(x·u)u. 99–101초 보라r·초록u와 직각, 단위벡터 조건을 남긴다. 예고 없이 종료.'),
]
def spoken(s):
    s=s.replace('Residual','리지듀얼')
    words={'45':'사십오','0':'영','1':'일','2':'이','3':'삼','4':'사'}
    return re.sub(r'\d+',lambda m:words.get(m[0],m[0]),s)
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    cues=[];start=0
    for row in RAW.splitlines():
        caption,end=row.rsplit('|',1);end=int(end);cues.append(dict(start=start,end=end,caption=caption));start=end
    assert len(cues)==26 and start==101
    (P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    script='\n\n'.join('\n'.join(c['caption'] for c in cues if s<=c['start']<e) for s,e,*_ in CUTS)+'\n'
    (P/'master_script.md').write_text('# 내적 LEVEL 03 — 방향 성분 제거와 직교 잔차\n\n사용자 제공 확정 원고·26개 문장 종료 시각, 총101초. 사용자 원문의 “앞서 살펴본” 문장은 그대로 사용하며 추가 복습·예고는 넣지 않는다.\n\n'+script,encoding='utf-8')
    (P/'tts_script.txt').write_text(spoken(script),encoding='utf-8')
    (P/'narration.md').write_text('# 문장별 내레이션\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n{c["caption"]}' for c in cues)+'\n',encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    manifest=[]
    for i,(s,e,title,claim,animation) in enumerate(CUTS):
        directory=f'scenes/{i+1:02}_scene';d=P/directory;shutil.copytree(P.parent/'_template/scenes/01_example',d,dirs_exist_ok=True)
        original='\n'.join(c['caption'] for c in cues if s<=c['start']<e)
        (d/'script.txt').write_text(spoken(original)+'\n',encoding='utf-8')
        spec=f'# {i+1:02} — {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('없음. 문제 제기로 시작한다.' if i==0 else CUTS[i-1][3])+f'\n\n## TTS와 확정 길이\n사용자 제공 문장 종료 시각 기준{s}–{e}초, 길이{e-s}초. 음원 미제공.\n\n{original}\n\n## 화면 구성\n2편과 같은 원점·스케일. x=(4,2) 파랑, u 초록, p=(3,3) 주황, r=(1,−1) 보라. 세로형 중앙 그래프·하단 계산, 가로형 좌측 그래프·우측 계산. 하단 자막 영역은 분리한다.\n\n## 구간별 애니메이션·화면 텍스트\n{animation}\n\n## 시작·종료 상태\n파란x는 위치를 고정하고 강조가 필요할 때 밝기만 바꾼다. 처음 보라잔차는p끝점에서x끝점으로 등장한다. 다음 컷에서 원점으로 옮길 때는 회전·크기 변경 없이 평행이동한다.\n\n## 다음 장면 연결\n'+(CUTS[i+1][3] if i+1<len(CUTS) else '본편의 결론으로 완결한다.')+'\n\n## 수학적 조건\n유클리드 내적, u=(1/√2,1/√2), ‖u‖=1. p=(x·u)u=(3,3). r=x−p=(1,−1). r·u=0, r·(1,1)=0. v=(1,1)의 길이는√2이며 직교 검사에 사용한다. p+r=x. 잔차 평행이동 전후 방향과길이는 동일. 주황 투영0은 실제 점으로 표시하며 양의 길이를 가진 선분을 그리지 않는다.\n'
        (d/'spec.md').write_text(spec,encoding='utf-8')
        (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ResidualBase\nclass Residual{i+1:02}(ResidualBase):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=directory,start=s,end=e,duration_seconds=e-s,title=title,**{'class':f'Residual{i+1:02}'}))
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('duration_seconds: 101\ntiming_source: user_sentence_end_times\nlayouts:\n  shorts: [1080, 1920, 30]\n  longform: [1920, 1080, 30]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    (P/'brief.md').write_text('# 내적 LEVEL 03 — 제작 기준\n\n## 목표\n정사영을 빼서 얻은 잔차가 기준 방향과 직교함을 계산과 그림으로 검증한다.\n\n## 확정 범위\n사용자 원고·실제 문장 종료 시각26개, 101초. 9:16 쇼츠1080×1920와16:9 롱폼1920×1080, 30fps. 음원 미제공으로 무음·자막. 8개 독립 씬. 추정 타이밍이나 길이 연장 없음.\n\n## 핵심 연출\n40–44초 r은 p=(3,3)에서 x=(4,2)로 먼저 등장. 44–49초 원점으로 평행이동. 53–58초 검사벡터v=(1,1)는 단위벡터u와 구별하고 길이1일 필요가 없는 직교 검사임을 표시. 58–62초 +1,−1→0. 65–70초 잔차의 기준방향 투영은 원점의 점. 89–93초p+r=x를 이어붙여 복원.\n\n## 시각·정확성\nx파랑, u초록, p주황, r보라. 원점과스케일은 2편과 동일하고 x는 움직이지 않는다. r의 이동은 방향·길이를 보존한다. 최종 제거 공식은 ‖u‖=1 조건과 표시. 사용자 원문의 “앞서 살펴본”은 보존하고, 추가 복습·예고는 넣지 않는다.\n',encoding='utf-8')
if __name__=='__main__':main()
