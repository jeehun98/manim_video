"""Materialize exact supplied narration and independent shot specifications."""
from pathlib import Path
import json,shutil
HERE=Path(__file__).resolve().parent
raw=[x.strip() for x in (HERE/'narration_source.txt').read_text(encoding='utf-8').splitlines() if x.strip()]
sentences=[];start=0
for text,end in zip(raw[::2],raw[1::2]):
 sentences.append(dict(start=start,end=int(end),text=text));start=int(end)
shots=[(0,11,'평면에서 공간으로','제곱근의 연속적 변화를 두 복소평면에서 관찰한다.'),
 (11,23,'입력의 회전과 제곱근','연속적으로 선택한 제곱근의 회전각은 입력의 절반이다.'),
 (23,44,'한 바퀴로는 돌아오지 않는다','입력은 한 바퀴, 제곱근은 두 바퀴의 입력 후 돌아온다.'),
 (44,61,'두 겹을 교차하여 연결한다','음의 실수축의 두 가장자리를 반대 겹과 교차 연결한다.'),
 (61,77,'위치에 담긴 제곱근의 정보','같은 z 위의 두 위치는 다른 제곱근을 나타낸다.'),
 (77,104,'원점에서는 w를 좌표로','S={(z,w):z=w²}는 w 좌표에서 매끄럽고 F(w)=w는 정칙이다.'),
 (104,129,'작은 복소평면으로 이루어진 공간','겹치는 국소 좌표의 전이가 정칙인 복소 1차원 다양체이다.'),
 (129,153,'직사각형에서 원환면으로','반대 변의 연결과 평면의 반복 타일은 같은 연결 규칙을 설명한다.'),
 (153,178,'원환면을 펼친 보편피복','평면의 두 독립 이동이 원환면을 감아 돈 횟수를 기록한다.'),
 (178,194,'모양을 넘어 공간을 비교한다','단위원판과 위쪽 반평면은 가역 정칙변환으로 대응한다.'),
 (194,209,'실제 복소변환으로 펼치는 원판','Cayley 변환과 그 역은 정칙이고 각도를 보존한다.'),
 (209,219,'균일화 정리','연결 리만 곡면의 보편피복은 구면·평면·원판 중 하나이다.')]
scenes=[dict(id=f'{i:02}',start=a,end=b,title=t,claim=c,**{'class':f'Shot{i:02}'}) for i,(a,b,t,c) in enumerate(shots,1)]
data=dict(title='복소평면에 숨겨진 기하학 — 구간 03',revision='v1_219s',duration=219,global_start_seconds=491,timing_source=f'사용자 제공 {len(sentences)}개 문장 종료 시각',sentences=sentences,scenes=scenes)
for name in ['script.json','timing.json']:(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
(HERE/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(sentences,1))+'\n',encoding='utf-8')
(HERE/'master_script.md').write_text('# 리만 곡면에서 균일화 정리까지\n\n'+ '\n\n'.join(f'{s["start"]}–{s["end"]}초 · {s["text"]}' for s in sentences),encoding='utf-8')
(HERE/'tts_script.txt').write_text(('\n\n'.join(' '.join(s['text'] for s in sentences if a<=s['start']<b) for a,b,_,_ in shots)+'\n').replace('90도','구십 도').replace('45도','사십오 도').replace('1','일'),encoding='utf-8')
for s in scenes:
 d=HERE/'scenes'/s['id'];d.mkdir(parents=True,exist_ok=True)
 (d/'scene.py').write_text(f"import os,sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nos.environ['QCS_LAYOUT']='longform'\nfrom longforms.complex_geometry_03.direction import SurfaceScene\nclass {s['class']}(SurfaceScene):shot={int(s['id'])-1}\n",encoding='utf-8')
 ss=[x for x in sentences if x['start']<s['end'] and x['end']>s['start']]
 (d/'script.txt').write_text('\n'.join(x['text'] for x in ss),encoding='utf-8')
 (d/'spec.md').write_text(f'# {s["title"]}\n\n주장: {s["claim"]}\n\n사용자 확정 대본·문장 종료 시각. {s["start"]}–{s["end"]}초, {s["end"]-s["start"]}초, {30*(s["end"]-s["start"])}프레임. TTS 미제공, 무음.\n\n16:9 1920×1080 30fps. 본문 y ≥ -2.6, 전체 내레이션 자막 별도 하단 영역. 화면 경계와 자막 영역 매 프레임 검사.\n\n'+ '\n\n'.join(f'- {x["start"]}–{x["end"]}초: {x["text"]}' for x in ss)+'\n\n수학 조건: 연결 리만 곡면, 가역 정칙 동치. 두 겹은 절단선 교차 연결 개념도이며 원점의 실제 좌표는 w. 원환면 3D 임베딩은 위상 설명이며 유클리드 등거리·등각 임베딩 주장이 아님. 원판 변환은 실제 Cayley 변환의 유한 뷰포트.\n',encoding='utf-8')
