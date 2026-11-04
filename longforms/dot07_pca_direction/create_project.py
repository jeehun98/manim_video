"""Create contracts from the user's approved 149-second narration."""
import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''여러 개의 데이터를 하나의 방향으로만 표현해야 한다면, 어떤 방향을 선택하는 것이 가장 좋을까요?|5
이번에는 내적과 정사영을 이용해 그 방향을 찾아보겠습니다.|9
2차원 좌표평면에 여러 데이터가 흩어져 있습니다.|12
이 점들을 하나의 직선 위에 표현한다면, 숫자 하나만으로 각 데이터의 위치를 나타낼 수 있습니다.|18
그런데 어떤 직선을 선택하느냐에 따라 잃어버리는 정보가 달라집니다.|22
수평 방향으로 정사영하면 세로 성분이 제거되고, 수직 방향으로 정사영하면 가로 성분이 제거됩니다.|29
그렇다면 원래 데이터를 가장 잘 보존하는 방향은 무엇일까요?|33
먼저 데이터의 평균을 원점으로 옮기겠습니다. 이것을 중심화라고 합니다.|38
이제 길이가 1인 기준벡터를 선택하겠습니다.|41
각 데이터와 이 벡터를 내적하면 해당 방향의 성분을 숫자로 측정할 수 있습니다.|46
이 값에 다시 단위벡터를 곱하면 정사영 벡터가 만들어집니다.|50
하지만 원래 데이터와 정사영 사이에는 제거된 성분, 즉 잔차가 남습니다.|55
우리는 모든 잔차의 길이를 제곱해 더한 값이 가장 작아지는 방향을 찾고 싶습니다.|60
그런데 여기서 중요한 관계가 나타납니다.|63
원래 벡터는 정사영 성분과 그에 직교하는 잔차로 나뉩니다.|67
따라서 피타고라스 정리에 의해 원래 벡터의 길이 제곱은 두 성분의 길이 제곱을 더한 값입니다.|73
즉, 잔차의 길이 제곱은 원래 벡터의 길이 제곱에서 정사영 성분의 길이 제곱を 뺀 값입니다.|79
이 관계를 모든 데이터에 적용해 보겠습니다.|82
원래 데이터들의 길이 제곱합은 방향을 바꿔도 일정합니다.|85
따라서 잔차의 제곱합을 최소화하려면 정사영한 성분들의 제곱합을 최대화해야 합니다.|91
그런데 정사영한 성분의 크기는 단위벡터와 내적한 값의 절댓값입니다.|96
데이터를 중심화했으므로 내적값들의 평균은 0입니다.|99
따라서 내적값들의 제곱합을 데이터 개수로 나누면, 그 방향으로 투영된 데이터의 분산이 됩니다.|106
결국 재구성 오차를 최소화하는 방향과 투영 분산을 최대화하는 방향은 같습니다.|111
이것이 주성분 분석, PCA의 핵심 원리입니다.|114
그렇다면 최적의 방향은 어떻게 구할까요?|117
중심화된 데이터로 공분산행렬을 만들면, 특정 방향의 분산을 행렬과 벡터의 곱으로 표현할 수 있습니다.|123
이 분산을 최대화하는 단위벡터는 공분산행렬의 가장 큰 고윳값에 대응하는 고유벡터입니다.|129
이것을 첫 번째 주성분이라고 합니다.|131
앞서 최소제곱법에서는 주어진 공간 안에서 목표에 가장 가까운 결과를 찾았습니다.|137
반면 PCA에서는 데이터를 가장 잘 표현하는 공간의 방향 자체를 찾습니다.|141
내적으로 방향의 성분을 측정하는 원리가, 데이터의 정보를 최대한 보존하는 방향을 찾는 방법으로 확장된 것입니다.|149'''.replace('제곱を','제곱을')
CUTS=[(0,9,'데이터를 담을 하나의 방향','하나의 직선으로 데이터를 표현하는 방향을 선택한다.'),(9,29,'방향에 따라 사라지는 정보','수평·수직 투영은 서로 다른 성분을 제거한다.'),(29,38,'평균을 원점으로 · 중심화','모든 데이터를 같은 평균벡터만큼 평행이동한다.'),(38,55,'내적 → 정사영 → 잔차','단위방향의 내적 c를 다시 u에 곱해 p를 만든다.'),(55,63,'가장 작은 재구성 오차','잔차 길이 제곱의 합 E를 최소화한다.'),(63,79,'직교하는 두 성분과 피타고라스','각 데이터에 대해 ‖x‖²=‖p‖²+‖r‖²이다.'),(79,91,'전체 에너지는 일정하다','E=T−V이므로 E의 최소와 V의 최대는 같다.'),(91,106,'내적값의 제곱합에서 분산으로','중심화된 내적값의 분산은 V/n이다.'),(106,114,'오차 최소 = 분산 최대','하나의 방향 선택을 두 관점에서 해석한다.'),(114,129,'공분산행렬이 알려주는 방향','uᵀΣu의 최대는 가장 큰 고윳값이다.'),(129,141,'첫 번째 주성분이 찾는 것','최소제곱은 고정 공간에서, PCA는 공간 방향 자체를 찾는다.'),(141,149,'정보를 가장 잘 보존하는 방향','내적으로 측정한 성분으로 최적의 1차원 표현을 만든다.')]
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def spoken(s):return s.replace('PCA','피 씨 에이').replace('2차원','이차원').replace('0입니다','영입니다').replace('1인','일인')
def main():
    shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\089d9f75-f627-4d71-967b-e0bc4543f10c\붙여넣은 텍스트.txt'),P/'storyboard.md')
    cues=[];start=0
    for row in RAW.splitlines():
        caption,end=row.rsplit('|',1);end=int(end);cues.append(dict(start=start,end=end,caption=caption));start=end
    assert len(cues)==32 and start==149
    (P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    script='\n\n'.join('\n'.join(c['caption'] for c in cues if s<=c['start']<e) for s,e,*_ in CUTS)+'\n'
    (P/'master_script.md').write_text('# 내적 LEVEL 07 — PCA\n\n사용자 확정 원고, 문장 종료 시각32개, 총149초.\n\n'+script,encoding='utf-8')
    (P/'tts_script.txt').write_text(spoken(script),encoding='utf-8')
    (P/'narration.md').write_text('# 문장별 내레이션\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n{c["caption"]}' for c in cues),encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    manifest=[]
    contract='같은16개 데이터와 고정된 좌표축·배율. 중심화 이후 데이터는 움직이지 않고 u와 정사영만 회전. 파랑x, 초록u, 주황p, 보라r. ‖u‖=1, c=x·u, p=cu, r=x−p. E=Σ‖r‖², V=Σc², T=Σ‖x‖², E+V=T. Σ=(1/n)Σxxᵀ, 분산=V/n=uᵀΣu. 표본분산 n−1과 혼용하지 않는다. 가장 큰 고윳값은 단순하며 ±u는 같은 직선을 표현한다.'
    for i,(s,e,title,claim) in enumerate(CUTS):
        directory=f'scenes/{i+1:02}_scene';d=P/directory;shutil.copytree(P.parent/'_template/scenes/01_example',d,dirs_exist_ok=True)
        original='\n'.join(c['caption'] for c in cues if s<=c['start']<e)
        (d/'script.txt').write_text(spoken(original)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+(CUTS[i-1][3] if i else '없음. 본편 질문.')+f'\n\n## TTS와 확정 길이\n사용자 제공 {s}–{e}초, {e-s}초. 음원 미제공.\n\n{original}\n\n## 화면·애니메이션·텍스트\n첨부 storyboard.md의 해당 시간대 연출을 구현. 세로 도형 위·수식 아래, 가로 도형 왼쪽·수식 오른쪽. 각 문장 종료 시각에서 수식과 강조 전환.\n\n## 시작·종료 상태와 다음 연결\n'+(CUTS[i+1][3] if i+1<len(CUTS) else '최적 방향과 재구성으로 독립 완결.')+'\n\n## 수학적 조건\n'+contract+'\n',encoding='utf-8')
        (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import PCABase\nclass PCA{i+1:02}(PCABase):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=directory,start=s,end=e,duration_seconds=e-s,title=title,**{'class':f'PCA{i+1:02}'}))
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('duration_seconds: 149\ntiming_source: user_sentence_end_times\nlayouts:\n  shorts: [1080, 1920, 30]\n  longform: [1920, 1080, 30]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    (P/'brief.md').write_text('# 내적 LEVEL 07 — 제작 기준\n\n149초, 사용자 문장 종료 시각32개. 세로1080×1920 및 가로1920×1080,30fps. 무음·자막. 12개 교체 가능한 독립 씬.\n\n'+contract+'\n\n중심화→측정→추출→잔차→피타고라스→에너지 보존→분산→공분산 고유벡터. 요청 원문의 최소제곱 비교만 유지하며 추가 복습·예고 없음.\n',encoding='utf-8')
if __name__=='__main__':main()
