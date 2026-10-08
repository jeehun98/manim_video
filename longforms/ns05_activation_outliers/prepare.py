"""Act 3: toy energy scaling, attributed construction, careful NN transition."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
SOURCES='- Navier–Stokes의 연결: 기존 3·4막 spec.md와 https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf (Theorem 1.1, §2)\n- Dettmers et al., LLM.int8(), NeurIPS 2022: https://arxiv.org/abs/2208.07339 (특히 §3.2, §4)\n- Xiao et al., SmoothQuant, ICML 2023: https://proceedings.mlr.press/v202/xiao23c.html (특히 §3, Fig.2)\n'
DATA=[('fluid', '먼저, 물에서 무엇을 보았을까?', 30, '신경망으로 넘어가기 전에, 물에서 무엇을 보았는지 한 번 더 짚어보겠습니다.\n서로 다른 속도로 움직이는 흐름은 구조를 옮기고 변형합니다. 점성은 급격한 속도 차이를 주변으로 퍼뜨립니다.\n전체 운동에너지는 속도 제곱을 공간 전체에 걸쳐 더한 값입니다.\n그런데 가장 빠른 곳의 속도는, 이 합친 값과 다른 것을 측정합니다.\n전체를 합쳐 보는 눈과, 강한 부분을 찾아보는 눈이 모두 필요합니다.', '불균일한 속도장 → 변형/퍼짐 → 전체 게이지/최대 화살표 분기', '밀도 일정. 이류가 언제나 증폭한다고 하지 않는다. 에너지와 속도 최대값은 서로 다른 양이다. 유체 그림은 개념도.'), ('bridge', '작은 영역의 집중을, 다른 관점으로', 34, '빠른 영역의 속도가 커져도, 그 영역이 충분히 작아지면 에너지 기여는 그대로일 수 있습니다.\n줄어드는 것은 같은 물 덩어리의 부피가 아니라, 높은 속도가 나타나는 영역입니다.\n앞선 막에서는 이런 모양이 실제 흐름이 되려면 운동 법칙까지 만족해야 한다는 점도 보았습니다.\n신경망에서도 많은 값 가운데 일부에 큰 크기가 집중될 수 있습니다. 하지만 같은 유체 방정식을 따른다는 뜻은 아닙니다.\n유한한 개수의 숫자로 이루어진 이상치를, 연속 유체의 특이점과 동일시할 수도 없습니다.\n이제 가져갈 것은 전체 요약과 국소적인 극단값을 함께 보는 관점입니다.', 'U²V 일정인 영역 축소 → 운동 법칙 조건 → 연속 공간/유한 행렬 나란히 → 관점 연결', '유한 벡터에서 max|a|≤L2, n 고정 시 max≤n mean|a|. 유체의 L2 유계와 속도 발산을 유한 행렬에 문자 그대로 옮기지 않는다.'), ('matrix', '토큰과 특징 차원에 숫자를 놓다', 30, '신경망은 입력을 처리하면서 각 층에서 숫자들을 만들어냅니다.\n어떤 층의 표현을, 토큰마다 한 줄씩 나열해 보겠습니다.\n행은 토큰이고, 열은 특징 차원입니다.\n한 칸은 특정 토큰의 특정 차원에 있는 활성값입니다.\n이제 공간의 속도 화살표 대신, 이 숫자들의 분포를 살펴보겠습니다.', '속도장 → 토큰 행/특징 열 행렬 → 한 칸 확대 → 색으로 값 표현', 'X는 T×D 행렬, 배치 생략. 특징 차원 하나가 사람에게 해석 가능한 의미 하나와 반드시 대응한다고 하지 않는다. 숫자들은 설명용이다.'), ('outliers', '큰 값이, 특정 차원에 모인다면', 28, '대부분의 활성값이 작은 범위에 모여 있다고 생각해 보겠습니다.\n그런데 한 칸에서 주변보다 훨씬 큰 값이 나타납니다. 이런 값을 이상치, 아웃라이어라고 부릅니다.\n다른 토큰에서도 같은 특징 차원에 큰 값이 나타날 수 있습니다.\n실제로 일부 대규모 언어 모델에서 이런 체계적인 활성값 이상치가 보고되었습니다.\n모든 모델이 똑같은 패턴을 보이는 것은 아닙니다. 큰 값이 있다는 사실만으로 계산이 잘못된 것도 아닙니다.', '8×8 heatmap → 한 원소 밝아짐 → 같은 열의 여러 원소 밝아짐 → 논문 출처', 'LLM.int8 §4의 systematic outlier dimension 관찰에 귀속. 합성 행렬이고 실제 모델 측정값이 아니다. 밝기는 절댓값.'), ('statistics', '평균은 작은데, 최대값은 크다', 30, '전체 행렬을 하나의 숫자로 요약해 보겠습니다.\n예를 들어 예순네 개 중 예순세 개의 값이 영 점 오, 하나만 팔이라면 어떨까요?\n평균적인 절댓값은 약 영 점 육이지만, 최대값은 팔입니다.\n평균만 보면 그 큰 값이 어디에 있고, 어떤 계산에 영향을 주는지까지는 알 수 없습니다.\n유한한 행렬에서는 최대값이 엘투 노름 이하라는 상한도 있습니다. 이 장면은 무한대 폭주가 아니라, 평균과 극단값의 차이를 보여줍니다.', '63×.5/1×8 행렬 → 평균 .617 / 최대8 → 위치 찾기 → L2≈8.93와 상한', 'mean=.6171875, L2=sqrt79.75≈8.9303, RMS≈1.1163≤max8. RMS와 L2를 혼동하지 않는다. 최대≤L2, 평균≤최대이며 n이 고정되면 평균으로부터도 유한 상한은 있다.'), ('quantization', '숫자를, 정해진 눈금에 올리다', 28, '큰 활성값이 문제가 되는 한 가지 상황은, 계산 정밀도를 낮출 때입니다.\n팔 비트 정수로 표현하려면, 실수 값을 정해진 눈금에 맞춰야 합니다.\n서로 다른 값이 가까운 눈금으로 옮겨지는 과정이 양자화입니다.\n이때 같은 묶음의 값들이 하나의 눈금 간격을 공유한다고 생각해 보겠습니다.\n멀리 떨어진 큰 값 하나까지 포함하면, 작은 값들이 쓰던 눈금은 어떻게 달라질까요?', '실수축 .1 .2 .4 .8 → 촘촘한 격자 → 가까운 눈금 이동 → 큰 값100의 축소 개요', '같은 양자화 그룹의 대칭 absmax INT8 모형. s=M/127, q=clip(round(x/s),−127,127), 복원=sq. 눈금은 일부만 표시할 수 있다.'), ('precision', '큰 값 하나가, 다른 값의 차이를 지운다', 38, '최대 절댓값이 일일 때와, 백일 때를 비교하겠습니다.\n같은 정수 범위로 백까지 담으려면, 눈금 간격이 백 배 넓어집니다.\n영 점 일과 영 점 이는 모두 영으로 바뀝니다. 영 점 사와 영 점 팔도 같은 정수로 바뀝니다.\n큰 값 하나를 표현하는 과정에서, 원래 다른 작은 값들의 차이가 사라진 것입니다.\n이 현상은 같은 눈금을 공유할 때의 예시입니다. 양자화 묶음과 방법이 달라지면 영향도 달라집니다.', 'M1/100 비교 → 국소 눈금 .007874/.787402 → 정확한 반올림 복원 표 → q0/1 합침 강조', '값 .1,.2,.4,.8, M1: q13,25,51,102; M100: q0,0,1,1; 복원0,0,.787402,.787402. 단일 그룹 모형이며 모든 INT8 방식의 필연 현상으로 일반화하지 않는다.'), ('mixed', '중요한 큰 값은, 따로 계산하다', 30, '그렇다면 큰 값을 그냥 잘라내면 될까요?\n그 값이 중요한 계산에 쓰였다면, 없애는 순간 출력도 달라질 수 있습니다.\n엘엘엠 인트 에이트는 이상치가 나타나는 특징 차원의 계산을 분리하는 방법을 제시했습니다.\n일반 차원은 팔 비트로, 이상치 차원은 십육 비트로 계산하고 두 기여를 합칩니다.\n큰 값을 없애는 대신, 그 값에 맞는 정밀도를 따로 주는 것입니다.', '열 강조 → 제거시 출력 변화 개념 → 일반 INT8/이상치 FP16 분기 → 기여 합산', 'LLM.int8 mixed precision decomposition. X의 일부 열과 대응 W행의 기여 분리. 저정밀 계산이 모든 모델에서 정확한 출력을 보장한다고 하지 않는다.'), ('smooth', '크기를 옮겨도, 곱은 유지할 수 있다', 34, '또 다른 방법은, 큰 크기를 활성값 쪽에만 두지 않는 것입니다.\n한 차원의 활성값이 팔이고, 가중치가 영 점 이오라면 곱은 이입니다.\n활성값을 팔로 나누고 가중치를 팔 배 하면, 일과 이를 곱해 같은 결과를 얻습니다.\n스무스 퀀트는 이런 차원별 크기 보상으로, 활성값의 양자화 어려움을 가중치 쪽으로 옮기는 접근입니다.\n정확한 산술에서는 변환 전후의 결과가 같습니다. 이후 양자화에서 생기는 오차는 달라질 수 있습니다.', '활성8/가중.25 막대 → 활성1/가중2 보상 → 곱2 유지 → 양자화 전후 구별', 'SmoothQuant의 가역 양수 대각 스케일 개념. Y=XW=(XS⁻¹)(SW). 예시1차원S8. 가중치 쪽 부담도 고려해 스케일 선택해야 하며 S8은 실제 논문 calibration 값이 아니다.'), ('direction', '큰 값과, 큰 영향은 같은 말일까?', 30, '다시 처음의 질문으로 돌아가겠습니다. 전체적인 숫자가 평범해 보여도, 일부 큰 값은 표현 정밀도에 영향을 줄 수 있습니다.\n유체와 신경망을 연결하는 것은 같은 폭주가 아니라, 전체와 국소를 구별하는 관점입니다.\n그런데 어떤 값이 큰지뿐 아니라, 다음 계산에서 어떤 영향을 만드는지도 살펴봐야 합니다.\n같은 길이의 변화라도, 지나가는 방향에 따라 더 커지거나 작아질 수 있습니다.\n다음 막에서는 값의 크기에서, 방향에 따른 증폭으로 질문을 옮겨보겠습니다.', '활성 열 → W 통과 → 동일 길이 e1/e2 변환 후2/.5 → 6막', 'toy W=diag(2,.5). 두 입력길이1, 출력길이2/.5. 큰 activation이 큰 Jacobian 증폭을 보장하지 않는다. 다음 막의 연결만 제시.')]

def stamp(t):
    m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'

def main():
    manifest=[];master=['# 5막 — 전체와 국소에서 활성값 이상치로'];tts=[];cues=[];offset=0
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
{DATA[i-2][1] if i>1 else '4막 마지막의 전체 크기와 국소 집중에 관한 관점'}
## TTS 원문과 확정 길이
{spoken}

- TTS: {'사용자 측정 '+str(duration)+'초' if voice else '미확정. 사용자 허용에 따라 화면 제작 우선.'}
- 화면: {duration}초. 원래 화면 기준은 {original}초.
## 화면 구성과 시간대별 애니메이션
{visual}
문장 순서대로 timing.json의 ends에 맞춰 cue를 진행한다.
## 화면 텍스트
{title}, 영역·속도, 활성 행렬, 양자화 눈금과 복원값, 연구 출처, 문장 자막. 영문과 숫자 기호는 화면에 원 표기를 쓴다.
## 시작·종료 상태
첫 대상에서 마지막 대상으로 연속 변형한다. 상단 제목과 하단 자막 영역을 확보한다.
## 다음 장면 연결
{DATA[i][1] if i<len(DATA) else '6막: 방향에 따른 증폭'}
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
    (ROOT/'sources.md').write_text('# 출처와 확인 기준\n\n확인: 2026-10-08. 논문 관찰과 설명용 수치 모형을 구별한다. 양자화의 실제 반올림과 복원값을 사용한다.\n\n'+SOURCES,encoding='utf-8')
    yaml='id: ns05\ntitle: "5막 — 활성값 이상치와 표현 정밀도"\nvideo:\n  width: 1920\n  height: 1080\n  fps: 30\ntiming_basis: '+('user_sentence_end_times' if voice else 'visual_storyboard_without_tts')+'\nscenes:\n'
    for row in manifest:yaml+='  - '+'\n    '.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in row.items())+'\n'
    (ROOT/'scenes.yaml').write_text(yaml,encoding='utf-8')

if __name__=='__main__':main()
