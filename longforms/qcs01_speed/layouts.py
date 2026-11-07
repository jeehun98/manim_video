"""Body positions and subtitle bands for native portrait/landscape compositions."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Layout:
    portrait: bool
    def y(self,value):return value if self.portrait else value*.64
    def point(self,x,y):return np.array([x,self.y(y),0.])
    @property
    def heading_y(self):return 5.5 if self.portrait else 3.2
    @property
    def brand_y(self):return 7.15 if self.portrait else 4.02
    @property
    def note_y(self):return -3.9 if self.portrait else -2.35
    @property
    def caption_y(self):return -6.15 if self.portrait else -3.4
    @property
    def caption_height(self):return 2.15 if self.portrait else 1.35
    @property
    def caption_width(self):return 7.65 if self.portrait else 14.2
    @property
    def caption_chars(self):return 26 if self.portrait else 52
    @property
    def dense_grid_size(self):return .65 if self.portrait else .46
