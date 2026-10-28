import json
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''이번에는 빛의 이동 시간에서 나타나는 자연의 최적화를 살펴보겠습니다.|4
공기 중에서 물을 향해 빛을 비추면, 빛은 경계면에서 방향이 꺾입니다.|9
이것을 굴절이라고 합니다.|10
그런데 이 현상에는 흥미로운 수학적 성질이 숨어 있습니다.|14
빛의 출발점과 물속의 한 지점을 선택해 보겠습니다.|17
두 지점 사이의 가장 짧은 경로는 직선입니다.|20
하지만 실제 빛은 경계면에서 꺾인 경로를 지나갑니다.|23
그 이유는 빛의 속력이 매질에 따라 다르기 때문입니다.|27
빛은 공기보다 물속에서 더 느리게 이동합니다.|30
따라서 공기에서 조금 더 먼 거리를 이동하더라도, 물속의 거리를 줄이면 전체 이동 시간이 짧아질 수 있습니다.|37
즉, 중요한 것은 이동 거리가 아니라 이동 시간입니다.|40
그렇다면 빛은 어떻게 이 경로를 찾아낸 걸까요?|43
가능한 모든 경로를 계산한 걸까요?|45
물론 아닙니다.|46
빛은 특정한 도착점을 미리 알고 움직이지 않습니다.|50
광원에서 나온 빛이 전파된 후, 우리는 그중 한 지점에 도달하는 경로를 선택해 분석하는 것입니다.|56
그렇다면 실제 굴절은 어떻게 일어날까요?|59
이번에는 빛을 광선이 아니라 파동으로 생각해 보겠습니다.|63
빛의 파면이 공기와 물의 경계에 비스듬하게 도달합니다.|67
파면의 한쪽이 먼저 물속으로 들어가면 그 부분은 느리게 진행하고, 아직 공기 중에 있는 부분은 더 빠르게 이동합니다.|74
이러한 속도 차이로 파면의 방향이 바뀌고, 빛의 진행 방향도 꺾입니다.|78
빛은 목적지를 알 필요 없이, 현재 위치의 매질에 따라 전파될 뿐입니다.|83
그런데 이렇게 만들어진 경로를 전체적으로 살펴보면 특별한 조건이 나타납니다.|88
출발점과 도착점을 고정하고, 경계면을 통과하는 위치를 조금씩 바꾸어 보겠습니다.|93
통과 위치에 따라 전체 이동 시간이 달라집니다.|96
그런데 실제 광선의 경로에서는 이동 시간의 일차 변화량이 0이 됩니다.|101
이것이 페르마의 원리입니다.|103
이 조건을 수학적으로 정리하면 입사각과 굴절각의 관계인 스넬 법칙이 나타납니다.|108
여기서 파동의 간섭을 살펴보면 한 단계 더 이해할 수 있습니다.|112
서로 다른 경로에 대응하는 파동들은 이동 시간에 따라 위상이 달라집니다.|117
경로가 조금 바뀔 때 위상이 크게 달라지면 파동의 기여가 서로 상쇄되기 쉽습니다.|122
반면 이동 시간이 정지하는 경로 근처에서는 위상 변화가 작아, 그 주변의 기여가 두드러질 수 있습니다.|128
빛은 전체 이동 시간을 미리 계산하지 않습니다.|131
파동은 각 위치의 물리적 조건에 따라 전파될 뿐입니다.|135
하지만 우리가 전체 경로를 수학적으로 분석하면, 이동 시간에 대한 최적화 조건이 나타납니다.|141
자연이 미래의 목적지를 알고 움직이는 것이 아니라, 국소적인 물리법칙의 결과를 전체적인 수학적 원리로도 표현할 수 있는 것입니다.|149'''
BOUNDS=[0,4,10,17,23,30,40,46,56,59,67,74,78,83,88,96,103,108,117,128,135,141,149]
TITLES=['물속으로 전파되는 빛','경계에서 방향이 꺾인다','전파한 뒤 관찰점을 선택한다','가장 짧은 거리와 실제 광선','같은 시간 · 다른 이동 거리','거리보다 중요한 이동 시간','만약 모든 경로를 계산한다면?','빛의 전파가 먼저다','광선에서 파면으로','비스듬히 도착하는 파면','먼저 물에 들어간 부분은 더 느리게','파면이 바뀌면 진행 방향도 바뀐다','목적지 없이 계속 전파된다','물리적 전파 → 수학적 경로 분석','통과점 C를 조금씩 바꾸면','실제 경로에서 시간의 일차 변화가 0','페르마의 원리에서 스넬 법칙으로','서로 다른 시간 · 서로 다른 위상','정지시간 근처에서는 위상이 모인다','물리적 전파와 수학적 해석','두 관점이 같은 굴절 경로를 준다','국소적인 법칙 · 전체적인 조건']
CLAIMS=['광원에서 여러 방향으로 전파한다. B를 먼저 표시하지 않는다.','이미 전파한 광선 중 하나와 법선·굴절각을 관찰한다.','관찰점 B는 전파 이후 14초부터 선택해 표시한다.','거리 수치는 동일 A·B에서 계산하며 직선은 가상 비교 경로다.','비분산 이상화에서 상대 위상속력 1:.75를 같은 시간 동안 비교한다.','동일한 A·B와 실제 구간 길이로 두 경로의 시간을 계산한다.','전체 탐색은 실제 물리 과정이 아닌 사고실험으로 표시한다.','B 없이 전파한 뒤 B를 선택하는 순서를 다시 보여준다.','파면은 같은 위상의 면이고 진행 방향에 수직이다.','국소 평면파 모형의 위상 등위면을 3D 패치로 표시한다.','주파수·접선 파수 연속과 서로 다른 위상속력으로 계산한다.','파면 법선과 광선 방향이 같은 굴절각을 갖는다.','B 없이 파면 전파를 먼저 보여준 뒤 선택점을 다시 표시한다.','실제 시간에 따른 전파와 후보 경로 비교를 분리한다.','C와 T(x)를 하나의 변수로 동기화하며 A·B는 고정한다.','이 설정에서는 최소시간이며 일반 페르마 원리는 정지 조건이다.','각도는 경계의 법선 기준이다.','동일 진폭의 수학적 위상 기여 모형이며 광선 경쟁 과정이 아니다.','같은 폭의 경로 표본·주파수로 비교하며 다른 기여가 정확히 0이라고 하지 않는다.','파면의 국소 전파와 경로 전체 조건을 나란히 관찰한다.','파면으로 계산한 방향과 정지시간 경로를 정확히 겹친다.','사용자 콘티의 세 현상 비교로 결론을 맺으며 다음 편 예고는 없다.']
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    rows=[];s=0
    for line in RAW.splitlines():
        text,e=line.rsplit('|',1);e=int(e);rows.append(dict(start=s,end=e,caption=text));s=e
    assert s==149
    (P/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["caption"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
    manifest=[];narr=[];tts=[]
    for i,(s,e,title,claim) in enumerate(zip(BOUNDS,BOUNDS[1:],TITLES,CLAIMS)):
        d=P/'scenes'/f'{i+1:02}_sequence';d.mkdir(parents=True,exist_ok=True);script='\n'.join(r['caption'] for r in rows if s<=r['start']<e);tts.append(script)
        (d/'script.txt').write_text(script+'\n',encoding='utf-8');(d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import LightBase\nclass LightShot(LightBase):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=f'scenes/{d.name}',start=s,end=e,duration_seconds=e-s,title=title,**{'class':'LightShot'}))
        (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n## 목적·핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('없음' if i==0 else TITLES[i-1])+f'\n\n## TTS와 확정 길이\n사용자 구간 {s}–{e}초, {e-s}초. timing.json의 원문·문장 종료 시각을 따른다. 음원 미제공.\n\n{script}\n\n## 화면·애니메이션\nreference/storyboard.txt 시퀀스 {i+1:02}, visuals.py INDEX={i}. 진입 약 0~0.5초, 구간 중간에 대상의 전파·비교·변화, 마지막에 결론 상태 유지. 애니메이션 실제 합계는 코드가 확정 길이 초과를 검사한다.\n\n## 화면 텍스트\n{title}. 물리 수치와 함수는 physics.py, 자막은 사용자 원문이다.\n\n## 시작·종료 상태\n동일한 매질과 좌표로 독립 구성하고 관찰 또는 분석 결과로 종료한다.\n\n## 다음 시각적 연결\n'+(TITLES[i+1] if i<21 else '세 현상과 국소 법칙의 결론. 다음 편 예고 없음.')+f'\n\n## 조건·정확성\n{claim}\n정지·균일·등방성·비분산 매질의 이상화. 반사와 진폭 전달 계수는 생략한다. 위상합은 기하광학의 정지위상 직관이며 완전한 장 적분이나 입자의 경로 탐색으로 제시하지 않는다.\n',encoding='utf-8')
        narr.append(f'## {i+1:02} · {s}–{e}초 · {title}\n\n{script}\n')
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    for f in ['master_script.md','narration.md']:(P/f).write_text('# 자연의 최적화 03 — 사용자 대본·종료 시각\n\n'+'\n'.join(narr),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
    y='id: nature03_refraction\ntitle: 빛은 목적지를 모르는데 어떻게 최단시간 경로가 나타날까?\nvideo:\n  fps: 30\n  layouts:\n    shorts: [1080, 1920]\n    longform: [1920, 1080]\nscenes:\n'
    for m in manifest:y+=f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: LightShot\n    duration_seconds: {m["duration_seconds"]}\n    transition: cut\n'
    (P/'scenes.yaml').write_text(y,encoding='utf-8')
if __name__=='__main__':main()
