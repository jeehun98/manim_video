"""Compare decoded subtitle pixels with clean captions around every boundary."""
import argparse,json,os,subprocess
from pathlib import Path
import numpy as np
from PIL import Image

def main():
    ap=argparse.ArgumentParser();ap.add_argument('video');ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    os.environ['QUANTUM_PREVIEW']=str(int(args.preview))
    from scene import SCRIPT,label,wrapped,Scene
    video=Path(args.video).resolve()
    out=video.parents[1]/'media/science22/caption_review'/('preview' if args.preview else 'final')
    out.mkdir(parents=True,exist_ok=True)
    width,height=(360,640) if args.preview else (1080,1920)
    top=int(height*.8)
    camera=Scene().camera
    references=[]
    for end,s in SCRIPT['sentences']:
        camera.reset();camera.capture_mobjects([label(wrapped(s),-6,28)])
        references.append(np.asarray(camera.get_image().convert('RGB').crop((0,top,width,height))).astype(float))
    boundaries=[0]+[end*30 for end,s in SCRIPT['sentences'][:-1]]
    frames=sorted({max(0,min(4079,b+delta)) for b in boundaries for delta in [-1,0,1]}|{4079})
    select='+'.join(f'eq(n,{f})' for f in frames)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f"select='{select}',crop={width}:{height-top}:0:{top}",'-fps_mode','vfr',str(out/'frame_%03d.png')],check=True)
    results=[]
    for i,frame in enumerate(frames,1):
        index=next((j for j,(end,s) in enumerate(SCRIPT['sentences']) if frame<end*30),25)
        actual=np.asarray(Image.open(out/f'frame_{i:03d}.png').convert('RGB')).astype(float)
        error=float(np.abs(actual-references[index]).mean())
        # Ignore the uniform RGB shift from H.264 YUV conversion. Compare
        # bright glyph pixels; a stale caption adds substantial extra ink.
        expected_mask=references[index].max(axis=2)>110
        actual_mask=actual.max(axis=2)>110
        mismatch=float(np.count_nonzero(actual_mask!=expected_mask)/expected_mask.sum())
        results.append({'frame':frame,'sentence':index+1,'mean_pixel_error':round(error,4),'glyph_mismatch_ratio':round(mismatch,4)})
    report={'frames_checked':len(results),'method':'decoded subtitle glyph mask versus clean caption at each boundary -1/0/+1 frame','max_glyph_mismatch_ratio':max(r['glyph_mismatch_ratio'] for r in results),'glyph_mismatch_limit':.12,'results':results}
    (out/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    # Negative control: synthetic overlap of every adjacent caption must fail.
    masks=[r.max(axis=2)>110 for r in references]
    assert all(np.count_nonzero((a|b)!=b)/b.sum()>.12 for a,b in zip(masks,masks[1:])), 'Overlap negative control failed'
    failed=[r for r in results if r['glyph_mismatch_ratio']>.12]
    assert not failed,failed
    print(f"Caption checks passed: {len(results)} frames; maximum glyph mismatch {report['max_glyph_mismatch_ratio']:.4f}")

if __name__=='__main__':main()
