import json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from physics import A,B,V1,V2,N1,N2,STAR,STRAIGHT,TMIN,DIR1,DIR2,SLOW1,SLOW2,OMEGA,time,derivative,second,metrics,front_segments,phasors,ray_exit
P=Path(__file__).resolve().parent
def geometry():
    actual=metrics(STAR);straight=metrics(STRAIGHT)
    assert actual['distance']>straight['distance'] and actual['time']<straight['time']
    assert abs(derivative(STAR))<1e-12 and min(second(x) for x in np.linspace(-10,10,101))>0
    h=1e-5;finite=(time(STAR+h)-time(STAR-h))/(2*h);assert abs(finite)<1e-7
    assert abs(N1*DIR1[0]-N2*DIR2[0])<1e-12
    assert abs(SLOW1[0]-SLOW2[0])<1e-12
    assert abs(np.linalg.norm(SLOW1)*V1-1)<1e-12 and abs(np.linalg.norm(SLOW2)*V2-1)<1e-12
    direction=ray_exit(STAR)-np.array([STAR,0]);towardB=B-np.array([STAR,0]);assert abs(np.linalg.det(np.array([direction,towardB])))<1e-12
    normals=[];level_errors=[];boundary=[]
    for tau in np.linspace(-3,3,101):
        crossing=[]
        for j,p,q in front_segments(tau):
            s=SLOW1 if j==0 else SLOW2
            normals.append(abs(float(np.dot(q-p,s))))
            for v in [p,q]:
                level_errors.append(abs(float(np.dot(v-np.array([STAR,0]),s)-tau)))
                if abs(v[1])<1e-10:crossing.append(v[0])
        if len(crossing)>1:boundary.append(abs(crossing[0]-crossing[1]))
    assert max(normals)<1e-12 and max(level_errors)<1e-12 and max(boundary)<1e-12
    xo,zo=phasors(-.5);xn,zn=phasors(STAR)
    assert abs(zo.mean())<.05 and abs(zn.mean())>.95 and abs(zo.mean())>0
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'));timing=json.loads((P/'timing.json').read_text(encoding='utf-8'))
    assert len(manifest)==22 and sum(m['duration_seconds'] for m in manifest)==149
    assert timing[0]['start']==0 and timing[-1]['end']==149 and all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))
    out=dict(actual=actual,straight=straight,time_first_derivative=float(derivative(STAR)),time_first_derivative_finite_difference=float(finite),time_second_derivative=float(second(STAR)),snell_residual=float(N1*DIR1[0]-N2*DIR2[0]),phase_tangential_slowness_residual=float(SLOW1[0]-SLOW2[0]),wavefront_normal_residual=max(normals),phase_level_residual=max(level_errors),wavefront_boundary_gap=max(boundary),off_stationary_normalized_sum=float(abs(zo.mean())),near_stationary_normalized_sum=float(abs(zn.mean())),equal_sample_count=len(zo),same_frequency=OMEGA,sentence_count=len(timing),duration=149)
    (P/'geometry_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
def delivery():
    def check(layout):
        source=P.parents[1]/'exports'/f'nature03_refraction_149s_{layout}_final.mp4'
        streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,duration','-of','json',str(source)]))['streams'];assert len(streams)==1
        v=streams[0];assert v['codec_type']=='video' and int(v['nb_read_frames'])==4470 and v['r_frame_rate']=='30/1' and abs(float(v['duration'])-149)<.001,v
        assert (v['width'],v['height'])==((1080,1920) if layout=='shorts' else (1920,1080))
        return dict(layout=layout,output=str(source),**v)
    with ThreadPoolExecutor(max_workers=2) as pool:out=list(pool.map(check,['shorts','longform']))
    (P/'delivery_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
def contact(kind,layout):
    from PIL import Image,ImageDraw
    source=P.parents[1]/'exports'/f'nature03_refraction_149s_{layout}_{kind}.mp4';w,h=(180,320) if layout=='shorts' else (320,180)
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
