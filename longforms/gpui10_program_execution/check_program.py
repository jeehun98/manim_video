"""Slot-address PC and immutable instruction-memory teaching model."""
import json,itertools
from pathlib import Path
from check_instruction import decode,execute
MEMORY=(int('00110110',2),int('01111101',2),None,None)
def fetch(pc):
 assert 0<=pc<len(MEMORY) and MEMORY[pc] is not None
 return MEMORY[pc]
def next_pc(pc,target,taken):return target if taken else pc+1
def commit_pc(pc,candidate,enable,rising):return candidate if enable and rising else pc
def branch_taken(is_branch,value):return bool(is_branch and value==0)
def step(pc,regs):
 word=fetch(pc);after,result=execute(word,regs)
 return next_pc(pc,0,False),after,result

def main():
 before=MEMORY;pc=0;regs=(0,5,3,0);trace=[]
 for expected in [8,3]:
  old_pc=pc;word=fetch(pc);pc,regs,result=step(pc,regs);assert result==expected;trace.append(dict(pc=old_pc,word=f'{word:08b}',result=result,next_pc=pc,regs=regs))
 assert regs==(0,5,3,3) and pc==2 and MEMORY==before
 assert decode(MEMORY[1])==dict(op=1,rd=3,rs1=3,rs2=1)
 cases=0
 for pc,target,taken,en,edge in itertools.product(range(16),range(16),range(2),range(2),range(2)):
  candidate=next_pc(pc,target,taken);after=commit_pc(pc,candidate,en,edge)
  assert candidate==(target if taken else pc+1)
  assert after==(candidate if en and edge else pc);cases+=1
 for ib,v in itertools.product(range(2),range(16)):assert branch_taken(ib,v)==bool(ib and v==0)
 assert next_pc(1,3,False)==2 and next_pc(1,3,True)==3
 assert MEMORY==before
 q=Path(__file__).parent/'qa';q.mkdir(exist_ok=True)
 (q/'program_verification.json').write_text(json.dumps(dict(all_passed=True,pc_cases=cases,branch_conditions=32,memory_immutable=True,slot_addresses=True,trace=trace,branch_example={'pc':1,'sequential':2,'target':3,'taken_next_pc':3,'not_taken_next_pc':2},branch_not_encoded_in_arithmetic_isa=True),indent=2),encoding='utf-8')
 print('PASS2048 PC selection/edge cases;32 branch conditions;ADD8→SUB3;immutable memory')
if __name__=='__main__':main()
