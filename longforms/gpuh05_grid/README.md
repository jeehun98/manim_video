# GPU 계층 구조 LEVEL 05 — Grid

사용자 문장 종료 시각178초, 독립씬18개. 세로1080×1920·가로1920×1080, 30fps, 무음·전체 자막.

```powershell
python longforms/gpuh05_grid/build.py --preview
python longforms/gpuh05_grid/build.py
python longforms/gpuh05_grid/verify.py
```

논리 Grid12Block과4SM의 물리 배치를 분리한다. vectorAdd는128Thread/Block·N1536. 2D imageKernel은별도80×64이미지·16×16Thread/Block·5×4Grid. CUDA 실행 결과와 논리 인덱스를 검증하며 스케줄링 애니메이션은 실측trace가 아니다.
