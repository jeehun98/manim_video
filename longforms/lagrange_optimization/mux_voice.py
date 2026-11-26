"""Attach the supplied narration, preserving its ending and the visual timing."""
from pathlib import Path
import hashlib,json,math,shutil,subprocess
R=Path(__file__).resolve().parent;W=R.parents[1]
VIDEO=W/'exports/lagrange_optimization_426s_final.mp4'
AUDIO=W/'exports/최적화.mp3'
OUT=W/'exports/lagrange_optimization_426s_voiced.mp4'
def probe(p,count=False):
 cmd=['ffprobe','-v','error']+(['-count_frames'] if count else [])+['-show_streams','-show_format','-of','json',str(p)]
 return json.loads(subprocess.check_output(cmd))
def main():
 vi=probe(VIDEO);ai=probe(AUDIO);v=next(s for s in vi['streams'] if s['codec_type']=='video')
 audio_duration=float(ai['format']['duration']);original=float(v['duration']);fps=30
 frames=round(original*fps);extra=max(0,math.ceil((audio_duration-original)*fps));duration=(frames+extra)/fps
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(VIDEO),'-i',str(AUDIO),'-map','0:v:0','-map','1:a:0',
      '-vf',f'tpad=stop_mode=clone:stop={extra}','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
      '-af','apad','-c:a','aac','-b:a','192k','-t',f'{duration:.9f}','-movflags','+faststart',str(OUT)]
 subprocess.run(cmd,check=True)
 info=probe(OUT,True);vs=next(s for s in info['streams'] if s['codec_type']=='video');aud=next(s for s in info['streams'] if s['codec_type']=='audio')
 assert (vs['width'],vs['height'])==(1920,1080) and vs['avg_frame_rate']=='30/1'
 assert int(vs['nb_read_frames'])==frames+extra and abs(float(vs['duration'])-duration)<.001
 assert float(aud['duration'])>=audio_duration-.04 and abs(float(aud['duration'])-duration)<.04
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(OUT),'-f','null','NUL'],check=True)
 shutil.copyfile(R/'captions.srt',OUT.with_suffix('.srt'))
 report=dict(output=str(OUT),source_video_sha256=hashlib.sha256(VIDEO.read_bytes()).hexdigest(),source_audio_sha256=hashlib.sha256(AUDIO.read_bytes()).hexdigest(),source_audio_duration=audio_duration,original_video_duration=original,appended_last_frame_count=extra,final_video=vs,final_audio=aud,sentence_timing_unchanged=True,decode_check='passed')
 (R/'verification_voiced.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('COMPLETE',OUT,flush=True);print('DURATION',duration,'APPENDED_FRAMES',extra,flush=True)
if __name__=='__main__':main()
