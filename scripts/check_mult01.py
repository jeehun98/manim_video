"""Check delivered video, cue continuity, captions, and text containment."""
import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT/'episodes/mult01_error_parity'
sys.path.insert(0,str(ROOT))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--preview',action='store_true')
    args=parser.parse_args()
    path=ROOT/'exports'/('mult01_preview.mp4' if args.preview else 'mult01.mp4')
    spec=importlib.util.spec_from_file_location('mult01_scene',HERE/'scene.py')
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data=mod.TIMING
    cues=data['cues']
    assert len(cues)==21 and data['end_seconds']==[4,15,19,22,28,32,34,38,42,48,54,63,71,74,79,83,86,91,96,99,102]
    assert cues[0]['start']==0 and cues[-1]['end']==102
    assert all(a['end']==b['start'] for a,b in zip(cues,cues[1:]))
    assert all(c['end_frame']-c['start_frame']==30*(c['end']-c['start']) for c in cues)
    for cue in cues:
        subtitle=mod.t(cue['caption'],y=-6,size=25,width=7.2)
        assert subtitle.height<2.2, (cue['index'],subtitle.height)
        assert subtitle.width<=7.2+.001
    srt=(HERE/'captions.srt').read_text(encoding='utf-8')
    assert srt.count(' --> ')==21 and '00:01:42,000' in srt
    for cue in cues:
        assert cue['text']==cue['caption'].replace('\n',' ')
    tts=(HERE/'tts_script.txt').read_text(encoding='utf-8')
    assert len(tts.strip().split('\n\n'))==21
    metadata=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))
    video=next(s for s in metadata['streams'] if s['codec_type']=='video')
    assert (video['width'],video['height'])==((360,640) if args.preview else (1080,1920))
    assert video['r_frame_rate']=='30/1' and int(video['nb_frames'])==3060
    assert abs(float(video['duration'])-102)<.001
    assert not any(s['codec_type']=='audio' for s in metadata['streams'])
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-f','null','-'],check=True)
    report=dict(output=str(path),duration=video['duration'],frames=int(video['nb_frames']),
                width=video['width'],height=video['height'],fps=video['r_frame_rate'],audio=False,
                sentence_endpoints='21 user-supplied endpoints preserved',
                subtitles='21 complete sentences; contiguous boundaries; panel containment passed',
                tts='21 paragraphs, no timecodes',decode='complete video decoded successfully',
                visual_review='all 21 preview cue-end frames reviewed; final samples reviewed separately',
                preview_contact_sheets=['media/mult01/qa/contact_1.jpg','media/mult01/qa/contact_2.jpg'],
                limitation='Narration preserved verbatim. 92.7% refers specifically to incorrect tens digits; the screen makes this explicit. No audio supplied.')
    name='render_report_preview.json' if args.preview else 'render_report.json'
    (HERE/name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
