"""Open grid stage and subtitle box; no global render configuration changes."""

from math import ceil

from manim import BLACK, WHITE, Line, Rectangle, Text, VGroup

from .theme import FONT


class DialogueBackground(VGroup):
    """16:9 layout by default. Coordinates are relative to this group's center.

    Add content above ``stage_bottom`` and below ``height / 2``.
    Keep this group stationary; use ``set_caption`` for subtitle replacement.
    """

    def __init__(self, width=16, height=9, grid_step=0.36,
                 grid_color="#242424", grid_opacity=0.8,
                 border_width=2.5, font=FONT, show_marker=True,
                 grid_under_dialogue=False, **kwargs):
        super().__init__(**kwargs)
        if width <= 0 or height <= 0 or grid_step <= 0:
            raise ValueError("width, height and grid_step must be positive")
        self.font = font
        self.show_marker = show_marker
        self.stage_bottom = -height * 0.265
        grid_bottom = -height / 2 if grid_under_dialogue else self.stage_bottom
        self.backdrop = Rectangle(width=width, height=height,
                                  stroke_width=0, fill_color=BLACK, fill_opacity=1)
        self.grid = VGroup()
        for i in range(-ceil(width / (2 * grid_step)), ceil(width / (2 * grid_step)) + 1):
            x = i * grid_step
            if abs(x) < width / 2:
                self.grid.add(Line([x, grid_bottom, 0], [x, height / 2, 0]))
        for i in range(ceil(height / grid_step) + 1):
            y = height / 2 - i * grid_step
            if y >= grid_bottom:
                self.grid.add(Line([-width / 2, y, 0], [width / 2, y, 0]))
        self.grid.set_stroke(grid_color, width=0.8, opacity=grid_opacity)
        self.dialogue = Rectangle(
            width=width * 0.86, height=height * 0.14,
            stroke_color=WHITE, stroke_width=border_width,
            fill_color=BLACK, fill_opacity=1,
        ).move_to([0, -height * 0.38, 0])
        self.caption = VGroup()
        self.add(self.backdrop, self.grid, self.dialogue, self.caption)
        self.backdrop.set_z_index(-100)
        self.grid.set_z_index(-99)
        self.dialogue.set_z_index(100)
        self.set_caption("")

    def set_caption(self, text, font_size=28):
        """Replace the caption instantly. Explicit newlines support two lines.

        Text is fitted to the inner box so it cannot overlap its border.
        """
        self.caption.remove(*list(self.caption.submobjects))
        left = self.dialogue.get_left()[0] + 0.24
        top = self.dialogue.get_top()[1] - 0.20
        if self.show_marker:
            marker = Text("*", font=self.font, font_size=font_size, color=WHITE)
            marker.move_to([left + marker.width / 2, top - marker.height / 2, 0])
            self.caption.add(marker)
            left += 0.36
        if text:
            label = Text(text, font=self.font, font_size=font_size,
                         color=WHITE, line_spacing=0.8)
            available_width = self.dialogue.get_right()[0] - 0.24 - left
            available_height = self.dialogue.height - 0.4
            label.scale(min(1, available_width / label.width,
                            available_height / label.height))
            label.move_to([left + label.width / 2, top - label.height / 2, 0])
            self.caption.add(label)
        self.caption.set_z_index(101)
        return self
