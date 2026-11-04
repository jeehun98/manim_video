"""Verify exact media timing and code/mask/lane consistency; review actual frames."""
import json,subprocess,io,argparse
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def main():
    a=argparse.ArgumentParser();a.add_argument('--preview',action='store_true');args=a.parse_args();suffix='preview' if args.preview else 'final';fps=15 if args.preview else 30
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'));cues=json.loads((P/'timing.json').read_text(encoding='utf-8'))
    assert len(manifest)==20 and len(cues)==34
    for series in [manifest,cues]:
        assert series[0]['start']==0 and series[-1]['end']==167
        for left,right in zip(series,series[1:]):assert left['end']==right['start']
    report=dict(duration_seconds=167,frames=167*fps,checks=[],audio='none; narration audio not supplied')
    times=[4,13,24,32,44,54,60,76,83,93,98,104,115,127,140,163]
    for layout in ['shorts','longform']:
        path=ROOT/'exports'/f'gpuh02_warp_167s_{layout}_{suffix}.mp4';data=probe(path);v=next(x for x in data['streams'] if x['codec_type']=='video')
        dims=((360,640) if layout=='shorts' else (640,360)) if args.preview else ((1080,1920) if layout=='shorts' else (1920,1080))
        assert (v['width'],v['height'])==dims and v['r_frame_rate']==f'{fps}/1'
        assert int(v['nb_frames'])==167*fps and abs(float(v['duration'])-167)<.001
        assert v['pix_fmt']=='yuv420p' and not any(x['codec_type']=='audio' for x in data['streams'])
        bounds=[];traces=[]
        for m in manifest:
            i=int(m['id'])-1
            bounds.extend(json.loads((P/f'geometry_{layout}_{i:02}.json').read_text(encoding='utf-8')))
            traces.extend(json.loads((P/f'states_{layout}_{i:02}.json').read_text(encoding='utf-8')))
        fw,fh=(9,16) if layout=='shorts' else (16,9)
        for b in bounds:
            assert -fw/2+.15<b['left']<b['right']<fw/2-.15,b
            assert -fh/2+.15<b['bottom']<b['top']<fh/2-.15,b
        maps=[t for t in traces if t['kind']=='layout'];assert len(maps)==20
        for key in ['lane_centers','map_centers']:
            ref=maps[0][key];assert len(ref)==32
            for t in maps:
                assert len(t[key])==32
                assert max(abs(a-b) for l,r in zip(ref,t[key]) for a,b in zip(l,r))<1e-6,(key,t)
        masks=[t for t in traces if t['kind']=='mask']
        for t in masks:
            mode=t['mode'];expected=list(range(16)) if mode=='mul' else list(range(16,32)) if mode=='add' else list(range(32))
            assert t['active_lanes']==expected and t['mask']==f'0x{sum(1<<k for k in expected):08X}'
            if mode=='mul':assert any('* 2.0f' in s for s in t['active_code']),t
            if mode=='add':assert any('+ 1.0f' in s for s in t['active_code']),t
        assert any(95<=t['time']<102 and t['mode']=='mul' for t in masks)
        assert any(102<=t['time']<106 and t['mode']=='add' for t in masks)
        assert any(124<=t['time']<129 and t['mode']=='all' for t in masks)
        tw,th=(270,480) if layout=='shorts' else (480,270)
        sheet=Image.new('RGB',(tw*4,(th+26)*4),'#182438');draw=ImageDraw.Draw(sheet)
        for j,t in enumerate(times):
            raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf',f'scale={tw}:{th}','-f','image2pipe','-vcodec','png','-'])
            frame=Image.open(io.BytesIO(raw)).convert('RGB');x=(j%4)*tw;y=(j//4)*(th+26);sheet.paste(frame,(x,y));draw.text((x+8,y+th+5),f'{t}s',fill='white')
        out=ROOT/'exports'/f'gpuh02_qa_{layout}_{suffix}.jpg';sheet.save(out,quality=92)
        report['checks'].append(dict(path=str(path),width=v['width'],height=v['height'],frames=int(v['nb_frames']),fps=fps,seconds=v['duration'],codec=v['codec_name'],geometry_samples=len(bounds),mask_states=len(masks),lane_coordinates='32 fixed positions across all 20 scenes',code_and_mask='consistent',contact_sheet=str(out)))
    (P/f'qa_{suffix}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
