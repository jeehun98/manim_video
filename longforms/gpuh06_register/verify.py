"""Validate narration timing, CUDA data, resource arithmetic and the two videos."""
import argparse,json,re,subprocess,io,math
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--layout',choices=['both','shorts','longform'],default='both');a=ap.parse_args()
    cues=json.loads((P/'timing.json').read_text(encoding='utf-8'));shots=json.loads((P/'manifest.json').read_text(encoding='utf-8'))
    assert len(cues)==38 and len(shots)==18
    for rows in [cues,shots]:
        assert rows[0]['start']==0 and rows[-1]['end']==175
        assert all(x['end']==y['start'] for x,y in zip(rows,rows[1:]))
    cuda=json.loads((P/'cuda_trace.json').read_text());log=(P/'cuda_compile.log').read_text(encoding='utf-8',errors='replace')
    assert cuda['outputs']==[2*i+3 for i in range(1536)] and [cuda['a'],cuda['b'],cuda['sum']]==[3,4,7]
    assert cuda['registers_per_thread']==int(re.search(r'Used (\d+) registers',log).group(1))
    assert cuda['local_bytes']==0 and '0 bytes spill stores, 0 bytes spill loads' in log
    report=[]
    for layout,w,h in [('shorts',1080,1920),('longform',1920,1080)]:
        if a.layout!='both' and layout!=a.layout:continue
        suffix=layout+('_preview' if a.preview else '_final');fps=15 if a.preview else 30
        if a.preview:w//=3;h//=3
        path=ROOT/'exports'/f'gpuh06_register_175s_motion_v3_{suffix}.mp4'
        info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]));stream=info['streams'][0]
        assert (stream['width'],stream['height'])==(w,h)
        assert stream['r_frame_rate']==f'{fps}/1' and int(stream['nb_frames'])==175*fps
        assert abs(float(info['format']['duration'])-175)<.001 and not any(s['codec_type']=='audio' for s in info['streams'])
        baseline=None;states=[];geometry_count=0
        for i in range(18):
            s=json.loads((P/f'states_{layout}_{i:02}.json').read_text(encoding='utf-8'));states.extend(s);first=s[0];last=s[-1]
            assert first['kind']=='identity' and last['kind']=='final_identity'
            assert first['thread']==last['thread']==2 and first['block']==last['block']==0 and first['sm']==last['sm']==0
            mem=next(v for v in s if v['kind']=='memory_layout')
            assert mem['mini_thread_center']==last['mini_thread_center'] and mem['register_center']==last['register_center']
            if i>0:assert first['mini_thread_center']==last['mini_thread_center'] and first['register_center']==last['register_center']
            else:assert 9<=mem['time']<=9.05
            coords=[mem['mini_thread_center'],mem['register_center']]
            if baseline is None:baseline=coords
            assert coords==baseline
            l,r,b,t=mem['sm']
            for k in ['register','shared','l1']:
                nl,nr,nb,nt=mem[k];assert l<=nl<nr<=r and b<=nb<nt<=t
            assert mem['l2'][0]>r and mem['dram'][0]>r and not mem['register_to_shared_serial_path']
            geometry=json.loads((P/f'geometry_{layout}_{i:02}.json').read_text(encoding='utf-8'))
            for item in geometry:
                fw,fh=(9,16) if layout=='shorts' else (16,9)
                assert item['left']>-fw/2+.15 and item['right']<fw/2-.15 and item['bottom']>-fh/2+.15 and item['top']<fh/2-.15
            assert geometry[0]['bottom']>geometry[1]['top']+.08
            geometry_count+=len(geometry)
        demands=[s for s in states if s['kind']=='demand'];assert [(s['registers_per_thread'],s['total_registers']) for s in demands]==[(32,4096),(64,8192)]
        for s in demands:assert s['hypothetical'] and s['register_bits']==32 and s['total_registers']==128*s['registers_per_thread']
        for s in states:
            if s['kind']=='residency':
                assert s['resident_blocks']==s['register_budget']//(s['block_threads']*s['registers_per_thread']) and s['resident_warps']==s['resident_blocks']*4
                assert s['hypothetical'] and s['performance_ratio'] is None
            if s['kind']=='values':assert s['thread']==2 and s['a']==3 and s['b']==4 and s['sum'] in [None,7] and not s['physical_slot_mapping']
            if s['kind']=='compiler':assert s['registers']==cuda['registers_per_thread'] and s['spill_stores']==s['spill_loads']==0 and not s['source_variables_equal_registers']
            if s['kind']=='spill':assert s['cache_hit_possible'] and not s['all_accesses_reach_dram'] and s['not_actual_vectorAdd_spill'] and s['backing']==['L1','L2','DRAM']
        assert any(s['kind']=='values' and s['stored'] and s['sum']==7 for s in states)
        moves=[s for s in states if s['kind']=='map_motion' and s['operation'] in ['load','add','store'] and 32<=s['start']<41]
        assert [(s['operation'],s['value']) for s in moves]==[('load',3),('load',4),('add',7),('store',7)]
        assert all(s['end']>s['start'] and s['end']<=41 for s in moves)
        for s in moves:
            if s['operation']=='load':assert s['route']==['L2','L1','Register'] and any(('A[i]' if s['value']==3 else 'B[i]') in code for code in s['active_code'])
            if s['operation']=='add':assert 'float sum = a + b;' in s['active_code']
            if s['operation']=='store':assert s['route']==['Register','L2'] and 'C[i] = sum;' in s['active_code']
        budgets=[s for s in states if s['kind']=='map_budget']
        assert {s['segments'] for s in budgets}=={4,8}
        for s in budgets:assert s['block_count']==s['segments'] and s['warp_count']==s['segments']*4 and s['segment_fraction']==1/s['segments']
        spills=[s for s in states if s['kind']=='map_motion' and s['operation'] in ['spill_store','spill_load']]
        assert any(s['operation']=='spill_store' for s in spills) and any(s['operation']=='spill_load' for s in spills)
        times=[19,29,37,44,53,61,67,77,82,92,100,111,122,134,140,153,163,173]
        tw,th=(216,384) if layout=='shorts' else (384,216);sheet=Image.new('RGB',(tw*4,(th+24)*math.ceil(len(times)/4)),'#0B1220');draw=ImageDraw.Draw(sheet)
        for k,t in enumerate(times):
            data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf',f'scale={tw}:{th}','-f','image2pipe','-vcodec','png','-'])
            im=Image.open(io.BytesIO(data));x=k%4*tw;y=k//4*(th+24);sheet.paste(im,(x,y));draw.text((x+5,y+th+4),f'{t}s',fill='white')
        sheet.save(ROOT/'exports'/f'gpuh06_qa_{suffix}.jpg',quality=93)
        report.append(dict(layout=layout,frames=int(stream['nb_frames']),duration=info['format']['duration'],geometry_samples=geometry_count,identity='Execution map transitions at 9s; fixed Thread 2 / SM Register memory map afterward',motion='Load3, Load4, Add7, Store7 synchronized with code; allocation width and resident counts change; Spill Store/Load packets move',memory_map='Register, Shared, L1 within SM; L2 and device DRAM outside SM; no forced serial path through Shared',CUDA='1536 outputs; Thread 2 = 3+4=7',compiled_registers=cuda['registers_per_thread'],actual_spill_bytes=0,hypothetical_register_demands=[4096,8192],local_memory='private scope; cache-hit path supported; no mandatory DRAM access'))
    dest=P/('qa_preview.json' if a.preview else 'qa_final.json')
    if a.layout!='both' and dest.exists():
        prior={r['layout']:r for r in json.loads(dest.read_text(encoding='utf-8'))};prior.update({r['layout']:r for r in report});combined=[prior[k] for k in ['shorts','longform'] if k in prior]
    else:combined=report
    dest.write_text(json.dumps(combined,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
