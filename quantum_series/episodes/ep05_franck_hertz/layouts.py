"""Responsive positions; tube stays fixed across apparatus, graph and collection chapters."""
from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p

@dataclass(frozen=True)
class FranckHertzLayout(Layout):
    @property
    def tube_center(self):return p(0,2.55) if self.portrait else p(-3.8,.35)
    @property
    def tube_scale(self):return 1.02 if self.portrait else 1.0
    @property
    def plot_center(self):return p(0,-.8) if self.portrait else p(3.65,.1)
    @property
    def plot_width(self):return 6.5 if self.portrait else 6.1
    @property
    def plot_height(self):return 2.35 if self.portrait else 3.25
    @property
    def atom_center(self):return p(-1.65,-.65) if self.portrait else p(1.15,.25)
    @property
    def level_center(self):return p(1.95,-.65) if self.portrait else p(5.15,.25)
    @property
    def energy_center(self):return p(-1.65,-2.05) if self.portrait else p(1.15,-1.65)
    @property
    def pair_columns(self):return [-1.95,1.95] if self.portrait else [-3.7,3.7]
