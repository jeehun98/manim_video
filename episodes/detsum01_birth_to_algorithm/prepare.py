from pathlib import Path
import json
R=Path(__file__).resolve().parent
SOURCE='''3|오늘날 우리는 행렬을 배우고 난 뒤 행렬식을 배웁니다.
8|하지만 역사적으로 행렬식에 관한 연구는 현대적인 행렬 이론보다 먼저 등장했습니다.
13|그 출발점은 연립방정식이었습니다.
17|두 개의 일차방정식에서 하나의 미지수를 제거하면, 에이 디 마이너스 비 씨라는 계수의 조합이 등장합니다.
23|이 값이 영이 아니라면 해를 유일하게 결정할 수 있지만, 영이라면 해가 없거나 무한히 많아집니다.
29|이처럼 행렬식은 방정식의 계수들 사이에서 해의 유일성을 판단하는 값으로 나타납니다.
33|그런데 동일한 행렬을 공간의 변환으로 바라보면 새로운 의미가 발견됩니다.
39|행렬의 두 열을 벡터로 해석하면, 단위 정사각형은 두 벡터가 만드는 평행사변형으로 변합니다.
44|그리고 이 평행사변형의 넓이를 계산하면, 다시 에이 디 마이너스 비 씨의 절댓값이 등장합니다.
50|행렬식이 영이라면 공간은 더 낮은 차원으로 붕괴하고, 음수라면 공간의 방향이 반전됩니다.
58|삼차원에서는 정육면체의 부피 변화로, 더 높은 차원에서는 해당 차원의 부피 변화로 동일하게 해석할 수 있습니다.
62|이러한 기하학적 성질은 행렬식의 계산 공식에도 반영됩니다.
65|각 열벡터를 기본 방향의 성분으로 분해해 보겠습니다.
71|행렬식은 각각의 열벡터에 대해 선형적이므로, 각 벡터의 성분들을 조합하여 계산할 수 있습니다.
78|예를 들어 삼차원에서는 세 벡터 각각에 세 가지 방향의 성분이 존재하므로, 모두 스물일곱 가지 조합이 만들어집니다.
83|가능한 모든 성분의 조합 중 같은 방향이 반복되는 경우에는 부피가 영이 됩니다.
87|결국 서로 다른 기본 방향을 하나씩 선택한 조합만 남습니다.
91|삼차원에서는 이렇게 여섯 가지 방향 조합만 남게 됩니다.
92|이것이 바로 순열입니다.
99|그리고 벡터의 순서를 교환할 때마다 공간의 방향이 반전되므로, 순열의 홀짝성에 따라 각 항의 부호가 결정됩니다.
102|이러한 계산 구조를 라이프니츠 공식이라고 합니다.
107|하지만 행렬의 크기가 커지면 가능한 순열의 개수도 폭발적으로 증가합니다.
111|십 행 십 열 행렬만 하더라도 삼백육십만 개가 넘는 항이 등장합니다.
115|여기서 우리는 행렬식의 또 다른 성질을 활용할 수 있습니다.
122|한 벡터에 다른 벡터의 배수를 더하면 도형의 형태는 달라지지만, 부호 있는 부피는 그대로 유지됩니다.
128|이 성질을 행 연산에 적용하면 행렬식을 유지하면서 대각선 아래의 원소들을 영으로 만들 수 있습니다.
133|그러면 순열에 따른 대부분의 곱셈 항이 사라지고, 대각선 원소들의 곱만 남습니다.
137|이것이 가우스 소거법을 이용한 효율적인 행렬식 계산의 핵심입니다.
144|이를 통해 팩토리얼에 따라 증가하던 순열 항의 직접 계산을, 행렬 크기의 세제곱에 비례하는 연산량으로 대체할 수 있습니다.
149|그런데 공간을 가로 방향으로 십 배 늘리고, 세로 방향으로 십분의 일로 줄이면 어떻게 될까요?
153|공간의 형태는 크게 달라지지만, 행렬식은 여전히 일입니다.
157|즉, 행렬식은 공간의 모든 변화를 표현하는 값은 아닙니다.
161|복잡한 공간의 변화에서 전체 부피와 방향이라는 정보를 추출한 값입니다.
168|방정식의 해를 판단하는 기준에서 공간의 변환으로, 그리고 순열과 불변성을 이용한 계산 알고리즘으로.
177|행렬식은 복잡한 수학적 대상에서 중요한 성질을 추출하는 것이 어떻게 서로 다른 문제를 연결할 수 있는지 보여주는 대표적인 예시입니다.'''
shots=[(0,13,'학습 순서와 역사 순서'),(13,17,'소거에서 ad−bc가 등장한다'),(17,23,'유일한 해·해 없음·무한한 해'),(23,29,'행렬식과 해의 유일성'),(29,39,'행렬의 열벡터와 공간 변환'),(39,44,'넓이 계산에서 같은 공식'),(44,50,'차원 붕괴와 방향 반전'),(50,62,'차원별 부피와 계산 성질'),(62,71,'성분 분해와 다중선형성'),(71,78,'삼차원 성분의 27가지 조합'),(78,83,'중복 방향의 부피는 0'),(83,92,'27개 조합에서 6개 순열로'),(92,102,'교환과 부호 및 라이프니츠 공식'),(102,115,'순열 항의 팩토리얼 증가'),(115,122,'다른 벡터의 배수 더하기는 부피 보존'),(122,128,'행 연산으로 상삼각화'),(128,137,'대각선 곱만 남는다'),(137,144,'직접 전개와 소거의 연산량'),(144,157,'같은 행렬식과 다른 공간 변형'),(157,161,'부피와 방향이라는 정보 추출'),(161,168,'네 가지 관점의 연결'),(168,177,'하나의 수학적 구조로 연결')]
lines=[];tts=[];start=0
for row in SOURCE.splitlines():
 end,s=row.split('|',1);end=int(end);tts.append(s)
 for a,b in [('에이 디 마이너스 비 씨','ad−bc'),('영이','0이'),('영이라면','0이라면'),('여전히 일입니다','여전히 1입니다'),('삼차원','3차원'),('스물일곱','27'),('여섯','6'),('십 행 십 열','10×10'),('삼백육십만','360만'),('십 배','10배'),('십분의 일','1/10')]:s=s.replace(a,b)
 lines.append(dict(start=start,end=end,text=s));start=end
