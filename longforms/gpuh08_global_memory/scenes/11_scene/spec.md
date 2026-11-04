# Lane 순서보다 주소 집합

## 주장
Lane 순서보다 주소 집합

## 확정 길이
117–127초. 사용자 문장 종료 시각 기준. 음원 미제공.

## 대본
여기서 중요한 것은 단순히 데이터를 얼마나 많이 읽느냐가 아닙니다.
스레드들이 어떤 주소에 접근하는지가 메모리 시스템의 효율을 바꿀 수 있다는 것입니다.

## 타임라인
- 117초: 역순Lane매핑도동일4섹터
- 122초: 주소집합이효율을결정

## 화면과 연결
상단 SM·Warp·Global 관계도와 하단 32Lane/32Sector 고정 격자의 식별을 유지한다. 주소 변경시 선택칸·연결선·섹터표시가 실제로 이동한다. Register 보라/Shared 청록/Global 황금. 코드 테두리 유지, 줄번호 없음, 자막 영역 분리.

## 정확성
32B 경계에 정렬된 기준 주소, NVIDIA CC6.0+의 32B sector 모델, 32개 활성 Lane, float32 Load 한 명령 기준. byteAddress=base+4*lane*stride, sector=floor(byteAddress/32). stride1은 4섹터, stride8은 32섹터. 유효 데이터 모두128B, sector footprint128B/1024B. 동일 데이터량이지 동일 원소값은 아님. 섹터 수는 실측 DRAM 요청이나 실행시간이 아니다. Global은 논리 주소공간, 일반적인 데이터의 물리 저장은 Device DRAM이며 캐시 적중 가능. Global→Shared→Register 필수 직렬 경로를 만들지 않는다. Bank Conflict는 다른 메커니즘.

## 시작/종료
앞뒤 씬의 같은 주소와 색을 유지하며 다음 편 예고 없이 해당 주장을 완결한다.
