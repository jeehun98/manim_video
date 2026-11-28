from pathlib import Path
import json,shutil
HERE=Path(__file__).resolve().parent
raw=[x.strip() for x in (HERE/'narration_source.txt').read_text(encoding='utf-8').splitlines() if x.strip()]
sentences=[];start=0
for text,end in zip(raw[::2],raw[1::2]):
 sentences.append(dict(start=start,end=int(end),text=text));start=int(end)
shots=[(0,23,'세 가지 공간과 세 가지 기하학','원판의 외형을 유지하며 새로운 거리의 질문을 제시한다.'),
 (23,46,'원판은 그대로, 내부는 움직인다','실제 원판 자기동형이 작은 원과 격자 전체를 바꾼다.'),
 (46,59,'어떤 변환을 이동으로 삼을까?','정칙 자기동형을 등거리 이동으로 삼으려면 길이 측정법을 바꾸어야 한다.'),
 (59,70,'복소미분이 알려 주는 길이의 변화','복소미분값의 절댓값은 국소적 길이 배율이다.'),
 (70,91,'이동 함수를 미분해 축소 비율을 구한다','Ta prime(0)=1-|a|²는 원점에서의 국소 축소 비율이다.'),
 (91,109,'작아진 만큼 더 크게 측정한다','국소적인 축소 비율의 역수를 곱하면 원점 대비 길이를 보정한다.'),
 (109,122,'모든 위치에서 이동을 보존하는 규칙','표준 정규화 ds=2|dz|/(1-|z|²)는 원판 자기동형에 불변이다.'),
 (122,136,'새로운 거리의 눈금','r=tanh(d/2)로 배치한 눈금은 같은 쌍곡 간격이다.'),
 (136,153,'같은 한 걸음, 작아지는 보폭','매번 쌍곡 거리 0.5씩 이동하면 화면상의 보폭이 감소한다.'),
 (153,172,'작아지는 틈과 커지는 보정','경계 틈을 반분할 때마다 실제 거리 증가량은 ln 2보다 크다.'),
 (172,183,'유한한 좌표, 무한한 거리','화면 이동량의 합은 유한하지만 쌍곡 거리의 합은 발산한다.'),
 (183,203,'유한한 원판 속의 무한한 공간','정확한 자기동형으로 옮긴 원들은 같은 쌍곡 반지름이다.'),
 (203,220,'같은 점들, 서로 다른 기하학','원판 자기동형은 새 거리를 보존하며 동일한 점 집합에도 다른 계량을 줄 수 있다.'),
 (220,243,'수의 연산에서 공간의 기하학으로','곱셈·미분·함수의 구조를 통해 새로운 거리까지 이어진다.')]
scenes=[dict(id=f'{i:02}',start=a,end=b,title=t,claim=c,**{'class':f'Shot{i:02}'}) for i,(a,b,t,c) in enumerate(shots,1)]
data=dict(title='복소평면에 숨겨진 기하학 — 구간 04',revision='v1_243s',duration=243,global_start_seconds=710,timing_source=f'사용자 제공 {len(sentences)}개 문장 종료 시각',sentences=sentences,scenes=scenes)
for name in ['script.json','timing.json']:(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
(HERE/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(sentences,1))+'\n',encoding='utf-8')
(HERE/'master_script.md').write_text('# 쌍곡 거리의 유도와 푸앵카레 원판\n\n'+ '\n\n'.join(f'{s["start"]}–{s["end"]}초 · {s["text"]}' for s in sentences),encoding='utf-8')
tts='\n\n'.join(' '.join(s['text'] for s in sentences if a<=s['start']<b) for a,b,_,_ in shots)+'\n'
(HERE/'tts_script.txt').write_text(tts.replace('4분의 1','사분의 일').replace('1','일').replace('0','영'),encoding='utf-8')
for s in scenes:
 d=HERE/'scenes'/s['id'];d.mkdir(parents=True,exist_ok=True)
 (d/'scene.py').write_text(f"import os,sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nos.environ['QCS_LAYOUT']='longform'\nfrom longforms.complex_geometry_04.direction import MetricScene\nclass {s['class']}(MetricScene):shot={int(s['id'])-1}\n",encoding='utf-8')
 ss=[x for x in sentences if x['start']<s['end'] and x['end']>s['start']]
 (d/'script.txt').write_text('\n'.join(x['text'] for x in ss),encoding='utf-8')
 (d/'spec.md').write_text(f'# {s["title"]}\n\n주장: {s["claim"]}\n\n사용자 확정 대본과 발화시간: {s["start"]}–{s["end"]}초 · {30*(s["end"]-s["start"])}프레임. 음원 미제공, 무음·전체 내레이션 자막. 화면 제작 전에 타이밍과 주장을 확정했다.\n\n1920×1080 30fps. 본문 y ≥ -2.6, 하단 자막 영역 분리.\n\n'+ '\n\n'.join(f'- {x["start"]}–{x["end"]}초: {x["text"]}' for x in ss)+'\n\n조건: |z|,|a|<1. 경계는 집합으로 보존되며 개별 점 고정은 아님. 유한 원은 정확한 원 변환, 선분 배율은 국소적인 미분으로 구분. ds의 상수 2는 곡률 -1 표준 정규화. 반분 구간의 실제 거리는 ln 2보다 크고 그 값에 수렴한다. 패턴은 동일 반지름 원의 배치로 엄밀한 타일링이 아니다. 마지막 4초에 수식을 없애며 243초를 연장하지 않는다.\n',encoding='utf-8')
