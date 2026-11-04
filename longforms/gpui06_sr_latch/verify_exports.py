"""Validate both delivered streams and retain exact hashes and caption timing evidence."""
import hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parents[1]
def main():
 rows=json.loads((R/'timing.json').read_text(encoding='utf-8'));manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
 assert len(rows)==29 and rows[0]['start']==0 and rows[-1]['end']==140
 assert all(a['end']==b['start'] for a,b in zip(rows,rows[1:]))
 assert len(manifest)==14 and sum(m['duration_seconds'] for m in manifest)==140
 report={}
 for layout,wh in [('longform',(1920,1080)),('shorts',(1080,1920))]:
  p=W/'exports'/f'gpui06_memory_140s_{layout}_final.mp4'
  streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_name,codec_type,width,height,r_frame_rate,nb_read_frames,duration','-of','json',str(p)]))['streams']
  assert len(streams)==1 and streams[0]['codec_type']=='video'
  v=streams[0];assert (v['width'],v['height'])==wh and v['r_frame_rate']=='30/1'
  assert int(v['nb_read_frames'])==4200 and float(v['duration'])==140 and v['codec_name']=='h264'
  assert p.with_name(p.stem+'_captions.srt').read_bytes()==(R/'captions.srt').read_bytes()
  report[layout]=dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),**v)
 (R/'verification_final.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
