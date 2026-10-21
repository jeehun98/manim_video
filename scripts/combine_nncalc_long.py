"""Join the eight user-supplied landscape masters without re-encoding."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'media/nncalc_compilation'
WORK.mkdir(parents=True, exist_ok=True)
OUT = ROOT / 'exports/nncalc_complete.mp4'
TITLES = ['같은 정답, 다른 알고리즘', 'Induction Heads', 'Patterning',
          'Feature Superposition', 'Sparse Autoencoders', 'Circuit Tracing',
          'Probing & Intervention', '알고리즘의 발견에서 형성 유도까지']

def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))

def main():
    files = [ROOT / f'exports/nncalc_long{i}.mp4' for i in range(1, 9)]
    data = [probe(p) for p in files]
    durations = [float(d['format']['duration']) for d in data]
    signatures = []
    for d in data:
        v = next(s for s in d['streams'] if s['codec_type'] == 'video')
        a = next(s for s in d['streams'] if s['codec_type'] == 'audio')
        signatures.append((v['codec_name'], v['width'], v['height'], v['r_frame_rate'],
                           v['pix_fmt'], v['time_base'], a['codec_name'], a['sample_rate'], a['channels']))
    assert len(set(signatures)) == 1, signatures
    listing = WORK / 'concat.txt'
    listing.write_text('\n'.join("file '" + p.as_posix() + "'" for p in files) + '\n', encoding='utf-8')
    metadata = [';FFMETADATA1', 'title=신경망 내부의 계산 — 표현에서 알고리즘까지',
                'comment=Episodes 01–08, original picture and narration preserved.']
    chapters = []
    elapsed = 0.0
    for i, (title, duration) in enumerate(zip(TITLES, durations), 1):
        start, end = round(elapsed * 1000), round((elapsed + duration) * 1000)
        metadata += ['[CHAPTER]', 'TIMEBASE=1/1000', f'START={start}', f'END={end}', f'title={i:02d} {title}']
        sec = int(elapsed)
        chapters.append(f'{sec // 60:02d}:{sec % 60:02d} {i:02d} {title}')
        elapsed += duration
    meta = WORK / 'chapters.ffmetadata'
    meta.write_text('\n'.join(metadata) + '\n', encoding='utf-8')
    (ROOT / 'exports/nncalc_complete_chapters.txt').write_text('\n'.join(chapters) + '\n', encoding='utf-8')
    command = ['ffmpeg', '-hide_banner', '-nostdin', '-n', '-f', 'concat', '-safe', '0',
                    '-i', str(listing), '-i', str(meta), '-map', '0:v:0', '-map', '0:a:0',
                    '-map_metadata', '1', '-map_chapters', '1', '-c', 'copy',
                    '-movflags', '+faststart', str(OUT)]
    if not OUT.exists():
        subprocess.run(command, check=True)
    result = probe(OUT)
    actual = float(result['format']['duration'])
    assert abs(actual - elapsed) < 0.15, (actual, elapsed)
    assert len([s for s in result['streams'] if s['codec_type'] in ('video', 'audio')]) == 2
    report = dict(output=str(OUT), sources=[str(p) for p in files],
                  expected_duration=elapsed, actual_duration=actual,
                  signature=signatures[0], reencoded=False, audio_preserved=True)
    (WORK / 'checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
