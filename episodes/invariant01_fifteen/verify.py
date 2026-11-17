"""Check narration, mathematical invariance, and optionally actual render audits."""
import argparse
import json
from pathlib import Path
from model import SOLVED,IMPOSSIBLE,neighbors,parity,color,invariant,move,samples
from prepare import SCRIPT,stamp

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--rendered',action='store_true');args=parser.parse_args()
    data=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
    sentences=data['sentences'];scenes=data['scenes']
    assert sentences[0]['start']==scenes[0]['start']==0
    assert sentences[-1]['end']==scenes[-1]['end']==165
    assert all(a['end']==b['start'] for a,b in zip(sentences,sentences[1:]))
    assert all(a['end']==b['start'] for a,b in zip(scenes,scenes[1:]))
    assert [(s['end'],s['text']) for s in sentences]==[(int(line.split('|',1)[0]),line.split('|',1)[1]) for line in SCRIPT.splitlines()]
    blocks=(HERE/'captions.srt').read_text(encoding='utf-8').strip().split('\n\n')
    assert len(blocks)==len(sentences)
    for i,(block,s) in enumerate(zip(blocks,sentences),1):
        assert block.splitlines()==[str(i),f"{stamp(s['start'])} --> {stamp(s['end'])}",s['text']]
    assert invariant(SOLVED)==0 and invariant(IMPOSSIBLE)==1
    # The rendered pass checks actual transitions; the preflight checks the model.
    if not args.rendered:
        for i in range(16):
            for j in range(i+1,16):
                b=list(SOLVED);b[i],b[j]=b[j],b[i]
                assert parity(tuple(b))==1
        for start in (SOLVED,IMPOSSIBLE):
            for b in samples(start,2048):
                for index in neighbors(b.index(0)):
                    after=move(b,index)
                    assert invariant(after)==invariant(start)
    move_count=0
    if args.rendered:
        audit=HERE.parents[1]/'media/invariant01/final/audit'
        records=[]
        for shot in scenes:
            records.extend(json.loads((audit/(shot['id']+'.json')).read_text()))
            transitions=json.loads((audit/(shot['id']+'_moves.json')).read_text())
            for t in transitions:
                before,after=tuple(t['before']),tuple(t['after'])
                assert move(before,t['index'])==after
                assert before[t['index']]==t['tile']
                assert (parity(after),color(after),invariant(after))==(t['p'],t['c'],t['I'])
                assert shot['start']<=t['at']<t['end']<=shot['end']+.00001
                move_count+=1
        assert {r['sentence'] for r in records}==set(range(1,len(sentences)+1))
        assert all(abs(r['at']-sentences[r['sentence']-1]['start'])<1/60+.00001 for r in records)
        assert all(r['width']<=7.65001 and r['height']<=2.15001 for r in records)
    print(f'Verified {len(sentences)} captions, 165 seconds, parity and checker invariant; {move_count} rendered legal moves')

if __name__=='__main__':main()
