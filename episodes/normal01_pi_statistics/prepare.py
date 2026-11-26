"""Preserve approved sentence timings; generate deterministic mathematical data."""
from pathlib import Path
import json
import mpmath as mp
HERE=Path(__file__).resolve().parent
SCRIPT='''2|명확한 수학적 관계로부터 정의되는 원주율.
7|하지만 이를 소수로 표현하면, 마치 무작위로 생성된 숫자들의 배열처럼 보입니다.
13|수학에서는 일반적으로 수를 유리수와 무리수, 또는 대수적 수와 초월수 등으로 분류합니다.
19|하지만 이러한 분류만으로는 그 수를 구성하는 숫자들이 어떠한 분포를 갖는지 설명할 수 없습니다.
25|예를 들어 숫자 1 사이에 존재하는 0의 개수를 하나씩 증가시키며 만들어낸 수를 생각해 보겠습니다.
28|이 수는 순환하지 않는 무한소수이므로 무리수입니다.
35|하지만 0과 1을 제외한 숫자는 등장하지 않으며, 자릿수를 늘려갈수록 0의 출현 비율은 1에 가까워집니다.
40|즉, 무리수라는 성질이 숫자들의 균일한 분포를 보장하지는 않습니다.
45|이에 수학에서는 수를 대수적 성질뿐만 아니라 통계적 성질을 통해서도 이해하고자 합니다.
49|이러한 관점에서 사용되는 개념 중 하나가 바로 정규수입니다.
55|어떤 수가 10진법에서 정규수라면, 0부터 9까지의 숫자는 각각 10분의 1의 비율로 등장합니다.
63|뿐만 아니라 35와 같은 두 자리의 숫자 배열은 100분의 1의 비율로, 세 자리의 숫자 배열은 각각 1000분의 1의 비율로 등장합니다.
69|이를 일반화하면, 길이가 k인 임의의 숫자 배열의 출현 비율은 10의 k제곱분의 1에 수렴해야 합니다.
73|이러한 성질은 또 다른 형태의 수학적 문제로 표현할 수 있습니다.
77|어떤 수에 10을 곱하고 정수 부분을 제거하는 과정을 반복해 보겠습니다.
83|이 과정에서 소수점의 위치가 한 자리씩 이동하며, 0 이상 1 미만의 새로운 수가 만들어집니다.
92|이때 35라는 숫자 배열이 소수점 바로 뒤에 등장한다는 것은, 해당 값이 0.35 이상 0.36 미만의 구간에 존재한다는 것을 의미합니다.
95|그리고 이 구간의 길이는 정확히 100분의 1입니다.
102|따라서 숫자 배열의 출현 빈도에 관한 문제는, 수열이 0과 1 사이에서 균등하게 분포하는지를 묻는 문제로 바뀌게 됩니다.
104|그렇다면 원주율은 정규수일까요?
110|지금까지 계산된 방대한 원주율의 자릿수에서는 균일한 분포에 가까운 통계적 성질이 관찰되고 있습니다.
117|하지만 심지어 0부터 9까지의 개별 숫자가 각각 10분의 1의 비율로 등장하는지조차 아직 증명되지 않았습니다.
126|더욱 흥미로운 것은 1909년, 수학자 에밀 보렐에 의해 측도론적 의미에서 거의 모든 실수가 정규수라는 사실이 증명되었다는 점입니다.
133|그럼에도 원주율이나 자연상수, 루트 2와 같이 우리에게 익숙한 수들의 정규성은 아직 밝혀지지 않았습니다.
138|명확한 수학적 관계로부터 정의된 수와 그 수에서 나타나는 통계적 성질.
145|이 둘 사이의 관계를 이해하려는 연구는 정수론, 확률론, 동역학계 등 다양한 수학적 분야로 이어지고 있습니다.
152|수를 어떠한 관계로 표현할 수 있는지를 넘어, 그 표현 속에서 어떠한 성질이 나타나는지를 이해하고자 하는 것입니다.'''
ENDS=[7,13,19,25,28,35,40,45,49,55,63,69,73,77,83,92,95,102,104,110,117,126,133,138,145,152]
TITLES=['원주율의 두 가지 모습','서로 다른 수의 분류','관계와 분포는 다른 질문','규칙으로 만드는 무한소수','순환하지 않는 소수','숫자의 비율은 불균등하다','무리수여도 정규수는 아니다','수를 바라보는 두 관점','10진법 정규수','한 자리 숫자의 빈도','두 자리, 세 자리의 배열','모든 길이의 숫자 배열','숫자열을 공간의 점으로','10을 곱하고 정수 부분 제거','하나의 수에서 생기는 수열','숫자 배열 35와 구간','구간의 길이는 1/100','정규성과 균등분포','원주율은 정규수일까?','실제 π의 자릿수 통계','관찰과 증명은 다르다','보렐: 거의 모든 실수','전체의 정리와 특정한 수','정의된 수와 나타나는 성질','정수론·확률론·동역학계','수를 표현하고, 이해한다는 것']
def stamp(v):return f'{v//3600:02}:{v//60%60:02}:{v%60:02},000'
def main():
    rows=[];start=0
    for item in SCRIPT.splitlines():
        end,s=item.split('|',1);end=int(end)
        rows.append(dict(start=start,end=end,text=s));start=end
    scenes=[];start=0
    for i,(end,title) in enumerate(zip(ENDS,TITLES),1):
        scenes.append(dict(id=f'{i:02}',**{'class':f'Shot{i:02}'},start=start,end=end,title=title));start=end
    data=dict(duration=152,fps=30,audio='silent; TTS not provided',sentences=rows,scenes=scenes)
    (HERE/'timing.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (HERE/'narration.md').write_text('# 원주율의 정규성 — 수를 이해하는 통계적 관점\n\n確定'.replace('確定','사용자 확정 대본 · 152초 · TTS 미제공\n\n')+'\n\n'.join(f"{r['start']}–{r['end']}초\n\n{r['text']}" for r in rows)+'\n',encoding='utf-8')
    blocks=[]
    for shot in scenes:
        blocks.append(' '.join(r['text'] for r in rows if shot['start']<=r['start']<shot['end']))
    (HERE/'tts_script.txt').write_text('\n\n'.join(blocks)+'\n',encoding='utf-8')
    (HERE/'captions.srt').write_text('\n\n'.join(f"{i}\n{stamp(r['start'])} --> {stamp(r['end'])}\n{r['text']}" for i,r in enumerate(rows,1))+'\n',encoding='utf-8')
    mp.mp.dps=10100
    digits=str(mp.pi).split('.')[1][:10000]
    samples={}
    for n in [100,1000,10000]:
        s=digits[:n];counts=[s.count(str(d)) for d in range(10)]
        samples[str(n)]=dict(counts=counts,frequencies=[c/n for c in counts],count35=sum(s[i:i+2]=='35' for i in range(n-1)),positions=n-1)
    # Independent precision check: no random numbers stand in for pi.
    mp.mp.dps=10200
    assert str(mp.pi).split('.')[1][:10000]==digits
    for m in [1,2,5,10,30,100]:
        s=''.join('1'+'0'*k for k in range(1,m+1))
        assert len(s)==m*(m+3)//2 and s.count('0')==m*(m+1)//2
    from fractions import Fraction
    seed='14358261'*8
    orbit=[float(Fraction(int(seed[n:]),10**len(seed[n:]))) for n in range(10)]
    assert .35<=orbit[2]<.36
    output=dict(pi_digits=digits,samples=samples,orbit=orbit,seed=seed,
                counterexample=''.join('1'+'0'*k for k in range(1,101)),
                checks=dict(pi_precision_agreement=True,block_count_formula=True,orbit_interval=True),
                sources=['https://www.davidhbailey.com/dhbpapers/normality-digits-pi.pdf','https://www.claymath.org/library/annual_report/ar2006/06report_normalnumbers.pdf'])
    (HERE/'model_data.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
