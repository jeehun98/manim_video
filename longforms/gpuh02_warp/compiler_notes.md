# CUDA 소스 경로와 실제 compiler 산출물

2026-10-29, CUDA 13.3, `-arch=sm_86`, RTX 3060, driver 610.88.

`warp_examples.cu`의 벡터 덧셈·조건문·균일 경로 예제 결과는 실제 GPU에서 모두 CPU 참조 결과와 일치했다. `__ballot_sync`로 얻은 0x0000FFFF와 0xFFFF0000은 각 소스 조건을 만족하는 Thread 집합이다. 이를 실제 SASS 명령의 active mask trace로 해석하지 않는다.

`cuobjdump --dump-sass exports/gpuh02_warp_examples.exe`로 `branchExample`의 기계 명령을 확인했다. 해당 환경에서는 조건 `i>=16`을 predicate P0에 저장하고, 먼저 전체에 `+1`을 계산한 뒤 `@!P0` 조건의 덧셈으로 앞 16개 값의 두 배를 계산해 결과를 바꾼다. 소스의 `*2`는 덧셈으로 대체되었다. EXIT 뒤의 BRA는 패딩 부분이며 소스 조건문의 분기 명령이라고 세지 않는다.

따라서 영상의 ‘곱셈 경로 먼저, 덧셈 경로 나중’ 연출은 소스 수준의 두 경로와 참여 Thread를 설명하는 개념도다. 실제 compiler 산출물의 명령 순서·참여 mask와 일치하는 trace 또는 성능 benchmark라고 제시하지 않는다. 발산의 원리는 같은 Warp의 제어 흐름 차이를 기준으로 설명하고, 이 작은 kernel이 실제 장치에서 정확히 두 배 느리다는 주장은 하지 않는다.

이 확인은 고정된 실험 환경에 대한 것이다. 다른 compiler·옵션·GPU에서는 다른 기계 명령이 나올 수 있다. 영상의 원문과 사용자 종료 시각은 수정하지 않고, 코드 패널·마스크·하단 주석에 개념도와 compiler 변환 가능성을 표시한다.
