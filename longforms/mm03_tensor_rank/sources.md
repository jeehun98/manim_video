# 수학적 근거와 검증 범위

- S. Winograd, On multiplication of 2×2 matrices, Linear Algebra and its Applications 4 (1971), 381–388: https://www.sciencedirect.com/science/article/pii/0024379571900097
- Tensor Rank and Complexity (연구 강의 노트): https://arxiv.org/abs/2004.01492

첫 논문의 공개 초록에 제시된 2×2 최소 7곱 결과를 별도 하한 정리로 인용한다. 영상에서 하한 증명 전체를 제공하지 않는다.

verify_tensor.py는 표준 8항과 Strassen 7항의 64개 계수를 정수 산술로 비교한다. 이는 모든 입력에 대한 상한 항등식 검증이다. 숫자 예제의 출력과 개별 기여분도 별도로 확인한다. 고정 계수의 덧셈·곱셈 비용과 실제 실행시간은 랭크 수와 구분한다.
