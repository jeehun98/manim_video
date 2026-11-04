"""Check that blue data points stay fixed while the projection line rotates."""
import json,subprocess
import numpy as np
from PIL import Image
from visuals import DATA,P
root=P.parents[1];out=root/'media/dot07_qa';out.mkdir(exist_ok=True)
reports=[]
for layout in ['shorts','longform']:
    short=layout=='shorts';w,h=(360,640) if short else (640,360);scale=.95 if short else .78
    center=np.array([180,264]) if short else np.array([160,180])
    expected=center+DATA*np.array([40*scale,-40*scale])
    file=P/'scenes/07_scene'/f'visual_{layout}_preview.mp4';centroids=[]
    for t in [.1,5.8,11.8]:
        dest=out/f'fixed_{layout}_{t}.png'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(file),'-frames:v','1',str(dest)],check=True)
        a=np.asarray(Image.open(dest).convert('RGB'));mask=(a[:,:,0]<125)&(a[:,:,1]>120)&(a[:,:,1]<210)&(a[:,:,2]>200)
        frame=[]
        for point,x in zip(DATA,expected):
            if np.linalg.norm(point)<1:continue
            px,py=np.rint(x).astype(int);yy,xx=np.where(mask[max(0,py-3):py+4,max(0,px-3):px+4]);assert len(xx), (layout,t,x)
            frame.append([float(xx.mean()+px-3),float(yy.mean()+py-3)])
        centroids.append(frame)
    displacement=float(np.max(np.linalg.norm(np.asarray(centroids)-np.asarray(centroids)[0],axis=2)))
    assert displacement<.6,(layout,displacement)
    reports.append(dict(layout=layout,samples_seconds=[.1,5.8,11.8],checked_points=len(centroids[0]),max_centroid_displacement_pixels=displacement))
(P/'qa_render_geometry.json').write_text(json.dumps(reports,indent=2),encoding='utf-8');print(json.dumps(reports,indent=2))
