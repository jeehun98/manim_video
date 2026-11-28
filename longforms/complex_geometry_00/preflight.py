import os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
os.environ['QCS_PREVIEW']='1'
os.environ['CG_ASSET_KEY']='preflight'
os.environ['QCS_AUDIT_DIR']=str(ROOT/'media/complex_geometry_00_preflight/audit')
from manim import tempconfig
from longforms.complex_geometry_00.direction import IntroScene
if __name__=='__main__':
 first=int(sys.argv[1]) if len(sys.argv)>1 else 1
 with tempconfig({'dry_run':True,'skip_animations':True,'verbosity':'ERROR','progress_bar':'none'}):
  for i in range(first-1,8):
   type(f'Check{i+1:02}',(IntroScene,),{'shot':i})().render()
   print('PASS',i+1,flush=True)
