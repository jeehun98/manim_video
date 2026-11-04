"""Combine the user's six voiced exports without re-encoding."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'exports' / 'qr_full_01_06_longform.mp4'
TITLES = ['벡터와 새로운 공간', '위삼각행렬의 구조', '대각선과 부피', 'QR과 SVD', 'QR 반복과 고윳값', 'QR 분해의 기하학 — 마무리']

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], text=True, encoding='utf-8'))

def main():
    inputs = [ROOT / 'exports' / f'qr_long_{i}.mp4' for i in range(1, 7)]
    probes = [probe(p) for p in inputs]
    signatures = [[tuple(s.get(k) for k in ('codec_type', 'codec_name', 'width', 'height', 'pix_fmt', 'r_frame_rate', 'time_base', 'sample_rate', 'channels')) for s in p['streams']] for p in probes]
    assert all(s == signatures[0] for s in signatures), 'Input stream formats differ'
    durations = [float(p['format']['duration']) for p in probes]
    (HERE / 'concat.txt').write_text(''.join("file '" + p.as_posix() + "'\n" for p in inputs), encoding='utf-8')
    metadata = [';FFMETADATA1', 'title=QR 분해의 기하학']
    offset = 0.0
    chapters = []
    for path, title, duration in zip(inputs, TITLES, durations):
        start, end = round(offset * 1000), round((offset + duration) * 1000)
        metadata += ['[CHAPTER]', 'TIMEBASE=1/1000', f'START={start}', f'END={end}', f'title={title}']
        chapters.append({'source': str(path.relative_to(ROOT)), 'title': title, 'start_seconds': offset, 'duration_seconds': duration})
        offset += duration
    (HERE / 'chapters.ffmetadata').write_text('\n'.join(metadata) + '\n', encoding='utf-8')
    with (HERE / 'concat.log').open('a', encoding='utf-8') as log:
      if '--verify-only' not in sys.argv:
        subprocess.run(['ffmpeg', '-hide_banner', '-n', '-f', 'concat', '-safe', '0', '-i', str(HERE / 'concat.txt'), '-i', str(HERE / 'chapters.ffmetadata'), '-map', '0:v:0', '-map', '0:a:0', '-map_metadata', '1', '-map_chapters', '1', '-c', 'copy', '-movflags', '+faststart', str(OUT)], check=True, stdout=log, stderr=log)
    final = probe(OUT)
    expected_frames = sum(int(next(s for s in p['streams'] if s['codec_type'] == 'video')['nb_frames']) for p in probes)
    video = next(s for s in final['streams'] if s['codec_type'] == 'video')
    assert int(video['nb_frames']) == expected_frames
    assert abs(float(final['format']['duration']) - offset) < 0.1
    assert (video['width'], video['height'], video['r_frame_rate']) == (1920, 1080, '30/1')
    report = {'output': str(OUT), 'chapters': chapters, 'expected_duration_seconds': offset, 'actual_duration_seconds': float(final['format']['duration']), 'video_frames': expected_frames, 'video_codec': video['codec_name'], 'audio_codec': next(s['codec_name'] for s in final['streams'] if s['codec_type'] == 'audio'), 'method': 'stream copy; original audio and video preserved'}
    (HERE / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=True, indent=2))

if __name__ == '__main__':
    main()
