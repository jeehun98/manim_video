from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p
@dataclass(frozen=True)
class ComplementarityLayout(Layout):
 @property
 def apparatus(self):return p(0,2.5) if self.portrait else p(-3.65,.25)
 @property
 def screen(self):return p(0,-.25) if self.portrait else p(3.65,1.05)
 @property
 def profile(self):return p(0,-2.05) if self.portrait else p(3.65,-.85)
 @property
 def summary_y(self):return -3.35 if self.portrait else -2.2
 @property
 def panels(self):return (p(0,2.4),p(0,-1.1)) if self.portrait else (p(-3.65,.2),p(3.65,.2))
