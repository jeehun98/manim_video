"""User supplied sentence clocks, not estimated durations."""
import json, math, shutil
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
RAW='''철사로 만든 고리를 비눗물에 담갔다 꺼내면, 얇은 비눗막이 만들어집니다.|4
그런데 두 개의 원형 고리를 나란히 놓고, 그 사이에 비눗막을 만든 뒤 고리를 조금씩 벌려보겠습니다.|10
비눗막은 원기둥 형태를 유지하지 않습니다.|13
가운데가 잘록해지면서 독특한 곡면을 만들어냅니다.|16
이 곡면을 카테노이드라고 합니다.|19
그런데 왜 이런 모양이 나타나는 걸까요?|21
그 이유를 이해하려면 비눗막을 이루는 분자들부터 살펴봐야 합니다.|26
액체 내부의 분자들은 주변의 다른 분자들과 끊임없이 상호작용합니다.|30
분자 사이에는 가까워지면 강하게 밀어내는 반발력과, 일정 거리에서 서로 끌어당기는 인력이 존재합니다.|36
이러한 상호작용 때문에 분자들은 적절한 거리에서 더 낮은 위치에너지를 가질 수 있습니다.|42
그런데 액체 내부의 분자 하나를 표면으로 옮긴다고 생각해 보겠습니다.|47
표면 바깥쪽에는 같은 액체 분자가 상대적으로 적습니다.|51
따라서 이 분자는 내부에 있을 때 누리던 인력에 의한 상호작용 일부를 잃게 됩니다.|55
서로 끌어당기던 분자들을 떼어놓으려면 에너지가 필요하듯, 새로운 액체 표면을 만드는 데에도 에너지 비용이 발생합니다.|62
실제 액체에서는 분자들의 열운동과 배열까지 고려해야 하지만, 핵심은 표면을 넓히는 데 추가적인 자유에너지가 필요하다는 것입니다.|71
균일한 표면에서는 이 에너지 비용이 표면적에 비례합니다.|75
그 비례계수가 바로 표면장력입니다.|77
즉, 표면적이 커질수록 표면을 유지하는 데 필요한 에너지도 증가합니다.|82
그렇다면 비눗막이 에너지를 줄이는 가장 직접적인 방법은 무엇일까요?|86
바로 표면적을 줄이는 것입니다.|89
하지만 비눗막의 가장자리는 철사 고리에 고정되어 있습니다.|93
막 전체가 하나의 점으로 줄어들 수는 없습니다.|96
따라서 정해진 경계를 유지하면서 표면적을 줄이는 방향으로 형태가 변합니다.|101
그 결과 안정된 평형에 도달하면, 작은 변형으로는 더 이상 표면적을 줄일 수 없는 곡면이 만들어집니다.|107
이것이 최소곡면입니다.|109
그런데 여기서 흥미로운 질문이 등장합니다.|112
비눗막은 어떻게 이러한 곡면을 찾아낸 걸까요?|115
가능한 모든 곡면의 면적을 계산하고, 그중 가장 작은 것을 선택한 걸까요?|120
물론 아닙니다.|121
비눗막의 아주 작은 부분을 확대해 보겠습니다.|123
이 부분은 전체 곡면의 모양이나 표면적을 알 필요가 없습니다.|127
그저 주변에서 작용하는 힘에 반응할 뿐입니다.|130
힘의 균형이 맞지 않으면 움직이고, 형태가 바뀌면서 주변과의 균형을 찾아갑니다.|135
그리고 각 부분에서 힘의 균형이 이루어지면, 전체 곡면에서도 특별한 수학적 조건이 나타납니다.|141
곡면을 아주 조금 변형했을 때, 표면적의 일차 변화량이 0이 되는 것입니다.|146
수학에서는 이를 면적의 첫 번째 변분이 0이라고 표현합니다.|150
비눗막을 구성하는 분자들은 전체 표면적을 계산하지 않습니다.|154
각 부분은 현재의 물리적 조건에 반응할 뿐입니다.|157
하지만 그렇게 형성된 전체 곡면은 수학적인 최적화 조건을 만족합니다.|162
자연은 최적의 형태를 미리 알고 있는 것이 아닙니다.|165
그런데 우리는 자연의 국소적인 물리법칙에서, 전체적인 최적화의 구조를 발견할 수 있습니다.|171
그리고 이런 현상은 비눗막에서만 나타나는 것이 아닙니다.|174'''
BOUNDS=[0,4,10,16,21,30,42,51,55,62,71,77,82,89,96,101,109,115,121,123,135,146,156,165,174]
TITLES=['고리 위에 생긴 얇은 막','같은 축 위의 두 고리','가운데가 잘록해진다','카테노이드','표면 안으로 들어가면','분자 사이의 거리와 에너지','내부에서 표면으로','주변 상호작용의 차이','새로운 표면에는 비용이 든다','표면 자유에너지','면적에 비례하는 에너지','면적이 줄면 에너지도 줄어든다','에너지를 줄이는 방법','가장자리는 고정되어 있다','같은 경계 · 다른 면적','안정된 평형과 최소곡면','계산해서 고르는 걸까?','전체 탐색은 필요 없다','작은 부분을 들여다보면','주변 막이 당기는 힘','힘의 평형과 곡률','시간 변화와 다른, 작은 변형','국소적인 법칙 · 전체의 조건','미리 아는 것이 아니라']
NOTES=['원판 막은 한 고리의 예시다.','안정 가지를 사용하며 R=a cosh(h/2a)를 유지한다.','원기둥은 점선 비교 모형이며 운동 시뮬레이션이 아니다.','축을 포함하는 단면의 현수선을 강조한다.','분자 배열·진동은 개념 모형이다.','Lennard–Jones는 개념 모형이며 실제 비눗물의 단일 퍼텐셜이 아니다.','단일 분자 모형과 자유에너지를 동일시하지 않는다.','바깥쪽 액체 이웃이 상대적으로 적음을 표현한다.','분자 수 보존의 유체 시뮬레이션이 아닌 표면 비용 개념도다.','온도·조성·γ 일정, A는 중간면 면적, 두 계면을 포함한다.','표면장력 γ는 한 계면의 계수다.','실제 계수 단위와 구별되는 상대량을 사용한다.','경계는 고정되며 막 전체가 점으로 수축하지 않는다.','세 후보는 동일 경계이며 표시 면적은 수치 적분한다.','기하학적 보간이며 실제 유체 시간 발전이 아니다.','압력차·중력 무시, 안정한 국소 최소와 전역 최소를 구별한다.','가상 탐색이라는 사고실험 표시를 유지한다.','자연의 실제 탐색 알고리즘처럼 표현하지 않는다.','패치 경계의 접평면 안쪽에서 바깥쪽 공법선 방향을 사용한다.','장력은 표면에 접하며 압력차 없는 개념 모형이다.','각 힘은 남고 합력만 상쇄된다. 유한 패치 수치 오차와 곡률을 구별한다.','ε는 실제 시간과 다르다. 경계를 보존한 축대칭 후보의 실제 면적을 적분한다.','δA=0은 전역 최소의 보장이 아니다.','사용자 마지막 문장은 유지하되 사슬·빛·다음 편 예고는 표시하지 않는다.']
def area(blend=1.,eps=0.):
    z=np.linspace(-.8,.8,20001);a=1.;R=np.cosh(.8)
    r=R+blend*(a*np.cosh(z/a)-R)+eps*np.cos(np.pi*z/1.6)**2
    dr=blend*np.sinh(z/a)-eps*np.pi/1.6*np.sin(2*np.pi*z/1.6)
    return float(2*np.pi*np.trapezoid(r*np.sqrt(1+dr*dr),z))
