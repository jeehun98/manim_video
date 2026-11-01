import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from cache_visuals import CacheBase
class Cache01(CacheBase):
    INDEX=0
