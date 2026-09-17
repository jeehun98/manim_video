"""Series palette, layout, and animation timing (logical units / seconds)."""
from manim import Text

BG = '#091119'
INK = '#EDF3F7'
MUTED = '#94A7B7'
DATA = '#68D9F0'
THREAD = '#F3CF75'
BLOCK = '#61E4CF'
GRID = '#AF9CF5'
RESULT = '#FF8C9D'
FONT = 'Malgun Gothic'
FRAME_WIDTH, FRAME_HEIGHT = 9, 16
TITLE_Y, HEAD_Y, CAPTION_Y = 6.7, 5.1, -6.2
FORMULA_Y, ARRAY_Y, THREAD_Y = 2.9, 0.5, 1.9
CELL_SIZE, CELL_GAP = 0.78, 0.16
FADE, MOVE, COMPUTE = 0.5, 1.4, 1.8
INPUT = (3, 7, 2, 9, 1, 5)
OUTPUT = tuple(x + 1 for x in INPUT)

def label(text, size=28, color=INK, max_width=7.7):
    obj = Text(str(text), font=FONT, font_size=size, color=color, line_spacing=1.2)
    if obj.width > max_width:
        obj.scale_to_fit_width(max_width)
    return obj
