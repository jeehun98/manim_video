# GPU 연산과 최적화 09 — ReLU는 GPU에서 어떻게 계산될까?

- 학습 목표: ReLU의 수학은 단순한 `max(0,x)`지만, 별도 대형 Tensor 커널에서는 각 원소를 읽고 결과를 쓰는 데이터 이동이 실행 비용의 중심이 될 수 있음을 이해한다.
- 중심 반전: `Compute`가 작아도 `Read → ReLU → Write`가 필요하다. MatMul 결과 `Y`에 ReLU를 별도 적용하면 중간 `Write Y → Read Y`가 필요할 수 있으나, 지원되는 fused epilogue에서는 출력 fragment에 ReLU를 바로 적용하고 최종값만 저장할 수 있다.
- 시리즈 번호: 기존 `gpuops05`는 GEMM의 accumulator와 Bias·ReLU epilogue를 자세히 설명한다. 이 편은 독립 ReLU의 memory traffic에서 출발하는 별도 09화로 둔다.
- 87초, 1080×1920, 30fps, 세로 무음. SRT·TTS 별도. TTS 발음 대본의 공백·문장부호 제외 510글자를 구간별로 세어 8·7·10·7·9·9·10·9·9·9초로 배분했다. 실제 음성 파형과의 일치 여부는 음성 파일이 없어 미검증이다.
- 장면: ReLU 수식과 예시 → 원소별 독립성 → Thread별 할당 → 작은 계산량 → `GPU Memory ↔ SM Compute` → 대형 Tensor의 읽기·쓰기 부담 → MatMul 뒤 중간 `Y` materialization → on-chip 출력 fragment에서 ReLU → Separate/Fused 비교 → 같은 수식, 다른 실행 비용.
- 정확성 경계: ReLU는 각 출력 원소가 자기 입력만 필요하다. 한 Thread가 정확히 한 원소만 맡는다고 고정하지 않고 하나 이상을 맡을 수 있다고 표현한다. GPU Memory는 연산 유닛과 구별하기 위해 외부 Global Memory/HBM의 개념도로 나타낸다. 작은 Tensor에서는 kernel launch overhead 등 다른 비용이 중요할 수 있으므로 언제나 memory-bound라고 단정하지 않는다.
- Fusion은 구현이 지원되고 중간 `Y`를 다른 소비자가 필요로 하지 않는 경우의 개념적 경로다. 실제 물리적 traffic은 캐시·타일링·데이터형·프레임워크에 따라 달라진다. Separate와 Fused의 막대·경로는 정량 측정값이 아닌 개념도다. 최종 출력 `Z`의 write는 남는다.
- 화면·자막·대본은 숫자·영어 원표기, 한글 발음은 `tts_script.txt`에만 둔다.
- 기술 참고: [PyTorch compiler의 pointwise fusion 설명](https://docs.pytorch.org/docs/main/user_guide/torch_compiler/torch.compiler_get_started.html), [NVIDIA CUTLASS의 fused GEMM epilogue](https://docs.nvidia.com/cutlass/latest/media/docs/operators/tutorials/001_gemm_with_fused_epilogue.html), [NVIDIA CUDA Best Practices의 메모리 bandwidth 예시](https://docs.nvidia.com/cuda/pdf/CUDA_C_Best_Practices_Guide.pdf).
