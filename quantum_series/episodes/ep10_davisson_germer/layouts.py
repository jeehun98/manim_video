from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p
@dataclass(frozen=True)
class DiffractionLayout(Layout):
 @property
 def panels(self):return (p(0,2.1),p(0,-1.25)) if self.portrait else (p(-3.6,.15),p(3.6,.15))
