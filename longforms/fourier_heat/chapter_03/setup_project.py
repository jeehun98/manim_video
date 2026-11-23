"""Create production sources from approved narration and exact end times."""
import json,shutil
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parents[2]
DATA='''9|앞서 우리는 복잡한 온도 분포를 여러 진동 성분으로 분해하고, 각각의 변화를 계산한 뒤 다시 합하여 열방정식의 해를 구하는 방법을 살펴봤습니다.
14|그런데 이러한 방법을 통해 알 수 있는 것은 온도 분포의 변화뿐만이 아닙니다.
18|열방정식의 해가 반드시 가지는 몇 가지 중요한 수학적 성질도 발견할 수 있습니다.
21|첫 번째는 매끄러움 성질입니다.
24|처음 온도 분포가 매우 불규칙한 형태를 가진다고 생각해 보겠습니다.
29|어떤 부분은 뾰족하게 솟아 있고, 다른 부분에서는 온도가 갑자기 변합니다.
36|그런데 시간이 흐르면 이러한 급격한 변화들이 점차 사라지고, 온도 분포는 매끄러운 곡선으로 변합니다.
40|앞서 살펴본 푸리에 급수를 이용하면 그 이유를 이해할 수 있습니다.
45|복잡한 온도 분포는 서로 다른 주파수를 가진 진동 성분들의 합으로 표현할 수 있습니다.
50|그리고 열방정식에서는 주파수가 높은 성분일수록 진폭이 더 빠르게 감소합니다.
56|따라서 급격한 변화를 만들어 내는 고주파 성분들이 먼저 사라지고, 상대적으로 완만한 저주파 성분들이 남게 됩니다.
64|그런데 열방정식의 매끄러움 성질은 단순히 곡선이 점차 완만해진다는 것보다 훨씬 강한 의미를 가지고 있습니다.
72|적절한 조건에서는 처음 온도 분포가 불연속적이더라도, 시간이 조금이라도 지나면 해는 공간에 대해 무한히 여러 번 미분할 수 있는 함수가 됩니다.
80|즉, 처음에 아무리 불규칙한 온도 분포가 주어지더라도, 열의 확산 과정이 그 분포를 매끄럽게 만드는 것입니다.
82|두 번째는 최댓값 원리입니다.
86|처음 막대의 모든 지점의 온도가 0도에서 100도 사이라고 생각해 보겠습니다.
93|외부에서 열을 공급하지 않는다면, 시간이 지난 뒤 막대 내부에서 100도보다 높은 온도가 새롭게 나타날 수 있을까요?
96|일반적인 열방정식에서는 그럴 수 없습니다.
102|그 이유는 열이 주변보다 온도가 높은 곳에서 빠져나가고, 주변보다 온도가 낮은 곳으로 들어오기 때문입니다.
108|어떤 지점이 주변보다 높은 온도를 가진다면, 그 지점의 온도는 감소하는 방향으로 변화합니다.
112|반대로 주변보다 낮은 지점에서는 온도가 증가하는 방향으로 변화합니다.
118|따라서 적절한 경계조건 아래에서는 처음의 최댓값보다 더 높은 온도가 새롭게 만들어지지 않습니다.
123|마찬가지로 처음의 최솟값보다 더 낮은 온도도 새롭게 만들어지지 않습니다.
125|이것이 열방정식의 최댓값 원리입니다.
130|그런데 이 원리는 단순히 온도의 범위를 제한하는 데 그치지 않습니다.
139|열방정식의 서로 다른 두 해를 비교하여 어느 해가 더 큰 값을 가지는지 판단하거나, 주어진 조건에서 해가 유일한지를 증명하는 데에도 활용됩니다.
142|마지막 세 번째는 하르나크 부등식입니다.
147|앞서 최댓값 원리는 온도 분포가 가질 수 있는 전체적인 값의 범위를 제한했습니다.
152|그렇다면 서로 다른 위치와 시간에서의 온도 사이에도 일정한 관계가 존재할까요?
157|예를 들어 처음에는 한 지점에만 열이 집중되어 있다고 생각해 보겠습니다.
161|시간이 지나면 열이 주변으로 퍼지면서 멀리 떨어진 지점의 온도도 변화합니다.
170|그런데 열방정식을 만족하는 양의 함수라면, 서로 떨어진 두 위치와 서로 다른 시각에서의 값이 아무런 관계 없이 결정될 수는 없습니다.
174|이러한 관계를 수학적으로 나타내는 것이 하르나크 부등식입니다.
182|하르나크 부등식은 적절한 조건에서 한 지점의 현재 값과 다른 지점의 미래 값 사이에 성립하는 정량적인 제한을 제공합니다.
185|그런데 왜 이러한 관계가 나타나는 것일까요?
190|열방정식에서는 어떤 지점의 온도 변화가 주변의 온도 분포에 의해 결정됩니다.
195|따라서 열이 퍼지는 과정에서는 서로 다른 위치의 값들이 시간에 따라 연결됩니다.
204|예를 들어 양의 온도 분포에서 한 지점의 값이 매우 크다면, 이후 다른 지점의 값이 얼마나 작을 수 있는지에도 거리와 시간에 따른 제한이 생깁니다.
208|하르나크 부등식은 이러한 관계를 구체적인 부등식으로 표현한 것입니다.
215|정리하자면, 매끄러움 성질은 처음의 불규칙한 온도 분포가 시간이 지나면서 매끄러워진다는 사실을 설명합니다.
219|최댓값 원리는 새로운 극댓값과 극솟값이 나타나는 것을 제한하고,
225|하르나크 부등식은 서로 다른 위치와 시간에서의 양의 해가 어떤 관계를 가져야 하는지 알려줍니다.
234|이러한 성질들은 열방정식의 해가 단순히 시간에 따라 변화하는 함수가 아니라, 그 변화 과정에서 매우 정교한 수학적 규칙을 따른다는 사실을 보여줍니다.
237|그런데 여기서 또 하나의 흥미로운 질문이 생깁니다.
242|지금까지 우리는 열방정식을 이용해 온도 분포가 어떻게 변하는지 계산했습니다.
249|그렇다면 반대로 수많은 입자가 무작위로 움직이는 과정을 관찰하는 것만으로도 열방정식의 해를 구할 수 있을까요?
252|놀랍게도 이 두 문제는 서로 연결되어 있습니다.
255|바로 브라운 운동과 파인만–카츠 공식입니다.'''
CUTS=[(18,'계산한 해에서 새로운 성질로'),(36,'불규칙한 분포가 매끄러워진다'),(56,'고주파 성분이 먼저 사라진다'),(64,'완만해지는 것보다 강한 성질'),(72,'양의 시간에는 무한 번 미분 가능'),(80,'불규칙한 초기값에서 매끄러운 해로'),(93,'새로운 최고 온도가 나타날 수 있을까?'),(108,'봉우리에서는 온도가 내려간다'),(112,'골짜기에서는 온도가 올라간다'),(125,'처음의 최댓값과 최솟값 사이'),(139,'해의 비교에서 유일성으로'),(152,'두 위치와 두 시각의 값'),(161,'집중된 열이 주변으로 퍼진다'),(174,'현재의 A와 미래의 B를 비교한다'),(185,'미래 값이 작아질 수 있는 한계'),(195,'거리와 시간 간격이 중요하다'),(208,'하르나크 부등식의 정량적 관계'),(215,'매끄러움 — 해의 규칙성'),(219,'최댓값 원리 — 해의 범위'),(225,'하르나크 — 값 사이의 제약'),(234,'열방정식의 해를 지배하는 규칙'),(242,'온도 분포의 변화에서 새로운 질문으로'),(249,'확산을 무작위 입자로 바라보다'),(255,'브라운 운동과 파인만–카츠 공식')]
def stamp(t):return f'{t//3600:02d}:{t//60%60:02d}:{t%60:02d},000'
def main():
 for f in ['README.md','master_script.md','scenes.yaml']:
  if not (R/f).exists():shutil.copyfile(W/'longforms/_template'/f,R/f)
 lines=[];start=0
 for i,row in enumerate(DATA.splitlines(),1):
  end,txt=row.split('|',1);end=int(end);lines.append(dict(id=i,start=start,end=end,text=txt));start=end
 (R/'timing.json').write_text(json.dumps(dict(duration=255,source='User sentence end times; audio not supplied',lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
 narration='# 열방정식 3장 — 사용자 확정 대본\n\n'+'\n\n'.join(f"{x['start']}–{x['end']}초\n{x['text']}" for x in lines)+'\n'
 for f in ['narration.md','master_script.md']:(R/f).write_text(narration,encoding='utf-8')
 (R/'tts_script.txt').write_text('\n\n'.join(x['text'].replace('파인만–카츠','파인만 카츠') for x in lines)+'\n',encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f"{x['id']}\n{stamp(x['start'])} --> {stamp(x['end'])}\n{x['text']}" for x in lines)+'\n',encoding='utf-8')
 manifest=[];start=0
 for i,(end,title) in enumerate(CUTS,1):
  d=R/'scenes'/f'{i:02d}';d.mkdir(parents=True,exist_ok=True);script='\n\n'.join(x['text'] for x in lines if start<=x['start']<end)
  m=dict(id=f'{i:02d}',directory=f'scenes/{i:02d}',class_name=f'Shot{i:02d}',start=start,duration_seconds=end-start,title=title);manifest.append(m)
  (d/'script.txt').write_text(script+'\n',encoding='utf-8')
  (d/'spec.md').write_text(f'# {i:02d} — {title}\n\n## 목적과 핵심 주장\n{title}\n\n## 앞 장면에서 받은 내용\n'+('2장의 해와 감쇠 성분' if i==1 else CUTS[i-2][1])+f'\n\n## 확정 TTS·길이\n{script}\n\n{start}–{end}초, {end-start}초. 문장 종료 시각은 사용자 제공값, 음원 없음.\n\n## 화면과 시간대별 애니메이션\n첨부 storyboard_source.txt의 해당 구간을 따른다. visuals.py geometry/labels에서 실제 시간에 따라 정확한 해·미분·하한·마커를 생성한다. 상단 챕터/맥락, 본문 그래프, 전용 하단 자막 영역.\n\n## 화면 텍스트\n'+title+' 및 visuals.py의 해당 수식과 조건.\n\n## 시작·종료 상태와 다음 연결\n'+('양의 밀도곡선과 무작위 입자를 남기고 255초에 종료.' if i==len(CUTS) else '다음 주장: '+CUTS[i][1])+ '\n\n## 수학적 조건과 단순화\nbrief.md 참조. 매끄러움·최댓값은 실제 주기적 열핵 합성해, 하르나크의 명시적 상수는 전체 실수선의 양의 해에서 계산한다. 비교값 막대와 실제 해의 값을 구별한다. 무한 미분 가능성의 도식은 유한한 미분 3개만으로 증명했다고 표현하지 않는다.\n',encoding='utf-8')
  if not (d/'scene.py').exists():(d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import PropertiesScene\nclass Shot{i:02d}(PropertiesScene):index={i}\n',encoding='utf-8')
  start=end
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('title: 열방정식 3장 — 해의 성질\nvideo: {width: 1920, height: 1080, fps: 30}\nduration_seconds: 255\naudio: none\nscenes:\n'+''.join(f"  - id: '{m['id']}'\n    directory: {m['directory']}\n    start: {m['start']}\n    duration_seconds: {m['duration_seconds']}\n" for m in manifest),encoding='utf-8')
 print(f'{len(lines)} sentences, {len(manifest)} scenes, {start} seconds')
if __name__=='__main__':main()
