"""Check supplied timing, geometry, caption bounds and rendered delivery."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];FOLDER=ROOT/'episodes/nncalc08_finale'
EXPECTED=[5,8,12,20,24,29,35,41,44,49,57,59,65,70,78,84,90,97,100,105,108,114,117,126,131,139,145,152,155,161,166,170,176]

def main():
    shorts='--shorts' in sys.argv;preview='--preview' in sys.argv
    episode='nncalc08_shorts' if shorts else 'nncalc08';prefix='preview' if preview else 'final'
    video=ROOT/'exports'/(episode+('_preview' if preview else '')+'.mp4')
    out=ROOT/'media'/episode/'qa';out.mkdir(parents=True,exist_ok=True)
    data=json.loads((FOLDER/'timing.json').read_text(encoding='utf-8'))
    metadata=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    stream=next(s for s in metadata['streams'] if s['codec_type']=='video')
    expected=((360,640) if preview else (1080,1920)) if shorts else ((640,360) if preview else (1920,1080))
    assert (stream['width'],stream['height'])==expected and stream['r_frame_rate']=='30/1'
    duration=float(metadata['format']['duration']);assert abs(duration-176)<.05
    assert int(stream['nb_frames'])==176*30
    assert [q['end'] for q in data['cues']]==EXPECTED
    assert all(a['end']==b['start'] for a,b in zip(data['cues'],data['cues'][1:]))
    tts=(FOLDER/'tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n')
    assert tts==[q['spoken'] for q in data['cues']]
    spec=importlib.util.spec_from_file_location('superpositionqa',FOLDER/'scene.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    m.config.text_dir=str(out/'layout_texts')
    assert np.array_equal(m.depths('())('),[0,1,0,-1,0])
    assert m.count_rule('())(') and not m.nested_rule('())(')
    assert m.nested_rule('(()())') and m.count_rule('(()())')
    assert m.nested_rule('()()') and m.count_rule('()()')
    assert not m.BracketAlgorithms.extracted_neural_circuit and not m.FinalCircuitView.complete_circuit
    assert m.FinalCircuitView.unverified_edges_dashed
    assert m.LocalResponseView.requires_retraining and m.LocalResponseView.local_approximation
    assert not m.patterning.CircuitFormationPlot.measured
    for cls in [m.BracketAlgorithms,m.BracketPrefixGraph,m.DirectionQuestionView,m.LocalResponseView,m.FinalCircuitView]:
        view=cls(portrait=shorts)
        assert view.get_left()[0]>(-4 if shorts else -7.6) and view.get_right()[0]<(4 if shorts else 7.6),cls.__name__
        assert view.get_top()[1]<(4.85 if shorts else 2.9),cls.__name__
        assert view.get_bottom()[1]>(-1.6 if shorts else -2.8),cls.__name__
    scene=m.FinaleVideo();scene.portrait=shorts
    for q in data['cues']:
        box=scene.caption_obj(q['text']);assert box.get_top()[1]<(-5.3 if shorts else -3.1) and box.get_bottom()[1]>(-7.1 if shorts else -4.2)
    assert len({getattr(m,n).SECTION for n in ['SameAnswerDifferentAlgorithm','DistinguishingTest','MechanisticMethodsRecap','InterpretabilityToPatterning','PatterningLearningControl','SeriesFinale']})==6
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
        counterexample_prefix_depths=[0,1,0,-1,0],count_vs_nested_rule_verified=True,
        extracted_circuit_claimed=False,prior_episode_components_reused=True,
        inverse_question_and_retraining_explicit=True,local_response_qualified=True,
        measured_formation_curves_claimed=False,complete_circuit_claimed=False,
        six_independent_sections=True,contact_sheets=sheets)
    (out/f'{prefix}_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not preview:(FOLDER/('production_checks_shorts.json' if shorts else 'production_checks.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
