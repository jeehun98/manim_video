# Register와 선택적인 Shared Memory

## 확정 대본/길이
72–81초,사용자문장종료시각.음원미제공.

이 과정에서 스레드마다 필요한 계산값은 레지스터에 보관될 수 있습니다.
같은 블록의 스레드들이 데이터를 함께 사용해야 한다면 공유 메모리를 활용할 수도 있습니다.

## 화면타임라인
- 72초: Register Thread별할당
- 76초: Shared는선택적협력,이커널은미사용

## 지속요소
상단의Grid·선택Block1 Thread5·SM1·Cache·Controller·DRAM위치를유지한다. 논리조직은왼쪽,물리하드웨어는오른쪽으로분리한다. 하단확대도와코드는상단의요청·값이동에맞춘다.

## 정확성
N=512,Grid4,Block128,4Warp/Block,32Thread/Warp. Block1 Thread5→i133→Warp0 Lane5,選択値A133=4 B133=7 C133=11. 첫4원소A1,2,3,4/B5,6,7,8/C6,8,10,12. Block1→SM1은가정한배치이며실제SM번호·동시성·배치순서는보장되지않음. Warp는32Thread하드웨어실행묶음이며CUDA Launch에서별도크기를지정하는계층이아니다. Shared는원본커널에없고실제데이터이동경로에포함하지않음. 모든변수=고정Register슬롯이아님. CacheHit/Miss/DRAM경로는가정모형. A의L1/B의L2Hit뒤에보이는DRAM은같은B Load의다른상황이며세번째입력이아님. Global Store요청은DRAM기록완료와다름. 512결과채움은동시실행/실제타이밍추적이아님. 자원예산과Coalescing은별도구조설명예시,원본vectorAdd성능실측아님. 논리주소/캐시/DRAM물리공간을동일포함계층에중첩하지않음. 사용자최종요청대로가로형만제작,191초길이유지.
