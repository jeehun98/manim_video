# Manim 교육 영상 프로젝트

## 롱폼 제작

롱폼은 짧은 완성 씬을 독립적으로 제작한 뒤 결합하는 방식으로 관리합니다. 새 롱폼을 시작하거나 다른 환경에서 이어서 작업할 때는 [롱폼 제작 규격](longforms/README.md)과 [`longforms/_template`](longforms/_template/)를 먼저 확인하세요.

# Activation Function Series

## 분포의 수학

- 분포의 수학 01 **분포는 무엇을 나타내는가?** — 52초, 1080×1920, 30fps, 무음. 여섯 관측값을 값 공간에 모아 경험적 확률을 만든 뒤, 분포를 가능한 값에 놓인 확률의 구조로 소개합니다. 미지의 생성 분포와 경험적 분포를 구별하고 마지막에는 분포의 중심을 묻습니다.
- 실제 파일: [장면](episodes/dist01_what_is_distribution/scene.py) · [대본](episodes/dist01_what_is_distribution/narration.md) · [제작 기준](episodes/dist01_what_is_distribution/brief.md) · [자막](episodes/dist01_what_is_distribution/captions.srt) · [TTS](episodes/dist01_what_is_distribution/tts_script.txt)
- 미리보기: `python scripts/render.py dist01 --preview` → `exports/dist01_preview.mp4`
- 최종본: `python scripts/render.py dist01` → `exports/dist01.mp4`
- 분포의 수학 02 **분포의 중심은 어디일까?** — 70초, 1080×1920, 30fps, 무음. 최빈값·중앙값·평균을 대칭 분포에서 소개하고, 먼 값과 비대칭 분포로 세 중심의 차이를 보여줍니다. 같은 평균에도 퍼짐이 다를 수 있다는 질문으로 마칩니다.
- 실제 파일: [장면](episodes/dist02_where_is_center/scene.py) · [대본](episodes/dist02_where_is_center/narration.md) · [제작 기준](episodes/dist02_where_is_center/brief.md) · [자막](episodes/dist02_where_is_center/captions.srt) · [TTS](episodes/dist02_where_is_center/tts_script.txt)
- 미리보기: `python scripts/render.py dist02 --preview` → `exports/dist02_preview.mp4`
- 최종본: `python scripts/render.py dist02` → `exports/dist02.mp4`
- 분포의 수학 03 **분산은 무엇을 측정하는가?** — 49초, 1080×1920, 30fps, 무음. 평균이 같은 두 분포의 거리 차이에서 시작해 편차의 상쇄, 제곱, 확률가중 평균으로 분산을 설명합니다. 같은 평균과 분산에도 다른 모양이 가능하다는 질문으로 마칩니다.
- 실제 파일: [장면](episodes/dist03_what_is_variance/scene.py) · [대본](episodes/dist03_what_is_variance/narration.md) · [제작 기준](episodes/dist03_what_is_variance/brief.md) · [자막](episodes/dist03_what_is_variance/captions.srt) · [TTS](episodes/dist03_what_is_variance/tts_script.txt)
- 미리보기: `python scripts/render.py dist03 --preview` → `exports/dist03_preview.mp4`
- 최종본: `python scripts/render.py dist03` → `exports/dist03.mp4`
- 분포의 수학 04 **같은 평균과 분산이면 같은 분포일까?** — 43초, 1080×1920, 30fps, 무음. 단봉형과 양봉형 이산 분포가 모두 `μ=0`, `σ²=1`인 예시로 두 숫자가 분포를 압축한 요약일 뿐임을 보여주고, 두 변수 데이터로 다음 질문을 엽니다.
- 실제 파일: [장면](episodes/dist04_same_mean_variance/scene.py) · [대본](episodes/dist04_same_mean_variance/narration.md) · [제작 기준](episodes/dist04_same_mean_variance/brief.md) · [자막](episodes/dist04_same_mean_variance/captions.srt) · [TTS](episodes/dist04_same_mean_variance/tts_script.txt)
- 미리보기: `python scripts/render.py dist04 --preview` → `exports/dist04_preview.mp4`
- 최종본: `python scripts/render.py dist04` → `exports/dist04.mp4`
- 분포의 수학 05 **두 변수를 동시에 보면 무엇이 달라질까?** — 46초 목표, 1080×1920, 30fps, 무음. 키·몸무게 관측값을 평면의 점으로 놓고, 개별 분포가 똑같아도 짝짓기에 따라 점구름의 방향이 달라짐을 보여줍니다. 공분산 질문으로 마칩니다.
- 실제 파일: [장면](episodes/dist05_two_variables/scene.py) · [대본](episodes/dist05_two_variables/narration.md) · [제작 기준](episodes/dist05_two_variables/brief.md) · [자막](episodes/dist05_two_variables/captions.srt) · [TTS](episodes/dist05_two_variables/tts_script.txt)
- 미리보기: `python scripts/render.py dist05 --preview` → `exports/dist05_preview.mp4`
- 최종본: `python scripts/render.py dist05` → `exports/dist05.mp4`
- 분포의 수학 06 **두 값이 같이 움직인다는 것은 무슨 뜻일까?** — 49초 목표, 1080×1920, 30fps, 무음. 두 평균에서의 편차 부호를 곱해 공분산의 양수·음수·0을 설명하고, 같은 길쭉한 점구름을 회전해 공분산과 기울기의 관계를 묻습니다.
- 실제 파일: [장면](episodes/dist06_covariance/scene.py) · [대본](episodes/dist06_covariance/narration.md) · [제작 기준](episodes/dist06_covariance/brief.md) · [자막](episodes/dist06_covariance/captions.srt) · [TTS](episodes/dist06_covariance/tts_script.txt)
- 미리보기: `python scripts/render.py dist06 --preview` → `exports/dist06_preview.mp4`
- 최종본: `python scripts/render.py dist06` → `exports/dist06.mp4`
- 분포의 수학 07 **공분산이 바뀌면 왜 분포가 기울어질까?** — 49초 목표, 1080×1920, 30fps, 무음. 두 변수의 분산을 각각 1로 고정하고 공분산만 바꾸며 점구름의 대각선 방향을 보여준 뒤 공분산 행렬로 묶습니다.
- 실제 파일: [장면](episodes/dist07_covariance_direction/scene.py) · [대본](episodes/dist07_covariance_direction/narration.md) · [제작 기준](episodes/dist07_covariance_direction/brief.md) · [자막](episodes/dist07_covariance_direction/captions.srt) · [TTS](episodes/dist07_covariance_direction/tts_script.txt)
- 미리보기: `python scripts/render.py dist07 --preview` → `exports/dist07_preview.mp4`
- 최종본: `python scripts/render.py dist07` → `exports/dist07.mp4`
- 분포의 수학 08 **행렬 안에서 분포의 방향을 찾을 수 있을까?** — 실제 TTS 길이에 맞춘 42초, 1080×1920, 30fps, 무음. 단위방향으로 점구름을 투영해 분산의 최대점을 찾은 뒤, 그 방향을 공분산 행렬의 최대 고유값에 대응하는 고유벡터로 연결합니다.
- 실제 파일: [장면](episodes/dist08_eigen_directions/scene.py) · [대본](episodes/dist08_eigen_directions/narration.md) · [제작 기준](episodes/dist08_eigen_directions/brief.md) · [자막](episodes/dist08_eigen_directions/captions.srt) · [TTS](episodes/dist08_eigen_directions/tts_script.txt)
- 미리보기: `python scripts/render.py dist08 --preview` → `exports/dist08_preview.mp4`
- 최종본: `python scripts/render.py dist08` → `exports/dist08.mp4`
- 분포의 수학 09 **왜 퍼짐은 행렬이 되고, PCA로 이어질까?** — 50초 목표, 1080×1920, 30fps, 무음. 1차원 분산에서 방향별 퍼짐, 공분산 행렬, 고유방향, 좌표축 재선택과 PCA를 연결하는 2부 결론편입니다.
- 실제 파일: [장면](episodes/dist09_pca_finale/scene.py) · [대본](episodes/dist09_pca_finale/narration.md) · [제작 기준](episodes/dist09_pca_finale/brief.md) · [자막](episodes/dist09_pca_finale/captions.srt) · [TTS](episodes/dist09_pca_finale/tts_script.txt)
- 미리보기: `python scripts/render.py dist09 --preview` → `exports/dist09_preview.mp4`
- 최종본: `python scripts/render.py dist09` → `exports/dist09.mp4`
- 분포의 수학 10 **거리의 단위는 분포가 결정할 수 있다 | Mahalanobis Distance** — 50초 목표, 1080×1920, 30fps, 무음. 같은 직선거리의 A·B를 분포와 함께 보여주고, 방향마다 다른 눈금으로 재면 원형 등거리선이 타원형이 되는 장면에서 마할라노비스 거리를 소개합니다.
- 실제 파일: [장면](episodes/dist10_mahalanobis_distance/scene.py) · [대본](episodes/dist10_mahalanobis_distance/narration.md) · [제작 기준](episodes/dist10_mahalanobis_distance/brief.md) · [자막](episodes/dist10_mahalanobis_distance/captions.srt) · [TTS](episodes/dist10_mahalanobis_distance/tts_script.txt)
- 미리보기: `python scripts/render.py dist10 --preview` → `exports/dist10_preview.mp4`
- 최종본: `python scripts/render.py dist10` → `exports/dist10.mp4`
- 분포의 수학 11 **Gaussian의 타원은 어디서 오는가?** — 50초 목표, 1080×1920, 30fps, 무음. 마할라노비스 등거리선과 Gaussian 등밀도선이 같은 타원인 이유를 거리 제곱과 지수 감쇠로 설명하고 Whitening 질문으로 연결합니다.
- 실제 파일: [장면](episodes/dist11_gaussian_ellipse/scene.py) · [대본](episodes/dist11_gaussian_ellipse/narration.md) · [제작 기준](episodes/dist11_gaussian_ellipse/brief.md) · [자막](episodes/dist11_gaussian_ellipse/captions.srt) · [TTS](episodes/dist11_gaussian_ellipse/tts_script.txt)
- 미리보기: `python scripts/render.py dist11 --preview` → `exports/dist11_preview.mp4`
- 최종본: `python scripts/render.py dist11` → `exports/dist11.mp4`
- 분포의 수학 12 **모든 Gaussian은 하나의 원에서 만들 수 있을까?** — 50초 목표, 1080×1920, 30fps, 무음. 표준 원형 Gaussian을 늘리고 회전하고 옮겨 `X=AZ+μ`, `AAᵀ=Σ`로 원하는 Gaussian을 생성합니다. 역방향 Whitening을 짧게 회수하고 더 복잡한 분포 생성의 질문으로 마칩니다.
- 실제 파일: [장면](episodes/dist12_gaussian_generation/scene.py) · [대본](episodes/dist12_gaussian_generation/narration.md) · [제작 기준](episodes/dist12_gaussian_generation/brief.md) · [자막](episodes/dist12_gaussian_generation/captions.srt) · [TTS](episodes/dist12_gaussian_generation/tts_script.txt)
- 미리보기: `python scripts/render.py dist12 --preview` → `exports/dist12_preview.mp4`
- 최종본: `python scripts/render.py dist12` → `exports/dist12.mp4`

- 분포의 수학 13, 4부 **하나의 분포를 넘어**: **하나의 Gaussian으로 부족하다면? | Gaussian Mixture Model** — 실제 TTS 41초에 맞춘 영상 43초, 1080×1920, 30fps, 무음. 두 군집 사이의 빈 공간을 단일 Gaussian이 채우는 문제에서 시작해 가중합으로 복잡한 분포를 만들고, 한 점의 성분 소속 확률을 다음 질문으로 남깁니다.
- 실제 파일: [장면](episodes/dist13_gaussian_mixture/scene.py) · [대본](episodes/dist13_gaussian_mixture/narration.md) · [제작 기준](episodes/dist13_gaussian_mixture/brief.md) · [자막](episodes/dist13_gaussian_mixture/captions.srt) · [TTS](episodes/dist13_gaussian_mixture/tts_script.txt)
- 미리보기: `python scripts/render.py dist13 --preview` → `exports/dist13_preview.mp4`
- 최종본: `python scripts/render.py dist13` → `exports/dist13.mp4`

- 분포의 수학 14, 4부 **하나의 분포를 넘어**: **한 점은 반드시 하나의 집단에만 속해야 할까? | Responsibility** — 45초 목표, 1080×1920, 30fps, 무음. 경계 근처의 작은 이동이 하드 배정을 뒤집는 장면에서 시작해 두 성분의 가중 밀도를 `30%/70%` 소속 확률로 정규화하고 잠재 출처의 질문을 남깁니다.
- 실제 파일: [장면](episodes/dist14_responsibility/scene.py) · [대본](episodes/dist14_responsibility/narration.md) · [제작 기준](episodes/dist14_responsibility/brief.md) · [자막](episodes/dist14_responsibility/captions.srt) · [TTS](episodes/dist14_responsibility/tts_script.txt)
- 미리보기: `python scripts/render.py dist14 --preview` → `exports/dist14_preview.mp4`
- 최종본: `python scripts/render.py dist14` → `exports/dist14.mp4`

