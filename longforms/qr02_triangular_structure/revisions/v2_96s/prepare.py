from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent
OLD=P.parents[1]
RAW='''4|QR 분해에서 행렬 R은 왜 대각선 아래쪽이 모두 0일까요?
7|아무런 방향도 없는 원점 하나를 생각해 보겠습니다.
9|여기에 첫 번째 벡터를 추가합니다.
12|이 벡터를 따라 움직이면 하나의 직선이 만들어집니다.
16|이 직선을 표현하기 위해서는 하나의 기준 방향만 있으면 됩니다.
19|이제 두 번째 벡터를 추가해 보겠습니다.
25|두 번째 벡터가 첫 번째 직선에서 벗어나 있다면, 두 벡터의 조합으로 하나의 평면을 만들 수 있습니다.
30|직선에서는 앞뒤로만 움직일 수 있었지만, 이제 평면 위의 모든 방향으로 움직일 수 있습니다.
34|이 평면을 표현하려면 서로 수직인 두 개의 기준 방향이 필요합니다.
38|첫 번째 방향을 큐 원, 두 번째 방향을 큐 투라고 하겠습니다.
40|이번에는 세 번째 벡터를 추가해 보겠습니다.
47|이 벡터가 기존 평면 밖으로 뻗어나간다면, 이제 세 방향을 조합해 3차원 공간 전체를 표현할 수 있습니다.
51|평면에 수직인 새로운 기준 방향을 큐 쓰리라고 하겠습니다.
53|이제 처음의 벡터들을 다시 살펴보겠습니다.
58|첫 번째 벡터는 하나의 직선 위에 있으므로 큐 원 방향만으로 표현됩니다.
63|두 번째 벡터는 평면 위에 있으므로 큐 원과 큐 투, 두 방향으로 표현됩니다.
66|세 번째 벡터는 세 방향 모두를 사용할 수 있습니다.
69|이 조합의 계수들을 열 순서대로 정리해 보겠습니다.
75|첫 번째 열에는 하나, 두 번째 열에는 최대 두 개, 세 번째 열에는 최대 세 개의 계수가 들어갑니다.
78|그리고 사용되지 않는 방향의 계수는 모두 0입니다.
81|이렇게 만들어진 것이 바로 위삼각행렬 R입니다.
90|QR 분해는 원래 벡터들이 만들어가는 직선과 평면, 공간을 그대로 유지하면서, 그 기준을 서로 직교하는 방향들로 다시 표현합니다.
96|R의 아래쪽에 나타나는 0들은 공간이 한 차원씩 확장되어 온 순서가 행렬에 남긴 흔적입니다.'''
STARTS=[0,4,7,9,12,16,19,25,30,34,38,40,44,47,51,53,58,63,66,69,75,78,81,90]
TITLES=['왜 아래쪽만 0일까?','0차원 · 원점','첫 번째 벡터 추가','하나의 방향이 만드는 직선','직선에는 기준 방향 하나','두 번째 벡터 추가','직선을 벗어나면 평면으로','평면 위의 모든 방향으로','기존 성분을 빼고 새 방향 찾기','평면의 직교 기준 q₁과 q₂','세 번째 벡터 추가','기존 평면 밖의 새로운 성분','평면에서 3차원 공간으로','평면에 수직인 기준 q₃','원래 벡터를 다시 표현하면','첫 벡터는 한 방향으로','둘째 벡터는 두 방향으로','셋째 벡터는 세 방향으로','벡터의 계수 → 행렬의 열','직선 · 평면 · 공간의 계수','수직인 방향의 계수는 0','위삼각행렬 R의 완성','같은 공간 · 서로 다른 기준','공간의 확장 순서가 남긴 흔적']
def screen(s):
    for a,b in [('큐 원','q₁'),('큐 투','q₂'),('큐 쓰리','q₃')]:s=s.replace(a,b)
    return s
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    cues=[];start=0
    for line in RAW.splitlines():
        end,s=line.split('|',1);end=int(end);cues.append(dict(start=start,end=end,tts=s,caption=screen(s)));start=end
    for name,obj in [('timing.json',cues),('project.json',dict(duration=96,ending_confirmed=True,revision='v2',supersedes='98s original'))]:(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'tts_script.txt').write_text('\n\n'.join(c['tts'] for c in cues)+'\n',encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    text='# QR 2편 — 96초 수정본 v2\n\n사용자 확정 새 대본·종료 시각. 이전 98초 대본과 구분.\n\n| 시작 | 종료 | 내레이션 |\n|---|---|---|\n'+'\n'.join(f'| {c["start"]} | {c["end"]} | {c["caption"]} |' for c in cues)+'\n'
    for name in ['narration.md','master_script.md']:(P/name).write_text(text,encoding='utf-8')
    manifest=[]
    for i,(start,title) in enumerate(zip(STARTS,TITLES)):
        end=STARTS[i+1] if i+1<len(STARTS) else 96;directory=f'scenes/{i+1:02}_scene';d=P/directory;d.mkdir(parents=True,exist_ok=True)
        manifest.append(dict(id=f'{i+1:02}',directory=directory,**{'class':'QRShot'},start=start,end=end,duration_seconds=end-start,title=title))
        (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import QRBase\nclass QRShot(QRBase):\n    INDEX = '+str(i)+'\n',encoding='utf-8')
        (d/'script.txt').write_text('\n\n'.join(c['tts'] for c in cues if c['start']<end and c['end']>start)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} {title}\n\n- 주장: {title}\n- 新 대본 시각 {start}–{end}초, 길이 {end-start}초. 이전 98초 시각 미사용.\n- 화면: storyboard.md 컷 {i+1:02}, visuals.py INDEX {i}.\n- 원점·직선·평면을 유지하며 독립 방향을 추가한다.\n- a₁=(1,1,0), a₂=(0,2,0), a₃=(1,2,2), 열 전체 계수·양의 대각 규약.\n- 발화는 상위 timing.json에서 한 번만 진행하며 컷 경계 문장을 중복하지 않는다.\n- 음원 미제공, 무음·자막 최종본.\n',encoding='utf-8')
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('title: QR 2편 96초 v2\nduration_seconds: 96\ntiming_source: revised_user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    source: {m["directory"]}/scene.py\n    class: QRShot\n    start: {m["start"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    (P/'build.py').write_text((OLD/'build.py').read_text(encoding='utf-8').replace('qr02_triangular_structure','qr02_triangular_structure_v2'),encoding='utf-8')
    s=(OLD/'base.py').read_text(encoding='utf-8').replace('QR / 02     수직 관계가 만드는 0','QR / 02     공간의 확장과 위삼각 구조')
    (P/'base.py').write_text(s,encoding='utf-8')
    helper=(OLD/'visuals.py').read_text(encoding='utf-8').split('    def shot(self):')[0].replace('class QRBase(SharedBase):','class Helpers(SharedBase):')
    (P/'helpers.py').write_text(helper,encoding='utf-8')
    s=(OLD/'verify_final.py').read_text(encoding='utf-8').replace('qr02_triangular_structure','qr02_triangular_structure_v2').replace('2940','2880').replace('98','96')
    s=s.replace('WORK=P.parents[1]',"WORK=next(p for p in P.parents if (p/'scripts/render.py').exists())")
    s=s.replace('TIMES=[2,12,18,24,29,34,40,45,51,56,60,64,69,74,78,85,90,93,97]','TIMES=[2,5,8,11,15,23,28,33,37,42,46,50,56,61,65,68,72,77,80,84,88,94]')
    (P/'verify_final.py').write_text(s,encoding='utf-8')
    shutil.copy2(OLD/'math_verification.json',P/'math_verification_previous_geometry.json')
if __name__=='__main__':main()
