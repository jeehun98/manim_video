import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LINES=[
('행렬 분해 이상형 월드컵!',1),('EVD 대 SVD.',3),('드디어 마지막 시간입니다.',4),
('지금까지 일곱 번의 대결을 진행했습니다.',6),('현재 스코어는 EVD 3 대 SVD 4.',9),
('그렇다면 정말 SVD가 더 뛰어난 행렬 분해일까요?',13),('하나의 행렬 A를 생각해 보겠습니다.',15),
('EVD와 SVD는 모두 이 행렬을 분해하지만, 그 과정에서 드러내는 정보는 서로 다릅니다.',20),
('먼저 EVD입니다.',22),('고유값 분해는 행렬을 적용해도 같은 직선 위에 남는 고유방향을 찾아냅니다.',26),
('그리고 각 고유방향이 얼마나 확대되거나 축소되는지를 고윳값으로 나타냅니다.',31),
('여기서 고윳값은 음수가 될 수도 있습니다.',34),
('예를 들어 고윳값이 마이너스 2라면, 해당 고유벡터는 반대 방향으로 뒤집히면서 길이가 두 배가 됩니다.',40),
('즉, 고윳값의 부호와 크기에는 고유방향에서 일어나는 변화가 함께 담겨 있습니다.',46),
('이러한 성질은 같은 행렬을 반복해서 적용하는 시스템을 분석할 때 특히 유용합니다.',51),
('고유성분이 시간이 흐르며 어떻게 변화하는지 직접 살펴볼 수 있기 때문입니다.',56),
('그렇다면 SVD는 어떨까요?',58),('특이값 분해는 입력에서 서로 직교하는 방향들을 찾아냅니다.',62),
('그리고 이 방향들이 행렬에 의해 얼마나 늘어나거나 줄어드는지 특이값으로 나타냅니다.',67),
('특이값은 항상 0 이상입니다.',69),('그렇다면 SVD는 방향이 뒤집히는 변환을 표현하지 못하는 걸까요?',74),
('그렇지 않습니다.',75),('SVD에서는 입력과 출력의 특이벡터가 서로 다른 방향을 향할 수 있습니다.',80),
('따라서 특이값이 길이의 변화를 나타내고, 입력과 출력의 기저가 회전이나 방향 반전까지 표현합니다.',86),
('이 구조는 행렬이 어떤 방향을 가장 크게 늘리는지, 어떤 방향의 정보를 잃는지를 분석하는 데 유용합니다.',93),
('또한 큰 특이값의 성분부터 남기면, 정해진 랭크에서 원래 행렬을 가장 정확하게 근사할 수 있습니다.',98),
('결국 두 분해는 서로 다른 질문에 답하고 있습니다.',102),
('EVD는 이 변환이 가진 고유방향과 그 방향에서의 변화를 알고 싶을 때,',107),
('SVD는 입력이 어떤 출력 방향으로 변하고, 길이와 정보가 어떻게 달라지는지 알고 싶을 때 유용합니다.',113),
('물론 EVD는 모든 행렬에 적용할 수 없지만, SVD는 모든 행렬에 적용할 수 있습니다.',118),
('그렇다고 SVD가 EVD를 완전히 대체할 수 있는 것은 아닙니다.',122),('두 분해가 알려주는 정보가 서로 다르기 때문입니다.',126),
('그렇다면 행렬 분해 이상형 월드컵의 최종 승자는?',129),('누적 스코어는 EVD 3 대 SVD 4.',132),
('이번 월드컵의 우승은 SVD입니다!',135),('하지만 마지막으로 하나의 질문을 남기고 싶습니다.',138),
('우리가 알고 싶은 것은 행렬의 어떤 성질일까요?',141),('행렬을 어떻게 분해할 것인지는, 바로 그 질문에서 시작됩니다.',146),
('지금까지 행렬 분해 이상형 월드컵이었습니다!',149)]
SCENES=[
('open',0,4,'FINAL EPISODE','기존디자인오프닝,3초FINAL표시.'),
('results',4,9,'일곱 라운드 · 현재 3 : 4','사용자가명시적으로요청한최종편회상.1,3,5 EVD,2,4,6,7 SVD.점수검산.'),
('question',9,13,'점수가 높으면 더 좋은 분해일까?','선정한기준의누적승리와수학적우열구분.'),
('same',13,20,'같은 행렬 · 서로 다른 정보','A=diag(-2,1)고정.두분해갈래.'),
('eigen',20,26,'EVD · 같은 직선 위의 방향','수평·수직실제고유방향.수평반전후같은직선.'),
('eigenvalues',26,31,'고유방향에서의 배율','λ₁=-2,λ₂=1.실제예시에없는수축추가안함.'),
('negative',31,34,'고윳값은 음수가 될 수 있다','λ₁=-2의부호강조.특이값음수표기금지.'),
('flip',34,40,'−2 · 반전하면서 길이 두 배','(1,0)→(-2,0).수평선안에서반전,180도회전처럼움직이지않음.'),
('sign_magnitude',40,46,'부호와 크기의 역할','−:방향반전,2:길이배율.같은출력벡터.'),
('powers',46,56,'반복하면 방향도 번갈아 바뀐다','(-2)^n,1→-2→4→-8.처음부터고정[-9,9]축척.'),
('svd',56,62,'SVD · 직교하는 입력 방향','입력v₁=e₁,v₂=e₂직교.이예시고유방향과일치하나일반보장아님.'),
('singularvalues',62,67,'특이값은 길이 배율','Σ단계만2,1.전체A가아닌중간배율임명시.'),
('nonnegative',67,69,'특이값은 항상 0 이상','σ≥0,실제2,1.'),
('can_flip',69,75,'그렇다면 반전은 어디에?','λ=-2와σ=2를비교.74초그렇지않습니다에정확재현표시.'),
('input_output',75,80,'입력과 출력의 단위방향','v₁=(1,0),u₁=(-1,0).같은직선의반대방향,다른직선아님.'),
('svd_flip',80,86,'같은 변환 · 다른 설명','Av₁=σ₁u₁=2(-1,0)=(-2,0).EVD의출력과같음.'),
('uses',86,93,'최대 확대와 정보 소실','86–89 A의원→타원,89초별도B=diag(2,0)교체명시.7라운드사례.원→선분.'),
('approximation',93,98,'정해진 랭크에서 최소 오차','6라운드별도10×10행렬명시.실제상위5성분합과오차1.208,Frobenius기준.'),
('two_questions',98,102,'서로 다른 질문에 답한다','같은A로다시복귀명시.고유방향vs입력·출력방향.'),
('evd_question',102,107,'EVD · 고유방향에서 어떤 변화?','같은A의e₁→-2e₁,부호있는배율.'),
('svd_question',107,113,'SVD · 입력이 어떻게 출력으로?','같은v₁→2u₁.이A에는영특이값없음.'),
('conditions',113,118,'적용 가능한 행렬의 범위','EVD는A=PDP⁻¹의대각화의미.정사각·기저조건,SVD모든실수행렬.'),
('replace',118,122,'더 넓게 적용돼도 대체는 아니다','두분해카드균등배치,우열오해방지.'),
('information',122,126,'직접 드러내는 정보가 다르다','두정확한분해식과질문.'),
('winner_question',126,129,'행렬 분해 월드컵 · 최종 승자는?','승부재미,새라운드점수추가안함.'),
('score',129,132,'FINAL SCORE · EVD 3 : 4 SVD','SVD4강조,누적7라운드점수고정.'),
('champion',132,135,'SVD · CHAMPION','트로피와금색효과,선정7기준의월드컵우승.'),
('last_question',135,141,'행렬의 어떤 성질을 알고 싶은가?','점수·트로피제거,중앙A와네질문.'),
('message',141,146,'분해는 질문에서 시작된다','중앙A에서균등두분해로분기,145초질문강조.'),
('end',146,149,'행렬을 이해하는 두 가지 관점','시리즈로고,FINAL3:4,마지막1초정지.이후예고없음.')]
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    cues=[];start=0
    for caption,end in LINES:
        assert end>start;cues.append(dict(start=start,end=end,caption=caption));start=end
    assert start==149
    (ROOT/'project.json').write_text(json.dumps(dict(duration=149,ending_confirmed=True,timing_source='user_sentence_end_times',pending=[]),indent=2),encoding='utf-8')
    (ROOT/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    full='\n\n'.join(' '.join(c['caption'] for c in cues if a<=c['start']<b) for _,a,b,*_ in SCENES)
    (ROOT/'master_script.md').write_text('# 8편 확정 대본 — 최종 선택\n\n사용자확정원문·문장종료시각149초.최종편의회상·종합구조는이번요청에명시된내용.\n\n'+full+'\n',encoding='utf-8')
    (ROOT/'narration.md').write_text('\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues)+'\n',encoding='utf-8')
    (ROOT/'tts_script.txt').write_text(full.replace('EVD','이 브이 디').replace('SVD','에스 브이 디').replace('A','에이')+'\n',encoding='utf-8')
    manifest=[]
    for i,(slug,a,b,title,claim) in enumerate(SCENES):
        folder=ROOT/'scenes'/f'{i+1:02}_{slug}';folder.mkdir(parents=True,exist_ok=True);directory=folder.relative_to(ROOT).as_posix();cls=f'FinalChoice{i+1:02}'
        words=' '.join(c['caption'] for c in cues if a<=c['start']<b)
        (folder/'script.txt').write_text(words+'\n',encoding='utf-8')
        (folder/'spec.md').write_text(f'# {title}\n\n## 목적·주장\n{claim}\n\n## 앞 장면에서 받은 내용\nA=diag(-2,1)고정.별도사례는행렬변경명시.\n\n## TTS 원문·확정 길이\n{words}\n\n{a}–{b}초, {b-a}초.사용자문장종료시각.\n\n## 화면·시간별 애니메이션\n{claim}\nvisuals.py의scene_{i}로해당시각의움직임정의.세로·가로별도배치.\n\n## 화면 텍스트\n{title}\n\n## 시작·종료·연결\n현재주장하나완결.사용자가요청한최종편종합구조유지,새라운드추가·후속예고없음.\n\n## 수학적 조건·과장 방지\nEVD대각화가능조건,SVD모든실수행렬.특이값은비음수,반전은기저관계로표현.고유방향=특이방향은이번예시에한함.우승은선정7기준의점수.\n',encoding='utf-8')
        (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import FinalChoiceScene\nclass {cls}(FinalChoiceScene):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=directory,start=a,end=b,duration_seconds=b-a,**{'class':cls},title=title))
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'scenes.yaml').write_text('title: EVD vs SVD — 최종 선택\nduration_seconds: 149\nlayouts: [9:16,16:9]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
if __name__=='__main__':main()
