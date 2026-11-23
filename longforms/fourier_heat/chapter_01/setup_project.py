"""Create production metadata from the user's approved script and timestamps."""
import json, shutil
from pathlib import Path
R=Path(__file__).resolve().parent
W=R.parents[2]
DATA='''4|우리는 뜨거운 물체가 시간이 지나면서 식어간다는 사실을 잘 알고 있습니다.
12|뜨거운 물체와 차가운 물체가 접촉하면 열은 뜨거운 곳에서 차가운 곳으로 이동하고, 시간이 흐르면서 온도 차이는 점차 줄어듭니다.
19|그런데 이러한 단순한 현상을 설명하는 열방정식이 수학의 수많은 분야와 연결되어 있다는 사실을 알고 계신가요?
24|얼음이 얼어붙으면서 물과 얼음 사이의 경계가 움직이는 현상을 다루는 스테판 문제,
29|점성을 가진 물과 공기의 움직임을 설명하는 나비에–스토크스 방정식,
38|액체가 좁은 틈이나 다공성 매질 사이로 침투하면서 경계가 변화하는 헬레–쇼 문제는 모두 열방정식과 관련된 수학적 구조를 공유합니다.
42|그런데 이러한 연결은 물리적인 현상에서 끝나지 않습니다.
48|불규칙하게 움직이는 입자들의 브라운 운동에서는 입자의 위치에 대한 확률분포가 열방정식을 따르며,
55|주식의 옵션 가격을 계산하는 블랙–숄즈 방정식 역시 적절한 변수변환을 통해 열방정식의 형태로 바꿀 수 있습니다.
59|그리고 그 영향은 더욱 추상적인 수학으로 확장됩니다.
67|열이 공간 위에서 어떻게 퍼지는지를 연구하는 방법은 기하학적 성질과 위상적 불변량을 연결하는 지표정리의 연구에도 활용되었으며,
75|공간의 기하학적 구조 자체가 시간에 따라 변화하는 기하학적 흐름에서도 열방정식과 유사한 확산 구조가 등장합니다.
80|이러한 연구는 나아가 수학의 오랜 난제였던 푸앵카레 추측의 해결과도 연결됩니다.
87|서로 전혀 관련이 없어 보이는 문제들 속에서 수학자들은 반복해서 열방정식과 비슷한 수학적 구조를 발견한 것입니다.
94|이처럼 열방정식이 다양한 현상과 연결되는 이유를 이해하려면, 먼저 이 방정식이 무엇을 설명하는지 살펴볼 필요가 있습니다.
98|열방정식은 두 가지 기본적인 물리 법칙에서 출발합니다.
101|첫 번째는 에너지 보존 법칙입니다.
110|외부에서 별도의 에너지가 공급되거나 내부에서 열이 발생하지 않는다면, 어떤 영역의 열에너지 변화는 그 영역으로 들어오고 나가는 열의 차이로 결정됩니다.
112|두 번째는 푸리에의 열전도 법칙입니다.
119|열은 온도가 높은 곳에서 낮은 곳으로 이동하며, 온도가 공간에 따라 급격하게 달라질수록 더 강하게 흐른다는 것입니다.
126|이 두 가지 원리를 결합하면, 시간에 따라 온도 분포가 어떻게 변화하는지를 설명하는 열방정식이 등장합니다.
131|그리고 이 방정식의 해는 위치와 시간에 따른 온도를 나타내는 함수입니다.
138|즉, 열방정식의 해를 구한다는 것은 주어진 초기 온도 분포가 시간이 흐르면서 어떻게 변화하는지 알아내는 것입니다.
145|앞서 살펴본 여러 현상에서도 중요한 것은 시간이 흐르면서 각각의 물리량이나 상태가 어떻게 변화하는지를 이해하는 일입니다.
150|하지만 실제 물체의 온도 분포는 매우 복잡한 형태를 가질 수 있습니다.
155|그렇다면 이러한 복잡한 온도 분포에 대해서는 어떻게 방정식의 해를 구할 수 있을까요?
163|프랑스의 수학자 조제프 푸리에는 이 문제를 해결하기 위해 복잡한 온도 분포를 단순한 함수들의 합으로 표현하는 방법을 연구했습니다.
169|그리고 이 아이디어는 훗날 푸리에 해석이라는 거대한 수학 분야로 발전하게 됩니다.'''
CUTS=[(4,'익숙한 냉각'),(12,'온도 차이가 줄어든다'),(19,'하나의 방정식에서 여러 분야로'),(24,'스테판 문제: 움직이는 상 경계'),(29,'점성은 속도를 확산시킨다'),(38,'헬레–쇼: 움직이는 유체 경계'),(42,'물리에서 확률로'),(48,'무작위 운동에서 확률밀도로'),(55,'옵션 가격 PDE의 변수변환'),(59,'평면에서 곡면으로'),(67,'열핵 방법과 지표정리'),(75,'기하학 자체의 변화'),(80,'푸앵카레 추측과 리치 흐름'),(87,'동일한 식이 아닌 공통된 구조'),(94,'막대 하나로 돌아가기'),(101,'두 물리 원리와 작은 구간'),(110,'유입과 유출의 차이'),(119,'온도 구배가 흐름을 정한다'),(126,'두 원리에서 열방정식으로'),(138,'해는 위치와 시간의 함수'),(145,'서로 다른 상태의 시간 변화'),(155,'복잡한 초기 온도 분포'),(169,'복잡한 함수를 단순한 진동의 합으로')]
def stamp(t):return f'{t//3600:02d}:{t//60%60:02d}:{t%60:02d},000'
def main():
 template=W/'longforms/_template'
 for f in ['README.md','master_script.md','scenes.yaml']:
  if not (R/f).exists():shutil.copyfile(template/f,R/f)
 lines=[];start=0
 for i,row in enumerate(DATA.splitlines(),1):
  end,txt=row.split('|',1);end=int(end);lines.append(dict(id=i,start=start,end=end,text=txt));start=end
 (R/'timing.json').write_text(json.dumps(dict(source='User supplied sentence end times; no audio supplied',duration=169,lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'narration.md').write_text('# 열방정식 1장 — 사용자 확정 대본\n\n'+'\n\n'.join(f"{x['start']}–{x['end']}초\n{x['text']}" for x in lines)+'\n',encoding='utf-8')
 (R/'master_script.md').write_text((R/'narration.md').read_text(encoding='utf-8'),encoding='utf-8')
 (R/'tts_script.txt').write_text('\n\n'.join(x['text'].replace('나비에–스토크스','나비에 스토크스').replace('헬레–쇼','헬레 쇼').replace('블랙–숄즈','블랙 숄즈') for x in lines)+'\n',encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f"{x['id']}\n{stamp(x['start'])} --> {stamp(x['end'])}\n{x['text']}" for x in lines)+'\n',encoding='utf-8')
 manifest=[];start=0
 for i,(end,title) in enumerate(CUTS,1):
  d=R/'scenes'/f'{i:02d}';d.mkdir(parents=True,exist_ok=True)
  script='\n\n'.join(x['text'] for x in lines if start<=x['start']<end)
  m=dict(id=f'{i:02d}',directory=f'scenes/{i:02d}',class_name=f'Shot{i:02d}',start=start,duration_seconds=end-start,title=title);manifest.append(m)
  (d/'script.txt').write_text(script+'\n',encoding='utf-8')
  (d/'spec.md').write_text(f'# {i:02d} — {title}\n\n## 목적과 핵심 주장\n{title}\n\n## 앞 장면에서 받은 내용\n'+('없음' if i==1 else CUTS[i-2][1])+f'\n\n## TTS 원문·확정 길이\n{script}\n\n{start}–{end}초, {end-start}초. 사용자 종료 시각 기준. 음원 미제공.\n\n## 화면·애니메이션\n첨부 콘티 해당 컷을 공유 visuals.py의 geometry/labels로 구현. 본문 y=-2.45~2.8, 자막 y=-3.25. 시작에서 종료까지 해당 현상의 변화가 진행된다.\n\n## 화면 텍스트\n{title}. 구체적인 수식·보조 표시는 visuals.py labels 참조.\n\n## 시작·종료 상태와 연결\n공통 남색 배경, 열·물·확률·기하 색상 유지. '+('처음의 뜨거운 막대에서 시작. ' if i==1 else '')+('여러 진동 성분과 합성 곡선을 유지하며 169초에 종료.' if i==23 else f'다음 컷: {CUTS[i][1]}.')+'\n\n## 수학적 조건·과장 방지\nbrief.md의 조건 준수. 유체·자유경계·기하학적 변형은 개념도이며 수치해로 표기하지 않는다. 3차원 다양체와 2차원 구면은 구별한다. 열전도 해는 단열 경계의 코사인 모드 해석해를 사용한다.\n',encoding='utf-8')
  (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import HeatScene\nclass Shot{i:02d}(HeatScene):index={i}\n',encoding='utf-8');start=end
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('title: 열방정식 1장\nresolution: [1920, 1080]\nfps: 30\nduration_seconds: 169\naudio: none\nscenes:\n'+''.join(f"  - id: '{m['id']}'\n    directory: {m['directory']}\n    start: {m['start']}\n    duration_seconds: {m['duration_seconds']}\n" for m in manifest),encoding='utf-8')
if __name__=='__main__':main()
