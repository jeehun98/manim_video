# Quantization 시리즈 5편 제작 기준

- 학습 목표는 `Quantization Error = 원래 값이 가장 가까운 격자로 이동하며 생기는 차이`다.
- 반드시 한 값의 snap, 여러 값의 many-to-one 합류, 촘촘한/거친 격자의 이동 거리 차이를 모두 보여준다.
- Error의 부호는 `e=x̂−x`로 정의한다. 다른 부호 convention도 가능하지만 영상 내부에서는 이 정의로 고정한다.
- `0.43→0.45` 예시의 error는 `+0.02`다.
- Many-to-one 예시는 step `0.10`, 대표값 `0.50`의 bin 내부 값 `0.46,0.48,0.49,0.51,0.53`을 사용한다. 모두 최근접 반올림으로 0.50에 매핑된다.
- `|e|≤Δ/2`는 clipping이 없고 가장 가까운 격자로 반올림하는 값에 대한 bound임을 화면과 내레이션에서 명시한다.
- 8bit와 4bit 비교는 동일 범위 `0~1`에서 입력 `0.43`을 사용한다. 최근접 값은 각각 약 `0.431`, `0.400`이다.
- clipping error, saturation, outlier, MSE, calibration, stochastic rounding, quantization noise 해석은 제외한다.
- 영상은 60초, 1080×1920, 30fps, 무음 마스터다.
