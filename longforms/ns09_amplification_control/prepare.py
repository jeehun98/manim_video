"""Act 9: amplification and control."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
SOURCES='- MIT Marine Hydrodynamics, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html\n- Pascanu et al. (2013), On the difficulty of training recurrent neural networks: https://proceedings.mlr.press/v28/pascanu13.html\n- Ba et al. (2016), Layer Normalization: https://arxiv.org/abs/1607.06450\n- He et al. (2016), Deep Residual Learning: https://arxiv.org/abs/1512.03385\n'
DATA=[('return', '처음의 두 메커니즘으로 돌아가다', 30, '처음에 우리는 나비에 스토크스 방정식 안에서 서로 다른 두 경향을 발견했습니다.\n유체의 흐름은 소용돌이를 늘어나게 만들고, 특정 조건에서 회전의 강도를 증폭시킬 수 있었습니다.\n반대편에서는 점성이 급격한 속도 차이와 보티시티의 변화를 확산시켰습니다.\n하나는 국소적인 회전을 강화할 수 있고, 다른 하나는 그것을 완화하는 효과를 가집니다.\n그렇다면 점성이 존재한다는 사실만으로, 소용돌이의 끝없는 증폭을 막을 수 있을까요?', '늘어나는 관과 확산 단면 → 같은 실제 흐름에서 두 효과', '늘어남은 점성 제외한 부피 보존 변형 예시. 확산은 2D Gaussian 보티시티의 단면 ω(x,0,t)=σ0²/σ² exp(−x²/2σ²), σ²=σ0²+2νt. 분리 비교는 전체 NS 해가 아니며 점성이 모든 위치의 ω를 매순간 감소시키는 것은 아님.'), ('competition', '점성이 존재해도 왜 문제가 어려웠을까?', 40, '소용돌이의 변화를 나타내는 방정식을 다시 보겠습니다.\n보티시티는 유체의 변형에 의해 증폭될 수 있고, 동시에 점성에 의해 확산됩니다.\n그런데 이 두 항이 항상 일정한 비율로 작용하는 것은 아닙니다.\n보티시티가 주변 흐름의 늘어나는 방향과 정렬되면 회전의 강도가 커질 수 있습니다.\n반면 점성의 효과는 보티시티가 공간적으로 어떻게 분포하는지에 따라 달라집니다.\n따라서 증폭 항과 확산 항이 존재한다는 사실만으로, 어느 쪽이 항상 우세한지 결정할 수는 없습니다.\n중요한 것은 두 효과가 실제 흐름 안에서 어떻게 결합되는가입니다.', '회전축 정렬과 공간 분포 · 같은 점성계수 · 경쟁의 조건', '상수 ν 비압축성, curl f=0의 보티시티 식. Ju=S+A에서 Aω=0; 자기 회전 강도 증가의 변형 효과는 ωᵀSω. 고정하는 것은 변형률 S이며 보티시티를 전체 Ju와 독립적으로 선택한다고 하지 않음. Laplacian은 분포에 의존하고 점별 부호가 일정하지 않음. 실제 3D 해나 특이점의 수치 시뮬레이션 아님.'), ('backprop', '신경망에서도 변화는 증폭될 수 있다', 40, '이제 신경망으로 돌아가 보겠습니다.\n앞에서는 작은 입력 변화가 야코비안을 통과하면서 방향에 따라 다르게 증폭되는 모습을 살펴봤습니다.\n그런데 신경망은 여러 층을 연속해서 통과합니다.\n한 층에서 변형된 변화는 다음 층으로 전달되고, 그다음 층의 야코비안에 다시 영향을 받습니다.\n역전파에서도 비슷한 문제가 나타납니다.\n여러 층의 야코비안이 반복해서 작용하면서, 특정 조건에서는 그래디언트의 크기가 급격하게 증가할 수 있습니다.\n이를 익스플로딩 그래디언트, 그래디언트 폭주라고 합니다.', '3층 방향 증폭 → 전달 방향 반전 → transpose 역전파', 'J_l=∂h(l+1)/∂h(l), δh(l+1)≈J_lδh(l), g_l=J_lᵀg(l+1). J=diag(2,.5) 3층의 정렬 e1 예시. 전방 활성값 자체와 작은 입력 변화, hidden gradient와 전체 파라미터 gradient는 구별. clipping 장면은 모은 파라미터 gradient를 사용.'), ('clipping', '큰 그래디언트를 잘라내면 해결될까?', 38, '그렇다면 그래디언트가 너무 커지는 것을 막으려면 어떻게 해야 할까요?\n한 가지 방법은 그래디언트의 크기에 상한을 두는 것입니다.\n그래디언트의 길이가 정해진 기준을 넘으면, 방향은 유지한 채 길이만 줄입니다.\n이를 그래디언트 클리핑이라고 합니다.\n단순한 그래디언트 디센트에서는, 이 방법으로 한 번의 업데이트가 지나치게 커지는 것을 제한할 수 있습니다.\n하지만 여기서 중요한 차이가 있습니다.\n그래디언트의 크기를 제한했다고 해서, 그래디언트가 커지는 내부 원인 자체가 사라진 것은 아닙니다.', 'global gradient norm 임계3 · 길이10→3, 방향 유지 · SGD 보폭', 'global L2 norm clipping c=3, g=(6,8), clipped=(1.8,2.4). g=0은 그대로0. plain SGD Δθ=−η clipped g, η=.1이므로 ||Δθ||≤.3. momentum/Adam/weight decay 적용 후 실제 업데이트의 같은 상한 보장은 아님. 내부 계산의 overflow 방지나 모든 Jacobian의 제약도 아님.'), ('where', '증폭을 막는 것과 결과를 제한하는 것은 다르다', 36, '두 가지 상황을 비교해 보겠습니다.\n첫 번째에서는 작은 변화가 여러 층을 통과하면서 계속 증폭됩니다.\n하지만 마지막에 그래디언트의 크기를 잘라냅니다.\n두 번째에서는 애초에 각 변환이 변화를 과도하게 증폭하지 않도록 설계합니다.\n두 경우 모두 최종적으로 큰 업데이트를 피할 수 있을지 모릅니다.\n하지만 작동하는 위치는 다릅니다.\n하나는 이미 커진 결과를 제한하고, 다른 하나는 내부의 변화가 전달되는 구조를 조절하려는 것입니다.', '결과 제한 1/2/4/8/3 vs 구조 제어1/1.2/1.1/1.3/1.2', 'A는 같은 방향 전달 모형에서1→2→4→8 후 clipping3. B는 [1,1.2,1.1,1.3,1.2], 단계 gain=다음/이전인 실제 선형 예시. 작은 개별 gain도 누적증폭될 수 있으며 이 모형을 전체 학습 안정성 보장으로 주장하지 않는다.'), ('design', 'Normalization과 Residual Connection은 무엇을 바꿀까?', 42, '신경망에는 그래디언트를 잘라내는 방법 외에도 여러 설계가 존재합니다.\n노멀라이제이션은 활성값의 분포나 크기를 조절하는 데 사용됩니다.\n레지듀얼 커넥션은 입력을 변환 결과에 더하는 경로를 만듭니다.\n이런 구조는 깊은 신경망의 학습을 돕지만, 모든 방향의 증폭을 무조건 억제하는 장치는 아닙니다.\n예를 들어 레지듀얼 블록의 변화율은 항등행렬과 변환의 야코비안의 합으로 나타납니다.\n따라서 잔차 경로가 존재한다는 사실만으로 전체 야코비안의 크기가 반드시 작아지는 것은 아닙니다.', '표준화의 값 분포 → skip와 F 경로 → Iδ와 JFδ 벡터 합', '표준화 예시 [10,12,14]→[-√1.5,0,√1.5], mean/std division, ε=0, 비제로분산, affine γ=1 β=0. 실제 norm 종류와 ε/learned scale은 별도. residual y=x+F(x), J=I+JF. JF=.8I→gain1.8, JF=−.8I→gain.2; 잔차 합의 방향에 따라다름. 모든 방향 축소 보장 없음.'), ('compare', '두 시스템의 안정화는 정말 같은 것일까?', 42, '이제 나비에 스토크스와 신경망을 다시 비교해 보겠습니다.\n유체에서 점성은 공간적인 차이를 확산시키는 물리적 메커니즘입니다.\n신경망에서 그래디언트 클리핑은 큰 업데이트를 제한하는 최적화 기법입니다.\n노멀라이제이션은 활성값의 표현을 변화시키고, 레지듀얼 커넥션은 정보가 전달되는 경로를 바꿉니다.\n이들은 서로 같은 수학적 연산이 아닙니다.\n그럼에도 공통된 질문을 던질 수 있습니다.\n어떤 과정에서 변화가 증폭될 수 있을 때, 그것을 제어하는 다른 메커니즘은 실제로 무엇을 제한하고 있을까요?\n그리고 그 제한은 시스템 전체의 안정성을 보장하기에 충분할까요?', '유체/역전파/순전파 비교 · 개입 대상과 위치 → 공통 질문', '점성은 물리적 공간 확산, clipping은 gradient 결과 제한, norm은 표현변환, residual은 전달경로. 동일 연산이 아님. 어떤 안정성 정의/조건인지 밝히지 않은 장치의 존재만으로 전체 보장을 내리지 않는다.'), ('transient', '정말 안정적인 시스템이라면 변화는 항상 작아질까?', 42, '그렇다면 안정적이라는 것은 정확히 무엇을 의미할까요?\n작은 변화가 매 순간 줄어든다는 뜻일까요?\n아니면 중간에는 커지더라도, 충분히 시간이 지나면 결국 사라진다는 뜻일까요?\n이 둘은 서로 다른 조건입니다.\n어떤 시스템에서는 모든 변화가 장기적으로 사라지더라도, 그 과정에서 일시적으로 크게 증폭될 수 있습니다.\n즉 마지막에는 안정적인 상태로 돌아온다는 사실만으로, 중간에 어떤 일이 발생하는지 모두 알 수는 없습니다.\n이제 안정성에 관한 질문을 한 번 더 바꿔보겠습니다.\n최종적으로는 안정적인데, 중간에는 큰 증폭이 나타날 수도 있을까요?', '단조 감소와 일시적 증폭 뒤 감소 · 실제 선형 모형의 크기 곡선 → 10막', '단조 curve ||e^(−t)z0||=e^(−t). 다른 curve A=[[-1,12],[0,-2]], z0=(0,1), z(t)=(12(e^(−t)−e^(−2t)),e^(−2t)). eigenvalues−1/−2, norm 처음1 중간약3 후0, 선형 점근안정이나 단조수축아님. 모든 시간이 유계이고 초기크기 비례. 실제 유체특이점/신경망학습 관측으로 주장하지 않는다. 10막에서 비정규성을 설명.')]

def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def main():
    manifest=[];master=['# 9막 — 증폭과 제어가 개입하는 위치'];tts=[];cues=[];offset=0
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
{DATA[i-2][1] if i>1 else '8막 마지막의 증폭과 안정화 질문'}
## TTS 원문과 확정 길이
{spoken}

- TTS: {'사용자 측정 '+str(duration)+'초' if voice else '미확정. 사용자 허용에 따라 화면 제작 우선.'}
- 화면: {duration}초. 원래 화면 기준은 {original}초.
## 화면 구성과 시간대별 애니메이션
{visual}
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
{title}, 보티시티, 변형률 정렬, 공간 확산, 층별 transpose, global norm clipping, 표준화, 잔차 합, 장기 감소와 일시적 증폭, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
{DATA[i][1] if i<len(DATA) else '10막: 비정규 동역학과 일시적 증폭'}
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
    (ROOT/'sources.md').write_text('# 출처와 확인 기준\n\n확인: 2026-10-08. 논문 관찰과 설명용 수치 모형을 구별한다. 물리적 확산과 최적화 결과 제한, 표현 변환, 전달 경로의 역할을 구별한다. Gaussian 확산과 선형 전달, 안정 선형 모형은 설명용 예시이며 실제 전체 NS 또는 대형 신경망의 측정값이 아니다.\n\n'+SOURCES,encoding='utf-8')
    yaml='id: ns09\ntitle: "9막 — 증폭과 안정화"\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\ntiming_basis: '+('user_sentence_end_times' if voice else 'visual_storyboard_without_tts')+'\nscenes:\n'
    for row in manifest:yaml+='  - '+'\n    '.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in row.items())+'\n'
    (ROOT/'scenes.yaml').write_text(yaml,encoding='utf-8')

if __name__=='__main__':main()
