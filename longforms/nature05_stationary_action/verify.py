import json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from scipy.integrate import quad
from physics import *
P=Path(__file__).resolve().parent

def geometry_check():
    times=np.linspace(0,DURATION,101)
    assert max(abs(sum(energy(times))-3))<1e-12
    assert min(lagrangian(times))<0<max(lagrangian(times))
    action_errors=[];variation_errors=[]
    for eps in np.linspace(-1,1,21):
        assert max(abs(q(0,eps)-q(0)))<1e-12
        assert max(abs(q(4,eps)-q(4)))<1e-12
        for vertical in [False,True]:action_errors.append(abs(action(eps,vertical)-exact_action(eps,vertical)))
        variation_errors.append(abs(first_variation(eps)-2*COEFF*eps))
    assert max(action_errors)<1e-11 and max(variation_errors)<1e-11
    assert abs(S0+8/3)<1e-11 and abs(SY0+14/3)<1e-11
    assert abs(S0-SY0-.5*M*VX**2*DURATION)<1e-12
    # Independent quadrature: signed positive and negative contributions.
    roots=[0,2-np.sqrt(2),2+np.sqrt(2),4]
    areas=[quad(lambda t:lagrangian(t),a,b)[0] for a,b in zip(roots,roots[1:])]
    assert areas[0]>0 and areas[1]<0 and areas[2]>0 and abs(sum(areas)-S0)<1e-12
    ivp_error=float(np.max(np.abs(newton(times)-q(times))))
    bvp_error=float(np.max(np.abs(variational(times)-q(times))))
    assert max(ivp_error,bvp_error)<1e-10
    initial_velocity_error=abs(EL(0,1)-VY)
    assert initial_velocity_error<1e-10
    for k in range(1,8):
        f=lambda t:np.sin(k*np.pi*t/4)
        df=lambda t:k*np.pi/4*np.cos(k*np.pi*t/4)
        residual=quad(lambda t:M*vy(t)*df(t)-M*G*f(t),0,4)[0]
        assert abs(residual)<1e-11
    rng=np.random.default_rng(5);discrete_gradient=[]
    for i in range(1,len(GRID)-1):discrete_gradient.append(M*(2*Y_EL[i]-Y_EL[i-1]-Y_EL[i+1])/DT-M*G*DT)
    assert max(abs(np.array(discrete_gradient)))<1e-10
    xx,yy=retimed_q(times)
    assert max(abs(yy-(Y0+VY*(xx/VX)-.5*G*(xx/VX)**2)))<1e-12
    assert max(abs(retimed_q(times)[1]-q(times)[1]))>.4
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'));timing=json.loads((P/'timing.json').read_text(encoding='utf-8'))
    assert len(manifest)==27 and sum(m['duration_seconds'] for m in manifest)==162
    assert len(timing)==38 and timing[0]['start']==0 and timing[-1]['end']==162
    assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))
    assert all(a['end']==b['start'] for a,b in zip(manifest,manifest[1:]))
    out=dict(**metrics(),action_quadrature_max_error=float(max(action_errors)),first_variation_max_error=float(max(variation_errors)),signed_integral_parts=areas,newton_max_error=ivp_error,variational_max_error=bvp_error,variational_initial_velocity_error=float(initial_velocity_error),discrete_stationarity_residual=float(max(abs(np.array(discrete_gradient)))),sentence_count=38,scene_count=27,duration=162)
    (P/'geometry_verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))

def delivery():
    def check(layout):
        source=P.parents[1]/'exports'/f'nature05_stationary_action_162s_{layout}_final.mp4'
        streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,duration','-of','json',str(source)]))['streams'];assert len(streams)==1
        v=streams[0];assert v['codec_type']=='video' and int(v['nb_read_frames'])==4860 and v['r_frame_rate']=='30/1' and abs(float(v['duration'])-162)<.001,v
        assert (v['width'],v['height'])==((1080,1920) if layout=='shorts' else (1920,1080))
        return dict(layout=layout,output=str(source),**v)
    with ThreadPoolExecutor(max_workers=2) as pool:out=list(pool.map(check,['shorts','longform']))
    (P/'delivery_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
def contact(kind,layout):
    from PIL import Image,ImageDraw
    source=P.parents[1]/'exports'/f'nature05_stationary_action_162s_{layout}_{kind}.mp4';w,h=(180,320) if layout=='shorts' else (320,180)
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
