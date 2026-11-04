"""User-approved narration, exact speech boundaries, independent scene specs."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
SCRIPT='''5|앞서 우리는 전압을 두 가지 논리 상태로 구분해 정보를 표현하는 방법을 살펴봤습니다.
11|하지만 이렇게 표현한 신호를 이용해 계산하려면, 단순히 정보를 전달하는 것만으로는 부족합니다.
16|입력된 신호에 따라 다른 신호를 만들어내거나, 전류의 흐름을 제어할 수 있어야 합니다.
20|그렇다면 전기적 신호로 다른 전류의 흐름을 제어할 수 있을까요?
22|먼저 평범한 스위치를 생각해 보겠습니다.
28|스위치를 연결하면 전류가 흐를 수 있는 통로가 만들어지고, 끊으면 전류의 흐름이 차단됩니다.
33|그런데 이 스위치를 손으로 움직이는 대신, 또 다른 전기적 신호로 제어할 수 있다면 어떨까요?
38|예를 들어 한쪽에 전압을 가하면 통로가 열리고, 전압을 낮추면 통로가 닫히는 것입니다.
43|이렇게 하면 하나의 전기적 신호를 이용해 다른 전류 경로를 제어할 수 있습니다.
47|그렇다면 실제로 움직이는 부품 없이 이런 스위치를 만들 수 있을까요?
50|여기서 반도체의 특성을 이용할 수 있습니다.
55|반도체 내부에서는 전기장을 가하면 전하의 분포가 달라질 수 있습니다.
62|이를 이용하면 두 지점 사이에 전류가 흐르기 쉬운 통로를 형성하거나, 반대로 그 흐름을 크게 억제할 수 있습니다.
68|즉, 물리적인 접점을 붙였다 떼지 않고도 전기적 신호만으로 통로의 전도성을 바꿀 수 있는 것입니다.
73|이 원리를 이용한 대표적인 소자가 MOSFET이라는 트랜지스터입니다.
79|MOSFET에는 전류 경로의 양쪽에 위치한 Source와 Drain, 그리고 그 통로를 제어하는 Gate가 있습니다.
87|Gate에 가해지는 전압이 반도체 내부의 전하 분포를 바꾸면서 Source와 Drain 사이의 전류 흐름을 조절합니다.
92|앞서 생각했던 전압으로 제어하는 스위치를 실제 반도체 소자로 구현한 것입니다.
95|그렇다면 이 스위치로 새로운 신호도 만들 수 있을까요?
100|출력 지점이 높은 전압의 전원과 연결되면, 높은 전압 상태를 만들 수 있습니다.
104|반대로 접지와 연결되면 낮은 전압 상태를 만들 수 있습니다.
109|이때 각각의 연결을 입력 전압에 따라 선택하도록 여러 트랜지스터를 배치할 수 있습니다.
116|예를 들어 입력 전압이 낮을 때는 출력이 높아지고, 입력 전압이 높을 때는 출력이 낮아지도록 만드는 것입니다.
120|이것이 입력을 반전시키는 회로인 인버터의 기본적인 원리입니다.
123|여기에는 별도의 계산 프로그램이 필요하지 않습니다.
130|입력 전압이 바뀌면 전류 경로의 상태가 달라지고, 미리 설계된 회로의 연결 구조에 따라 출력 전압이 결정됩니다.
136|결국 전기적 신호를 제어하는 소자들을 조합하면, 입력에 따라 새로운 출력 신호를 만들어낼 수 있습니다.
142|그렇다면 이 스위치들을 서로 다른 방식으로 연결하면 어떤 논리 연산까지 구현할 수 있을까요?'''
SCENES=[
 (0,16,'need','표현에서 신호 제어로','정보 표현과 입력에 따른 출력 생성은 구별된다.'),
 (16,28,'manual','전류 경로를 여닫는 스위치','닫힌 회로는 전류가 흐를 수 있는 경로를 만든다.'),
 (28,43,'control','손 대신 전기 신호로','제어 입력은 별도의 전류 경로를 제어한다.'),
 (43,62,'field','움직이지 않는 스위치','절연된 전극의 전기장이 반도체 전하 분포와 전도성을 바꾼다.'),
 (62,68,'electronic','접점 대신 전도성 변화','기계적인 접촉 이동 없이 경로의 전도성을 바꿀 수 있다.'),
 (68,92,'mosfet','이 장치의 이름, MOSFET','충분한 Gate–Source 전압이 n채널 형성을 제어한다.'),
 (92,109,'output','새로운 출력은 어디에서 올까?','출력 노드를 VDD 또는 GND에 연결해 전압 상태를 만든다.'),
 (109,120,'inverter','입력과 반대인 출력','상보적인 pMOS·nMOS 연결이 반전을 구현한다.'),
 (120,136,'physical','연결 구조가 정하는 규칙','별도 프로그램 없이 회로의 물리적 연결이 입력·출력 관계를 만든다.'),
 (136,142,'networks','연결을 바꾸면 어떤 규칙이 될까?','소자들을 연결하는 방식으로 다양한 회로를 구성할 수 있다.'),
]
CUES=[
 [(0,5,'LOW/0·HIGH/1 표현 상자'),(5,11,'입력 상자와 미지의 처리 장치·출력선'),(11,16,'입력이 바뀌어도 출력은 아직 미정')],
 [(16,20,'전원·열린 접점·전구·귀환선의 닫힌 회로 모형'),(20,22,'열린 접점 강조'),(22,25,'접점 회전·경로 활성화·전구 점등'),(25,28,'접점 개방·경로 차단·전구 소등')],
 [(28,33,'동일 접점 아래에 별도의 보라색 제어 입력'),(33,38,'입력 HIGH/LOW에 따라 접점 연결·차단'),(38,43,'제어 입력과 전류 경로를 명확히 분리해 표시')],
 [(43,47,'기계 접점에서 반도체 몸체로'),(47,50,'반도체와 전하 운반자 모형'),(50,55,'전극·절연막·전기장·전하 재분포'),(55,62,'표면 근처 전도 채널 형성과 억제')],
 [(62,65,'움직이는 접점과 움직이지 않는 반도체를 비교'),(65,68,'반도체 구조를 중심으로 확대')],
 [(68,73,'MOSFET 이름 소개'),(73,79,'Source·Drain·Gate를 순서대로 표시'),(79,87,'Source 기준 Gate 전압과 채널 ON/OFF, 양의 VDS 조건'),(87,92,'단면에서 절연 Gate를 가진 세 단자 기능 기호로 전환')],
 [(92,95,'출력 노드 도입'),(95,100,'위쪽 VDD 경로로 출력 HIGH'),(100,104,'아래쪽 GND 경로로 출력 LOW'),(104,109,'두 경로와 공통 Gate 입력 구성')],
 [(109,113,'입력 LOW: pMOS ON·nMOS OFF·출력 HIGH'),(113,116,'입력 HIGH: pMOS OFF·nMOS ON·출력 LOW'),(116,119,'입출력 대응표와 반전 관계'),(119,120,'NOT / INVERTER 명명')],
 [(120,123,'CMOS 회로 자체를 관찰'),(123,130,'입력 변화와 상보 경로·출력 전압 변화를 세 번 반복'),(130,136,'입력→물리 회로→출력의 기능 구조와 반전 대응표')],
 [(136,139,'세 단자 소자 1→2→4→8개'),(139,142,'직렬·병렬 연결을 일부 제시하고 물음표로 마무리')],
]
def stamp(t):
 t=int(round(t*1000));return f'{t//3600000:02}:{t//60000%60:02}:{t//1000%60:02},{t%1000:03}'
def main():
 rows=[];start=0
 for line in SCRIPT.splitlines():
  end,s=line.split('|',1);end=int(end);rows.append(dict(start=start,end=end,text=s));start=end
 assert len(rows)==28 and start==142
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows))+'\n',encoding='utf-8')
 manifest=[];narr=['# GPU 개론 02 — 트랜지스터는 어떻게 전기 신호를 제어할까?','','사용자 원문 28문장·종료 시각 확정, 총 142초. 음원 미제공.','']
 yaml=['id: gpui02_transistor','title: "트랜지스터는 어떻게 전기 신호를 제어할까?"','duration_seconds: 142','video:','  fps: 30','  layouts:','    longform: [1920, 1080]','    shorts: [1080, 1920]','audio: null','scenes:']
 for i,(a,b,slug,title,claim) in enumerate(SCENES,1):
  directory=f'scenes/{i:02}_{slug}';folder=R/directory;folder.mkdir(parents=True,exist_ok=True)
  selected=[r for r in rows if a<=r['start']<b];script='\n\n'.join(r['text'] for r in selected)
  (folder/'script.txt').write_text(script+'\n',encoding='utf-8')
  (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import TransistorScene\n\nclass Scene{i:02}(TransistorScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=directory,**{'class':f'Scene{i:02}'},start=a,end=b,duration_seconds=b-a,title=title))
  yaml.extend([f'  - id: "{i:02}"',f'    directory: {directory}',f'    class: Scene{i:02}',f'    start_seconds: {a}',f'    end_seconds: {b}',f'    duration_seconds: {b-a}','    transition: cut'])
  table='| 전체 시각(초) | 화면 |\n| --- | --- |\n'+'\n'.join(f'| {x}–{y} | {e} |' for x,y,e in CUES[i-1])
  spec=f'''# {i:02} · {title}

## 목적·주장
{claim}

## 앞 장면과 시작 상태
{'LOW/HIGH로 표현한 정보에서 시작한다.' if i==1 else SCENES[i-2][4]}
동일 색상·기능 배치로 이전 씬의 개념을 유지한다.

## TTS 원문과 확정 길이
사용자 종료 시각 {a}–{b}초, {b-a}초. 음원 미제공. 추정 타이밍을 사용하지 않는다.

{script}

## 화면·타임라인·텍스트
{table}

핵심 용어는 단면/회로 옆에, 설명은 전용 하단 자막에 둔다. 동작은 ../../scene_engine.py의 {slug} 메서드에서 구현한다. 원문 콘티: ../../storyboard_reference.md.

## 종료 상태와 다음 연결
종료 주장: {claim}
{'소자 연결의 가능성을 질문하며 종료한다.' if i==10 else '다음 씬은 이 기능 구조를 유지하며 '+SCENES[i][3]+'로 확장한다.'}

## 조건·과장 방지
Gate 입력과 Source–Drain 경로를 연결하지 않는다. 절연막을 통과하는 전자 이동을 그리지 않는다. 전도 경로는 빛나는 선으로 표시하며 입자 이동으로 전류 속도를 표현하지 않는다. MOSFET은 n채널 강화형의 개념 단면이며 몸체 접속 등은 생략한다. VGS는 Source 기준, VDS>0의 예시다. CMOS는 정적 상보 상태를 표시하고 출력 전압 전환은 설명용 시간으로 확대한다. 기계 접점과 MOSFET 채널 형성을 동일 물리 현상으로 표현하지 않는다. 사용자의 도입·마지막 질문은 확정 원문 그대로 유지한다.
'''
  (folder/'spec.md').write_text(spec,encoding='utf-8')
  narr.extend([f'## {a}–{b}초 · {title}','']+[f'{r["start"]}–{r["end"]}초: {r["text"]}\n' for r in selected])
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('\n'.join(yaml)+'\n',encoding='utf-8')
 for name in ['narration.md','master_script.md']:(R/name).write_text('\n'.join(narr),encoding='utf-8')
 tts=[]
 for r in rows:
  s=r['text']
  for a,b in [('MOSFET','모스펫'),('Source','소스'),('Drain','드레인'),('Gate','게이트'),('0과 1','영과 일')]:s=s.replace(a,b)
  tts.append(s)
 (R/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
 # Reuse the verified independent render/concat and caption-boundary QA workflow.
 old=R.parent/'gpui01_binary_signals'
 for name in ['build.py','inspect_caption_boundaries.py','inspect_frames.py']:
  s=(old/name).read_text(encoding='utf-8').replace('gpui01_binary_signals','gpui02_transistor').replace('gpui01_binary_113s','gpui02_transistor_142s').replace("f'gpui01_{suffix}'","f'gpui02_{suffix}'").replace('==113','==142').replace('==113*fps','==142*fps').replace('-113','-142').replace('duration_seconds=113','duration_seconds=142')
  if name=='inspect_frames.py':s=s.replace('TIMES=[2,9,18,26,34,40,52,59,64,72,76,80,86,92,97,106,111]','TIMES=[3,9,14,19,24,27,31,35,41,46,52,58,64,71,77,83,90,97,102,107,111,115,119,125,132,138,141]')
  (R/name).write_text(s,encoding='utf-8')
 print('Prepared 28 sentences, 10 scenes, 142 seconds, dual layouts.')
if __name__=='__main__':main()
