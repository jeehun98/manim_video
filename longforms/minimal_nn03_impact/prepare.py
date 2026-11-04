"""Exact narration clock, independent specifications and computed demonstration data."""
import json,shutil
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent
LINES='''3|신경망에는 수많은 가중치와 뉴런이 존재합니다.
7|그런데 이 모든 차원이 실제 예측에 필요한 것은 아닐 수도 있습니다.
13|앞서 우리는 신경망 내부의 표현이 예상보다 낮은 차원에 존재할 가능성을 살펴봤습니다.
16|하지만 그 차원을 정확하게 측정하는 것은 쉽지 않았습니다.
21|그렇다면 차원이 몇 개인지 알아내는 대신, 실제로 줄여보면 어떨까요?
23|큰 언어모델을 생각해 보겠습니다.
28|모델 내부에는 수많은 가중치 행렬이 있고, 이 행렬들을 이용해 입력 데이터를 변환합니다.
33|이때 하나의 큰 행렬을 두 개의 작은 행렬로 나누면, 전체 파라미터 수를 줄일 수 있습니다.
36|이것이 저랭크 압축의 기본적인 아이디어입니다.
42|하지만 무작정 차원을 줄이면 원래 행렬이 수행하던 계산에 오차가 발생합니다.
46|기존의 저랭크 압축 방법은 주로 이 오차를 작게 만드는 데 집중했습니다.
48|그런데 여기서 문제가 있습니다.
53|행렬을 원래와 비슷하게 복원한다고 해서, 신경망의 예측까지 유지되는 것은 아닙니다.
59|같은 크기의 오차라도 어떤 방향에서 발생했는지에 따라 최종 성능에 미치는 영향이 달라질 수 있기 때문입니다.
66|2026년, 연구진은 이러한 문제를 해결하기 위해 IMPACT라는 압축 방법을 제안했습니다.
72|연구진은 먼저 신경망 내부에서 실제 데이터가 통과할 때 만들어지는 활성화값을 분석했습니다.
78|가중치 행렬 자체보다 활성화값에서 더 뚜렷한 저랭크 구조가 나타날 수 있다는 점에 주목한 것입니다.
84|하지만 활성화값을 최대한 비슷하게 복원하는 것만으로도 충분하지 않았습니다.
88|모든 활성화 방향이 최종 예측에 똑같이 중요한 것은 아니기 때문입니다.
91|그래서 연구진은 기울기 정보를 함께 사용했습니다.
97|특정 방향에서 오차가 발생했을 때 모델의 손실이 얼마나 민감하게 변하는지를 고려한 것입니다.
102|이 정보를 바탕으로 중요한 활성화 방향을 우선적으로 보존하는 저랭크 압축을 구성했습니다.
109|즉, 모든 방향을 똑같이 복원하는 대신, 성능에 중요한 방향의 오차를 더 작게 만들도록 한 것입니다.
117|그 결과 여러 언어모델과 평가 작업에서 기존 압축 방법보다 모델 크기를 더 줄이면서도 비슷하거나 더 나은 정확도를 유지했습니다.
123|일부 비교에서는 기존 방법보다 최대 55.4퍼센트 더 큰 모델 크기 감소를 달성했습니다.
128|물론 모든 모델에서 같은 결과가 나타난다는 뜻은 아닙니다.
130|하지만 중요한 차이는 분명했습니다.
137|원래 행렬을 가장 정확하게 복원하는 것과, 신경망의 기능을 가장 잘 유지하는 것은 같은 문제가 아니었습니다.
141|신경망의 최소 표현을 찾기 위해 반드시 모든 정보를 보존할 필요는 없습니다.
146|중요한 것은 어떤 정보를 제거했을 때 실제 기능이 달라지는가입니다.
150|그렇다면 신경망의 모든 층에서도 이러한 압축이 똑같이 가능할까요?
156|아니면 어떤 층은 더 많이 줄일 수 있고, 어떤 층은 반드시 유지해야 하는 차원이 존재할까요?'''
SCENES=[('opening',0,21,'차원을 측정하는 대신 실제로 줄여보자'),('factorization',21,36,'큰 행렬을 두 작은 행렬로 저랭크 근사한다'),('error_direction',36,59,'같은 크기의 오차도 방향에 따라 예측이 달라진다'),('activations',59,78,'IMPACT는 활성화의 구조를 관찰한다'),('activation_space',78,88,'활성화 복원만으로 성능 보존을 보장할 수 없다'),('importance',88,109,'기울기 중요도를 함께 반영해 복원 기저를 구성한다'),('results',109,128,'비교 방법 대비 최대 55.4% 더 큰 모델 크기 감소'),('function',128,146,'원본 복원과 기능 보존은 다른 목표다'),('layers',146,156,'층마다 유지해야 하는 차원이 같을까?')]
DETAILS=[
'0–3초 네트워크 등장. 3–7초 모든 차원이 필요한가 질문. 7–13초 저차원 곡선. 13–16초 측정 차원에 물음표. 16–21초 Measure → Compress. 사용자 대본에 직접 포함된 연결 구간을 그대로 적용하며 추가 복습·예고 문구는 넣지 않는다.',
'21–23초 LLM 블록. 23–28초 W와 입력·출력. 28–33초 W(8×8)→A(8×3)B(3×8),64→48개. 33–36초 r=2로 줄여 A(8×2)B(2×8),32개. 반드시 r(m+n)<mn일 때만 크기 감소. SVD로 실제 A,B 계산.',
'36–42초 동일 입력의 원본·압축 출력. 42–46초 실제 W−AB 오차 격자. 46–53초 분류 결과 비교. 53–59초 h=(.3,.2)에 동일 길이 .75의 수직·수평 오차: x좌표 부호에 따른 A/B 분류. 2차원 수학적 사례이며 LLM 측정치가 아니다.',
'59–66초 ACL2026 논문. 66–72초 W는 고정하고 서로 다른 입력 x를 통과시켜 y를 수집. 72–78초 활성화 Y를 쌓고 W,Y의 계산된 특이값 집중도 대비. npz의 입력과 행렬에서 실제 계산한다.',
'78–84초 활성화 점이 평면 근처에 모이는 3D 투영. 84–88초 복원에 중요한 방향을 질문. 평면 자체를 특정 LLM의 관측 결과로 표시하지 않는다. 영상 안내성 자막은 생략하고 이 문서에만 제작 방식을 기록한다.',
'88–91초 손실 기울기 g=(-1,0) 등장. 91–97초 ε1=(0,.75),ε2=(-.75,0), 길이 동일, 내적0과.75. 국소 1차 근사 ΔL≈g·ε로 손실 민감도 설명. 97–102초 성능에 민감한 수평 방향을 보존할 부분공간 강조. 102–109초 활성화 구조+기울기 중요도→중요도 가중 공분산→복원 기저→저랭크 행렬. 랭크 탐색·가중치 업데이트로 표현하지 않는다.',
'109–117초 여러 언어모델·평가 작업 및 비교 정확도. 가상 성능 곡선이나 임의 측정 수치 없음. 117–123초 최대55.4%를 비교 방법 대비 더 큰 크기 감소로 표시. 123–128초 모델·작업·압축 조건 카드. 원본 전체의55.4% 제거율 또는55.4%p로 표현하지 않는다.',
'128–130초 기능 보존 강조. 130–137초 실제 행렬 차이 격자와 예측 보존 비교. 137–141초 기능 쪽 강조. 141–146초 어떤 정보를 제거하면 기능이 달라지는가 질문. 단순 복원과 기능 보존의 평가 대상을 구분한다.',
'146–150초 같은 크기의5개 층. 150–156초 각 층의 서로 다른 유지 차원을 물음표와 폭 차이로 질문한다. 실제 LLM의 계층별 압축률이라는 표시는 하지 않는다. 다음 편 번호·예고 문구 없이 해당 질문으로 종료.'
]
def stamp(t):return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
def main():
 rows=[];start=0
 for line in LINES.splitlines():
  end,s=line.split('|',1);end=int(end);rows.append(dict(start=start,end=end,text=s));start=end
 (R/'timing.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 script='\n\n'.join(r['text'] for r in rows)+'\n'
 for name in ['narration.md','master_script.md']:(R/name).write_text(script,encoding='utf-8')
 (R/'tts_script.txt').write_text(script.replace('2026년','이천이십육 년').replace('IMPACT','임팩트').replace('55.4퍼센트','오십오 점 사 퍼센트'),encoding='utf-8')
 (R/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows,1))+'\n',encoding='utf-8')
 ex=R/'scenes'/'01_example'
 if ex.exists():shutil.rmtree(ex)
 manifest=[]
 for i,(slug,start,end,claim) in enumerate(SCENES,1):
  folder=R/'scenes'/f'{i:02}_{slug}';folder.mkdir(parents=True,exist_ok=True)
  rr=[r for r in rows if r['start']<end and r['end']>start];speech='\n\n'.join(r['text'] for r in rr)
  (folder/'script.txt').write_text(speech+'\n',encoding='utf-8')
  (folder/'spec.md').write_text(f'# {i:02} — {claim}\n\n## 목적·핵심 주장\n{claim}\n\n## 앞 장면에서 받은 내용\n'+('네트워크의 크기와 기능에 대한 질문.' if i==1 else SCENES[i-2][3])+f'\n\n## TTS·확정 길이\n{speech}\n\n사용자 문장 종료 시각 기준 {start}–{end}초, {end-start}초. 음원 미제공.\n\n## 화면·시간별 애니메이션·텍스트\n{DETAILS[i-1]}\n\n## 시작·종료 상태·연결\n씬 하나의 주장을 완결하고 동일 행렬·오차 방향을 다음 장면에서 이어받는다. 가로는 좌우, 세로는 상하 배치.\n\n## 정확성·출처\nACL2026 IMPACT 최종본을 기준으로 한다. 단순행렬·활성화·민감도 계산은 제작용 수학적 예시이며 논문 실험의 수치 재현이 아니다. 결과의55.4%만 원문 보고 수치이다. 이 구분은 제작 문서에 기록하며 사용자의 이전 요청대로 영상 내부의 안내성 자막은 생략한다.\n',encoding='utf-8')
  (folder/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scene_engine import ImpactScene\nclass Scene{i:02}(ImpactScene):\n    index={i-1}\n',encoding='utf-8')
  manifest.append(dict(id=f'{i:02}',directory=folder.relative_to(R).as_posix(),start=start,end=end,duration_seconds=end-start,claim=claim,**{'class':f'Scene{i:02}'}))
 (R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'scenes.yaml').write_text('title: 최소 조건 2부 · 신경망 3편 · IMPACT\nduration_seconds: 156\nlayouts: [1920x1080,1080x1920]\nfps: 60\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    class: {m["class"]}\n    duration_seconds: {m["duration_seconds"]}\n' for m in manifest),encoding='utf-8')
 rng=np.random.default_rng(2026);q,_=np.linalg.qr(rng.normal(size=(8,8)));p,_=np.linalg.qr(rng.normal(size=(8,8)))
 W=q@np.diag(np.linspace(1.5,.7,8))@p.T
 X=rng.normal(size=(96,8))*np.array([2,1.1,.09,.07,.06,.05,.04,.03]);Y=X@W.T
 u,s,v=np.linalg.svd(W,full_matrices=False)
 data=dict(W=W,X=X,Y=Y,U=u,S=s,V=v,weight_spectrum=s/s[0],activation_spectrum=np.linalg.svd(Y,compute_uv=False)/np.linalg.svd(Y,compute_uv=False)[0])
 for rank in [2,3,4]:data[f'A{rank}']=u[:,:rank]*s[:rank];data[f'B{rank}']=v[:rank]
 residual=W.copy();residual[0]=0;ru,rs,rv=np.linalg.svd(residual,full_matrices=False)
 Wf=np.outer(np.eye(8)[0],W[0])+np.outer(ru[:,0]*rs[0],rv[0])
 candidates=rng.normal(size=(2000,8));wrong=np.flatnonzero(np.sign(candidates@W[0])!=np.sign(candidates@(data['A2']@data['B2'])[0]));assert len(wrong)
 example=candidates[wrong[0]]
 if (W@example)[0]<0:example=-example
 data['W_function']=Wf;data['example_input']=example
 np.savez(R/'demonstration_data.npz',**data)
 verification=dict(original_parameters=W.size,rank2_parameters=data['A2'].size+data['B2'].size,rank3_parameters=data['A3'].size+data['B3'].size,weight_relative_rank2_error=float(np.linalg.norm(W-data['A2']@data['B2'])/np.linalg.norm(W)),orthogonal_error_norm=.75,parallel_error_norm=.75,gradient=[-1,0],loss_inner_products=[0,.75],prediction_before='A',prediction_orthogonal='A',prediction_parallel='B',total_seconds=156,final_frames=9360)
 verification['function_example']=dict(rank=int(np.linalg.matrix_rank(Wf)),first_row_preserved=bool(np.allclose(Wf[0],W[0])),svd_frobenius_error=float(np.linalg.norm(W-data['A2']@data['B2'])),function_frobenius_error=float(np.linalg.norm(W-Wf)),original_score=float((W@example)[0]),svd_score=float(((data['A2']@data['B2'])@example)[0]),function_score=float((Wf@example)[0]))
 (R/'math_verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'brief.md').write_text('# 제작 기준\n\n신경망 시리즈3편, 링크 원본 콘티04편. 사용자 확정32개 문장·156초. 롱폼1920×1080·쇼츠1080×1920,60fps·무음·전체 문장 자막. 제공 대본의7–16초 연결 구간은 최신 직접 요청을 우선해 그대로 유지하며 추가 복습·예고는 넣지 않는다. 종료 질문은 영상 자체의 질문으로 남긴다.\n\n행렬 파라미터 감소는 r(m+n)<mn. 8×8→8×3와3×8은64→48, r=2는32. SVD·활성화·오차 내적은실제 계산. 기울기는 활성화 교란의 국소 손실 민감도이며 가중치 업데이트가 아니다. IMPACT는 중요도 가중 활성화 공분산의 기저를 구성하는 방식으로 표현한다.\n\n55.4%는 ACL2026 최종본의 비교 방법 대비 최대 모델 크기 감소 개선량이다. 원본 전체 제거율과 혼동하지 않는다. 가상 성능 곡선·가짜 정확도 수치를 넣지 않는다. 안내성 데이터 자막은 기존 사용자 요청대로 제외한다.\n\n콘티: https://chatgpt.com/s/t_6ae8122ed2008191a469909546d5410a\n논문: https://aclanthology.org/2026.acl-long.183/\nPDF: https://aclanthology.org/2026.acl-long.183.pdf\n',encoding='utf-8')
if __name__=='__main__':main()
