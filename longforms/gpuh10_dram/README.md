# GPU LEVEL 10 — Memory Controller & DRAM

164초 · 독립 씬14개 · 가로/세로 30fps · 무음·전체 자막.

```powershell
python longforms/gpuh10_dram/build.py --preview
python longforms/gpuh10_dram/build.py --jobs 4
python longforms/gpuh10_dram/verify.py
```

상태 모형은 설명용이며 실제 캐시/DRAM 추적이나 타이밍 측정이 아니다.

`dram_visuals.py`는 화면과 애니메이션, `dram_model.py`는 단일 Bank의 행 상태 전이, `dram_examples.cu`는 실행 가능한 CUDA 예제다. CUDA 출력값은 `cuda_trace.json`과 `cuda_validation.txt`, 최종 검증은 `verification.json`에 기록한다.

모형은 닫힌 Bank→ACTIVATE/READ, 동일 Row→READ, 다른 열린 Row→PRECHARGE/ACTIVATE/READ를 구분한다. 각 Bank에 동시에 한 행만 열리며, 실제 물리 주소 매핑·Refresh·Auto-precharge·제품별 타이밍은 재현하지 않는다.

최종 영상은 `exports/gpuh10_dram_164s_shorts_final.mp4`와 `exports/gpuh10_dram_164s_longform_final.mp4`다.

기술출처: [Micron HBM2E 동작](https://assets.micron.com/adobe/assets/urn%3Aaaid%3Aaem%3A275edf31-79e3-4b6c-8bbd-a233babe9281/renditions/original/as/micron-hbm2e-memory-wp.pdf), [Micron HBM](https://www.micron.com/products/memory/hbm), [Micron Graphics Memory](https://www.micron.com/products/memory/graphics-memory).
