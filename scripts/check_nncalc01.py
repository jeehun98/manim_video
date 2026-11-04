"""Check video metadata and make a per-section visual review sheet."""
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'episodes/nncalc01_same_answers'
OUT=ROOT/'media/nncalc01/qa'

def main():
    shorts='--shorts' in sys.argv
    preview='--preview' in sys.argv
    episode='nncalc01_shorts' if shorts else 'nncalc01'
    output_dir=ROOT/'media'/episode/'qa'
    video=ROOT/'exports'/(episode+('_preview' if preview else '')+'.mp4')
    data=json.loads((FOLDER/'timing.json').read_text(encoding='utf-8'))
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    stream=next(s for s in probe['streams'] if s['codec_type']=='video')
    duration=float(probe['format']['duration'])
    expected=((360,640) if preview else (1080,1920)) if shorts else ((640,360) if preview else (1920,1080))
    thumb_w,thumb_h=(360,640) if shorts else (640,360)
    cols,rows=(4,2) if shorts else (2,4)
    assert (stream['width'],stream['height'])==expected
    assert stream['r_frame_rate']=='30/1'
    assert abs(duration-data['duration'])<.1 and duration<180
    tts=(FOLDER/'tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n')
    assert tts==[' '.join(c['spoken'] for c in s['cues']) for s in data['segments']]
    assert [c['end'] for c in data['cues']]==[3,6,13,19,25,29,35,38,43,50,57,61,65,67,72,80,85,89,97,103,108,114,119,124,127,135,140,144,151,156,159,164]
    assert all(a['end']==b['start'] for a,b in zip(data['segments'],data['segments'][1:]))
    for s in data['segments']:
        assert s['start']<s['end']
        assert all(c['start']<c['end'] for c in s['cues'])
    output_dir.mkdir(parents=True,exist_ok=True)
    frames=[]
    for s in data['segments']:
        target=output_dir/f'{"preview" if preview else "final"}_{s["index"]:02}.png'
        # Sample after section transition with a representative caption visible.
        time=s['start']+(s['end']-s['start'])*.58
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(time),'-i',str(video),
                        '-frames:v','1','-vf',f'scale={thumb_w}:{thumb_h}',str(target)],check=True)
        frames.append(target)
    sheets=[]
    for offset in (0,8):
        sheet=Image.new('RGB',(thumb_w*cols,(thumb_h+20)*rows),'#182633')
        draw=ImageDraw.Draw(sheet)
        for j,path in enumerate(frames[offset:offset+8]):
            x=(j%cols)*thumb_w;y=(j//cols)*(thumb_h+20)
            sheet.paste(Image.open(path),(x,y+20))
            draw.text((x+10,y+3),f'{offset+j+1:02}',fill='white')
        dest=output_dir/f'{"preview" if preview else "final"}_sheet_{offset//8+1}.jpg'
        sheet.save(dest,quality=94);sheets.append(str(dest))
    result={'video':str(video),'duration':duration,'width':stream['width'],'height':stream['height'],
            'fps':stream['r_frame_rate'],'audio_streams':sum(s['codec_type']=='audio' for s in probe['streams']),
            'timing_source':'32 user-provided cumulative sentence ends; no audio file supplied','narration_tts_consistent':True,'sections':len(frames),
            'contact_sheets':sheets}
    detail=Image.new('RGB',(thumb_w*2,(thumb_h+20)*2),'#182633')
    detaildraw=ImageDraw.Draw(detail)
    for j,time in enumerate([74,77,138,160]):
        target=output_dir/f'{"preview" if preview else "final"}_detail_{time}.png'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(time),'-i',str(video),
                        '-frames:v','1','-vf',f'scale={thumb_w}:{thumb_h}',str(target)],check=True)
        x=j%2*thumb_w;y=j//2*(thumb_h+20)
        detail.paste(Image.open(target),(x,y+20));detaildraw.text((x+10,y+3),f'{time}s',fill='white')
    detailpath=output_dir/f'{"preview" if preview else "final"}_critical.jpg'
    detail.save(detailpath,quality=94)
    result['critical_frames']=str(detailpath)
    (output_dir/f'{"preview" if preview else "final"}_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
