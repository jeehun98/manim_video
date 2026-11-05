"""Normal-incidence, equally spaced surface-row phase-sum model."""
import numpy as np
def normalized_amplitude(angle_degrees,wavelength=.165,spacing=.215,count=8):
 delta=spacing*np.sin(np.deg2rad(angle_degrees))
 return float(abs(sum(np.exp(2j*np.pi*n*delta/wavelength) for n in range(count)))/count)
def electron_wavelength_nm(voltage):
 return 6.62607015e-34/np.sqrt(2*9.1093837139e-31*1.602176634e-19*voltage)*1e9
