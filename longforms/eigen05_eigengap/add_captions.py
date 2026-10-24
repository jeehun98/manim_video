"""Burn concise narration excerpts using only supplied storyboard cue boundaries."""
from pathlib import Path
import argparse,json,subprocess
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]
CUES=[(0, 6, '데이터는 조금 달라졌는데\n주요 방향은 크게 바뀔까요?'), (6, 10, '주성분 분석, PCA에서\n이런 현상이 나타날 수 있습니다.'), (10, 13, '평면에 데이터 점들이\n놓여 있다고 생각해 보겠습니다.'), (13, 20, '길쭉한 분포에서는\n가장 넓게 퍼진 방향이 뚜렷합니다.'), (20, 23, 'PCA는 이런 방향을 찾습니다.'), (23, 29, '평균을 기준으로 위치를 읽고\n퍼짐을 공분산행렬에 담습니다.'), (29, 34, '공분산행렬의 고유벡터로\n가장 크게 퍼진 방향을 찾습니다.'), (34, 38, '가장 큰 고윳값의 고유벡터가\n첫 번째 주성분 방향입니다.'), (38, 43, '분포가 원형에 가깝다면\n어떻게 될까요?'), (43, 49, '두 방향의 퍼짐이 비슷해지면\n두 고윳값도 가까워집니다.'), (49, 53, '가장 넓게 퍼진 방향을\n구분하기 어려워집니다.'), (53, 58, '데이터 일부를 조금\n바꿔보겠습니다.'), (58, 61, '전체적인 점들의 분포는\n거의 달라지지 않았습니다.'), (61, 67, 'PCA를 다시 계산하면\n첫 주성분 직선이 크게 회전합니다.'), (67, 74, '길쭉한 분포는 비슷한 변화에도\n주성분이 비교적 안정적입니다.'), (74, 76, '왜 이런 차이가 발생할까요?'), (76, 81, '가장 큰 고윳값과\n두 번째 고윳값 사이의 간격입니다.'), (81, 84, '이 간격이 아이겐갭,\nEigengap입니다.'), (84, 88, '고윳값은 각 주성분 방향의\n분산을 나타냅니다.'), (88, 91, '고윳값의 간격은\n무엇을 알려줄까요?'), (91, 97, '간격이 크면 첫 주성분의 분산이\n다른 방향보다 뚜렷하게 큽니다.'), (97, 105, '간격이 작으면 작은 변화에도\n주성분이 크게 바뀔 수 있습니다.'), (105, 110, '모든 방향의 분산이 같다면\n어떤 방향으로 투영해도 같습니다.'), (110, 113, '특별한 첫 번째 주성분을\n결정할 수 없습니다.'), (113, 120, '아주 작은 변화에 따라\n특정 주성분 방향이 선택됩니다.'), (120, 125, '데이터의 구조가 갑자기\n크게 바뀌었다는 뜻은 아닙니다.'), (125, 131, '여러 방향의 퍼짐이 거의 같아서\n주성분 방향이 불안정했습니다.'), (131, 136, '고윳값으로 각 주성분 방향의\n퍼짐을 알 수 있습니다.'), (136, 142, '방향의 뚜렷함과 안정성을 보려면\n고윳값 하나만으로는 부족합니다.'), (142, 146, '고윳값의 크기와 함께\n고윳값의 간격도 살펴봐야 합니다.')]
def stamp(t,ass=False):
 return f'{t//3600}:{t//60%60:02d}:{t%60:02d}.00' if ass else f'{t//3600:02d}:{t//60%60:02d}:{t%60:02d},000'
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--layout',choices=['shorts','longform','both'],default='both');parser.add_argument('--preview',action='store_true');args=parser.parse_args()
 (ROOT/'caption_cues.json').write_text(json.dumps({'kind':'내레이션 핵심 발췌 자막','timing':'사용자 제공 문장별 종료 시각 30개, 146초','cues':[{'start':a,'end':b,'text':s} for a,b,s in CUES]},ensure_ascii=False,indent=2),encoding='utf-8')
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
  source=WORKSPACE/'exports'/f'eigen05_146s_{layout}_{suffix}.mp4';target=source.with_name(source.stem+'_captioned.mp4')
  relative=ass.relative_to(WORKSPACE).as_posix()
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',f'ass={relative}','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(target)],check=True,cwd=WORKSPACE)
  (ROOT/f'captions_excerpt_{layout}.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s if portrait else s.replace(chr(10)," ")}' for i,(a,b,s) in enumerate(CUES))+'\n',encoding='utf-8')
  print('CAPTIONED',target,flush=True)
if __name__=='__main__':main()
