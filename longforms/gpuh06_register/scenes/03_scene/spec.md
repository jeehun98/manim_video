# Thread 2의 Load · Add · Store

## 목적과 핵심 주장
Thread 2의 Load · Add · Store를 같은GPU구조에서설명한다.

## 앞 장면에서 받은 내용
선택Thread2·Block0·SM0와보라색RegisterFile의정체성을유지.

## TTS와 확정 길이
사용자확정종료시각 32–41초, 9초. 음원미제공.

스레드는 배열 A와 B에서 각각 하나의 값을 읽어옵니다.
그리고 두 값을 더해 중간 결과를 만든 다음, 출력 배열 C에 저장합니다.

## 화면·애니메이션
- 32초: Thread2의 A[2]=3과B[2]=4 읽기
- 36초: 3+4=7 계산
- 39초: C[2]=7 저장

## 화면 텍스트
SM0 / Block0 / Thread2 / Register File. 실제CUDA와개념적컴파일명령패널을명확히구분.

## 시작·종료 상태와 연결
도입9초에서실행집합을메모리관계도로전환한다. 이후상단은SM내Register·Shared·L1과SM밖L2·DeviceDRAM관계를유지하고현재자원만강조한다. 다음씬에서도동일Thread2와SM0를사용하며다음영상예고는없다.

## 정확성
소스변수와물리Register의1:1배치금지. Thread2값3·4·7은실제검증입력과대응. 32/64개는별도가상커널의32bitRegister요구량단순계산,할당단위·다른자원제약무시. 가상SM예산32768/max32Warp예시. Pressure와Spilling은별개. Local은Thread전용범위이며L1/L2캐시와DRAM계층사용,매접근이DRAM까지간다고표현하지않음.출처brief.md.


## v3 동작과 흐름
상단메모리관계도는코드·중간값·요구량의변화와동기화한다. Load의3·4이동, Add의7변환, Store요청의Register→L2이동을동작으로보인다. 가상Register요구량이증가하면Block별할당폭이늘고상주Block/Warp수가줄어든다. Spilling은별도가정의추가메모리접근으로표시한다. 중간설명은동일객체변형으로연결한다.실측캐시경로·실행시간트레이스로주장하지않는다.
