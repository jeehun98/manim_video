"""First-person Manim poses for an untimed click-through draft."""
from pathlib import Path
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from manim import Scene, VGroup, Polygon, Rectangle, Line, WHITE, tempconfig
from visual_library.manim import DialogueBackground

CAPTIONS = ['', '', '', '', 'Training complete.',
            "Someday, I'll be a hero like Aldric.",
            'And protect this world, just like he did.']
COUNTS = [1, 2, 5, 2, 6, 2, 1]


def block(w, h, x, y, color):
    return Rectangle(width=w, height=h, stroke_width=0,
                     fill_color=color, fill_opacity=1).move_to([x, y, 0])


def pixel_caption(text):
    # Pillow's embedded bitmap font: exact English case, hard-edged square pixels.
    font = ImageFont.load_default_imagefont()
    image = Image.new('1', (font.getbbox(text)[2] + 2, 14))
    ImageDraw.Draw(image).text((0, 0), text, font=font, fill=1)
    image = image.crop(image.getbbox())
    pixels = np.array(image)
    result = VGroup()
    unit = .05
    for y, row in enumerate(pixels):
        x = 0
        while x < len(row):
            if not row[x]:
                x += 1
                continue
            end = x + 1
            while end < len(row) and row[end]:
                end += 1
            result.add(block((end-x)*unit, unit, (x+end)*unit/2, -y*unit, WHITE))
            x = end
    result.shift([-7.12 + .56 - result.get_left()[0],
                  -2.25 - .46 - result.get_top()[1], 0])
    result.set_z_index(101)
    return result


def sprite_layer(draw_sprite):
    # 160x90 logical pixels; nearest-neighbour enlargement preserves square dots.
    canvas = Image.new('RGBA', (160, 90))
    draw = ImageDraw.Draw(canvas)
    def point(p):
        return (round((p[0]+8)*10), round((4.5-p[1])*10))
    def polygon(points, color):
        draw.polygon([point(p) for p in points], fill=color)
    def line(points, color, width=1):
        draw.line([point(p) for p in points], fill=color, width=width)
    draw_sprite(polygon, line)
    # Native rectangles avoid image compositing differences between renderers.
    result = VGroup()
    pixels = np.array(canvas)
    for y,row in enumerate(pixels):
        x = 0
        while x < 160:
            if row[x,3] == 0:
                x += 1
                continue
            end = x+1
            while end < 160 and np.array_equal(row[end],row[x]):
                end += 1
            color = '#%02x%02x%02x' % tuple(row[x,:3])
            result.add(block((end-x)*.1,.1,-8+(x+end)*.05,4.5-(y+.5)*.1,color))
            x = end
    return result


def sword(pose):
    if pose == 'hit':
        h, t = np.array([4.4, -1.35, 0]), np.array([-2.0, 2.5, 0])
    elif pose == 'rest':
        h, t = np.array([6.7, -2.2, 0]), np.array([4.45, .8, 0])
    else:
        h, t = np.array([6.0, -1.2, 0]), np.array([2.7, 3.0, 0])
    d = (t-h)/np.linalg.norm(t-h)
    n = np.array([-d[1], d[0], 0])
    start = h+d*.23
    def draw(poly, line):
        # Dark pixel outline, two silver blade faces, brass crossguard and wrap.
        poly([h-d*.86+n*.19,h+n*.19,h-n*.19,h-d*.86-n*.19], '#211D2A')
        line([h-d*.73,h], '#795744', 3)
        for f in (.2,.4,.6):
            line([h-d*f-n*.11,h-d*f+n*.11], '#B2916C')
        poly([start+n*.30,t+d*.08,start-n*.30], '#242938')
        poly([start+n*.20,t,start], '#F3F4E8')
        poly([start,t,start-n*.20], '#929DAF')
        line([h-n*.59,h+n*.59], '#282633', 5)
        line([h-n*.49,h+n*.49], '#BDA267', 3)
        line([h-n*.43+d*.08,h+n*.43+d*.08], '#F2D99A')
        line([h-d*.8-n*.17,h-d*.8+n*.17], '#BDA267', 3)
    return sprite_layer(draw)


