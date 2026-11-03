import json
from pathlib import Path
def half(a,b):return a^b,a&b
def full(a,b,c):
 x,g=half(a,b);s,h=half(x,c);return s,g|h
def ripple(a,b,c=0,n=4):
 carry=[c];s=0
 for i in range(n):
  q,c=full((a>>i)&1,(b>>i)&1,c);s|=q<<i;carry.append(c)
 return s|(c<<n),carry
def lookahead(a,b,c=0,n=4):
 g=[((a>>i)&1)&((b>>i)&1) for i in range(n)];p=[((a>>i)&1)^((b>>i)&1) for i in range(n)];cs=[c]
 for k in range(1,n+1):
  value=0
  for j in range(k):
   term=g[j]
   for l in range(j+1,k):term&=p[l]
   value|=term
  term=c
  for l in range(k):term&=p[l]
  cs.append(value|term)
 s=sum((p[i]^cs[i])<<i for i in range(n))|(cs[-1]<<n)
 return s,cs
def main():
 for a in range(2):
  for b in range(2):
   s,c=half(a,b);assert s+2*c==a+b
   for q in range(2):
    s,c=full(a,b,q);assert s+2*c==a+b+q
 for a in range(16):
  for b in range(16):
   for c in range(2):assert ripple(a,b,c)==lookahead(a,b,c) and ripple(a,b,c)[0]==a+b+c
 assert ripple(3,1)[0]==4 and ripple(15,1)[0]==16
 p=Path(__file__).parent/'qa';p.mkdir(exist_ok=True)
 (p/'arithmetic_verification.json').write_text(json.dumps(dict(half_adder_cases=4,full_adder_cases=8,four_bit_cases=512,matching_sum_and_every_carry=True,examples=['11+01=100','1111+0001=10000']),indent=2))
 print('PASS: half 4, full 8, ripple/CLA 512 input combinations and every carry')
if __name__=='__main__':main()
