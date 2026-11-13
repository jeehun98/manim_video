"""Extract review sheets and decode completed deliverables. Run from repository root."""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');parser.add_argument('--layout',choices=['both','shorts','longform'],default='both');args=parser.parse_args()
    quality='preview' if args.preview else 'final';qa=ROOT/'media'/'quantum04'/'qa'/quality;qa.mkdir(parents=True,exist_ok=True)
    results=[]
    for layout in (['shorts','longform'] if args.layout=='both' else [args.layout]):
        source=ROOT/'exports'/f"quantum04_{layout}{'_preview' if args.preview else ''}.mp4"
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(source)]))
        video=next(s for s in probe['streams'] if s['codec_type']=='video')
        assert int(video['nb_frames'])==3390 and video['r_frame_rate']=='30/1'
        assert abs(float(probe['format']['duration'])-113)<.001
        assert not any(s['codec_type']=='audio' for s in probe['streams'])
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(source),'-f','null','-'],check=True)
        thumbs=[]
        for t in [2,5,14,19,25,30,43,49,54,63,69,74,81,88,93,100,106,112]:
            output=qa/f'{layout}_{t:03}.png'
            subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(source),'-frames:v','1',str(output)],check=True)
            im=Image.open(output).convert('RGB');im.thumbnail((270,480) if layout=='shorts' else (480,270))
            tile=Image.new('RGB',(im.width,im.height+24),'#151a29');tile.paste(im,(0,24));ImageDraw.Draw(tile).text((8,5),f'{layout} {t}s',fill='white');thumbs.append(tile)
        cols=5 if layout=='shorts' else 3;w,h=thumbs[0].size
        sheet=Image.new('RGB',(cols*w,((len(thumbs)+cols-1)//cols)*h),'#212735')
        for i,im in enumerate(thumbs):sheet.paste(im,((i%cols)*w,(i//cols)*h))
        sheet.save(qa/f'{layout}_contact.png')
        results.append(dict(layout=layout,width=video['width'],height=video['height'],frames=int(video['nb_frames']),duration=113,fps=30,full_decode='passed',audio='not supplied; silent',contact_sheet=str(qa/f'{layout}_contact.png')))
    (qa/'decode.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(qa,flush=True)
if __name__=='__main__':main()
