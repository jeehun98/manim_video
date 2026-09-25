# Quantization 시리즈 6편 제작 기준

- 이 편의 유일한 인과관계는 `outlier → range 확대 → scale 증가 → 나머지 값의 resolution 저하`다.
- 눈에 보이는 예시를 위해 고정된 16 levels를 사용한다. 이는 낮은 bit에서 현상이 두드러짐을 보여주는 장난감 예시다.
- Outlier가 없을 때 `−1~1`의 step은 `2/15≈0.1333`이다.
- Outlier 20을 포함한 `−1~20`의 step은 `21/15=1.4`다.
- 넓어진 격자에서 `−1~1` 안의 실제 grid point는 `−1`과 `0.4`뿐이다. 예시 값 `−.8,−.4`는 `−1`, `−.1,.2,.6`은 `.4`로 최근접 매핑된다.
- 문제를 outlier 자체의 오차가 아니라 다른 다수 값에 생기는 collateral resolution loss로 표현한다.
- 실제 tensor 장면은 weight와 activation에 outlier가 생길 수 있다는 수준으로만 설명하며 원인은 다루지 않는다.
- clipping, percentile calibration, SmoothQuant, AWQ, per-group quantization은 제외한다.
- 마지막에는 Channel A/B를 하나의 scale에서 별도 scale로 분리하는 질문만 제시한다.
- 영상은 60초, 1080×1920, 30fps, 무음 마스터다.
