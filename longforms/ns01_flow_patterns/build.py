"""Render independent scenes and concatenate the silent Act 1."""
import argparse,json,subprocess,sys,shutil
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]

def run(args): subprocess.run(args,check=True,cwd=WORKSPACE)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--preview',action='store_true'); parser.add_argument('--scene',type=int); parser.add_argument('--concat-only',action='store_true'); args=parser.parse_args()
    manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    durations=[s['duration_seconds'] if s['duration_seconds'] is not None else s['storyboard_seconds'] for s in manifest]
    total_seconds=sum(durations)
    resolution='854,480' if args.preview else '1920,1080'
    fps=15 if args.preview else 30
    suffix='preview' if args.preview else '1080p30'
    files=[]
    for s in manifest:
        target=ROOT/s['directory']/f'visual_{suffix}.mp4'; files.append(target)
        if args.concat_only:continue
        if args.scene and int(s['id'])!=args.scene:continue
        media=WORKSPACE/'media'/f'ns01_{suffix}'/s['id']
        run([sys.executable,'-m','manim','--resolution',resolution,'--fps',str(fps),'--verbosity','ERROR','--media_dir',str(media),str(ROOT/s['directory']/'scene.py'),s['class']])
        candidates=list(media.rglob(s['class']+'.mp4'))
        if len(candidates)!=1:raise RuntimeError(candidates)
        shutil.copy2(candidates[0],target)
    if args.scene:return
    concat=ROOT/f'concat_{suffix}.txt'
    concat.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in files)+'\n',encoding='utf-8')
    exports=WORKSPACE/'exports';exports.mkdir(exist_ok=True)
    output=exports/f'ns01_act01_{total_seconds:g}s_{suffix}.mp4'
    import av
    # Normalize timestamps to a single frame clock; concat demuxer duration
    # rounding otherwise introduces tiny chapter boundary offsets.
    frame_offset=0; clock_base=Fraction(1,fps*512)
    with av.open(str(files[0])) as template, av.open(str(output),'w',options={'movflags':'+faststart'}) as destination:
        out=destination.add_stream_from_template(template.streams.video[0]); out.time_base=clock_base
        reference=None
        for source_path,record,duration in zip(files,manifest,durations):
            count=0
            with av.open(str(source_path)) as source:
                stream=source.streams.video[0]
                parameters=(stream.width,stream.height,stream.codec_context.name,stream.codec_context.extradata)
                if reference is None:reference=parameters
                assert parameters==reference,source_path
                assert stream.frames==round(duration*fps),source_path
                for packet in source.demux(stream):
                    if packet.pts is None or packet.dts is None:continue
                    pts=round(packet.pts*packet.time_base*fps)+frame_offset
                    dts=round(packet.dts*packet.time_base*fps)+frame_offset
                    packet.pts=pts*512; packet.dts=dts*512; packet.duration=512
                    packet.time_base=clock_base; packet.stream=out
                    destination.mux(packet);count+=1
            assert count==round(duration*fps)
            frame_offset+=count
    shutil.copy2(ROOT/'captions.srt',output.with_suffix('.srt'))
    with av.open(str(output)) as video:
        stream=video.streams.video[0]
        assert stream.frames==round(total_seconds*fps),(stream.frames,total_seconds*fps)
        assert (stream.width,stream.height)==tuple(map(int,resolution.split(',')))
        assert abs(float(stream.duration*stream.time_base)-total_seconds)<1/fps
        assert stream.average_rate==fps,stream.average_rate
        print(f'OK: {output}; {stream.frames} frames; {fps} fps; {total_seconds:g} seconds')

if __name__=='__main__':main()
