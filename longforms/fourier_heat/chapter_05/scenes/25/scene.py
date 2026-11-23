import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import GeometryScene
from manim import VGroup
class Shot25(GeometryScene):
 index=25
 def geometry(self,t):
  # Keep a flat family across the patch/sphere/graph/operator transitions.
  # Nested become() alignment otherwise multiplies old curve families.
  return VGroup(*super().geometry(t).family_members_with_points())
