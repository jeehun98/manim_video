# 계산의 두 얼굴 03 — GPU는 왜 데이터를 일부러 뒤섞을까?

부제: Swizzled Layout과 Tensor Core.

## 학습 목표

같은 행렬의 값과 논리적 의미를 유지하면서 논리 좌표와 물리 주소의 대응을 바꿀 수 있음을 이해한다. Bank 충돌뿐 아니라 Tensor Core 공급과 Producer/Consumer 사이의 변환까지 포함한 전체 비용으로 layout을 선택한다.

## 제작 기준

- 콘티 구간 기준 105초, 8장면. 종료 12,25,39,51,68,82,96,105초.
- 1080×1920·30fps, 미리보기 360×640. 무음, 별도 TTS 원고·SRT. 실제 음원 미제공으로 문장 시각은 추정이다.
- 이전 편 복습·요약과 다음 편 예고를 넣지 않는다. 첫 질문과 전체 비용 결론으로 완결한다.
- 실제 성능 수치 없이 주소 대응을 시각화한다. 비용 막대는 단위 없는 가상 예시다.

## 기술 조건과 검산

1. 도입 4×4 값 0–15. 물리 열 = 논리 행 XOR 논리 열. 각 행의 값을 해당 위치에 저장하면 행 우선 물리 저장 순서는 `[0,1,2,3,5,4,7,6,10,11,8,9,15,14,13,12]`가 된다. 논리적 A의 값이나 원소 순서를 바꾸는 연산이 아니다.
2. 본문은 실제 GPU가 아닌 교육용 8-bank 모형이다. 한 원소가 한 bank 단위, 행 길이 8, bank=원소주소 mod 8. 일반 주소 8r+c에서 같은 열은 같은 bank, XOR 주소 8r+(r XOR c)에서 같은 열은 8개 bank로 분산된다. N=8, r,c는 0–7, offset=0이다.
3. 8×8 그림의 숫자는 논리적 열 번호이며 화면의 위치가 물리적 열이다. 논리 열 0의 8개 원소가 swizzle 후 대각선으로 배치되는 것을 추적한다. XOR는 행마다 전단사이고 추가 저장 칸은 없다.
4. Swizzle은 좌표와 주소의 매핑이다. 애니메이션은 두 저장 배치를 비교하는 표현이며 반드시 별도 복사 커널이 존재한다는 뜻이 아니다. Producer가 해당 배치에 처음부터 저장할 수도 있다.
5. A[3,5]=29인 값 예시: 일반 원소주소 29, XOR 주소 30. 둘 다 같은 논리 원소를 읽는다. 행 3의 XOR 물리 값은 `[27,26,25,24,31,30,29,28]`이다.
6. Tensor Core 공급은 아키텍처·MMA 명령에 따라 다르다. Shared→Register Fragment→MMA와 Shared operand를 SMEM descriptor로 지정하는 WGMMA를 대안 예시로 표시한다. Descriptor를 행렬 데이터 자체로 표현하거나 모든 Tensor Core가 Shared를 직접 읽는다고 일반화하지 않는다. 구체적인 실제 fragment 비트 배열을 재현하는 장면은 아니다.
7. 실제 swizzle은 dtype·접근 폭·tile·명령과 맞아야 한다. 단순 8×8 XOR가 모든 GPU 명령의 모든 bank conflict를 제거한다고 주장하지 않는다.
8. Producer/Consumer는 앞선/다음 연산 또는 커널의 추상적 단계다. Layout Conversion은 Global 복사뿐 아니라 Register 교환, Shared 재배치 등일 수도 있다. Producer 출력 조정은 가능할 때의 선택이며 그 자체의 비용도 고려한다.
9. 비용 식은 직렬 실행의 단순 모형이다. P의 `(2,4,3)` 합 9와 Q의 `(3,0,3)` 합 6은 가상값이며 실측·보편적 속도 관계가 아니다. 실제 실행은 overlap·동기화·자원 제한에 따라 단순 합으로 설명되지 않을 수 있다.

