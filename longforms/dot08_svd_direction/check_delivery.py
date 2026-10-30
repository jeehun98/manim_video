"""Verify the finished files, clocks, subtitles and pronunciation copy."""
import json,re,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
cues=json.loads((P/'timing.json').read_text(encoding='utf-8'));assert len(cues)==33 and cues[0]['start']==0 and cues[-1]['end']==147
assert all(a['end']==b['start'] for a,b in zip(cues,cues[1:]))
assert '00:02:27,000' in (P/'captions.srt').read_text(encoding='utf-8')
tts=(P/'tts_script.txt').read_text(encoding='utf-8');assert not re.search(r'[A-Z0-9]',tts),tts
report=[]
for layout,dims in [('shorts',(1080,1920)),('longform',(1920,1080))]:
    f=ROOT/'exports'/f'dot08_svd_direction_147s_{layout}_final.mp4'
    metadata=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));v=metadata['streams'][0]
    assert len(metadata['streams'])==1 and v['codec_type']=='video'
    assert (v['width'],v['height'])==dims and v['r_frame_rate']=='30/1' and int(v['nb_frames'])==4410
    assert abs(float(v['duration'])-147)<.001 and v['codec_name']=='h264' and v['pix_fmt']=='yuv420p'
    subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True)
    report.append(dict(output=str(f),width=v['width'],height=v['height'],fps=30,frames=4410,duration_seconds=147,audio=False,full_decode='passed',bytes=f.stat().st_size))
(P/'qa_delivery.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
