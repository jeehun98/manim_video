"""Positions only; no animation or scattering physics."""
from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p

@dataclass(frozen=True)
class RutherfordLayout(Layout):
    @property
    def main_center(self):return p(0,.8) if self.portrait else p(-3.25,.15)
    @property
    def plot_center(self):return p(0,.8) if self.portrait else p(-2.8,.15)
    @property
    def scatter_scale(self):return .65
    @property
    def detector_scale(self):return .65 if self.portrait else .47
    @property
    def callout_center(self):return p(0,-2.55) if self.portrait else p(4.15,.25)
    @property
    def pair_columns(self):return [-1.95,1.95] if self.portrait else [-3.7,3.7]
    @property
    def spiral_center(self):return p(0,.7) if self.portrait else p(-3.5,.15)
    @property
    def spiral_radius(self):return 2 if self.portrait else 1.7
