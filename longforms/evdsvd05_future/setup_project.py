from pathlib import Path
import json,numpy as np
ROOT=Path(__file__).resolve().parent
for name in ['build.py','verify_final.py']:
    p=ROOT/name;s=p.read_text(encoding='utf-8').replace('evdsvd04_values','evdsvd05_future').replace('103','130').replace('3090','3900')
    if name=='verify_final.py':
        s=s.replace("[(13.5,'square'),(28.5,'eigenline'),(44.,'vertical'),(64.5,'maximum'),(70.5,'minimum'),(79.,'compare'),(102.5,'score')]","[(21.,'steps'),(46.,'growth'),(61.,'trajectory'),(73.5,'cancel'),(91.,'svd'),(97.5,'twosteps'),(104.,'mismatch'),(115.,'limits'),(129.5,'score')]")
    p.write_text(s,encoding='utf-8')
p=ROOT/'prepare.py';s=p.read_text(encoding='utf-8').replace('現在の例示行列と色を保持。別行列への変更は画面に明記。','현재 예시 행렬과 색 유지. 별도 행렬로 변경할 때 화면에 명시.').replace('TTS原文・確定長さ','TTS 원문·확정 길이').replace('秒、','초, ').replace('秒。ユーザー提供の文末時刻。','초. 사용자 제공 문장 종료 시각.');p.write_text(s,encoding='utf-8')
AE=np.diag([2.,.5]);AS=np.array([[0.,-1.],[2.,0.]]);B=np.array([[.8,2.],[0.,.7]])
assert np.allclose(AS@AS,-2*np.eye(2))
assert np.allclose(np.linalg.svd(AS,compute_uv=False),[2,1])
assert np.allclose(np.linalg.svd(AS@AS,compute_uv=False),[2,2])
for n in range(10):assert np.allclose(np.linalg.matrix_power(AE,n),np.diag([2.**n,.5**n]))
norms=[float(np.linalg.norm(np.linalg.matrix_power(B,n)@[0,1])) for n in range(25)]
assert norms[1]>norms[0] and norms[-1]<norms[0]
(ROOT/'math_verification.json').write_text(json.dumps(dict(evd_eigenvalues=[2,.5],svd_values=[2,1],svd_squared_matrix_values=[2,2],transient_norms=norms,checks='passed'),indent=2),encoding='utf-8')
print('Exact matrix and transient-growth checks passed.')
