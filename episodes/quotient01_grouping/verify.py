"""Validate exact narration, quotient operations, and actual square transformations."""
import argparse
import json
from pathlib import Path
import numpy as np
import model
from prepare import SCRIPT,stamp
HERE=Path(__file__).resolve().parent
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--rendered',action='store_true');args=parser.parse_args()
    d=json.loads((HERE/'timing.json').read_text(encoding='utf-8'));s=d['sentences'];shots=d['scenes']
    assert s[0]['start']==shots[0]['start']==0 and s[-1]['end']==shots[-1]['end']==174
    for items in (s,shots):assert all(a['end']==b['start'] for a,b in zip(items,items[1:]))
    assert [(x['end'],x['text']) for x in s]==[(int(l.split('|',1)[0]),l.split('|',1)[1]) for l in SCRIPT.splitlines()]
    blocks=(HERE/'captions.srt').read_text(encoding='utf-8').strip().split('\n\n');assert len(blocks)==len(s)
    for i,(block,x) in enumerate(zip(blocks,s),1):assert block.splitlines()==[str(i),f"{stamp(x['start'])} --> {stamp(x['end'])}",x['text']]
    count=0
    if not args.rendered:
        for a in range(-9,10):
            for b in range(-9,10):
                for u,v in ((-4,6),(0,2),(8,-2)):
                    assert model.parity(a+b)==model.quotient_add(model.parity(a),model.parity(b))==model.parity((a+u)+(b+v))
        for g in model.D4:
            for r in model.ROTATIONS:
                assert any(np.array_equal(g@r@g.T,h) for h in model.ROTATIONS)
            for h in model.D4:
                model.name(g@h)
                assert model.symmetry_class(g@h)==model.quotient_add(model.symmetry_class(g),model.symmetry_class(h))
        assert np.array_equal(model.S@model.R@model.S.T,model.R.T)
        assert len({tuple(m.flat) for m in model.D4})==8
    else:
        audit=HERE.parents[1]/'media/quotient01/final/audit';captions=[]
        for shot in shots:
            captions.extend(json.loads((audit/(shot['id']+'.json')).read_text()))
            records=json.loads((audit/(shot['id']+'_actions.json')).read_text())
            for r in records:
                expected=np.array(r['transform'])@np.array(r['before'])
                assert np.array_equal(expected,r['after'])
                assert model.symmetry_class(expected)==r['class_index'] and model.name(expected)==r['name']
                assert shot['start']<=r['at']<r['end']<=shot['end']+.00001
                count+=1
            if shot['id']=='08':
                assert len(records)==8
                assert {r['name'] for r in records}=={'e','r','r²','r³','s','rs','r²s','r³s'}
        assert {r['sentence'] for r in captions}==set(range(1,len(s)+1))
        assert all(abs(r['at']-s[r['sentence']-1]['start'])<1/60+.00001 for r in captions)
        assert all(r['width']<=7.65001 and r['height']<=2.15001 for r in captions)
    print(f'Verified {len(s)} captions, 174 seconds, representative independence and D4 quotient; {count} rendered symmetries')
if __name__=='__main__':main()
