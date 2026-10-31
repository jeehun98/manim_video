# GPU 계층 구조 LEVEL 06 — Register

현재판 v3는 관계도가 실제 동작에 반응하는 영상이다. Load3·4→Register값7→Store를 코드 강조와 동기화한다. 32/64Register 비교는 상단 할당 영역이8분할→4분할로 변하면서8Block/32Warp→4Block/16Warp를 표시한다. Spill Store/Load도 해당 경로로 값이 이동한다. 아래 설명은 같은 대상의 변화로 연결한다. 출력명: `gpuh06_register_175s_motion_v3_shorts_final.mp4`, `gpuh06_register_175s_motion_v3_longform_final.mp4`. v2는 고정 관계도 중심의 이전판이다.

상단 도식 수정 v2: 도입 9초에서 실행 구조도를 메모리 관계도로 전환한다. SM 내부 Register·Shared·L1, SM 밖 L2·Device DRAM을 구분하고 Thread 2 → Register File 연결을 유지한다. Shared/L1의 물리 자원 공유 가능성을 표시한다. 출력명: `gpuh06_register_175s_memory_v2_shorts_final.mp4`, `gpuh06_register_175s_memory_v2_longform_final.mp4`. 기존 실행 구조 중심 영상은 이전 버전이다.

사용자문장종료시각175초, 독립씬18개. 가로·세로30fps무음·전체자막.

```powershell
python longforms/gpuh06_register/build.py --preview
python longforms/gpuh06_register/build.py
python longforms/gpuh06_register/verify.py
```

Thread2의3+4=7을SMRegisterFile과연결한다. 실제vectorAdd의컴파일로그와32/64Register가상예시를분리한다. Pressure·Spilling·LocalMemory를구분하며성능을단정하지않는다.
