"""Act 3: toy energy scaling, attributed construction, careful NN transition."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
SOURCES='- MIT Marine Hydrodynamics, Lecture 9, Vorticity Equation: https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec09/lecture9.html\n- FAMU-FSU Fluid Mechanics, Kinematics / Decomposition: https://web1.eng.famu.fsu.edu/~dommelen/courses/flm/10/topics/kine/node5.html\n- Stanford CS231n, Derivatives, Backpropagation, and Vectorization: https://cs231n.stanford.edu/2017/handouts/derivatives.pdf\n- MIT OCW, Singular Value Decomposition: https://ocw.mit.edu/courses/res-18-009-learn-differential-equations-up-close-with-gilbert-strang-and-cleve-moler-fall-2015/resources/singular-value-decomposition-the-svd/\n'
DATA=[('vortex', '소용돌이는 왜 축을 따라 늘어났을까?', 34, '앞에서 삼차원의 소용돌이는 회전축을 따라 늘어나면서, 회전의 강도가 커질 수 있다고 했습니다.\n왜 하필 회전축을 따라 늘어나는 것이 중요할까요?\n보티시티 벡터의 방향은 국소적인 회전축을, 길이는 회전의 강도를 나타냅니다.\n이 축을 따라 주변의 속도가 달라지면, 소용돌이를 잡아 늘리는 효과가 생길 수 있습니다.\n반대로 압축되면 회전이 약해질 수 있고, 변형에 의해 축의 방향도 기울어질 수 있습니다.', '부피 보존 3D 관 → 보티시티 축 → 축 늘어남/압축/전단 비교', '점성과 외력의 컬에 의한 생성은 제외해 변형 효과만 분리한 개념도. F=diag(s⁻¹/²,s⁻¹/²,s), 이후 x←x+kz 전단은 detF=1. 보티시티는 Fω0로 변화하는 비점성 국소 변형 예시. 기울어짐이 순수 강체 회전 때문이라고 하지 않는다.'), ('derivative', '주변의 변화율을 한 장에 기록하다', 36, '유체의 속도는 위치에 따라 달라집니다. 이동하는 방향에 따라, 만나는 속도의 변화도 다릅니다.\n아주 작은 거리를 세 방향으로 움직이며, 속도가 어떻게 달라지는지 기록해 보겠습니다.\n이 정보를 모은 행렬을 속도장의 야코비안이라고 합니다.\n여기에 보티시티 벡터를 곱하면, 회전축 방향을 따라 속도장이 어떻게 변하는지 계산할 수 있습니다.\n이 곱은 다음 순간의 보티시티 자체가 아니라, 보티시티의 시간 변화에 들어가는 하나의 항입니다.', 'x/y/z 작은 변위 → 속도 차이 → Jacobian 카드 → ω 통과 → 시간 변화율 항', 'Jij=∂ui/∂xj convention. (ω·∇)u=Juω 정확한 항등식. 물질 미분Dω/Dt=Juω+νΔω+curl f. Juω의 단위는 ω/time이며 NN의 유한 확대비와 다르다. 프로브예시 J=[[-.5,-.5,0],[.5,-.5,0],[0,0,1]], omega=(0,0,1).'), ('alignment', '같은 강도라도, 회전축 방향이 다르면', 34, '이번에는 주변 흐름의 늘어남과 압축 효과를 고정하겠습니다.\n길이가 같은 보티시티 벡터를, 늘어나는 방향과 압축되는 방향에 각각 놓아보겠습니다.\n늘어나는 방향과 정렬되면 강해지고, 압축되는 방향과 정렬되면 약해지는 효과를 받습니다.\n비스듬한 방향에서는 길이뿐 아니라 방향도 달라질 수 있습니다.\n회전의 크기만큼, 회전축이 주변 변형의 어느 방향을 가리키는지도 중요합니다. 여기서는 점성의 영향을 잠시 제외했습니다.', '고정 S의 x-z 단면 → 같은 길이 ω 방향0/90/45도 → 짧은 시간 뒤 변화 → signed 증감 지표', '고정하는 것은 S=diag(-.5,-.5,1)이고 독립적으로 omega 방향을 비교한다. 하나의 고정된 전체 Ju에서 omega를 독립적으로 바꿀 수 있다고 주장하지 않는다. 1/2 D|ω|²/Dt=ωᵀSω (ν=0,curl f=0). A=(Ju−Juᵀ)/2, Aω=0; 자체 vorticity를 국소 강체회전 성분이 기울인다고 하지 않는다. 짧은 뒤 exp(.3S)omega 설명용 비교.'), ('shared', '신경망에도, 변화율이 방향에 작용한다', 40, '이제 하나의 신경망 입력을 고정하고, 그 주변에서 아주 작은 변화를 주겠습니다.\n변화의 크기가 같아도, 어느 방향으로 움직였는지에 따라 출력의 반응은 달라질 수 있습니다.\n이 작은 반응을 계산할 때도 야코비안이 등장합니다.\n신경망의 야코비안에 작은 입력 변화 벡터를 곱하면, 출력의 변화를 국소적으로 근사할 수 있습니다.\n유체에서는 공간의 변화율이 보티시티에 작용했습니다. 신경망에서는 입력에 대한 변화율이 입력의 작은 변화에 작용합니다.\n공통점은 행렬이 방향 벡터에 작용한다는 구조입니다. 유체의 시간 발전과 신경망의 입력 반응은 서로 다른 현상입니다.', '유체 관/NN 입력 원 → 작은 입력 원과 출력 타원 → 두 Jacobian×Vector 색상 대응 → 결과 해석 구별', '미분 가능한 f의 기준입력에서 δy=Jf(x)δx+o(||δx||). 원-타원은 magnified local linear model, 실제 비선형 신경망의 큰 입력 영역을 정확히 타원으로 변환한다고 하지 않는다. Juω는 미분 항, Jfδx는 국소 출력 변화 근사.'), ('ellipse', '원은, 어느 방향에서 가장 늘어날까?', 38, '입력 주변의 작은 원 위에서는, 모든 변화가 중심에서 같은 거리만큼 떨어져 있습니다.\n이 변화를 신경망에 통과시키면, 국소적인 선형 근사에서는 원이 타원으로 바뀔 수 있습니다.\n야코비안은 고정하고, 입력 변화의 방향만 돌려보겠습니다.\n어떤 방향에서는 출력이 크게 늘어나고, 다른 방향에서는 줄어듭니다.\n가장 많이 늘어나는 방향의 확대 비율을, 야코비안의 가장 큰 특잇값이라고 합니다. 같은 입력 크기라도 방향에 따라 반응이 달라지는 것입니다.', '단위 방향 원 → diag(1.8,.5) 타원 → theta30/90/0도 → gain1.58/.5/1.8 → sigma_max', 'J=diag(1.8,.5) 국소 예시. 실제 입력 반경ε의 그림을 확대해 ||v||=1 방향으로 표시. ratio=sqrt((1.8cosθ)²+(.5sinθ)²), θ30 gain≈1.578765. σmax=1.8, 최소=.5. 일반 네트워크의 보장값이 아니다.'), ('layers', '다음 층에서도 같은 방향으로 늘어날까?', 36, '이제 작은 변화가 여러 층을 통과한다고 생각해 보겠습니다.\n한 층에서 변한 방향과 크기는 다음 층으로 전달됩니다. 다음 층의 야코비안이 여기에 다시 작용합니다.\n연속된 층에서 늘어나는 방향과 잘 맞으면, 작은 차이가 점점 커질 수 있습니다.\n하지만 다음 층에서 압축되는 방향과 만난다면, 앞에서 커진 변화가 다시 작아질 수 있습니다.\n각 층의 최대 확대 비율만큼, 층 사이에서 방향이 어떻게 연결되는지도 중요합니다. 이 층별 합성은 유체의 시간 발전과 구별해야 합니다.', '3층 선형 국소 모형 → 1/1.8/3.24/5.832 → 두번째 층 압축축 교체 → 1/1.8/.9/1.62', '연쇄법칙 Jtotal=JL…J1 (각 J는 해당 기준 hidden state에서 평가). aligned 3×diag(1.8,.5) e1gain5.832, middle=diag(.5,1.8) e1gain1.62. 각 σmax1.8이며 ∥product∥≤∏σmax, equality 보장하지 않는다.'), ('next', '진짜 공통점은, 방향에 따른 작용', 42, '이제 소용돌이와 신경망을 나란히 보겠습니다.\n유체의 변화율은 보티시티의 시간 변화에 관여하고, 신경망의 변화율은 작은 입력 변화에 대한 출력 반응을 알려줍니다.\n유체의 순간적인 강도 증감은 변형률과의 정렬로, 신경망의 최대 국소 확대는 야코비안의 특잇값으로 살펴봅니다.\n두 현상을 같은 것으로 만드는 것이 아니라, 변화율이 모든 방향에 똑같이 작용하지 않는다는 구조를 공유하는 것입니다.\n이제 입력 공간에서 파라미터 공간으로 질문을 옮겨보겠습니다. 손실 지형에도 가파른 방향과 평평한 방향이 함께 있을 수 있습니다.\n그렇다면 단 하나의 가파른 방향이 전체 학습을 제한할 수도 있을까요? 다음 막에서는 이 방향성을 헤시안으로 살펴보겠습니다.', '소용돌이/원타원 나란히 → Local derivative×Direction → S 정렬/σ 구별 → 우측만 손실 등고선 → 7막 Hessian 질문', '입력 Jacobian과 파라미터 손실 Hessian은 서로 다른 미분 대상. 다음 막 contour L=.5(4θ1²+.25θ2²) 예시, stiffness 방향x. 유체 자체vorticity의 antisymmetric part Aω=0. 결과 동일성/신경망 유체 PDE 동일성 주장하지 않는다.')]

def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def main():
    manifest=[];master=['# 6막 — 소용돌이와 신경망의 방향별 작용'];tts=[];cues=[];offset=0
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
        spoken='\n\n'.join(lines);tts.append(spoken)
        (directory/'script.txt').write_text(spoken+'\n',encoding='utf-8')
        master.append(f'## {i:02} — {title} ({stamp(offset)}–{stamp(offset+duration)})\n\n'+spoken)
        (directory/'spec.md').write_text(f'''# Scene {i:02} — {title}
## 목적과 핵심 주장
{title}를 한 장면에서 이해시킨다.
## 앞 장면에서 받은 내용
{DATA[i-2][1] if i>1 else '5막 마지막의 값의 크기와 방향별 증폭에 관한 질문'}
## TTS 원문과 확정 길이
{spoken}

- TTS: {'사용자 측정 '+str(duration)+'초' if voice else '미확정. 사용자 허용에 따라 화면 제작 우선.'}
- 화면: {duration}초. 원래 화면 기준은 {original}초.
## 화면 구성과 시간대별 애니메이션
{visual}
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
{title}, 보티시티와 변형 방향, 입력 원과 출력 타원, 국소 확대 비율, 층별 방향 연결, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
{DATA[i][1] if i<len(DATA) else '7막: Hessian과 가파른 방향'}
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
    (ROOT/'sources.md').write_text('# 출처와 확인 기준\n\n확인: 2026-10-08. 논문 관찰과 설명용 수치 모형을 구별한다. 변화율 항과 확대 비율을 구별한다. 고정 S의 보티시티 방향 비교와 국소 Jacobian 예시는 설명용이다.\n\n'+SOURCES,encoding='utf-8')
    yaml='id: ns06\ntitle: "6막 — 방향별 증폭과 Jacobian"\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\ntiming_basis: '+('user_sentence_end_times' if voice else 'visual_storyboard_without_tts')+'\nscenes:\n'
    for row in manifest:yaml+='  - '+'\n    '.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in row.items())+'\n'
    (ROOT/'scenes.yaml').write_text(yaml,encoding='utf-8')

if __name__=='__main__':main()
