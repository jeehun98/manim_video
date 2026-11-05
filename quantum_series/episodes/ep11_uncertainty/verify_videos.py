"""Validate final 177-second videos after rendering, including complete decode."""
from pathlib import Path
import json,subprocess
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def main():
 reports=[]
 for layout,dims in [('shorts',(1080,1920)),('longform',(1920,1080))]:
  path=ROOT/'exports'/f'quantum11_{layout}.mp4'
  subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],check=True)
  data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]));v=data['streams'][0]
  assert len(data['streams'])==1 and v['codec_type']=='video'
  assert (v['width'],v['height'])==dims and int(v['nb_frames'])==5310 and v['r_frame_rate']=='30/1'
  assert abs(float(data['format']['duration'])-177)<.001
  raw=subprocess.check_output(['ffmpeg','-v','error','-ss','176','-i',str(path),'-vf','scale=160:90','-pix_fmt','rgb24','-f','rawvideo','-'])
  frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,90,160,3).astype(float);delta=np.abs(np.diff(frames,axis=0)).mean(axis=(1,2,3));assert len(frames)==30 and delta.max()<.5
  assert Image.open(path.with_name(path.stem+'_ending.png')).size==dims
  reports.append({'layout':layout,'duration':177,'frames':5310,'dimensions':dims,'fps':30,'full_decode':'pass','audio':'not supplied; silent','last_second_frames':len(frames),'last_second_max_mean_pixel_delta':float(delta.max())})
 report={'videos':reports,'physics_report':'physics_report.json','visual_review':'Both aspect ratios: plane wave, superposition, coupled distributions, microscope, apparatus removal, commutator, free evolution, detection and ending.'}
 (HERE/'qa_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(reports,ensure_ascii=False))
if __name__=='__main__':main()
