"""Only positions and sizes change between native aspect ratios."""
from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p
@dataclass(frozen=True)
class MatrixLayout(Layout):
 @property
 def center(self):return p(0,1.05) if self.portrait else p(0,.2)
 @property
 def observation_centers(self):return (p(0,2.6),p(0,-.85)) if self.portrait else (p(-3.7,.25),p(3.6,.25))
 @property
 def matrix_centers(self):return (p(-1.9,2.0),p(1.9,2.0)) if self.portrait else (p(-3.4,.35),p(3.4,.35))
 @property
 def calculation_y(self):return -.3 if self.portrait else -1.35
 @property
 def links_y(self):return -1.25 if self.portrait else -2.05
 @property
 def sum_y(self):return -2.55 if self.portrait else -2.05
