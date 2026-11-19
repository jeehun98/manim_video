"""Standalone still preview: run from the repository root (see README)."""

from manim import Scene, config
from visual_library.manim.dialogue_background import DialogueBackground


config.frame_width = 16
config.frame_height = 9
config.pixel_width = 1920
config.pixel_height = 1080


class DialogueBackgroundPreview(Scene):
    def construct(self):
        self.add(DialogueBackground())
