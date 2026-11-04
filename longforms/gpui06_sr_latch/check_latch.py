"""NOR latch event model: no oscillatory parallel iteration, no illegal input demo."""
import itertools,json
from pathlib import Path
def nor(a,b):return int(not(a or b))
def stable(s,r,q,qbar):return q==nor(r,qbar) and qbar==nor(s,q)
def states(s,r):return [(q,b) for q,b in itertools.product([0,1],repeat=2) if stable(s,r,q,b)]
def transition(q,s,r):
 if s and r:raise ValueError('S=R=1 is excluded from the demonstration')
 old=(q,1-q);events=[];a,b=old
 # Gate events are ordered by the asserted external input.
 for gate in ([1,0] if s else [0,1]):
  if gate==0:a=nor(r,b)
  else:b=nor(s,a)
  if (a,b)!=(events[-1][1:] if events else old):events.append((gate,a,b))
 assert stable(s,r,a,b)
 return events,(a,b)
def main():
 assert states(0,0)==[(0,1),(1,0)]
 assert states(1,0)==[(1,0)] and states(0,1)==[(0,1)]
 assert states(1,1)==[(0,0)] # Both outputs low; release is not a valid stored state.
 count=0
 for q in [0,1]:
  for s,r in [(0,0),(1,0),(0,1)]:
   events,final=transition(q,s,r);assert final[0]==(1 if s else 0 if r else q)
   assert transition(final[0],0,0)[1]==final;count+=1
 assert transition(0,1,0)[0]==[(1,0,0),(0,1,0)]
 assert transition(1,0,1)[0]==[(0,0,0),(1,0,1)]
 # All 3^6 legal input sequences for both assumed initial states.
 for initial in [0,1]:
  for sequence in itertools.product([(0,0),(1,0),(0,1)],repeat=6):
   q=initial
   for s,r in sequence:
    _,(q,b)=transition(q,s,r);assert stable(s,r,q,b)
 p=Path(__file__).parent/'qa';p.mkdir(exist_ok=True)
 (p/'latch_verification.json').write_text(json.dumps(dict(stable_states_hold=states(0,0),legal_single_transitions=count,six_input_sequences=1458,set_event_order='Qbar=0 then Q=1',reset_event_order='Q=0 then Qbar=1',illegal_input_excluded=True,volatile_storage=True),indent=2),encoding='utf-8')
 print('PASS: 6 transitions, 1458 legal six-input sequences, both fixed-point equations and hold')
if __name__=='__main__':main()
