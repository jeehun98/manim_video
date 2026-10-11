"""Create an uncropped portrait companion with synchronized large captions."""
from pathlib import Path
import json,subprocess,textwrap
from PIL import Image,ImageDraw,ImageFont
import av
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]

def main():
    source=WORKSPACE/'exports/mm01_cubic_question_142s_1080p30.mp4'
    output=WORKSPACE/'exports/mm01_cubic_question_142s_short_1080x1920.mp4'
    bg=Image.new('RGB',(1080,1920),'#081622');draw=ImageDraw.Draw(bg)
    font_path='C:/Windows/Fonts/malgun.ttf'
    def label(s,y,size,color):
        font=ImageFont.truetype(font_path,size)
        for line in s.split('\n'):
            box=draw.textbbox((0,0),line,font=font)
            draw.text(((1080-(box[2]-box[0]))/2,y),line,font=font,fill=color)
            y+=int(size*1.5)
    label('행렬곱의 계산량 · 01',155,36,'#8FAABD')
    label('행렬곱은 정말\n세제곱번 계산해야 할까?',245,62,'#EAF5FB')
    draw.line((80,490,1000,490),fill='#294958',width=2)
    label('8번의 곱셈 → 7번의 재조합',1245,40,'#51D8EE')
    label('입력은 그대로 · 계산 구조는 다르게',1325,32,'#8FAABD')
    label('STRASSEN · MATRIX MULTIPLICATION',1810,24,'#8FAABD')
    bg.save(ROOT/'short_background.png')
    header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Malgun Gothic,48,&H00FBF5EA,&H00FBF5EA,&H00221608,&H00221608,0,0,0,0,100,100,0,0,1,1,0,5,90,90,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    def stamp(t):return f'{t//3600}:{t//60%60:02d}:{t%60:02d}.00'
    events=[]
    for r in json.loads((ROOT/'narration_timing.json').read_text(encoding='utf-8')):
        caption=r'\N'.join(textwrap.wrap(r['text'],width=22))
        events.append(f"Dialogue: 0,{stamp(r['start'])},{stamp(r['end'])},Default,,0,0,0,,{{\\pos(540,1540)}}{caption}")
    ass=ROOT/'short_captions.ass';ass.write_text(header+'\n'.join(events)+'\n',encoding='utf-8-sig')
    # Run in ROOT so the libass filter needs no Windows drive escaping.
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-i','short_background.png','-i',str(source),
        '-filter_complex','[1:v]scale=1080:608[v];[0:v][v]overlay=0:560,ass=short_captions.ass[out]',
        '-map','[out]','-an','-t','142','-r','30','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],cwd=ROOT,check=True)
    with av.open(str(output)) as c:
        s=c.streams.video[0]
        assert (s.width,s.height,s.frames)==(1080,1920,4260)
        assert s.average_rate==30
        assert abs(float(s.duration*s.time_base)-142)<1/30
    print(f'OK: {output}')

if __name__=='__main__':main()
