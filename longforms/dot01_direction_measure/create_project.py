"""Materialize the supplied, approved 102-second script and scene contracts."""
import json,shutil,re
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''두 벡터를 곱하면 무엇이 나올까요?|2
이번에는 가장 기본적인 벡터 연산 중 하나인 내적을 살펴보겠습니다.|6
내적은 영어로 닷 프로덕트, Dot Product라고 합니다.|9
두 벡터의 대응하는 원소끼리 곱한 다음, 모두 더하는 연산입니다.|13
예를 들어 첫 번째 벡터가 3, 4이고 두 번째 벡터가 1, 0이라면,|18
3 곱하기 1, 더하기 4 곱하기 0.|20
결과는 3입니다.|21
그런데 이 숫자는 무엇을 의미할까요?|24
먼저 벡터에는 방향과 길이가 있습니다.|26
가로로 3, 세로로 4만큼 향하는 벡터의 길이는 피타고라스 정리를 이용해 5라는 것을 알 수 있습니다.|33
이번에는 이 벡터의 길이만 1로 줄여보겠습니다.|36
각 성분을 전체 길이인 5로 나누면, 0.6과 0.8이 됩니다.|40
이렇게 방향은 그대로 유지하고 길이를 1로 만든 벡터를 단위벡터라고 합니다.|45
이제 원래 벡터와 이 단위벡터를 내적해 보겠습니다.|49
3 곱하기 0.6은 1.8.|51
4 곱하기 0.8은 3.2.|53
두 값을 더하면 결과는 5입니다.|55
바로 원래 벡터의 길이입니다.|57
즉, 같은 방향의 단위벡터와 내적하면 원래 벡터의 길이를 측정할 수 있습니다.|62
그렇다면 기준 방향을 바꾸면 어떻게 될까요?|65
오른쪽을 향하는 단위벡터, 1과 0을 사용하면 내적은 3입니다.|69
이번에는 위쪽을 향하는 단위벡터, 0과 1을 사용하면 결과는 4입니다.|74
원래 벡터는 움직이지 않았지만, 어떤 방향을 기준으로 측정하느냐에 따라 결과가 달라집니다.|80
같은 방향에서는 전체 길이를 측정하고, 기울어진 방향에서는 그 방향으로 뻗어 있는 성분을 측정하는 것입니다.|86
그리고 기준 방향과 수직이라면 내적은 0이 됩니다.|90
결국 단위벡터와의 내적은 특정 방향을 기준으로 벡터가 얼마나 뻗어 있는지를 하나의 숫자로 나타냅니다.|96
내적은 단순히 숫자들을 곱하고 더하는 공식이 아니라, 방향을 기준으로 성분을 측정하는 연산입니다.|102'''
cuts=[(0,13,'내적의 계산 규칙'),(13,24,'계산한 숫자 3의 의미'),(24,33,'방향과 길이'),(33,45,'길이가 1인 기준'),(45,62,'같은 방향에서 측정한 길이'),(62,74,'기준 방향을 바꾸면'),(74,90,'방향에 따라 달라지는 성분'),(90,102,'방향을 기준으로 성분을 측정한다')]
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def spoken(s):
    s=s.replace('Dot Product','닷 프로덕트')
    words={'0.6':'영 점 육','0.8':'영 점 팔','1.8':'일 점 팔','3.2':'삼 점 이','0':'영','1':'일','2':'이','3':'삼','4':'사','5':'오'}
    return re.sub(r'\d+(?:\.\d+)?',lambda m:words.get(m[0],m[0]),s)
def main():
    cues=[];start=0
    for line in RAW.splitlines():
        caption,end=line.rsplit('|',1);end=int(end);cues.append(dict(start=start,end=end,caption=caption));start=end
    (P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    script='\n\n'.join('\n'.join(c['caption'] for c in cues if s<=c['start']<e) for s,e,_ in cuts)+'\n'
    (P/'tts_script.txt').write_text(spoken(script),encoding='utf-8')
    (P/'master_script.md').write_text('# 내적 LEVEL 01 — 방향을 측정하는 연산\n\n사용자 제공 확정 대본·문장 종료 시각, 총 102초.\n\n'+script,encoding='utf-8')
    (P/'narration.md').write_text((P/'master_script.md').read_text(encoding='utf-8'),encoding='utf-8')
    manifest=[]
    for i,(s,e,title) in enumerate(cuts):
        d=P/'scenes'/f'{i+1:02}_scene';shutil.copytree(P.parent/'_template/scenes/01_example',d,dirs_exist_ok=True)
        speech='\n'.join(c['caption'] for c in cues if s<=c['start']<e)
        (d/'script.txt').write_text(spoken(speech)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n## 목적·주장\n{title}. 첨부 상세 콘티의 대응 구간을 구현한다.\n\n## 확정 시간\n{s}–{e}초, 길이 {e-s}초. 사용자 제공 문장 종료 시각 기준.\n\n## 화면·애니메이션\n파란 x=(3,4), 초록 기준벡터, 주황 측정 성분. 같은 좌표 스케일과 원점 유지. 상단 개념, 중앙 좌표, 별도 계산 영역, 하단 자막.\n\n## TTS\n{speech}\n\n## 시작·종료 상태와 연결\n직전 구간의 좌표계와 벡터 상태를 이어받는다. 다음 컷의 초기 상태와 일치하도록 종료한다.\n\n## 정확성\n단위벡터 길이 1; 원래 벡터 길이 5. 내적은 스칼라이고 주황 선은 대응하는 방향 성분의 도식이다. 수직 기준은 (-0.8,0.6).\n',encoding='utf-8')
        (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import DotBase\nclass Dot{i+1:02}(DotBase):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=f'scenes/{i+1:02}_scene',start=s,end=e,duration_seconds=e-s,title=title,**{'class':f'Dot{i+1:02}'}))
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('scenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    (P/'brief.md').write_text('# 제작 기준\n\n102초, 9:16 쇼츠 / 16:9 롱폼, 30fps. 사용자 제공 대본과 문장 종료 시각을 그대로 적용. 음원 미제공으로 무음 자막 영상.\n\n내적 계산→3-4-5 길이→단위벡터→같은 방향에서 5→가로 3·세로 4→수직 0→성분 측정이라는 결론. 이전 편 복습·다음 편 예고 없음.\n\n원래 x는 고정. 정규화는 복제한 기준 화살표를 축소한다. 초록 벡터는 단위벡터로 확정한 뒤 항상 길이 1을 유지. 회전은 제공 발화시각 74초의 세로 상태에서 시작한다.\n',encoding='utf-8')
if __name__=='__main__':main()
