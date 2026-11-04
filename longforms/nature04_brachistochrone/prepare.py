import json
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''이번에는 중력 아래에서 이동 시간을 최소화하는 최적화 문제를 살펴보겠습니다.|4
높이가 다른 두 지점을 연결하는 미끄럼틀을 생각해 보겠습니다.|8
마찰이 없고, 물체를 정지 상태에서 놓는다고 가정하겠습니다.|12
두 지점 사이의 가장 짧은 경로는 직선입니다.|15
그런데 직선이 가장 빠른 경로는 아닙니다.|18
처음에 가파르게 내려갔다가 완만해지는 곡선에서는 물체가 초반부터 빠르게 가속할 수 있습니다.|23
이후에는 이미 얻은 속력으로 나머지 구간을 이동합니다.|27
물론 지나치게 깊이 내려가면 이동 거리가 길어져 오히려 시간이 늘어날 수 있습니다.|32
따라서 이동 거리와 속력의 변화를 함께 고려해야 합니다.|35
그렇다면 어떤 곡선이 전체 이동 시간을 최소화할까요?|39
먼저 물체가 얼마나 빠르게 움직이는지 알아보겠습니다.|41
마찰이 없다면 내려간 높이만큼 중력 위치에너지가 운동에너지로 바뀝니다.|47
따라서 물체의 속력은 지금까지 내려온 높이에 의해 결정됩니다.|51
같은 높이에 도달한 물체들은 서로 다른 경로를 지나왔더라도 속력이 같습니다.|56
하지만 그 높이에 도달하는 데 걸린 시간은 다를 수 있습니다.|60
이제 경로를 아주 작은 구간으로 나누어 보겠습니다.|63
각 구간의 이동 시간은 구간의 길이를 그곳에서의 속력으로 나눈 값입니다.|68
이 시간들을 전체 경로에 걸쳐 합하면 총 이동 시간을 구할 수 있습니다.|72
출발점과 도착점을 고정한 상태에서 이 시간을 최소화하는 곡선을 찾는 것입니다.|77
이 문제를 최속강하선 문제라고 합니다.|80
그리고 그 해는 놀랍게도 사이클로이드라는 곡선입니다.|84
원이 직선을 따라 굴러갈 때, 원 위의 한 점이 그리는 곡선입니다.|88
그런데 여기서 앞선 빛의 굴절과 흥미로운 연결이 나타납니다.|93
빛도 이동 시간을 경로의 작은 길이를 해당 위치의 속력으로 나누어 계산했습니다.|98
차이는 속력이 달라지는 이유입니다.|100
빛은 매질의 굴절률에 따라 속력이 달라지고, 물체는 중력에 의해 내려간 높이에 따라 속력이 달라집니다.|107
이제 공간을 아주 얇은 수평층으로 나누고, 깊이에 따라 빛의 속력이 점점 빨라지는 가상의 매질을 생각해 보겠습니다.|114
빛은 각 층의 경계에서 굴절하고, 층을 점점 얇게 만들면 경로가 연속적으로 휘어집니다.|120
이때 빛의 속력 분포를 중력 아래 물체의 속력과 같게 설정하면, 두 문제의 이동 시간 식도 같아집니다.|126
결국 빛의 굴절 법칙을 이용해 최속강하선을 구할 수도 있습니다.|130
서로 다른 물리현상이 같은 수학적 최적화 문제로 연결되는 것입니다.|135
하지만 중요한 차이가 있습니다.|137
빛은 매질을 따라 실제로 굴절하지만, 물체는 스스로 최적의 미끄럼틀을 만들지 않습니다.|142
물체는 주어진 트랙 위에서 중력과 접촉력에 따라 움직일 뿐입니다.|146
최적의 트랙을 찾는 것은 우리가 설정한 수학적 문제입니다.|150
이번에는 자연이 만들어낸 형태를 관찰하는 것을 넘어, 자연의 물리법칙을 이용해 가장 빠른 경로를 설계한 것입니다.|156
서로 다른 물리법칙에서도 같은 최적화 구조를 발견할 수 있다는 사실.|161
이것이 변분법이 물리학을 넘어 다양한 문제에 적용될 수 있는 이유 중 하나입니다.|165'''
BOUNDS=[0,4,12,18,27,35,39,47,56,60,68,77,80,84,88,93,100,107,114,120,126,130,135,142,150,156,165]
TITLES=['가장 빠른 길은 어떤 모양일까?','같은 출발점 · 같은 도착점','가장 짧다고 가장 빠르지는 않다','초반의 가속이 도착 시간을 바꾼다','깊게 내려가면 더 빠를까?','거리와 속력을 함께 비교한다','내려온 높이가 속력을 결정한다','같은 높이에서는 같은 속력','같은 속력 · 다른 도달 시간','작은 구간의 시간을 더한다','곡선 전체의 이동 시간','최속강하선 문제','정답은 사이클로이드','굴러가는 원이 그리는 곡선','중력과 빛의 흥미로운 연결','이동 시간을 구하는 같은 방법','속력이 달라지는 이유','깊을수록 빠른 가상의 매질','경계마다 굴절하는 광선','층을 얇게 만들면 곡선이 된다','같은 속력 분포를 설정한다','서로 다른 현상 · 같은 최적화','빛의 전파와 트랙의 설계','물체는 주어진 트랙을 따라간다','물리법칙을 이용해 경로를 설계한다','공통된 수학적 사고방식 · 변분법']
def main():
    rows=[];s=0
    for line in RAW.splitlines():
        t,e=line.rsplit('|',1);e=int(e);rows.append(dict(start=s,end=e,caption=t));s=e
    (P/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    stamp=lambda t:f'00:{t//60:02}:{t%60:02},000'
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["caption"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
    ms=[];narr=[];tts=[]
    for i,(s,e,title) in enumerate(zip(BOUNDS,BOUNDS[1:],TITLES)):
        d=P/'scenes'/f'{i+1:02}_sequence';d.mkdir(parents=True,exist_ok=True)
        script='\n'.join(r['caption'] for r in rows if s<=r['start']<e);tts.append(script)
        (d/'script.txt').write_text(script+'\n',encoding='utf-8')
        (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import BrachiBase\nclass BrachiShot(BrachiBase):\n    INDEX={i}\n',encoding='utf-8')
        ms.append(dict(id=f'{i+1:02}',directory=f'scenes/{d.name}',start=s,end=e,duration_seconds=e-s,title=title,**{'class':'BrachiShot'}))
        (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n## 주장\n{title}\n\n## 확정 대본·길이\n사용자 종료 시각 {s}–{e}초. 음원 미제공.\n\n{script}\n\n## 화면\n첨부 콘티 reference/storyboard.txt의 시퀀스 {i+1:02}. visuals.py INDEX={i}. 진입, 물리량 또는 후보 경로 비교, 결론 유지. 자막은 전체 원문 시각을 유지한다.\n\n## 조건\n균일 중력, 마찰 없는 점입자, 정지 출발, 같은 A·B. 깊이 y는 아래가 양수. 구슬은 위치 표식이며 구르는 강체가 아니다. 후보 비교는 물체가 스스로 트랙을 만드는 과정이 아니다. 가상 매질의 y=0은 극한이고 유한층은 중간 깊이 속력을 쓴다.\n\n## 시작·종료\n독립적으로 좌표와 대상 제시 → 해당 주장 관찰. 다음 편 예고 없음.\n',encoding='utf-8')
        narr.append(f'## {i+1:02} · {s}–{e}초 · {title}\n\n{script}\n')
    (P/'manifest.json').write_text(json.dumps(ms,ensure_ascii=False,indent=2),encoding='utf-8')
    for f in ['master_script.md','narration.md']:(P/f).write_text('# 자연의 최적화 04\n\n'+'\n'.join(narr),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
    (P/'scenes.yaml').write_text('id: nature04_brachistochrone\nvideo:\n  fps: 30\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: BrachiShot\n    duration_seconds: {m["duration_seconds"]}\n    transition: cut\n' for m in ms),encoding='utf-8')
    from physics import metrics
    (P/'geometry.json').write_text(json.dumps(metrics(),indent=2),encoding='utf-8')
if __name__=='__main__':main()
