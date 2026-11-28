"""Prepend the voiced intro to the existing verified longform picture."""
from pathlib import Path
import importlib.util,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
b=load('assembly',HERE.parent/'complex_geometry_full_01_04/build.py')
b.HERE=HERE

def main():
 intro=b.pair(0);intro['title']='인트로 — 수의 확장에서 공간의 발견까지'
 previous=json.loads((HERE.parent/'complex_geometry_full_01_04/verification.json').read_text(encoding='utf-8'))
 chapters=[intro,*previous['chapters']]
 offset=0;meta=[';FFMETADATA1','title='+b.TITLE]
 for c in chapters:
  c['start_seconds']=offset/30
  meta+=['[CHAPTER]','TIMEBASE=1/30',f'START={offset}',f'END={offset+c["frames"]}',f'title={c["title"]}'];offset+=c['frames']
 metadata=HERE/'chapters.ffmetadata';metadata.write_text('\n'.join(meta)+'\n',encoding='utf-8')
 manifest=HERE/'concat.txt';pictures=[]
 # Video-only remuxes prevent the concat demuxer from shifting picture timestamps
 # to accommodate the unused AAC encoder priming packets.
 for name,p,d in [('intro',intro['output'],intro['duration']),('body',previous['output'],previous['duration_seconds'])]:
  picture=HERE/(name+'_picture.mp4')
  b.run(['-y','-i',p,'-map','0:v:0','-c:v','copy','-an','-map_chapters','-1',str(picture)],HERE/(name+'_picture.log'))
  pictures.append((picture,d))
 manifest.write_text(''.join("file '"+p.as_posix()+"'\nduration "+f'{d:.12f}'+'\n' for p,d in pictures),encoding='utf-8')
 final=b.EXPORT/'complex_geometry_full_00_04_longform.mp4';temp=final.with_name(final.stem+'.building.mp4')
 inputs=['-y','-copyts','-f','concat','-safe','0','-i',str(manifest),'-i',str(metadata)]
 filters=[]
 for j,c in enumerate(chapters):
  inputs+=['-i',c['audio']]
  filters.append(f'[{j+2}:a:0]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono,apad,atrim=end_sample={c["frames"]*1600},asetpts=PTS-STARTPTS[a{j}]')
 filters.append(''.join(f'[a{j}]' for j in range(5))+'concat=n=5:v=0:a=1[voice]')
 b.run(inputs+['-filter_complex',';'.join(filters),'-map','0:v:0','-map','[voice]','-map_metadata','1','-map_chapters','1','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','1','-t',f'{offset/30:.9f}','-movflags','+faststart',str(temp)],HERE/'concat.log');temp.replace(final)
 result=b.probe(final);v=next(s for s in result['streams'] if s['codec_type']=='video');a=next(s for s in result['streams'] if s['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',offset)
 assert abs(float(v['duration'])-offset/30)<.002 and abs(float(a['duration'])-offset/30)<.025
 assert len(result['chapters'])==5
 for actual,c in zip(result['chapters'],chapters):assert abs(float(actual['start_time'])-c['start_seconds'])<.001
 b.run(['-v','error','-i',str(final),'-map','0:v:0','-map','0:a:0','-f','null','-'],HERE/'decode_check.log')
 assert not (HERE/'decode_check.log').read_text().strip()
 cues=[]
 for c in chapters:
  sentences=json.loads((HERE.parent/f'complex_geometry_{c["number"]:02}/script.json').read_text(encoding='utf-8'))['sentences']
  for j,s in enumerate(sentences):cues.append((c['start_seconds']+s['start'],c['start_seconds']+(c['duration'] if j==len(sentences)-1 else s['end']),s['text']))
 assert len(cues)==201 and all(x<y for x,y,_ in cues)
 assert all(abs(x[1]-y[0])<.00001 for x,y in zip(cues,cues[1:])) and abs(cues[-1][1]-offset/30)<.00001
 final.with_name(final.stem+'_captions.srt').write_text('\n\n'.join(f'{i}\n{b.timecode(x)} --> {b.timecode(y)}\n{s}' for i,(x,y,s) in enumerate(cues,1))+'\n',encoding='utf-8')
 old=(HERE.parent/'complex_geometry_full_01_04/youtube_description.txt').read_text(encoding='utf-8')
 before,tail=old.split('챕터\n',1);_,after=tail.split('\n\n',1)
 description=before+'챕터\n'+'\n'.join(b.yt(c['start_seconds'])+' '+c['title'] for c in chapters)+'\n\n'+after
 (HERE/'youtube_description.txt').write_text(description,encoding='utf-8')
 (b.EXPORT/'complex_geometry_full_00_04_youtube_description.txt').write_text(description,encoding='utf-8')
 report=dict(output=str(final),chapters=chapters,duration_seconds=offset/30,video_frames=offset,video=v,audio=a,caption_cues=len(cues),full_decode='passed',previous_picture=previous['output'],method='Copy intro and existing full picture; encode five original voices once with exact sample boundaries; preserve complete audio and hold intro last frame.')
 (HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 check=load('alignment',HERE.parent/'complex_geometry_full_01_04/check_audio_alignment.py');check.HERE=HERE;check.main()
 print(f'COMPLETE {final}: {offset/30:.3f}s; intro {intro["duration"]:.3f}s',flush=True)
if __name__=='__main__':main()
