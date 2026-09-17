"""Composable Manim objects; no scene or resolution side effects."""
from manim import *
from .style import DATA, THREAD, BLOCK, GRID, MUTED, RESULT, CELL_SIZE, CELL_GAP, label

class DataCell(VGroup):
    def __init__(self, value, size=CELL_SIZE, color=DATA, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.box = Square(side_length=size, color=color, stroke_width=2,
                          fill_color=color, fill_opacity=.08)
        self.number = label(value, 30, color).scale_to_fit_height(size * .43)
        if self.number.width > size * .8:
            self.number.scale_to_fit_width(size * .8)
        self.add(self.box, self.number)

    def change(self, value, color=RESULT):
        """Return an animation that preserves this cell's position and scale."""
        self.value = value
        new = label(value, 30, color).scale_to_fit_height(self.box.height * .43)
        if new.width > self.box.width * .8:
            new.scale_to_fit_width(self.box.width * .8)
        new.move_to(self.number)
        return AnimationGroup(Transform(self.number, new), self.box.animate.set_color(color))

class ThreadMarker(VGroup):
    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.tag = label(f'T{index}', 24, THREAD)
        self.marker = Dot(radius=.045, color=THREAD).next_to(self.tag, DOWN, buff=.1)
        self.add(self.tag, self.marker)

class ThreadGroup(VGroup):
    def __init__(self, count=6, start=0, spacing=CELL_SIZE + CELL_GAP, **kwargs):
        super().__init__(**kwargs)
        self.add(*[ThreadMarker(start + i).move_to(RIGHT * i * spacing) for i in range(count)])
        self.center()

class MemoryBox(VGroup):
    def __init__(self, title, width=3, height=1, color=DATA, **kwargs):
        super().__init__(**kwargs)
        self.box = Rectangle(width=width, height=height, color=color, stroke_width=1.6,
                             fill_color=color, fill_opacity=.045)
        self.title = label(title, 19, color, width - .2).move_to(self.box.get_top() + DOWN * .25)
        self.add(self.box, self.title)

class GPUBlock(VGroup):
    def __init__(self, index=0, count=6, width=6.5, height=2.4, **kwargs):
        super().__init__(**kwargs)
        self.box = Rectangle(width=width, height=height, color=BLOCK, stroke_width=2)
        self.title = label(f'Block {index}', 25, BLOCK).move_to(UP * (height / 2 - .32))
        # Thread IDs are local to each block.
        self.threads = ThreadGroup(count, spacing=(width - 1) / max(count - 1, 1))
        self.shared = MemoryBox('Shared Memory', width - .6, .6, BLOCK).move_to(DOWN * (height / 2 - .4))
        self.add(self.box, self.title, self.threads, self.shared)

class GPUGrid(VGroup):
    def __init__(self, count=4, columns=2, **kwargs):
        super().__init__(**kwargs)
        self.blocks = VGroup(*[GPUBlock(i).scale(.47) for i in range(count)])
        self.blocks.arrange_in_grid(cols=columns, buff=.35)
        self.box = SurroundingRectangle(self.blocks, buff=.3, color=GRID, stroke_width=2)
        self.title = label('Grid · one kernel launch', 24, GRID).next_to(self.box, UP, buff=.2)
        self.add(self.box, self.title, self.blocks)

class DataArrow(Arrow):
    def __init__(self, start, end, color=DATA, **kwargs):
        super().__init__(start, end, buff=.08, color=color, stroke_width=2,
                         max_tip_length_to_length_ratio=.15, **kwargs)

    def transfer(self, value, color=DATA):
        """A visible value travels along the arrow; caller removes it afterwards."""
        token = label(value, 23, color).move_to(self.get_start())
        return token, MoveAlongPath(token, self)

def data_row(values, size=CELL_SIZE, color=DATA):
    return VGroup(*[DataCell(v, size, color) for v in values]).arrange(RIGHT, buff=CELL_GAP)
