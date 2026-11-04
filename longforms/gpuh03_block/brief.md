# GPU 계층 구조 LEVEL 03 — Block

- 사용자 확정 원문 39개 문장·종료 시각 기준 178초. 20개 독립 씬. 음원 미제공으로 무음·전체 내레이션 자막 영상.
- 세로 1080×1920·가로 1920×1080, 30fps. 5340프레임. 미리보기는 360×640·640×360, 15fps.
- 같은 GPU/SM0/Block0 기준 지도를 유지하고 Warp0에서 4 Warp·128 Thread의 협력으로 확대한다. Warp0의 녹색 실행 그룹 표현을 유지한다. Thread와 Shared 주소 128개는 reduction 중에도 자리를 유지한다.
- Shared Memory는 Warp마다 따로 만들지 않고 Block0에 귀속된 한 배열 s[128]로 표현한다. SM의 물리 자원을 Block에 할당한 공간이며 Thread의 개별 물리 메모리가 아니다.
- 입력은 정확한 소정수 float 1…128, 합은8256. 한 Block·정확히128 Thread·128 float에 특화된 커널. 일반적인 다중 Block reduction 또는 임의 길이 구현으로 제시하지 않는다.
- 부분 합계 수는128→64→32→16→8→4→2→1. 전체 Thread 수는 계속128. stride=n이면 Thread0…n−1이 덧셈을 하지만 장벽은 모든128 Thread가 참여한다. __syncthreads는 if 바깥에 둔다.
- 77–102초 기록 완료 순서·장벽 도착은 가능한 진행 상태를 설명하는 개념도다. 실제 GPU 스케줄 trace·하드웨어 사이클 맞춤·실제 데이터 경쟁 실행이 아니다. 대기와 메모리 가시성을 구분한다.
- 127–135초는 첫 합산의 연결 관계를 다시 관찰하는 예시다. Thread0이 기록한 s[0]=1과 Thread64가 기록한 s[64]=65를 같은 Shared 배열에서 읽어66을 만든다. 실제 결과를 되돌린 실행 또는 Warp 직접 전송으로 표현하지 않는다.
- Block 전체는 하나의 SM에 배치된다. 여러 Block 동시 상주는 자원 조건에 따른다. 일반적 __syncthreads 및 __shared__ 범위는 같은 Block이며 특수 cooperative/cluster 기능은 범위 밖이다.
- 코드 패널은 배경·테두리·제목줄, 줄 번호 없이 큰 글자의2–6줄 발췌. 일반적64·256 Thread launch 설정은 개념 비교이며 이 kernel을 그 크기로 실행하지 않는다.
- 실제 GPU에서 원본 blockSum의 출력과 별도 debug kernel의8단계×128 Shared 슬롯을 CPU 모델과 비교한다. debug kernel은 snapshot 보호용 장벽을 추가했으므로 성능·스케줄 trace로 해석하지 않는다.
- 이전 편 복습·다음 편 예고 없음. TTS 원고는 주요 화면 변화마다 빈 줄 구분. 사용자 원문의 종료 시각은 timing.json·자막·영상에 적용한다.
