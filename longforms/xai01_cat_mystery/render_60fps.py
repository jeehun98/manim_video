from pathlib import Path
import subprocess,shutil,av,json,time
root=Path.cwd(); project=root/'longforms/xai01_cat_mystery'
items=[('01_hook','Act01Hook',111),('02_input_changes','Act02InputChanges',146),('03_internal_clues','Act03InternalClues',154),('04_intervention','Act04Intervention',193),('05_meaning_and_paths','Act05MeaningAndPaths',226)]
results=[]
for folder,cls,duration in items:
 print('START',folder,flush=True)
 media=root/'media'/('xai60_'+folder[:2]);media.mkdir(parents=True,exist_ok=True)
 with (media/'render.log').open('w',encoding='utf-8') as log:
  subprocess.run([str(root/'.venv/Scripts/python.exe'),'-m','manim','-qh','--resolution','1920,1080','--fps','60','--verbosity','ERROR','--media_dir',str(media),str(project/'scenes'/folder/'scene.py'),cls],stdout=log,stderr=log,check=True)
 source=media/'videos/scene/1080p60'/f'{cls}.mp4'
 target=root/'exports'/f'xai01_act{folder[:2]}_1080p60.mp4'
 shutil.copy2(source,target)
 shutil.copy2(project/'scenes'/folder/'captions.srt',target.with_suffix('.srt'))
 c=av.open(str(target));s=c.streams.video[0]
 assert s.frames==duration*60,(folder,s.frames)
 assert (s.width,s.height)==(1920,1080)
 t=float(s.duration*s.time_base);assert abs(t-duration)<.05,t
 c.seek(int((duration/2)/s.time_base),stream=s);next(c.decode(s))
 results.append({'act':folder,'frames':s.frames,'seconds':t,'file':str(target)})
 c.close();print('DONE',folder,s.frames,flush=True)
 (project/'render_60fps_status.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('ALL COMPLETE',flush=True)
