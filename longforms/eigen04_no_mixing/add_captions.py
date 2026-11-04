"""Burn concise narration excerpts using only supplied storyboard cue boundaries."""
from pathlib import Path
import argparse,json,subprocess
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]
CUES=[(0, 4, '행렬은 서로 다른\n좌표 성분을 섞기도 합니다.'), (4, 8, '좌표계를 잘 선택하면\n성분의 섞임을 없앨 수 있을까요?'), (8, 10, '하나의 행렬을 살펴보겠습니다.'), (10, 16, '첫 출력 성분에는\n두 입력이 모두 영향을 줍니다.'), (16, 18, '두 번째 출력 성분도\n마찬가지입니다.'), (18, 20, '좌표축을 바꿔보겠습니다.'), (20, 27, '서로 독립인 두 벡터를\n새 기저로 선택할 수 있습니다.'), (27, 32, '아무 좌표계나 고른다고\n섞임이 사라지지는 않습니다.'), (32, 35, '첫 번째 축 위의 벡터를\n변환해 보겠습니다.'), (35, 42, '축을 벗어난 출력은\n다른 축 성분도 만든다는 뜻입니다.'), (42, 45, '두 번째 축에서도\n같은 일이 일어날 수 있습니다.'), (45, 50, '변환 후에도 각 축을 벗어나지 않는\n방향을 선택하면 어떨까요?'), (50, 52, '이것이 바로 고유벡터 방향입니다.'), (52, 56, '고유벡터는 변환 후에도\n원래의 직선 위에 남습니다.'), (56, 62, '각 축이 자기 직선 위에 남으면\n다른 축의 성분을 만들지 않습니다.'), (62, 68, '첫 고유축의 성분은\n다른 축의 출력 성분은 0입니다.'), (68, 75, '독립인 두 고유축을 고르면\n각 성분은 배율만 바뀝니다.'), (75, 80, '첫 번째 성분은 3배,\n두 번째 성분은 그대로입니다.'), (80, 86, '새 좌표계에서는\n두 성분이 독립적으로 변합니다.'), (86, 93, '고유벡터 기저로 표현해\n대각행렬이 되면 대각화입니다.'), (93, 95, '세 단계로 설명할 수 있습니다.'), (95, 98, '먼저 벡터를\n고유벡터 기저의 좌표로 읽습니다.'), (98, 101, '각 성분에\n해당 고윳값을 곱합니다.'), (101, 104, '결과를 원래 좌표계로\n되돌립니다.'), (104, 108, '세 단계를 정리한 것이\n대각화 공식입니다.'), (108, 110, '행렬의 작용 자체를\n바꾼 것은 아닙니다.'), (110, 115, '성분은 서로 섞이지 않고\n각자의 배율로만 변합니다.')]
def stamp(t,ass=False):
 return f'{t//3600}:{t//60%60:02d}:{t%60:02d}.00' if ass else f'{t//3600:02d}:{t//60%60:02d}:{t%60:02d},000'
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--layout',choices=['shorts','longform','both'],default='both');parser.add_argument('--preview',action='store_true');args=parser.parse_args()
 (ROOT/'caption_cues.json').write_text(json.dumps({'kind':'내레이션 핵심 발췌 자막','timing':'사용자 제공 문장별 종료 시각 27개, 115초','cues':[{'start':a,'end':b,'text':s} for a,b,s in CUES]},ensure_ascii=False,indent=2),encoding='utf-8')
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
  source=WORKSPACE/'exports'/f'eigen04_115s_{layout}_{suffix}.mp4';target=source.with_name(source.stem+'_captioned.mp4')
  relative=ass.relative_to(WORKSPACE).as_posix()
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',f'ass={relative}','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(target)],check=True,cwd=WORKSPACE)
  (ROOT/f'captions_excerpt_{layout}.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s if portrait else s.replace(chr(10)," ")}' for i,(a,b,s) in enumerate(CUES))+'\n',encoding='utf-8')
  print('CAPTIONED',target,flush=True)
if __name__=='__main__':main()
