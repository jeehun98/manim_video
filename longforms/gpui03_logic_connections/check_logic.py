"""Exhaustively check the depicted CMOS connectivity and NAND-only netlists."""
import json
from pathlib import Path
from logic_model import NETLISTS,evaluate,nand_state,reachable
R=Path(__file__).resolve().parent
def main():
 report=[]
 for a,b in [(0,0),(0,1),(1,0),(1,1)]:
  state=nand_state(a,b);assert state['y']==int(not(a and b))
  assert not reachable(state['edges'],'VDD','GND')
  expect={'NOT':1-a,'AND':a&b,'OR':a|b,'XOR':a^b}
  actual={name:evaluate(name,a,b)['Y'] for name in NETLISTS}
  assert actual==expect,(a,b,actual,expect)
  report.append(dict(a=a,b=b,nand=state['y'],pull_up=state['up'],pull_down=state['down'],netlists=actual))
 timing=json.loads((R/'timing.json').read_text(encoding='utf-8'))
 expected=[4,9,12,16,19,22,26,28,33,36,40,43,45,50,55,63,71,75,81,88,93,95,100,106,111,119,124,129,135,139,145,152,158,164]
 assert [x['end'] for x in timing]==expected
 assert timing[0]['start']==0 and all(x['end']==y['start'] for x,y in zip(timing,timing[1:]))
 qa=R/'qa';qa.mkdir(exist_ok=True)
 (qa/'logic_verification.json').write_text(json.dumps(dict(truth_tables=report,nand_gate_counts={k:len(v) for k,v in NETLISTS.items()},sentence_count=34,duration_seconds=164),indent=2),encoding='utf-8')
 print('PASS: four CMOS NAND states; no supply short; NAND-only NOT/AND/OR/XOR; 34 exact endpoints.')
if __name__=='__main__':main()