def wood(split=0):
    def draw(poly, line):
        if split == 0:
            poly([(-1.28,.05),(-1.28,2.45),(-.96,2.69),(.96,2.69),(1.28,2.45),(1.28,.05),(.98,-.17),(-.98,-.17)], '#2E2530')
            poly([(-1.15,.11),(-1.15,2.43),(1.15,2.43),(1.15,.11),(.92,-.04),(-.92,-.04)], '#80503B')
            poly([(-1.05,.12),(-1.05,2.35),(-.63,2.35),(-.63,-.03)], '#B0784C')
            poly([(.75,-.02),(.75,2.35),(1.15,2.35),(1.15,.11)], '#51392F')
            for x,y in [(-.85,1.9),(-.35,1.3),(.16,1.85),(.60,.9),(-.13,.5)]:
                line([(x,y+.25),(x,y),(x+.1,y-.1),(x+.1,y-.43)], '#DCAC70')
            poly([(-1.14,2.43),(-.89,2.59),(.89,2.59),(1.14,2.43),(.89,2.21),(-.89,2.21)], '#E0BB80')
            line([(-.78,2.41),(-.55,2.50),(.55,2.50),(.78,2.41),(.55,2.30),(-.55,2.30),(-.78,2.41)], '#9C6944')
            line([(-.35,2.4),(.35,2.4)], '#9C6944')
            return
        for side in (-1,1):
            center = np.array([side*.64,1.25,0])
            angle = -side*.23*split
            c,s = np.cos(angle),np.sin(angle)
            rotation = np.array([[c,-s,0],[s,c,0],[0,0,1]])
            def points(coords):
                return [rotation@np.array([x,y,0])+center+np.array([side*1.4*split,-.70*split,0]) for x,y in coords]
            # A short round log, bark with chipped corners and bright cut end.
            poly(points([(-.64,-1.3),(-.64,1.23),(-.45,1.44),(.43,1.44),(.64,1.2),(.64,-1.26),(.43,-1.42),(-.43,-1.42)]),'#2E2530')
            poly(points([(-.54,-1.23),(-.54,1.16),(.54,1.16),(.54,-1.20),(.35,-1.31),(-.34,-1.31)]),'#80503B')
            poly(points([(-.49,-1.14),(-.49,1.05),(-.21,1.05),(-.21,-1.25)]),'#B0784C')
            poly(points([(.30,-1.24),(.30,1.05),(.52,1.05),(.52,-1.17)]),'#51392F')
            for x,y in [(-.34,.7),(.04,.23),(-.12,-.75),(.37,-.4)]:
                line(points([(x,y+.30),(x,y),(x+.08,y-.12),(x+.08,y-.43)]),'#DCAC70')
            poly(points([(-.54,1.16),(-.35,1.35),(.34,1.35),(.54,1.16),(.35,.96),(-.34,.96)]),'#E0BB80')
            line(points([(-.31,1.15),(-.17,1.24),(.18,1.24),(.33,1.15),(.18,1.07),(-.16,1.07),(-.31,1.15)]),'#9C6944')
            line(points([(-.10,1.15),(.10,1.15)]),'#9C6944')
            if split:
                # Pale splintered inner face makes the split immediately readable.
                x=-side*.51
                line(points([(x,1.04),(x,-1.15)]),'#E0BB80',2)
    return sprite_layer(draw)


def pixel_label(text, center, unit=.05, color=WHITE):
    label = pixel_caption(text)
    label.scale(unit/.05).set_color(color).move_to(center).set_z_index(20)
    return label


def distant_world(stage):
    def draw(poly, line):
        stone = '#B8BCCB' if stage == 5 else '#555C70'
        roof = '#A7A0B2' if stage == 6 else '#353C4B'
        wall = '#6E7786' if stage == 6 else '#252D3A'
        # Village lies farther away than Aldric's small sword-bearing monument.
        for x,y,w in [(-1.0,2.7,.85),(.5,2.85,.7),(1.9,2.6,1.0),(3.4,2.8,.7),(4.6,2.65,.85)]:
            poly([(x-w,y-.6),(x-w,y+.05),(x+w,y+.05),(x+w,y-.6)],wall)
            poly([(x-w-.15,y+.05),(x,y+.65),(x+w+.15,y+.05)],roof)
            line([(x,y-.6),(x,y-.25)],'#CEC498' if stage==6 else '#454552',2)
        line([(-2.0,2.05),(5.6,2.05)], wall)
        x=-3.65
        poly([(x-.65,.1),(x-.65,.35),(x-.45,.35),(x-.45,.65),(x+.45,.65),(x+.45,.35),(x+.65,.35),(x+.65,.1)],stone)
        poly([(x-.30,.65),(x-.25,1.5),(x-.43,1.85),(x-.20,2.0),(x+.27,2.0),(x+.40,1.75),(x+.28,1.35),(x+.34,.65)],stone)
        poly([(x-.19,2.02),(x-.19,2.40),(x+.19,2.40),(x+.19,2.02)],stone)
        line([(x+.25,1.8),(x+.70,1.65),(x+.85,2.2)],stone,2)
        line([(x+.85,1.8),(x+.85,2.95)],stone,2)
        line([(x+.60,2.13),(x+1.08,2.13)],stone,2)
    return sprite_layer(draw).set_z_index(-10)