- 분포의 수학 15, 4부 **하나의 분포를 넘어**: **관측된 데이터 뒤에는 무엇이 숨어 있을까? | Latent Variable** — 실제 TTS 95초에 맞춘 100초 영상, 1080×1920, 30fps, 무음. 14화의 `30%/70%` 관측점에서 시간을 되감아 `z` 선택과 `x` 생성을 보여준 뒤, 관측값에서 숨은 선택을 거꾸로 추론하는 Responsibility와 잠재변수의 의미를 연결합니다. 연속 잠재 요인으로 확장하고 EM의 순환 문제를 남깁니다.
- 실제 파일: [장면](episodes/dist15_latent_variable/scene.py) · [대본](episodes/dist15_latent_variable/narration.md) · [제작 기준](episodes/dist15_latent_variable/brief.md) · [자막](episodes/dist15_latent_variable/captions.srt) · [TTS](episodes/dist15_latent_variable/tts_script.txt)
- 미리보기: `python scripts/render.py dist15 --preview` → `exports/dist15_preview.mp4`
- 최종본: `python scripts/render.py dist15` → `exports/dist15.mp4`

- 분포의 수학 16, 4부 **하나의 분포를 넘어**: **닭이 먼저냐 달걀이 먼저냐를 수학은 어떻게 풀까? | Expectation-Maximization** — 110초 목표, 1080×1920, 30fps, 무음. 불완전한 초기 GMM에서 부드러운 소속을 추정하고 그 소속으로 분포를 다시 맞추는 반복을 실제 계산으로 보여줍니다. 초기값에 따라 다른 해에 도달할 수 있음을 보여준 뒤, 로그 가능도가 왜 내려가지 않는지 다음 편의 질문으로 남깁니다.
- 실제 파일: [장면](episodes/dist16_expectation_maximization/scene.py) · [대본](episodes/dist16_expectation_maximization/narration.md) · [제작 기준](episodes/dist16_expectation_maximization/brief.md) · [자막](episodes/dist16_expectation_maximization/captions.srt) · [TTS](episodes/dist16_expectation_maximization/tts_script.txt)
- 미리보기: `python scripts/render.py dist16 --preview` → `exports/dist16_preview.mp4`
- 최종본: `python scripts/render.py dist16` → `exports/dist16.mp4`

- 분포의 수학 17, 4부 **하나의 분포를 넘어**: **직접 오르기 어렵다면 발판을 만들면 된다 | ELBO** — 122초 목표, 1080×1920, 30fps, 무음. 실제 잠재 Gaussian 모형의 likelihood와 ELBO를 사용해 E-step의 접점, M-step의 상승, likelihood 비감소의 이유를 보여줍니다. 다음 질문은 KL Divergence의 방향입니다.
- 실제 파일: [장면](episodes/dist17_elbo/scene.py) · [대본](episodes/dist17_elbo/narration.md) · [제작 기준](episodes/dist17_elbo/brief.md) · [자막](episodes/dist17_elbo/captions.srt) · [TTS](episodes/dist17_elbo/tts_script.txt)
- 미리보기: `python scripts/render.py dist17 --preview` → `exports/dist17_preview.mp4`
- 최종본: `python scripts/render.py dist17` → `exports/dist17.mp4`

- 분포의 수학 17 **대안편**: **점점 좋아지는데 왜 정답은 아닐 수 있을까? | Local Optimum** — 114초 목표, 1080×1920, 30fps, 무음. 같은 세 덩어리의 데이터에 Gaussian 두 개를 서로 다른 초기값에서 맞춰 서로 다른 수렴 결과를 보여줍니다. Local Optimum과 여러 초기값의 의미를 설명하고 다음은 Maximum Likelihood Estimation으로 연결합니다. 기존 ELBO 편은 보존합니다.
- 실제 파일: [장면](episodes/dist17_local_optimum/scene.py) · [대본](episodes/dist17_local_optimum/narration.md) · [제작 기준](episodes/dist17_local_optimum/brief.md) · [자막](episodes/dist17_local_optimum/captions.srt) · [TTS](episodes/dist17_local_optimum/tts_script.txt)
- 미리보기: `python scripts/render.py dist17_local --preview` → `exports/dist17_local_preview.mp4`
- 최종본: `python scripts/render.py dist17_local` → `exports/dist17_local.mp4`

- 분포의 수학 17 **GMM Singularity 버전**: **학습 점수를 무한히 올릴 수 있다면 좋은 모델일까? | GMM Singularity** — 대본 길이에 비례한 59.2초 추정, 1080×1920, 30fps, 무음. 한 성분의 분산 붕괴가 전체 학습 로그 가능도를 무한히 높일 수 있음을 실제 혼합밀도 계산으로 보여줍니다. 기존 두 17화는 보존합니다.
- 실제 파일: [장면](episodes/dist17_gmm_singularity/scene.py) · [타이밍 기준](episodes/dist17_gmm_singularity/content.py) · [대본](episodes/dist17_gmm_singularity/narration.md) · [제작 기준](episodes/dist17_gmm_singularity/brief.md) · [자막](episodes/dist17_gmm_singularity/captions.srt) · [TTS](episodes/dist17_gmm_singularity/tts_script.txt)
- 미리보기: `python scripts/render.py dist17_singularity --preview` → `exports/dist17_singularity_preview.mp4`
- 최종본: `python scripts/render.py dist17_singularity` → `exports/dist17_singularity.mp4`

- 분포의 수학 **17-2 보충 해설**: **왜 한 점이 전체 학습 점수를 무한히 올릴까? | GMM Singularity** — 174.2초 추정, 1080×1920, 30fps, 무음. 밀도와 면적, 단일 Gaussian의 손실, 고정 배경 성분이 남긴 양의 밀도를 거쳐 전체 로그 가능도가 발산하는 과정을 설명합니다. 기존 17화들은 보존합니다.
- 실제 파일: [장면](episodes/dist17_2_singularity_explained/scene.py) · [타이밍](episodes/dist17_2_singularity_explained/content.py) · [대본](episodes/dist17_2_singularity_explained/narration.md) · [제작 기준](episodes/dist17_2_singularity_explained/brief.md) · [자막](episodes/dist17_2_singularity_explained/captions.srt) · [TTS](episodes/dist17_2_singularity_explained/tts_script.txt)
- 미리보기: `python scripts/render.py dist17_2 --preview` → `exports/dist17_2_preview.mp4`
- 최종본: `python scripts/render.py dist17_2` → `exports/dist17_2.mp4`

## 활성화 함수의 기하학

- 활성화 함수의 기하학 01 **ReLU는 좌표를 어떻게 압축할까?** — 94초, 1080×1920, 30fps, 무음. 고정된 `x₁,x₂` 좌표계 위에서 `w` 방향의 새 좌표 `u=wᵀx+b`를 만들고, `(u,v)→(max(0,u),v)`가 음수 쪽 격자를 `u=0` 경계로 붕괴시키는 과정을 보여줍니다. 여러 `uᵢ`의 부호 패턴과 piecewise affine 규칙으로 확장합니다.
- 실제 파일: [장면](episodes/act01_relu_geometry/scene.py) · [대본](episodes/act01_relu_geometry/narration.md) · [제작 기준](episodes/act01_relu_geometry/brief.md) · [자막](episodes/act01_relu_geometry/captions.srt) · [TTS](episodes/act01_relu_geometry/tts_script.txt)
- 미리보기: `python scripts/render.py act01 --preview` → `exports/act01_preview.mp4`
- 최종본: `python scripts/render.py act01` → `exports/act01.mp4`

## 신경망의 수학

