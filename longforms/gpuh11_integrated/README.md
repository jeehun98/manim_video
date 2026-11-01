# GPU LEVEL 11 — 최종 통합편

191초 · 독립 씬16개 · 가로형만 · 30fps · 무음·전체 자막.

```powershell
python longforms/gpuh11_integrated/build.py --preview
python longforms/gpuh11_integrated/build.py --jobs 4
python longforms/gpuh11_integrated/verify.py
```

N=512 / Block=128 / Grid=4의 실행 가능한 vectorAdd 하나를 끝까지 추적한다. Block 1 Thread 5의 i=133에서 4+7=11이다. 캐시·SM 배치와 자원 비교는 가정 모형이며 실제 GPU 실행 추적이 아니다. 원본 커널의 Shared 사용은 0 bytes.

`vector_add.cu`는 실제 CUDA 예제, `integrated_visuals.py`는 통합 관계도와 애니메이션, `cuda_trace.json`은 512개 출력과 컴파일 자원 정보, `verification.json`은 최종 검증 결과다. 소스 변수와 물리 Register를 1:1로 대응시키지 않는다. Shared에는 실제 데이터 이동 화살표가 없으며, DRAM 사례는 같은 B Load의 다른 가능한 상태다.

최종 산출물: `exports/gpuh11_integrated_191s_longform_final.mp4`. 가로형만 생성하며 191초·30fps·1920×1080·무음·전체 자막이다.

출처: [NVIDIA Advanced Kernel Programming](https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html), [Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html).
