from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p
@dataclass(frozen=True)
class BornLayout(Layout):
 @property
 def center(self):return p(0,1.05) if self.portrait else p(0,.15)
 @property
 def panels(self):return (p(0,2.6),p(0,-.85)) if self.portrait else (p(-3.8,.3),p(3.65,.3))
 @property
 def detector_center(self):return p(0,2.45) if self.portrait else p(-3.65,.4)
 @property
 def hist_center(self):return p(0,-1.05) if self.portrait else p(3.65,.1)
 @property
 def detector_width(self):return 6.5 if self.portrait else 6.25
 @property
 def detector_height(self):return 2.25 if self.portrait else 3.0
 @property
 def scatter_center(self):return p(0,2.1) if self.portrait else p(-3.65,.35)
 @property
 def pair(self):return (-1.95,1.95) if self.portrait else (-3.6,3.6)
