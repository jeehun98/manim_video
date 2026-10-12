from itertools import product
import sympy as s
e=s.symbols('epsilon',nonzero=True);a,b,c,d=s.symbols('a b c d')
assert s.expand(((a+e*b)*(c+e*d)-a*c)/e-(a*d+b*c+e*b*d))==0
coeff={i:s.expand(e**sum(i)/e-(1/e if i==(0,0,0) else 0)) for i in product(range(2),repeat=3)}
W={i:int(sum(i)==1) for i in coeff}
assert all(s.limit(v,e,0)==W[i] for i,v in coeff.items())
assert all(s.expand(3*v.subs(e,1)-3*v.subs(e,2)+v.subs(e,3))==W[i] for i,v in coeff.items())
x,y=s.symbols('alpha beta');S1=s.Matrix([[0,1],[1,0]]);S2=s.Matrix([[1,0],[0,0]])
assert (x*S1+y*S2).det()==-x*x
assert s.Matrix([[0,1,1,0],[1,0,0,0]]).rank()==2
# Rank 2 would force the 2D slice space to contain two independent rank-one matrices;
# det=-alpha^2 permits only one rank-one direction. Thus R(W)>=3.
# Flattening rank 2 gives border rank >=2, and displayed degeneration gives <=2.
num=[(5+i,6+5*i+i*i) for i in [1,2,3]]
assert tuple(3*num[0][j]-3*num[1][j]+num[2][j] for j in range(2))==(5,6)
# For k=2 confirm interpolation of degree 4 coefficient products exactly.
for i,j in product(coeff,repeat=2):
 f=s.expand(coeff[i]*coeff[j]);poly=s.interpolate([(n,f.subs(e,n)) for n in range(1,6)],e)
 assert s.expand(poly).subs(e,0)==W[i]*W[j]
print('Verified: all 8 W coefficients; exact interpolation; numeric outputs (5,6); rank and border-rank lower-bound criteria; 64 coefficients at k=2.')

# Geometric projection shown in v2: components 211 and 221.
assert s.expand(e**sum((1,0,0)))==e
assert s.expand(e**sum((1,1,0)))==e**2
assert coeff[(1,0,0)]==1 and coeff[(1,1,0)]==e
print("Verified v2 projection: S(t) -> (t,t²); normalized difference -> (1,t).")
