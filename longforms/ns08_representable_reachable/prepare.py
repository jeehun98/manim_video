"""Act 8: representability and training selection."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
SOURCES='- Gunasekar et al., Characterizing Implicit Bias in Terms of Optimization Geometry (2018): https://proceedings.mlr.press/v80/gunasekar18a.html\n- Min et al., Initialization and Implicit Bias of Overparametrized Linear Networks (2021): https://proceedings.mlr.press/v139/min21c.html\n- Stanford CS231n, Derivatives and Backpropagation: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf\n'
DATA=[('conditions', '4막에서 남겨 두었던 질문', 34, '앞에서 우리는 속도가 끝없이 커지는 유체의 모습을 생각해 봤습니다.\n빠른 흐름이 나타나는 영역을 좁히면, 전체 에너지는 유한하게 유지될 수 있었습니다.\n하지만 그런 속도장을 그리는 것만으로는 나비에 스토크스의 해가 되지 않았습니다.\n실제 유체는 이류와 압력, 점성, 그리고 외력의 조건을 함께 만족해야 했기 때문입니다.\n즉 수학적으로 원하는 모양을 만드는 것과, 실제 운동 법칙이 그 모양을 허용하는 것은 서로 다른 문제였습니다.\n이번에는 이 구별을 신경망에 적용해 보겠습니다.', '集中 속도장 → PDE와 초기/외력 조건 검증 → 존재와 도달 질문', '에너지 집중은 이전 설명용 모형. 그 모형이 NS 해라는 주장이나 폭주해 검증을 새로 하지 않는다. PDE/비압축성/초기·경계/외력 조건 검증과 학습 동역학은 다른 문제.'), ('exists', '신경망 안에 좋은 답이 존재한다면?', 36, '하나의 신경망을 생각해 보겠습니다.\n이 신경망의 파라미터를 바꾸면 서로 다른 함수를 만들 수 있습니다.\n그중에는 주어진 데이터를 매우 정확하게 설명하는 파라미터도 존재할 수 있습니다.\n파라미터 공간에서 이 해를 하나의 점으로 나타내 보겠습니다.\n이 점에서는 손실이 매우 낮습니다.\n즉 모델의 표현 능력만 보면 좋은 답이 존재하는 것입니다.\n그렇다면 학습도 반드시 이 점에 도착할까요?', '파라미터 공간의 여러 점 → 낮은 손실 후보 → 떨어진 초기점', '좋은 파라미터의 존재와 특정 초기화·알고리즘의 수렴 보장은 구별. 2D 그림은 설명용 모델.'), ('local_rule', '학습은 모든 답을 비교하지 않는다', 34, '신경망의 학습은 가능한 모든 파라미터를 하나씩 비교하는 방식으로 이루어지지 않습니다.\n일반적인 그래디언트 디센트는 현재 위치에서 손실이 가장 빠르게 증가하는 방향을 계산합니다.\n그리고 그 반대 방향으로 조금씩 이동합니다.\n다음 위치에서도 같은 계산을 반복합니다.\n즉 학습은 최종적으로 어디에 좋은 해가 존재하는지 미리 알고 움직이지 않습니다.\n매 순간 현재 위치에서 얻은 정보에 따라 다음 위치를 결정하는 것입니다.', '정확한 비볼록 toy loss의 −gradient 화살표 → GD 경로', 'L(x,y)=.25(x²−1)²+.12x+.5y²−L_min; gradient=(x³−x+.12,y). 유클리드 파라미터 거리에서 gradient는 최급 증가 방향. GD η=.12, 실제 수치 반복. 벡터장 방향은 gradient flow와 공유하지만 이산 GD 경로를 표시.'), ('basins', '같은 모델에서도 출발점이 달라지면', 36, '이번에는 같은 손실 지형 위에서 서로 다른 초기점들을 선택해 보겠습니다.\n모든 점에 동일한 학습 규칙을 적용합니다.\n하지만 처음 위치가 다르면 각 지점에서 계산되는 그래디언트도 달라집니다.\n그래서 서로 다른 경로를 따라 이동하고, 다른 해에 도착할 수 있습니다.\n어떤 경로는 낮은 손실의 영역에 도착하지만, 다른 경로는 상대적으로 높은 손실의 국소 최솟값에 머무를 수도 있습니다.\n좋은 해가 존재한다는 사실과 실제 학습이 그 해에 도달한다는 사실은 다릅니다.', '같은 toy loss와 규칙, 서로 다른 두 초기값 → 두 국소 최소', '같은 L, η=.12, 시작(-1.7,.9)/(1.7,.9), 50스텝. 국소 최소는 cubic x³−x+.12=0의 바깥 두근. 실제 대형신경망 실패 일반 설명으로 단정하지 않는다.'), ('two_answers', '더 흥미로운 경우: 둘 다 좋은 해에 도착했다면?', 42, '이번에는 두 초기점에서 출발한 학습이 모두 낮은 손실에 도착했다고 가정하겠습니다.\n두 모델 모두 같은 학습 데이터를 정확하게 설명합니다.\n그런데 파라미터 공간에서 두 해는 서로 다른 위치에 있습니다.\n심지어 학습 데이터에 대한 결과가 같더라도, 새로운 입력에 대한 반응은 다를 수 있습니다.\n그렇다면 무엇이 두 해를 구분한 것일까요?\n모델의 표현 능력만으로는 답할 수 없습니다.\n어떤 초기점에서 출발했고, 어떤 학습 경로를 따라왔는지를 살펴봐야 합니다.', '부족결정 선형 모델 · 같은 훈련점 → 두 수렴해 → 새 입력의 다른 예측', 'f(a,b)(x)=ax+b, train(1,1), L=.5(a+b−1)². GD η=.2의 두 초기(0,0)/(0,2)는 (.5,.5)/(−.5,1.5)로 수렴. 수렴 극한 해를 표시. 훈련 예측 둘다1, 새 입력 x=−1에서는0/2. 참값을 지정하지 않아 일반화 우열을 주장하지 않는다.'), ('bias', '학습 규칙은 어떤 해를 선택하는가?', 34, '이제 질문이 다시 바뀝니다.\n신경망이 어떤 함수를 표현할 수 있는가가 아니라, 학습 과정이 가능한 여러 해 중 어떤 해를 선택하는가입니다.\n이 선택에는 초기값과 학습 알고리즘, 파라미터화 방식 등이 영향을 줄 수 있습니다.\n특히 손실이 낮은 해가 여러 개 존재할 때, 학습 알고리즘이 특정 성질의 해를 선호하는 현상을 암묵적 편향, 임플리시트 바이어스라고 합니다.\n명시적으로 그런 해를 선택하라고 지시하지 않아도, 학습 동역학 자체가 선택에 영향을 줄 수 있는 것입니다.', '좋은 해 직선 → 초기값 변화 → GD/방향별 보정 선택 → 암묵적 편향', '동일 loss의 최소 집합 a+b=1. 유클리드 GD는 초기 nullspace성분 보존. zero init GD→(.5,.5) 최소 유클리드 노름. zero init 방향별 고정 보정 P=diag(4,1), η=.1의 θ←θ−ηPgradient→(.8,.2); 명시적 정규화 추가 아님. 특정 모델 결과이며 일반 신경망 보편 보장 아님.'), ('compare', '이제 두 시스템을 다시 비교한다', 46, '이제 나비에 스토크스와 신경망을 다시 나란히 놓아보겠습니다.\n유체에서는 속도가 폭주하는 함수를 만드는 것만으로 충분하지 않았습니다.\n그 함수가 실제 운동 방정식과 초기 조건, 외력의 조건을 모두 만족해야 했습니다.\n신경망에서는 낮은 손실을 가진 파라미터가 존재하는 것만으로 학습이 그곳에 도달한다고 보장할 수 없습니다.\n주어진 초기값과 학습 규칙이 어떤 경로를 만드는지 살펴봐야 합니다.\n여기서 두 문제는 엄밀히 다릅니다.\n하나는 방정식과 조건을 만족하는 해가 존재하는지의 문제이고, 다른 하나는 학습 동역학이 어떤 해를 선택하는지의 문제입니다.\n하지만 두 질문에는 공통된 관점이 있습니다.\n가능한 상태들의 집합을 아는 것만으로는, 실제로 실현되는 상태를 설명할 수 없다는 것입니다.', '후보 유체의 조건 검증 / 여러 해에서 학습 경로 선택 · 화살표 의미 구별', '왼쪽 화살표는 조건 검증, 오른쪽은 동역학에 의한 선택. 후보 모양/유효 PDE 해/표현가능 함수/선택된 파라미터의 다른 수준을 혼동하지 않는다.'), ('paths', '시스템은 결과뿐 아니라 경로로 이해해야 한다', 44, '우리는 어떤 시스템을 볼 때 최종 상태에 집중하기 쉽습니다.\n유체에서는 특정한 속도장, 신경망에서는 낮은 손실을 가진 파라미터입니다.\n하지만 그 상태가 실제로 가능한지, 그리고 어떤 과정을 통해 나타나는지는 별개의 질문입니다.\n특히 신경망에서는 최종 손실이 비슷하더라도 학습 경로와 선택된 해가 다를 수 있습니다.\n따라서 모델을 이해하려면 무엇을 표현할 수 있는지만이 아니라, 실제 학습이 어떻게 진행되는지도 살펴봐야 합니다.\n이제 지금까지 발견한 패턴을 다시 모아보겠습니다.\n전체와 국소의 차이, 방향별 증폭, 가장 제한적인 모드, 그리고 실제 경로의 중요성.\n이 모든 이야기에는 공통된 질문이 숨어 있습니다.\n복잡한 시스템에서 증폭과 안정화는 어떻게 함께 작용할까요?', '전체와 국소, 방향, 제한적 모드, 경로 카드 → 증폭과 안정화 질문', '최종 손실 같음은 함수나 파라미터, 일반화 같음 뜻 아님. 가능한 경로와 실제 도달 경로는 주어진 초기값/학습 규칙에 의존. 9막의 증폭·안정화 질문으로 연결.')]

def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def main():
    manifest=[];master=['# 8막 — 좋은 해와 실제 학습 경로'];tts=[];cues=[];offset=0
    vp=ROOT/'voice_timing.json';voice=json.loads(vp.read_text(encoding='utf-8')) if vp.exists() else None
    if voice:
        assert len(voice['ends'])==sum(len(row[3].splitlines()) for row in DATA)
        assert all(a<b for a,b in zip([0]+voice['ends'][:-1],voice['ends']))
    sentence_index=0
    for i,(slug,title,duration,script,visual,conditions) in enumerate(DATA,1):
        original=duration;directory=ROOT/'scenes'/f'{i:02}_{slug}';directory.mkdir(parents=True,exist_ok=True)
        lines=script.splitlines();weights=[len(s)+12 for s in lines]
        if voice:
            measured=[e-offset for e in voice['ends'][sentence_index:sentence_index+len(lines)]];duration=measured[-1]
        sentence_index+=len(lines)
        current=0;ends=[];local=[]
        for j,(line,w) in enumerate(zip(lines,weights)):
            end=measured[j] if voice else current+duration*w/sum(weights);ends.append(end)
            display=line.replace('암묵적 편향, 임플리시트 바이어스','암묵적 편향, Implicit Bias')
            for a,b in [('이천이십육 년 구월 팔일','2026년 9월 8일'),('오픈에이아이','OpenAI'),('구월 십일','9월 11일'),('나비에 스토크스','Navier–Stokes'),('엘투 노름','L₂ 노름')]: display=display.replace(a,b)
            for a,b in [('엘엘엠 인트 에이트', 'LLM.int8()'), ('스무스 퀀트', 'SmoothQuant'), ('십육 비트', '16비트'), ('팔 비트', '8비트'), ('예순네 개', '64개'), ('예순세 개', '63개'), ('영 점 이오', '0.25'), ('영 점 오', '0.5'), ('영 점 육', '0.6'), ('영 점 이는', '0.2는'), ('영 점 일', '0.1'), ('영 점 사', '0.4'), ('영 점 팔', '0.8'), ('하나만 팔', '하나만 8'), ('최대값은 팔', '최대값은 8'), ('최대 절댓값이 일일 때', '최대 절댓값이 1일 때'), ('백일 때', '100일 때'), ('백까지', '100까지'), ('백 배', '100배'), ('활성값이 팔', '활성값이 8'), ('곱은 이', '곱은 2'), ('활성값을 팔로', '활성값을 8로'), ('가중치를 팔 배', '가중치를 8배'), ('일과 이를', '1과 2를')]: display=display.replace(a,b)
            local.append(f'{j+1}\n{stamp(current)} --> {stamp(end)}\n{display}')
            cues.append(f'{len(cues)+1}\n{stamp(offset+current)} --> {stamp(offset+end)}\n{display}');current=end
        (directory/'captions.srt').write_text('\n\n'.join(local)+'\n',encoding='utf-8')
        (directory/'timing.json').write_text(json.dumps({'duration':duration,'ends':ends,'lines':lines,'basis':voice['basis'] if voice else 'visual storyboard; TTS unmeasured'},ensure_ascii=False,indent=2),encoding='utf-8')
        spoken='\n\n'.join(lines).replace('헤시안, Hessian','헤시안');tts.append(spoken)
        (directory/'script.txt').write_text(spoken+'\n',encoding='utf-8')
        master.append(f'## {i:02} — {title} ({stamp(offset)}–{stamp(offset+duration)})\n\n'+spoken)
        (directory/'spec.md').write_text(f'''# Scene {i:02} — {title}
## 목적과 핵심 주장
{title}를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
{DATA[i-2][1] if i>1 else '7막 마지막의 가능한 상태와 도달 경로 질문'}
## TTS 원문과 확정 길이
{spoken}

- TTS: {'사용자 측정 '+str(duration)+'초' if voice else '미확정. 사용자 허용에 따라 화면 제작 우선.'}
- 화면: {duration}초. 원래 화면 기준은 {original}초.
## 화면 구성과 시간대별 애니메이션
{visual}
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
{title}, 속도장 조건, 파라미터 공간, 손실 지형, 초기점과 학습 경로, 훈련점과 새로운 입력, 해 집합, 암묵적 편향, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
{DATA[i][1] if i<len(DATA) else '9막: 증폭과 안정화'}
## 수학 조건·과장 방지
{conditions}
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 유한 활성 행렬의 이상치를 유체 특이점과 동일시하지 않는다.
## 출처
{SOURCES}
''',encoding='utf-8')
        (directory/'scene.py').write_text(f"from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import EnergyScene\n\nclass Scene{i:02}(EnergyScene):\n    index={i}\n",encoding='utf-8')
        manifest.append({'id':f'{i:02}','slug':slug,'directory':f'scenes/{i:02}_{slug}','class':f'Scene{i:02}','duration_seconds':duration if voice else None,'storyboard_seconds':original})
        offset+=duration
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'master_script.md').write_text('\n\n'.join(master)+'\n',encoding='utf-8')
    (ROOT/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(cues)+'\n',encoding='utf-8')
    (ROOT/'sources.md').write_text('# 출처와 확인 기준\n\n확인: 2026-10-08. 논문 관찰과 설명용 수치 모형을 구별한다. 유체 후보의 조건 검증과 학습 경로의 해 선택을 구별한다. 비볼록 toy loss와 부족결정 선형 회귀는 설명용 수치 예시이며 실제 대형 모델의 측정값이 아니다.\n\n'+SOURCES,encoding='utf-8')
    yaml='id: ns08\ntitle: "8막 — 표현 가능성과 도달 가능성"\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\ntiming_basis: '+('user_sentence_end_times' if voice else 'visual_storyboard_without_tts')+'\nscenes:\n'
    for row in manifest:yaml+='  - '+'\n    '.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in row.items())+'\n'
    (ROOT/'scenes.yaml').write_text(yaml,encoding='utf-8')

if __name__=='__main__':main()
