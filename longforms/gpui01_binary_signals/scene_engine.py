"""One voltage experiment, eight replaceable scenes, two intentional layouts."""
import os,json,textwrap
from bisect import bisect_right
from functools import lru_cache
from pathlib import Path
import numpy as np
from manim import *

R=Path(__file__).resolve().parent
VERT=os.environ.get('GPUI_LAYOUT','longform')=='shorts'
config.frame_width=9 if VERT else 16
config.frame_height=16 if VERT else 9
config.background_color='#080F1C'
INK='#EDF4FF';MUTED='#8B9CB5';BLUE='#4EA7FF';GREEN='#53D6AA';ORANGE='#FFA75E';RED='#FF6D7C';EDGE='#243249';PANEL='#101E31'
TIMING=json.loads((R/'timing.json').read_text(encoding='utf-8'))
MANIFEST=json.loads((R/'manifest.json').read_text(encoding='utf-8'))

def txt(s,size=30,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m

def pill(s,w=2.1,h=.7,color=BLUE,size=27):
 return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.14,fill_color=PANEL,fill_opacity=1,stroke_color=color,stroke_width=1.4),txt(s,size,color,w-.24))

@lru_cache(maxsize=128)
def voltage_label(hundredths):return txt(f'{hundredths/100:.2f} V',32,BLUE)

