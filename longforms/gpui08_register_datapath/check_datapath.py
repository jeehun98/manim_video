"""Four-bit register, non-destructive read, independent selectors, edge-enabled write."""
import json,itertools
from pathlib import Path
def bits(n):assert 0<=n<16;return tuple((n>>i)&1 for i in [3,2,1,0])
def integer(bs):return sum(b<<i for b,i in zip(bs,[3,2,1,0]))
def mux(a,b,sel):assert sel in [0,1];return [a,b][sel]
def write(regs,dest,value,we,rising):
 assert 0<=dest<len(regs) and 0<=value<16
 out=list(regs)
 if we and rising:out[dest]=value
 return tuple(out)
def compute(regs,ra,rb):return (regs[ra]+regs[rb])&15
def main():
 for n in range(16):assert integer(bits(n))==n
 for a,b,s in itertools.product(range(16),range(16),range(2)):assert mux(a,b,s)==(a if s==0 else b)
 cases=0
 for dest,value,we,edge in itertools.product(range(3),range(16),range(2),range(2)):
  before=(5,3,8);out=write(before,dest,value,we,edge)
  for i in range(3):assert out[i]==(value if i==dest and we and edge else before[i])
  cases+=1
 regs=(5,3,0);result=compute(regs,0,1);assert result==8 and regs==(5,3,0)
 regs=write(regs,2,result,1,1);assert regs==(5,3,8)
 assert mux(5,regs[2],0)+3==8 and mux(5,regs[2],1)+2==10
 assert write(regs,2,10,0,1)==regs
 # All pairs of independent read selectors retain every stored value.
 for regs in itertools.product(range(16),repeat=3):
  before=regs
  for a,b in itertools.product(range(3),repeat=2):assert compute(regs,a,b)==(regs[a]+regs[b])&15 and regs==before
 p=Path(__file__).parent/'qa';p.mkdir(exist_ok=True)
 (p/'datapath_verification.json').write_text(json.dumps(dict(register_values=16,mux_cases=512,write_cases=cases,read_cases=36864,read_is_non_destructive=True,write_requires_enable_and_edge=True,examples={'5':'0101','3':'0011','8':'1000','10':'1010'},sequence=[8,10],all_passed=True),indent=2),encoding='utf-8')
 print('PASS16 four-bit values,512 MUX cases,192 write cases,36864 non-destructive independent read pairs')
if __name__=='__main__':main()
