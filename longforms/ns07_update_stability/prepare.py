"""Act 7: explicit update stability."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
SOURCES='- MIT, Strang, Heat Equation and Convection-Diffusion: https://math.mit.edu/classes/18.086/2006/am54.pdf\n- MIT, Forward and Backward Euler Methods: https://web.mit.edu/10.001/Web/Course_Notes/Differential_Equations_Notes/node3.html\n- Stanford EE270, Lecture 14, Second-Order Optimization: https://web.stanford.edu/class/ee270/Lecture14.pdf\n'
DATA=[('grid', '실제 유체와 컴퓨터 속 유체는 다르다', 32, '앞에서는 소용돌이가 회전축 방향으로 늘어나면서, 보티시티의 강도가 커질 수 있다는 사실을 살펴봤습니다.\n그런데 이번에는 실제 유체가 아니라, 컴퓨터로 계산하는 유체를 생각해 보겠습니다.\n나비에 스토크스 방정식은 연속적인 공간과 시간에서 정의됩니다.\n하지만 컴퓨터에서는 모든 위치와 모든 순간을 직접 계산할 수 없습니다.\n그래서 공간을 작은 격자로 나누고, 시간을 일정한 간격으로 건너뛰며 다음 상태를 계산합니다.\n이때 두 가지 간격이 등장합니다.\n공간의 간격과 시간의 간격입니다.', '연속 흐름 → 공간 격자 → 시간 눈금 → 두 간격', '격자 유체 개념도이며 NS 전체의 수치해가 아니다.'), ('refine', '공간을 더 자세히 보면 시간도 더 잘게 나눠야 할까?', 38, '이번에는 유체의 한 부분을 더 자세히 계산해 보겠습니다.\n격자 간격을 절반으로 줄입니다.\n그러면 기존에는 하나의 칸으로 표현했던 영역을 여러 칸으로 나누어 계산할 수 있습니다.\n그런데 문제가 생깁니다.\n점성에 의한 확산을 간단한 명시적 방법으로 계산한다면, 공간 격자 간격에 따라 허용되는 시간 간격도 달라집니다.\n한 차원의 단순한 확산 계산에서는 공간 간격을 절반으로 줄이면, 안정성을 위해 시간 간격을 사분의 일 이하로 줄여야 합니다.\n공간을 두 배 더 촘촘하게 살펴보려 했을 뿐인데, 시간은 네 배 더 세밀하게 계산해야 하는 것입니다.', '격자 1 → 1/2 · 시간 간격 1 → 1/4', '1D 등간격 중앙차분 + Forward Euler, ν>0, r=νΔt/Δx²≤1/2. Δx/2이면 같은 r에서 Δt/4. 다른 차원/적분법 계수 다름.'), ('diffusion', '왜 너무 큰 시간 간격에서는 계산이 불안정해질까?', 36, '그렇다면 시간 간격이 너무 크면 어떤 일이 일어날까요?\n점성은 원래 급격한 속도 차이를 완화하는 효과를 가지고 있습니다.\n그런데 확산을 한 번에 너무 큰 간격으로 계산하면, 수치적인 오차가 오히려 증폭될 수 있습니다.\n실제 방정식에서는 매끄럽게 퍼져야 할 변화가, 컴퓨터 계산에서는 진동하며 커질 수 있는 것입니다.\n여기서 중요한 구별이 있습니다.\n이것은 실제 유체에 특이점이 생겼다는 뜻이 아닙니다.\n물리적으로 안정적인 과정도, 잘못된 계산 간격에서는 수치적으로 불안정해질 수 있다는 뜻입니다.', '주기 격자 FTCS 실제 반복 · 안정/불안정 오차 모드', '주기 16점, u0=.3cos(2πj/16)+.03(-1)^j. FTCS r=.2/.6, g(k)=1−4r sin²(kΔx/2). 동일 스텝 수 비교이며 물리 경과 시간은 다름. 최대 격자 모드 g=.2/−1.4.'), ('global', '가장 작은 공간 스케일이 전체 계산을 제한한다', 38, '이제 전체 유체로 돌아가 보겠습니다.\n대부분의 영역에서는 흐름이 완만하게 변합니다.\n하지만 아주 작은 영역에서만 급격한 속도 차이가 나타난다고 생각해 보겠습니다.\n그 구조를 충분히 표현하려면 주변의 격자를 더 촘촘하게 만들어야 할 수 있습니다.\n그리고 명시적인 계산에서는 이 작은 격자가 허용되는 시간 간격까지 제한할 수 있습니다.\n거대한 유체 전체를 계산하고 있지만, 실제 업데이트 크기는 가장 까다로운 일부 영역의 조건에 의해 결정될 수 있는 것입니다.\n중요한 것은 전체 흐름의 평균적인 변화가 아닙니다.\n가장 작은 스케일에서 계산이 안정적으로 유지되는가입니다.', '국소 세밀 격자 → 전역 시간 간격 병목', '하나의 전역 Δt를 쓰는 명시적 확산 예시. 비균일 격자의 정확한 안정성 계수는 이산 연산자에 의존. 작은 격자는 제한할 수 있음. 암시적/국소 시간적분, 이류 CFL 등 별도.'), ('learning', '신경망에도 비슷한 제한이 있을까?', 32, '이제 신경망의 학습으로 넘어가 보겠습니다.\n신경망은 손실을 줄이기 위해 파라미터를 조금씩 수정합니다.\n가장 간단한 방법인 그래디언트 디센트에서는 현재 위치의 기울기를 계산하고, 그 반대 방향으로 이동합니다.\n이때 한 번에 얼마나 이동할지를 결정하는 값이 학습률입니다.\n학습률을 크게 하면 빠르게 움직일 수 있지만, 너무 크면 손실이 줄어들지 않고 진동하거나 발산할 수 있습니다.\n그렇다면 적절한 학습률은 무엇이 결정할까요?', '손실 등고선 → 기울기 반대 방향 → 두 학습률 궤적', '양의 정부호 2D 이차 손실 H=diag(1,12), θ0=(.8,.1), η=.1/.2. GD는 θ←(I−ηH)θ; 8스텝. 실제 신경망 측정 궤적 아님.'), ('hessian', '모든 방향의 손실이 똑같이 변하지 않는다', 36, '앞에서는 야코비안이 입력 변화의 방향에 따라 서로 다른 증폭을 만든다는 사실을 살펴봤습니다.\n이번에는 입력이 아니라 파라미터를 움직여 보겠습니다.\n한 방향으로 조금 움직이면 손실이 거의 달라지지 않습니다.\n하지만 다른 방향으로 같은 거리만큼 움직이면 손실이 급격하게 증가할 수 있습니다.\n이처럼 파라미터 공간에서 손실이 얼마나 휘어져 있는지를 나타내는 것이 헤시안입니다.\n헤시안의 고유벡터는 곡률의 주요 방향을 나타내고, 고유값은 그 방향으로 얼마나 가파르게 휘어져 있는지를 나타냅니다.', '같은 거리 두 방향 → 손실 증가 → Hessian 카드', 'H=diag(1,12), 최솟값 θ=0 주변. 같은 변위 .5에서 손실 .125/1.5. 일반 비볼록 손실의 곡률과 기울기를 동일시하지 않음.'), ('steep', '단 하나의 가파른 방향이 학습률을 제한한다', 40, '이제 대부분의 방향은 완만하지만, 단 하나의 방향만 유난히 가파른 손실 지형을 생각해 보겠습니다.\n완만한 방향만 본다면 학습률을 크게 설정해도 괜찮아 보입니다.\n하지만 가파른 방향에서는 같은 학습률이 지나치게 클 수 있습니다.\n파라미터가 최솟값을 넘어 반대편으로 이동하고, 다시 반대편으로 넘어가는 과정이 반복됩니다.\n심하면 이동 폭이 점점 커지면서 발산할 수도 있습니다.\n양의 곡률을 가진 단순한 이차 손실에서는, 가장 큰 헤시안 고유값이 안정적인 학습률의 상한을 결정합니다.\n즉 다른 방향들이 모두 완만하더라도, 가장 가파른 방향 하나 때문에 전체 학습률을 낮춰야 할 수 있습니다.', '완만/가파른 모드 · 같은 학습률 · 진동 증폭 → 학습률 상한', '고정 H=diag(1,12), η=.2이면 g=.8/−1.4. 모든 초기 오차에 대한 수렴 보장은 0<η<2/λmax. 특정 고유방향 성분이 0인 특별 초기값은 예외. Adam/SGD/변하는 Hessian 일반 보장 아님.'), ('compare', '유체와 신경망에서 같은 제한이 나타난다', 36, '이제 두 시스템을 나란히 놓아보겠습니다.\n유체의 명시적 시뮬레이션에서는 작은 공간 격자가 허용되는 시간 간격을 제한할 수 있었습니다.\n신경망의 그래디언트 디센트에서는 큰 곡률을 가진 방향이 허용되는 학습률을 제한할 수 있습니다.\n하나는 공간을 나눈 뒤 시간을 계산하는 문제이고, 다른 하나는 손실 지형에서 파라미터를 업데이트하는 문제입니다.\n서로 다른 계산이지만, 공통된 구조가 있습니다.\n전체가 안정적으로 움직이려면, 가장 까다로운 모드에서도 업데이트가 안정적이어야 한다는 것입니다.\n평균적인 변화만으로 업데이트 크기를 결정하면, 일부 모드에서 오히려 오차가 증폭될 수 있습니다.', '확산 격자와 손실 방향 · 두 제한 나란히', '선형 확산 FTCS와 고정 양의 정부호 이차 손실 GD의 비교. 물리 특이점과 무관.'), ('modes', '두 시스템의 수학적 구조는 더 가까울까?', 40, '그런데 이 유사성은 단순히 겉모습이 닮은 것일까요?\n조금 더 깊이 살펴보겠습니다.\n유체의 점성 확산을 격자 위에서 계산하면, 각 진동 모드가 다음 시간에 얼마나 남는지를 계산할 수 있습니다.\n신경망의 이차 손실에서도 헤시안의 각 고유방향이 다음 스텝에 얼마나 남는지를 계산할 수 있습니다.\n두 경우 모두 업데이트 연산자가 각각의 모드에 일정한 배율을 적용합니다.\n그 배율의 절댓값이 1보다 크면 작은 오차가 반복적으로 증폭될 수 있습니다.\n즉 두 시스템에서는 모두 업데이트 연산자의 고유값을 통해 안정성을 분석할 수 있습니다.', '고주파 모드/고유방향 → 배율 반복 → 공통 업데이트 구조', '두 업데이트는 I−hB 꼴의 대칭 선형 모형. |g|>1인 모드에 0이 아닌 오차가 있을 때 증폭. |g|≤1은 비증폭, |g|<1은 엄격 감쇠. g=−1은 감쇠 없는 진동, g=1은 보존. 확산 평균 모드 g=1 정상. 비정규 일반 행렬의 순간 증폭 보장으로 확대하지 않음.'), ('reachable', '무엇이 전체를 제한하는가?', 38, '지금까지 우리는 세 가지 서로 다른 문제를 살펴봤습니다.\n유체에서는 전체 에너지의 유한성만으로, 작은 영역의 극단적인 속도를 막을 수 없다는 점을 보았습니다.\n신경망에서는 특정 방향의 변화가 다른 방향보다 훨씬 크게 증폭될 수 있었습니다.\n그리고 이제는 그중 가장 제한적인 방향 하나가 전체 계산의 업데이트 크기를 결정할 수 있다는 사실을 보았습니다.\n하지만 여기서 한 가지를 구분해야 합니다.\n유체의 수학적 특이점과, 컴퓨터가 너무 큰 시간 간격을 사용해 발생시키는 수치적 불안정성은 서로 다릅니다.\n우리가 발견한 공통점은 현상 자체가 아니라, 여러 모드 중 가장 제한적인 모드가 전체 계산의 안정성을 제약한다는 수학적 구조입니다.\n그렇다면 다음 질문은 무엇일까요?\n어떤 상태가 수학적으로 가능하다는 사실과, 실제 운동 법칙이나 학습 과정이 그 상태에 도달할 수 있다는 사실은 같을까요?', '에너지/방향/안정성 정리 → 경로와 목표 → Possible vs Reachable', '에너지 유한성만으로 연속장의 최대값을 제어하지 못한다는 이전 모형을 요약. 가능한 상태와 도달 경로 구분은 다음 막 질문이며 도달 불가능 증명 아님.')]

def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def main():
    manifest=[];master=['# 7막 — 가장 제한적인 모드와 업데이트'];tts=[];cues=[];offset=0
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
            display=line
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
{DATA[i-2][1] if i>1 else '6막의 방향별 증폭과 Hessian에 관한 질문'}
## TTS 원문과 확정 길이
{spoken}

- TTS: {'사용자 측정 '+str(duration)+'초' if voice else '미확정. 사용자 허용에 따라 화면 제작 우선.'}
- 화면: {duration}초. 원래 화면 기준은 {original}초.
## 화면 구성과 시간대별 애니메이션
{visual}
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
{title}, 격자 간격, 시간 눈금, 확산 모드, 손실 등고선, 학습률, 곡률 방향, 반복 배율, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
{DATA[i][1] if i<len(DATA) else '8막: 가능한 상태와 도달 가능한 경로'}
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
    (ROOT/'sources.md').write_text('# 출처와 확인 기준\n\n확인: 2026-10-08. 논문 관찰과 설명용 수치 모형을 구별한다. 실제 특이점과 수치 불안정을 구별한다. FTCS 확산과 양의 정부호 이차 손실의 GD는 계산 예시이며 실제 신경망 측정값이 아니다.\n\n'+SOURCES,encoding='utf-8')
    yaml='id: ns07\ntitle: "7막 — 업데이트 안정성"\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\ntiming_basis: '+('user_sentence_end_times' if voice else 'visual_storyboard_without_tts')+'\nscenes:\n'
    for row in manifest:yaml+='  - '+'\n    '.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in row.items())+'\n'
    (ROOT/'scenes.yaml').write_text(yaml,encoding='utf-8')

if __name__=='__main__':main()
