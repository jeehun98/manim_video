"""SVD series entry point; shared visuals and timing live in svd_series."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.svd_series.visuals import SVDEpisode

class SVD05(SVDEpisode):
    episode = 5
