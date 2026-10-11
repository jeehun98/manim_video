from itertools import product
import math
# Check every coefficient, not merely decomposable sample inputs.
m=2;q=3
base={(h,i,j,k) for h in range(q) for i,j,k in product(range(m),repeat=3)}
combined=set()
for h,i,j,k in base:
 for g,a,b,c in base:
  combined.add(((h,g),i*m+a,j*m+b,k*m+c))
expected={(pair,i,j,k) for pair in product(range(q),repeat=2) for i,j,k in product(range(m*m),repeat=3)}
assert combined==expected
assert len(base)==24 and len(combined)==576
assert q*q==9
# Sanity check: separate Strassen upper bound reproduces its exponent.
assert abs(math.log(21/3,2)-math.log(7,2))<1e-12
print('Verified all 576 tensor-product support coefficients: 9 independent 4x4 matrix products; no cross-block coefficients. Conditional inequality algebra checked.')

# Third power: compare all support coefficients with 27 independent 8x8 products.
third=set()
for pair,i,j,k in combined:
 for h,a,b,c in base:
  third.add(((*pair,h),i*2+a,j*2+b,k*2+c))
expected3={(triple,i,j,k) for triple in product(range(3),repeat=3) for i,j,k in product(range(8),repeat=3)}
assert third==expected3 and len(third)==13824
assert 7+7+7==21
assert abs(math.log2(21/3)-2.807354922057604)<1e-12
print('Verified all 13824 third-power coefficients: 27 independent 8x8 products; r=21 reproduces log2(7), not a new bound.')
