from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p
@dataclass(frozen=True)
class AspectLayout(Layout):
    @property
    def atom(self):return p(0,1.0) if self.portrait else p(-3.5,.1)
    @property
    def info(self):return p(0,-2.6) if self.portrait else p(3.7,.1)
    @property
    def spectrum(self):return p(0,-1.9) if self.portrait else p(3.65,-.7)
    @property
    def spectrum_width(self):return 6.6 if self.portrait else 6.0

    @property
    def emphasis_scale(self):return 1 if self.portrait else .82
