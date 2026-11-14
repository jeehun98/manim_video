from pathlib import Path
import json,hashlib
import numpy as np
from model import C,TAU,OMEGA,RAW,FREQ,AMP,response,mixture,numerical_example,matrices
def validate(here):
 here=Path(here);stamp=hashlib.sha256((here/'model.py').read_bytes()+Path(__file__).read_bytes()).hexdigest()
 report=here/'math_checks.json'
 if report.exists() and json.loads(report.read_text()).get('source_sha256')==stamp:return
 avg=np.convolve(RAW,np.ones(3)/3,mode='valid');assert np.allclose(avg,[(RAW[i-1]+RAW[i]+RAW[i+1])/3 for i in range(1,len(RAW)-1)])
 times=np.linspace(-2,2,201)
 assert np.allclose(np.exp(1j*OMEGA*(times-TAU)),np.exp(1j*OMEGA*times)*np.exp(-1j*OMEGA*TAU))
 direct=sum(c*np.exp(1j*OMEGA*(times-k*TAU)) for k,c in enumerate(C));assert np.allclose(direct,response(OMEGA)*np.exp(1j*OMEGA*times))
 t,f,g,y,via=numerical_example();error=float(np.max(np.abs(y-via)));assert error<1e-12
 errors=[]
 for n in [6,24]:
  matrix,W,D=matrices(n);errors.append(float(np.max(np.abs(W@matrix@np.linalg.inv(W)-D))))
 assert max(errors)<1e-12
 assert np.isclose(np.angle(np.exp(-1j*OMEGA*TAU)),-np.pi/4)
 gains=[float(abs(response(2*np.pi*f))) for f in FREQ];assert gains[0]>gains[1]>gains[2]
 assert all(np.isclose(np.fft.fft(g)[int(f)],response(2*np.pi*f)) for f in FREQ)
 report.write_text(json.dumps(dict(source_sha256=stamp,moving_average='valid samples exact',delay_phase_radians=float(-OMEGA*TAU),eigenfunction_error=float(np.max(np.abs(direct-response(OMEGA)*np.exp(1j*OMEGA*times)))),fft_error=error,diagonalization_error=max(errors),gains=gains,boundaries='valid average; zero-extended general example; periodic DFT explicitly distinguished'),indent=2),encoding='utf-8')
if __name__=='__main__':validate(Path(__file__).resolve().parent)
