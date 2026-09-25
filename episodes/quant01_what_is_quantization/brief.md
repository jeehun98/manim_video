# Quantization 시리즈 1편 제작 기준

- 이 편의 유일한 학습 목표는 `Quantization = 표현 가능한 값의 종류를 제한하는 과정`이라는 직관이다.
- 비트 수는 마지막 다음 편 예고에서만 언급하며, INT8 범위·scale·zero point·대칭성·GPU 성능·Tensor Core·LLM 4bit는 설명하지 않는다.
- 메인 비주얼은 `0.17, 0.21, 0.24, 0.31, 0.36 → 0.25`다. 서로 다른 점이 하나로 합쳐지는 순간을 가장 강하게 강조한다.
- `숫자를 줄인다`는 표현이 숫자의 크기를 줄인다는 뜻으로 오해되지 않도록 `값의 종류를 줄인다`고 명시한다.
- 예시 격자는 개념 설명을 위해 5개만 사용한 장난감 예시이며 실제 INT 형식의 범위를 뜻하지 않는다.
- 공통 컴포넌트 `QuantizationLine`, `ValueDot`은 이후 Quantization Error, Range/Resolution, Outlier 편에서 재사용한다.
- 영상은 52초, 1080×1920, 30fps, 무음 마스터다. `captions.srt`와 `tts_script.txt`를 별도 제공한다.
