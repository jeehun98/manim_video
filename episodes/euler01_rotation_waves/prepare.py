"""Approved narration and exact supplied speech boundaries."""
import json
import shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
LINES='''2|원을 따라 움직이는 점 하나를 생각해 보겠습니다.
5|이 점은 일정한 속도로 원을 돌고 있습니다.
10|그런데 점의 움직임 전체가 아니라, 높이만 관찰하면 어떻게 될까요?
13|점은 올라갔다가 내려오고, 다시 올라갑니다.
18|이 높이의 변화를 시간 순서대로 펼치면, 익숙한 물결 모양의 곡선이 나타납니다.
19|바로 사인파입니다.
22|이번에는 점의 가로 위치를 관찰해 보겠습니다.
26|역시 비슷한 물결이 나타나지만, 시작하는 위치가 조금 다릅니다.
28|이것이 코사인파입니다.
35|사인과 코사인은 서로 다른 움직임처럼 보이지만, 사실 원을 도는 점의 세로 위치와 가로 위치를 각각 나타낸 것입니다.
40|그렇다면 이 두 좌표를 따로 표현하지 않고, 하나로 나타낼 수는 없을까요?
42|여기서 복소수가 등장합니다.
46|우리가 익숙한 실수는 하나의 수직선 위에 나타낼 수 있습니다.
49|하지만 복소수는 여기에 새로운 축을 하나 더 추가합니다.
52|이때 사용하는 것이 허수 단위 i입니다.
55|i는 제곱하면 마이너스 1이 되는 수로 정의됩니다.
62|실수 부분을 가로축에, 허수 부분을 세로축에 놓으면 복소수 하나로 평면 위의 점을 표현할 수 있습니다.
64|이 평면을 복소평면이라고 합니다.
66|이제 다시 원을 도는 점으로 돌아가 보겠습니다.
73|반지름이 1인 원에서, 각도 세타만큼 회전한 점의 가로 좌표는 코사인 세타, 세로 좌표는 사인 세타입니다.
78|따라서 이 점은 코사인 세타 더하기 i 사인 세타로 표현할 수 있습니다.
81|그런데 이 회전을 나타내는 또 다른 방법이 있습니다.
83|바로 지수함수입니다.
88|보통 e의 x제곱은 값이 연속적으로 증가하거나 감소하는 함수로 알고 있습니다.
93|하지만 지수에 허수 단위 i를 곱한 각도를 넣으면, 전혀 다른 모습이 나타납니다.
98|크기가 커지거나 작아지는 대신, 크기 1을 유지하면서 방향이 변하는 것입니다.
104|즉, e의 i세타 제곱은 복소평면에서 각도 세타만큼 회전한 점을 나타냅니다.
108|그리고 이 점은 앞에서 코사인과 사인으로 표현했던 바로 그 점입니다.
110|따라서 두 표현은 서로 같습니다.
112|이것이 오일러 공식입니다.
116|왼쪽에는 지수함수가 있고, 오른쪽에는 삼각함수가 있습니다.
119|하지만 둘 다 복소평면에서 같은 회전을 나타냅니다.
126|그리고 이 회전하는 점의 가로 위치와 세로 위치를 각각 관찰하면 코사인파와 사인파가 나타납니다.
133|결국 우리가 서로 다른 현상이라고 생각했던 회전과 진동은 하나의 움직임을 다른 방식으로 바라본 결과였습니다.
134|원을 도는 점 하나.
139|그 안에서 지수함수와 삼각함수, 회전과 진동이 하나로 연결됩니다.'''
def main():
    segments=[];start=0
    for line in LINES.splitlines():
        end,s=line.split('|',1);end=int(end)
        segments.append(dict(id=len(segments)+1,start=start,end=end,text=s));start=end
    bounds=[0,10,19,28,40,49,64,73,81,93,104,116,139]
    titles=['원을 도는 점 하나','높이를 기록하면 사인파','가로 위치를 기록하면 코사인파','두 파형의 출발점은 하나','수직선에서 평면으로','허수 단위 i와 복소평면','원의 두 좌표','두 좌표를 하나의 복소수로','또 하나의 표현, 지수함수','크기 1, 변하는 방향','같은 점을 가리키는 두 표현','회전과 진동을 잇는 오일러 공식']
    scenes=[dict(id=i+1,start=a,end=b,title=titles[i],cls=f'Shot{i+1:02}') for i,(a,b) in enumerate(zip(bounds,bounds[1:]))]
    data=dict(duration=139,fps=60,audio=None,timing_source='user supplied sentence ends',segments=segments,scenes=scenes)
    (HERE/'timing.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (HERE/'narration.md').write_text('# 원을 도는 점에서 어떻게 파도가 나올까?\n\n사용자 확정 대본·문장 종료 시각 기준 139초. 음원 미제공.\n\n'+'\n\n'.join(f'[{s["start"]:03}–{s["end"]:03}s] {s["text"]}' for s in segments)+'\n',encoding='utf-8')
    paragraphs=['\n'.join(s['text'].replace('i','아이').replace('e','이') for s in segments if shot['start']<=s['start']<shot['end']) for shot in scenes]
    (HERE/'tts_script.txt').write_text('\n\n'.join(paragraphs)+'\n',encoding='utf-8')
    def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
    (HERE/'captions.srt').write_text('\n\n'.join(f'{s["id"]}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for s in segments)+'\n',encoding='utf-8')
    shutil.copyfile(Path('C:/Users/as042/.codex/attachments/195de838-7dde-42ad-b551-445b217b8ae0/붙여넣은 텍스트.txt'),HERE/'storyboard_original.md')
if __name__=='__main__':main()
