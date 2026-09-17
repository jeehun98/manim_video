"""Softmax finale: Q-K scores, competitive weights, and a Value mixture. 152s."""
import os
import numpy as np
from manim import *
config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#091119'
INK,MUTED,MINT,BLUE,GOLD,PINK='#EDF3F7','#94A7B7','#61E4CF','#68D9F0','#F3CF75','#FF8C9D'
COLORS=[BLUE,GOLD,PINK]
DURATION=152
CAPTIONS=[
(0,'앞에서 소프트맥스는 여러 점수를 하나의 분포로 바꾸고,\n그 값들이 서로 경쟁하게 만든다고 했습니다.'),
(6,'이 성질은 Attention에서 그대로 사용됩니다.'),
(9.5,'먼저 Query와 여러 Key의 관계를 계산해서\n각각 하나의 점수를 만듭니다.'),
(15,'예를 들어 소프트맥스에 들어갈 점수가\n[1, 2, 5]라고 해보겠습니다.'),
(21,'이 점수는 각 Key가 현재 Query와\n얼마나 잘 맞는지를 나타냅니다.'),
(26,'여기에 소프트맥스를 적용하면\n합이 1인 가중치로 바뀝니다.'),
(31,'결과는 대략\n[0.017, 0.047, 0.936]입니다.'),
(36,'이 가중치는 각 Key에 대응하는 Value를\n얼마나 반영할지 나타내는 비중입니다.'),
(42,'Attention의 출력은\n이 가중치로 Value들을 섞어서 만듭니다.'),
(47,'그림에서는 세 Value를\n평면 위의 벡터로 나타내보겠습니다.'),
(52,'가중합으로 만든 출력은\n비중이 가장 큰 세 번째 Value 가까이에 놓입니다.'),
(58,'세 번째 Value는 크게 반영되지만,\n다른 Value들의 영향도 조금씩 남아 있습니다.'),
(64,'그런데 소프트맥스는 각 점수를\n독립적으로 바꾸는 함수가 아닙니다.'),
(69,'첫 번째 점수만 올려보겠습니다.\n그 가중치는 커지고, 다른 가중치들은 함께 작아집니다.'),
(76,'다른 점수는 그대로여도 공통 분모가 커지기 때문입니다.\n전체 비중의 합은 여전히 1입니다.'),
(83,'즉 각 Key는 제한된 전체 비중을 두고 경쟁하며,\n그 결과에 따라 Value가 섞이는 비율도 바뀝니다.'),
(90,'또한 소프트맥스는 점수의 절대적인 크기보다\n점수 사이의 차이에 반응합니다.'),
(96,'두 점수의 차이는\n가중치의 지수적인 비율로 바뀝니다.'),
(101,'처음 점수 [1, 2, 5]에서는\n세 번째가 첫 번째보다 4만큼 높습니다.'),
(106,'그래서 세 번째 가중치는 첫 번째의\n약 55배가 됩니다.'),
(111,'반대로 여러 Key의 점수가 비슷하면\n가중치도 여러 곳에 나뉩니다.'),
(116,'세 점수가 모두 같아지면 비중은 각각 3분의 1,\n출력은 세 Value의 평균이 됩니다.'),
(123,'이것이 소프트맥스가 Attention에서\n단순한 정규화 이상의 역할을 하는 이유입니다.'),
(129,'소프트맥스는 Query와 Key의 상대적인 점수를\nValue를 섞기 위한 경쟁적인 가중치로 바꿉니다.'),
(136,'Attention은 정보 하나만 고르는 대신,\n여러 정보에 서로 다른 비중을 주어\n하나의 새로운 표현을 만듭니다.'),
(144,'그리고 그 비중을 결정하는 함수가\n우리가 살펴본 소프트맥스입니다.'),
]
def txt(s,size=29,color=INK):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if m.width>7.5:m.scale_to_fit_width(7.5)
 return m
def soft(scores):
 x=np.asarray(scores,dtype=float);e=np.exp(x-x.max());return e/e.sum()
def row(strings,y,size=32):
 return VGroup(*[txt(s,size,c).move_to([x,y,0]) for s,c,x in zip(strings,COLORS,[-2.5,0,2.5])])
def weighted_bar(p,y=-2.2):
 g=VGroup();left=-3.3
 for v,c in zip(p,COLORS):
  w=6.6*v;g.add(Rectangle(width=w,height=.45,stroke_width=0,fill_color=c,fill_opacity=.9).move_to([left+w/2,y,0]));left+=w
 return g
