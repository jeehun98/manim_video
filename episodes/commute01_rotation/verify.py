"""Validate exact narration, matrices, and recorded world-axis rotations."""
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
    assert s[0]['start']==shots[0]['start']==0 and s[-1]['end']==shots[-1]['end']==167
    for items in (s,shots):assert all(a['end']==b['start'] for a,b in zip(items,items[1:]))
    assert [(x['end'],x['text']) for x in s]==[(int(l.split('|',1)[0]),l.split('|',1)[1]) for l in SCRIPT.splitlines()]
    blocks=(HERE/'captions.srt').read_text(encoding='utf-8').strip().split('\n\n');assert len(blocks)==len(s)
    for i,(block,x) in enumerate(zip(blocks,s),1):assert block.splitlines()==[str(i),f"{stamp(x['start'])} --> {stamp(x['end'])}",x['text']]
    assert np.allclose(model.RY@model.RX@model.NORMAL,[0,-1,0])
    assert np.allclose(model.RX@model.RY@model.NORMAL,[1,0,0])
    assert np.array_equal(model.R2@np.array([2,1]),[-1,2])
    count=0
    if not args.rendered:
        for axis in ('X','Y'):
            for t in np.linspace(0,np.pi/2,61):
                r=model.rotation(axis,t);assert np.allclose(r.T@r,np.eye(3)) and np.isclose(np.linalg.det(r),1)
        assert np.array_equal(model.R2[:,0],[0,1]) and np.array_equal(model.R2[:,1],[-1,0])
        assert np.allclose(model.PROJECTION@model.PROJECTION.T,np.eye(2))
    else:
        audit=HERE.parents[1]/'media/commute01/final/audit';captions=[]
        for shot in shots:
            captions.extend(json.loads((audit/(shot['id']+'.json')).read_text()))
            records=json.loads((audit/(shot['id']+'_rotations.json')).read_text())
            for r in records:
                expected=(model.RX if r['axis']=='X' else model.RY)@np.array(r['before'])
                assert np.allclose(expected,r['after']) and np.allclose(expected@model.NORMAL,r['normal'])
                assert shot['start']<=r['at']<r['end']<=shot['end']+.00001
                count+=1
            if shot['id'] in ('02','07'):
                assert [r['axis'] for r in records]==['X','Y','Y','X']
                assert np.allclose(records[0]['before'],np.eye(3)) and np.allclose(records[2]['before'],np.eye(3))
                assert np.allclose(records[1]['normal'],[0,-1,0]) and np.allclose(records[3]['normal'],[1,0,0])
        assert {r['sentence'] for r in captions}==set(range(1,len(s)+1))
        assert all(abs(r['at']-s[r['sentence']-1]['start'])<1/60+.00001 for r in captions)
        assert all(r['width']<=7.65001 and r['height']<=2.15001 for r in captions)
    print(f'Verified {len(s)} captions, 167 seconds, basis images and rotation conventions; {count} rendered rotations')
if __name__=='__main__':main()
