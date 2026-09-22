"""Generate episode entry points, narration and subtitle sidecars from editorial data."""
import re
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from episodes.svd_series.data import EPISODES

SLUGS=['optimal_forgetting','difference_survival','sensitivity_map','independent_questions','ellipse_extrema']

def korean_tts(caption):
    """Read narration aloud; do not add on-screen-only formulas or timing labels."""
    replacements = {
        'εσᵢuᵢ': '엡실론 곱하기 시그마 아이, 곱하기 유 아이',
        'truncated SVD': '트렁케이티드 에스 브이 디',
        'SVD': '에스 브이 디',
        'Rank': '랭크',
        'σᵢ': '시그마 아이',
        'vᵢ': '브이 아이',
        'uᵢ': '유 아이',
        'k개': '케이 개',
        'k': '케이',
        'x': '엑스',
        '5분의 1': '오 분의 일',
        '−': '마이너스 ',
    }
    for original,spoken in replacements.items():
        caption=caption.replace(original,spoken)
    digits=dict(zip('0123456789','영일이삼사오육칠팔구'))
    def number(match):
        value=match.group()
        whole,*fraction=value.split('.')
        if len(whole)!=1:
            raise ValueError(f'Add an explicit Korean reading for {value}')
        return digits[whole]+(' 점 '+' '.join(digits[d] for d in fraction[0]) if fraction else '')
    caption=re.sub(r'\d+(?:\.\d+)?',number,caption)
    if re.search(r'[A-Za-z0-9σᵢ]',caption):
        raise ValueError(f'Unconverted TTS token: {caption}')
    return caption

def stamp(seconds,srt=False):
    h,rest=divmod(seconds,3600);m,s=divmod(rest,60)
    return f'{h:02d}:{m:02d}:{s:02d},000' if srt else f'{m:02d}:{s:02d}'

def main():
    for number,(title,segments) in EPISODES.items():
        folder=ROOT/'episodes'/f'svd{number:02d}_{SLUGS[number-1]}'
        folder.mkdir(exist_ok=True)
        (folder/'scene.py').write_text(
            '"""SVD series entry point; shared visuals and timing live in svd_series."""\n'
            'import sys\nfrom pathlib import Path\n'
            'sys.path.insert(0,str(Path(__file__).resolve().parents[2]))\n'
            'from episodes.svd_series.visuals import SVDEpisode\n\n'
            f'class SVD{number:02d}(SVDEpisode):\n    episode = {number}\n',encoding='utf-8')
        duration=sum(s[0] for s in segments)
        rows=[f'# SVD {number:02d} — {title}',f'\n{duration}초 · 1080×1920 · 30fps · 한국어 자막 · 무음 마스터\n',
              '발화 예상 길이에 맞춘 편집이며 실제 음성은 포함하지 않습니다.\n',
              '| 시간 | 내레이션 | 화면 |','|---|---|---|']
        subs=[];elapsed=0
        for i,(d,h,c,f,kind,value) in enumerate(segments,1):
            rows.append(f'| {stamp(elapsed)}–{stamp(elapsed+d)} | '+c.replace('\n','<br>')+f' | {h}<br>{f} |')
            subs.append(f'{i}\n{stamp(elapsed,True)} --> {stamp(elapsed+d,True)}\n{c}\n')
            elapsed+=d
        (folder/'narration.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
        (folder/'brief.md').write_text(f'# SVD {number:02d} — {title}\n\n'
            f'{duration}초. 시리즈 공통 수학·시각 기준은 [제작 안내](../svd_series/README.md)를 참고합니다.\n\n'
            f'실행: `python scripts/render.py svd{number:02d}`\n\n'
            '대본과 타이밍의 원본은 `episodes/svd_series/data.py`, 그림은 `episodes/svd_series/visuals.py`입니다.\n',encoding='utf-8')
        (folder/'subtitles.srt').write_text('\n'.join(subs),encoding='utf-8')
        (ROOT/'exports'/f'svd{number:02d}.srt').write_text('\n'.join(subs),encoding='utf-8')
        speech='\n\n'.join(korean_tts(segment[2]) for segment in segments)+'\n'
        (folder/'tts_script.txt').write_text(speech,encoding='utf-8')
        (ROOT/'exports'/f'svd{number:02d}_tts_script.txt').write_text(speech,encoding='utf-8')
    print(f'Prepared {len(EPISODES)} SVD episodes, SRT files and Korean TTS scripts.')

if __name__=='__main__':main()
