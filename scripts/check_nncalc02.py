"""Inspect delivered video metadata and sample every scene plus circuit details."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'episodes/nncalc02_induction_heads'
EXPECTED=[1,3,5,11,17,22,27,33,37,42,46,51,54,61,64,71,74,78,83,92,95,100,108,114,123,131,139,142,149,154,156,158,165]

def main():
    shorts='--shorts' in sys.argv;preview='--preview' in sys.argv
    episode='nncalc02_shorts' if shorts else 'nncalc02'
    video=ROOT/'exports'/(episode+('_preview' if preview else '')+'.mp4')
    out=ROOT/'media'/episode/'qa';out.mkdir(parents=True,exist_ok=True)
    data=json.loads((FOLDER/'timing.json').read_text(encoding='utf-8'))
    metadata=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    stream=next(s for s in metadata['streams'] if s['codec_type']=='video')
    expected=((360,640) if preview else (1080,1920)) if shorts else ((640,360) if preview else (1920,1080))
    assert (stream['width'],stream['height'])==expected and stream['r_frame_rate']=='30/1'
    duration=float(metadata['format']['duration']);assert abs(duration-165)<.1
    assert [q['end'] for q in data['cues']]==EXPECTED
    assert all(a['end']==b['start'] for a,b in zip(data['cues'],data['cues'][1:]))
    tts=(FOLDER/'tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n')
    assert tts==[' '.join(q['spoken'] for q in s['cues']) for s in data['segments']]
    spec=importlib.util.spec_from_file_location('circuitqa',FOLDER/'scene.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    m.config.text_dir=str(out/'layout_texts')
    assert m.QKOVVisualizer.qk_edge==(5,2) and m.QKOVVisualizer.ov_edge==(2,5)
    row=m.TokenSequence();assert row.tokens=='ABCDA' and len(row.cells)==5
    assert m.PreviousTokenHead(row,m.ResidualStreamView(row,0)).logical_edges==[(2,1),(3,2),(4,3),(5,4)]
    scene=m.InductionVideo();scene.portrait=shorts
    for q in data['cues']:
        box=scene.caption_obj(q['text'])
        assert box.get_top()[1]<(-5.3 if shorts else -3.1)
        assert box.get_bottom()[1]>(-7.1 if shorts else -4.2)
    tw,th=(360,640) if shorts else (640,360);cols,rows=(4,2) if shorts else (2,4)
    prefix='preview' if preview else 'final'
    def frame(time,name):
        path=out/f'{prefix}_{name}.png'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(time),'-i',str(video),
            '-frames:v','1','-vf',f'scale={tw}:{th}',str(path)],check=True)
        return path
    def sheet(frames,name):
        im=Image.new('RGB',(tw*cols,(th+20)*rows),'#182633');draw=ImageDraw.Draw(im)
        for j,(caption,path) in enumerate(frames):
            x=j%cols*tw;y=j//cols*(th+20);im.paste(Image.open(path),(x,y+20));draw.text((x+9,y+3),caption,fill='white')
        path=out/f'{prefix}_{name}.jpg';im.save(path,quality=94);return str(path)
    sampled=[]
    for s in data['segments']:
        time=s['start']+(s['end']-s['start'])*.65
        sampled.append((f'{s["index"]:02} / {time:.1f}s',frame(time,f'{s["index"]:02}')))
    sheets=[sheet(sampled[i:i+8],f'sheet_{i//8+1}') for i in range(0,len(sampled),8)]
    details=[(f'{time}s',frame(time,f'detail_{time}')) for time in [44,49,58,62,68,119,128,162]]
    critical=sheet(details,'critical')
    result=dict(video=str(video),duration=duration,width=stream['width'],height=stream['height'],fps=stream['r_frame_rate'],
        audio_streams=sum(s['codec_type']=='audio' for s in metadata['streams']),
        timing_basis=data['timing_basis'],user_sentence_ends_verified=True,cues=33,sections=19,
        narration_tts_consistent=True,caption_layout_verified=True,input_positions=5,prediction_slot_is_input=False,
        qk_selection=[5,2],ov_information_flow=[2,5],contact_sheets=sheets,critical_frames=critical)
    (out/f'{prefix}_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
