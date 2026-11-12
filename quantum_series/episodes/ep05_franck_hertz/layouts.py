from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p
@dataclass(frozen=True)
class AspectLayout(Layout):
    @property
    def tube(self):return p(0,2.3) if self.portrait else p(-3.7,.4)
    @property
    def plot(self):return p(0,-1.5) if self.portrait else p(3.65,.2)
    @property
    def zoom(self):return p(0,1.5) if self.portrait else p(-3.5,.3)
    @property
    def levels(self):return p(0,-1.1) if self.portrait else p(3.6,.2)
    @property
    def info(self):return p(0,-2.8) if self.portrait else p(3.65,.1)
    @property
    def comparison(self):return [p(0,2),p(0,-.7)] if self.portrait else [p(-3.7,.3),p(3.7,.3)]
