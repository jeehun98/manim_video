from pathlib import Path
import sys
sys.path.insert(0,str(Path('longforms/svd02_direction_map').resolve()))
from scene_engine import DirectionScene
from manim import tempconfig
R=Path('longforms/svd02_direction_map/qa');R.mkdir(exist_ok=True)
for t in [39,54,76,99,112,118,147]:
 class Snap(DirectionScene):start_time=t;end_time=t+.04
 with tempconfig({'pixel_width':1280,'pixel_height':720,'frame_rate':25,'dry_run':True,'skip_animations':True,'progress_bar':'none','verbosity':'ERROR'}):
  s=Snap();s.render();s.renderer.update_frame(s);s.renderer.get_frame()
  from PIL import Image
  Image.fromarray(s.renderer.get_frame()).save(R/f'layout_{t}.png')
print('Saved 7 layout snapshots')
