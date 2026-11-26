"""Materialize the approved narration and user-supplied sentence end times."""
from pathlib import Path
import json, shutil
R=Path(__file__).resolve().parent
cuts=[0,26,55,80,87,112,142,151,171,197,209,240,267,297,319,343,355,388,408,426]
titles=['최적화와 목적함수','미분은 국소적인 선형 근사','수평인 접선과 극값','미분값 0은 필요조건','곡선에서 곡면으로','접평면과 편미분','내부 극값의 후보','편미분에서 그래디언트로','방향에 따른 일차 변화량','곡면에서 등위선으로','등위선과 그래디언트의 수직 관계','울타리 문제와 제약조건','제약조건이 허용하는 방향','교차에서 접촉으로','두 그래디언트의 비례관계','라그랑주 승수법','직사각형의 최대 넓이','접선에서 제약 최적화까지','허용된 방향의 일차 변화율']
claims=['최적화는 목적함수의 최대·최소를 찾는다.','미분은 곡선을 접선으로 국소 근사한다.','미분 가능한 함수의 내부 극값에서는 접선이 수평이다.','미분값 0만으로 극값을 보장하지 않는다.','같은 곡선은 이변수 함수 곡면의 단면이다.','접평면의 기울기는 두 편미분으로 결정된다.','내부 극값에서 두 편미분은 모두 0이다.','그래디언트와 작은 변위의 내적은 일차 변화량이다.','고정된 변위 길이에서 그래디언트 방향의 증가량이 최대다.','같은 높이의 단면을 입력 평면에 투영하면 등위선이다.','0이 아닌 그래디언트는 등위선의 접선에 수직이다.','둘레를 고정하면 가로와 세로를 자유롭게 바꿀 수 없다.','제약곡선의 접선 방향이 허용된 방향이다.','접촉점에서는 허용된 방향의 일차 변화율이 0이다.','정칙 제약 아래 목적함수의 그래디언트는 제약함수 그래디언트의 상수배다.','그래디언트 관계와 원래 제약식을 함께 풀어 후보를 구한다.','둘레 8의 직사각형 최대 넓이는 4다.','접선·접평면·등위선은 하나의 일차 변화 원리로 연결된다.','제약에 따라 달라지는 것은 고려해야 할 방향의 범위다.']
def main():
 lines=[];start=0
 for row in (R/'narration_source.txt').read_text(encoding='utf-8').splitlines():
  text,end=row.rsplit('|',1);end=int(end);lines.append(dict(start=start,end=end,text=text));start=end
 assert start==426 and all(a['end']==b['start'] for a,b in zip(lines,lines[1:]))
 (R/'timing.json').write_text(json.dumps(dict(duration_seconds=426,source='User-provided sentence end times, 2026-11-26',audio_provided=False,lines=lines),ensure_ascii=False,indent=2),encoding='utf-8')
 manifest=[];blocks=[]
 for i,(a,b,title,claim) in enumerate(zip(cuts,cuts[1:],titles,claims),1):
  d=R/'scenes'/f'{i:02d}';d.mkdir(parents=True,exist_ok=True)
  if not (d/'spec.md').exists():shutil.copyfile(R.parent/'_template/scenes/01_example/spec.md',d/'spec.md')
  script='\n'.join(x['text'] for x in lines if a<=x['start']<b).translate(str.maketrans({'0':'영','2':'이','4':'사','8':'팔'}));blocks.append(script)
  (d/'script.txt').write_text(script+'\n',encoding='utf-8')
  (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import OptimizationScene\nclass Shot{i:02d}(OptimizationScene):\n index={i}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02d}',directory=f'scenes/{i:02d}',class_name=f'Shot{i:02d}',start=a,duration_seconds=b-a,title=title))
  events=[x for x in lines if a<=x['start']<b]
  (d/'spec.md').write_text(f'# SCENE {i:02d} — {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('없음' if i==1 else claims[i-2])+f'\n\n## TTS 원문과 확정 길이\n{script}\n\n- 사용자 확정 구간: {a}–{b}초, {b-a}초. 음원 미제공, 무음.\n\n## 화면과 애니메이션\n- 16:9, 딥 네이비 배경. 본문 y=-2.65~3.1, 자막 y=-3.3.\n- 청색 목적함수, 금색 접선·접평면·그래디언트, 녹색 최적점, 적색 제약, 보라색 허용 변위.\n'+ '\n'.join(f"- {x['start']-a}–{x['end']-a}초: {x['text']}" for x in events)+f'\n- 구체 도형·수식·시각 변화: `../../visuals.py`의 index={i} 분기.\n\n## 시작·종료 상태 및 연결\n- 시작: {title}의 대상 도형.\n- 종료: {claim}\n- 다음: '+(titles[i] if i<len(titles) else '허용된 방향에서의 일차 변화율 0을 유지하며 종료. 별도 엔드카드 없음.')+'\n\n## 정확성 확인\n미분 가능·정의역 내부, 등식 제약은 ∇G≠0인 정칙점. 필요조건과 충분조건 구분. 등위선 이동과 접선의 유한 직선 이동 구분. 2D 벡터 도형은 x,y 동일 단위. 직사각형 x,y≥0 경계 비교. 3D는 높이축 압축 정사영.\n',encoding='utf-8')
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'tts_script.txt').write_text('\n\n'.join(blocks)+'\n',encoding='utf-8')
 (R/'master_script.md').write_text('# 미분에서 시작하는 최적화의 기하학 — 라그랑주 승수법\n\n사용자 확정 원문·문장 종료 시각. 총 426초.\n\n'+'\n\n'.join(f"{x['start']}–{x['end']}초 | {x['text']}" for x in lines)+'\n',encoding='utf-8')
 (R/'brief.md').write_text('# 제작 기준\n\n426초, 1920×1080, 30fps. 사용자 확정 대본 유지, 문장 종료 시각 준수. 음원 미제공: 무음·전체 자막.\n\nF(x,y)=2x+10y-x²+2xy-3y²=19-(x-y-1)²-2(y-3)². 초기 f(x)=F(x,3). P=(2,2), F=16, ∇F=(2,2). 전역 최대 F(4,3)=19. 후반 F=xy, G=x+y=4, x,y≥0. 후보 (2,2), 넓이 4, 퇴화 경계 넓이 0.\n\n첨부 이미지의 슬라이더는 애니메이션으로 구현. 깨진 LaTeX 표기는 정상 MathTex로 교정. 도입의 극대·극소 곡선은 개념 안내용이며, 26초부터 공통 이차함수 사용. 19개 독립 렌더. 기존 구조 재사용, 요청 없는 쇼츠·음원·썸네일 추가 없음.\n\nKnowledge Atlas lagrange-multiplier 기록 확인: 관련 출처·관계 미등록. 기본 미적분 공식은 수치·대수 검사로 확인한다.\n',encoding='utf-8')
 def stamp(t):return f'{t//3600:02d}:{t//60%60:02d}:{t%60:02d},000'
 import textwrap
 (R/'captions.srt').write_text('\n\n'.join(f"{i}\n{stamp(x['start'])} --> {stamp(x['end'])}\n"+'\n'.join(textwrap.wrap(x['text'],width=58,break_long_words=False,break_on_hyphens=False)) for i,x in enumerate(lines,1))+'\n',encoding='utf-8')
 (R/'scenes.yaml').write_text('id: lagrange_optimization\ntitle: 미분에서 시작하는 최적화의 기하학\nvideo: {width: 1920, height: 1080, fps: 30}\naudio: null\nscenes:\n'+''.join(f"  - id: '{m['id']}'\n    directory: {m['directory']}\n    class: {m['class_name']}\n    start: {m['start']}\n    duration_seconds: {m['duration_seconds']}\n" for m in manifest),encoding='utf-8')
if __name__=='__main__':main()