(HERE/'scenes.yaml').write_text('title: 쌍곡 거리의 유도와 푸앵카레 원판\nwidth: 1920\nheight: 1080\nfps: 30\nduration: 243\nscenes:\n'+''.join(f'  - id: "{s["id"]}"\n    start: {s["start"]}\n    end: {s["end"]}\n    title: {s["title"]}\n' for s in scenes),encoding='utf-8')
build=(HERE.parent/'complex_geometry_03/build.py').read_text(encoding='utf-8').replace('complex_geometry_03','complex_geometry_04').replace('219','243').replace('46 exact user-supplied sentence ends; 12 scenes',f'{len(sentences)} exact user-supplied sentence ends; {len(scenes)} scenes')
build=build.replace("HERE/'script.json',","ROOT/'longforms/complex_geometry_03/direction.py',HERE/'script.json',")
(HERE/'build.py').write_text(build,encoding='utf-8')
pre=(HERE.parent/'complex_geometry_03/preflight.py').read_text().replace('complex_geometry_03','complex_geometry_04').replace('SurfaceScene','MetricScene').replace('first-1,12','first-1,14')
(HERE/'preflight.py').write_text(pre,encoding='utf-8')
shutil.copyfile(Path(r'C:\Users\as042\.codex\attachments\34e16f94-1b5e-483f-b9b9-f33d618ec615\붙여넣은 텍스트.txt'),HERE/'storyboard_source.md')
ids='e30459d7-1e2e-4761-be80-62f6b3ac174f af01f65c-7af6-4b56-acd3-1266c8c52d2a 8d479db2-df6b-4757-9147-7ce8b8ed1132 2ab1fa22-388b-43de-805c-bc7d2b3c879c 05b6aba2-6090-4ac2-b096-60a1bb40015d 1ffd2666-47ef-4691-b311-3d6eaaa183b4 c1372c8c-0ce3-487d-855a-85392e89d91a ccd25ac9-3b71-4cef-8e61-f235f63c1ecc f719b286-b481-46d5-95f4-60881fad1f80 4b263961-3abe-4e1f-9770-6fceb441332c 9ec246be-a064-4aef-bbb9-ee4e3dac0ced ac8b0e1c-4eed-4ac2-bcf1-4172dbf11bad f70135c4-a272-481a-bcec-9212df41cc37 eb306c53-48f8-42d8-86c5-a5856135d112 9d0a5371-2422-49f5-8b1e-7ade33222150 6ec11aca-14a6-4227-aabb-f5cf204e5092 eb6de4d9-3f33-4f19-9807-ab5cb99fd8e8 75881130-8ddd-4f33-ba17-db651f5a1d7b 21f180a3-c28e-44d2-8d26-ea3b87b4fd47 7450710b-4d05-4b2c-8b53-a4f11c9644f0 17161f7c-f2e7-46cf-a2d3-b4966fb4b064 bbc7423b-192e-44c2-b3f2-d10cedc98b3e 9cf02bec-9914-4011-ab56-7b571ab9f96c'.split()
(HERE/'references').mkdir(exist_ok=True)
for i,id in enumerate(ids,1):shutil.copyfile(Path(r'C:\Users\as042\AppData\Local\Temp')/f'codex-clipboard-{id}.png',HERE/'references'/f'{i:02}.png')
(HERE/'README.md').write_text(f'# 쌍곡 거리의 유도와 푸앵카레 원판\n\n사용자 확정 {len(sentences)}문장·243초, 14개 독립 씬. 1920×1080 30fps, 무음·전체 내레이션 자막. 원판을 자기 자신으로 보내는 실제 뫼비우스 변환과 표준 곡률 -1 계량을 사용한다.\n\n실행: `py -3.12 longforms/complex_geometry_04/build.py`\n\n선택 검수: `py -3.12 longforms/complex_geometry_04/build.py --preview --scene 02 05 10 12`\n\n결과: `exports/complex_geometry_04.mp4`. 앞 세 영상과 별도의 파일이며, 마지막 화면을 포함하여 정확히 243초. 문서의 추가 2–3초 제안은 적용하지 않았다. 화면에서 유한한 원과 국소 미분 배율을 구분하고, 반분 구간의 거리는 정확히 계산한다.\n',encoding='utf-8')
print(len(sentences),'sentences;',len(scenes),'scenes')
