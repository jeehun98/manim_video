"""Approved narration and supplied sentence ends; no inferred speech timing."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
LINES='앞서 우리는 양자컴퓨터의 속도 향상이 문제의 수학적 구조와도 관련되어 있다는 사실을 살펴봤습니다.\n6\n쇼어 알고리즘은 주기적인 구조를 활용해 큰 속도 향상을 얻습니다.\n10\n그렇다면 이러한 규칙이 없는 무작위 데이터에서도 같은 일이 가능할까요?\n15\n2008년, 물리학자 스콧 아론슨과 안드리스 암바이니스는 이 질문과 관련된 하나의 추측을 제시했습니다.\n21\n이를 이해하기 위해 수많은 0과 1로 이루어진 데이터를 생각해 보겠습니다.\n26\n일반적인 컴퓨터는 데이터를 확인할 때 특정 위치의 비트를 읽습니다.\n31\n반면 양자컴퓨터는 여러 위치가 중첩된 상태에 조회 연산을 적용할 수 있습니다.\n36\n이러한 차이가 양자 알고리즘의 속도 향상을 가능하게 만드는 요소 중 하나입니다.\n41\n그런데 입력 데이터가 무작위로 주어진다면 어떨까요?\n44\n특정한 반복이나 규칙을 기대하기 어려운 상황에서도 양자컴퓨터는 지수적으로 적은 조회만으로 문제를 해결할 수 있을까요?\n52\n아론슨과 암바이니스는 이 문제를 다른 방향에서 바라봤습니다.\n56\n양자컴퓨터가 얼마나 빠르게 답을 찾아내는지 직접 분석하는 대신, 일반 컴퓨터가 양자컴퓨터의 결과를 예측할 수 있는지 질문한 것입니다.\n64\n예를 들어 어떤 양자 알고리즘이 주어진 데이터를 읽고 예 또는 아니오를 출력한다고 생각해 보겠습니다.\n71\n양자컴퓨터는 확률적으로 작동하므로, 같은 입력에 대해서도 예를 출력할 확률이 존재합니다.\n76\n이 확률은 입력 데이터에 따라 달라집니다.\n79\n그렇다면 일반 컴퓨터는 모든 데이터를 읽지 않고도, 양자컴퓨터가 예라고 답할 확률을 예측할 수 있을까요?\n86\n여기서 중요한 것은 양자컴퓨터의 내부 계산을 그대로 재현할 필요가 없다는 점입니다.\n91\n최종적으로 예를 출력할 확률만 충분히 정확하게 근사하면 됩니다.\n95\n만약 양자컴퓨터가 데이터를 T번 조회했다면, 일반 컴퓨터도 T의 일정한 거듭제곱에 비례하는 횟수만 조회해서 그 확률을 예측할 수 있을까요?\n105\n이것이 무작위 입력에 대한 양자 가속의 한계를 이해하는 중요한 질문이었습니다.\n109\n다만 모든 입력에서 정확히 예측해야 한다는 뜻은 아닙니다.\n113\n무작위로 선택한 입력의 대부분에서, 작은 오차를 허용하고 예측할 수 있는지를 묻는 것입니다.\n119\n아론슨과 암바이니스는 이러한 가능성을 낮은 차수의 다항식에 관한 수학적 추측과 연결했습니다.\n125\n그리고 그 추측이 성립한다면, 일반 컴퓨터도 대부분의 무작위 입력에서 양자 알고리즘의 출력 확률을 다항식 수준의 조회 횟수로 근사할 수 있음을 보였습니다.\n135\n이는 무작위 입력에 대한 지수적인 양자 조회 가속이 제한된다는 의미였습니다.\n140\n하지만 이를 뒷받침하는 핵심 수학적 추측은 오랫동안 증명되지 않았습니다.\n144\n그렇다면 양자컴퓨터의 출력 확률과 다항식 사이에는 어떤 관계가 있었을까요?\n149\n그리고 수많은 입력 중 일부만 확인해도 결과를 예측할 수 있다는 사실은 어떻게 증명할 수 있을까요?\n155'.splitlines()
BOUNDS=[0, 10, 15, 21, 26, 31, 41, 52, 64, 71, 79, 86, 95, 105, 109, 119, 125, 135, 140, 144, 155]
TITLES=['속도 향상과 문제의 구조', '무작위 데이터에서도 빠를까?', '2008년, 새로운 수학적 질문', '수많은 비트로 이루어진 입력', '고전 조회: 특정 위치의 비트', '양자 조회: 중첩된 위치에 연산', '입력이 무작위라면?', '계산의 속도에서 예측의 문제로', '예 또는 아니오를 출력한다면', '입력마다 달라지는 출력 확률', '일부 비트만 읽어 예측할 수 있을까?', '내부 계산 대신 출력 확률을 근사', 'T번 조회와 다항식 수준의 조회', '다항식과 지수식의 성장', '입력 대부분과 작은 오차', '출력 확률을 다항식으로 바라보다', '추측이 성립한다면 가능한 근사', '지수적인 조회 가속에 대한 제약', '오랫동안 남았던 수학적 추측', '일부 입력으로 결과를 예측하려면?']
DETAILS=['사용자 도입 문장을 보존하고 1,2,4,8 반복 구조를 재사용한다.', '독립 균등 비트의 고정 시드 표본. 무작위에 아무 성질도 없다고 단정하지 않는다.', '2008 제안 시점과 2009 원논문·2014 저널판 구별. 연구자 이름은 직함 없이 표시한다.', '같은 64비트 배열을 조회 장면에서 재사용한다.', '위치 i를 선택해 x_i 한 값을 읽는 조회.', 'U_x |i,b⟩=|i,b XOR x_i⟩의 선형 작용. 여러 값을 개별적으로 동시에 읽는 표현 금지.', '균등 무작위 입력 조건, 지수 가속은 질문으로만 제시.', '내부 게이트를 하나의 상자로 압축하고 출력 확률에 초점 이동.', 'YES/NO는 가능한 두 출력이며 동시에 관측한 결과가 아니다.', '개념 예시 A YES70% NO30%, B YES40% NO60%. 실제 회로의 측정 데이터가 아님.', '고전 조회로 읽지 않은 비트는 ?로 표시. 예측 가능성을 묻고 성공을 미리 단정하지 않는다.', '가상 예 p=.70, p~= .68, 절대오차 .02. 개념 예시 표시. 내부 상태 재현과 구별.', '동일 알고리즘 실행이 아닌 별도의 고전 추정 알고리즘. 오차 epsilon·예외입력비율 delta 고정 시 poly(T).', 'T²와2^T 성장의 정확한 계산 예. 실제 조회 복잡도 데이터가 아님.', 'Pr_uniform(|estimate-p|≤epsilon)≥1-delta. epsilon과delta 구분. 카드 색 비율은 개념 예시.', 'p(x)∈[0,1]인 Boolean cube 다항식. 차수≤2T는 모델 내부 검증만, 다음 내용 선행 강조 금지.', '추측⇒poly(T,1/epsilon,1/delta) 고전 조회. 알고리즘을 알고 입력만 조회한다는 모델.', '고정 오차·예외비율, 균등 무작위 입력에서 출력확률 근사 조회에 한정. 전체 실행시간 주장 금지.', '당시의 추측에서 출발한 역사적 서술. 2008→2026 18년 경과. 현시점 미해결이라고 표시하지 않는다.', '144–149 출력확률과 다항식,149–155 일부 비트의 영향. 확정 질문만 보존하며 다음편 제목·별도 엔드카드 없음.']

sentences=[];start=0
for i in range(0,len(LINES),2):
    end=int(LINES[i+1]);sentences.append({'start':start,'end':end,'text':LINES[i]});start=end
scenes=[{'id':f'{i+1:02}','class':f'Shot{i+1:02}','start':a,'end':b,'title':TITLES[i]} for i,(a,b) in enumerate(zip(BOUNDS,BOUNDS[1:]))]
data={'title':'무작위 데이터에서도 양자컴퓨터는 압도적으로 빠를까?','revision':'v1_155s','duration':155,'timing_source':'사용자 제공 확정 대본 및 문장 종료 시각','sentences':sentences,'scenes':scenes}
for name,obj in [('script.json',data),('timing.json',{'fps':60,**data})]:
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def wrap(s,n=32):
    out=[];line=''
    for w in s.split():
        if line and len(line)+len(w)+1>n:out.append(line);line=w
        else:line=(line+' '+w).strip()
    return '\n'.join(out+[line])
(HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
script='# 무작위 데이터에서도 양자컴퓨터는 압도적으로 빠를까?\n\n사용자 확정 대본 · 155초\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n'
for name in ['master_script.md','narration.md']:(HERE/name).write_text(script,encoding='utf-8')
tts=[]
for sentence in sentences:
    s=sentence['text']
    for a,b in [('2008년','이천팔 년'),('0과 1','영과 일'),('T번','티 번'),('T의','티의')]:s=s.replace(a,b)
    tts.append(s)
(HERE/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
for i,scene in enumerate(scenes):
    f=HERE/'scenes'/scene['id'];f.mkdir(parents=True,exist_ok=True)
    (f/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom longforms.qcs03_random.direction import EpisodeThreeScene\n\nclass '+scene['class']+'(EpisodeThreeScene):\n    shot='+str(i)+'\n',encoding='utf-8')
    text='\n\n'.join(s['text'] for s in sentences if s['end']>scene['start'] and s['start']<scene['end'])
    (f/'script.txt').write_text(text+'\n',encoding='utf-8')
    (f/'spec.md').write_text(f"# {scene['id']} · {scene['title']}\n\n## 목적과 주장\n\n{TITLES[i]}를 도형과 수식으로 설명한다.\n\n## 확정 대본·길이\n\n{scene['start']}–{scene['end']}초, {(scene['end']-scene['start'])*60}프레임. 문장 경계와 겹치는 원문은 아래와 같으며 실제 자막 시각은 timing.json을 따른다.\n\n{text}\n\n## 화면·연산·정확성\n\n{DETAILS[i]}\n\n## 연결\n\n앞 장면: {TITLES[i-1] if i else '사용자가 제공한 도입'}. 다음: {TITLES[i+1] if i<19 else '물리학적 질문으로 종료'}. direction.py의 s{i+1:02}가 독립 렌더 진입점이다. 하단에는 내레이션 자막을 유지한다.\n",encoding='utf-8')
manifest=[{**s,'directory':'scenes/'+s['id'],'duration_seconds':s['end']-s['start']} for s in scenes]
(HERE/'scenes.yaml').write_text(json.dumps({'id':'qcs03','title':data['title'],'video':{'longform':[1920,1080],'shorts':[1080,1920],'fps':60,'duration_seconds':155},'scenes':manifest},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert len(sentences)==28 and sentences[-1]['end']==155 and len(scenes)==20
