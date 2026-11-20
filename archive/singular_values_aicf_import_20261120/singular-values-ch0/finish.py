import json, subprocess, wave
from pathlib import Path
R=Path(__file__).resolve().parent
data=json.loads((R/'timing.json').read_text(encoding='utf-8'))
start=0
srt=[]
def stamp(t):return f'{int(t)//3600:02}:{int(t)//60%60:02}:{int(t)%60:02},000'
for i,end in enumerate(data['ends']):
 duration=end-start
 with wave.open(str(R/f'voice-{i}.wav')) as w: actual=w.getnframes()/w.getframerate()
 ratio=actual/(duration-.08)
 chain=[]
 while ratio>2:chain.append('atempo=2');ratio/=2
 while ratio<.5:chain.append('atempo=0.5');ratio*=2
 chain += [f'atempo={ratio}',f'apad',f'atrim=duration={duration}']
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/f'voice-{i}.wav'),'-af',','.join(chain),'-ar','48000','-ac','1',str(R/f'aligned-{i}.wav')],check=True)
 srt.append(f'{i+1}\n{stamp(start)} --> {stamp(end)}\n{data["narration"][i]}\n')
 start=end
(R/'narration.srt').write_text('\n'.join(srt),encoding='utf-8')
(R/'audio-list.txt').write_text('\n'.join(f"file 'aligned-{i}.wav'" for i in range(11)),encoding='utf-8')
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(R/'audio-list.txt'),'-i',str(R/'visual.mp4'),'-map','1:v','-map','0:a','-c:v','copy','-c:a','aac','-b:a','192k','-t','63','-movflags','+faststart',str(R/'singular-values-ch0.mp4')],check=True)
print('Completed',R/'singular-values-ch0.mp4')
