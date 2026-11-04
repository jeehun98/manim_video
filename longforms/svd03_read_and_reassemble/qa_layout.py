from pathlib import Path
import sys
sys.path.insert(0,str(Path('longforms/svd03_read_and_reassemble').resolve()))
from scene_engine import ReadingScene
from manim import tempconfig
from PIL import Image
R=Path('longforms/svd03_read_and_reassemble/qa');R.mkdir(exist_ok=True)
for t in [30,56,75,84,105,116,134,149]:
 class Snap(ReadingScene):start_time=t;end_time=t+.04
 with tempconfig({'pixel_width':1280,'pixel_height':720,'frame_rate':25,'dry_run':True,'skip_animations':True,'progress_bar':'none','verbosity':'ERROR'}):
  s=Snap();s.render();s.renderer.update_frame(s);Image.fromarray(s.renderer.get_frame()).save(R/f'layout_{t}.png')
print('Saved 8 layout snapshots')
