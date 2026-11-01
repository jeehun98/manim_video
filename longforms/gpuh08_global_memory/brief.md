# 제작 기준

165초 · 30fps · 세로1080×1920 / 가로1920×1080 · 무음·전체 자막. 사용자 확정 대본과 종료시각 유지. 추가 복습·다음 편 예고 없음.

32B 경계에 정렬된 기준 주소, NVIDIA CC6.0+의 32B sector 모델, 32개 활성 Lane, float32 Load 한 명령 기준. byteAddress=base+4*lane*stride, sector=floor(byteAddress/32). stride1은 4섹터, stride8은 32섹터. 유효 데이터 모두128B, sector footprint128B/1024B. 동일 데이터량이지 동일 원소값은 아님. 섹터 수는 실측 DRAM 요청이나 실행시간이 아니다. Global은 논리 주소공간, 일반적인 데이터의 물리 저장은 Device DRAM이며 캐시 적중 가능. Global→Shared→Register 필수 직렬 경로를 만들지 않는다. Bank Conflict는 다른 메커니즘.

시각화는 고정된 32Lane와32Sector×8word 격자를 유지한다. 연속→stride8로 주소 화살표와 유효word 선택이 이동하며4→32섹터가 변한다. 모든 요청이DRAM까지 가는 화살표를 피하고캐시적중과저장요청을구분한다. 실제CUDA로vectorAdd와stride1/8/reverse주소예제결과를검증하되성능실측으로표현하지않는다.
