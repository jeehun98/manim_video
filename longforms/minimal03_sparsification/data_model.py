"""Deterministic weighted graphs and certificates used in the film."""
import json,itertools
from pathlib import Path
import numpy as np
def complete(n,w=1):return [(i,j,float(w)) for i,j in itertools.combinations(range(n),2)]
def laplacian(n,edges):
 L=np.zeros((n,n))
 for i,j,w in edges:
  assert i!=j and w>0
  L[i,i]+=w;L[j,j]+=w;L[i,j]-=w;L[j,i]-=w
 return L
def energy(edges,x):return float(sum(w*(x[i]-x[j])**2 for i,j,w in edges))
def bounds(n,g,h):
 L=laplacian(n,g);H=laplacian(n,h);v,U=np.linalg.eigh(L);Q=U[:,v>1e-9];d=v[v>1e-9]
 B=(Q/np.sqrt(d)).T@H@(Q/np.sqrt(d));return np.linalg.eigvalsh(B)
def components(n,edges):
 adj={i:[] for i in range(n)}
 for i,j,w in edges:adj[i].append(j);adj[j].append(i)
 seen=set();out=[]
 for i in range(n):
  if i in seen:continue
  group=set();todo=[i]
  while todo:
   j=todo.pop()
   if j in group:continue
   group.add(j);todo.extend(adj[j])
  seen|=group;out.append(sorted(group))
 return out
TREE=[(i,i+1,1.) for i in range(7)]
TRI_G=complete(3)
TRI_H=[(0,1,1.5),(0,2,1.5)]
TRI_VALUES=[[0,1,2],[1,0,0],[0,1,-1]]
CLUSTERS=[(i,j,1.) for group in [range(4),range(4,8)] for i,j in itertools.combinations(group,2)]+[(3,4,1.)]
CYCLE={(i,i+1) for i in range(7)}|{(0,7)}
SPARSE_G=[(i,j,4. if (i,j) in CYCLE else .1) for i,j in itertools.combinations(range(8),2)]
SPARSE_H=[(i,j,4.6) for i,j in sorted(CYCLE)]
VALUES=[[0,1,2,3,2,1,0,-1],[1,0,-1,0,1,0,-1,0],[0,0,0,0,1,1,1,1]]
def effective_resistances():
 inv=np.linalg.pinv(laplacian(8,CLUSTERS));return {(i,j):float(inv[i,i]+inv[j,j]-2*inv[i,j]) for i,j,w in CLUSTERS}
def verify():
 assert len(TREE)==7 and len(components(8,TREE))==1
 assert len(components(8,[e for e in CLUSTERS if e[:2] not in [(0,1),(3,4)]]))==2
 assert energy(TRI_G,[0,1,2])==6 and energy(TRI_H,[0,1,2])==7.5
 tr=bounds(3,TRI_G,TRI_H);assert np.allclose(tr,[.5,1.5])
 ratios=bounds(8,SPARSE_G,SPARSE_H);assert ratios.min()>=.85 and ratios.max()<=1.15
 # Analytic all-vector certificate: simultaneous eigenbasis of cycle and K8.
 lams=np.array([2-2*np.cos(2*np.pi*k/8) for k in range(1,8)])
 analytic=4.6*lams/(3.9*lams+.8);assert np.allclose(np.sort(analytic),ratios)
 r=effective_resistances();assert abs(r[(0,1)]-.5)<1e-10 and abs(r[(3,4)]-1)<1e-10
 report=dict(triangle=dict(original=6,sparse=7.5,all_vector_ratio_range=[float(tr.min()),float(tr.max())]),validated_graph=dict(nodes=8,original_edges=28,sparse_edges=8,original_weights={'cycle':4,'other':.1},sparse_weight=4.6,epsilon=.15,all_vector_ratio_range=[float(ratios.min()),float(ratios.max())],analytic_cycle_eigenvalue_certificate=True,examples=[dict(values=x,original=energy(SPARSE_G,x),sparse=energy(SPARSE_H,x)) for x in VALUES]),effective_resistance=dict(internal=r[(0,1)],bridge=r[(3,4)]))
 (Path(__file__).resolve().parent/'math_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');return report
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
