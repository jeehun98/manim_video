"""Materialize the supplied script and exact sentence/scene boundaries."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
SCRIPT='''4|전기를 이용해 정보를 전달하고, 계산하는 장치를 만든다고 생각해 보겠습니다.
7|가장 먼저 필요한 것은 정보를 표현하는 방법입니다.
12|전기는 전압이라는 물리량을 가지고 있고, 이 전압은 연속적인 값을 가질 수 있습니다.
16|그렇다면 전압의 크기에 서로 다른 의미를 부여하면 어떨까요?
23|예를 들어 0.1볼트는 1, 0.2볼트는 2, 0.3볼트는 3을 나타내도록 정하는 것입니다.
28|이론적으로는 더 많은 전압 수준을 구분할수록 하나의 신호로 더 많은 정보를 표현할 수 있습니다.
31|하지만 실제 회로에서는 문제가 발생합니다.
36|전기적 신호에는 잡음이 섞일 수 있고, 전압도 완벽하게 일정하게 유지되지 않습니다.
42|0.2볼트로 전달하려던 신호가 조금만 달라져도, 다른 값으로 잘못 해석될 수 있는 것입니다.
44|이 문제를 해결하려면 어떻게 해야 할까요?
50|전압을 더욱 정밀하게 측정할 수도 있겠지만, 반대로 구분해야 하는 상태의 개수를 줄일 수도 있습니다.
53|예를 들어 전압을 크게 두 영역으로 나누는 것입니다.
55|낮은 전압과 높은 전압.
61|이렇게 하면 전압에 작은 변화가 발생하더라도 동일한 상태로 해석할 수 있는 여유가 생깁니다.
62|물론 여기에는 대가가 있습니다.
66|하나의 신호로는 단 두 가지 상태밖에 표현할 수 없다는 것입니다.
69|그런데 여러 신호를 함께 사용하면 어떨까요?
74|두 가지 상태를 가진 신호 두 개를 조합하면 네 가지 경우가 만들어집니다.
77|세 개라면 여덟 가지, 네 개라면 열여섯 가지입니다.
81|이처럼 신호를 추가할 때마다 표현할 수 있는 조합은 두 배로 늘어납니다.
88|이제 이 두 상태를 각각 0과 1이라고 부르고, 하나의 상태를 나타내는 단위를 비트라고 정의해 보겠습니다.
95|우리는 연속적인 전압을 정밀하게 구분하는 대신, 구별하기 쉬운 두 상태를 여러 개 조합해 정보를 표현하는 방법을 얻었습니다.
98|이것이 이진 디지털 표현의 기본적인 아이디어입니다.
102|하지만 아직 우리가 만든 것은 정보를 표현하는 방법일 뿐입니다.
108|이 신호들을 이용해 실제 계산을 수행하려면, 입력에 따라 새로운 출력을 만들어내는 장치가 필요합니다.
113|그렇다면 전기적 신호만으로 다른 신호를 만들어내는 것은 어떻게 가능할까요?'''
SCENES=[
 (0,12,'signal','전기 신호와 전압','연속적인 전압으로 정보를 표현하는 문제를 제시한다.'),
 (12,28,'levels','전압에 의미 부여','전압과 숫자의 대응은 정한 해석 규칙이다.'),
 (28,42,'noise','잡음과 오인식','신호 변동과 판정 경계를 넘는 오류를 구별한다.'),
 (42,61,'binary','두 논리 상태의 발견','같은 전압 범위에서 상태 간격을 넓혀 변동 여유를 확보한다.'),
 (61,66,'tradeoff','표현력의 한계','한 신호가 표현하는 상태 수를 줄이는 대가가 있다.'),
 (66,81,'combinations','신호 조합 확장','독립 신호 하나를 추가할 때 조합 수가 두 배가 된다.'),
 (81,98,'bit','비트의 도입','두 논리 상태를 조합하는 이진 정보 표현에 도달한다.'),
 (98,113,'processing','표현에서 계산으로','표현과 입력을 변환하는 회로의 역할을 구별한다.'),
]
CUES=[
 [(0,4,'발광점에서 파란 신호선이 확장'),(4,7,'동일 신호가 Voltage–Time 그래프로 전환'),(7,12,'전압 표시점·수평 가이드·전압 수치가 연속 변화')],
 [(12,16,'0.1V→1, 0.2V→2, 0.3V→3의 가상 대응을 순차 제시'),(16,23,'한 전압 신호가 세 수준을 이동하며 대응 카드 강조'),(23,28,'0.05V·0.35V 수준을 추가해 표현 상태 수 확대')],
 [(28,31,'0.20V 기준선 주변의 작은 변동'),(31,36,'0.15V 판정 경계와 현재 판정 2 표시'),(36,38,'선택 지점 0.17V는 경계 안에 있어 2 유지'),(38,42,'0.13V로 이동해 경계를 넘는 순간 판정 1로 변경')],
 [(42,44,'다수준 기준선과 잡음 상태를 관찰'),(44,50,'촘촘한 상태 표시를 약화하고 두 기준 수준으로 정리'),(50,53,'두 유효 영역과 중간의 판정 보장 밖 구간'),(53,55,'LOW·HIGH 명명'),(55,61,'같은 크기의 변동에도 LOW 범위 안에서 판정 유지')],
 [(61,62,'넓은 두 유효 영역 유지'),(62,66,'중간 상태 추가 시도 후 한 신호·두 상태의 대가 표시')],
 [(66,69,'LOW·HIGH를 임시 기호 0·1로 표시'),(69,74,'기존 두 조합이 각각 분기하여 네 조합'),(74,77,'네 조합 각각이 분기하여 여덟 조합'),(77,81,'여덟 조합 각각이 분기하여 열여섯 조합과 2ⁿ')],
 [(81,85,'LOW·HIGH를 논리 기호 0·1에 대응'),(85,88,'Binary Digit를 Bit으로 축약·정보 단위 정의'),(88,95,'촘촘한 한 신호와 두 상태의 여러 신호 비교'),(95,98,'적은 상태×여러 신호=다양한 정보 표현으로 정리')],
 [(98,102,'0101 비트 배열을 유지'),(102,108,'입력 배열이 미지의 처리 장치로 이동'),(108,112.4,'처리 장치의 물음표 강조'),(112.4,113,'주요 도형을 암전하며 종료')],
]
def stamp(t):
 t=int(round(t*1000));return f'{t//3600000:02}:{t//60000%60:02}:{t//1000%60:02},{t%1000:03}'
def main():
 timing=[];start=0
 for line in SCRIPT.splitlines():
  end,s=line.split('|',1);end=int(end);timing.append(dict(start=start,end=end,text=s));start=end
 assert len(timing)==26 and start==113
 (R/'timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(timing))+'\n',encoding='utf-8')
 narration=['# GPU 개론 01 — 컴퓨터는 왜 0과 1을 사용할까?','', '사용자 제공 확정 원문·종료 시각. 총 113초, 26문장. 음원 미제공.','']
 manifest=[];yaml=['id: gpui01_binary_signals','title: "컴퓨터는 왜 0과 1을 사용할까?"','duration_seconds: 113','video:','  fps: 30','  layouts:','    longform: [1920, 1080]','    shorts: [1080, 1920]','audio: null','scenes:']
 for i,(a,b,slug,title,claim) in enumerate(SCENES,1):
  directory=f'scenes/{i:02}_{slug}';folder=R/directory;folder.mkdir(parents=True,exist_ok=True)
  rows=[r for r in timing if a<=r['start']<b];script='\n\n'.join(r['text'] for r in rows)
  (folder/'script.txt').write_text(script+'\n',encoding='utf-8')
  (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import BinaryScene\n\nclass Scene{i:02}(BinaryScene):\n    index={i-1}\n',encoding='utf-8')
  cue_table='| 전체 시각(초) | 화면 변화 |\n| --- | --- |\n'+'\n'.join(f'| {x}–{y} | {event} |' for x,y,event in CUES[i-1])
  manifest.append(dict(id=f'{i:02}',directory=directory,**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title))
  yaml.extend([f'  - id: "{i:02}"',f'    directory: {directory}',f'    class: Scene{i:02}',f'    duration_seconds: {b-a}',f'    start_seconds: {a}',f'    end_seconds: {b}', '    transition: cut'])
  narration.extend([f'## {a}–{b}초 · {title}','']+[f'{r["start"]}–{r["end"]}초: {r["text"]}\n' for r in rows])
  spec=f'''# {i:02} · {title}

## 목적과 주장
{claim}

## TTS와 확정 길이
사용자 문장 종료 시각 기준 {a}–{b}초, {b-a}초. 음원 미제공으로 현재 무음. 원문은 script.txt, 문장별 경계는 ../../timing.json.

## 화면과 타임라인
사용자 콘티 ../../storyboard_reference.md의 SCENE {i:02}를 기준으로 한다. 상세 이벤트는 ../../scene_engine.py의 {slug} 메서드에 구현한다. 자막은 사용자 문장별 시간 그대로 표시한다.

{cue_table}

## 시작·종료 상태와 연결
시작: {'전압 신호가 나타나기 전의 어두운 실험 화면' if i==1 else SCENES[i-2][3]+'에서 도달한 개념'}.
종료: {claim}
연결: {'완성된 표현 체계에서 입력을 변환하는 미지의 장치로 시선 이동' if i==8 else '같은 색·좌표계 또는 데이터 조합을 다음 씬에서 유지'}.

## 화면 텍스트·조건
긴 설명은 하단 전체 문장 자막에 둔다. 전압·숫자·LOW/HIGH·경우의 수는 중심 화면에 표시한다. 초기 전압 대응은 가상 규칙이다. 0과 1이라는 논리 기호는 조합 소개 이전에 표시하지 않는다. LOW/HIGH 사이에는 판정 보장 밖의 구간을 유지한다. 0/1은 정확한 0V/1V라는 뜻이 아니다. 실제 소자 규격·잡음 내성의 실측을 주장하지 않는다. 마지막 질문은 사용자 확정 대본과 콘티의 명시적 요청에 따라 유지한다.

## 원문
{script}
'''
  (folder/'spec.md').write_text(spec,encoding='utf-8')
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('\n'.join(yaml)+'\n',encoding='utf-8')
 (R/'narration.md').write_text('\n'.join(narration),encoding='utf-8')
 (R/'master_script.md').write_text('\n'.join(narration),encoding='utf-8')
 # Pronunciation-only spellings, no headings or timecodes; paragraph boundaries follow visual changes.
 tts=[]
 for row in timing:
  s=row['text']
  for raw,spoken in [('0.1','영 점 일'),('0.2','영 점 이'),('0.3','영 점 삼'),('0과 1','영과 일')]:s=s.replace(raw,spoken)
  tts.append(s)
 (R/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
 print(f'Prepared {len(timing)} sentences, {len(manifest)} scenes, 113 seconds.')
if __name__=='__main__':main()
