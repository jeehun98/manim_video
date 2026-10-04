"""Join the five compatible Manim H.264 chapters and their SRT files.

No audio generation or audio alignment. Container timestamps are normalised to
the 30fps frame clock so chapter boundaries match the measured total durations.
"""
from fractions import Fraction
from pathlib import Path
import re
import av

PROJECT = Path(__file__).resolve().parent
WORKSPACE = PROJECT.parents[1]
EXPORTS = WORKSPACE / "exports"
CHAPTERS = [
    ("xai01_act01_rich_1080p30", 111),
    ("xai01_act02_146s_1080p30", 146),
    ("xai01_act03_154s_1080p30", 154),
    ("xai01_act04_193s_1080p30", 193),
    ("xai01_act05_226s_1080p30", 226),
]
TIME_BASE = Fraction(1, 15360)
FRAME_TICKS = 512


def stamp(milliseconds):
    m = milliseconds
    return f"{m // 3600000:02}:{m // 60000 % 60:02}:{m // 1000 % 60:02},{m % 1000:03}"


def milliseconds(s):
    h, m, sec, ms = map(int, re.split(r"[:,]", s))
    return ((h * 60 + m) * 60 + sec) * 1000 + ms


def concat_subtitles():
    blocks, offset = [], 0
    previous = 0
    for name, seconds in CHAPTERS:
        contents = (EXPORTS / f"{name}.srt").read_text(encoding="utf-8-sig").strip()
        for block in re.split(r"\n\s*\n", contents):
            rows = block.splitlines()
            start_text, end_text = rows[1].split(" --> ")
            start = milliseconds(start_text) + offset
            end = milliseconds(end_text) + offset
            assert previous <= start < end <= offset + seconds * 1000
            blocks.append(f"{len(blocks) + 1}\n{stamp(start)} --> {stamp(end)}\n" + "\n".join(rows[2:]))
            previous = end
        offset += seconds * 1000
    subtitle = "\n\n".join(blocks) + "\n"
    (EXPORTS / "xai01_full_silent_1080p30.srt").write_text(subtitle, encoding="utf-8")
    (PROJECT / "captions.srt").write_text(subtitle, encoding="utf-8")
    print(f"SRT: {len(blocks)} cues; {offset / 1000:g} seconds")


def concat_video():
    # Check all codec parameters before starting the output file.
    reference = None
    for name, seconds in CHAPTERS:
        with av.open(str(EXPORTS / f"{name}.mp4")) as source:
            stream = source.streams.video[0]
            context = stream.codec_context
            parameters = (context.name, context.width, context.height, context.extradata)
            if reference is None:
                reference = parameters
            assert parameters == reference, f"Codec mismatch: {name}"
            assert context.width == 1920 and context.height == 1080
            assert stream.frames == seconds * 30, f"Unexpected frame count: {name}"

    target = EXPORTS / "xai01_full_silent_1080p30.mp4"
    template_input = av.open(str(EXPORTS / f"{CHAPTERS[0][0]}.mp4"))
    offset_frames, previous_dts = 0, None
    with av.open(str(target), mode="w", options={"movflags": "+faststart"}) as output:
        stream_out = output.add_stream_from_template(template_input.streams.video[0])
        stream_out.time_base = TIME_BASE
        for name, seconds in CHAPTERS:
            count = 0
            with av.open(str(EXPORTS / f"{name}.mp4")) as source:
                stream = source.streams.video[0]
                for packet in source.demux(stream):
                    if packet.pts is None or packet.dts is None:
                        continue
                    original_base = packet.time_base
                    pts_frame = round(packet.pts * original_base * 30) + offset_frames
                    dts_frame = round(packet.dts * original_base * 30) + offset_frames
                    assert previous_dts is None or dts_frame > previous_dts
                    previous_dts = dts_frame
                    packet.pts = pts_frame * FRAME_TICKS
                    packet.dts = dts_frame * FRAME_TICKS
                    packet.duration = FRAME_TICKS
                    packet.time_base = TIME_BASE
                    packet.stream = stream_out
                    output.mux(packet)
                    count += 1
            assert count == seconds * 30, f"Unexpected packet count: {name}: {count}"
            offset_frames += count
    template_input.close()
    print(f"Video: {offset_frames} frames; {offset_frames / 30:g} seconds")


if __name__ == "__main__":
    concat_video()
    concat_subtitles()
