"""Dual-ratio staging; animation never changes with the aspect ratio."""
from dataclasses import dataclass
from quantum_series.shared.theme import Layout,p
@dataclass(frozen=True)
class MatterLayout(Layout):
 @property
 def ring(self):return p(0,1.65) if self.portrait else p(-3.8,.15)
 @property
 def radius(self):return 1.85 if self.portrait else 1.8
 @property
 def straight(self):return p(0,-1.8) if self.portrait else p(3.7,.15)
 @property
 def straight_width(self):return 6.7 if self.portrait else 6.1
 @property
 def flat_amplitude(self):return .32 if self.portrait else .5
 @property
 def phase_y(self):return -3.3 if self.portrait else -1.7
 @property
 def center(self):return p(0,1) if self.portrait else p(0,.1)
 @property
 def pair_y(self):return .8 if self.portrait else .15
