import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'media/nncalc_compilation'
rows = json.loads((WORK / 'input_probe.json').read_text())
sheet = Image.new('RGB', (1280, 800), '#09131c')
draw = ImageDraw.Draw(sheet)
elapsed = 0
for i, row in enumerate(rows):
    path = WORK / f'chapter_{i+1:02d}.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(elapsed+1),
                    '-i', str(ROOT / 'exports/nncalc_complete.mp4'), '-frames:v', '1',
                    '-vf', 'scale=320:180', str(path)], check=True)
    x, y = (i % 2)*640, (i // 2)*200
    sheet.paste(Image.open(path), (x, y+20))
    draw.text((x+5, y+3), f'Chapter {i+1} at {elapsed:.3f}s', fill='white')
    elapsed += float(row['metadata']['format']['duration'])
sheet.save(WORK / 'chapter_checks.jpg')
