"""Conceptual time units, not measured seconds/ns. Shared by diagram and checks."""
import itertools,json
from pathlib import Path
CQ=.3
def data(t):return int(1<=t<6)
def clock(t):return int(2<=t<4 or 8<=t<9.5)
EDGES=[2,8]
def q_at(t):
 q=0
 for edge in EDGES:
  if t>=edge+CQ:q=data(edge)
 return q
def output_bus(t):return 0 if t<6 else 8
def capture_bus(edge,setup=.5,hold=.2):
 if edge-setup<6<=edge+hold:return None
 return output_bus(edge)
def bank(bits,q,clk_prev,clk):return tuple(bits) if not clk_prev and clk else tuple(q)
def period_ok(period,cq=1,logic=5,setup=1,uncertainty=.5):return period>=cq+logic+setup+uncertainty
def main():
 for e in EDGES:
  assert data(e-.5)==data(e)==data(e+.2)
  assert q_at(e+.299)==q_at(e-.001)
  assert q_at(e+.301)==data(e)
 assert q_at(3)==1 and data(6.5)==0 and q_at(6.5)==1 and q_at(8.5)==0
 assert capture_bus(3)==0 and capture_bus(8)==8 and capture_bus(6) is None
 assert not period_ok(4) and period_ok(8)
 cases=0
 for d in itertools.product([0,1],repeat=4):
  for q in itertools.product([0,1],repeat=4):
   for old,new in [(0,0),(0,1),(1,0),(1,1)]:
    expect=d if (old,new)==(0,1) else q;assert bank(d,q,old,new)==expect;cases+=1
 assert bank((1,0,0,0),(0,0,0,0),0,1)==(1,0,0,0)
 p=Path(__file__).parent/'qa';p.mkdir(exist_ok=True)
 (p/'timing_verification.json').write_text(json.dumps(dict(four_bit_edge_cases=cases,clock_to_q=CQ,rising_edges=EDGES,q_changes_after_edges=True,early_capture=0,late_capture=8,unstable_capture=None,bank8='1000',period_check='CQ+logic+setup+uncertainty; hold is a separate constraint',all_passed=True),indent=2),encoding='utf-8')
 print('PASS 1024 bank/edge cases, Q after edge, hold between edges, early/late capture and period margin')
if __name__=='__main__':main()
