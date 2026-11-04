from pathlib import Path
import subprocess,json
r=Path('longforms/minimal01_07_finale');(r/'assets').mkdir(exist_ok=True)
for i,t in [(2,93),(3,18),(4,86),(5,49),(6,70),(7,108)]:
 p=Path(f'exports/minimal{i:02}_long.mp4')
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','crop=1720:650:100:150,scale=688:260',str(r/f'assets/ep{i:02}.png')],check=True)
