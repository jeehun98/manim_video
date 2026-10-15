# 업로드용 제목

GPU의 병렬성을 높였는데 왜 느려질까? — Register Spilling과 Occupancy | 계산의 두 얼굴 05

# 영상 설명

GPU에서 더 많은 Warp를 상주시킬 수 있다면 성능도 높아질까요? 반드시 그렇지는 않습니다.

스레드는 계산 중간값을 레지스터에 보관합니다. 하지만 SM의 레지스터는 한정되어 있어, 스레드당 사용량이 늘면 상주할 수 있는 Warp 수가 줄어들 수 있습니다.

GPU는 데이터를 기다리는 Warp 대신 준비된 다른 Warp의 명령을 실행해 지연을 숨길 수 있습니다. 그렇다면 레지스터를 줄여 Occupancy를 높이면 항상 유리할까요?

컴파일러는 제한된 레지스터에 맞춰 일부 중간값을 Local Memory에 저장하고 다시 읽는 코드를 생성할 수 있습니다. 이것이 Register Spilling입니다. 활성 Warp가 늘어도 메모리 접근 역시 늘 수 있는 것입니다.

GEMM도 같은 상충관계를 가집니다. 출력 타일과 스레드별 누산 원소 수가 늘면 재사용에 유리할 수 있지만, 유지해야 하는 중간값과 레지스터 사용도 증가할 수 있습니다. Tile 종류와 매핑에 따라 관계는 달라집니다.

이번 영상은 Register Pressure, Occupancy, Latency Hiding, Register Spilling을 통해 병렬성 최대화와 실행 시간 최소화가 다른 문제임을 살펴봅니다. 교육용 자원 모형을 사용하며 특정 GPU의 성능 실측을 제시하지 않습니다.

계산의 두 얼굴 05 — 같은 수식, 다른 실행 비용

#GPU #CUDA #Occupancy #RegisterSpilling #RegisterPressure #GEMM #GPU최적화 #AICompiler
