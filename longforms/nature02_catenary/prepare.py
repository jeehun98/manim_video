"""Preserve the user's 35 sentences and exact end times."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''이번에는 중력 위치에너지를 최소화하는 자연의 최적화를 살펴보겠습니다.|4
사슬의 양쪽 끝을 고정하고 늘어뜨리면, 가운데가 처지는 곡선이 만들어집니다.|9
그런데 이 곡선은 주어진 조건에서 전체 중력 위치에너지가 최소인 형태입니다.|14
이처럼 정해진 조건을 지키면서 어떤 값을 최소화하는 것을 제약조건하에서의 최적화라고 합니다.|20
그렇다면 사슬은 어떻게 이 형태를 찾아낸 걸까요?|23
사슬의 아주 작은 부분 하나를 살펴보겠습니다.|26
이 부분에는 아래로 작용하는 중력과, 양옆의 사슬이 당기는 장력이 작용합니다.|31
힘의 균형이 맞지 않으면 이 부분은 움직이고, 연결된 다른 부분의 위치와 장력도 달라집니다.|37
이러한 변화가 이웃한 부분으로 전달되면서 사슬 전체의 형태가 변합니다.|42
하지만 양쪽 끝의 위치와 전체 길이는 고정되어 있습니다.|45
따라서 한 부분이 아래로 내려가면 다른 부분의 위치도 함께 변해야 합니다.|50
높이가 낮아질수록 중력 위치에너지는 감소하지만, 한 부분의 에너지가 줄어든다고 전체 에너지가 반드시 감소하는 것은 아닙니다.|57
실제 사슬은 중력과 장력에 따라 움직이고, 진동과 마찰을 거쳐 안정된 평형에 도달합니다.|63
이제 움직임이 멈춘 사슬을 살펴보겠습니다.|66
모든 부분에서 중력과 장력이 균형을 이루고 있습니다.|69
이때 장력의 수평 성분은 일정하지만, 수직 성분은 중심에서 멀어질수록 커집니다.|75
그에 따라 사슬의 기울기도 점점 가팔라집니다.|78
이러한 힘의 균형을 수학적으로 정리하면 특별한 곡선이 나타납니다.|81
바로 현수선, 카테너리입니다.|84
포물선처럼 보이지만, 쌍곡코사인 함수로 표현되는 곡선입니다.|88
그런데 이 곡선은 다른 방법으로도 구할 수 있습니다.|91
양쪽 끝과 전체 길이를 고정한 여러 곡선의 중력 위치에너지를 비교하는 것입니다.|96
그중 전체 에너지가 최소인 곡선을 구하면, 동일한 현수선이 나타납니다.|100
하나는 각 부분의 힘의 균형에서, 다른 하나는 전체 에너지의 최소화에서 출발했지만 같은 결과에 도달한 것입니다.|107
사슬의 각 부분은 전체 에너지를 계산하지 않습니다.|110
그저 중력과 주변의 장력에 반응할 뿐입니다.|114
하지만 각 부분의 상호작용이 연결되면서 전체적으로는 에너지가 최소인 구조가 형성됩니다.|120
그런데 여기서 한 가지 더 흥미로운 사실이 있습니다.|123
이 현수선을 중심축 주위로 회전시키면 하나의 3차원 곡면이 만들어집니다.|128
바로 카테노이드입니다.|129
앞서 비눗막에서 발견했던 최소곡면입니다.|132
비눗막은 표면에너지를, 사슬은 중력 위치에너지를 줄입니다.|136
서로 다른 최적화 문제인데도 동일한 쌍곡코사인 함수가 등장하는 것입니다.|140
자연은 최적의 형태를 미리 계산하지 않습니다.|143
각 부분이 현재의 물리적 조건에 반응할 뿐이지만, 그 결과에서 우리는 전체적인 최적화의 구조를 발견할 수 있습니다.|150'''
BOUNDS=[0,4,9,14,20,23,31,37,42,50,57,63,69,78,84,88,96,100,107,120,128,132,150]
TITLES=['중력 위치에너지의 최소화','양 끝을 고정한 균일한 사슬','같은 조건에서 가장 낮은 에너지','최소화의 목표와 지켜야 할 조건','전체 계산보다 작은 부분으로','작은 부분에 작용하는 세 힘','힘이 맞지 않으면 움직인다','연결된 이웃도 함께 움직인다','끝점과 총길이는 그대로','한 부분의 에너지와 전체 에너지','진동하면서 에너지를 잃는다','움직임이 멈춘 평형','수평 장력은 일정 · 수직 장력은 증가','힘의 균형에서 곡선으로','포물선이 아닌 현수선','같은 길이의 후보를 비교하면','두 곡선이 정확히 겹친다','서로 다른 접근 · 같은 형태','부분은 전체 에너지를 계산하지 않는다','현수선을 축 주위로 회전하면','카테노이드가 만들어진다','다른 에너지 · 같은 cosh']
CLAIMS=['중력 아래의 고정 길이 사슬이 주제다.','질량은 수평 간격이 아닌 실제 호길이에 균일하다.','후보들의 길이와 끝점을 모두 고정해 에너지를 비교한다.','최적화의 목표와 제약을 구별한다.','후보 탐색은 자연의 실제 계산 과정이 아니다.','이상적인 유연한 사슬의 중력·접선 장력 모형이다.','합력은 가속을 만들고 제약을 통해 이웃 운동과 연결된다.','연결은 사슬 부분들을 독립적으로 움직이지 못하게 한다.','PBD의 고정점과 거리 제약을 수치 검증한다.','국소 에너지 감소만으로 전체 감소를 판단할 수 없다.','감쇠 중 U는 증가할 수 있고 U+K가 감소한다.','정적 평형에서 알짜힘은 0이다.','단위 실제 길이당 하중 일정인 균일 사슬을 전제한다.','기울기는 장력 성분 비와 일치한다.','같은 꼭짓점·중심 곡률을 가진 포물선을 비교하며 실제 차이를 표시한다.','수학적 후보 비교와 실제 물리 과정을 분리한다.','두 접근은 동일한 현수선을 준다.','국소적 평형과 길이 제약 아래의 에너지 최소화가 연결된다.','부분의 물리적 반응으로 생긴 결과를 전체적 조건으로 기술한다.','반지름의 최솟값은 a이며 회전축은 최저점보다 a 아래다.','1편과 같은 a=1,h=1.6,R=cosh(.8)의 안정 가지다.','현재 사용자 대본이 명시한 두 현상의 비교이며 다음 편 예고는 없다.']
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    rows=[];start=0
    for line in RAW.splitlines():
        caption,end=line.rsplit('|',1);end=int(end);rows.append(dict(start=start,end=end,caption=caption));start=end
    assert start==150
    (P/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(rows))+'\n',encoding='utf-8')
    manifest=[];narr=[];tts=[]
    for i,(s,e,title,claim) in enumerate(zip(BOUNDS,BOUNDS[1:],TITLES,CLAIMS)):
        d=P/'scenes'/f'{i+1:02}_sequence';d.mkdir(parents=True,exist_ok=True)
        script='\n'.join(c['caption'] for c in rows if s<=c['start']<e);tts.append(script)
        (d/'script.txt').write_text(script+'\n',encoding='utf-8')
        (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import ChainBase\nclass SoapShot(ChainBase):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=f'scenes/{d.name}',start=s,end=e,duration_seconds=e-s,title=title,**{'class':'SoapShot'}))
        (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n## 목적·핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('없음' if i==0 else TITLES[i-1])+f'\n\n## TTS·확정 길이\n사용자 구간 {s}–{e}초, {e-s}초. 문장별 원문·종료 시각은 timing.json이 기준이다. 음원 미제공.\n\n{script}\n\n## 화면·애니메이션\nreference/storyboard.txt의 시퀀스 {i+1:02} 및 visuals.py의 INDEX={i}. 진입 0~0.5초, 중간 구간 변화·관찰, 마지막 상태에서 발화 종료까지 유지한다. 실제 애니메이션 시간은 코드가 확정 길이 초과를 검사한다.\n\n## 화면 텍스트\n{title}. 수식·값은 계산 자료, 자막은 사용자 원문을 사용한다.\n\n## 시작·종료 상태\n독립 씬으로 대상을 재구성하고 관찰·평형·비교의 결론 상태로 종료한다.\n\n## 다음 시각적 연결\n'+(TITLES[i+1] if i<21 else '국소 법칙과 전체 최적화의 결론. 다음 편 예고 없음.')+f'\n\n## 조건·정확성\n{claim}\n이상적인 유연한 균일 사슬, 고정점·총길이 고정, 균일 중력. 후보는 연속체 적분, 움직임은 별도 검증한 이산 질점 모형이다.\n',encoding='utf-8')
        narr.append(f'## {i+1:02} · {s}–{e}초 · {title}\n\n{script}\n')
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    for filename in ['master_script.md','narration.md']:(P/filename).write_text('# 자연의 최적화 02 — 사용자 대본·종료 시각\n\n'+'\n'.join(narr),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
    y='id: nature02_catenary\ntitle: 매달린 사슬이 포물선이 아닌 이유\nvideo:\n  fps: 30\n  layouts:\n    shorts: [1080, 1920]\n    longform: [1920, 1080]\nscenes:\n'
    for m in manifest:y+=f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: SoapShot\n    duration_seconds: {m["duration_seconds"]}\n    transition: cut\n'
    (P/'scenes.yaml').write_text(y,encoding='utf-8')
if __name__=='__main__':main()

