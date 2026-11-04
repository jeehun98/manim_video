# 제작 기준

178초·30fps·독립 완결·9:16/16:9. 사용자 확정 문장과 종료 시각 준수. 음원 미제공, 무음·전체 대본 자막.

Grid는 SM에 포함시키지 않는다. 12Block×128Thread=N1536. Block5 초록색 ID를 두 영역에서 유지. 실행 배치·상주 수·순서는 설명용 가정으로 표시. Block은 SM 하나에서 실행되고 한 SM에는 여러 Block이 상주할 수 있다. Warp 스케줄링과 Block 배치를 혼동하지 않는다. 독립 출력의 vectorAdd에 한해 순서가 달라도 결과 같음을 제시.

2D 예제는 별도 imageKernel, width80,height64, block16×16, grid5×4, 선택Block(2,1). 원래12Block·128Thread 예제와 혼합 금지. 좌표는 논리적 데이터 공간이며 실제 SM 위치가 아니다.

출처: https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/intro-to-cuda-cpp.html (launch·인덱스·dim3) 및 https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html (독립 Block).