def write(n,s):(R/n).write_text(s,encoding='utf-8')
def stamp(s):return f'{s//3600:02}:{s%3600//60:02}:{s%60:02},000'
write('timing.json',json.dumps(dict(duration=177,source='사용자 제공35개 문장 종료 시각',lines=lines),ensure_ascii=False,indent=2))
write('tts_script.txt','\n\n'.join(tts)+'\n')
write('captions.srt','\n\n'.join(f'{i+1}\n{stamp(l["start"])} --> {stamp(l["end"])}\n{l["text"]}' for i,l in enumerate(lines))+'\n')
write('narration.md','# 행렬식의 탄생부터 계산 원리까지\n\n확정35문장·177초\n\n'+'\n\n'.join(f'{l["start"]}–{l["end"]}초\n\n{l["text"]}' for l in lines)+'\n')
manifest=[]
for i,(a,b,claim) in enumerate(shots,1):
 d=R/'scenes'/f'{i:02}';d.mkdir(parents=True,exist_ok=True)
 manifest.append(dict(id=f'{i:02}',directory=f'scenes/{i:02}',class_name=f'Shot{i:02}',start=a,duration_seconds=b-a,claim=claim))
 (d/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import SummaryScene\nclass Shot'+f'{i:02}'+'(SummaryScene):\n    index='+str(i)+'\n',encoding='utf-8')
 (d/'spec.md').write_text(f'# {i:02} · {claim}\n\n- {a}–{b}초, 9:16 1080×1920 30fps.\n- storyboard.md와 scene.py s{i:02} 기준. 기존 수학 로직 재사용, 세로 배치.\n- 확정 내레이션 및 종료 시각 유지, 무음·전체 자막.\n- 자막은 y=−5.35 중심, 최하단 UI 영역에 중요 정보 없음.\n- n!은 항 수이며 단순 직접 전개는 O(n·n!), 소거는 O(n³).\n- 행 교환은 부호 보정, k와1/k는 매 프레임 동시 갱신.\n- 순열은 각 열에서 선택한 행 번호를 나타낸다.\n',encoding='utf-8')
 (d/'script.txt').write_text('\n\n'.join(tts[j] for j,l in enumerate(lines) if a<=l['start'] and l['end']<=b)+'\n',encoding='utf-8')
write('manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))

# Keep orientation labels upright during reflection.
p=R/"scenes/07/scene.py"
p.write_text(p.read_text(encoding="utf-8")+"\n    def s07(self):\n        from visuals import board, eq, tx, basis, geometry, np, VGroup, UpdateFromAlphaFunc, RED, GREEN\n        b=board([[3,1],[1,3]])\n        self.add(b)\n        self.morph(b,[[3,3],[1,1]],2.2)\n        self.show(eq(r'\\det(A)=0',-2.7,51,RED),d=.4)\n        self.to(47)\n        self.clear(.25)\n        original=np.array([[-1.5,-.2,0],[1.5,-.2,0],[1.5,2.8,0],[-1.5,2.8,0]])\n        def figure(alpha):\n            points=original.copy();points[:,0]*=1-2*alpha\n            color=GREEN if alpha<.5 else RED\n            return VGroup(geometry.outline(points,color),basis.arrows(list(points),c=color),*[eq(str(j+1),p[1],27,color,x=p[0]) for j,p in enumerate(points)])\n        g=figure(0);self.add(g)\n        self.act(1.2,UpdateFromAlphaFunc(g,lambda m,t:m.become(figure(t))))\n        self.show(eq(r'\\det(B)=-1',-2.5,50,RED),d=.4)\n        self.to(50)\n",encoding="utf-8")

# Keep the collapsed parallelepiped above its explanatory label.
p=R/"scenes/11/scene.py"
p.write_text(p.read_text(encoding="utf-8")+"\n    def s11(self):\n        from visuals import basis, eq, tx, np, UP, RED, GREEN\n        self.add(basis.cards((0,0,1),0,4.6,.65),eq(r'(\\mathbf e_1,\\mathbf e_1,\\mathbf e_2)',3.3,42,RED))\n        M=np.array([[1,1,0],[0,0,1],[0,0,0]])\n        flat=basis.cube(M,[0,1.0,0],1.6).shift(UP*1.1)\n        self.add(flat,tx('같은 방향이 반복되면',-.2,31,RED),eq('V=0',-1.2,57,RED))\n        self.show(eq(r'\\det(\\mathbf e_1,\\mathbf e_2,\\mathbf e_3)=1',-2.8,39,GREEN),d=.5)\n        self.to(83)\n",encoding="utf-8")
