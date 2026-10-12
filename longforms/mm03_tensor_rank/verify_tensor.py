"""Verify the bilinear identity coefficient by coefficient, not by sampling."""
from tensor_data import *
assert np.array_equal(TERMS.sum(axis=0),TARGET)
assert PRODUCTS.tolist()==[65,35,-2,8,24,22,-30]
assert (PRODUCTS@W).tolist()==[19,22,43,50]
assert (PRODUCTS[0]*W[0]).tolist()==[65,0,0,65]
assert np.einsum('ijk,i,j->k',TARGET,X,Y).tolist()==[19,22,43,50]
print('All 64 coefficients agree: standard 8 terms = Strassen 7 terms.')
print('M1 contribution [65,0,0,65]; total output [19,22,43,50].')
print('This checks rank <= 7, not the independent rank >= 7 theorem.')

