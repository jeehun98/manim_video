# 제작 기준

## 2026-10-31 추가 피드백 — 관계도의 실제 변화와 흐름

상단을 정적 길잡이로 두지 않는다. Thread2의Load에서3·4가L2→L1→Register로 이동하고, 같은 계산 값이3+4→7로 바뀐 뒤Store요청에서Register→L2로 움직인다. L2적중은 설명용 가정으로 명시하며실측trace를주장하지않고Store요청을DRAM쓰기완료와동일시하지않는다. 요구량32→64에서한Block의할당폭이2배가되고상주Block/Warp수가줄어드는변화를같은관계도에반영한다. Spilling은별도가정의추가메모리명령경로로움직인다. 단순점멸·반복입자보다코드와원인·결과가대응하는움직임을우선한다. 중간설명도같은객체의변형으로이어붙인다. 대본과175초타이밍유지.

## 2026-10-31 사용자 피드백 — 상단 메모리 관계도

실행 단위 집합을 반복하는 상단 도식을 교체한다. 도입9초에서 기존 실행 구조가 SM 메모리 자원과 GPU 전역 메모리 관계도로 전환된다. Register·Shared·L1은 SM 내부, L2·Device DRAM은 SM 외부로 표시한다. Thread2가 RegisterFile을 사용함을 연결하되 Register→Shared→L1의 필수 직렬 경로를 만들지 않는다. Shared/L1은 용도가 다르지만 물리 자원을 공유할 수 있음을 명시. 이후 메모리편도 이 관계도를 기준으로 현재 자원을 강조한다. 대본·발화시각은 유지한다.

175초·30fps·세로1080×1920·가로1920×1080. 사용자확정대본과발화시각유지. 이번사용자대본의복습문장은명시제공원문이므로유지하며별도복습·예고를추가하지않는다. 무음·전체자막.

선택Thread2는Block0·SM0에속하며입력A[2]=3,B[2]=4,결과C[2]=7. RegisterFile은SM자원으로보라색표시. 지역변수a,b,sum을실제3Register슬롯으로그리지않음.

32/64개는32bitRegister요구량의가상비교,실제vectorAdd로그와분리. 128×32=4096,128×64=8192. 가상SM32768Register/max32Warp,다른제약·할당단위무시시8Block/32Warp대4Block/16Warp. 실제GPU사양아님. Pressure가자동Spilling을뜻하지않으며성능비수치없음.

LocalMemory는Thread전용논리주소공간이다. L1/L2/DRAM경로를별도로표시하되캐시적중가능성을보여준다. Spill명령은소스코드와구분한컴파일개념패널.

출처: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#register-pressure 및 #local-memory, #occupancy.
