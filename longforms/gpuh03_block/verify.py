"""Validate CUDA/model/video alignment and build review sheets from final frames."""
import json,subprocess,io,argparse
from pathlib import Path
from PIL import Image,ImageDraw
from reduction_model import STAGES
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def main():
    a=argparse.ArgumentParser();a.add_argument('--preview',action='store_true');args=a.parse_args();suffix='preview' if args.preview else 'final';fps=15 if args.preview else 30
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'));cues=json.loads((P/'timing.json').read_text(encoding='utf-8'))
    assert len(manifest)==20 and len(cues)==39
    for series in [manifest,cues]:
        assert series[0]['start']==0 and series[-1]['end']==178
        for left,right in zip(series,series[1:]):assert left['end']==right['start']
    gpu=json.loads((P/'cuda_trace.json').read_text(encoding='utf-8'));assert gpu['output']==8256 and gpu['total_threads']==128
    assert gpu['stages']==STAGES
    report=dict(duration_seconds=178,frames=178*fps,cuda_validation='original output and all 128 slots at all 8 snapshots match CPU model',checks=[],audio='none; narration audio not supplied')
    times=[3,15,26,40,53,65,75,85,95,110,118,125,132,141,154,175]
    for layout in ['shorts','longform']:
        path=ROOT/'exports'/f'gpuh03_block_178s_{layout}_{suffix}.mp4';data=probe(path);v=next(x for x in data['streams'] if x['codec_type']=='video')
        dims=((360,640) if layout=='shorts' else (640,360)) if args.preview else ((1080,1920) if layout=='shorts' else (1920,1080))
        assert (v['width'],v['height'])==dims and v['r_frame_rate']==f'{fps}/1'
        assert int(v['nb_frames'])==178*fps and abs(float(v['duration'])-178)<.001 and v['pix_fmt']=='yuv420p'
        assert not any(x['codec_type']=='audio' for x in data['streams'])
        bounds=[];traces=[]
        for m in manifest:
            i=int(m['id'])-1
            bounds.extend(json.loads((P/f'geometry_{layout}_{i:02}.json').read_text(encoding='utf-8')))
            traces.extend(json.loads((P/f'states_{layout}_{i:02}.json').read_text(encoding='utf-8')))
        fw,fh=(9,16) if layout=='shorts' else (16,9)
        for b in bounds:
            assert -fw/2+.15<b['left']<b['right']<fw/2-.15,b
            assert -fh/2+.15<b['bottom']<b['top']<fh/2-.15,b
        layouts=[t for t in traces if t['kind']=='layout'];assert len(layouts)==20
        for key,n in [('thread_centers',128),('shared_centers',128)]:
            ref=layouts[0][key];assert len(ref)==n
            for t in layouts:
                assert len(t[key])==n
                assert max(abs(a-b) for l,r in zip(ref,t[key]) for a,b in zip(l,r))<1e-6
        for t in [s for s in traces if s['kind'] in ['reduction','cross_warp_example','final_reduction']]:
            expected=next(s for s in STAGES if s['stride']==t['stride'])
            assert t['values']==expected['values'] and t['count']==expected['count']
            assert t['total_threads']==128 and t['barrier_participants']==128 and t['add_participants']==t['stride']
            assert sum(t['values'][:t['count']])==8256
            assert any('s[t] += s[t + stride]' in s for s in t['add_code'])
            assert t['barrier_code']==['__syncthreads();']
        seq=[t['stride'] for t in traces if t['kind']=='reduction'];assert seq==[64,32,16,8,4,2,1],seq
        for t in [s for s in traces if s['kind']=='barrier']:
            assert t['participants']==128 and t['scope']=='Block 0' and t['active_code']==['__syncthreads();']
        assert any(t['kind']=='output' and t['output']==8256 and t['thread']==0 for t in traces)
        tw,th=(270,480) if layout=='shorts' else (480,270)
        sheet=Image.new('RGB',(tw*4,(th+26)*4),'#182438');draw=ImageDraw.Draw(sheet)
        for j,t in enumerate(times):
            raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf',f'scale={tw}:{th}','-f','image2pipe','-vcodec','png','-'])
            frame=Image.open(io.BytesIO(raw)).convert('RGB');x=(j%4)*tw;y=(j//4)*(th+26);sheet.paste(frame,(x,y));draw.text((x+8,y+th+5),f'{t}s',fill='white')
        out=ROOT/'exports'/f'gpuh03_qa_{layout}_{suffix}.jpg';sheet.save(out,quality=92)
        report['checks'].append(dict(path=str(path),width=v['width'],height=v['height'],frames=int(v['nb_frames']),fps=fps,seconds=v['duration'],codec=v['codec_name'],geometry_samples=len(bounds),thread_and_shared_coordinates='128 fixed thread slots and 128 fixed shared slots across 20 scenes',reduction_counts=seq,all_barriers=128,output=8256,contact_sheet=str(out)))
    (P/f'qa_{suffix}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
