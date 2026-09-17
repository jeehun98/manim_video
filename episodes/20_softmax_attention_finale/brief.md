# Softmax 09 — Attention의 비중을 결정하는 함수

152초 · 세로 FHD · 30fps · 무음 · 시리즈 완결.

## 대본 검토

[1,2,5]의 Softmax는 [0.0171478,0.0466126,0.9362396]. 소수 둘째 자리 반올림 [.02,.05,.94]는 합이 1.01이 되므로 화면과 대본에서는 [.017,.047,.936]을 사용하고 반올림 명시. 차이가 아니라 비율이 지수적으로 변한다고 설명. 다른 점수 고정 시 공통 분모 증가로 다른 비중 감소.

## Attention 범위

표준 scaled dot-product attention의 한 Query, 한 head 예시. sᵢ=q·kᵢ/√dₖ로 점수가 스케일링된 이후를 [1,2,5]로 가정. 보이는 세 Key는 모두 허용된 항목이며 dropout 없는 기본 가중합. Key와 같은 인덱스의 Value를 섞는다. 점수는 학습된 관련성 척도이며 의미적 정답을 보장하는 것은 아니다.

## 그래프

설명용 V₁=(-2,-1), V₂=(2,-1), V₃=(0,2). 출력=ΣpᵢVᵢ를 흰 점과 벡터로 표시. 첫 점수 1→6에서 경쟁 변화. 원래 점수로 돌아와 p₃/p₁=e⁴≈54.6을 설명. [2,2,2]에서는 동일 가중치와 원점인 평균을 표시. 실제 Value는 고차원 벡터일 수 있다.

## 근거

[PyTorch 공식 scaled_dot_product_attention 문서](https://docs.pytorch.org/docs/main/generated/torch.nn.functional.scaled_dot_product_attention.html): 스케일된 Query-Key 점수에 Softmax를 적용하고 Value 행렬과 곱하는 구성.

## 파일

음성 없이 발화 길이 기준 추정. narration.md, tts_script.txt, captions.srt 제공.

`python scripts/render.py 20 --preview`

`python scripts/render.py 20`
