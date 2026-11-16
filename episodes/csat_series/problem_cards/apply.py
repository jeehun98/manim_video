"""Composite a reserved problem strip above an undistorted 1600x900 lesson."""
import argparse,concurrent.futures,hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]))
def apply_card(video,episode,backup=False):
 video=Path(video).resolve();card=HERE/'assets'/f'{episode}.png'
 if not card.exists():raise FileNotFoundError(card)
 qa=ROOT/'media'/'problem_cards'/'qa';qa.mkdir(parents=True,exist_ok=True)
 source=video
 if backup:
  dest=ROOT/'exports'/'problem_card_originals'/video.name;dest.parent.mkdir(exist_ok=True)
  if not dest.exists():shutil.copy2(video,dest)
  source=dest
 info=probe(source);v=next(s for s in info['streams'] if s['codec_type']=='video');frames=int(v['nb_read_frames']);duration=float(info['format']['duration'])
 if (v['width'],v['height'])!=(1920,1080):raise ValueError('Only 1920x1080 final lessons are supported')
 temp=video.with_name(video.stem+'_card_tmp.mp4');log=qa/f'{episode}_encode.log'
 cmd=['ffmpeg','-y','-v','error','-i',str(source),'-loop','1','-framerate','30','-i',str(card),'-filter_complex_threads','1','-filter_complex','[0:v]scale=1600:900:flags=lanczos,pad=1920:1080:160:180:color=0x0B1020[body];[body][1:v]overlay=0:0:shortest=1,setsar=1[out]','-map','[out]','-map','0:a?','-c:a','copy','-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p','-r','30','-fps_mode','cfr','-frames:v',str(frames),'-movflags','+faststart',str(temp)]
 with log.open('w',encoding='utf-8') as out:subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT,check=True)
 final=probe(temp);fv=next(s for s in final['streams'] if s['codec_type']=='video')
 assert int(fv['nb_read_frames'])==frames
 assert fv['width']==1920 and fv['height']==1080 and fv['r_frame_rate']=='30/1'
 assert abs(float(final['format']['duration'])-duration)<.034
 # ffprobe count_frames fully decodes all video frames; error-level decode is an additional corruption check.
 with (qa/f'{episode}_decode.log').open('w') as out:subprocess.run(['ffmpeg','-v','error','-i',str(temp),'-f','null','-'],stdout=out,stderr=subprocess.STDOUT,check=True)
 os.replace(temp,video)
 report=dict(episode=episode,output=str(video),source=str(source),source_sha256=sha(source) if source!=video else None,card_sha256=sha(card),sha256=sha(video),frames=frames,duration=duration,width=1920,height=1080,fps=30,layout=dict(card=[0,0,1920,180],lesson=[160,180,1600,900],scale='uniform 5/6; no crop'),decode='passed',timing='unchanged',audio='preserved from source')
 (qa/f'{episode}_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 return report
def main():
 p=argparse.ArgumentParser();p.add_argument('--video');p.add_argument('--episode');p.add_argument('--all',action='store_true');p.add_argument('--workers',type=int,default=2);a=p.parse_args()
 if a.all:
  ids=[f'csat{i:02d}' for i in range(1,23)];reports=[]
  with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
   jobs={pool.submit(apply_card,ROOT/'exports'/f'{e}.mp4',e,True):e for e in ids}
   for job in concurrent.futures.as_completed(jobs):
    r=job.result();reports.append(r);print(f"DONE {r['episode']} {r['duration']} sec {r['frames']} frames",flush=True)
  (HERE/'batch_report.json').write_text(json.dumps(sorted(reports,key=lambda r:r['episode']),ensure_ascii=False,indent=2),encoding='utf-8')
 else:print(json.dumps(apply_card(a.video,a.episode),ensure_ascii=False))
if __name__=='__main__':main()
