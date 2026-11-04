# CUDA 검증과 설명용 스케줄

## 실제 검증

2026-10-29, CUDA 13.3 / sm_86 / RTX 3060에서 `grid_examples.cu`를 실행했다.

- `vectorAdd<<<12,128>>>`, N=1536의 전체 출력이 `A[i]+B[i]`와 일치했다. 검증 입력은 A[i]=i, B[i]=10i+1이고, C[5]=56, C[133]=1464다.
- 출력 위치 `i=blockIdx.x*128+threadIdx.x`는 Block0 Thread5에서5, Block1 Thread5에서133이다.
- 두 개의 Block 순서 permutation을 CPU에서 적용한 결과가 동일한 GPU 출력과 일치한다. 이것은 독립적인 출력 영역을 쓰는 이 vectorAdd 예제의 성질을 검사하며 실제 GPU 실행 순서를 측정한 결과가 아니다.
- 별도 `imageKernel`을16×16 Thread/Block, 5×4 Block으로 실행했다. 80×64의5120픽셀과 경계 확인용77×61의4697픽셀을 모두 검증했다.
- 영상에서 선택한 이미지 Block(2,1)은 x32…47, y16…31의16×16타일이다. 이 좌표는 SM번호나 칩의 물리 좌표가 아니다.

## 영상의 가정

4SM·SM당 표시 슬롯2개는 배치를 설명하기 위한 예시이며 RTX3060의 SM 수·상주 한계가 아니다. 블록 배치 순서, 완료 시점, 대기 시간은 측정 trace가 아니다. Block5는 논리 Grid와 SM 배치에서 같은 초록색이다. 1D Grid의 Block 번호표는 화면상 줄바꿈해 표시하며, 4×3의2D launch를 뜻하지 않는다.

2D 예제는 별도 kernel 실행이다. 12Block×128Thread의1D launch와20Block×256Thread의2D launch를 하나의 설정으로 섞지 않는다.

## 참고

- [NVIDIA CUDA Programming Guide — Intro to CUDA C++](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/intro-to-cuda-cpp.html): launch 설정, 인덱스, dim3와 경계 검사.
- [NVIDIA CUDA Programming Guide — Programming Model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html): 논리 Grid와 독립적인 Thread Block 실행.

사용자 확정 대본의 문장과 종료 시각은 유지하고, 구현상 가정은 화면 보조 문구로 표시한다.
