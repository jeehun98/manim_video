"""Act 3: toy energy scaling, attributed construction, careful NN transition."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
SOURCES='''- https://openai.com/index/navier-stokes-solution/ (2026-09-08 発表)
- https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf (Theorem 1.1, §2, Figure 1)
- https://www.claymath.org/news/navier-stokes-announcement/ (2026-09-11)
'''.replace('発表','발표')
DATA=[('rules', '원하는 모양이면 충분할까?', 27, '전체 에너지는 유한하지만, 작은 영역의 속도가 계속 커지는 모습을 상상할 수 있습니다.\n그런 그림 하나만으로 실제 유체의 움직임을 설명할 수 있을까요?\n유체는 이동과 압력, 점성이 함께 작용하는 운동 법칙을 따라야 합니다.\n이번 막의 질문은, 극단적인 모양을 그리는 데서 실제 흐름을 만드는 일로 넘어갑니다.', '설계한 집중 그림과 운동 법칙의 문 연결 → 조건의 문을 통과해야 실제 해', '발산 함수와 NS 해를 구별한다. 실제 PDE 계산 장면이 아니다.'), ('reverse', '흐름에서 필요한 힘으로', 28, '보통은 힘을 가한 뒤, 물이 어떻게 움직이는지 생각합니다.\n이번에는 생각의 방향을 뒤집어 보겠습니다. 먼저 만들고 싶은 흐름을 정합니다.\n그리고 그 흐름을 이루려면 어떤 힘이 필요한지 거꾸로 따져봅니다.\n이 관점은 출발점입니다. 원하는 흐름을 정했다고 모든 조건이 저절로 맞는 것은 아닙니다.', '힘→흐름 화살표 → 방향 반전 → 원하는 흐름→필요한 힘 → 조건 확인', '외력 역산의 직관이다. 압력과 비압축성 조건, 외력 매끄러움 등 실제 구성의 모든 조건을 생략해 자동으로 증명됐다고 하지 않는다.'), ('force', '힘까지 거칠어지면?', 29, '설계한 흐름이 극단적으로 변하면, 그것을 만드는 데 필요한 힘도 거칠어질 수 있습니다.\n바깥에서 무한히 큰 힘을 넣어 속도를 키운다면, 우리가 찾는 경우가 아닙니다.\n필요한 것은 외부의 힘은 시간과 공간에 걸쳐 매끄러운데, 내부의 속도는 폭주하는 흐름입니다.\n힘의 크기만 작으면 되는 것도 아닙니다. 여기저기 또는 순간순간 갑자기 튀는 변화까지 제어해야 합니다.', '두 경로：속도/외력 동반 거칠어짐 vs 속도 증가/매끄러운 외력 → 작은 급변과 매끄러움 비교', '매끄러움은 단순 작은 값이나 시각적 완만함과 동치가 아니다. 그림은 조건 비교다.'), ('research', '정지에서 시작해, 중심으로 모이다', 37, '이천이십육 년 구월 팔일, 오픈에이아이는 이런 유한시간 특이점 구성을 제시한 논문을 공개했습니다.\n논문은 처음에 정지한 유체에서 출발하고, 매끄러운 외력을 가합니다.\n설명된 중심 흐름은 안쪽으로 회전하며, 축 방향으로 흘러나갑니다.\n빠른 흐름의 중심 영역은 반지름과 높이가 모두 줄어듭니다. 반지름이 더 빨리 줄어 상대적으로 가늘어집니다.\n그 작은 영역의 속도는 커지지만, 전체 에너지는 유계로 유지되도록 구성했다고 제시합니다.', '정지 점 격자 → 외력 → 안쪽 회전/축 유출 → 반지름·높이 축소 → 최대속도/전체에너지', 'OpenAI 발표와 논문 Theorem 1.1/§2에 귀속. 물질관 길이 증가와 고속 영역 높이 감소를 혼동하지 않는다. 정확한 해의 시뮬레이션은 아니다.'), ('balance', '큰 효과가 만나, 작은 합을 남기다', 32, '움직임이 격해지면, 운동 법칙에 등장하는 여러 효과도 커질 수 있습니다.\n그런데 큰 효과들이 모두 같은 방향으로 작용하는 것은 아닙니다.\n반대 방향의 효과들이 정밀하게 맞물리면, 각각은 커도 합쳐진 결과는 작게 남을 수 있습니다.\n발표된 연구가 설명하는 핵심 중 하나는, 이 균형을 맞춰 외력은 매끄럽게 남기면서 내부 속도가 커지도록 구성하는 것입니다.', '서로 반대 방향의 벡터 → 큰 벡터 합산 → 작은 결과 화살표 → 균형 유지', '단일 성분의 signed 수치 비유. 실제 PDE 항 수치를 계산하지 않는다. 작은 합만으로 매끄러움을 증명하지 않는다.'), ('repair', '한순간의 균형으로는 부족하다', 32, '한순간에 효과들이 잘 맞는 것만으로는 충분하지 않습니다.\n이 균형은 시간이 지나고, 공간의 위치가 바뀌어도 유지되어야 합니다.\n흐름의 한 부분을 고치면 다른 부분도 달라져, 새로운 오차가 생길 수 있습니다.\n연구의 어려움은 원하는 흐름과 매끄러운 외력, 운동 법칙을 동시에 맞추는 데 있습니다. 화면은 이 어려움을 설명하는 개념도입니다.', '시간×공간 격자 → 여러 위치의 오차 표시 → 보정하면서 새 오차 등장 → 세 조건 동시 유지', '실제 보정 알고리즘/증명을 재현하지 않는다. 모든 차수의 매끄러운 연장은 단순 화면 평활화와 구별.'), ('meaning', '가능한 모양에서, 가능한 움직임으로', 33, '발표된 논문은 특별하게 구성한 매끄러운 외력 아래에서, 전체 에너지는 유계지만 속도는 발산하는 흐름을 제시합니다.\n외력이 없는 모든 유체가 폭주한다는 뜻은 아닙니다. 논문과 린 형식화의 공개도, 공식 평가와 수상 확정과는 구별해야 합니다.\n클레이 수학연구소는 구월 십일 성명에서 평가 절차를 안내했습니다.\n이번 두 막에서 가져갈 관점은 두 가지입니다. 전체의 크기와 가장 극단적인 부분은 다릅니다. 그리고 가능한 모양과, 실제 운동 법칙으로 이루어지는 움직임도 다릅니다.\n이제 이 두 가지 질문을 신경망의 표현과 증폭에도 가져가 보겠습니다.', '발표된 조건 네 카드 → 날짜/출처/평가 구분 → 두 핵심 관점 → 다음 신경망 막', '2026-10-08 확인. Clay가 특정 공식 심사 착수했다고 단정하지 않는다. 발표 결과를 귀속하고 무외력 일반 폭주로 확대하지 않는다. 유한 벡터의 L∞≤L² 조건은 다음 신경망 막에서도 유지해야 한다.')]

def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def main():
    manifest=[];master=['# 4막 — 실제 흐름과 매끄러운 외력'];tts=[];cues=[];offset=0
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
{DATA[i-2][1] if i>1 else '2막 마지막의 유한한 에너지와 국소 강도에 관한 질문'}
## TTS 원문과 확정 길이
{spoken}

- TTS: {'사용자 측정 '+str(duration)+'초' if voice else '미확정. 사용자 허용에 따라 화면 제작 우선.'}
- 화면: {duration}초. 원래 화면 기준은 {original}초.
## 화면 구성과 시간대별 애니메이션
{visual}
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
{title}, 에너지·속도·부피 지표, 수식, 출처·날짜, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
{DATA[i][1] if i<len(DATA) else '5막: 신경망의 표현과 방향별 증폭'}
## 수학 조건·과장 방지
{conditions}
모든 단순 모형과 개념도는 실제 NS 해나 신경망의 측정값이 아니다. 실제 해의 정확한 항 수치를 시뮬레이션하지 않는다. 외력이 있는 3막에서는 2막의 curl f=0 조건을 가정하지 않는다.
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
    (ROOT/'sources.md').write_text('# 출처와 확인 기준\n\n확인: 2026-10-08. 발표·논문·Clay 안내에 내용을 귀속하고 수상 확정으로 표현하지 않는다.\n\n'+SOURCES,encoding='utf-8')
    yaml='id: ns04\ntitle: "4막 — 실제 흐름의 구성"\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\ntiming_basis: '+('user_sentence_end_times' if voice else 'visual_storyboard_without_tts')+'\nscenes:\n'
    for row in manifest:yaml+='  - '+'\n    '.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in row.items())+'\n'
    (ROOT/'scenes.yaml').write_text(yaml,encoding='utf-8')

if __name__=='__main__':main()
