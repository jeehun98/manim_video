"""Caption timing and reusable documentary staging; layout is supplied by the episode."""
from manim import *
from quantum_series.shared.theme import text,p,INK,MUTED

def wrap(s,limit):
    rows=[];line=''
    for word in s.split():
        if line and len(line)+len(word)+1>limit:rows.append(line);line=word
        else:line=(line+' '+word).strip()
    return '\n'.join(rows+[line])
class ChapterScene(Scene):
    offset=0
    def setup(self):
        self.L=self.layout;self.body=VGroup();self.caption=None;self.heading=None
        self.add(text(self.brand,y=self.L.brand_y,size=18,color=MUTED))
        y=6.65 if self.L.portrait else 3.5;w=7.6 if self.L.portrait else 14.4
        self.add(Line(p(-w/2,y),p(w/2,y),color=MUTED,stroke_width=1,stroke_opacity=.3))
    def to(self,target):
        dt=target-self.offset-self.time
        if dt<-.018:raise RuntimeError(f'Timing overrun {self.offset+self.time:.3f} > {target}')
        frames=round(dt*30)
        if frames>0:self.wait((frames+1e-5)/30)
    def cue(self,i):
        s=self.script['sentences'][i];self.to(s['start'])
        if self.caption:self.remove(self.caption)
        self.caption=text(wrap(s['text'],26 if self.L.portrait else 62),y=self.L.caption_y,size=24 if self.L.portrait else 25,width=7.6 if self.L.portrait else 14.1)
        self.add(self.caption)
        h=text(s['heading'],y=self.L.heading_y,size=32,width=self.L.body_width)
        if self.heading:self.play(Transform(self.heading,h),run_time=.25)
        else:self.heading=h;self.play(FadeIn(h),run_time=.25)
    def show(self,*objects,run_time=.4):
        self.body.add(*objects);self.play(*[FadeIn(o) for o in objects],run_time=run_time)
    def clear_body(self):
        if len(self.body):
            for o in self.body.get_family():o.clear_updaters()
            self.play(FadeOut(self.body),run_time=.25)
        self.body=VGroup()
    def note(self,s):return text(wrap(s,42 if self.L.portrait else 95),y=-4.15 if self.L.portrait else -2.7,size=17,color=MUTED,width=self.L.body_width)
    def info(self,s,color=INK):return text(s,*self.L.info[:2],size=27,color=color,width=7 if self.L.portrait else 6)
