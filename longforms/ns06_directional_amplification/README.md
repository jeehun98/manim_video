# 6막 — 소용돌이와 신경망의 방향별 작용

7개 독립 씬, 사용자 음성 실측 206초(3분26초), 가로형 1920×1080 30fps 무음 영상. 37개 문장의 누적 종료 시각에 맞췄다. 수식 원소 분해보다 3D 관, 회전축의 방향, 입력 원과 출력 타원, 층 사이의 방향 연결을 중심으로 구성한다.

- 준비: python longforms/ns06_directional_amplification/prepare.py
- 미리보기: python longforms/ns06_directional_amplification/build.py --preview --tag timed
- 최종본: python longforms/ns06_directional_amplification/build.py --tag timed
- 씬 교체: build.py --scene N 후 build.py --concat-only
- 음성 실측: voice_timing.json의 basis, ends에 문장별 누적 종료 시각을 넣고 prepare.py 실행
- TTS: tts_script.txt (화면 cue마다 빈 줄)
- 산출물: exports/ns06_act06_206s_timed_1080p30.mp4와 SRT

## 정확성 조건

유체의 Juω는 시간 변화율의 한 항이며 다음 보티시티 자체가 아니다. 점성/외력의 컬을 제외한 방향 비교에서는 S를 고정한다. 보티시티와 전체 Ju를 독립적으로 바꾼다고 하지 않는다. Ju=S+A에서 Aω=0이므로 자체 보티시티 기울어짐을 단순한 국소 강체회전 탓으로 묘사하지 않는다. 비점성·curl f=0일 때 순간 크기 변화는 ωᵀSω로 결정된다.

신경망은 기준 입력 주변의 국소 선형 근사이며 큰 입력 영역의 정확한 타원 변환을 주장하지 않는다. 예시 J=diag(1.8,.5)의 최대 특잇값1.8은 유체의 signed 증감률과 다른 지표다. 각 층의 최대 특잇값을 곱한 값은 일반적으로 상한이며 실제 증폭과 항상 같지 않다. 입력 민감도와 파라미터 Hessian도 구별한다. sources.md와 각 spec.md 참조.
