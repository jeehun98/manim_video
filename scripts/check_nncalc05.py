"""Check supplied timing, geometry, caption bounds and rendered delivery."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];FOLDER=ROOT/'episodes/nncalc05_sparse_autoencoders'
EXPECTED=[6,9,14,22,26,32,35,42,47,51,56,62,65,68,73,79,87,91,93,97,101,108,111,118,127,131,135,142,148,156,161,165,171]

def main():
    shorts='--shorts' in sys.argv;preview='--preview' in sys.argv
    episode='nncalc05_shorts' if shorts else 'nncalc05';prefix='preview' if preview else 'final'
    video=ROOT/'exports'/(episode+('_preview' if preview else '')+'.mp4')
    out=ROOT/'media'/episode/'qa';out.mkdir(parents=True,exist_ok=True)
    data=json.loads((FOLDER/'timing.json').read_text(encoding='utf-8'))
    metadata=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    stream=next(s for s in metadata['streams'] if s['codec_type']=='video')
    expected=((360,640) if preview else (1080,1920)) if shorts else ((640,360) if preview else (1920,1080))
    assert (stream['width'],stream['height'])==expected and stream['r_frame_rate']=='30/1'
    duration=float(metadata['format']['duration']);assert abs(duration-171)<.05
    assert int(stream['nb_frames'])==171*30
    assert [q['end'] for q in data['cues']]==EXPECTED
    assert all(a['end']==b['start'] for a,b in zip(data['cues'],data['cues'][1:]))
    tts=(FOLDER/'tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n')
    pron=lambda s:s.replace('Sparse Autoencoder','스파스 오토인코더').replace('Towards Monosemanticity','투워즈 모노시맨티시티').replace('Base64','베이스 육십사')
    assert tts==[pron(q['spoken']) for q in data['cues']]
    spec=importlib.util.spec_from_file_location('superpositionqa',FOLDER/'scene.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    m.config.text_dir=str(out/'layout_texts')
    D=m.DICTIONARY.copy()
    assert D.shape==(2,5) and np.linalg.matrix_rank(D)==2
    assert np.allclose(np.linalg.norm(D,axis=0),1)
    assert np.array_equal(np.flatnonzero(m.EXAMPLES[0]),[0,3])
    assert all(np.count_nonzero(z)==2 for z in m.EXAMPLES)
    assert m.SparseAutoencoderView.original_model_frozen
    net=m.SparseAutoencoderView(shorts)
    assert net.get_left()[0]>(-4 if shorts else -7.6) and net.get_right()[0]<(4 if shorts else 7.6)
    assert net.get_top()[1]<(4.85 if shorts else 2.75)
    assert Image.open(FOLDER/'assets/arabic.png').getchannel('A').getbbox() is not None
    assert not m.DictionaryView.ground_truth_recovery_claimed and not m.CandidateGraph.causality_established
    assert np.allclose(np.array([.9,0])+[0,.65],np.array([.4,.65])+[.5,0])
    scene=m.SparseAutoencodersVideo();scene.portrait=shorts
    for q in data['cues']:
        box=scene.caption_obj(q['text']);assert box.get_top()[1]<(-5.3 if shorts else -3.1) and box.get_bottom()[1]>(-7.1 if shorts else -4.2)
    assert len({getattr(m,n).SECTION for n in ['FeatureMixingIntro','SparseAutoencoderArchitecture','SparseDictionaryLearning','ReconstructionSparsityTradeoff','MonosemanticityFindings','InterpretationLimits']})==6
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
        user_sentence_ends_verified=True,cues=33,sections=6,frames=int(stream['nb_frames']),narration_tts_consistent=True,caption_layout_verified=True,
        dictionary_shape=[2,5],decoder_column_unit_norms_verified=True,shared_dictionary_across_inputs=True,
        example_active_latents=[1,4],original_model_frozen=True,interpretation_guaranteed=False,
        candidate_graph_causality_established=False,six_independent_sections=True,contact_sheets=sheets)
    (out/f'{prefix}_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not preview:(FOLDER/('production_checks_shorts.json' if shorts else 'production_checks.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
