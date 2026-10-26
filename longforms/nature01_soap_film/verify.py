"""Independent boundary/area/force invariants and delivered-media validation."""
import json,subprocess
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
def patch_force(eps,n=4001):
    """Integral of outward surface co-normal along four patch edges, divided by gamma_eff."""
    ts=np.linspace(-np.pi/2-.42,-np.pi/2+.42,n);zs=np.linspace(-.38,.38,n)
    total=np.zeros(3)
    for z,sign in [(-.38,-1),(.38,1)]:
        r=np.cosh(z)+eps*np.cos(np.pi*z/1.6)**2
        dr=np.sinh(z)-eps*np.pi/1.6*np.sin(2*np.pi*z/1.6)
        vec=np.stack([dr*np.cos(ts),dr*np.sin(ts),np.ones_like(ts)],axis=1)/np.sqrt(1+dr*dr)
        total+=sign*r*np.trapezoid(vec,ts,axis=0)
    dr=np.sinh(zs)-eps*np.pi/1.6*np.sin(2*np.pi*zs/1.6)
    length=np.trapezoid(np.sqrt(1+dr*dr),zs)
    for t,sign in [(ts[0],-1),(ts[-1],1)]:total+=sign*length*np.array([-np.sin(t),np.cos(t),0.])
    return total
def geometry():
    d=json.loads((P/'geometry.json').read_text());assert d['stability_value']<1
    z=np.array([-.8,.8]);R=d['R']
    for b in np.linspace(0,1,11):assert np.max(np.abs(R+b*(np.cosh(z)-R)-R))<1e-12
    for eps in np.linspace(-.22,.22,45):assert np.max(np.abs(np.cosh(z)+eps*np.cos(np.pi*z/1.6)**2-R))<1e-12
    assert d['areas']['0']>d['areas']['0.5']>d['areas']['1']
    assert abs(d['first_derivative'])<1e-5
    force0=patch_force(0);force1=patch_force(.12)
    assert np.linalg.norm(force0)<1e-6,(force0,force1)
    assert np.linalg.norm(force1)>.05
    timing=json.loads((P/'timing.json').read_text(encoding='utf-8'));assert timing[0]['start']==0 and timing[-1]['end']==174
    assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'));assert sum(m['duration_seconds'] for m in manifest)==174
    out=dict(stability=d['stability_value'],area_candidates=d['areas'],area_first_derivative=d['first_derivative'],equilibrium_patch_force_over_gamma=force0.tolist(),deformed_patch_force_over_gamma=force1.tolist(),sentence_count=len(timing),duration=174)
    (P/'geometry_verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
def contact(path,layout):
    from PIL import Image,ImageDraw
    short=layout=='shorts';w,h=(180,320) if short else (320,180)
    sheet=Image.new('RGB',(w*4,(h+24)*6),'#091421');draw=ImageDraw.Draw(sheet)
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'))
    dest=P/'qa';dest.mkdir(exist_ok=True)
    for i,m in enumerate(manifest):
        t=m['start']+min(m['duration_seconds']*.65,m['duration_seconds']-.25);frame=dest/f'{layout}_{i+1:02}.png'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(path),'-frames:v','1','-vf',f'scale={w}:{h}',str(frame)],check=True)
        sheet.paste(Image.open(frame),((i%4)*w,(i//4)*(h+24)));draw.text(((i%4)*w+5,(i//4)*(h+24)+h+3),f'{i+1:02} / {t:.1f}s',fill='white')
    sheet.save(dest/f'contact_{layout}_{"preview" if "preview" in path.name else "final"}.png')
def delivery():
    from concurrent.futures import ThreadPoolExecutor
    def check(layout):
        path=P.parents[1]/'exports'/f'nature01_soap_film_174s_{layout}_final.mp4'
        info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,duration','-of','json',str(path)]))['streams']
        assert len(info)==1 and info[0]['codec_type']=='video',info
        v=info[0];assert int(v['nb_read_frames'])==5220 and v['r_frame_rate']=='30/1' and abs(float(v['duration'])-174)<.001,v
        assert (v['width'],v['height'])==((1080,1920) if layout=='shorts' else (1920,1080)),v
        return dict(layout=layout,output=str(path),**v)
    with ThreadPoolExecutor(max_workers=2) as pool:out=list(pool.map(check,['shorts','longform']))
    (P/'delivery_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
if __name__=='__main__':
    import sys
    geometry()
    if len(sys.argv)>1 and sys.argv[1]=='delivery':delivery()
    elif len(sys.argv)>1:
        kind=sys.argv[1]
        for layout in ['shorts','longform']:contact(P.parents[1]/'exports'/f'nature01_soap_film_174s_{layout}_{kind}.mp4',layout)