def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
def main():
    rows=[];start=0
    for line in RAW.splitlines():
        text,end=line.rsplit('|',1);end=int(end);rows.append(dict(start=start,end=end,caption=text));start=end
    (P/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(rows))+'\n',encoding='utf-8')
    manifests=[];narr=[];tts=[]
    for i,(s,e,title,note) in enumerate(zip(BOUNDS,BOUNDS[1:],TITLES,NOTES)):
        d=P/'scenes'/f'{i+1:02}_sequence';d.mkdir(parents=True,exist_ok=True)
        # Sentences spanning a visual cut are spoken once, in the unit where they start.
        script='\n'.join(c['caption'] for c in rows if s<=c['start']<e)
        (d/'script.txt').write_text(script+'\n',encoding='utf-8');tts.append(script)
        (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import SoapBase\nclass SoapShot(SoapBase):\n    INDEX={i}\n',encoding='utf-8')
        manifests.append(dict(id=f'{i+1:02}',directory=f'scenes/{d.name}',start=s,end=e,duration_seconds=e-s,title=title,**{'class':'SoapShot'}))
        (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n## 목적·핵심 주장\n{title}\n\n## 앞 장면에서 받은 내용\n'+('없음' if i==0 else TITLES[i-1])+f'\n\n## TTS·길이\n사용자 확정 구간 {s}–{e}초, {e-s}초. 문장 시각은 ../../timing.json이 기준이다. script.txt는 이 구간에서 시작하는 문장만 포함하며, 경계에 걸친 발화를 재시작하지 않는다. 음원 미제공.\n\n{script}\n\n## 화면·애니메이션\nvisuals.py의 INDEX={i} 구현. 첫 0.6초 대상 진입, 중간 구간의 변화·비교, 마지막 0.3초 종료 상태 유지. 전체 구간은 위 사용자 시각에 고정한다.\n\n## 화면 텍스트\n{title}; 구현의 공식·주석 및 timing.json의 원문 자막.\n\n## 시작·종료 상태\n독립적으로 대상을 구성하고 비교 또는 평형 상태로 끝낸다.\n\n## 다음 장면 연결\n'+(TITLES[i+1] if i<23 else '비눗막의 독립 결론으로 종료. 다음 편 예고 없음.')+f'\n\n## 정확성\n{note}\n',encoding='utf-8')
        narr.append(f'## {i+1:02} · {s}–{e}초 · {title}\n\n{script}\n')
    (P/'manifest.json').write_text(json.dumps(manifests,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'narration.md').write_text('# 자연의 최적화 01 — 사용자 확정 발화 시각\n\n'+ '\n'.join(narr),encoding='utf-8')
    (P/'master_script.md').write_text((P/'narration.md').read_text(encoding='utf-8'),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(x for x in tts if x)+'\n',encoding='utf-8')
    yaml='id: nature01_soap_film\ntitle: 비눗막은 어떻게 최소 면적을 찾을까?\nvideo:\n  fps: 30\n  layouts:\n    shorts: [1080, 1920]\n    longform: [1920, 1080]\nscenes:\n'
    for m in manifests:yaml+=f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: SoapShot\n    duration_seconds: {m["duration_seconds"]}\n    transition: cut\n'
    (P/'scenes.yaml').write_text(yaml,encoding='utf-8')
    values=dict(a=1.,height=1.6,R=float(np.cosh(.8)),half_height_over_a=.8,stable_condition='u*tanh(u) < 1',stability_value=float(.8*np.tanh(.8)),areas={str(k):area(k) for k in [0,.5,1]},variation=[dict(eps=float(v),area=area(1,float(v))) for v in np.linspace(-.22,.22,45)],first_derivative=(area(1,1e-5)-area(1,-1e-5))/2e-5)
    (P/'geometry.json').write_text(json.dumps(values,indent=2),encoding='utf-8')
if __name__=='__main__':main()
