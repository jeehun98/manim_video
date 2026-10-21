"""Check supplied timing, geometry, caption bounds and rendered delivery."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];FOLDER=ROOT/'episodes/nncalc04_feature_superposition'
EXPECTED=[5,11,14,19,22,27,33,37,40,48,51,57,64,70,74,84,89,95,99,105,110,114,119,123,129,133,137,142,147,152,158,166,173,178]

def main():
    shorts='--shorts' in sys.argv;preview='--preview' in sys.argv
    episode='nncalc04_shorts' if shorts else 'nncalc04';prefix='preview' if preview else 'final'
    video=ROOT/'exports'/(episode+('_preview' if preview else '')+'.mp4')
    out=ROOT/'media'/episode/'qa';out.mkdir(parents=True,exist_ok=True)
    data=json.loads((FOLDER/'timing.json').read_text(encoding='utf-8'))
    metadata=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    stream=next(s for s in metadata['streams'] if s['codec_type']=='video')
    expected=((360,640) if preview else (1080,1920)) if shorts else ((640,360) if preview else (1920,1080))
    assert (stream['width'],stream['height'])==expected and stream['r_frame_rate']=='30/1'
    duration=float(metadata['format']['duration']);assert abs(duration-178)<.05
    assert int(stream['nb_frames'])==178*30
    assert [q['end'] for q in data['cues']]==EXPECTED
    assert all(a['end']==b['start'] for a,b in zip(data['cues'],data['cues'][1:]))
    tts=(FOLDER/'tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n')
    assert tts==[q['spoken'] for q in data['cues']]
    spec=importlib.util.spec_from_file_location('superpositionqa',FOLDER/'scene.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    m.config.text_dir=str(out/'layout_texts')
    V=m.vectors(m.INITIAL);a,b=np.linalg.solve(V[:,:2],V[:,2])
    assert np.linalg.matrix_rank(V)==2 and 0<a<1 and 0<b<1
    assert np.allclose(a*V[:,0]+b*V[:,1],V[:,2])
    assert np.isclose(V[:,2]@V[:,0],np.cos(np.deg2rad(40)))
    W=m.vectors(m.REGULAR)
    assert np.allclose(np.diff(m.REGULAR),np.deg2rad(72))
    assert np.all(np.abs(W[:,0])>.1) and W[0,0]>0 and W[0,4]>0
    assert m.ToyModel.nonlinear_output and m.ToyModel.tied_weights
    assert m.NeuronResponse.hypothetical
    assert m.ActivationPattern.DENSE.sum()>m.ActivationPattern.SPARSE.sum()
    assert (m.ActivationPattern.SPARSE.sum(axis=1)==2).any()
    scene=m.SuperpositionVideo();scene.portrait=shorts
    for q in data['cues']:
        box=scene.caption_obj(q['text']);assert box.get_top()[1]<(-5.3 if shorts else -3.1) and box.get_bottom()[1]>(-7.1 if shorts else -4.2)
    plane=m.FeaturePlane(shorts)
    for angle in [m.INITIAL,m.REGULAR]:
        for j,v in enumerate(angle):
            g=plane.glyph(j,v)
            assert g.get_left()[0]>-7.6 and g.get_right()[0]<7.6
            assert g.get_top()[1]<(4.85 if shorts else 2.75)
    tw,th=(360,640) if shorts else (640,360);cols,rows=(4,2) if shorts else (2,4)
    def frame(time,name):
        path=out/f'{prefix}_{name}.png'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(time),'-i',str(video),'-frames:v','1','-vf',f'scale={tw}:{th}',str(path)],check=True)
        return path
    def sheet(items,name):
        im=Image.new('RGB',(tw*cols,(th+20)*rows),'#182633');draw=ImageDraw.Draw(im)
        for j,(caption,path) in enumerate(items):
            x=j%cols*tw;y=j//cols*(th+20);im.paste(Image.open(path),(x,y+20));draw.text((x+9,y+3),caption,fill='white')
        path=out/f'{prefix}_{name}.jpg';im.save(path,quality=94);return str(path)
    sampled=[]
    for q in data['cues']:
        time=q['start']+(q['end']-q['start'])*.7
        sampled.append((f'{q["index"]+1:02} / {time:.1f}s',frame(time,f'{q["index"]+1:02}')))
    sheets=[sheet(sampled[i:i+8],f'sheet_{i//8+1}') for i in range(0,len(sampled),8)]
    result=dict(video=str(video),duration=duration,width=stream['width'],height=stream['height'],fps=stream['r_frame_rate'],
        audio_streams=sum(s['codec_type']=='audio' for s in metadata['streams']),timing_basis=data['timing_basis'],
        user_sentence_ends_verified=True,cues=34,sections=7,frames=int(stream['nb_frames']),narration_tts_consistent=True,caption_layout_verified=True,
        feature_matrix_rank=2,exact_collision_verified=True,single_feature_cross_projection_verified=True,coefficients=[float(a),float(b)],
        regular_pentagon_spacing_degrees=72,single_feature_spans_two_neurons=True,
        shared_positive_neuron_component_verified=True,relu_reconstruction_explicit=True,
        conceptual_geometry_not_measured=True,contact_sheets=sheets)
    (out/f'{prefix}_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not preview:(FOLDER/('production_checks_shorts.json' if shorts else 'production_checks.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
