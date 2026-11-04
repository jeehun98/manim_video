"""Check exact timing, identity-preserving placement, independent outputs and media."""
import argparse,json,subprocess,io,math
from collections import Counter
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--layout',choices=['both','shorts','longform'],default='both');a=ap.parse_args()
    cues=json.loads((P/'timing.json').read_text(encoding='utf-8'));shots=json.loads((P/'manifest.json').read_text(encoding='utf-8'))
    assert len(cues)==37 and len(shots)==18
    for rows in [cues,shots]:
        assert rows[0]['start']==0 and rows[-1]['end']==178
        assert all(x['end']==y['start'] for x,y in zip(rows,rows[1:]))
    cuda=json.loads((P/'cuda_trace.json').read_text());assert cuda['N']==1536 and cuda['grid']==12 and cuda['block']==128
    assert cuda['C']==[i*11+1 for i in range(1536)]
    assert 'all 5120 pixels' in (P/'cuda_validation.txt').read_text() and 'all 4697 pixels' in (P/'cuda_validation.txt').read_text()
    report=[]
    for layout,w,h in [('shorts',1080,1920),('longform',1920,1080)]:
        if a.layout!='both' and a.layout!=layout:continue
        suffix=layout+('_preview' if a.preview else '_final');fps=15 if a.preview else 30
        if a.preview:w//=3;h//=3
        path=ROOT/'exports'/f'gpuh05_grid_178s_{suffix}.mp4'
        info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]));stream=info['streams'][0]
        assert (stream['width'],stream['height'])==(w,h)
        assert stream['r_frame_rate']==f'{fps}/1' and int(stream['nb_frames'])==178*fps
        assert abs(float(info['format']['duration'])-178)<.001
        assert not any(s['codec_type']=='audio' for s in info['streams'])
        baseline=None;states=[];geometry_count=0
        for i in range(18):
            scene_states=json.loads((P/f'states_{layout}_{i:02}.json').read_text(encoding='utf-8'));states.extend(scene_states)
            first=scene_states[0];assert first['kind']=='logical_layout'
            assert first['block_count']==12 and first['logical_threads']==1536 and first['threads_per_block']==128
            assert first['block5_color']=='#50E0AE'
            if baseline is None:baseline=first['block_centers']
            assert first['block_centers']==baseline
            geometry=json.loads((P/f'geometry_{layout}_{i:02}.json').read_text(encoding='utf-8'))
            for b in geometry:
                fw,fh=(9,16) if layout=='shorts' else (16,9)
                assert b['left']>-fw/2+.15 and b['right']<fw/2-.15
                assert b['bottom']>-fh/2+.15 and b['top']<fh/2-.15
            # The logical Grid is spatially outside the physical GPU panel.
            assert geometry[0]['bottom']>geometry[1]['top']+.05
            geometry_count+=len(geometry)
        for s in states:
            if s['kind']=='assignment':
                mapping={int(b):sm for b,sm in s['mapping'].items()};done=set(s['completed']);pending=set(s['pending']);resident=set(mapping)
                assert resident|done|pending==set(range(12)) and not (resident&done or resident&pending or done&pending)
                assert all(0<=sm<4 for sm in mapping.values()) and all(n<=2 for n in Counter(mapping.values()).values())
                assert s['illustrative']
            if s['kind']=='index':assert s['index']==s['block']*s['block_dim']+s['thread']
            if s['kind']=='order_examples':
                assert sorted(s['order_a'])==sorted(s['order_b'])==list(range(12)) and s['order_a']!=s['order_b']
                for order in [s['order_a'],s['order_b']]:
                    out=[None]*1536
                    for b in order:
                        for t in range(128):i=b*128+t;assert out[i] is None;out[i]=11*i+1
                    assert out==cuda['C']
            if s['kind']=='image_layout':assert s['grid']==[5,4] and s['block']==[16,16] and s['image']==[80,64] and s['separate_kernel']=='imageKernel'
        assert [(s['block'],s['thread'],s['index']) for s in states if s['kind']=='index']==[(0,5,5),(1,5,133)]
        assert any(s['kind']=='assignment' and 104<=s['time']<108 and s['mapping'].get('0')==s['mapping'].get('7')==0 for s in states)
        assert any(s['kind']=='assignment' and 111<=s['time']<115 and s['mapping'].get('4')==0 and 7 in s['completed'] for s in states)
        assert any(s['kind']=='image_assignment' and s['tile']==[2,1] and s['sm']==3 for s in states)
        times=[11,25,38,45,52,66,75,84,90,102,113,124,130,138,149,154,164,176]
        tw,th=(216,384) if layout=='shorts' else (384,216);sheet=Image.new('RGB',(tw*4,(th+24)*math.ceil(len(times)/4)),'#0B1220');draw=ImageDraw.Draw(sheet)
        for k,t in enumerate(times):
            data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf',f'scale={tw}:{th}','-f','image2pipe','-vcodec','png','-'])
            im=Image.open(io.BytesIO(data));x=k%4*tw;y=k//4*(th+24);sheet.paste(im,(x,y));draw.text((x+5,y+th+4),f'{t}s',fill='white')
        sheet.save(ROOT/'exports'/f'gpuh05_qa_{suffix}.jpg',quality=93)
        report.append(dict(layout=layout,frames=int(stream['nb_frames']),duration=info['format']['duration'],geometry_samples=geometry_count,grid='fixed 12 logical Blocks, separate from physical GPU',index_examples=[5,133],placement='capacity and ID invariants passed; illustrative scenarios',CUDA='1536 vector outputs and separate 2D kernels passed'))
    dest=P/('qa_preview.json' if a.preview else 'qa_final.json')
    if a.layout!='both' and dest.exists():
        prior={r['layout']:r for r in json.loads(dest.read_text(encoding='utf-8'))}
        prior.update({r['layout']:r for r in report});combined=[prior[k] for k in ['shorts','longform'] if k in prior]
    else:combined=report
    dest.write_text(json.dumps(combined,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
