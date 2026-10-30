# GPU 계층 구조 LEVEL 04 — SM

사용자 문장 종료 시각 기준 178초, 독립 씬 16개. 세로1080×1920·가로1920×1080 / 30fps / 무음·전체 자막.

```powershell
python longforms/gpuh04_sm/build.py --preview
python longforms/gpuh04_sm/build.py
python longforms/gpuh04_sm/verify.py
```

SM 관계도와 상주 Warp 위치를 고정한다. Latency Hiding은 실행 순서를 가정한 개념 애니메이션으로 실제 하드웨어 트레이스가 아니다. Occupancy의 최대32Warp는 가상 예시이며 성능비를 뜻하지 않는다. compute.cu는 실제 CUDA 검증용.
