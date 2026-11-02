"""Preserve supplied narration and exact sentence-end timestamps."""
import json, shutil
from pathlib import Path
R=Path(__file__).resolve().parent
LINES='''2|신경망에는 수많은 가중치가 존재합니다.
8|가중치가 20만 개라면, 일반적인 학습에서는 20만 개의 값을 각각 조정할 수 있습니다.
13|그런데 정말 20만 개를 모두 독립적으로 조정해야만 문제를 해결할 수 있을까요?
18|2018년, 연구진은 이 질문을 확인하기 위해 독특한 실험을 진행했습니다.
22|먼저 약 20만 개의 가중치를 가진 신경망을 준비했습니다.
25|하지만 이번에는 모든 가중치를 자유롭게 학습시키지 않았습니다.
29|대신 훨씬 적은 수의 변수만 학습하도록 제한했습니다.
32|예를 들어 가중치가 세 개 있다고 생각해 보겠습니다.
38|일반적으로는 세 값을 각각 변경할 수 있지만, 세 값을 하나의 변수에 연결하면 상황이 달라집니다.
43|변수 하나를 변경할 때마다 세 가중치가 정해진 비율로 함께 움직이는 것입니다.
48|가중치는 여전히 세 개지만, 실제로 조정할 수 있는 독립적인 값은 하나뿐입니다.
52|연구진은 이 방법을 수십만 개의 가중치에 적용했습니다.
58|무작위로 정해진 방향들을 고정하고, 그 방향을 따라 움직이는 소수의 변수만 학습시켰습니다.
59|그 결과는 놀라웠습니다.
71|MNIST 손글씨 숫자 분류 실험에서, 199,210개의 파라미터를 가진 신경망이 약 750개의 학습 변수만으로도 원래 모델 정확도의 90퍼센트 이상에 도달했습니다.
76|전체 파라미터 수의 약 0.38퍼센트에 해당하는 자유도만 사용한 것입니다.
78|여기서 중요한 점이 있습니다.
81|연구진은 신경망의 연결을 제거한 것이 아닙니다.
84|모든 가중치는 그대로 존재하며 계산에 사용됩니다.
87|단지 가중치들이 움직일 수 있는 방향을 제한했을 뿐입니다.
89|이것은 무엇을 의미할까요?
96|신경망에 존재하는 파라미터의 수와, 특정 문제를 해결하기 위해 필요한 학습 자유도의 수는 같지 않을 수 있다는 것입니다.
104|연구진은 이렇게 특정 성능에 도달하는 데 필요한 부분공간의 차원을 내재 차원, Intrinsic Dimension이라는 개념으로 측정했습니다.
109|물론 이것이 모든 신경망에서 750개의 변수만 필요하다는 뜻은 아닙니다.
113|모델 구조와 데이터, 요구하는 성능에 따라 결과는 달라집니다.
116|하지만 이 실험은 중요한 가능성을 보여줍니다.
119|우리는 신경망의 크기를 파라미터의 개수로 측정합니다.
124|그런데 그 파라미터들이 모두 독립적으로 움직일 필요는 없었습니다.
129|그렇다면 신경망이 문제를 해결하는 데 필요한 진짜 차원은 무엇으로 결정되는 걸까요?'''
SCENES=[('question',0,13,'모든 가중치를 독립적으로 조정해야 할까?'),('research',13,29,'신경망을 유지하고 학습 제어만 바꾼다'),('three_weights',29,48,'세 가중치가 하나의 변수에 따라 직선 위에서 움직인다'),('projection',48,59,'고정된 무작위 방향으로 전체 가중치를 조정한다'),('result',59,76,'199,210개 파라미터와 약 750개 학습 변수'),('connections',76,87,'모든 연결은 계산에 그대로 사용된다'),('measurement',87,104,'성능 기준에 도달하는 무작위 부분공간 차원을 측정한다'),('conditions',104,116,'내재 차원은 문제와 모델과 성능 기준에 따라 달라진다'),('conclusion',116,129,'파라미터 수와 학습 자유도는 다를 수 있다')]
def stamp(t):
 return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