## 장면 구성

| 시간 | 내용 |
|---|---|
| 0–12 | 4×4 일반 저장과 XOR 저장, 같은 논리적 행렬 |
| 12–25 | 교육용 8-bank에서 같은 열 접근 충돌 |
| 25–39 | 8×8 XOR 주소 매핑, 같은 열의 bank 분산 |
| 39–51 | 같은 A[3,5]가 다른 물리 주소에, 값 보존 |
| 51–68 | Tensor Core operand 공급 방식과 layout 제약 |
| 68–82 | Producer → Conversion → Consumer / 출력 layout 조정 |
| 82–96 | 세 비용을 합한 가상 막대 비교 |
| 96–105 | 같은 텐서, 다른 layout, 다른 전체 비용 |

## 출처

- [NVIDIA CuTe Swizzle](https://docs.nvidia.com/cutlass/4.4.0/media/docs/pythonDSL/cute_dsl_api/cute.html): 비트 주소 재배열의 추상화.
- [CUTLASS Implicit GEMM](https://github.com/NVIDIA/cutlass/blob/main/media/docs/cpp/implicit_gemm_convolution.md): permuted Shared layout과 ldmatrix/Tensor Core 데이터 공급.
- [CUTLASS GEMM API](https://github.com/NVIDIA/cutlass/blob/main/media/docs/cpp/gemm_api.md): register fragment와 shared tile 경로.
- [Warpgroup MMA Programming](https://docs.nvidia.com/cutlass/4.5.2/media/docs/pythonDSL/mma_docs/wgmma_programming.html): shared-memory descriptor 또는 register A operand.

## 검증

모든 행의 XOR 전단사, 모든 열의 bank 분산, 선택 원소 값 보존, 가상 비용 합계를 검산한다. 누적 시간 gate와 미리보기·최종 주요 화면의 겹침·자막·프레임 범위를 확인한다. 실제 음원 싱크와 GPU 성능은 별도다.

### 2026-10-14 제작 검증 결과

- Manim 0.21.0, FFmpeg, Malgun Gothic 확인. 미리보기와 최종 렌더 완료.
- 최종 1080×1920·30fps 설정·3,150프레임·약 105.000초. 105초 목표와 1프레임 이내 차이. 무음.
- 미리보기 10/24/37/49/65/80/94/104초 확인. 카드의 텍스트 세로 늘어남을 수정하고 65/80초 재확인. 최종 37/65/94초 확인.
- 모든 누적 시각 gate 통과. 4×4 및 8×8의 행별 XOR 전단사와 열별 bank 분산, A[3,5] 값/주소, 가상 비용 합계를 검산했다.
- 실제 음원 발화 경계 및 GPU 성능 실측은 미실시다.

## 2026-10-15 사용자 발화 경계 적용 — 현재 기준

- 현재 영상은 92초다. 위 105초 기준은 최초 제작 이력이다.
- 문장 종료 시각: 4,9,12,17,20,24,31,36,41,45,50,55,59,65,69,74,80,85,92초.
- 장면 종료 시각: 9,20,36,45,59,69,80,92초. 전체 배속 없이 Scene.time 누적 목표와 대기 시간을 조정한다. 애니메이션 이동 시간과 원고 내용은 유지한다.
- SRT와 timing.json은 같은 사용자 경계를 적용한다. 실제 음원 파일 대조는 미실시다.

### 92초 수정본 검증 결과

미리보기·최종 렌더 완료. 1080×1920, 30fps 설정, 2,760프레임, 92.000초로 목표 92초와 1프레임 이내 차이. 무음. 사용자 제공 19개 문장 종료 시각과 SRT·timing.json 일치, 모든 누적 시간 gate 통과. 미리보기 34/57/78초 및 최종 78초 확인. 실제 음원 파일 대조는 미실시.
