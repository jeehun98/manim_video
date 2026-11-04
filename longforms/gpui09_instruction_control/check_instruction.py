"""Educational 8-bit ISA; four ordinary registers holding unsigned 4-bit values."""
import itertools,json
from pathlib import Path
OPS=('ADD','SUB','AND','OR')
def decode(word):
 assert 0<=word<256
 return dict(op=(word>>6)&3,rd=(word>>4)&3,rs1=(word>>2)&3,rs2=word&3)
def encode(op,rd,rs1,rs2):return op<<6|rd<<4|rs1<<2|rs2
def alu(op,a,b):return ((a+b,a-b,a&b,a|b)[op])&15
def execute(word,regs,we=True,rising=True):
 d=decode(word);value=alu(d['op'],regs[d['rs1']],regs[d['rs2']]);out=list(regs)
 if we and rising:out[d['rd']]=value
 return tuple(out),value

def main():
 for fields in itertools.product(range(4),repeat=4):
  word=encode(*fields);assert tuple(decode(word).values())==fields
 for op,a,b in itertools.product(range(4),range(16),range(16)):
  expected=[(a+b)%16,(a-b)%16,a&b,a|b][op];assert alu(op,a,b)==expected
 cases=0
 for word,we,edge in itertools.product(range(256),range(2),range(2)):
  before=(9,5,3,0);after,value=execute(word,before,we,edge);d=decode(word)
  for i in range(4):assert after[i]==(value if i==d['rd'] and we and edge else before[i])
  assert before==(9,5,3,0);cases+=1
 add=int('00110110',2);sub=int('01110110',2)
 assert decode(add)==dict(op=0,rd=3,rs1=1,rs2=2)
 assert execute(add,(0,5,3,0))==((0,5,3,8),8)
 assert execute(sub,(0,5,3,8),False)==((0,5,3,8),2)
 q=Path(__file__).parent/'qa';q.mkdir(exist_ok=True)
 (q/'instruction_verification.json').write_text(json.dumps(dict(all_passed=True,encodings=256,alu_cases=1024,write_cases=cases,example={'instruction':'00110110','fields':decode(add),'result':8,'registers':[0,5,3,8]},sub_preview_write_disabled=True),indent=2),encoding='utf-8')
 print('PASS256 encodings;1024 ALU cases;1024 write conditions;ADD/SUB example')
if __name__=='__main__':main()
