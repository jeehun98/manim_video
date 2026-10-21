# Circuit Tracing · 제작 기준

확정 발화 33문장, 사용자 누적 종료 시각 기준 166초(2:46), 30fps.
일반 1920×1080와 쇼츠 1080×1920를 별도 배치한다. 음원 미제공으로 자막 포함 무음.
사용자 원문은 content.py·tts_script.txt에 유지하며 화면·자막에서는 영문 기술명을 사용한다.

## 질문 표기의 구분

8–13초 발화는 원문 그대로 둔다. 화면에는 콘티에서 권장한 연구형 질문 “댈러스가 속한 주의 주도는?”을 표시한다.
실제 연구 프롬프트에는 Texas를 미리 주지 않는다. 원문에 Texas가 언급되는 점과 화면 질문의 차이를 임의로 같은 문장이라고 설명하지 않는다.

## 여섯 주장과 독립 제작 단위

0–26초: 특징 노드를 발견하는 것과 실제 계산 관계를 아는 것은 다르다.
26–71초: 원래 MLP의 계산을 희소 CLT로 근사해 분석용 대체 모델을 만든다.
71–99초: 특정 입력·목표 출력의 계산상 기여를 그래프로 추적한다.
99–109초: Texas 특징군과 capital 가지, 지름길이 있는 계산 가설.
109–146초: 대체 모델의 가설을 원래 모델의 개입 실험으로 검증하되 완전성은 보장하지 않는다.
146–166초: 출력 관찰 → 특징 → 계산 관계, 정보의 존재와 실제 사용의 차이.

## 과학적·시각적 조건

- 회색 Original Model, 청록 CLT features, 보라 Attribution, 노랑 가설, 주황 개입, 붉은 오차를 고정한다.
- SAE는 h→z→ĥ, Transcoder는 x→z→f̂(x). CLT 특징은 한 층에서 읽고 같은 층 및 이후 층의 MLP 출력을 복원하는 데 기여한다. 과거 층으로 쓰는 화살표를 만들지 않는다.
- 대체 모델은 MLP 계산을 CLT로 바꾼 분석 구조다. Attention의 입력별 패턴 고정/선형화와 근사 오차 항 등 추가 처리가 있다는 점을 표시한다. 전체 원 모델을 그대로 복제했다고 표현하지 않는다.
- 그래프는 특정 입력·출력 logit에 대한 것. 특징 외에도 입력·오차·출력 노드를 포함할 수 있다.
- 간선은 대체 모델에서 계산한 방향성 기여다. 공활성화와 구분하며, 부호·두께는 설명용으로 실측 수치가 아니다.
- Dallas→Texas→Austin만으로 완결된 단일 직렬 경로라고 표시하지 않는다. capital→say capital 가지와 Dallas→say Austin 지름길을 함께 둔다. Texas는 여러 관련 특징을 묶은 특징군이다.
- Texas 억제·California 활성화 개입은 원래 Dallas 입력을 고정한다. Oakland는 California 특징을 식별할 별도 자료였으며, 최종 시험 입력을 Oakland로 교체한 것으로 묘사하지 않는다.
- 개입 전 Austin, 개입 후 Sacramento는 보고된 사례를 단순화한 그림이다. 기여/확률/활성화 수치를 꾸며 넣지 않는다. 각 간선의 인과성이나 전체 계산의 완전한 복원을 단정하지 않는다.
- 제공 마지막 두 발화는 유지하되 다음 편 번호·제목 예고나 별도 복습은 추가하지 않는다.

## 연구 근거

[Ameisen et al. (2025), Circuit Tracing: Revealing Computational Graphs in Language Models](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)

[Lindsey et al. (2025), On the Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html#sec-multi-step-reasoning)

원 논문의 실제 노드·연결·기여도를 재현한 데이터 그래프가 아니라 원리에 대한 단순화 도식이다.

## 검토

미리보기와 최종본의 발화 33개·4,980프레임·자막·레이아웃·CLT 쓰기 방향·Dallas 고정 개입·복수 경로를 검증한다.
