"""Exact small-integer model of the provided shared-memory reduction."""
def snapshots():
    values=list(range(1,129));out=[dict(stride=None,count=128,values=values.copy())]
    stride=64
    while stride:
        old=values.copy()
        for t in range(stride):values[t]=old[t]+old[t+stride]
        out.append(dict(stride=stride,count=stride,values=values.copy()))
        stride//=2
    return out
STAGES=snapshots()