(HERE/'scenes.yaml').write_text('title: 리만 곡면에서 균일화 정리까지\nwidth: 1920\nheight: 1080\nfps: 30\nduration: 219\nscenes:\n'+''.join(f'  - id: "{s["id"]}"\n    start: {s["start"]}\n    end: {s["end"]}\n    title: {s["title"]}\n' for s in scenes),encoding='utf-8')
build=(HERE.parent/'complex_geometry_02/build.py').read_text(encoding='utf-8').replace('complex_geometry_02','complex_geometry_03').replace('288','219').replace('57 exact user-supplied sentence ends; 16 scenes',f'{len(sentences)} exact user-supplied sentence ends; {len(scenes)} scenes')
(HERE/'build.py').write_text(build,encoding='utf-8')
src=Path(r'C:\Users\as042\.codex\attachments\8425dd16-20bf-4b1f-b1a5-01989138a6c3\붙여넣은 텍스트.txt')
shutil.copyfile(src,HERE/'storyboard_source.md')
ids='86b9ffa8-8013-4efb-a438-46fe8269ab32 ae0aae2d-4c5b-4d74-9f18-971d3d279ee9 71f25984-7cc6-410e-a226-d1d1266ab06e 2f016072-fd49-4500-9a8d-b02ed44a670b 914797e7-ba76-4e1f-889d-c67620202049 a1e0e610-794c-4703-9fd6-6e706062ef4b 0c94f9c1-a3d9-4af0-98cc-9209c10ad9bd ae6bb720-5df7-4048-b59b-142702bf46b5 15378b03-9c52-4790-889b-457b66d2ce7b 6c929db5-518e-4726-9975-1738dbd436e3 ba266fd3-2a97-43c3-a174-500eaf649a92 14a9d12e-55d1-4ec8-ad13-04cf14365345 00c9028c-c7f8-4057-ac01-86725e4bad41 e934465f-da78-4848-b7e9-b3a36526add3 768c475f-32c6-4dad-a513-4e52a765f05b b1f108fc-7a25-485c-84e7-05fb933fd50f 90543aa9-a6ff-4905-b5a5-ca335a328781 7a3b534d-5954-4390-97ac-ba83f7dba441'.split()
(HERE/'references').mkdir(exist_ok=True)
for i,id in enumerate(ids,1):shutil.copyfile(Path(r'C:\Users\as042\AppData\Local\Temp')/f'codex-clipboard-{id}.png',HERE/'references'/f'{i:02}.png')
(HERE/'README.md').write_text('# 리만 곡면에서 균일화 정리까지\n\n사용자 확정 46문장·219초, 12개 독립 씬. 16:9 1920×1080 30fps, 무음·전체 내레이션 자막. 앞 두 구간과 별도의 영상.\n\n실행: `py -3.12 longforms/complex_geometry_03/build.py`\n\n선택 미리보기: `py -3.12 longforms/complex_geometry_03/build.py --preview --scene 04 06 11`\n\n결과: `exports/complex_geometry_03.mp4`. 소스 해시가 일치하는 씬만 재사용하며 최종 프레임 수·자막 시작·경계·전체 디코딩을 검사한다. 참고 콘티는 사용자 요청과 구분해 storyboard_source.md에 보존했다.\n',encoding='utf-8')
print(len(sentences),'sentences;',len(scenes),'scenes')
