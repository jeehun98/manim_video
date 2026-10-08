"""Storyboard-first Act 2; narration timing remains provisional until TTS."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
DATA=[
('plane','평면에서는 축을 늘릴 수 없다',25,
'''왜 삼차원일까요? 먼저 이차원의 소용돌이부터 살펴보겠습니다.
평면 위에서도 소용돌이는 이동하고, 주변 흐름 때문에 모양이 찌그러질 수 있습니다.
하지만 회전축은 언제나 평면에 수직입니다.
흐름이 평면 안에만 있다면, 이 축을 따라 소용돌이를 잡아 늘릴 수는 없습니다.''',
'평면 격자와 소용돌이 → 면적 보존 전단 변형 → 수직 축 강조 → 축방향 흐름 없음'),
('vorticity','회전의 방향과 강도 — 보티시티',28,
'''회전의 강도와 방향을 나타내는 물리량을 와도, 영어로는 보티시티라고 합니다.
작은 유체 조각 하나를 생각해 보겠습니다.
주변의 속도 차이에는 이 조각을 회전시키는 성분이 있습니다.
보티시티는 속도장의 컬로 정의되며, 국소적인 회전의 강도와 축 방향을 나타냅니다.
단순한 강체 회전에서는 보티시티의 크기가 각속도의 두 배입니다.
이차원에서는 회전축 방향이 고정되어, 부호를 가진 하나의 값으로 표현할 수 있습니다.''',
'작은 십자 원판 → 접선 속도 벡터 → 원판 회전 → ω=∇×u → ω=2Ω → 부호 있는 와도 색 지도'),
('tube','평면을 벗어나면, 관이 보인다',27,
'''이제 소용돌이를 삼차원에서 바라보겠습니다.
회전하는 단면들을 축 방향으로 이어 놓으면, 관 같은 구조를 생각할 수 있습니다.
유체는 관 둘레를 따라 회전하고, 보티시티 벡터는 관의 축을 가리킵니다.
삼차원에서는 주변 흐름이 축 방향으로도 달라질 수 있습니다.
바로 이 방향의 변형이 새로운 회전 증폭 경로를 만듭니다.''',
'평면 원 → 투영된 원형 단면 → 3D 관 → 접선 회전과 축 벡터 → 양끝 외향 흐름'),
('stretch','길어지고, 가늘어지고, 강해진다',32,
'''같은 유체 조각으로 이루어진 짧고 두꺼운 관을 보겠습니다.
주변 흐름이 축 방향으로 관을 늘립니다.
길이가 두 배가 되면, 부피를 유지하기 위해 단면적은 절반이 됩니다.
그래서 반지름은 루트 이 분의 일 배가 됩니다.
점성의 영향을 잠시 제외한 이상적인 축 방향 늘어남에서는 보티시티도 두 배로 커집니다.
이것이 소용돌이 늘어남, 보텍스 스트레칭입니다.
왜 회전이 강해지는지는 방정식으로 확인해 보겠습니다.''',
'λ=1 관 → 외향 축 흐름 → λ=2, L×2, A/2 → r/√2 → ω×2 → 부피와 와도 구분'),
('equation','보티시티를 바꾸는 새로운 항',31,
'''유체 조각을 따라가며 보티시티의 변화를 살펴봅시다.
점성 확산을 나타내는 항 옆에, 보티시티 방향으로 유체가 얼마나 늘어나거나 변형되는지를 나타내는 항이 있습니다.
유체가 보티시티의 방향으로 늘어나면, 이 항은 회전의 강도를 키울 수 있습니다.
반대로 압축되는 방향에서는 회전이 약해질 수도 있고, 주변 흐름에 의해 회전축의 방향이 바뀔 수도 있습니다.
보티시티와 속도장은 서로 연결되어 있어, 변화한 흐름이 다른 소용돌이의 변형에도 영향을 줍니다.
증폭의 경로는 있지만, 모든 소용돌이가 저절로 끝없이 강해진다는 뜻은 아닙니다.''',
'Dω/Dt → stretching+diffusion 수식 → Sω 정렬 → 양/음 방향 대비 → 상태-속도장-변형 경로 → 증폭은 조건부'),
('competition','늘어남과 확산은 함께 작용한다',30,
'''다시 같은 초기 소용돌이에서 출발하겠습니다.
늘어남만 강조하면, 회전이 길고 가는 관에 집중될 수 있습니다.
점성 확산만 강조하면, 보티시티가 주변으로 퍼지며 급격한 차이가 완화됩니다.
실제 흐름에서는 이 두 과정이 함께 작용합니다.
따라서 중요한 질문은 증폭이 가능한가에서 끝나지 않습니다.
증폭과 완화의 경쟁이, 더 작은 스케일에서도 어떻게 이어지는가를 봐야 합니다.''',
'同 초기 관 둘 → 축 늘어남 / 가우시안 와도 확산 → 효과 합성 개념 → 증폭률 / ν/ℓ²'),
('contrast','두 차원을 가르는 하나의 항',37,
'''이차원과 삼차원의 차이를 나란히 놓아보겠습니다.
엄밀한 이차원 흐름에는 회전축을 따라 늘어나는 항이 없습니다.
적절한 초기 조건과 공간 조건을 갖춘 이차원 점성 유체는, 매끄러움이 모든 시간에 유지됩니다.
삼차원에는 보티시티를 증폭하거나 방향을 바꾸는 추가적인 항이 있습니다.
이 항을 제어하는 일이 삼차원의 매끄러움 문제를 어렵게 만듭니다.
다만 보티시티가 커지는 모습만으로 특이점이 생겼다고 말할 수는 없습니다.
다음에는 질문을 바꿔보겠습니다.
전체 에너지가 유한해도, 아주 작은 영역의 강도는 끝없이 커질 수 있을까요?''',
'2D / 3D 방정식 비교 → 2D zero stretching → 조건부 regularity → 3D 추가 항 → 관측과 특이점 구별 → 국소 영역 강조 → 3막 질문'),
]

def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def main():
    manifest=[];master=['# 2막 — 왜 3차원에서는 소용돌이가 스스로 강해질 수 있을까?'];tts=[];cues=[];offset=0
    voice_path=ROOT/'voice_timing.json'
    voice=json.loads(voice_path.read_text(encoding='utf-8')) if voice_path.exists() else None
    if voice:
        assert len(voice['ends'])==sum(len(row[3].splitlines()) for row in DATA)
        assert all(a<b for a,b in zip([0]+voice['ends'][:-1],voice['ends']))
    sentence_index=0
    for i,(slug,title,duration,script,visual) in enumerate(DATA,1):
        storyboard_duration=duration
        directory=ROOT/'scenes'/f'{i:02}_{slug}';directory.mkdir(parents=True,exist_ok=True)
        lines=script.splitlines();weights=[len(s)+12 for s in lines]
        if voice:
            measured_ends=[end-offset for end in voice['ends'][sentence_index:sentence_index+len(lines)]]
            duration=measured_ends[-1]
        sentence_index+=len(lines)
        current=0;ends=[];local=[]
        for line_index,(line,w) in enumerate(zip(lines,weights)):
            end=measured_ends[line_index] if voice else current+duration*w/sum(weights);ends.append(end)
            local.append(f'{len(local)+1}\n{stamp(current)} --> {stamp(end)}\n{line}')
            cues.append(f'{len(cues)+1}\n{stamp(offset+current)} --> {stamp(offset+end)}\n{line}')
            current=end
        (directory/'captions.srt').write_text('\n\n'.join(local)+'\n',encoding='utf-8')
        (directory/'timing.json').write_text(json.dumps({'duration':duration,'ends':ends,'lines':lines,'basis':voice['basis'] if voice else 'visual storyboard; not measured TTS'},ensure_ascii=False,indent=2),encoding='utf-8')
        spoken='\n\n'.join(lines)
        (directory/'script.txt').write_text(spoken+'\n',encoding='utf-8');tts.append(spoken)
        master.append(f'## {i:02} — {title} ({stamp(offset)}–{stamp(offset+duration)})\n\n'+spoken)
        spec=f'''# Scene {i:02} — {title}
## 목적과 핵심 주장
{title}. 아래 역할을 하나의 완결된 장면으로 설명한다.
## 앞 장면에서 받은 내용
{DATA[i-2][1] if i>1 else '1막 마지막 질문: 왜 삼차원인가?'}
## TTS 원문과 확정 길이
{spoken}

- TTS 길이: {'사용자 제공 문장 종료 시각 기준 '+str(duration)+'초. 실제 음원 파일은 없음.' if voice else '미확정. 화면 제작을 먼저 진행한다.'}
- 화면 길이: {duration}초. {'사용자 제공 문장별 시각에 맞춘다.' if voice else '문장별 타이밍은 추정이다.'} 원래 콘티 길이는 {storyboard_duration}초.
## 화면 구성과 시간대별 애니메이션
{visual.replace('同','동일한')}
각 문장의 순서대로 timing.json의 ends에 맞춰 cue를 진행한다. 시작 상태는 첫 대상, 종료 상태는 마지막 대상이다.
## 화면 텍스트
{title}. 수식은 원래 기호를 사용하고 한글 발음은 음성 대본에만 사용한다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목·하단 자막 안전 영역을 공통 사용한다.
## 다음 장면 연결
{DATA[i][1] if i<7 else '3막: 유한한 전체 에너지와 국소적인 강도 증가'}
## 수학적 조건과 과장 방지
- 일정 밀도·점성, 비압축성, curl f=0인 외력(외력 없는 경우 포함). curl f≠0인 외력을 넣으면 보티시티 방정식에 curl f가 추가된다.
- 엄밀한 2D: u=(u1(x,y),u2(x,y),0), ∂z u=0, ω=(0,0,ωz). 따라서 (ω·∇)u=0.
- 3D stretching 항은 (∇u)ω=Sω. 와도와 strain 방향에 따라 강화·약화·재배향이 가능하다.
- 관은 3D 좌표를 직교 투영한 개념도다. λ=L/L0, r=r0/√λ, 부피 πr²L 일정.
- 점성 제외 국소 affine 예: u=(-a x/2-Ωy, Ωx-a y/2, az), Ω'=aΩ. λ=e^(at), ωz=2Ω=ω0λ. 전역 유한 에너지 해를 주장하지 않는다.
- 부피 보존만으로 와도 증폭을 도출하지 않는다. 와도 성장에는 stretching 방정식과 정렬 조건이 필요하다.
- 확산 경로는 고정 길이의 가우시안 와도 단면이며 σ²가 증가, 최고값은 1/σ²로 감소한다. 관의 물질 부피 팽창을 뜻하지 않는다.
- 2D 매끄러움은 적절한 매끄러운 발산 없는 초기 자료, 주기 공간 또는 적절한 감쇠 조건 등을 갖춘 ν>0 흐름에 대한 진술이다.
- stretching과 확산의 분리 화면은 개념 비교다. 결합 화면은 전체 PDE 수치 해가 아니다.
- 와도 증가만으로 속도의 유한 시간 특이점을 결론내리지 않는다. 2026년 특정 결과나 증명은 다루지 않는다.
## 검토 출처
- https://virtualmath1.stanford.edu/~ryzhik/notes-256B-24.pdf (vorticity, 2D/3D, strain, regularity)
- https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf (문제의 자료·공간 조건)
'''
        (directory/'spec.md').write_text(spec,encoding='utf-8')
        (directory/'scene.py').write_text(f"from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import VortexScene\n\nclass Scene{i:02}(VortexScene):\n    index={i}\n",encoding='utf-8')
        manifest.append({'id':f'{i:02}','slug':slug,'directory':f'scenes/{i:02}_{slug}','class':f'Scene{i:02}','duration_seconds':duration if voice else None,'storyboard_seconds':storyboard_duration})
        offset+=duration
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'master_script.md').write_text('\n\n'.join(master)+'\n',encoding='utf-8')
    (ROOT/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(cues)+'\n',encoding='utf-8')
    yaml='id: ns02\ntitle: "2막 — 소용돌이 늘어남"\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\ntiming_basis: '+('user_sentence_end_times' if voice else 'visual_storyboard_without_tts')+'\nscenes:\n'
    for row in manifest:yaml+='  - '+'\n    '.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in row.items())+'\n'
    (ROOT/'scenes.yaml').write_text(yaml,encoding='utf-8')

if __name__=='__main__':main()
