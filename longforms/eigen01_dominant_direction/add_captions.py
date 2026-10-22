"""Burn concise narration excerpts using only supplied storyboard cue boundaries."""
from pathlib import Path
import argparse,json,subprocess
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]
CUES=[
(0,3,'평면 위에 벡터 하나를\n놓아보겠습니다.'),
(3,12,'같은 행렬을 반복해서 적용하면\n벡터의 방향이 달라집니다.'),
(12,19,'반복할수록 벡터가\n특정한 방향을 향하기 시작합니다.'),
(19,26,'길이를 일정하게 맞추고\n방향의 변화만 관찰하겠습니다.'),
(26,34,'서로 다른 방향의 벡터들도\n하나의 직선 방향으로 정렬됩니다.'),
(34,45,'어떤 방향에서는 변환 후에도\n벡터가 원래의 직선 위에 남습니다.'),
(45,55,'한 방향은 길이가 3배로 늘어나고\n다른 방향은 그대로 유지됩니다.'),
(55,60,'같은 직선 위에 남는 특별한 방향을\n고유방향이라고 합니다.'),
(60,64,'그 방향 위의 영벡터가 아닌 벡터가\n고유벡터입니다.'),
(64,69,'고유벡터를 몇 배로 바꾸는지\n나타내는 수가 고윳값입니다.'),
(69,74,'고윳값은 첫 방향에서 3,\n두 번째 방향에서 1입니다.'),
(74,80,'고유방향과 고윳값은\n행렬의 변환 방식이 결정합니다.'),
(80,84,'지금 선택한 벡터에는\n두 고유성분이 섞여 있습니다.'),
(84,88,'한 번 적용하면 첫 성분은 3배,\n두 번째 성분은 그대로입니다.'),
(88,92,'두 번 적용하면\n첫 성분은 처음의 9배가 됩니다.'),
(92,96,'세 번 적용하면\n첫 성분은 처음의 27배가 됩니다.'),
(96,105,'더 크게 자라는 성분이 압도하면\n전체 방향도 그쪽으로 향합니다.'),
(105,114,'처음에 그 고유성분이 없다면\n그 방향으로 수렴하지 않습니다.'),
(114,119,'더 크게 증폭되는 고유성분이\n전체 벡터의 방향을 결정합니다.')]
def stamp(t,ass=False):
 return f'{t//3600}:{t//60%60:02d}:{t%60:02d}.00' if ass else f'{t//3600:02d}:{t//60%60:02d}:{t%60:02d},000'
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--layout',choices=['shorts','longform','both'],default='both');args=parser.parse_args()
 (ROOT/'caption_cues.json').write_text(json.dumps({'kind':'내레이션 핵심 발췌 자막','timing':'사용자 콘티의 구간 및 정의·성장률 세부 시각; 문장 종료 시각 추정 아님','cues':[{'start':a,'end':b,'text':s} for a,b,s in CUES]},ensure_ascii=False,indent=2),encoding='utf-8')
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
  source=WORKSPACE/'exports'/f'eigen01_119s_{layout}_final.mp4';target=source.with_name(source.stem+'_captioned.mp4')
  relative=ass.relative_to(WORKSPACE).as_posix()
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',f'ass={relative}','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(target)],check=True,cwd=WORKSPACE)
  (ROOT/f'captions_excerpt_{layout}.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s if portrait else s.replace(chr(10)," ")}' for i,(a,b,s) in enumerate(CUES))+'\n',encoding='utf-8')
  print('CAPTIONED',target,flush=True)
if __name__=='__main__':main()