- 신경망의 수학 01 **왜 모델은 필요 이상으로 큰 학습 공간에서 움직일까?** — 112초, 1080×1920, 30fps, 무음. 무작위 부분공간에서 `θ = θ₀ + Pφ`로 학습 가능한 자유도만 제한하는 실험을 통해 parameter count와 intrinsic dimension의 차이를 보여주고, 좋은 해의 기하학과 overparameterization에 대한 질문을 엽니다.
- 실제 파일: [장면](episodes/nnmath01_intrinsic_dimension/scene.py) · [대본](episodes/nnmath01_intrinsic_dimension/narration.md) · [제작 기준](episodes/nnmath01_intrinsic_dimension/brief.md) · [자막](episodes/nnmath01_intrinsic_dimension/captions.srt) · [TTS](episodes/nnmath01_intrinsic_dimension/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath01 --preview` → `exports/nnmath01_preview.mp4`
- 최종본: `python scripts/render.py nnmath01` → `exports/nnmath01.mp4`
- 신경망의 수학 02 **왜 더 큰 공간에서 답을 찾는 것이 쉬울까?** — 116초, 1080×1920, 30fps, 무음. 고립된 점과 연속적인 해 집합을 대비하고, 독립 제약 수가 유지될 때 여분의 파라미터가 해 집합의 자유도를 늘릴 수 있다는 overparameterization의 기하학적 직관을 설명합니다.
- 실제 파일: [장면](episodes/nnmath02_overparameterization_geometry/scene.py) · [대본](episodes/nnmath02_overparameterization_geometry/narration.md) · [제작 기준](episodes/nnmath02_overparameterization_geometry/brief.md) · [자막](episodes/nnmath02_overparameterization_geometry/captions.srt) · [TTS](episodes/nnmath02_overparameterization_geometry/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath02 --preview` → `exports/nnmath02_preview.mp4`
- 최종본: `python scripts/render.py nnmath02` → `exports/nnmath02.mp4`
- 신경망의 수학 03 **백만 개의 파라미터가 정말 백만 개의 역할을 할까? — Parameter Symmetry** — 132초, 1080×1920, 30fps, 무음. 두 단계 곱셈 모델의 `w₁w₂=6` 곡선으로 서로 다른 파라미터가 같은 함수를 만들 수 있음을 보여줍니다. 구간 길이는 1분 58초 TTS의 대본 분량에 비례해 조정했습니다.
- 실제 파일: [장면](episodes/nnmath03_parameter_symmetry/scene.py) · [대본](episodes/nnmath03_parameter_symmetry/narration.md) · [제작 기준](episodes/nnmath03_parameter_symmetry/brief.md) · [자막](episodes/nnmath03_parameter_symmetry/captions.srt) · [TTS](episodes/nnmath03_parameter_symmetry/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath03 --preview` → `exports/nnmath03_preview.mp4`
- 최종본: `python scripts/render.py nnmath03` → `exports/nnmath03.mp4`
- 신경망의 수학 04 **서로 다른 두 신경망 사이에도 정답이 있을까? — Mode Connectivity** — 114초, 1080×1920, 30fps, 무음. 두 좋은 해를 직선으로 섞어 Loss 장벽을 확인한 뒤, 우회하는 저손실 경로를 찾는 실험을 보여줍니다. 1분 51초 TTS 길이에 맞춰 구간별 대본 분량으로 전환 시간을 조정했습니다.
- 실제 파일: [장면](episodes/nnmath04_mode_connectivity/scene.py) · [대본](episodes/nnmath04_mode_connectivity/narration.md) · [제작 기준](episodes/nnmath04_mode_connectivity/brief.md) · [자막](episodes/nnmath04_mode_connectivity/captions.srt) · [TTS](episodes/nnmath04_mode_connectivity/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath04 --preview` → `exports/nnmath04_preview.mp4`
- 최종본: `python scripts/render.py nnmath04` → `exports/nnmath04.mp4`
- 신경망의 수학 05 **좋은 해의 주변은 어떤 모양일까? — Hessian Spectrum** — 84초, 1080×1920, 30fps, 무음. 저손실 경로 위 한 해의 방향별 곡률을 비교하고 Hessian 고유값 분포로 읽습니다.
- 실제 파일: [장면](episodes/nnmath05_hessian_spectrum/scene.py) · [대본](episodes/nnmath05_hessian_spectrum/narration.md) · [제작 기준](episodes/nnmath05_hessian_spectrum/brief.md) · [자막](episodes/nnmath05_hessian_spectrum/captions.srt) · [TTS](episodes/nnmath05_hessian_spectrum/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath05 --preview` → `exports/nnmath05_preview.mp4`
- 최종본: `python scripts/render.py nnmath05` → `exports/nnmath05.mp4`
- 신경망의 수학 06 **평평한 해가 정말 더 좋은 모델일까? — Flatness vs Generalization** — 97초, 1080×1920, 30fps, 무음. Flatness의 국소 안정성과 좌표 의존성이 충돌하는 실험을 통해 측정 기준의 선택을 묻습니다. 1분 33초 TTS 길이에 맞춰 장면별 대본 분량으로 전환 시간을 조정했습니다.
- 실제 파일: [장면](episodes/nnmath06_flatness_generalization/scene.py) · [대본](episodes/nnmath06_flatness_generalization/narration.md) · [제작 기준](episodes/nnmath06_flatness_generalization/brief.md) · [자막](episodes/nnmath06_flatness_generalization/captions.srt) · [TTS](episodes/nnmath06_flatness_generalization/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath06 --preview` → `exports/nnmath06_preview.mp4`
- 최종본: `python scripts/render.py nnmath06` → `exports/nnmath06.mp4`
- 신경망의 수학 07 **모델은 클수록 과적합된다? 실제로는 다시 좋아질 수 있습니다 — Double Descent** — 106초, 1080×1920, 30fps, 무음. U자형 과적합 직관을 더 큰 모델 범위로 확장했을 때 나타날 수 있는 두 번째 Test Error 하강을 보여줍니다.
- 실제 파일: [장면](episodes/nnmath07_double_descent/scene.py) · [대본](episodes/nnmath07_double_descent/narration.md) · [제작 기준](episodes/nnmath07_double_descent/brief.md) · [자막](episodes/nnmath07_double_descent/captions.srt) · [TTS](episodes/nnmath07_double_descent/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath07 --preview` → `exports/nnmath07_preview.mp4`
- 최종본: `python scripts/render.py nnmath07` → `exports/nnmath07.mp4`
- 신경망의 수학 08 **좋은 답이 존재해도 학습하지 못할 수 있을까? — Optimization & Implicit Bias** — 96초, 1080×1920, 30fps, 무음. 표현 가능·도달 가능·실제로 선택됨을 구별하고 optimizer의 암묵적 편향을 소개합니다. 1분 34초 TTS 길이에 맞춰 구간별 대본 분량으로 전환 시간을 조정했습니다.
- 실제 파일: [장면](episodes/nnmath08_optimization_implicit_bias/scene.py) · [대본](episodes/nnmath08_optimization_implicit_bias/narration.md) · [제작 기준](episodes/nnmath08_optimization_implicit_bias/brief.md) · [자막](episodes/nnmath08_optimization_implicit_bias/captions.srt) · [TTS](episodes/nnmath08_optimization_implicit_bias/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath08 --preview` → `exports/nnmath08_preview.mp4`
- 최종본: `python scripts/render.py nnmath08` → `exports/nnmath08.mp4`
- 신경망의 수학 09 **Loss가 같다면 어떤 해가 더 좋을까? — Beyond the Loss Value** — 93초, 1080×1920, 30fps, 무음. 동률인 Training Loss에서 주변 안정성을 시험하고 좌표 의존성을 확인한 뒤 실제 함수 변화로 평가 관점을 넓힙니다.
- 실제 파일: [장면](episodes/nnmath09_beyond_loss_value/scene.py) · [대본](episodes/nnmath09_beyond_loss_value/narration.md) · [제작 기준](episodes/nnmath09_beyond_loss_value/brief.md) · [자막](episodes/nnmath09_beyond_loss_value/captions.srt) · [TTS](episodes/nnmath09_beyond_loss_value/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath09 --preview` → `exports/nnmath09_preview.mp4`
- 최종본: `python scripts/render.py nnmath09` → `exports/nnmath09.mp4`
- 신경망의 수학 10 **작게 만들 수 있는데 왜 처음부터 크게 학습할까? — Overparameterization & Compressibility** — 87초, 1080×1920, 30fps, 무음. 큰 모델에서 답을 찾는 과정과 찾은 답을 작게 표현하는 과정을 구별하고, 압축에는 보존할 동작의 선택이 중요함을 보여줍니다.
- 실제 파일: [장면](episodes/nnmath10_overparameterization_compressibility/scene.py) · [대본](episodes/nnmath10_overparameterization_compressibility/narration.md) · [제작 기준](episodes/nnmath10_overparameterization_compressibility/brief.md) · [자막](episodes/nnmath10_overparameterization_compressibility/captions.srt) · [TTS](episodes/nnmath10_overparameterization_compressibility/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath10 --preview` → `exports/nnmath10_preview.mp4`
- 최종본: `python scripts/render.py nnmath10` → `exports/nnmath10.mp4`
- 신경망의 수학 11 **왜 신경망은 문제보다 훨씬 클까? — From Parameter Space to Learned Solution** — 86초, 1080×1920, 30fps, 무음. 앞선 10편의 해의 구조·대칭·학습 경로·압축 가능성을 처음 질문으로 모아 시리즈를 마무리합니다.
- 실제 파일: [장면](episodes/nnmath11_series_finale/scene.py) · [대본](episodes/nnmath11_series_finale/narration.md) · [제작 기준](episodes/nnmath11_series_finale/brief.md) · [자막](episodes/nnmath11_series_finale/captions.srt) · [TTS](episodes/nnmath11_series_finale/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath11 --preview` → `exports/nnmath11_preview.mp4`
- 최종본: `python scripts/render.py nnmath11` → `exports/nnmath11.mp4`
- 신경망의 수학 12 **서로 다른 파라미터가 어떻게 같은 신경망이 될까? — Permutation Symmetry & Quotient Space** — 122초, 1080×1920, 30fps, 무음. 은닉 뉴런의 전체 연결을 함께 순열해 함수가 보존되는 모습을 출발점으로, 동일 함수·동일 출력·동일 loss·대칭 minimum을 연결하고, permutation equivalence class를 한 점으로 보는 quotient space를 도출합니다.
- 실제 파일: [장면](episodes/nnmath12_parameter_symmetry_quotient/scene.py) · [대본](episodes/nnmath12_parameter_symmetry_quotient/narration.md) · [제작 기준](episodes/nnmath12_parameter_symmetry_quotient/brief.md) · [자막](episodes/nnmath12_parameter_symmetry_quotient/captions.srt) · [TTS](episodes/nnmath12_parameter_symmetry_quotient/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath12 --preview` → `exports/nnmath12_preview.mp4`
- 최종본: `python scripts/render.py nnmath12` → `exports/nnmath12.mp4`

## 신경망의 수학 2부 — 학습된 내부 구조

- 신경망의 수학 2부 01 **분류만 하면 되는데 왜 클래스는 정삼각형을 만들까? — Neural Collapse** — 110초, 1080×1920, 30fps, 무음. 이미 완벽히 분류 가능한 representation이 학습 후반에 클래스 내부 붕괴, simplex ETF 형태의 대칭적 평균, classifier 정렬, nearest-class-center 결정으로 향할 수 있다는 현상을 보여줍니다.
- 실제 파일: [장면](episodes/nnmath2p01_neural_collapse/scene.py) · [대본](episodes/nnmath2p01_neural_collapse/narration.md) · [제작 기준](episodes/nnmath2p01_neural_collapse/brief.md) · [자막](episodes/nnmath2p01_neural_collapse/captions.srt) · [TTS](episodes/nnmath2p01_neural_collapse/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p01 --preview` → `exports/nnmath2p01_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p01` → `exports/nnmath2p01.mp4`
- 신경망의 수학 2부 02 **2차원 공간에 5개의 특징을 저장할 수 있을까? — Superposition** — 102초, 1080×1920, 30fps, 무음. 두 좌표축에 다섯 개의 비직교 feature direction을 배치하면 capacity를 늘리는 대신 interference가 생기며, sparse activation이 그 기대 비용을 낮출 수 있다는 표현 기하학을 보여줍니다.
- 실제 파일: [장면](episodes/nnmath2p02_superposition/scene.py) · [대본](episodes/nnmath2p02_superposition/narration.md) · [제작 기준](episodes/nnmath2p02_superposition/brief.md) · [자막](episodes/nnmath2p02_superposition/captions.srt) · [TTS](episodes/nnmath2p02_superposition/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p02 --preview` → `exports/nnmath2p02_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p02` → `exports/nnmath2p02.mp4`
- 신경망의 수학 2부 03 **뉴런 하나는 하나의 의미를 담당할까? — Polysemanticity** — 108초, 1080×1920, 30fps, 무음. 한 뉴런의 여러 반응을 출발점으로 뉴런을 의미의 상자가 아닌 representation 공간의 좌표축으로, feature를 여러 뉴런에 걸친 방향으로 다시 해석하고 Sparse Autoencoder의 분해 문제로 연결합니다.
- 실제 파일: [장면](episodes/nnmath2p03_polysemanticity/scene.py) · [대본](episodes/nnmath2p03_polysemanticity/narration.md) · [제작 기준](episodes/nnmath2p03_polysemanticity/brief.md) · [자막](episodes/nnmath2p03_polysemanticity/captions.srt) · [TTS](episodes/nnmath2p03_polysemanticity/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p03 --preview` → `exports/nnmath2p03_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p03` → `exports/nnmath2p03.mp4`
- 신경망의 수학 2부 04 **모델의 진짜 Feature를 찾았다는 걸 어떻게 알까? — Identifiability** — 112초, 1080×1920, 30fps, 무음. 서로 다른 feature decomposition이 같은 activation을 복원할 수 있다는 문제에서 출발해 좋은 설명, 유일한 설명, 실제 메커니즘을 구분하고 sparsity와 intervention이 어떤 추가 증거를 제공하는지 보여줍니다.
- 실제 파일: [장면](episodes/nnmath2p04_identifiability/scene.py) · [대본](episodes/nnmath2p04_identifiability/narration.md) · [제작 기준](episodes/nnmath2p04_identifiability/brief.md) · [자막](episodes/nnmath2p04_identifiability/captions.srt) · [TTS](episodes/nnmath2p04_identifiability/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p04 --preview` → `exports/nnmath2p04_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p04` → `exports/nnmath2p04.mp4`
- 썸네일: `exports/nnmath2p04_thumbnail.png`

- 신경망의 수학 2부 05 **Feature가 진짜인지 직접 지워보면 알 수 있을까? — Causal Intervention** — 112초, 1080×1920, 30fps, 무음. 관찰적 상관관계를 넘어 feature 방향을 제거·추가하는 개입을 필요성과 충분성의 관점에서 비교하고, redundancy, off-distribution intervention, superposition이 인과적 결론을 어떻게 어렵게 만드는지 보여준 뒤 circuits로 연결합니다.
- 실제 파일: [장면](episodes/nnmath2p05_causal_intervention/scene.py) · [대본](episodes/nnmath2p05_causal_intervention/narration.md) · [제작 기준](episodes/nnmath2p05_causal_intervention/brief.md) · [자막](episodes/nnmath2p05_causal_intervention/captions.srt) · [TTS](episodes/nnmath2p05_causal_intervention/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p05 --preview` → `exports/nnmath2p05_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p05` → `exports/nnmath2p05.mp4`
- 썸네일: `exports/nnmath2p05_thumbnail.png`

- 신경망의 수학 2부 06 **훈련 정확도 100% 이후에도 모델은 무엇을 배울까? — Grokking** — 126초, 1080×1920, 30fps, 무음. Train Accuracy가 일찍 100%에 도달한 뒤 Test Accuracy가 오래 정체되다가 뒤늦게 상승하는 delayed generalization을 출발점으로, 정확도 포화와 optimization 종료를 구분하고 memorizing solution과 generalizing solution 사이의 장기 dynamics를 설명합니다.
- 실제 파일: [장면](episodes/nnmath2p06_grokking/scene.py) · [대본](episodes/nnmath2p06_grokking/narration.md) · [제작 기준](episodes/nnmath2p06_grokking/brief.md) · [자막](episodes/nnmath2p06_grokking/captions.srt) · [TTS](episodes/nnmath2p06_grokking/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p06 --preview` → `exports/nnmath2p06_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p06` → `exports/nnmath2p06.mp4`
- 썸네일: `exports/nnmath2p06_thumbnail.png`

- 신경망의 수학 2부 07 **신경망은 학습하며 정말 새로운 Feature를 만들까? — Feature Learning vs Lazy Learning** — 139초, 1080×1920, 30fps, 무음. 같은 초기 point cloud에서 출발해 Feature 축 자체가 바꾰는 학습과 초기 tangent feature를 거의 고정한 채 조합 계수를 바꾰는 학습을 좌우로 비교합니다.
- 실제 파일: [장면](episodes/nnmath2p07_feature_vs_lazy/scene.py) · [대본](episodes/nnmath2p07_feature_vs_lazy/narration.md) · [제작 기준](episodes/nnmath2p07_feature_vs_lazy/brief.md) · [자막](episodes/nnmath2p07_feature_vs_lazy/captions.srt) · [TTS](episodes/nnmath2p07_feature_vs_lazy/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p07 --preview` → `exports/nnmath2p07_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p07` → `exports/nnmath2p07.mp4`
- 썸네일: `exports/nnmath2p07_thumbnail.png`

- 신경망의 수학 2부 08 **Spectral Bias — 신경망은 왜 낮은 주파수부터 학습할까?** — 143초, 1080×1920, 30fps, 무음. `sin x + 0.3 sin(10x)` target의 성분별 학습 속도를 비교하고, kernel learning dynamics의 고유방향과 고유값이 mode별 error decay를 다르게 만들 수 있음으로 연결해 `Representable ≠ Equally Learnable`로 결론짓습니다.
- 실제 파일: [장면](episodes/nnmath2p08_spectral_bias/scene.py) · [대본](episodes/nnmath2p08_spectral_bias/narration.md) · [제작 기준](episodes/nnmath2p08_spectral_bias/brief.md) · [자막](episodes/nnmath2p08_spectral_bias/captions.srt) · [TTS](episodes/nnmath2p08_spectral_bias/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p08 --preview` → `exports/nnmath2p08_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p08` → `exports/nnmath2p08.mp4`
- 썸네일: `exports/nnmath2p08_thumbnail.png`

- 신경망의 수학 2부 09 **Edge of Stability — 신경망은 왜 불안정해지기 직전까지 학습할까?** — 256초, 1080×1920, 30fps, 무음. 넓은/좁은 골짜기로 curvature를 설명하고, quadratic update에서 `ηλ=2` 경계를 직접 유도한 뒤 `η=0.01` 고정 숫자 예시로 local curvature 변화와 Edge of Stability를 연결합니다.
- 실제 파일: [장면](episodes/nnmath2p09_edge_of_stability/scene.py) · [대본](episodes/nnmath2p09_edge_of_stability/narration.md) · [제작 기준](episodes/nnmath2p09_edge_of_stability/brief.md) · [자막](episodes/nnmath2p09_edge_of_stability/captions.srt) · [TTS](episodes/nnmath2p09_edge_of_stability/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p09 --preview` → `exports/nnmath2p09_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p09` → `exports/nnmath2p09.mp4`
- 썸네일: `exports/nnmath2p09_thumbnail.png`

- 신경망의 수학 2부 09A **왜 ηλ=2가 안정성의 경계일까?** — 104초, 1080×1920, 30fps, 무음. 넓은/좁은 골짜기로 curvature를 소개하고 quadratic update를 직접 정리해 `ηλ=0.5`, `1.5`, `2`의 궤적을 비교합니다.
- 실제 파일: [장면](episodes/nnmath2p09a_stability_boundary/scene.py) · [대본](episodes/nnmath2p09a_stability_boundary/narration.md) · [제작 기준](episodes/nnmath2p09a_stability_boundary/brief.md) · [자막](episodes/nnmath2p09a_stability_boundary/captions.srt) · [TTS](episodes/nnmath2p09a_stability_boundary/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p09a --preview` → `exports/nnmath2p09a_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p09a` → `exports/nnmath2p09a.mp4`

- 신경망의 수학 2부 09B **Edge of Stability — 고정된 Learning Rate, 발산해야 할 것 같은데 왜 학습은 계속될까?** — 122초, 1080×1920, 30fps, 무음. `η=0.01`을 고정한 숫자 예시에서 `λ_max` 증가가 `ηλ_max`를 경계 2로 이동시키는 과정을 보여주고 Edge of Stability로 연결합니다.
- 실제 파일: [장면](episodes/nnmath2p09b_edge_dynamics/scene.py) · [대본](episodes/nnmath2p09b_edge_dynamics/narration.md) · [제작 기준](episodes/nnmath2p09b_edge_dynamics/brief.md) · [자막](episodes/nnmath2p09b_edge_dynamics/captions.srt) · [TTS](episodes/nnmath2p09b_edge_dynamics/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p09b --preview` → `exports/nnmath2p09b_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p09b` → `exports/nnmath2p09b.mp4`

- 신경망의 수학 2부 10 **Catapult Mechanism — Loss가 폭발했는데 왜 다시 학습될까?** — 175초, 1080×1920, 30fps, 무음. large-LR 구간의 Loss spike와 recovery를 NTK 최대 고유값 감소, critical Learning Rate 상승, 변화한 network dynamics로 연결합니다.
- 실제 파일: [장면](episodes/nnmath2p10_catapult/scene.py) · [대본](episodes/nnmath2p10_catapult/narration.md) · [제작 기준](episodes/nnmath2p10_catapult/brief.md) · [자막](episodes/nnmath2p10_catapult/captions.srt) · [TTS](episodes/nnmath2p10_catapult/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p10 --preview` → `exports/nnmath2p10_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p10` → `exports/nnmath2p10.mp4`
- 썸네일: `exports/nnmath2p10_thumbnail.png`

### 신경망의 수학 2부 11 — Benign Overfitting

- 실제 파일: [장면](episodes/nnmath2p11_benign_overfitting/scene.py) · [대본](episodes/nnmath2p11_benign_overfitting/narration.md) · [제작 기준](episodes/nnmath2p11_benign_overfitting/brief.md) · [자막](episodes/nnmath2p11_benign_overfitting/captions.srt) · [TTS](episodes/nnmath2p11_benign_overfitting/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p11 --preview` → `exports/nnmath2p11_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p11` → `exports/nnmath2p11.mp4`
- 썸네일: `exports/nnmath2p11_thumbnail.png`

### 신경망의 수학 2부 12 — Mode Connectivity

- 실제 파일: [장면](episodes/nnmath2p12_mode_connectivity/scene.py) · [대본](episodes/nnmath2p12_mode_connectivity/narration.md) · [제작 기준](episodes/nnmath2p12_mode_connectivity/brief.md) · [자막](episodes/nnmath2p12_mode_connectivity/captions.srt) · [TTS](episodes/nnmath2p12_mode_connectivity/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath2p12 --preview` → `exports/nnmath2p12_preview.mp4`
- 최종본: `python scripts/render.py nnmath2p12` → `exports/nnmath2p12.mp4`
- 썸네일: `exports/nnmath2p12_thumbnail.png`

## 현재 체크아웃에서 제작 가능한 GPU 연산과 최적화 시리즈

- GPU 연산과 최적화 01 **곱셈과 덧셈을 적었는데, GPU는 FMA를 실행한다** — 73초, 1080×1920, 30fps, 무음. CUDA source의 `a*b+c`가 조건에 따라 FMA로 contraction될 수 있으며 반올림 결과도 달라질 수 있음을 보여줍니다.
- 실제 파일: [장면](episodes/gpuops01_fma/scene.py) · [대본](episodes/gpuops01_fma/narration.md) · [제작 기준](episodes/gpuops01_fma/brief.md) · [자막](episodes/gpuops01_fma/captions.srt) · [TTS](episodes/gpuops01_fma/tts_script.txt)
- 미리보기: `python scripts/render.py gpuops01 --preview` → `exports/gpuops01_preview.mp4`
- 최종본: `python scripts/render.py gpuops01` → `exports/gpuops01.mp4`
- GPU 연산과 최적화 02 **GPU가 계산하기도 전에 끝난 계산** — 90초, 1080×1920, 30fps, 무음. `2.0f * 3.0f`가 컴파일 때 `6.0f`로 접히는 흐름과 compile time / runtime의 경계를 보여줍니다.
- 실제 파일: [장면](episodes/gpuops02_constant_folding/scene.py) · [대본](episodes/gpuops02_constant_folding/narration.md) · [제작 기준](episodes/gpuops02_constant_folding/brief.md) · [자막](episodes/gpuops02_constant_folding/captions.srt) · [TTS](episodes/gpuops02_constant_folding/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops02 --preview` → `exports/gpuops02_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops02` → `exports/gpuops02.mp4`
- GPU 연산과 최적화 03 **반복문을 없애면 왜 빨라질까?** — 84초, 1080×1920, 30fps, 무음. Loop Unrolling으로 네 반복이 드러나면 명령 배치와 FMA contraction의 기회가 생기지만, 코드 크기와 레지스터 사용량의 비용도 고려해야 함을 보여줍니다.
- 실제 파일: [장면](episodes/gpuops03_loop_unrolling/scene.py) · [대본](episodes/gpuops03_loop_unrolling/narration.md) · [제작 기준](episodes/gpuops03_loop_unrolling/brief.md) · [자막](episodes/gpuops03_loop_unrolling/captions.srt) · [TTS](episodes/gpuops03_loop_unrolling/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops03 --preview` → `exports/gpuops03_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops03` → `exports/gpuops03.mp4`
- GPU 연산과 최적화 04 **GPU는 코드를 어떤 순서로 실행할까?** — 108초, 1080×1920, 30fps, 무음. Thread 32개로 이루어진 Warp, 공통 FMA 명령, 준비된 Warp를 선택해 메모리 지연을 숨기는 실행과 컴파일 시점 명령 배치의 차이를 보여줍니다.
- 실제 파일: [장면](episodes/gpuops04_warp_scheduling/scene.py) · [대본](episodes/gpuops04_warp_scheduling/narration.md) · [제작 기준](episodes/gpuops04_warp_scheduling/brief.md) · [자막](episodes/gpuops04_warp_scheduling/captions.srt) · [TTS](episodes/gpuops04_warp_scheduling/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops04 --preview` → `exports/gpuops04_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops04` → `exports/gpuops04.mp4`
- GPU 연산과 최적화 05 **행렬곱 뒤의 연산은 왜 합칠 수 있을까?** — 112초, 1080×1920, 30fps, 무음. Thread/Warp가 accumulator/register 상태로 가지고 있는 출력 일부에 원소별 Bias와 ReLU를 연속 적용하고, 그 결과로 중간 materialization을 피하는 Epilogue Fusion을 화면 내 설명 자막과 함께 보여줍니다.
- 실제 파일: [장면](episodes/gpuops05_epilogue_fusion/scene.py) · [대본](episodes/gpuops05_epilogue_fusion/narration.md) · [제작 기준](episodes/gpuops05_epilogue_fusion/brief.md) · [자막](episodes/gpuops05_epilogue_fusion/captions.srt) · [TTS](episodes/gpuops05_epilogue_fusion/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops05 --preview` → `exports/gpuops05_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops05` → `exports/gpuops05.mp4`
- GPU 연산과 최적화 06 **여러 값이 필요한 연산도 합칠 수 있을까?** — 90초, 1080×1920, 30fps, 무음. ReLU 결과 Tensor 전체를 materialize하는 대신 생성되는 값을 partial reduction state에 반영하고, 병렬 partial result를 merge하는 Reduction Fusion을 설명합니다.
- 실제 파일: [장면](episodes/gpuops06_reduction_fusion/scene.py) · [대본](episodes/gpuops06_reduction_fusion/narration.md) · [제작 기준](episodes/gpuops06_reduction_fusion/brief.md) · [자막](episodes/gpuops06_reduction_fusion/captions.srt) · [TTS](episodes/gpuops06_reduction_fusion/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops06 --preview` → `exports/gpuops06_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops06` → `exports/gpuops06.mp4`
- GPU 연산과 최적화 07 **Softmax는 왜 하나의 Kernel이 될 수 있을까?** — 90초, 1080×1920, 30fps, 무음. 안정적인 Softmax를 `MAX → SUB → EXP → SUM → DIV`로 펼치고, reduction 상태 `m`, `ℓ`와 원소별 데이터를 유지하거나 다시 읽으며 여러 단계를 한 Kernel 안에서 연결하는 구조를 설명합니다.
- 실제 파일: [장면](episodes/gpuops07_softmax_fusion/scene.py) · [대본](episodes/gpuops07_softmax_fusion/narration.md) · [제작 기준](episodes/gpuops07_softmax_fusion/brief.md) · [자막](episodes/gpuops07_softmax_fusion/captions.srt) · [TTS](episodes/gpuops07_softmax_fusion/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops07 --preview` → `exports/gpuops07_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops07` → `exports/gpuops07.mp4`
- GPU 연산과 최적화 08 **왜 모든 연산을 하나로 합치지 않을까?** — 90초, 1080×1920, 30fps, 무음. Fusion이 제거한 materialization 대신 live value를 Register에 유지해야 하며, 겹치는 lifetime이 register pressure와 resident warp 수에 영향을 줄 수 있다는 trade-off를 설명합니다.
- 실제 파일: [장면](episodes/gpuops08_register_pressure/scene.py) · [대본](episodes/gpuops08_register_pressure/narration.md) · [제작 기준](episodes/gpuops08_register_pressure/brief.md) · [자막](episodes/gpuops08_register_pressure/captions.srt) · [TTS](episodes/gpuops08_register_pressure/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops08 --preview` → `exports/gpuops08_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops08` → `exports/gpuops08.mp4`
- GPU 연산과 최적화 09 **ReLU는 GPU에서 어떻게 계산될까?** — 87초, 1080×1920, 30fps, 무음. 원소별 ReLU의 작은 계산과 `Read → ReLU → Write`의 데이터 이동을 대비하고, MatMul 뒤 Fusion으로 중간 `Write Y → Read Y`를 피할 수 있는 조건을 보여줍니다.
- 실제 파일: [장면](episodes/gpuops09_relu_memory_fusion/scene.py) · [대본](episodes/gpuops09_relu_memory_fusion/narration.md) · [제작 기준](episodes/gpuops09_relu_memory_fusion/brief.md) · [자막](episodes/gpuops09_relu_memory_fusion/captions.srt) · [TTS](episodes/gpuops09_relu_memory_fusion/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops09 --preview` → `exports/gpuops09_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops09` → `exports/gpuops09.mp4`
- GPU 연산과 최적화 10 **Softmax는 GPU에서 왜 까다로울까?** — 108초, 1080×1920, 30fps, 무음. ReLU의 원소별 독립성과 달리 안정적인 Softmax는 MAX와 SUM 두 Reduction 및 Thread 간 결과 공유가 필요함을 보여줍니다.
- 실제 파일: [장면](episodes/gpuops10_softmax_parallel/scene.py) · [대본](episodes/gpuops10_softmax_parallel/narration.md) · [제작 기준](episodes/gpuops10_softmax_parallel/brief.md) · [자막](episodes/gpuops10_softmax_parallel/captions.srt) · [TTS](episodes/gpuops10_softmax_parallel/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops10 --preview` → `exports/gpuops10_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops10` → `exports/gpuops10.mp4`
- GPU 연산과 최적화 11 **Softmax + Cross Entropy — 중간 확률 없이 Loss까지** — 100초, 1080×1920, 30fps, 무음. 같은 네 입력이 위·아래 두 경로로 분기해 같은 Loss에 도착합니다. 위쪽은 확률 네 개를 만들고 메모리에 저장·읽기, 아래쪽은 정답 값과 공통 정보로 직접 Loss를 계산합니다. 비교 뒤 MAX·SUM tree와 수치 안정성을 설명하고 마지막에는 두 경로가 함께 이동합니다. 실제 Kernel 수는 구현과 입력 크기에 따릅니다.
- 실제 파일: [장면](episodes/gpuops11_softmax_cross_entropy/scene.py) · [대본](episodes/gpuops11_softmax_cross_entropy/narration.md) · [제작 기준](episodes/gpuops11_softmax_cross_entropy/brief.md) · [자막](episodes/gpuops11_softmax_cross_entropy/captions.srt) · [TTS](episodes/gpuops11_softmax_cross_entropy/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops11 --preview` → `exports/gpuops11_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops11` → `exports/gpuops11.mp4`
- GPU 연산과 최적화 12 **Dropout — GPU가 기억해야 하는 선택표, Mask** — 147초 (2:27), 1080×1920, 30fps, 무음. Mask를 입력과 별개의 남김·지움 선택표로 먼저 소개합니다. 같은 표를 통과하는 Forward 값과 Backward gradient를 보여준 뒤, 저장·읽기와 재생성을 비교합니다. GPU 병렬 난수 생성은 후반에 Mask를 만드는 수단으로 설명합니다.
- 실제 파일: [장면](episodes/gpuops12_dropout_rng/scene.py) · [대본](episodes/gpuops12_dropout_rng/narration.md) · [제작 기준](episodes/gpuops12_dropout_rng/brief.md) · [자막](episodes/gpuops12_dropout_rng/captions.srt) · [TTS](episodes/gpuops12_dropout_rng/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops12 --preview` → `exports/gpuops12_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops12` → `exports/gpuops12.mp4`

> 아래 목록에는 현재 체크아웃에 소스가 없는 과거 시리즈 기록도 포함되어 있습니다. 렌더 전에 실제 파일을 확인하세요.

## Pruning & Sparsity — 신경망은 어떻게 더 가볍고 빠르게 계산될까?

- Pruning & Sparsity 01 **Weight를 0으로 만들면 정말 빨라질까?** — 50초, 1080×1920, 30fps, 무음. 작은 Weight를 제거해 Dense 행렬이 Sparse 행렬로 바뀌는 과정을 보여주고, `x × 0 = 0`에서 출발해 `90% PRUNED → 10× FASTER?`라는 질문을 남깁니다.
- [대본](episodes/prune01_zero_weights/narration.md) · [제작 기준](episodes/prune01_zero_weights/brief.md)
- `python scripts/render.py prune01 --preview` → `exports/prune01_preview.mp4`
- `python scripts/render.py prune01` → `exports/prune01.mp4`
- Pruning & Sparsity 02 **90%를 지웠는데 왜 10배 빨라지지 않을까?** — 82초. Dense GEMM이 0도 처리하는 이유에서 출발해, sparse 실행에 필요한 위치 정보·불규칙한 메모리 접근·작업량 불균형을 보여주며 실제 속도는 0의 개수뿐 아니라 배치 구조에도 달렸음을 설명합니다.
- [2편 대본](episodes/prune02_why_not_10x/narration.md) · [2편 제작 기준](episodes/prune02_why_not_10x/brief.md)
- `python scripts/render.py prune02 --preview` → `exports/prune02_preview.mp4`
- `python scripts/render.py prune02` → `exports/prune02.mp4`
- Pruning & Sparsity 03 **왜 하필 2:4 Sparsity일까?** — 90초. Unstructured의 선택 자유와 Structured의 규칙성 사이에서, 연속된 4개마다 2개를 유지하되 남길 위치는 선택할 수 있는 `Semi-Structured` 절충안을 소개합니다.
- [3편 대본](episodes/prune03_why_2_4/narration.md) · [3편 제작 기준](episodes/prune03_why_2_4/brief.md)
- `python scripts/render.py prune03 --preview` → `exports/prune03_preview.mp4`
- `python scripts/render.py prune03` → `exports/prune03.mp4`
- Pruning & Sparsity 04 **신경망 최적화는 왜 하드웨어를 알아야 할까?** — 100초, Pruning 챕터 완결편. 2:4의 지원 경로와 모델 적응을 사례로 `최적화는 수학 × 모델 × 하드웨어의 공동 문제`라는 시리즈 관점을 정리합니다.
- [4편 대본](episodes/prune04_hardware_aware/narration.md) · [4편 제작 기준](episodes/prune04_hardware_aware/brief.md)
- `python scripts/render.py prune04 --preview` → `exports/prune04_preview.mp4`
- `python scripts/render.py prune04` → `exports/prune04.mp4`

## Quantization — AI의 숫자를 얼마나 단순하게 표현해도 될까?

- Quantization 01 **Quantization은 숫자를 어떻게 줄이는 걸까?** — 52초, 1080×1920, 30fps, 무음. 서로 다른 실수 값들이 제한된 대표값 격자로 이동해 하나로 합쳐지는 장면을 통해, Quantization을 `표현 가능한 값의 종류를 줄이는 과정`으로 설명합니다.
- [대본](episodes/quant01_what_is_quantization/narration.md) · [제작 기준](episodes/quant01_what_is_quantization/brief.md)
- `python scripts/render.py quant01 --preview` → `exports/quant01_preview.mp4`
- `python scripts/render.py quant01` → `exports/quant01.mp4`
- Quantization 02 **8bit와 4bit는 실제로 무엇이 다를까?** — 56초. bit가 하나 늘 때마다 가능한 조합과 격자가 두 배씩 늘어나는 과정을 거쳐, 같은 `0~1` 범위에서 8bit의 256개 위치와 4bit의 16개 위치가 만드는 해상도 차이를 보여줍니다.
- [2편 대본](episodes/quant02_bits_and_levels/narration.md) · [2편 제작 기준](episodes/quant02_bits_and_levels/brief.md)
- `python scripts/render.py quant02 --preview` → `exports/quant02_preview.mp4`
- `python scripts/render.py quant02` → `exports/quant02.mp4`
- Quantization 03 **정수 1칸은 실제 값으로 얼마를 의미할까?** — 60초. 실수 `0~1`과 정수 `0~255` 두 축을 대응시켜 `scale=1/255≈0.0039`가 정수 한 칸의 실제 크기임을 설명하고, `0.43→q=110→0.431` 매핑으로 확인합니다.
- [3편 대본](episodes/quant03_scale/narration.md) · [3편 제작 기준](episodes/quant03_scale/brief.md)
- `python scripts/render.py quant03 --preview` → `exports/quant03_preview.mp4`
- `python scripts/render.py quant03` → `exports/quant03.mp4`
- Quantization 04 **실수의 0은 정수 격자의 어디에 놓여야 할까?** — 60초. `−1~3 ↔ 0~255`에서 실수 0이 정수 약 64에 놓이는 이유를 보여주고, 실수 자를 움직여 zero point가 범위에 따라 이동하는 모습을 설명합니다.
- [4편 대본](episodes/quant04_zero_point/narration.md) · [4편 제작 기준](episodes/quant04_zero_point/brief.md)
- `python scripts/render.py quant04 --preview` → `exports/quant04_preview.mp4`
- `python scripts/render.py quant04` → `exports/quant04.mp4`
- Quantization 05 **Quantization을 하면 원래 숫자에서 무엇이 사라질까?** — 60초. 한 값의 격자 snap에서 error를 정의하고, 여러 실수가 하나의 대표값으로 합쳐지는 many-to-one 정보 손실과 최근접 반올림의 `|e|≤Δ/2` 경계를 보여줍니다.
- [5편 대본](episodes/quant05_quantization_error/narration.md) · [5편 제작 기준](episodes/quant05_quantization_error/brief.md)
- `python scripts/render.py quant05 --preview` → `exports/quant05_preview.mp4`
- `python scripts/render.py quant05` → `exports/quant05.mp4`
- Quantization 06 **값 하나가 Quantization 전체를 망칠 수 있는 이유** — 60초. 고정된 16개 격자에서 outlier `20`이 range를 `−1~1`에서 `−1~20`으로 넓혀 step을 약 `0.133`에서 `1.4`로 키우고, 중심 값들을 소수의 대표값으로 합치는 과정을 보여줍니다.
- [6편 대본](episodes/quant06_outlier/narration.md) · [6편 제작 기준](episodes/quant06_outlier/brief.md)
- `python scripts/render.py quant06 --preview` → `exports/quant06_preview.mp4`
- `python scripts/render.py quant06` → `exports/quant06.mp4`
- Quantization 07 **INT8은 컴퓨터에서 무엇을 줄일까?** — 60초. FP32와 INT8의 값당 저장 공간을 비교하고, 동일한 16-byte 전송에 4개와 16개 값을 담는 HBM→Compute 흐름을 통해 작은 datatype이 memory traffic을 줄일 수 있는 이유를 보여줍니다.
- [7편 대본](episodes/quant07_int8_memory/narration.md) · [7편 제작 기준](episodes/quant07_int8_memory/brief.md)
- `python scripts/render.py quant07 --preview` → `exports/quant07_preview.mp4`
- `python scripts/render.py quant07` → `exports/quant07.mp4`
- Quantization 08 **Quantized 모델은 행렬곱을 어떻게 계산할까?** — 60초. `W≈s_wQ_w`, `X≈s_xQ_x`를 대입해 `WX≈s_ws_x(Q_wQ_x)`로 정리하고, Integer GEMM 뒤에 결합 scale을 적용해 근사 출력을 복원하는 과정을 보여줍니다.
- [8편 대본](episodes/quant08_quantized_matmul/narration.md) · [8편 제작 기준](episodes/quant08_quantized_matmul/brief.md)
- `python scripts/render.py quant08 --preview` → `exports/quant08_preview.mp4`
- `python scripts/render.py quant08` → `exports/quant08.mp4`
- Quantization 09 **왜 Weight보다 Activation이 더 까다로울까?** — 60초. inference 전에 고정된 weight는 분포와 scale을 미리 준비해 재사용할 수 있지만, activation은 입력마다 범위가 달라져 고정 scale에서 clipping 또는 거친 resolution이 생길 수 있음을 비교합니다.
- [9편 대본](episodes/quant09_weight_vs_activation/narration.md) · [9편 제작 기준](episodes/quant09_weight_vs_activation/brief.md)
- `python scripts/render.py quant09 --preview` → `exports/quant09_preview.mp4`
- `python scripts/render.py quant09` → `exports/quant09.mp4`
- Quantization 10 **Quantization은 언제 적용해야 할까?** — 60초. 학습 완료 모델을 나중에 줄이는 PTQ와, forward에서 quantization 오차를 경험하며 FP weight를 조정하는 QAT를 `오차를 학습 중 경험했는가`라는 기준으로 비교합니다.
- [10편 대본](episodes/quant10_ptq_vs_qat/narration.md) · [10편 제작 기준](episodes/quant10_ptq_vs_qat/brief.md)
- `python scripts/render.py quant10 --preview` → `exports/quant10_preview.mp4`
- `python scripts/render.py quant10` → `exports/quant10.mp4`
- Quantization 11 **1비트까지 줄이면 무엇을 잃고, 무엇이 남을까?** — 60초, 1부 완결편. 실수 weight의 magnitude가 direction/selection으로 축약되는 의미를 중심으로, activation과 weight가 모두 binary일 때 dot product가 XNOR와 match count로 바뀌는 구조와 ternary의 add/subtract/ignore 의미를 보여줍니다.
- [11편 대본](episodes/quant11_binary_ternary/narration.md) · [11편 제작 기준](episodes/quant11_binary_ternary/brief.md)
- `python scripts/render.py quant11 --preview` → `exports/quant11_preview.mp4`
- `python scripts/render.py quant11` → `exports/quant11.mp4`

## FlashAttention — 계산보다 데이터를 움직이는 방법

- FlashAttention 01 **Attention은 무엇을 저장하고 있을까?** — 64초, 1080×1920, 30fps, 무음. 표준적인 materialized Attention이 `S = QKᵀ`, `P = softmax(S)`의 `N × N` 중간 결과를 만들고 HBM에 쓰고 읽는 흐름을 보여준 뒤, 같은 출력 `O`를 유지하면서 저장을 피할 수 있는지 묻습니다.
- [대본](episodes/flash01_attention_storage/narration.md) · [제작 기준](episodes/flash01_attention_storage/brief.md)
- `python scripts/render.py flash01 --preview` → `exports/flash01_preview.mp4`
- `python scripts/render.py flash01` → `exports/flash01.mp4`
- FlashAttention 02 **계산보다 데이터 이동이 문제라면?** — 72초. 동일한 Attention 수학을 유지한 채 materialized 경로의 HBM 왕복과 tile 기반 on-chip working set을 대비합니다. 마지막에는 전체 score가 필요해 보이는 Softmax 문제를 3편으로 넘깁니다.
- [2편 대본](episodes/flash02_io_awareness/narration.md) · [2편 제작 기준](episodes/flash02_io_awareness/brief.md)
- `python scripts/render.py flash02 --preview` → `exports/flash02_preview.mp4`
- `python scripts/render.py flash02` → `exports/flash02.mp4`
- FlashAttention 03 **전체를 저장하지 않고 Softmax할 수 있을까?** — 78초. 세 score block을 순서대로 보며 running max `m`과 지수합 `ℓ`을 갱신하고, 최댓값이 바뀔 때 기존 합을 새 기준으로 rescale하는 online softmax의 핵심을 보여줍니다.
- [3편 대본](episodes/flash03_online_softmax/narration.md) · [3편 제작 기준](episodes/flash03_online_softmax/brief.md)
- `python scripts/render.py flash03 --preview` → `exports/flash03_preview.mp4`
- `python scripts/render.py flash03` → `exports/flash03.mp4`
- FlashAttention 04 **Attention 출력도 바로 누적할 수 있을까?** — 80초. Key/Value tile을 함께 처리하며 online softmax의 `m,ℓ`과 정규화된 output state `O`를 동시에 갱신하고, full Attention과 같은 결과를 얻는 과정을 보여줍니다.
- [4편 대본](episodes/flash04_output_accumulator/narration.md) · [4편 제작 기준](episodes/flash04_output_accumulator/brief.md)
- `python scripts/render.py flash04 --preview` → `exports/flash04_preview.mp4`
- `python scripts/render.py flash04` → `exports/flash04.mp4`
- FlashAttention 05 **FlashAttention은 무엇을 바꾼 걸까?** — 84초 완결편. Standard의 S/P materialization과 HBM 왕복을 FlashAttention의 tiling, on-chip `m,ℓ,O` state와 나란히 비교하고 두 경로가 같은 exact output에 도달함을 보여줍니다.
- [완결편 대본](episodes/flash05_finale/narration.md) · [완결편 제작 기준](episodes/flash05_finale/brief.md)
- `python scripts/render.py flash05 --preview` → `exports/flash05_preview.mp4`
- `python scripts/render.py flash05` → `exports/flash05.mp4`

## EML — 하나의 primitive로 만드는 계산

- EML 01 **과학용 계산기의 연산자를 하나만 남긴다면?** — 50초, 1080×1920, 30fps, 무음. primitive 축소가 표현 규칙과 연산 graph를 통일하는 이유를 살펴보고, 실제 실행 효율과 구분한 뒤 `EML(x,1)=eˣ`를 첫 tree로 구성합니다.
- [대본](episodes/eml01_single_operator/narration.md) · [시리즈 제작 기준](episodes/eml01_single_operator/brief.md)
- `python scripts/render.py eml01 --preview` → `exports/eml01_preview.mp4`
- `python scripts/render.py eml01` → `exports/eml01.mp4`
- EML 02 **같은 연산자를 연결해서 로그 만들기** — 60초. 동일한 EML 노드 세 개를 아래에서 위로 평가해 `ln x`가 남는 과정을 보여줍니다.
- [2편 대본](episodes/eml02_log_tree/narration.md) · [2편 제작 기준](episodes/eml02_log_tree/brief.md)
- `python scripts/render.py eml02 --preview` → `exports/eml02_preview.mp4`
- `python scripts/render.py eml02` → `exports/eml02.mp4`
- EML 03 **덧셈도 기본 연산자가 아니라면?** — 66초. `1 Add node`와 직접 탐색된 `9 EML nodes · depth 8` graph를 비교해 표현 통일과 실행 최적화를 구분합니다.
- [3편 대본](episodes/eml03_addition_graph/narration.md) · [3편 제작 기준](episodes/eml03_addition_graph/brief.md)
- `python scripts/render.py eml03 --preview` → `exports/eml03_preview.mp4`
- `python scripts/render.py eml03` → `exports/eml03.mp4`
- EML 04 **하나의 연산자로 계산한다는 것은 무엇일까?** — 72초 완결편. 동일한 EML 블록을 exp·ln·add topology로 재배치하며 primitive의 표현력과 실행 효율을 구분합니다.
- [완결편 대본](episodes/eml04_primitive_finale/narration.md) · [완결편 제작 기준](episodes/eml04_primitive_finale/brief.md)
- `python scripts/render.py eml04 --preview` → `exports/eml04_preview.mp4`
- `python scripts/render.py eml04` → `exports/eml04.mp4`

## SVD — 네 가지 관점

한국어 화면 자막을 포함한 세로 1080×1920, 30fps 무음 마스터 네 편입니다. 각 MP4와 같은 이름의 SRT가 `exports/`에 있습니다.

| ID | 제목 | 길이 | 대본 | 영상 |
|---|---|---|---|---|
| svd01 | 최적의 망각 | 115초 | [대본](episodes/svd01_optimal_forgetting/narration.md) | [MP4](exports/svd01.mp4) |
| svd02 | 차이의 생존율 | 99초 | [대본](episodes/svd02_difference_survival/narration.md) | [MP4](exports/svd02.mp4) |
| svd03 | 방향별 감도 지도 | 100초 | [대본](episodes/svd03_sensitivity_map/narration.md) | [MP4](exports/svd03.mp4) |
| svd04 | 입력에게 던지는 독립적인 질문 | 100초 | [대본](episodes/svd04_independent_questions/narration.md) | [MP4](exports/svd04.mp4) |
| svd05 | 타원을 훑어 찾는 두 값 | 85초 | [대본](episodes/svd05_ellipse_extrema/narration.md) | [MP4](exports/svd05.mp4) |
| svd06 | Condition Number: 방향의 불균형 | 60초 | [대본](episodes/svd06_condition_number/narration.md) | [MP4](exports/svd06.mp4) |
| svd07 | 역행렬이 오차를 키우는 이유 | 60초 | [대본](episodes/svd07_inverse_error/narration.md) | [MP4](exports/svd07.mp4) |
| svd08 | 방정식은 거의 같은데, 답은 왜 다를까? | 69초 | [대본](episodes/svd08_near_parallel_lines/narration.md) | [MP4](exports/svd08.mp4) |
| svd09 | 행렬이 한 방향을 완전히 잃는 순간 | 60초 | [대본](episodes/svd09_singular_matrix/narration.md) | [MP4](exports/svd09.mp4) |

[시리즈 제작 안내와 수학적 기준](episodes/svd_series/README.md). `python scripts/render.py svd01`로 렌더합니다. 나머지도 같은 방식이며 `--preview`를 추가하면 360×640 미리보기를 생성합니다.

GPU 연산 시리즈 1화: **수식 하나가 GPU에서 실행되기까지** (145초, 한국어 내레이션 포함).
대본·타이밍·실행 안내는 [GPU 01](episodes/gpu01_formula_to_gpu/narration.md)을 참고하세요.
`python scripts/render.py gpu01 --preview` 또는 `python scripts/render.py gpu01`로 렌더합니다.
공통 시각 컴포넌트는 `gpu_series/`에 분리되어 있습니다.

GPU 2화 **Warp란 무엇인가** (164초, 무음): [대본](episodes/gpu02_warp/narration.md), [구성 안내](episodes/gpu02_warp/brief.md).
`python scripts/render.py gpu02` → `exports/gpu02.mp4`.

GPU 3화 **같은 계산, 다른 메모리 접근** (175초, 무음): [대본](episodes/gpu03_memory_access/narration.md), [구성 안내](episodes/gpu03_memory_access/brief.md).
`python scripts/render.py gpu03` → `exports/gpu03.mp4`. TTS 텍스트는 영어·수식을 한글 발음으로 표기합니다.

Manim 세로형 수학 Shorts. 1080 × 1920, 30fps, 어두운 배경과 원소별 파스텔 색상.
렌더는 음성·음악 없는 마스터로 생성합니다. 보존한 기존 GPU 01 MP4에는 한국어 내레이션이 포함되어 있습니다. LaTeX는 필요 없습니다.

## 에피소드

| ID | 주제 | 길이 | 소스·대본 | 결과물 |
| --- | --- | --- | --- | --- |
| 01 | ReLU 소개 | 38초 | `episodes/01_relu/` | `exports/01.mp4` |
| 02 | ReLU — Information Loss #1 | 42초 | `episodes/02_relu_information_loss/` | `exports/02.mp4` |
| 03 | ReLU — Beyond the count | 40초 | `episodes/03_relu_change_magnitude/` | `exports/03.mp4` |
| 04 | Irreversibility — Beyond Information Loss | 100초 | `episodes/04_irreversibility/` | `exports/04.mp4` |
| 05 | Information Guides Optimization | 100초 | `episodes/05_computation_simplification/` | `exports/05.mp4` |
| 06 | Sigmoid 01 — 위치에 따라 달라지는 압축 | 70초 | `episodes/06_sigmoid_intro/` | `exports/06.mp4` |
| 07 | Sigmoid 02 — 기울기로 읽는 압축률 | 100초 | `episodes/07_sigmoid_derivative/` | `exports/07.mp4` |
| 08 | Sigmoid 03 — 포화와 작아지는 학습 신호 | 100초 | `episodes/08_sigmoid_saturation/` | `exports/08.mp4` |
| 09 | Sigmoid 04 — 값에서 분포로 | 100초 | `episodes/09_sigmoid_distribution/` | `exports/09.mp4` |
| 10 | Sigmoid 05 — 누적확률이라는 새 좌표 | 137초 | `episodes/10_sigmoid_cdf/` | `exports/10.mp4` |
| 11 | Sigmoid 06 — 한계와 선택의 이유 | 150초 | `episodes/11_sigmoid_finale/` | `exports/11.mp4` |
| 12 | Softmax 01 — 점수에서 분포로 | 90초 | `episodes/12_softmax_intro/` | `exports/12.mp4` |
| 13 | Softmax 02 — 숫자가 달라도 결과가 같은 이유 | 84초 | `episodes/13_softmax_shift/` | `exports/13.mp4` |
| 14 | Softmax 03 — 차이가 비율이 되는 이유 | 80초 | `episodes/14_softmax_ratio/` | `exports/14.mp4` |
| 15 | Softmax 04 — Temperature로 분포 조절하기 | 108초 | `episodes/15_softmax_temperature/` | `exports/15.mp4` |
| 16 | Softmax 05 — 서로 연결된 출력과 자코비안 | 119초 | `episodes/16_softmax_jacobian/` | `exports/16.mp4` |
| 17 | Softmax 06 — 두 입력의 Softmax와 Sigmoid | 124초 | `episodes/17_softmax_sigmoid/` | `exports/17.mp4` |
| 18 | Softmax 07 — Smooth Max의 기울기 | 176초 | `episodes/18_softmax_lse/` | `exports/18.mp4` |
| 19 | Softmax 08 — 분포의 집중도를 읽는 Entropy | 166초 | `episodes/19_softmax_entropy/` | `exports/19.mp4` |
| 20 | Softmax 09 — Attention의 비중을 결정하는 함수 (완결) | 152초 | `episodes/20_softmax_attention_finale/` | `exports/20.mp4` |
| legacy | 초기 프로토타입 | 10초 | `archive/relu_short.py` | `exports/legacy.mp4` |

## 실행

```powershell
python -m pip install -r requirements.txt
python scripts/render.py 20 --preview
python scripts/render.py 20
python scripts/render.py 19 --preview
python scripts/render.py 19
python scripts/render.py 18 --preview
python scripts/render.py 18
python scripts/render.py 17 --preview
python scripts/render.py 17
python scripts/render.py 16 --preview
python scripts/render.py 16
python scripts/render.py 15 --preview
python scripts/render.py 15
python scripts/render.py 14 --preview
python scripts/render.py 14
python scripts/render.py 13 --preview
python scripts/render.py 13
python scripts/render.py 12 --preview
python scripts/render.py 12
python scripts/render.py 11 --preview
python scripts/render.py 11
python scripts/render.py 10 --preview
python scripts/render.py 10
python scripts/render.py 09 --preview
python scripts/render.py 09
python scripts/render.py 08 --preview
python scripts/render.py 08
python scripts/render.py 07 --preview
python scripts/render.py 07
python scripts/render.py 06 --preview
python scripts/render.py 06
python scripts/render.py 05 --preview
python scripts/render.py 05
python scripts/render.py 04 --preview
python scripts/render.py 04
python scripts/render.py 03 --preview
python scripts/render.py 03
python scripts/render.py 02 --preview
python scripts/render.py 02
python scripts/render.py 01
python scripts/render.py legacy
```

미리보기는 360 × 640이며 `exports/02_preview.mp4`처럼 별도 저장됩니다.
렌더 스크립트는 실행 위치와 무관하게 프로젝트 루트를 기준으로 동작합니다.

## 폴더 규칙

- `episodes/<번호>_<주제>/`: scene.py, narration.md, 필요하면 brief.md.
- `archive/`: 보존하는 초기 프로토타입.
- `scripts/`: 공통 렌더 도구.
- `exports/`: 공유·편집용 MP4. Git 제외.
- `media/<ID>/`: 재생성 가능한 렌더 캐시. 기존 media 결과도 보존.

새 에피소드는 scripts/render.py의 EPISODES에 등록합니다.
각 에피소드 소스는 독립적으로 동작하며 공통 해상도 환경변수를 지원합니다.
02편은 벡터 → 억제 비율 → 분포 → 음수 확률 → 같은 개수, 다른 크기로 이어집니다.
Zeroed Ratio는 정보 손실 자체가 아닌 단순 억제 지표입니다.

## TTS 편집용 타이밍

13편부터 짧은 질문·연결 문장은 2~3.5초 내에 전환하고, 문장 길이와 시각적 설명량에 따라 시간을 배분합니다. 전환 시간은 각 구간에 포함합니다. 실제 음성 미제공 시 발화 길이를 추정하며, 타임코드 대본과 SRT를 함께 제공합니다.

- GPU 04: `episodes/gpu04_memory_spaces/scene.py` → `python scripts/render.py gpu04` → `exports/gpu04.mp4` (174초, 무음)

- GPU 05: `episodes/gpu05_naive_gemm/scene.py` → `python scripts/render.py gpu05` → `exports/gpu05.mp4` (174초, 무음)

- GPU 06: `episodes/gpu06_tiled_gemm/scene.py` → `python scripts/render.py gpu06` → `exports/gpu06.mp4` (174초, 무음)

- GPU 07: `episodes/gpu07_tile_size/scene.py` → `python scripts/render.py gpu07` → `exports/gpu07.mp4` (174초, 무음)

- GPU 08: `episodes/gpu08_register_occupancy/scene.py` → `python scripts/render.py gpu08` → `exports/gpu08.mp4` (174초, 무음)

- GPU 09: `episodes/gpu09_bank_conflict/scene.py` → `python scripts/render.py gpu09` → `exports/gpu09.mp4` (174초, 무음)

## 선형대수학 시리즈

- LA 01 **행렬은 관계를 기록한다** — 130초, 1080×1920, 30fps, 무음. 세 대상 사이의 방향 있는 연결이 행렬의 각 칸으로 정리되는 과정.
- [대본](episodes/la01_matrix_relations/narration.md) · [제작 의도와 시리즈 구상](episodes/la01_matrix_relations/brief.md)
- `python scripts/render.py la01 --preview` → `exports/la01_preview.mp4`
- `python scripts/render.py la01` → `exports/la01.mp4`
- 이전 공간 변환 버전 영상·대본: `archive/la01_space_version/`. 다음 편 예고: 행렬과 벡터의 곱.

- LA 02 **기여를 모으면 결과가 된다** — 90초, 1080×1920, 30fps, 무음. 여러 출발점의 가중 기여를 목적지별로 합산합니다.
- [2편 대본](episodes/la02_matrix_vector_product/narration.md) · [구성 및 수학 확인](episodes/la02_matrix_vector_product/brief.md)
- `python scripts/render.py la02` → `exports/la02.mp4` (`--preview`는 별도 미리보기).

- LA 03 **경로를 잇고, 기여를 모은다** — 100초, 1080×1920, 30fps, 무음. 두 단계 경로의 곱과 합을 통해 A²와 행렬곱을 설명합니다.
- [3편 대본](episodes/la03_matrix_paths/narration.md) · [구성 및 수학 확인](episodes/la03_matrix_paths/brief.md)
- `python scripts/render.py la03` → `exports/la03.mp4` (`--preview`는 별도 미리보기).

## 화면 표기와 TTS 표기

영상의 화면 문구, 자막(SRT), narration.md에서는 숫자·영어·수식을 원래 표기 그대로 사용합니다(예: `0.8`, `A²`, `k`, `BA`). `영 점 팔`, `에이 제곱`, `케이` 같은 한글 발음 표기는 `tts_script.txt`에만 사용합니다. 자연스러운 한국어 서수 표현(첫 번째, 두 번째 등)은 유지합니다.

- LA 04 **반복하면 어떤 패턴이 남을까?** — 110초, 1080×1920, 30fps, 무음. 반복 계산의 크기와 비율을 비교하며 고유벡터·고유값을 예고합니다.
- [4편 대본](episodes/la04_repeated_patterns/narration.md) · [구성 및 수학 확인](episodes/la04_repeated_patterns/brief.md)
- `python scripts/render.py la04` → `exports/la04.mp4` (`--preview`는 별도 미리보기).

- LA 05 **같은 입력, 다른 패턴별 배율** — 99초, 1080×1920, 30fps, 무음. 섞인 두 고유패턴을 서로 다르게 조절하고 다시 합치는 과정을 보여줍니다.
- [5편 대본](episodes/la05_pattern_filter/narration.md) · [구성 및 수학 확인](episodes/la05_pattern_filter/brief.md)
- `python scripts/render.py la05` → `exports/la05.mp4` (`--preview`는 별도 미리보기).

- LA 06 **행렬이 지우는 차이** — 100초, 1080×1920, 30fps, 무음. 두 입력이 같은 출력으로 겹치는 과정에서 영공간을 설명합니다.
- [6편 대본](episodes/la06_nullspace/narration.md) · [구성 및 수학 확인](episodes/la06_nullspace/brief.md)
- `python scripts/render.py la06` → `exports/la06.mp4` (`--preview`는 별도 미리보기).

- LA 07 **벡터가 늘면 자유도도 늘까?** — 108초, 1080×1920, 30fps, 무음. 계수의 중복과 상쇄 관계를 통해 자유도·선형독립·표현의 유일성을 설명합니다.
- [7편 대본](episodes/la07_independence/narration.md) · [구성 및 수학 확인](episodes/la07_independence/brief.md)
- `python scripts/render.py la07` → `exports/la07.mp4` (`--preview`는 별도 미리보기).

- LA 08 **Rank: 실제로 남는 자유도** — 107초, 1080×1920, 30fps, 무음. 같은 2×2 행렬의 Rank 1·2를 출력 공간으로 비교합니다.
- [8편 대본](episodes/la08_rank/narration.md) · [구성 및 수학 확인](episodes/la08_rank/brief.md)
- `python scripts/render.py la08` → `exports/la08.mp4` (`--preview`는 별도 미리보기).

- LA 09 **방향과 조합으로 나누어 기록하기** — 112초, 1080×1920, 30fps, 무음. Rank 분해 A=BC로 독립적인 방향과 열의 조합을 분리합니다.
- [9편 대본](episodes/la09_rank_factorization/narration.md) · [구성 및 수학 확인](episodes/la09_rank_factorization/brief.md)
- `python scripts/render.py la09` → `exports/la09.mp4` (`--preview`는 별도 미리보기).

- LA 10 **SVD: 관계를 채널로 나누어 보기** — 109초, 1080×1920, 30fps, 무음. 반투명 채널 레이어로 입력 패턴·전달 강도·출력 패턴을 분리합니다.
- [10편 대본](episodes/la10_svd_channels/narration.md) · [구성 및 수학 확인](episodes/la10_svd_channels/brief.md)
- `python scripts/render.py la10` → `exports/la10.mp4`

## 정보 이론 · 엔트로피 시리즈

- info01 **정보는 무엇을 줄이는가?** — 45.5초, 무음 세로 영상.
- [대본](episodes/info01_eliminating_possibilities/narration.md) · [제작 기준](episodes/info01_eliminating_possibilities/brief.md)
- `.\.venv\Scripts\python.exe scripts/render.py info01 --preview`
- `.\.venv\Scripts\python.exe scripts/render.py info01` → `exports/info01.mp4`
- 후속 구성: 02 같은 결과와 관측 전 확률(구현), 03 자기정보량과 로그(구현), 04 평균 정보량과 엔트로피(구현).

- info02 **같은 결과, 다른 정보량** — 51.93초, 무음 세로 영상. 확률과 믿음을 구분하고 관측 전 예측분포를 비교합니다.
- [대본](episodes/info02_prior_probability/narration.md) · [제작 기준](episodes/info02_prior_probability/brief.md)
- `.\.venv\Scripts\python.exe scripts/render.py info02 --preview`
- `.\.venv\Scripts\python.exe scripts/render.py info02` → `exports/info02.mp4`

- info03 **확률은 곱해지는데, 정보는 왜 더해질까?** — 59.47초, 무음 세로 영상. 로그를 곱셈의 깊이를 세는 좌표계로 보여줍니다.
- [대본](episodes/info03_multiplication_depth/narration.md) · [제작 기준](episodes/info03_multiplication_depth/brief.md)
- `.\.venv\Scripts\python.exe scripts/render.py info03 --preview`
- `.\.venv\Scripts\python.exe scripts/render.py info03` → `exports/info03.mp4`

- info04 **현실 하나를 특정하려면 몇 번을 나눠야 할까?** — 58.50초, 개정판 무음 세로 영상. 질문 트리의 평균 깊이를 통해 엔트로피와 구분 비용의 한계를 보여줍니다.
- [대본](episodes/info04_expected_information/narration.md) · [제작 기준](episodes/info04_expected_information/brief.md)
- `.\.venv\Scripts\python.exe scripts/render.py info04 --preview`
- `.\.venv\Scripts\python.exe scripts/render.py info04` → `exports/info04.mp4`

- info05 **압축은 예상 가능한 것을 짧게 쓰는 것이다** — 57.03초, 무음 세로 영상. 같은 20기호를 40→30 bits로 표현하며 확률에 맞춘 비용 재배분을 보여줍니다.
- [대본](episodes/info05_predictable_cost/narration.md) · [제작 기준](episodes/info05_predictable_cost/brief.md)
- `.\.venv\Scripts\python.exe scripts/render.py info05 --preview`
- `.\.venv\Scripts\python.exe scripts/render.py info05` → `exports/info05.mp4`

- info06 **틀린 확률을 믿으면 왜 더 많은 비트를 쓰게 될까?** — 58.63초, 무음 세로 영상. 현실의 빈도와 모형의 가격표로 Cross Entropy를 보여줍니다. 실제 정수 코드 길이와 이상적 log-cost를 구별합니다.
- [대본](episodes/info06_wrong_price/narration.md) · [제작 기준](episodes/info06_wrong_price/brief.md)
- `.\.venv\Scripts\python.exe scripts/render.py info06 --preview`
- `.\.venv\Scripts\python.exe scripts/render.py info06` → `exports/info06.mp4`

- info07 **같은 데이터, 187비트 차이** — 59.30초, 무음 세로 영상. 같은 1000개 데이터의 산술 부호화 본문 813/1000비트를 비교하고, 실제 차이와 KL의 이상적 평균 차이를 구분합니다.
- [대본](episodes/info07_extra_bill/narration.md) · [제작 기준](episodes/info07_extra_bill/brief.md)
- `.\.venv\Scripts\python.exe scripts/render.py info07 --preview`
- `.\.venv\Scripts\python.exe scripts/render.py info07` → `exports/info07.mp4`

- info08 **이미 아는 것은 다시 보내지 않는다** — 59.83초, 개정판 무음 세로 영상. 같은B의01전송과 이미 아는0+새로 받은1 복원으로 조건부 엔트로피·상호정보량을 소개합니다. X도 새로 보내면1bit+1bit=2bits라는 장면8초와 확률가중 평균의 조건을 강조하고, 이미 아는 정보의 가공으로9편을 연결합니다.
- [대본](episodes/info08_known_bit/narration.md) · [제작 기준](episodes/info08_known_bit/brief.md)
- `.\.venv\Scripts\python.exe scripts/render.py info08 --preview`
- `.\.venv\Scripts\python.exe scripts/render.py info08` → `exports/info08.mp4`

- info09 **계산이 복잡해지면, 단서도 늘까?** — 58.13초, 무음 세로 영상. 같은0으로 합쳐진 A/B를 ×5,+3,제곱,+8로 가공해 같은17이 되는 과정을 보여줍니다. 구분 보존과 추가 합치기를 비교한 뒤 Data Processing Inequality를 소개합니다.
- [대본](episodes/info09_same_input/narration.md) · [제작 기준](episodes/info09_same_input/brief.md)
- `.\.venv\Scripts\python.exe scripts/render.py info09 --preview`
- `.\.venv\Scripts\python.exe scripts/render.py info09` → `exports/info09.mp4`

- info10 **엔트로피가 압축 한계가 되는 이유** — 70.40초, 개정판 무음 세로 영상. 공유목록의01전송과8비트복원,1비트번호충돌,4후보/8후보 비교를 통해 전형후보수→번호길이→기호당엔트로피한계를 설명합니다. 가우시안은제외했습니다.
- [대본](episodes/info10_typical_worlds/narration.md) · [제작 기준](episodes/info10_typical_worlds/brief.md)
- `.\.venv\Scripts\python.exe scripts/render.py info10 --preview`
- `.\.venv\Scripts\python.exe scripts/render.py info10` → `exports/info10.mp4`

- info11 **가장 밀도가 높은 곳에 샘플이 모일까?** — 70.57초, 무음 세로 영상. 실제100차원샘플2000개의거리분포와동일폭고리의공간크기를비교해,최대점밀도와확률질량이모이는영역을구별합니다.
- [대본](episodes/info11_density_shell/narration.md) · [제작 기준](episodes/info11_density_shell/brief.md)
- `.\.venv\Scripts\python.exe scripts/render.py info11 --preview`
- `.\.venv\Scripts\python.exe scripts/render.py info11` → `exports/info11.mp4`


## 과학의 한 장면

질문 하나에서 출발해 현상 → 예상 → 관측의 불일치 → 설명으로 이어지는 3분 이내 세로 영상.

- `science01`: **은하 바깥의 별은 왜 이렇게 빠를까?** — 암흑물질 헤일로를 운동에서 추론하는 58초 영상.
- 실제 소스: `episodes/science01_dark_matter/scene.py`, `brief.md`, `narration.md`, `captions.srt`, `tts_script.txt`.
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py science01 --preview`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py science01`
- 출력: `exports/science01_preview.mp4`, `exports/science01.mp4` (무음; TTS/SRT 별도).

science01 화면 길이는 대사 글자 수에 비례해 배분합니다. `python scripts/retime_science01.py --duration 58`로 대본·SRT·timing.json을 다시 생성한 뒤 렌더합니다.


### 과학의 한 장면 02 — 보이지 않는 질량은 어떻게 찾을까?

- `science02`: 빛의 왜곡 → 총질량 지도 → 별·가스와 비교 → 암흑물질. 61초 무음 세로 영상.
- 실제 소스: `episodes/science02_gravitational_lensing/`의 scene.py, brief.md, narration.md, captions.srt, tts_script.txt, timing.json.
- 타이밍 재배분: `.\.venv\Scripts\python.exe scripts/retime_science02.py --duration 61`
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py science02 --preview`
- 최종: `.\.venv\Scripts\python.exe scripts/render.py science02`
- 출력: `exports/science02_preview.mp4`, `exports/science02.mp4`.


### 과학의 한 장면 03 — 가스와 질량은 왜 서로 다른 곳에 있을까?

- `science03`: Bullet Cluster 충돌 → 가스와 은하의 다른 운동 → X선 가스 지도와 렌즈 질량 지도의 어긋남. 76초 무음 세로 영상.
- 실제 파일: `episodes/science03_bullet_cluster/`의 scene.py, brief.md, narration.md, tts_script.txt, captions.srt, timing.json.
- 타이밍: `.\.venv\Scripts\python.exe scripts/retime_science03.py --duration 76`
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py science03 --preview`
- 최종: `.\.venv\Scripts\python.exe scripts/render.py science03`
- 출력: `exports/science03_preview.mp4`, `exports/science03.mp4`.
- 화면은 02편의 공통 색상·문자·대사 길이 기반 구간 도구를 가져와 사용한다.


### 과학의 한 장면 04 — 멀리 있는 천체의 질량을 재는 법

- `science04`: 비리얼 정리. 같은 크기에서 빠를수록, 같은 속도에서 클수록 더 무겁다는 관계를 설명하는 83초 무음 영상.
- 실제 파일: `episodes/science04_virial_theorem/`의 scene.py, brief.md, narration.md, tts_script.txt, captions.srt, timing.json.
- 타이밍 재배분: `.\.venv\Scripts\python.exe scripts/retime_science04.py --duration 83`
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py science04 --preview`
- 최종: `.\.venv\Scripts\python.exe scripts/render.py science04`
- 출력: `exports/science04_preview.mp4`, `exports/science04.mp4`.
- 적용 조건은 안정된 중력계이며, 충돌 은하단에는 평형 가정부터 확인해야 합니다.


### 과학의 한 장면 05 — 중력으로 붕괴하면 왜 한 점이 되지 않을까?

- `science05`: 수축 → 가속 → 중심 통과 → 궤도 혼합 → 움직이는 안정. 91초 무음 세로 영상.
- 실제 소스: `episodes/science05_gravitational_collapse/`의 scene.py, brief.md, narration.md, captions.srt, tts_script.txt, timing.json, prepare.py, collapse_data.npz.
- 입자 자료 재생성: `.\.venv\Scripts\python.exe episodes/science05_gravitational_collapse/prepare.py`
- 타이밍: `.\.venv\Scripts\python.exe scripts/retime_science05.py --duration 91`
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py science05 --preview`
- 최종: `.\.venv\Scripts\python.exe scripts/render.py science05`
- 출력: `exports/science05_preview.mp4`, `exports/science05.mp4`.


### 과학의 한 장면 06 — 우주는 팽창하는데 왜 어떤 곳은 다시 무너질까?

- `science06`: 평균 배경 팽창과 국소 과밀 영역의 최대 팽창 및 수축을 같은 시간축으로 비교하는 90초 무음 영상.
- 실제 파일: `episodes/science06_turnaround/`의 scene.py, brief.md, narration.md, tts_script.txt, captions.srt, timing.json.
- 타이밍 재배분: `.\.venv\Scripts\python.exe scripts/retime_science06.py --duration 90`
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py science06 --preview`
- 최종: `.\.venv\Scripts\python.exe scripts/render.py science06`
- 출력: `exports/science06_preview.mp4`, `exports/science06.mp4`.


### 과학의 한 장면 07 — 안정된 크기는 왜 최대 팽창의 절반쯤일까?

- `science07`: 최대 팽창과 비리얼 상태의 에너지를 비교해 반지름 1/2을 유도하는 93초 무음 영상.
- 실제 파일: `episodes/science07_half_radius/`의 scene.py, brief.md, narration.md, tts_script.txt, captions.srt, timing.json.
- 타이밍 재배분: `.\.venv\Scripts\python.exe scripts/retime_science07.py --duration 93`
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py science07 --preview`
- 최종: `.\.venv\Scripts\python.exe scripts/render.py science07`
- 출력: `exports/science07_preview.mp4`, `exports/science07.mp4`.
- 질량과 에너지가 보존되고, 두 상태의 구조 계수가 같은 단순 구형 모형의 결과다. 실제 모든 halo의 반지름이 반드시 절반이라는 주장이 아니다.


### 과학의 한 장면 08 — 작은 밀도 차이는 어떻게 은하가 될까?

- `science08`: 상대적인 밀도 차이의 중력 성장 → 비선형 붕괴 → 헤일로 → 가스 냉각·원반·별 → 은하. 102초 무음 세로 영상.
- 실제 파일: `episodes/science08_density_growth/`의 scene.py, brief.md, narration.md, tts_script.txt, captions.srt, timing.json.
- 타이밍 재배분: `.\.venv\Scripts\python.exe scripts/retime_science08.py --duration 102`
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py science08 --preview`
- 최종: `.\.venv\Scripts\python.exe scripts/render.py science08`
- 출력: `exports/science08_preview.mp4`, `exports/science08.mp4`.
- 1.686은 실제 밀도 배수가 아니라 물질 우세 구형 모형에서 선형 이론으로 연장한 붕괴 기준이다. 마지막은 원반 은하가 만들어지는 한 사례를 개념도로 보여준다.


### 과학의 한 장면 09 — 은하는 왜 납작할까?

- `science09`: 중력 수축 → 각운동량과 빠른 회전 → 두꺼운 구름 → 가스 충돌·방사 냉각 → 얇은 원반. 78초 무음 세로 영상.
- 실제 파일: `episodes/science09_flat_galaxies/`의 scene.py, brief.md, narration.md, tts_script.txt, captions.srt, timing.json.
- 타이밍: `.\.venv\Scripts\python.exe scripts/retime_science09.py --duration 78`
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py science09 --preview`
- 최종: `.\.venv\Scripts\python.exe scripts/render.py science09`
- 출력: `exports/science09_preview.mp4`, `exports/science09.mp4`.
- 마지막에는 동일한 3D 별 원반과 두꺼운 중심부를 정면에서 옆면으로 90도 시점 회전하여 비교한다.

### 과학의 한 장면 10 — 우주에는 왜 거대한 빈 공간이 생길까?

- `science10`: 작은 저밀도 → 주변으로 물질 이동 → 더 성긴 영역 → 벽·필라멘트와 Cosmic Void. 70초 무음 세로 영상.
- 실제 파일: `episodes/science10_cosmic_void/`의 scene.py, brief.md, narration.md, tts_script.txt, captions.srt, timing.json.
- 대사 길이 기준 재배분: `.\.venv\Scripts\python.exe scripts/retime_science10.py --duration 70`
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py science10 --preview`
- 최종: `.\.venv\Scripts\python.exe scripts/render.py science10`
- 출력: `exports/science10_preview.mp4`, `exports/science10.mp4`.

## 과학의 한 장면 11 — 보이지 않는 입자를 어떻게 관측할까?

- `science11`: 뉴트리노의 희귀한 상호작용 → 2차 하전입자 → 체렌코프 빛 → 센서 시간차 → 우주 방향 재구성. 2026년 노벨 물리학상과 연결되는 61초 무음 세로 영상.
- 실제 파일: `episodes/science11_icecube_neutrino/`의 scene.py, brief.md, narration.md, tts_script.txt, captions.srt, timing.json.
- 확인된 TTS 구간 적용: `.\.venv\Scripts\python.exe scripts/retime_science11.py` 또는 `python scripts/retime_science11.py`.
- 미리보기: `python scripts/render.py science11 --preview`
- 최종: `python scripts/render.py science11`
- 출력: `exports/science11_preview.mp4`, `exports/science11.mp4`.

## 과학의 한 장면 12 — 검출기를 만든 것이 왜 노벨상일까?

- `science12`: 빛의 흡수와 하전 우주선의 굴절 → 방향을 보존하는 고에너지 뉴트리노 → 거대 검출기의 필요 → 2002년 우주 뉴트리노와 2013년 IceCube의 차이 → 새로운 관측 창. 2026년 노벨 물리학상 2편, 67초 무음 세로 영상.
- 실제 파일: `episodes/science12_neutrino_telescope/`의 scene.py, brief.md, narration.md, tts_script.txt, captions.srt, timing.json.
- 확인된 TTS 구간 적용: `python scripts/retime_science12.py`
- 미리보기: `python scripts/render.py science12 --preview`
- 최종: `python scripts/render.py science12`
- 출력: `exports/science12_preview.mp4`, `exports/science12.mp4`.
- Void가 물질을 밀어내는 힘은 없다. 평균보다 약한 중력 감속과 주변 과밀 구조로의 이동을 구별하며, 완전히 비어 있지 않음을 표시한다. 입자 흐름과 우주 거미줄은 개념도다.


## GPU 연산과 최적화 13 — LayerNorm (148초 · 2:28)

- 실제 파일: [장면](episodes/gpuops13_layernorm/scene.py) · [대본](episodes/gpuops13_layernorm/narration.md) · [제작 기준](episodes/gpuops13_layernorm/brief.md) · [자막](episodes/gpuops13_layernorm/captions.srt) · [TTS](episodes/gpuops13_layernorm/tts_script.txt)
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py gpuops13 --preview` → `exports/gpuops13_preview.mp4`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py gpuops13` → `exports/gpuops13.mp4`
- 평균·분산의 병렬 집계, Welford 상태 병합, 결합 실행과 입력 재사용을 데이터 이동으로 설명합니다.

### 정보이론 12 — 정보 1비트를 지우는 데 필요한 최소 비용

`episodes/info12_landauer/`의 `scene.py`, `content.py`, `brief.md`, `narration.md`, `tts_script.txt`, `captions.srt`를 사용합니다. 두 칸 상자의 공을 왼쪽에 모으는 물리적 초기화를 중심으로 설명합니다. 약 79.5초이며, 평균 환경 열의 하한 수식은 후반에 한 번만 등장합니다. 실제 컴퓨터 소비와 삭제의 최소 비용을 구분합니다.

```powershell
.\.venv\Scripts\python.exe scripts/render.py info12 --preview
.\.venv\Scripts\python.exe scripts/render.py info12
```

결과: `exports/info12_preview.mp4`, `exports/info12.mp4` (무음, 음성 합성 대본과 자막 별도).

### 정보이론 13 — 삭제하지 말고 되감아라

`episodes/info13_uncompute/`의 `scene.py`, `content.py`, `brief.md`, `narration.md`, `tts_script.txt`, `captions.srt`를 사용합니다. 약 74초의 compute–copy–uncompute 예제로 입력 보존, 결과 보존, 작업 칸 복원을 보여준 뒤 동일한 양자 회로로 연결합니다.

```powershell
.\.venv\Scripts\python.exe scripts/render.py info13 --preview
.\.venv\Scripts\python.exe scripts/render.py info13
```

결과: `exports/info13_preview.mp4`, `exports/info13.mp4` (무음, TTS 대본과 자막 별도).

### 정보이론 14 — 정보만 있으면 제2법칙을 깰 수 있을까?

`episodes/info14_maxwell_demon/`의 `scene.py`, `content.py`, `brief.md`, `narration.md`, `tts_script.txt`, `captions.srt`를 사용합니다. 약 79초, 맥스웰의 도깨비의 분자 선별·온도 차이·열기관·메모리 재사용을 시각화하고 정보가 물리적 제어 자원이라는 결론으로 끝납니다. 기존 13편은 유지합니다.

```powershell
.\.venv\Scripts\python.exe scripts/render.py info14 --preview
.\.venv\Scripts\python.exe scripts/render.py info14
```

결과: `exports/info14_preview.mp4`, `exports/info14.mp4` (무음, TTS 대본과 자막 별도).

### 정보이론 15 — 1비트의 정보는 얼마의 일을 만들 수 있을까?

`episodes/info15_szilard_engine/`의 `scene.py`, `content.py`, `brief.md`, `narration.md`, `tts_script.txt`, `captions.srt`를 사용합니다. 약 78초, 같은 열환경과 팽창을 좌우 비교합니다. 위치 미확인 상태의 칸막이 제거와 위치 측정 후 피스톤 연결을 비교해, 1비트가 일을 꺼낼 방향을 선택하는 역할을 보여줍니다. 최대 평균 일 수식은 비교 뒤에 제시합니다.

```powershell
.\.venv\Scripts\python.exe scripts/render.py info15 --preview
.\.venv\Scripts\python.exe scripts/render.py info15
```

결과: `exports/info15_preview.mp4`, `exports/info15.mp4` (무음, TTS 대본과 자막 별도).


## 정보이론 16 — 학습이 가능하려면 세상이 특별해야 합니다 — No Free Lunch

`episodes/info16_no_free_lunch/`의 영상·제작 기준·대본·TTS·SRT를 사용합니다. 약 79초. 제목·중간 설명·마무리에서 No Free Lunch 정리의 이름과 의미를 연결합니다. 같은 학습 데이터에 맞는 16개 세계와 8/8 분할로 No Free Lunch의 균등 평균 조건을 보여주고, 현실의 구조와 귀납 편향이 맞을 때 일반화가 가능하다는 결론으로 마무리합니다. 기존 15편은 유지합니다.

```powershell
.\.venv\Scripts\python.exe scripts/render.py info16 --preview
.\.venv\Scripts\python.exe scripts/render.py info16
```

결과: `exports/info16_preview.mp4`, `exports/info16.mp4` (무음 / TTS·자막 별도).
# 신경망의 수학 13 — 신경망 학습을 동역학계로 보면 보이는 것

- 147초 목표, 1080×1920, 30fps, 무음. 한 점의 gradient를 Parameter Space 전체의 vector field로 확장하고, initial condition에서 시작한 trajectory가 basin, saddle, stable/unstable direction, attractor로 이어지는 구조를 보여줍니다. Gradient Flow와 실제 Gradient Descent를 구별하고 learning rate와 SGD noise를 짧게 보충합니다.
- 실제 파일: [장면](episodes/nnmath13_gradient_dynamics/scene.py) · [대본](episodes/nnmath13_gradient_dynamics/narration.md) · [제작 기준](episodes/nnmath13_gradient_dynamics/brief.md) · [자막](episodes/nnmath13_gradient_dynamics/captions.srt) · [TTS](episodes/nnmath13_gradient_dynamics/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath13 --preview` → `exports/nnmath13_preview.mp4`
- 최종본: `python scripts/render.py nnmath13` → `exports/nnmath13.mp4`

## 신경망의 수학 14 — 왜 Hessian에는 0에 가까운 고유값이 많을까?

- 141초 목표, 1080×1920, 30fps, 무음. 둥근 bowl과 방향별 곡률에서 출발해 Hessian 고유방향과 near-zero spectrum을 소개하고, overparameterization, ReLU scaling symmetry, data-null direction, inactive unit이 flat direction을 만드는 과정을 보여줍니다. exact symmetry와 approximately flat direction을 구별한 뒤 `few stiff directions + many flat directions`인 고차원 valley로 정리합니다.
- 실제 파일: [장면](episodes/nnmath14_hessian_flat_directions/scene.py) · [대본](episodes/nnmath14_hessian_flat_directions/narration.md) · [제작 기준](episodes/nnmath14_hessian_flat_directions/brief.md) · [자막](episodes/nnmath14_hessian_flat_directions/captions.srt) · [TTS](episodes/nnmath14_hessian_flat_directions/tts_script.txt)
- 미리보기: `python scripts/render.py nnmath14 --preview` → `exports/nnmath14_preview.mp4`
- 최종본: `python scripts/render.py nnmath14` → `exports/nnmath14.mp4`
