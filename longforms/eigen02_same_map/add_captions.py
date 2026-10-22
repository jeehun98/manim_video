"""Burn concise narration excerpts using only supplied storyboard cue boundaries."""
from pathlib import Path
import argparse,json,subprocess
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]
CUES=[(0, 1, '서로 다른 두 행렬'), (1, 7, 'A에는 2와 1, D의 대각선에는\n3과 1이 놓여 있습니다.'), (7, 10, '같은 좌표 숫자를 입력하면\n서로 다른 결과가 나옵니다.'), (10, 15, '반드시 서로 다른 변환일까요?'), (15, 20, '먼저 둘 다 같은 수평·수직\n좌표계에서 해석하겠습니다.'), (20, 25, 'A는 수평·수직 성분을\n서로 섞으며 공간을 변형합니다.'), (25, 30, 'D는 수평으로 3배 늘리고\n수직 방향은 그대로 유지합니다.'), (30, 31, '분명 서로 다른 모습입니다.'), (31, 34, '한 가지를 바꿔보겠습니다.'), (34, 37, '변환 자체가 아니라\n변환을 바라보는 좌표계입니다.'), (37, 43, '수평과 수직만이\n좌표축의 선택지는 아닙니다.'), (43, 49, '오른쪽 위와 오른쪽 아래를 향하는\n두 대각선을 새 축으로 선택합니다.'), (49, 53, '각 축의 단위 눈금도\n새로운 기준에 맞춰 바꿉니다.'), (53, 59, '벡터는 움직이지 않았습니다.\n기준과 좌표 숫자만 달라졌습니다.'), (59, 64, '같은 벡터의 좌표가\n(2, 1)에서 (1.5, 0.5)로 바뀝니다.'), (64, 68, '각 좌표계에서\n각각의 행렬을 적용하겠습니다.'), (68, 72, 'A를 적용한 표준 좌표는\n(5, 4)입니다.'), (72, 77, 'D를 적용한 새로운 좌표는\n(4.5, 0.5)입니다.'), (77, 79, '출력 좌표 숫자는 서로 다릅니다.'), (79, 85, '새 좌표축으로 결과를 그리면\n두 실제 화살표가 겹칩니다.'), (85, 89, '다른 숫자로 계산했지만\n같은 실제 벡터에 도달했습니다.'), (89, 93, '이 벡터에서만 일어나는\n우연이 아닙니다.'), (93, 99, '어떤 벡터도 좌표를 바르게 바꾸면\n같은 실제 결과에 도달합니다.'), (99, 106, '새 좌표계에서는 두 방향의\n독립적인 확대와 유지로 보입니다.'), (106, 110, '두 축은 이 변환의\n고유벡터 방향입니다.'), (110, 115, '같은 변환을 다른 기저로 표현하면\n두 행렬은 닮음 관계입니다.'), (115, 120, '행렬의 숫자는 변환의 작용과\n표현의 좌표계를 함께 반영합니다.')]
def stamp(t,ass=False):
 return f'{t//3600}:{t//60%60:02d}:{t%60:02d}.00' if ass else f'{t//3600:02d}:{t//60%60:02d}:{t%60:02d},000'
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--layout',choices=['shorts','longform','both'],default='both');parser.add_argument('--preview',action='store_true');args=parser.parse_args()
 (ROOT/'caption_cues.json').write_text(json.dumps({'kind':'내레이션 핵심 발췌 자막','timing':'사용자 제공 문장별 종료 시각 27개, 120초','cues':[{'start':a,'end':b,'text':s} for a,b,s in CUES]},ensure_ascii=False,indent=2),encoding='utf-8')
 for layout in (['shorts','longform'] if args.layout=='both' else [args.layout]):
  portrait=layout=='shorts';w,h=(1080,1920) if portrait else (1920,1080)
  header=f'''[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Malgun Gothic,{60 if portrait else 46},&H00F7F3ED,&H00F7F3ED,&H00101A26,&H80000000,0,0,0,0,100,100,0,0,1,0,0,2,65,65,{170 if portrait else 30},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
  lines=[]
  for a,b,s in CUES:
   caption=s.replace('\n',r'\N' if portrait else ' ')
   lines.append(f'Dialogue: 0,{stamp(a,True)},{stamp(b,True)},Default,,0,0,0,,{caption}')
  ass=ROOT/f'captions_excerpt_{layout}.ass';ass.write_text(header+'\n'.join(lines)+'\n',encoding='utf-8-sig')
  suffix='preview' if args.preview else 'final'
  source=WORKSPACE/'exports'/f'eigen02_120s_{layout}_{suffix}.mp4';target=source.with_name(source.stem+'_captioned.mp4')
  relative=ass.relative_to(WORKSPACE).as_posix()
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',f'ass={relative}','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(target)],check=True,cwd=WORKSPACE)
  (ROOT/f'captions_excerpt_{layout}.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s if portrait else s.replace(chr(10)," ")}' for i,(a,b,s) in enumerate(CUES))+'\n',encoding='utf-8')
  print('CAPTIONED',target,flush=True)
if __name__=='__main__':main()