def main():
 rows=[];start=0
 for line in LINES.splitlines():
  end,s=line.split('|',1);end=int(end);rows.append(dict(start=start,end=end,text=s));start=end
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 script='\n\n'.join(r['text'] for r in rows)+'\n'
 for name in ['narration.md','master_script.md']:(R/name).write_text(script,encoding='utf-8')
 tts=script
 for source,spoken in [('2018년','이천십팔 년'),('20만 개','이십만 개'),('199,210개','십구만 구천이백십 개'),('750개','칠백오십 개'),('90퍼센트','구십 퍼센트'),('0.38퍼센트','영 점 삼팔 퍼센트'),('MNIST','엠니스트'),('Intrinsic Dimension','인트린식 디멘션')]:tts=tts.replace(source,spoken)
 (R/'tts_script.txt').write_text(tts,encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows,1))+'\n',encoding='utf-8')
 manifest=[]
 example=R/'scenes'/'01_example'
 if example.exists():shutil.rmtree(example)
 for i,(slug,start,end,claim) in enumerate(SCENES,1):
  folder=R/'scenes'/f'{i:02}_{slug}';folder.mkdir(parents=True,exist_ok=True)
  rr=[r for r in rows if start<=r['start']<end];speech='\n\n'.join(r['text'] for r in rr)
  (folder/'script.txt').write_text(speech+'\n',encoding='utf-8')
  (folder/'spec.md').write_text(f'# {i:02} — {claim}\n\n## 목적·핵심 주장\n{claim}\n\n## 앞 장면과 연결\n'+('독립적인 질문으로 시작한다.' if i==1 else '직전 장면에서 제시한 가중치와 학습 변수의 구분을 이어받는다.')+f'\n\n## TTS 원문·확정 길이\n{speech}\n\n사용자 문장 종료 시각 기준 {start}–{end}초, {end-start}초. 음원 미제공.\n\n## 화면·애니메이션·텍스트\n첨부 콘티 SCENE {i:02} 및 scene_engine.py의 해당 메서드를 따른다. 가로형은 좌우, 세로형은 상하 배치. timing.json의 문장 경계에 자막을 교체한다.\n\n## 시작·종료 상태\n주장을 설명할 도형이 등장하고 핵심 문장을 유지한다. 독립 교체 가능한 완성 씬.\n\n## 정확성\n199,210은 편향을 포함한 전체 파라미터 수. 750은 MNIST 완전연결망의 d_int90 측정값. 성능 곡선은 개념도이며 실제 측정 데이터가 아니다. 3차원 좌표계는 세 가중치 예시에만 사용한다. 복습과 다음 편 예고는 넣지 않는다.\n',encoding='utf-8')
  (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import IntrinsicScene\nclass Scene{i:02}(IntrinsicScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=str(folder.relative_to(R)).replace('\\','/'),start=start,end=end,duration_seconds=end-start,claim=claim,**{'class':f'Scene{i:02}'}))
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('title: 최소 조건 2부 · 신경망 1편 · 내재 차원\nduration_seconds: 129\nlayouts: [1920x1080, 1080x1920]\nfps: 60\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
 (R/'brief.md').write_text('# 제작 기준\n\n사용자 제공 대본·29개 문장 종료 시각을 확정 기준으로 129초 제작. 요청 명칭은 최소 조건 2부 신경망 시리즈 1편이며, 첨부 콘티 제목의 02편보다 현재 요청을 우선한다. 가로 1920×1080·세로 1080×1920, 모두 60fps. 음원 미제공이므로 무음·전체 대본 자막 영상.\n\n핵심: 파라미터 수, 학습 자유도, 특정 성능을 달성하는 무작위 부분공간의 차원을 구분한다. 세 가중치 예시는 (1,2,3)+t(2,−1,1)로 실제 계산한다. 비율 막대는 750/199210 그대로 그린다. 성능 그래프는 개념도 표기. 750개의 뉴런으로 그리지 않는다. 연결을 제거하지 않는다. 끝 질문은 해당 주제의 열린 질문이며 후속편 예고 문구는 넣지 않는다.\n\n출처: Li, Farkhoor, Liu, Yosinski (2018), Measuring the Intrinsic Dimension of Objective Landscapes. https://arxiv.org/abs/1804.08838\nhttps://yosinski.com/media/papers/Li__2018__Measuring_the_Intrinsic_Dimension_of_Objective_Landscapes__.pdf\n',encoding='utf-8')
 shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\4069f0af-8353-4370-9d65-ea94e8806a60\붙여넣은 텍스트.txt'),R/'storyboard_reference.md')
if __name__=='__main__':main()
