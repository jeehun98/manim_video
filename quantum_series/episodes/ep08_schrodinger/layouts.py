from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p
@dataclass(frozen=True)
class WaveLayout(Layout):
 @property
 def center(self):return p(0,1.0) if self.portrait else p(0,.15)
 @property
 def panels(self):return (p(0,2.4),p(0,-.95)) if self.portrait else (p(-3.8,.25),p(3.7,.25))
 @property
 def pair(self):return (-1.95,1.95) if self.portrait else (-3.6,3.6)
 @property
 def row_y(self):return [3.1,1.2,-.7] if self.portrait else [1.6,.15,-1.3]
