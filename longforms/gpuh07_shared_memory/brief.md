# 제작 기준

160초·30fps·세로1080×1920·가로1920×1080. 사용자확정대본및시각유지. 무음·전체자막. 복습문장은이번에명시제공된원문을유지하며추가복습·다음편예고없음.

Thread5녹색,Thread6주황,Shared청록,Register보라. Shared는SM물리자원/Block별논리할당을분리. 실제관계도의기록·대기·해제·이웃읽기·Tile재사용·자원점유·Bank경로가변한다. 소스코드와상태변화동기화.

안전한neighborRead만실제CUDA로검증. unsafe화면은미기록값?이며잘못된특정숫자를보장하지않음. 배리어는동시발행이아닌모든참여자의도착과가시성. 다른Block공유배열은분리.

별도GEMM4×4/T2예제의선택C2×2출력은90,100,202,228. Global요청원소수32→16은캐시/DRAM트랜잭션이나실측성능아님. 예제의그리드·Thread수와neighborRead128을섞지않는다. Bank주소는32bitword%32,4활성Lane만확대,동일주소broadcast는예외. 용량64KiB와8/16KiB요구량은가상예시,neighborRead의512B와구분.

출처: NVIDIA CUDA Best Practices Shared Memory/Bank Conflicts 및 CUDA Programming Guide synchronization.
