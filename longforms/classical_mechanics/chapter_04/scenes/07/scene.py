import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import ChapterScene,rig,Arc,Circle,BLUE,GOLD,GREEN,MUTED,I,A,EC,np,VGroup,Dot,Line,state
class Shot07(ChapterScene):
 index=7
 def prepare(self):
  super().prepare();self.level_cache={};self.period_cache={}
  for text in self.energy_labels.values():text.set_y(-2.4)
  def replace_group(target):
   self.dynamic.submobjects=target.submobjects
   return self.dynamic
  self.dynamic.become=replace_group
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def level(self,ax,r,*args,**kwargs):
  key=(r,tuple(ax.x_range),tuple(ax.y_range),tuple(ax.get_center()),ax.width,ax.height,repr(args),repr(sorted(kwargs.items())))
  if key not in self.level_cache:self.level_cache[key]=super().level(ax,r,*args,**kwargs)
  return self.level_cache[key].copy()
 def live_state(self,t):
  r=self.energy_ratio(t);u=(t-234)*.45
  if r>1:
   if r not in self.period_cache:
    q=np.linspace(0,2*np.pi,4097);speed=np.sqrt(2*(EC*r-A*(1-np.cos(q)))/I)
    self.period_cache[r]=float(np.trapezoid(1/speed,q))
   u%=self.period_cache[r]
  return r,state(r,min(u,11.9))
 def geometry(self,t):
  r,(q,p)=self.live_state(t);wrapped=(q+np.pi)%(2*np.pi)-np.pi;ax=self.portrait.copy();g=VGroup(ax)
  for e in [.25,.6,1,1.3]:g.add(self.level(ax,e,GREEN if e==1 else BLUE,2,.55 if e==1 else .18))
  g.add(self.energy_labels[round(r*100)].copy(),self.level(ax,r,GOLD,4,.95),Dot(ax.c2p(wrapped,p),color=GOLD,radius=.08),rig(0,pivot=(-4.8,.1,0),L=1.5,theta=float(q),omega=float(p/I),trace=False))
  g.add(Line([-1.7,-2.12,0],[5.7,-2.12,0],color=MUTED,stroke_opacity=.3),Dot([-1.7+(r-.1)/1.3*7.4,-2.12,0],radius=.075,color=GOLD))
  if r<1:
   amp=np.arccos(1-2*r);path=Arc(radius=1.5,start_angle=-np.pi/2-amp,angle=2*amp,arc_center=(-4.8,.1,0),color=BLUE,stroke_opacity=.2,fill_opacity=0)
  else:path=Circle(radius=1.5,color=BLUE,stroke_opacity=.2,fill_opacity=0).move_to([-4.8,.1,0])
  g.add(path);return g
