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

- `science01`: **은하 바깥의 별은 왜 이렇게 빠를까?** — 암흑물질 헤일로를 운동에서 추론하는 104초 영상.
- 실제 소스: `episodes/science01_dark_matter/scene.py`, `brief.md`, `narration.md`, `captions.srt`, `tts_script.txt`.
- 미리보기: `.\.venv\Scripts\python.exe scripts/render.py science01 --preview`
- 최종본: `.\.venv\Scripts\python.exe scripts/render.py science01`
- 출력: `exports/science01_preview.mp4`, `exports/science01.mp4` (무음; TTS/SRT 별도).
