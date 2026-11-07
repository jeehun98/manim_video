"""Read/write direction, writeback selection and valid-response gating."""
import json,itertools
from pathlib import Path

def writeback(alu_value,mem_value,source):
 assert source in ['ALU','MEM'];return alu_value if source=='ALU' else mem_value

def reg_write(regs,dest,data,we=True,edge=True,valid=True):
 out=list(regs)
 if we and edge and valid:out[dest]=data
 return tuple(out)

def mem_write(memory,address,data,we=True,edge=True,ready=True):
 out=dict(memory)
 if we and edge and ready:out[address]=data
 return out

class Machine:
 def __init__(self,regs=(0,0,0,0)):
  self.regs=tuple(regs);self.memory={100:5,101:3,102:0,103:0};self.command='대기';self.pending=None
 def load(self,address,dest,ready=True,edge=True):
  self.command=f'LOAD R{dest}, [{address}]';self.pending=(address,dest,'LOAD')
  if ready and edge:self.regs=reg_write(self.regs,dest,self.memory[address]);self.pending=None
 def add(self,a=1,b=2,dest=3,edge=True):
  self.command=f'ADD R{dest}, R{a}, R{b}';value=self.regs[a]+self.regs[b];self.regs=reg_write(self.regs,dest,value,edge=edge);return value
 def store(self,address=102,src=3,edge=True):
  self.command=f'STORE R{src}, [{address}]';self.memory=mem_write(self.memory,address,self.regs[src],edge=edge)

def main():
 for a,b,source in itertools.product(range(16),range(16),['ALU','MEM']):assert writeback(a,b,source)==(a if source=='ALU' else b)
 rc=mc=0
 for dest,value,we,edge,valid in itertools.product(range(4),range(16),range(2),range(2),range(2)):
  before=(9,5,3,0);out=reg_write(before,dest,value,we,edge,valid)
  for i in range(4):assert out[i]==(value if i==dest and we and edge and valid else before[i])
  rc+=1
 for address,value,we,edge,ready in itertools.product([100,101,102],range(16),range(2),range(2),range(2)):
  before={100:5,101:3,102:0};out=mem_write(before,address,value,we,edge,ready)
  for a in before:assert out[a]==(value if a==address and we and edge and ready else before[a])
  mc+=1
 m=Machine();original=dict(m.memory);trace=[]
 m.load(100,1);trace.append(dict(command=m.command,regs=m.regs,memory=dict(m.memory)));assert m.memory==original and m.regs==(0,5,0,0)
 m.load(101,2);trace.append(dict(command=m.command,regs=m.regs,memory=dict(m.memory)));assert m.memory==original and m.regs==(0,5,3,0)
 assert m.add()==8;trace.append(dict(command=m.command,regs=m.regs,memory=dict(m.memory)));assert m.memory==original and m.regs==(0,5,3,8)
 before=m.regs;m.store();trace.append(dict(command=m.command,regs=m.regs,memory=dict(m.memory)));assert m.regs==before and m.memory=={100:5,101:3,102:8,103:0}
 p=Machine();p.load(100,1,ready=False);assert p.regs==(0,0,0,0) and p.pending==(100,1,'LOAD') and p.memory==original
 q=Path(__file__).parent/'qa';q.mkdir(exist_ok=True)
 (q/'memory_verification.json').write_text(json.dumps(dict(all_passed=True,writeback_cases=512,register_write_cases=rc,memory_write_cases=mc,read_non_destructive=True,store_does_not_write_registers=True,invalid_response_does_not_write=True,trace=trace),indent=2),encoding='utf-8')
 print('PASS512 MUX;512 register writes;384 memory writes;LOAD5/3→ADD8→STORE102;pending Load holds')
if __name__=='__main__':main()
