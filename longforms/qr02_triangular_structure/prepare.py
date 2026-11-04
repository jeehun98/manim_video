"""Approved 98-second clock and 25 independent scene specifications."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent
RAW='''4|QR 분해에서 행렬 R은 왜 대각선 아래쪽이 모두 0일까요?
10|이것은 단순히 계산하기 편하도록 정해 놓은 형태가 아닙니다. 벡터들이 공간을 구성하는 방식과 관련이 있습니다.
14|세 개의 선형독립 벡터를 열로 가진 행렬 A를 생각해 보겠습니다.
21|이 벡터들을 순서대로 직교화하면, 서로 수직이고 길이가 1인 세 방향, 큐 원, 큐 투, 큐 쓰리를 얻습니다.
25|첫 번째 벡터 에이 원은 큐 원 방향만으로 표현할 수 있습니다.
27|그런데 왜 큐 투와 큐 쓰리의 계수는 0일까요?
30|두 방향 모두 첫 번째 벡터에 수직이기 때문입니다.
36|직교하는 단위벡터를 기준으로 할 때, 각 방향의 계수는 원래 벡터와의 내적으로 구할 수 있습니다.
41|수직인 두 벡터의 내적은 0이므로, 첫 번째 열의 아래쪽 두 계수는 0이 됩니다.
43|이번에는 두 번째 벡터를 보겠습니다.
47|두 번째 벡터는 큐 원과 큐 투의 선형결합으로 표현됩니다.
53|세 번째 방향 큐 쓰리는 처음 두 벡터가 만드는 평면에 수직이므로, 두 번째 벡터와의 내적도 0입니다.
57|반면 세 번째 벡터는 세 방향 모두의 성분을 가질 수 있습니다.
61|이제 각 벡터를 표현하는 계수들을 열 순서대로 모아보겠습니다.
65|대각선 아래쪽이 모두 0인 위삼각행렬 R이 만들어집니다.
67|여기에는 더 중요한 구조가 숨어 있습니다.
71|첫 번째 원래 벡터가 만드는 직선은 큐 원이 만드는 직선과 같습니다.
76|처음 두 벡터가 만드는 평면도 큐 원과 큐 투가 만드는 평면과 같습니다.
79|세 번째 벡터까지 포함해도 마찬가지입니다.
87|QR 분해는 원래 벡터들이 순서대로 만들어가는 부분공간을 보존하면서, 그 공간의 기준을 직교하는 방향들로 바꿉니다.
91|따라서 R의 아래쪽에 나타나는 0들은 우연한 계산 결과가 아닙니다.
98|뒤에 만들어진 직교 방향이 앞의 벡터들이 만드는 공간에 수직이라는 사실이, 행렬에 그대로 나타난 것입니다.'''
STARTS=[0,4,10,14,21,25,27,30,36,41,43,47,53,57,61,65,67,71,76,79,83,87,91,94,96]
TITLES=['왜 아래쪽은 모두 0일까?','숫자의 구조 ↔ 공간의 구조','세 개의 선형독립 벡터','서로 직교하는 단위벡터','첫 벡터에는 첫 방향만','나머지 두 계수는 왜 0일까?','첫 벡터와 수직인 두 방향','각 방향의 계수 = 내적','내적의 0이 행렬의 0으로','두 번째 벡터의 계수','두 방향으로 벡터 복원','평면에 수직이면 내적은 0','세 번째 벡터의 세 성분','계수들을 열 순서대로','위삼각행렬의 완성','무엇이 그대로 유지될까?','길이가 달라도 같은 직선','벡터가 달라도 같은 평면','두 기저가 만드는 같은 공간','직선 ⊂ 평면 ⊂ 공간','공간을 유지하며 기준 바꾸기','공간의 직교 관계가 만든 0','뒤 방향은 앞 공간에 수직','수직 관계를 기록한 계수','위삼각 구조에 담긴 기하학']
def screen(s):
    for a,b in [('큐 원','q₁'),('큐 투','q₂'),('큐 쓰리','q₃'),('에이 원','a₁')]:s=s.replace(a,b)
    return s
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    if not (P/'scenes.yaml').exists():shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
    cues=[];start=0
    for line in RAW.splitlines():
        end,s=line.split('|',1);end=int(end);cues.append(dict(start=start,end=end,tts=s,caption=screen(s)));start=end
    for name,obj in [('timing.json',cues),('project.json',dict(duration=98,ending_confirmed=True))]:(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(c['tts'] for c in cues)+'\n',encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    narration='# QR 2편 — 왜 R의 아래쪽은 모두 0일까?\n\n사용자 확정 원고·문장 종료 시각. 총 98초, 음원 미제공.\n\n| 시작 | 종료 | 내레이션 |\n|---|---|---|\n'+'\n'.join(f'| {c["start"]} | {c["end"]} | {c["caption"]} |' for c in cues)+'\n'
    for name in ['narration.md','master_script.md']:(P/name).write_text(narration,encoding='utf-8')
    manifest=[]
    for i,(start,title) in enumerate(zip(STARTS,TITLES)):
        end=STARTS[i+1] if i+1<len(STARTS) else 98
        directory=f'scenes/{i+1:02}_scene';d=P/directory;d.mkdir(parents=True,exist_ok=True)
        manifest.append(dict(id=f'{i+1:02}',directory=directory,**{'class':'QRShot'},start=start,end=end,duration_seconds=end-start,title=title))
        (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import QRBase\nclass QRShot(QRBase):\n    INDEX = '+str(i)+'\n',encoding='utf-8')
        (d/'script.txt').write_text('\n\n'.join(c['tts'] for c in cues if c['start']<end and c['end']>start)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} {title}\n\n- 주장: {title}\n- 전체 시각 {start}–{end}초, 길이 {end-start}초.\n- 화면: storyboard.md 컷 {i+1:02}, visuals.py INDEX {i}.\n- 좌표: a₁=(1,1,0), a₂=(0,2,0), a₃=(1,2,2). 세 벡터는 선형독립.\n- Q는 양의 대각 규약의 순서 보존 직교화 결과.\n- 자막·발화는 상위 timing.json을 공유한다. 컷 경계를 가로지르는 문장은 중복 발화하지 않는다.\n- 음원 미제공으로 무음 visual을 사용.\n- 각 컷은 같은 좌표계와 색상·수식 배치를 유지하며 독립 교체 가능.\n',encoding='utf-8')
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('title: QR 2편 — 위삼각 구조\nduration_seconds: 98\ntiming_source: user_sentence_end_times\naudio: not_supplied\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    source: {m["directory"]}/scene.py\n    class: QRShot\n    start: {m["start"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    prev=P.parent/'qr01_new_directions'
    (P/'build.py').write_text((prev/'build.py').read_text(encoding='utf-8').replace('qr01_new_directions','qr02_triangular_structure'),encoding='utf-8')
    s=(prev/'visuals.py').read_text(encoding='utf-8').split('    def shot(self):')[0]
    s=s.replace('A3=np.array([1.,1,2])','A3=np.array([1.,2,2])').replace('QR / 01     새로운 방향을 찾아서','QR / 02     수직 관계가 만드는 0')
    s=s.replace("'도입: 평면 위 종속 사례' if self.INDEX<7 else '본 계산: 선형독립인 세 벡터'","'선형독립인 열벡터 · 순서를 보존하는 QR'")
    s=s.replace("if 7<=self.INDEX<=12 and t=='z':continue","if self.INDEX in [4,7,8,9,10] and t=='z':continue")
    # Keep labels away from the larger original vectors and the panel header.
    s=s.replace("if name=='q₁':offset=np.array([.05,-.38,0])","if name=='q₁':offset=np.array([.05,-.38,0])\n            if name=='q₂':offset=np.array([-.32,.12,0])")
    s=s.replace("self.center=np.array([-.6,.35,0]) if SHORT else np.array([-3.9,-.4,0])","self.center=np.array([-.6,1.,0]) if SHORT else np.array([-3.9,-.5,0])")
    s=s.replace("self.scale3=1.65 if SHORT else 1.25","self.scale3=1.45 if SHORT else 1.15")
    (P/'base.py').write_text(s,encoding='utf-8')
if __name__=='__main__':main()
