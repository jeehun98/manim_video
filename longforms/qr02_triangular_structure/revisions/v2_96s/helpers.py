"""Space → inner product → matrix entry, using a common 3D model."""
from base import *
from base import QRBase as SharedBase
RED='#FF777E'
VALUES=[['r₁₁','r₁₂','r₁₃'],['0','r₂₂','r₂₃'],['0','0','r₃₃']]
class Helpers(SharedBase):
    def original(self,indices=(0,1,2),opacity=1):
        for j in indices:self.put(self.vec([A1,A2,A3][j],INK,['a₁','a₂','a₃'][j],opacity=opacity))
    def matrix(self,known=(),focus=None,all_known=False,numeric=False):
        c=np.array([0.,-2.55,0]) if SHORT else np.array([3.65,.15,0])
        dx=1.32;dy=.7
        cells={};g=VGroup()
        vals=[['√2','√2','3/√2'],['0','√2','1/√2'],['0','0','2']] if numeric else VALUES
        for row in range(3):
            for col in range(3):
                s=vals[row][col] if all_known or (row,col) in known else '?'
                color=RED if row>col and s=='0' else INK
                cell=label(s,29,color,1.05).move_to(c+[(col-1)*dx,(1-row)*dy,0])
                if focus is not None and col!=focus:cell.set_opacity(.35)
                cells[row,col]=cell;g.add(cell)
        for x in [-2.05,2.05]:
            g.add(Line(c+[x,-1.12,0],c+[x,1.12,0],color=MUTED,stroke_width=2))
            inward=.16 if x<0 else -.16
            g.add(Line(c+[x,-1.12,0],c+[x+inward,-1.12,0],color=MUTED),Line(c+[x,1.12,0],c+[x+inward,1.12,0],color=MUTED))
        g.add(label('R =',28).move_to(c+[-2.65,1.45,0]))
        for j in range(3):g.add(label(['a₁','a₂','a₃'][j],20,MUTED).move_to(c+[(j-1)*dx,1.45,0]))
        for j,col in enumerate([BLUE,GREEN,ORANGE]):g.add(label(['q₁','q₂','q₃'][j],20,col).move_to(c+[-2.45,(1-j)*dy,0]))
        self.put(g);return g,cells
    def formula(self,s,note='',color=INK):
        pos=[0,-4.45,0] if SHORT else [3.65,-1.75,0]
        eq=label(s,29,color,8 if SHORT else 6.5).move_to(pos);self.put(eq)
        if note:self.put(label(note,21,MUTED,8 if SHORT else 6.5).next_to(eq,DOWN,buff=.28))
        return eq
    def link(self,cell,source=ORIGIN):
        arc=Arrow(self.proj(source),cell.get_center(),buff=.17,color=PURPLE,stroke_width=2,max_tip_length_to_length_ratio=.07)
        self.animate(GrowArrow(arc),d=.45);self.animate(Indicate(cell,color=RED,scale_factor=1.3),d=.45)
        self.remove(arc)
    def zeros(self,cells,which):
        for k in which:
            old=cells[k];new=label('0',29,RED).move_to(old)
            self.animate(Transform(old,new),d=.35);self.link(old)
            self.animate(old.animate.set_color(MUTED),d=.2)
    def mark(self,u,v):self.put(self.rightmark(ORIGIN,u,v))
    def grid3(self):
        g=VGroup()
        for z in [-.8,.8,1.8]:
            for t in [-1,0,1,2]:
                g.add(Line(self.proj((t,-1,z)),self.proj((t,2,z)),color=PURPLE,stroke_opacity=.17,stroke_width=1),Line(self.proj((-1,t,z)),self.proj((2,t,z)),color=PURPLE,stroke_opacity=.17,stroke_width=1))
        for x,y in [(-1,-1),(-1,2),(2,-1),(2,2)]:g.add(Line(self.proj((x,y,-.8)),self.proj((x,y,1.8)),color=PURPLE,stroke_opacity=.25,stroke_width=1))
        return g
