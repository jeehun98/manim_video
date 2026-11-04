"""Only placement and sizing; choreography remains screen-ratio independent."""
from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p

@dataclass(frozen=True)
class PhotoelectricLayout(Layout):
    @property
    def apparatus_center(self):return p(0,1.4) if self.portrait else p(-3.8,.35)
    @property
    def apparatus_scale(self):return .95 if self.portrait else 1.05
    @property
    def readout_center(self):return p(0,-1.8) if self.portrait else p(3.5,.05)
    @property
    def comparison_centers(self):return [p(0,2),p(0,-1.45)] if self.portrait else [p(-3.65,.05),p(3.65,.05)]
    @property
    def panel_width(self):return 7.15 if self.portrait else 6.7
    @property
    def panel_height(self):return 2.8 if self.portrait else 4.2
    @property
    def pair_columns(self):return [-1.95,1.95] if self.portrait else [-3.7,3.7]
