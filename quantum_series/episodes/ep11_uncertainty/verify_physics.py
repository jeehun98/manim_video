"""Independent numerical normalization/Fourier-moment checks for the animation."""
import sys,json
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from quantum_series.shared.uncertainty import psi,density,momentum_std,component_sum,free_psi
HERE=Path(__file__).resolve().parent

def main():
 n=16384;dx=.005;x=(np.arange(n)-n//2)*dx;k=2*np.pi*np.fft.fftshift(np.fft.fftfreq(n,d=dx));dk=k[1]-k[0];rows=[]
 for sx in [.43,.5,.7,1.2]:
  wave=psi(x,sx);rho=abs(wave)**2
  phi=np.fft.fftshift(np.fft.fft(np.fft.ifftshift(wave)))*dx/np.sqrt(2*np.pi);pk=abs(phi)**2
  normx=rho.sum()*dx;normp=pk.sum()*dk;meanx=(x*rho).sum()*dx;meanp=(k*pk).sum()*dk
  stdx=np.sqrt(((x-meanx)**2*rho).sum()*dx);stdp=np.sqrt(((k-meanp)**2*pk).sum()*dk)
  assert abs(normx-1)<1e-10 and abs(normp-1)<1e-10
  assert abs(stdx-sx)<1e-10 and abs(stdp-momentum_std(sx))<1e-10 and abs(meanp-6)<1e-10
  rows.append({'sigma_x':float(stdx),'sigma_p_fft':float(stdp),'normalization_x':float(normx),'normalization_p':float(normp),'product':float(stdx*stdp)})
 q=np.linspace(-3,3,601);error=float(np.max(abs(component_sum(q)-psi(q,.7))));assert error<1e-9
 evolved=abs(free_psi(x,.9))**2;norm=evolved.sum()*dx;mean=(x*evolved).sum()*dx;std=np.sqrt(((x-mean)**2*evolved).sum()*dx)
 expected=.65*np.sqrt(1+(.9/(2*.65**2))**2)
 assert abs(norm-1)<1e-10 and abs(mean-1.08)<1e-10 and abs(std-expected)<1e-10
 report={'gaussian_fft_checks':rows,'component_sum_max_complex_error':error,'free_evolution':{'normalization':float(norm),'mean':float(mean),'sigma':float(std),'analytic_sigma':expected}}
 (HERE/'physics_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('PASS: normalization, FFT widths, component sum, free evolution')
if __name__=='__main__':main()
