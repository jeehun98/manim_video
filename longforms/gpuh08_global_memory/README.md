# GPU LEVEL 08 — Global Memory & Coalescing

165초 · 14개 독립 씬 · 가로/세로 30fps · 무음·전체 자막.

```powershell
python longforms/gpuh08_global_memory/build.py --preview
python longforms/gpuh08_global_memory/build.py --jobs 4
python longforms/gpuh08_global_memory/verify.py
```

정렬된 32개 float32 Load의 32B 섹터 모델. 유효 데이터 128B를 유지하며 4→32개 섹터로 변경한다. 섹터 수는 실측 DRAM 전송량이나 실행시간이 아니다.

CUDA 검증 결과는 `cuda_validation.txt`와 `cuda_trace.json`에 보관한다. Vector Addition 256개 출력, Stride 1/8 및 역순 접근 각각 32개 출력이 CPU 예상값과 일치한다. `verification.json`은 주소·Lane 대응, 섹터 계산, 영상 규격 검증 결과다.

핵심 시각화는 `global_visuals.py`, 실제 CUDA 예제는 `global_examples.cu`에 있다. 최종 산출물은 `exports/gpuh08_global_memory_165s_shorts_final.mp4` 및 `exports/gpuh08_global_memory_165s_longform_final.mp4`다.

출처: [NVIDIA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html), [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html).
