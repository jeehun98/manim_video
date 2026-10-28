"""One shared geometry for rays, travel times, phase planes and phasors."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
P=Path(__file__).resolve().parent
A=np.array([-2.4,1.4]);B=np.array([2.4,-1.1]);V1=1.;V2=.75;N1=1.;N2=1/V2
def times(x):
    x=np.asarray(x);return np.hypot(x-A[0],A[1])/V1,np.hypot(x-B[0],B[1])/V2
def time(x):
    a,b=times(x);return a+b
def derivative(x):
    return (x-A[0])/(V1*np.hypot(x-A[0],A[1]))+(x-B[0])/(V2*np.hypot(x-B[0],B[1]))
def second(x):return A[1]**2/(V1*((x-A[0])**2+A[1]**2)**1.5)+B[1]**2/(V2*((x-B[0])**2+B[1]**2)**1.5)
STAR=float(brentq(derivative,A[0],B[0],xtol=1e-14));STRAIGHT=float((A[0]*(-B[1])+B[0]*A[1])/(A[1]-B[1]));TMIN=float(time(STAR))
DIR1=(np.array([STAR,0.])-A);DIR1/=np.linalg.norm(DIR1)
DIR2=(B-np.array([STAR,0.]));DIR2/=np.linalg.norm(DIR2)
SLOW1=DIR1/V1;SLOW2=DIR2/V2
OMEGA=120.;WINDOW=.16;COUNT=9
def phasors(center):
    xs=np.linspace(center-WINDOW,center+WINDOW,COUNT);phase=OMEGA*(time(xs)-TMIN)
    return xs,np.exp(1j*phase)
def metrics(x):
    t1,t2=times(x);return dict(x=float(x),d_air=float(t1*V1),d_water=float(t2*V2),distance=float(t1*V1+t2*V2),t_air=float(t1),t_water=float(t2),time=float(t1+t2))
def front_segments(level,bounds=(-3.2,3.2,-1.7,1.8)):
    """Intersect s_x (x-STAR)+s_y y=level with each medium's rectangle."""
    xmin,xmax,ymin,ymax=bounds;result=[]
    for medium,(lo,hi,s) in enumerate([(0,ymax,SLOW1),(ymin,0,SLOW2)]):
        pts=[]
        for y in [lo,hi]:
            x=STAR+(level-s[1]*y)/s[0]
            if xmin-1e-10<=x<=xmax+1e-10:pts.append([x,y])
        for x in [xmin,xmax]:
            y=(level-s[0]*(x-STAR))/s[1]
            if lo-1e-10<=y<=hi+1e-10:pts.append([x,y])
        unique=[]
        for p in pts:
            if not any(np.linalg.norm(np.array(p)-q)<1e-8 for q in unique):unique.append(np.array(p))
        if len(unique)>=2:result.append((medium,unique[0],unique[1]))
    return result
def ray_exit(x,y=-1.55):
    inc=np.array([x,0.])-A;inc/=np.linalg.norm(inc)
    sin2=V2/V1*inc[0];d2=np.array([sin2,-np.sqrt(1-sin2*sin2)])
    return np.array([x,0.])+(-y/(-d2[1]))*d2
def main():
    def phase_data(c):
        x,z=phasors(c);return dict(center=float(c),xs=x.tolist(),phases=(OMEGA*(time(x)-TMIN)).tolist(),normalized_sum=float(abs(z.mean())))
    data=dict(A=A.tolist(),B=B.tolist(),v_air=V1,v_water=V2,n_air=N1,n_water=N2,actual=metrics(STAR),straight=metrics(STRAIGHT),derivative_at_actual=float(derivative(STAR)),second_derivative_at_actual=float(second(STAR)),angle_air=float(np.degrees(np.arctan2(DIR1[0],-DIR1[1]))),angle_water=float(np.degrees(np.arctan2(DIR2[0],-DIR2[1]))),slowness_air=SLOW1.tolist(),slowness_water=SLOW2.tolist(),omega=OMEGA,phase_window=WINDOW,off_stationary=phase_data(-.5),near_stationary=phase_data(STAR),assumptions='Stationary isotropic homogeneous nondispersive media; monochromatic phase model; reflection/amplitude factors omitted in the visualization; equal-weight phasors are explanatory, not a complete field integral.')
    (P/'geometry.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(data,indent=2))
if __name__=='__main__':main()
