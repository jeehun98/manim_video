"""Check delivered media and create visual review sheets from actual frames."""
import json,subprocess,io,argparse
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def main():
    a=argparse.ArgumentParser();a.add_argument('--preview',action='store_true');args=a.parse_args()
    suffix='preview' if args.preview else 'final';fps=15 if args.preview else 30
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'));cues=json.loads((P/'timing.json').read_text(encoding='utf-8'))
    assert len(manifest)==16 and len(cues)==33
    for series in [manifest,cues]:
        assert series[0]['start']==0 and series[-1]['end']==152
        for left,right in zip(series,series[1:]):assert left['end']==right['start']
    report=dict(duration_seconds=152,frames=152*fps,checks=[],audio='none; source narration audio not provided')
    times=[6,12,26,34,45,53,58,66,75,88,96,106,118,126,132,150]
    for layout in ['shorts','longform']:
        path=ROOT/'exports'/f'gpuh01_thread_152s_{layout}_{suffix}.mp4'
        data=probe(path);streams=data['streams'];v=next(x for x in streams if x['codec_type']=='video')
        dims=((360,640) if layout=='shorts' else (640,360)) if args.preview else ((1080,1920) if layout=='shorts' else (1920,1080))
        assert (v['width'],v['height'])==dims
        assert v['r_frame_rate']==f'{fps}/1' and int(v['nb_frames'])==152*fps
        assert abs(float(v['duration'])-152)<.001 and v['pix_fmt']=='yuv420p'
        assert not any(x['codec_type']=='audio' for x in streams)
        bounds=[]
        for f in P.glob(f'geometry_{layout}_*.json'):bounds.extend(json.loads(f.read_text(encoding='utf-8')))
        assert bounds
        fw,fh=(9,16) if layout=='shorts' else (16,9)
        for b in bounds:
            assert -fw/2+.15<b['left']<b['right']<fw/2-.15,b
            assert -fh/2+.15<b['bottom']<b['top']<fh/2-.15,b
        tw,th=(270,480) if layout=='shorts' else (480,270)
        sheet=Image.new('RGB',(tw*4,(th+26)*4),'#182438');draw=ImageDraw.Draw(sheet)
        for j,t in enumerate(times):
            raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf',f'scale={tw}:{th}','-f','image2pipe','-vcodec','png','-'])
            frame=Image.open(io.BytesIO(raw)).convert('RGB');x=(j%4)*tw;y=(j//4)*(th+26)
            sheet.paste(frame,(x,y));draw.text((x+8,y+th+5),f'{t}s',fill='white')
        out=ROOT/'exports'/f'gpuh01_qa_{layout}_{suffix}.jpg';sheet.save(out,quality=92)
        report['checks'].append(dict(path=str(path),width=v['width'],height=v['height'],frames=int(v['nb_frames']),fps=fps,seconds=v['duration'],codec=v['codec_name'],geometry_samples=len(bounds),contact_sheet=str(out)))
    (P/f'qa_{suffix}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
