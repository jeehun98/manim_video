"""Burn concise narration excerpts using only supplied storyboard cue boundaries."""
from pathlib import Path
import argparse,json,subprocess
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]
CUES=[(0, 5, '반복해서 적용하면 어떤 벡터는\n특정한 방향에 가까워집니다.'), (5, 9, '그 고유방향에서의 배율이\n고윳값입니다.'), (9, 14, '같은 선형변환도 좌표계에 따라\n다른 행렬로 표현됩니다.'), (14, 18, '벡터의 좌표도, 행렬 원소도\n달라집니다.'), (18, 22, '좌표계가 달라져도\n변하지 않는 것은 무엇일까요?'), (22, 24, '하나의 행렬을 살펴보겠습니다.'), (24, 31, '첫 방향은 3배로 늘어나고,\n두 번째 방향은 그대로입니다.'), (31, 33, '고윳값은 각각 3과 1입니다.'), (33, 36, '다른 좌표계에서\n같은 행렬을 표현하겠습니다.'), (36, 41, '좌표축과 단위 눈금이 바뀌면\n행렬의 원소도 달라집니다.'), (41, 44, '다른 좌표계에서는\n행렬의 숫자가 또 달라집니다.'), (44, 47, '그런데 고윳값 3과 1은\n변하지 않습니다.'), (47, 53, '고유벡터의 좌표가 달라져도\n실제 변환의 배율은 같습니다.'), (53, 57, '좌표계를 바꿔도 유지되는 성질을\n불변량이라고 합니다.'), (57, 60, '고윳값 외에도\n변하지 않는 숫자가 있습니다.'), (60, 66, '대각 원소의 합인 대각합,\n부호 포함 면적 배율인 행렬식'), (66, 69, '이번 행렬의 대각합은 4,\n행렬식은 3입니다.'), (69, 74, '고윳값 3과 1을 더하면 4,\n곱하면 3이 됩니다.'), (74, 75, '이는 우연이 아닙니다.'), (75, 83, '고윳값의 합은 대각합,\n곱은 행렬식입니다. 중복도 셉니다.'), (83, 87, '좌표계가 달라져도\n이 관계는 유지됩니다.'), (87, 90, '한 가지 주의할 점이 있습니다.'), (90, 96, '이 불변량들이 같아도\n닮음 관계가 보장되지는 않습니다.'), (96, 104, '항등행렬과 전단행렬은\n이 불변량들이 모두 같습니다.'), (104, 107, '하지만 두 행렬은\n닮음 관계가 아닙니다.'), (107, 114, '유지되는 성질이 있다는 것과\n변환 전체를 아는 것은 다릅니다.'), (114, 121, '고윳값은 구조를 보여주지만\n모든 정보를 담지는 않습니다.')]
def stamp(t,ass=False):
 return f'{t//3600}:{t//60%60:02d}:{t%60:02d}.00' if ass else f'{t//3600:02d}:{t//60%60:02d}:{t%60:02d},000'
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--layout',choices=['shorts','longform','both'],default='both');parser.add_argument('--preview',action='store_true');args=parser.parse_args()
 (ROOT/'caption_cues.json').write_text(json.dumps({'kind':'내레이션 핵심 발췌 자막','timing':'사용자 제공 문장별 종료 시각 27개, 121초','cues':[{'start':a,'end':b,'text':s} for a,b,s in CUES]},ensure_ascii=False,indent=2),encoding='utf-8')
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
  source=WORKSPACE/'exports'/f'eigen03_121s_{layout}_{suffix}.mp4';target=source.with_name(source.stem+'_captioned.mp4')
  relative=ass.relative_to(WORKSPACE).as_posix()
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',f'ass={relative}','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(target)],check=True,cwd=WORKSPACE)
  (ROOT/f'captions_excerpt_{layout}.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s if portrait else s.replace(chr(10)," ")}' for i,(a,b,s) in enumerate(CUES))+'\n',encoding='utf-8')
  print('CAPTIONED',target,flush=True)
if __name__=='__main__':main()
