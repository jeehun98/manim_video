"""Phase and de Broglie relations, independent of rendering."""
import numpy as np
H=6.62607015e-34
HBAR=H/(2*np.pi)
def wavelength(momentum):
 if momentum<=0:raise ValueError('Positive momentum required')
 return H/momentum
def phase(cycles,u):return np.exp(2j*np.pi*cycles*np.asarray(u))
def is_phase_matched(cycles,tolerance=1e-9):return abs(phase(cycles,1)-phase(cycles,0))<tolerance
def angular_momentum(cycles):return cycles*HBAR
