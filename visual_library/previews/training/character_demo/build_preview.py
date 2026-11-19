from pathlib import Path
from PIL import Image, ImageDraw

p = Path(__file__).resolve().parent
walk = []
for i in range(4):
    original = Image.open(p / f'walk4_{i}.png').convert('RGB')
    upper = original.crop((0, 0, 224, 153))
    lower = original.crop((0, 153, 224, 224)).resize((224, 43), Image.Resampling.NEAREST)
    cell = Image.new('RGB', (224, 224), 'black')
    cell.paste(upper, (0, 10))
    cell.paste(lower, (0, 163))
    cell.save(p / f'walk4_shortlegs_{i}.png')
    walk.append(cell)
sheet = Image.open(p / 'hero_sheet.png').convert('RGBA')
poses = [sheet.crop(((i % 3)*512, (i // 3)*512, (i % 3+1)*512, (i // 3+1)*512)).resize((224, 224), Image.Resampling.NEAREST) for i in range(6)]
frames, durations = [], []
def add(sprite, x, duration):
    frame = Image.new('RGB', (800, 450), 'black')
    if sprite.mode == 'RGBA':
        frame.paste(sprite, (x, 70), sprite)
    else:
        frame.paste(sprite, (x, 70))
    ImageDraw.Draw(frame).rectangle((44, 337, 756, 434), outline='white', width=2)
    frames.append(frame)
    durations.append(duration)
add(poses[0], 210, 650)
for i in range(16):
    add(walk[i % 4], 210+(i+1)*7, 140)
for pose, duration in [(3, 280), (4, 220), (0, 180), (5, 1600)]:
    add(poses[pose], 322, duration)
frames[0].save(p / 'hero_animation_shortlegs.gif', save_all=True, append_images=frames[1:], duration=durations, loop=0, disposal=2)
