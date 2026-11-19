"""Minimal black initial screen. Independent of earlier training storyboards."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from manim import Scene, Rectangle, Line, Text, VGroup, tempconfig
from visual_library.manim import DialogueBackground

class InitialScreen(Scene):
    show_equation=False
    def construct(self):
        background=DialogueBackground(show_marker=False)
        background.grid.set_opacity(0)
        background.dialogue.stretch_to_fit_width(14.24)
        background.dialogue.stretch_to_fit_height(1.92)
        background.dialogue.move_to([0,-3.21,0])
        # A single small square dot is the only character placeholder.
        player=Rectangle(width=.12,height=.12,stroke_width=0,
                         fill_color='#FFFFFF',fill_opacity=1).move_to([-1.5,1.125,0])
        enemy=Rectangle(width=.12,height=.12,stroke_width=0,
                        fill_color='#FF6666',fill_opacity=1).move_to([1.5,1.125,0])
        self.add(background,player,enemy)
        if self.show_equation:
            self.add(
                VGroup(Line([1.5,1.20,0],[2.6,2.25,0]),
                       Line([2.6,2.25,0],[3.25,2.25,0]))
                .set_stroke('#FF6666',width=1.5,opacity=.55),
                Rectangle(width=.09,height=.09,stroke_width=0,
                          fill_color='#FF6666',fill_opacity=1).move_to([3.4,2.25,0]),
                Text('x + 3 = 5',font='Consolas',font_size=28)
                .move_to([4.95,2.25,0]))

if __name__=='__main__':
    out=Path(__file__).parent/'initial'
    out.mkdir(exist_ok=True)
    with tempconfig({'frame_width':16,'frame_height':9,'pixel_width':1280,'pixel_height':720,
                     'save_last_frame':True,'write_to_movie':False,'verbosity':'ERROR',
                     'media_dir':str(ROOT/'media'/'initial_screen')}):
        for name,show in [('screen',False),('equation',True)]:
            scene=InitialScreen();scene.show_equation=show;scene.render()
            camera=scene.renderer.camera;camera.reset();camera.pixel_array_to_cairo_context.clear()
            camera.capture_mobjects(scene.mobjects);camera.get_image().save(out/f'{name}.png')
