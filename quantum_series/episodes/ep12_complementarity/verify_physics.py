"""Numerical checks independent of the drawing code."""
import sys,json
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from quantum_series.shared.complementarity import amplitudes,probability,marker_overlap,samples,envelope
HERE=Path(__file__).resolve().parent
def main():
 x=np.linspace(-3,3,60001);dx=x[1]-x[0];a,b=amplitudes(x);inner=np.trapezoid(np.conj(a)*b,x);assert abs(inner)<1e-12
 checks=[]
 for d in [0,.3,.6,.85,1]:
  gamma=marker_overlap(d);pdf=probability(x,gamma);joint=a[:,None]*np.array([1,0])+b[:,None]*np.array([gamma,d]);reduced=abs(joint[:,0])**2+abs(joint[:,1])**2
  norm=float(np.trapezoid(pdf,x));assert abs(norm-1)<1e-12 and pdf.min()>-1e-14
  error=float(np.max(abs(pdf-reduced)));assert error<1e-12 and abs(d*d+gamma*gamma-1)<1e-12
  checks.append({'D':d,'V':float(gamma),'normalization':norm,'partial_trace_max_error':error})
 assert np.max(abs(probability(x,0)-envelope(x)))<1e-12
 sample_checks=[]
 for d in [0,1]:
  pts=samples(d);assert pts.shape==(2000,3) and np.all(abs(pts[:,0])<=3)
  hist,edges=np.histogram(pts[:,0],bins=30,range=(-3,3));expected=[]
  for lo,hi in zip(edges[:-1],edges[1:]):
   grid=np.linspace(lo,hi,101);expected.append(np.trapezoid(probability(grid,marker_overlap(d)),grid))
  total_variation=float(abs(hist/2000-np.array(expected)).sum()/2);assert total_variation<.09
  sample_checks.append({'D':d,'count':len(pts),'empirical_total_variation_30bins':total_variation})
 report={'path_overlap':{'real':float(inner.real),'imag':float(inner.imag)},'marker_checks':checks,'samples':sample_checks,'record_first_two':samples(1)[:2,2].tolist()}
 (HERE/'physics_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('PASS: normalization, marker partial trace, duality and 2000-event samples')
if __name__=='__main__':main()
