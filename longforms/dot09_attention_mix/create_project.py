"""Approved 154-second narration, clocks and independent scene contracts."""
import json,re,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
RAW='''인공지능은 여러 정보 중 어떤 정보에 더 주목해야 할지 어떻게 결정할까요?|4
이번에는 내적이 신경망에서 어떻게 사용되는지 살펴보겠습니다.|8
트랜스포머에서는 어텐션이라는 연산을 이용해 여러 정보의 중요도를 계산하고 결합합니다.|14
예를 들어 고양이가 소파에 앉았고, 그것이 잠들었다는 문장을 생각해 보겠습니다.|18
여기서 '그것'이라는 단어를 처리할 때, 앞서 등장한 고양이와 소파의 정보를 서로 다른 비율로 참고할 수 있습니다.|25
이 과정에서 세 종류의 벡터가 등장합니다.|28
큐어리, 키, 밸류입니다.|29
큐어리는 현재 어떤 정보를 찾는지 나타내는 벡터입니다.|33
키는 각 정보와 비교하기 위한 벡터이고, 밸류는 실제로 결합할 정보를 담는 벡터입니다.|39
그렇다면 어떤 정보를 더 많이 참고할지 어떻게 계산할까요?|42
여기서 내적이 등장합니다.|44
계산을 단순하게 하기 위해 2차원 벡터를 사용하겠습니다.|48
큐어리가 2와 1이고, 두 개의 키가 각각 1과 1, 그리고 0과 2라고 해보겠습니다.|53
먼저 큐어리와 첫 번째 키를 내적하면 2 곱하기 1, 더하기 1 곱하기 1로 3이 나옵니다.|59
두 번째 키와 내적하면 2 곱하기 0, 더하기 1 곱하기 2로 2가 나옵니다.|64
이렇게 내적을 이용해 각 정보에 대한 점수를 구할 수 있습니다.|67
이번 예제에서는 첫 번째 정보의 점수가 더 높습니다.|70
하지만 이 점수를 그대로 사용하는 것은 아닙니다.|73
어텐션에서는 키 벡터의 차원 수의 제곱근으로 점수를 나눕니다.|77
이를 스케일링이라고 합니다.|79
그리고 스케일링한 점수들에 소프트맥스를 적용합니다.|82
그러면 두 점수는 합이 1인 가중치로 바뀝니다.|85
이번 예제에서는 첫 번째 정보에 약 67퍼센트, 두 번째 정보에 약 33퍼센트의 가중치가 주어집니다.|93
그렇다면 이 가중치로 무엇을 할까요?|95
여기서 밸류 벡터가 사용됩니다.|97
첫 번째 밸류를 4와 0, 두 번째 밸류를 0과 2라고 하겠습니다.|101
각 밸류에 앞에서 구한 가중치를 곱합니다.|104
첫 번째는 약 2.68과 0, 두 번째는 0과 0.66이 됩니다.|109
이 두 벡터를 더하면 약 2.68과 0.66이라는 새로운 출력 벡터가 만들어집니다.|115
즉, 어텐션은 내적으로 정보 간의 점수를 계산하고, 그 점수를 이용해 여러 정보를 서로 다른 비율로 결합하는 연산입니다.|123
그런데 앞서 배운 정사영과는 중요한 차이가 있습니다.|126
정사영에서는 단위벡터와 내적해 특정 방향의 성분을 추출했습니다.|131
반면 어텐션에서는 학습된 큐어리와 키를 내적해 점수를 구하고, 별도의 밸류 벡터들을 결합합니다.|137
따라서 어텐션의 내적값은 반드시 정사영의 성분을 의미하지는 않습니다.|142
또한 점수는 벡터 사이의 각도뿐 아니라 길이에도 영향을 받습니다.|146
결국 내적은 방향의 성분을 측정하는 데서 출발해, 신경망이 여러 정보의 연관성을 평가하고 결합하는 계산으로까지 확장됩니다.|154'''
CUTS=[
 (0,14,'어떤 정보를 더 참고할까?','Attention은 여러 정보의 점수를 가중치로 바꾸어 결합한다.','0–4초 정보카드와 같은 굵기 연결. 4–8초 내적 기호와 점수 물음표. 8–14초 개념적 연결 굵기 차이·Attention 용어.'),
 (14,25,'문장 속 정보 참조 관계','현재 처리하는 그것은 앞선 정보를 서로 다른 비율로 참고할 수 있다.','14–18초 문장과 고양이·소파·그것 카드. 18–25초 현재 단어에서 두 정보로 연결. 개념도이며 숫자 가중치나 실제 토큰 경계를 주장하지 않는다.'),
 (25,39,'Query · Key · Value','Q는 비교 기준, K는 점수 비교 대상, V는 결합할 정보다.','25–29초 세 벡터 역할. 29–33초 Q 강조. 33–39초 같은 정보에서 온 K와V를 별도 카드로 구별.'),
 (39,53,'가상의 2차원 벡터 예제','q=(2,1), k₁=(1,1), k₂=(0,2)를 같은 좌표평면에 그린다.','39–42초 Q와K의 물음표. 42–44초 내적 기호. 44–48초 2차원 고정축. 48–53초 세 좌표와 벡터. 문장 예시와 분리된 가상 수치 예제임을 표시.'),
 (53,70,'내적이 정보의 점수가 된다','q·k₁=3, q·k₂=2는 가중치가 아닌 원점수다.','53–59초 k₁만 강조·성분곱. 59–64초 k₂만 강조·성분곱. 64–67초 두 점수 카드. 67–70초 원점수 막대3:2. 퍼센트 표기 없음.'),
 (70,79,'먼저 차원에 맞춰 스케일링','dₖ=2이므로 점수를 √2로 나눈다.','70–73초3,2 원점수. 73–77초 나누기√2와 동시 수치변화. 77–79초2.1213,1.4142 및 일반식. 아직 확률이나 가중치가 아님.'),
 (79,93,'Softmax · 합이 1인 가중치','softmax(3/√2,2/√2)≈(0.6698,0.3302).','79–82초 scaled 점수→softmax. 82–85초 가중치막대. 85–93초67.0%,33.0%, 하나의100%막대. 원점수3:2와 구별.'),
 (93,115,'가중치는 별도의 Value에 적용한다','v₁=(4,0),v₂=(0,2)의 가중합은 약(2.68,0.66)이다.','93–95초 가중치 유지·용도질문. 95–97초 Value영역 전환. 97–101초 두Value. 101–104초 정확한 α만큼 축소. 104–109초 각가중벡터. 109–112초 둘째벡터를 첫끝점에 연결. 112–115초 출력벡터 생성.'),
 (115,123,'점수 → 가중치 → 정보 결합','Attention(Q,K,V)=softmax(QKᵀ/√dₖ)V.','115–120초3,2→scaled softmax→Value출력. 120–123초 행이Query인 행렬식과 각Query행에softmax 적용. 세 단계의 데이터 전달 강조.'),
 (123,146,'정사영과 Attention의 차이','단위방향의 성분 추출과 학습된 벡터의 점수·별도Value결합을 구별한다.','123–126초 정사영 도형. 126–131초p=(x·u)u,‖u‖=1,직교잔차. 131–137초QK점수와별도V. 137–142초역할차이·직교조건 일반적보장없음. 142–146초같은각도에서k길이만1→2배,점수3→6.'),
 (146,154,'내적 · 정보의 비교에서 결합으로','내적점수를 가중치로 바꾸어 여러Value를 합친다.','146–154초가상예제Q와K연결·67%,33%가중치·별도Value→출력. 문장예시카드는재사용하지않고 본편결론으로완결.')]
