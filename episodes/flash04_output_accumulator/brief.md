# FlashAttention 시리즈 4편 제작 기준

- 핵심은 online softmax 상태 `m, ℓ`에 Attention output state `O`를 결합하는 것이다.
- 예시 score는 3편과 동일한 `[1,3,2]`, `[2,5,4]`, `[0,4,1]`이고 scalar Value는 `[1,2,4]`, `[3,6,8]`, `[2,5,7]`을 사용한다.
- 첫 블록: `m=3`, `ℓ≈1.503`, unnormalized weighted sum `a≈3.607`, normalized output `O=a/ℓ≈2.399`.
- 두 번째 블록: `m=5`, `ℓ≈1.621`, `a≈9.581`, `O≈5.910`.
- 마지막: `m=5`, `ℓ≈2.014`, `a≈11.562`, `O≈5.741`. Full softmax로 직접 계산한 출력도 같다.
- 화면에는 별도의 장기 상태 `a`를 도입하지 않는다. 대신 `old O mass`가 `ℓ_old·exp(m_old−m_new)`에 따라 재조정되고 새 Value 기여와 결합된다는 개념만 보여준다.
- `O` 자체에 단순히 `exp(m_old−m_new)`를 곱한다고 표현하지 않는다. 이전 output의 weight mass를 조정한 뒤 새 `ℓ`로 다시 정규화한다.
- 지나간 score와 weight tile은 시각적으로 제거하고 `m,ℓ,O`만 남겨 1편의 질문에 답한다.
- 5편 예고는 HBM read/write, tiling, on-chip computation, exact output을 한 화면에서 비교하는 것으로 끝낸다.

