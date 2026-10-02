"""Allocate science10's total duration by spoken character count, without audio."""
import argparse
import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / 'episodes/science10_cosmic_void'

def weight(text):
    return sum(c.isalnum() for c in text)

def stamp(frame):
    ms = round(frame * 1000 / 30)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--duration', type=float, default=70)
    args = parser.parse_args()
    if args.duration <= 0 or args.duration >= 180:
        parser.error('Duration must be between 0 and 180 seconds.')
    source = (EPISODE / 'narration.md').read_text(encoding='utf-8')
    title = source.split('\n', 1)[0]
    dialogue = [s.strip() for s in re.findall(r'## [^\n]+\n\s*([^#]+)', source)]
    if len(dialogue) != 10:
        raise ValueError('Expected exactly ten scene dialogues.')
    weights = [weight(s) for s in dialogue]
    total_frames = round(args.duration * 30)
    edges = [round(total_frames * sum(weights[:i]) / sum(weights)) for i in range(11)]
    cues = [dict(start_frame=a, end_frame=b, characters=w, text=t)
            for a, b, w, t in zip(edges, edges[1:], weights, dialogue)]
    data = dict(duration=total_frames/30, fps=30,
                method='alphanumeric characters; excludes spaces and punctuation', cues=cues)
    (EPISODE / 'timing.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (EPISODE / 'narration.md').write_text(title+'\n\n'+'\n\n'.join(
        f'## {a/30:.2f}–{b/30:.2f}초\n\n{t}' for a,b,t in zip(edges,edges[1:],dialogue))+'\n', encoding='utf-8')
    (EPISODE / 'tts_script.txt').write_text('\n\n'.join(t for t in dialogue)+'\n', encoding='utf-8')
    entries = []
    for cue in cues:
        parts = re.split(r'(?<=[.?,])\s+', cue['text'])
        part_weights = [weight(s) for s in parts]
        span = cue['end_frame']-cue['start_frame']
        bounds = [cue['start_frame']+round(span*sum(part_weights[:i])/sum(part_weights))
                  for i in range(len(parts)+1)]
        for a,b,t in zip(bounds,bounds[1:],parts):
            lines = '\n'.join(textwrap.wrap(t, width=29, break_long_words=False, break_on_hyphens=False))
            entries.append(f'{len(entries)+1}\n{stamp(a)} --> {stamp(b)}\n{lines}\n')
    (EPISODE / 'captions.srt').write_text('\n'.join(entries), encoding='utf-8')
    for i,c in enumerate(cues,1):
        print(f"{i}: {c['start_frame']/30:.2f}-{c['end_frame']/30:.2f}s ({c['characters']} characters)")

if __name__ == '__main__':
    main()