class BinaryScene(Scene):
 index=0
 def at(self,global_time):
  local=global_time-self.start
  if self.time>local+.04:raise RuntimeError(f'Scene {self.index+1}: {self.time} exceeds {local}')
  if local-self.time>.001:self.wait(local-self.time)
 def note(self,s,color=MUTED):
  self.notice.become(txt(s,25 if VERT else 24,color,7.7 if VERT else 14).move_to([0,-3.85 if VERT else -2.1,0]))
 def construct(self):
  m=MANIFEST[self.index];self.start=m['start'];self.end=m['end']
  top=7.2 if VERT else 3.88
  # Do not reveal the binary answer in the initial title.
  self.add(txt('GPU 개론  /  01',21,MUTED).move_to([0,top,0]))
  self.add(txt(m['title'],37 if VERT else 39,INK,7.9 if VERT else 14.5).move_to([0,top-.73,0]))
  self.notice=txt(' ',24).move_to([0,-3.85 if VERT else -2.1,0]);self.add(self.notice)
  # Exactly one caption object exists. Initialize it before the first rendered
  # frame; inactive future sentences must never start at their default opacity.
  starts=[row['start'] for row in TIMING]
  def caption_index():
   now=self.start+self.time
   i=bisect_right(starts,now+1e-7)-1
   return i if 0<=i<len(TIMING) and now<TIMING[i]['end']-1e-7 else -1
  def caption_text(i):
   s=TIMING[i]['text'] if i>=0 else ' '
   s='\n'.join(textwrap.wrap(s,width=26 if VERT else 52,break_long_words=True))
   return txt(s,30 if VERT else 29,INK,7.55 if VERT else 14.2).move_to([0,-5.73 if VERT else -3.19,0]).set_z_index(31)
  self.active_caption=caption_index()
  self.caption=caption_text(self.active_caption)
  def update_caption(mob):
   i=caption_index()
   if i!=self.active_caption:
    mob.become(caption_text(i));mob.set_z_index(31);self.active_caption=i
  self.caption.add_updater(update_caption)
  # Opaque dedicated subtitle region also separates captions from diagram notes.
  panel=Rectangle(width=8.2 if VERT else 15,height=2.25 if VERT else 1.40,stroke_width=0,fill_color=config.background_color,fill_opacity=1).move_to([0,-5.73 if VERT else -3.19,0]).set_z_index(29)
  self.add(panel,self.caption)
  y=-7.24 if VERT else -4.1;x=3.9 if VERT else 7.3
  base=Line([-x,y,0],[x,y,0],color=EDGE,stroke_width=2)
  progress=base.copy().set_color(BLUE)
  progress.add_updater(lambda mob:mob.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/113)))
  self.add(base,progress)
  self.add(txt(f'{self.index+1:02} / 08',17,MUTED).move_to([x-.55,y+.27,0]))
  [self.signal,self.levels,self.noise,self.binary,self.tradeoff,self.combinations,self.bit,self.processing][self.index]()
  self.at(self.end)

 def graph(self):
  # Identical physical voltage range and graph position for scenes 1–5.
  self.gx=-2.8 if VERT else -5.1;self.gy=-1.65 if VERT else -1.4
  self.gw=5.7 if VERT else 10.1;self.gh=5.1 if VERT else 3.2
  self.p=lambda x,v:np.array([self.gx+x*self.gw,self.gy+v/.4*self.gh,0])
  axes=VGroup(Line(self.p(0,0),self.p(0,.4),color=MUTED,stroke_width=1.5),Line(self.p(0,0),self.p(1,0),color=MUTED,stroke_width=1.5))
  labels=VGroup(txt('Voltage',22,MUTED).next_to(axes[0],UP,buff=.16),txt('Time',22,MUTED).next_to(axes[1],DOWN,buff=.14).align_to(axes[1],RIGHT))
  ticks=VGroup()
  for v in [.1,.2,.3,.4]:
   ticks.add(Line(self.p(0,v),self.p(1,v),color=EDGE,stroke_width=.8),txt(f'{v:.1f} V',17,MUTED).move_to(self.p(0,v)+LEFT*.49))
  return VGroup(axes,labels,ticks)

 def wave(self,level=.2,amp=0,color=BLUE,phase=0):
  pts=[self.p(x,level+amp*(.70*np.sin(47*x+phase)+.30*np.sin(89*x+phase))) for x in np.linspace(.02,.96,150)]
  return VMobject(color=color,stroke_width=3).set_points_as_corners(pts)

 def dense(self,more=False):
  # Extra nominal levels stay outside the 0.10/0.20 pair: 0.15 V is a decision
  # boundary, never a simultaneously valid nominal level in this decoder.
  ls=VGroup();vals=[.05,.1,.2,.3,.35] if more else [.1,.2,.3]
  for v in vals:
   ls.add(DashedLine(self.p(.02,v),self.p(.98,v),color=BLUE,stroke_width=1,dash_length=.10).set_opacity(.55))
  return ls

 def bands(self,labels=True):
  out=VGroup()
  for lo,hi,c in [(0,.18,BLUE),(.26,.4,GREEN)]:
   rect=Rectangle(width=self.gw,height=(hi-lo)/.4*self.gh,stroke_width=0,fill_color=c,fill_opacity=.14).move_to((self.p(0,lo)+self.p(1,hi))/2)
   out.add(rect)
  for v in [.18,.26]:out.add(DashedLine(self.p(0,v),self.p(1,v),color=MUTED,stroke_width=1.3))
  if labels:
   out.add(txt('LOW',25,BLUE).move_to(self.p(.86,.08)),txt('HIGH',25,GREEN).move_to(self.p(.86,.32)),txt('판정 보장 밖',18,MUTED).move_to(self.p(.78,.22)))
  return out

 def signal(self):
  origin=np.array([0,1.2 if VERT else .4,0]);dot=Dot(origin,radius=.08,color=BLUE)
  glow=Dot(origin,radius=.23,color=BLUE,fill_opacity=.14)
  line=Line(origin+LEFT*.02,origin+RIGHT*.02,color=BLUE,stroke_width=3)
  self.play(FadeIn(glow),FadeIn(dot),run_time=.6)
  self.play(Transform(line,Line(origin+LEFT*(2.7 if VERT else 5),origin+RIGHT*(2.7 if VERT else 5),color=BLUE,stroke_width=3)),run_time=2)
  self.at(4);g=self.graph();w=self.wave(.2,.09)
  self.play(FadeOut(glow),FadeOut(dot),FadeIn(g),ReplacementTransform(line,w),run_time=1.5)
  self.at(7)
  value=ValueTracker(.2)
  guide=always_redraw(lambda:DashedLine(self.p(0,value.get_value()),self.p(.65,value.get_value()),color=BLUE,stroke_width=1.4))
  point=always_redraw(lambda:Dot(self.p(.65,value.get_value()),radius=.075,color=BLUE))
  readout=always_redraw(lambda:voltage_label(int(round(value.get_value()*100))).copy().move_to([1.3,4.3 if VERT else 2.55,0]))
  self.add(guide,point,readout)
  self.play(value.animate.set_value(.31),run_time=1.5);self.play(value.animate.set_value(.12),run_time=1.5);self.play(value.animate.set_value(.2),run_time=1.5)
  self.note('연속적으로 변하는 물리적 신호')

 def levels(self):
  graph=self.graph()
  initial=self.wave(.2,.09)
  self.add(graph,initial);self.note('전압에 의미를 부여하는 가상의 규칙')
  refs=VGroup();mapping=VGroup()
  for j,(v,n) in enumerate([(.1,1),(.2,2),(.3,3)]):
   refs.add(DashedLine(self.p(.02,v),self.p(.96,v),color=BLUE,stroke_width=1.2))
   mapping.add(pill(f'{v:.1f} V → {n}',w=2.25 if VERT else 2.5,h=.65,size=24))
  mapping.arrange(DOWN if VERT else RIGHT,buff=.12 if VERT else .35).move_to([0,4.55 if VERT else 2.5,0])
  self.play(LaggedStart(*[FadeIn(x) for x in refs],lag_ratio=.3),LaggedStart(*[FadeIn(x) for x in mapping],lag_ratio=.3),run_time=3)
  self.at(16)
  self.play(FadeOut(initial),run_time=.4)
  value=ValueTracker(.1)
  current=always_redraw(lambda:self.wave(value.get_value()))
  point=always_redraw(lambda:Dot(self.p(.65,value.get_value()),color=BLUE,radius=.09))
  self.add(current,point)
  for v,j in [(.1,0),(.2,1),(.3,2)]:
   self.play(value.animate.set_value(v),Indicate(mapping[j],color=GREEN),run_time=1.6)
  self.at(23)
  more=self.dense(True)
  self.play(FadeIn(more),run_time=1)
  self.note('구분하는 수준이 늘면, 표현할 수 있는 상태도 증가',BLUE)
  self.play(value.animate.set_value(.2),run_time=1)

 def noise(self):
  self.add(self.graph(),self.dense(True));ref=self.wave(.2);self.add(ref)
  self.note('기준 0.20 V  /  숫자 2를 전달')
  amp=ValueTracker(0);phase=ValueTracker(0)
  def noise_trace():
   xs=sorted(set(list(np.linspace(.02,.96,150))+[.62]))
   return VMobject(color=ORANGE,stroke_width=3).set_points_as_corners([self.p(x,.2-amp.get_value()*np.cos(2*np.pi*5*(x-.62))) for x in xs])
  noisy=always_redraw(noise_trace)
  self.add(noisy)
  self.play(amp.animate.set_value(.018),phase.animate.set_value(2),run_time=2)
  self.at(31)
  # The decoder chooses nearest 0.1-V level; boundary 0.15 V separates 1 and 2.
  bound=DashedLine(self.p(0,.15),self.p(1,.15),color=RED,stroke_width=2)
  bound_label=txt('판정 경계 0.15 V',20,RED).next_to(bound,DOWN,buff=.1).align_to(bound,RIGHT)
  self.play(FadeIn(bound),FadeIn(bound_label),amp.animate.set_value(.035),phase.animate.set_value(5),run_time=2)
  result=always_redraw(lambda:pill('판정: 1' if .2-amp.get_value()<.15 else '판정: 2',w=2.3,color=RED if .2-amp.get_value()<.15 else BLUE).move_to([0,4.35 if VERT else 2.5,0]))
  self.add(result)
  self.at(36)
  point=always_redraw(lambda:Dot(self.p(.62,.2-amp.get_value()),radius=.10,color=ORANGE))
  self.add(point)
  self.play(amp.animate.set_value(.03),run_time=1.3)
  self.note('흔들려도 경계 안에서는 같은 값으로 판정',ORANGE)
  self.at(38)
  self.play(amp.animate.set_value(.07),run_time=1.2)
  self.play(Flash(point,color=RED,flash_radius=.35),run_time=.7)
  self.note('0.13 V < 0.15 V  →  인접 값으로 오인식',RED)

 def binary(self):
  self.add(self.graph());dense=self.dense(True);oldwave=self.wave(.2,.075,ORANGE,8)
  self.add(dense,oldwave);self.note('같은 전압 범위에서 구분할 상태 수를 줄이면?')
  self.at(44)
  self.play(dense.animate.set_opacity(.2),oldwave.animate.set_opacity(.2),run_time=1.5)
  clean=VGroup(self.wave(.1),self.wave(.3,color=GREEN))
  self.play(FadeIn(clean),run_time=1)
  self.at(50)
  bands=self.bands(False);self.play(FadeOut(dense),FadeOut(oldwave),FadeIn(bands),run_time=1.6)
  self.at(53)
  labels=VGroup(txt('LOW',27,BLUE).move_to(self.p(.85,.08)),txt('HIGH',27,GREEN).move_to(self.p(.85,.32)),txt('판정 보장 밖',18,MUTED).move_to(self.p(.77,.22)))
  self.play(FadeIn(labels),run_time=.7)
  self.at(55)
  # Same peak negative error as before (-0.07 V), around a better-separated nominal level.
  amp=ValueTracker(.03)
  point=always_redraw(lambda:Dot(self.p(.62,.1-amp.get_value()),radius=.09,color=BLUE))
  def stable_trace():
   xs=sorted(set(list(np.linspace(.02,.96,150))+[.62]))
   return VMobject(color=BLUE,stroke_width=3).set_points_as_corners([self.p(x,.1-amp.get_value()*np.cos(2*np.pi*5*(x-.62))) for x in xs])
  noisy=always_redraw(stable_trace);status=pill('LOW 유지',w=2.6,color=BLUE).move_to([0,4.35 if VERT else 2.5,0])
  self.play(FadeIn(noisy),FadeIn(status),FadeIn(point),run_time=.6)
  self.play(amp.animate.set_value(.07),run_time=1.1);self.play(amp.animate.set_value(.02),run_time=1.1);self.play(amp.animate.set_value(.065),run_time=1.1)
  self.note('변동을 허용하는 여유 증가 · 큰 잡음에는 오류 가능')

 def tradeoff(self):
  self.add(self.graph(),self.bands(),self.wave(.1,.065,BLUE,8),self.wave(.3,color=GREEN))
  self.note('안정적인 구분 ↔ 한 신호의 표현력')
  candidate=DashedLine(self.p(.03,.2),self.p(.96,.2),color=ORANGE,stroke_width=2)
  marker=pill('상태를 더 넣으면?',w=3.5,color=ORANGE,size=25).move_to([0,4.35 if VERT else 2.5,0])
  self.at(62);self.play(FadeIn(candidate),FadeIn(marker),run_time=.7)
  self.play(candidate.animate.set_opacity(.15),Transform(marker,pill('한 신호 · 두 상태',w=3.5,color=INK,size=25).move_to(marker)),run_time=.7)

 def combo_grid(self,n):
  combos=VGroup();cols=2 if n<=3 else 4
  if not VERT:cols=2 if n==1 else 4
  rows=int(np.ceil(2**n/cols));cellw=3.15 if VERT and cols==2 else (1.68 if VERT else 2.6)
  h=.66 if n==4 else .85
  for i in range(2**n):
   bits=f'{i:0{n}b}';cells=VGroup()
   step=min(.52,(cellw-.2)/n)
   for b in bits:
    c=BLUE if b=='0' else GREEN
    cells.add(VGroup(RoundedRectangle(width=step-.05,height=.50,corner_radius=.07,stroke_color=c,stroke_width=1.1,fill_color=c,fill_opacity=.12),txt(b,23,c)))
   cells.arrange(RIGHT,buff=.05)
   combos.add(cells)
  combos.arrange_in_grid(rows=rows,cols=cols,buff=(.35 if VERT else .48,.35 if n==4 else .65)).move_to([0,1.05 if VERT else .30,0])
  return combos

 def combinations(self):
  self.note('신호 하나를 추가하면 기존의 모든 조합이 두 갈래로')
  old=self.combo_grid(1)
  summary=txt('신호 1개  ·  2가지 조합',32,INK,7.5).move_to([0,4.5 if VERT else 2.35,0])
  self.play(FadeIn(old),FadeIn(summary),run_time=.8)
  under=VGroup(txt('LOW',22,BLUE).next_to(old[0],DOWN,buff=.2),txt('HIGH',22,GREEN).next_to(old[1],DOWN,buff=.2))
  self.play(FadeIn(under),run_time=.5)
  self.at(69);self.play(FadeOut(under),run_time=.2)
  for n,t in [(2,69.2),(3,74),(4,77)]:
   self.at(t);new=self.combo_grid(n)
   lines=VGroup(*[Line(old[i//2].get_center(),new[i].get_center(),color=BLUE if i%2==0 else GREEN,stroke_width=1.1,stroke_opacity=.45) for i in range(2**n)])
   newsummary=txt(f'신호 {n}개  ·  {2**n}가지 조합',32,INK,7.5).move_to(summary)
   self.play(FadeIn(lines),Transform(summary,newsummary),*[TransformFromCopy(old[i//2],new[i]) for i in range(2**n)],run_time=1.1)
   self.remove(old,*list(old));self.add(new)
   self.play(FadeOut(lines),run_time=.25);old=new
  equation=txt('2 × 2 × 2 × 2 = 16   →   2ⁿ',31,BLUE,7.4 if VERT else 13).move_to([0,-2.5 if VERT else -1.65,0])
  self.play(FadeIn(equation),run_time=.6)

 def bit(self):
  left=pill('LOW',w=2.7,h=1.35,color=BLUE,size=39);right=pill('HIGH',w=2.7,h=1.35,color=GREEN,size=39)
  pair=VGroup(left,right).arrange(RIGHT,buff=.65).move_to([0,2.2 if VERT else .95,0]);self.add(pair)
  self.note('論理 상태는 전압의 유효 범위에 대응'.replace('論理','논리'))
  self.play(Transform(left,pill('0',w=2.7,h=1.35,color=BLUE,size=58).move_to(left)),Transform(right,pill('1',w=2.7,h=1.35,color=GREEN,size=58).move_to(right)),run_time=1.3)
  name=txt('Binary Digit',35,INK).move_to([0,-.1 if VERT else -.7,0]);self.play(FadeIn(name),run_time=.7)
  self.at(85);self.play(Transform(name,txt('Bit',48,INK).move_to(name)),run_time=.8)
  small=txt('두 상태 중 하나를 나타내는 정보의 단위',23,MUTED,7.5).next_to(name,DOWN,buff=.4);self.play(FadeIn(small),run_time=.5)
  self.at(88)
  self.play(FadeOut(pair),FadeOut(name),FadeOut(small),run_time=.5)
  # Revisit the same experiment, abstracted into a compact voltage ruler.
  a=VGroup(txt('하나의 신호',26,MUTED),txt('촘촘한 전압 수준',29,BLUE)) .arrange(DOWN,buff=.3)
  ruler=VGroup(*[Line(LEFT*1.5,RIGHT*1.5,color=BLUE,stroke_width=1.3).shift(UP*(j-.5)*.20) for j in range(6)])
  a.add(ruler.next_to(a,DOWN,buff=.4))
  b=VGroup(txt('여러 신호',26,MUTED),txt('구분하기 쉬운 두 상태',29,GREEN)).arrange(DOWN,buff=.3)
  bits=VGroup(*[pill(c,.8,.85,BLUE if c=='0' else GREEN,30) for c in '0101']).arrange(RIGHT,buff=.16);b.add(bits.next_to(b,DOWN,buff=.4))
  if VERT:a.move_to([0,3.1,0]);b.move_to([0,-.5,0])
  else:a.move_to([-3.9,.65,0]);b.move_to([3.9,.65,0])
  arrow=Arrow(a.get_bottom() if VERT else a.get_right(),b.get_top() if VERT else b.get_left(),color=MUTED,buff=.35)
  self.play(FadeIn(a),GrowArrow(arrow),FadeIn(b),run_time=1.2)
  self.note('0 / 1은 정확한 0 V / 1 V를 뜻하지 않습니다')
  self.at(95)
  self.play(FadeOut(a),FadeOut(b),FadeOut(arrow),run_time=.5)
  end=VGroup(txt('적은 상태 × 여러 신호',38,INK,7.3),txt('다양한 정보 표현',36,GREEN,7.3)).arrange(DOWN,buff=.5).move_to([0,1 if VERT else .5,0])
  self.play(FadeIn(end),run_time=.7)

 def processing(self):
  bits=VGroup(*[pill(c,.9,1.05,BLUE if c=='0' else GREEN,35) for c in '0101']).arrange(RIGHT,buff=.13).move_to([0,1.7 if VERT else .5,0])
  self.add(bits);self.note('정보를 표현하는 방법을 얻었습니다')
  self.at(102)
  box=VGroup(RoundedRectangle(width=3.3,height=2.3,corner_radius=.2,stroke_color=MUTED,fill_color=PANEL,fill_opacity=1),txt('?',74,INK))
  if VERT:
   self.play(bits.animate.scale(.85).move_to([0,3.65,0]),run_time=.7);box.move_to([0,.55,0]);arrow=Arrow(bits.get_bottom(),box.get_top(),buff=.18,color=BLUE)
   out=DashedLine(box.get_bottom()+DOWN*.12,box.get_bottom()+DOWN*1.45,color=MUTED)
  else:
   self.play(bits.animate.scale(.8).move_to([-5,.4,0]),run_time=.7);box.move_to([.2,.4,0]);arrow=Arrow(bits.get_right(),box.get_left(),buff=.18,color=BLUE)
   out=DashedLine(box.get_right()+RIGHT*.12,box.get_right()+RIGHT*2.7,color=MUTED)
  self.play(FadeIn(box),GrowArrow(arrow),Create(out),run_time=1.3)
  self.note('입력에 따라 새로운 출력을 만드는 장치')
  for _ in range(2):
   d=Dot(arrow.get_start(),radius=.06,color=BLUE);self.add(d);self.play(MoveAlongPath(d,arrow),run_time=.7);self.remove(d)
  self.at(108);self.play(box[1].animate.scale(1.28).set_color(BLUE),run_time=1.5)
  self.note('표현에서 계산으로')
  self.at(112.4)
  self.play(FadeOut(bits),FadeOut(box),FadeOut(arrow),FadeOut(out),run_time=.6)
