"""Assemble only explicit, completed longform chapters; planned episodes are never used."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from quantum_series.episodes.ep01_planck.build import probe,timestamp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',type=Path,default=HERE/'chapters.json')
    parser.add_argument('--output',type=Path,default=ROOT/'exports'/'quantum_series_longform.mp4')
    args=parser.parse_args()
    data=json.loads(args.manifest.read_text(encoding='utf-8'))
    work=ROOT/'media'/'quantum_series'/'assembly'
    work.mkdir(parents=True,exist_ok=True)
    paths=[];metadata=[';FFMETADATA1'];captions=[];elapsed=0;signature=None
    for chapter in data['chapters']:
        path=ROOT/chapter['video']
        info=probe(path)
        stream=next(s for s in info['streams'] if s['codec_type']=='video')
        sig=(stream['width'],stream['height'],stream['r_frame_rate'],stream['codec_name'],
             tuple(s['codec_type'] for s in info['streams']))
        if signature and signature!=sig:raise ValueError('Chapter video/audio formats differ; normalize before assembly.')
        signature=sig
        duration=float(info['format']['duration'])
        if abs(duration-chapter['duration'])>.02:raise ValueError(f"Unexpected duration: {path}")
        paths.append(path)
        safe_title=chapter['title'].replace('\\','\\\\').replace('=','\\=').replace(';','\\;').replace('#','\\#').replace('\n',' ')
        metadata.extend(['[CHAPTER]','TIMEBASE=1/1000',f'START={round(elapsed*1000)}',f'END={round((elapsed+duration)*1000)}',f'title={safe_title}'])
        script=json.loads((ROOT/chapter['script']).read_text(encoding='utf-8'))
        for sentence in script['sentences']:
            captions.append(f"{len(captions)+1}\n{timestamp(elapsed+sentence['start'])} --> {timestamp(elapsed+sentence['end'])}\n{sentence['text']}")
        elapsed+=duration
    if not paths:raise ValueError('No completed chapters')
    concat=work/'concat.txt';meta=work/'chapters.ffmeta'
    concat.write_text('\n'.join("file '"+str(p.resolve()).replace('\\','/')+"'" for p in paths)+'\n',encoding='utf-8')
    meta.write_text('\n'.join(metadata)+'\n',encoding='utf-8')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),
                    '-i',str(meta),'-map','0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(args.output)],check=True)
    args.output.with_suffix('.srt').write_text('\n\n'.join(captions)+'\n',encoding='utf-8')
    print(f'{args.output} · {elapsed:.3f}s · {len(paths)} chapter(s)')

if __name__=='__main__':main()
