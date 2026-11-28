"""Create the intro specifications from the supplied final narration, before animation."""
from pathlib import Path
import json,shutil
HERE=Path(__file__).resolve().parent
raw=[x.strip() for x in (HERE/'narration_source.txt').read_text(encoding='utf-8').splitlines() if x.strip()]
sentences=[];start=0
for text,end in zip(raw[::2],raw[1::2]):
 sentences.append(dict(start=start,end=int(end),text=text));start=int(end)
shots=[(0,13,'복소평면에 숨겨진 기하학','평평한 원판의 반복 패턴을 실제 쌍곡 이동으로 관찰한다.'),
 (13,22,'복소수의 곱셈과 복소미분','수의 곱셈과 각 점 주변의 국소적인 변화를 연결한다.'),
 (22,30,'경계와 내부를 연결하는 규칙','정칙함수의 코시 적분 공식이 경계와 내부를 연결함을 예고한다.'),
 (30,39,'물리적 문제를 다른 공간으로','실제 등각 함수로 온도장과 격자를 함께 옮긴다.'),
 (39,48,'함수를 표현하기 위해 공간을 바꾼다','두 겹의 연결과 w 국소좌표는 서로 다른 시각화로 구분한다.'),
 (48,54,'다양한 공간의 세 가지 기본 구조','분류 대상은 리만 곡면 자체가 아니라 그 보편피복이다.'),
 (54,66,'복소미분에서 새로운 거리로','국소 축소 비율과 길이 측정법, 같은 쌍곡 반지름의 패턴을 연결한다.'),
 (66,69,'이야기의 출발점으로','복잡한 패턴에서 본편 첫 화면의 실수축으로 돌아온다.')]
scenes=[dict(id=f'{i:02}',start=a,end=b,title=t,claim=c,**{'class':f'Shot{i:02}'}) for i,(a,b,t,c) in enumerate(shots,1)]
data=dict(title='복소평면에 숨겨진 기하학 — 인트로',revision='v1_69s',duration=69,global_start_seconds=0,timing_source='사용자 제공 11개 문장 종료 시각',sentences=sentences,scenes=scenes)
for name in ['script.json','timing.json']:(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
(HERE/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(sentences,1))+'\n',encoding='utf-8')
(HERE/'master_script.md').write_text('# 인트로 — 수의 확장에서 공간의 발견까지\n\n'+ '\n\n'.join(f'{s["start"]}–{s["end"]}초 · {s["text"]}' for s in sentences),encoding='utf-8')
paragraphs=[' '.join(s['text'] for s in sentences if a<=s['start']<b) for a,b,_,_ in shots]
(HERE/'tts_script.txt').write_text('\n\n'.join(x for x in paragraphs if x)+'\n',encoding='utf-8')
for s in scenes:
 d=HERE/'scenes'/s['id'];d.mkdir(parents=True,exist_ok=True)
 (d/'scene.py').write_text(f"import os,sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nos.environ['QCS_LAYOUT']='longform'\nfrom longforms.complex_geometry_00.direction import IntroScene\nclass {s['class']}(IntroScene):shot={int(s['id'])-1}\n",encoding='utf-8')
 ss=[x for x in sentences if x['start']<s['end'] and x['end']>s['start']]
 (d/'script.txt').write_text('\n'.join(x['text'] for x in ss),encoding='utf-8')
 (d/'spec.md').write_text(f'# {s["title"]}\n\n주장: {s["claim"]}\n\n사용자 확정 대본·문장 종료 시각: {s["start"]}–{s["end"]}초 · {30*(s["end"]-s["start"])}프레임. 음원 미제공, 무음·전체 자막.\n\n16:9 1920×1080 30fps. 본문 y ≥ -2.6, 자막은 별도 하단 영역. 본편 01–04의 수학적 객체와 실제 계산 함수를 재사용한다.\n\n'+'\n\n'.join(f'- {x["start"]}–{x["end"]}초: {x["text"]}' for x in ss)+'\n\n조건: 정칙성·분기점 좌표·보편피복과 원래 곡면을 구분한다. 같은 쌍곡 반지름의 원은 엄밀한 타일링으로 표시하지 않는다. 기존 통합본은 수정하지 않으며 인트로 별도 파일을 생성한다.\n',encoding='utf-8')
(HERE/'scenes.yaml').write_text('title: 인트로 — 수의 확장에서 공간의 발견까지\nwidth: 1920\nheight: 1080\nfps: 30\nduration: 69\nscenes:\n'+''.join(f'  - id: "{s["id"]}"\n    start: {s["start"]}\n    end: {s["end"]}\n    title: {s["title"]}\n' for s in scenes),encoding='utf-8')
build=(HERE.parent/'complex_geometry_04/build.py').read_text(encoding='utf-8').replace('complex_geometry_04','complex_geometry_00').replace('243','69').replace('49 exact user-supplied sentence ends; 14 scenes','11 exact user-supplied sentence ends; 8 scenes')
build=build.replace("ROOT/'longforms/complex_geometry_03/direction.py',", "ROOT/'longforms/complex_geometry_02/direction.py',ROOT/'longforms/complex_geometry_03/direction.py',ROOT/'longforms/complex_geometry_04/direction.py',")
(HERE/'build.py').write_text(build,encoding='utf-8')
pre=(HERE.parent/'complex_geometry_04/preflight.py').read_text().replace('complex_geometry_04','complex_geometry_00').replace('MetricScene','IntroScene').replace('first-1,14','first-1,8')
(HERE/'preflight.py').write_text(pre,encoding='utf-8')
shutil.copyfile(Path(r'C:\Users\as042\.codex\attachments\df7f1acf-3763-4a71-9f67-52ffa8e2097b\붙여넣은 텍스트.txt'),HERE/'storyboard_source.md')
ids='b093eebe-c0cd-4f73-b03a-13f86e28d6ee f19d0af0-7932-4b14-b591-930ccbd6ebbd 9ac65f37-a606-4df5-8094-4a772c86d955 f2e9fe9e-a8a2-430f-a3ea-17e627a19c28 b3bc4a49-ab50-41b3-8f9c-7b699c6a5d05 24fd4ff9-1519-4ecc-9266-c563a3d8ef5a 207e037e-3f85-41b3-8152-f0e373502d81 8bbbd466-efa2-41cb-9fc1-76597991cc43 c6fb6419-7bb3-46c6-98f1-ba1cd8107876 c298df9d-a6f8-4a3f-bc93-432cf56078b6'.split()
(HERE/'references').mkdir(exist_ok=True)
for i,id in enumerate(ids,1):shutil.copyfile(Path(r'C:\Users\as042\AppData\Local\Temp')/f'codex-clipboard-{id}.png',HERE/'references'/f'{i:02}.png')
(HERE/'README.md').write_text('# 인트로 — 수의 확장에서 공간의 발견까지\n\n사용자 확정 11문장·69초, 8개 독립 씬. 1920×1080 30fps, 무음·전체 자막. 본편 01–04에서 검증한 계산 함수와 도형을 재사용하며 69초의 실수축 화면으로 끝난다.\n\n실행: `py -3.12 longforms/complex_geometry_00/build.py`\n\n대표 씬 검수: `py -3.12 longforms/complex_geometry_00/build.py --preview --scene 01 04 05 07`\n\n결과: `exports/complex_geometry_00.mp4`. 기존 음성 포함 통합본은 변경하지 않는다. 인트로 음원·배경 음악은 제공되지 않아 무음이다.\n',encoding='utf-8')
print('11 sentences; 8 shots; 69 seconds')
