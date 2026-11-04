"""Reproducible 2D Ising samples, fair block spins, and explicitly schematic RG coordinates."""
from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).resolve().parent
TC=2/np.log(1+np.sqrt(2));SEED=606

def wolff(s,T,rng):
 n=len(s);seed=tuple(rng.integers(n,size=2));v=s[seed];p=1-np.exp(-2/T);cluster={seed};stack=[seed]
 while stack:
  i,j=stack.pop()
  for q in [((i+1)%n,j),((i-1)%n,j),(i,(j+1)%n),(i,(j-1)%n)]:
   if q not in cluster and s[q]==v and rng.random()<p:cluster.add(q);stack.append(q)
 for q in cluster:s[q]*=-1
 return len(cluster)

def block(s,rng):
 n=len(s);assert n%2==0;tot=s.reshape(n//2,2,n//2,2).sum(axis=(1,3));out=np.sign(tot).astype(np.int8);ties=tot==0;out[ties]=rng.choice([-1,1],size=ties.sum());return out,int(ties.sum())

def energy(s):return float(-np.mean(s*(np.roll(s,1,0)+np.roll(s,1,1))))
def correlation(s):return float(np.mean(s*np.roll(s,1,0)))
def make_data():
 rng=np.random.default_rng(SEED);data={};stats={}
 for name,T in [('low',1.4),('high',4.),('critical',TC)]:
  s=rng.choice([-1,1],size=(16,16)).astype(np.int8)
  for _ in range(1600):wolff(s,T,rng)
  samples=[]
  for _ in range(64):
   for _ in range(30):wolff(s,T,rng)
   samples.append(s.copy())
  samples=np.array(samples);data[name]=samples
  stats[name]=dict(T=float(T),mean_abs_magnetization=float(np.abs(samples.mean((1,2))).mean()),mean_energy=float(np.mean([energy(q) for q in samples])),mean_neighbor_correlation=float(np.mean([correlation(q) for q in samples])))
 # Select a mixed, correlated equilibrium sample for visual legibility, not exponent estimation.
 k=int(np.argmin(abs(abs(data['critical'].mean((1,2)))-.35)));s=data['critical'][k].copy();data['level0']=s;tie_counts=[];brng=np.random.default_rng(1608)
 for lev in range(1,4):s,ties=block(s,brng);data[f'level{lev}']=s;tie_counts.append(ties)
 np.savez_compressed(ROOT/'simulation_data.npz',**data)
 report=dict(seed=SEED,model='16x16 periodic 2D nearest-neighbor Ising, J=kB=1, h=0',method='Wolff single-cluster Monte Carlo',burnin_cluster_updates=1600,samples_per_temperature=64,updates_between_samples=30,critical_temperature=float(TC),sample_statistics=stats,selected_critical_sample=k,selection='Mixed equilibrium snapshot selected for legibility, not measurement.',block_sizes=[16,8,4,2],block_tie_counts=tie_counts,tie_rule='Each zero-sum 2x2 block independently samples -1 or +1 with equal probability; fixed seed 1608.',rg_flow='Schematic local map (r,g)->(2r,g/2), not inferred Ising coupling constants.',critical_manifold='r=0; g decays to zero. r!=0 grows away from fixed point.',scaling_curves='Illustrative power-law curves only, no measured critical exponents.')
 (ROOT/'simulation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');return report

def verify():
 if not (ROOT/'simulation_data.npz').exists():make_data()
 d=np.load(ROOT/'simulation_data.npz');rng=np.random.default_rng(1608)
 for lev in range(3):
  out,ties=block(d[f'level{lev}'],rng);assert np.array_equal(out,d[f'level{lev+1}'])
  assert set(np.unique(out))<= {-1,1}
 # Tie handling has no deterministic preference for either orientation.
 r=np.random.default_rng(12);balanced=np.array([[1,1],[-1,-1]],np.int8);up=sum(block(balanced,r)[0][0,0]>0 for _ in range(5000));assert .46<up/5000<.54
 a=np.array([0.,.8]);b=np.array([0.,-.65]);off=np.array([.05,.3]);history=[]
 for _ in range(7):
  history.append(dict(a=a.tolist(),b=b.tolist(),off=off.tolist()));a*=np.array([2,.5]);b*=np.array([2,.5]);off*=np.array([2,.5])
 assert abs(a[1])<.01 and abs(b[1])<.01 and off[0]>.05
 rep=json.loads((ROOT/'simulation_report.json').read_text(encoding='utf-8'));assert rep['sample_statistics']['critical']['mean_neighbor_correlation']>.3
 report=dict(block_reproduction_passed=True,tie_up_fraction=up/5000,critical_correlations_not_iid=True,rg_fixed_point_invariant=True,rg_history=history,rg_relevant_multiplier=2,rg_irrelevant_multiplier=.5,scope='Equilibrium samples and block spins are computed. RG flow and material diagrams are illustrative; no effective Hamiltonian is fitted.')
 (ROOT/'math_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');return report
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
