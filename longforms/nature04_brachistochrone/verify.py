import json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from scipy.integrate import quad
from physics import *
P=Path(__file__).resolve().parent

def geometry_check():
    assert np.linalg.norm(cycle(THETA)-[X,Y])<1e-10
    assert TC<TS<TD
    assert abs(quad(integrand,0,1)[0]-TD)<1e-10
    errors=[];snell=[]
    yy=np.linspace(0,Y,101)
    exact=np.array([light(y)[0] for y in yy])
    for n in [6,12,24,48]:
        pts,p,v=layers(n)
        assert np.linalg.norm(pts[-1]-[X,Y])<1e-8
        diff=np.diff(pts,axis=0);sin=diff[:,0]/np.linalg.norm(diff,axis=1)
        snell.append(float(np.max(abs(sin/v-p))))
        errors.append(float(max(abs(np.interp(yy,pts[:,1],pts[:,0])-exact))))
    assert all(b<a for a,b in zip(errors,errors[1:]))
    light_error=max(np.linalg.norm(light(cycle(t)[1])-cycle(t)) for t in np.linspace(0,THETA,81))
    assert light_error<1e-8 and max(snell)<1e-12
    dt=1e-5
    for k in ['cycle','straight','deep']:
        for t in np.linspace(.1,{'cycle':TC,'straight':TS,'deep':TD}[k]-.1,31):
            v=np.linalg.norm((pos(k,t+dt)-pos(k,t-dt))/(2*dt))
            assert abs(v*v-2*G*pos(k,t)[1])<.003,(k,t,v)
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'));timing=json.loads((P/'timing.json').read_text(encoding='utf-8'))
    assert len(manifest)==26 and sum(m['duration_seconds'] for m in manifest)==165
    assert len(timing)==38 and timing[-1]['end']==165
    assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))
    out=dict(**metrics(),layer_max_x_errors=errors,snell_residuals=snell,independent_light_error=float(light_error),sentence_count=38,scene_count=26,duration=165)
    (P/'geometry_verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))

def delivery():
    def check(layout):
        source=P.parents[1]/'exports'/f'nature04_brachistochrone_165s_{layout}_final.mp4'
        streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,duration','-of','json',str(source)]))['streams'];assert len(streams)==1
        v=streams[0];assert v['codec_type']=='video' and int(v['nb_read_frames'])==4950 and v['r_frame_rate']=='30/1' and abs(float(v['duration'])-165)<.001,v
        assert (v['width'],v['height'])==((1080,1920) if layout=='shorts' else (1920,1080))
        return dict(layout=layout,output=str(source),**v)
    with ThreadPoolExecutor(max_workers=2) as pool:out=list(pool.map(check,['shorts','longform']))
    (P/'delivery_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
def contact(kind,layout):
    from PIL import Image,ImageDraw
    source=P.parents[1]/'exports'/f'nature04_brachistochrone_165s_{layout}_{kind}.mp4';w,h=(180,320) if layout=='shorts' else (320,180)
    sheet=Image.new('RGB',(w*4,(h+24)*7),'#091421');draw=ImageDraw.Draw(sheet);dest=P/'qa';dest.mkdir(exist_ok=True)
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'))
    for i,m in enumerate(manifest):
        t=m['start']+.65*m['duration_seconds'];img=dest/f'{layout}_{i+1:02}.png'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(source),'-frames:v','1','-vf',f'scale={w}:{h}',str(img)],check=True)
        sheet.paste(Image.open(img),((i%4)*w,(i//4)*(h+24)));draw.text(((i%4)*w+5,(i//4)*(h+24)+h+3),f'{i+1:02} / {t:.1f}s',fill='white')
    sheet.save(dest/f'contact_{layout}_{kind}.png')
if __name__=='__main__':
    import sys
    geometry_check()
    if len(sys.argv)>1 and sys.argv[1]=='delivery':delivery()
    elif len(sys.argv)>1:
        for layout in ['shorts','longform']:contact(sys.argv[1],layout)
