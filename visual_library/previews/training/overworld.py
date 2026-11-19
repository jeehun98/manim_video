"""Third-person tile-map training preview; no final video timing."""
from pathlib import Path
import sys
from scene import (ROOT, CAPTIONS, COUNTS, sprite_layer, pixel_caption,
                   pixel_label, block)
from manim import Scene, VGroup, Line, WHITE, tempconfig
from visual_library.manim import DialogueBackground


def map_sprite():
    def draw(poly,line):
        def rect(x,y,w,h,c):
            poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],c)
        rect(-8,-4.5,16,9,'#55765A')
        for row in range(6):
            for col in range(13):
                x,y=-7.6+col*1.2,-2+row*1.1
                if (col+row)%3==0:
                    line([(x,y),(x+.1,y+.15),(x+.2,y)],'#769268')
        # Continuous paths and an open practice clearing.
        rect(-3.9,-2.3,7.8,4.1,'#B9AB83')
        rect(-.55,1.6,1.1,2.9,'#B9AB83')
        rect(3.3,2.15,4.7,.9,'#B9AB83')
        for x,y in [(-3.5,-1.8),(-2.4,.9),(2.7,-1.4),(1.8,1.3),(-.3,3.7)]:
            line([(x,y),(x+.2,y)],'#9B906F')
        # Short fence leaves a doorway facing north.
        for x in [-3.8,-2.9,-2,2,2.9,3.8]:
            rect(x,1.65,.12,.6,'#574E42')
        line([(-3.8,1.95),(-2,1.95)],'#D1BC86',2)
        line([(2,1.95),(3.9,1.95)],'#D1BC86',2)
        def tree(x,y):
            rect(x-.14,y-.55,.28,.7,'#5B493B')
            poly([(x-.7,y-.1),(x-.7,y+.6),(x-.4,y+.9),(x+.4,y+.9),(x+.7,y+.6),(x+.7,y-.1),(x+.4,y-.35),(x-.4,y-.35)],'#294D43')
            poly([(x-.5,y+.1),(x-.5,y+.6),(x-.2,y+.8),(x+.35,y+.8),(x+.5,y+.4),(x+.2,y+.1)],'#6F9260')
            line([(x-.3,y+.55),(x+.05,y+.65)],'#9CAF77',2)
        for x,y in [(-6.5,3.2),(-5,3.2),(-6.7,1.3),(-6.5,-.6),(6.6,.5),(6.7,-1.3),(4.9,-.9)]:
            tree(x,y)
        # One small original village house, viewed from above.
        rect(3.5,2.7,2.7,1.1,'#D8CEAA')
        rect(4.65,2.7,.45,.8,'#665B51')
        poly([(3.2,3.65),(3.65,4.35),(6.05,4.35),(6.5,3.65)],'#624F5B')
        line([(3.5,3.8),(6.2,3.8)],'#A07678',2)
        rect(3.85,2.95,.45,.4,'#687D87')
        rect(5.45,2.95,.45,.4,'#687D87')
        # Aldric's modest monument sits along the north path.
        rect(-.55,2.8,1.1,.35,'#606B72')
        rect(-.4,3.1,.8,.35,'#AAB3AE')
        rect(-.22,3.45,.44,.55,'#BFC7B9')
        rect(-.2,4,.4,.35,'#BFC7B9')
        line([(.2,3.8),(.55,3.7),(.55,4.3)],'#D6DBC5',2)
    return sprite_layer(draw).set_z_index(-50)


def player(x,y,back=False,step=0,attack=False):
    def draw(poly,line):
        def rect(a,b,w,h,c):
            poly([(x+a,y+b),(x+a+w,y+b),(x+a+w,y+b+h),(x+a,y+b+h)],c)
        rect(-.35,-.25,.8,.15,'#48554B')
        rect(-.23,-.2,.19,.3,'#303C4B');rect(.12,-.2+step*.08,.19,.3,'#303C4B')
        rect(-.3,.06,.65,.42,'#708EA0');rect(-.2,.12,.45,.12,'#D2BD83')
        rect(-.35,.45,.75,.5,'#423E45');rect(-.23,.42,.5,.32,'#E1BD95')
        rect(-.4,.8,.85,.25,'#9B6670');rect(-.27,1.03,.58,.12,'#BF8C87')
        if back:
            rect(-.27,.45,.57,.35,'#51434A')
        else:
            rect(.1,.59,.08,.08,'#30333C')
        if not back:
            if attack:
                line([(.4+x,.35+y),(1.35+x,.70+y)],'#E8E6CE',2)
            else:
                line([(.42+x,.2+y),(.75+x,.8+y)],'#E8E6CE',2)
            line([(.3+x,.35+y),(.58+x,.2+y)],'#BBA16E',2)
    return sprite_layer(draw)


class OverworldStill(Scene):
    stage=0
    frame=0
    def construct(self):
        s,f=self.stage,self.frame
        bg=DialogueBackground(show_marker=False,grid_under_dialogue=True)
        bg.dialogue.stretch_to_fit_width(14.24).stretch_to_fit_height(1.92).move_to([0,-3.21,0])
        self.add(bg,map_sprite())
        x,y=-1.2,-.1
        if s==5:
            x,y=-1.2+f*.6,-.1+f*.6
        elif s==6:
            x,y=0,1.15
        self.add(player(x,y,back=s>=5,step=f%2,attack=s in (2,4) and f in (1,2)))
        caption=CAPTIONS[s] if s!=4 or f==5 else ''
        self.add(pixel_caption('* '+caption))
        if s in (0,1,3):
            eq='1 + 1 = ?' if s==0 else ('1 + 1 = 2' if s==1 else '2 + 2 = 4')
            label=pixel_label(eq,[x+.6,y+2.0,0],.045)
            backing=block(label.width+.5,.65,x+.6,y+2.,'#263C39').set_z_index(19)
            self.add(backing,label)
        power=2 if s in (1,2) else 4
        color='#BCEDF0' if power==2 else '#FFE2A2'
        if s in (1,3) and f==1 or s in (2,4) and f==0:
            for i in range(4 if power==2 else 8):
                self.add(block(.1,.1,x+.6+((i%3)-1)*.24,y+.5+(i//3)*.28,color))
        if s in (2,4) and 1<=f<=3:
            px=x+1.0+f*.85
            for i in range(3 if power==2 else 5):
                self.add(block(.14,.16,px+(i%2)*.15,y+.1+i*.17,color))
            self.add(pixel_label(str(power),[px,y+.65,0],.06,color))
        # No target reaction: arithmetic power itself is the focus.
        if s==5:
            self.add(pixel_label('ALDRIC',[0,2.52,0],.025,'#E8E6CE'))


def render_stills():
    out=Path(__file__).parent/'frames_overworld'
    out.mkdir(exist_ok=True)
    for s,count in enumerate(COUNTS):
        for f in range(count):
            if len(sys.argv)>1 and (s,f)!=(int(sys.argv[1]),int(sys.argv[2])):
                continue
            with tempconfig({'frame_width':16,'frame_height':9,'pixel_width':1280,'pixel_height':720,
                             'save_last_frame':True,'write_to_movie':False,'verbosity':'ERROR',
                             'media_dir':str(ROOT/'media'/'training_overworld')}):
                scene=OverworldStill();scene.stage,scene.frame=s,f;scene.render()
                camera=scene.renderer.camera;camera.reset();camera.pixel_array_to_cairo_context.clear()
                camera.capture_mobjects(scene.mobjects);camera.get_image().save(out/f'{s}_{f}.png')

if __name__=='__main__':
    render_stills()
