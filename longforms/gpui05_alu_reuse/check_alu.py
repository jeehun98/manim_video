"""Executable circuit model shared by the animation and exhaustive arithmetic checks."""
import json
from pathlib import Path
def addsub(a,b,sub,n=4):
 mask=(1<<n)-1;bb=b^(mask if sub else 0);wide=a+bb+sub;r=wide&mask
 v=int(bool(((a^b) if sub else ~(a^b))&(a^r)&(1<<(n-1))))
 return dict(result=r,carry=wide>>n,b_input=bb,cin=sub,z=int(r==0),negative=(r>>(n-1))&1,overflow=v)
def signed(x,n=4):return x-(1<<n) if x&(1<<(n-1)) else x
def comparisons(a,b):
 f=addsub(a,b,1);return dict(eq=f['z'],unsigned_lt=1-f['carry'],signed_lt=f['negative']^f['overflow'])
def alu(a,b,opcode):
 assert 0<=opcode<4
 sub=int(opcode==1);arith=addsub(a,b,sub)
 candidates=[arith['result'],a&b,a|b];port=[0,0,1,2][opcode]
 return dict(result=candidates[port],candidates=candidates,port=port,sub=sub,arithmetic=arith)
def main():
 count=0
 for a in range(16):
  for b in range(16):
   for sub in range(2):
    f=addsub(a,b,sub);assert f['result']==((a-b if sub else a+b)&15)
    exact=signed(a)-signed(b) if sub else signed(a)+signed(b)
    assert f['overflow']==int(not -8<=exact<=7)
   c=comparisons(a,b);assert c==dict(eq=int(a==b),unsigned_lt=int(a<b),signed_lt=int(signed(a)<signed(b)))
   for op,expected in enumerate([(a+b)&15,(a-b)&15,a&b,a|b]):
    assert alu(a,b,op)['result']==expected;count+=1
 assert [alu(5,3,k)['result'] for k in range(4)]==[8,2,1,7]
 assert addsub(5,3,1)['carry']==1 and addsub(5,6,1)['carry']==0
 assert comparisons(7,15)['signed_lt']==0 and addsub(7,15,1)['overflow']==1
 report=dict(addsub_cases=512,comparison_cases=256,alu_opcode_cases=count,example_outputs=['1000','0010','0001','0111'],carry_convention='Cout=1 means no borrow for A+NOT(B)+1',mux_ports=[0,0,1,2],sub_controls=[0,1,0,0],all_passed=True)
 r=Path(__file__).parent/'qa';r.mkdir(exist_ok=True);(r/'alu_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('PASS: ADD/SUB 512, comparisons 256, ALU/MUX 1024 cases; signed overflow included')
if __name__=='__main__':main()
