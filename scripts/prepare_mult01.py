"""Preserve supplied sentence boundaries; do not estimate internal word timings."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'episodes/mult01_error_parity'
spec = importlib.util.spec_from_file_location('mult_content', HERE / 'content.py')
content = importlib.util.module_from_spec(spec)
spec.loader.exec_module(content)

def stamp(seconds):
    ms = round(seconds * 1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def wrap(text, limit=26):
    rows = ['']
    for word in text.split():
        if rows[-1] and len(rows[-1]) + len(word) + 1 > limit:
            rows.append(word)
        else:
            rows[-1] += (' ' if rows[-1] else '') + word
    return '\n'.join(rows)

if __name__ == '__main__':
    cues = []
    start = 0
    narration = ['# 인공지능은 어떻게 곱셈을 틀릴까?', '',
                 '사용자 제공 확정 낭독문과 문장 종료 시각. 총 102초. 원문을 수정하지 않음.', '',
                 '> 통계 주의: 22–32초의 홀짝은 화면에서 확대하는 **십의 자리 숫자**를 가리킨다. 92.7%는 답 전체의 홀짝 일치율이 아니다.', '']
    for i, ((end, text), title) in enumerate(zip(content.LINES, content.TITLES), 1):
        cues.append(dict(index=i, start=start, end=end, start_frame=start*30,
                         end_frame=end*30, title=title, text=text, caption=wrap(text)))
        narration += [f'## {start}–{end}초 · {title}', '', text, '']
        start = end
    timing = dict(duration=102, fps=30, method='user-provided cumulative sentence endpoints',
                  end_seconds=[end for end, _ in content.LINES],
                  subtitle_timing='whole sentence held over user-specified interval; no inferred sub-sentence times', cues=cues)
    (HERE/'timing.json').write_text(json.dumps(timing, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (HERE/'narration.md').write_text('\n'.join(narration), encoding='utf-8')
    tts = '\n\n'.join(text for _, text in content.LINES)
    tts = tts.replace('2026년 10월', '이천이십육년 시월').replace('1만 7천 개', '일만 칠천 개').replace('92.7퍼센트', '구십이 점 칠 퍼센트')
    (HERE/'tts_script.txt').write_text(tts+'\n', encoding='utf-8')
    (HERE/'captions.srt').write_text('\n\n'.join(f"{c['index']}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['caption']}" for c in cues)+'\n', encoding='utf-8')
    print('Prepared 21 cues, 3060 frames, 102 seconds.')
