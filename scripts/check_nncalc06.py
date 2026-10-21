"""Check supplied timing, geometry, caption bounds and rendered delivery."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];FOLDER=ROOT/'episodes/nncalc06_circuit_tracing'
EXPECTED=[3,8,13,16,22,26,34,39,45,50,53,62,66,71,75,81,84,88,93,99,104,109,111,117,123,128,135,139,146,148,156,159,166]

def main():
    shorts='--shorts' in sys.argv;preview='--preview' in sys.argv
    episode='nncalc06_shorts' if shorts else 'nncalc06';prefix='preview' if preview else 'final'
    video=ROOT/'exports'/(episode+('_preview' if preview else '')+'.mp4')
    out=ROOT/'media'/episode/'qa';out.mkdir(parents=True,exist_ok=True)
    data=json.loads((FOLDER/'timing.json').read_text(encoding='utf-8'))
    metadata=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    stream=next(s for s in metadata['streams'] if s['codec_type']=='video')
    expected=((360,640) if preview else (1080,1920)) if shorts else ((640,360) if preview else (1920,1080))
    assert (stream['width'],stream['height'])==expected and stream['r_frame_rate']=='30/1'
    duration=float(metadata['format']['duration']);assert abs(duration-166)<.05
    assert int(stream['nb_frames'])==166*30
    assert [q['end'] for q in data['cues']]==EXPECTED
    assert all(a['end']==b['start'] for a,b in zip(data['cues'],data['cues'][1:]))
    tts=(FOLDER/'tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n')
    assert tts==[q['spoken'] for q in data['cues']]
    spec=importlib.util.spec_from_file_location('superpositionqa',FOLDER/'scene.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    m.config.text_dir=str(out/'layout_texts')
    assert all(target>=source for source,target in m.CrossLayerTranscoderView.write_pairs)
    assert len(m.CrossLayerTranscoderView.write_pairs)==10
    assert m.AttributionGraphView.input_specific and m.AttributionGraphView.has_capital_branch and m.AttributionGraphView.has_shortcut
    assert not m.AttributionGraphView.complete_circuit and not m.AttributionGraphView.original_model_causality_established
    assert not m.ContributionEdge.measured and not m.TransformerComparison.exact_copy
    assert m.InterventionPanel.prompt_unchanged and m.InterventionPanel.target_model=='original'
    assert (m.InterventionPanel.before_output,m.InterventionPanel.after_output)==('Austin','Sacramento')
    assert '텍사스' not in m.PROMPT and '댈러스' in m.PROMPT
    graph=m.AttributionGraphView(shorts)
    assert float(graph.edge_style[5].get_fill_opacity())==0
    assert float(graph.node_style[0][0].get_fill_opacity())<.1
    assert graph.get_left()[0]>(-4 if shorts else -7.6) and graph.get_right()[0]<(4 if shorts else 7.6)
    assert graph.get_top()[1]<(4.85 if shorts else 2.9)
    assert graph.get_bottom()[1]>(-1.6 if shorts else -2.75)
    scene=m.CircuitTracingVideo();scene.portrait=shorts
    for q in data['cues']:
        box=scene.caption_obj(q['text']);assert box.get_top()[1]<(-5.3 if shorts else -3.1) and box.get_bottom()[1]>(-7.1 if shorts else -4.2)
    assert len({getattr(m,n).SECTION for n in ['CircuitQuestionIntro','TranscoderArchitecture','AttributionGraphConstruction','DallasTexasAustinCircuit','InterventionValidation','ProbingInterventionBridge']})==6
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
        clt_current_and_later_layer_writes_verified=True,input_specific_attribution_graph=True,
        capital_branch_and_shortcut_present=True,measured_weights_claimed=False,
        original_model_intervention=True,intervention_input_unchanged=True,
        before_output='Austin',after_output='Sacramento',original_model_causality_fully_established=False,
        six_independent_sections=True,contact_sheets=sheets)
    (out/f'{prefix}_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not preview:(FOLDER/('production_checks_shorts.json' if shorts else 'production_checks.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
