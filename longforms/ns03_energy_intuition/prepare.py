"""Act 3: toy energy scaling, attributed construction, careful NN transition."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
SOURCES='''- https://openai.com/index/navier-stokes-solution/ (2026-09-08 発表)
- https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf (Theorem 1.1, §2, Figure 1)
- https://www.claymath.org/news/navier-stokes-announcement/ (2026-09-11)
'''.replace('発表','발표')
DATA=[('total', '전체를 한 숫자로 담으면', 28, '전체 에너지가 유한하면, 물속 어디에서도 속도가 제한되어 있을까요?\n물속에는 서로 다른 길이의 속도 화살표가 펼쳐져 있습니다.\n운동에너지는 이 움직임들을 공간 전체에 걸쳐 합쳐 본 값입니다. 빠른 움직임일수록 더 크게 기여합니다.\n하지만 하나로 합친 숫자가, 가장 빠른 곳까지 알려주는 것은 아닙니다.', '속도장 → 각 영역의 기여를 에너지 게이지로 모음 → 전체와 최대의 질문', 'E는 속도 제곱의 공간 적분에 비례한다. 화면 화살표는 연속 속도장의 표본이다.'), ('volume', '더 빨라져도, 영역이 줄어든다면', 28, '빠르게 움직이는 영역 하나를 보겠습니다.\n같은 크기의 영역에서 속도가 두 배가 되면, 에너지 기여는 네 배가 됩니다.\n그런데 빠른 영역의 부피가 동시에 사분의 일로 줄어든다면 어떨까요?\n더 큰 속도와 더 작은 영역이 서로 맞물려, 에너지 기여는 처음과 같아집니다.', '정육면체 부피와 속도 화살표 → 속도 두 배 → 부피 사분의 일 → 일정한 에너지', '변 길이를 부피의 세제곱근으로 줄인다. 지역의 에너지 기여에 대한 단순 모형이다.'), ('concentration', '더 작은 곳에, 더 강한 움직임', 30, '이제 같은 변화를 반복해 보겠습니다. 속도는 네 배, 여덟 배, 그 이상으로 커집니다.\n빠른 흐름이 나타나는 영역은 그보다 충분히 빠르게 작아집니다.\n여기서 줄어드는 것은 같은 물 덩어리의 부피가 아닙니다. 높은 속도가 나타나는 영역의 크기입니다.\n따라서 전체 에너지의 유한성만으로, 작은 영역에서 속도가 커지는 가능성을 막을 수는 없습니다.', 'U 증가에 맞춰 V=U⁻²인 공간 영역 축소 → 동일한 에너지 게이지 → 물질과 영역 구별', '물질 조각의 압축이 아니다. 비압축성 NS 해를 구성한 장면도 아니다. 그림은 에너지 집중의 단순 모형.'), ('two_views', '모두 합하기와, 가장 큰 것 찾기', 28, '같은 흐름을 두 가지 방식으로 바라보겠습니다.\n왼쪽에서는 공간 전체의 움직임을 더합니다. 오른쪽에서는 가장 빠른 부분을 찾습니다.\n전체를 보는 눈과, 극단적인 부분을 보는 눈은 서로 다른 정보를 줍니다.\n어떤 유한한 시간에 가까워질수록 최대 속도가 한계 없이 커진다면, 속도의 유한시간 폭주라고 부를 수 있습니다.', '같은 장면을 좌우 복제 → 합산 게이지/최대 화살표 → 시간 T에 가까워지는 눈금', '연속 공간에서 L² 유계는 L∞ 유계를 함의하지 않는다. 속도 발산형 폭주를 설명하며 모든 특이점과 동치라고 하지 않는다.'), ('question', '실제 유체도 이렇게 움직일까?', 26, '하지만 지금까지의 그림은 가능성을 설명하는 모형입니다.\n빠른 영역이 좁아지는 모습을 그리는 것과, 실제 유체가 그렇게 움직이는 것은 다른 문제입니다.\n실제 흐름은 주변으로 이동하고, 압력에 밀리고, 점성으로 퍼지는 과정을 함께 따라야 합니다.\n그렇다면 이 조건들을 지키면서도 속도가 폭주하는 흐름을 만들 수 있을까요? 다음 막에서는 이 질문을 보겠습니다.', '집중 개념도 → 이동/압력/퍼짐/외력의 네 조건 → 4막 질문', '수식의 항별 분석은 하지 않는다. 실제 해의 조건이 따로 필요함을 분명히 한다.')]

def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def main():
    manifest=[];master=['# 3막 — 전체 에너지와 작은 영역의 집중'];tts=[];cues=[];offset=0
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
{DATA[i][1] if i<len(DATA) else '4막: 실제 흐름을 구성하는 조건'}
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
    yaml='id: ns03a\ntitle: "3막 — 에너지 집중의 직관"\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\ntiming_basis: '+('user_sentence_end_times' if voice else 'visual_storyboard_without_tts')+'\nscenes:\n'
    for row in manifest:yaml+='  - '+'\n    '.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in row.items())+'\n'
    (ROOT/'scenes.yaml').write_text(yaml,encoding='utf-8')

if __name__=='__main__':main()
