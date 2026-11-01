# 제작 기준

191초 · 가로1920×1080 · 30fps · 무음·전체자막. 사용자대본과시간확정. 명시제공된회상/최종정리는유지하며임의예고없음.

N=512,Grid4,Block128,4Warp/Block,32Thread/Warp. Block1 Thread5→i133→Warp0 Lane5,선택값A133=4 B133=7 C133=11. 첫4원소A1,2,3,4/B5,6,7,8/C6,8,10,12. Block1→SM1은가정한배치이며실제SM번호·동시성·배치순서는보장되지않음. Warp는32Thread하드웨어실행묶음이며CUDA Launch에서별도크기를지정하는계층이아니다. Shared는원본커널에없고실제데이터이동경로에포함하지않음. 모든변수=고정Register슬롯이아님. CacheHit/Miss/DRAM경로는가정모형. A의L1/B의L2Hit뒤에보이는DRAM은같은B Load의다른상황이며세번째입력이아님. Global Store요청은DRAM기록완료와다름. 512결과채움은동시실행/실제타이밍추적이아님. 자원예산과Coalescing은별도구조설명예시,원본vectorAdd성능실측아님. 논리주소/캐시/DRAM물리공간을동일포함계층에중첩하지않음. 사용자최종요청대로가로형만제작,191초길이유지.
