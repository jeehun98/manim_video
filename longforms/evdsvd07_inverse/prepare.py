import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LINES=[
('행렬 분해 이상형 월드컵!',1),('EVD 대 SVD.',3),('대결 기준, 역변환입니다.',5),
('좌표평면에 하나의 원을 그려 보겠습니다.',8),('이 원에 행렬 A를 적용하면, 원이 타원으로 변할 수 있습니다.',12),
('그렇다면 타원을 다시 원으로 되돌릴 수 있을까요?',14),('가능합니다. 행렬 A에 역행렬이 존재한다면 말이죠.',18),
('먼저 EVD입니다.',20),('행렬 A가 대각화 가능하다면, A는 P, D, P 역행렬의 곱으로 표현됩니다.',25),
('이때 모든 고윳값이 0이 아니라면, 가운데 대각행렬의 고윳값들을 각각 역수로 바꿀 수 있습니다.',31),
('그리고 P, D 역행렬, P 역행렬을 차례대로 곱하면 A의 역행렬이 만들어집니다.',37),
('즉, 고유방향에서 일어난 확대와 축소를 반대로 되돌릴 수 있는 것이죠.',41),
('그렇다면 SVD는 어떨까요?',43),('SVD는 행렬 A를 U, 시그마, V 전치의 곱으로 표현합니다.',48),
('정사각행렬 A의 모든 특이값이 0보다 크다면, SVD에서도 특이값들을 역수로 바꾸어 역행렬을 만들 수 있습니다.',56),
('여기까지만 보면 두 분해 모두 역변환이 가능합니다.',59),('그런데 이번에는 조금 다른 변환을 생각해 보겠습니다.',62),
('원이 타원으로 변하는 대신, 하나의 직선으로 완전히 눌려 버린다면 어떨까요?',67),
('서로 다른 위치에 있던 점들이 같은 위치로 겹치게 됩니다.',70),
('이제 결과만 보고 원래 점의 위치를 정확히 알아내는 것은 불가능합니다.',74),
('변환 과정에서 한 방향의 정보가 사라졌기 때문입니다.',77),('이런 행렬에는 역행렬이 존재하지 않습니다.',80),
('그렇다면 원래 입력에 대해 아무것도 알아낼 수 없는 걸까요?',84),('여기서 SVD의 또 다른 특징이 나타납니다.',87),
('SVD에서는 특이값이 0인 방향을 통해 어떤 입력 방향의 정보가 사라졌는지 확인할 수 있습니다.',93),
('그리고 0이 아닌 특이값들만 역수로 바꾸면, 의사역행렬이라는 새로운 행렬을 만들 수 있습니다.',99),
('의사역행렬은 사라진 정보를 되살리는 마법은 아닙니다.',102),
('대신 주어진 출력에 가장 가까운 결과를 만드는 입력을 찾고, 가능한 입력이 여러 개라면 그중 길이가 가장 짧은 것을 선택합니다.',110),
('이러한 성질은 정확한 해가 없거나 해가 여러 개인 연립방정식을 다룰 때도 활용됩니다.',115),
('물론 의사역행렬을 계산하는 방법이 SVD에만 있는 것은 아닙니다.',120),
('하지만 SVD는 모든 행렬에 적용할 수 있고, 사라진 방향과 남아 있는 방향을 특이값으로 명확하게 구분합니다.',127),
('그렇다면 역변환 대결의 승자는?',129),('SVD!',131),
('정확한 역변환이 불가능한 상황에서도, 의사역행렬을 통해 최선의 근사 해를 구할 수 있다는 점에 한 표를 주겠습니다.',137),
('현재 스코어, EVD 3 대 SVD 4.',141),('SVD 가 앞서갑니다.',142)]
SCENES=[
('open',0,5,'ROUND 07 · 역변환','현재3:3,이번질문제시.'),
('circle',5,8,'단위원에서 출발','원점중심반지름1,가로세로단위동일.'),
('ellipse',8,12,'A₁ · 원 → 타원','A₁=diag(2,0.5),실제좌표변환.축척고정.'),
('restore',12,18,'다시 원으로 되돌릴 수 있을까?','A₁⁻¹=diag(0.5,2)로타원과선택벡터복원.'),
('evd',18,25,'EVD · A = PDP⁻¹','대각화가능조건. 작용순서P⁻¹→D→P를오른쪽부터강조.'),
('reciprocal',25,31,'0이 아닌 고윳값의 역수','2→0.5,0.5→2.모든λ≠0조건.'),
('evd_inverse',31,37,'A⁻¹ = PD⁻¹P⁻¹','곱의표기순서와작용순서구분.오른쪽부터P⁻¹→D⁻¹→P.'),
('eigendirections',37,41,'고유방향의 배율을 반대로','수평2→1,수직0.5→1,동일축척.'),
('svd',41,48,'SVD · A = UΣVᵀ','Vᵀ→Σ→U.실제예시는U=V=I.'),
('svd_inverse',48,56,'A⁻¹ = VΣ⁻¹Uᵀ','정사각·모든σ>0조건.U,V순서교환을명시.'),
('both',56,59,'가역인 예시에서는 둘 다 가능','EVD는대각화가능한가역행렬,SVD는가역행렬.이예시한정.'),
('change',59,62,'다른 변환으로 교체','A₁=diag(2,0.5)→A₂=diag(2,0).행렬이바뀌었음을명시.'),
('collapse',62,67,'원 → 유한한 선분','실제A₂점별변환,출력은[-2,2]×{0},무한직선아님.'),
('overlap',67,70,'서로 다른 입력이 같은 출력으로','(0.6,±0.8)두점이동일출력(1.2,0)으로.색고정.'),
('ambiguous',70,74,'출력 하나 · 가능한 입력 무수히 많음','두대표점뿐아니라x=0.6직선의일부와연장표시.'),
('lost',74,77,'수직 방향 정보 소실','수평은2배,수직은0.원점에점으로수축.'),
('no_inverse',77,80,'역행렬 없음','det(A₂)=0.일대일아님.정보소실을되감지않음.'),
('question',80,84,'가능한 입력은 무엇일까?','출력b=(1.2,0)을유지.가능한입력검색.'),
('nullspace',84,93,'특이값 0 · 사라진 입력 방향','σ₁=2수평남음,σ₂=0수직영공간.실제변환.'),
('pseudoinverse',93,99,'0이 아닌 특이값만 역수로','Σ⁺=diag(0.5,0).0의역수를계산하지않고0유지. A₂⁺=VΣ⁺Uᵀ.'),
('not_magic',99,102,'선택한 해 ≠ 반드시 원래 입력','b=(1.2,0)→선택(0.6,0),원래두점과다른노랑점.'),
('minnorm',102,110,'가능한 해 중 가장 짧은 입력','입력선x=0.6,대표점까지의길이비교,선택(0.6,0).정확해존재사례임명시.'),
('systems',110,115,'Ax = b · 최소제곱과 최소 노름','b=(1.2,0)는무수한해,별도출력b′=(1.2,0.8)는불일치.투영(1.2,0),잔차0.8.같은A₂.'),
('other_methods',115,120,'의사역행렬 계산법은 다양하다','SVD이외AᵀA의대칭고유분해도가능.독점적도구로표현안함.'),
('directions',120,127,'남은 방향과 사라진 방향','수평σ2와수직σ0의직교방향을유지.모든실수행렬적용가능.'),
('verdict',127,137,'ROUND 07 · SVD 승','129초승자,131초이유.최소제곱해중최소노름.'),
('score',137,142,'EVD 3 : 4 SVD','139–140점수갱신,141리드문구.복습·예고없음.')]
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def main():
    cues=[];start=0
    for caption,end in LINES:
        assert end>start;cues.append(dict(start=start,end=end,caption=caption));start=end
    assert start==142
    (ROOT/'project.json').write_text(json.dumps(dict(duration=142,ending_confirmed=True,timing_source='user_sentence_end_times',pending=[]),indent=2),encoding='utf-8')
    (ROOT/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
    full='\n\n'.join(' '.join(c['caption'] for c in cues if a<=c['start']<b) for _,a,b,*_ in SCENES)
    (ROOT/'master_script.md').write_text('# 7편 확정 대본 — 역변환\n\n사용자원문·문장종료시각.총142초.\n\n'+full+'\n',encoding='utf-8')
    (ROOT/'narration.md').write_text('\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues)+'\n',encoding='utf-8')
    (ROOT/'tts_script.txt').write_text(full.replace('EVD','이 브이 디').replace('SVD','에스 브이 디').replace('A','에이').replace('U','유').replace('V','브이').replace('P','피').replace('D','디')+'\n',encoding='utf-8')
    manifest=[]
    for i,(slug,a,b,title,claim) in enumerate(SCENES):
        folder=ROOT/'scenes'/f'{i+1:02}_{slug}';folder.mkdir(parents=True,exist_ok=True);directory=folder.relative_to(ROOT).as_posix();cls=f'Inverse{i+1:02}'
        words=' '.join(c['caption'] for c in cues if a<=c['start']<b)
        (folder/'script.txt').write_text(words+'\n',encoding='utf-8')
        (folder/'spec.md').write_text(f'# {title}\n\n## 목적·주장\n{claim}\n\n## 앞 장면에서 받은 내용\n같은좌표척도와색.59초행렬교체명시.전반A₁,후반A₂.\n\n## TTS 원문·확정 길이\n{words}\n\n{a}–{b}초, {b-a}초. 사용자문장종료시각.\n\n## 화면·시간별 애니메이션\n{claim}\n세로·가로별도배치.실제행렬곱으로좌표계산.\n\n## 화면 텍스트\n{title}\n\n## 시작·종료·연결\n현재주장하나를완결.동일점을유지하고입력·출력공간을구분.\n\n## 수학적 조건·과장 방지\n역행렬은가역일때.EVD식은대각화가능할때.의사역행렬은최소제곱해중최소노름해선택.잃은정보를복원하지않음.본래두점과선택점은다름.평면전체에서입력은무수히많음.\n',encoding='utf-8')
        (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import InverseScene\nclass {cls}(InverseScene):\n    INDEX={i}\n',encoding='utf-8')
        manifest.append(dict(id=f'{i+1:02}',directory=directory,start=a,end=b,duration_seconds=b-a,**{'class':cls},title=title))
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'scenes.yaml').write_text('title: EVD vs SVD — 역변환\nduration_seconds: 142\nlayouts: [9:16,16:9]\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
if __name__=='__main__':main()
