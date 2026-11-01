# GPU LEVEL 09 — L1 & L2 Cache

169초 · 독립 씬14개 · 가로/세로 30fps · 무음·전체 자막.

```powershell
python longforms/gpuh09_cache/build.py --preview
python longforms/gpuh09_cache/build.py --jobs 4
python longforms/gpuh09_cache/verify.py
```

메모리 공간과 캐시 계층을 별도 축에 배치한다. 캐시 상태와 자원 배분 비율은 설명용 모형이며 실측 결과가 아니다. 실제 CUDA 계산 결과는 `cuda_trace.json`과 `cuda_validation.txt`에 기록한다.

`cache_visuals.py`는 화면과 애니메이션, `cache_model.py`는 가정한 캐시 사례, `cache_examples.cu`는 실행 가능한 CUDA 예제다. `verify.py`는 요청 종료 지점, L1 우회, 값 공급원, Shared 명시적 저장, L2 재사용 가정, 실제 출력값과 영상 규격을 검증한다.

최종 영상은 `exports/gpuh09_cache_169s_shorts_final.mp4`와 `exports/gpuh09_cache_169s_longform_final.mp4`다.

기술출처: [NVIDIA Programming Model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html), [Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html).
