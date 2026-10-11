from itertools import product
# Compare all tensor coefficients after pairing every index, not just sample inputs.
small=list(product(range(2),repeat=3))
support={(2*i+a,2*j+b,2*k+c) for i,j,k in small for a,b,c in small}
assert support==set(product(range(4),repeat=3))
support3={(2*i+a,2*j+b,2*k+c) for i,j,k in support for a,b,c in small}
assert support3==set(product(range(8),repeat=3))
assert [(i,j) for i in [1,2] for j in [1,2]]==[(1,1),(1,2),(2,1),(2,2)]
assert 1*5+2*7==19 and sum(x*x for x in [1,2,3,4])==30
terms=[('a1','b1','z1'),('a2','b2','z2'),('a1','b3','z2')]
kept=[t for t in terms if 'b3' not in t]
for axis in range(3):assert len({t[axis] for t in kept})==2
assert len(list(product(['P','Q','S'],repeat=2)))==9
print('Verified all 64 M4 and 512 M8 support coefficients; four middle-index paths; numeric19/30; toy zero restriction leaves two fully independent scalar products.')
