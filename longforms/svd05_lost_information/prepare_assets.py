"""All displayed approximations are actual truncated SVD, never blur effects."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;D=R/'assets';D.mkdir(exist_ok=True)
source=R.parent/'xai01_cat_mystery/assets/cat_photo.png'
rgba=Image.open(source).convert('RGBA');bg=Image.new('RGBA',rgba.size,(220,225,230,255));bg.alpha_composite(rgba)
photo=np.asarray(bg.convert('L').resize((160,192),Image.Resampling.LANCZOS),dtype=float)/255
u,s,vt=np.linalg.svd(photo,full_matrices=False)
def save(a,name):Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(D/(name+'.png'))
save(photo,'photo_original');errors={}
for k in [1,2,5,10]:
 a=(u[:,:k]*s[:k])@vt[:k];save(a,f'photo_rank{k}')
 err=np.linalg.norm(photo-a,'fro')**2;tail=float(np.sum(s[k:]**2));assert np.isclose(err,tail)
 errors[str(k)]={'squared_frobenius':float(err),'relative_frobenius':float(np.sqrt(err)/np.linalg.norm(photo,'fro')),'discarded_sigma_squared_sum':tail}
rng=np.random.default_rng(20261022);q,_=np.linalg.qr(rng.normal(size=(6,6)));v,_=np.linalg.qr(rng.normal(size=(6,6)))
ss=np.array([8,4,2,1,.5,.2]);parts=np.array([ss[i]*np.outer(q[:,i],v[:,i]) for i in range(6)]);a=parts.sum(axis=0);a3=parts[:3].sum(axis=0)
def heat(x,name,lim=8):
 z=x/lim;rgb=np.zeros((*x.shape,3));rgb[:]=[.07,.12,.19]
 for p,col in [(z>=0,np.array([.32,.85,.77])),(z<0,np.array([.74,.6,.99]))]:
  amount=np.clip(np.abs(z),0,1)[p,None];rgb[p]=rgb[p]*(1-amount)+col*amount
 Image.fromarray(np.uint8(rgb*255)).resize((360,360),Image.Resampling.NEAREST).save(D/(name+'.png'))
for i,p in enumerate(parts):heat(p,f'component{i+1}')
for x,n in [(a,'matrix_original'),(a3,'matrix_rank3'),(a-a3,'matrix_error')]:heat(x,n)
# Orthogonal zero-sum local marker: exact rank 2, with singular values 8 and 0.3.
n=16;marker=np.zeros((n,n));marker[7:9,7:9]=.15*np.array([[1,-1],[-1,1]])
marked=.5*np.ones((n,n))+marker;mu,ms,mv=np.linalg.svd(marked,full_matrices=False);rank1=(mu[:,:1]*ms[:1])@mv[:1]
assert np.allclose(ms[:2],[8,.3]);assert np.allclose(rank1,.5);assert np.allclose(ms[2:],0,atol=1e-12)
score=lambda m:float((m[7,7]-m[7,8]-m[8,7]+m[8,8])/4)
assert score(marked)>.075 and score(rank1)<.075
for x,name in [(marked,'marker_original'),(rank1,'marker_rank1')]:
 save(x,name);save(x[6:10,6:10],name+'_zoom')
np.savez(D/'svd_data.npz',photo=photo,photo_sigma=s,components=parts,matrix=a,matrix_rank3=a3,marker=marked,marker_rank1=rank1)
report={'photo_source':str(source),'source_kind':'existing photorealistic generated image; see xai01_cat_mystery/assets/generation.md','photo_shape':list(photo.shape),'photo_errors':errors,'display':'grayscale display clips to [0,1]; all ranks/errors computed on unclipped float matrices','rank3_squared_error':float(np.linalg.norm(a-a3)**2),'rank2_example':{'sigma':[8,4,2],'keep_8_4_error':4,'keep_8_2_error':16},'marker':{'sigma':ms[:2].tolist(),'original_score':score(marked),'rank1_score':score(rank1),'threshold':.075,'squared_frobenius_error':float(np.linalg.norm(marked-rank1)**2),'relative_frobenius_error':float(np.linalg.norm(marked-rank1)/np.linalg.norm(marked))}}
(D/'numerical_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
