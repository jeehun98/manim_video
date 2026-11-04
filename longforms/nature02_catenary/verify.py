import json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from physics import B,R,L,height,slope,integrals
P=Path(__file__).resolve().parent
def geometry():
    data=json.loads((P/'geometry.json').read_text(encoding='utf-8'));d=data['dynamics']
    for c in data['candidates']:
        assert abs(c['length']-L)<1e-10,c
        assert max(abs(c['left']-R),abs(c['right']-R))<1e-12,c
    u0=integrals(0)['energy'];assert all(c['energy']>u0 for c in data['candidates'][1:])
    assert abs(u0-(B+.5*np.sinh(2*B)))<1e-11
    sim=np.load(P/'dynamics.npz');assert d['max_endpoint_error']==0 and d['max_segment_error']<1.1e-5,d
    total_lengths=np.linalg.norm(np.diff(sim['positions'],axis=1),axis=2).sum(axis=1)
    max_length_error=float(np.max(np.abs(total_lengths-L)))
    assert max_length_error/L<1e-4
    assert d['potential_increase_steps']>0 and d['final_mechanical_energy']<d['initial_mechanical_energy']
    assert d['max_positive_mechanical_increment']<1e-7,d
    force=[]
    for x in np.linspace(-.55,.55,9):
        left=x-.1;right=x+.1
        net=np.array([-1,-np.sinh(left)])+np.array([1,np.sinh(right)])+np.array([0,-(np.sinh(right)-np.sinh(left))]);force.append(float(np.linalg.norm(net)))
    assert max(force)<1e-12
    one=json.loads((P.parent/'nature01_soap_film'/'geometry.json').read_text())
    assert abs(one['R']-R)<1e-12 and one['a']==1 and one['height']==1.6
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'));timing=json.loads((P/'timing.json').read_text(encoding='utf-8'))
    assert len(manifest)==22 and sum(m['duration_seconds'] for m in manifest)==150
    assert timing[0]['start']==0 and timing[-1]['end']==150 and all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))
    out=dict(candidate_length_errors=[c['length']-L for c in data['candidates']],candidate_energies=[c['energy'] for c in data['candidates']],equilibrium_force_residual=max(force),matching_episode01_catenoid=True,dynamics=d,dynamic_max_total_length_error=max_length_error,dynamic_max_relative_length_error=max_length_error/L,sentence_count=len(timing),duration=150)
    (P/'geometry_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
def delivery():
    def check(layout):
        path=P.parents[1]/'exports'/f'nature02_catenary_150s_{layout}_final.mp4'
        streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,duration','-of','json',str(path)]))['streams'];assert len(streams)==1
        v=streams[0];assert v['codec_type']=='video' and int(v['nb_read_frames'])==4500 and v['r_frame_rate']=='30/1' and abs(float(v['duration'])-150)<.001,v
        assert (v['width'],v['height'])==((1080,1920) if layout=='shorts' else (1920,1080))
        return dict(layout=layout,output=str(path),**v)
    with ThreadPoolExecutor(max_workers=2) as pool:out=list(pool.map(check,['shorts','longform']))
    (P/'delivery_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
def contact(kind,layout):
    from PIL import Image,ImageDraw
    source=P.parents[1]/'exports'/f'nature02_catenary_150s_{layout}_{kind}.mp4';w,h=(180,320) if layout=='shorts' else (320,180)
    sheet=Image.new('RGB',(w*4,(h+24)*6),'#091421');draw=ImageDraw.Draw(sheet);dest=P/'qa';dest.mkdir(exist_ok=True)
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'))
    for i,m in enumerate(manifest):
        t=m['start']+.65*m['duration_seconds'];img=dest/f'{layout}_{i+1:02}.png'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(source),'-frames:v','1','-vf',f'scale={w}:{h}',str(img)],check=True)
        sheet.paste(Image.open(img),((i%4)*w,(i//4)*(h+24)));draw.text(((i%4)*w+5,(i//4)*(h+24)+h+3),f'{i+1:02} / {t:.1f}s',fill='white')
    sheet.save(dest/f'contact_{layout}_{kind}.png')
if __name__=='__main__':
    import sys
    geometry()
    if len(sys.argv)>1 and sys.argv[1]=='delivery':delivery()
    elif len(sys.argv)>1:
        for layout in ['shorts','longform']:contact(sys.argv[1],layout)
