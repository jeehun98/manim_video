import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import ChapterScene
class Scene01(ChapterScene):
    index=1
