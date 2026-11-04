"""Materialize approved narration and its supplied clock, never estimate speech."""
import json, shutil
from pathlib import Path

P=Path(__file__).resolve().parent
LINES=[
(3,'벡터가 세 개 있으면, 반드시 3차원 공간을 만들 수 있을까요?'),
(8,'첫 번째 벡터가 있습니다. 이 벡터에 여러 숫자를 곱하면 하나의 직선을 만들 수 있습니다.'),
(16,'두 번째 벡터를 추가해 보겠습니다. 첫 번째 벡터와 다른 방향을 향하고 있다면, 두 벡터의 선형결합으로 하나의 평면을 만들 수 있습니다.'),
(19,'그렇다면 세 번째 벡터는 어떨까요?'),
(24,'세 번째 벡터가 이미 만들어진 평면 위에 있다면, 벡터는 세 개지만 공간은 여전히 2차원입니다.'),
(30,'중요한 것은 벡터의 개수가 아니라, 기존 벡터들로 표현할 수 없는 새로운 방향이 존재하는가입니다.'),
(34,'그렇다면 새로운 방향만 따로 찾아낼 수 있을까요?'),
(38,'첫 번째 벡터의 길이를 1로 만들어 기준 방향 큐 원을 정의합니다.'),
(40,'이제 두 번째 벡터를 살펴보겠습니다.'),
(45,'두 번째 벡터에는 큐 원과 나란한 성분과, 그 방향에 수직인 성분이 있습니다.'),
(51,'큐 원 방향으로 투영한 성분을 제거하면, 기존 방향으로 설명할 수 없는 부분만 남습니다.'),
(56,'이 성분의 길이가 0이 아니라면, 정규화해서 새로운 기준 방향 큐 투를 만들 수 있습니다.'),
(62,'이제 세 번째 벡터를 추가해 보겠습니다. 이번에는 기존의 두 방향에 대한 투영 성분을 모두 제거합니다.'),
(67,'남은 벡터가 0이 아니라면, 기존 평면에 수직인 새로운 방향 큐 쓰리를 얻을 수 있습니다.'),
(71,'이렇게 만들어진 세 방향은 서로 직교하며, 각각 길이가 1입니다.'),
(76,'그리고 원래 벡터들은 이 직교하는 방향들의 선형결합으로 다시 표현할 수 있습니다.'),
(82,'직교하는 기준 방향들을 모은 행렬이 큐, 원래 벡터들을 그 기준으로 표현한 계수들을 모은 행렬이 알입니다.'),
(85,'바로 에이 이퀄 큐 알. QR 분해입니다.'),
(89,'QR 분해는 단순히 벡터를 수직으로 만드는 계산이 아닙니다.'),
(95,'각 벡터가 기존 공간에서 얼마나 설명될 수 있고, 무엇을 새롭게 추가하는지 드러내는 과정입니다.'),
]
STARTS=[0,3,8,12,16,19,24,30,34,38,40,45,51,56,59,62,65,67,71,76,79,82,85,89]
TITLES=['벡터 3개 = 3차원?','하나의 방향 → 직선','두 방향의 선형결합','직선에서 평면으로','세 번째 벡터는?','벡터 3개, 차원은 2','개수보다 새로운 방향','새로운 방향만 분리하기','길이 1의 기준 방향','두 번째 벡터 관찰','나란한 성분 + 수직 성분','기존 방향 성분 제거','남은 성분을 정규화','평면 밖의 세 번째 벡터','기존 평면에 투영','평면 위 성분 제거','새로운 기준 방향','서로 직교 · 길이 1','원래 벡터를 다시 만들기','기준 방향을 열로 모으면','조합 계수를 열로 모으면','기하학에서 행렬 분해로','원래 벡터와 기준 방향','공간에 새롭게 추가되는 방향']
def screen(s):
    for a,b in [('큐 원','q₁'),('큐 투','q₂'),('큐 쓰리','q₃'),('에이 이퀄 큐 알','A = QR'),('큐,','Q,'),('알입니다','R입니다')]:s=s.replace(a,b)
    return s
def stamp(t):return f'{int(t)//3600:02}:{int(t)//60%60:02}:{int(t)%60:02},000'
def main():
    template=P.parent/'_template'
    if not (P/'scenes.yaml').exists():shutil.copytree(template,P,dirs_exist_ok=True)
    cues=[];start=0
    for end,s in LINES:
        cues.append(dict(start=start,end=end,tts=s,caption=screen(s)));start=end
    (P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(s for _,s in LINES)+'\n',encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    narration='# QR 1편 — 벡터는 어떻게 새로운 공간을 만드는가?\n\n사용자 확정 원고·문장 종료 시각, 총 95초. 음원 미제공.\n\n| 시작 | 종료 | 내레이션 |\n|---|---|---|\n'+'\n'.join(f'| {c["start"]} | {c["end"]} | {c["caption"]} |' for c in cues)+'\n'
    for name in ['narration.md','master_script.md']:(P/name).write_text(narration,encoding='utf-8')
    manifest=[]
    for i,(start,title) in enumerate(zip(STARTS,TITLES)):
        end=STARTS[i+1] if i+1<len(STARTS) else 95
        directory=f'scenes/{i+1:02}_scene';d=P/directory;d.mkdir(parents=True,exist_ok=True)
        manifest.append(dict(id=f'{i+1:02}',directory=directory,**{'class':'QRShot'},start=start,end=end,duration_seconds=end-start,title=title))
        (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import QRBase\nclass QRShot(QRBase):\n    INDEX = '+str(i)+'\n',encoding='utf-8')
        overlapping=[c for c in cues if c['start']<end and c['end']>start]
        (d/'script.txt').write_text('\n\n'.join(c['tts'] for c in overlapping)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} {title}\n\n- 주장: {title}\n- 전체 시각: {start}–{end}초, 길이 {end-start}초. 사용자 종료 시각을 기준으로 컷 분할.\n- 발화: 상위 timing.json을 공유하며, 분할 컷에서 같은 문장을 중복 발화하지 않는다.\n- 화면: 상위 storyboard.md의 컷 {i+1:02} 및 visuals.py의 해당 INDEX를 사용.\n- 좌표: a₁=(1,1,0), a₂=(0,2,0), 본 계산 a₃=(1,1,2).\n- 도입 종속 사례만 a₃=a₁+a₂=(1,3,0).\n- 음원: 미제공. 무음 visual을 최종본으로 사용.\n- 연결: 같은 좌표 모델과 색상을 유지한다. 복습·예고 없음.\n',encoding='utf-8')
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('title: QR 1편 — 새로운 방향\nduration_seconds: 95\ntiming_source: user_sentence_end_times\naudio: not_supplied\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    source: {m["directory"]}/scene.py\n    class: QRShot\n    start: {m["start"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    (P/'project.json').write_text(json.dumps(dict(duration=95,ending_confirmed=True),indent=2),encoding='utf-8')
if __name__=='__main__':main()