CONTRACT='q=(2,1), K의 행은 k₁=(1,1),k₂=(0,2). dₖ=2, 원점수(3,2), scaled=(3/√2,2/√2). 안정적softmax로 정확한 α계산, α합1. Value행은(4,0),(0,2). o=αV≈(2.679046,0.660477), 표시(2.68,0.66). 막대·화살표·수식은 동일한 정확한 α를 사용하고 표시만 반올림. 문장예시는측정데이터가아닌개념도이며67%,33%를고양이·소파에붙이지않음. Q,K는학습된비교벡터이며단위벡터조건없음. 점수는각도와길이에영향, 일반적으로코사인유사도나정사영성분이아님. 정사영잔차직교성과Attention가중합을동일시하지않음. 행렬식softmax는각Query행별. 마스크·multihead는본편범위밖으로추가하지않음.'
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def spoken(s):
    for a,b in [('2차원','이차원'),('67','육십칠'),('33','삼십삼'),('2.68','이 점 육팔'),('0.66','영 점 육육')]:s=s.replace(a,b)
    return re.sub(r'\d+',lambda m:{'0':'영','1':'일','2':'이','3':'삼','4':'사'}.get(m[0],m[0]),s)
def main():
    shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\99b419da-ae24-4446-819c-70ee7fe4fb25\붙여넣은 텍스트.txt'),P/'storyboard.md')
    cues=[];start=0
    for row in RAW.splitlines():
        caption,end=row.rsplit('|',1);end=int(end);cues.append(dict(start=start,end=end,caption=caption));start=end
    assert len(cues)==36 and start==154
    (P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    script='\n\n'.join('\n'.join(c['caption'] for c in cues if s<=c['start']<e) for s,e,*_ in CUTS)+'\n'
    (P/'master_script.md').write_text('# 내적 LEVEL 09 — Attention\n\n사용자 확정 원고36문장, 제공 종료시각 기준154초.\n\n'+script,encoding='utf-8')
    (P/'tts_script.txt').write_text(spoken(script),encoding='utf-8')
    (P/'narration.md').write_text('# 문장별 내레이션\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n{c["caption"]}' for c in cues),encoding='utf-8')
    (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    manifest=[]
    for i,(s,e,title,claim,animation) in enumerate(CUTS):
        directory=f'scenes/{i+1:02}_scene';d=P/directory;shutil.copytree(P.parent/'_template/scenes/01_example',d,dirs_exist_ok=True)
        original='\n'.join(c['caption'] for c in cues if s<=c['start']<e)
        (d/'script.txt').write_text(spoken(original)+'\n',encoding='utf-8')
        (d/'spec.md').write_text(f'# {i+1:02} — {title}\n\n## 목적과 핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+(CUTS[i-1][3] if i else '없음. 본편 질문.')+f'\n\n## TTS와 확정 길이\n사용자 제공 {s}–{e}초, {e-s}초. 음원 미제공.\n\n{original}\n\n## 화면 구성\n토큰개념도→QK벡터·점수→가중치→Value가중합을 구별. 세로 도형 위·수식 아래, 가로 도형 왼쪽·수식 오른쪽. 자막 영역 별도. 파랑Q,초록K₁/V₁,보라K₂/V₂,주황점수,청록가중치,밝은파랑출력.\n\n## 구간별 애니메이션·텍스트\n{animation}\n\n## 시작·종료 상태와 다음 연결\n'+(CUTS[i+1][3] if i+1<len(CUTS) else '내적점수와Value결합으로본편독립완결.')+'\n\n## 수학적 조건\n'+CONTRACT+'\n',encoding='utf-8')
        (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import AttentionBase\nclass Attention{i+1:02}(AttentionBase):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=directory,start=s,end=e,duration_seconds=e-s,title=title,**{'class':f'Attention{i+1:02}'}))
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/'scenes.yaml').write_text('duration_seconds: 154\ntiming_source: user_sentence_end_times\nlayouts:\n  shorts: [1080, 1920, 30]\n  longform: [1920, 1080, 30]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
    (P/'brief.md').write_text('# 내적 LEVEL 09 — 제작 기준\n\n154초, 사용자 확정36문장과 종료시각. 11개 독립씬. 세로1080×1920,가로1920×1080,30fps. 음원미제공으로무음·자막.\n\n'+CONTRACT+'\n\n요청대본의정사영비교만유지하고추가복습·예고는넣지않는다.\n',encoding='utf-8')
if __name__=='__main__':main()

