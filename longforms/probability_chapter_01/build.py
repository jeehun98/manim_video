"""Render and verify the independently replaceable landscape clips."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = json.loads((HERE / 'timing.json').read_text(encoding='utf-8'))
PUBLISHED = json.loads((HERE / 'publication_timing.json').read_text(encoding='utf-8'))
LEAD_IN = DATA['duration'] - PUBLISHED['duration']
FPS = 30


def verify(path, seconds, dimensions):
    result = json.loads(subprocess.check_output(
        ['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    video, = result['streams']
    assert video['codec_type'] == 'video', path
    assert (video['width'], video['height']) == dimensions, path
    assert video['avg_frame_rate'] == f'{FPS}/1', path
    assert int(video['nb_frames']) == seconds * FPS, path
    assert abs(float(result['format']['duration']) - seconds) < .017, path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preview', action='store_true')
    parser.add_argument('--scene', choices=[s['id'] for s in DATA['scenes']])
    args = parser.parse_args()
    mode = 'preview' if args.preview else 'final'
    dimensions = (640, 360) if args.preview else (1920, 1080)
    media = ROOT / 'media/probability_chapter_01' / mode
    media.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    dependencies = [HERE / name for name in ('scene.py', 'timing.json', 'build.py')]
    dependencies.extend(HERE.parent / 'probability_chapter_00' / name for name in ('scene.py', 'timing.json'))
    digest = hashlib.sha256(b''.join(path.read_bytes() for path in dependencies)).hexdigest()
    clips = []
    for shot in DATA['scenes']:
        if args.scene and shot['id'] != args.scene:
            continue
        name = shot['class']
        cache = media / digest / name
        cache.mkdir(parents=True, exist_ok=True)
        clip = cache / f'{name}.mp4'
        duration = shot['end'] - shot['start']
        if not clip.exists():
            print(f'Render {mode} {name}', flush=True)
            log = cache / 'render.log'
            with log.open('w', encoding='utf-8') as stream:
                result = subprocess.run(
                    [sys.executable, '-m', 'manim', 'render', str(HERE / 'scene.py'), name,
                     '--media_dir', str(cache), '-r', f'{dimensions[0]},{dimensions[1]}', '--fps', str(FPS), '--disable_caching', '--verbosity', 'WARNING',
                     '--progress_bar', 'none'], cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT)
            if result.returncode:
                raise RuntimeError(log.read_text(encoding='utf-8')[-6000:])
            rendered, = (cache / 'videos').rglob(f'{name}.mp4')
            verify(rendered, duration, dimensions)
            rendered.replace(clip)
        verify(clip, duration, dimensions)
        clips.append(clip)
    if args.scene:
        print(clips[0])
        return
    assemble(clips, media, args.preview, dimensions)


def assemble(clips, media, preview, dimensions):
    # The opening sentence occupies a complete 3-second lead-in in the
    # original render. Trim at its keyframe so later scenes stay reusable.
    first = media / 'BernoulliDefinition_trimmed.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(LEAD_IN),
                    '-i', str(clips[0]), '-map', '0:v:0', '-c', 'copy', str(first)],
                   check=True)
    verify(first, DATA['scenes'][0]['end'] - LEAD_IN, dimensions)
    clips = [first, *clips[1:]]
    duration = PUBLISHED['duration']
    manifest = media / 'concat_standalone.txt'
    manifest.write_text(''.join(f"file '{clip.as_posix()}'\n" for clip in clips), encoding='utf-8')
    output = (media / 'probability_chapter_01_preview.mp4' if preview
              else ROOT / 'exports/probability_chapter_01_long.mp4')
    output.parent.mkdir(exist_ok=True)
    temporary = output.with_suffix('.trimmed.tmp.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0',
                    '-i', str(manifest), '-c', 'copy', '-movflags', '+faststart', str(temporary)], check=True)
    verify(temporary, duration, dimensions)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(temporary), '-f', 'null', '-'], check=True)
    temporary.replace(output)
    print(f'Verified {output}')


if __name__ == '__main__':
    main()
