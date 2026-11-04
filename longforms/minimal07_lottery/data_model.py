"""Small, fixed synthetic-XOR demonstration; not a reproduction of the LTH paper."""
from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).resolve().parent
SIZES=[2,6,4,2];STEPS=300;LR=.02

def initialize(seed):
 r=np.random.default_rng(seed);return [r.normal(0,np.sqrt(1/a),(a,b)) for a,b in zip(SIZES,SIZES[1:])],[np.zeros(b) for b in SIZES[1:]]
def data(seed,n):
 r=np.random.default_rng(seed);centers=r.choice([-1,1],(n,2));x=centers+r.normal(0,.24,(n,2));y=(centers[:,0]*centers[:,1]<0).astype(int);return x,y
X,Y=data(17,256);XT,YT=data(18,512)
def forward(x,w,b):
 a=[x]
 for k in range(2):a.append(np.tanh(a[-1]@w[k]+b[k]))
 z=a[-1]@w[-1]+b[-1];z-=z.max(1,keepdims=True);p=np.exp(z);p/=p.sum(1,keepdims=True);return a,p

def train(w0,b0,masks):
 w=[q.copy()*m for q,m in zip(w0,masks)];b=[q.copy() for q in b0];params=w+b;m=[np.zeros_like(q) for q in params];v=[q.copy() for q in m];acc=[];loss=[];hist=[]
 for step in range(STEPS+1):
  a,p=forward(X,w,b);loss.append(float(-np.log(p[np.arange(len(Y)),Y]+1e-12).mean()));_,pt=forward(XT,w,b);acc.append(float((pt.argmax(1)==YT).mean()));hist.append(np.concatenate([q.ravel() for q in w]))
  if step==STEPS:break
  delta=p.copy();delta[np.arange(len(Y)),Y]-=1;delta/=len(Y);gw=[None]*3;gb=[None]*3
  for k in reversed(range(3)):
   gw[k]=(a[k].T@delta)*masks[k];gb[k]=delta.sum(0)
   if k:delta=(delta@w[k].T)*(1-a[k]**2)
  grads=gw+gb;t=step+1
  for k,(q,g) in enumerate(zip(params,grads)):
   m[k]=.9*m[k]+.1*g;v[k]=.999*v[k]+.001*g*g;q-=LR*(m[k]/(1-.9**t))/(np.sqrt(v[k]/(1-.999**t))+1e-8)
  for q,mask in zip(w,masks):q*=mask
 return dict(weights=w,bias=b,accuracy=np.array(acc),loss=np.array(loss),history=np.array(hist))

def make_data():
 w0,b0=initialize(707);ones=[np.ones_like(q) for q in w0];dense=train(w0,b0,ones);flat=np.concatenate([q.ravel() for q in dense['weights']]);keep=33;mask=np.zeros(len(flat));mask[np.argsort(abs(flat),kind='stable')[-keep:]]=1
 masks=[];k=0
 for q in w0:masks.append(mask[k:k+q.size].reshape(q.shape));k+=q.size
 original=train(w0,b0,masks);wr,br=initialize(708);random=train(wr,br,masks)
 payload=dict(initial=np.concatenate([q.ravel() for q in w0]),trained=flat,mask=mask,random_initial=np.concatenate([q.ravel() for q in wr]),dense_accuracy=dense['accuracy'],ticket_accuracy=original['accuracy'],random_accuracy=random['accuracy'],dense_loss=dense['loss'],ticket_loss=original['loss'],random_loss=random['loss'],dense_history=dense['history'],ticket_history=original['history'],random_history=random['history'])
 np.savez_compressed(ROOT/'experiment_data.npz',**payload)
 threshold=.95
 def first(v):
  z=np.flatnonzero(v>=threshold);return int(z[0]) if len(z) else None
 report=dict(scope='Fixed illustrative synthetic XOR experiment, not original-paper results or general evidence.',architecture=SIZES,connection_weights=len(flat),retained_weights=keep,retention=.75,pruning='One-shot global magnitude pruning of trained connection weights. Biases are retained.',steps=STEPS,optimizer='Full-batch Adam',learning_rate=LR,train_size=256,test_size=512,seeds=dict(original=707,reinitialization=708,training_data=17,test_data=18),comparison='Same mask, data, optimizer, learning rate and iteration budget; biases initialized to zero in all cases.',target_accuracy=threshold,first_target_iterations=dict(dense=first(dense['accuracy']),original=first(original['accuracy']),random=first(random['accuracy'])),final_test_accuracy=dict(dense=float(dense['accuracy'][-1]),original=float(original['accuracy'][-1]),random=float(random['accuracy'][-1])))
 assert np.array_equal(original['history'][0],payload['initial']*mask)
 assert np.all(original['history'][:,mask==0]==0) and np.all(random['history'][:,mask==0]==0)
 assert np.any(payload['initial'][mask==1]!=payload['random_initial'][mask==1])
 (ROOT/'experiment_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');return report
if __name__=='__main__':print(json.dumps(make_data(),ensure_ascii=False,indent=2))