def charge(power):
    group=VGroup()
    color='#A8DDE8' if power==2 else '#FFE7A0'
    for i in range(7 if power==2 else 13):
        t=i/(6 if power==2 else 12)
        x,y=3.0+2.7*t,2.7-3.5*t
        size=.10 if power==2 else .18
        group.add(block(size,size,x+(-1)**i*.32,y,color))
    group.add(Line([2.7,3,0],[5.9,-1,0],color=color,
                   stroke_width=9 if power==2 else 19).set_opacity(.35))
    return group


def projectile(power, x):
    color='#A8DDE8' if power==2 else '#FFE7A0'
    scale=.62 if power==2 else .95
    shape=Polygon([x-.85*scale,1.3,0],[x,1.3+.95*scale,0],
                  [x+.85*scale,1.3,0],[x,1.3-.95*scale,0],
                  stroke_color=color,stroke_width=5,
                  fill_color='#18222C',fill_opacity=1)
    # A short trailing slash makes the flight direction readable.
    trail=Line([x+.7,1.3,0],[x+1.8,1.3,0],color=color,stroke_width=5)
    return VGroup(trail,shape,pixel_label(str(power),[x,1.3,0],.065,color))


class TrainingStill(Scene):
    stage=0
    frame=0

    def construct(self):
        s,f=self.stage,self.frame
        background=DialogueBackground(show_marker=False,grid_under_dialogue=True)
        background.dialogue.stretch_to_fit_width(14.24)
        background.dialogue.stretch_to_fit_height(1.92)
        background.dialogue.move_to([0,-3.21,0])
        self.add(background,distant_world(s))
        caption=CAPTIONS[s] if s!=4 or f==5 else ''
        self.add(pixel_caption('* '+caption))
        shattered=s>=5 or (s==4 and f>=3)
        target=wood(min(1,(f-2)*.5) if s==4 and f>=3 else (1 if shattered else 0))
        if s>=5:
            target.scale(.65).shift([0,-.65,0]).set_opacity(.4)
        cracked=s==3 or (s==2 and f>=3) or (s==4 and f<3)
        if cracked:
            target.add(Line([.15,2.13,0],[-.1,1.6,0],color='#241C25',stroke_width=6),
                       Line([-.1,1.6,0],[.2,1.25,0],color='#241C25',stroke_width=6))
        if s==2 and f==3:
            target.shift([.20,0,0]).rotate(-.045)
        self.add(target)
        pose='hit' if s in (2,4) and 1<=f<=4 else 'ready'
        if s>=6 or s==5 and f==1:
            pose='rest'
        self.add(sword(pose))
        if s in (0,1,3):
            equation='1 + 1 = ?' if s==0 else ('1 + 1 = 2' if s==1 else '2 + 2 = 4')
            self.add(pixel_label(equation,[4.6,3.65,0],.055))
        if s in (1,3) and f==1 or s in (2,4) and f==0:
            self.add(charge(2 if s in (1,2) else 4))
        if s in (2,4) and f in (1,2):
            self.add(projectile(2 if s==2 else 4,2.6 if f==1 else .0))
        if s==4 and f in (3,4):
            for i in range(8):
                self.add(block(.12,.12,(-1)**i*(.7+i*.18),1.8-(i%4)*.5,'#E0BB80'))


def render_stills():
    target=Path(__file__).parent/'frames_v4'
    target.mkdir(exist_ok=True)
    for stage,count in enumerate(COUNTS):
        for i in range(count):
            if len(sys.argv)>1 and (stage,i)!=(int(sys.argv[1]),int(sys.argv[2])):
                continue
            with tempconfig({'frame_width':16,'frame_height':9,
                             'pixel_width':1280,'pixel_height':720,
                             'save_last_frame':True,'write_to_movie':False,
                             'media_dir':str(ROOT/'media'/'training_draft'),
                             'verbosity':'ERROR'}):
                scene=TrainingStill()
                scene.stage,scene.frame=stage,i
                scene.render()
                camera=scene.renderer.camera
                camera.reset()
                camera.pixel_array_to_cairo_context.clear()
                camera.capture_mobjects(scene.mobjects)
                camera.get_image().save(target/f'{stage}_{i}.png')


if __name__=='__main__':
    render_stills()
