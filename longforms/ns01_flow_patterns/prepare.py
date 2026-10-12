"""Create the seven independent storyboard units and estimated subtitle cues."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
DATA = [
('freeze', '물을 멈춰서 바라본다면?', 28, '물의 움직임은 위치마다 다른 속도와 방향으로 표현할 수 있다.',
'''우리가 보는 물은 끊임없이 형태를 바꿉니다.
잔잔한 물결이 생기고, 물줄기가 휘어지고, 때로는 복잡한 소용돌이가 만들어집니다.
그런데 이 움직임을 한순간 멈춰서, 물속의 모든 위치를 살펴본다면 어떨까요?
각 위치에는 저마다 다른 속도와 방향이 있을 것입니다.''',
'흐르는 곡선 → 정지 → 위치마다 속도 화살표 → 곡선이 사라지고 속도장만 남음'),
('field', '물을 하나의 속도장으로 바꾸다', 29, '속도장은 각 위치의 속도 벡터이며 시간에 따라 변한다.',
'''이제 물을 개별 분자가 아니라, 공간 전체에 펼쳐진 속도 화살표들의 집합으로 표현해 보겠습니다.
어느 위치에서 얼마나 빠르게, 어느 방향으로 움직이는지를 나타내는 것입니다.
이를 속도장, Velocity Field라고 합니다.
시간이 흐르면 화살표들도 변합니다.
Navier–Stokes 방정식은 바로 이 속도장이 시간에 따라 어떻게 변하는지 기술합니다.''',
'규칙적 화살표 → 위치와 속도 강조 → 방향·길이 변화 → u(x,t)'),
('roles', '속도장을 바꾸는 네 가지 역할', 35, '이류·압력·점성·외력이 다음 순간의 속도장을 함께 결정한다.',
'''방정식은 복잡해 보이지만, 각 항이 하는 일은 비교적 분명합니다.
유체가 현재 속도를 따라 이동하면서 다른 위치의 속도 분포를 바꾸는 이류.
압력 차이가 유체를 밀어내는 압력 항.
서로 다른 속도를 가진 영역 사이에서 운동량을 확산시키는 점성 항.
그리고 중력이나 외부에서 가하는 힘입니다.
이 역할들이 결합하면서 다음 순간의 속도장이 결정됩니다.''',
'수식 고정 → 이류·압력·점성·외력 순서로 동일 격자에 효과를 시연 → 네 항 결합'),
('advection', '흐름은 자신의 구조를 운반한다', 32, '불균일한 흐름은 운반되는 구조를 변형한다.',
'''이류 항을 조금 더 자세히 보겠습니다.
유체는 움직이면서 자신이 가진 속도의 분포도 함께 운반합니다.
그런데 모든 부분이 같은 방향과 속도로 움직이지는 않습니다.
어떤 부분은 빠르게, 다른 부분은 느리게 이동합니다.
그래서 처음에는 단순했던 구조가 점점 휘어지고 늘어나거나 압축될 수 있습니다.
중요한 것은 유체의 움직임이 다시 다음 순간의 유체 움직임을 결정한다는 것입니다.''',
'같은 표지 영역 → 균일한 운반 / 면적 보존 전단 변형 비교 → 불균일한 흐름 확대'),
('viscosity', '점성은 속도 차이를 퍼뜨린다', 31, '점성은 운동량을 확산해 급격한 속도 차이를 완화한다.',
'''반대쪽에는 점성이 있습니다.
빠르게 흐르는 영역 옆에 느린 영역이 있다고 생각해 보겠습니다.
점성은 두 영역 사이의 운동량을 전달합니다.
빠른 영역의 속도는 주변과의 차이가 줄어들고, 느린 영역도 영향을 받습니다.
이 과정에서 급격한 속도 차이가 점차 완화됩니다.
이것이 점성에 의한 확산입니다.''',
'중앙의 빠른 띠 → 주변 운동량 전달 → 최고값 감소·폭 증가 → 완만한 속도 분포'),
('compare', '같은 구조, 서로 다른 두 경향', 38, '실제 유체에서는 이류와 점성이 동시에 작용하며 중요도는 조건에 따라 달라진다.',
'''이제 같은 초기 구조를 두 가지 방식으로 변화시켜 보겠습니다.
한쪽에서는 흐름의 불균일함 때문에 구조가 계속 변형됩니다.
다른 쪽에서는 점성이 속도 차이를 주변으로 확산시킵니다.
실제 유체에서는 이 과정들이 따로 일어나지 않습니다.
같은 순간, 같은 공간에서 동시에 일어납니다.
그리고 어느 효과가 더 중요해지는지는 흐름의 크기와 속도, 점성의 크기, 그리고 구조의 공간적 스케일에 따라 달라집니다.''',
'동일한 초기 전단 띠 분기 → 이류 운반·전단 / 점성 확산 → 하나의 합성 설명 화면 → U,L,ν,ℓ'),
('question', '그렇다면 어느 쪽이 이기는가?', 29, '매끄러움이 항상 유지되는지는 3차원 비압축성 유체의 핵심 질문이다.',
'''처음에 매끄러웠던 유체가 있다고 생각해 보겠습니다.
시간이 지나면서 복잡한 흐름이 생기고, 더 작고 날카로운 구조들이 만들어질 수 있습니다.
점성은 계속 그 구조들을 완화하려고 합니다.
그렇다면 점성은 언제나 이런 변화를 충분히 억제할 수 있을까요?
아니면 유체 내부에서 만들어지는 구조가 점점 더 강해져, 매끄러움이 무너지는 순간이 생길 수도 있을까요?
이 질문이 Navier–Stokes의 가장 어려운 문제 중 하나로 이어집니다.
그리고 이 문제가 특히 흥미로워지는 곳이 바로 3차원입니다.''',
'매끄러운 장 → 회전하는 곡선과 완화 효과 → 정지 → 3차원 소용돌이 단면으로 전환'),
]

def stamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def main():
    all_cues=[]; offset=0; manifest=[]; master=['# 1막 — 물은 왜 매끄러워야 하는가?\n']; tts_sections=[]
    voice_path=ROOT/'voice_timing.json'
    voice=json.loads(voice_path.read_text(encoding='utf-8')) if voice_path.exists() else None
    if voice:
        assert len(voice['ends'])==sum(len(row[4].splitlines()) for row in DATA)
        assert all(a<b for a,b in zip([0]+voice['ends'][:-1],voice['ends']))
    sentence_index=0
    for i,(slug,title,duration,claim,script,visual) in enumerate(DATA,1):
        storyboard_duration=duration
        directory=ROOT/'scenes'/f'{i:02}_{slug}'; directory.mkdir(parents=True,exist_ok=True)
        tts=script.replace('Velocity Field','벨로시티 필드').replace('Navier–Stokes','나비에 스토크스').replace('3차원','삼차원')
        tts='\n\n'.join(tts.splitlines())
        (directory/'script.txt').write_text(tts+'\n',encoding='utf-8')
        tts_sections.append(tts)
        lines=script.splitlines(); weights=[len(s)+10 for s in lines]; total=sum(weights)
        if voice:
            measured_ends=[end-offset for end in voice['ends'][sentence_index:sentence_index+len(lines)]]
            duration=measured_ends[-1]
        sentence_index+=len(lines)
        current=0; cues=[]; ends=[]
        for line_index,(line,w) in enumerate(zip(lines,weights)):
            end=measured_ends[line_index] if voice else current+duration*w/total
            cues.append(f'{len(cues)+1}\n{stamp(current)} --> {stamp(end)}\n{line}')
            all_cues.append(f'{len(all_cues)+1}\n{stamp(offset+current)} --> {stamp(offset+end)}\n{line}')
            ends.append(end); current=end
        (directory/'captions.srt').write_text('\n\n'.join(cues)+'\n',encoding='utf-8')
        (directory/'timing.json').write_text(json.dumps({'duration':duration,'ends':ends,'lines':lines,'basis':voice['basis'] if voice else 'storyboard; TTS not measured'},ensure_ascii=False,indent=2),encoding='utf-8')
        spec=f'''# Scene {i:02} — {title}
## 목적과 핵심 주장
{claim}
## 앞 장면에서 받은 내용
{DATA[i-2][3] if i>1 else '없음. 1막 도입.'}
## TTS 원문과 길이
{script}

- TTS 길이: {'사용자 제공 문장별 누적 시각 기준 '+str(duration)+'초. 실제 음원 파일은 없음.' if voice else '미정. 음원 없음.'}
- 화면 길이: {duration}초. 원래 콘티 길이: {storyboard_duration}초.
## 화면 구성과 애니메이션
{visual}
문장별 구간은 timing.json의 ends를 사용한다. {'사용자가 제공한 문장별 종료 시각을 적용한다.' if voice else '내레이션 분량으로 배분한 추정값이다.'}
## 화면 텍스트
{title}, 핵심 연산·수식, 문장별 자막. 수식은 원래 기호를 유지한다.
## 시작·종료 상태
시작: 위 흐름의 첫 대상. 종료: 마지막 대상과 다음 질문. 공통 배경과 색 체계를 유지한다.
## 다음 장면 연결
{DATA[i][3] if i<7 else '2막: 3차원 소용돌이의 늘어남은 왜 중요한가?'}
## 수학적 조건과 과장 방지
- 일정 밀도·점성의 비압축성 유체. p는 밀도로 나눈 압력, f는 단위 질량당 외력, ∇·u=0.
- 이류가 항상 작은 구조를 만들지는 않는다. 점성은 모든 위치의 속도를 일률적으로 줄이지 않는다.
- 운반되는 색 영역은 수동 표지이며 속도 자체와 동일하지 않다. 전단 변형은 면적을 보존한다.
- 점성 예시는 x 방향 속도 u_x(y)의 열 방정식 확산이다. 최고값은 줄고 주변값은 커진다.
- 6번 분리 비교는 설명용 연산 시연이며 전체 Navier–Stokes 해의 수치 시뮬레이션이 아니다.
- 7번은 질문을 제시한다. 특이점·실제 자기증폭·vortex stretching의 결과를 보여주지 않는다.
'''
        (directory/'spec.md').write_text(spec,encoding='utf-8')
        (directory/'scene.py').write_text(f"from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom visuals import FlowScene\n\nclass Scene{i:02}(FlowScene):\n    index = {i}\n",encoding='utf-8')
        manifest.append({'id':f'{i:02}','slug':slug,'directory':f'scenes/{i:02}_{slug}','class':f'Scene{i:02}','duration_seconds':duration if voice else None,'storyboard_seconds':storyboard_duration})
        master.append(f'## {i:02}. {title} ({stamp(offset)}–{stamp(offset+duration)})\n\n{script}\n')
        offset+=duration
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    yaml='id: ns01\ntitle: "1막 — 물은 왜 매끄러워야 하는가?"\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\ntiming_basis: '+('user_sentence_end_times' if voice else 'storyboard_without_audio')+'\nscenes:\n'
    for s in manifest:
        yaml+='  - '+ '\n    '.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in s.items())+'\n'
    (ROOT/'scenes.yaml').write_text(yaml,encoding='utf-8')
    (ROOT/'master_script.md').write_text('\n'.join(master),encoding='utf-8')
    (ROOT/'tts_script.txt').write_text('\n\n'.join(tts_sections)+'\n',encoding='utf-8')
    (ROOT/'captions.srt').write_text('\n\n'.join(all_cues)+'\n',encoding='utf-8')

if __name__=='__main__': main()