class SoftmaxAttentionFinale(Scene):
 def until(self,t):
  if self.time>t+.05:raise ValueError(f'Timing overrun {self.time}>{t}')
  if t>self.time:self.wait(t-self.time)
 def cue(self,i):
  self.until(CAPTIONS[i][0]);new=txt(CAPTIONS[i][1]).move_to(DOWN*5.85)
  self.play(FadeOut(self.sub),FadeIn(new),run_time=.2);self.sub=new
 def heading(self,s):self.play(Transform(self.head,txt(s,30,MINT).move_to(UP*3.65)),run_time=.3)
 def construct(self):
  self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.85);self.head=txt('점수 → 경쟁하는 비중',30,MINT).move_to(UP*3.65)
  episode=txt('09  /  Attention의 비중을 결정하는 함수',23,MINT).move_to(UP*4.65)
  self.add(txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85),txt('Softmax',66).move_to(UP*5.65),episode,self.head,self.sub)
  intro=VGroup(txt('점수',36,BLUE),txt('↓  Softmax',28,MUTED),txt('합이 1인 가중치',36,MINT)).arrange(DOWN,buff=.5).move_to(UP*.3)
  self.play(FadeIn(intro),run_time=.5)
  self.cue(1);self.heading('Attention에서 만나는 Softmax')
  self.cue(2);self.play(FadeOut(intro),run_time=.3)
  query=txt('Query',38,MINT).move_to(UP*2.6);keys=row(['Key 1','Key 2','Key 3'],.6,31)
  links=VGroup(*[Arrow([0,2.1,0],[x,1.1,0],buff=.08,color=c,stroke_width=2) for x,c in zip([-2.5,0,2.5],COLORS)])
  self.play(FadeIn(query),FadeIn(keys),Create(links),run_time=.6)
  self.cue(3)
  scores=row(['1','2','5'],-.7,40);scale=txt('점수 sᵢ = (q · kᵢ) / √dₖ',25,MUTED).move_to(DOWN*2.2)
  self.play(FadeIn(scores),FadeIn(scale),run_time=.5)
  self.cue(4);self.play(Indicate(keys[2]),Indicate(scores[2]),run_time=.7)
  self.cue(5)
  self.play(*[FadeOut(m) for m in [query,keys,links,scale]],scores.animate.move_to(UP*2),run_time=.4)
  arrow=txt('↓  Softmax',28,MUTED).move_to(UP*.8);weights=row(['0.017','0.047','0.936'],-.4,35)
  band=weighted_bar(soft([1,2,5]));note=txt('합 = 1 · 표시값은 반올림',23,MUTED).move_to(DOWN*3.3)
  self.play(FadeIn(arrow),FadeIn(weights),FadeIn(band),FadeIn(note),run_time=.6)
  self.cue(6);self.play(Indicate(weights),run_time=.6)
  self.cue(7)
  values=row(['× Value 1','× Value 2','× Value 3'],-1.35,26);self.play(FadeIn(values),run_time=.5)
  self.cue(8)
  self.play(*[FadeOut(m) for m in [scores,arrow,weights,band,note,values]],run_time=.3)
  formula=txt('출력 = Σᵢ pᵢ Vᵢ',43,MINT).move_to(UP*.7)
  expansion=txt('p₁V₁ + p₂V₂ + p₃V₃',34,GOLD).move_to(DOWN*1)
  self.play(FadeIn(formula),FadeIn(expansion),run_time=.5)
  self.cue(9);self.play(FadeOut(formula),FadeOut(expansion),run_time=.3);self.heading('Value 벡터의 가중합')
  trackers=[ValueTracker(v) for v in [1,2,5]]
  def current():return soft([t.get_value() for t in trackers])
  # Value coordinates in a two-dimensional example, shown with fixed axes.
  vectors=np.array([[-2.,-1.],[2.,-1.],[0.,2.]])
  ax=Axes(x_range=[-3,3,1],y_range=[-2,3,1],x_length=6.1,y_length=3.65,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1,'tip_width':.1,'tip_height':.1}).move_to(DOWN*.4)
  points=[ax.c2p(*v) for v in vectors]
  triangle=Polygon(*points,color=MUTED,stroke_width=1.5,fill_color=MINT,fill_opacity=.025)
  arrows=VGroup(*[Arrow(ax.c2p(0,0),pt,buff=0,color=c,stroke_width=2) for pt,c in zip(points,COLORS)])
  labels=VGroup(*[txt(s,24,c).next_to(pt,direction,buff=.13) for s,c,pt,direction in zip(['V₁','V₂','V₃'],COLORS,points,[LEFT,RIGHT,UP])])
  self.play(FadeIn(ax),Create(triangle),Create(arrows),FadeIn(labels),run_time=.7)
  outpoint=lambda:ax.c2p(*(current()@vectors))
  outarrow=always_redraw(lambda:Line(ax.c2p(0,0),outpoint(),color=INK,stroke_width=5))
  dot=always_redraw(lambda:Dot(outpoint(),color=INK,radius=.095))
  def numrow(y,probability=False):
   g=VGroup()
   for i,(x,c) in enumerate(zip([-2.35,0,2.35],COLORS)):
    lab=txt(('p' if probability else 's')+['₁','₂','₃'][i]+' =',22,c).move_to([x-.5,y,0])
    n=DecimalNumber(float(current()[i]) if probability else trackers[i].get_value(),mob_class=Text,num_decimal_places=3 if probability else 1,font_size=24,color=c).move_to([x+.5,y,0])
    n.add_updater(lambda m,i=i,probability=probability:m.set_value(float(current()[i]) if probability else trackers[i].get_value()))
    g.add(lab,n)
   return g
  sr=numrow(3.05);pr=numrow(2.4,True)
  dynbar=always_redraw(lambda:weighted_bar(current(),-3.45))
  legend=txt('흰 점: 출력 ΣpᵢVᵢ · 설명용 2차원 Value',23,INK).move_to(DOWN*2.8)
  sumlabel=txt('전체 비중 = 1',22,MUTED).move_to(DOWN*4.15)
  self.add(sr,pr,dynbar,legend,sumlabel)
  self.cue(10);self.add(outarrow,dot);self.play(Indicate(labels[2]),run_time=.6)
  self.cue(11);self.play(Indicate(labels[0]),Indicate(labels[1]),run_time=.6)
  self.cue(12);self.heading('한 점수의 변화가 전체 비중을 바꿉니다')
  self.cue(13);self.play(trackers[0].animate.set_value(6),run_time=4,rate_func=smooth)
  self.cue(14);self.play(Indicate(sumlabel),run_time=.6)
  self.cue(15);self.play(Indicate(dot),run_time=.6)
  self.cue(16);self.heading('차이가 만드는 가중치의 비율')
  self.play(*[t.animate.set_value(v) for t,v in zip(trackers,[1,2,5])],run_time=2)
  self.cue(17)
  ratio=txt('p₃ / p₁ = exp(s₃ − s₁)',29,GOLD).move_to(DOWN*4.15)
  self.play(FadeOut(sumlabel),FadeIn(ratio),run_time=.4)
  self.cue(18);self.play(Transform(ratio,txt('s₃ − s₁ = 5 − 1 = 4',29,GOLD).move_to(ratio)),run_time=.4)
  self.cue(19);self.play(Transform(ratio,txt('p₃ / p₁ = e⁴ ≈ 54.6배',29,GOLD).move_to(ratio)),run_time=.4)
  self.cue(20);self.heading('점수가 비슷하면, 비중도 나뉩니다')
  self.play(FadeOut(ratio),run_time=.2)
  self.play(*[t.animate.set_value(2) for t in trackers],run_time=3.5)
  self.cue(21)
  average=txt('출력 = (V₁ + V₂ + V₃) / 3',28,MINT).move_to(DOWN*4.15);self.play(FadeIn(average),run_time=.5)
  self.cue(22)
  visual=VGroup(ax,triangle,arrows,labels,outarrow,dot,sr,pr,dynbar,legend,average)
  for mob in visual.get_family():mob.clear_updaters()
  self.play(FadeOut(visual),run_time=.4);self.heading('정규화를 넘어, 비중을 결정합니다')
  flow=VGroup(txt('Query · Key',35,BLUE),txt('↓  상대적인 점수',28,MUTED),txt('Softmax',42,MINT),txt('↓  경쟁하는 가중치',28,MUTED),txt('Value의 가중합',35,GOLD)).arrange(DOWN,buff=.35).move_to(UP*.2)
  self.play(FadeIn(flow),run_time=.5)
  self.cue(23);self.play(Indicate(flow[2]),run_time=.6)
  self.cue(24);self.play(Indicate(flow[4]),run_time=.6)
  self.cue(25);self.play(FadeOut(flow),run_time=.3);self.heading('점수에서 관계로, 관계에서 표현으로')
  end=VGroup(txt('어떤 정보를',35,BLUE),txt('얼마나 반영할 것인가',35,GOLD),txt('Softmax',53,MINT)).arrange(DOWN,buff=.55).move_to(UP*.3)
  self.play(FadeIn(end),Transform(episode,txt('SOFTMAX  /  SERIES FINALE',24,MINT).move_to(episode)),run_time=.6)
  self.until(DURATION)
