from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p
@dataclass(frozen=True)
class FinaleLayout(Layout):
 @property
 def panels(self):return p(-3.8,.25),p(3.8,.25)
 @property
 def summary_y(self):return -2.1
