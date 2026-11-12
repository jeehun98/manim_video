from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p
@dataclass(frozen=True)
class UncertaintyLayout(Layout):
 @property
 def panels(self):return (p(0,2.15),p(0,-1.3)) if self.portrait else (p(-3.65,.2),p(3.65,.2))
 @property
 def summary_y(self):return -3.25 if self.portrait else -2.15
 @property
 def top_wave(self):return p(0,2.25) if self.portrait else p(-3.6,.25)
