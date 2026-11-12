"""Quadrature checks of the exact displayed state, operator and basis transformation."""
from pathlib import Path
import sys,json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from quantum_series.shared.representations import C,H,basis,wave,energy_action,unitary,transformed
HERE=Path(__file__).resolve().parent
def main():
 x=np.linspace(0,1,40001);phi=basis(x);gram=np.array([[np.trapezoid(phi[:,i]*phi[:,j],x) for j in range(3)] for i in range(3)])
 norm=float(np.trapezoid(abs(wave(x))**2,x));second=np.gradient(np.gradient(wave(x),x,edge_order=2),x,edge_order=2);direct=float(np.trapezoid(np.conj(wave(x))*(-second/np.pi**2),x).real);matrix=float((C.conj()@H@C).real)
 assert np.max(abs(gram-np.eye(3)))<1e-12 and abs(norm-1)<1e-12 and abs(direct-3.5)<1e-6 and abs(matrix-direct)<1e-6
 checks=[]
 for theta in [0,np.pi/6,.9]:
  u=unitary(theta);cp,hp=transformed(theta);reconstructed=(phi@u)@cp
  error=float(np.max(abs(wave(x)-reconstructed)));value=float((cp.conj()@hp@cp).real)
  assert error<1e-12 and abs(value-3.5)<1e-12 and np.max(abs(u.conj().T@u-np.eye(3)))<1e-12
  assert np.max(abs(np.linalg.eigvalsh(hp)-[1,4,9]))<1e-12
  checks.append({'angle':theta,'coefficients':cp.tolist(),'energy_matrix':hp.tolist(),'expectation':value,'wave_reconstruction_max_error':error})
 report={'gram_matrix':gram.tolist(),'normalization':norm,'energy_direct':direct,'energy_matrix':matrix,'unitary_checks':checks}
 (HERE/'physics_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('PASS: orthonormal basis, normalized state, operator expectation and basis invariance')
if __name__=='__main__':main()
